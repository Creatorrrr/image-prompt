"""Exact source-qualified roleviews and every actual E/receiver/whole-dimension lock. No source/proof edits."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');base=O/'check_01255_01260_v1.py';exec(compile(base.read_text().split('cases=[]',1)[0],str(base),'exec'))
import photo_search_layout as layout
import photo_role_proposals as proposals
HB=[('holder','H'),('held_object','O')];GB=[('gaze_owner','G'),('target','T')];VB=[('operator','P'),('tester','V'),('tested_endpoint','M')]
contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
configs=[(1255,'base',holding,HB),(1256,'blank_badge',badge,GB),(1256,'access_card',card,GB),(1257,'base',scene,None),(1258,'base',voltage,VB),(1259,'base',tarot,None)]
def chosen(o,rid,k,mapping,view='full'):
 e=entry(o,rid,True)
 if mapping:e,k=selected(e,k,mapping)
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
results=[];vr=[]
for ordinal,rid,k,mapping in configs:
 e,k=chosen(ordinal,rid,k,mapping);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];checks=[]
 for prop in ps:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked.pop('canonical_sha256',None);locked['intent_lock']['semantic_anchors']=[copy.deepcopy(prop)];z,k1=chosen(ordinal,rid,locked,mapping,view)
   assert not n.property_scope_allowed(k1,z['affected_dimensions'],z['affected_properties'],record=z),(ordinal,rid,view,prop)
   assert not generator.core_entry_eligible(S,k1,contract,picked,slot,z),(ordinal,rid,view,'consumerproperty',prop)
   checks.append({'case':'every_actual_E_target_and_receiver_property_lock','view':view,'anchor':prop,'permission_denied':True,'actual_oldbinding_consumer_denied':True})
 for dim in ds:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked.pop('canonical_sha256',None);locked['intent_lock']['open_dimensions'].remove(dim);locked['intent_lock']['locked_dimensions'].append(dim);z,k1=chosen(ordinal,rid,locked,mapping,view)
   assert not generator.core_entry_eligible(S,k1,contract,picked,slot,z),(ordinal,rid,view,'wholedimension',dim)
   checks.append({'case':'every_whole_E_dimension_lock','view':view,'dimension':dim,'actual_oldbinding_consumer_denied':True})
 for assertion_row in k['semantic_assertions']:
  if assertion_row['axes']['kind']not in ['fact','disjoint']:continue
  bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[a for a in bad['semantic_assertions']if a['assertion_id']!=assertion_row['assertion_id']]
  for view in ['full','compact']:
   z,k1=chosen(ordinal,rid,bad,mapping,view);assert not generator.core_entry_eligible(S,k1,contract,picked,slot,z),(ordinal,rid,view,'missingP',assertion_row)
   checks.append({'case':'every_missing_independent_P_or_disjoint_witness','view':view,'removed':assertion_row,'actual_oldbinding_consumer_denied':True})
 results.append({'ordinal':ordinal,'realization_id':rid,'expanded_dimensions':ds,'expanded_properties':ps,'checks':checks})
 if ordinal in [1255,1258]:
  cid=e['id'];rec=S['candidates'][cid];guard=layout.guard_record(rec,S);spec=S['slot_catalog']['relational_action'];full=n.qualification(spec,rec,rid,source_data=S);compact=n.qualification(spec,guard,rid,source_data=S)
  assert full==compact and full['status']=='eligible',(ordinal,full,compact)
  assert full['matched_manual_role_views']
  noauthority=[n.qualification(spec,x,rid)['status']for x in [rec,guard]];assert noauthority==['review_required','review_required']
  proposal=proposals.propose(S,'relational_action',cid,[],realization_ids=[rid]);assert proposal['semantic_fit']['status']=='review_required' and proposal['semantic_fit']['reason']=='explicit_existing_owner_selection_required'
  for view in ['full','compact']:
   z,k1=chosen(ordinal,rid,k,mapping,view);assert generator.core_entry_eligible(S,k1,contract,picked,'relational_action',z),(ordinal,view,'actualsamebindingnewrole')
  # New role consumes SAME full E scope; a view cannot create relationship permission.
  assert 'relationship'not in ds and {p['dimension']for p in ps}<=set(ds)
  bad=copy.deepcopy(rec);p=bad['content']['role_evidence'];p['manual_role_views'][0]['canonical_fact_refs'][0]['fact_sha256']='0'*64;p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
  try:n.validate(bad,S['slot_catalog'],corpus=S)
  except ValueError:negative_rejected=True
  else:raise AssertionError('forged canonical view hash accepted')
  vr.append({'ordinal':ordinal,'full_compact_qualification_equal':full,'missing_full_source_authority_status':noauthority,'proposal':proposal,'actual_oldbinding_consumer_new_role_full_compact_allowed':True,'original_permission_dimensions':ds,'original_expanded_properties':ps,'forged_canonical_fact_view_hash_rejected':negative_rejected})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b={'schema':'photo-native-whole-E-Rx-roleview-isolated-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'records':results,'role_view_checks':vr,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in results),'all_E_Rx_P_case_count':sum(len(r['checks'])for r in results),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'root_accepted':0,'operating':0,'source_proof_status_changes':0,'real_request_core_freeze_runtime_render_pixels':False,'boundary':'Independent controlled synthetic witnesses only. Actual new manual role views have exact fullsource authority, fullcompact equal eligible source qualification; search proposal remains explicit-existing-owner-selection review_required, actual selected oldbinding consumer and unchanged wholeE permissions. Every actual E target/Rx property and whole dimension denied. No real runtime adoption/pixels or source activation.'}
p=O/'CHECKS-01255-01260-VIEWS-ALL-E-RX-v2.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(p.read_bytes()).hexdigest(),b['actual_expanded_property_count'],b['all_E_Rx_P_case_count'])
