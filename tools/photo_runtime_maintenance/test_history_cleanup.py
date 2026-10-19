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


if __name__=='__main__':unittest.main()
