"""Controlled explicit primitive fixtures; no requester core or inferred source facts."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.load(open(D/'INPUT.json'));S=json.load(gzip.open(I['current_snapshot']['file'],'rt'));cp=R/'authored/native_11870_formal03_checkpoint_01255_01260.json';J=json.load(open(cp))
def core(role,owner,prop,typ,value,open_dims):
 text='Controlled independently declared scene S or tarot-card set T as explicitly chosen for this primitive test.'
 def assertion(aid,kind,**axes):return {'assertion_id':aid,'dimension':'subject','polarity':'required','source_span_ids':['fixture'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':text}}
 rows=[assertion('owner','owner',owner=owner,owner_kind='entity'),assertion('role','role',role=role,owner=owner),assertion('fact','fact',owner=owner,property=prop,value_type=typ,value=value)]
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':open_dims,'semantic_anchors':[]}}
scene=core('scene','scene_S','entity.presence','entity.presence/v1','present',['atmosphere']);cards=core('primary_prop','cards_T','props.type','props.type/v1','tarot_card_set',['role'])
def without(k):z=copy.deepcopy(k);z['semantic_assertions']=z['semantic_assertions'][:2];return z
wrong=copy.deepcopy(cards);wrong['semantic_assertions'][2]['axes']['value']='ordinary_card_set';generic=copy.deepcopy(cards);generic['semantic_assertions'][2]['axes'].update(property='entity.presence',value_type='entity.presence/v1',value='present')
cases=[(1257,'scene_exact',scene,True),(1257,'scene_role_only',without(scene),False),(1259,'tarot_set_exact',cards,True),(1259,'set_role_only',without(cards),False),(1259,'wrong_specific_set',wrong,False),(1259,'generic_presence_not_tarot_identity',generic,False)];results=[];entries={}
for ordinal,label,k,expect in cases:
 r=next(x for x in J['records']if x['ordinal']==ordinal);rec=copy.deepcopy(r['source_after']);rec['content']['role_evidence']=r['proof'];S['candidates'][r['candidate_id']]=rec;e=c.entry(S,r['candidate_id'],realization_id='base');entries[ordinal]=e
 full=copy.deepcopy(e);full.pop('_semantic_evidence_guard');compact=copy.deepcopy(e);compact.pop('role_evidence',None)
 for view,x in [('full',full),('compact',compact)]:
  actual=n.admission(x,k);assert actual['allowed']==expect,(ordinal,label,view,actual);results.append({'ordinal':ordinal,'case':label,'view':view,'expected':expect,'admission':actual,'core_sha256':c.digest(k)})
import prompt_generator as generator
permissions=[]
for ordinal,k,dim,owner,prop in [(1257,scene,'atmosphere','scene_S','weather.precipitation'),(1259,cards,'role','cards_T','prop.state')]:
 e=entries[ordinal];assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 z=copy.deepcopy(k);z['intent_lock']['semantic_anchors']=[{'dimension':dim,'target':owner,'property':prop}];assert not n.property_scope_allowed(z,e['affected_dimensions'],e['affected_properties'],record=e)
 contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}};assert generator.core_entry_eligible(S,k,contract,picked,'',e)
 z=copy.deepcopy(k);z['intent_lock']['open_dimensions'].remove(dim);z['intent_lock']['locked_dimensions'].append(dim);assert not generator.core_entry_eligible(S,z,contract,picked,'',e);permissions.append({'ordinal':ordinal,'property_open_pass':True,'same_actual_property_anchor_deny':True,'full_consumer_open_pass':True,'full_consumer_closed_dimension_deny':True})
mods={}
for name,m in sys.modules.items():
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','source_checkpoint':{'file':str(cp),'sha256':c.digest(J)},'input_sha256':c.digest(I),'frozen_generation':G.name,'all_late_production_modules_inside_frozen_generation':True,'module_paths_sha256':mods,'synthetic_cases':results,'permissions':permissions,'synthetic_full_compact_admission_assertions_passed':len(results),'property_scope_assertions_passed':4,'full_consumer_assertions_passed':4,'root_acceptance':0,'actual_request_core_freeze_runtime_or_final_render':False,'os_network_denied':True,'all_provider_keys_absent':True,'boundary':'Controlled manually declared literal synthetic fixtures only; no actual request core was generated, frozen or retrofitted; no whole-corpus/batch verification, runtime retrieval, pixels or operating approval.'};p=R/'authored/native_11870_formal03_checks_01255_01260_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(p,c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest());print('12admission+4property+4consumer isolated assertions passed')
