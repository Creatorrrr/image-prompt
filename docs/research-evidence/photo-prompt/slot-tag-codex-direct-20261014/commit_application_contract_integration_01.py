"""Commit allowlist for exact named application coverage; no provider or network."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'application-contract-integration-01'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
tests = json.loads((OUT / 'ROOT-TESTS.json').read_bytes())
runtime = json.loads((OUT / 'native-v4-runtime-01/VERIFICATION.json').read_bytes())
inventory = json.loads((OUT / 'APPLICATION-FIELD-INVENTORY.json').read_bytes())
assert tuple(tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips']) == (208, 202, 595, 0, 0, 0)
assert runtime['actual_acquire']['generation_id'] == runtime['publication']['generation_id'] == '07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07'
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified' and runtime['actual_acquire']['exact_source_record_match']
assert runtime['build']['vector_reuse'] == 18180 and runtime['embedding_attempts'] == runtime['gemini_calls'] == 0
assert runtime['canonical_native_qualified_records'] == 0 and not runtime['canonical_source_or_bindings_changed']
assert inventory['original_source_count'] == 0 and inventory['research_proposal_count'] == 46 and inventory['all_actual_rids_covered']
for name, sha in tests['frozen_code_and_tests'].items():
    assert raw(ROOT / name) == sha, name
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha
manifest = ROOT / 'skills/photo-prompt-image-generator/assets/photo_candidate_search.json'
assert manifest.read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:' + str(manifest.relative_to(ROOT))], cwd=ROOT)
paths = {ROOT / name for name in [
    'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py',
    'tests/test_photo_application_contract_fields.py',
    'skills/photo-prompt-image-generator/references/maintenance.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md',
]}
paths.update(HERE / name for name in [Path(__file__).name, 'run_application_contract_coverage_01.py'])
paths.update(OUT / name for name in ['ROOT-TESTS.log', 'ROOT-TESTS.json', 'APPLICATION-FIELD-INVENTORY.json',
    'native-v4-runtime-01/PREFLIGHT.json', 'native-v4-runtime-01/VERIFICATION.json',
    'native-v4-runtime-01/build-cache/BUILD-REPORT.json'])
report = HERE / 'ROOT-APPLICATION-CONTRACT-INTEGRATION-REPORT-01.json'
save(report, {
    'schema': 'photo-root-application-contract-integration/v1', 'actor': '/root',
    'root_complete_one_constant_diff_and_all_five_new_tests_read': True,
    'exact_named_field': '/content/application_contract',
    'retrieval_text_or_projection_changed': False, 'index_manifest_bytes_unchanged': True,
    'research_only_46_field_inventory': inventory,
    'whole_46_meaning_review_created': False,
    'root_regression': {key: tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'log_raw_sha256']},
    'runtime': runtime, 'protected_unrelated_dirty_files_unchanged': protected,
    'native_candidate_approvals': 0, 'operating_source_or_catalog_changed': False,
    'all_final146_core_bound_search_or_pixel_quality_verified': False, 'stages05_08_complete': False,
})
paths.add(report)
for path in paths:
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': json.loads(path.read_bytes())
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-APPLICATION-CONTRACT-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded': True, 'cached_check_returncode': check.returncode,
    'gemini_calls': 0, 'new_inference_inputs': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'staged_files': len(staged), 'verified_files': len(paths), 'gemini_calls': 0}))
