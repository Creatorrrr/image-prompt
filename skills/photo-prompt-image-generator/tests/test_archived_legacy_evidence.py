import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_archived_legacy_evidence as evidence


class ArchivedLegacyEvidenceTest(unittest.TestCase):
    def test_sealed_archive_binds_provenance_and_detects_changes(self):
        cid = 'cand_' + 'a' * 32
        original = {'id': cid, 'meaning': 'preserved historical content'}
        record_hash = evidence.digest(original)
        shard = gzip.compress(json.dumps({cid: original}).encode(), mtime=0)
        shard_path = 'body/aaa.json.gz'
        source = json.dumps({'files': {shard_path: hashlib.sha256(shard).hexdigest()}}).encode()
        locator = gzip.compress(json.dumps({cid: {'path': shard_path, 'sha256': record_hash}}).encode(), mtime=0)
        manifest = {'files': {'source-manifest.json': hashlib.sha256(source).hexdigest(),
                              'body-locator.json.gz': hashlib.sha256(locator).hexdigest(),
                              shard_path: hashlib.sha256(shard).hexdigest()}}
        generation = evidence.digest(manifest)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tarpath = root / 'input.tar'
            with tarfile.open(tarpath, 'w') as tar:
                for name, raw in [('manifest.json', json.dumps(manifest).encode()),
                                  ('source-manifest.json', source),
                                  ('body-locator.json.gz', locator), (shard_path, shard)]:
                    info = tarfile.TarInfo(name)
                    info.size = len(raw)
                    tar.addfile(info, io.BytesIO(raw))
            archive = root / 'evidence.tar.zst'
            with archive.open('wb') as out:
                subprocess.run(['zstd', '-q', '-c', str(tarpath)], stdout=out, check=True)
            registry = root / 'registry.json'
            registry.write_text(json.dumps({'schema': 'photo-legacy-evidence-registry/v1', 'archives': [{
                'generation_id': generation, 'archive': str(archive), 'archive_sha256': evidence.file_sha(archive)}]}))
            records = {cid: {'provenance': [{'source': f'installed-h-f2-canonical-candidate:{generation}/{cid}',
                                             'sha256': record_hash}]}}
            self.assertEqual(evidence.verify(records, registry), {'archives': 1, 'candidates': 1})
            records[cid]['provenance'][0]['sha256'] = 'f' * 64
            with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
                evidence.verify(records, registry)
            archive.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'archive missing or changed'):
                evidence.verify(records, registry)

    def test_records_without_legacy_reference_do_not_require_archive(self):
        self.assertEqual(evidence.verify({'x': {'provenance': []}}, '/missing/registry.json'),
                         {'archives': 0, 'candidates': 0})

    def test_malformed_legacy_reference_is_not_ignored(self):
        records = {'x': {'provenance': [{'source': 'installed-h-f2-canonical-candidate:broken',
                                          'sha256': 'f' * 64}]}}
        with self.assertRaisesRegex(ValueError, 'invalid legacy candidate provenance'):
            evidence.verify(records, '/missing/registry.json')


if __name__ == '__main__':
    unittest.main()
