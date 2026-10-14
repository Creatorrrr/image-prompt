"""Preserve the exact independently verified one-record research acceptance."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'native_batches/review08250-11128-04'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


report = json.loads((OUT / 'ROOT-VERIFICATION-01.json').read_bytes())
assert len(report['admission_cases']) == 20 and len(report['locked_properties']) == 10
assert len(report['actual_original_binding_consumers']) == 6
assert report['effect_assignment_conflicts'] == 0
assert raw(OUT / 'BATCH.json') == '27aac21c0b5366b044dd890df315880ba523e9b5560e2b558079b1907b51b55e'
assert raw(HERE / 'authored/native_fresh_08250_11128_04_checks.json') == 'e1abc2bf691f150527ef0dd727cab0385372f3b9b89bd3c77b6ca544a15f0a63'
assert raw(HERE / 'worker-notes/native-fresh-08250-11128-04.json') == 'ee1c75dd8aa9e2fc44c4d9ba1418a017a4604ad5e92c90d03cb2c95314f155a5'
paths = {path for path in OUT.iterdir() if path.is_file()}
paths.update(HERE / name for name in [Path(__file__).name,
    'authored/native_fresh_08250_11128_04.py',
    'authored/native_fresh_08250_11128_04_checks.py',
    'authored/native_fresh_08250_11128_04_checks.json',
    'worker-notes/native-fresh-08250-11128-04.json'])
paths.add(ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
allowlist_path = HERE / 'ROOT-POSTURE-QUOTE-REVIEW-04-COMMIT-ALLOWLIST.json'
value = {'schema': 'photo-root-research-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allowlist_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True,
    'root_accepted_research_records': 1, 'operational_native_qualified_records': 0,
    'canonical_or_binding_changes': False, 'stage05_complete': False,
    'gemini_calls': 0, 'provider_or_embedding_calls': 0}
with allowlist_path.open('x') as stream:
    json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
paths.add(allowlist_path)
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) == set(names)
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes()
print(json.dumps({'staged_files': len(paths), 'root_accepted_research': 1, 'operational_native_qualified': 0, 'cached_check': 'pass'}))
