"""Fresh selected App-gavel view and every actual E/Rx lock, actual oldbinding consumer, independent exact-P negatives."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');base=O/'check_01260_01264_v1.py';exec(compile(base.read_text().split('cases=[',1)[0],str(base),'exec'))
import photo_search_layout as layout
import photo_role_proposals as proposals
contract={'subject_category':'human','domains':[],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
configs=[(1260,person),(1261,scene),(1262,gavel),(1263,face)];results=[];viewchecks=[]
def chosen(o,k,view='full'):
 e=entry(o,True);e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
for o,k in configs:
 e,k=chosen(o,k);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for prop in ps:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked['intent_lock']['semantic_anchors']=[copy.deepcopy(prop)];z,_=chosen(o,locked,view)
   assert not n.property_scope_allowed(locked,z['affected_dimensions'],z['affected_properties'],record=z),(o,view,prop)
   assert not generator.core_entry_eligible(S,locked,contract,picked,slot,z),(o,view,'consumerproperty',prop)
   checks.append({'case':'every_actual_E_target_Rx_property','view':view,'anchor':prop,'permission_denied':True,'actual_oldbinding_consumer_denied':True})
 for dim in ds:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked['intent_lock']['open_dimensions'].remove(dim);locked['intent_lock']['locked_dimensions'].append(dim);z,_=chosen(o,locked,view)
   assert not generator.core_entry_eligible(S,locked,contract,picked,slot,z),(o,view,'wholedimension',dim)
   checks.append({'case':'every_whole_E_dimension','view':view,'dimension':dim,'actual_oldbinding_consumer_denied':True})
 for a in k['semantic_assertions']:
  if a['axes']['kind']not in ['fact','disjoint']:continue
  bad=copy.deepcopy(k);bad['semantic_assertions']=[x for x in bad['semantic_assertions']if x['assertion_id']!=a['assertion_id']]
  for view in ['full','compact']:
   z,_=chosen(o,bad,view);assert not generator.core_entry_eligible(S,bad,contract,picked,slot,z),(o,view,'missingP',a)
   checks.append({'case':'every_missing_independent_P_disjoint','view':view,'removed':a,'actual_oldbinding_consumer_denied':True})
 results.append({'ordinal':o,'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks})
 if o==1262:
  cid=e['id'];rec=S['candidates'][cid];guard=layout.guard_record(rec,S);spec=S['slot_catalog']['relational_action'];full=n.qualification(spec,rec,source_data=S);compact=n.qualification(spec,guard,source_data=S);assert full==compact and full['status']=='eligible'
  assert full['matched_manual_role_views'][0]['fact']['value']['value']=='announcing_bid_using_holding_same_raised_gavel'
  proposal=proposals.propose(S,'relational_action',cid,[]);assert proposal['semantic_fit']['status']=='eligible'
  for view in ['full','compact']:
   z,_=chosen(o,k,view);assert generator.core_entry_eligible(S,k,contract,picked,'relational_action',z)
  assert ds==['action','pose'] and len(ps)==3
  viewchecks.append({'ordinal':1262,'full_compact_sourcefit':full,'proposal':proposal,'actual_existingbinding_consumer_requested_relational_role_full_compact_pass':True,'original_E_scope':{'dimensions':ds,'properties':ps},'boundary':'Only complete App using/holding facet supplies view, ENpartialreference does not anchor view; same full action relation/value and gavelRx preserved. No standalone announcement-to-gavel inference.'})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-every-E-Rx-manual-view-check/v1','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'manual_view_checks':viewchecks,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'case_count':sum(len(r['checks'])for r in results),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'real_request_core_freeze_runtime_render_pixels':False,'source_proof_status_changes':0}
p=O/'CHECKS-01260-01264-VIEWS-ALL-E-RX-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['case_count'])
