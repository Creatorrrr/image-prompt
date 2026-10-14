"""Stage only the tested source-reference feature and its exact evidence.

The operating corpus/catalog and all source/tag approval counts are unchanged.
This helper neither commits nor contacts a model or remote Git endpoint.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'semantic-reference-integration-01'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
tests = json.loads((OUT / 'ROOT-TESTS.json').read_bytes())
runtime = json.loads((OUT / 'native-v4-runtime-01/VERIFICATION.json').read_bytes())
assert (tests['test_executions'], tests['unique_test_ids'], tests['subtests']) == (259, 247, 532)
assert tests['failures'] == tests['errors'] == tests['skips'] == 0
assert tests['production_unchanged_during_tests'] and tests['os_network_denied']
assert raw(OUT / 'ROOT-TESTS.log') == tests['log_raw_sha256']
assert runtime['build']['vector_reuse'] == 18180
assert runtime['build']['provider_calls'] == runtime['build']['provider_cache_hits'] == 0
assert runtime['embedding_attempts'] == runtime['fresh_local_inference_inputs'] == runtime['gemini_calls'] == 0
assert runtime['publication']['generation_id'] == runtime['actual_acquire']['generation_id']
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified'
assert runtime['actual_acquire']['exact_source_record_match']
assert runtime['canonical_record_count'] == 18250 and runtime['canonical_slot_count'] == 139
assert runtime['canonical_native_qualified_records'] == 0
assert not runtime['canonical_source_or_bindings_changed']
pinned = {
    'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py': '0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4',
    'tests/test_photo_semantic_reference_units.py': '0326c450c7931ad473020e4bac4b469ecf675d97a22b7368781d39c6dc91823f',
    'worker-notes/native-08250-semantic-reference-implementation-20261015.json': '9c59aa73249f8bbe1cb17b2ed40f63c5279e9a708eb9fbe2aa1908a8ed1fba42',
    'worker-notes/native-08250-semantic-reference-unit-contract-20261015.md': '81049e8836c3ba1fd8e0b0c12b5e046554f99f059fdc51c3eb65c4b3a1409005',
}
for name, sha in pinned.items():
    path = HERE / name if name.startswith('worker-notes/') else ROOT / name
    assert raw(path) == sha, name
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
}
for name, sha in protected.items():
    assert raw(ROOT / name) == sha, name
generation = Path(runtime['publication']['generation_directory']) if 'generation_directory' in runtime['publication'] else Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / runtime['publication']['generation_id']
assert raw(generation / 'scripts/photo_semantic_evidence.py') == pinned['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py']
report_path = HERE / 'ROOT-SEMANTIC-REFERENCE-INTEGRATION-REPORT-01.json'
save(report_path, {
    'schema': 'photo-root-semantic-reference-integration-report/v1', 'actor': '/root',
    'root_complete_production_diff_and_sixteen_worker_tests_read': True,
    'root_two_additional_public_pack_and_fresh_runtime_tests': True,
    'relation_semantics': 'Manual one-hop field-local references retain restatements and local constraints without creating facts, role evidence, effects, permissions, or guard exemptions.',
    'root_regression': {key: tests[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'elapsed_seconds', 'log_raw_sha256']},
    'runtime': runtime,
    'protected_unrelated_dirty_files_unchanged': protected,
    'skill_quick_validation': 'pass',
    'root_test_boundary': tests['boundary'],
    'operating_catalog_count': 139, 'research146_activated': False,
    'canonical_native_candidate_approvals': 0, 'whole146_core_bound_hybrid_search_verified': False,
    'pixels_verified': False, 'stage05_complete': False, 'stages06_08_complete': False,
    'gemini_calls': 0,
})
paths = {ROOT / name for name in [
    'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py',
    'skills/photo-prompt-image-generator/references/maintenance.md',
    'tests/test_photo_semantic_reference_units.py',
    'tests/test_photo_semantic_reference_workflow.py',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md',
]}
paths.update(HERE / name for name in [
    Path(__file__).name,
    'run_semantic_reference_root_tests_01.py',
    'integrate_semantic_reference_runtime_01.py',
    'semantic-reference-integration-01/ROOT-TESTS.json',
    'semantic-reference-integration-01/ROOT-TESTS.log',
    'semantic-reference-integration-01/native-v4-runtime-01/PREFLIGHT.json',
    'semantic-reference-integration-01/native-v4-runtime-01/VERIFICATION.json',
    'worker-notes/native-08250-semantic-reference-implementation-20261015.json',
    'worker-notes/native-08250-semantic-reference-unit-contract-20261015.md',
])
paths.add(report_path)
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
allow_path = HERE / 'ROOT-SEMANTIC-REFERENCE-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow_path, {
    'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allow_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True,
    'native_approvals': 0, 'operating_source_or_catalog_changed': False,
})
paths.add(allow_path)
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) == set(names)
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'staged_files': len(paths), 'generation_id': runtime['publication']['generation_id'], 'regression_executions': 259, 'gemini_calls': 0, 'native_approvals': 0}))
