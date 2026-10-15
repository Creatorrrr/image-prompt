"""Targeted same-model peer source review and fe5b consumer controls; no old artifact writes."""
import ast,copy,gzip,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';O=Path(__file__).resolve().parent;W=R/'authored/native_12250_expression5_149_01';D=R/'native-inputs/prepared/review12250-expression5-149-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/fe5b593c819806a31803e40c620e6f2b28c3b54103f451dd6f38920f2d537258');forbidden=[]
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,name,path=None,target=None):
  if name.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama','requests','httpx'}:forbidden.append(name);raise AssertionError(name)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import prompt_generator as generator
H=c.digest;raw=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_bytes())
assert raw(n.__file__)=='722a4be059b95c6a875cffa00d106ba63d7288c16ea8b155f13eb0e4f183104a'
J=read(W/'BATCH-v1.json');A=read(D/'ASSIGNMENT.json');I=read(D/'INPUT.json');PACK=read(D/'PREPARED-PACKET.json');PLAN=read(R/'authored/native_12250_approval_pilot149_source25_plan_05.json');S=json.loads(gzip.decompress((ROOT/I['current_snapshot']['file']).read_bytes()));CAT=S['slot_catalog'];COR=copy.deepcopy(S)
assert raw(W/'BATCH-v1.json')=='6b3cb14402286afef1e5b947957bd1e118051622e061b145baa89e5f6bd6b4a0';assert H(J)=='03af0630fab05e390aa5d5e390ed9c49c58782a96fd5572d74f42a84e298672d';assert H(S)=='d353a2f3282415e682fb6623aa34f395c82d20f2310ce77fbec3bea592360f05';assert H(CAT)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15';assert H(PLAN)=='644991678f9a8241de3cea3d476b71787ebd0c85dfdbe1a81b6271227fa92185';assert H(I)==A['input']['sha256']==J['input_sha256'] and H(A)==J['assignment_sha256'];assert raw(D/'INPUT.json')==A['input']['file_sha256']
for row in J['records']:
 cid=row['candidate_id'];p=next(x for x in PLAN['records'] if x['candidate_id']==cid);assert row['source_before']==p['before']==PACK['original_records'][cid];assert row['source_after']==p['after']==S['candidates'][cid]==PACK['current_records'][cid];assert row['proof']['facts']==p['facts'];assert row['source_after']['effects']==row['source_before']['effects'];assert row['source_after']['conditions']==row['source_before']['conditions']=={'for_any':['human']};assert n.referenced_records(row['source_after'],S)=={};assert {k:b for k,b in S['slot_bindings'].items() if b['candidate_id']==cid}==p['own_bindings'];old=row['original_compiled'];cp=ROOT/old['file'];assert raw(cp)==old['file_sha256'];assert H(read(cp)['decisions'][old['item']-1])==old['row_sha256'];assert read(cp)['decisions'][old['item']-1]==PACK['historical_compiled_rows'][cid]
 COR['candidates'][cid]['content']['role_evidence']=copy.deepcopy(row['proof'])
EXPECTED='9da30bc08c5459dcee8ee2546070e4ebee364189b3c62d5c5d649931f5285c66';assert H(COR)==EXPECTED
# Manual same-model semantic judgement, authored after actually reading all5 source/proofs and plan05.
manual={9629:'Same selected human owns scrunched nose-bridge short visible creases and KO local tension, noncosmetic region. One expression E plus same-fact facial contour view; no permanent wrinkles, age, optical finish, mechanics or private emotion.',9762:'Inward lip roll and reduced exposed lip area are E; original remains-closed mouth seam is literal PR. KO red lip area scopes exposure, not a selected hue/pigment or optical finish. Same fact facial_geometry preserves complete E/requires.',9834:'Rising mouth corners, cheek lift and narrowed but partly open eyes remain one selected visible response E. Source App explicitly grounds mouth with corners. Original partly-open PR remains; eye_detail E facet and facial_geometry view do not add E/dimensions/owner or happiness.',9853:'Lowered upper lid margins cover more upper iris with comparatively open lower contours; exact partly-open aperture is PR. Both local shape/eye views bind the same full App E; no gaze, sleep, health, new eyes or permanent remodeling.',9868:'Taut-looking relatively thinned lip margins with relatively straight mouth line are selected E. No unsourced closed-seam PR, actual mechanical modulus, permanent lip anatomy, gloss, emotion or age is added.'}
manifest={'schema':'photo-expression5-same-model-peer-manual-review/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','source26_sha256':H(S),'batch_raw_sha256':raw(W/'BATCH-v1.json'),'batch_sha256':H(J),'expected_peer_reviewed_full_research_source_sha256':EXPECTED,'prepared':5,'actual_peer_whole_original_current_pairs_read':5,'actual_peer_fact_read':37,'actual_peer_unit_rows_read':59,'unique_positive_fields':58,'actual_peer_same_fact_views_read':7,'native_proof_or_status_changes':0,'root_acceptance':0,'manual_rows':[{'ordinal':r['ordinal'],'candidate_id':r['candidate_id'],'meaning':manual[r['ordinal']],'status':'peer_source_and_same_fact_modes_supported','proof_sha256':H(r['proof'])} for r in J['records']],'review_boundary':'Same gpt-6.1-sol/high separate task peer. Whole original/current/after, all facts/unit rationale/view anchors/closure/conditions/ownbindings/full used149 specs read. Source26/plan05 before/after/facts exact equality references reuse those actual peer reads; no read credit from the earlier truncated broad displays. Final units are ordinary App E/P and exact original PR plus bounded semantic references; earlier plan05 source_units are proposals, not adopted direct evidence. No alias/tag/unknown metadata anchor, new owner, P from a role word or desired E freezing. Canonical original expression/main_subject/face.expression/set_value/Rx[] and all P/PR retained in same-fact views.','limits':'Root source-only selection is not native/operating acceptance. Explicit source freeze will bind only exact five proof transports in this process. No mandatory permission plan, post-state/pixels/final prompt or independent human/different-model accuracy claim.'}
mp=O/'PEER-REVIEW.json';assert not mp.exists();mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Exact pure previously read fixture definitions; writer top-level598 suite is not executed.
fp=W/'check_v3.py';tree=ast.parse(fp.read_text());nodes=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in {'core','pin','selection','entry'}:nodes.append(node)
 elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'VALUE_ROWS','TEXTS','contract','picked'} for t in node.targets):nodes.append(node)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(fp),'exec'),globals())
