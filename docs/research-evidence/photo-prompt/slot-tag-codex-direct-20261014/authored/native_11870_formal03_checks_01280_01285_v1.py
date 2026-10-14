"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01280_01285.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independent isolated fixture declares scene S, camera C, image I and crowd G only when listed; concept and event remain locked.'}}
def core(roles,values,opendims):
 text='Independent isolated fixture declares scene S, camera C, image I and crowd G only when listed; concept and event remain locked.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
ghost=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['setting'])
shore=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['setting','timing'])
mood=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['atmosphere'])
concert=core([('recording_camera','camera_C'),('image','image_I'),('secondary_subject','crowd_G'),('scene','scene_S')],[('subject','camera_C','entity.presence','entity.presence/v1','present'),('subject','image_I','entity.presence','entity.presence/v1','present'),('subject','scene_S','entity.presence','entity.presence/v1','present'),('subject','crowd_G','entity.type','entity.type/v1','crowd')],['camera','composition'])
def removed(k,p,owner=None):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p and(owner is None or x['axes']['owner']==owner))];return z
wrong=copy.deepcopy(concert);next(x for x in wrong['semantic_assertions']if x['axes'].get('property')=='entity.type')['axes']['value']='one_person'
def entry(ordinal):
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;return c.entry(S,row['candidate_id'],realization_id='base')
cases=[(1280,'scene_only_no_ghost_P_required',ghost,True),(1280,'scene_role_only',removed(ghost,'entity.presence'),False),(1281,'scene_independent',shore,True),(1281,'no_scene_P',removed(shore,'entity.presence'),False),(1282,'scene_independent',mood,True),(1282,'no_scene_P',removed(mood,'entity.presence'),False),(1283,'exact_independent_camera_image_crowd_scene',concert,True),(1283,'missing_crowd_type',removed(concert,'entity.type'),False),(1283,'one_person_not_crowd',wrong,False),(1283,'missing_scene',removed(concert,'entity.presence','scene_S'),False)]
results=[]
for ordinal,label,k,expect in cases:
 e=entry(ordinal);full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for v,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,v,result);results.append({'ordinal':ordinal,'case':label,'view':v,'expected':expect,'result':result,'core_sha256':c.digest(k)})
import prompt_generator as generator
permissions=[];consumers=[]
for ordinal,k,dim,target,prop in [(1281,shore,'timing','scene_S','timing.season'),(1282,mood,'atmosphere','scene_S','mood.atmosphere')]:
 e=entry(ordinal);assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 anchored=copy.deepcopy(k);anchored['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});assert not n.property_scope_allowed(anchored,e['affected_dimensions'],e['affected_properties'],record=e);permissions.append({'ordinal':ordinal,'open_allowed':True,'same_owner_property_anchor_denied':True})
 contract={'subject_category':'environment','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['environment'],'domains':[]}};picked={'subject':{'kind':['environment'],'tags':['environment']}};assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);assert not generator.core_entry_eligible(S,closed,contract,picked,'',e);consumers.append({'ordinal':ordinal,'same_fixture_open_allowed':True,'closed_actual_effect_denied':True})
for ordinal,k,locked_dim in [(1280,ghost,'concept'),(1283,concert,'event')]:
 e=entry(ordinal);contract={'subject_category':'environment','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['environment'],'domains':[]}};picked={'subject':{'kind':['environment'],'tags':['environment']}};assert locked_dim in k['intent_lock']['locked_dimensions']and locked_dim not in k['intent_lock']['open_dimensions'];assert not generator.core_entry_eligible(S,k,contract,picked,'',e);consumers.append({'ordinal':ordinal,'typed_admission_only':True,'required_locked_actual_effect_denied':locked_dim,'locked_dimension_not_opened_for_test':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01280_01285_v1.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permissions,'consumer_checks':consumers,'synthetic_admission_assertions':20,'property_assertions':4,'consumer_assertions':6,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Only isolated literal primitive request fixtures. Actual concept1280/event1283 retain source meaning and remain locked, typed admission does not prove final eligibility. Original/new binding policies not all tested. No runtime/corefreeze/final/render/pixels or operating approval.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('20 admission+4 property+6 consumer assertions passed')
