"""Manually specified independent synthetic witnesses. Never an actual requester core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-05';D=R/'native-inputs/prepared/review11870-01250-01300-05';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import prompt_generator as generator
J=json.loads((O/'CHECKPOINT-01250-01255-v1.json').read_text());I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
TEXT='Synthetic independent request declares an existing face F at primary_face and image I at image when applicable; an existing thread charm C at primary_prop when applicable; or three distinct existing entities participant A, participant B and counter K, with exact counter type, independently and explicitly selected. No candidate supplied these witnesses.'
def assertion(aid,kind,dim='subject',**axes):return {'assertion_id':aid,'dimension':dim,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dim],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}}
def core(owners,roles,values,relations,opendims):
 rows=[assertion('o'+str(j),'owner',owner=x,owner_kind='entity')for j,x in enumerate(owners)]
 rows += [assertion('r'+str(j),'role',owner=x,role=role)for j,(role,x)in enumerate(roles)]
 rows += [assertion('f'+str(j),'fact',d,owner=x,property=p,value_type=t,value=v)for j,(d,x,p,t,v)in enumerate(values)]
 rows += [assertion('rel'+str(j),kind,left=l,right=r)for j,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':TEXT}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
faceval=('subject','F','anatomy.face.presence','anatomy.face.presence/v1','present')
face=core(['F'],[('primary_face','F')],[faceval],[],['expression'])
imageface=core(['I','F'],[('image','I'),('primary_face','F')],[('subject','I','entity.presence','entity.presence/v1','present'),faceval],[],['composition','framing'])
charm=core(['C'],[('primary_prop','C')],[('subject','C','props.type','props.type/v1','thread_charm')],[],['color','role'])
counter=core(['A','B','K'],[],[('subject','A','entity.presence','entity.presence/v1','present'),('subject','B','entity.presence','entity.presence/v1','present'),('subject','K','props.type','props.type/v1','counter'),('subject','K','entity.presence','entity.presence/v1','present')],[('disjoint','A','B'),('disjoint','K','A'),('disjoint','K','B')],['composition','relationship'])
def remove_fact(k,p,owner=None):
 z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']=='fact'and x['axes']['property']==p and(owner is None or x['axes']['owner']==owner))];return z
def change_fact(k,p,field,value):
 z=copy.deepcopy(k);a=next(x for x in z['semantic_assertions']if x['axes'].get('property')==p);(a if field=='dimension'else a['axes'])[field]=value;return z
def entry(ordinal,binding=False):
 row=next(x for x in J['records']if x['ordinal']==ordinal);s=copy.deepcopy(row['source_after']);s['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=s
 bids=[bid for bid,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']]
 return c.entry(S,row['candidate_id'],bids[0]if binding else None,realization_id='base')
def selected(e,k,bindings):
 k=copy.deepcopy(k);k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['candidate_id']==e['id']);graph=n.frozen_witnesses(k)['graph'];z=copy.deepcopy(e);z['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':a}for t,a in bindings]}]};return z,k
COUNTER_BINDINGS=[('counter','K'),('participant_a','A'),('participant_b','B')]
ce,ck=selected(entry(1253),counter,COUNTER_BINDINGS)
cases=[(1250,'neutral_face',entry(1250),face,True),(1250,'missing_face',entry(1250),remove_fact(face,'anatomy.face.presence'),False),(1250,'obsolete_namespace',entry(1250),change_fact(change_fact(face,'anatomy.face.presence','property','face.presence'),'face.presence','value_type','face.presence/v1'),False),(1250,'wrong_dimension',entry(1250),change_fact(face,'anatomy.face.presence','dimension','appearance'),False),(1251,'image_and_face',entry(1251),imageface,True),(1251,'missing_image',entry(1251),remove_fact(imageface,'entity.presence'),False),(1251,'missing_face',entry(1251),remove_fact(imageface,'anatomy.face.presence'),False),(1252,'neutral_face',entry(1252),face,True),(1252,'missing_face',entry(1252),remove_fact(face,'anatomy.face.presence'),False),(1254,'exact_thread_charm',entry(1254),charm,True),(1254,'missing_precise_type',entry(1254),remove_fact(charm,'props.type'),False),(1254,'ordinary_thread_is_not_charm',entry(1254),change_fact(charm,'props.type','value','ordinary_thread'),False),(1253,'all_three_explicit_selected_scopes',ce,ck,True),(1253,'selection_missing',entry(1253),counter,False)]
for left,right in [('A','B'),('K','A'),('K','B')]:
 k=copy.deepcopy(counter);k['semantic_assertions']=[x for x in k['semantic_assertions']if not(x['axes']['kind']=='disjoint'and x['axes']['left']==left and x['axes']['right']==right)];e,k=selected(entry(1253),k,COUNTER_BINDINGS);cases.append((1253,'missing_disjoint_'+left+'_'+right,e,k,False))
for label,k in [('counter_type_missing',remove_fact(counter,'props.type')),('wrong_counter_type',change_fact(counter,'props.type','value','untyped_surface')),('counter_presence_missing',remove_fact(counter,'entity.presence','K')),('participant_A_missing',remove_fact(counter,'entity.presence','A')),('participant_B_missing',remove_fact(counter,'entity.presence','B'))]:
 e,k=selected(entry(1253),k,COUNTER_BINDINGS);cases.append((1253,label,e,k,False))
e,k=selected(entry(1253),counter,[('counter','K'),('participant_a','A'),('participant_b','A')]);cases.append((1253,'participants_aliased',e,k,False))
results=[]
for ordinal,label,e,k,expect in cases:
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==expect,(ordinal,label,view,got);results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'result':got,'core_sha256':c.digest(k)})
# These tests consume actual own binding guards separately from source proof guards.
consumer=[];permissions=[]
configs=[(1250,face,'expression','F','expression.face'),(1251,imageface,'framing','I','framing.shot_scale'),(1252,face,'expression','F','expression.face'),(1253,counter,'relationship','A','relationship.distance.formal_reading'),(1254,charm,'color','C','color.local')]
contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
for ordinal,k,dim,target,prop in configs:
 e=entry(ordinal,True)
 if ordinal==1253:e,k=selected(e,k,COUNTER_BINDINGS)
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop})
 el=e
 if ordinal==1253:el,locked=selected(entry(ordinal,True),locked,COUNTER_BINDINGS)
 assert not n.property_scope_allowed(locked,el['affected_dimensions'],el['affected_properties'],record=el)
 permissions.append({'ordinal':ordinal,'open_allowed':True,'actual_owner_property_anchor_denied':True})
 slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract,picked,slot,e),(ordinal,'positiveconsumer')
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if ordinal==1253:ec,closed=selected(entry(ordinal,True),closed,COUNTER_BINDINGS)
 assert not generator.core_entry_eligible(S,closed,contract,picked,slot,ec)
 consumer.append({'ordinal':ordinal,'actual_binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'all_whole_effects_open_allowed':True,'closed_whole_effect_dimension_denied':True})
# Source human remains conjunctive with the old expression human/animal display gate.
for ordinal in [1250,1252]:
 e=entry(ordinal,True);animal_contract={'subject_category':'animal','adult_allowed':False,'intent_constraints':{'subject_categories':['animal'],'domains':[]}};animal_picked={'subject':{'kind':['animal'],'tags':['animal']}};assert not generator.core_entry_eligible(S,face,animal_contract,animal_picked,e['_presentation_role'],e);consumer.append({'ordinal':ordinal,'actual_binding_id':e['binding_id'],'old_animal_display_permission_does_not_waive_source_human':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permissions,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':len(permissions)*2,'consumer_assertions':12,'all_passed':True,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False,'root_acceptance_count':0,'boundary':'Manually declared isolated synthetic independent witness cases. Exact v3 caller-selected owners, v2 three disjoint source-target guards, custom counter/charm type, neutral atomic presence, all whole effects and actual historical binding consumer checked. This is not an actual requester core or final runtime proof. Exact source-local partial references on1253 are retained and validated; no reference supplies facts or permissions. Historical fixture literals reused after direct inspection, not actual requester cores.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};p=O/'CHECKS-01250-01255-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(p,c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest(),len(results),10,12)
