"""Append V13 while preserving every prior byte and frozen scene contract."""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/subculture-illustration-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import validate_illustration_assets as validator

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
previous_path = ASSETS / 'photo_regression_baseline_v12.json'
previous = json.loads(previous_path.read_text())
pack_path = HERE / 'current-boundary-v13-pack.json'
pack = json.loads(pack_path.read_text())[0]
preserved = {key: pack.get(key) for key in ('authorial_core', 'creative_controls', 'embodiment_review', 'authorial_composition', 'negative_en')}
digest = hashlib.sha256(json.dumps(preserved, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert digest == previous['preserved_contract_sha256']
assert validator._public_photo_candidate_count(pack) == previous['public_candidate_count']
assert pack['negative_en'] == previous['negative_en']
assert pack['contract_version'] == previous['contract_version']
assert pack['provenance']['omitted_private_fields'] == previous['private_fields_absent']
assert pack['pack_id'] == validator._canonical_photo_pack_id(pack)
assert all(sha(ROOT / name) == value for name, value in previous['frozen_inputs'].items())
row = copy.deepcopy(previous)
row.update({'schema': 'photo_regression_baseline/v13', 'created_at': '2026-10-05',
            'historical_baseline': {'path': previous_path.name, 'schema': previous['schema'], 'sha256': sha(previous_path)},
            'change_scope': 'seduction_expression_equivalent_and_current_visible_state_integration',
            'sha256': sha(pack_path), 'pack_id': pack['pack_id'],
            'purpose': 'Append the new authored corpus observation. Preserve V1-V12 bytes, frozen requester/core/controls/review inputs, scene and composition contract, public candidate count, negatives and private boundary. No native-pixel or user-acceptance claim.'})
row['command'][row['command'].index('--output-file') + 1] = '/tmp/subculture-illustration-photo-baseline-v13.json'
path = ASSETS / 'photo_regression_baseline_v13.json'
assert not path.exists()
path.write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
report = validator.validate_photo_regression_baseline(ASSETS)
(HERE / 'CURRENT-BOUNDARY-V13-VALIDATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False))
