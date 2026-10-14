"""Fresh direct noise review retaining the original canonical effect and locks."""
import copy
import gzip
import hashlib
import importlib.abc
import json
import sys
from pathlib import Path

ROOT = Path.cwd(); R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch', 'transformers', 'sentence_transformers', 'tensorflow', 'jax', 'mlx', 'google', 'openai', 'anthropic', 'litellm', 'ollama'}:
            raise AssertionError('model/API import forbidden: ' + fullname)
sys.meta_path.insert(0, Deny()); sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_semantic_role_views as views
sys.path.insert(0, str(R)); import native_reviews as nr
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
assert Path(nr.native.__file__).resolve().is_relative_to(G)
def read(path): return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())
def save(path, value):
    with path.open('x') as stream: json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2); stream.write('\n')

D = R / 'native-inputs/prepared/root-03169-149-03'
I, A, P = [read(D / name) for name in ['INPUT.json', 'ASSIGNMENT.json', 'PREPARED-PACKET.json']]
cid = A['ids'][0]; before = P['original_records'][cid]; source = P['current_records'][cid]
corpus = read(ROOT / I['current_snapshot']['file']); catalog = corpus['slot_catalog']
assert c.digest(corpus) == 'b1af3261d4af57d1635f2522ca656b6277dafaa13d238b1cc39a78e1da0f25d5'
assert source['effects'] == before['effects'] == {'dimensions': ['style'], 'properties': [{'dimension': 'style', 'property': 'rendering.noise', 'target': 'image_plane'}]}
assert source['content']['en'] == source['content']['embedding_text'] == 'ISO 3200 high-sensitivity noise grain'
assert source['content']['ko'] == 'ISO 3200 고감도 노이즈 입자'
facts = [{'id': 'root3169r3_imageP', 'realization_id': 'base', 'pointer': '/content/application_contract', 'quote': 'the existing image plane',
          'dimension': 'subject', 'target': 'image_plane', 'property': 'entity.presence', 'mode': 'prerequisite',
          'value': {'type': 'entity.presence/v1', 'value': 'present'}, 'requires': []}]
units = []; role_refs = []; facets = {}
for name, key, facet in [('en', 'en', 'noise grain'), ('ko', 'ko', '노이즈 입자'),
                         ('embedding', 'embedding_text', 'noise grain'), ('application', 'application_contract', 'noise-grain image treatment')]:
    fid = 'root3169r3_' + name; pointer = '/content/' + key; quote = source['content'][key]
    facts.append({'id': fid, 'realization_id': 'base', 'pointer': pointer, 'quote': quote,
                  'dimension': 'style', 'target': 'image_plane', 'property': 'rendering.noise', 'mode': 'effect',
                  'value': {'type': 'rendering.noise/v1', 'value': 'ISO 3200 high-sensitivity noise grain'},
                  'requires': ['root3169r3_imageP'], 'operation': 'set_value', 'receivers': []})
    units.append({'realization_id': 'base', 'pointer': pointer, 'quote': quote, 'disposition': 'semantic',
                  'fact_refs': (['root3169r3_imageP', fid] if name == 'application' else [fid])})
    role_refs.append(fid); facets[fid] = facet
reason = ('Fresh root direct re-review after the independently observed original rendering.noise lock bypass in unaccepted01. The exact application text is now in the recognized full positive application_contract field; no source statement or canonical effect is changed by that field repair. '
          'Retain the original style/rendering.noise/image_plane effect exactly and explicitly map source image_plane to the existing actual image. '
          'The independently present image is prerequisite. All four source fields directly select the same ISO3200-referenced image noise appearance; '
          'no measured capture ISO, low-light scene, physical grain, camera/sensor or film stock is inferred. '
          'The grain_profile manual view states only that exact positive noise facet, preserving whole typed E/value/operation/owner/Rx/P closure. '
          'No image.noise alias or shadow effect is added to fit a role prefix; retain actual own product/jewelry/food exclusions.')
old = P['historical_compiled_rows'][cid]; loc = I['original_decisions'][cid]
proof = {'schema': n.SCHEMA, 'meaning_sha256': n.meaning_sha256(source), 'catalog_sha256': c.digest(catalog), 'complete': True,
         'facts': facts, 'roles': {'grain_profile': {'spec_sha256': c.digest(catalog['grain_profile']), 'scope': 'whole_record',
                       'realization_ids': ['base'], 'fact_refs': role_refs, 'support_modes': ['effect']}},
         'owner_maps': {'base': {'schema': n.SELECTOR_OWNER_SCHEMA, 'bindings': [{'target': 'image_plane', 'origin': 'existing',
                       'introduced_by': None, 'selector': {'kind': 'core_role', 'role': 'image'}}]}},
         'source_units': units, 'effect_sets': {'base': n.effect_set(source, 'base')}, 'dependencies': {'base': []},
         'reference_sha256': {}, 'guard_sets': {'base': n.source_guard_set(source, 'base', corpus)}, 'profile_contracts': {'base': None},
         'review': {'basis': reason, 'whole_source_reviewed': True,
                    'source_correction': {'before_sha256': n.meaning_sha256(before), 'after_sha256': n.meaning_sha256(source), 'rationale': reason},
                    'original_review': {'candidate_id': cid, 'source_record_sha256': old['source_record_sha256'], 'catalog_sha256': old['catalog_sha256'],
                                        'decision_sha256': loc['row_sha256'], 'artifact': loc['file'] + '#item=' + str(loc['item'])},
                    'native_review': {'reviewer': '/root', 'method': 'codex_direct_source_read', 'native_contract_sha256': ''}}}
