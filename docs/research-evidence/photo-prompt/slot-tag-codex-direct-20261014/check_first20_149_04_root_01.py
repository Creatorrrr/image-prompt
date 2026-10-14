"""Rerun reviewed actual consumers; add cross-dimension property controls."""
import copy,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
forbidden=[]
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','mlx','sentence_transformers','google','openai','anthropic','requests','httpx','urllib3'}:
   forbidden.append(fullname);raise RuntimeError('Forbidden model/API import: '+fullname)
sys.meta_path.insert(0,DenyModels());sys.dont_write_bytecode=True
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
specifications=[
 ('native_06250_first20_149_04.lighting-check.py','690ef7647287e6a45cd6671d62b424006c951e7e538a6b046b4ca875b89a0ceb',"q=O/'DIAGNOSTIC-LIGHTING07.json'","q=R/'ROOT-FIRST20-LIGHTING04-CONSUMER-RERUN-01.json'"),
 ('native_06250_first20_149_04.reused-check.py','8739b9597d33e4fed894494e62e8fb71bd0f3b938d2a1807b9b7e57ff90867a3',"p=O/'DIAGNOSTIC-REUSED13.json'","p=R/'ROOT-FIRST20-REUSED13-CONSUMER-RERUN-01.json'"),
 ('native_06250_first20_149_04.controls.py','4ebaf55adafb04eef824a9d92c29d863c8c6188330bac66f6cbba4ba670cc62d',"q=O/'CONTROLS.json'","q=R/'ROOT-FIRST20-04-EVIDENCE-CONTROLS-RERUN-01.json'"),
]
spaces=[]
for name,pin,before,after in specifications:
 path=R/'authored'/name;assert raw(path)==pin;code=path.read_text();assert code.count(before)==1
 # Only output destinations differ. All source fixtures/assertions are exact.
 ns={'__name__':'root_controlled_rerun','__file__':str(path)};exec(compile(code.replace(before,after),str(path),'exec'),ns);spaces.append(ns)
l=spaces[0];e,c,layout,g=l['e'],l['c'],l['layout'],l['g'];extras=[]
for ordinal in l['ORDINALS']:
 row=l['B']['records'][ordinal];cid=row['candidate_id'];record=copy.deepcopy(row['source_after']);record['content']['role_evidence']=row['proof'];data={**l['S'],'candidates':{**l['S']['candidates'],cid:record}}
 own=[b for b in data['slot_bindings'].values() if b['candidate_id']==cid];assert len(own)==1
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(record,data)}})]:
  for bid in [None,own[0]['id']]:
   base=l['fixture'](ordinal);entry=c.entry(view,cid,bid,realization_id='base',owner_selections=l['choices'](record,base));dims,properties,graph=e.permission_scope(entry,base)
   for prop in properties:
    core=l['fixture'](ordinal,anchor=('appearance',prop['target'],prop['property']))
    actual=c.entry(view,cid,bid,realization_id='base',owner_selections=l['choices'](record,core));ds,ps,_=e.permission_scope(actual,core)
    assert not e.property_scope_allowed(core,ds,ps,record=actual)
    assert not g.core_entry_eligible(view,core,l['contract'],l['picked'],next(iter(row['proof']['roles'])),actual)
    extras.append(dict(ordinal=ordinal,view=label,binding_id=bid,case='exact_actual_property_locked_under_another_dimension',target=prop['target'],property=prop['property'],allowed=False))
   core=l['fixture'](ordinal,anchor=('appearance','receiver_B','custom.unrelated_property'))
   actual=c.entry(view,cid,bid,realization_id='base',owner_selections=l['choices'](record,core));ds,ps,_=e.permission_scope(actual,core)
   assert e.property_scope_allowed(core,ds,ps,record=actual)
   assert g.core_entry_eligible(view,core,l['contract'],l['picked'],next(iter(row['proof']['roles'])),actual)
   extras.append(dict(ordinal=ordinal,view=label,binding_id=bid,case='independent_unrelated_property_control',allowed=True))
assert len(extras)==140 and not forbidden
G=l['G'];modules={}
for name,m in sys.modules.items():
 if name.startswith('photo_') and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);modules[name]=dict(file=str(p),raw_sha256=raw(p))
out=R/'ROOT-FIRST20-04-CONSUMER-VERIFICATION-01.json'
value=dict(schema='photo-root-actual-consumer-rerun/v1',actor='/root',same_reviewed_worker_suites_rerun=True,
 worker_suite_counts=dict(new7_full_compact_oldbinding=28,reused13_full_compact_oldbinding=52,lighting_original_property_all_receivers_alias_ancestor=448,lighting_missing_wrong_scope_relation_context=344),
 independently_added_controls=140,extra_controls=extras,photo_module_paths=modules,model_API_import_attempts=forbidden,Gemini_calls=0,network_denied=True,
 native_approvals=0,operating_changes=0,output_only_script_replacements=[dict(file=name,raw_sha256=pin,from_text=before,to_text=after) for name,pin,before,after in specifications],
 scope='Actual source/proof consumers with independent synthetic cores. This does not establish real-request semantic completeness, generation, saved pixels, operating adoption or root acceptance.')
with out.open('xb') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
print(json.dumps(dict(worker_matrices=80,worker_lighting_lock_cases=448,worker_lighting_negatives=344,root_additional_controls=140,model_API_import_attempts=0,native_approvals=0,operating_changes=0)))
