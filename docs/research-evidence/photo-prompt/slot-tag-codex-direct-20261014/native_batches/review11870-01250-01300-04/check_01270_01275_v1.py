from fixture_wire_v1 import *
J=json.loads((O/'CHECKPOINT-01270-01275.json').read_text())
TEXT='Independent synthetic baseline declares actual fairy-light source L and image I; a single actual hand H and existing Polaroid-print set P are explicitly distinct; actual leather surface S is independently selected; an existing action figure or doll T is independently typed for that case; actual air volume A and scene Q are declared. No small, stacked, holding, bokeh, cracked, beam or haze effect is already frozen. No production requester core is created.'
def core(*args,**kwargs):return make_core(TEXT,*args,**kwargs)
light=core(['L','I'],[('light_source','L'),('image','I')],[('lighting','L','lighting.source.type','lighting.source.type/v1','fairy_lights'),('subject','I','entity.presence','entity.presence/v1','present')],[],['camera'],extra_locked=['lighting'])
prints=core(['H','P'],[('primary_hands','H'),('primary_prop','P')],[('subject','H','entity.type','entity.type/v1','hand'),('subject','P','props.type','props.type/v1','polaroid_print_set')],[('disjoint','H','P')],['action','role'])
leather=core(['S'],[],[('subject','S','entity.presence','entity.presence/v1','present'),('material','S','surface.material','surface.material/v1','leather')],[],['material'],anchors=[{'dimension':'material','target':'S','property':'surface.material'}])
figure=core(['T'],[],[('subject','T','entity.presence','entity.presence/v1','present'),('subject','T','props.type','props.type/v1','action_figure')],[],['appearance','role'])
doll=core(['T'],[],[('subject','T','entity.presence','entity.presence/v1','present'),('subject','T','props.type','props.type/v1','doll')],[],['appearance','role'])
air=core(['A','Q'],[('light_receiver','A'),('scene','Q')],[('subject','A','entity.type','entity.type/v1','air_volume'),('subject','Q','entity.presence','entity.presence/v1','present')],[],['atmosphere','lighting'])
cases=[]
def case(o,label,k,want,rid='base',bind=None):
 e=entry(J,o,rid)
 if bind:e,k=selected(J,e,k,bind)
 cases.append((o,rid,label,e,k,want))
case(1270,'precise_light_and_image',light,True);case(1270,'no_light_type',remove(light,'fact','lighting.source.type'),False);case(1270,'no_image',remove(light,'fact','entity.presence'),False);case(1270,'wrong_light_type',change(light,'lighting.source.type','neon'),False)
case(1271,'same_single_hand_and_precise_print_set',prints,True);case(1271,'distinctness_missing',remove(prints,'disjoint'),False);case(1271,'hand_type_missing',remove(prints,'fact','entity.type'),False);case(1271,'hands_group_not_single_hand',change(prints,'entity.type','hands_group'),False);case(1271,'precise_print_set_missing',remove(prints,'fact','props.type'),False)
case(1272,'chosen_leather',leather,True,bind=[('surface','S')]);case(1272,'no_caller_choice',leather,False);case(1272,'no_precise_leather',remove(leather,'fact','surface.material'),False,bind=[('surface','S')]);case(1272,'wrong_material',change(leather,'surface.material','fabric'),False,bind=[('surface','S')]);case(1272,'no_presence',remove(leather,'fact','entity.presence'),False,bind=[('surface','S')])
case(1273,'selected_action_figure_no_pre_small_P',figure,True,'small_action_figure',[('toy','T')]);case(1273,'selected_doll_no_pre_prop_role_P',doll,True,'small_doll',[('toy','T')]);case(1273,'figure_rid_wrong_doll',doll,False,'small_action_figure',[('toy','T')]);case(1273,'doll_rid_wrong_figure',figure,False,'small_doll',[('toy','T')]);case(1273,'figure_missing_choice',figure,False,'small_action_figure');case(1273,'doll_missing_precise_type',remove(doll,'fact','props.type'),False,'small_doll',[('toy','T')])
case(1274,'actual_air_volume_and_scene_no_pre_beams_P',air,True);case(1274,'air_type_missing',remove(air,'fact','entity.type'),False);case(1274,'wrong_air_scope_type',change(air,'entity.type','receiving_wall'),False);case(1274,'scene_missing',remove(air,'fact','entity.presence'),False)
results=[]
for o,rid,label,e,k,want in cases:
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,rid,label,view,got);results.append({'ordinal':o,'rid':rid,'case':label,'view':view,'expected':want,'result':got,'core_sha256':c.digest(k)})
configs=[(1270,'base',light,None,'camera','I','lens.artifact.bokeh','human'),(1271,'base',prints,None,'action','H','action.holding','human'),(1271,'base',prints,None,'role','P','prop.state','human'),(1272,'base',leather,[('surface','S')],'material','S','surface.texture','human'),(1273,'small_action_figure',figure,[('toy','T')],'appearance','T','object.geometry.size','human'),(1273,'small_action_figure',figure,[('toy','T')],'role','T','props.scene_role','human'),(1273,'small_doll',doll,[('toy','T')],'appearance','T','object.geometry.size','human'),(1273,'small_doll',doll,[('toy','T')],'role','T','props.scene_role','human'),(1274,'base',air,None,'lighting','A','lighting.shape.volumetric_beams','environment'),(1274,'base',air,None,'atmosphere','A','atmosphere.medium','environment')]
permissions=[];consumer=[]
for o,rid,k,b,dim,target,prop,category in configs:
 e=entry(J,o,rid,True)
 if b:e,k=selected(J,e,k,b)
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 lock=copy.deepcopy(k);lock['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,lock=selected(J,entry(J,o,rid,True),lock,b)
 assert not n.property_scope_allowed(lock,el['affected_dimensions'],el['affected_properties'],record=el);permissions.append({'ordinal':o,'rid':rid,'dimension':dim,'open_allowed':True,'same_actual_owner_property_anchor_denied':True})
 slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract(category),picked(category),slot,e),(o,rid,'consumer_positive')
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(J,entry(J,o,rid,True),closed,b)
 assert not generator.core_entry_eligible(S,closed,contract(category),picked(category),slot,ec);consumer.append({'ordinal':o,'rid':rid,'dimension':dim,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'open_allowed':True,'closed_whole_E_dimension_denied':True,'binding_display_does_not_assert_positive_role_truth':True})
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':modules(),'synthetic_cases':results,'property_permission_checks':permissions,'actual_own_binding_consumer_checks':consumer,'admission_assertions':48,'property_assertions':20,'consumer_assertions':20,'all_passed':True,'root_acceptance_count':0,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False,'boundary':'Only explicitly authored isolated synthetic cases. Existing binding eligibility being allowed is not positive role certification (1270 historical light_shape remains unsupported). No actual requester core/runtime/final/render/pixels claim; no semantic_reference units.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};p=O/'CHECKS-01270-01275-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(p,c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest(),48,20,20)
