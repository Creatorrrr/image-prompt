"""Fresh149actual1264 proof under final50fd92, literal independently reviewed historical fixture cases."""
from fixture_01264_v1 import *
import gzip
D=R/'native-inputs/prepared/review11870-01250-01300-05';I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());J=json.loads((O/'CHECKPOINT-01260-01265-v1.json').read_text());row=next(x for x in J['records']if x['ordinal']==1264);cid=row['candidate_id'];S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after'];p=row['proof'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=p;S['candidates'][cid]=rec;n.validate(rec,CAT,corpus=S);cp=n.compact(rec,S)
base=core()
def add_relation(k,kind,left,right):
 v=copy.deepcopy(k);v['semantic_assertions'].append({'assertion_id':'extra_'+kind+'_'+left+'_'+right,'dimension':'subject','polarity':'required','source_span_ids':['independent_request'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,'left':left,'right':right},'evidence':{'meaning':TEXT}});return v
def add_owner(k,owner):
 v=copy.deepcopy(k)
 for a_id,kind,axes in [('extraowner_'+owner,'owner',{'owner':owner,'owner_kind':'object'}),('extrapresence_'+owner,'fact',{'owner':owner,'property':'entity.presence','value_type':'entity.presence/v1','value':'present'})]:
  v['semantic_assertions'].append({'assertion_id':a_id,'dimension':'subject','polarity':'required','source_span_ids':['independent_request'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}})
 return v
alias=add_relation(delete(add_owner(base,'C_alias'),'extrapresence_C_alias'),'equivalent','C','C_alias')
cases=[('exact_existing_samechair_actualseat',base,True,True,None),('missing_actual_selection',base,False,False,None),('missing_exact_chair_type',delete(base,'chair_type'),False,True,None),('wrong_chair_type',alter(base,'chair_type',value='table'),False,True,None),('missing_exact_seat_part_kind',delete(base,'seat_type'),False,True,None),('wrong_part_kind',alter(base,'seat_type',value='backrest'),False,True,None),('missing_chair_presence',delete(base,'chair_presence'),False,True,None),('missing_seat_presence',delete(base,'seat_presence'),False,True,None),('missing_actual_part_of',delete(base,'actual_seat_of_same_chair'),False,True,None),('reverse_part_of',alter(base,'actual_seat_of_same_chair',left='C',right='S'),False,True,None),('equivalence_only_not_part_of',add_relation(delete(delete(base,'actual_seat_of_same_chair'),'seat_presence'),'equivalent','S','C'),False,True,None),('part_of_wrong_actual_chair',alter(add_owner(base,'D'),'actual_seat_of_same_chair',right='D'),False,True,None),('swapped_actual_owner_selection',base,False,True,[('chair','S'),('seat','C')]),('seat_kind_on_wholechair_not_seat',alter(base,'seat_type',owner='C'),False,True,None),('v2_explicit_equivalent_chair_alias',alias,True,True,[('chair','C_alias'),('seat','S')])]
ad=[];consumer=[]
for label,k,want,choose,binding in cases:
 for view in ['full','compact']:
  e=ent(S,cid,True,view)
  if choose:e,kk=select(e,k,p,binding)
  else:kk=k
  got=n.admission(e,kk);assert got['allowed']==want,(label,view,got)
  if want:assert len(got['resolved_guard_supports'])==1 and got['resolved_guard_supports'][0]['execution']['status']=='verified'
  ad.append({'case':label,'view':view,'expected':want,'result':got})
 e=ent(S,cid)
 if choose:e,kk=select(e,k,p,binding)
 else:kk=k
 got=generator.core_entry_eligible(S,kk,contract(),picked(),'aftermath_trace',e);assert got==want,(label,'consumer',got);consumer.append({'case':label,'expected':want,'allowed':got})
