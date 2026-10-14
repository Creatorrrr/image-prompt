"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-02';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal02_checkpoint_01250_01255.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'}}
def core(roles,values,opendims):
 text='Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
face=core([('primary_face','face_F')],[('subject','face_F','anatomy.face.presence','anatomy.face.presence/v1','present')],['expression'])
faceimage=core([('primary_face','face_F'),('image','image_I')],[('subject','face_F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','image_I','entity.presence','entity.presence/v1','present')],['composition','framing'])
charm=core([('primary_prop','charm_C')],[('subject','charm_C','props.type','props.type/v1','thread_charm')],['color','role'])
def removed(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes']['property']==p)];return z
def changed(k,field,val):z=copy.deepcopy(k);x=next(x for x in z['semantic_assertions'] if x['axes']['kind']=='fact');(x if field=='dimension' else x['axes'])[field]=val;return z
cases=[(1250,'common_face_positive',face,True),(1250,'owner_role_only',removed(face,'anatomy.face.presence'),False),(1250,'custom_old_face_namespace',changed(changed(face,'property','face.presence'),'value_type','face.presence/v1'),False),(1250,'historical_appearance_dimension',changed(face,'dimension','appearance'),False),(1251,'common_image_and_face_positive',faceimage,True),(1251,'missing_image_presence',removed(faceimage,'entity.presence'),False),(1251,'missing_face_presence',removed(faceimage,'anatomy.face.presence'),False),(1252,'common_face_positive',face,True),(1252,'no_face_presence',removed(face,'anatomy.face.presence'),False),(1254,'exact_custom_identity_positive',charm,True),(1254,'owner_role_only',removed(charm,'props.type'),False),(1254,'wrong_specific_type',changed(charm,'value','ordinary_thread'),False)]
results=[]
for ordinal,label,k,expect in cases:
 row=next(x for x in J['records'] if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;entry=c.entry(S,row['candidate_id'],realization_id='base');full=copy.deepcopy(entry);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(entry);compact.pop('role_evidence',None)
 for view,e in [('full',full),('compact',compact)]:
  adm=n.admission(e,k);assert adm['allowed']==expect,(ordinal,label,view,adm)
  results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'admission':adm,'core_sha256':c.digest(k)})
# Mutation permission separately; literal same-value/effect assignment still needs open affected dimensions.
locks=[]
for ordinal,k,dim in [(1250,face,'expression'),(1251,faceimage,'framing'),(1252,face,'expression'),(1254,charm,'color')]:
 row=next(x for x in J['records'] if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;e=c.entry(S,row['candidate_id'],realization_id='base')
 allowed=n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e);assert allowed
 locked=copy.deepcopy(k);locked['intent_lock']['open_dimensions'].remove(dim);locked['intent_lock']['locked_dimensions'].append(dim);denied=n.property_scope_allowed(locked,e['affected_dimensions'],e['affected_properties'],record=e);assert not denied
 locks.append({'ordinal':ordinal,'open_actual_effect_dimensions':True,'locked_'+dim+'_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith('photo_') and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,str(p));mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal02_checkpoint_checks_01250_01255.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'input_sha256':c.digest(I),'frozen_generation':G.name,'all_late_production_modules_inside_frozen_generation':True,'module_paths_sha256':mods,'synthetic_cases':results,'effect_dimension_permission_checks':locks,'synthetic_full_compact_admission_assertions_passed':len(results),'effect_permission_assertions_passed':len(locks)*2,'fresh_source_proof_count':4,'pending_count':1,'full50_complete':False,'normal_independent_core_freeze_or_runtime_or_final_checks_performed':False,'boundary':'Controlled manually declared isolated primitive cores only. No production requester core was generated, refrozen or retrofitted. No whole corpus validation, intrinsic old tag guard integration, batch verification, final render audit, runtime retrieval, pixels or operating approval.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('24 full/compact admission assertions +8 effect-permission assertions passed')
