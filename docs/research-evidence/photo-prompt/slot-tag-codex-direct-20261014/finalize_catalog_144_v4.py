"""Root's explicit one-spec artificial-face followup to the whole144 review.

The unchanged143 specifications retain exact prior read provenance. Root read
the new complete expression before/after, all5 full witnesses/bindings and9
neighbor specs. This writes research input approval only, never native proofs.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GENERATION = '534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as corpus
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]


def read(name):
    return reviews.read_json(HERE / name)


def artifact(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': corpus.digest(read(name))}


def save(name, value):
    with (HERE / name).open('xb') as stream:
        stream.write(corpus.canonical_bytes(value) + b'\n')
    return artifact(name)


name = 'authored/catalog_expression_artificial_face_12250.proposal_v2.json'
proposal = read(name)
assert corpus.digest(proposal) == 'b3ee2a1e7626a385ee63f10e5dbb0c805513eb09d4ca0c869113a60dfae2f57b'
old_proposal = read('authored/catalog_expression_artificial_face_12250.proposal.json')
previous = read('CATALOG-FINAL-144-V3.json')
before = read('CATALOG.json')
original = read('SOURCE.json.gz')
assert proposal['before'] == previous['expression']
assert corpus.digest(previous) == proposal['base_catalog_sha256'] == '20ba9b75b3afa86ec02a1aa7a7d750eda86ca61c99573d03c94ea12ea9375c39'
# Exact root-requested removal of the unreviewed new eye-closure restriction.
literal = copy.deepcopy(old_proposal['after'])
literal['excludes'][1] = 'Eye or iris direction, a named gaze target or camera/participant engagement alone; these properties require their own evidence and roles.'
assert literal == proposal['after']
after = copy.deepcopy(previous)
after['expression'] = copy.deepcopy(proposal['after'])
assert len(after) == 144 and sum(after[key] != previous[key] for key in after) == 1
assert corpus.digest(after) == proposal['hypothetical_catalog_sha256'] == '5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
source_checks = []
for witness in proposal['witnesses']:
    cid = witness['candidate_id']
    assert original['candidates'][cid] == witness['source_before']
    assert corpus.digest(witness['source_before']) == witness['source_sha256']
    own = {key: row for key, row in original['slot_bindings'].items() if row['candidate_id'] == cid}
    assert own == witness['actual_own_bindings']
    assert witness['reference_records'] == witness['reference_bindings'] == {}
    source_checks.append({'ordinal': witness['ordinal'], 'candidate_id': cid,
        'whole_original_and_bindings_exact': True, 'root_whole_source_after5B_and_bindings_read': True,
        'native_facts_approved': False})
assert len(source_checks) == 5
for key, row in proposal['neighbors_directly_read'].items():
    assert row['spec'] == previous[key] and row['sha256'] == corpus.digest(previous[key])

old_review = read('CATALOG-FINAL-144-V3-REVIEW.json')
reasons = {row['pointer'][1:]: row['reason'] for row in old_review['changes']}
reasons['expression'] = 'Admit only a positively declared visible response on an actual artificial/represented face, as well as the existing human/animal scope. Retain actual owner/part conditions; no consciousness, private emotion, biological anatomy, gaze direction/target/engagement or additional actor is inferred. Keep the prior eye-area-response scope; no unreviewed eye-closure exclusion is added.'
changed = [key for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
review = {'reviewer': 'Codex/root with prior sol/high whole144 review and12250 direct expression followup',
    'whole_catalog_reviewed': True, 'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
    'changes': [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key),
                 'after_exists': key in after, 'after': after.get(key), 'reason': reasons[key]} for key in changed],
    'provenance': [artifact(item) for item in [
        'CATALOG-FINAL-144-V3-REVIEW.json', 'CATALOG-FINAL-144-V3-ACCEPTANCE.json',
        'ROOT-FINAL-CATALOG-144-V3-VERIFICATION.json',
        'authored/catalog_expression_artificial_face_12250.proposal.json',
        'authored/catalog_expression_artificial_face_12250.proposal_v2.json',
        'worker-notes/catalog_expression_artificial_face_12250.proposal.json',
        'worker-notes/catalog_expression_artificial_face_12250.proposal_v2.json']]}
reviews.verify_catalog(before, after, review, ROOT)
container = copy.deepcopy(original)
container['slot_catalog'] = copy.deepcopy(after)
corpus.validate(container)
modules = {}
for key, module in list(sys.modules.items()):
    if key.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (key, str(path))
        modules[key] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
catalog_ref = save('CATALOG-FINAL-144-V4.json', after)
review_ref = save('CATALOG-FINAL-144-V4-REVIEW.json', review)
acceptance_ref = save('CATALOG-FINAL-144-V4-ACCEPTANCE.json', {
    'schema': 'photo-codex-final-catalog-acceptance/v1', 'actor': '/root',
    'status': 'final_for_fresh_native_direct_reviews_not_canonical_application',
    'catalog': catalog_ref, 'catalog_count': 144, 'catalog_ids': sorted(after),
    'catalog_sha256': corpus.digest(after), 'original_catalog_sha256': corpus.digest(before),
    'previous_catalog': artifact('CATALOG-FINAL-144-V3.json'), 'review': review_ref,
    'changed_from_previous': ['expression'], 'new_slots_from_previous': 0,
    'root_personally_reread_complete_changed_specification': True,
    'root_personally_reread_all_five_source_witnesses': True,
    'whole_catalog_read_basis': '143 exact unchanged specs retain the pinned whole144 R02 direct-read evidence; the1 new complete expression spec was directly read by12250 androot. No new144-read count is inferred from hashes.',
    'root_review': reasons['expression'], 'source_witness_integrity': source_checks,
    'eye_closure_restriction_removed_before_acceptance': True,
    'represented_positive_source_example_claimed': False,
    'existing_source_intrinsic_and_binding_conditions_preserved': True,
    'old_expression_binding_robot_restriction_migrated': False,
    'historical_reviews_changed': False, 'native_requalification_required': True,
    'operational_catalog_changed': False, 'operational_native_qualified_records': 0,
    'stages05_08_complete': False, 'gemini_calls': 0,
})
approval_ref = save('NATIVE-CATALOG-APPROVAL-144-V4.json', {
    'schema': 'photo-codex-native-input-catalog-approval/v1', 'actor': '/root',
    'status': 'final_approved', 'catalog': catalog_ref, 'catalog_count': 144,
    'catalog_ids': sorted(after), 'catalog_sha256': corpus.digest(after), 'review': review,
    'reason': 'Root explicitly accepts the artificial-face expression followup to the complete144 catalog. Fresh direct-review input only. All original source guards and exact owner/part/mode/receiver/permission requirements remain mandatory; no source, binding, old proof or approval is converted.',
})
verification_ref = save('ROOT-FINAL-CATALOG-144-V4-VERIFICATION.json', {
    'schema': 'photo-root-final-catalog-verification/v1', 'actor': '/root',
    'catalog': catalog_ref, 'review': review_ref, 'acceptance': acceptance_ref,
    'input_approval': approval_ref, 'changed_specs_from144V3': 1,
    'unchanged143_exact_and_prior_read_provenance_retained': True,
    'changed_specs_from139': len(changed), 'source_witnesses_exact': source_checks,
    'complete18250_container_integrity': 'pass', 'all144_spec_schema_neighbor_dimensions': 'pass',
    'canonical_mutations': 0, 'candidate_native_approvals': 0,
    'frozen_code_generation': GENERATION, 'used_frozen_modules': modules,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0,
    'local_inference_inputs': 0, 'stages05_08_complete': False,
})
print(json.dumps({'catalog': catalog_ref, 'review': review_ref, 'acceptance': acceptance_ref,
    'native_input_approval': approval_ref, 'verification': verification_ref,
    'canonical_changes': 0, 'native_source_approvals': 0}))
