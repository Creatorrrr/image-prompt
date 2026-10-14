from fixture_wire_v1 import *
J=json.loads((O/'CHECKPOINT-01280-01285.json').read_text())
TEXT='Independent isolated synthetic witnesses declare scene S, recording camera K, image I, existing crowd C, caller selected existing face F with eyes on F. No season, mood, concert, ghost bride, focal plane or crowd arrangement is pre-frozen. Not a real requester core.'
def core(*a,**kw):return make_core(TEXT,*a,**kw)
scene=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['setting','timing','atmosphere','concept']);scene['intent_lock']['locked_dimensions'].remove('concept')
concert=core(['K','I','C','S'],[('recording_camera','K'),('image','I'),('secondary_subject','C'),('scene','S')],[('subject','K','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','C','entity.type','entity.type/v1','crowd'),('subject','S','entity.presence','entity.presence/v1','present')],[],['camera','composition','event']);concert['intent_lock']['locked_dimensions'].remove('event')
face=core(['I','F'],[('image','I')],[('subject','I','entity.presence','entity.presence/v1','present'),('subject','F','entity.presence','entity.presence/v1','present'),('subject','F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present')],[],['camera']);FB=[('face','F')]
cases=[]
def case(o,label,k,want,b=None):
 e=entry(J,o)
 if b:e,k=selected(J,e,k,b)
 cases.append((o,label,e,k,want))
for o in [1280,1281,1282]:case(o,'existing_scene_no_selected_value_prefrozen',scene,True);case(o,'scene_missing',remove(scene,'fact','entity.presence'),False)
case(1283,'camera_image_crowd_scene',concert,True)
for prop,owner in [('entity.type','K'),('entity.type','C'),('entity.presence','I'),('entity.presence','S')]:case(1283,prop+'_'+owner+'_missing',remove(concert,'fact',prop,owner),False)
case(1284,'same_selected_face_atomic_parts',face,True,FB);case(1284,'selection_missing',face,False)
for prop in ['entity.presence','anatomy.face.presence','anatomy.eyes.presence']:case(1284,prop+'_on_face_missing',remove(face,'fact',prop,'F'),False,FB)
k=copy.deepcopy(face);next(x for x in k['semantic_assertions']if x['axes'].get('property')=='anatomy.eyes.presence')['axes']['owner']='I';case(1284,'eyes_on_image_no_inheritance',k,False,FB)
results=[]
for o,label,e,k,want in cases:
 for mode in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if mode=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,label,mode,got);results.append({'ordinal':o,'case':label,'view':mode,'expected':want,'result':got,'core_sha256':c.digest(k)})
configs=[(1280,scene,None,'setting','S','setting.location'),(1280,scene,None,'concept','S','narrative.association'),(1281,scene,None,'setting','S','setting.location'),(1281,scene,None,'timing','S','timing.season'),(1282,scene,None,'atmosphere','S','mood.atmosphere'),(1283,concert,None,'camera','K','camera.direction'),(1283,concert,None,'composition','I','composition.view_boundary'),(1283,concert,None,'event','S','occasion.context'),(1284,face,FB,'camera','I','focus.selected_plane')]
permission=[];consumer=[]
for o,k,b,dim,target,prop in configs:
 e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 dims,props,g=n.permission_scope(e,k);assert n.property_scope_allowed(k,dims,props,record=e)
 locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,locked=selected(J,entry(J,o,binding=True),locked,b)
 dl,pl,gl=n.permission_scope(el,locked);assert not n.property_scope_allowed(locked,dl,pl,record=el);permission.append({'ordinal':o,'dimension':dim,'property':prop,'expanded_open_allowed':True,'anchor_denied':True})
 cat='human';co=contract(cat,['album'])if o==1284 else contract(cat);pi=picked(cat);pi['subject']['tags']+=['album']if o==1284 else [];slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,co,pi,slot,e),(o,'open')
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(J,entry(J,o,binding=True),closed,b)
 assert not generator.core_entry_eligible(S,closed,co,pi,slot,ec);consumer.append({'ordinal':o,'dimension':dim,'actual_old_binding_open_allowed':True,'closed_whole_E_denied':True})
for o,k,b,dim,receiver,prop in [(1283,concert,None,'composition','C','composition.view_boundary'),(1284,face,FB,'camera','F','focus.selected_plane')]:
 k=copy.deepcopy(k);k['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':receiver,'property':prop});e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 ds,ps,gr=n.permission_scope(e,k);assert not n.property_scope_allowed(k,ds,ps,record=e);pi=picked('human');pi['subject']['tags'].append('album');assert not generator.core_entry_eligible(S,k,contract('human',['album']),pi,e['_presentation_role'],e);permission.append({'ordinal':o,'receiver_anchor':receiver,'expanded_E_denied':True});consumer.append({'ordinal':o,'receiver_anchor':receiver,'actual_consumer_denied':True})
e,k=selected(J,entry(J,1284,binding=True),face,FB);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);consumer.append({'ordinal':1284,'kpop_or_album_missing_denied':True})
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':modules(),'synthetic_cases':results,'property_permission_checks':permission,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':len(permission)*2,'consumer_assertions':len(consumer)*2-3,'all_passed':True,'root_acceptance_count':0,'os_network_denied':True,'provider_keys_absent':True,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False};p=O/'CHECKS-01280-01285-v2.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),len(results),len(permission),len(consumer))
