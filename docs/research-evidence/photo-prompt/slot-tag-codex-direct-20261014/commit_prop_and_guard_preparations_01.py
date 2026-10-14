"""Exact research source choices and prepared packets; no semantic proof commit."""
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


def add(path, expected=None):
    assert path.is_file() and not path.is_symlink(), path
    if expected: assert raw(path) == expected, path
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    paths.add(path)


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
paths = set()
add(Path(__file__).resolve())
prop = HERE / 'native-inputs/bare-prop-applications-plan-06'
guard = HERE / 'native-inputs/guard-support-rechecks-plan-07-R02'
prop_report = json.loads((prop / 'ROOT-PREPARATION-VERIFICATION.json').read_bytes())
guard_report = json.loads((guard / 'ROOT-PREPARATION-VERIFICATION.json').read_bytes())
assert prop_report['source_changed_records_vs_original'] == 62 and prop_report['selected_new_applications'] == 4
assert prop_report['native_approvals'] == prop_report['actual_read_count_created_by_preparation'] == 0
assert guard_report['prepared_count'] == 2 and guard_report['native_approvals'] == 0
for directory in [prop, guard]:
    for name in ['ROOT-PREPARATION-VERIFICATION.json']:
        add(directory / name)
for name in ['CURRENT-PROPOSAL.json.gz', 'SOURCE-APPROVAL.json', 'ROOT-REQUIREMENTS.json']:
    add(prop / name)
add(guard / 'ROOT-REQUIREMENTS.json')
for report in [prop_report, guard_report]:
    for row in report['prepared']:
        assert row['prepared_count'] == 1 and row['actual_read_count'] == 0
        parent = prop if report is prop_report else guard
        add(parent / f"PLAN-{row['ordinal']:05d}.json")
        if report is prop_report: add(parent / f"ORIGINAL-SELECTION-{row['ordinal']:05d}.json")
        for name in ['INPUT.json', 'ASSIGNMENT.json', 'PREPARED-PACKET.json', 'PREPARATION.json']:
            add(ROOT / row['directory'] / name)
for key in ['source', 'source_approval', 'selection']:
    item = prop_report[key]
    add(ROOT / item['file'], item['file_sha256'])
note_path = HERE / 'worker-notes/native-06250-bare-prop-C-final-20261015.json'
add(note_path, '28a54af515318eed133d562765713e23a9bb342fd6c5d74971518e9bd459afe4')
note = json.loads(note_path.read_bytes())
assert note['whole_after_copies_actually_reread'] == note['individual_application_judgements'] == 4
assert note['root_selection_count'] == note['formal_native_proofs'] == note['operating_approvals'] == 0
for name, sha in note['artifacts'].items(): add(ROOT / name, sha)
for name, sha in note['previous_frozen_artifacts_unchanged'].items(): add(Path(name), sha)
for name in ['prepare_bare_prop_applications_06.py', 'prepare_guard_support_rechecks_07.py', 'prepare_guard_support_rechecks_07_r02.py',
    'native-inputs/guard-support-rechecks-plan-07/ROOT-REQUIREMENTS.json', 'native-inputs/guard-support-rechecks-plan-07/ROOT-FAILED-PREPARATION.json']:
    add(HERE / name)
add(ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-PROP-AND-GUARD-PREPARATIONS-01-COMMIT-ALLOWLIST.json'
with allow.open('x') as stream:
    json.dump({'schema': 'photo-root-exact-commit-allowlist/v1',
        'files': sorted(names + [str(allow.relative_to(ROOT))]),
        'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
        'self_hash_excluded': True, 'cached_check_returncode': 0,
        'selected_new_source_applications': 4, 'prepared_independent_review_inputs': 6,
        'actual_read_count_created_by_preparation': 0, 'native_approvals': 0,
        'canonical_source_catalog_binding_or_status_changes': False, 'Gemini_calls': 0}, stream, sort_keys=True, indent=2)
    stream.write('\n')
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'selected_applications': 4, 'prepared_inputs': 6, 'native_approvals': 0}))
