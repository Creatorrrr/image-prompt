"""Current corpus baseline advances without replacing historical observations."""
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


class ReligionIconographyBoundaryHistoryTests(unittest.TestCase):
    def test_prior_photo_observations_are_byte_immutable(self):
        hashes = {
            1: '3db499287144390ea4724a916069ef1a01b7b6d86064cebee56dd4a496d252c8',
            2: '52034126911f4ac042f1a03efde05c27eed74e65c878c7db9d27fed9225ded2f',
            3: 'f5330bcee1a8bfdf92861152ab941cded669269cda4de4d6a7183c3933dfacd5',
            4: '0cea827c27183e08db36a29ecd443f7264d183953e9be24281199ea47fa7f127',
            5: '96d13676e1c0635a35ac27d03ddea87859c92551c1105211f3556e15cadc5473',
        }
        for version, digest in hashes.items():
            with self.subTest(version=version):
                path = SKILL / 'assets' / f'photo_regression_baseline_v{version}.json'
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
        # The two branches independently authored V6; retain both byte records.
        parallel = {
            'photo_regression_baseline_v6.json': 'c1285744b58639b4b31bf665dcd3dc0ccbf48bc0c0197b662142842cbe54421d',
            'photo_regression_baseline_v6_religion_iconography.json': '691aca1ba73acb0e6324596ab10d5c96356f9bdfc981f9dfd46618b4d0eb40ca',
        }
        for filename, digest in parallel.items():
            self.assertEqual(hashlib.sha256((SKILL / 'assets' / filename).read_bytes()).hexdigest(), digest)

    def test_current_lineage_mutation_fails_before_any_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            names = ['universal_scene_baseline_v1.json'] + [
                f'photo_regression_baseline_v{v}.json' for v in range(1, 8)]
            names.append('photo_regression_baseline_v6_religion_iconography.json')
            for name in names:
                shutil.copyfile(SKILL / 'assets' / name, assets / name)
            path = assets / 'photo_regression_baseline_v7.json'
            original = json.loads(path.read_text())
            for field, value in (('path', 'photo_regression_baseline_v4.json'),
                                 ('sha256', '0' * 64)):
                with self.subTest(field=field):
                    changed = json.loads(json.dumps(original))
                    changed['historical_baseline'][field] = value
                    path.write_text(json.dumps(changed))
                    with patch.object(validator.subprocess, 'run') as run:
                        with self.assertRaisesRegex(validator.ValidationFailure,
                                'current photo baseline lineage mismatch'):
                            validator.validate_photo_regression_baseline(assets)
                        run.assert_not_called()

    def test_parallel_local_observation_tampering_is_rejected_before_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            for path in (SKILL / 'assets').glob('photo_regression_baseline_v*.json'):
                shutil.copyfile(path, assets / path.name)
            shutil.copyfile(SKILL / 'assets/universal_scene_baseline_v1.json',
                assets / 'universal_scene_baseline_v1.json')
            path = assets / 'photo_regression_baseline_v6_religion_iconography.json'
            path.write_text(path.read_text() + '\n')
            with patch.object(validator.subprocess, 'run') as run:
                with self.assertRaisesRegex(validator.ValidationFailure,
                        'merged photo parallel baseline or frozen contract drift'):
                    validator.validate_photo_regression_baseline(assets)
                run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
