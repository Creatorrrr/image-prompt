"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01270_01275.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independent isolated fixture declares fairy lights L, image I, leather surface S and air volume A in scene C only when individually listed.'}}
def core(roles,values,opendims):
 text='Independent isolated fixture declares fairy lights L, image I, leather surface S and air volume A in scene C only when individually listed.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
bokeh=core([('light_source','lights_L'),('image','image_I')],[('lighting','lights_L','lighting.source.type','lighting.source.type/v1','fairy_lights'),('subject','image_I','entity.presence','entity.presence/v1','present')],['camera']);bokeh['intent_lock']['locked_dimensions'].append('lighting')
leather=core([('foreground_surface','surface_O'),('background_surface','surface_S')],[('subject','surface_S','entity.presence','entity.presence/v1','present'),('material','surface_S','surface.material','surface.material/v1','leather'),('subject','surface_O','entity.presence','entity.presence/v1','present'),('material','surface_O','surface.material','surface.material/v1','vinyl')],['material']);leather['intent_lock']['semantic_anchors']=[{'dimension':'material','target':'surface_S','property':'surface.material'},{'dimension':'material','target':'surface_O','property':'surface.material'}]
air=core([('light_receiver','air_A'),('scene','scene_C')],[('atmosphere','air_A','air.presence','air.presence/v1','air_volume'),('subject','scene_C','entity.presence','entity.presence/v1','present')],['atmosphere','lighting']);air['intent_lock']['semantic_anchors']=[{'dimension':'atmosphere','target':'air_A','property':'air.presence'}]
def removed(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p)];return z
def changed(k,p,v):z=copy.deepcopy(k);next(x for x in z['semantic_assertions']if x['axes'].get('property')==p)['axes']['value']=v;return z
def entry(ordinal):
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;return c.entry(S,row['candidate_id'],realization_id='base')
def selected(e,k,owner):
 k=copy.deepcopy(k);k['canonical_sha256']=c.digest(k);proof=next(x['proof']for x in J['records']if x['candidate_id']==e['id']);graph=n.frozen_witnesses(k)['graph'];x=copy.deepcopy(e);x['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':proof['meaning_sha256'],'qualification_sha256':c.digest(proof),'bindings':[{'target':'surface','owner_id':owner}]}]};return x,k
le=entry(1272);chosen,chosen_core=selected(le,leather,'surface_S');wrong,wrongcore=selected(le,leather,'surface_O');noexist,noexistcore=selected(le,removed(leather,'entity.presence'),'surface_S');notype,notypecore=selected(le,removed(leather,'surface.material'),'surface_S')
cases=[(1270,'exact_source_and_image',entry(1270),bokeh,True),(1270,'missing_precise_fairy_type',entry(1270),removed(bokeh,'lighting.source.type'),False),(1270,'ordinary_bulb_not_fairy_lights',entry(1270),changed(bokeh,'lighting.source.type','ordinary_bulb'),False),(1270,'missing_image_existence',entry(1270),removed(bokeh,'entity.presence'),False),(1272,'explicit_actual_background_leather',chosen,chosen_core,True),(1272,'no_actual_selection',le,leather,False),(1272,'wrong_vinyl_owner',wrong,wrongcore,False),(1272,'type_without_existence',noexist,noexistcore,False),(1272,'existence_without_leather',notype,notypecore,False),(1274,'exact_air_volume_and_scene',entry(1274),air,True),(1274,'missing_air_type',entry(1274),removed(air,'air.presence'),False),(1274,'generic_entity_not_air_type',entry(1274),core([('light_receiver','air_A'),('scene','scene_C')],[('subject','air_A','entity.presence','entity.presence/v1','present'),('subject','scene_C','entity.presence','entity.presence/v1','present')],['atmosphere','lighting']),False),(1274,'missing_scene',entry(1274),removed(air,'entity.presence'),False)]
results=[]
for ordinal,label,e,k,expect in cases:
 full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for view,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,view,result);results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'result':result,'core_sha256':c.digest(k)})
import prompt_generator as generator
permissions=[];consumers=[]
for ordinal,e,k,dim,target,prop in [(1270,entry(1270),bokeh,'camera','image_I','lens.artifact.bokeh'),(1272,chosen,chosen_core,'material','surface_S','surface.texture'),(1274,entry(1274),air,'lighting','air_A','lighting.shape.volumetric_beams')]:
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 anchored=copy.deepcopy(k);anchored['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop})
 if ordinal==1272:anchored.pop('canonical_sha256');ea,anchored=selected(le,anchored,'surface_S')
 else:ea=e
 assert not n.property_scope_allowed(anchored,ea['affected_dimensions'],ea['affected_properties'],record=ea);permissions.append({'ordinal':ordinal,'unanchored_actual_effect_allowed':True,'same_actual_owner_property_anchor_denied':True})
 contract={'subject_category':'environment','adult_allowed':False,'intent_constraints':{'subject_categories':['environment'],'domains':[]}};picked={'subject':{'kind':['environment'],'tags':['environment']}}
 assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim)
 if ordinal==1272:closed.pop('canonical_sha256');ec,closed=selected(le,closed,'surface_S')
 else:ec=e
 assert not generator.core_entry_eligible(S,closed,contract,picked,'',ec);consumers.append({'ordinal':ordinal,'same_fixture_open_allowed':True,'closed_actual_effect_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01270_01275_v1.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permissions,'consumer_checks':consumers,'synthetic_admission_assertions':26,'property_assertions':6,'consumer_assertions':6,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Actual-source proof checks on manually declared isolated fixtures only. Selector digests bind these test objects, not actual requester freeze. Type P remains frozen via exact source anchors while separate actual E is open. No whole batch/corpus/operating approval.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('26 admission+6 property+6 consumer assertions passed')
