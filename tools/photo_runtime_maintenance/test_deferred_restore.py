"""Destructive-cleanup boundaries: atomic recovery, tamper and path rejection."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from deferred_restore import publish_exclusive, restore_rows


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.sealed=self.root/'sealed';self.sealed.mkdir()
        (self.sealed/'data').write_bytes(b'original')
        self.row={'path':'assets/old/data','sha256':hashlib.sha256(b'original').hexdigest(),
            'bytes':8,'mode':0o644,'sealed_generation':str(self.sealed),'sealed_relative':'data'}

    def test_recovery_is_independent_copy(self):
        target=restore_rows([self.row],self.root/'restored')/'assets/old/data'
        self.assertEqual(target.read_bytes(),b'original')
        self.assertNotEqual(target.stat().st_ino,(self.sealed/'data').stat().st_ino)

    def test_existing_destination_is_never_overwritten(self):
        target=self.root/'existing';target.mkdir();(target/'user-work').write_bytes(b'keep')
        with self.assertRaises(ValueError):restore_rows([self.row],target)
        self.assertEqual((target/'user-work').read_bytes(),b'keep')

    def test_traversal_and_duplicate_are_rejected(self):
        for rows in ([{**self.row,'path':'../escape'}],[self.row,self.row]):
            with self.assertRaises(ValueError):restore_rows(rows,self.root/'restored')
        self.assertFalse((self.root/'restored').exists())

    def test_tamper_and_partial_failure_publish_nothing(self):
        invalid={**self.row,'path':'assets/second','sha256':'0'*64}
        with self.assertRaises(ValueError):restore_rows([self.row,invalid],self.root/'restored')
        self.assertFalse((self.root/'restored').exists())
        self.assertEqual((self.sealed/'data').read_bytes(),b'original')

    def test_symlink_source_is_rejected(self):
        (self.sealed/'alias').symlink_to(self.sealed/'data')
        with self.assertRaises(ValueError):restore_rows([{**self.row,'sealed_relative':'alias'}],self.root/'restored')
        self.assertFalse((self.root/'restored').exists())

    def test_atomic_publication_does_not_replace_an_empty_directory(self):
        source=self.root/'ready';source.mkdir();target=self.root/'existing';target.mkdir()
        with self.assertRaises(OSError):publish_exclusive(source,target)
        self.assertTrue(source.is_dir());self.assertTrue(target.is_dir())

    def test_missing_git_object_never_publishes_partial_tree(self):
        with self.assertRaises(ValueError):
            restore_rows([{**self.row,'git_blob':'0'*40}],self.root/'restored','git')
        self.assertFalse((self.root/'restored').exists())


if __name__=='__main__':unittest.main()
