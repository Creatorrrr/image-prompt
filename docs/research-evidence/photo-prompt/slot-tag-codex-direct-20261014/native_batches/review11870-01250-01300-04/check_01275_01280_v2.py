from fixture_wire_v1 import *
J=json.loads((O/'CHECKPOINT-01275-01280.json').read_text())
TEXT='Independent synthetic baseline: existing human P at main_subject and existing star-map tablet T at primary_prop are explicitly distinct, with declared star-map semantic content fixed. Existing recording camera K, image I and railing R are declared. Existing human character C has already declared face F and actual hands-region H containing hands; F and H are distinct parts of C. No exact total hands, help action, temperature, familiarity, study action or blank expression is pre-frozen. Existing scene S is declared. These are isolated synthetic cases, not a real requester core.'
def core(*a,**kw):return make_core(TEXT,*a,**kw)
study=core(['P','T'],[('main_subject','P'),('primary_prop','T')],[('subject','P','entity.type','entity.type/v1','human'),('subject','T','props.type','props.type/v1','star_map_tablet'),('concept','T','representation.content','representation.content/v1','star_map')],[('disjoint','P','T')],['action','relationship'])
view=core(['K','I','R'],[('recording_camera','K'),('image','I'),('primary_prop','R')],[('subject','K','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','R','props.type','props.type/v1','railing')],[],['camera','composition'])
person=core(['P'],[('main_subject','P')],[('subject','P','entity.type','entity.type/v1','human')],[],['appearance'])
handvals=[('subject','C','entity.presence','entity.presence/v1','present'),('subject','F','entity.presence','entity.presence/v1','present'),('subject','H','entity.presence','entity.presence/v1','present'),('subject','C','entity.category','entity.category/v1','human'),('subject','F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','H','entity.type','entity.type/v1','hands_region'),('subject','H','anatomy.hands.presence','anatomy.hands.presence/v1','present')]
hands=core(['C','F','H'],[],handvals,[('part_of','F','C'),('part_of','H','C'),('disjoint','F','H')],['expression','character_response'])
scene=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['setting'])
HB=[('character','C'),('face','F'),('hands','H')]
cases=[]
def case(o,label,k,want,bind=None):
 e=entry(J,o)
 if bind:e,k=selected(J,e,k,bind)
 cases.append((o,label,e,k,want))
case(1275,'same_studier_tablet_and_preserved_content',study,True);case(1275,'content_preservation_witness_missing',remove(study,'fact','representation.content'),False);case(1275,'wrong_preserved_map_content',change(study,'representation.content','blank_screen'),False);case(1275,'precise_tablet_missing',remove(study,'fact','props.type'),False);case(1275,'distinctness_missing',remove(study,'disjoint'),False)
case(1276,'camera_image_and_railing',view,True);case(1276,'camera_type_missing',remove(view,'fact','entity.type'),False);case(1276,'image_presence_missing',remove(view,'fact','entity.presence'),False);case(1276,'railing_type_missing',remove(view,'fact','props.type'),False)
case(1277,'precise_human_P',person,True);case(1277,'person_type_missing',remove(person,'fact','entity.type'),False)
case(1278,'selected_same_character_owned_regions',hands,True,HB);case(1278,'selection_missing',hands,False)
for label,k in [('character_human_missing',remove(hands,'fact','entity.category')),('face_anatomy_missing',remove(hands,'fact','anatomy.face.presence')),('hands_region_type_missing',remove(hands,'fact','entity.type')),('actual_hands_presence_missing',remove(hands,'fact','anatomy.hands.presence')),('generic_face_presence_for_selector_missing',remove(hands,'fact','entity.presence','F')),('generic_hands_presence_for_selector_missing',remove(hands,'fact','entity.presence','H')),('region_disjoint_missing',remove(hands,'disjoint'))]:case(1278,label,k,False,HB)
for left in ['F','H']:
 k=copy.deepcopy(hands);k['semantic_assertions']=[x for x in k['semantic_assertions']if not(x['axes']['kind']=='part_of'and x['axes']['left']==left)];case(1278,'missing_part_of_'+left,k,False,HB)
