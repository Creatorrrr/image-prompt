"""Review an intentional current-corpus checksum refresh with fixed meanings.

The immutable V1-V4 history and all frozen lexical/pixel holdouts are untouched.
The current V5 full-pack checksum includes corpus metadata. Only that checksum
and its pack ID may advance after exact comparison of every remaining value.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
ASSETS = ROOT / 'skills/subculture-illustration-image-generator/assets'
path = ASSETS / 'photo_regression_baseline_v5.json'
receipt = OUT / 'CURRENT-BOUNDARY-REFRESH.json'
if receipt.exists():
    raise SystemExit('The reviewed current-boundary refresh already ran.')
raw = path.read_bytes()
baseline = json.loads(raw)
previous_raw = (ROOT / 'docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/photo-boundary-v5.actual.json').read_bytes()
assert hashlib.sha256(previous_raw).hexdigest() == baseline['sha256']
previous = json.loads(previous_raw)[0]
command = list(baseline['command'])
current_path = OUT / 'photo-boundary.final.json'
command[command.index('--output-file') + 1] = str(current_path)
environment = os.environ.copy()
environment['GEMINI_API_KEY'] = ''
environment['GOOGLE_API_KEY'] = ''
subprocess.run(command, cwd=ROOT, env=environment, check=True, capture_output=True, text=True)
current_raw = current_path.read_bytes()
current = json.loads(current_raw)[0]

def differences(a, b, prefix=''):
    if type(a) is not type(b):
        return [prefix]
    if isinstance(a, dict):
        delta=[]
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                delta.append(prefix + '/' + key)
            else:
                delta.extend(differences(a[key], b[key], prefix + '/' + key))
        return delta
    if isinstance(a, list):
        if len(a) != len(b):
            return [prefix]
        return [item for i, (x,y) in enumerate(zip(a,b))
                for item in differences(x,y,prefix + '/' + str(i))]
    return [prefix] if a != b else []

delta = differences(previous, current)
allowed = {'/pack_id', '/provenance/tags_hash', '/core_retrieval/canonical_sha256',
           '/core_retrieval/retrieval', '/core_retrieval/slot_corpus_sha256',
           '/core_retrieval/slot_ownership_sha256'}
assert set(delta) == allowed, delta
assert current['slots'] == previous['slots']
assert current['authorial_core'] == previous['authorial_core']
assert current['negative_en'] == previous['negative_en']
count = sum(len(slot['candidates']) for slot in current['slots'].values())
assert count == baseline['public_candidate_count'] == 64
new_sha = hashlib.sha256(current_raw).hexdigest()
old_baseline_snapshot = OUT / 'photo-regression-v5.before.json'
old_baseline_snapshot.write_bytes(raw)
text = raw.decode()
text = text.replace(baseline['sha256'], new_sha).replace(baseline['pack_id'], current['pack_id'])
updated = json.loads(text)
assert {key:value for key,value in updated.items() if key not in {'sha256','pack_id'}} == {
    key:value for key,value in baseline.items() if key not in {'sha256','pack_id'}}
path.write_text(text)
record = dict(schema_version='reviewed-current-corpus-boundary-refresh/v1',status='PASS',
    changed_baseline_fields=['sha256','pack_id'], reviewed_pack_differences=delta,
    complete_candidate_inventory_exact=True, candidate_count=64,
    frozen_core_exact=True, negative_exact=True,
    frozen_lexical_and_pixel_holdouts_rewritten=False,
    before=dict(sha256=baseline['sha256'],pack_id=baseline['pack_id']),
    after=dict(sha256=new_sha,pack_id=current['pack_id']),
    original_baseline_sha256=hashlib.sha256(raw).hexdigest(),
    current_baseline_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    preserved_history=[dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                       for p in sorted(ASSETS.glob('photo_regression_baseline_v[1-4].json'))])
receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False))
