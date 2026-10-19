"""Additional fail-closed checks for the bounded pytest compiler and recovery wrapper."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import stat
import zipfile

import pytest_checks
import pytest_gc
import pytest_proof
import pytest_restore
from pytest_restore import restore_zip
import state


class PytestCleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_more_than_65_members_rejected_before_archive_read(self):
        seal={'files':{str(i):{'bytes':1} for i in range(66)}}
        with self.assertRaises(ValueError):restore_zip(self.root/'missing.zip',seal,self.root/'out')
        self.assertFalse((self.root/'out').exists())

    def test_oversize_original_byte_budget_rejected(self):
        with self.assertRaises(ValueError):restore_zip(self.root/'missing.zip',{'files':{'a':{'bytes':807567}}},self.root/'out')

    def test_pinned_dependency_drift_refuses_compile(self):
        dep=self.root/'dependency.py';dep.write_bytes(b'original');lock={'files':{str(dep):state.sha(dep)}}
        dep.write_bytes(b'changed')
        with self.assertRaises(ValueError):pytest_proof.check_toolchain(lock)

    def test_missing_source_blob_never_publishes_partial_recompile(self):
        row={'path':'tests/cache.pyc','git_blob':'0'*40,'source_sha256':'0'*64}
        with mock.patch.object(pytest_proof,'git',side_effect=RuntimeError('missing local object; no fetch')):
            with self.assertRaises(RuntimeError):pytest_proof.compile_rows([row],self.root/'new',toolchain={'files':{}})
        self.assertFalse((self.root/'new').exists())

    def test_existing_recompile_destination_preserves_work(self):
        out=self.root/'existing';out.mkdir();(out/'work').write_bytes(b'keep')
        with self.assertRaises(FileExistsError):pytest_proof.compile_rows([],out)
        self.assertEqual((out/'work').read_bytes(),b'keep')

    def test_unsafe_recompile_path_rejected_before_source_read(self):
        with self.assertRaises(ValueError):pytest_proof.compile_rows([{'path':'../escape','git_blob':'0'*40}],self.root/'new',toolchain={'files':{}})
        self.assertFalse((self.root/'new').exists())

    def test_changed_source_lock_is_rejected(self):
        path=self.root/'RESTORE-LOCK.json.gz';state.write(path,{'rows':[]})
        state.write(self.root/'TOOLCHAIN.json',{'files':{}})
        state.write(self.root/'STAGE02.json',{'lock_sha256':state.sha(path),'toolchain_sha256':state.sha(self.root/'TOOLCHAIN.json')})
        path.write_bytes(b'tampered')
        with mock.patch.object(pytest_proof,'E',self.root):
            with self.assertRaises(ValueError):pytest_proof.load_lock()

    def test_changed_zip_seal_is_rejected(self):
        seal=self.root/'seal.json';seal.write_bytes(b'original')
        state.write(self.root/'STAGE03.json',{'seal_sha256':state.sha(seal)})
        seal.write_bytes(b'tampered')
        with mock.patch.object(pytest_restore,'E',self.root),mock.patch.object(pytest_restore,'SEAL',seal):
            with self.assertRaises(ValueError):pytest_restore.load_seal()

    def test_unicode_normalization_collision_never_publishes(self):
        archive=self.root/'collision.zip';seal={'files':{}}
        with zipfile.ZipFile(archive,'w') as z:
            for name in ('\u00e9.pyc','e\u0301.pyc'):
                info=zipfile.ZipInfo(name);info.external_attr=(stat.S_IFREG|0o640)<<16
                z.writestr(info,b'old');seal['files'][name]={'bytes':3,'sha256':hashlib.sha256(b'old').hexdigest(),'mode':0o640}
        seal['archive_sha256']=state.sha(archive)
        with self.assertRaises(ValueError):restore_zip(archive,seal,self.root/'new')
        self.assertFalse((self.root/'new').exists())

    def test_regression_worker_preserves_previous_failure_evidence(self):
        evidence=self.root/'OPERATING-old.json';evidence.write_bytes(b'previous failure')
        with mock.patch.object(pytest_checks,'E',self.root):
            with self.assertRaises(FileExistsError):pytest_checks.run_check('OPERATING','old')
        self.assertEqual(evidence.read_bytes(),b'previous failure')

    def test_gc_source_change_defers_without_touching_work(self):
        (self.root/'cache').write_bytes(b'old');(self.root/'source.py').write_bytes(b'old source')
        row={'path':'cache','analysis':{'source':'source.py'},'preflight':'READY',
            'before':state.stamp(self.root/'cache'),'source_before':state.stamp(self.root/'source.py')}
        (self.root/'source.py').write_bytes(b'new work')
        with mock.patch.object(pytest_gc,'ROOT',self.root):
            with self.assertRaises(ValueError):pytest_gc.preflight(row)
        self.assertEqual((self.root/'source.py').read_bytes(),b'new work')

    def test_pytest_quarantine_unknown_file_prevents_deletion(self):
        q=self.root/'q';q.mkdir();(q/'cache').write_bytes(b'old')
        row={'path':'cache','before':state.stamp(q/'cache')};(q/'user-work').write_bytes(b'keep')
        with self.assertRaises(ValueError):pytest_gc.delete_verified(q,[row],lambda _:None)
        self.assertEqual((q/'cache').read_bytes(),b'old');self.assertEqual((q/'user-work').read_bytes(),b'keep')

    def test_pytest_native_failure_blocks_finalization_before_lock(self):
        state.write(self.root/'NATIVE-final.json',{'status':'FAIL','test_count':70})
        state.write(self.root/'OFFLINE-FINAL.json',{'status':'PASS','files':65})
        with mock.patch.object(pytest_gc,'E',self.root):
            with self.assertRaises(ValueError):pytest_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())

    def test_pytest_skipped_native_test_does_not_qualify_deletion(self):
        state.write(self.root/'NATIVE-final.json',{'status':'PASS','test_count':70,'stderr':'OK (skipped=1)'})
        state.write(self.root/'OFFLINE-FINAL.json',{'status':'PASS','files':65})
        with mock.patch.object(pytest_gc,'E',self.root):
            with self.assertRaises(ValueError):pytest_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())

    def test_pytest_incomplete_offline_recovery_blocks_deletion(self):
        state.write(self.root/'NATIVE-final.json',{'status':'PASS','test_count':70})
        state.write(self.root/'OFFLINE-FINAL.json',{'status':'PASS','files':64})
        with mock.patch.object(pytest_gc,'E',self.root):
            with self.assertRaises(ValueError):pytest_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())

    def test_pytest_incomplete_independent_zip_blocks_deletion(self):
        for name,value in [('NATIVE-final.json',{'status':'PASS','test_count':70}),
            ('OFFLINE-FINAL.json',{'status':'PASS','files':65}),('SUITE-absent-B.json',{'status':'PASS'}),
            ('SAFETY-07-FINAL.json',{'status':'PASS','tests':53,'failures':0,'errors':0}),('ZIP-INDEPENDENT.json',{'status':'PASS','files':64})]:
            state.write(self.root/name,value)
        with mock.patch.object(pytest_gc,'E',self.root):
            with self.assertRaises(ValueError):pytest_gc.finalize()
        self.assertFalse((self.root/'FINALIZE.LOCK').exists())


if __name__=='__main__':unittest.main()
