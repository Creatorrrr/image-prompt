"""Independent exact ambient carrier/person/crane/hair/scene P and actual whole/property locks."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');p=O/'check_01275_01280_v1.py';exec(compile(p.read_text().split('study=core',1)[0],str(p),'exec'))
J=json.loads((O/'CHECKPOINT-01290-01295-v1.json').read_text());assert c.digest(J)=='f0ce7127c9518fe0e74963e519fee862bf441e913da67603008f386498375563'
TEXT='Independent controlled baseline: existing actual scene/environment S with neutral presence, existing human P at main_subject, existing paper crane C at primary_prop with exact identity, existing owned hair region H with atomic hair presence at primary_hair. No already-hot/tropical/campus-like/folded/left-behind/signal/long/wavy/black/flowing or apartment threshold selected state is frozen. Concept remains protected. These are synthetic independent declarations, not generated source witnesses or a real requester core.'
heat=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['atmosphere','material'])
person=core(['P'],[('main_subject','P')],[('subject','P','entity.type','entity.type/v1','human')],[],['appearance'])
crane=core(['C'],[('primary_prop','C')],[('subject','C','props.type','props.type/v1','paper_crane')],[],['role'])
hair=core(['H'],[('primary_hair','H')],[('subject','H','anatomy.hair.presence','anatomy.hair.presence/v1','present')],[],['appearance'])
scene=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['setting'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def entry(o):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0],realization_id='base')
def choose(o,k,view='full'):
 e=entry(o);e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,copy.deepcopy(k)
configs=[(1290,heat,True,[('S','entity.presence')]),(1291,person,True,[('P','entity.type')]),(1292,crane,False,[('C','props.type')]),(1293,hair,True,[('H','anatomy.hair.presence')]),(1294,scene,True,[('S','entity.presence')])]
results=[];extra=[]
for o,k,wantbase,atoms in configs:
 e,k=choose(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for view in ['full','compact']:
  z,kk=choose(o,k,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,view,receipt);assert generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z)==wantbase,(o,view,'baseconsumer',wantbase);assert n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z)
  checks.append({'case':'independent_preciseP_actualsourceadmission','view':view,'admission':receipt,'actual_oldbinding_consumer_allowed':wantbase,'normalconcept_not_opened':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,bad,view);assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,'property',prop);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z)
   checks.append({'case':'every_actualE_target_and_Rx_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_oldbinding_consumer_denied':True,'consumer_already_denied_by_concept':o==1292})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k)
   if dim in bad['intent_lock']['open_dimensions']:bad['intent_lock']['open_dimensions'].remove(dim)
   if dim not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['locked_dimensions'].append(dim)
   z,kk=choose(o,bad,view);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z),(o,view,'whole',dim);checks.append({'case':'every_wholeE_dimension','view':view,'dimension':dim,'actual_oldbinding_consumer_denied':True,'normalconcept_not_opened':True})
 for owner,prop in atoms:
  a=next(a for a in k['semantic_assertions']if a['axes']['kind']=='fact'and a['axes']['owner']==owner and a['axes']['property']==prop);bad=copy.deepcopy(k);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,kk=choose(o,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,view,'missingP',a,receipt);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z);checks.append({'case':'every_manual_exact_independentP','view':view,'removed':a,'admission':receipt,'actual_oldbinding_consumer_denied':True})
 results.append({'ordinal':o,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'core':k,'expanded_dimensions':ds,'expanded_properties':ps,'base_actual_consumer_expected':wantbase,'checks':checks})
 for role in next(r['proof']['roles']for r in J['records']if r['ordinal']==o):
  for view in ['full','compact']:
   z,kk=choose(o,k,view);assert generator.core_entry_eligible(S,kk,contract('human'),picked('human'),role,z)==wantbase;extra.append({'ordinal':o,'view':view,'case':'each_sourcequalifiedrole_same_actual_oldbinding','role':role,'allowed':wantbase})
for o,k,domains in [(1291,person,['documentary','craft','wildlife','product','jewelry','food']),(1293,hair,['product','jewelry','food','wildlife'])]:
 for domain in domains:
  for view in ['full','compact']:
   e,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('human',[domain]),picked('human'),e['_presentation_role'],e);extra.append({'ordinal':o,'view':view,'case':'exact_ownbinding_deny_domain','domain':domain,'consumer_denied':True})
 for view in ['full','compact']:
  e,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('object'),picked('object'),e['_presentation_role'],e);extra.append({'ordinal':o,'view':view,'case':'broader_catalog_not_waive_source_human_or_oldhumanbinding','consumer_denied':True})
for view in ['full','compact']:
 bad=copy.deepcopy(hair);bad['semantic_assertions']=[a for a in bad['semantic_assertions']if a['axes']['kind']!='fact'];bad['semantic_assertions'].append(assertion('generic_presence','fact',owner='H',property='entity.presence',value_type='entity.presence/v1',value='present'));e,kk=choose(1293,bad,view);receipt=n.admission(e,kk);assert not receipt['allowed'];extra.append({'ordinal':1293,'view':view,'case':'genericpresence_not_atomic_ownedhair_witness','admission':receipt})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Independent controlled fixtures only.1290 actualambientphysicalheat+weather two E;1292 protectedconcept staysclosed despite sourcequalification;1293 exactownedhairP and4appearanceE retained, broaderwig/haircatalog notwaive oldhuman/sourceguards. Everyactualeffect property+whole dimension/P/oldbinding tested fullcompact. No sourcerename/alias/code/runtime writes.'}
p=O/'CHECKS-01290-01295-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
