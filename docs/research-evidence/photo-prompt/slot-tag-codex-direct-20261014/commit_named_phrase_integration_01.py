"""Stage exact named-phrase code, local index closure, and verified evidence.

Keep prior generation files and unrelated work. No model, network or Git push.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
OUT = HERE / 'named-phrase-local-runtime-01'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
final_path = HERE / 'worker-notes/native-06250-phrase-consumer-final-20261015.json'
assert raw(final_path) == 'ffbe97130cefb7fbb3ae6285a74fcd8f4cdfe6aa68da111cb70ad24b2f4c5395'
worker = json.loads(final_path.read_bytes())
runtime = json.loads((OUT / 'VERIFICATION.json').read_bytes())
tests = json.loads((HERE / 'memberA-phrase-root-integration-01/ROOT-TESTS.json').read_bytes())
assert (tests['test_executions'], tests['unique_test_ids'], tests['subtests'], tests['failures'], tests['errors'], tests['skips']) == (203, 197, 592, 0, 0, 0)
assert runtime['fresh_local_document_inference_inputs'] == 381
assert runtime['fresh_local_query_inference_inputs'] == 1 and runtime['gemini_calls'] == 0
assert runtime['build']['vector_reuse'] == 17799 and runtime['build']['provider_cache_hits'] == 0
assert runtime['actual_acquire']['generation_id'] == runtime['publication']['generation_id'] == 'e9a03bb489e8b03cb7846787fcbe6c0f6e6ede02ac106a998ecbc6c57f6e9942'
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified'
assert runtime['low_level_bm25_cosine_rrf_and_pruning_verification'] is True
assert not runtime['canonical_source_or_bindings_changed'] and runtime['operational_native_qualified_records'] == 0
for name, sha in tests['frozen_code_and_tests'].items():
    assert raw(ROOT / name) == sha, name
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha
paths = {final_path}
for name, sha in worker['artifacts'].items():
    path = ROOT / name
    assert raw(path) == sha, name
    paths.add(path)
for name, row in worker['production_paths'].items():
    path = ROOT / name
    assert raw(path) == row['after_raw_sha256']
    assert hashlib.sha256(subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)).hexdigest() == row['before_raw_sha256']
    paths.add(path)
paths.update(ROOT / name for name in [
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md',
    'skills/photo-prompt-image-generator/references/maintenance.md',
])
paths.update(HERE / name for name in [
    Path(__file__).name, 'integrate_named_phrase_local_runtime_01.py',
    'worker-notes/native-08250-phrase-field-consumer-audit-20261015.md',
    'worker-notes/native-08250-phrase-fields-inventory-20261015.json',
])
paths.update(OUT / name for name in [
    'PREFLIGHT.json', 'PREVIOUS-INDEX-MANIFEST.json', 'DOCUMENT-EXECUTIONS.json',
    'QUERY-CONSUMER-VERIFICATION.json', 'VERIFICATION.json', 'build-cache/BUILD-REPORT.json',
])
manifest_path = ASSETS / 'photo_candidate_search.json'
manifest = json.loads(manifest_path.read_bytes())
assert manifest['layout_id'] == runtime['build']['layout_id'] == 'a1f1996d11b68c9c8256111751b06c5831574593f7ddcc0e650ef5f7e40e7289'
paths.add(manifest_path)
members = [manifest['metadata'], *manifest['shards']]
assert len(members) == 722
for row in members:
    path = ASSETS / row['path']
    assert path.resolve().is_relative_to(ASSETS / 'photo_candidate_search_shards' / manifest['layout_id'])
    assert path.is_file() and not path.is_symlink() and path.stat().st_size == row['bytes'] and raw(path) == row['sha256']
    paths.add(path)
report_path = HERE / 'ROOT-NAMED-PHRASE-INTEGRATION-REPORT-01.json'
save(report_path, {
    'schema': 'photo-root-named-phrase-integration-report/v1', 'actor': '/root',
    'root_complete_two_production_diffs_and_eleven_new_tests_read': True,
    'root_three_whole_source_examples_and_own_bindings_read': [6673, 5151, 2667],
    'whole18250_comparison': worker['actual18250_structural_comparison'],
    'root_regression': {key: tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'log_raw_sha256']},
    'runtime': runtime,
    'exact_new_layout_members_verified': len(members),
    'old_layout_recovery_files_deleted': 0,
    'protected_unrelated_dirty_files_unchanged': protected,
    'application_contract_native_only_followup': 'The46 research-only named application fields still need their own explicit coverage patch. Existing full ordinary units are preserved; no generic field or retrieval expansion is approved here.',
    'native_candidate_approvals': 0, 'operating_source_or_slot_catalog_changed': False,
    'all_final146_core_bound_search_semantic_quality_or_pixels_verified': False,
    'gemini_calls': 0,
})
paths.add(report_path)
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
archival = {path for path in paths if path.suffix in {'.patch', '.log'}}
all_check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
clean = subprocess.run(['git', 'diff', '--cached', '--check', '--', *sorted(str(path.relative_to(ROOT)) for path in paths - archival)], cwd=ROOT, capture_output=True, text=True)
assert clean.returncode == 0, clean.stdout
if all_check.returncode:
    headers = [line for line in all_check.stdout.splitlines() if not line.startswith('+')]
    assert headers and all(line.split(':', 1)[0] in {str(path.relative_to(ROOT)) for path in archival} for line in headers), all_check.stdout
allow = HERE / 'ROOT-NAMED-PHRASE-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {
    'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allow}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded': True, 'cached_nonarchival_check_returncode': clean.returncode,
    'cached_all_files_returncode': all_check.returncode, 'raw_archival_only_check_output': all_check.stdout,
    'gemini_calls': 0, 'new_local_document_inputs': 381, 'new_local_query_inputs': 1,
})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'staged_files': len(staged), 'verified_files': len(paths), 'new_layout_members': 722,
    'local_document_inputs': 381, 'local_query_inputs': 1, 'gemini_calls': 0}))