k=copy.deepcopy(hands);next(x for x in k['semantic_assertions']if x['axes'].get('property')=='anatomy.face.presence')['axes']['owner']='C';case(1278,'face_anatomy_on_whole_character_no_inheritance',k,False,HB)
case(1279,'existing_scene_and_full_phrase_units',scene,True);case(1279,'scene_missing',remove(scene,'fact','entity.presence'),False)
results=[]
for o,label,e,k,want in cases:
 for mode in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if mode=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,label,mode,got);results.append({'ordinal':o,'case':label,'view':mode,'expected':want,'result':got,'core_sha256':c.digest(k)})
configs=[(1275,study,None,'action','P','action.studying'),(1275,study,None,'relationship','P','relationship.familiarity'),(1276,view,None,'camera','K','camera.direction'),(1276,view,None,'composition','I','composition.boundary_arrangement'),(1277,person,None,'appearance','P','presentation.style'),(1278,hands,HB,'expression','F','expression.face'),(1278,hands,HB,'character_response','H','response.presentation'),(1278,hands,HB,'character_response','H','character.contrast'),(1279,scene,None,'setting','S','setting.location')]
permission=[];consumer=[]
for o,k,b,dim,target,prop in configs:
 e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 lock=copy.deepcopy(k);lock['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,lock=selected(J,entry(J,o,binding=True),lock,b)
 assert not n.property_scope_allowed(lock,el['affected_dimensions'],el['affected_properties'],record=el);permission.append({'ordinal':o,'dimension':dim,'property':prop,'open_allowed':True,'same_actual_owner_property_anchor_denied':True})
 slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract('human'),picked('human'),slot,e),(o,'positiveconsumer');closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(J,entry(J,o,binding=True),closed,b)
 assert not generator.core_entry_eligible(S,closed,contract('human'),picked('human'),slot,ec);consumer.append({'ordinal':o,'dimension':dim,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'open_allowed':True,'closed_whole_E_dimension_denied':True})
# Complete contrast E sees its actual face receiver and the actual character ancestor; part_of is never equality.
for target in ['F','C']:
 k=copy.deepcopy(hands);k['intent_lock']['semantic_anchors'].append({'dimension':'character_response','target':target,'property':'character.contrast'});e,k=selected(J,entry(J,1278,binding=True),k,HB);raw=n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e);assert raw==(target=='F');dims,expanded,graph=n.permission_scope(e,k);assert not n.property_scope_allowed(k,dims,expanded,record=e);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);permission.append({'ordinal':1278,'actual_receiver_or_ancestor_anchor':target,'raw_unexpanded_property_only_allowed':raw,'expanded_whole_contrast_E_denied':True});consumer.append({'ordinal':1278,'receiver_or_ancestor_anchor':target,'actual_whole_E_consumer_denied':True})
e=entry(J,1277,binding=True);assert not generator.core_entry_eligible(S,person,contract('human',['documentary']),picked('human'),e['_presentation_role'],e);consumer.append({'ordinal':1277,'documentary_tag_does_not_waive_exact_old_display_documentary_deny':True})
r=next(x for x in J['records']if x['ordinal']==1279);assert {x['pointer']for x in r['proof']['source_units']} >= {'/content/phrase_en','/content/phrase_ko'};assert {x['pointer']for x in r['proof']['facts']} >= {'/content/phrase_en','/content/phrase_ko'}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':modules(),'synthetic_cases':results,'property_permission_checks':permission,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':22,'consumer_assertions':21,'positive_phrase_unit_fact_inventory_assertions':2,'all_passed':True,'root_acceptance_count':0,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False,'boundary':'Only manually specified independent synthetic witnesses. Actual part owners, exact source-target v2 guards, receiver/ancestor anchors and implicit selected-owner generic presence are checked separately from precise body/class P. No new reference units or actual requester/runtime/final/render/pixel claim.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};p=O/'CHECKS-01275-01280-v2.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(p,c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest(),len(results),22,21,2)
