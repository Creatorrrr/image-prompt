"""Same-model soil3 peer integration controls; isolated research source only."""
import ast,copy,gzip,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';O=Path(__file__).resolve().parent;D=R/'native-inputs/prepared/review09250-soil3-149-01';W=R/'native_batches/review09250-soil3-149-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/fe5b593c819806a31803e40c620e6f2b28c3b54103f451dd6f38920f2d537258');denied=[]
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:denied.append(fullname);raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as n
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
import photo_native_permission as pe
H=c.digest
raw=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
assert raw(n.__file__)=='722a4be059b95c6a875cffa00d106ba63d7288c16ea8b155f13eb0e4f183104a'
assert raw(pe.__file__)=='98fbdfad68ccc265bb72c06b666429ed1317460cd73a8addd40befab2f847e8e'
M=read(O/'PEER-REVIEW.json');B=read(W/'BATCH.json');I=read(D/'INPUT.json');A=read(D/'ASSIGNMENT.json');P=read(D/'PREPARED-PACKET.json')
assert raw(W/'BATCH.json')==M['batch_expected_raw_sha256'] and H(B)==M['batch_expected_sha256'];assert H(I)==A['input']['sha256'] and raw(D/'INPUT.json')==A['input']['file_sha256'];assert B['input_sha256']==H(I) and B['assignment_sha256']==H(A)
sp=ROOT/I['current_snapshot']['file'];S=json.loads(gzip.decompress(sp.read_bytes()));assert raw(sp)==I['current_snapshot']['file_sha256'] and H(S)==M['source_expected_sha256'];assert H(S['slot_catalog'])==M['catalog_expected_sha256'] and S['slot_catalog']==I['catalog_review']['after'];assert len(S['candidates'])==18250
original=json.loads(gzip.decompress((ROOT/I['original_snapshot']['file']).read_bytes()));assert H(original)==I['original_snapshot']['sha256'];origcompiled=ROOT/B['records'][0]['original_compiled']['file'];compiled=read(origcompiled)
data=copy.deepcopy(S)
for row in B['records']:
 cid=row['candidate_id'];assert row['source_after']==S['candidates'][cid]==P['current_records'][cid];assert row['source_before']==original['candidates'][cid]==P['original_records'][cid];assert row['source_after']['effects']==row['source_before']['effects'];assert row['source_after']['conditions']==row['source_before']['conditions']=={};z=copy.deepcopy(row['source_after']);del z['content']['application_contract'];assert z==row['source_before'];assert row['dependency_records']==row['reference_bindings']=={};assert n.referenced_records(row['source_after'],S)=={}
 old=row['original_compiled'];assert raw(origcompiled)==old['file_sha256'] and H(compiled['decisions'][old['item']-1])==old['row_sha256'];assert row['proof']['review']['original_review']['artifact']==str(origcompiled.relative_to(ROOT))+'#item='+str(old['item']);assert H(row['proof'])==next(x['proof_sha256'] for x in M['rows'] if x['candidate_id']==cid)
 data['candidates'][cid]['content']['role_evidence']=copy.deepcopy(row['proof'])
assert H(data)==M['reviewed_research_snapshot_expected_sha256']
assert [k for k in S if S[k]!=data[k]]==['candidates'];assert {cid for cid in S['candidates'] if S['candidates'][cid]!=data['candidates'][cid]}==set(I['ids'])
# Reuse only exact manually read pure fixture definitions; do not run writer top-level code.
fp=R/'authored/native_soil3_09250_149_01.check-v3.py';tree=ast.parse(fp.read_text());wanted={'fixture','selections','contract','picked','entry_for'};nodes=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in wanted:nodes.append(node)
 elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'CORE_FACTS','BROKEN'} for t in node.targets):nodes.append(node)
assert {node.name for node in nodes if isinstance(node,ast.FunctionDef)}==wanted
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(fp), 'exec'),globals())
C=read(W/'CONTROLLED-CORES-v1.json')
for x in C['cores']:assert fixture(x['ordinal'])==x['core']
checks=[];baselines=[];negative=[]
def check(test,label,**details):
 if not test:raise AssertionError((label,details))
 checks.append({'test':label,**details})
def reject(label,fn,**details):
 try:fn()
 except (ValueError,TypeError,KeyError) as e:check(True,label,error=str(e),**details);return str(e)
 raise AssertionError(('expected reject',label,details))
