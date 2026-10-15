"""Exact revision integrity + frozen owner/typed-value primitive controls; NOT full native admission."""
import copy,datetime,hashlib,importlib.abc,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def h(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/provider import forbidden: '+fullname)
sys.meta_path.insert(0,DenyModels())
import photo_semantic_evidence as native
w=native.witnesses
pins={}
for m in [native,w,native.c,sys.modules['photo_precore_bridge']]:
 p=Path(m.__file__).resolve();assert p.is_relative_to(G);pins[m.__name__]={'path':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
assert pins['photo_semantic_evidence']['raw_sha256']=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
p=R/'authored/native_12250_approval_pilot149_source25_plan_05.json';a=json.loads(p.read_text());b=json.loads((R/'authored/native_12250_approval_pilot149_source25_plan_04.json').read_text());assert len(a['records'])==5
rows=[]
for r,old in zip(a['records'],b['records']):
 for key in ['ordinal','candidate_id','before','after','delta','own_bindings','owner_maps','actual_rids','reference_records','reference_bindings','role_proposals']:
  assert r[key]==old[key],key
 e=next(f for f in r['facts'] if f['mode']=='effect');oe=next(f for f in old['facts'] if f['mode']=='effect')
 assert {k:v for k,v in e.items() if k!='requires'}=={k:v for k,v in oe.items() if k!='requires'}
 assert e['requires']==oe['requires']+['owner_human'];assert len(r['facts'])==len(old['facts'])+1
 for f in r['facts']:
  native._fact_valid(f)
  if f['id']=='owner_human':
   assert f['target']==e['target']=='main_subject' and f['dimension']=='subject' and f['property']=='entity.type' and f['mode']=='prerequisite' and f['value']=={'type':'entity.type/v1','value':'human'} and f['requires']==[] and f['quote'] in r['after']['content']['application_contract']
  elif f['mode']!='effect':assert f==next(x for x in old['facts'] if x['id']==f['id'])
 for u,ou in zip(r['source_units'],old['source_units']):
  expected=copy.deepcopy(ou)
  if u['pointer']=='/content/application_contract':expected['fact_refs'].append('owner_human')
  assert u==expected
 for v,ov in zip(r['manual_same_fact_role_view_plans'],old['manual_same_fact_role_view_plans']):
  expected=copy.deepcopy(ov);expected['canonical_fact_sha256']=h(e);expected['canonical_assignment']['requires'].append('owner_human')
  for basis in expected['whole_unit_local_positive_basis']:basis['aggregate_fact_sha256']=h(e)
  assert v==expected
 for u,ou in zip(r['positive_unit_entailment_plans'],old['positive_unit_entailment_plans']):
  expected=copy.deepcopy(ou);expected['aggregate_fact_sha256']=h(e)
  if u['pointer']=='/content/application_contract':expected['fact_refs'].append('owner_human');expected['complete_E_witness']['fact_sha256']=h(e)
  assert u==expected
 rows.append({'ordinal':r['ordinal'],'after_sha256':h(r['after']),'same_whole_after04':True,'new_P_sha256':h(next(f for f in r['facts'] if f['id']=='owner_human')),'E_sha256':h(e),'requires_added_only':'owner_human','all_prior_nonE_facts_exact04':True})
# Independently authored artificial controls: no candidate source/CID enters frozen request authoring.
def frozen_control(name,rows):
 text={'genuine_selected_human':'Existing H is explicitly human. Select H. Existing O is a disjoint object.', 'selected_object_plus_separate_human':'Existing O is explicitly an object. Select O. Existing H is explicitly a separate disjoint human.', 'selected_object_missing_type_plus_separate_human':'Existing O is selected without a type fact. Existing H is explicitly a separate disjoint human.', 'selected_human_wrong_type_namespace':'Existing H has the exact category/v1 human fact only. Select H. Existing O is a disjoint object.'}[name]
 def native_row(i,axes):return {'assertion_id':i,'dimension':'subject','affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1',**axes},'polarity':'required','source_span_ids':['scope'],'evidence':{'meaning':text}}
 assertions=[native_row('H',{'kind':'owner','owner':'H','owner_kind':'entity'}),native_row('O',{'kind':'owner','owner':'O','owner_kind':'entity'}),native_row('distinct',{'kind':'disjoint','left':'H','right':'O'})]
 assertions += [native_row('type'+str(i),{'kind':'fact','owner':f['target'],'property':f['property'],'value_type':f['value']['type'],'value':f['value']['value']}) for i,f in enumerate(rows)]
 f=w.read(assertions,[{'source_span_id':'scope','text':text}],text)
 return {'source_text':text,'assertions':assertions,'frozen':f}
controls=[]
for design in a['control_fixture_design']:
 f=frozen_control(design['name'],design['independent_frozen_facts']);graph=f['frozen']['graph'];owner=design['selected_existing_owner'];bycase=[]
 for r in a['records']:
  pf=next(x for x in r['facts'] if x['id']=='owner_human')
  # These are exactly the dimension/property/overlap/same-entity and typed equality comparisons in frozen native admission, lines873-881. This harness does not call admission or issue a proof.
  matches=[row for row in f['frozen']['facts'] if row['dimension']==pf['dimension'] and row['property']==pf['property'] and w.owner_relation(graph,row['target'],owner)=='overlap' and native._same_entity(graph,row['target'],owner)]
  allowed=len(matches)==1 and w.value_key(matches[0]['value'])==w.value_key(pf['value'])
  assert allowed==(design['expected_owner_type_P']=='allow')
  bycase.append({'ordinal':r['ordinal'],'selected_actual_owner':owner,'exact_same_owner_matches':matches,'owner_type_P_satisfied':allowed})
 controls.append({'name':design['name'],'fixture':f,'results':bycase,'expected':design['expected_owner_type_P'],'PASS':True})
assert sum(len(r['facts']) for r in a['records'])==37
out={'schema':'photo-worker-five-pilot-plan05-human-owner-P-revision-note/v1','task_name':'/root/review_12250_13000','model':'gpt-6.1-sol','reasoning_effort':'high','stop':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_file':str(p),'canonical_sha256':h(a),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'facts':37,'original_E':5,'added_human_P':5,'same_fact_role_views':7,'source_after_same04':5,'additional_whole_source_or_spec_reread_count':0,'new_P_and_E_requires_delta_directly_reread_count':5,'roleview_local_basis_reused_actual_prior_read':7,'whole_source_units_reused_actual_prior_read':58,'prototype_pinned_modules':pins,'mechanical_exact_delta_checks':'PASS','frozen_owner_typed_value_primitive_controls':controls,'primitive_control_candidate_checks':20,'full_native_admission_executed':False,'formal_native_qualification_or_source_approval_count':0,'required_freshINPUT_controls':['All original anatomy P and original seam/open PR on selected owner remain required. Genuine selected human with these facts and other conditions/permissions passes whole admission.','Select object O with explicit object type and all otherwise matching anatomy/state witnesses; separately present disjoint H is human and satisfies global for_any human. Whole admission must deny on O entity.type.','O without its type plus separate human must deny; wrong type namespace with human scalar must deny.'],'boundary':'Frozen actual owner and typed-value primitive comparisons executed, not a complete source/native admission. Current source26 freshINPUT must perform the whole native gates, source/binding guards and permission checks. Synthetic independent request controls do not approve or reinterpret any actual source.','source_text_effect_address_value_mode_operation_Rx_owner_condition_binding_changes':0,'E_requires_additions':5,'runtime_engine_predicate_development':0,'production_source_catalog_status_proof_git_changes':0,'provider_network_model_calls':0}
q=R/'worker-notes/native-12250-approval-pilot149-source25-plan05-20261015.json'
with q.open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'plan_canonical':h(a),'plan_raw':out['raw_sha256'],'note':str(q),'note_canonical':h(out),'facts':37,'views':7,'controls':20,'results':[{k:c[k] for k in ['name','expected','PASS']} for c in controls],'rows':rows,'modules':pins},ensure_ascii=False))
