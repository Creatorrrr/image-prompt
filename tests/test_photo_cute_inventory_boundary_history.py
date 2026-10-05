"""The V17 successor cannot rebaseline a changed scene or candidate object."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from types import ModuleType

ROOT=Path(__file__).resolve().parents[1]
ILLUSTRATION=ROOT/'skills/subculture-illustration-image-generator'
sys.path.insert(0,str(ILLUSTRATION/'scripts'))
import photo_prompt_fixtures as fixtures


class CuteInventoryBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global v
        temp = tempfile.TemporaryDirectory(prefix='immutable-v17-parent-')
        cls.addClassCleanup(temp.cleanup)
        cls.source_root = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Historical fixture invoked Git or a subprocess')):
            v = fixtures.archived_v17_validator(cls.source_root)

    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.assets=Path(temp.name)
        historical_assets = self.source_root / 'skills/subculture-illustration-image-generator/assets'
        for path in historical_assets.glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path,self.assets/path.name)
        shutil.copyfile(historical_assets/'universal_scene_baseline_v2.json',
                        self.assets/'universal_scene_baseline_v2.json')
        self.baseline=json.loads((self.assets/'photo_regression_baseline_v17.json').read_text())
        self.raw=(self.assets/'photo_regression_baseline_v17_pack.json').read_bytes()
        self.pack=json.loads(self.raw)[0]

    def validate(self,pack=None,raw=None,repo=None):
        return v._validate_v17_cute_data_successor(self.assets,self.source_root if repo is None else repo,self.baseline,
            self.pack if pack is None else pack,self.raw if raw is None else raw)

    def test_fixture_restores_exact_source_and_original_validator_without_git(self):
        manifest = fixtures._v17_parent_manifest()
        self.assertEqual(len(manifest['members']), 149)
        for row in manifest['members'] + manifest['dependencies']:
            raw = (self.source_root / row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'], row['path'])
            self.assertEqual(len(raw), row['bytes'], row['path'])
        self.assertEqual(Path(v.__file__).read_bytes(), (self.source_root / fixtures.V17_PARENT_VALIDATOR).read_bytes())

    def test_sealed_successor_preserves_every_frozen_scene_and_candidate_field(self):
        self.validate()
        old=json.loads((self.assets/'photo_regression_baseline_v16_pack.json').read_text())[0]
        for field in ['authorial_core','creative_controls','authorial_composition','negative_en',
                      'negative_intent_guard','slots','candidate_bundles','visual_concept_candidates',
                      'intent_preservation','embodiment_preflight','adult_appeal']:
            with self.subTest(field=field):self.assertEqual(old[field],self.pack[field])

    def test_coordinated_candidate_core_negative_and_control_rehash_is_rejected(self):
        for kind in ['candidate','order','core','negative','controls','adoption']:
            changed=copy.deepcopy(self.pack)
            rows=next(s['candidates'] for s in changed['slots'].values() if len(s['candidates'])>=2)
            if kind=='candidate':rows[0]['concept_terms'][0]+=' altered'
            elif kind=='order':rows.reverse()
            elif kind=='core':changed['authorial_core']['subject']+=' altered'
            elif kind=='negative':changed['negative_en']+=', altered'
            elif kind=='controls':changed['creative_controls']['extra']=True
            else:rows[0]['adoption']='required'
            changed['pack_id']=v._canonical_photo_pack_id(changed)
            raw=(json.dumps([changed],ensure_ascii=False,indent=2)+'\n').encode()
            (self.assets/'photo_regression_baseline_v17_pack.json').write_bytes(raw)
            self.baseline.update(sha256=hashlib.sha256(raw).hexdigest(),pack_id=changed['pack_id'])
            with self.subTest(kind=kind),self.assertRaisesRegex(v.ValidationFailure,'immutable pack binding'):
                self.validate(changed,raw)

    def test_predecessor_manifest_is_immutable(self):
        path=self.assets/'photo_regression_baseline_v16.json'
        path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'pack binding'):
            self.validate()

    def test_transition_cannot_be_reclassified_as_metadata_only(self):
        for field in ['metadata_only_transition','zero_pack_delta_transition',
                      'optional_inventory_transition','authored_metadata_ownership_transition']:
            self.baseline[field]={}
            with self.subTest(field=field),self.assertRaisesRegex(v.ValidationFailure,'cannot relabel'):
                self.validate()
            del self.baseline[field]

    def test_v17_still_rejects_the_live_successor_inventory(self):
        with self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
            self.validate(repo=ROOT)

    def test_v16_still_rejects_the_live_successor_inventory(self):
        baseline=json.loads((self.assets/'photo_regression_baseline_v16.json').read_text())
        raw=(self.assets/'photo_regression_baseline_v16_pack.json').read_bytes()
        with self.assertRaisesRegex(v.ValidationFailure,'exact DATA inventory'):
            v._validate_v16_seduction_source_successor(self.assets,ROOT,baseline,json.loads(raw)[0],raw)


class V17ParentSourceFixtureTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='v17-fixture-integrity-')
        self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name)
        self.source = self.directory / 'source'
        self.output = self.directory / 'output'
        self.manifest = fixtures._v17_parent_manifest()
        manifest_path = self.source / fixtures.V17_PARENT_MANIFEST
        manifest_path.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / fixtures.V17_PARENT_MANIFEST, manifest_path)

    def backing_files(self):
        # Copy only manifest-listed files; mutations cannot touch committed bytes.
        for row in self.manifest['members'] + self.manifest['dependencies']:
            source = ROOT / row['source_path']
            target = self.source / row['source_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def support_files(self):
        support = fixtures._v17_support_manifest()
        shutil.copyfile(ROOT / fixtures.V17_SUPPORT_MANIFEST, self.source / fixtures.V17_SUPPORT_MANIFEST)
        for row in support['members']:
            target = self.source / row['source_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / row['source_path'], target)
        return support

    def assert_rejected(self, message):
        with self.assertRaisesRegex(AssertionError, message):
            fixtures.materialize_v17_parent_source(self.output, source_root=self.source)
        self.assertFalse(self.output.exists(), 'Invalid fixture wrote historical members')

    def test_manifest_hash_rejects_coordinated_payload_and_mapping_rehash(self):
        self.backing_files()
        row = self.manifest['members'][0]
        target = self.source / row['source_path']
        raw = target.read_bytes() + b'\n'
        target.unlink()
        target.write_bytes(raw)
        row.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                   git_blob=hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
        (self.source / fixtures.V17_PARENT_MANIFEST).write_text(json.dumps(self.manifest))
        self.assert_rejected('manifest drift')

    def test_unsafe_missing_duplicate_or_relabelled_manifest_members_fail(self):
        original = (ROOT / fixtures.V17_PARENT_MANIFEST).read_bytes()
        for kind in ('absolute', 'traversal', 'backslash', 'duplicate', 'missing', 'source_pin', 'live_source'):
            manifest = json.loads(original)
            if kind == 'absolute': manifest['members'][0]['path'] = '/tmp/escaped-v17-fixture'
            elif kind == 'traversal': manifest['members'][0]['path'] = '../escaped-v17-fixture'
            elif kind == 'backslash': manifest['members'][0]['source_path'] = '..\\escaped-v17-fixture'
            elif kind == 'duplicate': manifest['members'][1] = manifest['members'][0]
            elif kind == 'missing': manifest['members'].pop()
            elif kind == 'source_pin': manifest['source_pin'] = '0' * 40
            else: manifest['members'][0]['source_path'] = manifest['members'][0]['path']
            (self.source / fixtures.V17_PARENT_MANIFEST).write_text(json.dumps(manifest))
            with self.subTest(kind=kind):
                self.assert_rejected('manifest drift')

    def test_safe_path_check_rejects_absolute_traversal_and_noncanonical_paths(self):
        for value in ('/tmp/escape', '../escape', 'one/../../escape', 'one\\escape',
                      'C:/escape', 'one//escape', './escape', 'one/./escape', 'one/\x00escape'):
            with self.subTest(path=value), self.assertRaisesRegex(AssertionError, 'Unsafe'):
                fixtures._v17_safe_path(value)

    def test_missing_retained_shard_fails_without_live_generation_fallback(self):
        self.backing_files()
        row = next(row for row in self.manifest['members'] if row['kind'] == 'reuse_retained_semantic_generation')
        (self.source / row['source_path']).unlink()
        self.assert_rejected('Missing V17 historical source payload')

    def test_changed_retained_shard_fails(self):
        self.backing_files()
        row = next(row for row in self.manifest['members'] if row['kind'] == 'reuse_retained_semantic_generation')
        target = self.source / row['source_path']
        raw = target.read_bytes()
        target.unlink()
        target.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        self.assert_rejected('payload drift')

    def test_changed_snapshot_and_reused_evidence_fail(self):
        self.backing_files()
        for kind in ('new_immutable_snapshot_same_git_blob', 'reuse_committed_evidence'):
            row = next(row for row in self.manifest['members'] if row['kind'] == kind)
            target = self.source / row['source_path']
            original = ROOT / row['source_path']
            target.unlink()
            target.write_bytes(original.read_bytes() + b'\n')
            with self.subTest(kind=kind):
                self.assert_rejected('payload drift')
            target.unlink()
            shutil.copyfile(original, target)

    def test_payload_symlinks_cannot_escape_fixed_sources(self):
        self.backing_files()
        row = self.manifest['members'][0]
        target = self.source / row['source_path']
        target.unlink()
        target.symlink_to(ROOT / row['source_path'])
        self.assert_rejected('Unsafe V17 historical source symlink')

    def test_each_support_dependency_drift_fails_before_validator_load(self):
        self.backing_files()
        support = self.support_files()
        for row in support['members']:
            target = self.source / row['source_path']
            raw = target.read_bytes()
            target.write_bytes(raw + b'\n')
            with self.subTest(module=row['module']), mock.patch.object(fixtures.importlib.util, 'spec_from_file_location') as load:
                with self.assertRaisesRegex(AssertionError, 'payload drift'):
                    fixtures.pinned_v17_validator(self.output, source_root=self.source)
                load.assert_not_called()
                self.assertFalse(self.output.exists())
            target.write_bytes(raw)

    def test_verified_imports_ignore_cached_live_modules_and_restore_module_cache(self):
        poisoned = {name: ModuleType(name) for name in (
            'illustration_runtime', 'illustration_audit', 'universal_scene_runtime')}
        for module in poisoned.values():
            module.canonical_json_bytes = lambda value: b'unrelated live implementation'
        previous_private = {key: value for key, value in sys.modules.items()
                            if key.startswith('_archived_photo_v17_')}
        with mock.patch.dict(sys.modules, poisoned):
            validator = fixtures.pinned_v17_validator(self.output)
            self.assertEqual(validator.canonical_json_bytes({'b': 2, 'a': 1}), b'{"a":1,"b":2}')
            for name, module in poisoned.items():
                self.assertIs(sys.modules[name], module)
            imported = validator.audit_composed_prompt.__globals__['__builtins__']['__import__']
            late = imported('universal_scene_runtime')
            self.assertEqual(Path(late.__file__), self.output / Path(fixtures.V17_PARENT_VALIDATOR).with_name('universal_scene_runtime.py'))
            self.assertIsNot(late, poisoned['universal_scene_runtime'])
        self.assertEqual({key: value for key, value in sys.modules.items()
                          if key.startswith('_archived_photo_v17_')}, previous_private)
