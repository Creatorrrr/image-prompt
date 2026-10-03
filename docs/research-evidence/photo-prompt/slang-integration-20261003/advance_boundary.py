"""Append V8 corpus observation, preserving every earlier record and input byte."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/subculture-illustration-image-generator/assets'
previous_path = ASSETS / 'photo_regression_baseline_v7.json'
previous = json.loads(previous_path.read_text())
current = dict(previous)
current['schema'] = 'photo_regression_baseline/v8'
current['created_at'] = '2026-10-03'
current['historical_baseline'] = {'path': previous_path.name, 'schema': previous['schema'],
    'sha256': hashlib.sha256(previous_path.read_bytes()).hexdigest()}
current['change_scope'] = 'reviewed_slang_visual_alternatives_and_atomic_relations'
command = list(previous['command'])
output = HERE / 'current-boundary-pack.json'
command[command.index('--output-file') + 1] = str(output)
env = os.environ.copy(); env['GEMINI_API_KEY'] = ''; env['GOOGLE_API_KEY'] = ''
result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
if result.returncode: raise RuntimeError(result.stderr or result.stdout)
raw = output.read_bytes(); pack = json.loads(raw)[0]
contract = {k: pack.get(k) for k in ('authorial_core', 'creative_controls', 'embodiment_review', 'authorial_composition', 'negative_en')}
digest = hashlib.sha256(json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert digest == previous['preserved_contract_sha256'], 'Frozen scene changed'
for path, expected in previous['frozen_inputs'].items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert pack['negative_en'] == previous['negative_en']
assert pack['contract_version'] == previous['contract_version']
count = sum(len(x['candidates']) for x in pack['slots'].values())
assert count == previous['public_candidate_count']
current['sha256'] = hashlib.sha256(raw).hexdigest()
current['pack_id'] = pack['pack_id']
current['command'] = list(previous['command'])
current['command'][current['command'].index('--output-file') + 1] = '/tmp/subculture-illustration-photo-baseline-v8.json'
current['purpose'] = 'Append the current corpus observation after reviewed slang alternative integration. Preserve V1-V7 bytes, the four frozen authoring inputs, scene and composition contract, candidate cap and public provenance boundary. This observation makes no new pixel-quality claim.'
(ASSETS / 'photo_regression_baseline_v8.json').write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n')
universal_path = ASSETS / 'universal_scene_baseline_v2.json'
universal = json.loads(universal_path.read_text())
universal['validator_contract']['sha256'] = hashlib.sha256((ASSETS.parent / 'scripts/validate_illustration_assets.py').read_bytes()).hexdigest()
# The existing descriptor is compact JSON. Only its validator-byte binding
# changes; its source oracle, scene expectations and manifest stay intact.
universal_path.write_text(json.dumps(universal, ensure_ascii=False, separators=(',', ':')) + '\n')
print(json.dumps({'pack_sha256': current['sha256'], 'pack_id': current['pack_id'], 'public_candidate_count': count,
    'frozen_contract_preserved': True, 'previous_record_preserved': True}))
