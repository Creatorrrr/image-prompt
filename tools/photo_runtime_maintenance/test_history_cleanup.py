"""Recovery must never overwrite work or publish a partial/tampered tree."""
import hashlib
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock
import zipfile

import history_proof
import history_restore
import history_checks
import history_gc
from deferred_gc import rollback
from history_restore import restore_zip
from deferred_restore import publish_exclusive
import state


class HistoryRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.archive=self.root/'recovery.zip'

    def pack(self,members,mode=stat.S_IFREG|0o640):
        seal={'files':{}}
        with zipfile.ZipFile(self.archive,'w') as z:
            for name,raw in members:
                info=zipfile.ZipInfo(name);info.external_attr=mode<<16;z.writestr(info,raw)
                seal['files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mode':mode&0o777}
        seal['archive_sha256']=state.sha(self.archive)
        return seal

    def test_original_bytes_permissions_and_independent_inode(self):
        seal=self.pack([('tests/__pycache__/old.pyc',b'original')])
        out=restore_zip(self.archive,seal,self.root/'new')/'tests/__pycache__/old.pyc'
        self.assertEqual(out.read_bytes(),b'original');self.assertEqual(out.stat().st_mode&0o777,0o640)
        self.assertNotEqual(out.stat().st_ino,self.archive.stat().st_ino)

    def test_existing_destination_and_symlink_are_preserved(self):
        seal=self.pack([('a',b'original')]);target=self.root/'existing';target.mkdir();(target/'work').write_bytes(b'keep')
        with self.assertRaises(FileExistsError):restore_zip(self.archive,seal,target)
        alias=self.root/'alias';alias.symlink_to(target)
        with self.assertRaises(FileExistsError):restore_zip(self.archive,seal,alias)
        self.assertEqual((target/'work').read_bytes(),b'keep')

    def test_traversal_and_absolute_names_rejected(self):
        for name in ('../escape','/absolute'):
            seal=self.pack([(name,b'no')])
            with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')
            self.assertFalse((self.root/'new').exists())

    def test_duplicate_and_case_colliding_names_rejected(self):
        for names in ([('a',b'one'),('a',b'two')],[('A',b'one'),('a',b'two')]):
            seal=self.pack(names)
            with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')

    def test_symlink_archive_member_rejected(self):
        seal=self.pack([('link',b'/outside')],stat.S_IFLNK|0o777)
        with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')

    def test_archive_tamper_and_partial_member_tamper_publish_nothing(self):
        seal=self.pack([('a',b'one'),('b',b'two')]);seal['files']['b']['sha256']='0'*64
        with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')
        self.assertFalse((self.root/'new').exists())
        seal=self.pack([('a',b'one')]);self.archive.write_bytes(self.archive.read_bytes()+b'tamper')
        with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')

    def test_missing_member_rejected(self):
        seal=self.pack([('a',b'one')]);seal['files']['missing']=dict(seal['files']['a'])
        with self.assertRaises(ValueError):restore_zip(self.archive,seal,self.root/'new')

    def test_atomic_publication_race_keeps_other_writer(self):
        seal=self.pack([('a',b'original')]);target=self.root/'new'
        def race(source,destination):
            target.mkdir();(target/'work').write_bytes(b'new work');publish_exclusive(source,destination)
        with mock.patch.object(history_restore,'publish_exclusive',side_effect=race):
            with self.assertRaises(OSError):restore_zip(self.archive,seal,target)
        self.assertEqual((target/'work').read_bytes(),b'new work')

    def test_zip_recovery_does_not_require_git_or_matching_compilers(self):
        seal=self.pack([('a',b'original')])
        with mock.patch.object(history_proof,'git',side_effect=RuntimeError('Git unavailable')):
            with mock.patch.object(history_proof,'BINARIES',{}):
                restored=restore_zip(self.archive,seal,self.root/'new')
        self.assertEqual((restored/'a').read_bytes(),b'original')

    def test_failed_git_compile_never_publishes_partial_tree(self):
        row={'path':'old/cache.pyc','git_blob':'0'*40,'source_sha256':'0'*64}
        with mock.patch.object(history_proof,'git',side_effect=RuntimeError('no object; no fetch')):
            with self.assertRaises(RuntimeError):history_proof.compile_rows([row],self.root/'new')
        self.assertFalse((self.root/'new').exists())

    def test_failed_suite_evidence_is_not_overwritten(self):
        output=self.root/'OPERATING-old.json';output.write_bytes(b'original failure')
        with mock.patch.object(history_checks,'E',self.root):
            with self.assertRaises(FileExistsError):history_checks.suite('old')
        self.assertEqual(output.read_bytes(),b'original failure')

    def test_single_check_refuses_existing_output(self):
        output=self.root/'NATIVE-old.json';output.write_bytes(b'original evidence')
        with mock.patch.object(history_checks,'E',self.root):
            with self.assertRaises(FileExistsError):history_checks.run_check('NATIVE','old')
        self.assertEqual(output.read_bytes(),b'original evidence')

    def test_rollback_never_overwrites_concurrent_work(self):
        original=self.root/'original';saved=self.root/'saved'
        original.write_bytes(b'new user work');saved.write_bytes(b'old cache')
        self.assertEqual(rollback([(original,saved)]),[str(original)])
        self.assertEqual(original.read_bytes(),b'new user work');self.assertEqual(saved.read_bytes(),b'old cache')

    def test_rollback_preserves_original_inode(self):
        original=self.root/'original';saved=self.root/'saved';saved.write_bytes(b'old cache');inode=saved.stat().st_ino
        self.assertEqual(rollback([(original,saved)]),[]);self.assertEqual(original.stat().st_ino,inode)

    def test_unowned_quarantine_member_prevents_finalization(self):
        folder=self.root/'quarantine';folder.mkdir();(folder/'cache').write_bytes(b'old')
        row={'path':'cache','before':state.stamp(folder/'cache')}
        (folder/'new-user-work').write_bytes(b'keep')
        with self.assertRaises(ValueError):history_gc.validate_quarantine(folder,[row])
        self.assertEqual((folder/'new-user-work').read_bytes(),b'keep')

    def test_source_changed_since_freeze_is_deferred(self):
        root=self.root/'repo';root.mkdir();(root/'cache').write_bytes(b'old');(root/'source.py').write_bytes(b'old source')
        row={'path':'cache','analysis':{'source':'source.py'},'preflight':'READY',
            'before':state.stamp(root/'cache'),'source_before':state.stamp(root/'source.py')}
        (root/'source.py').write_bytes(b'new user work')
        with mock.patch.object(history_gc,'ROOT',root):
            with self.assertRaises(ValueError):history_gc.preflight(row)
        self.assertEqual((root/'source.py').read_bytes(),b'new user work')

    def test_unowned_empty_quarantine_directory_is_preserved(self):
        folder=self.root/'quarantine';folder.mkdir();(folder/'cache').write_bytes(b'old')
        row={'path':'cache','before':state.stamp(folder/'cache')};(folder/'user-directory').mkdir()
        with self.assertRaises(ValueError):history_gc.validate_quarantine(folder,[row])
        self.assertTrue((folder/'user-directory').is_dir())

    def test_failed_native_gate_prevents_final_deletion(self):
        state.write(self.root/'NATIVE-final.json',{'status':'FAIL','test_count':70})
        state.write(self.root/'OFFLINE-FINAL.json',{'status':'PASS','files':228})
        kept=self.root/'cache';kept.write_bytes(b'original')
        with mock.patch.object(history_gc,'E',self.root):
            with self.assertRaises(ValueError):history_gc.finalize()
        self.assertEqual(kept.read_bytes(),b'original');self.assertFalse((self.root/'FINALIZE.LOCK').exists())

    def test_incomplete_recovery_gate_prevents_final_deletion(self):
        state.write(self.root/'NATIVE-final.json',{'status':'PASS','test_count':70})
        state.write(self.root/'OFFLINE-FINAL.json',{'status':'PASS','files':227})
        with mock.patch.object(history_gc,'E',self.root):
            with self.assertRaises(ValueError):history_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())

    def test_exact_closed_quarantine_can_be_removed(self):
        folder=self.root/'q';(folder/'parent').mkdir(parents=True);p=folder/'parent/cache';p.write_bytes(b'old')
        row={'path':'parent/cache','before':state.stamp(p)};deleted=[]
        kept=self.root/'user-work';kept.write_bytes(b'keep')
        history_gc.delete_verified(folder,[row],deleted.append)
        self.assertEqual(deleted,['parent/cache']);self.assertFalse(folder.exists());self.assertEqual(kept.read_bytes(),b'keep')

    def test_final_deletion_refuses_quarantine_with_new_user_file(self):
        folder=self.root/'q';folder.mkdir();p=folder/'cache';p.write_bytes(b'old')
        row={'path':'cache','before':state.stamp(p)};(folder/'new-user-work').write_bytes(b'keep')
        with self.assertRaises(ValueError):history_gc.delete_verified(folder,[row],lambda p:None)
        self.assertEqual(p.read_bytes(),b'old');self.assertEqual((folder/'new-user-work').read_bytes(),b'keep')

    def test_incomplete_independent_zip_gate_prevents_deletion(self):
        for name,value in [('NATIVE-final.json',{'status':'PASS','test_count':70}),
            ('OFFLINE-FINAL.json',{'status':'PASS','files':228}),('SUITE-absent-B.json',{'status':'PASS'}),
            ('SAFETY-07-FINAL.json',{'status':'PASS'}),('ZIP-INDEPENDENT.json',{'status':'PASS','files':227})]:
            state.write(self.root/name,value)
        with mock.patch.object(history_gc,'E',self.root):
            with self.assertRaises(ValueError):history_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())


if __name__=='__main__':unittest.main()
