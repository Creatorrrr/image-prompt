"""Commit exact B2 implementation, preserved failures and actual publication."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'member-B2-integration-01'


def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p): return json.loads(p.read_bytes())


def save(p, value):
    with p.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
handoff_path = HERE / 'worker-notes/native-member-B2-FINAL-02-handoff-02-20261015.json'
assert raw(handoff_path) == 'c709df3db8e1791ef7b1fa04d6823377863ab5cec2f63e89313d606071639f74'
handoff = read(handoff_path)
paths = {Path(__file__).resolve(), handoff_path}
for row in handoff['changed_files']:
    p = ROOT / row['file']; assert raw(p) == row['raw_sha256']; paths.add(p)
for p in (HERE / 'worker-notes').glob('native-member-B2*'):
    if p.is_file(): paths.add(p)
    elif p.is_dir(): paths.update(x for x in p.rglob('*') if x.is_file())
for suffix in ['json', 'md']:
    paths.add(HERE / ('worker-notes/native-existing-member-scope-B2-release-plan-20261015.' + suffix))
tests = read(HERE / 'run_member_B2_root_integration_01.json')
assert (tests['executions'], tests['unique_tests'], tests['subtests']) == (517, 493, 1103)
assert tests['successful'] and not tests['errors'] and not tests['failures'] and not tests['skipped']
assert not tests['blocked_embedding_attempts'] and not tests['model_imports_loaded'] and tests['source_bytes_stable']
for name, sha in tests['after_hashes'].items(): assert raw(ROOT / name) == sha, name
boundary = read(HERE / 'ROOT-MEMBER-B2-DISCOVERY-BOUNDARY-01.json')
assert boundary['all_passed'] and len(boundary['cases']) == 2
runtime = read(OUT / 'native-v4-runtime-01/VERIFICATION.json')
generation = runtime['actual_acquire']['generation_id']
assert generation == '694ba2cc064e0eae2ae0d24603f37250577122cd4a700ae10f6e379ec9057609'
assert generation == runtime['publication']['generation_id']
assert runtime['actual_acquire']['cache_status'] == 'lazy_verified' and runtime['actual_acquire']['exact_source_record_match']
assert runtime['build']['vector_reuse'] == 18180
assert runtime['build']['provider_calls'] == runtime['build']['provider_cache_hits'] == runtime['embedding_attempts'] == runtime['gemini_calls'] == 0
assert runtime['fresh_local_inference_inputs'] == runtime['canonical_native_qualified_records'] == 0
assert runtime['canonical_record_count'] == 18250 and runtime['canonical_slot_count'] == 139
generation_root = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / generation
for row in handoff['changed_files']:
    if row['file'].startswith('skills/'):
        assert raw(generation_root / 'scripts' / Path(row['file']).name) == row['raw_sha256']
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name, sha in protected.items(): assert raw(ROOT / name) == sha
manifest = ROOT / 'skills/photo-prompt-image-generator/assets/photo_candidate_search.json'
assert manifest.read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:' + str(manifest.relative_to(ROOT))], cwd=ROOT)
paths.update(HERE / name for name in [
    'run_member_B2_root_integration_01.py', 'run_member_B2_root_integration_01.json', 'run_member_B2_root_integration_01.log',
    'run_member_B2_runtime_01.py', 'run_member_B2_runtime_01.log',
    'check_member_B2_discovery_boundary_01.py', 'ROOT-MEMBER-B2-DISCOVERY-BOUNDARY-01.json'])
paths.update(OUT / name for name in ['FROZEN-PRODUCTION-PINS.json',
    'native-v4-runtime-01/PREFLIGHT.json', 'native-v4-runtime-01/VERIFICATION.json', 'native-v4-runtime-01/build-cache/BUILD-REPORT.json'])
paths.update(ROOT / name for name in ['skills/photo-prompt-image-generator/references/maintenance.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
report = HERE / 'ROOT-MEMBER-B2-INTEGRATION-01.json'
save(report, {'schema': 'photo-root-member-B2-integration/v1', 'actor': '/root',
    'root_whole_final4_production_diffs_and2_new_tests_read': True,
    'final_worker_handoff': {'file': str(handoff_path.relative_to(ROOT)), 'raw_sha256': raw(handoff_path)},
    'worker_actual_regression': handoff['final_metrics'],
    'root_actual_regression': {key: tests[key] for key in ['executions', 'unique_tests', 'subtests', 'successful', 'errors', 'failures', 'skipped', 'elapsed_seconds', 'blocked_embedding_attempts', 'model_imports_loaded', 'source_bytes_stable']},
    'root_extra_actual_discovery_boundary': boundary,
    'root_finding': 'Actual root optional closure omission reused stale context before repair. Diagnostic alone established no final composed/runtime bypass. Exact active-root/selected-edge checks now reject it while preserving verified descendant subsets; identity-only scalar lookup grants no admission.',
    'worker_additional_finding': 'Actual per-source preservation receipt initially missed an independent chosen-root equal-value E overlap. Shared complete permission view now covers the joint chosen union without recursive expansion. Original failures and final prior passing results remain unchanged.',
    'one_source_qualified_shared_B1_view': True,
    'all_P_PR_members_and_E_targets_receivers_guards_children_profiles_locks_retained': True,
    'quantified_guards_v3_supported_as_constraints': True,
    'quantified_guard_only_role_support_v1_supported': False,
    'runtime': runtime, 'actual_published4_module_hashes_match_worker_freeze': True,
    'canonical_source_catalog_binding_or_native_qualification_changed': False,
    'protected_unrelated_dirty_files_unchanged': protected, 'index_manifest_bytes_unchanged': True,
    'native_operating_qualified_records': 0,
    'actual_corpus_scope_semantic_or_final149_core_bound_hybrid_quality_claim': False,
    'remaining': ['Generic same-fact manual role view consumers', '1264 typed-person domain override consumer', 'Full corpus semantic/proof review and approved149 tagging', 'Final all-slot actual search/sharding and final independent-seed sample'],
    'B2_engine_consumer_integration_complete': True, 'stages05_08_complete': False, 'Gemini_calls': 0})
paths.add(report)
for p in paths:
    assert p.is_file() and not p.is_symlink(), p
    if p.suffix == '.py': ast.parse(p.read_bytes(), filename=str(p))
    if p.suffix == '.json': read(p)
names = sorted(str(p.relative_to(ROOT)) for p in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
archival = [name for name in names if name.endswith('.patch')]
check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *[name for name in names if name not in archival]], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-MEMBER-B2-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(p.relative_to(ROOT)): raw(p) for p in sorted(paths)},
    'self_hash_excluded': True, 'archival_patch_whitespace_exempt': archival,
    'nonarchival_cached_check_returncode': 0, 'new_inference_and_Gemini_calls': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= {str(p.relative_to(ROOT)) for p in paths}
for p in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(p.relative_to(ROOT))], cwd=ROOT) == p.read_bytes()
print(json.dumps({'verified_files': len(paths), 'published_generation': generation, 'new_operating_native_qualified': 0}))
