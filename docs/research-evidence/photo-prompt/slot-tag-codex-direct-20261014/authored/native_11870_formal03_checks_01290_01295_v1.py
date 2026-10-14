"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01290_01295.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independent isolated fixture declares scene S, person P, existing paper crane C and owned hair H only where stated. Concept stays locked.'}}
def core(roles,values,opendims):
 text='Independent isolated fixture declares scene S, person P, existing paper crane C and owned hair H only where stated. Concept stays locked.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
weather=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['atmosphere'])
person=core([('main_subject','person_P')],[('subject','person_P','entity.presence','entity.presence/v1','present')],['appearance'])
crane=core([('primary_prop','crane_C')],[('subject','crane_C','props.type','props.type/v1','paper_crane')],['role'])
hair=core([('primary_hair','hair_H')],[('subject','hair_H','anatomy.hair.presence','anatomy.hair.presence/v1','present')],['appearance'])
place=core([('scene','scene_S')],[('subject','scene_S','entity.presence','entity.presence/v1','present')],['setting'])
def removed(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p)];return z
wrongcrane=copy.deepcopy(crane);next(x for x in wrongcrane['semantic_assertions']if x['axes'].get('property')=='props.type')['axes']['value']='living_crane'
wronghair=copy.deepcopy(hair);next(x for x in wronghair['semantic_assertions']if x['axes']['kind']=='fact')['axes']['owner']='person_P';wronghair['semantic_assertions'].append(assertion('other_owner','owner',owner='person_P',owner_kind='entity'))
def entry(ordinal):
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;return c.entry(S,row['candidate_id'],realization_id='base')
cases=[(1290,'scene_presence',weather,True),(1290,'scene_role_only',removed(weather,'entity.presence'),False),(1291,'person_presence',person,True),(1291,'person_role_only',removed(person,'entity.presence'),False),(1292,'precise_paper_crane',crane,True),(1292,'prop_role_only',removed(crane,'props.type'),False),(1292,'living_bird_not_paper_type',wrongcrane,False),(1293,'common_hair_presence',hair,True),(1293,'hair_role_only',removed(hair,'anatomy.hair.presence'),False),(1293,'hair_of_other_owner_not_inherited',wronghair,False),(1294,'scene_presence',place,True),(1294,'scene_role_only',removed(place,'entity.presence'),False)]
results=[]
for ordinal,label,k,expect in cases:
 e=entry(ordinal);full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for v,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,v,result);results.append({'ordinal':ordinal,'case':label,'view':v,'expected':expect,'result':result,'core_sha256':c.digest(k)})
import prompt_generator as generator
permissions=[];consumers=[]
for ordinal,k,dim,target,prop in [(1290,weather,'atmosphere','scene_S','weather.declared'),(1291,person,'appearance','person_P','presentation.style'),(1293,hair,'appearance','hair_H','hair.color'),(1294,place,'setting','scene_S','setting.location')]:
 e=entry(ordinal);assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 anchored=copy.deepcopy(k);anchored['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});assert not n.property_scope_allowed(anchored,e['affected_dimensions'],e['affected_properties'],record=e);permissions.append({'ordinal':ordinal,'open_allowed':True,'same_owner_property_anchor_denied':True})
 contract={'subject_category':'human','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}};assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);assert not generator.core_entry_eligible(S,closed,contract,picked,'',e);consumers.append({'ordinal':ordinal,'same_fixture_open_allowed':True,'closed_actual_effect_denied':True})
e=entry(1292);contract={'subject_category':'human','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}};assert not generator.core_entry_eligible(S,crane,contract,picked,'',e);consumers.append({'ordinal':1292,'typed_admission_positive':True,'concept_E_required_locked_denied':True,'concept_not_opened_for_test':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01290_01295_v1.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permissions,'consumer_checks':consumers,'synthetic_admission_assertions':24,'property_assertions':8,'consumer_assertions':9,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Only isolated literal primitive fixtures.1292 concept effect stays locked, common owned hair does not inherit another owners fact. No all binding policy/global/corefreeze/runtime/final/render/operating success.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('24 admission+8 property+9 consumer assertions passed')
