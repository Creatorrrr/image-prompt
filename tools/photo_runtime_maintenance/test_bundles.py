import hashlib
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

from bundles import pack, restore, safe_name, split_archive
from state import sha


class BundleSafety(unittest.TestCase):
    def test_verified_restore_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t); (p/'source').write_text('exact source')
            seal = pack(p/'a.zip', {'scripts/a.py':p/'source'})
            restore(p/'a.zip', seal, p/'restored')
            self.assertEqual((p/'restored/scripts/a.py').read_text(), 'exact source')
            with self.assertRaises(ValueError): restore(p/'a.zip', seal, p/'restored')
            (p/'a.zip').write_bytes(b'tampered')
            with self.assertRaises(ValueError): restore(p/'a.zip', seal, p/'other')
            self.assertFalse((p/'other').exists())

    def test_traversal_duplicate_and_symlink_rejected(self):
        for name in ('.','../x','/x','a/../x','a\\x','a//x'):
            with self.assertRaises(ValueError): safe_name(name)
        with tempfile.TemporaryDirectory() as t:
            p = Path(t); z = p/'bad.zip'
            with zipfile.ZipFile(z,'w') as out:
                item = zipfile.ZipInfo('link'); item.external_attr = (stat.S_IFLNK|0o777)<<16
                out.writestr(item,b'target')
            seal = {'archive_sha256':sha(z),'files':{'link':{'sha256':hashlib.sha256(b'target').hexdigest(),'bytes':6}}}
            with self.assertRaises(ValueError): restore(z,seal,p/'destination')
            self.assertFalse((p/'destination').exists())

    def test_split_parts_restore_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t);(p/'source').write_bytes(b'restored exact bytes')
            seal = pack(p/'a.zip',{'source':p/'source'})
            seal = split_archive(p/'a.zip',seal,64)
            self.assertFalse((p/'a.zip').exists())
            restore(p/'a.zip',seal,p/'restored')
            self.assertEqual((p/'restored/source').read_bytes(),b'restored exact bytes')
            part = p/seal['parts'][0]['name'];part.write_bytes(b'changed')
            with self.assertRaises(ValueError):restore(p/'a.zip',seal,p/'bad')
            self.assertFalse((p/'bad').exists())

    def test_duplicate_members_cannot_create_restore_root(self):
        import warnings
        with tempfile.TemporaryDirectory() as t:
            p = Path(t);z = p/'bad.zip'
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',UserWarning)
                with zipfile.ZipFile(z,'w') as out:
                    out.writestr('same',b'one');out.writestr('same',b'two')
            seal = {'archive_sha256':sha(z),'files':{'same':{'sha256':hashlib.sha256(b'two').hexdigest(),'bytes':3}}}
            with self.assertRaises(ValueError):restore(z,seal,p/'bad')
            self.assertFalse((p/'bad').exists())


if __name__ == '__main__': unittest.main()
