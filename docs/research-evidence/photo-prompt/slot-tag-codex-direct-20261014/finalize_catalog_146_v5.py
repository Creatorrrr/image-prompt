"""Approve the explicitly reviewed146 catalog as fresh research input only.

The136 unchanged existing definitions retain exact prior whole-catalog read
provenance. The10 changed/new definitions use the pinned root/independent
direct reads. This is not a fresh146 personal-read claim or a candidate approval.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as corpus
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def read(name):
    return reviews.read_json(HERE / name)


def artifact(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': corpus.digest(read(name))}


def save(name, value):
    with (HERE / name).open('xb') as stream:
        stream.write(corpus.canonical_bytes(value) + b'\n')
    return artifact(name)


proposal_name = 'authored/root_catalog146_v5_humidity_proposal_04.json'
proposal = read(proposal_name)
assert corpus.digest(proposal) == 'c2d7c5e2696c1deab3e20847b683b30f1ec1c06f5758008099eddc6db400bab2'
peer145 = artifact('worker-notes/native-12250-root145-v5-independent-20261015.json')
peer146 = artifact('worker-notes/native-12250-root146-v5-independent-20261015.json')
assert peer145['file_sha256'] == '40193e7a226ef536b2701a7d3051e34646d341be4f1f1ebb236145e09fa1806c'
assert peer146['file_sha256'] == 'bfe136de1e17c964ddc5005f216b6db0ddf26c6f2f3866aaf9bd007db5d90bdd'
before = read('CATALOG.json')
previous = read('CATALOG-FINAL-144-V4.json')
after = copy.deepcopy(proposal['proposed_catalog'])
assert corpus.digest(previous) == '5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
assert corpus.digest(after) == '3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
assert len(after) == 146 and len(previous) == 144
changed_previous = sorted(key for key in after if previous.get(key) != after[key])
assert changed_previous == proposal['changed_or_new_specs_from144']
assert sum(after[key] == value for key, value in previous.items()) == 136
old_review = read('CATALOG-FINAL-144-V4-REVIEW.json')
reasons = {row['pointer'][1:]: row['reason'] for row in old_review['changes']}
reasons.update({
    'age_presentation': 'Keep explicit whole-carrier and owned local-region visible age presentation distinct from chronological age. Exact region ownership remains mandatory. Local skin/age meaning has consistent appearance and age permission projections; source adult guards remain unchanged.',
    'air_humidity': 'Add the explicit physical humidity state of an actual air/zone carrier indoors or outdoors. Actual4948 declares humid growing-room air without fog, wet surfaces, temperature or measured RH. Preserve complete state, number/unit qualifiers only when actually stated; humidity does not infer optical response or a weather cause.',
    'atmospheric_medium': 'Retain the existing continuous spatial optical-response role. Add only a reciprocal humidity-only exclusion and air_humidity neighbor. Independently declared humidity and haze may coexist; neither proves the other.',
    'gaze_target': 'Remove blanket human/wildlife gates while retaining actual human/animal/represented gaze-carrier and eye/target evidence. A phone camera target is not the recording camera, viewer engagement, hardware aim or actual cognition. Original source and binding conditions remain conjunctive.',
    'material_form': 'Add actual macroscopic contour/shape of a declared free fluid/coherent material mass/transient material body. Teardrop flame-body form is not projected light geometry or lamp housing. No anatomy, new body, temperature, mechanism or ritual is inferred.',
    'object_structure': 'Add the reciprocal free-material-body exclusion while retaining discrete object/fixture/constructed item geometry and part assembly. Soft constructed bags/textile panels remain constructed objects; a same contour is not duplicated by renaming its owner.',
    'occasion_context': 'Repair the Korean inclusion/exclusion contradiction against the unchanged English occasion/event definition. Generic preparation, review or work stages alone are not occasions. A source-declared event may coexist with its procedural/narrative phase; fictional depiction does not require authenticated history. Keep all existing applicability and role scope.',
    'proxemics': 'Remove blanket human/wildlife gates for explicitly declared participant spacing such as natural flock spacing. Actual participants, endpoints/membership and physical gaps remain independently grounded. No count, crowd density, intimacy, composition or part posture is inferred.',
    'skin_finish': 'Permit explicitly declared biological, synthetic and represented skin finish only on its real owned skin region. Synthetic matte skin/pores stay artificial; material identity alone does not establish finish or living anatomy. Local age contrast retains its actual scoped age/appearance projections without duplicate owners or arbitrary extra tags.',
    'space_condition': 'Admit explicit natural/built place-zone physical exposure/inundation state separately from location, tide/event phase and surface wetness. Preserve all simultaneous zones and actual medium, high-tide reference and internally consistent tide state. Existing/preserved and selected states retain their actual modes, with original source/binding gates unchanged.'})
changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
provenance = [artifact(name) for name in [
    'CATALOG-FINAL-144-V4-REVIEW.json', 'CATALOG-FINAL-144-V4-ACCEPTANCE.json', 'ROOT-FINAL-CATALOG-144-V4-VERIFICATION.json',
    'authored/native_catalog_v5_gap_proposal_01.json', 'authored/native_catalog_v5_gap_proposal_02.json',
    'authored/root_catalog145_v5_boundary_proposal_03.json', proposal_name,
    'worker-notes/native-12250-root145-v5-independent-20261015.json', 'worker-notes/native-12250-root146-v5-independent-20261015.json']]
review = {'reviewer': 'Codex/root with exact prior144 whole-catalog read provenance and sol/high independent145/146 delta reviews',
    'whole_catalog_reviewed': True, 'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
    'changes': [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key), 'after_exists': key in after, 'after': after.get(key), 'reason': reasons[key]} for key in changed],
    'provenance': provenance}
reviews.verify_catalog(before, after, review, ROOT)
original = read('SOURCE.json.gz')
container = copy.deepcopy(original)
container['slot_catalog'] = copy.deepcopy(after)
corpus.validate(container)
modules = {}
for key, module in list(sys.modules.items()):
    if key.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN), (key, str(path))
        modules[key] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
catalog = save('CATALOG-FINAL-146-V5.json', after)
review_ref = save('CATALOG-FINAL-146-V5-REVIEW.json', review)
acceptance = save('CATALOG-FINAL-146-V5-ACCEPTANCE.json', {
    'schema': 'photo-codex-final-catalog-acceptance/v1', 'actor': '/root',
    'status': 'final_for_fresh_native_direct_reviews_not_canonical_application',
    'catalog': catalog, 'catalog_count': 146, 'catalog_ids': sorted(after), 'catalog_sha256': corpus.digest(after),
    'previous_catalog': artifact('CATALOG-FINAL-144-V4.json'), 'review': review_ref,
    'changed_or_new_from144': changed_previous, 'new_slots': ['air_humidity', 'material_form'],
    'unchanged136_exact_prior_read_provenance_retained': True,
    'root_direct_changed_spec_and_witness_read_basis': [artifact('authored/root_catalog145_v5_boundary_proposal_03.json'), artifact(proposal_name)],
    'independent_changed_spec_and_witness_read_basis': [peer145, peer146],
    'fresh_personal_whole146_read_claimed': False,
    'whole_catalog_read_basis': '136 exact unchanged existing definitions retain pinned144V4/earlier whole-catalog direct-read provenance. The10 changed/new definitions and nine actual witnesses use the explicitly bounded root and independent delta reads. Hash equality is not counted as a new read.',
    'source_and_binding_conditions_remain_conjunctive': True,
    'candidate_role_fact_mode_owner_receiver_decisions_granted': 0,
    'old_sources_drafts_proofs_statuses_acceptances_changed': False,
    'native_requalification_required': True, 'operational_catalog_changed': False,
    'operational_native_qualified_records': 0, 'stages05_08_complete': False, 'gemini_calls': 0})
approval = save('NATIVE-CATALOG-APPROVAL-146-V5.json', {
    'schema': 'photo-codex-native-input-catalog-approval/v1', 'actor': '/root', 'status': 'final_approved',
    'catalog': catalog, 'catalog_count': 146, 'catalog_ids': sorted(after), 'catalog_sha256': corpus.digest(after),
    'review': review,
    'reason': 'Root explicitly accepts these exact146 definitions for fresh native direct-review input. No operating catalog/source/tag, old draft/proof/status or candidate approval is converted. Exact source intrinsic/binding guards and actual owner/part/typed-mode/receiver/permission obligations remain mandatory.'})
verification = save('ROOT-FINAL-CATALOG-146-V5-VERIFICATION.json', {
    'schema': 'photo-root-final-catalog-verification/v1', 'actor': '/root',
    'catalog': catalog, 'review': review_ref, 'acceptance': acceptance, 'input_approval': approval,
    'whole18250_container_integrity': 'pass', 'all146_spec_schema_dimensions_neighbor_refs': 'pass',
    'new_slots': ['air_humidity', 'material_form'], 'changed_or_new_from144': changed_previous,
    'unchanged136_existing_from144_exact': True, 'native_candidate_approvals': 0, 'canonical_changes': 0,
    'used_frozen_modules': modules, 'os_network_denied': True, 'provider_keys_removed': True,
    'local_inference_calls': 0, 'gemini_calls': 0, 'stages05_08_complete': False})
print(json.dumps({'catalog': catalog, 'verification': verification, 'fresh_input_approved': True, 'native_candidate_approvals': 0, 'canonical_changes': 0}))
