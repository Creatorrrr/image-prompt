"""Literal five-case human-owner prerequisite revision; research only, no source application/signature."""
import copy,datetime,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def h(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
p=R/'authored/native_12250_approval_pilot149_source25_plan_04.json';old=json.loads(p.read_text());assert h(old)=='84660972fe703a525124e4f2932018ca43b8fd131f403dc3a7d9c5547b837090'
# Individually chosen literal source facts: each App explicitly selects an existing human actor at its original main_subject target.
PS={
9629:{'id':'owner_human','realization_id':'base','pointer':'/content/application_contract','quote':'existing human actor selected for the original source target main_subject','dimension':'subject','target':'main_subject','property':'entity.type','mode':'prerequisite','value':{'type':'entity.type/v1','value':'human'},'requires':[]},
9762:{'id':'owner_human','realization_id':'base','pointer':'/content/application_contract','quote':'existing human actor selected for the original source target main_subject','dimension':'subject','target':'main_subject','property':'entity.type','mode':'prerequisite','value':{'type':'entity.type/v1','value':'human'},'requires':[]},
9834:{'id':'owner_human','realization_id':'base','pointer':'/content/application_contract','quote':'existing human actor selected for the original source target main_subject','dimension':'subject','target':'main_subject','property':'entity.type','mode':'prerequisite','value':{'type':'entity.type/v1','value':'human'},'requires':[]},
9853:{'id':'owner_human','realization_id':'base','pointer':'/content/application_contract','quote':'existing human actor selected for the original source target main_subject','dimension':'subject','target':'main_subject','property':'entity.type','mode':'prerequisite','value':{'type':'entity.type/v1','value':'human'},'requires':[]},
9868:{'id':'owner_human','realization_id':'base','pointer':'/content/application_contract','quote':'existing human actor selected for the original source target main_subject','dimension':'subject','target':'main_subject','property':'entity.type','mode':'prerequisite','value':{'type':'entity.type/v1','value':'human'},'requires':[]}}
a=copy.deepcopy(old)
for r,prior in zip(a['records'],old['records']):
 o=r['ordinal'];pf=copy.deepcopy(PS[o]);app=r['after']['content']['application_contract'];assert pf['quote'] in app
 assert not any(f['id']==pf['id'] for f in r['facts']);r['facts'].insert(2,pf)
 e=next(f for f in r['facts'] if f['mode']=='effect');previous_e=next(f for f in prior['facts'] if f['mode']=='effect');assert pf['id'] not in e['requires'];e['requires'].append(pf['id']);eh=h(e)
 for u in r['source_units']:
  if u['pointer']=='/content/application_contract':u['fact_refs'].append(pf['id'])
 for u in r['positive_unit_entailment_plans']:
  u['aggregate_fact_sha256']=eh
  if u['pointer']=='/content/application_contract':
   u['fact_refs'].append(pf['id']);u['complete_E_witness']['fact_sha256']=eh
 for v in r['manual_same_fact_role_view_plans']:
  v['canonical_fact_sha256']=eh;v['canonical_assignment']['requires'].append(pf['id'])
  for b in v['whole_unit_local_positive_basis']:b['aggregate_fact_sha256']=eh
 # Historical anchor revision remains a statement specifically about04; do not misstate the05 requires addition as unchanged.
 r['original_E_anchor_revision']['comparison_scope']='Historical plan03-to-plan04 anchor correction, not a claim that plan05 requires is unchanged.'
 r['selected_owner_human_prerequisite_revision']={'prior04_fact_count':len(prior['facts']),'added_fact':pf,'E_fact_ref':e['id'],'prior04_E_sha256':h(previous_e),'updated_E_sha256':eh,'E_delta':{'requires':{'before':previous_e['requires'],'after':e['requires']}},'same_source_owner':'main_subject','same_actual_RID':'base','canonical_assignment_address_value_mode_operation_all_receivers_preserved':True,'source_application_text_added':False,'source_intrinsic_for_any_human_not_owner_type_witness':True,'reason':'The same independently selected actual existing owner must itself carry the exact frozen subject/entity.type/entity.type-v1 human scalar. A different human satisfying a global gate cannot supply this owner-specific prerequisite. The explicit App states existing human actor; no role-word-to-human inference or new owner is made.'}
 r['status']='root_source26_choice_and_freshINPUT_pending_with_actual_selected_human_P_research_only'
a.update(schema='photo-worker-five-expression-aggregate-anchor-role-view-plan/v5',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),prior04_path=str(p),prior04_sha256=h(old),prior04_preserved=True,added_selected_owner_human_prerequisites=5,prior04_existing_facts=32,total_facts=37,canonical_E_requires_additions=5,canonical_E_address_value_mode_operation_receivers_changes=0,source_body_after_changes_from04=0,whole_after_exact04_prior_read_reuse_count=5,additional_whole_source_or_spec_read_count=0,new_human_P_direct_App_fact_read_count=5,manual_same_fact_role_views=7,roleview_original_local_basis_samebytes_reuse_count=7,formal_native_proof_count=0,source_approval_count=0)
a['semantic_E_assignments_changed']=0
a['E_requirements_changed_from04']=5
a['control_fixture_design']=[{'name':'genuine_selected_human','selected_existing_owner':'H','independent_frozen_facts':[{'dimension':'subject','target':'H','property':'entity.type','value':{'type':'entity.type/v1','value':'human'}}],'other_obligations':'Independently provide each exact original anatomy P and original seam/open PR at H; retain all source/binding guards.','expected_owner_type_P':'allow','expected_fresh_native_admission_if_all_other_source_obligations_and_permissions_satisfied':'allow'}, {'name':'selected_object_plus_separate_human','selected_existing_owner':'O','independent_frozen_facts':[{'dimension':'subject','target':'O','property':'entity.type','value':{'type':'entity.type/v1','value':'object'}},{'dimension':'subject','target':'H','property':'entity.type','value':{'type':'entity.type/v1','value':'human'}}],'explicit_topology':'O and H are distinct disjoint owners. Global human gate can be satisfied by H. All anatomy P and original seam/open PR are independently present at O for isolation; do not infer them from object/human names.','expected_owner_type_P':'deny','expected_fresh_native_admission':'deny'}, {'name':'selected_object_missing_type_plus_separate_human','selected_existing_owner':'O','independent_frozen_facts':[{'dimension':'subject','target':'H','property':'entity.type','value':{'type':'entity.type/v1','value':'human'}}],'explicit_topology':'O and H are distinct disjoint owners; missing O/entity.type is not inferred from O owner_kind.','expected_owner_type_P':'deny','expected_fresh_native_admission':'deny'}, {'name':'selected_human_wrong_type_namespace','selected_existing_owner':'H','independent_frozen_facts':[{'dimension':'subject','target':'H','property':'entity.type','value':{'type':'category/v1','value':'human'}}],'expected_owner_type_P':'deny','expected_fresh_native_admission':'deny_exact_typed_scalar_required'}]
a['control_verification_boundary']='Primitive frozen-owner and exact-typed-scalar comparisons can run separately. Actual source26/freshINPUT whole native admission remains required; no source qualification or actual request is asserted by controlled independent fixtures.'
q=R/'authored/native_12250_approval_pilot149_source25_plan_05.json'
with q.open('x') as f:json.dump(a,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'path':str(q),'canonical':h(a),'raw':hashlib.sha256(q.read_bytes()).hexdigest(),'facts':37,'same_fact_views':7}))
for r in a['records']:
 print(json.dumps({'ordinal':r['ordinal'],'new_P':r['selected_owner_human_prerequisite_revision'],'E':next(f for f in r['facts'] if f['mode']=='effect'),'source_after_same04':r['after']==next(p for p in old['records'] if p['ordinal']==r['ordinal'])['after']},ensure_ascii=False))