# Every real E target has actual scope; no artificial receiver or guard projection adds a mutation.
locks=[]
for dim,target,prop in [('pose','C','prop.orientation'),('role','S','prop.state.disturbed'),('timing','S','trace.recent_disturbance'),('role','C','prop.state.disturbed'),('timing','C','trace.recent_disturbance')]:
 # Last two ensure a protected wholechair also protects its actual part, without equating their scopes.
 e,k=select(ent(S,cid),base,p);ds,ps,g=n.permission_scope(e,k);assert n.property_scope_allowed(k,ds,ps,record=e);closed=copy.deepcopy(base);closed['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el,kl=select(ent(S,cid),closed,p);dl,pl,_=n.permission_scope(el,kl);denied=not n.property_scope_allowed(kl,dl,pl,record=el);assert denied,(dim,target,prop,pl);assert not generator.core_entry_eligible(S,kl,contract(),picked(),'aftermath_trace',el);locks.append({'dimension':dim,'target':target,'property':prop,'expanded_effects':pl,'denied':True})
whole=[]
for dim in ['pose','role','timing']:
 k=copy.deepcopy(base);k['intent_lock']['open_dimensions'].remove(dim);k['intent_lock']['locked_dimensions'].append(dim);e,kk=select(ent(S,cid),k,p);assert not generator.core_entry_eligible(S,kk,contract(),picked(),'aftermath_trace',e);whole.append({'dimension':dim,'denied':True})
# The independent structural relation is P, not an appearance E; it cannot open locked actual state scopes.
e,k=select(ent(S,cid),base,p);ds,ps,_=n.permission_scope(e,k);assert set(ds)=={'pose','role','timing'} and len(ps)==3 and all(x['dimension']!='appearance'for x in ps)
q=n.qualification(CAT['object_structure'],rec);assert q['status']=='eligible' and q['guard_admission_required'] and q['matched_properties']==[]
# Actual old presentation gates stay cumulative. Source itself has no human-only intrinsic requirement.
gates=[]
for category,domains,want in [('human',[],True),('human',['product'],False),('object',[],False),('object',['visual_structure'],True),('object',['visual_structure','product'],False),('human',['jewelry'],False),('human',['food'],False),('human',['wildlife'],False)]:
 e,k=select(ent(S,cid),base,p);got=generator.core_entry_eligible(S,k,contract(category,domains),picked(category),'aftermath_trace',e);assert got==want,(category,domains,got);gates.append({'category':category,'domains':domains,'allowed':got,'expected':want})
e,k=select(ent(S,cid),base,p)
import photo_global_retrieval
assert photo_global_retrieval.guard_policy(e['_role_conditions']['subject_applicability'],contract('object',['visual_structure']))
assert generator.entry_block_reason(e,'aftermath_trace',contract('object',['visual_structure']),catalog=CAT)is None
# Reject malformed/foreign provenance and role/unit claims even after a fresh authored-structure hash.
invalid=[]
for defect in ['foreign_cid','foreign_rid','branch_index','condition_hash','rule_hash','guard_schema_v1_on_actual_v2','endpoint','quote_from_metadata','mode_effect','projection_wrong_target','role_prefix_mismatch','missing_ordinary_guard_unit','introduced_endpoint','fake_typed_scalar_guard','guard_id_fact_collision']:
 z=copy.deepcopy(rec);pp=z['content']['role_evidence'];g=pp['guard_supports'][0]
 if defect=='foreign_cid':g['guard']['declaring_candidate_id']='cand_'+'0'*32
 elif defect=='foreign_rid':g['guard']['declaring_realization_id']='unselected'
 elif defect=='branch_index':g['guard']['source_condition_index']=1
 elif defect=='condition_hash':g['guard']['conditions_sha256']='0'*64
 elif defect=='rule_hash':g['guard']['rule_sha256']='0'*64
 elif defect=='guard_schema_v1_on_actual_v2':g['guard']['schema']='photo-native-source-guards/v1'
 elif defect=='endpoint':g['endpoints']['left']['target']='chair'
 elif defect=='quote_from_metadata':g['pointer']='/content/tags';g['quote']='trace'
 elif defect=='mode_effect':g['mode']='effect'
 elif defect=='projection_wrong_target':g['semantic_projection']['target']='foreign_owner'
 elif defect=='role_prefix_mismatch':g['semantic_projection']['property']='body.connection.part_of'
 elif defect=='missing_ordinary_guard_unit':pp['source_units'][2].pop('guard_refs')
 elif defect=='introduced_endpoint':pp['owner_maps']['base']['bindings'][1]['origin']='introduced'
 elif defect=='fake_typed_scalar_guard':g['value']={'type':'entity.owner_id/v1','value':'C'}
 elif defect=='guard_id_fact_collision':g['id']='chairP'
 pp['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(pp)
 try:n.validate(z,CAT,corpus={**S,'candidates':{**S['candidates'],cid:z}})
 except (ValueError,TypeError,KeyError) as exc:invalid.append({'case':defect,'rejected':True,'error':str(exc)})
 else:raise AssertionError('Invalid proof accepted: '+defect)
# Part graph cycles do not generate prerequisites; they are rejected independently before admission.
cycle=add_relation(base,'part_of','C','S')
try:n.frozen_witnesses(cycle)
except (ValueError,TypeError,KeyError) as exc:invalid.append({'case':'actual_part_cycle','rejected':True,'error':str(exc)})
else:raise AssertionError('part cycle accepted')
out={'schema':'photo-native-single06-actual-candidate-isolated-checks/v1','assignment_sha256':c.digest(A),'input_sha256':c.digest(I),'proposed_batch_sha256':c.digest(J),'full_source_validated':True,'compact':cp,'independent_synthetic_core':base,'full_compact_admission':ad,'actual_oldbinding_consumers':consumer,'oldbinding_display_gates':gates,'current_actual_consumer_override_check':{'object_visual_structure_binding_guard_allows':True,'actual_consumer_allows':True,'actual_entry_block_reason':None,'boundary':'Exact same actual input binding domain override consumed under final50fd92. Historical188c objectconsumer failure files remain immutable; source/proof/guards not changed to manufacture a human-only pass.'},'actual_target_and_part_ancestor_property_locks':locks,'whole_effect_dimension_locks':whole,'actual_E_permission_expanded':ps,'guard_role_qualification':q,'invalid_guard_provenance_and_cycle_cases':invalid,'scalar_count':len(p['facts']),'guard_support_count':len(p['guard_supports']),'sourceunit_count':len(p['source_units']),'all_passed':True,'module_paths_sha256':modules(),'frozen_generation':str(G),'root_accepted':False,'operating_count':0,'actual_runtime_request_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'v1_v2_boundary':'Actual source is v2 only; no synthetic conversion to v1. A v1 locator falsely addressing actual v2 is rejected. v2 canonical alias is independently explicit; part_of is never equivalence.','model_import_harddeny':True};f=O/'CHECKS-01264-v1.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('PASS',c.digest(out),'admission',len(ad),'consumer',len(consumer),'gates',len(gates),'propertylocks',len(locks),'wholelocks',len(whole),'invalid',len(invalid))
