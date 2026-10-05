"""The original V22 validator and source replay from sealed offline fixtures."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]


class V22HistoricalFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory(prefix='verified-v22-fixture-')
        cls.addClassCleanup(temp.cleanup)
        cls.root = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Fixture invoked subprocess')):
            cls.validator = fixtures.archived_v22_validator(cls.root, source_root=ROOT)
        cls.manifest = fixtures._v22_parent_manifest(ROOT)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)

    def test_exact_900b_source_and_dependencies_are_loaded_without_git(self):
        self.assertEqual('900bf2efdd17fbc6a6ef3aa340f3526b1e01f223', self.manifest['source_pin'])
        self.assertEqual((168, 261), (len(self.manifest['members']), len(self.manifest['dependencies'])))
        counts = {'reuse_v21_parent_source': 129, 'reuse_retained_vector_shard': 31,
                  'new_immutable_snapshot_same_git_blob': 8}
        self.assertEqual(counts, dict(Counter(row['kind'] for row in self.manifest['members'])))
        self.assertEqual(counts, self.manifest['counts'])
        for row in self.manifest['members'] + self.manifest['dependencies']:
            path = self.root / row['path']
            raw = path.read_bytes()
            self.assertFalse(path.is_symlink(), row['path'])
            self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest(), row['path'])
            self.assertEqual(row['bytes'], len(raw), row['path'])
            self.assertEqual(row['git_blob'],
                             hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest(), row['path'])
        self.assertEqual(self.root / fixtures.V17_PARENT_VALIDATOR, Path(self.validator.__file__))
        self.assertTrue(hasattr(self.validator, '_validate_v22_ornament_data_successor'))
        self.assertFalse(hasattr(self.validator, '_validate_v23_lobe_boundary_successor'))

    def test_original_v22_boundary_passes_with_its_frozen_source(self):
        assets = self.root / 'skills/subculture-illustration-image-generator/assets'
        baseline = json.loads((assets / 'photo_regression_baseline_v22.json').read_bytes())
        raw = (assets / 'photo_regression_baseline_v22_pack.json').read_bytes()
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Fixture invoked subprocess')):
            self.validator._validate_v22_ornament_data_successor(
                assets, self.root, baseline, json.loads(raw)[0], raw)

    def test_manifest_rejects_path_mapping_inventory_and_coordinated_rehash(self):
        original = (ROOT / fixtures.V22_PARENT_MANIFEST).read_bytes()
        source = self.temp / 'input'
        target = source / fixtures.V22_PARENT_MANIFEST
        target.parent.mkdir(parents=True)
        for kind in ('absolute', 'traversal', 'duplicate', 'missing', 'dependency_missing',
                     'source_pin', 'live_source', 'counts', 'coordinated_rehash'):
            manifest = json.loads(original)
            if kind == 'absolute':
                manifest['members'][0]['path'] = '/tmp/escaped-v22-fixture'
            elif kind == 'traversal':
                manifest['members'][0]['source_path'] = '../escaped-v22-fixture'
            elif kind == 'duplicate':
                manifest['members'][1] = manifest['members'][0]
            elif kind == 'missing':
                manifest['members'].pop()
            elif kind == 'dependency_missing':
                manifest['dependencies'].pop()
            elif kind == 'source_pin':
                manifest['source_pin'] = '0' * 40
            elif kind == 'live_source':
                row = next(row for row in manifest['members']
                           if row['kind'] == 'new_immutable_snapshot_same_git_blob')
                row['source_path'] = row['path']
            elif kind == 'counts':
                manifest['counts']['reuse_v21_parent_source'] += 1
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
            with self.subTest(kind=kind), self.assertRaises(AssertionError):
                fixtures.materialize_v22_parent_source(output, source_root=source)
            self.assertFalse(output.exists())

    def test_payload_paths_reject_absolute_traversal_and_noncanonical_forms(self):
        original = self.manifest['members'][0]
        for name in ('/tmp/escaped-v22-fixture', '../escaped-v22-fixture',
                     'nested/../escaped-v22-fixture', './payload', 'nested//payload',
                     'nested\\payload', 'C:/payload', 'nested/\x00payload'):
            row = dict(original, source_path=name)
            with self.subTest(path=name), self.assertRaises(AssertionError):
                fixtures._v17_verified_payload(self.temp, row)

    def test_source_payload_rejects_missing_mutated_and_symlink_bytes(self):
        rows = [row for row in self.manifest['members']
                if row['kind'] == 'new_immutable_snapshot_same_git_blob']
        for kind in ('reuse_v21_parent_source', 'reuse_retained_vector_shard'):
            rows.append(next(row for row in self.manifest['members'] if row['kind'] == kind))
        rows.append(self.manifest['dependencies'][0])
        source = self.temp / 'input'
        for row in rows:
            target = source / row['source_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            with self.subTest(path=row['path'], kind='missing'), self.assertRaises(AssertionError):
                fixtures._v17_verified_payload(source, row)
            target.write_bytes((ROOT / row['source_path']).read_bytes() + b'\n')
            with self.subTest(path=row['path'], kind='mutated'), self.assertRaises(AssertionError):
                fixtures._v17_verified_payload(source, row)
            target.unlink()
            target.symlink_to(ROOT / row['source_path'])
            with self.subTest(path=row['path'], kind='symlink'), self.assertRaises(AssertionError):
                fixtures._v17_verified_payload(source, row)
            target.unlink()

    def test_missing_payload_does_not_create_a_partial_destination_or_fetch(self):
        source = self.temp / 'input'
        manifests = [getattr(fixtures, f'V{version}_PARENT_MANIFEST')
                     for version in range(17, 23)]
        manifests.append(fixtures.V17_SUPPORT_MANIFEST)
        for name in manifests:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        self.assertEqual(self.manifest, fixtures._v22_parent_manifest(source))
        output = self.temp / 'invalid-output'
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Fixture invoked subprocess')):
            with self.assertRaisesRegex(AssertionError, 'Missing .*historical source payload'):
                fixtures.materialize_v22_parent_source(output, source_root=source)
        self.assertFalse(output.exists())

    def test_manifest_and_payload_parent_symlinks_rejected(self):
        source = self.temp / 'input'
        manifest = source / fixtures.V22_PARENT_MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.symlink_to(ROOT / fixtures.V22_PARENT_MANIFEST)
        output = self.temp / 'invalid-output'
        with self.assertRaises(AssertionError):
            fixtures.materialize_v22_parent_source(output, source_root=source)
        self.assertFalse(output.exists())
        row = self.manifest['members'][0]
        outside = self.temp / 'outside'
        outside.mkdir()
        (outside / 'payload').write_bytes((ROOT / row['source_path']).read_bytes())
        (source / 'linked').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(AssertionError):
            fixtures._v17_verified_payload(source, dict(row, source_path='linked/payload'))

    def test_destination_must_be_empty_and_regular(self):
        existing = self.temp / 'existing'
        existing.mkdir()
        (existing / 'keep').write_text('keep')
        linked = self.temp / 'linked'
        linked.symlink_to(existing, target_is_directory=True)
        linked_empty_target = self.temp / 'empty'
        linked_empty_target.mkdir()
        linked_empty = self.temp / 'linked-empty'
        linked_empty.symlink_to(linked_empty_target, target_is_directory=True)
        for destination in (existing, linked, linked_empty):
            with self.subTest(path=destination), self.assertRaises(AssertionError):
                fixtures.materialize_v22_parent_source(destination, source_root=ROOT)
        self.assertEqual('keep', (existing / 'keep').read_text())
        self.assertEqual([], list(linked_empty_target.iterdir()))


if __name__ == '__main__':
    unittest.main()
