"""Commit exact pure role-view foundation; native consumer changes excluded."""
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
handoff_path = HERE / 'worker-notes/native-role-view-08250-handoff-20261015-v1.json'
assert raw(handoff_path) == 'ac0a4a80127d189a0bb082101998f18428a2f88ee28446e15fd0a39668c8cd5a'
handoff = json.loads(handoff_path.read_bytes())
paths = {Path(__file__).resolve(), handoff_path}
for name, sha in handoff['allowed_new_code_files'].items():
    path = ROOT / name; assert raw(path) == sha; paths.add(path)
for item in [handoff['snapshot_patch'], handoff['validation']]:
    path = ROOT / item['path']; assert raw(path) == item['sha256']; paths.add(path)
for suffix in ['md', 'runner.py', 'validation.log']:
    paths.add(handoff_path.with_suffix('.' + suffix))
assert raw(handoff_path.with_suffix('.md')) == '9fbdebb20c25b7cc25a154fc824af68132ebba0d33d0b9353143aa4593ce6143'
assert raw(ROOT / handoff['validation']['log']) == handoff['validation']['log_sha256']
root_tests = json.loads((HERE / 'ROOT-PURE-ROLE-VIEW-TESTS-01.json').read_bytes())
assert (root_tests['tests_run'], root_tests['unique_test_ids'], root_tests['subtests']) == (22, 22, 41)
assert root_tests['success'] and not root_tests['failures'] and not root_tests['errors'] and not root_tests['skipped']
for name in ['run_pure_role_view_root_01.py', 'ROOT-PURE-ROLE-VIEW-TESTS-01.json', 'ROOT-PURE-ROLE-VIEW-TESTS-01.log']:
    paths.add(HERE / name)
for stem, suffixes in [
    ('native-08250-fact-role-projection-design-20261015-v1', ['json', 'md', 'repro.py', 'repro.json']),
    ('native-08250-generic-role-view-supplement-20261015-v1', ['json', 'md', 'repro.py', 'repro.json']),
    ('native-08250-generic-role-view-pure-api-design-20261015-v1', ['json', 'md']),
]:
    paths.update(HERE / 'worker-notes' / (stem + '.' + suffix) for suffix in suffixes)
report = HERE / 'ROOT-PURE-ROLE-VIEW-INTEGRATION-01.json'
save(report, {'schema': 'photo-root-pure-role-view-foundation/v1', 'actor': '/root',
    'root_whole_385_line_module_and304_line_test_read': True,
    'root_review_finding': 'No blocking finding in the pure foundation. It grants neither source qualification nor permission and has no native consumer yet.',
    'root_focused_tests': {key: root_tests[key] for key in ['tests_run', 'unique_test_ids', 'subtests', 'success', 'failures', 'errors', 'skipped']},
    'worker_focused_tests': handoff['validation'],
    'same_fact_full_spec_normal_anchor_and_canonical_quote_occurrence_bound': True,
    'canonical_fact_mode_value_operation_targets_all_receivers_requires_unchanged': True,
    'context_to_direct_and_preservation_sentinel_trait_rejected': True,
    'immutable_result_and_external_exact_binding_required': True,
    'external_binding_boundary': 'Native integrator must derive actual context and exact expected binding from full source validation/published immutable qualification. A reconstructed class or both matching self-authored receipts cannot establish provenance or manual semantic truth.',
    'well_shaped_false_NL_interpretation_still_requires_manual_rejection': True,
    'consumer_integration_and_whole_lock_runtime_regression_complete': False,
    'new_module_in_current_published188c': False,
    'runtime_publication_or_actual_corpus_meaning_approval': False,
    'canonical_source_catalog_proof_status_or_binding_changes': False,
    'native_candidate_approvals': 0, 'model_embedding_provider_network_calls': 0,
    'Gemini_calls': 0, 'stages05_08_complete': False,
    'remaining': handoff['integration_obligations']})
paths.update({report, ROOT / 'skills/photo-prompt-image-generator/references/maintenance.md',
    ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'})
for path in paths:
    assert path.is_file() and not path.is_symlink(), path
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': json.loads(path.read_bytes())
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *[name for name in names if not name.endswith('.patch')]], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-PURE-ROLE-VIEW-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded': True, 'archived_patch_whitespace_exempt': [name for name in names if name.endswith('.patch')],
    'nonarchival_cached_check_returncode': 0, 'native_approvals': 0, 'Gemini_calls': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'native_approvals': 0}))
