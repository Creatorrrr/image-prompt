"""Pin the independently finished current release, without restoring old user state."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,os,sys
import run
from history_state import new,pointers
E=run.E;ROOT=run.ROOT;SKILL=run.SKILL;state=run.state
b=run.baseline();t=state.read(E/'TARGETS.json');foreign=ROOT/'docs/research-evidence/photo-prompt/candidate-contract-source-repair-20261020'
finished=state.read(foreign/'FINAL.json');assert finished['status']=='PASS' and finished['shared_CURRENT_writes']==0
cfg=state.read(SKILL/'retrieval-runtime.json');assert cfg['generation_id']==finished['installed_generation_id'] and cfg['native_generation_id']==finished['installed_native_generation_id']
paths=set(b['files']);repos={}
for work in state.worktrees():
 dirty={p:s for p,s in state.status(work).items() if work!=ROOT or not run.owned(p)}
 index=Path(state.git(work,'rev-parse','--git-path','index').decode().strip());index=index if index.is_absolute() else work/index
 row={'head':state.git(work,'rev-parse','HEAD').decode().strip(),'status':dirty,'staged':state.git(work,'diff','--cached','--raw','-z').decode(),'index_path':str(index),'index_sha256':state.sha(index)}
 assert row['head']==b['repositories'][str(work)]['head'] and row['index_sha256']==b['repositories'][str(work)]['index_sha256'] and not row['staged'];repos[str(work)]=row
 tracked=set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
 paths.update(str(work/p) for p in tracked|set(dirty) if work!=ROOT or not run.owned(p))
store=state.SHARED/cfg['store_subdirectory'];closure=[store/'generations'/cfg['native_generation_id'],store/'h-f2-generations'/cfg['generation_id'],store/'receipts',store/'h-f2-receipts',store/'receipt-index']
for root in closure:
 for directory,dirs,files in os.walk(root,followlinks=False):
  for name in list(dirs):
   p=Path(directory)/name
   if p.is_symlink():paths.add(str(p));dirs.remove(name)
   elif name=='__pycache__':dirs.remove(name)
  paths.update(str(Path(directory)/n) for n in files)
current=pointers();assert current==b['pointers'];paths.update(current)
print('pinning current completed release and original protected paths:',len(paths),flush=True)
ordered=sorted(paths)
with ThreadPoolExecutor(max_workers=4) as pool:actual=dict(zip(ordered,pool.map(state.stamp,ordered)))
changes={p:{'before':s,'after':actual[p]} for p,s in b['files'].items() if s!=actual[p]}
allowed={str(SKILL/'retrieval-runtime.json'),*[str(foreign/x) for x in ('staged-managed-delivery.log','staged-managed/run/workflow.json','verify_repair_invariants.py','SOURCE-RESOLUTION-VERIFICATION.json')]}
new(E/'OPERATING-SNAPSHOT-REVIEW.json.gz',{'files':actual,'repositories':repos,'pointers':current,'changes':changes})
assert set(changes)<=allowed, list(changes)
assert all(actual[str(ROOT/p)]==s for p,s in t['original'].items())
assert all(actual[p]==b['files'][p] for p in current)
new(E/'OPERATING-BASELINE-DELTA.json.gz',{'parent_baseline_sha256':state.sha(E/'BASELINE-DELTA.json.gz'),'preexisting_external_replacements':changes,
 'additional_files':{p:actual[p] for p in paths if p not in b['files']},'repositories':repos,'pointers':current,
 'installed':{'config':cfg,'store':str(store),'native':str(closure[0]),'hroot':str(closure[1])},
 'fixture':str(foreign/'installed-managed/run'),'foreign_final_sha256':state.sha(foreign/'FINAL.json'),
 'all_8_cleanup_source_bytes_still_match_qualification':True,'original_CURRENT_bytes_equal':True})
new(E/'OPERATING-BOUNDARY.json',{'status':'PASS','reason':'Another task finished source repair and installed new release while cleanup was being qualified; preserve that uncommitted selection and data',
 'previous_config':state.read(E/'BASELINE-DELTA.json.gz').get('previous_config',state.read(run.PARENT/'BASELINE-DELTA.json.gz').get('previous_config')),
 'new_config':cfg,'changed_preexisting_paths':sorted(changes),'original_CURRENT_unchanged':True,'source_targets_unchanged':True,
 'protected_paths':len(paths),'previous_current_and_generations_preserved':True,'foreign_final_sha256':state.sha(foreign/'FINAL.json'),
 'new_snapshot_does_not_erase_earlier_failed_evidence':True,'cleanup_source_changes':0,'Gemini_calls':0,'CURRENT_writes':0})
print('current installed boundary pinned; protected',len(paths),'external replacements',list(changes),flush=True)
