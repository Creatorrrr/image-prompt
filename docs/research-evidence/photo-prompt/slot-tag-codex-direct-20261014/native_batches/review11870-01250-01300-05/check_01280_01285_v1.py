"""Independent fixtures keep normally protected concept/event closed; all actual E/Rx locks."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05')
p=O/'check_01275_01280_v1.py';exec(compile(p.read_text().split('study=core',1)[0],str(p),'exec'))
J=json.loads((O/'CHECKPOINT-01280-01285-v1.json').read_text());assert c.digest(J)=='59334ea4f2ae6983e7d467dec12fd37017bfb2afdadffe09e80d6ae9a695d0a1'
TEXT='Independent synthetic baseline declares existing scene S; existing recording camera K, image I, actual crowd C; caller selects existing face carrier F and distinct existing face X, each neutral presence, with actual face and eyes presence on F only, image at common role. No existing ghost association, summer, mood, concert or focal plane is frozen. Concept and event stay normally protected; independent album eligibility can be supplied separately. Controlled fixture, not source-derived actual request.'
scene=core(['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['setting','timing','atmosphere'])
concert=core(['K','I','C','S'],[('recording_camera','K'),('image','I'),('secondary_subject','C'),('scene','S')],[('subject','K','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','C','entity.type','entity.type/v1','crowd'),('subject','S','entity.presence','entity.presence/v1','present')],[],['camera','composition'])
face=core(['I','F','X'],[('image','I')],[('subject','I','entity.presence','entity.presence/v1','present'),('subject','F','entity.presence','entity.presence/v1','present'),('subject','F','anatomy.face.presence','anatomy.face.presence/v1','present'),('subject','F','anatomy.eyes.presence','anatomy.eyes.presence/v1','present'),('subject','X','entity.presence','entity.presence/v1','present')],[],['camera'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category,album=False):return {'subject':{'kind':[category],'tags':[category]+(['album']if album else[])}}
def entry(o):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0],realization_id='base')
def choose(o,k,view='full',owner='F'):
 e=entry(o);k=copy.deepcopy(k)
 if o==1284 and owner is not None:
  k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':'face','owner_id':owner}]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
configs=[(1280,scene,False,[('S','entity.presence')]),(1281,scene,True,[('S','entity.presence')]),(1282,scene,True,[('S','entity.presence')]),(1283,concert,False,[('K','entity.type'),('I','entity.presence'),('C','entity.type'),('S','entity.presence')]),(1284,face,True,[('I','entity.presence'),('F','entity.presence'),('F','anatomy.face.presence'),('F','anatomy.eyes.presence')])]
results=[];extra=[]
for o,k,wantbase,atoms in configs:
 e,k=choose(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[];co=contract('human',['album'])if o==1284 else contract('human');pi=picked('human',o==1284)
 for view in ['full','compact']:
  z,kk=choose(o,k,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,view,receipt)
  assert generator.core_entry_eligible(S,kk,co,pi,slot,z)==wantbase,(o,view,'baseconsumer',wantbase)
  assert n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z)
  checks.append({'case':'precise_independent_source_admission_separate_from_whole_permission','view':view,'admission':receipt,'base_actual_oldbinding_consumer_allowed':wantbase,'unanchored_property_only_allowed':True,'concept_and_event_not_opened':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,bad,view)
   assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,'property',prop);assert not generator.core_entry_eligible(S,kk,co,pi,slot,z)
   checks.append({'case':'every_actual_E_target_and_Rx_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_ownbinding_consumer_denied':True,'consumer_already_denied_by_protected_concept_or_event':not wantbase})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None)
   if dim in bad['intent_lock']['open_dimensions']:bad['intent_lock']['open_dimensions'].remove(dim)
   if dim not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['locked_dimensions'].append(dim)
   z,kk=choose(o,bad,view);assert not generator.core_entry_eligible(S,kk,co,pi,slot,z),(o,view,'whole',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_ownbinding_consumer_denied':True,'concept_and_event_not_opened':True})
 for owner,prop in atoms:
  a=next(a for a in k['semantic_assertions']if a['axes']['kind']=='fact'and a['axes']['owner']==owner and a['axes']['property']==prop);bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,kk=choose(o,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,view,'missingP',a,receipt);assert not generator.core_entry_eligible(S,kk,co,pi,slot,z)
   checks.append({'case':'every_manual_precise_P_or_selectedexisting_neutralpresence','view':view,'removed':a,'admission':receipt,'actual_ownbinding_consumer_denied':True})
 results.append({'ordinal':o,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'core':k,'expanded_dimensions':ds,'expanded_properties':ps,'base_actual_consumer_expected':wantbase,'checks':checks})
for view in ['full','compact']:
 for owner,label in [(None,'caller_face_choice_missing'),('X','chosen_different_face_without_samecarrier_eyes')]:
  e,k=choose(1284,face,view,owner);receipt=n.admission(e,k);assert not receipt['allowed'];extra.append({'ordinal':1284,'view':view,'case':label,'admission':receipt})
 e,k=choose(1284,face,view);assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);extra.append({'ordinal':1284,'view':view,'case':'external_kpop_or_album_missing_despite_candidate_own_kpop_tag','consumer_denied':True})
 bad=copy.deepcopy(face)
 for a in bad['semantic_assertions']:
  if a['axes']['kind']=='fact'and a['axes']['property']=='anatomy.eyes.presence':a['axes']['owner']='X'
 e,k=choose(1284,bad,view);receipt=n.admission(e,k);assert not receipt['allowed'];extra.append({'ordinal':1284,'view':view,'case':'eyes_on_other_face_no_carrier_inheritance','admission':receipt})
 bad=copy.deepcopy(face);bad['semantic_assertions']=[a for a in bad['semantic_assertions']if not(a['axes']['kind']=='fact'and a['axes']['property']in ['anatomy.face.presence','anatomy.eyes.presence'])];bad['semantic_assertions'].append(assertion('array','fact','body_geometry',owner='F',property='body.parts',value_type='body.parts/v1',value=['face','eyes']));bad['intent_lock']['semantic_anchors'].append({'dimension':'body_geometry','target':'F','property':'body.parts'})
 e,k=choose(1284,bad,view);receipt=n.admission(e,k);assert not receipt['allowed'];extra.append({'ordinal':1284,'view':view,'case':'old_array_not_atomic_or_source_guard_alias','admission':receipt})
# Phrase coverage inventory asserts only actual positive fields, no new semantic content from strings.
for row in J['records']:
 rec=S['candidates'][row['candidate_id']];assert n.qualification(S['slot_catalog'][next(iter(row['proof']['roles']))],rec,source_data=S)['status']=='eligible'
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Five fresh controlled independent fixtures.1280concept and1283event remain closed: sourceadmissionpositive but normalactualconsumerdenied, not semantic rejection. All actual E/Rx properties and whole dimensions/P tested fullcompact.1284 samecarrieratomicparts/callerexistingpresence/sourcev2rules and externalalbum eligibility mandatory. No oldproperty alias or effectname rewrite.'}
p=O/'CHECKS-01280-01285-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
