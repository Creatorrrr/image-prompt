"""Bounded four-function cleanup protection; never imports the production runtime."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
import os

import logic_state
import state
from history_state import new, pointers

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['GIT_NO_LAZY_FETCH'] = '1'
ROOT = state.ROOT
SKILL = ROOT/'skills/photo-prompt-image-generator'
E = ROOT/'docs/research-evidence/photo-prompt/runtime-four-functions-20261019'
PREVIOUS = ROOT/'docs/research-evidence/photo-prompt/runtime-legacy-followup-20261019/PROTECTION-DELTA.json.gz'
PLAN = 'docs/plans/photo-four-function-cleanup.md'
TOOLS = {'tools/photo_runtime_maintenance/'+name for name in (
    'four_state.py','four_review.py','four_patch.py','four_checks.py')}
FUNCTIONS = {'_normalized_lexicon':'bm25f_retrieval.py', 'resolve_rows':'photo_native_pack.py',
             'legacy_camera_clauses':'photo_camera_evidence.py', 'publish_if_ready':'photo_runtime_sources.py'}
SOURCE_PATHS = {'skills/photo-prompt-image-generator/scripts/'+name for name in FUNCTIONS.values()}


def owned(name):
    return name == PLAN or name in TOOLS or name.startswith(str(E.relative_to(ROOT))+'/')


def previous_files():
    previous = state.read(PREVIOUS)
    if state.sha(ROOT/previous['base_path']) != previous['base_sha256']:
        raise ValueError('previous protection changed')
    result = dict(logic_state.load_baseline()['files'])
    result.update(previous['additional_files'])
    return result


def baseline():
    delta = state.read(E/'BASELINE-DELTA.json.gz')
    if state.sha(PREVIOUS) != delta['previous_sha256']:
        raise ValueError('previous protection delta changed')
    files = previous_files()
    files.update(delta['additional_files'])
    return {**delta, 'files':files}


def freeze():
    if (E/'BASELINE-DELTA.json.gz').exists():
        raise FileExistsError('baseline already frozen')
    expected = previous_files()
    paths = set(expected); repos = {}
    for work in state.worktrees():
        dirty = state.status(work)
        if work == ROOT:
            dirty = {p:s for p,s in dirty.items() if not owned(p)}
        index = state.git(work,'rev-parse','--path-format=absolute','--git-path','index').decode().strip()
        repos[str(work)] = {'head':state.git(work,'rev-parse','HEAD').decode().strip(),
            'status':dirty,'staged':state.git(work,'diff','--cached','--raw','-z').decode(),
            'index_path':index,'index_sha256':state.sha(index)}
        tracked = set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked|set(dirty) if work != ROOT or not owned(p))
    if repos[str(ROOT)]['staged']:
        raise ValueError('preserve existing staged work; no mixed commits')
    if SOURCE_PATHS & set(repos[str(ROOT)]['status']):
        raise ValueError('target source now has existing work; defer')
    current = pointers(); paths.update(current); paths = sorted(paths)
    print('freezing',len(paths),'protected files;',len(current),'CURRENT',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        actual = dict(zip(paths,pool.map(state.stamp,paths)))
    if any(actual[p] != s for p,s in expected.items()):
        raise ValueError('previous protected files drifted')
    targets = []
    for name,filename in FUNCTIONS.items():
        relative = 'skills/photo-prompt-image-generator/scripts/'+filename
        raw = (ROOT/relative).read_bytes();lines = raw.splitlines(keepends=True)
        node = next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name == name)
        first = min([node.lineno,*(d.lineno for d in node.decorator_list)])
        function = b''.join(lines[first-1:node.end_lineno])
        if state.git(ROOT,'show','HEAD:'+relative) != raw:
            raise ValueError('target file differs from HEAD')
        targets.append({'name':name,'path':relative,'first':first,'last':node.end_lineno,
            'lines':node.end_lineno-first+1,'source_sha256':state.sha(ROOT/relative),
            'function_sha256':hashlib.sha256(function).hexdigest(),
            'ast_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()})
    if len(targets)!=4 or sum(t['lines'] for t in targets)!=50:
        raise ValueError('approved four-function/50-line scope changed')
    old = state.read(PREVIOUS)
    new(E/'BASELINE-DELTA.json.gz',{'schema':'photo-four-function-protection/v1',
        'previous_path':str(PREVIOUS.relative_to(ROOT)),'previous_sha256':state.sha(PREVIOUS),
        'additional_files':{p:s for p,s in actual.items() if p not in expected},
        'repositories':repos,'pointers':current,'previous_absent':old['previous_absent'],
        'protected_count':len(actual)})
    new(E/'TARGETS.json',{'schema':'photo-four-function-targets/v1','targets':targets})
    new(E/'STAGE01.json',{'status':'PASS','functions':4,'function_lines':50,
        'protected_paths':len(actual),'CURRENT_count':len(current),
        'original_dirty_paths':{p:len(r['status']) for p,r in repos.items()},
        'source_changes':0,'Gemini_calls':0,'CURRENT_writes':0})


def verify(output, *, full=False):
    before = baseline();files = before['files'];application = E/'APPLICATION.json'
    changed = state.read(application).get('applied',{}) if application.exists() else {}
    if not set(changed) <= SOURCE_PATHS:
        raise ValueError('application outside exact source allowlist')
    selected = files if full else {p:s for p,s in files.items() if p in before['pointers']
        or (Path(p).parent in {SKILL/'scripts',SKILL/'precore'} and Path(p).suffix == '.py')
        or Path(p).name in {'retrieval-runtime.json','embedding-default.json','embedding-runtime.lock.json'}
        or (Path(p).suffix == '.pyc' and Path(p).is_relative_to(ROOT))}
    paths = sorted(selected);failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for p,after in zip(paths,pool.map(state.stamp,paths)):
            rel = str(Path(p).relative_to(ROOT)) if Path(p).is_relative_to(ROOT) else None
            if rel in changed:
                good = after.get('sha256') == changed[rel] and all(after.get(k)==files[p].get(k) for k in ('mode','links'))
            else:
                good = after == files[p]
            if not good:failures.append(p)
    for work,row in before['repositories'].items():
        dirty = state.status(work)
        if work == str(ROOT):
            dirty = {p:s for p,s in dirty.items() if not owned(p) and p not in changed}
        if dirty != row['status']:failures.append(work+':original work')
        if state.git(work,'diff','--cached','--raw','-z').decode() != row['staged']:
            failures.append(work+':staging')
        if work != str(ROOT) and (state.git(work,'rev-parse','HEAD').decode().strip()!=row['head']
                                  or state.sha(row['index_path'])!=row['index_sha256']):
            failures.append(work+':other worktree')
    if pointers()!=before['pointers']:failures.append('CURRENT inventory')
    for p in before['previous_absent']:
        if Path(p).exists() or Path(p).is_symlink():failures.append(p+':removed cache reappeared')
    result = {'status':'FAIL' if failures else 'PASS','full':full,'checked_paths':len(paths),
        'CURRENT_count':len(before['pointers']),'approved_source_files':sorted(changed),'failures':failures,
        'Gemini_calls':0,'CURRENT_writes':0}
    new(output,result);print(result,flush=True)
    if failures:raise ValueError('preservation failed')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('freeze','verify'))
    parser.add_argument('--output',type=Path);parser.add_argument('--full',action='store_true')
    args = parser.parse_args()
    freeze() if args.command=='freeze' else verify(args.output,full=args.full)
