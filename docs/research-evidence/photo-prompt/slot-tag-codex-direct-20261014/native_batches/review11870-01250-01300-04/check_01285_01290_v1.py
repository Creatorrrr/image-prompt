from fixture_wire_v1 import *
J=json.loads((O/'CHECKPOINT-01285-01290.json').read_text())
TEXT='Independent synthetic baseline: existing distinct humans A and B, mirror M and image I. Caller selected existing distinct humans C and D, existing camera K and existing subject U. Existing scene S. No colleague role, off-frame placement, pair visibility/count, camera movement, blur, sharpness or place selected in advance. Not a real requester core.'
def core(*a,**kw):return make_core(TEXT,*a,**kw)
pair=core(['A','B','M','I'],[('main_subject','A'),('secondary_subject','B'),('primary_prop','M'),('image','I')],[('subject','A','entity.type','entity.type/v1','human'),('subject','B','entity.type','entity.type/v1','human'),('subject','M','props.type','props.type/v1','mirror'),('subject','I','entity.presence','entity.presence/v1','present')],[('disjoint','A','B')],['composition','framing','count']);pair['intent_lock']['locked_dimensions'].remove('count')
coll=core(['C','D','I'],[('image','I')],[('subject','C','entity.presence','entity.presence/v1','present'),('subject','D','entity.presence','entity.presence/v1','present'),('subject','C','entity.category','entity.category/v1','human'),('subject','D','entity.category','entity.category/v1','human'),('subject','I','entity.presence','entity.presence/v1','present')],[('disjoint','C','D')],['relationship','framing']);CB=[('colleague','C'),('other_person','D')]
pan=core(['K','I','U'],[('recording_camera','K'),('image','I'),('main_subject','U')],[('subject','K','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','U','entity.presence','entity.presence/v1','present')],[],['camera'])
scene=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['setting'])
cases=[]
def case(o,label,k,want,b=None):
 e=entry(J,o)
 if b:e,k=selected(J,e,k,b)
 cases.append((o,label,e,k,want))
case(1286,'distinct_pair_mirror_image',pair,True);case(1286,'distinctness_missing',remove(pair,'disjoint'),False);case(1286,'precise_mirror_missing',remove(pair,'fact','props.type'),False)
for owner in ['A','B']:case(1286,'human_missing_'+owner,remove(pair,'fact','entity.type',owner),False)
case(1287,'selected_distinct_colleague_other_image',coll,True,CB);case(1287,'selection_missing',coll,False);case(1287,'distinctness_missing',remove(coll,'disjoint'),False,CB)
for prop,owner in [('entity.category','C'),('entity.category','D'),('entity.presence','C'),('entity.presence','D'),('entity.presence','I')]:case(1287,prop+'_'+owner+'_missing',remove(coll,'fact',prop,owner),False,CB)
case(1288,'camera_image_actual_subject',pan,True)
for prop,owner in [('entity.type','K'),('entity.presence','I'),('entity.presence','U')]:case(1288,prop+'_'+owner+'_missing',remove(pan,'fact',prop,owner),False)
case(1289,'scene_with_both_positive_phrase_units',scene,True);case(1289,'scene_missing',remove(scene,'fact','entity.presence'),False)
results=[]
for o,label,e,k,want in cases:
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,label,view,got);results.append({'ordinal':o,'case':label,'view':view,'expected':want,'result':got,'core_sha256':c.digest(k)})
configs=[(1286,pair,None,'composition','I','composition.group_arrangement'),(1286,pair,None,'composition','I','image.reflection'),(1286,pair,None,'framing','I','framing.subject_inclusion'),(1286,pair,None,'count','I','participant.count.visible'),(1287,coll,CB,'relationship','C','participant.role.colleague'),(1287,coll,CB,'relationship','C','context.offscreen.off_frame'),(1287,coll,CB,'framing','I','frame.coverage.selected_colleague'),(1288,pan,None,'camera','K','camera.movement'),(1288,pan,None,'camera','I','image.motion.blur'),(1288,pan,None,'camera','I','image.sharpness.subject'),(1289,scene,None,'setting','S','setting.location')]
permission=[];consumer=[]
for o,k,b,dim,target,prop in configs:
 e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 ds,ps,g=n.permission_scope(e,k);assert n.property_scope_allowed(k,ds,ps,record=e)
 locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,locked=selected(J,entry(J,o,binding=True),locked,b)
 dl,pl,gl=n.permission_scope(el,locked);assert not n.property_scope_allowed(locked,dl,pl,record=el);permission.append({'ordinal':o,'property':prop,'expanded_open_allowed':True,'actual_owner_anchor_denied':True})
 slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract('human'),picked('human'),slot,e),(o,'open');closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(J,entry(J,o,binding=True),closed,b)
 assert not generator.core_entry_eligible(S,closed,contract('human'),picked('human'),slot,ec);consumer.append({'ordinal':o,'dimension':dim,'exact_old_binding_open_allowed':True,'closed_dimension_denied':True})
for o,k,b,dim,target,prop in [(1286,pair,None,'composition','M','image.reflection'),(1286,pair,None,'count','B','participant.count.visible'),(1287,coll,CB,'relationship','D','participant.role.colleague'),(1287,coll,CB,'relationship','I','context.offscreen.off_frame'),(1287,coll,CB,'framing','C','frame.coverage.selected_colleague'),(1288,pan,None,'camera','U','image.sharpness.subject')]:
 k=copy.deepcopy(k);k['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});e=entry(J,o,binding=True)
 if b:e,k=selected(J,e,k,b)
 ds,ps,g=n.permission_scope(e,k);assert not n.property_scope_allowed(k,ds,ps,record=e);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);permission.append({'ordinal':o,'actual_receiver_anchor':target,'property':prop,'expanded_E_denied':True});consumer.append({'ordinal':o,'actual_receiver_anchor':target,'whole_consumer_denied':True})
e,k=selected(J,entry(J,1287,binding=True),coll,CB);assert not generator.core_entry_eligible(S,k,contract('human',['product']),picked('human'),e['_presentation_role'],e);consumer.append({'ordinal':1287,'original_product_deny_retained':True})
r=next(x for x in J['records']if x['ordinal']==1289);assert {f['pointer']for f in r['proof']['facts']} >= {'/content/phrase_en','/content/phrase_ko'};assert {f['pointer']for f in r['proof']['source_units']} >= {'/content/phrase_en','/content/phrase_ko'}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':modules(),'synthetic_cases':results,'property_permission_checks':permission,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':len(configs)*2+6,'consumer_assertions':len(configs)*2+7,'positive_phrase_unit_fact_inventory_assertions':2,'all_passed':True,'root_acceptance_count':0,'os_network_denied':True,'provider_keys_absent':True,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False};f=O/'CHECKS-01285-01290-v1.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),len(results))
