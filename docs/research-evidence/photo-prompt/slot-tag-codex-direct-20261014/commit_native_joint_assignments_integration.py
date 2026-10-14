"""Commit allowlist checks for the frozen selected-effect/lazy-child fix.

This script stages explicit reviewed paths only. It never approves corpus
semantics, invokes a provider, or removes historical recovery/log bytes.
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
spec = importlib.util.spec_from_file_location('joint_root_verifier', HERE / 'root_verify_native_joint_assignments.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


frozen = verifier.frozen_files()
handoff_path = HERE / 'worker-notes/native-joint-assignment-handoff-20261015.json'
handoff = json.loads(handoff_path.read_bytes())
tests = json.loads((HERE / 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TEST-VERIFICATION.json').read_bytes())
runtime_path = HERE / 'native-joint-assignment-integration-01/native-v4-runtime-01/VERIFICATION.json'
runtime = json.loads(runtime_path.read_bytes())
assert tests['frozen_code_files'] == frozen
assert (tests['test_executions'], tests['unique_test_ids'], tests['subtests'], tests['failures'], tests['errors'], tests['skips']) == (366, 342, 601, 0, 0, 0)
assert raw(HERE / 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TESTS.log') == tests['log_sha256']
assert runtime['build']['vector_reuse'] == 18180 and runtime['build']['provider_calls'] == 0
assert runtime['embedding_attempts'] == runtime['fresh_local_inference_inputs'] == runtime['gemini_calls'] == 0
assert runtime['actual_acquire']['generation_id'] == runtime['publication']['generation_id'] == '96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified'
assert runtime['actual_acquire']['exact_source_record_match']
assert runtime['canonical_record_count'] == 18250 and runtime['canonical_slot_count'] == 139
assert runtime['canonical_native_qualified_records'] == 0 and not runtime['canonical_source_or_bindings_changed']
assert tests['provider_or_inference_calls'] == tests['gemini_calls'] == 0
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha
report_path = HERE / 'ROOT-NATIVE-JOINT-ASSIGNMENTS-INTEGRATION-REPORT.json'
save(report_path, {
    'schema': 'photo-root-native-joint-integration-report/v1', 'actor': '/root',
    'root_complete_production_diff_and_fourteen_test_source_read': True,
    'frozen_code_files': frozen, 'worker_tests': handoff['validation'],
    'root_tests': {key: tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'elapsed_seconds', 'log_sha256']},
    'synthetic_public_pack_and_fresh_runtime_evidence': handoff['consumer_proof'],
    'actual_metadata_runtime': runtime,
    'canonical_source_or_role_bindings_changed': False,
    'operational_native_qualified_records': 0,
    'whole_final144_core_bound_hybrid_search_or_pixels_complete': False,
    'skill_quick_validation': 'pass',
    'protected_unrelated_dirty_files_unchanged': protected,
    'provider_or_inference_calls_for_implementation_validation_rebuild': 0,
    'gemini_calls': 0, 'stage05_complete': False, 'stages06_08_complete': False})
paths = {ROOT / name for name in frozen}
paths.update(ROOT / name for name in [
    'skills/photo-prompt-image-generator/references/composition-contract.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
paths.update(HERE / name for name in [
    Path(__file__).name, 'root_verify_native_joint_assignments.py',
    'NATIVE-JOINT-ASSIGNMENTS-ROOT-TEST-VERIFICATION.json', 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TESTS.log',
    'native-joint-assignment-integration-01/native-v4-runtime-01/PREFLIGHT.json',
    'native-joint-assignment-integration-01/native-v4-runtime-01/VERIFICATION.json',
    'authored/native_joint_effect_assignment_repro_20261015.py',
    'worker-notes/native-joint-effect-assignment-diagnostic-20261015.json',
    'worker-notes/native-joint-effect-assignment-diagnostic-20261015-r02.json',
    'worker-notes/native-joint-effect-assignment-diagnostic-20261015.md',
    'worker-notes/native-joint-assignment-handoff-20261015.json',
    'worker-notes/native-joint-assignment-handoff-20261015.md'])
paths.update(ROOT / row['path'] for row in handoff['evidence'])
backup_manifest = json.loads((HERE / 'worker-notes/native-joint-assignment-before-20261015/MANIFEST.json').read_bytes())
backup_paths = {ROOT / row['backup_path'] for row in backup_manifest['files']}
paths.update(backup_paths)
paths.add(report_path)
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
all_check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
warnings = all_check.stdout.splitlines()
archival = backup_paths | {ROOT / row['path'] for row in handoff['evidence'] if row['path'].endswith('.log')}
nonarchival = sorted(str(path.relative_to(ROOT)) for path in paths - archival)
clean_check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *nonarchival], cwd=ROOT, capture_output=True, text=True)
assert clean_check.returncode == 0, clean_check.stdout
if all_check.returncode:
    # Each warning's file is an exact byte-pinned archive; preserve raw bytes.
    headers = [line for line in warnings if not line.startswith('+')]
    archive_names = {str(path.relative_to(ROOT)) for path in archival}
    assert headers and all(line.split(':', 1)[0] in archive_names for line in headers), warnings
cached_path = HERE / 'ROOT-NATIVE-JOINT-ASSIGNMENTS-CACHED-CHECK.json'
save(cached_path, {
    'schema': 'photo-root-scoped-cached-check/v1',
    'production_docs_new_test_nonarchival_returncode': clean_check.returncode,
    'all_files_returncode': all_check.returncode, 'all_files_output': all_check.stdout,
    'raw_archival_log_or_recovery_only_exceptions': True,
    'archival_byte_pins': {str(path.relative_to(ROOT)): raw(path) for path in sorted(archival)},
    'recovery_matches_authorized_guardv2_commit': True,
    'unexpected_whitespace_findings': 0})
paths.add(cached_path)
allowlist_path = HERE / 'ROOT-NATIVE-JOINT-ASSIGNMENTS-COMMIT-ALLOWLIST.json'
save(allowlist_path, {
    'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allowlist_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True,
    'canonical_source_changed': False, 'operational_native_qualified_records': 0,
    'stage05_complete': False})
subprocess.run(['git', 'add', '--', str(cached_path.relative_to(ROOT)), str(allowlist_path.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged == {str(path.relative_to(ROOT)) for path in paths | {allowlist_path}}
for path in paths | {allowlist_path}:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes()
print(json.dumps({'staged_files': len(staged), 'root_test_executions': 366,
    'actual_generation': runtime['publication']['generation_id'], 'provider_calls': 0,
    'cached_archival_only_warnings': warnings}))
