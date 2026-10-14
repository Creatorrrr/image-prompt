from fixture_v1 import *
J=json.loads((O/'BATCH.json').read_text());row=J['records'][0];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;n.validate(rec,S['slot_catalog'],corpus=S);cp=n.compact(rec,S)
TEXT='Independent synthetic baseline declares actual existing object O, actual chair C, and existing selected participant endpoints P and Q. Each independently has neutral entity presence. C has exact chair type. O/C and P/Q are explicitly disjoint. No object/chair placement, propped state, contact, counterpart role or chair association is already frozen; all are selected effects with composition/role/relationship open. These independent declarations are synthetic, not real requester or runtime evidence.'
core=make_core(TEXT,['O','C','P','Q'],[],[('subject','O','entity.presence','entity.presence/v1','present'),('subject','C','entity.presence','entity.presence/v1','present'),('subject','P','entity.presence','entity.presence/v1','present'),('subject','Q','entity.presence','entity.presence/v1','present'),('subject','C','props.type','props.type/v1','chair')],[('disjoint','O','C'),('disjoint','P','Q')],['composition','role','relationship']);B=[('propped_object','O'),('chair','C'),('counterpart','P'),('other_participant','Q')]
def dropedge(k,left,right):
 z=copy.deepcopy(k);z['semantic_assertions']=[a for a in z['semantic_assertions']if not(a['axes']['kind']=='disjoint'and a['axes']['left']==left and a['axes']['right']==right)];return z
cases=[('exact_existing_endpoints_no_selected_state_P',core,True,True),('missing_actual_selection',core,False,False),('missing_exact_chair',remove(core,'fact','props.type'),False,True),('wrong_existing_chair_type',change(core,'props.type','table'),False,True),('missing_object_chair_distinctness',dropedge(core,'O','C'),False,True),('missing_participant_distinctness',dropedge(core,'P','Q'),False,True),('missing_actual_object_presence',remove(core,'fact','entity.presence','O'),False,True),('missing_actual_chair_presence',remove(core,'fact','entity.presence','C'),False,True),('missing_counterpart_presence',remove(core,'fact','entity.presence','P'),False,True),('missing_other_participant_presence',remove(core,'fact','entity.presence','Q'),False,True)]
ad=[];consumer=[]
for label,k,want,choose in cases:
 for view in ['full','compact']:
  e=entry(J,1285,binding=True)
  if choose:e,k=selected(J,e,k,B)
  e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(e,k);assert got['allowed']==want,(label,view,got);ad.append({'case':label,'view':view,'expected':want,'result':got})
 e=entry(J,1285,binding=True)
 if choose:e,k=selected(J,e,k,B)
 got=generator.core_entry_eligible(S,k,contract('human'),picked('human'),'prop_placement',e);assert got==want,(label,'consumer',got);consumer.append({'case':label,'allowed':got,'expected':want})
locks=[]
for dim,target,prop in [('composition','O','props.placement.against_selected_chair'),('composition','C','props.placement.against_selected_chair'),('role','O','prop.state.propped'),('role','C','prop.state.propped'),('relationship','O','contact.leaning_support'),('relationship','C','contact.leaning_support'),('relationship','P','relationship.role.counterpart'),('relationship','Q','relationship.role.counterpart'),('relationship','C','relationship.chair_association'),('relationship','P','relationship.chair_association')]:
 e,k=selected(J,entry(J,1285,binding=True),core,B);ds,ps,_=n.permission_scope(e,k);assert n.property_scope_allowed(k,ds,ps,record=e);closed=copy.deepcopy(core);closed['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el,kl=selected(J,entry(J,1285,binding=True),closed,B);dl,pl,_=n.permission_scope(el,kl);assert not n.property_scope_allowed(kl,dl,pl,record=el);assert not generator.core_entry_eligible(S,kl,contract('human'),picked('human'),'prop_placement',el);locks.append({'dimension':dim,'actual_owner':target,'property':prop,'expanded_open_allowed':True,'target_or_receiver_anchor_denied':True})
whole=[]
for dim in ['composition','role','relationship']:
 closed=copy.deepcopy(core);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);e,k=selected(J,entry(J,1285,binding=True),closed,B);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),'prop_placement',e);whole.append({'dimension':dim,'denied':True})
e,k=selected(J,entry(J,1285,binding=True),core,B);assert not generator.core_entry_eligible(S,k,contract('human',['product']),picked('human'),'prop_placement',e);assert not generator.core_entry_eligible(S,k,contract('object'),picked('object'),'prop_placement',e)
invalid=[]
for defect in ['self_anchor','canonical_not_direct','short_quote','foreign_RID','missing_reference_rationale','nonsemantic_conflict','unknown_reference_relation']:
 z=copy.deepcopy(rec);pp=z['content']['role_evidence'];u=pp['source_units'][3]
 if defect=='self_anchor':u['fact_refs']=['placeEN']
 elif defect=='canonical_not_direct':pp['source_units'][2]['fact_refs'].remove('counterpartApp')
 elif defect=='short_quote':u['quote']='partner chair'
 elif defect=='foreign_RID':u['realization_id']='other'
 elif defect=='missing_reference_rationale':u['retained_constraint_rationale']=''
 elif defect=='nonsemantic_conflict':pp['source_units'][0]['disposition']='nonsemantic';pp['source_units'][0]['fact_refs']=[]
 elif defect=='unknown_reference_relation':u['reference_relation']='automatic_meaning_inheritance'
 pp['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(pp)
 try:n.validate(z,S['slot_catalog'],corpus={**S,'candidates':{**S['candidates'],row['candidate_id']:z}})
 except (ValueError,TypeError,KeyError)as exc:invalid.append({'case':defect,'rejected':True,'error':str(exc)})
 else:raise AssertionError('Invalid reference accepted: '+defect)
q=n.qualification(S['slot_catalog']['participant_role'],rec);assert q['status']=='eligible'and q['fact_refs']==['counterpartApp']
oldp=json.loads((R/'native_batches/review11870-01285-05/BATCH.json').read_text())['records'][0]['proof'];assert oldp['effect_sets']==row['proof']['effect_sets'];assert oldp['owner_maps']==row['proof']['owner_maps'];assert oldp['guard_sets']==row['proof']['guard_sets'];assert all(f['mode']=='prerequisite'and f['requires']==[]for f in row['proof']['facts']if f['id']in ['objectP','chairP','counterpartP','otherP'])
out={'schema':'photo-native-single-source-isolated-verification/v1','input_sha256':c.digest(I),'batch_sha256':c.digest(J),'full_source_validated':True,'compact':cp,'independent_synthetic_core':core,'explicit_actual_owner_bindings':B,'full_compact_admission':ad,'admission_count':len(ad),'actual_old_binding_consumers':consumer,'consumer_count':len(consumer),'actual_target_receiver_locks':locks,'whole_effect_dimension_locks':whole,'actual_old_binding_product_and_nonhuman_denied':True,'invalid_semantic_reference_cases':invalid,'source_qualification_participant_role':q,'all_five_E_owner_and_guard_sets_exact_equal_05':True,'all_passed':True,'module_paths_sha256':modules(),'frozen_generation':str(G),'root_accepted':False,'operational_native_qualified_count':0,'actual_runtime_request_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True};p=O/'CHECKS-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),len(ad),len(consumer),len(locks))
