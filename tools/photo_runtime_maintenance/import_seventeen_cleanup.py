"""Qualify exactly seventeen imports and four dead helpers without activation."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess

import checks
import four_checks
import four_patch
import four_state
import imports_cleanup
import small_cleanup
import state
from history_state import new, pointers

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['GIT_NO_LAZY_FETCH'] = '1'
ROOT = state.ROOT
SKILL = ROOT/'skills/photo-prompt-image-generator'
E = ROOT/'docs/research-evidence/photo-prompt/runtime-import-seventeen-cleanup-20261019'
ANALYSIS = ROOT/'docs/research-evidence/photo-prompt/runtime-remaining-after-imports-20261019'
HELPER = 'tools/photo_runtime_maintenance/import_seventeen_cleanup.py'
IMPORTS = {'photo_contextual_appeal': ['math'], 'photo_global_index': ['Path'],
    'photo_candidate_semantics': ['re'], 'qualify_local_embeddings': ['collections', 'time'],
    'install_photo_h_f2_runtime': ['sys'], 'audit_moe_render_review': ['sys'],
    'photo_search_reader': ['array'], 'validate_precore_feature_selection': ['hashlib', 're'],
    'photo_feature_selection': ['json'],
    'prompt_generator': ['argparse', 'secrets', 'time', 'Counter', 'Callable', 'os']}
FUNCTIONS = ['get_gemini_api_key', 'cached_gemini_client', 'extract_embedding_values', 'round_embedding_vector']
TARGETS = {'skills/photo-prompt-image-generator/'+('precore/' if m == 'photo_feature_selection' else 'scripts/')+m+'.py'
           for m in IMPORTS}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def owned(relative):
    return relative == HELPER or relative.startswith(str(E.relative_to(ROOT))+'/')


def previous_files(protection=None):
    delta = state.read(protection or ANALYSIS/'PROTECTION-DELTA.json.gz')
    parent = Path(delta['parent'])
    assert state.sha(parent/'BASELINE-DELTA.json.gz') == delta['parent_baseline_sha256']
    assert state.sha(parent/'AFTER-DELTA.json.gz') == delta['parent_after_sha256']
    files = dict(imports_cleanup.baseline()['files'])
    for path, row in state.read(parent/'AFTER-DELTA.json.gz')['source_replacements'].items():
        assert files[path] == row['before']
        files[path] = row['after']
    assert not set(files) & set(delta['additional_files'])
    files.update(delta['additional_files'])
    return files


def baseline():
    delta = state.read(E/'BASELINE-DELTA.json.gz')
    protection = E/'PREVIOUS-PROTECTION.json.gz'
    assert state.sha(protection) == delta['analysis_sha256']['PROTECTION-DELTA.json.gz']
    files = previous_files(protection)
    assert not set(files) & set(delta['additional_files'])
    files.update(delta['additional_files'])
    return {**delta, 'files': files}


def freeze(private):
    if E.exists(): raise FileExistsError('never overwrite evidence')
    previous = state.read(ANALYSIS/'PROTECTION-DELTA.json.gz')
    expected = previous_files()
    paths = set(expected); repositories = {}
    for work in state.worktrees():
        dirty = {p:s for p,s in state.status(work).items() if work != ROOT or not owned(p)}
        row = previous['repositories'][str(work)]
        head = state.git(work, 'rev-parse', 'HEAD').decode().strip()
        staged = state.git(work, 'diff', '--cached', '--raw', '-z').decode()
        assert head == row['head'] and staged == row['staged'] == ''
        assert state.sha(row['index_path']) == row['index_sha256'], 'index changed; inspect'
        # New evidence from the preceding analysis is original work for this task.
        assert {p:s for p,s in dirty.items() if not (work == ROOT and p.startswith(str(ANALYSIS.relative_to(ROOT))+'/'))} == row['status']
        tracked = set(state.git(work, 'ls-files', '-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked|set(dirty) if work != ROOT or not owned(p))
        repositories[str(work)] = {**row, 'status': dirty}
    current = pointers(); assert current == previous['pointers']; paths.update(current)
    additions = {p:state.stamp(p) for p in sorted(paths-set(expected))}
    expected.update(additions)
    private.mkdir(parents=True, exist_ok=True)
    new(private/'BEFORE.json.gz', {'files': expected, 'repositories': repositories,
        'pointers': current, 'previous_absent': previous['previous_absent'],
        'additional_files': additions})
    print('protected baseline frozen:', len(expected), 'paths;', len(current), 'CURRENT', flush=True)


def transform(raw, module):
    tree = ast.parse(raw); lines = raw.splitlines(keepends=True)
    removed = set(); found = set(); functions = []
    for node in list(tree.body):
        if module == 'prompt_generator' and isinstance(node, ast.FunctionDef) and node.name in FUNCTIONS:
            first = min([node.lineno, *[d.lineno for d in node.decorator_list]])
            removed.update(range(first, node.end_lineno+1)); tree.body.remove(node); functions.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            selected = [a for a in node.names if (a.asname or a.name) in IMPORTS[module]]
            if not selected: continue
            assert node.lineno == node.end_lineno
            found.update(a.asname or a.name for a in selected)
            node.names = [a for a in node.names if a not in selected]
            if not node.names:
                removed.add(node.lineno); tree.body.remove(node)
            else:
                assert isinstance(node, ast.ImportFrom) and not node.level
                fields = ', '.join(a.name+(' as '+a.asname if a.asname else '') for a in node.names)
                lines[node.lineno-1] = ('from '+node.module+' import '+fields+'\n').encode()
    assert found == set(IMPORTS[module])
    assert set(functions) == (set(FUNCTIONS) if module == 'prompt_generator' else set())
    changed = b''.join(line for i,line in enumerate(lines, 1) if i not in removed)
    assert ast.dump(tree, include_attributes=False) == ast.dump(ast.parse(changed), include_attributes=False)
    return changed


def make_patch(private, label, originals, candidates):
    result = []
    for rel in sorted(TARGETS):
        directory = private/'patch-input'/label/Path(rel).stem; directory.mkdir(parents=True)
        first, second = directory/'before.py', directory/'after.py'
        first.write_bytes(originals[rel]); second.write_bytes(candidates[rel])
        child = subprocess.run(['git', 'diff', '--no-index', '--no-ext-diff', '--no-color',
            '--diff-algorithm=myers', '--', str(first), str(second)], capture_output=True, text=True)
        assert child.returncode == 1, child.stderr
        for line in child.stdout.splitlines(keepends=True):
            if line.startswith('diff --git '): line = 'diff --git a/'+rel+' b/'+rel+'\n'
            elif line.startswith('--- '): line = '--- a/'+rel+'\n'
            elif line.startswith('+++ '): line = '+++ b/'+rel+'\n'
            result.append(line)
    raw = ''.join(result).encode()
    (E/(label+'.patch.gz')).write_bytes(gzip.compress(raw, mtime=0))
    (private/(label+'.patch')).write_bytes(raw)
    return {'raw_sha256': digest(raw), 'sha256': state.sha(E/(label+'.patch.gz'))}


def prepare(private):
    if E.exists(): raise FileExistsError('never overwrite qualification')
    before = state.read(private/'BEFORE.json.gz'); originals = {p:(ROOT/p).read_bytes() for p in TARGETS}
    head = before['repositories'][str(ROOT)]['head']
    heads = {p:state.git(ROOT, 'show', head+':'+p) for p in TARGETS}
    assert all(state.stamp(ROOT/p) == before['files'][str(ROOT/p)] for p in TARGETS)
    dirty_targets = TARGETS & set(before['repositories'][str(ROOT)]['status'])
    assert dirty_targets == {'skills/photo-prompt-image-generator/scripts/prompt_generator.py'}
    work = {p:transform(raw, Path(p).stem) for p,raw in originals.items()}
    index = {p:transform(raw, Path(p).stem) for p,raw in heads.items()}
    payloads = {p:small_cleanup.dirty_payload(heads[p], originals[p]) for p in TARGETS}
    assert all(small_cleanup.dirty_payload(index[p], work[p]) == payloads[p] for p in TARGETS)
    predicted = next(r for r in state.read(ANALYSIS/'PATCH-METRICS.json')['cases'] if r['case'] == 'combined')
    assert {r['path']:r['working_candidate_sha256'] for r in predicted['details']} == {p:digest(raw) for p,raw in work.items()}
    assert {r['path']:r['HEAD_candidate_sha256'] for r in predicted['details']} == {p:digest(raw) for p,raw in index.items()}
    E.mkdir(parents=True)
    shutil.copy2(ANALYSIS/'PROTECTION-DELTA.json.gz', E/'PREVIOUS-PROTECTION.json.gz')
    references = ['PROTECTION-DELTA.json.gz', 'ANALYSIS.json', 'IMPORTS.json', 'FUNCTIONS.json',
        'CONDITIONAL-REFERENCES.json', 'PATCH-METRICS.json', 'PROBE-SUMMARY.json', 'PRESERVATION.json', 'FINAL-CHECK.json']
    new(E/'BASELINE-DELTA.json.gz', {k:v for k,v in before.items() if k != 'files'} |
        {'analysis_path': str(ANALYSIS.relative_to(ROOT)), 'analysis_sha256': {n:state.sha(ANALYSIS/n) for n in references}})
    patches = {label:make_patch(private,label,old,after) for label,old,after in [('WORKING',originals,work),('INDEX',heads,index)]}
    projects = {}
    for label in ('control', 'combined', 'operating'):
        project = private/label; skill = four_patch.copy_code(project); projects[label] = str(project)
        if label != 'control':
            for rel,raw in work.items(): (project/rel).write_bytes(raw)
        if label == 'control':
            (skill/'.runtime').symlink_to(SKILL/'.runtime', target_is_directory=True)
        else:
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/'assets'),str(skill/'assets')], check=True)
            shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
            (project/'docs').symlink_to(ROOT/'docs', target_is_directory=True)
            lock = state.read(SKILL/'embedding-runtime.lock.json'); package = skill/lock['package']
            package.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(package)],check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
        print('private project prepared:',label,flush=True)
    project = Path(projects['combined'])
    subprocess.run(['git','-C',str(project),'apply','--reverse',str(private/'WORKING.patch')],check=True)
    assert all((project/p).read_bytes() == raw for p,raw in originals.items())
    subprocess.run(['git','-C',str(project),'apply',str(private/'WORKING.patch')],check=True)
    new(E/'TARGETS.json', {'base_head':head, 'imports':IMPORTS, 'functions':FUNCTIONS,
        'import_bindings_removed':17, 'functions_removed':4, 'function_lines_removed':38,
        'original':{p:before['files'][str(ROOT/p)] for p in sorted(TARGETS)},
        'working':{p:digest(raw) for p,raw in work.items()},'index':{p:digest(raw) for p,raw in index.items()},
        'original_dirty_payload_sha256':payloads,'patches':patches,'remaining_AST_equal':True,
        'working_patch_inverse_exact':True,'original_dirty_payload_equal':True,
        'source_added_lines':1,'source_deleted_lines':55,'net_removed_lines':54})
    new(E/'PRIVATE-PROJECTS.json',{'projects':projects,'private_parent':str(private),
        'model_and_assets_independent_APFS_clones':True,'model_files':len(lock['files']),
        'source_files':76,'scratch_is_not_unique_recovery_material':True})


def worker(project, removed, modules, policy, timeout, log=None):
    env = checks.environment(); env['PHOTO_RUNTIME_STORE'] = str(project/'.test-runtime')
    cmd = ['/usr/bin/sandbox-exec','-p',policy,str(SKILL/'.runtime/embedding-python/bin/python'),
        '-I','-B',str(E/'worker.py'),str(project),'1' if removed else '0',*modules]
    child = subprocess.Popen(cmd,cwd=project,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        text=True,start_new_session=True)
    try: stdout,stderr = child.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid,signal.SIGTERM); stdout,stderr = child.communicate()
        if log: log.write_text(stderr)
        return {'status':'TIMEOUT','stdout':stdout,'stderr':stderr}
    if log: log.write_text(stderr)
    try: result = json.loads(stdout.splitlines()[-1])
    except (ValueError,IndexError): result = {'status':'HARNESS_UNAVAILABLE'}
    return {**result,'exit_code':child.returncode,'stdout':stdout,'stderr':stderr}


def source(group):
    output=E/('SOURCE-'+group+'.json'); assert not output.exists()
    project=Path(state.read(E/'PRIVATE-PROJECTS.json')['projects']['operating' if group=='operating' else 'combined'])
    log=project/('source-'+group+'.log')
    new(E/('SOURCE-'+group+'-progress.json'),{'private_log':str(log),'final_log':output.name})
    result=worker(project,True,checks.GROUPS[group],four_patch.policy()+
        '(deny file-read* (regex "/site-packages/torch(/|$)"))',1800,log)
    expected=state.read(E/'TARGETS.json')['working']
    assert result.get('exit_code')==0 and result.get('tests')==(48 if group=='operating' else 70) and result.get('skipped')==0, result.get('stderr','')[-5000:]
    for rel,sha in expected.items(): assert result['loaded_modules'][Path(rel).stem]['sha256']==sha
    new(output,{**result,'network_denied':True,'original_source_reads_denied':True,
        'original_writes_denied':True,'torch_module_read_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    print(group,result['status'],result['tests'],'tests',flush=True)


def smoke(kind):
    output=E/('SMOKE-'+kind+'.json'); assert not output.exists()
    targets=state.read(E/'TARGETS.json')
    project=ROOT if kind=='applied' else Path(state.read(E/'PRIVATE-PROJECTS.json')['projects'][kind])
    policy=checks.profile() if kind=='applied' else four_patch.policy()
    policy+='(deny file-read* (regex "/site-packages/torch(/|$)"))'
    if kind=='applied': policy+='(deny file-read* (regex '+json.dumps('^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    result=worker(project,kind!='control',[],policy,90)
    assert result.get('exit_code')==0 and result.get('status')=='PASS',result
    expected={p:s['sha256'] for p,s in targets['original'].items()} if kind=='control' else targets['working']
    for rel,sha in expected.items(): assert result['loaded_modules'][Path(rel).stem]['sha256']==sha
    new(output,{**result,'bytecode_reads_denied':kind=='applied','network_denied':True,
        'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    print(kind,'source/algorithm/guard smoke PASS',flush=True)


def delegate(kind):
    previous=four_state.E; four_state.E=E
    try:
        if kind.startswith('managed-'): four_checks.managed(kind.removeprefix('managed-'))
        elif kind.startswith('history-'): four_checks.history(kind.removeprefix('history-'))
        elif kind=='installed': four_checks.installed()
        else: raise ValueError(kind)
    finally: four_state.E=previous


def index_check():
    before=baseline(); row=before['repositories'][str(ROOT)]; targets=state.read(E/'TARGETS.json')
    assert state.sha(row['index_path'])==row['index_sha256']
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent']); index=private/'qualified.index'
    shutil.copy2(row['index_path'],index); env={**os.environ,'GIT_INDEX_FILE':str(index)}
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    assert digest(raw)==targets['patches']['INDEX']['raw_sha256']
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:
        subprocess.run(['git','-C',str(ROOT),*args],input=raw,env=env,check=True)
    blobs={p:digest(subprocess.check_output(['git','-C',str(ROOT),'show',':'+p],env=env)) for p in TARGETS}
    stats=subprocess.check_output(['git','-C',str(ROOT),'diff','--cached','--numstat'],env=env).decode().splitlines()
    assert blobs==targets['index'] and {r.split('\t')[2] for r in stats}==TARGETS
    assert sum(int(r.split('\t')[0]) for r in stats)==1 and sum(int(r.split('\t')[1]) for r in stats)==55
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],env=env,check=True)
    assert state.sha(row['index_path'])==row['index_sha256']
    new(E/'INDEX-DRY-RUN.json',{'status':'PASS','private_index_blobs':blobs,'source_added_lines':1,
        'source_deleted_lines':55,'numstat':stats,'real_index_unchanged':True,'original_dirty_changes_staged':False})
    print('private partial index PASS: 1 added / 55 deleted source lines',flush=True)


def verify(output, full=False):
    before=baseline(); targets=state.read(E/'TARGETS.json'); applied=(E/'APPLICATION.json').exists()
    selected=before['files'] if full else {p:s for p,s in before['files'].items() if p in before['pointers'] or
        Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore') or Path(p).name in
        {'retrieval-runtime.json','embedding-default.json','embedding-runtime.lock.json'}}
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(selected,pool.map(state.stamp,selected)):
            rel=str(Path(path).relative_to(ROOT)) if Path(path).is_relative_to(ROOT) else None
            good=actual==selected[path] if not applied or rel not in TARGETS else actual.get('sha256')==targets['working'][rel] and all(actual.get(k)==selected[path].get(k) for k in ('mode','links'))
            if not good: failures.append(path)
    for work,row in before['repositories'].items():
        dirty=state.status(work)
        if work==str(ROOT): dirty={p:s for p,s in dirty.items() if not owned(p) and not (applied and p in TARGETS and p not in row['status'])}
        if dirty!=row['status']: failures.append(work+': original status')
        if state.git(work,'diff','--cached','--raw','-z').decode()!=row['staged'] or state.sha(row['index_path'])!=row['index_sha256']: failures.append(work+': staging/index')
        if state.git(work,'rev-parse','HEAD').decode().strip()!=row['head']: failures.append(work+': HEAD')
    if pointers()!=before['pointers']: failures.append('CURRENT inventory')
    failures.extend(p for p in before['previous_absent'] if Path(p).exists() or Path(p).is_symlink())
    if applied:
        for rel in TARGETS:
            original=state.git(ROOT,'show',targets['base_head']+':'+rel)
            if small_cleanup.dirty_payload(transform(original,Path(rel).stem),(ROOT/rel).read_bytes())!=targets['original_dirty_payload_sha256'][rel]: failures.append(rel+': dirty payload')
    result={'status':'FAIL' if failures else 'PASS','checked_paths':len(selected),'full':full,
        'CURRENT_count':len(before['pointers']),'failures':failures,'original_dirty_payload_preserved':applied,
        'Gemini_calls':0,'CURRENT_writes':0}
    new(output,result); print(json.dumps(result),flush=True)
    assert not failures,failures[:10]


GATES=['SMOKE-control.json','SMOKE-combined.json','SOURCE-operating.json','SOURCE-native.json',
    'HEAD-COMPARISON.json','INDEX-DRY-RUN.json','BEFORE-APPLICATION-FULL.json',
    'MANAGED-control.json','MANAGED-combined.json','INSTALLED.json','HISTORY-frozen.json',
    'HISTORY-archive.json','HISTORY-negative.json','HISTORY-native-view.json','CLI-HELP.json']


def apply():
    assert not (E/'APPLICATION.json').exists() and not (E/'APPLY-INTENT.json').exists()
    assert all(state.read(E/n)['status']=='PASS' for n in GATES)
    for key in ('algorithm_without_code','algorithm_binding_signature'):
        assert state.read(E/'SMOKE-control.json')[key]==state.read(E/'SMOKE-combined.json')[key]
    targets=state.read(E/'TARGETS.json')
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head'] and not state.git(ROOT,'diff','--cached','--name-only')
    assert all(state.stamp(ROOT/p)==stamp for p,stamp in targets['original'].items())
    raw=gzip.decompress((E/'WORKING.patch.gz').read_bytes())
    assert digest(raw)==targets['patches']['WORKING']['raw_sha256'] and state.sha(E/'WORKING.patch.gz')==targets['patches']['WORKING']['sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--check','-'],input=raw,check=True)
    new(E/'APPLY-INTENT.json',{'gate_sha256':{n:state.sha(E/n) for n in GATES},'candidate':targets['working']})
    subprocess.run(['git','-C',str(ROOT),'apply','-'],input=raw,check=True)
    assert all(state.sha(ROOT/p)==sha for p,sha in targets['working'].items())
    new(E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','applied':targets['working'],
        'import_bindings_removed':17,'functions_removed':4,'function_lines_removed':38,'source_added_lines':1,
        'source_deleted_lines':55,'net_removed_lines':54,'runtime_publish_calls':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('applied exact qualified 17-import/4-helper patch',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('command')
    parser.add_argument('--private',type=Path); parser.add_argument('--output',type=Path); parser.add_argument('--full',action='store_true')
    args=parser.parse_args()
    if args.command=='freeze': freeze(args.private)
    elif args.command=='prepare': prepare(args.private)
    elif args.command in checks.GROUPS: source(args.command)
    elif args.command.startswith('smoke-'): smoke(args.command.removeprefix('smoke-'))
    elif args.command=='verify': verify(args.output,args.full)
    elif args.command=='index-check': index_check()
    elif args.command=='apply': apply()
    else: delegate(args.command)
