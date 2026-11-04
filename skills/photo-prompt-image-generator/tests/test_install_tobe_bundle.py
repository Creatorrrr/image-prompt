import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install_photo_tobe_bundle as bundle


def archive(rows):
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode='w') as tar:
        for name, data, kind in rows:
            item = tarfile.TarInfo(name)
            if kind == 'link':
                item.type = tarfile.SYMTYPE; item.linkname = '/outside'; tar.addfile(item)
            else:
                item.size = len(data); tar.addfile(item, io.BytesIO(data))
    out.seek(0)
    return out


class BundleExtraction(unittest.TestCase):
    def test_only_selected_regular_members_are_extracted(self):
        rows = [('repo/private.txt', b'private', 'file'),
                ('runtime/generations/abc/manifest.json', b'sealed', 'file')]
        with tempfile.TemporaryDirectory() as d:
            prefix = PurePosixPath('runtime/generations/abc')
            seen = bundle.extract_members(archive(rows), d, [prefix])
            self.assertEqual(seen, {prefix / 'manifest.json'})
            self.assertEqual((Path(d) / prefix / 'manifest.json').read_bytes(), b'sealed')
            self.assertFalse((Path(d) / 'repo/private.txt').exists())

    def test_escape_symlink_and_duplicate_are_rejected(self):
        prefix = PurePosixPath('runtime/generations/abc')
        for rows in ([('../escape', b'x', 'file')],
                     [('runtime/generations/abc/link', b'', 'link')],
                     [('runtime/generations/abc/a', b'x', 'file'),
                      ('runtime/generations/abc/a', b'y', 'file')]):
            with self.subTest(rows=rows), tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):
                    bundle.extract_members(archive(rows), d, [prefix])

    def test_source_index_rejects_changed_candidate_corpus(self):
        layout = 'a' * 64
        manifest = {'layout_id': layout, 'corpus_sha256': 'expected', 'shards': [],
                    'metadata': {'path': f'photo_candidate_search_shards/{layout}/meta', 'sha256': 'b' * 64}}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'photo_candidate_search.json'; p.write_text(json.dumps(manifest))
            lock = {'source_manifest_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                    'source_layout_id': layout, 'source_corpus_sha256': 'expected'}
            with patch.object(bundle.corpus, 'load', return_value={}), patch.object(bundle.corpus, 'digest', return_value='different'):
                with self.assertRaisesRegex(ValueError, 'candidate source changed'):
                    bundle.verify_source_index(d, lock)


if __name__ == '__main__':
    unittest.main()
