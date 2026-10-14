"""Literal independent exact P sets; every actual effect/receiver and full dimension. Protectedsubject stays closed."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');src=O/'check_01265_01270_four_v1.py';exec(compile(src.read_text().split('cases=[]',1)[0],str(src),'exec'))
from fixture_01267_v1 import make_core
import photo_search_layout as layout
import photo_role_proposals as proposals
LTXT='Independent synthetic request declares already-existing illumination L, shrine-lantern source S, spatial region R, each neutral presence, exact source type and exact region identity. Caller selects these actual owners. Source use and grid geometry not frozen. Only lighting is mutable; no surface or scattering material is declared.'
light=make_core(LTXT,['L','S','R'],[],[('subject','L','entity.presence','entity.presence/v1','present'),('subject','S','entity.presence','entity.presence/v1','present'),('subject','R','entity.presence','entity.presence/v1','present'),('subject','S','props.type','props.type/v1','shrine_lantern'),('setting','R','space.region.kind','space.region.kind/v1','spatial_region')],[],['lighting'],anchors=[{'dimension':'setting','target':'R','property':'space.region.kind'}])
# Exact independent required fixture atoms chosen manually; unrelated foreground O facts are not candidate prerequisites.
configs=[(1265,surface,'environment',True,[('fact','S','entity.presence'),('fact','S','surface.material')]),(1266,wand,'human',True,[('fact','P','entity.type'),('fact','V','props.type'),('fact','Q','entity.presence'),('disjoint','P','V')]),(1267,light,'human',True,[('fact','L','entity.presence'),('fact','S','entity.presence'),('fact','R','entity.presence'),('fact','S','props.type'),('fact','R','space.region.kind')]),(1268,person,'human',False,[('fact','P','entity.type')]),(1269,face,'human',True,[('fact','F','anatomy.face.presence'),('fact','F','anatomy.mouth.presence'),('fact','F','anatomy.lips.presence')])]
def choose(o,k,view='full'):
 e=entry(o,True)
 if o==1265:e,k=selected(e,k,'S')
 elif o==1267:
  k=copy.deepcopy(k);k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);pr=next(x['proof']for x in J['records']if x['ordinal']==o);graph=n.frozen_witnesses(k)['graph'];e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(graph),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':pr['meaning_sha256'],'qualification_sha256':c.digest(pr),'bindings':[{'target':'light','owner_id':'L'},{'target':'lantern_source','owner_id':'S'},{'target':'illuminated_region','owner_id':'R'}]}]}
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
results=[];vr=[]
for o,k,category,wantbase,atoms in configs:
 e,k=choose(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];assert generator.core_entry_eligible(S,k,contract(category),picked(category),slot,e)==wantbase
 checks=[]
 for prop in ps:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['intent_lock']['semantic_anchors'].append(copy.deepcopy(prop));z,bad=choose(o,bad,view)
   assert not n.property_scope_allowed(bad,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,prop)
   assert not generator.core_entry_eligible(S,bad,contract(category),picked(category),slot,z),(o,view,'consumerproperty',prop)
   checks.append({'case':'every_actual_E_target_Rx_property','view':view,'anchor':prop,'property_permission_denied':True,'actual_oldbinding_consumer_denied':True,'consumer_already_denied_by_subject_lock':o==1268})
 for dim in ds:
  for view in ['full','compact']:
   bad=copy.deepcopy(k);bad.pop('canonical_sha256',None)
   wasopen=dim in bad['intent_lock']['open_dimensions']
   if wasopen:bad['intent_lock']['open_dimensions'].remove(dim)
   if dim not in bad['intent_lock']['locked_dimensions']:bad['intent_lock']['locked_dimensions'].append(dim)
   z,bad=choose(o,bad,view);assert not generator.core_entry_eligible(S,bad,contract(category),picked(category),slot,z),(o,view,'whole',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'was_open':wasopen,'actual_oldbinding_consumer_denied':True,'subject_not_opened':True})
 for kind,owner,prop_or_right in atoms:
  if kind=='fact':a=next(x for x in k['semantic_assertions']if x['axes']['kind']=='fact'and x['axes']['owner']==owner and x['axes']['property']==prop_or_right)
  else:a=next(x for x in k['semantic_assertions']if x['axes']['kind']==kind and x['axes']['left']==owner and x['axes']['right']==prop_or_right)
  bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[x for x in bad['semantic_assertions']if x['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,bad2=choose(o,bad,view);receipt=n.admission(z,bad2);assert not receipt['allowed'],(o,view,'missingP',a,receipt)
   assert not generator.core_entry_eligible(S,bad2,contract(category),picked(category),slot,z)
   checks.append({'case':'every_manually_identified_independent_required_P_or_disjoint','view':view,'removed':a,'admission':receipt,'actual_oldbinding_consumer_denied':True})
 results.append({'ordinal':o,'base_actual_consumer_expected':wantbase,'base_actual_consumer_allowed':wantbase,'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks})
 if o==1266:
  rec=S['candidates'][e['id']];guard=layout.guard_record(rec,S)
  for role in ['relational_action','staging_degree']:
   spec=S['slot_catalog'][role];full=n.qualification(spec,rec,source_data=S);compact=n.qualification(spec,guard,source_data=S);assert full==compact and full['status']=='eligible'and full['matched_manual_role_views']
   proposal=proposals.propose(S,role,e['id'],[]);assert proposal['semantic_fit']['status']=='eligible'
   for view in ['full','compact']:
    z,k1=choose(o,k,view);assert generator.core_entry_eligible(S,k1,contract('human'),picked('human'),role,z)
   assert ds==['action','pose','setting']
   vr.append({'ordinal':1266,'role':role,'fullcompact_qualification':full,'proposal':proposal,'actual_sameoldbinding_requestedrole_fullcompact_allowed':True,'original_E_dimensions':ds,'original_E_properties':ps,'boundary':'Source-positive App holder/wand interaction or namedstageposing facet only. No extra interaction/staging/style effect, no cameraawareness, same full canonical facts/modes/value/Rx/guards preserved.'})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-P-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_role_view_checks':vr,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'actual_request_core_freeze_runtime_render_pixels':False,'boundary':'Explicit independent controlled fixtures only.1268source admitted but originalsubject lock consumer denied; never opened subject. Every actual E/Rx property, whole dimension and manually identified required P/guard tested fullcompact. Roleviews unchanged fullcanonical E, same oldbinding consumed.'}
p=O/'CHECKS-01265-01270-VIEWS-ALL-E-RX-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['case_count'])
