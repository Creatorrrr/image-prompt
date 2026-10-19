"""Protection and exact scope for the nine-function/replay cleanup. No runtime imports."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
from pathlib import Path

import pytest_state
import state
from history_state import new, pointers

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['GIT_NO_LAZY_FETCH'] = '1'
ROOT = state.ROOT
E = ROOT/'docs/research-evidence/photo-prompt/runtime-logic-cleanup-20261019'
PREVIOUS = ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-retained-21-20261019/PROTECTION-DELTA.json.gz'
PLAN = 'docs/plans/photo-unused-functions-and-replay-separation.md'
TOOLS = {'tools/photo_runtime_maintenance/'+name for name in (
    'logic_state.py', 'logic_review.py', 'native_replay.py', 'test_native_replay.py',
    'logic_pilot.py', 'logic_checks.py', 'historical_evidence.py')}
DOCS = {PLAN, 'docs/plans/README.md', 'tools/photo_runtime_maintenance/README.md',
        'docs/research-archives/photo-prompt/REPLAY.md'}
FUNCTIONS = {
    'legacy_camera_clauses': 'photo_camera_evidence.py',
    'get_gemini_api_key': 'prompt_generator.py',
    'cached_gemini_client': 'prompt_generator.py',
    'extract_embedding_values': 'prompt_generator.py',
    'round_embedding_vector': 'prompt_generator.py',
    '_bm25f_lexicon_from_documents': 'prompt_generator.py',
    'candidate_pack_float': 'prompt_generator.py',
    'candidate_pack_assertion_discovery': 'prompt_generator.py',
    'authorial_core_bm25f_query_fields': 'prompt_generator.py',
}


def owned(name):
    return name in TOOLS | DOCS or name.startswith(str(E.relative_to(ROOT))+'/')


def previous_files():
    delta = state.read(PREVIOUS)
    base = pytest_state.load_baseline()
    path = ROOT/delta['base_path']
    if state.sha(path) != delta['base_sha256']:
        raise ValueError('previous protection changed')
    absent = {str(ROOT/p) for p in delta['excluded_removed_relative']}
    files = {p:s for p,s in base['files'].items() if p not in absent}
    files.update(delta['additional_files'])
    return files, sorted(absent | set(base['previous_absent']))


def load_baseline():
    delta = state.read(E/'BASELINE-DELTA.json.gz')
    if state.sha(PREVIOUS) != delta['previous_sha256']:
        raise ValueError('previous protection delta changed')
    files, absent = previous_files()
    files = {p:s for p,s in files.items() if p not in delta['excluded_owned']}
    files.update(delta['additional_files'])
    return {**delta, 'files':files, 'absent':absent}


def freeze():
    if (E/'BASELINE-DELTA.json.gz').exists():
        raise FileExistsError('baseline already frozen')
    previous, absent = previous_files()
    excluded = {p for p in previous if Path(p).is_relative_to(ROOT)
                and owned(str(Path(p).relative_to(ROOT)))}
    expected = {p:s for p,s in previous.items() if p not in excluded}
    paths = set(expected)
    repos = {}
    for work in state.worktrees():
        dirty = state.status(work)
        if work == ROOT:
            dirty = {p:s for p,s in dirty.items() if not owned(p)}
        index = state.git(work,'rev-parse','--path-format=absolute','--git-path','index').decode().strip()
        repos[str(work)] = {'head':state.git(work,'rev-parse','HEAD').decode().strip(),
            'status':dirty, 'staged':state.git(work,'diff','--cached','--raw','-z').decode(),
            'index_path':index, 'index_sha256':state.sha(index)}
        tracked = set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked | set(dirty)
                     if work != ROOT or not owned(p))
    if repos[str(ROOT)]['staged']:
        raise ValueError('existing staging must remain untouched')
    current = pointers()
    paths.update(current)
    paths = sorted(paths)
    print('freezing',len(paths),'protected paths',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        actual = dict(zip(paths,pool.map(state.stamp,paths)))
    failures = [p for p,s in expected.items() if actual[p] != s]
    failures += [p for p in absent if Path(p).exists() or Path(p).is_symlink()]
    if failures:
        raise ValueError('prior protected state drift: '+str(failures[:10]))
    targets = []
    for name, filename in FUNCTIONS.items():
        relative = 'skills/photo-prompt-image-generator/scripts/'+filename
        path = ROOT/relative
        source = path.read_bytes()
        lines = source.splitlines(keepends=True)
        node = next(n for n in ast.parse(source).body
                    if isinstance(n,ast.FunctionDef) and n.name == name)
        first = min([node.lineno, *(d.lineno for d in node.decorator_list)])
        raw = b''.join(lines[first-1:node.end_lineno])
        targets.append({'name':name,'path':relative,'first':first,'last':node.end_lineno,
            'function_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':state.sha(path),
            'source_dirty':relative in repos[str(ROOT)]['status'],
            'ast_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()})
    if len(targets) != 9:
        raise ValueError('function scope changed')
    new(E/'BASELINE-DELTA.json.gz',{'schema':'photo-logic-protection/v1',
        'previous_path':str(PREVIOUS.relative_to(ROOT)), 'previous_sha256':state.sha(PREVIOUS),
        'excluded_owned':sorted(excluded),
        'additional_files':{p:s for p,s in actual.items() if p not in expected},
        'repositories':repos, 'pointers':current, 'protected_count':len(actual)})
    new(E/'TARGETS.json',{'schema':'photo-logic-functions/v1','targets':targets})
    new(E/'STAGE01.json',{'status':'PASS','functions':9,'protected_paths':len(actual),
        'CURRENT_count':len(current),'existing_source_edits':sum(t['source_dirty'] for t in targets),
        'dirty_paths':{p:len(r['status']) for p,r in repos.items()},
        'plan':PLAN,'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 1 frozen; 9 functions;',len(current),'CURRENT',flush=True)


def verify(output=None):
    baseline = load_baseline()
    paths = sorted(baseline['files'])
    failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for p,actual in zip(paths,pool.map(state.stamp,paths)):
            if actual != baseline['files'][p]:
                failures.append(p)
    for work,row in baseline['repositories'].items():
        dirty = state.status(work)
        if work == str(ROOT):
            dirty = {p:s for p,s in dirty.items() if not owned(p)}
        if dirty != row['status']:
            failures.append(work+': original status')
        if state.git(work,'diff','--cached','--raw','-z').decode() != row['staged']:
            failures.append(work+': staging')
        if work != str(ROOT):
            if state.git(work,'rev-parse','HEAD').decode().strip() != row['head']:
                failures.append(work+': HEAD')
            if state.sha(row['index_path']) != row['index_sha256']:
                failures.append(work+': index')
    if pointers() != baseline['pointers']:
        failures.append('CURRENT inventory')
    for p in baseline['absent']:
        if Path(p).exists() or Path(p).is_symlink():
            failures.append(p+': prior cache reappeared')
    result = {'status':'FAIL' if failures else 'PASS','protected_paths':len(paths),
        'CURRENT_count':len(baseline['pointers']),'failures':failures,
        'source_changes':0,'Gemini_calls':0,'CURRENT_writes':0}
    if output:
        new(output,result)
    print(result,flush=True)
    if failures:
        raise ValueError('protected state changed')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('freeze','verify'))
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    freeze() if args.command == 'freeze' else verify(args.output)
