"""Current corpus observation advances without rewriting scene holdouts."""
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


class SlangBoundaryHistoryTests(unittest.TestCase):
    def test_v7_and_all_four_frozen_inputs_are_preserved_byte_for_byte(self):
        old = SKILL / 'assets/photo_regression_baseline_v7.json'
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), '06d092e166d4a8be2e956abb552fe9fd58eb0401d71c964ff071e356a11f33ca')
        current = json.loads((SKILL / 'assets/photo_regression_baseline_v8.json').read_text())
        previous = json.loads(old.read_text())
        self.assertEqual(current['historical_baseline'], {'path': old.name, 'schema': previous['schema'], 'sha256': hashlib.sha256(old.read_bytes()).hexdigest()})
        for key in ('frozen_inputs', 'preserved_contract_sha256', 'contract_version', 'public_candidate_count', 'negative_en', 'private_fields_absent'):
            self.assertEqual(current[key], previous[key])
        for path, digest in current['frozen_inputs'].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)

    def test_invalid_successor_lineage_fails_before_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            for path in (SKILL / 'assets').glob('photo_regression_baseline_v*.json'):
                shutil.copyfile(path, assets / path.name)
            shutil.copyfile(SKILL / 'assets/universal_scene_baseline_v1.json', assets / 'universal_scene_baseline_v1.json')
            path = assets / 'photo_regression_baseline_v8.json'
            row = json.loads(path.read_text()); row['historical_baseline']['sha256'] = '0' * 64
            path.write_text(json.dumps(row))
            with patch.object(validator.subprocess, 'run') as run:
                with self.assertRaisesRegex(validator.ValidationFailure, 'current photo successor lineage mismatch'):
                    validator.validate_photo_regression_baseline(assets)
                run.assert_not_called()


if __name__ == '__main__': unittest.main()
