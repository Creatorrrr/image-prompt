"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-02';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());CAT=I['catalog_review']['after'];CH=c.digest(CAT);ROWS=[];CPS=[]
for start in range(1250,1300,5):
 cp=R/('authored/native_11870_formal02_checkpoint_%05d_%05d.json'%(start,start+5));j=json.loads(cp.read_text());ROWS.extend(j['records']);CPS.append({'file':str(cp),'sha256':c.digest(j),'file_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()})
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'}}
def core(roles,values,opendims):
 text='Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}

# Literal independently declared synthetic requests. No values generated from proof P facts.
# Tuple: ordinal, explicit core roles, exact frozen witness facts.
def ep(owner):return ('subject',owner,'entity.presence','entity.presence/v1','present')
def ap(owner,part):return ('subject',owner,'anatomy.'+part+'.presence','anatomy.'+part+'.presence/v1','present')
def pt(owner,value):return ('subject',owner,'props.type','props.type/v1',value)
F=ap('F','face');E=ep('I');SC=ep('S');PE=ep('P')
FIXTURES=[
 (1250,[('primary_face','F')],[F]),
 (1251,[('image','I'),('primary_face','F')],[E,F]),
 (1252,[('primary_face','F')],[F]),
 (1254,[('primary_prop','C')],[pt('C','thread_charm')]),
 (1257,[('scene','S')],[SC]),
 (1259,[('primary_prop','C')],[pt('C','tarot_card_set')]),
 (1260,[('main_subject','P')],[PE]),
 (1261,[('scene','S')],[SC]),
 (1262,[('main_subject','P'),('primary_prop','G')],[PE,pt('G','gavel')]),
 (1263,[('primary_face','F')],[F,ap('F','eyes'),ap('F','mouth')]),
 (1266,[('main_subject','P'),('primary_prop','W'),('scene','S')],[PE,pt('W','magic_wand_prop'),SC]),
 (1268,[('main_subject','P')],[PE,('subject','P','entity.type','entity.type/v1','human')]),
 (1269,[('primary_face','F')],[F,ap('F','mouth'),ap('F','lips')]),
 (1270,[('light_source','L'),('image','I')],[('lighting','L','lighting.source.type','lighting.source.type/v1','fairy_lights'),E]),
 (1271,[('primary_prop','Q'),('primary_hands','H')],[pt('Q','polaroid_print_set'),('body_geometry','H','body.part.presence','body.part.presence/v1','hand')]),
 (1274,[('light_receiver','A'),('scene','S')],[('atmosphere','A','air.presence','air.presence/v1','air_volume'),SC]),
 (1276,[('recording_camera','K'),('image','I'),('primary_prop','R')],[ep('K'),E,pt('R','railing')]),
 (1277,[('main_subject','P')],[PE]),
 (1279,[('scene','S')],[SC]),
 (1281,[('scene','S')],[SC]),
 (1282,[('scene','S')],[SC]),
 (1283,[('recording_camera','K'),('image','I'),('secondary_subject','C'),('scene','S')],[ep('K'),E,('subject','C','entity.type','entity.type/v1','crowd'),SC]),
 (1288,[('recording_camera','K'),('image','I'),('main_subject','P')],[ep('K'),E,PE]),
 (1289,[('scene','S')],[SC]),
 (1290,[('scene','S')],[SC]),
 (1291,[('main_subject','P')],[PE]),
 (1292,[('primary_prop','C')],[pt('C','paper_crane')]),
 (1293,[('primary_hair','H')],[ap('H','hair')]),
 (1294,[('scene','S')],[SC]),
 (1297,[('primary_prop','O')],[ep('O')]),
 (1298,[('primary_prop','B')],[pt('B','florist_delivery_box')])]
assert [x['ordinal'] for x in ROWS]==list(range(1250,1300))
assert [x['ordinal'] for x in ROWS if x['proof']]==[x[0] for x in FIXTURES]

import prompt_generator as generator
# Open scopes are declared literal fixture requests; protected selections remain protected.
CASES=[(1263,['expression','character_response'],'human',True,'expression_and_character_contrast_are_actual_E'),(1269,['expression'],'human',True,'pursed_lips_actual_expression_only'),(1268,['appearance'],'human',False,'subject_presentation_effect_kept_subject_locked'),(1283,['camera','composition'],'human',False,'concert_context_is_actual_event_effect_locked'),(1292,['role'],'human',False,'signal_token_is_actual_concept_effect_locked'),(1298,[],'human',False,'cover_identity_is_actual_concept_effect_locked'),(1297,['composition','style'],'object',True,'apparent_floating_staging_actual_style_and_composition'),(1274,['lighting','atmosphere'],'human',True,'air_presence_frozen_property_but_medium_and_beams_open'),(1288,['camera'],'human',True,'panning_blur_and_image_sharpness_no_focal_plane')]
results=[]
for ordinal,opendims,category,expected,label in CASES:
 row=next(x for x in ROWS if x['ordinal']==ordinal);_,roles,values=next(x for x in FIXTURES if x[0]==ordinal);k=core(roles,values,opendims)
 if ordinal==1274:k['intent_lock']['semantic_anchors']=[{'dimension':'atmosphere','target':'A','property':'air.presence'}]
 contract={'subject_category':category,'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':[]}};picked={'subject':{'kind':[category],'tags':[category]}}
 rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;entry=c.entry(S,row['candidate_id'],realization_id='base');full=copy.deepcopy(entry);full.pop('_semantic_evidence_guard');short=copy.deepcopy(entry);short.pop('role_evidence',None)
 for view,en in [('full',full),('compact',short)]:
  result=generator.core_entry_eligible(S,k,contract,picked,'',en);assert result==expected,(ordinal,label,view,result)
  results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expected,'actual_full_consumer_eligible':result,'core_sha256':c.digest(k),'entry_sha256':c.digest(en)})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None) and (name.startswith('photo_') or name=='prompt_generator' or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal02_effect_consumption_checks.json';assert not O.exists();out={'schema':'photo-native-explicit-fixture-full-consumer-boundary/v1','task_name':'/root/review_11870_12250','input_sha256':c.digest(I),'frozen_generation':G.name,'all_late_production_modules_inside_frozen_generation':True,'module_paths_sha256':mods,'full_consumer_assertions_passed':len(results),'results':results,'source_proofs_changed':False,'actual_input_changed':False,'source_or_core_retrofit':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'actual_request_core_freeze_or_runtime_retrieval_or_final_render_or_pixels_or_operating_checks':False,'boundary':'Actual full consumer on literal isolated test requests only. Contextual roles do not erase locked event/concept/subject effects. No requester core refreeze, corpus deployment or final/pixel claim.'};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print(len(results),'full/compact full consumer checks passed')
