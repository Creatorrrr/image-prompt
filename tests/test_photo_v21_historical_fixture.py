"""V21's original validator and source are explicit, sealed, offline fixtures."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]


class V21HistoricalFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory(prefix='verified-v21-fixture-')
        cls.addClassCleanup(temp.cleanup)
        cls.root = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Fixture invoked subprocess')):
            cls.validator = fixtures.archived_validator_with_v24_source(cls.root, version=21, source_root=ROOT)
        cls.manifest = fixtures._v21_parent_manifest(ROOT)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)

    def test_exact_726c_source_and_dependencies_are_loaded_without_git(self):
        self.assertEqual('726c51b015294930f0ad98ca126cde11e6caead2', self.manifest['source_pin'])
        self.assertEqual((166, 216), (len(self.manifest['members']), len(self.manifest['dependencies'])))
        self.assertEqual(9, sum(row['kind'] == 'new_immutable_snapshot_same_git_blob'
                                for row in self.manifest['members']))
        for row in self.manifest['members'] + self.manifest['dependencies']:
            raw = (self.root / row['path']).read_bytes()
            self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest(), row['path'])
            self.assertEqual(row['bytes'], len(raw), row['path'])
        self.assertEqual(self.root / fixtures.V17_PARENT_VALIDATOR, Path(self.validator.__file__))
        self.assertFalse(hasattr(self.validator, '_validate_v22_ornament_data_successor'))

    def test_manifest_rejects_path_traversal_duplicate_missing_and_coordinated_rehash(self):
        original = (ROOT / fixtures.V21_PARENT_MANIFEST).read_bytes()
        source = self.temp / 'input'
        target = source / fixtures.V21_PARENT_MANIFEST
        target.parent.mkdir(parents=True)
        for kind in ('absolute', 'traversal', 'duplicate', 'missing', 'source_pin',
                     'live_source', 'coordinated_rehash'):
            manifest = json.loads(original)
            if kind == 'absolute': manifest['members'][0]['path'] = '/tmp/escaped-v21-fixture'
            elif kind == 'traversal': manifest['members'][0]['source_path'] = '../escaped-v21-fixture'
            elif kind == 'duplicate': manifest['members'][1] = manifest['members'][0]
            elif kind == 'missing': manifest['members'].pop()
            elif kind == 'source_pin': manifest['source_pin'] = '0' * 40
            elif kind == 'live_source': manifest['members'][0]['source_path'] = manifest['members'][0]['path']
            else:
                row = manifest['members'][0]
                raw = (ROOT / row['source_path']).read_bytes() + b'\n'
                payload = source / row['source_path']
                payload.parent.mkdir(parents=True, exist_ok=True)
                payload.write_bytes(raw)
                manifest['total_member_bytes'] += 1
                row.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                           git_blob=hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
            target.write_text(json.dumps(manifest))
            output = self.temp / 'invalid-output'
            with self.subTest(kind=kind), self.assertRaisesRegex(AssertionError, 'V21 parent source manifest drift'):
                fixtures.materialize_v21_parent_source(output, source_root=source)
            self.assertFalse(output.exists())

    def test_source_payload_rejects_missing_mutated_and_symlink_bytes(self):
        rows = [row for row in self.manifest['members']
                if row['kind'] == 'new_immutable_snapshot_same_git_blob']
        rows += [next(row for row in self.manifest['members'] if '/7ff3e10cc7163368/' in row['path'])]
        source = self.temp / 'input'
        for row in rows:
            target = source / row['source_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            with self.subTest(path=row['path'], kind='missing'), self.assertRaisesRegex(AssertionError, 'Missing .*historical source payload'):
                fixtures._v17_verified_payload(source, row)
            target.write_bytes((ROOT / row['source_path']).read_bytes() + b'\n')
            with self.subTest(path=row['path'], kind='mutated'), self.assertRaisesRegex(AssertionError, 'payload drift'):
                fixtures._v17_verified_payload(source, row)
            target.unlink()
            target.symlink_to(ROOT / row['source_path'])
            with self.subTest(path=row['path'], kind='symlink'), self.assertRaisesRegex(AssertionError, 'historical source symlink'):
                fixtures._v17_verified_payload(source, row)
            target.unlink()

    def test_destination_must_be_empty_and_regular(self):
        existing = self.temp / 'existing'
        existing.mkdir()
        (existing / 'keep').write_text('keep')
        linked = self.temp / 'linked'
        linked.symlink_to(existing, target_is_directory=True)
        for destination in (existing, linked):
            with self.subTest(path=destination), self.assertRaisesRegex(AssertionError, 'empty directory'):
                fixtures.materialize_v21_parent_source(destination, source_root=ROOT)
        self.assertEqual('keep', (existing / 'keep').read_text())


if __name__ == '__main__':
    unittest.main()
