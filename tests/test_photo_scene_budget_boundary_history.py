"""V26 expands prose budgets while V25 keeps its original source and duties."""
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

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as validator


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


class SceneBudgetBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original = {name: globals()[name] for name in ('ROOT', 'ILLUSTRATION', 'validator')}
        frozen = tempfile.TemporaryDirectory(prefix='sealed-v26-scene-parent-')
        cls.addClassCleanup(frozen.cleanup)
        root = Path(frozen.name)
        archived = fixtures.archived_v26_validator(root, source_root=ROOT)
        (root / '.venv').symlink_to((ROOT / '.venv').resolve(), target_is_directory=True)
        cls.addClassCleanup(lambda: globals().update(original))
        globals().update(ROOT=root, ILLUSTRATION=root / 'skills/subculture-illustration-image-generator',
                         validator=archived)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='v26-boundary-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        self.proof = json.loads((ROOT / EVIDENCE / 'V26-SCENE-BUDGET-PROOF.json').read_bytes())
        self.manifest = json.loads((ROOT / self.proof['parent_manifest']).read_bytes())
        paths = {row['source_path'] for row in self.manifest['members']}
        paths.update(self.proof['source_files_after'])
        paths.update({self.proof['parent_manifest'], self.proof['previous_proof_path'],
                      str(EVIDENCE / 'V26-SCENE-BUDGET-PROOF.json')})
        paths.update(str(p.relative_to(ROOT)) for p in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v26.json').read_bytes())
        self.raw = (self.assets / 'photo_regression_baseline_v26_pack.json').read_bytes()
        self.pack = json.loads(self.raw)[0]

    @contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        original = path.readlink()
        path.unlink()
        if raw is not None:
            path.write_bytes(raw)
        try:
            yield
        finally:
            path.unlink(missing_ok=True)
            path.symlink_to(original)

    def validate(self, pack=None, raw=None):
        return validator._validate_v26_scene_budget_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_only_budget_and_pack_identity_change(self):
        self.validate()
        previous = json.loads((self.assets / 'photo_regression_baseline_v25_pack.json').read_bytes())[0]
        current = copy.deepcopy(self.pack)
        current['authorial_composition']['prompt_budget'] = previous['authorial_composition']['prompt_budget']
        current['pack_id'] = previous['pack_id']
        self.assertEqual(previous, current)
        self.assertEqual(6, len(self.proof['reviewed_pack_delta']))
        self.assertEqual(6, len(self.proof['reviewed_source_deltas']))
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))
        self.assertEqual(self.proof['frozen_inputs'], self.baseline['frozen_inputs'])

    def test_current_default_and_explicit_v26_are_registered(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')
        with mock.patch.object(validator.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 26):
                result = validator.validate_photo_regression_baseline(ILLUSTRATION / 'assets', baseline_version=version)
                self.assertEqual('photo_regression_baseline/v26', result['schema'])
                self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        with self.assertRaisesRegex(validator.ValidationFailure, 'unsupported photo baseline version'):
            validator.validate_photo_regression_baseline(self.assets, baseline_version=27)

    def test_real_current_command_reproduces_exact_v26(self):
        result = validator.validate_photo_regression_baseline(ILLUSTRATION / 'assets')
        self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        self.assertEqual(self.pack['pack_id'], result['pack_id'])

    def test_rehashed_candidate_meaning_control_negative_and_budget_changes_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v26_pack.json').relative_to(ROOT))
        for kind in ('candidate', 'order', 'core', 'controls', 'negative', 'budget', 'policy'):
            changed = copy.deepcopy(self.pack)
            candidates = next(row['candidates'] for row in changed['slots'].values() if len(row['candidates']) >= 2)
            if kind == 'candidate':
                candidates[0]['concept_terms'][0] += ' changed'
            elif kind == 'order':
                candidates.reverse()
            elif kind == 'core':
                changed['authorial_core']['subject'] += ' changed'
            elif kind == 'controls':
                changed['creative_controls']['extra'] = True
            elif kind == 'negative':
                changed['negative_en'] += ', changed'
            elif kind == 'budget':
                changed['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            else:
                changed['authorial_composition']['prompt_budget']['policy']['scene_coherence_outranks_concision'] = False
            changed['pack_id'] = validator._canonical_photo_pack_id(changed)
            raw = encoded([changed])
            baseline = copy.deepcopy(self.baseline)
            self.baseline.update(sha256=hashlib.sha256(raw).hexdigest(), pack_id=changed['pack_id'])
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaises(validator.ValidationFailure):
                self.validate(changed, raw)
            self.baseline = baseline

    def test_proof_runtime_data_and_historical_payload_mutations_rejected(self):
        row = next(row for row in self.manifest['members'] if row['kind'] == 'archived_parent_source')
        names = [str(EVIDENCE / 'V26-SCENE-BUDGET-PROOF.json'),
                 'skills/photo-prompt-image-generator/scripts/photo_contracts.py',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json',
                 row['source_path']]
        for name in names:
            original = (self.repo / name).read_bytes()
            with self.subTest(path=name), self.changed(name, original + b'\n'), self.assertRaises(validator.ValidationFailure):
                self.validate()

    def test_universal_descriptor_cannot_change_beyond_validator_binding(self):
        name = str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))
        value = json.loads((self.repo / name).read_bytes())
        value['extra'] = True
        with self.changed(name, encoded(value)), self.assertRaisesRegex(validator.ValidationFailure, 'universal descriptor'):
            self.validate()


