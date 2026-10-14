from fixture_wire_v1 import *
J=json.loads((O/'CHECKPOINT-01295-01300.json').read_text());TEXT='Independent synthetic witnesses: actual skin regions R and Y are distinct parts of declared owner O, each explicitly skin. Holder H has actual distinct hands A and B, each hand is a declared part of H; mug M is distinct from each hand. Existing object X, existing florist-delivery box F fixed as that exact type. No aged/young skin, heat, holding/contact, floating or cover function pre-frozen. Not a real requester core.'
def core(*a,**kw):return make_core(TEXT,*a,**kw)
skin=core(['R','Y','O'],[],[('subject','R','entity.presence','entity.presence/v1','present'),('subject','Y','entity.presence','entity.presence/v1','present'),('subject','O','entity.presence','entity.presence/v1','present'),('subject','R','body.region.kind','body.region.kind/v1','skin'),('subject','Y','body.region.kind','body.region.kind/v1','skin')],[('part_of','R','O'),('part_of','Y','O'),('disjoint','R','Y')],['appearance','age']);skin['intent_lock']['locked_dimensions'].remove('age');SB=[('aged_region','R'),('young_region','Y'),('aged_owner','O'),('young_owner','O')]
mug=core(['M','A','B','H'],[],[('subject','M','entity.presence','entity.presence/v1','present'),('subject','A','entity.presence','entity.presence/v1','present'),('subject','B','entity.presence','entity.presence/v1','present'),('subject','H','entity.presence','entity.presence/v1','present'),('subject','M','props.type','props.type/v1','mug'),('subject','A','entity.type','entity.type/v1','hand'),('subject','B','entity.type','entity.type/v1','hand')],[('part_of','A','H'),('part_of','B','H'),('disjoint','A','B'),('disjoint','M','A'),('disjoint','M','B')],['action','material','relationship']);MB=[('mug','M'),('hand_a','A'),('hand_b','B'),('holder','H')]
obj=core(['X'],[('primary_prop','X')],[('subject','X','entity.type','entity.type/v1','object')],[],['composition','style'])
box=core(['F'],[('primary_prop','F')],[('subject','F','props.type','props.type/v1','florist_delivery_box')],[],['concept']);box['intent_lock']['locked_dimensions'].remove('concept')
cases=[]
def case(o,label,k,want,b=None):
 e=entry(J,o)
 if b:e,k=selected(J,e,k,b)
 cases.append((o,label,e,k,want))
case(1295,'two_regions_same_actual_owner_valid',skin,True,SB);case(1295,'caller_selection_missing',skin,False);case(1295,'regions_not_disjoint',remove(skin,'disjoint'),False,SB)
for prop,owner in [('entity.presence','R'),('entity.presence','Y'),('entity.presence','O'),('body.region.kind','R'),('body.region.kind','Y')]:case(1295,prop+'_'+owner+'_missing',remove(skin,'fact',prop,owner),False,SB)
for l in ['R','Y']:
 k=copy.deepcopy(skin);k['semantic_assertions']=[x for x in k['semantic_assertions']if not(x['axes']['kind']=='part_of'and x['axes']['left']==l)];case(1295,'part_of_missing_'+l,k,False,SB)
case(1295,'wrong_region_material',change(skin,'body.region.kind','fabric'),False,SB)
case(1296,'same_holder_two_actual_hands',mug,True,MB);case(1296,'selection_missing',mug,False)
for prop,owner in [('props.type','M'),('entity.type','A'),('entity.type','B'),('entity.presence','M'),('entity.presence','A'),('entity.presence','B'),('entity.presence','H')]:case(1296,prop+'_'+owner+'_missing',remove(mug,'fact',prop,owner),False,MB)
for kind,l,r in [('part_of','A','H'),('part_of','B','H'),('disjoint','A','B'),('disjoint','M','A'),('disjoint','M','B')]:
 k=copy.deepcopy(mug);k['semantic_assertions']=[x for x in k['semantic_assertions']if not(x['axes']['kind']==kind and x['axes'].get('left')==l and x['axes'].get('right')==r)];case(1296,kind+l+r+'_missing',k,False,MB)
