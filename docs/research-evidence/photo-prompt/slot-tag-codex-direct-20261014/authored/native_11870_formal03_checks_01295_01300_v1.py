"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));cp=R/'authored/native_11870_formal03_checkpoint_01295_01300.json';J=json.loads(cp.read_text())
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independent isolated fixture declares existing object O and florist-delivery box B only where stated. Concept stays locked.'}}
def core(roles,values,opendims):
 text='Independent isolated fixture declares existing object O and florist-delivery box B only where stated. Concept stays locked.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
obj=core([('primary_prop','object_O')],[('subject','object_O','entity.presence','entity.presence/v1','present')],['composition','style'])
box=core([('primary_prop','box_B')],[('subject','box_B','props.type','props.type/v1','florist_delivery_box')],['appearance'])
def removed(k,p):z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p)];return z
wrongbox=copy.deepcopy(box);next(x for x in wrongbox['semantic_assertions']if x['axes'].get('property')=='props.type')['axes']['value']='ordinary_box'
def entry(ordinal):
 row=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;return c.entry(S,row['candidate_id'],realization_id='base')
cases=[(1297,'independent_existing_object',obj,True),(1297,'prop_role_only',removed(obj,'entity.presence'),False),(1298,'precise_florist_box',box,True),(1298,'prop_role_only',removed(box,'props.type'),False),(1298,'ordinary_box_not_precise_type',wrongbox,False)]
results=[]
for ordinal,label,k,expect in cases:
 e=entry(ordinal);full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for v,en in [('full',full),('compact',compact)]:
  result=n.admission(en,k);assert result['allowed']==expect,(ordinal,label,v,result);results.append({'ordinal':ordinal,'case':label,'view':v,'expected':expect,'result':result,'core_sha256':c.digest(k)})
import prompt_generator as generator
permissions=[];consumer=[];e=entry(1297);assert n.property_scope_allowed(obj,e['affected_dimensions'],e['affected_properties'],record=e)
anchored=copy.deepcopy(obj);anchored['intent_lock']['semantic_anchors'].append({'dimension':'style','target':'object_O','property':'presentation.staging'});assert not n.property_scope_allowed(anchored,e['affected_dimensions'],e['affected_properties'],record=e);permissions.append({'ordinal':1297,'open_allowed':True,'selected_staging_property_anchor_denied':True})
contract={'subject_category':'object','domains':['product'],'adult_allowed':False,'intent_constraints':{'subject_categories':['object'],'domains':['product']}};picked={'subject':{'kind':['object'],'tags':['product']}};assert generator.core_entry_eligible(S,obj,contract,picked,'',e);consumer.append({'ordinal':1297,'object_product_original_guard_open':True})
for dim in ['composition','style']:
 closed=copy.deepcopy(obj);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);assert not generator.core_entry_eligible(S,closed,contract,picked,'',e);consumer.append({'ordinal':1297,'closed_actual_effect_dimension_denied':dim})
human={'subject_category':'human','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};hp={'subject':{'kind':['human'],'tags':['human']}};assert not generator.core_entry_eligible(S,obj,human,hp,'',e);consumer.append({'ordinal':1297,'original_object_product_food_source_guard_denies_human_only':True})
e=entry(1298);assert not generator.core_entry_eligible(S,box,human,hp,'',e);consumer.append({'ordinal':1298,'typed_admission_positive_but_concept_locked_consumer_denied':True,'concept_not_opened_for_test':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal03_checks_01295_01300_v1.json';assert not O.exists();out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'frozen_generation':G.name,'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permissions,'consumer_checks':consumer,'synthetic_admission_assertions':10,'property_assertions':2,'consumer_assertions':5,'normal_independent_core_freeze_runtime_final_pixels_or_operating_checks':False,'boundary':'Only isolated literal primitive fixtures.1297 static staged presentation is real style E, original object/product/food source guard retained.1298 concept remains locked. No actual requester corefreeze/retrieval/runtime/final/render/allbinding/operating success.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print('10 admission+2 property+5 consumer assertions passed')
