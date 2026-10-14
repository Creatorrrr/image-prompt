"""Root verifies and accepts the exact manually reviewed field-local repair."""
from __future__ import annotations
import hashlib
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore'), str(HERE)]
import photo_candidate_corpus as c
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(reviews.read_json(path))}


out = HERE / 'native_batches/review11870-01285-06'
old = reviews.read_json(HERE / 'native_batches/review11870-01285-05/BATCH.json')['records'][0]
batch = reviews.read_json(out / 'BATCH.json'); row = batch['records'][0]
assert c.digest(batch) == 'a1aa6181b3abc09b876f656dc434ed30978cd9928aec882fa89c819c15bf5ef9'
removed = {'counterpartEN', 'counterpartKO', 'assocEN', 'assocKO'}
assert row['source_before'] == old['source_before'] and row['source_after'] == old['source_after']
assert {fact['id']: fact for fact in row['proof']['facts']} == {fact['id']: fact for fact in old['proof']['facts'] if fact['id'] not in removed}
for key in ['effect_sets', 'owner_maps', 'guard_sets', 'dependencies', 'profile_contracts', 'reference_sha256', 'meaning_sha256', 'catalog_sha256']:
    assert row['proof'][key] == old['proof'][key], key
assert row['proof']['roles']['participant_role']['fact_refs'] == ['counterpartApp']
units = row['proof']['source_units']; assert len(units) == 5
assert [unit['fact_refs'] for unit in units[:2]] == [['placeEN', 'stateEN', 'contactEN'], ['placeKO', 'stateKO', 'contactKO']]
assert all(unit['fact_refs'] == ['counterpartApp', 'assocApp'] and unit['disposition'] == 'semantic_reference'
    and unit['reference_relation'] == 'partial_restatement' for unit in units[-2:])
worker_checks = reviews.read_json(out / 'CHECKS-v1.json')
assert worker_checks['all_passed'] and worker_checks['admission_count'] == 20 and worker_checks['consumer_count'] == 10
assert len(worker_checks['actual_target_receiver_locks']) == 10 and len(worker_checks['whole_effect_dimension_locks']) == 3
assert len(worker_checks['invalid_semantic_reference_cases']) == 7
assignment = HERE / 'native-inputs/prepared/review11870-01285-06/ASSIGNMENT.json'
verified = reviews.verify_batch(str(assignment.relative_to(ROOT)), str((out / 'BATCH.json').relative_to(ROOT)), str((out / 'NOTE.json').relative_to(ROOT)))
assert row['status'] == 'approved'
reason = ('Root accepts this exact fresh06 research repair after direct whole current/original/source-choice/5B/binding review, all19 old facts/3units/5roles/owners/guards/effects and whole relevant specs, followed by direct reading of all5 new units/new role references and exact unchanged15 retained facts. '
    'Four over-complete short-field fact duplicates are removed; all five actual E groups, four existing endpoint bindings, original guards, actual values/operations/receivers and whole locks remain byte-identical. '
    'The complete application directly anchors counterpart and chair association; whole English/Korean short fields retain their own placement/state/support and one-hop partial relation references, without independently asserting the complete two-participant relationship. '
    'No performed propping action, legal ownership, new person/object or generic projection bypass follows. Worker20full/compact admission,10actual-oldbinding consumers,10target/receiver+3whole locks and7reference negatives are worker evidence, not newly claimed root execution. '
    'Root full-batch/acceptance integrity validation is separate. Original05 proof/status/reopen remain historical, operating source/catalog/bindings/tags/qualification/runtime are unchanged; no all-first50 or full-corpus acceptance.')
acceptance = {'schema': reviews.ACCEPTANCE, 'actor': '/root',
    **{key: verified[key] for key in ['assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256']},
    'reviews': {key: {'review_sha256': c.digest(value), 'status': 'approved'} for key, value in verified['records'].items()}, 'reason': reason}
save(out / 'ROOT-ACCEPTANCE.json', acceptance)
reviews.verify_acceptance(ROOT, ref(out / 'ROOT-ACCEPTANCE.json'), verified)
save(out / 'ROOT-VERIFICATION-01.json', {'schema': 'photo-root-partner-chair-field-repair-verification/v1',
    'actor': '/root', 'acceptance': ref(out / 'ROOT-ACCEPTANCE.json'),
    'new_units_and_role_references_directly_read': True, 'retained15_fact_bytes_reused_from_exact_root05_direct_read': True,
    'all_five_effects_owners_guards_and_receivers_unchanged': True,
    'worker_checks': ref(out / 'CHECKS-v1.json'), 'root_actual_request_consumer_rerun': False,
    'operating_native_qualified_records': 0, 'Gemini_calls': 0})
print(json.dumps({'research_accepted': 1, 'facts': 15, 'units': 5, 'operating_qualified': 0}))
