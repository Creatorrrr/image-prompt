"""Horror's additive V31 qualification preserves exact V30 and owner duties."""
from __future__ import annotations
import contextlib
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ILL = ROOT / 'skills/subculture-illustration-image-generator'
sys.path.insert(0, str(ILL / 'scripts'))
import validate_illustration_assets as validator
from tests import photo_prompt_fixtures as fixtures

class HorrorMainBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = fixtures._v31_transition(ROOT)
        cls.baseline = json.loads((ILL / 'assets/photo_regression_baseline_v31.json').read_bytes())
        cls.raw = (ILL / 'assets/photo_regression_baseline_v31_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='horror-v31-boundary-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / ILL.relative_to(ROOT) / 'assets'
        paths = set(self.proof['source_files_after']) | set(self.proof['active_shards_after'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update([str(fixtures.V31_HORROR_PROOF), str(fixtures.V30_PARENT_SOURCE), str(fixtures.V30_WATER_PROOF)])
        paths.update(str(p.relative_to(ROOT)) for p in (ILL / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILL / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(ROOT / name)

    def validate(self, pack=None, raw=None):
        validator._validate_v31_horror_main_successor(self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    @contextlib.contextmanager
    def changed(self, name, raw, mode=None):
        path = self.repo / name
        original = path.readlink()
        path.unlink()
        if raw is not None:
            path.write_bytes(raw)
            if mode is not None:
                path.chmod(mode)
        try:
            yield
        finally:
            path.unlink(missing_ok=True)
            path.symlink_to(original)

    def test_current_public_cli_receipt_and_exact_reviewed_delta(self):
        result = validator.validate_photo_regression_baseline(ILL / 'assets')
        self.assertEqual(result['schema'], 'photo_regression_baseline/v31')
        self.assertEqual(result['sha256'], self.proof['current_pack_sha256'])
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))
        previous = json.loads((ILL / 'assets/photo_regression_baseline_v30_pack.json').read_bytes())[0]
        for key in self.proof['preserved_contract_keys']:
            with self.subTest(key=key):
                self.assertEqual(previous[key], self.pack[key])

    def test_current_sources_and_byte_exact_v30_parent_pass(self):
        self.validate()
        self.assertEqual(1307, self.parent['member_count'])
        self.assertEqual(155, self.proof['horror_candidates'])
        self.assertEqual(155, self.proof['horror_profiles'])

    def test_unreviewed_candidate_order_meaning_core_controls_or_budget_fail(self):
        for kind in ('meaning', 'order', 'core', 'controls', 'budget', 'negative'):
            pack = copy.deepcopy(self.pack)
            rows = pack['slots']['anatomical_connection']['candidates']
            if kind == 'meaning': rows[0]['concept_terms'][0] += ' changed'
            if kind == 'order': rows.reverse()
            if kind == 'core': pack['authorial_core']['subject'] += ' changed'
            if kind == 'controls': pack['creative_controls']['extra'] = True
            if kind == 'budget': pack['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            if kind == 'negative': pack['negative_en'] += ', changed'
            pack['pack_id'] = validator._canonical_photo_pack_id(pack)
            raw = (json.dumps([pack], ensure_ascii=False, indent=2) + '\n').encode()
            with self.subTest(kind=kind), self.assertRaises(validator.ValidationFailure):
                self.validate(pack, raw)

    def test_horror_water_runtime_registration_and_shards_are_bound(self):
        names = ['skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_horror.json',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_water_relations.json',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json',
                 'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py',
                 next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

    def test_undeclared_source_cannot_enter_current_inventory(self):
        (self.repo / 'skills/photo-prompt-image-generator/assets/photo_prompt_unrelated_extension.json').write_text('{}')
        with self.assertRaises(validator.ValidationFailure):
            self.validate()

    def test_missing_or_rehashed_proof_and_parent_fail(self):
        for name in (str(fixtures.V31_HORROR_PROOF), str(fixtures.V30_PARENT_SOURCE)):
            for raw in (None, (ROOT / name).read_bytes() + b'\n'):
                with self.subTest(path=name, missing=raw is None), self.changed(name, raw):
                    with self.assertRaises((validator.ValidationFailure, OSError)):
                        self.validate()

    def test_original_v30_source_bytes_and_mode_cannot_drift(self):
        row = next(row for row in self.parent['members'] if row['path'] == 'tests/photo_prompt_fixtures.py')
        name = row['source_path']; raw = (ROOT / name).read_bytes()
        for payload, mode in ((raw + b'\n', 0o644), (raw, 0o600)):
            with self.subTest(mode=mode), self.changed(name, payload, mode):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

if __name__ == '__main__':
    unittest.main()