case(1297,'existing_object',obj,True);case(1297,'object_type_missing',remove(obj,'fact','entity.type'),False)
case(1298,'same_precise_box_fixed',box,True);case(1298,'precise_box_missing',remove(box,'fact','props.type'),False);case(1298,'wrong_box_identity',change(box,'props.type','cardboard_box'),False)
results=[]
for o,label,e,k,want in cases:
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,label,view,got);results.append({'ordinal':o,'case':label,'view':view,'expected':want,'result':got,'core_sha256':c.digest(k)})
configs=[(1295,skin,SB,'appearance','R','skin.texture.age_appearance'),(1295,skin,SB,'appearance','Y','skin.texture.age_appearance'),(1295,skin,SB,'age','R','age.presentation.local_skin'),(1295,skin,SB,'age','Y','age.presentation.local_skin'),(1296,mug,MB,'material','M','object.temperature.declared'),(1296,mug,MB,'action','A','action.holding'),(1296,mug,MB,'action','B','action.holding'),(1296,mug,MB,'relationship','M','contact.held_by'),(1297,obj,None,'composition','X','objects.position'),(1297,obj,None,'style','X','presentation.staging'),(1298,box,None,'concept','F','narrative.clue.function')]
permission=[];consumer=[]
for o,k,b,dim,target,prop in configs:
 e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 ds,ps,g=n.permission_scope(e,k);assert n.property_scope_allowed(k,ds,ps,record=e)
 locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,locked=selected(J,entry(J,o,binding=True),locked,b)
 dl,pl,gl=n.permission_scope(el,locked);assert not n.property_scope_allowed(locked,dl,pl,record=el);permission.append({'ordinal':o,'actual_owner':target,'property':prop,'expanded_open_allowed':True,'anchor_denied':True})
 cat='object'if o==1297 else'human';co=contract(cat,['product'])if o==1297 else contract(cat);pi=picked(cat);slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,co,pi,slot,e),(o,'open')
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(J,entry(J,o,binding=True),closed,b)
 assert not generator.core_entry_eligible(S,closed,co,pi,slot,ec);consumer.append({'ordinal':o,'dimension':dim,'exact_old_binding_open_allowed':True,'closed_whole_E_denied':True})
for o,k,b,dim,owner,prop in [(1295,skin,SB,'age','O','age.presentation.local_skin'),(1295,skin,SB,'appearance','O','skin.texture.age_appearance'),(1296,mug,MB,'action','M','action.holding'),(1296,mug,MB,'action','H','action.holding'),(1296,mug,MB,'relationship','A','contact.held_by'),(1296,mug,MB,'relationship','H','contact.held_by')]:
 k=copy.deepcopy(k);k['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':owner,'property':prop});e,k=selected(J,entry(J,o,binding=True),k,b);ds,ps,g=n.permission_scope(e,k);assert not n.property_scope_allowed(k,ds,ps,record=e);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);permission.append({'ordinal':o,'actual_receiver_or_ancestor_anchor':owner,'property':prop,'expanded_E_denied':True});consumer.append({'ordinal':o,'actual_receiver_or_ancestor_anchor':owner,'whole_consumer_denied':True})
for o,k,cat,ds in [(1297,obj,'human',['product']),(1298,box,'object',[])]:
 e=entry(J,o,binding=True);assert not generator.core_entry_eligible(S,k,contract(cat,ds),picked(cat),e['_presentation_role'],e);consumer.append({'ordinal':o,'intrinsic_subject_condition_retained':True})
r=next(x for x in J['records']if x['ordinal']==1296);assert {f['pointer']for f in r['proof']['facts']if f['property']=='contact.held_by'}=={'/content/ko','/content/application_contract'}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':modules(),'synthetic_cases':results,'property_permission_checks':permission,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':28,'consumer_assertions':30,'contact_own_language_anchor_inventory_assertions':1,'all_passed':True,'root_acceptance_count':0,'os_network_denied':True,'provider_keys_absent':True,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False};f=O/'CHECKS-01295-01300-v1.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),len(results))
