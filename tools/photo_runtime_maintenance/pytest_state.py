"""Bounded 65-cache cleanup state; reuse immutable protection, store only additions."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import history_state
import state

ROOT = state.ROOT
E = ROOT/'docs/research-evidence/photo-prompt/runtime-pytest-cleanup-20261019'
INPUT = ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-final-deferred-20261019'
INPUTS = {'ANALYSIS.json':'7b3a0d92a707f99758670f101d83d66d34a8b0534d42695ab68cc57634f0332b',
          'PYTEST-PROBE.json':'81bca30174b9c3d0417984288e89ce1553c767621c8ed036308414cc3a90e510',
          'PYTEST-RECHECK.json':'560c2bc3d07061a6de575c10427b94068542002c90cc7fef07615a996d8c75d7'}
PLAN = 'docs/plans/photo-pytest-bytecode-cleanup.md'
TOOLS = {'tools/photo_runtime_maintenance/'+n for n in ('pytest_state.py','pytest_proof.py',
         'pytest_restore.py','pytest_checks.py','pytest_gc.py','test_pytest_cleanup.py')}
new = history_state.new
pointers = history_state.pointers


def owned(name):
    return name == PLAN or name in TOOLS or name.startswith(str(E.relative_to(ROOT))+'/')


def load_baseline():
    lock=state.read(E/'BASELINE-DELTA.json.gz')
    path=ROOT/lock['base_path']
    if state.sha(path)!=lock['base_sha256']:raise ValueError('original protection changed')
    base=state.read(path)
    files={p:s for p,s in base['files'].items() if p not in lock['previous_absent']}
    files.update(lock['additional_files'])
    repositories={}
    for root,row in lock['repositories'].items():
        dirty=dict(base['repositories'][root]['status'])
        for name in row['status_removed']:dirty.pop(name)
        dirty.update(row['status_added'])
        repositories[root]={**row,'status':dirty}
    return {**lock,'files':files,'repositories':repositories}


def targets():return state.read(E/'TARGETS.json.gz')['targets']


def freeze():
    if (E/'BASELINE-DELTA.json.gz').exists():raise FileExistsError('already frozen')
    for name,digest in INPUTS.items():
        if state.sha(INPUT/name)!=digest:raise ValueError('reviewed input changed')
    analysis=state.read(INPUT/'ANALYSIS.json');probe=state.read(INPUT/'PYTEST-PROBE.json')
    checked=state.read(INPUT/'PYTEST-RECHECK.json')
    names={r['path'] for r in analysis['review'] if r['decision']=='CANDIDATE_AFTER_ABSENCE_AND_RECOVERY_GATES'}
    exact={r['path']:r for r in probe['rows'] if r['matches']}
    if names!=set(exact) or names!={r['path'] for r in checked['rows'] if r['equal']}:
        raise ValueError('candidate sets differ')
    if len(names)!=65 or sum(r['bytes'] for r in exact.values())!=807566:raise ValueError('budget changed')
    base_path=history_state.E/'BASELINE.json.gz';base=state.read(base_path)
    previous={str(ROOT/p) for p in state.read(history_state.E/'REMOVED.json')}
    if len(previous)!=228:raise ValueError('earlier cleanup changed')
    paths=set(base['files'])-previous;repos={};full_status={}
    for root in state.worktrees():
        dirty=state.status(root)
        if root==ROOT:dirty={p:s for p,s in dirty.items() if not owned(p)}
        full_status[str(root)]=dirty
        old=base['repositories'][str(root)]['status']
        index=state.git(root,'rev-parse','--path-format=absolute','--git-path','index').decode().strip()
        repos[str(root)]={'head':state.git(root,'rev-parse','HEAD').decode().strip(),
            'staged':state.git(root,'diff','--cached','--raw','-z').decode(),
            'index_path':index,'index_sha256':state.sha(index),
            'status_removed':sorted(set(old)-set(dirty)),
            'status_added':{p:s for p,s in dirty.items() if old.get(p)!=s}}
        tracked=set(state.git(root,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(root/p) for p in tracked|set(dirty) if root!=ROOT or not owned(p))
    if repos[str(ROOT)]['staged']:raise ValueError('existing staging must stay untouched')
    current=pointers();paths.update(current)
    print('checking',len(paths),'protected paths; delta-only storage',flush=True)
    paths=sorted(paths)
    with ThreadPoolExecutor(max_workers=4) as pool:actual=dict(zip(paths,pool.map(state.stamp,paths)))
    drift=[p for p,s in base['files'].items() if p not in previous and actual[p]!=s]
    if drift:raise ValueError('protected state drift: '+str(drift[:10]))
    if any(Path(p).exists() for p in previous):raise ValueError('old cache reappeared')
    rows=[];original={r['path']:r for r in analysis['bytecodes']}
    for name,row in sorted(exact.items()):
        before=actual[str(ROOT/name)];source_before=state.stamp(ROOT/row['source'])
        ready=(before['sha256']==row['sha256'] and before['kind']=='file' and before['links']==1
            and name not in full_status[str(ROOT)] and row['source'] not in full_status[str(ROOT)])
        spec={**row,'header_hex':original[name]['header_hex']}
        rows.append({'path':name,'batch':'A' if row['matches'][0]['origin']=='current' else 'B',
            'before':before,'source_before':source_before,'analysis':spec,
            'preflight':'READY' if ready else 'DEFER_CHANGED'})
    if sum(r['batch']=='A' for r in rows)!=47:raise ValueError('fixed batch changed')
    added={p:s for p,s in actual.items() if p not in base['files']}
    new(E/'BASELINE-DELTA.json.gz',{'schema':'photo-pytest-protection-delta/v1',
        'base_path':str(base_path.relative_to(ROOT)),'base_sha256':state.sha(base_path),
        'previous_absent':sorted(previous),'additional_files':added,'repositories':repos,'pointers':current})
    new(E/'TARGETS.json.gz',{'schema':'photo-pytest-targets/v1','targets':rows})
    new(E/'ABSENT.json',[]);new(E/'REMOVED.json',[])
    new(E/'STAGE01.json',{'status':'PASS','inputs':INPUTS,'target_count':65,'target_bytes':807566,
        'batch_counts':{'A':47,'B':18},'protected_paths':len(actual),'additional_stamps':len(added),
        'CURRENT_count':len(current),'original_dirty_paths':{r:len(v) for r,v in full_status.items()},
        'preflight_deferred':[r['path'] for r in rows if r['preflight']!='READY'],
        'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 1 PASS; 65 frozen targets;',len(added),'additional protection entries',flush=True)


def verify(output=None):
    baseline=load_baseline();absent=set(state.read(E/'ABSENT.json'));removed=set(state.read(E/'REMOVED.json'))
    names={r['path'] for r in targets()}
    if not removed<=absent<=names:raise ValueError('absence allowlist expanded')
    if absent&set(baseline['repositories'][str(ROOT)]['status']):raise ValueError('cannot exempt dirty work')
    paths=[p for p in baseline['files'] if not (Path(p).is_relative_to(ROOT) and str(Path(p).relative_to(ROOT)) in absent)]
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,stamp in zip(paths,pool.map(state.stamp,paths)):
            if stamp!=baseline['files'][path]:failures.append(path)
    for path in [*(ROOT/p for p in absent),*map(Path,baseline['previous_absent'])]:
        if path.exists() or path.is_symlink():failures.append(str(path)+': reappeared')
    for root,row in baseline['repositories'].items():
        dirty=state.status(root)
        if root==str(ROOT):dirty={p:s for p,s in dirty.items() if not owned(p)}
        if dirty!=row['status']:failures.append(root+': original Git status changed')
        if state.git(root,'diff','--cached','--raw','-z').decode()!=row['staged']:failures.append(root+': staging changed')
        if root!=str(ROOT):
            if state.git(root,'rev-parse','HEAD').decode().strip()!=row['head']:failures.append(root+': HEAD changed')
            if state.sha(row['index_path'])!=row['index_sha256']:failures.append(root+': index changed')
    if pointers()!=baseline['pointers']:failures.append('CURRENT inventory changed')
    result={'status':'FAIL' if failures else 'PASS','protected_paths_checked':len(paths),
        'CURRENT_count':len(baseline['pointers']),'absent_files':len(absent),'removed_files':len(removed),
        'failures':failures,'Gemini_calls':0,'CURRENT_writes':0}
    if output:new(output,result)
    print(result,flush=True)
    if failures:raise ValueError('protected state changed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','verify']);p.add_argument('--output',type=Path);a=p.parse_args()
    freeze() if a.command=='freeze' else verify(a.output)
