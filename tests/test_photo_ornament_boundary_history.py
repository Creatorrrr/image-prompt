"""V22 accepts reviewed DATA changes and rejects coordinated rebaselining."""
import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/gothic-sharded-main-merge-20261005')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as v


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class OrnamentBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT, ILLUSTRATION, v
        cls.live_root = ROOT
        temp = tempfile.TemporaryDirectory(prefix='immutable-v22-parent-')
        cls.addClassCleanup(temp.cleanup)
        ROOT = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Historical fixture invoked a subprocess')):
            v = fixtures.archived_validator_with_v24_source(ROOT, version=22, source_root=cls.live_root)
        ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
        cls.proof = json.loads((ROOT / EVIDENCE / 'V22-ORNAMENT-BINDING-PROOF.json').read_bytes())

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        paths = set()
        for field in ('immutable_history', 'historical_dependencies', 'source_parent_files',
                      'source_files', 'active_semantic_shards', 'active_visual_shards', 'retained_visual_shards'):
            paths.update(self.proof[field])
        paths.update(str(p.relative_to(ROOT)) for p in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.update([str(EVIDENCE / 'V22-ORNAMENT-BINDING-PROOF.json'),
                      self.proof['source_parent_manifest'], self.proof['maintenance_path'],
                      str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))])
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v22.json').read_bytes())
        self.raw = (self.assets / 'photo_regression_baseline_v22_pack.json').read_bytes()
        self.pack = json.loads(self.raw)[0]

    @contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        existed = path.exists()
        if path.is_symlink():
            path.unlink()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        try:
            yield path
        finally:
            path.unlink()
            if existed:
                path.symlink_to(ROOT / name)

    def validate(self, pack=None, raw=None):
        return v._validate_v22_ornament_data_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_only_six_metadata_leaves_and_two_optional_lists_change(self):
        self.validate()
        before = json.loads((self.assets / 'photo_regression_baseline_v21_pack.json').read_bytes())[0]
        self.assertEqual(6, len(self.proof['reviewed_pack_delta']['bindings']))
        self.assertEqual(2, len(self.proof['reviewed_pack_delta']['optional_blocks']))
        self.assertEqual(64, v._public_photo_candidate_count(self.pack))
        for name in before['slots']:
            self.assertEqual(before['slots'][name]['candidates'], self.pack['slots'][name]['candidates'])
        for name in ('authorial_core', 'creative_controls', 'authorial_composition', 'negative_en'):
            self.assertEqual(before[name], self.pack[name])

    def test_current_default_and_explicit_v22_are_registered(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')
        with mock.patch.object(v.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 22):
                result = v.validate_photo_regression_baseline(ILLUSTRATION / 'assets', baseline_version=version)
                self.assertEqual('photo_regression_baseline/v22', result['schema'])
                self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported photo baseline version'):
            v.validate_photo_regression_baseline(self.assets, baseline_version=23)

    def test_rehashed_slot_core_owner_negative_privacy_and_optional_contracts_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v22_pack.json').relative_to(ROOT))
        for kind in ('candidate', 'order', 'core', 'owner', 'controls', 'negative', 'privacy', 'optional', 'optional_order'):
            changed = copy.deepcopy(self.pack)
            rows = next(slot['candidates'] for slot in changed['slots'].values() if len(slot['candidates']) >= 2)
            if kind == 'candidate': rows[0]['concept_terms'][0] += ' altered'
            elif kind == 'order': rows.reverse()
            elif kind == 'core': changed['authorial_core']['subject'] += ' altered'
            elif kind == 'owner': changed['core_retrieval']['slot_ownership_sha256'] = '0' * 64
            elif kind == 'controls': changed['creative_controls']['extra'] = True
            elif kind == 'negative': changed['negative_en'] += ', altered'
            elif kind == 'privacy': changed['provenance']['private_routing_exposed'] = True
            elif kind == 'optional': changed['visual_concept_candidates']['candidates'][0]['id'] += '-altered'
            else: changed['semantic_clarification']['candidates'].reverse()
            changed['pack_id'] = v._canonical_photo_pack_id(changed)
            raw = (json.dumps([changed], ensure_ascii=False, indent=2) + '\n').encode()
            self.baseline.update(sha256=digest(raw), pack_id=changed['pack_id'])
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaisesRegex(v.ValidationFailure, 'exact reviewed pack'):
                self.validate(changed, raw)

    def test_fixed_proof_rejects_coordinated_rehash(self):
        for field, value in (('source_commit', '0' * 40), ('source_tree', '0' * 40),
                             ('reviewed_source_deltas', []), ('reviewed_pack_delta', {}),
                             ('source_inventory_after', {}), ('active_visual_shards', {}),
                             ('current_pack_sha256', '0' * 64)):
            changed = copy.deepcopy(self.proof)
            changed[field] = value
            raw = json.dumps(changed).encode()
            self.baseline['ornament_data_transition']['evidence_sha256'] = digest(raw)
            with self.subTest(field=field), self.changed(EVIDENCE / 'V22-ORNAMENT-BINDING-PROOF.json', raw), self.assertRaisesRegex(v.ValidationFailure, 'immutable ornament proof'):
                self.validate()

    def test_sources_and_unregistered_extra_data_rejected(self):
        names = self.proof['added_source_files'] + [row['path'] for row in self.proof['reviewed_source_deltas']]
        names += ['skills/photo-prompt-image-generator/scripts/visual_profile_index_storage.py']
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaisesRegex(v.ValidationFailure, 'source_parent_files|DATA inventory|source binding'):
                self.validate()
        with self.changed('skills/photo-prompt-image-generator/assets/unexpected.json', b'{}'), self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
            self.validate()

    def test_active_and_retained_vector_shards_missing_extra_and_mutation_rejected(self):
        for field in ('active_semantic_shards', 'active_visual_shards', 'retained_visual_shards'):
            name = next(iter(self.proof[field]))
            for path, raw in ((name, (ROOT / name).read_bytes() + b' '),
                              (str(Path(name).parent / 'shard-999.json'), b'{}')):
                with self.subTest(field=field, path=path), self.changed(path, raw), self.assertRaises(v.ValidationFailure):
                    self.validate()
        name = next(iter(self.proof['active_visual_shards']))
        (self.repo / name).unlink()
        with self.assertRaises((FileNotFoundError, v.ValidationFailure)):
            self.validate()

    def test_parent_history_maintenance_and_transition_binding_are_immutable(self):
        for name in (self.proof['source_parent_manifest'], self.proof['previous_proof_path'],
                     self.proof['universal_v2_before_path'], self.proof['maintenance_path'],
                     'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v21.json'):
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaises(v.ValidationFailure):
                self.validate()
        original = copy.deepcopy(self.baseline)
        self.baseline['ornament_data_transition']['source_commit'] = 'PENDING'
        with self.assertRaisesRegex(v.ValidationFailure, 'ornament provenance'):
            self.validate()
        self.baseline = original
        self.baseline['visual_index_storage_transition'] = {}
        with self.assertRaisesRegex(v.ValidationFailure, 'cannot relabel'):
            self.validate()

    def test_v21_still_rejects_current_expanded_data(self):
        baseline = json.loads((self.assets / 'photo_regression_baseline_v21.json').read_bytes())
        raw = (self.assets / 'photo_regression_baseline_v21_pack.json').read_bytes()
        with self.assertRaises(v.ValidationFailure):
            v._validate_v21_visual_storage_successor(self.assets, ROOT, baseline, json.loads(raw)[0], raw)


if __name__ == '__main__':
    unittest.main()