oldchecks=read(W/'CHECKS-v3.json')
for r in J['records']:assert core(r['ordinal'])==next(x['base_core'] for x in oldchecks['synthetic_independent_cores'] if x['ordinal']==r['ordinal'])
checks=[];baselines=[]
def check(test,label,**details):
 if not test:raise AssertionError((label,details))
 checks.append({'case':label,**details})
for row in J['records']:
 rec=COR['candidates'][row['candidate_id']];n.validate(rec,CAT,corpus=COR);z=entry(row,core(row['ordinal']));check(not n.admission(z,core(row['ordinal']))['allowed'],'validate_and_compact_not_source_authority',ordinal=row['ordinal'])
authority=n.permission_envelope.freeze_source_authority(COR,expected_snapshot_sha256=EXPECTED,reviewer='/root/review_06250_07250:gpt-6.1-sol:high')
for row in J['records']:
 o=row['ordinal'];cid=row['candidate_id'];rec=COR['candidates'][cid];k=core(o);bids=[bid for bid,b in S['slot_bindings'].items() if b['candidate_id']==cid];assert len(bids)==1;bid=bids[0]
 for form in ['full','compact']:
  z=entry(row,k,binding=bid,view=form);ad=n.admission(z,k,source_data=COR);check(ad['allowed'],'baseline_exact_ownbinding_fullcompact',ordinal=o,form=form,receipt=ad);dims,props,_=n.permission_scope(z,k,source_data=COR);check(dims==['expression'] and props==[{'dimension':'expression','target':'H','property':'face.expression'}],'canonical_E_target_Rx_retained_no_role_projection_mutation',ordinal=o,form=form)
  rr=rec if form=='full' else {**rec,'_semantic_evidence_guard':n.compact(rec,COR)}
  if form=='compact':rr=copy.deepcopy(rr);rr['content'].pop('role_evidence')
  for role in row['proof']['roles']:
   q=n.qualification(CAT[role],rr,source_data=COR);check(q['status']=='eligible','actual_role_source_qualification',ordinal=o,form=form,role=role);check(generator.core_entry_eligible(COR,k,contract,picked,role,z),'actual_per_role_consumer',ordinal=o,form=form,role=role)
   check(not generator.core_entry_eligible(S,k,contract,picked,role,z),'unqualified_source_cannot_supply_view_authority',ordinal=o,form=form,role=role)
   if role!='expression':check(n.qualification(CAT[role],rr,source_data=None)['status']!='eligible','manual_same_fact_view_requires_full_source_authority',ordinal=o,form=form,role=role)
  baselines.append({'ordinal':o,'form':form,'binding_id':bid,'roles':list(row['proof']['roles']),'admission':ad,'effects':props})
  # Isolate owner-human: O gets every anatomy/PR scalar but remains an object; H/Z independently human cannot rescue O.
  bad=copy.deepcopy(k)
  for f in bad['semantic_assertions']:
   if f['axes']['kind']=='fact' and f['axes'].get('owner')=='H' and f['axes'].get('property')!='entity.type':f['axes']['owner']='O'
  for anchor in bad['intent_lock']['semantic_anchors']:
   if anchor['target']=='H':anchor['target']='O'
  pin(bad);zz=entry(row,bad,'O',binding=bid,view=form);check(not n.admission(zz,bad,source_data=COR)['allowed'],'selected_object_not_rescued_by_separate_human',ordinal=o,form=form)
  for role in row['proof']['roles']:check(not generator.core_entry_eligible(COR,bad,contract,picked,role,zz),'all_roles_require_same_selected_human',ordinal=o,form=form,role=role)
  # Missing exact selected-human scalar: no type inference from owner name or category.
  bad=copy.deepcopy(k);f=next(f for f in bad['semantic_assertions'] if f['axes']['kind']=='fact' and f['axes'].get('owner')=='H' and f['axes'].get('property')=='entity.type');bad['semantic_assertions'].remove(f);pin(bad);zz=entry(row,bad,binding=bid,view=form);check(not n.admission(zz,bad)['allowed'],'selected_owner_human_P_missing',ordinal=o,form=form)
  for owner in ['H','HA','B']:
   bad=copy.deepcopy(k);bad['intent_lock']['semantic_anchors'].append({'dimension':'expression','target':owner,'property':'face' if owner=='B' else 'face.expression'});pin(bad);zz=entry(row,bad,binding=bid,view=form)
   for role in row['proof']['roles']:check(not generator.core_entry_eligible(COR,bad,contract,picked,role,zz),'original_owner_alias_parent_property_ancestor_lock',ordinal=o,form=form,role=role,owner=owner)
  bad=copy.deepcopy(k);bad['intent_lock']['open_dimensions']=[];bad['intent_lock']['locked_dimensions'].append('expression');pin(bad);zz=entry(row,bad,binding=bid,view=form)
  for role in row['proof']['roles']:check(not generator.core_entry_eligible(COR,bad,contract,picked,role,zz),'whole_original_expression_lock',ordinal=o,form=form,role=role)
  for f in row['proof']['facts']:
   if f['mode']!='preservation':continue
   bad=copy.deepcopy(k);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes'].get('owner')=='H' and x['axes'].get('property')==f['property'])];pin(bad);zz=entry(row,bad,binding=bid,view=form);check(not n.admission(zz,bad)['allowed'],'original_PR_required_at_selected_owner',ordinal=o,form=form,fact=f['id'])
   for role in row['proof']['roles']:check(not generator.core_entry_eligible(COR,bad,contract,picked,role,zz),'all_role_views_preserve_original_PR',ordinal=o,form=form,role=role,fact=f['id'])
  for case,owner in [('actual_alias','HA'),('disjoint_property_lock','H')]:
   kk=copy.deepcopy(k)
   if case=='disjoint_property_lock':kk['intent_lock']['semantic_anchors'].append({'dimension':'expression','target':'O','property':'face.expression'});pin(kk)
   zz=entry(row,kk,owner,binding=bid,view=form)
   for role in row['proof']['roles']:check(generator.core_entry_eligible(COR,kk,contract,picked,role,zz),'positive_separate_or_alias_control',ordinal=o,form=form,role=role,control=case)
  animal=copy.deepcopy(picked);animal['subject']={'kind':['animal'],'tags':['animal']}
  for role in row['proof']['roles']:check(not generator.core_entry_eligible(COR,k,contract,animal,role,z),'intrinsic_human_AND_binding_human_OR_animal',ordinal=o,form=form,role=role)
