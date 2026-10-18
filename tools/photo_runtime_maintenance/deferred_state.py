"""Frozen protection and exact targets for the second, bounded cleanup."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

import state

ROOT = state.ROOT
E = ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-execution-20261019'
INPUT = ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-followup-20261019/ANALYSIS.json'
PLAN = 'docs/plans/photo-deferred-bytecode-and-shard-cleanup.md'
PREFIX = str(E.relative_to(ROOT))+'/'
TOOLS = {'tools/photo_runtime_maintenance/'+name for name in (
    'deferred_state.py','deferred_restore.py','deferred_checks.py','deferred_replay.py',
    'deferred_gc.py','test_deferred_restore.py')}
INPUT_SHA = '9b777b88118e141465a474ecb96a59ad9836878ea6de5197c67fd4cb4bfc559c'


def owned(relative):
    return relative == PLAN or relative in TOOLS or relative.startswith(PREFIX)


def freeze():
    if (E/'BASELINE.json.gz').exists():
        raise ValueError('execution baseline already exists')
    if state.sha(INPUT) != INPUT_SHA:
        raise ValueError('reviewed input changed')
    if state.git(ROOT,'diff','--cached','--name-only'):
        raise ValueError('preserve the existing staged index; no staging permitted')
    analysis = state.read(INPUT)
    repositories = {}
    protected = set()
    for root in state.worktrees():
        dirty = state.status(root)
        if root == ROOT:
            dirty = {p:s for p,s in dirty.items() if not owned(p)}
        tracked = set(state.git(root,'ls-files','-z').decode().split('\0'))-{''}
        index = state.git(root,'rev-parse','--path-format=absolute','--git-path','index').decode().strip()
        repositories[str(root)] = {'head':state.git(root,'rev-parse','HEAD').decode().strip(),
            'status':dirty,'index_sha256':state.sha(index),'index_path':index}
        protected.update(str(root/p) for p in tracked|set(dirty)
                         if root != ROOT or not owned(p))
    old = state.read(state.EVIDENCE/'BASELINE.json.gz')
    protected.update(old['files'])
    for name in ('ADDITIONAL-PROTECTED.json.gz','FIXTURE-PROTECTED.json.gz'):
        protected.update(state.read(state.EVIDENCE/name))
    for folder in (state.EVIDENCE, INPUT.parent, ROOT/'docs/research-archives/photo-prompt'):
        protected.update(str(p) for p in state.files(folder))
    command=['rg','--files','--hidden','--no-ignore','-g','CURRENT.json','-g','!**/.git/**',
             '-g','!**/.runtime/**','-g','!**/.venv/**','-g','!**/node_modules/**',
             *map(str,[*state.worktrees(),state.SHARED.parent])]
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    pointers=sorted(set(result.stdout.splitlines()))
    protected.update(pointers)
    for row in analysis['shards']:
        if row['duplicate']:
            protected.update(str(p) for p in state.files(row['duplicate']['generation']))
    for row in analysis['alternate_generation_integrity']:
        protected.update(str(p) for p in state.files(Path(row['manifest']).parent))
    for row in analysis['bytecodes']:
        protected.add(str(ROOT/row['path']))
    dirty = set(repositories[str(ROOT)]['status'])
    targets=[]
    for row in analysis['bytecodes']:
        if row['status']!='EXACT':continue
        path=ROOT/row['path']; stamp=state.stamp(path)
        targets.append({'path':row['path'],'group':'bytecode','expected_sha256':row['cache_sha256'],
                        'before':stamp,'analysis':row,'preflight':'READY' if stamp.get('sha256')==row['cache_sha256'] else 'DEFER_CHANGED'})
    shards=[]
    for row in analysis['shards']:
        if row['action']!='CONDITIONAL_DEDUPLICATION_CANDIDATE':continue
        folder=ROOT/row['path'];batch=1 if row['priority']=='first shard absence-validation batch' else 2
        shards.append({k:v for k,v in row.items() if k!='live_original_hashes'}|{'batch':batch})
        for name,sha in sorted(row['live_original_hashes'].items()):
            rel=row['path']+'/'+name;stamp=state.stamp(ROOT/rel)
            targets.append({'path':rel,'group':row['id'],'batch':batch,'expected_sha256':sha,
                            'before':stamp,'preflight':'READY' if stamp.get('sha256')==sha else 'DEFER_CHANGED'})
    if len(targets)!=5815 or len(shards)!=8:
        raise ValueError('frozen target ceiling differs')
    if dirty & {r['path'] for r in targets}:
        raise ValueError('targets overlap original dirty work')
    protected.update(str(ROOT/r['path']) for r in targets)
    print('hashing frozen protection:',len(protected),'paths',flush=True)
    paths=sorted(protected)
    with ThreadPoolExecutor(max_workers=4) as pool:
        stamps=dict(zip(paths,pool.map(state.stamp,paths)))
    state.write(E/'BASELINE.json.gz',{'schema':'photo-deferred-cleanup-baseline/v1',
        'repositories':repositories,'files':stamps,'pointers':pointers,'input_sha256':INPUT_SHA,
        'installed':state.read(ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json'),
        'owned_preexisting_plan':PLAN})
    state.write(E/'TARGETS.json.gz',{'schema':'photo-deferred-cleanup-targets/v1','targets':targets,'shards':shards,
        'excluded':'314 bytecodes; 3 dirty shards; rollback shard; all sealed generations and other work'})
    state.write(E/'REMOVED.json',[])
    state.write(E/'STAGE01.json',{'status':'PASS','protected_files':len(stamps),'CURRENT_count':len(pointers),
        'target_files':len(targets),'target_bytecodes':45,'target_shards':8,
        'original_dirty_paths':{r:len(v['status']) for r,v in repositories.items()},
        'changed_targets_deferred':[r['path'] for r in targets if r['preflight']!='READY'],
        'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 1 protection frozen;',len(pointers),'CURRENT',flush=True)


def verify(output=None):
    b=state.read(E/'BASELINE.json.gz');removed=set(state.read(E/'REMOVED.json'))
    targets={r['path']:r for r in state.read(E/'TARGETS.json.gz')['targets']}
    if not removed<=set(targets):raise ValueError('removal allowlist expanded')
    failures=[];paths=[]
    for path in b['files']:
        p=Path(path)
        rel=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
        if rel is not None and (owned(rel) or rel in removed):continue
        paths.append(path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(paths,pool.map(state.stamp,paths)):
            if actual!=b['files'][path]:failures.append(path)
    for rel in removed:
        if (ROOT/rel).exists() or (ROOT/rel).is_symlink():failures.append(rel+': reappeared')
    for root,row in b['repositories'].items():
        current=state.status(root)
        for rel,code in row['status'].items():
            if current.get(rel)!=code:failures.append(root+'/'+rel+': dirty status changed')
        if root!=str(ROOT):
            if state.git(root,'rev-parse','HEAD').decode().strip()!=row['head']:failures.append(root+': HEAD changed')
            if state.sha(row['index_path'])!=row['index_sha256']:failures.append(root+': index changed')
        else:
            for rel in current:
                if rel not in row['status'] and rel not in removed and not owned(rel):
                    failures.append(rel+': unexpected working change')
    result={'status':'PASS' if not failures else 'FAIL','protected_files_checked':len(paths),
        'CURRENT_count':len(b['pointers']),'removed_files':len(removed),'failures':failures,
        'Gemini_calls':0,'CURRENT_writes':0}
    if output:state.write(output,result)
    print(result,flush=True)
    if failures:raise ValueError('protected state changed')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['freeze','verify']);parser.add_argument('--output',type=Path)
    args=parser.parse_args();freeze() if args.command=='freeze' else verify(args.output)
