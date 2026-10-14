"""Local draft checks/freeze only. No full proof, signature or registration."""
import copy,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ROOT=R.parents[3]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_semantic_evidence as s
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
A=R/'authored';prefix='native_11870_01250_02250.01250_01300.'
ip=A/(prefix+'inputs_v1.json');bp=A/(prefix+'ownbindings_v1.json');dp=A/(prefix+'draft_before_reread_v4.json');v3=A/(prefix+'draft_before_reread_v3.json')
I=json.loads(ip.read_text());D=json.loads(dp.read_text());old=json.loads(v3.read_text());CAT=I['catalog_final142']
assert c.digest(CAT)=='e7ad376ae1e195ada8268259015b29751f33a24f47e23899c7b7e9329b4a3e28'
checks=[]
for row,prior in zip(D['rows'],old['rows']):
 rec=row['source_proposal'];n=row['ordinal'];cid=row['candidate_id']
 assert rec['conditions']==row['source_before']['conditions']
 assert row['source_before']==I['records'][cid]['after_existing5B_corrections']
 assert c.digest(row['source_before'])==row['before_source_full_sha256']
 assert c.digest(rec)==row['after_proposed_full_sha256']
 rr.validate_content(rec);c.validate_effects(rec['effects'],cid);c.validate_conditions(rec['conditions'],cid)
 assert rr.ids(rec)==['base'] and row['required_cid_closure']=={} and row['explicit_binding_closure']=={}
 assert row['existing_own_bindings_full']==json.loads(bp.read_text())['bindings_by_cid'][cid]
 for role in row['proposed_roles_and_binding_intent']:
  spec=CAT[role['tag']];assert role['spec_sha256']==c.digest(spec)
  assert role['semantic_role']==spec['semantic_role']
  c.validate_conditions(role['conditions'],cid+' proposed role '+role['tag'])
 if row['native_fact_draft']:
  fs={f['id']:f for f in row['native_fact_draft']};assert len(fs)==len(row['native_fact_draft'])
  for f in fs.values():
   s._fact_valid(f)
   assert f['quote']==s.positive_string(rec,f['pointer'],realization_id='base')
   assert all(req in fs and fs[req]['mode'] in ['prerequisite','preservation'] and req!=f['id'] for req in f['requires'])
  s._validate_owner_map(row['owner_maps_draft']['base'],row['native_fact_draft'])
  units={u['pointer']:u for u in row['source_units_draft']};assert len(units)==len(row['source_units_draft'])
  assert s.primary_paths(rec,'base')<=set(units),(n,s.primary_paths(rec,'base')-set(units))
  for pointer,u in units.items():
   assert u['quote']==s.positive_string(rec,pointer,realization_id='base')
   assert all(fs[ref]['pointer']==pointer for ref in u['fact_refs'])
  assert {ref for u in units.values() for ref in u['fact_refs']}==set(fs)
  effectset=s.effect_set(rec,'base')
  actual={(x['dimension'],x['target'],x['property']) for x in effectset['properties']}
  declared={(f['dimension'],f['target'],f['property']) for f in fs.values() if f['mode']=='effect'}
  assert actual==declared,(n,actual,declared)
  assert set(effectset['dimensions'])=={f['dimension'] for f in fs.values() if f['mode']=='effect'}
  for role in row['proposed_roles_and_binding_intent']:
   spec=CAT[role['tag']]
   for ref in role['fact_refs']:
    f=fs[ref]
    assert f['mode'] in role['support_modes'] and f['dimension'] in spec['dimensions']
    assert any(f['property']==prefix.rstrip('.') or f['property'].startswith(prefix if prefix.endswith('.') else prefix+'.') for prefix in spec['property_prefixes']),(n,role['tag'],f)
  row['effect_sets_draft']={'base':effectset}
 else:
  assert row['exact_pending_reasons'] and not row['proposed_roles_and_binding_intent']
  row['effect_sets_draft']=None
 # Direct reread was performed on complete v3 proposals in five 10-record batches;
 # 49 v4 records are canonically equal and 1293 was printed/read in full again.
 assert rec==prior['source_proposal'] or n==1293
 row['actual_read']['proposed_full_source_reread']=True
 row['actual_read']['proposed_source_reread_basis']='Full v3 source reread, exact full-value equality to v4' if n!=1293 else 'Complete changed v4 source reread after separating English wave from Korean flowing arrangement'
 checks.append({'ordinal':n,'candidate_id':cid,'source_shape_pass':True,'fact_fragment_shape_pass':bool(row['native_fact_draft']),'full_native_proof_validation_performed':False})
