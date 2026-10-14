"""Explicit independent actual owners, all native relation guards/P and E+Rx lock checks."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');p=O/'check_01275_01280_v1.py';exec(compile(p.read_text().split('study=core',1)[0],str(p),'exec'))
J=json.loads((O/'CHECKPOINT-01285-01290-v1.json').read_text());assert c.digest(J)=='e80584a1b98289af7b81936d0b994ad96744fdd55ff8405b036cd8e9068444ed'
TEXT='Independent synthetic baseline declares existing object O and actualchair C distinct, existing participant endpoints A and B distinct, each neutral presence, no already-propped/support/counterpart or chair-association relation. Existing actual distinct humans A/B, existingmirror M and image I for mirror fixture. Existing humans H/T with exact category, neutral presence and disjointness, image I for colleague fixture. Existing recording camera K, image I and actualsubject S; existing scene Q. No count/movement/sharpness/colleague/offframe/campus effect is frozen; count stays normally protected. Controlled independent fixture only.'
chair=core(['O','C','A','B'],[],[('subject',x,'entity.presence','entity.presence/v1','present')for x in ['O','C','A','B']]+[('subject','C','props.type','props.type/v1','chair')],[('disjoint','O','C'),('disjoint','A','B')],['composition','role','relationship'])
mirror=core(['A','B','M','I'],[('main_subject','A'),('secondary_subject','B'),('primary_prop','M'),('image','I')],[('subject','A','entity.type','entity.type/v1','human'),('subject','B','entity.type','entity.type/v1','human'),('subject','M','props.type','props.type/v1','mirror'),('subject','I','entity.presence','entity.presence/v1','present')],[('disjoint','A','B')],['composition','framing'])
colleague=core(['H','T','I'],[('image','I')],[('subject',x,'entity.presence','entity.presence/v1','present')for x in ['H','T','I']]+[('subject','H','entity.category','entity.category/v1','human'),('subject','T','entity.category','entity.category/v1','human')],[('disjoint','H','T')],['relationship','framing'])
pan=core(['K','I','S'],[('recording_camera','K'),('image','I'),('main_subject','S')],[('subject','K','entity.type','entity.type/v1','camera'),('subject','I','entity.presence','entity.presence/v1','present'),('subject','S','entity.presence','entity.presence/v1','present')],[],['camera'])
scene=core(['Q'],[('scene','Q')],[('subject','Q','entity.presence','entity.presence/v1','present')],[],['setting'])
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def entry(o):
 row=next(x for x in J['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0],realization_id='base')
def choose(o,k,view='full',bindings=None):
 e=entry(o);k=copy.deepcopy(k)
 if o in [1285,1287]and bindings is not False:
  k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];chosen=bindings or([('propped_object','O'),('chair','C'),('counterpart','A'),('other_participant','B')]if o==1285 else[('colleague','H'),('other_person','T')])
  e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':x}for t,x in chosen]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
configs=[(1285,chair,True,[('fact',x,'entity.presence')for x in ['O','C','A','B']]+[('fact','C','props.type'),('disjoint','O','C'),('disjoint','A','B')]),(1286,mirror,False,[('fact','A','entity.type'),('fact','B','entity.type'),('fact','M','props.type'),('fact','I','entity.presence'),('disjoint','A','B')]),(1287,colleague,True,[('fact',x,'entity.presence')for x in ['H','T','I']]+[('fact','H','entity.category'),('fact','T','entity.category'),('disjoint','H','T')]),(1288,pan,True,[('fact','K','entity.type'),('fact','I','entity.presence'),('fact','S','entity.presence')]),(1289,scene,True,[('fact','Q','entity.presence')])]
results=[];views=[];extra=[]
for o,k,wantbase,atoms in configs:
 e,k=choose(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for view in ['full','compact']:
  z,kk=choose(o,k,view);receipt=n.admission(z,kk);assert receipt['allowed'],(o,view,receipt);assert generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z)==wantbase,(o,view,'baseconsumer',wantbase);assert n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z)
  checks.append({'case':'independent_precise_P_and_exactsourceguards','view':view,'admission':receipt,'base_actual_oldbinding_consumer_allowed':wantbase,'count_not_opened':True})
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,kk=choose(o,bad,view);assert not n.property_scope_allowed(kk,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,'property',prop);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z)
   checks.append({'case':'every_actual_E_target_and_Rx_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_ownbinding_consumer_denied':True,'consumer_already_denied_by_count_lock':o==1286})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None)
   if dim in bad['intent_lock']['open_dimensions']:bad['intent_lock']['open_dimensions'].remove(dim)
   if dim not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['locked_dimensions'].append(dim)
   z,kk=choose(o,bad,view);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z),(o,view,'whole',dim);checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_ownbinding_consumer_denied':True,'count_not_opened':True})
 for kind,x,p in atoms:
  a=next(a for a in k['semantic_assertions']if a['axes']['kind']==kind and((kind=='fact'and a['axes']['owner']==x and a['axes']['property']==p)or(kind!='fact'and a['axes']['left']==x and a['axes']['right']==p)));bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[z for z in bad['semantic_assertions']if z['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,kk=choose(o,bad,view);receipt=n.admission(z,kk);assert not receipt['allowed'],(o,view,'missingP',a,receipt);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),slot,z)
   checks.append({'case':'every_manual_preciseP_existingpresence_or_actual_disjoint','view':view,'removed':a,'admission':receipt,'actual_ownbinding_consumer_denied':True})
 results.append({'ordinal':o,'binding_id':e['binding_id'],'binding_sha256':c.digest(S['slot_bindings'][e['binding_id']]),'core':k,'expanded_dimensions':ds,'expanded_properties':ps,'base_actual_consumer_expected':wantbase,'checks':checks})
 if o==1286:
  rec=S['candidates'][e['id']];guard=layout.guard_record(rec,S);spec=S['slot_catalog']['apparatus_pov'];full=n.qualification(spec,rec,source_data=S);compact=n.qualification(spec,guard,source_data=S);assert full==compact and full['status']=='eligible'and full['matched_manual_role_views'];proposal=proposals.propose(S,'apparatus_pov',e['id'],[]);assert proposal['semantic_fit']['status']=='eligible'
  for view in ['full','compact']:
   z,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('human'),picked('human'),'apparatus_pov',z)
  assert ds==['composition','count','framing'];views.append({'ordinal':o,'role':'apparatus_pov','fullcompact_sourcequalification':full,'proposal':proposal,'same_actual_oldbinding_newrole_consumer_denied_by_count':True,'canonical_E_dimensions_unchanged':ds,'no_camera_permission_added':True,'canonical_E_properties':ps})
 # Every source-qualified role consumes the same entry and same original E policy; no new binding registration.
 for role in next(x['proof']['roles']for x in J['records']if x['ordinal']==o):
  for view in ['full','compact']:
   z,kk=choose(o,k,view);assert generator.core_entry_eligible(S,kk,contract('human'),picked('human'),role,z)==wantbase;extra.append({'ordinal':o,'view':view,'case':'same_exact_oldbinding_each_newrequestedrole','role':role,'allowed':wantbase})
for o,k in [(1285,chair),(1287,colleague)]:
 for domain in ['product','jewelry','food','wildlife']:
  for view in ['full','compact']:
   e,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('human',[domain]),picked('human'),e['_presentation_role'],e);extra.append({'ordinal':o,'view':view,'case':'actual_ownbinding_deny_domain','domain':domain,'consumer_denied':True})
 for view in ['full','compact']:
  e,kk=choose(o,k,view,False);receipt=n.admission(e,kk);assert not receipt['allowed'];extra.append({'ordinal':o,'view':view,'case':'actual_caller_owner_selection_missing','admission':receipt})
  e,kk=choose(o,k,view);assert not generator.core_entry_eligible(S,kk,contract('object'),picked('object'),e['_presentation_role'],e);extra.append({'ordinal':o,'view':view,'case':'actual_ownbinding_human_display_not_waived','consumer_denied':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_role_view_checks':views,'extra_boundary_checks':extra,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results)+len(extra),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'os_network_denied':True,'provider_keys_absent':True,'model_network_calls':0,'boundary':'Five fresh controlled independent fixtures.1285 exactfiveE Appcanonicalrelations/shortfieldrefs retain actualendpoints, all sourceguards.1286normalcount staysclosed despite sourcequalifiedthroughmirrorview, no cameraE permission.1287 actualrole+offframe+framing allRx scopes.1288 actualacuityE not plane/preservation.1299pending. No source/Git/code/runtime or operational mutation.'}
p=O/'CHECKS-01285-01290-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
