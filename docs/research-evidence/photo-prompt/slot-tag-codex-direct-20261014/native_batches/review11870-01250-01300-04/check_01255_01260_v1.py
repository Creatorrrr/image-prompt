"""Literal independent synthetic cases for five newly read sources and six actual RIDs."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-04';D=R/'native-inputs/prepared/review11870-01250-01300-04';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import prompt_generator as generator
J=json.loads((O/'CHECKPOINT-01255-01260.json').read_text());I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
TEXT='Independent synthetic request: holder H and held object O are existing and distinct. Human gaze carrier G has actual eyes on G, distinct from an existing badge or access card T, selected by its exact independently declared type. Existing scene S. Existing human voltage operator P, voltage tester V and electrical-potential measurement target M; P and V are distinct while M is not assumed distinct from V. Existing tarot-card set C at primary_prop. These are explicitly declared synthetic baseline facts, not actual production requester data.'
def assertion(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}}
def core(owners,roles,values,relations,opendims):
 rows=[assertion('o'+str(j),'owner',owner=x,owner_kind='entity')for j,x in enumerate(owners)]+[assertion('r'+str(j),'role',owner=x,role=role)for j,(role,x)in enumerate(roles)]+[assertion('f'+str(j),'fact',d,owner=x,property=p,value_type=t,value=v)for j,(d,x,p,t,v)in enumerate(values)]+[assertion('rel'+str(j),kind,left=l,right=r)for j,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':TEXT}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}
def presence(x):return('subject',x,'entity.presence','entity.presence/v1','present')
holding=core(['H','O'],[],[presence('H'),presence('O')],[('disjoint','H','O')],['action','composition','role'])
gazevals=[presence('G'),presence('T'),('subject','G','entity.category','entity.category/v1','human'),('subject','G','anatomy.eyes.presence','anatomy.eyes.presence/v1','present')]
badge=core(['G','T'],[],gazevals+[('subject','T','props.type','props.type/v1','badge')],[('disjoint','G','T')],['expression','text'])
card=core(['G','T'],[],gazevals+[('subject','T','props.type','props.type/v1','access_card')],[('disjoint','G','T')],['expression'])
scene=core(['S'],[('scene','S')],[presence('S')],[],['atmosphere'])
voltage=core(['P','V','M'],[],[presence('P'),presence('V'),presence('M'),('subject','P','entity.category','entity.category/v1','human'),('subject','V','props.type','props.type/v1','voltage_tester'),('concept','M','measurement.target_domain','measurement.target_domain/v1','electrical_potential')],[('disjoint','P','V')],['action'])
tarot=core(['C'],[('primary_prop','C')],[('subject','C','props.type','props.type/v1','tarot_card_set')],[],['role'])
def remove(k,kind,prop=None,left=None,right=None):
 z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']==kind and(prop is None or x['axes'].get('property')==prop)and(left is None or x['axes'].get('left')==left)and(right is None or x['axes'].get('right')==right))];return z
def change(k,prop,value):
 z=copy.deepcopy(k);next(x for x in z['semantic_assertions']if x['axes'].get('property')==prop)['axes']['value']=value;return z
def entry(o,rid='base',binding=False):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0]if binding else None,realization_id=rid)
def selected(e,k,bindings):
 k=copy.deepcopy(k);k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['candidate_id']==e['id']);graph=n.frozen_witnesses(k)['graph'];z=copy.deepcopy(e);z['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':e['_realization_id'],'meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':v}for t,v in bindings]}]};return z,k
HB=[('holder','H'),('held_object','O')];GB=[('gaze_owner','G'),('target','T')];VB=[('operator','P'),('tester','V'),('tested_endpoint','M')]
cases=[]
def case(o,label,k,expected,rid='base',bindings=None):
 e=entry(o,rid)
 if bindings is not None:e,k=selected(e,k,bindings)
 cases.append((o,label,e,k,expected))
case(1255,'selected_same_holder_and_object',holding,True,bindings=HB);case(1255,'selection_missing',holding,False);case(1255,'explicit_disjoint_missing',remove(holding,'disjoint'),False,bindings=HB)
case(1256,'badge_without_preblank_text_P',badge,True,'blank_badge',GB);case(1256,'access_card_no_text_permission_needed',card,True,'access_card',GB);case(1256,'badge_branch_wrong_card_type',card,False,'blank_badge',GB);case(1256,'card_branch_wrong_badge_type',badge,False,'access_card',GB)
for rid,k in [('blank_badge',badge),('access_card',card)]:
 case(1256,rid+'_missing_eyes',remove(k,'fact','anatomy.eyes.presence'),False,rid,GB);case(1256,rid+'_missing_human_category',remove(k,'fact','entity.category'),False,rid,GB);case(1256,rid+'_missing_distinctness',remove(k,'disjoint'),False,rid,GB);case(1256,rid+'_missing_choice',k,False,rid)
case(1257,'declared_scene_no_umbrella_P',scene,True);case(1257,'missing_scene_presence',remove(scene,'fact','entity.presence'),False)
case(1258,'human_same_tester_and_selected_target',voltage,True,bindings=VB);case(1258,'measurement_domain_missing',remove(voltage,'fact','measurement.target_domain'),False,bindings=VB);case(1258,'wrong_measurement_domain',change(voltage,'measurement.target_domain','temperature'),False,bindings=VB);case(1258,'precise_tester_missing',remove(voltage,'fact','props.type'),False,bindings=VB);case(1258,'human_category_missing',remove(voltage,'fact','entity.category'),False,bindings=VB);case(1258,'operator_tester_disjoint_missing',remove(voltage,'disjoint'),False,bindings=VB)
# Independently declared measurement target may coincide with the tester: no invented extra disjointness.
selftest=core(['P','V'],[],[presence('P'),presence('V'),('subject','P','entity.category','entity.category/v1','human'),('subject','V','props.type','props.type/v1','voltage_tester'),('concept','V','measurement.target_domain','measurement.target_domain/v1','electrical_potential')],[('disjoint','P','V')],['action']);case(1258,'target_same_as_tester_explicitly_declared',selftest,True,bindings=[('operator','P'),('tester','V'),('tested_endpoint','V')])
case(1259,'precise_existing_tarot_set_no_spread_P',tarot,True);case(1259,'missing_precise_set',remove(tarot,'fact','props.type'),False);case(1259,'ordinary_card_not_tarot_set',change(tarot,'props.type','playing_cards'),False)
results=[]
for o,label,e,k,want in cases:
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);assert got['allowed']==want,(o,label,view,got);results.append({'ordinal':o,'case':label,'view':view,'expected':want,'result':got,'core_sha256':c.digest(k)})
contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
consumer=[];permission=[]
for o,rid,k,b,dim,target,prop in [(1255,'base',holding,HB,'composition','O','props.placement.near_same_holder'),(1256,'blank_badge',badge,GB,'text','T','text.lettering.presence'),(1256,'access_card',card,GB,'expression','G','gaze.target'),(1257,'base',scene,None,'atmosphere','S','weather.precipitation'),(1258,'base',voltage,VB,'action','P','action.checking_voltage_safely_with_same_tester'),(1259,'base',tarot,None,'role','C','prop.state')]:
 e=entry(o,rid,True)
 if b:e,k=selected(e,k,b)
 assert n.property_scope_allowed(k,e['affected_dimensions'],e['affected_properties'],record=e)
 lock=copy.deepcopy(k);lock['intent_lock']['semantic_anchors'].append({'dimension':dim,'target':target,'property':prop});el=e
 if b:el,lock=selected(entry(o,rid,True),lock,b)
 assert not n.property_scope_allowed(lock,el['affected_dimensions'],el['affected_properties'],record=el);permission.append({'ordinal':o,'rid':rid,'open_allowed':True,'same_actual_property_anchor_denied':True})
 slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract,picked,slot,e),(o,rid,'consumerpositive')
 closed=copy.deepcopy(k);closed['intent_lock']['open_dimensions'].remove(dim);closed['intent_lock']['locked_dimensions'].append(dim);ec=e
 if b:ec,closed=selected(entry(o,rid,True),closed,b)
 assert not generator.core_entry_eligible(S,closed,contract,picked,slot,ec);consumer.append({'ordinal':o,'rid':rid,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'open_allowed':True,'closed_whole_effect_dimension_denied':True})
# Access-card branch has no blankness selection; an independently closed text dimension remains harmless.
k=copy.deepcopy(card);k['intent_lock']['locked_dimensions'].append('text');e,k=selected(entry(1256,'access_card',True),k,GB);assert generator.core_entry_eligible(S,k,contract,picked,e['_presentation_role'],e);consumer.append({'ordinal':1256,'rid':'access_card','independently_closed_text_no_blankness_effect':True})
# Exact old human and denied domains are display guards, not positive facts. They still bind actual consumer calls.
for o,rid,k,b in [(1255,'base',holding,HB),(1256,'access_card',card,GB)]:
 e=entry(o,rid,True)
 if b:e,k=selected(e,k,b)
 bad={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':['product']}};assert not generator.core_entry_eligible(S,k,bad,picked,e['_presentation_role'],e);consumer.append({'ordinal':o,'rid':rid,'actual_old_binding_product_domain_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-isolated-source-admission-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'frozen_generation':str(G),'module_paths_sha256':mods,'synthetic_cases':results,'property_permission_checks':permission,'actual_own_binding_consumer_checks':consumer,'admission_assertions':len(results),'property_assertions':12,'consumer_assertions':15,'all_passed':True,'actual_request_core_freeze_runtime_retrieval_render_final_pixels_or_operating':False,'root_acceptance_count':0,'boundary':'Manually specified isolated independent fixture objects only. Every actual selected RID and v2 source-target guards consumed, exact old binding consumer tested separately; no real requester core or final/runtime/render proof and no new semantic_reference units.','os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0};p=O/'CHECKS-01255-01260-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(p,c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest(),len(results),12,15)
