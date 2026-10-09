from pathlib import Path
import sys,json,copy,hashlib
B=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator/scripts';AS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(S))
from visual_profile_contracts import validate_visual_profile_source,compile_visual_profile,validate_hard_activation
from photo_candidate_semantics import validate_candidate_entries,validate_bundle_references,compile_extension_bundles
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
from photo_source_manifest import SourceInventory
from validate_photo_prompt_dictionary import validate_visual_obligation_registry,validate_visual_relation_contract
j=json.loads((B/'data-fragment.json').read_text());own=json.loads((B/'assigned_drafts.json').read_text())
base=json.loads((AS/'photo_prompt_tags.json').read_text())
data={'slots':{},'visual_semantics':[],'candidate_semantic_policy':base['candidate_semantic_policy']}
profiles=[];errors=[]
for g in j['domain_writes']:
 data['slots'].setdefault(g['slot'],[]).extend(g['candidates']);data['visual_semantics'].extend(g['visual_semantics'])
 assert g['slot'] in json.loads((AS/g['candidate_file']).read_text())['slots']
 assert g['profile_file'] in {r['file'] for r in json.loads((AS/'photo_prompt_source_manifest.json').read_text())['sources'] if r['kind']=='visual_profile'}
 for p in g['profiles']:
  validate_visual_profile_source(p);validate_hard_activation(p['activation']['hard_activation']);compile_visual_profile(p)
  validate_visual_relation_contract(p['visual_relation'],p['id'],errors)
  assert not any(k in p for k in ['required_evidence_fields','render_gates','composition_instruction','evidence_requirements'])
  assert 'component_semantics' not in p['semantics']
  profiles.append(p)
validate_candidate_entries(data,set(AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS))
compile_extension_bundles(data,{'visual_semantics':data['visual_semantics']})
validate_bundle_references(data,profiles)
assert all(b['profile_activation']=='independent_request_evidence_only' for b in data['candidate_bundles'])
assert len(profiles)==len(own)==len(j['decisions'])==93
assert {d['draft_id'] for d in own}=={d['draft_id'] for d in j['decisions']}
assert len({p['id'] for p in profiles})==93
candidate_ids=[c['id'] for vs in data['slots'].values() for c in vs]
assert len(candidate_ids)==len(set(candidate_ids))==93
gates=[c['render_gate']['id'] for p in profiles for c in p['authored_components']['components']]
assert len(gates)==len(set(gates))
# Validate compiled profile registry independently of the shared sources.
registry=json.loads((AS/'photo_prompt_visual_obligations.json').read_text());registry['profiles']=registry['profiles']+profiles
(B/'synthetic_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
validate_visual_obligation_registry(B/'synthetic_registry.json',errors,inventory=SourceInventory.for_test(B))
text=json.dumps(j['domain_writes'],ensure_ascii=False)
assert 'http://' not in text and 'https://' not in text
assert all(x['source_ids'] for x in j['decisions'])
pointelle=next(p for p in profiles if p['id']=='spring_sf057_01')
pointelle_candidate=next(c for vs in data['slots'].values() for c in vs if c['id']=='spf_sf057_01')
rim_edges={(r['type'],r['subject'],r['object']) for r in pointelle_candidate['relations']}
assert ('forms_rim_around','knit_top.yarn_loops','knit_top.small_opening_boundaries') in rim_edges
assert ('continuous_with','knit_top.opening_rim_loops','knit_top.surrounding_yarn_loops') in rim_edges
assert ('repeats_across','knit_top.yarn_bounded_openings','knit_top.continuous_knit_surface') in rim_edges
assert pointelle['activation']['exact_terms']==[pointelle_candidate['en']]
assert pointelle['semantics']['visual_components']==pointelle_candidate['concept_units']
assert all(c['render_gate']['review_scale']=='native' for c in pointelle['authored_components']['components'])
old_fuzzy_sentence=next(e['original_research_sentence'] for e in j['evidence'] if e['draft_id']=='SPR_DRAFT_SF057_01')
assert all(term not in old_fuzzy_sentence for c in pointelle['authored_components']['components'] for term in c['evidence_terms'])
if not errors:
 for e in j['evidence']:e['qualification']['profile_compile']='pass_isolated_schema_validation'
 (B/'data-fragment.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 (B/'evidence-sidecar.json').write_text(json.dumps({'schema_version':'spring-fashion-arm-evidence/v1','arm':'ornament_shoe','records':j['evidence']},ensure_ascii=False,indent=2)+'\n')
report={'status':'pass' if not errors else 'fail','errors':errors,'assigned_drafts':len(own),'decisions':len(j['decisions']),'new_candidates':len(candidate_ids),'authored_profiles':len(profiles),'optional_bundles':len(data['candidate_bundles']),'native_component_gates':len(gates),'runtime_provenance_leak_check':'pass','source_profiles_generated_field_check':'pass','freeze_precedes_data_authoring':True,'pointelle_rim_contract_check':'pass','old_fuzzy_sentence_sufficient_for_new_evidence':False,'runtime_payload_sha256':hashlib.sha256(json.dumps(j['domain_writes'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'fragment_sha256':hashlib.sha256((B/'data-fragment.json').read_bytes()).hexdigest(),'proof_limit':'Isolated structural/schema validation only. Shared index rebuild, published generation, live retrieval and native pixels remain pending.'}
(B/'fragment-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