class V25ArchivedSceneParentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix='sealed-v25-scene-parent-')
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Offline materialization invoked a subprocess')):
            cls.validator = fixtures.archived_v25_validator(cls.root, source_root=ROOT)
        (cls.root / '.venv').symlink_to((ROOT / '.venv').resolve(), target_is_directory=True)

    def test_real_original_command_reproduces_exact_v25(self):
        assets = self.root / ILLUSTRATION.relative_to(ROOT) / 'assets'
        expected = json.loads((assets / 'photo_regression_baseline_v25.json').read_bytes())
        result = self.validator.validate_photo_regression_baseline(assets)
        self.assertEqual('photo_regression_baseline/v25', result['schema'])
        self.assertEqual(expected['sha256'], result['sha256'])

    def test_original_budget_and_imports_remain_independent(self):
        assets = self.root / ILLUSTRATION.relative_to(ROOT) / 'assets'
        pack = json.loads((assets / 'photo_regression_baseline_v25_pack.json').read_bytes())[0]
        budget = pack['authorial_composition']['prompt_budget']
        self.assertEqual('photo-authorial-prompt-budget/v2', budget['contract_version'])
        self.assertEqual(640, budget['absolute_maximum_words'])
        hook = self.validator.__dict__['__builtins__']['__import__']
        for name in ('illustration_runtime', 'universal_scene_runtime'):
            self.assertEqual(self.root / ILLUSTRATION.relative_to(ROOT) / 'scripts' / (name + '.py'),
                             Path(hook(name).__file__))

    def test_missing_or_rehashed_parent_source_cannot_fall_back(self):
        original = (ROOT / fixtures.V25_PARENT_MANIFEST).read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input'
            path = source / fixtures.V25_PARENT_MANIFEST
            path.parent.mkdir(parents=True)
            for raw in (original, original + b'\n'):
                path.write_bytes(raw)
                output = Path(tmp) / 'output'
                with mock.patch('subprocess.Popen', side_effect=AssertionError('Fallback invoked a subprocess')):
                    with self.assertRaises(AssertionError):
                        fixtures.materialize_v25_parent_source(output, source_root=source)
                self.assertFalse(output.exists())

    def test_symlink_destination_is_rejected_before_copying(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / 'real'
            directory.mkdir()
            alias = Path(tmp) / 'alias'
            alias.symlink_to(directory, target_is_directory=True)
            with self.assertRaisesRegex(AssertionError, 'symlink'):
                fixtures.materialize_v25_parent_source(alias / 'output', source_root=ROOT)
            self.assertEqual([], list(directory.iterdir()))
