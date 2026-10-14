"""Record and stage only the reviewed owner-selector integration allowlist.

Run once after independent tests and actual zero-inference runtime rebuild.
The script validates bytes/AST and stages exact paths; it never commits/pushes.
It preserves hash-bound recovery copies, including their original EOF bytes.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
from root_verify_owner_selector_addendum import frozen_files


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': sha(path)}


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


code_hashes = frozen_files()
initial = read(HERE / 'worker-notes/native-owner-selector-final-handoff-20261014.json')
addendum = read(HERE / 'worker-notes/native-resolved-assignment-handoff-addendum-20261014.json')
for row in initial['changed_code_files']:
    if row.get('before_sha256'):
        old = subprocess.check_output(['git', 'show', 'HEAD:' + row['path']], cwd=ROOT)
        if hashlib.sha256(old).hexdigest() != row['before_sha256']:
            raise ValueError('production before bytes differ from HEAD: ' + row['path'])

paths = set(code_hashes)
paths.update('skills/photo-prompt-image-generator/' + name for name in [
    'SKILL.md', 'references/composition-contract.md', 'references/photo-workflow.md'])
paths.update(str((HERE / name).relative_to(ROOT)) for name in [
    'root_verify_owner_selector.py', 'root_verify_owner_selector_addendum.py',
    'commit_owner_selector_integration.py',
    'NATIVE-OWNER-ROOT-TESTS.log', 'NATIVE-OWNER-ROOT-TEST-VERIFICATION.json',
    'NATIVE-OWNER-ADDENDUM-ROOT-TESTS.log', 'NATIVE-OWNER-ADDENDUM-ROOT-TEST-VERIFICATION.json',
    'native-owner-selector-addendum-integration-01/native-v4-runtime-01/PREFLIGHT.json',
    'native-owner-selector-addendum-integration-01/native-v4-runtime-01/VERIFICATION.json',
    'worker-notes/native-owner-selector-final-handoff-20261014.json',
    'worker-notes/native-resolved-assignment-handoff-addendum-20261014.json',
    'worker-notes/native-resolved-assignment-handoff-addendum-20261014.md',
    'worker-notes/native-resolved-assignment-six-case-proof-20261014.json',
    'worker-notes/native-resolved-assignment-final-tests-20261014.json',
    'worker-notes/native-evidence-resolved-owner-effect-conflict-reproduction-20261014.json'])
for row in initial['notes_and_recovery_manifests']:
    path = ROOT / row['path']
    if sha(path) != row['sha256']:
        raise ValueError('handoff artifact changed: ' + row['path'])
    paths.add(row['path'])

backup_files = set()
primary = HERE / 'worker-notes/native-v4-pre-owner-selector-backup-20261014/MANIFEST.json'
for row in read(primary)['allowlist']:
    if not row['existed_before']:
        continue
    path = ROOT / row['backup_path']
    if sha(path) != row['before_byte_sha256']:
        raise ValueError('before backup changed')
    backup_files.add(str(path.relative_to(ROOT)))
extra = HERE / 'worker-notes/native-owner-selector-global-audit-backup-20261014/MANIFEST.json'
for row in read(extra)['files']:
    path = extra.parent / row['copy']
    if sha(path) != row['sha256']:
        raise ValueError('global audit backup changed')
    backup_files.add(str(path.relative_to(ROOT)))
resolved = HERE / 'worker-notes/native-resolved-assignment-pre-fix-backup-20261014/MANIFEST.json'
paths.add(str(resolved.relative_to(ROOT)))
for row in read(resolved)['files']:
    path = ROOT / row['backup_path']
    if sha(path) != row['before_sha256']:
        raise ValueError('resolved assignment backup changed')
    backup_files.add(str(path.relative_to(ROOT)))
paths |= backup_files

pre_tests = read(HERE / 'NATIVE-OWNER-ROOT-TEST-VERIFICATION.json')
tests = read(HERE / 'NATIVE-OWNER-ADDENDUM-ROOT-TEST-VERIFICATION.json')
runtime_path = HERE / 'native-owner-selector-addendum-integration-01/native-v4-runtime-01/VERIFICATION.json'
runtime = read(runtime_path)
assert pre_tests['test_executions'] == 335 and pre_tests['unique_test_ids'] == 305 and pre_tests['subtests'] == 622
assert tests['test_executions'] == 292 and tests['unique_test_ids'] == 286 and tests['subtests'] == 498
for result in [pre_tests, tests]:
    assert result['failures'] == result['errors'] == result['skips'] == 0
assert tests['frozen_code_files'] == code_hashes
assert runtime['build']['vector_reuse'] == 18180
assert runtime['embedding_attempts'] == runtime['fresh_local_inference_inputs'] == runtime['gemini_calls'] == 0
assert runtime['source_sha256'] == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert runtime['actual_acquire']['exact_source_record_match'] is True
assert runtime['canonical_native_qualified_records'] == 0
for name in paths:
    path = ROOT / name
    if path.suffix == '.py':
        ast.parse(path.read_text(), filename=name)
    elif path.suffix == '.json':
        read(path)
protected = {
    'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md': 'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
    'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md': '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
}
for name, expected in protected.items():
    if sha(ROOT / name) != expected:
        raise ValueError('protected unrelated file changed')

report = {
    'schema': 'photo-root-owner-selector-integration/v1', 'actor': '/root',
    'status': 'code_fixture_zero_inference_runtime_integration_verified',
    'code_hashes': code_hashes, 'pre_addendum_broad_tests': ref(HERE / 'NATIVE-OWNER-ROOT-TEST-VERIFICATION.json'),
    'final_addendum_fresh_tests': ref(HERE / 'NATIVE-OWNER-ADDENDUM-ROOT-TEST-VERIFICATION.json'),
    'actual_runtime': ref(runtime_path),
    'published_generation': runtime['publication']['generation_id'],
    'published_source_fingerprint': runtime['publication']['source_fingerprint'],
    'skill_quick_validate': 'pass', 'code_and_docs_reviewed_by_root': True,
    'actual_original_reproductions': 'All6 source-valid alias cases now fail admission, permission, eligibility and final adoption. Isolated immutable-pack composed same-owner conflict fails and disjoint actual application passes.',
    'effect_conflict_scope': 'Within each selected source/RID, including different local/fixed/selected targets resolving to one actual owner. No new cross-CID aggregate assignment contract is claimed.',
    'canonical_records': 18250, 'canonical_slots': 139, 'canonical_native_qualified': 0,
    'source_bindings_and_vector_space_unchanged': True,
    'vector_reuse': 18180, 'fresh_inference_inputs': 0, 'gemini_calls': 0,
    'proof_boundary': 'Code/isolated fixtures and actual operating metadata publish/acquire. Not final-catalog native whole-corpus qualification, actual core-bound hybrid-query evaluation or image pixels.',
    'remaining_source_contracts': ['Explicit dynamic selected-target source guards',
        'Individual source/branch/owner/effect/tag qualification under final catalog',
        'Full migration/search/sharding/quality closure of stages05–08'],
    'protected_unrelated_hashes': protected,
    'backup_files': sorted(backup_files),
    'whitespace_policy': 'Changed production/docs must pass. Preserve byte-identical recovery-copy EOF-only warnings and record them explicitly, if any.',
}
report_path = HERE / 'ROOT-OWNER-SELECTOR-INTEGRATION-REPORT.json'
save(report_path, report)
paths.add(str(report_path.relative_to(ROOT)))
if subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip():
    raise ValueError('index must be empty before allowlisted staging')
subprocess.run(['git', 'add', '--', *sorted(paths)], cwd=ROOT, check=True)
save(HERE / 'ROOT-OWNER-SELECTOR-COMMIT-ALLOWLIST.json', {
    'schema': 'photo-root-exact-commit-allowlist/v1', 'files': sorted(paths),
    'file_byte_hashes': {name: sha(ROOT / name) for name in sorted(paths)},
    'canonical_source_changed': False, 'stage_completed': False,
})
print(json.dumps({'staged_allowlist_files': len(paths), 'production_and_new_test_files': len(code_hashes),
                  'backup_files': len(backup_files), 'generation': runtime['publication']['generation_id']}))
