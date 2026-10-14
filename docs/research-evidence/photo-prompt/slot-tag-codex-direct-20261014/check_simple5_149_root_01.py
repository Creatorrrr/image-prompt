"""Rerun the reviewed actual-source suite and add independent lock controls."""
import copy,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';forbidden=[]
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:
   forbidden.append(fullname);raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True
p=R/'authored/native_05250_simple5-source96.check-v1.py';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='fdb0ea0fff17dae462f41833286472b2110605f3c97eff6b57a278bff53751ad'
code=raw.decode();replacements=[("path=O/'ACTUAL-CHECKS-v1.json'","path=R/'ROOT-SIMPLE5-ACTUAL-CHECKS-RERUN-01.json'"),("p=O/'COMPLETION-v1.json'","p=R/'ROOT-SIMPLE5-COMPLETION-RERUN-01.json'")]
for old,new in replacements:assert code.count(old)==1;code=code.replace(old,new)
ns={'__name__':'root_actual_source_rerun','__file__':str(p)};exec(compile(code,str(p),'exec'),ns)
n,c,g,layout=ns['n'],ns['c'],ns['g'],ns['layout'];results=[];assertions=0
for row in ns['B']['records']:
 ordinal=row['ordinal'];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];data={**ns['S'],'candidates':{**ns['S']['candidates'],cid:rec}}
 own=[v for v in data['slot_bindings'].values() if v['candidate_id']==cid];assert len(own)==1
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}})]:
  for bid in [None,own[0]['id']]:
   entry=c.entry(view,cid,bid,realization_id='base');owner='image_A' if ordinal==6220 else 'scene_A'
   for dim,prop in ns['EXPECTED'][ordinal]:
    core=ns['fixture'](ordinal,anchor=('appearance',owner,prop));dims,props,_=n.permission_scope(entry,core)
    assert not n.property_scope_allowed(core,dims,props,record=entry)
    assert not g.core_entry_eligible(view,core,ns['contract_for'](ordinal),ns['picked'](ordinal),next(iter(row['proof']['roles'])),entry);assertions+=2
    results.append(dict(ordinal=ordinal,view=label,binding_id=bid,case='same_actual_property_locked_under_another_dimension',property=prop,allowed=False))
   core=ns['fixture'](ordinal,anchor=('appearance',owner,'custom.root_unrelated_property'));dims,props,_=n.permission_scope(entry,core)
   assert n.property_scope_allowed(core,dims,props,record=entry)
   assert g.core_entry_eligible(view,core,ns['contract_for'](ordinal),ns['picked'](ordinal),next(iter(row['proof']['roles'])),entry);assertions+=2
   results.append(dict(ordinal=ordinal,view=label,binding_id=bid,case='same_owner_unrelated_property_control',allowed=True))
assert len(results)==48 and assertions==96 and not forbidden
modules={}
for name,m in sys.modules.items():
 if (name.startswith('photo_') or name in {'prompt_generator','audit_composed_prompt'}) and getattr(m,'__file__',None):
  path=Path(m.__file__).resolve();assert path.is_relative_to(ns['G']);modules[name]=dict(file=str(path),raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
out=R/'ROOT-SIMPLE5-CONSUMER-VERIFICATION-01.json';value=dict(schema='photo-root-simple5-consumer-rerun/v1',actor='/root',reviewed_writer_suite_actual_assertions=589,full_compact_ownbinding_baselines=20,independently_added_cases=48,independently_added_assertions=96,extra_controls=results,actual_module_paths=modules,source_record_native_approvals_created=0,Gemini_calls=0,model_API_import_attempts=forbidden,network_denied=True,operating_changes=0,script_raw_sha256=hashlib.sha256(raw).hexdigest(),output_destination_only_replacements=replacements,scope='Exact source96 native qualification/admission/permission/consumer with controlled source fixtures. Independent extra property controls reuse the reviewed fixture constructor. No real requester/source-span truth, complete joint candidate union, final output preservation, runtime, pixels or root acceptance is inferred.')
with out.open('xb')as f:f.write(c.canonical_bytes(value)+b'\n')
print(json.dumps(dict(writer_assertions=589,root_extra_cases=48,root_extra_assertions=96,model_API_import_attempts=0,operating_changes=0)))
