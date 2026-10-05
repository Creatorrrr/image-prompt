"""V15 records its actual optional delta without relaxing any old boundary."""
from __future__ import annotations
import copy
import hashlib
import json
import zipfile
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/motion-graphics-main-merge-20261004')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
from photo_prompt_fixtures import pinned_v17_validator


class MotionOptionalInventoryBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT, ILLUSTRATION, v
        live_root = ROOT
        cls.source_temp = tempfile.TemporaryDirectory(prefix='immutable-v15-parent-')
        cls.addClassCleanup(cls.source_temp.cleanup)
        source_root = Path(cls.source_temp.name)
        archive = live_root / 'docs/research-evidence/photo-prompt/seduction-expression-main-merge-20261005/V15-source-parent.zip'
        if hashlib.sha256(archive.read_bytes()).hexdigest() != 'dd1bb1f996c99b34f8e0eddc9fa6c3f7acc9ee1175d2d25b1cb56478f2163ecf':
            raise AssertionError('Frozen V15 source archive drift')
        with zipfile.ZipFile(archive) as saved:
            if any(Path(name).is_absolute() or '..' in Path(name).parts for name in saved.namelist()):
                raise AssertionError('Unsafe historical source path')
            saved.extractall(source_root)
        validator_path = source_root / 'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'
        v = pinned_v17_validator(source_root)
        descriptor = source_root / 'skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json'
        raw = descriptor.read_bytes()
        old_sha = json.loads(raw)['validator_contract']['sha256'].encode()
        if raw.count(old_sha) != 1:
            raise AssertionError('Historical descriptive seal is not unique')
        descriptor.write_bytes(raw.replace(old_sha, hashlib.sha256(validator_path.read_bytes()).hexdigest().encode(), 1))
        ROOT = source_root
        ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
        cls.validator_replay_path = validator_path

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.assets = self.directory / 'assets'
        self.assets.mkdir()
        for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path, self.assets / path.name)
        for name in ('universal_scene_baseline_v1.json', 'universal_scene_baseline_v2.json'):
            shutil.copyfile(ILLUSTRATION / 'assets' / name, self.assets / name)
        self.path = self.assets / 'photo_regression_baseline_v15.json'
        self.baseline = json.loads(self.path.read_bytes())
        self.output = (self.assets / 'photo_regression_baseline_v15_pack.json').read_bytes()
        self.pack = json.loads(self.output)[0]
        self.proof = json.loads((ROOT / EVIDENCE / 'V15-OPTIONAL-INVENTORY-PROOF.json').read_bytes())

    def validate(self, version=None):
        def replay(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.output)
            return SimpleNamespace(returncode=0, stderr='', stdout='')
        with mock.patch.object(v.subprocess, 'run', side_effect=replay), mock.patch.object(v, '__file__', str(self.validator_replay_path)):
            return v.validate_photo_regression_baseline(self.assets, baseline_version=version)

    def direct(self, *, repo=None, pack=None, raw=None):
        return v._validate_v15_motion_inventory_successor(
            self.assets, ROOT if repo is None else repo, self.baseline,
            self.pack if pack is None else pack, self.output if raw is None else raw)

    def test_registered_current_default_and_unregistered_future(self):
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v15')
        (self.assets / 'photo_regression_baseline_v18.json').write_text(json.dumps({'schema':'photo_regression_baseline/v18','status':'current'}))
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v15')
        with self.assertRaisesRegex(v.ValidationFailure,'unsupported'):
            self.validate(18)

    def test_actual_optional_delta_does_not_claim_unchanged_candidate_inventory(self):
        old = json.loads((self.assets / 'photo_regression_baseline_v14_pack.json').read_bytes())[0]
        self.assertEqual(old['authorial_core'], self.pack['authorial_core'])
        self.assertEqual(old['creative_controls'], self.pack['creative_controls'])
        self.assertEqual(old['authorial_composition'], self.pack['authorial_composition'])
        self.assertEqual(old['negative_en'], self.pack['negative_en'])
        self.assertNotEqual(old['slots']['composition']['candidates'], self.pack['slots']['composition']['candidates'])
        self.assertEqual(self.pack['slots']['composition']['candidates'][1]['adoption'],'optional')
        self.assertEqual(v._public_photo_candidate_count(old),64)
        self.assertEqual(v._public_photo_candidate_count(self.pack),64)
        self.assertNotIn('zero_pack_delta_transition',self.baseline)
        self.assertNotIn('metadata_only_transition',self.baseline)
        self.direct()

    def test_recomputed_pack_and_manifest_hashes_cannot_authorize_material_changes(self):
        baseline_raw = self.path.read_bytes()
        archive = self.assets / 'photo_regression_baseline_v15_pack.json'
        for kind in ('candidate','order','core','controls','composition','negative','privacy','adoption'):
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
            raw = (json.dumps([pack],ensure_ascii=False,indent=2)+'\n').encode()
            archive.write_bytes(raw)
            self.baseline.update(sha256=hashlib.sha256(raw).hexdigest(),pack_id=pack['pack_id'])
            with self.subTest(kind=kind), self.assertRaisesRegex(v.ValidationFailure,'pack binding'):
                self.direct(pack=pack,raw=raw)
            self.baseline = json.loads(baseline_raw)
        archive.write_bytes(self.output)

    def test_parent_lineage_provenance_and_transition_kind_are_fixed(self):
        original = copy.deepcopy(self.baseline)
        for field in ('data_commit','data_parent_commit','evidence_sha256','source_files'):
            self.baseline = copy.deepcopy(original)
            self.baseline['optional_inventory_transition'][field] = {} if field == 'source_files' else '0'*64
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure,'provenance'):
                self.direct()
        self.baseline = copy.deepcopy(original)
        for field in ('metadata_only_transition','zero_pack_delta_transition'):
            self.baseline[field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure,'relabel'):
                self.direct()
            del self.baseline[field]
        previous = self.assets / 'photo_regression_baseline_v14.json'
        previous.write_bytes(previous.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'pack binding'):
            self.direct()

    def test_fixed_proof_rejects_coordinated_rehash_and_raw_format_changes(self):
        repo = self.directory / 'proof-only'
        shutil.copytree(ROOT / EVIDENCE, repo / EVIDENCE)
        proof_path = repo / EVIDENCE / 'V15-OPTIONAL-INVENTORY-PROOF.json'
        for field in ('data_commit','reviewed_pack_leaf_deltas','source_inventory_after','current_pack_sha256'):
            proof = copy.deepcopy(self.proof)
            proof[field] = [] if field == 'reviewed_pack_leaf_deltas' else '0'*64
            proof_path.write_text(json.dumps(proof))
            self.baseline['optional_inventory_transition']['evidence_sha256'] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure,'immutable inventory proof'):
                self.direct(repo=repo)
        self.baseline['optional_inventory_transition']['evidence_sha256'] = v.PHOTO_V15_INVENTORY_PROOF_SHA256
        with self.assertRaisesRegex(v.ValidationFailure,'pack binding'):
            self.direct(raw=self.output+b'\n')

    def test_current_source_extra_missing_or_changed_cannot_hide_behind_manifest_hashes(self):
        repo = self.directory / 'complete-source'
        shutil.copytree(ROOT / EVIDENCE, repo / EVIDENCE)
        for name in self.proof['immutable_history']:
            target = repo / name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT / name,target)
        source = Path('skills/photo-prompt-image-generator/assets')
        for name in self.proof['source_inventory_after']:
            target = repo / source / name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT / source / name,target)
        for name in self.proof['active_semantic_shards']:
            target = repo / name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT / name,target)
        target = repo / source / 'photo_prompt_motion_graphics_extension.json'
        original = target.read_bytes()
        for kind in ('changed','missing','extra'):
            if kind == 'changed': target.write_bytes(original+b'\n')
            elif kind == 'missing': target.unlink()
            else: (repo / source / 'unregistered-extra.json').write_text('{}')
            with self.subTest(kind=kind), self.assertRaisesRegex(v.ValidationFailure,'exact DATA inventory'):
                self.direct(repo=repo)
            target.write_bytes(original)
            extra = repo / source / 'unregistered-extra.json'
            if extra.exists(): extra.unlink()
        source_archive = repo / self.proof['source_parent_archive']
        source_archive.write_bytes(source_archive.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'historical source archive'):
            self.direct(repo=repo)


if __name__ == '__main__':
    unittest.main()
