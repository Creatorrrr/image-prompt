"""Additive V29 runtime boundary preserves every qualified V28 pack byte."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as validator


class RuntimeBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = fixtures._v29_transition(ROOT)
        cls.baseline = json.loads((ILLUSTRATION / 'assets/photo_regression_baseline_v29.json').read_bytes())
        cls.raw = (ILLUSTRATION / 'assets/photo_regression_baseline_v29_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='v29-runtime-boundary-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        paths = set(self.proof['source_files_after']) | set(self.proof['active_shards_after'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update((str(fixtures.V29_RUNTIME_PROOF), str(fixtures.V28_PARENT_SOURCE)))
        paths.update(str(path.relative_to(ROOT)) for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(ROOT / name)

    def validate(self, pack=None, raw=None):
        validator._validate_v29_runtime_successor(self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    @contextlib.contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        original = path.readlink()
        path.unlink()
        if raw is not None: path.write_bytes(raw)
        try: yield
        finally:
            path.unlink(missing_ok=True)
            path.symlink_to(original)

    def test_current_real_cli_and_independent_receipt_audit_preserve_v28_exactly(self):
        result = validator.validate_photo_regression_baseline(ILLUSTRATION / 'assets')
        self.assertEqual(result['schema'], 'photo_regression_baseline/v29')
        self.assertEqual(result['sha256'], self.proof['previous_pack_sha256'])
        self.assertEqual(self.raw, (ILLUSTRATION / 'assets/photo_regression_baseline_v28_pack.json').read_bytes())
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))

    def test_candidate_order_meaning_core_controls_negative_and_budget_cannot_be_rehashed(self):
        for key in ('order', 'meaning', 'core', 'controls', 'negative', 'budget'):
            pack = copy.deepcopy(self.pack)
            rows = next(row['candidates'] for row in pack['slots'].values() if len(row['candidates']) > 1)
            if key == 'order': rows.reverse()
            if key == 'meaning': rows[0]['concept_terms'][0] += ' changed'
            if key == 'core': pack['authorial_core']['subject'] += ' changed'
            if key == 'controls': pack['creative_controls']['extra'] = True
            if key == 'negative': pack['negative_en'] += ', changed'
            if key == 'budget': pack['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            pack['pack_id'] = validator._canonical_photo_pack_id(pack)
            raw = (json.dumps([pack], ensure_ascii=False, indent=2) + '\n').encode()
            with self.subTest(field=key), self.assertRaises(validator.ValidationFailure):
                self.validate(pack, raw)

    def test_runtime_data_and_active_shards_are_bound(self):
        names = ['skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json',
                 next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'):
                with self.assertRaises(validator.ValidationFailure): self.validate()

    def test_missing_or_rehashed_proof_and_parent_manifest_fail(self):
        for name in (str(fixtures.V29_RUNTIME_PROOF), str(fixtures.V28_PARENT_SOURCE)):
            for raw in (None, (ROOT / name).read_bytes() + b'\n'):
                with self.subTest(path=name, missing=raw is None), self.changed(name, raw):
                    with self.assertRaises((validator.ValidationFailure, OSError)): self.validate()

    def test_original_v28_runtime_snapshot_bytes_remain_hash_bound(self):
        row = next(row for row in self.parent['members']
                   if row['path'] == 'skills/photo-prompt-image-generator/scripts/prompt_generator.py')
        with self.changed(row['source_path'], (ROOT / row['source_path']).read_bytes() + b'\n'):
            with self.assertRaises(validator.ValidationFailure): self.validate()

    def test_historical_resolver_accepts_only_the_sealed_runtime_transition(self):
        row = next(row for row in self.parent['members']
                   if row['path'] == 'skills/photo-prompt-image-generator/scripts/prompt_generator.py')
        with tempfile.TemporaryDirectory(prefix='v29-history-regular-') as temporary:
            root = Path(temporary).resolve()
            for name in (str(fixtures.V29_RUNTIME_PROOF), str(fixtures.V28_PARENT_SOURCE), row['path'], row['source_path']):
                target = root / name; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            requested = dict(row, source_path=row['path'])
            self.assertEqual(fixtures._v24_verified_payload(root, requested), (ROOT / row['source_path']).read_bytes())
            path = root / row['path']; path.write_bytes(path.read_bytes() + b'\n')
            with self.assertRaises(AssertionError): fixtures._v24_verified_payload(root, requested)


if __name__ == '__main__': unittest.main()
