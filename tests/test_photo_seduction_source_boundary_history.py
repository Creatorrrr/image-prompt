"""V16 preserves candidate and scene bytes while binding the exact merged DATA."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/seduction-expression-main-merge-20261005')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as v
from tests.photo_prompt_fixtures import archived_v16_validator


class SeductionSourceBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.historical_repo = Path(temporary.name)
        cls.validator = archived_v16_validator(cls.historical_repo)
        cls.validator.ValidationFailure = v.ValidationFailure

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.assets = self.directory / 'assets'
        self.assets.mkdir()
        for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path, self.assets / path.name)
        for name in ('universal_scene_baseline_v1.json', 'universal_scene_baseline_v2.json'):
            shutil.copyfile(self.historical_repo / 'skills/subculture-illustration-image-generator/assets' / name,
                            self.assets / name)
        self.path = self.assets / 'photo_regression_baseline_v16.json'
        self.baseline = json.loads(self.path.read_bytes())
        self.output = (self.assets / 'photo_regression_baseline_v16_pack.json').read_bytes()
        self.pack = json.loads(self.output)[0]
        self.proof = json.loads((ROOT / EVIDENCE / 'V16-FIVE-BINDING-PROOF.json').read_bytes())

    def validate(self, version=None):
        def replay(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.output)
            return SimpleNamespace(returncode=0, stderr='', stdout='')
        with mock.patch.object(self.validator.subprocess, 'run', side_effect=replay):
            return self.validator.validate_photo_regression_baseline(self.assets, baseline_version=version)

    def direct(self, *, repo=None, pack=None, raw=None):
        return self.validator._validate_v16_seduction_source_successor(
            self.assets, self.historical_repo if repo is None else repo, self.baseline,
            self.pack if pack is None else pack, self.output if raw is None else raw)

    def test_registered_default_and_unregistered_future(self):
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v16')
        (self.assets / 'photo_regression_baseline_v17.json').write_text('{}')
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v16')
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported'):
            self.validate(17)

    def test_all_candidate_order_scene_and_privacy_fields_survive(self):
        old = json.loads((self.assets / 'photo_regression_baseline_v15_pack.json').read_bytes())[0]
        current = copy.deepcopy(self.pack)
        self.assertEqual(len(self.proof['reviewed_binding_deltas']), 5)
        for path in (('core_retrieval', 'canonical_sha256'), ('core_retrieval', 'slot_corpus_sha256'),
                     ('core_retrieval', 'slot_ownership_sha256'), ('pack_id',), ('provenance', 'tags_hash')):
            left, right = old, current
            for key in path[:-1]:
                left, right = left[key], right[key]
            self.assertNotEqual(left[path[-1]], right[path[-1]])
            del left[path[-1]], right[path[-1]]
        self.assertEqual(old, current)
        self.direct()

    def test_coordinated_pack_and_manifest_rehash_cannot_accept_material_changes(self):
        archive = self.assets / 'photo_regression_baseline_v16_pack.json'
        original = copy.deepcopy(self.baseline)
        for kind in ('candidate', 'order', 'core', 'controls', 'composition', 'negative', 'privacy', 'adoption'):
            pack = copy.deepcopy(self.pack)
            rows = next(s['candidates'] for s in pack['slots'].values() if len(s['candidates']) >= 2)
            if kind == 'candidate': rows[0]['concept_terms'][0] += ' changed'
            elif kind == 'order': rows.reverse()
            elif kind == 'core': pack['authorial_core']['subject'] += ' changed'
            elif kind == 'controls': pack['creative_controls']['extra'] = True
            elif kind == 'composition': pack['authorial_composition']['extra'] = True
            elif kind == 'negative': pack['negative_en'] += ', changed'
            elif kind == 'privacy': pack['provenance']['private_routing_exposed'] = True
            else: rows[0]['adoption'] = 'required'
            pack['pack_id'] = v._canonical_photo_pack_id(pack)
            raw = (json.dumps([pack], ensure_ascii=False, indent=2) + '\n').encode()
            archive.write_bytes(raw)
            self.baseline.update(sha256=hashlib.sha256(raw).hexdigest(), pack_id=pack['pack_id'])
            with self.subTest(kind=kind), self.assertRaisesRegex(v.ValidationFailure, 'pack binding'):
                self.direct(pack=pack, raw=raw)
            self.baseline = copy.deepcopy(original)

    def test_fixed_proof_and_transition_cannot_be_reclassified(self):
        repo = self.directory / 'proof-only'
        proof_path = repo / EVIDENCE / 'V16-FIVE-BINDING-PROOF.json'
        proof_path.parent.mkdir(parents=True)
        proof = copy.deepcopy(self.proof)
        proof['reviewed_binding_deltas'] = []
        proof_path.write_text(json.dumps(proof))
        self.baseline['authored_metadata_ownership_transition']['evidence_sha256'] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(v.ValidationFailure, 'immutable source proof'):
            self.direct(repo=repo)
        self.baseline = json.loads(self.path.read_bytes())
        for field in ('metadata_only_transition', 'zero_pack_delta_transition', 'optional_inventory_transition'):
            self.baseline[field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure, 'relabel'):
                self.direct()
            del self.baseline[field]

    def test_original_v15_rejects_live_v16_source_inventory(self):
        old_baseline = json.loads((self.assets / 'photo_regression_baseline_v15.json').read_bytes())
        old_output = (self.assets / 'photo_regression_baseline_v15_pack.json').read_bytes()
        with self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
            self.validator._validate_v15_motion_inventory_successor(
                self.assets, self.historical_repo, old_baseline, json.loads(old_output)[0], old_output)


if __name__ == '__main__':
    unittest.main()
