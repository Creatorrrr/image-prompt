"""Stage only root-reviewed frozen source-target guard implementation/evidence.

No semantic inference or candidate approvals. Preserve all unrelated files and
recovery snapshots. A copied historical EOF is retained as exact recovery bytes.
"""
from __future__ import annotations
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('guard_v2_root_verifier', HERE / 'root_verify_source_guards_v2.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


frozen = verifier.frozen_files()
tests = json.loads((HERE / 'NATIVE-SOURCE-GUARDS-V2-ROOT-TEST-VERIFICATION.json').read_bytes())
runtime_path = HERE / 'native-source-target-guards-v2-integration-01/native-v4-runtime-01/VERIFICATION.json'
runtime = json.loads(runtime_path.read_bytes())
assert tests['frozen_code_files'] == frozen
assert (tests['test_executions'], tests['unique_test_ids'], tests['subtests'], tests['failures'], tests['errors'], tests['skips']) == (352, 328, 533, 0, 0, 0)
assert runtime['build']['vector_reuse'] == 18180 and runtime['build']['provider_calls'] == 0
assert runtime['embedding_attempts'] == runtime['fresh_local_inference_inputs'] == runtime['gemini_calls'] == 0
assert runtime['actual_acquire']['generation_id'] == runtime['publication']['generation_id'] == 'e54254ce78fde43d717a5c6e1670a0ffa5b50050fdafcf4b813930e42ecd0a7f'
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified'
assert runtime['actual_acquire']['exact_source_record_match']
assert runtime['canonical_record_count'] == 18250 and runtime['canonical_slot_count'] == 139
assert runtime['canonical_native_qualified_records'] == 0 and runtime['canonical_source_or_bindings_changed'] is False
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha
report_path = HERE / 'ROOT-SOURCE-TARGET-GUARDS-V2-INTEGRATION-REPORT.json'
report = {'schema': 'photo-root-source-target-guard-integration-report/v1', 'actor': '/root',
    'frozen_code_files': frozen, 'root_complete_production_diff_and_new_test_read': True,
    'worker_tests': {'executions': 133, 'unique': 133, 'subtests': 331, 'failures': 0, 'errors': 0, 'skips': 0},
    'root_tests': {key: tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'elapsed_seconds', 'log_sha256']},
    'actual_runtime': runtime, 'source_guard2_case_proposals_not_accepted_or_applied': [1278, 1296],
    'canonical_source_or_role_bindings_changed': False, 'operational_native_qualified_records': 0,
    'full_corpus_native_qualification_or_final144_hybrid_query_or_pixels_complete': False,
    'joint_cross_CID_typed_assignment_diagnostic_separate_and_not_claimed_complete': True,
    'skill_quick_validation': 'pass', 'protected_unrelated_dirty_files_unchanged': protected,
    'provider_or_inference_calls_for_this_implementation_validation_and_rebuild': 0,
    'gemini_calls': 0, 'stage05_complete': False, 'stages06_08_complete': False}
if report_path.exists():
    assert json.loads(report_path.read_bytes()) == report
else:
    save(report_path, report)
