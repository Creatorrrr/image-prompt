"""Additional fail-closed checks for the bounded pytest compiler and recovery wrapper."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock

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


if __name__=='__main__':unittest.main()