def ent(view,rec,core,bid=None,owner='surface_A',choice=True,full=False,selection=None):
 e=c.entry(view,rec['id'],bid,realization_id='base',**({'owner_selections':selection if selection is not None else selections(rec,core,owner)} if choice else {}))
 if full:e.pop('_semantic_evidence_guard',None)
 return e
# Exact expected current research source was manually selected in a separate manifest before this process.
for row in B['records']:
 rec=data['candidates'][row['candidate_id']];core=fixture(row['ordinal']);n.validate(rec,data['slot_catalog'],corpus=data);guard=layout.guard_record(rec,data)
 for label,view,full in [('full',data,True),('compact',{**data,'candidates':{**data['candidates'],rec['id']:guard}},False)]:
  e=ent(view,rec,core,full=full);r=n.admission(e,core,source_data=data);check(not r['allowed'] and r['reason']=='source_bound_native_transport_required','validate_and_compact_issue_no_authority',ordinal=row['ordinal'],form=label,receipt=r)
  check(n.qualification(data['slot_catalog']['texture'],view['candidates'][rec['id']],source_data=data)['reason']=='independent_source_transport_authority_required','qualification_before_freeze_denied',ordinal=row['ordinal'],form=label)
  check(not g.core_entry_eligible(view,core,contract(),picked(),'texture',e),'consumer_before_freeze_denied',ordinal=row['ordinal'],form=label)
reject('wrong_independent_snapshot_freeze_denied',lambda:pe.freeze_source_authority(data,expected_snapshot_sha256='0'*64,reviewer=M['reviewer']))
for row in B['records']:
 reject('wrong_freeze_has_not_issued_transport',lambda row=row:pe.transport(data['candidates'][row['candidate_id']]),ordinal=row['ordinal'])