paths = {ROOT / name for name in frozen}
paths.update(ROOT / name for name in [
    'skills/photo-prompt-image-generator/SKILL.md',
    'skills/photo-prompt-image-generator/references/composition-contract.md',
    'skills/photo-prompt-image-generator/references/photo-workflow.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
paths.update(HERE / name for name in ['root_verify_source_guards_v2.py', Path(__file__).name,
    'NATIVE-SOURCE-GUARDS-V2-ROOT-TEST-VERIFICATION.json', 'NATIVE-SOURCE-GUARDS-V2-ROOT-TESTS.log',
    'native-source-target-guards-v2-integration-01/native-v4-runtime-01/PREFLIGHT.json',
    'native-source-target-guards-v2-integration-01/native-v4-runtime-01/VERIFICATION.json',
    'worker-notes/native-evidence-source-guards-v2-design-20261015.json',
    'worker-notes/native-evidence-source-guards-v2-design-20261015.md',
    'worker-notes/native-source-guards-v2-handoff-20261015.json',
    'worker-notes/native-source-guards-v2-handoff-20261015.md'])
backup = HERE / 'worker-notes/native-source-guards-v2-before-20261015'
paths.update(path for path in backup.iterdir() if path.is_file())
for directory in ['native-source-guards-v2-final-tests-20261015', 'native-source-guards-v2-final-tests-r02-20261015', 'native-source-guards-v2-final-tests-r03-20261015']:
    paths.update(HERE / 'worker-notes' / directory / name for name in ['RESULT.json', 'tests.log'])
paths.update(HERE / 'worker-notes/native-source-guards-v2-focused-tests-20261015' / name for name in ['INTERRUPTED.json', 'tests.log'])
paths.add(report_path)
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
allowlist_path = HERE / 'ROOT-SOURCE-TARGET-GUARDS-V2-COMMIT-ALLOWLIST.json'
cached_path = HERE / 'ROOT-SOURCE-TARGET-GUARDS-V2-CACHED-CHECK.json'
staged_before = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
expected_initial = {str(path.relative_to(ROOT)) for path in paths}
if staged_before:
    # Resume only this helper's exact first-attempt index; retain all worktree bytes.
    assert staged_before == expected_initial
    subprocess.run(['git', 'restore', '--staged', '--', *sorted(expected_initial)], cwd=ROOT, check=True)
interrupted_log = HERE / 'worker-notes/native-source-guards-v2-focused-tests-20261015/tests.log'
interrupted_receipt = json.loads(interrupted_log.with_name('INTERRUPTED.json').read_bytes())
assert interrupted_receipt['latest_final_code_hash_proof'] is False
assert raw(interrupted_log) == interrupted_receipt['log_sha256'] == '81ac70924d40abf90e0cff63c3da92efaa19da755adff05d7173a1c475d72c05'
subprocess.run(['git', 'add', '--', *sorted(str(path.relative_to(ROOT)) for path in paths)], cwd=ROOT, check=True)
all_check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
nonbackup = sorted(str(path.relative_to(ROOT)) for path in paths if not path.is_relative_to(backup) and path != interrupted_log)
clean_check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *nonbackup], cwd=ROOT, capture_output=True, text=True)
if clean_check.returncode:
    raise ValueError('production/docs/new-test/evidence whitespace failure: ' + clean_check.stdout)
warnings = all_check.stdout.splitlines()
if all_check.returncode:
    expected_warnings = [
        str((backup / 'prompt_generator.py').relative_to(ROOT)) + ':8569: new blank line at EOF.',
        str(interrupted_log.relative_to(ROOT)) + ':227: trailing whitespace.',
        '+test_native_observed_file_parent_coordinator_and_child_freeze (tests.test_photo_workflow_runtime_bridge.PhotoWorkflowRuntimeBridgeTests.test_native_observed_file_parent_coordinator_and_child_freeze) ... ']
    assert warnings == expected_warnings, warnings
save(cached_path, {'schema': 'photo-root-scoped-cached-check/v1',
    'production_docs_new_test_and_nonarchival_evidence_returncode': clean_check.returncode,
    'all_files_returncode': all_check.returncode, 'all_files_output': all_check.stdout,
    'recovery_byte_equality_to_original_HEAD_verified': True,
    'interrupted_log_preserved_sha256': raw(interrupted_log),
    'first_attempt_rejected_interrupted_raw_log_trailing_whitespace': True,
    'interrupted_log_is_final_completed_proof': False,
    'reason': 'Exact recovery snapshots retain original EOF bytes. The separately pinned raw interrupted log retains its incomplete line and is not completed-test proof. Production, new test, docs and all nonarchival evidence pass cached whitespace checks.',
    'unexpected_whitespace_findings': 0})
paths.add(cached_path)
allowlist = {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allowlist_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True, 'canonical_source_changed': False,
    'operational_native_qualified_records': 0, 'stage05_complete': False}
save(allowlist_path, allowlist)
subprocess.run(['git', 'add', '--', str(cached_path.relative_to(ROOT)), str(allowlist_path.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged == set(allowlist['files'])
print(json.dumps({'staged_files': len(staged), 'code_new_test_paths': len(frozen),
    'tests': tests['test_executions'], 'actual_generation': runtime['publication']['generation_id'],
    'vector_reuse': 18180, 'provider_calls': 0, 'cached_recovery_only_warnings': warnings}))
