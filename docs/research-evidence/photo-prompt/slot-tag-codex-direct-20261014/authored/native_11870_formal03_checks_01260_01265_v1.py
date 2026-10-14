"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01260_01265.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Synthetic independent request declares person P, scene S, gavel G and face F with its eyes and mouth only in cases where explicitly listed.'}}
def core(roles,values,opendims):
 text='Synthetic independent request declares person P, scene S, gavel G and face F with its eyes and mouth only in cases where explicitly listed.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
person=core([('main_subject','person_P')],[('subject','person_P','entity.presence','entity.presence/v1','present')],['appearance'])
scene=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['setting'])
gavel=core([('main_subject','person_P'),('primary_prop','gavel_G')],[('subject','person_P','entity.presence','entity.presence/v1','present'),('subject','gavel_G','props.type','props.type/v1','gavel')],['action','pose']);gavel['semantic_assertions'].append(assertion('actual_distinct','disjoint',left='person_P',right='gavel_G'))
facevalues=[('subject','face_F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','face_F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present'),('subject','face_F','anatomy.mouth.presence','anatomy.mouth.presence/v1','present')]
face=core([('primary_face','face_F')],facevalues,['expression','character_response'])
def remove(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p)];return z
nodisjoint=copy.deepcopy(gavel);nodisjoint['semantic_assertions']=[x for x in nodisjoint['semantic_assertions']if x['axes']['kind']!='disjoint']
wrongtype=copy.deepcopy(gavel);next(x for x in wrongtype['semantic_assertions']if x['axes'].get('property')=='props.type')['axes']['value']='hammer'
partof=copy.deepcopy(nodisjoint);partof['semantic_assertions'].append(assertion('part_relation','part_of',part='gavel_G',whole='person_P'))
extra=core([('primary_face','face_F')],facevalues+[('subject','face_F','anatomy.lips.presence','anatomy.lips.presence/v1','present')],['expression','character_response'])
other=core([('primary_face','face_F'),('secondary_face','face_M')],[facevalues[0],('subject','face_M','anatomy.eyes.presence','anatomy.eyes.presence/v1','present'),facevalues[2]],['expression','character_response'])
array=core([('primary_face','face_F')],[facevalues[0],('body_geometry','face_F','body.parts','body.parts/v1',['eyes','mouth'])],['expression','character_response'])
cases=[(1260,'common_person',person,True),(1260,'person_role_only',remove(person,'entity.presence'),False),(1261,'common_scene',scene,True),(1261,'scene_role_only',remove(scene,'entity.presence'),False),(1262,'exact_gavel_and_actual_disjoint',gavel,True),(1262,'roles_without_disjoint',nodisjoint,False),(1262,'part_of_not_disjoint',partof,False),(1262,'hammer_not_precise_gavel',wrongtype,False),(1262,'missing_gavel_P',remove(gavel,'props.type'),False),(1263,'exact_atomic',face,True),(1263,'missing_eyes',remove(face,'anatomy.eyes.presence'),False),(1263,'missing_mouth',remove(face,'anatomy.mouth.presence'),False),(1263,'missing_face',remove(face,'anatomy.face.presence'),False),(1263,'extra_atomic_allowed',extra,True),(1263,'other_owner_eyes_not_inherited',other,False),(1263,'old_array_no_subset_alias',array,False)]
results=[];entries={}
for ordinal,label,k,expect in cases:
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;e=c.entry(S,row['candidate_id'],realization_id='base');entries[ordinal]=e;full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for view,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,view,result);results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'result':result,'core_sha256':c.digest(k)})
# The relation receiver is a manually declared actual effect endpoint, retained in full and compact evidence.
r=next(x for x in J['records']if x['ordinal']==1262);ann=[x for x in r['proof']['facts']if x['property']=='action.announcing'];assert len(ann)==3 and all(x['receivers']==['gavel']and x['value']['value']=='announcing_bid_using_and_holding_same_raised_gavel'for x in ann)
by={}
for row in J['records']:
 if row['proof']:
  for f in row['proof']['facts']:
   if f['mode']=='effect':by.setdefault((row['ordinal'],f['realization_id'],f['target'],f['dimension'],f['property']),set()).add(c.digest([f['value'],f['operation'],sorted(f['receivers'])]))
assert all(len(v)==1 for v in by.values())
import prompt_generator as generator
locks=[];consumer=[]
for ordinal,k,dim,target,prop in [(1260,person,'appearance','person_P','presentation.style'),(1261,scene,'setting','scene_S','setting.location'),(1262,gavel,'action','person_P','action.announcing'),(1263,face,'expression','face_F','expression.face')]:
 e=entries[ordinal];assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 anchored=copy.deepcopy(k);anchored['intent_lock']['semantic_anchors']=[{'dimension':dim,'target':target,'property':prop}];assert not n.property_scope_allowed(anchored,e['affected_dimensions'],e['affected_properties'],record=e);locks.append({'ordinal':ordinal,'open_allowed':True,'same_owner_property_anchor_denied':True})
 contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
 assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 locked=copy.deepcopy(k);locked['intent_lock']['open_dimensions'].remove(dim);locked['intent_lock']['locked_dimensions'].append(dim);assert not generator.core_entry_eligible(S,locked,contract,picked,'',e);consumer.append({'ordinal':ordinal,'same_synthetic_core_open_allowed':True,'actual_effect_dimension_closed_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01260_01265_v1.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'effect_property_permission_checks':locks,'full_core_entry_consumer_checks':consumer,'synthetic_full_compact_admission_assertions_passed':len(results),'effect_property_assertions_passed':len(locks)*2,'full_consumer_assertions_passed':len(consumer)*2,'same_actual_property_effect_consistency':True,'same_announcer_gavel_receiver_preserved':True,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Only manually declared isolated primitive cores. Actual-source proof admission full/compact, exact disjoint and atomic requirements checked; not current reusable request or actual retrieval/final proof. Root acceptance0.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('32 admission +8 property +8 full consumer assertions passed')
