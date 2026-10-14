"""Preserve frozen contract designs and an explicitly unsubmitted semantic draft."""
from __future__ import annotations
import ast
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
pins = {
    'worker-notes/native-existing-member-scope-stageB-split-design-01.json': '38d7f8db2981d67601ae8b00bf3a3ca2caf6b823600dab3f0d21899aba53603b',
    'worker-notes/native-existing-member-scope-stageB-split-design-01-FULLREAD-SUPPLEMENT.json': 'e92bc9ce329a0a410ceaa4b4b85a49574b5ed24eaa2116aa191b0f98196f9a6e',
    'worker-notes/native-07250-guard-role-support-design-20261015.json': 'fa0af42deddb4bf06b35ec3f24690c7b8231b2f8374c6bf3cb07bf76b6e1ca5d',
    'worker-notes/native-08250-17437-04-pending-final-20261015.json': '83c57de4979b614d7f7629ec46ac1c2ed57e102340985af643eb2e5d88107eb7',
}
for name, sha in pins.items():
    assert raw(HERE / name) == sha, name
note = json.loads((HERE / 'worker-notes/native-08250-17437-04-pending-final-20261015.json').read_bytes())
for name, row in note['artifacts'].items():
    assert set(row) == {'raw_sha256'}
    assert raw(HERE / name) == row['raw_sha256'], name
    pins[name] = row['raw_sha256']
for suffix in ['md', 'repro.py', 'repro.json', 'files.sha256']:
    name = 'worker-notes/native-07250-guard-role-support-design-20261015.' + suffix
    pins[name] = raw(HERE / name)
batch = json.loads((HERE / 'native_batches/review08250-17437-04/BATCH.json').read_bytes())
assert len(batch['records']) == batch['actual_read_count'] == batch['prepared_count'] == 1
row = batch['records'][0]
assert row['ordinal'] == 17437 and row['status'] == 'pending' and row['proof'] is None
current = json.loads(gzip.decompress((HERE / 'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz').read_bytes()))
original = json.loads(gzip.decompress((HERE / 'SOURCE.json.gz').read_bytes()))
assert canonical(current) == '88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert row['source_after'] == current['candidates'][row['candidate_id']]
assert row['source_before'] == original['candidates'][row['candidate_id']]
draft = json.loads((HERE / 'authored/native_fresh_08250_17437_04_draft.json').read_bytes())
assert draft['proof_is_not_submitted_native_approval'] is True
assert draft['canonical_or_operating_mutations'] == 0
proof = draft['proof_draft']
assert len(proof['facts']) == 483 and len(proof['source_units']) == 786
assert note['role_gap']['slot_id'] == 'anatomical_connection'
assert note['status'] == 'pending' and note['formal_proof'] is None and not note['root_acceptance']
report = HERE / 'ROOT-PENDING-CONTRACT-RESEARCH-CHECKPOINT-01.json'
save(report, {
    'schema': 'photo-root-pending-contract-research-checkpoint/v1', 'actor': '/root',
    'frozen_files': pins, 'all_raw_identities_json_and_python_syntax_verified': True,
    'source_after_matches_exact_research_input': True, 'submitted_proof_is_null': True,
    'research_draft_facts': 483, 'research_draft_units': 786,
    'root_all_483_facts_or_786_units_personally_read_claimed': False,
    'worker_manual_whole_source_read_attestation': note['read_attestation'],
    'root_semantic_approval_created': False, 'operating_native_approvals': 0,
    'old03_precision_hold_superseded_by_new04_approval': False,
    'guard_role_implementation_direction': {
        'root_read': 'Entire design MD, actual scalar v1/v2 evaluators and full146 anatomical_connection/relational_action specifications.',
        'approved_scope': 'Optional exact source-local guard support for explicit owner_relation/frozen_entity_relation prerequisites, own positive quote and normal unit; roles and ordinary units may reference exact supports. Match actual selected source frame/rule/hash and actual executed admission receipt. Keep scalar facts, E, permissions and old no-field bytes intact.',
        'production_owner': '/root/review_07250_08250',
        'primary_allowlist': ['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py', 'new focused tests only'],
        'new_semantic_reference_guard_refs_authorized': False,
        'implementation_or_transport_verification_claimed_from_design': False,
    },
    'member_scope_B1_direction': {
        'root_read': 'Split contract/test plan, every B2 wiring/dependency item and complete full-read compatibility supplement.',
        'approved_scope': 'New pure resolution module and focused tests only. Distinguish old fixed-point witness context from exact core-bound scope/selected-owner contexts. Supplied bad hash never falls back. Expand each actual P/PR/E and all receivers once into shared typed ledger and footprint; part_of is distinct from equivalence. No source qualification, guard parser, adoption certificate or discovery decision in B1.',
        'production_owner': '/root/native_evidence',
        'allowlist': ['skills/photo-prompt-image-generator/scripts/photo_native_owner_resolution.py', 'tests/test_photo_native_member_scope_resolution.py'],
        'B2_consumer_adoption_or_feature_complete': False,
    },
    'source_catalog_index_runtime_changes_from_this_checkpoint': 0,
    'new_model_or_provider_calls': 0, 'gemini_calls': 0, 'stages05_08_complete': False,
})
paths = {HERE / name for name in pins} | {report, Path(__file__)}
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-PENDING-CONTRACT-RESEARCH-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1', 'files': names + [str(allow.relative_to(ROOT))],
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)}, 'self_hash_excluded': True,
    'cached_check_returncode': check.returncode, 'new_approvals': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= {str(path.relative_to(ROOT)) for path in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes(), str(path)
print(json.dumps({'verified_files': len(paths), 'staged_files': len(staged), 'pending_research_proof_submitted': False, 'native_approvals': 0}))
