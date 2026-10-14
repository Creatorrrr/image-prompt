"""Root direct weather review and independent literal-core controls, offline."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore'), str(HERE)]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import native_reviews as reviews
import photo_embedding_provider as provider


def forbidden(*args, **kwargs):
    raise RuntimeError('root weather checks forbid every embedding/provider execution')


provider.embed = provider.embed_many = forbidden
import prompt_generator as generator


def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(reviews.read_json(path))}


TEXT = 'Root independent synthetic fixture: scene S is an existing entity with entity.presence=present and is selected at scene role. Weather and atmosphere remain open. No existing rain, umbrella, humidity, wet surface, temperature or safety claim is established.'


def core():
    def row(aid, kind, **axes):
        return {'assertion_id': aid, 'dimension': 'subject', 'polarity': 'required',
            'source_span_ids': ['root_request'], 'affected_dimensions': ['subject'],
            'axes': {'native_schema': 'photo-frozen-semantics/v1', 'kind': kind, **axes},
            'evidence': {'literal': TEXT}}
    return {'contract_version': 'photo-authorial-core/v3', 'subject': TEXT, 'baseline_prompt_en': TEXT,
        'request_binding': {'active_spans': [{'source_span_id': 'root_request', 'text': TEXT}]},
        'semantic_assertions': [row('root_owner', 'owner', owner='S', owner_kind='entity'),
            row('root_role', 'role', owner='S', role='scene'),
            row('root_presence', 'fact', owner='S', property='entity.presence', value_type='entity.presence/v1', value='present')],
        'user_exclusions': [], 'intent_lock': {'contract_version': 'photo-intent-lock/v2',
            'locked_dimensions': ['subject', 'identity', 'count', 'age', 'concept'],
            'open_dimensions': ['atmosphere'], 'semantic_anchors': []}}


BASE = core()
core_before_source = c.digest(BASE)
assignment = HERE / 'native-inputs/prepared/review11870-01257-05/ASSIGNMENT.json'
verified = reviews.verify_batch(str(assignment.relative_to(ROOT)), str((OUT / 'BATCH.json').relative_to(ROOT)), str((OUT / 'NOTE.json').relative_to(ROOT)))
batch = reviews.read_json(OUT / 'BATCH.json')
assert c.digest(batch) == '3e165578f1ccd8202c248a093051629898b8645b08036b10bdbac0d835bdf18e'
row = batch['records'][0]
cid, proof = row['candidate_id'], row['proof']
assert row['status'] == 'approved' and len(proof['facts']) == 3 and len(proof['source_units']) == 4
assert [fact['quote'] for fact in proof['facts'][1:]] == ['light drizzle that barely needs an umbrella', '우산이 없어도 되는 가벼운 이슬비']
assert proof['source_units'][-1]['disposition'] == 'semantic_reference'
source = reviews.read_json(HERE / 'native-inputs/bounded-source-applications-plan-05/CURRENT-PROPOSAL.json.gz')
qualified = copy.deepcopy(row['source_after']); qualified['content']['role_evidence'] = proof
corpus = {**source, 'candidates': {**source['candidates'], cid: qualified}}
native.validate(qualified, corpus['slot_catalog'], corpus=corpus)
bid = 'bind_9f46f3d1613b55f483b86c50b8b5f1b5'
assert corpus['slot_bindings'][bid] == {'candidate_id': cid, 'conditions': {'subject_applicability': {}}, 'id': bid, 'role': 'optional', 'semantic_role': 'direct', 'slot_id': 'weather', 'weight': .82}
compact = c.entry(corpus, cid, bid, realization_id='base')
full = copy.deepcopy(compact); full.pop('_semantic_evidence_guard', None)
forms = {'full': full, 'compact': copy.deepcopy(compact)}
forms['compact'].pop('role_evidence', None)
cases = [('open', copy.deepcopy(BASE), True)]
for label, aid in [('missing_presence', 'root_presence'), ('missing_role', 'root_role')]:
    request = copy.deepcopy(BASE); request['semantic_assertions'] = [item for item in request['semantic_assertions'] if item['assertion_id'] != aid]
    cases.append((label, request, False))
wrong = copy.deepcopy(BASE); wrong['semantic_assertions'][2]['axes']['value'] = 'absent'
cases.append(('wrong_presence_value', wrong, False))
admissions, consumers, locks = [], [], []
for form, entry in forms.items():
    for label, request, want in cases:
        result = native.admission(entry, request)
        assert result['allowed'] is want, (form, label, result)
        admissions.append({'form': form, 'case': label, 'result': result})
for category, domains in [('human', []), ('object', ['product'])]:
    contract = {'subject_category': category, 'domains': domains, 'adult_allowed': False,
        'intent_constraints': {'subject_categories': [category], 'domains': domains}}
    picked = {'subject': {'kind': [category], 'tags': [category]}}
    for label, request, want in cases:
        actual = generator.core_entry_eligible(corpus, request, contract, picked, 'weather', compact)
        assert actual is want, (category, label, actual)
        consumers.append({'actual_old_binding': bid, 'category': category, 'domains': domains, 'case': label, 'allowed': actual})
    for label in ['same_scene_weather_property', 'whole_atmosphere']:
        request = copy.deepcopy(BASE)
        if label == 'same_scene_weather_property':
            request['intent_lock']['semantic_anchors'].append({'dimension': 'atmosphere', 'target': 'S', 'property': 'weather.precipitation'})
        else:
            request['intent_lock']['open_dimensions'] = []
            request['intent_lock']['locked_dimensions'].append('atmosphere')
        allowed = generator.core_entry_eligible(corpus, request, contract, picked, 'weather', compact)
        assert not allowed, label
        locks.append({'category': category, 'case': label, 'allowed': allowed})
assert c.digest(BASE) == core_before_source
modules = {}
for name, module in list(sys.modules.items()):
    if (name.startswith('photo_') or name == 'prompt_generator') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {key: value for key, value in verified.items() if key != 'records'}
report.update({'schema': 'photo-root-light-drizzle-research-verification/v1',
    'root_whole_original_current_5B_ownbinding_3facts4units_and_weather_spec_read': True,
    'manual_meaning': 'Both original languages select qualitative light drizzle with minimal umbrella need. No numerical threshold or safety/prop/microclimate fact follows. The whole application is a manually retained partial restatement, while each full original weather quote directly anchors its own canonical fact.',
    'independent_literal_core_before_candidate_load': BASE, 'core_sha256': core_before_source,
    'admissions': admissions, 'actual_old_binding_consumers': consumers, 'locks': locks,
    'source_or_binding_activated': False, 'used_frozen_modules': modules,
    'native_operating_qualified_records': 0, 'Gemini_or_embedding_provider_calls': 0,
    'actual_request_workflow_hybrid_search_or_pixels': False})
save(OUT / 'ROOT-VERIFICATION-01.json', report)
acceptance = {'schema': reviews.ACCEPTANCE, 'actor': '/root',
    **{key: verified[key] for key in ['assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256']},
    'reviews': {key: {'review_sha256': c.digest(value), 'status': value['status']} for key, value in verified['records'].items()},
    'reason': 'Root accepts this exact single146V5 research proof after whole original/current/old5B/ownbinding/empty closure and all3facts4units/owner/effect/guard/full weather spec direct review. Both full original language weather clauses anchor their own qualitative selection; partial application references retain no umbrella addition or safety assertion. Root independently authored a pre-source literal scene core and verified8full/compact P cases,8actual oldbinding human/object-product consumers and4whole-property/dimension lock cases. Operating source, tags, catalog, full corpus and actual request/search/pixels remain unchanged/unverified.'}
save(OUT / 'ROOT-ACCEPTANCE.json', acceptance)
reviews.verify_acceptance(ROOT, ref(OUT / 'ROOT-ACCEPTANCE.json'), verified)
print(json.dumps({'research_accepted': 1, 'admission_cases': len(admissions), 'actual_binding_consumers': len(consumers), 'lock_cases': len(locks), 'operating_qualified': 0}))