authority=pe.freeze_source_authority(data,expected_snapshot_sha256=M['reviewed_research_snapshot_expected_sha256'],reviewer=M['reviewer'])
reject('source_handle_not_serializable',lambda:json.dumps(authority))
for row in B['records']:
 o=row['ordinal'];cid=row['candidate_id'];rec=data['candidates'][cid];core=fixture(o);own=[b for b in S['slot_bindings'].values() if b['candidate_id']==cid];check(len(own)==1 and own[0]['slot_id']=='texture' and own[0]['conditions']=={'subject_applicability':{}} and own[0]['weight']==.45,'exact_ownbinding',ordinal=o,binding=own[0]);check(not any(x.get('axes',{}).get('property')=='surface_structure' for x in core['semantic_assertions']),'desired_texture_not_in_core',ordinal=o)
 check(pe.transport(rec)['qualification_sha256']==H(row['proof']),'explicit_freeze_issued_exact_source_transport',ordinal=o)
 compact=layout.guard_record(rec,data);view={**data,'candidates':{**data['candidates'],cid:compact}}
 for label,v,full in [('full',data,True),('compact',view,False)]:
  for bid in [None,own[0]['id']]:
   e=ent(v,rec,core,bid,full=full);receipt=n.admission(e,core,source_data=data);check(receipt['allowed'] and not receipt.get('search_only'),'baseline_after_explicit_freeze',ordinal=o,form=label,binding=bid)
   check(len(receipt['resolved_frozen_facts'])==(5 if o==11595 else 4) and {f['owner'] for f in receipt['resolved_frozen_facts']}=={'surface_A'},'same_actual_face_all_P_PR',ordinal=o,form=label,binding=bid)
   dims,props,_=n.permission_scope(e,core,source_data=data);check(dims==['material'] and props==[{'dimension':'material','target':'surface_A','property':'surface_structure'}],'original_target_E_and_Rx_empty_resolve_same_face',ordinal=o,form=label,binding=bid)
   for role in ['texture','surface_material']:
    q=n.qualification(data['slot_catalog'][role],v['candidates'][cid],source_data=data);check(q['status']=='eligible' and q['support_modes']==(['effect'] if role=='texture' else ['preservation']),'exact_role_mode',ordinal=o,form=label,role=role,binding=bid)
    check(g.core_entry_eligible(v,core,contract(),picked(),role,e),'actual_role_consumer_baseline',ordinal=o,form=label,role=role,binding=bid)
   baselines.append({'ordinal':o,'form':label,'binding_id':bid,'receipt':receipt,'actual_effects':props,'per_role_consumers':['texture','surface_material']})
   nochoice=ent(v,rec,core,bid,choice=False,full=full);check(not n.admission(nochoice,core,source_data=data)['allowed'],'no_implicit_selected_owner',ordinal=o,form=label,binding=bid)
   fields=['presence','kind','exposure','soil']+(['broken'] if o==11595 else [])
   for field in fields:
    for defect in ['missing_'+field,'other_owner_'+field]:
     badcore=fixture(o,defect=defect);bad=ent(v,rec,badcore,bid,full=full);ad=n.admission(bad,badcore,source_data=data);check(not ad['allowed'],'independent_same_owner_P_PR_required',ordinal=o,form=label,binding=bid,defect=defect,reason=ad['reason'])
     for role in ['texture','surface_material']:check(not g.core_entry_eligible(v,badcore,contract(),picked(),role,bad),'each_role_retains_all_P_PR',ordinal=o,form=label,binding=bid,defect=defect,role=role)
   cases=[('original_atomic_property',('material','surface_A','surface_structure'),{}),('parent_owner',('material','parent_A','surface_structure'),{'part':True}),('alias_owner',('material','alias_A','surface_structure'),{'alias':True}),('owner_wide',('material','surface_A','*'),{}),('bounded_prefix',('material','surface_A','surface*'),{})]
   for case,anchor,opts in cases:
    locked=fixture(o,anchor=anchor,**opts);le=ent(v,rec,locked,bid,full=full);ld,lp,_=n.permission_scope(le,locked,source_data=data);check(not n.property_scope_allowed(locked,ld,lp,record=le),'canonical_actual_owner_lock',ordinal=o,form=label,binding=bid,case=case)
    for role in ['texture','surface_material']:check(not g.core_entry_eligible(v,locked,contract(),picked(),role,le),'each_role_cannot_evade_original_lock',ordinal=o,form=label,binding=bid,case=case,role=role)
   whole=fixture(o,whole=True);we=ent(v,rec,whole,bid,full=full)
   for role in ['texture','surface_material']:check(not g.core_entry_eligible(v,whole,contract(),picked(),role,we),'whole_material_lock',ordinal=o,form=label,binding=bid,role=role)
   for case,cc,owner in [('separate_disjoint_target',fixture(o,anchor=('material','other_A','surface_structure')),'surface_A'),('same_owner_other_property',fixture(o,anchor=('material','surface_A','unrelated.sibling')),'surface_A'),('alias_same_owner_selection',fixture(o,alias=True),'alias_A'),('second_eligible_owner_not_defaulted',fixture(o,second_eligible=True),'surface_B')]:
    ce=ent(v,rec,cc,bid,owner=owner,full=full);check(n.admission(ce,cc,source_data=data)['allowed'],'positive_separate_control',ordinal=o,form=label,binding=bid,case=case)
    for role in ['texture','surface_material']:check(g.core_entry_eligible(v,cc,contract(),picked(),role,ce),'actual_consumer_separate_control',ordinal=o,form=label,binding=bid,case=case,role=role)
  # Changed compact self-hash is still not independently frozen transport.
  forged=copy.deepcopy(compact);proof=forged['_semantic_evidence_guard'];next(f for f in proof['facts'] if f['mode']=='effect')['property']='surface.texture';proof['effect_sets']['base']['properties'][0]['property']='surface.texture';proof['compact_sha256']=H({k:v for k,v in proof.items() if k!='compact_sha256'});fv={**data,'candidates':{**data['candidates'],cid:forged}};fe=ent(fv,rec,core)
  check(not n.admission(fe,core,source_data=data)['allowed'],'self_rehashed_compact_has_no_source_authority',ordinal=o)
 # Existing old binding remains an independent AND layer on both roles.
 guarded=copy.deepcopy(data);guarded['slot_bindings'][own[0]['id']]['conditions']={'subject_applicability':{'deny_domains':['science_inspection']}}
 for full in [True,False]:
  v=guarded if full else {**guarded,'candidates':{**guarded['candidates'],cid:layout.guard_record(rec,guarded)}};e=ent(v,rec,core,own[0]['id'],full=full)
  check(n.admission(e,core,source_data=data)['allowed'],'isolated_binding_does_not_replace_native_obligations',ordinal=o,full=full)
  for role in ['texture','surface_material']:check(not g.core_entry_eligible(v,core,contract(domain=['science_inspection']),picked(),role,e),'original_binding_AND_consumed_for_each_role',ordinal=o,full=full,role=role)
 for prop in ['surface.material','surface.exposure']:
  check(not n.property_scope_allowed(core,['material'],[{'dimension':'material','target':'surface_A','property':prop}]),'raw_other_mutation_of_required_or_preserved_property_denied',ordinal=o,property=prop)
