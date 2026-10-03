"""Appearance alternatives advance corpus history without rewriting frozen meaning."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/subculture-illustration-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import validate_illustration_assets as validator


class AppearanceBoundaryHistoryTests(unittest.TestCase):
    def test_predecessor_and_frozen_scene_are_preserved(self):
        previous_path = SKILL / 'assets/photo_regression_baseline_v8.json'
        previous = json.loads(previous_path.read_text())
        current = json.loads((SKILL / 'assets/photo_regression_baseline_v9.json').read_text())
        self.assertEqual(hashlib.sha256(previous_path.read_bytes()).hexdigest(),
                         'f5164a7cbc5ade0167dafc3733be189d1c2bc433c2f0e38a8bc81a52d5414935')
        self.assertEqual(current['historical_baseline'], {
            'path': previous_path.name, 'schema': previous['schema'],
            'sha256': hashlib.sha256(previous_path.read_bytes()).hexdigest(),
        })
        for key in ('frozen_inputs', 'preserved_contract_sha256', 'contract_version',
                    'public_candidate_count', 'negative_en', 'private_fields_absent'):
            self.assertEqual(current[key], previous[key], key)
        output_index = current['command'].index('--output-file') + 1
        self.assertEqual([x for i, x in enumerate(current['command']) if i != output_index],
                         [x for i, x in enumerate(previous['command']) if i != output_index])
        for path, digest in current['frozen_inputs'].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)

    def test_invalid_lineage_or_frozen_meaning_fails_before_replay(self):
        for mutation in ('historical_baseline', 'preserved_contract_sha256'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                assets = Path(directory)
                for path in (SKILL / 'assets').glob('photo_regression_baseline_v*.json'):
                    shutil.copyfile(path, assets / path.name)
                shutil.copyfile(SKILL / 'assets/universal_scene_baseline_v1.json',
                                assets / 'universal_scene_baseline_v1.json')
                path = assets / 'photo_regression_baseline_v9.json'
                row = json.loads(path.read_text())
                if mutation == 'historical_baseline':
                    row[mutation]['sha256'] = '0' * 64
                    expected = 'current photo successor lineage mismatch'
                else:
                    row[mutation] = '0' * 64
                    expected = 'photo successor changed the frozen scene or public boundary'
                path.write_text(json.dumps(row))
                with patch.object(validator.subprocess, 'run') as replay:
                    with self.assertRaisesRegex(validator.ValidationFailure, expected):
                        validator.validate_photo_regression_baseline(assets)
                    replay.assert_not_called()


if __name__ == '__main__':
    unittest.main()
