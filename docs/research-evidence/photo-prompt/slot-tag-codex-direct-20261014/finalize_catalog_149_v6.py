"""Select four directly reviewed spec deltas as new research input, no adoption."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore'), str(HERE)]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def read(name): return reviews.read_json(HERE / name)


def ref(name):
    p = HERE / name
    return {'file': str(p.relative_to(ROOT)), 'file_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(name, value):
    with (HERE / name).open('xb') as stream: stream.write(c.canonical_bytes(value) + b'\n')
    return ref(name)


proposal_name = 'authored/native_12250_catalog149_v6_proposal_20261015.json'
proposal = read(proposal_name)
assert c.digest(proposal) == '96bd87a91c37d35162a66d9a0bc7a42da969394044afd30df7470831f39e7878'
previous = read('CATALOG-FINAL-146-V5.json')
assert c.digest(previous) == '3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
after = read('authored/native_12250_catalog149_v6_proposal_20261015.catalog-compact.json')
assert c.digest(after) == 'd9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
assert len(after) == 149 and len(previous) == 146
new = ['material_mechanics', 'material_thickness', 'physical_mass']
assert sorted(set(after) - set(previous)) == new
assert sorted(key for key in previous if previous[key] != after[key]) == ['body_pose']
assert sorted(key for key in previous['body_pose'] if previous['body_pose'][key] != after['body_pose'][key]) == ['description', 'description_ko', 'excludes', 'includes']
assert all(after[key] == value for key, value in previous.items() if key != 'body_pose')
assert after['relational_action'] == previous['relational_action']
mechanics = read('authored/native_12250_taxonomy_mechanics_articulation_relational_20261015.json')
mass = read('authored/native_12250_taxonomy_mass_20261015.json')
assert after['material_mechanics'] == mechanics['research_new_slots']['material_mechanics']
assert after['material_thickness'] == mechanics['research_new_slots']['material_thickness']
assert after['physical_mass'] == mass['after']
assert after['body_pose'] == mechanics['existing_spec_revision_proposals']['body_pose']['after']
original = read('CATALOG.json')
old_review = read('CATALOG-FINAL-146-V5-REVIEW.json')
reasons = {row['pointer'][1:]: row['reason'] for row in old_review['changes']}
reasons.update({
    'material_mechanics': 'Explicit material softness/hardness/rigidity/flexibility/deformation response on its actual carrier, separate from material identity/optics/static form/motion. Actual toe ring, polymer/channel and flexible-layer witnesses; no inferred measurement, mass, temperature or new anatomy.',
    'material_thickness': 'Explicit material-layer/cross-section thickness, separate from in-plane width, garment volume and opacity. Actual thin trouser fabric and thick plastic-layer edges; ambiguous headband width remains pending, no invented cross-sectional axis.',
    'physical_mass': 'Explicit carrier mass or physical heaviness/lightness, including qualitative heavy ledger/gate and KO lightweight trousers. Preserve qualitative actual meaning without requiring grams. Visual/compositional weight and lightweight-looking remain excluded; no inferred density/body weight or measurement certification.',
    'body_pose': 'Retain whole-body posture/support and add explicitly stated owned non-hand local articulation such as bent elbow. Do not infer limbs/anatomy/full stance/current motion; hand articulation and body-axis orientation retain specialized boundaries, no same flexion double tag.'})
provenance_names = [
    'CATALOG-FINAL-146-V5-REVIEW.json', 'CATALOG-FINAL-146-V5-ACCEPTANCE.json', 'ROOT-FINAL-CATALOG-146-V5-VERIFICATION.json',
    'authored/native_12250_taxonomy_mechanics_articulation_relational_20261015.json',
    'worker-notes/native-12250-taxonomy-mechanics-articulation-relational-20261015.json',
    'authored/native_12250_taxonomy_mass_20261015.json', 'worker-notes/native-12250-taxonomy-mass-20261015.json',
    proposal_name, 'worker-notes/native_12250_catalog149_v6_proposal_20261015.json']
changed = sorted(key for key in set(original) | set(after) if original.get(key) != after.get(key))
review = {'reviewer': 'Codex/root delta direct review with exact prior146 whole-catalog provenance and delegated sol/high bounded source/spec review',
    'whole_catalog_reviewed': True, 'before': copy.deepcopy(original), 'after': copy.deepcopy(after),
    'changes': [{'pointer': '/' + key, 'before_exists': key in original, 'before': original.get(key), 'after_exists': key in after, 'after': after.get(key), 'reason': reasons[key]} for key in changed],
    'provenance': [ref(name) for name in provenance_names]}
reviews.verify_catalog(original, after, review, ROOT)
container = copy.deepcopy(read('SOURCE.json.gz')); container['slot_catalog'] = copy.deepcopy(after)
c.validate(container)
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        p = Path(module.__file__).resolve(); assert p.is_relative_to(GEN), (name, str(p))
        modules[name] = {'file': str(p), 'file_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
catalog = save('CATALOG-FINAL-149-V6.json', after)
review_ref = save('CATALOG-FINAL-149-V6-REVIEW.json', review)
acceptance = save('CATALOG-FINAL-149-V6-ACCEPTANCE.json', {
    'schema': 'photo-codex-final-catalog-acceptance/v1', 'actor': '/root',
    'status': 'final_for_fresh_native_direct_reviews_not_canonical_application',
    'catalog': catalog, 'catalog_count': 149, 'catalog_ids': sorted(after), 'catalog_sha256': c.digest(after),
    'previous_catalog': ref('CATALOG-FINAL-146-V5.json'), 'review': review_ref,
    'new_slots': new, 'changed_existing_specs': ['body_pose'], 'unchanged145_exact_prior_read_provenance_retained': True,
    'fresh_personal_whole149_read_claimed': False,
    'root_direct_read_basis': 'Root directly read complete four changed/new specs and full relevant neighbor specs, whole original/current/old5B/after/ownbinding/closure on4529/4714/4998/5033/5113/5210 and3749/5033/5901/6303/7129. Mass full five witnesses were reread;5033 is not counted twice toward bulk. Earlier related witness summaries are not whole-source claims.',
    'whole_catalog_read_basis': '145 byte-identical definitions preserve exact prior146 provenance. New3 and changed body_pose use pinned worker whole-spec/source review and bounded root direct delta review. Equality is not a new semantic read.',
    'source_and_binding_conditions_remain_conjunctive': True,
    'candidate_role_fact_mode_owner_receiver_decisions_granted': 0,
    'old_sources_drafts_proofs_statuses_acceptances_changed': False,
    'native_requalification_required': True, 'operational_catalog_changed': False,
    'operational_native_qualified_records': 0, 'stages05_08_complete': False, 'gemini_calls': 0})
approval = save('NATIVE-CATALOG-APPROVAL-149-V6.json', {
    'schema': 'photo-codex-native-input-catalog-approval/v1', 'actor': '/root', 'status': 'final_approved',
    'catalog': catalog, 'catalog_count': 149, 'catalog_ids': sorted(after), 'catalog_sha256': c.digest(after), 'review': review,
    'reason': 'Accept exact149 definitions for fresh research input only. No operating catalog/source/tag or old proof/status conversion. Actual carrier, local part, modes, receivers, all source/binding guards and whole permission remain cumulative. Prefix overlap never supplies semantic fit or a duplicate role.'})
save('ROOT-FINAL-CATALOG-149-V6-VERIFICATION.json', {
    'schema': 'photo-root-final-catalog-verification/v1', 'actor': '/root',
    'catalog': catalog, 'review': review_ref, 'acceptance': acceptance, 'input_approval': approval,
    'whole18250_container_integrity': 'pass', 'all149_spec_schema_dimensions_neighbor_refs': 'pass',
    'new_slots': new, 'changed_existing_specs': ['body_pose'], 'unchanged145_existing_from146_exact': True,
    'relational_action_unchanged': True, 'native_candidate_approvals': 0, 'canonical_changes': 0,
    'used_frozen_modules': modules, 'os_network_denied': True, 'provider_keys_removed': True,
    'local_inference_calls': 0, 'gemini_calls': 0, 'stages05_08_complete': False})
print(json.dumps({'catalog_count': 149, 'catalog_sha256': c.digest(after), 'fresh_input_approved': True, 'operating_changes': 0}))
