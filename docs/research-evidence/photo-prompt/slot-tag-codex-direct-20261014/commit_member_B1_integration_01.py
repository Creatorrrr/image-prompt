"""Exact B1 pure resolver commit; source/runtime/native coordinator excluded."""
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


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
handoff_path = HERE / 'worker-notes/native-member-B1-FROZEN-HANDOFF-20261015.json'
assert raw(handoff_path) == '8bd34822a893c7db39091872b1fae5832bc4ef8a68b179503545cd5785689dbe'
handoff = json.loads(handoff_path.read_bytes())
paths = {handoff_path, handoff_path.with_suffix('.md'), Path(__file__).resolve()}
assert raw(handoff_path.with_suffix('.md')) == 'c9803432ef37ada9d22b968967b5400f6a34644b4c74f03a934cf18c4ecc5fd8'
for item in handoff['allowed_new_files'] + handoff['artifacts']:
    path = ROOT / item['file']
    assert raw(path) == item['raw_sha256'], path
    paths.add(path)
assert (handoff['tests']['executions'], handoff['tests']['unique_tests'], handoff['tests']['subtest_executions']) == (33, 33, 88)
assert handoff['tests']['failures'] == handoff['tests']['errors'] == handoff['tests']['skips'] == 0
report = HERE / 'ROOT-MEMBER-B1-INTEGRATION-01.json'
save(report, {
    'schema': 'photo-root-member-B1-integration/v1', 'actor': '/root',
    'root_whole_module_395_lines_and_tests_596_lines_read': True,
    'root_finding': 'No blocking B1 finding after complete independent code and test review.',
    'worker_focused_tests': {key: handoff['tests'][key] for key in ['executions', 'unique_tests', 'subtest_executions', 'failures', 'errors', 'skips']},
    'combined_root_regression_reference': 'run_guard_member_root_integration_02.json',
    'combined_regression_boundary': '411 executions/399 unique/991 subtests PASS against also-uncommitted guard and maintenance-test changes; archived with their subsequent integration commit. Pure B1 focused tests do not import that native coordinator.',
    'function': 'resolve_selected_contracts(core, projection)',
    'pure_selected_projection_is_not_source_truth': True,
    'full_P_PR_context_E_and_receivers_expanded': True,
    'single_joint_assignment_ledger_and_permission_footprint': True,
    'no_admission_or_qualification_granted': True,
    'B2_consumers_and_source_guard_validation_complete': False,
    'canonical_source_catalog_binding_or_proof_changes': False,
    'native_candidate_approvals': 0, 'provider_or_model_calls_for_B1': 0,
    'gemini_calls': 0, 'stages05_08_complete': False,
    'preserved_failed_development': handoff['initial_and_intermediate'],
    'remaining': handoff['B2_remaining_and_no_completion_claim'],
    'handoff': {'file': str(handoff_path.relative_to(ROOT)), 'raw_sha256': raw(handoff_path)},
})
paths.update({report, ROOT / 'skills/photo-prompt-image-generator/references/maintenance.md',
    ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'})
for path in paths:
    assert path.is_file() and not path.is_symlink()
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': json.loads(path.read_bytes())
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
non_patch = [name for name in names if not name.endswith('.patch')]
check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *non_patch], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-MEMBER-B1-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'archived_patch_whitespace_exempt': [name for name in names if name.endswith('.patch')],
    'self_hash_excluded': True, 'all_nonpatch_cached_check_returncode': 0,
    'native_approvals': 0, 'gemini_calls': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'native_approvals': 0, 'Gemini_calls': 0}))
