"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-02';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal02_checkpoint_01265_01270.json';J=json.loads(cp.read_text())
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
row=next(x for x in J['records'] if x['ordinal']==1269);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;e=c.entry(S,row['candidate_id'],realization_id='base');full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
roles=[('primary_face','face_F')]
values=[('subject','face_F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','face_F','anatomy.mouth.presence','anatomy.mouth.presence/v1','present'),('subject','face_F','anatomy.lips.presence','anatomy.lips.presence/v1','present')]
valid=core(roles,values,['expression']);missinglips=core(roles,values[:2],['expression']);missingmouth=core(roles,[values[0],values[2]],['expression']);faceonly=core(roles,values[:1],['expression']);extra=core(roles,values+[('subject','face_F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present')],['expression']);wrongowner=core(roles+[('secondary_face','face_M')],[values[0],values[1],('subject','face_M','anatomy.lips.presence','anatomy.lips.presence/v1','present')],['expression']);oldarray=core(roles,[values[0],('body_geometry','face_F','body.parts','body.parts/v1',['mouth','lips'])],['expression']);onlyeyes=core(roles,[values[0],('subject','face_F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present')],['expression'])
cases=[('exact_same_carrier_atomic',valid,True),('mouth_not_lips_entailment',missinglips,False),('lips_not_mouth_entailment',missingmouth,False),('face_does_not_infer_parts',faceonly,False),('extra_unrelated_atomic_not_exhaustive',extra,True),('other_owner_lips_not_inherited',wrongowner,False),('legacy_array_not_subset_alias',oldarray,False),('eyes_not_mouth_or_lips_alias',onlyeyes,False)]
results=[]
for name,k,expected in cases:
 for view,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expected,(name,view,result);results.append({'case':name,'view':view,'expected':expected,'result':result,'core_sha256':c.digest(k)})
# All effect facts with the same actual source address retain identical assignments.
by={}
for fact in row['proof']['facts']:
 if fact['mode']=='effect':by.setdefault((fact['realization_id'],fact['target'],fact['dimension'],fact['property']),set()).add(c.digest({'value':fact['value'],'operation':fact['operation'],'receivers':sorted(fact['receivers'])}))
assert all(len(v)==1 for v in by.values())
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None) and (name.startswith('photo_') or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal02_atomic1269_checks.json';assert not O.exists();out={'schema':'photo-native-actual-source-atomic-carrier-checks/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'ordinal':1269,'source_proof_sha256':c.digest(row['proof']),'atomic_full_compact_assertions_passed':16,'results':results,'same_property_effect_assignment_consistency':True,'module_paths_sha256':mods,'frozen_generation':G.name,'os_network_denied':True,'provider_keys_absent':True,'network_model_calls':0,'normal_request_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Manually declared isolated primitive cores, exact source proof; no array subset/alias/carrier inheritance. Extra atomic facts may coexist but never supply missing required part.'};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest())
