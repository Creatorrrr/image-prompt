"""Root-authored two individual native reviews; no automated meaning decision."""
import copy
import gzip
import hashlib
import importlib.abc
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
FORBIDDEN = {'photo_local_embedding', 'photo_embedding_provider', 'torch', 'transformers', 'sentence_transformers',
             'tensorflow', 'jax', 'mlx', 'google', 'openai', 'anthropic', 'litellm', 'ollama'}
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in FORBIDDEN:
            raise AssertionError('provider/model import forbidden: ' + fullname)
sys.meta_path.insert(0, Deny())
sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0, str(R))
import native_reviews as nr
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
assert Path(nr.native.__file__).resolve().is_relative_to(G)

def read(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')

def fact(fid, pointer, quote, dimension, target, prop, mode, value_type, value, requires):
    result = {'id': fid, 'realization_id': 'base', 'pointer': pointer, 'quote': quote,
              'dimension': dimension, 'target': target, 'property': prop, 'mode': mode,
              'value': {'type': value_type, 'value': value}, 'requires': requires}
    if mode == 'effect': result.update(operation='set_value', receivers=[])
    return result

for ordinal in [3107, 3169]:
    D = R / f'native-inputs/prepared/root-{ordinal:05d}-149-01'
    I, A, P = [read(D / name) for name in ['INPUT.json', 'ASSIGNMENT.json', 'PREPARED-PACKET.json']]
    cid = A['ids'][0]
    source = copy.deepcopy(P['current_records'][cid]); before = P['original_records'][cid]
    corpus = read(ROOT / I['current_snapshot']['file'])
    assert c.digest(corpus) == '987964e32ed8459c2edeb0a439f7779374accddf39b109193995d977388db637'
    assert source == corpus['candidates'][cid] and P['references'][cid] == P['reference_bindings'][cid] == {}
    old = P['historical_compiled_rows'][cid]; loc = I['original_decisions'][cid]
    catalog = corpus['slot_catalog']; facts = []; units = []
    if ordinal == 3107:
        role, target, dimension, prop = 'mood', 'scene', 'atmosphere', 'mood.burnout_reset'
        value_type, value = 'mood.burnout_reset/v1', 'burnout-reset mood, tired but reorganizing'
        for name, pointer in [('en', '/content/en'), ('embedding', '/content/embedding_text')]:
            fid = 'root3107_' + name
            quote = source['content']['en'] if name == 'en' else source['content']['embedding_text']
            facts.append(fact(fid, pointer, quote, dimension, target, prop, 'effect', value_type, value, []))
            units.append({'realization_id': 'base', 'pointer': pointer, 'quote': quote, 'fact_refs': [fid], 'disposition': 'semantic'})
        units.append({'realization_id': 'base', 'pointer': '/content/ko', 'quote': source['content']['ko'],
                      'fact_refs': ['root3107_en'], 'disposition': 'semantic_reference',
                      'reference_relation': 'partial_restatement',
                      'retained_constraint_rationale': 'KO states a reset mood after burnout. It does not independently express every tired-but-reorganizing qualifier. Full exact EN and identical embedding remain ordinary canonical mood-effect evidence; no clinical diagnosis, private emotion, performed organizing action, optical effect or actor is inferred.'})
        role_refs = ['root3107_en', 'root3107_embedding']
        reason = 'Root freshly read both full source versions, exact5B, own binding, empty closure, complete proposal and mood/neighbor specs. Burnout-reset is proposed scene affect, an actual atmosphere effect supporting contextual mood. KO is an explicitly bounded partial restatement. Preserve all tired/reorganizing EN qualifiers as affect rather than actual clinical or performed activity. Existing scene role must resolve to an actual core owner; no new person or scene is created.'
    else:
        role, target, dimension, prop = 'grain_profile', 'image', 'style', 'image.noise'
        value_type, value = 'image.noise/v1', 'ISO 3200 high-sensitivity noise grain'
        app = source['content']['application_scope']
        facts.append(fact('root3169_imageP', '/content/application_scope', 'the existing image plane', 'subject', 'image',
                          'entity.presence', 'prerequisite', 'entity.presence/v1', 'present', []))
        role_refs = []
        for name, key in [('en', 'en'), ('ko', 'ko'), ('embedding', 'embedding_text'), ('application', 'application_scope')]:
            fid = 'root3169_' + name; pointer = '/content/' + key; quote = source['content'][key]
            facts.append(fact(fid, pointer, quote, dimension, target, prop, 'effect', value_type, value, ['root3169_imageP']))
            units.append({'realization_id': 'base', 'pointer': pointer, 'quote': quote,
                          'fact_refs': (['root3169_imageP', fid] if name == 'application' else [fid]), 'disposition': 'semantic'})
            role_refs.append(fid)
        reason = 'Root freshly read full original/current/5B/proposal/ownbinding/emptyclosure and grain/film/material specs. This selects ISO3200-referenced image noise appearance on the independently present existing image, not measured capture ISO, low-light scene, material particles, device or film stock. Exact same image.noise effect retains the original style dimension; noise is not a fake material or acquisition effect. Own product/jewelry/food exclusions remain conjunctive.'
    owner_map = {'schema': n.SELECTOR_OWNER_SCHEMA, 'bindings': [{'target': target, 'origin': 'existing', 'introduced_by': None,
                                                               'selector': {'kind': 'core_role', 'role': target}}]}
    proof = {'schema': n.SCHEMA, 'meaning_sha256': n.meaning_sha256(source), 'catalog_sha256': c.digest(catalog),
             'complete': True, 'facts': facts,
             'roles': {role: {'spec_sha256': c.digest(catalog[role]), 'scope': 'whole_record', 'realization_ids': ['base'],
                              'fact_refs': role_refs, 'support_modes': ['effect']}},
             'owner_maps': {'base': owner_map}, 'source_units': units,
             'effect_sets': {'base': n.effect_set(source, 'base')}, 'dependencies': {'base': []}, 'reference_sha256': {},
             'guard_sets': {'base': n.source_guard_set(source, 'base', corpus)}, 'profile_contracts': {'base': None},
             'review': {'basis': reason, 'whole_source_reviewed': True,
                        'source_correction': {'before_sha256': n.meaning_sha256(before), 'after_sha256': n.meaning_sha256(source),
                                              'rationale': 'Exact separately root-selected literal source correction; no further source edit. ' + reason},
                        'original_review': {'candidate_id': cid, 'source_record_sha256': old['source_record_sha256'],
                                            'catalog_sha256': old['catalog_sha256'], 'decision_sha256': loc['row_sha256'],
                                            'artifact': loc['file'] + '#item=' + str(loc['item'])},
                        'native_review': {'reviewer': '/root', 'method': 'codex_direct_source_read', 'native_contract_sha256': ''}}}
    proof['review']['native_review']['native_contract_sha256'] = n.native_contract_sha256(proof)
    record = copy.deepcopy(source); record['content']['role_evidence'] = proof; corpus['candidates'][cid] = record
    n.validate(record, catalog, corpus=corpus); compact = n.compact(record, corpus)
    delta = [{'pointer': '/' + key, 'before_exists': True, 'before': before[key], 'after_exists': True, 'after': source[key],
              'reason': reason} for key in before if before[key] != source[key]]
    row = {'candidate_id': cid, 'ordinal': ordinal, 'status': 'approved', 'rationale': reason, 'source_before': before,
           'source_after': source, 'delta': delta, 'original_compiled': loc, 'proof': proof,
           'dependency_records': {}, 'reference_bindings': {}, 'source_reread_complete': True, 'reference_reread_complete': True, 'revision': None}
    identity = {key: A[key] for key in ['task_name', 'model', 'reasoning_effort']}
    batch = {'schema': nr.BATCH, **identity, 'assignment_sha256': c.digest(A), 'input_sha256': c.digest(I),
             'prepared_count': 1, 'actual_read_count': 1, 'records': [row]}
    note = {'schema': nr.NOTE, **identity, 'assignment_sha256': c.digest(A), 'input_sha256': c.digest(I), 'batch_sha256': c.digest(batch),
            'prepared_count': 1, 'actual_read_count': 1, 'whole_source_read_ids': [cid], 'whole_dependency_read_ids': [cid]}
    O = R / f'native_batches/root-{ordinal:05d}-149-01'; O.mkdir(exist_ok=False)
    save(O / 'BATCH.json', batch); save(O / 'NOTE.json', note)
    verified = nr.verify_batch(D / 'ASSIGNMENT.json', O / 'BATCH.json', O / 'NOTE.json', root=ROOT, here=R)
    save(O / 'VERIFICATION.json', verified)
    save(O / 'COMPACT-CHECK.json', {'full_validation': True, 'compact': compact, 'proof_sha256': c.digest(proof),
                                   'root_source_decision': True, 'operating_changes': 0, 'consumer_tests_completed': False})
    print(json.dumps({'ordinal': ordinal, 'candidate_id': cid, 'facts': len(facts), 'source_units': len(units),
                      'full_compact_and_batch_shape_valid': True, 'operating_changes': 0}))
