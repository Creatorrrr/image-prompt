"""Root's exact research acceptance and independent fixed-core controls.

The fixed requests are authored before loading any candidate. Their assertions
are direct literal fixture evidence, not graph facts imported from a proof.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import prompt_generator as generator
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(reviews.read_json(path))}


def core(state):
    text = 'R is an independently established adult person and the main subject. Wardrobe, posture and activity may change.'
    text += (' No reference appearance or requester identity is established.' if state == 'known_absent'
             else ' Whether any reference appearance or requester identity is established has not been reviewed.')
    sha = hashlib.sha256(text.encode()).hexdigest()
    binding = {'request_sha256': sha, 'request_envelope_sha256': hashlib.sha256(('root independent request: ' + text).encode()).hexdigest(),
        'input_inventory': {'schema': 'photo-request-input-inventory/v1', 'complete': True, 'items': [{'id': 'root_request', 'kind': 'request_text', 'sha256': sha}]},
        'active_spans': [{'source_span_id': 'root_request', 'text': text}]}
    def row(aid, dimension, kind, **axes):
        return {'assertion_id': aid, 'dimension': dimension, 'polarity': 'required',
            'source_span_ids': ['root_request'], 'axes': {'native_schema': 'photo-frozen-semantics/v1', 'kind': kind, **axes},
            'evidence': {'literal': text}, 'affected_dimensions': [dimension]}
    rows = [row('root_owner', 'subject', 'owner', owner='R', owner_kind='human'),
        row('root_role', 'subject', 'role', role='main_subject', owner='R'),
        row('root_presence', 'subject', 'fact', owner='R', property='entity.presence', value_type='entity.presence/v1', value='present'),
        row('root_adult', 'age', 'fact', owner='R', property='age.declared', value_type='age.declared/v1', value='adult')]
    for scope in ['reference_appearance', 'requester_identity']:
        inventory = {'schema': 'photo-frozen-scope-inventory/v1', 'complete': True,
            'input_binding': native.witnesses.input_binding(binding), 'reviewed_input_ids': ['root_request'], 'state': state, 'items': []}
        rows.append(row('root_' + scope, 'subject', 'scope_inventory', owner='R', scope_kind=scope, inventory=native.witnesses.canonical(inventory)))
    value = {'contract_version': 'photo-authorial-core/v3', 'subject': text, 'baseline_prompt_en': text,
        'request_binding': binding, 'semantic_assertions': rows, 'user_exclusions': [],
        'intent_lock': {'contract_version': 'photo-intent-lock/v2', 'locked_dimensions': ['subject', 'age', 'identity', 'count', 'concept'],
            'open_dimensions': ['appearance', 'pose', 'action'], 'semantic_anchors': []}}
    native.frozen_witnesses(value)
    return value


CORES = {'known_absent': core('known_absent'), 'unknown': core('unknown')}
before_candidate_core_sha256 = c.digest(CORES)
assignment = HERE / 'native-inputs/prepared/review08250-11128-04/ASSIGNMENT.json'
verified = reviews.verify_batch(str(assignment.relative_to(ROOT)), str((OUT / 'BATCH.json').relative_to(ROOT)), str((OUT / 'NOTE.json').relative_to(ROOT)))
batch = reviews.read_json(OUT / 'BATCH.json')
assert c.digest(batch) == '3a295377302f3b997cccf3e0d4cd3aeff2784c39c30f90872da2add2271c5f34'
assert len(batch['records']) == 1 and batch['records'][0]['status'] == 'approved'
record = batch['records'][0]; proof = record['proof']; cid = record['candidate_id']
assert len(proof['facts']) == 71 and len(proof['source_units']) == 26
assert proof['catalog_sha256'] == '5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
assert record['source_after']['content']['ko'] == '성인이 펜슬 스커트 차림으로 자연스럽게 서 있거나 걷는 전체 자세.'
for fid in ['standing_p2_pose', 'walking_p2_pose']:
    fact = next(row for row in proof['facts'] if row['id'] == fid)
    assert fact['pointer'] == '/content/ko' and fact['quote'] == '자연스럽게 서 있거나 걷는 전체 자세'
source = reviews.read_json(HERE / 'native-inputs/08250-special-quote-color-plan-03/CURRENT-PROPOSAL.json.gz')
qualified = copy.deepcopy(record['source_after']); qualified['content']['role_evidence'] = proof
corpus = {**source, 'candidates': {**source['candidates'], cid: qualified}}
binding = 'bind_17f21e3dd66a5d1aa97b3b38efaab469'
assert source['slot_bindings'][binding]['candidate_id'] == cid
cases = []; locks = []; consumers = []; groups = {}
contract = {'subject_category': 'human', 'adult_allowed': True, 'domains': [], 'intent_constraints': {'subject_categories': ['human'], 'domains': []}}
plan = {'subject': {'kind': ['human'], 'tags': ['human']}}
for rid in ['standing', 'walking']:
    full = native._guard_entry(proof, rid, {})
    compact = c.entry(corpus, cid, realization_id=rid)
    for form, entry in [('full', full), ('compact', compact)]:
        for label in ['known_absent', 'unknown', 'no_adult', 'no_presence', 'wrong_adult']:
            request = copy.deepcopy(CORES['unknown' if label == 'unknown' else 'known_absent'])
            if label in ['no_adult', 'no_presence']:
                wanted = 'root_adult' if label == 'no_adult' else 'root_presence'
                request['semantic_assertions'] = [row for row in request['semantic_assertions'] if row['assertion_id'] != wanted]
            if label == 'wrong_adult':
                next(row for row in request['semantic_assertions'] if row['assertion_id'] == 'root_adult')['axes']['value'] = 'child'
            actual = native.admission(entry, request)
            assert actual['allowed'] is (label == 'known_absent'), (rid, form, label, actual)
            cases.append({'rid': rid, 'form': form, 'case': label, 'result': actual})
        for effect in proof['effect_sets'][rid]['properties']:
            request = copy.deepcopy(CORES['known_absent'])
            request['intent_lock']['semantic_anchors'].append({'dimension': effect['dimension'], 'target': 'R', 'property': effect['property']})
            dimensions, properties, _ = native.permission_scope(entry, request)
            assert not native.property_scope_allowed(request, dimensions, properties)
            locks.append({'rid': rid, 'form': form, 'property': effect, 'denied': True})
    presentation = c.entry(corpus, cid, binding, realization_id=rid)
    for label in ['human_open', 'adult_not_allowed', 'documentary_binding_denied']:
        tested = copy.deepcopy(contract)
        if label == 'adult_not_allowed': tested['adult_allowed'] = False
        if label == 'documentary_binding_denied':
            tested['domains'] = tested['intent_constraints']['domains'] = ['documentary']
        actual = generator.core_entry_eligible(corpus, CORES['known_absent'], tested, plan, 'wardrobe_style', presentation)
        assert actual is (label == 'human_open'), (rid, label, actual)
        consumers.append({'rid': rid, 'original_binding_id': binding, 'case': label, 'allowed': actual})
for fact in proof['facts']:
    if fact['mode'] == 'effect':
        key = (fact['realization_id'], fact['dimension'], fact['target'], fact['property'])
        value = (c.canonical_bytes(fact['value']), fact['operation'], frozenset(fact['receivers']))
        assert key not in groups or groups[key] == value
        groups[key] = value
assert c.digest(CORES) == before_candidate_core_sha256
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {key: value for key, value in verified.items() if key != 'records'}
report.update({'schema': 'photo-root-posture-quote-verification/v1', 'frozen_generation': GEN.name,
    'used_frozen_modules': modules, 'root_complete_source_71facts_26units_and_four_used_specs_read': True,
    'candidate_free_literal_fixture_cores': CORES, 'core_before_candidate_load_sha256': before_candidate_core_sha256,
    'admission_cases': cases, 'locked_properties': locks, 'actual_original_binding_consumers': consumers,
    'same_effect_assignment_groups': len(groups), 'effect_assignment_conflicts': 0,
    'source_and_bindings_not_operationally_applied': True, 'os_network_denied': True,
    'provider_keys_removed': True, 'provider_or_embedding_calls': 0, 'gemini_calls': 0,
    'operational_native_qualified_records': 0, 'actual_request_workflow_or_full144_search_or_pixels_performed': False})
save(OUT / 'ROOT-VERIFICATION-01.json', report)
acceptance = {'schema': reviews.ACCEPTANCE, 'actor': '/root',
    **{key: verified[key] for key in ['assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256']},
    'reviews': {cid: {'review_sha256': c.digest(row), 'status': row['status']} for cid, row in verified['records'].items()},
    'reason': 'Accept this exact current144V4 research revision after root complete corrected source, all71 facts/26 units, four used full specs, guards/owners/both RIDs and own-binding read. Both Korean pose facts now cite their own explicit naturalness qualifier. Root independently declared request cores before candidate loading, checked20 full/compact prerequisite cases,10 whole-effect locks and6 actual original-binding/adult/domain consumers. Preserve adult P, wardrobe/posture/walking E, exact alternatives and conditional established-scope protection. This is no operating activation, full-corpus approval, actual request/search or pixel validation. A later source/catalog dependency change requires separate review; never automatically rebind this acceptance.'}
save(OUT / 'ROOT-ACCEPTANCE.json', acceptance)
reviews.verify_acceptance(ROOT, ref(OUT / 'ROOT-ACCEPTANCE.json'), verified)
print(json.dumps({'root_accepted_research_records': 1, 'facts': 71, 'units': 26, 'admission_cases': len(cases), 'lock_cases': len(locks), 'binding_consumers': len(consumers), 'operational_native_qualified_records': 0, 'gemini_calls': 0}))
