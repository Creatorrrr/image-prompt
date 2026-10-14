"""Independent actual local-region/shared-holder witnesses, exact gates, every E/Rx/ancestor lock."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');p=O/'check_01275_01280_v1.py';exec(compile(p.read_text().split('study=core',1)[0],str(p),'exec'))
J=json.loads((O/'CHECKPOINT-01295-01300-v1.json').read_text());assert c.digest(J)=='f3b49d2d15052bb404580d9af2f0bd831162f02835c205b2e374bc84565bb4a4'
TEXT='Independent synthetic baseline: actual existing skin regions A and B, each exact skin type and independent neutral presence, distinct and each part of declared actual owner U or V; no aged/young appearance already frozen. Actual existing mug M, distinct actual existing hands H and K each part of same actual existing holder U; each independent neutral presence and exact mug/hand types. A third hand may exist; no whole anatomical count asserted. Existing actual object O at primary_prop; existing exact florist-delivery box X at primary_prop. Only declared effect dimensions mutable; age and concept remain protected. These are independently authored controlled declarations, not source-generated witnesses or a real requester core.'
def skin(same=False):
 owners=['A','B','U']if same else['A','B','U','V'];right='U'if same else'V'
 return core(owners,[],[('subject',x,'entity.presence','entity.presence/v1','present')for x in owners]+[('subject',x,'body.region.kind','body.region.kind/v1','skin')for x in ['A','B']],[('part_of','A','U'),('part_of','B',right),('disjoint','A','B')],['appearance'])
mug=core(['M','H','K','U'],[],[('subject',x,'entity.presence','entity.presence/v1','present')for x in ['M','H','K','U']]+[('subject','M','props.type','props.type/v1','mug'),('subject','H','entity.type','entity.type/v1','hand'),('subject','K','entity.type','entity.type/v1','hand')],[('part_of','H','U'),('part_of','K','U'),('disjoint','H','K'),('disjoint','M','H'),('disjoint','M','K')],['action','material','relationship'])
obj=core(['O'],[('primary_prop','O')],[('subject','O','entity.type','entity.type/v1','object')],[],['composition','style'])
box=core(['X'],[('primary_prop','X')],[('subject','X','props.type','props.type/v1','florist_delivery_box')],[],['role'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def entry(o):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0],realization_id='base')
def choose(o,k,view='full',bindings=None):
 e=entry(o);k=copy.deepcopy(k)
 if o in [1295,1296]and bindings is not False:
  k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];selected=bindings or([('aged_region','A'),('young_region','B'),('aged_owner','U'),('young_owner','V')]if o==1295 else[('mug','M'),('hand_a','H'),('hand_b','K'),('holder','U')])
  e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':x}for t,x in selected]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
configs=[(1295,skin(),False,'human'),(1296,mug,True,'object'),(1297,obj,True,'object'),(1298,box,False,'human')];results=[];extra=[];views=[]
for o,k,want,category in configs:
 e,kk=choose(o,k);ds,ps,_=n.permission_scope(e,kk);slot=e['_presentation_role'];checks=[]
 for view in ['full','compact']:
  z,kk=choose(o,k,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,view,receipt);assert generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z)==want,(o,view,'baseconsumer');assert n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z)
  checks.append({'case':'independent_precise_P_and_all_source_guards','view':view,'admission':receipt,'actual_same_oldbinding_consumer_allowed':want,'normal_age_concept_not_opened':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,bad,view);assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,'property',prop);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z)
   checks.append({'case':'every_actual_E_target_Rx_and_part_ancestor_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_oldbinding_consumer_denied':True,'consumer_normally_protected':not want})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k)
   if dim in bad['intent_lock']['open_dimensions']:bad['intent_lock']['open_dimensions'].remove(dim)
   if dim not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['locked_dimensions'].append(dim)
   z,kk=choose(o,bad,view);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z),(o,view,'whole',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_oldbinding_consumer_denied':True})
 # These fixture declarations are exactly the manual P/selected-origin/source-guard witnesses, no source effect facts.
 for a in k['semantic_assertions']:
  if a['axes']['kind']in ['owner','role']:continue
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']];z,kk=choose(o,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,view,'missingP_or_guard',a,receipt);assert not generator.core_entry_eligible(S,kk,contract(category),picked(category),slot,z)
   checks.append({'case':'each_exact_P_preservation_selected_origin_or_source_guard','view':view,'removed':a,'admission':receipt,'actual_oldbinding_consumer_denied':True})
 results.append({'ordinal':o,'core':k,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks,'base_actual_consumer_expected':want})
 for role in next(r['proof']['roles']for r in J['records']if r['ordinal']==o):
  for view in ['full','compact']:
   z,kk=choose(o,k,view);assert generator.core_entry_eligible(S,kk,contract(category),picked(category),role,z)==want,(o,view,role);extra.append({'ordinal':o,'view':view,'case':'each_sourcequalified_role_same_oldbinding','role':role,'allowed':want})
 for view in ['full','compact']:
  if o in [1295,1296]:
   z,kk=choose(o,k,view,False);receipt=n.admission(z,kk);assert not receipt['allowed'];extra.append({'ordinal':o,'view':view,'case':'no_actual_caller_owner_selection','admission':receipt})
 if o==1296:
  rec=S['candidates'][e['id']];guard=layout.guard_record(rec,S);full=n.qualification(I['catalog_review']['after']['relational_action'],rec,source_data=S);compact=n.qualification(I['catalog_review']['after']['relational_action'],guard,source_data=S);assert full==compact and full['status']=='eligible'and full['matched_manual_role_views'];assert ds==['action','material','relationship'];views.append({'ordinal':o,'fullcompact_qualification':full,'canonical_footprint_unchanged':{'dimensions':ds,'properties':ps}})
for view in ['full','compact']:
 k=skin(True);z,kk=choose(1295,k,view,[('aged_region','A'),('young_region','B'),('aged_owner','U'),('young_owner','U')]);receipt=n.admission(z,kk);assert receipt['allowed'];assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),'age_presentation',z);extra.append({'ordinal':1295,'view':view,'case':'two_distinct_regions_same_actual_owner_allowed_without_twopeople','core':k,'admission':receipt,'normal_age_consumer_denied':True})
 k=copy.deepcopy(mug);k['semantic_assertions'] +=[assertion('extra_hand_owner','owner',owner='Q',owner_kind='entity'),assertion('extra_hand_presence','fact',owner='Q',property='entity.presence',value_type='entity.presence/v1',value='present'),assertion('extra_hand_type','fact',owner='Q',property='entity.type',value_type='entity.type/v1',value='hand'),assertion('extra_hand_part','part_of',left='Q',right='U')];z,kk=choose(1296,k,view);receipt=n.admission(z,kk);assert receipt['allowed'];assert generator.core_entry_eligible(S,kk,contract('object'),picked('object'),'relational_action',z);extra.append({'ordinal':1296,'view':view,'case':'third_anatomical_hand_not_forbidden_participating_two_only','core':k,'admission':receipt,'consumer_allowed':True})
 k=copy.deepcopy(mug);k['semantic_assertions'].append(assertion('other_holder','owner',owner='V',owner_kind='entity'))
 for a in k['semantic_assertions']:
  if a['axes']['kind']=='part_of'and a['axes']['left']=='K':a['axes']['right']='V'
 z,kk=choose(1296,k,view);receipt=n.admission(z,kk);assert not receipt['allowed'];extra.append({'ordinal':1296,'view':view,'case':'second_hand_different_actual_holder_rejected','admission':receipt})
 for category in ['object','product','food']:
  z,kk=choose(1297,obj,view);receipt=n.admission(z,kk);assert receipt['allowed'];assert generator.core_entry_eligible(S,kk,contract(category),picked(category),'staging_degree',z);extra.append({'ordinal':1297,'view':view,'case':'original_object_product_food_gate_with_independent_exact_object_P','category':category,'consumer_allowed':True})
 z,kk=choose(1297,obj,view);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),'staging_degree',z);extra.append({'ordinal':1297,'view':view,'case':'source_object_product_food_gate_not_waived_by_generic_staging','human_consumer_denied':True})
 z,kk=choose(1298,box,view);assert not generator.core_entry_eligible(S,kk,contract('object'),picked('object'),'prop',z);extra.append({'ordinal':1298,'view':view,'case':'source_human_gate_not_waived_by_existing_box','consumer_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_role_view_checks':views,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Independent controlled declarations only, not actual requester witnesses. Every actual E/Rx/part-ancestor property, whole dimension, exact P/preservation/selected-origin/sourceguards and oldbinding checked fullcompact.1295 normal age and1298 normal concept remain protected. Same-owner regions and third anatomical hand positive; different-holder and missingpreciseP negative.1299pending untouched. No source/code/Git/runtime mutation.'}
p=O/'CHECKS-01295-01300-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
