import gzip
import base64
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_reviewed_source_evidence as evidence


class ReviewedGitSourceEvidence(unittest.TestCase):
    def test_preserved_source_pointer_quote_and_archive_are_checked(self):
        path = 'assets/original.json'
        raw = b'{"nodes":[{"meaning":"blue coat"}]}'
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        asset_tree = b'100644 original.json\0' + bytes.fromhex(blob)
        asset_oid = evidence._git_oid('tree', asset_tree)
        root_tree = b'40000 assets\0' + bytes.fromhex(asset_oid)
        root_oid = evidence._git_oid('tree', root_tree)
        raw_commit = ('tree ' + root_oid + '\nauthor test <test@example.com> 0 +0000\n'
                      'committer test <test@example.com> 0 +0000\n\ntest\n').encode()
        commit = evidence._git_oid('commit', raw_commit)
        sources = {commit + ':' + path: {'text': raw.decode(), 'git_blob_sha1': blob,
                                        'sha256': hashlib.sha256(raw).hexdigest()}}
        proof = {'raw_base64': base64.b64encode(raw_commit).decode(),
                 'trees': {root_oid: base64.b64encode(root_tree).decode(),
                           asset_oid: base64.b64encode(asset_tree).decode()}}
        bundle = {'schema': 'photo-reviewed-git-sources/v1', 'sources': sources,
                  'commits': {commit: proof}}
        packed = gzip.compress(json.dumps(bundle).encode(), mtime=0)
        overlay = {'items': [{'evidence': [{'locator': 'git:' + commit + ':' + path + '#/nodes/0',
                                           'quote': 'blue coat'}]}]}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'sources.gz').write_bytes(packed)
            registry = root / 'registry.json'
            registry.write_text(json.dumps({'schema': 'photo-reviewed-git-source-registry/v1',
                'archive': 'sources.gz', 'archive_sha256': hashlib.sha256(packed).hexdigest(),
                'source_files': 1}))
            self.assertEqual(evidence.verify_git([overlay], registry), {'documents': 1, 'quotes': 1})
            proof['trees'][root_oid] = base64.b64encode(root_tree + b'changed').decode()
            damaged = gzip.compress(json.dumps(bundle).encode(), mtime=0)
            (root / 'sources.gz').write_bytes(damaged)
            manifest = json.loads(registry.read_bytes())
            manifest['archive_sha256'] = hashlib.sha256(damaged).hexdigest()
            registry.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'tree proof changed'):
                evidence.verify_git([overlay], registry)
            (root / 'sources.gz').write_bytes(packed)
            manifest['archive_sha256'] = hashlib.sha256(packed).hexdigest()
            registry.write_text(json.dumps(manifest))
            overlay['items'][0]['evidence'][0]['quote'] = 'red coat'
            with self.assertRaisesRegex(ValueError, 'quote changed'):
                evidence.verify_git([overlay], registry)
            overlay['items'][0]['evidence'][0]['quote'] = 'blue coat'
            overlay['items'][0]['evidence'][0]['locator'] += '/missing'
            with self.assertRaisesRegex(ValueError, 'pointer missing'):
                evidence.verify_git([overlay], registry)
            (root / 'sources.gz').write_bytes(packed + b'altered')
            with self.assertRaisesRegex(ValueError, 'archive changed'):
                evidence.verify_git([overlay], registry)


if __name__ == '__main__':
    unittest.main()
