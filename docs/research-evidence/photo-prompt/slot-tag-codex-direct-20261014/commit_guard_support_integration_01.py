"""Pin exact guard integration, maintenance isolation, failures and publication."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'guard-support-integration-01'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
paths = {Path(__file__).resolve()}
worker_path = HERE / 'worker-notes/native-07250-guard-role-support-implementation-20261015.json'
assert raw(worker_path) == '906cbf30680db16941bb895f29d8ce4b132d0432ebd29732fd4f03c7d46eca10'
worker = json.loads(worker_path.read_bytes())
paths.add(worker_path)
for item in worker['artifacts']:
    path = ROOT / item['path']
    assert raw(path) == item['raw_sha256'], path
    paths.add(path)
for suffix in ['files.sha256']:
    paths.add(worker_path.with_suffix('.' + suffix))
review_path = HERE / 'worker-notes/native-guard-support-independent-review-20261015.json'
review = json.loads(review_path.read_bytes())
paths.add(review_path)
for item in review['evidence'] + [review['summary_markdown']]:
    path = ROOT / item['path']
    assert raw(path) == item['raw_sha256'], path
    paths.add(path)
assert review['actual_tests']['successful'] and not review['findings']
tests = json.loads((HERE / 'run_guard_member_root_integration_02.json').read_bytes())
failed = json.loads((HERE / 'run_guard_member_root_integration_01.json').read_bytes())
assert (tests['executions'], tests['unique_tests'], tests['subtests']) == (411, 399, 991)
assert tests['successful'] and not tests['errors'] and not tests['failures'] and not tests['skipped']
assert tests['all_existing_current_asset_configuration_tests_included']
assert not tests['blocked_embedding_attempts'] and not tests['model_imports_loaded']
assert not failed['successful'] and len(failed['errors']) == 2
for name, sha in tests['after_hashes'].items():
    assert raw(ROOT / name) == sha, name
runtime = json.loads((OUT / 'native-v4-runtime-01/VERIFICATION.json').read_bytes())
assert runtime['actual_acquire']['generation_id'] == runtime['publication']['generation_id']
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified' and runtime['actual_acquire']['exact_source_record_match']
assert runtime['build']['vector_reuse'] == 18180
assert runtime['build']['provider_calls'] == runtime['embedding_attempts'] == runtime['gemini_calls'] == 0
assert runtime['fresh_local_inference_inputs'] == runtime['canonical_native_qualified_records'] == 0
assert runtime['canonical_record_count'] == 18250 and runtime['canonical_slot_count'] == 139
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha
manifest = ROOT / 'skills/photo-prompt-image-generator/assets/photo_candidate_search.json'
assert manifest.read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:' + str(manifest.relative_to(ROOT))], cwd=ROOT)
paths.update(ROOT / name for name in [
    'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py',
    'tests/test_photo_native_guard_role_support.py', 'tests/test_photo_native_search_maintenance.py',
    'skills/photo-prompt-image-generator/references/maintenance.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
paths.update(HERE / name for name in [
    'run_guard_member_root_integration_01.preflight-path-error.py',
    'run_guard_member_root_integration_01.py', 'run_guard_member_root_integration_01.json', 'run_guard_member_root_integration_01.log',
    'run_guard_member_root_integration_02.py', 'run_guard_member_root_integration_02.json', 'run_guard_member_root_integration_02.log',
    'run_guard_support_runtime_01.py'])
paths.update(OUT / name for name in ['FROZEN-PRODUCTION-PINS.json',
    'native-v4-runtime-01/PREFLIGHT.json', 'native-v4-runtime-01/VERIFICATION.json',
    'native-v4-runtime-01/build-cache/BUILD-REPORT.json'])
report = HERE / 'ROOT-GUARD-SUPPORT-INTEGRATION-01.json'
save(report, {
    'schema': 'photo-root-guard-support-integration/v1', 'actor': '/root',
    'root_whole_guard_diff_and_focused_tests_read': True,
    'worker_frozen_native_raw_sha256': worker['production']['raw_sha256'],
    'root_final_native_raw_sha256': raw(ROOT / worker['production']['path']),
    'root_revision': 'Return empty optional support map before asking for candidate review/CID when guard_supports is absent. Added a focused independent-source-unit compatibility test.',
    'independent_review': {'file': str(review_path.relative_to(ROOT)), 'raw_sha256': raw(review_path), 'tests': review['actual_tests']},
    'worker_regression': worker['final_regression'],
    'root_regression': {key: tests[key] for key in ['executions', 'unique_tests', 'subtests', 'successful', 'failures', 'errors', 'skipped', 'elapsed_seconds', 'log_raw_sha256', 'blocked_embedding_attempts', 'model_imports_loaded']},
    'root_first_regression': {'executions': failed['executions'], 'successful': False, 'errors': failed['errors'],
        'resolution': 'Optional support helper coupled unrelated minimal source-unit checks to review/CID; fixed before fresh second run.'},
    'worker_prior_incident': worker['retained_failed_runs'],
    'maintenance_fixture_fix': 'Pin explicit synthetic fixture model space; deny provider scalar and batch plus local inference; exercise historical and local model spaces with synthetic exact execution traces. Earlier worker broad discovery really embedded nine temporary fixture inputs; not represented as zero inference.',
    'guard_support_boundary': 'Manual exact own source CID/RID/common or actual branch guard relation provenance, positive normal unit, whole spec binding and fresh verified predicate receipt. Supports are prerequisite-only; no scalar fact/E/value/permission creation or reference-only proof.',
    'no_optin_fields_no_new_receipt_keys': True,
    'runtime': runtime, 'index_manifest_bytes_unchanged': True,
    'protected_unrelated_dirty_files_unchanged': protected,
    'actual17437_or1264_new_proof_approval': False,
    'canonical_source_catalog_or_binding_changed': False,
    'canonical_native_qualified_records': 0,
    'final146_actual_core_bound_hybrid_or_semantic_quality_verified': False,
    'B2_member_consumers_complete': False, 'stages05_08_complete': False,
    'Gemini_calls': 0,
})
paths.add(report)
for path in paths:
    assert path.is_file() and not path.is_symlink(), path
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': json.loads(path.read_bytes())
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
archival = [name for name in names if name.endswith(('.patch', '.py.txt'))]
check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *[name for name in names if name not in archival]], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-GUARD-SUPPORT-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded': True, 'archival_whitespace_exempt': archival,
    'nonarchival_cached_check_returncode': 0, 'Gemini_calls': 0,
    'new_inference_for_root_regression_and_publication': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'generation': runtime['actual_acquire']['generation_id'], 'native_approvals': 0}))
