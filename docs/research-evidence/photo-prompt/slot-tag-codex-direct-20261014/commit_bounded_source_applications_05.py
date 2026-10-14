"""Pin and stage exact bounded research preparation; no operating edits."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
directory = HERE / 'native-inputs/bounded-source-applications-plan-05'
report = json.loads((directory / 'ROOT-PREPARATION-VERIFICATION.json').read_bytes())
assert report['new_source_choices'] == 3 and report['source_changed_records_vs_original'] == 58
assert report['native_proof_or_status_or_operating_changes'] == report['actual_read_count_created_by_preparation'] == report['gemini_calls'] == 0
assert len(report['prepared']) == 4
paths = {directory / name for name in ['CURRENT-PROPOSAL.json.gz', 'SOURCE-APPROVAL.json', 'ROOT-REVIEW-REQUIREMENTS.json', 'ROOT-PREPARATION-VERIFICATION.json']}
for row in report['prepared']:
    assert row['prepared_count'] == 1 and row['actual_read_count'] == 0
    ordinal = row['ordinal']
    paths.update(directory / name for name in [f'PLAN-{ordinal:05d}.json', f'ORIGINAL-SELECTION-{ordinal:05d}.json'])
    prepared = ROOT / row['directory']
    paths.update(prepared / name for name in ['ASSIGNMENT.json', 'INPUT.json', 'PREPARED-PACKET.json', 'PREPARATION.json'])
for row in [report['source'], report['source_approval']]:
    assert raw(ROOT / row['file']) == row['file_sha256']
paths.update(HERE / name for name in [Path(__file__).name, 'prepare_bounded_source_applications_05.py', 'ROOT-BOUNDED-SOURCE-APPLICATION-SELECTION-05.json'])
paths.add(ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
for name in ['authored/native_11870_01257_semantic_reference_candidate_v1.py', 'authored/native_11870_01257_semantic_reference_candidate_v2.py',
             'authored/native_11870_01257_semantic_reference_candidate_v2.json', 'worker-notes/native-11870-01257-semantic-reference-candidate-v2.json']:
    paths.add(HERE / name)
candidate = HERE / 'authored/native_11870_01257_semantic_reference_candidate_v2.json'
assert raw(candidate) == '56cb4dcc69b10c92b61338a413f68e3b9dd32fa780c54d4481c79855ad0eac9f'
review = json.loads(candidate.read_bytes())
assert review['native_proof'] is review['native_signature'] is None and not review['root_selected']
assert len(review['literal_candidate_facts']) == 3 and len(review['literal_candidate_source_units']) == 4
for path in paths:
    assert path.is_file() and not path.is_symlink()
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': json.loads(path.read_bytes())
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-BOUNDED-SOURCE-APPLICATIONS-05-COMMIT-ALLOWLIST.json'
with allow.open('x') as stream:
    json.dump({'schema': 'photo-root-exact-commit-allowlist/v1', 'files': names + [str(allow.relative_to(ROOT))],
        'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)}, 'self_hash_excluded': True,
        'cached_check_returncode': 0, 'native_approvals': 0, 'gemini_calls': 0}, stream, sort_keys=True, indent=2)
    stream.write('\n')
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'new_source_choices': 3, 'native_approvals': 0}))
