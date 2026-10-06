"""Official V24 replays from authenticated offline bytes, without live fallback."""
from collections import Counter
from contextlib import ExitStack, contextmanager
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


@contextmanager
def offline():
    with ExitStack() as stack:
        for name in ('subprocess.Popen', 'os.system', 'os.popen',
                     'socket.create_connection', 'socket.socket.connect',
                     'socket.socket.connect_ex', 'urllib.request.urlopen'):
            stack.enter_context(mock.patch(name, side_effect=AssertionError('Offline fixture attempted ' + name)))
        yield


class V24HistoricalFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix='verified-v24-fixture-')
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name).resolve()
        with offline():
            cls.validator = fixtures.archived_v24_validator(cls.root, source_root=ROOT)
            cls.manifest = fixtures._v24_parent_manifest(ROOT)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name).resolve()

    def manifest_only_source(self):
        source = self.temp / 'input'
        for version in range(17, 25):
            name = getattr(fixtures, f'V{version}_PARENT_MANIFEST')
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / name).read_bytes())
        return source

    def test_complete_membership_sizes_hashes_blobs_modes_and_original_source(self):
        manifest = self.manifest
        self.assertEqual('3b481ca94fdbbeeb453e1d3ec657db0f5baf6a80', manifest['source_pin'])
        self.assertEqual('5332eb72dcf23d5b517961313490f990cc18d56f', manifest['source_tree'])
        self.assertEqual((170, 426), (len(manifest['members']), len(manifest['dependencies'])))
        self.assertEqual({'reuse_official_v23_parent_source': 153,
                          'new_immutable_snapshot_same_git_blob': 17}, manifest['counts'])
        self.assertEqual(manifest['counts'], dict(Counter(row['kind'] for row in manifest['members'])))
        records = manifest['members'] + manifest['dependencies']
        self.assertEqual({row['path'] for row in records},
                         {path.relative_to(self.root).as_posix() for path in self.root.rglob('*') if path.is_file()})
        for row in records:
            path = self.root / row['path']
            raw = path.read_bytes()
            with self.subTest(path=row['path']):
                self.assertFalse(path.is_symlink())
                self.assertEqual(row['bytes'], len(raw))
                self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
                self.assertEqual(row['git_blob'], hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
                self.assertEqual(int(row['mode'][-3:], 8), path.stat().st_mode & 0o7777)
        self.assertEqual(13149751, sum(row['bytes'] for row in manifest['members']
                                     if row['kind'] == 'new_immutable_snapshot_same_git_blob'))
        self.assertEqual(0, manifest['new_archive_count'])
        self.assertEqual(0, manifest['new_git_blob_payload_bytes'])
        self.assertEqual(574, fixtures._v23_parent_manifest(ROOT)['member_count'])
        self.assertEqual(self.root / fixtures.V17_PARENT_VALIDATOR, Path(self.validator.__file__))
        self.assertTrue(hasattr(self.validator, '_validate_v24_structure_source_successor'))
        self.assertFalse(hasattr(self.validator, '_validate_v25_ct073_back_band_successor'))

    def test_original_v24_boundary_passes_and_current_data_fails_at_source_binding(self):
        assets = self.root / ILLUSTRATION / 'assets'
        baseline = json.loads((assets / 'photo_regression_baseline_v24.json').read_bytes())
        raw = (assets / 'photo_regression_baseline_v24_pack.json').read_bytes()
        with offline():
            self.validator._validate_v24_structure_source_successor(
                assets, self.root, baseline, json.loads(raw)[0], raw)
            with self.assertRaisesRegex(self.validator.ValidationFailure,
                                        'photo V24 authored source or runtime binding drift'):
                self.validator._validate_v24_structure_source_successor(
                    ROOT / ILLUSTRATION / 'assets', ROOT, baseline, json.loads(raw)[0], raw)

    def test_original_default_and_explicit_v24_reject_v25_without_generation(self):
        assets = self.root / ILLUSTRATION / 'assets'
        raw = (assets / 'photo_regression_baseline_v24_pack.json').read_bytes()

        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(raw)
            return subprocess.CompletedProcess(command, 0, '', '')

        with offline(), mock.patch.object(self.validator.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 24):
                with self.subTest(version=version):
                    result = self.validator.validate_photo_regression_baseline(assets, baseline_version=version)
                    self.assertEqual('photo_regression_baseline/v24', result['schema'])
            with self.assertRaisesRegex(self.validator.ValidationFailure, 'unsupported photo baseline version'):
                self.validator.validate_photo_regression_baseline(assets, baseline_version=25)

    def test_all_four_modules_and_lazy_imports_are_sealed_and_cache_independent(self):
        names = ('illustration_runtime', 'illustration_audit', 'universal_scene_runtime',
                 'validate_illustration_assets')
        original_path = list(sys.path)
        original_modules = {name: sys.modules.get(name) for name in names}
        hook = self.validator.__dict__['__builtins__']['__import__']
        with offline(), mock.patch.dict(sys.modules, {name: object() for name in names}):
            loaded = {name: hook(name) for name in names}
            self.assertIs(self.validator, loaded['validate_illustration_assets'])
            for name, module in loaded.items():
                self.assertEqual(self.root / ILLUSTRATION / 'scripts' / (name + '.py'), Path(module.__file__))
                self.assertNotIn(module.__name__, sys.modules)
                inner = module.__dict__['__builtins__']['__import__']
                for other in names:
                    self.assertIs(loaded[other], inner(other))
        self.assertEqual(original_path, sys.path)
        self.assertEqual(original_modules, {name: sys.modules.get(name) for name in names})

    def test_fixed_manifest_pin_rejects_mutation_and_coordinated_rehash(self):
        source = self.manifest_only_source()
        target = source / fixtures.V24_PARENT_MANIFEST
        for kind in ('source_pin', 'source_tree', 'previous_manifest', 'source_hash', 'coordinated_rehash'):
            changed = copy.deepcopy(self.manifest)
            if kind in ('source_pin', 'source_tree'):
                changed[kind] = '0' * 40
            elif kind == 'previous_manifest':
                changed['previous_manifest_sha256'] = '0' * 64
            elif kind == 'source_hash':
                changed['members'][0]['sha256'] = '0' * 64
            else:
                row = changed['members'][0]
                raw = (ROOT / row['source_path']).read_bytes() + b'\n'
                row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                           git_blob=hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
                changed['total_member_bytes'] += 1
            target.write_bytes(encoded(changed))
            output = self.temp / 'rejected'
            with self.subTest(kind=kind), offline(), self.assertRaisesRegex(AssertionError, 'V24 parent source manifest drift'):
                fixtures.materialize_v24_parent_source(output, source_root=source)
            self.assertFalse(output.exists())

    def test_inventory_checks_reject_invalid_paths_backings_modes_and_membership(self):
        source = self.manifest_only_source()
        target = source / fixtures.V24_PARENT_MANIFEST
        for kind in ('absolute', 'traversal', 'noncanonical', 'duplicate', 'cross_duplicate',
                     'missing', 'dependency_missing', 'unknown_kind', 'live_fallback',
                     'wrong_mode', 'wrong_blob', 'reuse_mismatch', 'counts', 'dependency_mapping'):
            changed = copy.deepcopy(self.manifest)
            row = changed['members'][0]
            if kind == 'absolute': row['path'] = '/tmp/escaped-v24'
            elif kind == 'traversal': row['source_path'] = '../escaped-v24'
            elif kind == 'noncanonical': row['source_path'] = 'nested//payload'
            elif kind == 'duplicate': changed['members'][1] = copy.deepcopy(row)
            elif kind == 'cross_duplicate': changed['dependencies'][0] = copy.deepcopy(row)
            elif kind == 'missing': changed['members'].pop()
            elif kind == 'dependency_missing': changed['dependencies'].pop()
            elif kind == 'unknown_kind': row['kind'] = 'live_source'
            elif kind == 'live_fallback':
                row = next(row for row in changed['members'] if row['kind'] == 'new_immutable_snapshot_same_git_blob')
                row['source_path'] = row['path']
            elif kind == 'wrong_mode': row['mode'] = '120000'
            elif kind == 'wrong_blob': row['git_blob'] = 'z' * 40
            elif kind == 'reuse_mismatch': row['sha256'] = '0' * 64
            elif kind == 'counts': changed['counts']['reuse_official_v23_parent_source'] += 1
            else: changed['dependencies'][0]['source_path'] = 'unregistered/payload'
            raw = encoded(changed)
            target.write_bytes(raw)
            # Exercise structural checks independently of the immutable outer seal.
            with self.subTest(kind=kind), mock.patch.object(fixtures, 'V24_PARENT_MANIFEST_SHA256',
                                                          hashlib.sha256(raw).hexdigest()):
                with self.assertRaises(AssertionError):
                    fixtures._v24_parent_manifest(source)

    def test_v23_chain_is_authenticated_without_payloads_or_git(self):
        source = self.manifest_only_source()
        with offline():
            self.assertEqual(self.manifest, fixtures._v24_parent_manifest(source))
        path = source / fixtures.V23_PARENT_MANIFEST
        path.write_bytes(path.read_bytes() + b'\n')
        with offline(), self.assertRaisesRegex(AssertionError, 'V23 parent source manifest drift'):
            fixtures._v24_parent_manifest(source)

    def test_payload_rejects_missing_mutated_size_hash_blob_mode_and_symlinks(self):
        source = self.temp / 'input'
        rows = [row for row in self.manifest['members'] if row['kind'] == 'new_immutable_snapshot_same_git_blob']
        rows += [self.manifest['members'][0], self.manifest['dependencies'][0]]
        for row in rows:
            path = source / row['source_path']
            path.parent.mkdir(parents=True, exist_ok=True)
            with self.subTest(path=row['path'], kind='missing'), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(source, row)
            raw = (ROOT / row['source_path']).read_bytes()
            path.write_bytes(raw + b'\n')
            path.chmod(int(row['mode'][-3:], 8))
            with self.subTest(path=row['path'], kind='mutated'), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(source, row)
            path.write_bytes(raw)
            for field, value in (('bytes', len(raw) + 1), ('sha256', '0' * 64), ('git_blob', '0' * 40)):
                with self.subTest(path=row['path'], field=field), self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(source, dict(row, **{field: value}))
            path.chmod(0o600)
            with self.subTest(path=row['path'], kind='mode'), self.assertRaisesRegex(AssertionError, 'mode drift'):
                fixtures._v24_verified_payload(source, row)
            path.unlink()
            path.symlink_to(ROOT / row['source_path'])
            with self.subTest(path=row['path'], kind='symlink'), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(source, row)
            path.unlink()

    def test_payload_paths_and_source_root_ancestors_reject_symlinks_and_traversal(self):
        row = self.manifest['members'][0]
        for name in ('/tmp/escaped-v24', '../escaped-v24', 'nested/../payload', './payload',
                     'nested//payload', 'nested\\payload', 'C:/payload', 'nested/\x00payload'):
            with self.subTest(path=name), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(ROOT, dict(row, source_path=name))
        linked = self.temp / 'linked'
        linked.symlink_to(ROOT, target_is_directory=True)
        with self.assertRaisesRegex(AssertionError, 'symlink'):
            fixtures._v24_parent_manifest(linked)
        with self.assertRaisesRegex(AssertionError, 'symlink'):
            fixtures._v24_verified_payload(linked / Path(row['source_path']).parent,
                                           dict(row, source_path=Path(row['source_path']).name))

    def test_missing_payload_never_fetches_or_falls_back_to_live_source(self):
        source = self.manifest_only_source()
        row = self.manifest['members'][0]
        live = source / row['path']
        live.parent.mkdir(parents=True, exist_ok=True)
        live.write_bytes((ROOT / row['source_path']).read_bytes())
        output = self.temp / 'output'
        with offline(), self.assertRaisesRegex(AssertionError, 'Missing V24 historical source payload'):
            fixtures.materialize_v24_parent_source(output, source_root=source)
        self.assertFalse(output.exists())

    def test_late_source_mutation_does_not_leave_partial_output(self):
        original = fixtures._v24_verified_payload
        count = len(self.manifest['members']) + len(self.manifest['dependencies'])
        for existing in (False, True):
            output = self.temp / str(existing)
            if existing:
                output.mkdir()
            calls = 0

            def changing_source(source, row):
                nonlocal calls
                calls += 1
                if calls == count + 2:
                    raise AssertionError('Simulated source mutation after preflight')
                return original(source, row)

            with self.subTest(existing=existing), offline(), mock.patch.object(
                    fixtures, '_v24_verified_payload', side_effect=changing_source):
                with self.assertRaisesRegex(AssertionError, 'after preflight'):
                    fixtures.materialize_v24_parent_source(output, source_root=ROOT)
            self.assertEqual(existing, output.exists())
            self.assertEqual([], list(output.iterdir()) if existing else [])
            self.assertFalse(list(self.temp.glob('.sealed-v24-*')))

    def test_destination_rejects_files_nonempty_and_symlink_ancestors(self):
        existing = self.temp / 'existing'
        existing.mkdir()
        (existing / 'keep').write_text('keep')
        regular = self.temp / 'file'
        regular.write_text('keep')
        empty = self.temp / 'empty'
        empty.mkdir()
        linked = self.temp / 'linked'
        linked.symlink_to(empty, target_is_directory=True)
        for output in (existing, regular, linked, linked / 'child'):
            with self.subTest(path=output), self.assertRaises(AssertionError):
                fixtures.materialize_v24_parent_source(output, source_root=ROOT)
        self.assertEqual('keep', regular.read_text())
        self.assertEqual('keep', (existing / 'keep').read_text())
        self.assertEqual([], list(empty.iterdir()))


if __name__ == '__main__':
    unittest.main()