anchors = []
for fact in facts[1:]:
    unit = next(unit for unit in units if unit['pointer'] == fact['pointer']); text = n.positive_string(source, fact['pointer'], realization_id='base')
    facet = facets[fact['id']]; start = text.index(facet)
    anchors.append({'fact_id': fact['id'], 'pointer': fact['pointer'], 'source_unit_sha256': c.digest(unit), 'full_field_sha256': c.digest(text),
                    'facet_quote': facet, 'start': start, 'stop': start + len(facet)})
proof['manual_role_views'] = [{'schema': views.SCHEMA, 'id': 'root3169r3_actual_noise_grain', 'candidate_id': cid, 'realization_id': 'base',
    'role_id': 'grain_profile', 'spec_sha256': c.digest(catalog['grain_profile']),
    'canonical_fact_refs': [{'fact_id': fact['id'], 'fact_sha256': c.digest(fact), 'mode': 'effect'} for fact in facts[1:]],
    'normal_anchors': anchors, 'endpoint_refs': [{'fact_id': fact['id'], 'position': 'target'} for fact in facts[1:]],
    'requires_refs': ['root3169r3_imageP'], 'whole_closure_sha256': c.digest({key: proof[key] for key in views.CLOSURE_FIELDS}),
    'manual_semantic_facet': 'Each exact source field positively declares image-plane noise grain, including its ISO3200 appearance reference. This is the grain/noise distribution facet on that same existing image.',
    'whole_value_retained': 'Retain original canonical style/rendering.noise effect, image_plane target mapped to actual image, exact ISO3200 reference value, set_value operation, empty actual receiver list and independent image presence prerequisite. No new property, E, owner or permission.',
    'manual_boundary_rationale': 'Image noise is not physical material grain, airborne dust, actual acquisition ISO or a full film emulation recipe. The old exact rendering.noise lock must remain effective on the actual image, alias and ancestor; prefix fit cannot justify a rename.'}]
proof['roles']['grain_profile']['view_refs'] = ['root3169r3_actual_noise_grain']
proof['review']['native_review']['native_contract_sha256'] = n.native_contract_sha256(proof)
record = copy.deepcopy(source); record['content']['role_evidence'] = proof; corpus['candidates'][cid] = record
n.validate(record, catalog, corpus=corpus); compact = n.compact(record, corpus)
required = I['required_revisions'][cid]
row = {'candidate_id': cid, 'ordinal': 3169, 'status': 'approved', 'rationale': reason, 'source_before': before, 'source_after': source,
       'delta': [{'pointer': '/content', 'before_exists': True, 'before': before['content'], 'after_exists': True, 'after': source['content'], 'reason': reason}],
       'original_compiled': loc, 'proof': proof, 'dependency_records': {}, 'reference_bindings': {}, 'source_reread_complete': True,
       'reference_reread_complete': True, 'revision': {'prior_review': required['prior_review'], 'memo_artifacts': required['memo_artifacts'], 'rationale': reason}}
identity = {key: A[key] for key in ['task_name', 'model', 'reasoning_effort']}
batch = {'schema': nr.BATCH, **identity, 'assignment_sha256': c.digest(A), 'input_sha256': c.digest(I), 'prepared_count': 1, 'actual_read_count': 1, 'records': [row]}
note = {'schema': nr.NOTE, **identity, 'assignment_sha256': c.digest(A), 'input_sha256': c.digest(I), 'batch_sha256': c.digest(batch),
        'prepared_count': 1, 'actual_read_count': 1, 'whole_source_read_ids': [cid], 'whole_dependency_read_ids': [cid]}
O = R / 'native_batches/root-03169-149-03'; O.mkdir(exist_ok=False)
save(O / 'BATCH.json', batch); save(O / 'NOTE.json', note)
save(O / 'VERIFICATION.json', nr.verify_batch(D / 'ASSIGNMENT.json', O / 'BATCH.json', O / 'NOTE.json', root=ROOT, here=R))
save(O / 'COMPACT-CHECK.json', {'full_validation': True, 'compact': compact, 'proof_sha256': c.digest(proof), 'same_canonical_role_view_count': 1,
                               'original_effect_set_preserved': source['effects'] == before['effects'], 'operating_changes': 0, 'consumer_tests_completed': False})
print(json.dumps({'facts': 5, 'units': 4, 'manual_views': 1, 'original_effect_set_preserved': True, 'full_compact_batch_verified': True, 'operating_changes': 0}))
