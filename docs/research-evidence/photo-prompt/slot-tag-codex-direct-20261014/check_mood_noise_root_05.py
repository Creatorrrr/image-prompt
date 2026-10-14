"""Actual two source proofs on explicit independent synthetic core witnesses."""
import copy
import gzip
import hashlib
import importlib.abc
import json
import sys
from pathlib import Path

ROOT = Path.cwd(); R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
FORBIDDEN = {'torch', 'transformers', 'sentence_transformers',
             'tensorflow', 'jax', 'mlx', 'google', 'openai', 'anthropic', 'litellm', 'ollama'}
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in FORBIDDEN: raise AssertionError('forbidden model/provider import: ' + fullname)
sys.meta_path.insert(0, Deny()); sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_embedding_provider as provider
import photo_local_embedding as local
def no_embedding(*args, **kwargs): raise AssertionError('embedding execution forbidden in this controlled check')
provider.embed = no_embedding
provider.embed_many = no_embedding
local.infer = no_embedding
import prompt_generator as generator
TEXT = 'Independent synthetic fixture: image I is existing and present within canvas C, and scene S is an existing context. I is part of C and disjoint from S. IA is an exact alias of image I. This declares no human, camera, low-light scene or measured capture ISO.'

def assertion(aid, kind, dimension='subject', **axes):
    return {'assertion_id': aid, 'dimension': dimension, 'polarity': 'required', 'source_span_ids': ['fixture'],
            'affected_dimensions': [dimension], 'axes': {'native_schema': 'photo-frozen-semantics/v1', 'kind': kind, **axes},
            'evidence': {'meaning': TEXT}}

def core():
    rows = [assertion('owner_' + owner, 'owner', owner=owner, owner_kind=('context' if owner == 'S' else 'image')) for owner in ['I', 'IA', 'C', 'S']]
    rows += [assertion('role_image', 'role', owner='I', role='image'), assertion('role_scene', 'role', owner='S', role='scene'),
             assertion('image_present', 'fact', owner='I', property='entity.presence', value_type='entity.presence/v1', value='present'),
             assertion('alias_image', 'equivalent', left='I', right='IA'), assertion('within_canvas', 'part_of', left='I', right='C'),
             assertion('different_scene', 'disjoint', left='I', right='S')]
    return {'contract_version': 'photo-authorial-core/v3', 'subject': TEXT, 'baseline_prompt_en': TEXT,
            'request_binding': {'active_spans': [{'source_span_id': 'fixture', 'text': TEXT}]}, 'semantic_assertions': rows,
            'user_exclusions': [], 'intent_lock': {'contract_version': 'photo-intent-lock/v2',
            'locked_dimensions': ['age', 'concept', 'count', 'event', 'identity', 'subject'],
            'open_dimensions': ['atmosphere', 'style'], 'semantic_anchors': []}}

def remove(state, aid):
    result = copy.deepcopy(state); result['semantic_assertions'] = [row for row in result['semantic_assertions'] if row['assertion_id'] != aid]
    return result

def contract(domains):
    return {'subject_category': 'environment', 'domains': domains, 'adult_allowed': False,
            'intent_constraints': {'subject_categories': ['environment'], 'domains': domains}}

def check(label, got, expected, output):
    assert got == expected, (label, got, expected)
    output.append({'case': label, 'expected': expected, 'observed': got})

