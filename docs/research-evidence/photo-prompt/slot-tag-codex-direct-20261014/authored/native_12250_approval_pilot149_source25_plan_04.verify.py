"""Mechanical equality/quote integrity checks only; not native validation, approval or signature."""
import json,hashlib,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def h(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def at(x,p):
 for k in p[1:].split('/'):x=x[int(k)] if isinstance(x,list) else x[k]
 return x
p=R/'authored/native_12250_approval_pilot149_source25_plan_04.json';a=json.loads(p.read_text());b=json.loads((R/'authored/native_12250_approval_pilot149_source23_plan_03.json').read_text());rows=[]
for x,y in zip(a['records'],b['records']):
 assert x['ordinal']==y['ordinal'] and x['before']==y['before'];assert x['after']['effects']==y['after']['effects'] and x['after']['conditions']==y['after']['conditions'];assert x['own_bindings']==y['own_bindings'] and x['actual_rids']==y['actual_rids'] and x['owner_maps']==y['owner_maps'];assert x['reference_records']==y['reference_records'] and x['reference_bindings']==y['reference_bindings']
 app=x['after']['content']['application_contract'];yp=y['after']['content']['application_contract']
 if x['ordinal']==9834:
  assert app==yp.replace('an existing face, mouth corners, cheeks and eyes with independently frozen partly open apertures','an existing face, mouth with its mouth corners, cheeks and eyes with independently frozen partly open apertures');assert {k:v for k,v in x['after']['content'].items() if k!='application_contract'}=={k:v for k,v in y['after']['content'].items() if k!='application_contract'}
 else:assert x['after']==y['after']
 assert len(x['facts'])==len(y['facts'])
 for f,g in zip(x['facts'],y['facts']):
  assert {k:v for k,v in f.items() if k not in ['pointer','quote']}=={k:v for k,v in g.items() if k not in ['pointer','quote']}
  assert f['quote'] in at(x['after'],f['pointer'])
  if f['mode']=='effect':assert f['pointer']=='/content/application_contract' and f['quote']==app and f['dimension']=='expression' and f['target']=='main_subject' and f['property']=='face.expression' and f['operation']=='set_value' and f['receivers']==[]
  elif x['ordinal']!=9834:assert f==g
 e=next(f for f in x['facts'] if f['mode']=='effect');assert sum(f['mode']=='effect' for f in x['facts'])==1
 for v in x['manual_same_fact_role_view_plans']:
  assert v['canonical_fact_sha256']==h(e) and v['canonical_complete_witness']['quote']==app
  assert v['canonical_assignment']=={k:e[k] for k in ['dimension','target','property','mode','value','requires','operation','receivers']}
  for q in v['whole_unit_local_positive_basis']:
   whole=at(x['after'],q['pointer']);assert whole==q['whole_positive_unit_quote'];assert whole[q['positive_local_start']:q['positive_local_end']]==q['positive_local_quote'];assert q['aggregate_fact_sha256']==h(e);assert not q['standalone_full_assignment_entailment']
 for u in x['positive_unit_entailment_plans']:
  assert u['whole_positive_unit_quote']==at(x['after'],u['pointer']) and u['aggregate_fact_sha256']==h(e)
  assert u['independently_entails_complete_aggregate_E']==(u['pointer']=='/content/application_contract')
 assert {u['pointer'] for u in x['source_units']}=={u['pointer'] for u in x['positive_unit_entailment_plans']}
 assert set(x['role_proposals'])==({'expression','facial_geometry','eye_detail'} if x['ordinal'] in [9834,9853] else {'expression','facial_geometry'})
 rows.append(dict(ordinal=x['ordinal'],after_sha256=h(x['after']),after_equals03=x['after']==y['after'],aggregate_E_fact_sha256=h(e),original_E_semantic_fields_exact03=True,all_P_PR_semantic_fields_exact03=True,whole_positive_units=len(x['source_units']),partial_restatement_unit_count=len(x['source_units'])-1,same_fact_views=[v['slot_id'] for v in x['manual_same_fact_role_view_plans']]))
out=dict(schema='photo-worker-five-pilot-plan04-integrity-reread-note/v1',task_name='/root/review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',stop=datetime.datetime.now(datetime.timezone.utc).isoformat(),plan_file=str(p),canonical_sha256=h(a),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source25_sha256=a['source25_sha256'],source25_raw_sha256=a['source25_raw_sha256'],catalog_sha256=a['catalog_sha256'],facts_count=sum(len(x['facts']) for x in a['records']),same_fact_role_view_count=7,canonical_E_count=5,canonical_E_added_renamed_deleted=0,semantic_E_assignment_changes=0,actual_owner_dimension_receiver_condition_binding_changes=0,complete_selected_App_direct_E_anchor_count=5,whole_source_units_direct_semantic_recheck_count=sum(len(x['source_units']) for x in a['records']),partial_positive_units=sum(len(x['source_units'])-1 for x in a['records']),whole_after_direct_reread_complete_count=1,whole_after_exact03_prior_read_reuse_count=4,new_original_source_whole_read_count=0,source25_selected_current_before_samebyte_reuse_count=5,global_changed_source_whole_reread_count=0,actual_new_semantic_reads=['9834completeafter with exact mouth-with-its-mouth-corners phrase','All5 fullApp E anchor assignments; sevenroleviews including completepositiveunit andexactlocalquote, canonicalassignmenthash andRID','All5 fullpositive-unit partial-facet annotations in bounded nontruncated lossless outputs','Full149 expression/eye_detail/facial_geometry/skin_finish/lip_finish/body_form specs'],immutable03_untouched=True,rows=rows,source_unit_boundary='Every EN/KO/embedding/concept/paraphrase/actual relation unit remains exact and separately reviewed. Its supported facets are literal partial restatements or owner scope; it is not represented as independently entailing the entire stronger aggregate assignment. Complete App directly quotes and binds that aggregate. View subquotes remain inside their full positive source units and bind that same actual canonical E.',facial_geometry_boundary='All five owned local contour geometries support manual facial_geometry views of the same expression E; no permanent-only limitation. 9834/9853 actual eye/lid E facets also support eye_detail views while original open PR is preserved.',no_new_slot_or_engine_work=True,formal_native_validation_proof_signature_source_approval=0,source_catalog_binding_runtime_git_changes=0,network_provider_model_calls=0)
q=R/'worker-notes/native-12250-approval-pilot149-source25-plan04-20261015.json'
with q.open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(plan=h(a),raw=out['raw_sha256'],facts=out['facts_count'],views=7,units=out['whole_source_units_direct_semantic_recheck_count'],partial_units=out['partial_positive_units'],note=str(q),rows=rows)))
