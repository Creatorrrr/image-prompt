"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01265_01270.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Synthetic independent request declares actual saltwater surface S and other surface O, human person P, and face F with mouth and lips only where individually stated.'}}
def core(roles,values,opendims):
 text='Synthetic independent request declares actual saltwater surface S and other surface O, human person P, and face F with mouth and lips only where individually stated.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
surface=core([('foreground_surface','surface_O'),('background_surface','surface_S')],[('subject','surface_S','entity.presence','entity.presence/v1','present'),('material','surface_S','surface.material','surface.material/v1','saltwater'),('subject','surface_O','entity.presence','entity.presence/v1','present'),('material','surface_O','surface.material','surface.material/v1','freshwater')],['material'])
surface['intent_lock']['semantic_anchors']=[{'dimension':'material','target':'surface_S','property':'surface.material'},{'dimension':'material','target':'surface_O','property':'surface.material'}]
person=core([('main_subject','person_P')],[('subject','person_P','entity.presence','entity.presence/v1','present'),('subject','person_P','entity.type','entity.type/v1','human')],['appearance'])
vals=[('subject','face_F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','face_F','anatomy.mouth.presence','anatomy.mouth.presence/v1','present'),('subject','face_F','anatomy.lips.presence','anatomy.lips.presence/v1','present')]
face=core([('primary_face','face_F')],vals,['expression'])
def removed(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p)];return z
wronghuman=copy.deepcopy(person);next(x for x in wronghuman['semantic_assertions']if x['axes'].get('property')=='entity.type')['axes']['value']='literal_doll'
other=core([('primary_face','face_F'),('secondary_face','face_M')],[vals[0],vals[1],('subject','face_M','anatomy.lips.presence','anatomy.lips.presence/v1','present')],['expression'])
array=core([('primary_face','face_F')],[vals[0],('body_geometry','face_F','body.parts','body.parts/v1',['mouth','lips'])],['expression'])
extra=core([('primary_face','face_F')],vals+[('subject','face_F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present')],['expression'])
# These canonical digests bind only deliberately isolated fixture objects; no request core freeze is invoked.
def entry(ordinal):
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;return c.entry(S,row['candidate_id'],realization_id='base')
def selected(e,k,owner):
 k=copy.deepcopy(k);k['canonical_sha256']=c.digest(k);proof=next(x['proof']for x in J['records']if x['candidate_id']==e['id']);graph=n.frozen_witnesses(k)['graph'];x=copy.deepcopy(e);x['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':proof['meaning_sha256'],'qualification_sha256':c.digest(proof),'bindings':[{'target':'surface','owner_id':owner}]}]};return x,k
surfaceentry=entry(1265);chosen,chosen_core=selected(surfaceentry,surface,'surface_S');wrongchoice,wrong_core=selected(surfaceentry,surface,'surface_O');nopresence=removed(surface,'entity.presence');noPentry,noPcore=selected(surfaceentry,nopresence,'surface_S');nochemical=removed(surface,'surface.material');noMentry,noMcore=selected(surfaceentry,nochemical,'surface_S')
cases=[(1265,'explicit_actual_background_saltwater_owner',chosen,chosen_core,True),(1265,'missing_explicit_selection',surfaceentry,surface,False),(1265,'wrong_chosen_freshwater',wrongchoice,wrong_core,False),(1265,'precise_saltwater_without_presence',noPentry,noPcore,False),(1265,'presence_without_precise_saltwater',noMentry,noMcore,False),(1268,'exact_human_type',entry(1268),person,True),(1268,'generic_presence_not_human',entry(1268),removed(person,'entity.type'),False),(1268,'literal_doll_not_human',entry(1268),wronghuman,False),(1269,'exact_atomic',entry(1269),face,True),(1269,'missing_lips',entry(1269),removed(face,'anatomy.lips.presence'),False),(1269,'missing_mouth',entry(1269),removed(face,'anatomy.mouth.presence'),False),(1269,'missing_face',entry(1269),removed(face,'anatomy.face.presence'),False),(1269,'wrong_owner_lips',entry(1269),other,False),(1269,'array_not_subset',entry(1269),array,False),(1269,'extra_atomic_not_exhaustive',entry(1269),extra,True)]
results=[]
for ordinal,label,e,k,expect in cases:
 full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for view,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,view,result);results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'result':result,'core_sha256':c.digest(k)})
import prompt_generator as generator
permission=[];consumer=[]
for ordinal,e,k,dim,target,prop in [(1265,chosen,chosen_core,'material','surface_S','surface.optical_response'),(1269,entry(1269),face,'expression','face_F','expression.mouth')]:
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors']=[{'dimension':dim,'target':target,'property':prop}]
 if ordinal==1265:
  locked.pop('canonical_sha256');e_locked,locked=selected(surfaceentry,locked,'surface_S')
 else:e_locked=e
 assert not n.property_scope_allowed(locked,e_locked['affected_dimensions'],e_locked['affected_properties'],record=e_locked);permission.append({'ordinal':ordinal,'open_allowed':True,'same_actual_owner_property_anchor_denied':True})
 contract={'subject_category':'environment'if ordinal==1265 else'human','adult_allowed':False,'intent_constraints':{'subject_categories':['environment'if ordinal==1265 else'human'],'domains':[]}};picked={'subject':{'kind':['environment'if ordinal==1265 else'human'],'tags':['environment'if ordinal==1265 else'human']}}
 assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim)
 if ordinal==1265:closed.pop('canonical_sha256');eclosed,closed=selected(surfaceentry,closed,'surface_S')
 else:eclosed=e
 assert not generator.core_entry_eligible(S,closed,contract,picked,'',eclosed);consumer.append({'ordinal':ordinal,'same_fixture_open_allowed':True,'closed_actual_effect_denied':True})
e=entry(1268);contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
assert not n.property_scope_allowed(person,e['affected_dimensions'],e['affected_properties'],record=e)
assert not generator.core_entry_eligible(S,person,contract,picked,'',e)
consumer.append({'ordinal':1268,'typed_admission_positive':True,'ordinary_subject_locked_property_scope_denied':True,'ordinary_subject_locked_full_consumer_denied':True,'subject_not_opened_for_test':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01265_01270_v3.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permission,'consumer_checks':consumer,'synthetic_admission_assertions':len(results),'property_assertions':5,'consumer_assertions':5,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Isolated manually declared fixtures only. Selector fixture canonical digest is structural binding, no real request freeze. Explicit caller chosen background owner checked; no automatic foreground.1268 exact human admission is not subject-locked eligibility. Root acceptance0.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('30 admission+5 property+5 consumer assertions passed')