results = []
for ordinal, role, target, dimension, prop in [(3107, 'mood', 'S', 'atmosphere', 'mood.burnout_reset'), (3169, 'grain_profile', 'I', 'style', 'rendering.noise')]:
    revision = '03' if ordinal == 3169 else '01'
    O = R / f'native_batches/root-{ordinal:05d}-149-{revision}'; B = json.loads((O / 'BATCH.json').read_bytes()); row = B['records'][0]
    D = R / f'native-inputs/prepared/root-{ordinal:05d}-149-{revision}'; I = json.loads((D / 'INPUT.json').read_bytes())
    data = json.loads(gzip.decompress((ROOT / I['current_snapshot']['file']).read_bytes()))
    record = copy.deepcopy(row['source_after']); record['content']['role_evidence'] = row['proof']; data['candidates'][record['id']] = record
    bid = next(key for key, binding in data['slot_bindings'].items() if binding['candidate_id'] == record['id'])
    entry = c.entry(data, record['id'], bid, realization_id='base'); base = core(); cases = []
    for view in ['full', 'compact']:
        e = copy.deepcopy(entry); e.pop('_semantic_evidence_guard' if view == 'full' else 'role_evidence', None)
        check(view + ':actual_source_bound_role_qualified', n.qualification(data['slot_catalog'][role], e, source_data=data)['status'] == 'eligible', True, cases)
        if ordinal == 3169:
            check(view + ':manual_view_without_full_source_authority_denied', n.qualification(data['slot_catalog'][role], e)['status'] == 'eligible', False, cases)
        check(view + ':independent_actual_owner_admission', n.admission(e, base)['allowed'], True, cases)
        check(view + ':open_property_permission', n.property_scope_allowed(base, e['affected_dimensions'], e['affected_properties'], record=e), True, cases)
        check(view + ':own_binding_consumer_open', generator.core_entry_eligible(data, base, contract([]), {'subject': {'kind': ['environment'], 'tags': ['environment']}}, role, e), True, cases)
        missing = remove(base, 'role_scene' if ordinal == 3107 else 'role_image')
        check(view + ':missing_exact_role_denied', n.admission(e, missing)['allowed'], False, cases)
        if ordinal == 3169:
            check(view + ':missing_image_presence_denied', n.admission(e, remove(base, 'image_present'))['allowed'], False, cases)
            for domain in ['product', 'jewelry', 'food']:
                check(view + ':actual_binding_deny_' + domain, generator.core_entry_eligible(data, base, contract([domain]), {'subject': {'kind': ['environment'], 'tags': ['environment']}}, role, e), False, cases)
        for owner, expected in [(target, False), ('IA' if ordinal == 3169 else 'I', ordinal == 3107), ('C', False)]:
            lock = copy.deepcopy(base); lock['intent_lock']['semantic_anchors'] = [{'dimension': dimension, 'target': owner, 'property': prop}]
            check(view + ':exact_property_lock_' + owner, n.property_scope_allowed(lock, e['affected_dimensions'], e['affected_properties'], record=e), expected, cases)
        if ordinal == 3169:
            original_lock = copy.deepcopy(base); original_lock['intent_lock']['semantic_anchors'] = [{'dimension': 'style', 'target': 'I', 'property': 'rendering.noise'}]
            check(view + ':original_actual_noise_property_lock_denied', n.property_scope_allowed(original_lock, e['affected_dimensions'], e['affected_properties'], record=e), False, cases)
        parent = copy.deepcopy(base); parent['intent_lock']['semantic_anchors'] = [{'dimension': dimension, 'target': target, 'property': prop.split('.')[0]}]
        check(view + ':parent_property_lock_denied', n.property_scope_allowed(parent, e['affected_dimensions'], e['affected_properties'], record=e), False, cases)
        whole = copy.deepcopy(base); whole['intent_lock']['open_dimensions'].remove(dimension); whole['intent_lock']['locked_dimensions'].append(dimension)
        check(view + ':whole_dimension_consumer_denied', generator.core_entry_eligible(data, whole, contract([]), {'subject': {'kind': ['environment'], 'tags': ['environment']}}, role, e), False, cases)
    results.append({'ordinal': ordinal, 'candidate_id': record['id'], 'proof_sha256': c.digest(row['proof']),
                    'actual_binding_id': bid, 'actual_binding_sha256': c.digest(data['slot_bindings'][bid]), 'checks': cases})
modules = {}
for name, module in sorted(sys.modules.items()):
    if (name.startswith('photo_') or name == 'prompt_generator') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(G), (name, path)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
assert not [name for name in sys.modules if name.split('.')[0] in FORBIDDEN]
report = {'schema': 'photo-root-two-source-controlled-consumer-check/v1', 'actor': '/root', 'frozen_generation': str(G),
          'results': results, 'assertions_passed': sum(len(row['checks']) for row in results), 'all_passed': True,
          'modules': modules, 'os_network_denied': True, 'model_provider_Gemini_calls': 0, 'operating_changes': 0,
          'boundary': 'Actual two research source proofs and actual own bindings on independent synthetic owner/core witnesses, full and compact. No actual user request, hybrid retrieval, final compose/runtime receipt or pixels; no semantic oracle claim.'}
out = R / 'ROOT-MOOD-NOISE-CONSUMER-CHECK-05.json'
with out.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2); stream.write('\n')
print(json.dumps({'assertions_passed': report['assertions_passed'], 'all_passed': True, 'model_calls': 0}))