mods={}
for name,m in sorted(sys.modules.items()):
 if (name.startswith('photo_') or name=='prompt_generator') and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'raw_sha256':raw(p)}
assert not forbidden
out={'schema':'photo-expression5-fe5b-targeted-peer-controls/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','all_passed':True,'assertion_count':len(checks),'actual_fullcompact_ownbinding_baselines':len(baselines),'actual_per_role_baseline_consumers':sum(len(x['roles']) for x in baselines),'checks':checks,'baselines':baselines,'source26_sha256':H(S),'reviewed_research_source_sha256':EXPECTED,'batch_raw_sha256':raw(W/'BATCH-v1.json'),'batch_sha256':H(J),'generation':str(G),'modules':mods,'fixture_source':{'file':str(fp.relative_to(ROOT)),'raw_sha256':raw(fp),'exact_controlled_cores_file':str((W/'CHECKS-v3.json').relative_to(ROOT)),'raw_sha256_checks':raw(W/'CHECKS-v3.json')},'writer598_suite_rerun':False,'root_acceptance':0,'operating_changes':0,'new_proof_signatures':0,'network_calls':0,'model_calls':0,'Gemini_calls':0,'limits':'Targeted actual engine tests on exact five worker proofs and source26 after manual same-model review. Whole37facts/59units/7views directly reviewed; fixture declarations are reused synthetic caller evidence, not real requester facts or independently observed anatomy. Explicit source transport freeze is separate from validate syntax and is isolated to this process. No permission plan/post-state/final prompt/pixel preservation, production adoption or independent human/different-model accuracy certificate.'}
p=O/'CONTROLS.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checks),'baselines',len(baselines),'perrole',sum(len(x['roles']) for x in baselines));print('PEER-REVIEW',raw(mp));print('CONTROLS',raw(p))
