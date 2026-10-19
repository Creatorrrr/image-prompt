"""One bounded, separately frozen 228-bytecode cleanup; no runtime imports."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
from pathlib import Path
import subprocess

import deferred_state
import state

ROOT = state.ROOT
E = ROOT/'docs/research-evidence/photo-prompt/runtime-bytecode-cleanup-20261019'
INPUT = ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-remaining-20261019/ANALYSIS.json'
INPUT_SHA = '72babbafdb1391bd1069597a0e4a3825e9d64c0bfabb5f1af01caf52a2e49519'
PLAN = 'docs/plans/photo-historical-bytecode-cleanup.md'
TOOLS = {'tools/photo_runtime_maintenance/'+name for name in (
    'history_state.py','history_proof.py','history_restore.py','history_checks.py',
    'history_gc.py','test_history_cleanup.py')}
PREFIX = str(E.relative_to(ROOT))+'/'


def owned(relative):
    return relative == PLAN or relative in TOOLS or relative.startswith(PREFIX)


def new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    with path.open('xb') as stream:
        stream.write(gzip.compress(raw,mtime=0) if path.suffix == '.gz' else raw)


def pointers():
    result = subprocess.run(['rg','--files','--hidden','--no-ignore','-g','CURRENT.json',
        '-g','!**/.git/**','-g','!**/.runtime/**','-g','!**/.venv/**',
        '-g','!**/node_modules/**',*map(str,[*state.worktrees(),state.SHARED.parent])],
        capture_output=True,text=True,check=True)
    return sorted(set(result.stdout.splitlines()))


def freeze():
    if (E/'BASELINE.json.gz').exists():raise FileExistsError('baseline already frozen')
    if state.sha(INPUT) != INPUT_SHA:raise ValueError('reviewed input changed')
    if state.git(ROOT,'diff','--cached','--name-only'):raise ValueError('existing staging must remain untouched')
    old = state.read(deferred_state.E/'BASELINE.json.gz')
    old_removed = set(state.read(deferred_state.E/'REMOVED.json'))
    paths = {p for p in old['files'] if not (Path(p).is_relative_to(ROOT)
        and str(Path(p).relative_to(ROOT)) in old_removed)}
    supplementary = deferred_state.E/'REPLAY-PROTECTED.json.gz'
    if supplementary.exists():paths.update(state.read(supplementary))
    repositories = {}
    for root in state.worktrees():
        dirty = state.status(root)
        if root == ROOT:dirty = {p:s for p,s in dirty.items() if not owned(p)}
        tracked = set(state.git(root,'ls-files','-z').decode().split('\0'))-{''}
        repositories[str(root)] = {'head':state.git(root,'rev-parse','HEAD').decode().strip(),
            'status':dirty,'staged':state.git(root,'diff','--cached','--raw','-z').decode()}
        paths.update(str(root/p) for p in tracked|set(dirty) if root != ROOT or not owned(p))
    current = pointers();paths.update(current)
    analysis = state.read(INPUT);targets=[]
    for row in analysis['bytecodes']:
        if row['new_status'] != 'EXACT_GIT_SOURCE':continue
        rel = row['path'];before = state.stamp(ROOT/rel)
        source = ROOT/row['source'];batch = 'A' if source.exists() else 'B'
        ready = (before.get('sha256') == row['sha256'] and before.get('links') == 1
            and before.get('kind') == 'file' and rel not in repositories[str(ROOT)]['status']
            and row['source'] not in repositories[str(ROOT)]['status'])
        targets.append({'path':rel,'batch':batch,'before':before,'analysis':row,
            'source_before':state.stamp(source),'preflight':'READY' if ready else 'DEFER_CHANGED'})
        paths.add(str(ROOT/rel))
    if len(targets)!=228 or sum(r['analysis']['bytes'] for r in targets)!=5063794:
        raise ValueError('reviewed target ceiling changed')
    if sum(r['batch']=='A' for r in targets)!=25:raise ValueError('source presence changed; inspect instead of repartitioning')
    paths = sorted(p for p in paths if not (Path(p).is_relative_to(ROOT)
        and owned(str(Path(p).relative_to(ROOT)))))
    print('freezing',len(paths),'protected paths',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:files=dict(zip(paths,pool.map(state.stamp,paths)))
    # Earlier protection is evidence, never silently relabeled after a change.
    drift = [p for p in old['files'] if p in files and files[p] != old['files'][p]]
    if drift:raise ValueError('previous protected state drifted: '+str(drift[:8]))
    new(E/'BASELINE.json.gz',{'schema':'photo-history-bytecode-baseline/v1','files':files,
        'repositories':repositories,'pointers':current,'input_sha256':INPUT_SHA})
    new(E/'TARGETS.json.gz',{'schema':'photo-history-bytecode-targets/v1','targets':targets})
    new(E/'ABSENT.json',[])
    new(E/'REMOVED.json',[])
    new(E/'STAGE01.json',{'status':'PASS','protected_paths':len(files),'CURRENT_count':len(current),
        'target_count':228,'target_bytes':5063794,'batch_counts':{'A':25,'B':203},
        'original_dirty_paths':{r:len(v['status']) for r,v in repositories.items()},
        'preflight_deferred':[r['path'] for r in targets if r['preflight']!='READY'],
        'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 1 frozen; 228 targets;',len(current),'CURRENT',flush=True)


def targets():return state.read(E/'TARGETS.json.gz')['targets']


def verify(output=None):
    baseline = state.read(E/'BASELINE.json.gz');rows={r['path']:r for r in targets()}
    absent = set(state.read(E/'ABSENT.json'));removed=set(state.read(E/'REMOVED.json'))
    if not removed<=absent<=set(rows):raise ValueError('absence allowlist expanded')
    original_dirty=set(baseline['repositories'][str(ROOT)]['status'])
    if absent & original_dirty:raise ValueError('cannot exempt original dirty work')
    paths=[p for p in baseline['files'] if not (Path(p).is_relative_to(ROOT)
        and str(Path(p).relative_to(ROOT)) in absent)]
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(paths,pool.map(state.stamp,paths)):
            if actual != baseline['files'][path]:failures.append(path)
    for rel in absent:
        if (ROOT/rel).exists() or (ROOT/rel).is_symlink():failures.append(rel+': reappeared')
    for root,row in baseline['repositories'].items():
        current=state.status(root)
        if root==str(ROOT):current={p:s for p,s in current.items() if not owned(p)}
        if current!=row['status']:failures.append(root+': original Git status changed')
        if state.git(root,'diff','--cached','--raw','-z').decode()!=row['staged']:
            failures.append(root+': staged work changed')
        if root!=str(ROOT) and state.git(root,'rev-parse','HEAD').decode().strip()!=row['head']:
            failures.append(root+': HEAD changed')
    if pointers()!=baseline['pointers']:failures.append('CURRENT inventory changed')
    result={'status':'FAIL' if failures else 'PASS','protected_paths_checked':len(paths),
        'CURRENT_count':len(baseline['pointers']),'absent_files':len(absent),'removed_files':len(removed),
        'failures':failures,'Gemini_calls':0,'CURRENT_writes':0}
    if output:new(output,result)
    print(result,flush=True)
    if failures:raise ValueError('protected state changed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['freeze','verify'])
    p.add_argument('--output',type=Path);a=p.parse_args()
    freeze() if a.command=='freeze' else verify(a.output)