# Two roots can share one exact selection document; conflicting actual same-face values reject.
for full in [True,False]:
 core=fixture(11595,second_eligible=True);rows=B['records'][:2];recs=[data['candidates'][row['candidate_id']] for row in rows]
 for distinct in [False,True]:
  ss=selections(recs[0],core);ss['entries']+=selections(recs[1],core,'surface_B' if distinct else 'surface_A')['entries'];entries=[]
  for rec in recs:
   v=data if full else {**data,'candidates':{**data['candidates'],rec['id']:layout.guard_record(rec,data)}};entries.append(ent(v,rec,core,full=full,selection=ss))
  if distinct:n.validate_joint_effect_assignments(entries,core);check(True,'joint_disjoint_faces_same_property_allowed',full=full)
  else:reject('joint_same_face_conflicting_texture_values_denied',lambda:n.validate_joint_effect_assignments(entries,core),full=full)
modules={}
for name,mod in sorted(sys.modules.items()):
 if (name.startswith('photo_') or name.startswith('_photo_precore') or name=='prompt_generator') and getattr(mod,'__file__',None):
  p=Path(mod.__file__).resolve();check(p.is_relative_to(G),'actual_module_frozen_generation',module=name);modules[name]={'file':str(p),'raw_sha256':raw(p)}
check(not denied,'no_forbidden_provider_or_local_model_imports')
research=O/'REVIEWED-RESEARCH-SOURCE.json.gz';assert not research.exists();research.write_bytes(gzip.compress(c.canonical_bytes(data),mtime=0))
result={'schema':'photo-soil3-same-model-peer-integration-controls/v1','reviewer':M['reviewer'],'model':'gpt-6.1-sol','reasoning_effort':'high','source_sha256':H(S),'reviewed_research_source_sha256':H(data),'reviewed_research_source_file':str(research.relative_to(ROOT)),'reviewed_research_source_raw_sha256':raw(research),'catalog_sha256':H(S['slot_catalog']),'batch_raw_sha256':raw(W/'BATCH.json'),'batch_sha256':H(B),'peer_review_raw_sha256':raw(O/'PEER-REVIEW.json'),'actual_assertion_count':len(checks),'full_compact_ownbinding_baselines':len(baselines),'per_role_consumer_baselines':2*len(baselines),'checks':checks,'baselines':baselines,'authority':'Explicit same-model peer freeze_source_authority after independent expected reviewed research snapshot and actual3 source/proof review. n.validate/compact before freeze issue0 transport. No serialized or self-rehashed payload grants authority. Only this isolated process research transport handles issued.','fixture_reuse':{'file':str(fp.relative_to(ROOT)),'raw_sha256':raw(fp),'frozen_cores_file':str((W/'CONTROLLED-CORES-v1.json').relative_to(ROOT)),'frozen_cores_raw_sha256':raw(W/'CONTROLLED-CORES-v1.json'),'method':'Only exact read CORE_FACTS/BROKEN and pure fixture/selectors functions were AST-selected without running writer top level; all3 reconstructed baselines equal frozen CONTROLLED-CORES bytes as JSON. Existing controlled synthetic caller semantics reused; not new real requester or independently observed source facts.'},'generation':str(G),'modules':modules,'bulk_new_unique_reads':0,'same_model_peer_source_read_count':3,'root_acceptance':0,'production_changes':0,'operating_qualified':0,'model_calls':0,'network_calls':0,'Gemini_calls':0,'forbidden_import_attempts':denied,'limits':['This targeted new-generation peer suite does not claim to rerun all writer1155 assertions. It directly tests actual full-proof entries and compact entries on controlled typed core fixtures, with no provider/image/pixel/final composed output.','surface_structure is atomic. No proper dotted property ancestor exists; exact atomic, owner-wide and bounded wildcard, actual parent-owner/alias and whole-material locks were tested without property renaming.','Rx[] is intentional target-only scope: original source target selected_surface maps solely to selected actual face. No additional receiver entity is invented.','Source25 has no permission_envelope opt-in; no mandatory permission inventory/plan or after-state scalar/pixel preservation qualification is claimed. Literal soil PR and exposure PR/P are checked as frozen requirements/current locks by actual native admission/consumer.','Isolated stricter own-binding copies test conjunctive guard consumption and do not change the selected source, proofs or operating binding policy.','Same gpt-6.1-sol/high peer; no independent human/different-model accuracy certification. Root acceptance remains separate.']}
p=O/'ACTUAL-CONTROLS.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checks),'baselines',len(baselines),'roles',len(baselines)*2);print(p.name,raw(p));print(research.name,raw(research),H(data))