D['draft_stage']='frozen_manual_source_fact_draft_after_whole_corrected_reread'
D['local_fragment_validation']=checks
D['full_native_validation_performed']=False
D['native_signature_emitted']=False
D['registration_performed']=False
D['actual_read_count']=50
D['semantic_draft_ready_count']=sum(not r['exact_pending_reasons'] for r in D['rows'])
D['semantic_pending_ordinals']=[r['ordinal'] for r in D['rows'] if r['exact_pending_reasons']]
out=A/(prefix+'draft_v1.json');assert not out.exists();out.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
files=[ip,bp,dp,v3,A/(prefix+'author_v4.py'),Path(__file__),out,R/'CATALOG-FINAL-142.json',R/'CATALOG-FINAL-142-REVIEW.json',R/'worker-notes/native-v3-authoring-guide-20261014_v2.md',R/'worker-notes/native-v3-compound-and-partial-lock-contract-20261014.md']
note={'schema':'native-direct-draft-worker-note/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','review_method':'codex_subagent_direct_source_read','assigned_range':[1250,2250],'completed_draft_range':[1250,1300],'actual_last_complete_source_read_ordinal':1299,'next_unread_ordinal':1300,'count':50,'prepared_count':50,'actual_read_count':50,'semantic_draft_ready_count':D['semantic_draft_ready_count'],'exact_semantic_pending_ordinals':D['semantic_pending_ordinals'],'formal_input_rebind_pending_ordinals':list(range(1250,1300)),'root_formal_fullsnapshot_assignment_input_pending':True,'source_sha256':I['source_sha256'],'catalog_sha256':I['catalog_final142_sha256'],'exact_ids':I['ids'],'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'source_read_batches':[[1250,1258],[1258,1270],[1270,1290],[1290,1300]],'full_registered5B_read_batches':[[1250,1258],[1258,1264],[1264,1270],[1270,1278],[1278,1285],[1285,1292],[1292,1300]],'own_binding_full_read_batches':[[1250,1270],[1270,1300]],'whole_corrected_proposal_reread_batches':[[1250,1260],[1260,1270],[1270,1280],[1280,1290],[1290,1300]],'reread_followup':[1293],'mandatory_closure':'All 50 are base visual_options with zero CID/member-binding closure; each own persisted display binding was separately read in full including ID/role/semantic_role/conditions/weight. No binding-only identity fallback.','binding_condition_policy':'Per-row intrinsic conditions retained exactly. Each proposed142 binding has individually authored conditions, optional role, semantic_role, weight and intent. No whole old-condition copy/intersection/default; source guards plus typed prerequisite obligations remain whole-cue gates. Root assigns stable new binding IDs later.','spec_read_boundary':'Relevant full final142 specs read directly; do not claim a new full142 catalog read. Final142 canonical digest rechecked.','local_validation_boundary':'Native helper fact-shape/owner-map/positive-string/path/effect fragments plus source effect/condition/content shape were checked only for this own subset. No full native proof, core witnesses, parity/runtime test, qualification, registration or global verification.','qualification_issues':['Exact source/application/effect/translation corrections are PROPOSALS awaiting root review, not operational approval.','All 50 require equality/rebind to root formal input/snapshot/spec/registered locator before a new native signature.','13 semantic pending cases retain exact gaps without invented endpoints, OR choice, current action or lock-avoiding prerequisite.','Volumetric air beams retain their lighting mutation but are not forced into surface-based light_shape or complete lighting roles.','Bokeh image artifact is separated from named source type; sharpness, mood and seasonal choices remain actual effects.'],'frozen_at_utc':datetime.now(timezone.utc).isoformat(),'network_model_git_registration_operational_changes':0}
np=R/'worker-notes/native-11870-01250-01300-draft-v1.json';assert not np.exists();np.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'draft':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'note':str(np),'note_sha256':hashlib.sha256(np.read_bytes()).hexdigest(),'ready':D['semantic_draft_ready_count'],'pending':D['semantic_pending_ordinals'],'last_full_read':1299,'next_unread':1300}))
