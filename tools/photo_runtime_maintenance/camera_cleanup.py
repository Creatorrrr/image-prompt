"""Qualify the bounded camera-parser removal without changing installed releases."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import difflib
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile

import checks
import four_checks
import four_patch
import four_state
from history_state import new, pointers
import state

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['GIT_NO_LAZY_FETCH'] = '1'
ROOT = state.ROOT
SKILL = ROOT/'skills/photo-prompt-image-generator'
E = ROOT/'docs/research-evidence/photo-prompt/runtime-camera-clause-cleanup-20261019'
PARENT = ROOT/'docs/research-evidence/photo-prompt/runtime-legacy-post-four-20261019/PROTECTION-DELTA.json.gz'
HELPER = 'tools/photo_runtime_maintenance/camera_cleanup.py'
MODULE = 'skills/photo-prompt-image-generator/scripts/photo_camera_clauses.py'
IMPORTER = 'skills/photo-prompt-image-generator/scripts/photo_camera_evidence.py'
TARGETS = {MODULE, IMPORTER}


def owned(relative):
    return relative == HELPER or relative.startswith(str(E.relative_to(ROOT))+'/')


def parent_files():
    delta = state.read(PARENT)
    files = dict(four_state.baseline()['files'])
    after = ROOT/delta['after_path']
    if state.sha(after) != delta['after_sha256']:
        raise ValueError('previous source protection changed')
    for path, row in state.read(after)['source_replacements'].items():
        if files[path] != row['before']:
            raise ValueError('previous source stamp changed')
        files[path] = row['after']
    files.update(delta['additional_files'])
    return files


def baseline():
    delta = state.read(E/'BASELINE-DELTA.json.gz')
    if state.sha(PARENT) != delta['parent_sha256']:
        raise ValueError('analysis protection changed')
    files = parent_files()
    files.update(delta['additional_files'])
    return {**delta, 'files': files}


def prepare(private):
    if (E/'PRIVATE-PROJECTS.json').exists():
        raise FileExistsError('completed preparation must not be repeated')
    before = state.read(private/'BEFORE.json.gz')
    previous = parent_files()
    if any(before['files'][p] != s for p, s in previous.items()):
        raise ValueError('parent protection drift')
    if TARGETS & set(before['repositories'][str(ROOT)]['status']):
        raise ValueError('target has existing work; defer')
    for rel in TARGETS:
        if (ROOT/rel).read_bytes() != state.git(ROOT, 'show', 'HEAD:'+rel):
            raise ValueError('target is not clean')
    new(E/'BASELINE-DELTA.json.gz', {
        'schema': 'photo-camera-cleanup-protection/v1',
        'parent_path': str(PARENT.relative_to(ROOT)), 'parent_sha256': state.sha(PARENT),
        'additional_files': {p:s for p,s in before['files'].items() if p not in previous},
        'repositories': before['repositories'], 'pointers': before['pointers'],
        'previous_absent': before['previous_absent'], 'protected_count': len(before['files'])})
    original = {rel:(ROOT/rel).read_bytes() for rel in TARGETS}
    tree = ast.parse(original[IMPORTER])
    imports = [n for n in tree.body if (isinstance(n, ast.ImportFrom)
        and n.module == 'photo_camera_clauses') or (isinstance(n, ast.Import)
        and any(a.name == 're' for a in n.names))]
    if len(imports) != 2 or any(n.end_lineno != n.lineno for n in imports):
        raise ValueError('two-import scope changed')
    lines = original[IMPORTER].splitlines(keepends=True)
    removed_lines = {n.lineno for n in imports}
    changed = b''.join(line for i,line in enumerate(lines,1) if i not in removed_lines)
    tree.body = [n for n in tree.body if n not in imports]
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(changed), include_attributes=False):
        raise ValueError('importer AST exceeds approved scope')
    if len(original[MODULE].splitlines()) != 185:
        raise ValueError('module size changed')
    candidate = {IMPORTER:changed, MODULE:None}
    raw = ''.join(line for rel in sorted(TARGETS) for line in difflib.unified_diff(
        original[rel].decode().splitlines(True), (candidate[rel] or b'').decode().splitlines(True),
        fromfile='a/'+rel, tofile='/dev/null' if candidate[rel] is None else 'b/'+rel)).encode()
    (E/'PATCH.patch.gz').write_bytes(gzip.compress(raw, mtime=0))
    executable = private/'qualified.patch'; executable.write_bytes(raw)
    projects = {}
    for label in ('control', 'combined', 'operating'):
        project = private/label
        skill = four_patch.copy_code(project)
        projects[label] = str(project)
        if label != 'control':
            (project/IMPORTER).write_bytes(changed)
            (project/MODULE).unlink()
        if label == 'control':
            (skill/'.runtime').symlink_to(SKILL/'.runtime', target_is_directory=True)
        else:
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/'assets'),str(skill/'assets')],check=True)
            shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
            (project/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
            lock = state.read(SKILL/'embedding-runtime.lock.json')
            package = skill/lock['package']; package.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(package)],check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
        print('private project prepared:',label,flush=True)
    project = Path(projects['combined'])
    subprocess.run(['git','-C',str(project),'apply','--reverse','--check',str(executable)],check=True)
    subprocess.run(['git','-C',str(project),'apply','--reverse',str(executable)],check=True)
    if any((project/rel).read_bytes() != raw for rel,raw in original.items()):
        raise ValueError('inverse did not restore exact source bytes')
    subprocess.run(['git','-C',str(project),'apply',str(executable)],check=True)
    new(E/'TARGETS.json', {'source_lines_removed':187,'original':{
        rel:before['files'][str(ROOT/rel)] for rel in sorted(TARGETS)},
        'candidate':{rel:hashlib.sha256(raw).hexdigest() if raw is not None else None
                     for rel,raw in candidate.items()},
        'remaining_importer_AST_equal':True,'inverse_exact':True,
        'patch_sha256':state.sha(E/'PATCH.patch.gz'),'raw_patch_sha256':hashlib.sha256(raw).hexdigest()})
    new(E/'PRIVATE-PROJECTS.json', {'projects':projects,'model_and_assets_independent_APFS_clones':True,
        'model_files':len(lock['files']),'working_code_files_before':77,'working_code_files_after':76,
        'scratch_is_not_unique_recovery_material':True})


RUNNER = r'''
import os,sys,json,unittest,hashlib
from pathlib import Path
project=Path(sys.argv.pop(1)).resolve();os.chdir(project);sys.path.insert(0,str(project))
suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
import photo_camera_evidence as camera,photo_runtime_sources as runtime
assert not (project/'skills/photo-prompt-image-generator/scripts/photo_camera_clauses.py').exists()
assert 'photo_camera_clauses' not in sys.modules
assert not hasattr(camera,'bounded_camera_clauses') and not hasattr(camera,'re')
assert 'scripts/photo_camera_clauses.py' not in runtime.LOADED_CODE
assert len(runtime.LOADED_CODE)==76
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
try:runtime._require_implementation({'code':{**runtime.LOADED_CODE,'scripts/foreign.py':'bad'},'environment':runtime.LOADED_ENVIRONMENT},None)
except runtime.FreshnessError as e:assert e.state=='runtime_restart_required'
else:raise AssertionError('implementation guard weakened')
modules={}
for m in (camera,runtime,camera._authoring):
 p=Path(m.__file__).resolve();assert p.is_relative_to(project)
 modules[m.__name__]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
result=unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'status':'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL',
 'tests':result.testsRun,'skipped':len(result.skipped),'loaded_modules':modules,
 'missing_module_verified':True,'code_files':len(runtime.LOADED_CODE),'implementation_guard_preserved':True}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
'''


def source(group):
    output = E/('SOURCE-'+group+'.json')
    if output.exists():raise FileExistsError('never overwrite a check')
    projects = state.read(E/'PRIVATE-PROJECTS.json')['projects']
    project = Path(projects['operating' if group == 'operating' else 'combined'])
    target = state.read(E/'TARGETS.json')['candidate']
    if (project/MODULE).exists() or state.sha(project/IMPORTER) != target[IMPORTER]:
        raise ValueError('candidate source drift')
    log = project/('source-'+group+'.log')
    new(E/('SOURCE-'+group+'-progress.json'),{'private_log':str(log),
        'complete_log_saved_in':output.name,'private_log_is_only_progress':True})
    env = checks.environment();env['PHOTO_RUNTIME_STORE'] = str(project/'.test-runtime')
    policy = four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    with log.open('x') as stream:
        worker = subprocess.Popen(['/usr/bin/sandbox-exec','-p',policy,
            str(SKILL/'.runtime/embedding-python/bin/python'),'-I','-B','-c',RUNNER,
            str(project),*checks.GROUPS[group]],cwd=project,env=env,
            stdout=subprocess.PIPE,stderr=stream,text=True,start_new_session=True)
        try:stdout,_ = worker.communicate(timeout=1800)
        except subprocess.TimeoutExpired:
            os.killpg(worker.pid,signal.SIGTERM);stdout,_ = worker.communicate()
            new(output,{'status':'TIMEOUT','stdout':stdout,'stderr':log.read_text()})
            raise ValueError('source timeout')
    stderr = log.read_text()
    try:result = json.loads(stdout.splitlines()[-1])
    except (ValueError,IndexError):result = {'status':'HARNESS_UNAVAILABLE'}
    result.update(exit_code=worker.returncode,stdout=stdout,stderr=stderr,
        groups=checks.GROUPS[group],network_denied=True,live_source_reads_denied=True,
        original_writes_denied=True,torch_module_read_denied=True,Gemini_calls=0,CURRENT_writes=0)
    if worker.returncode or result.get('tests') != (48 if group=='operating' else 70) or result.get('skipped') != 0:
        result['status'] = 'FAIL'
    loaded = result.get('loaded_modules',{}).get('photo_camera_evidence',{})
    if loaded.get('sha256') != target[IMPORTER]:result['status'] = 'FAIL'
    new(output,result)
    print(group,result['status'],result.get('tests'),'tests',flush=True)
    if result['status'] != 'PASS':raise ValueError(stderr[-5000:])


@contextmanager
def evidence_scope():
    previous = four_state.E
    four_state.E = E
    try:yield
    finally:four_state.E = previous


def delegate(kind):
    with evidence_scope():
        if kind.startswith('managed-'):four_checks.managed(kind.removeprefix('managed-'))
        elif kind.startswith('history-'):four_checks.history(kind.removeprefix('history-'))
        elif kind == 'installed':four_checks.installed()
        else:raise ValueError(kind)


def smoke(kind):
    output = E/('SOURCE-SMOKE-'+kind+'.json')
    if output.exists():raise FileExistsError('never overwrite a smoke result')
    projects = state.read(E/'PRIVATE-PROJECTS.json')['projects']
    project = ROOT if kind=='applied' else Path(projects[kind])
    skill = project/'skills/photo-prompt-image-generator'
    policy = checks.profile() if kind=='applied' else four_patch.policy()
    policy += '(deny file-read* (regex "/site-packages/torch(/|$)"))'
    if kind=='applied':
        import re
        policy += '(deny file-read* (regex '+json.dumps(
            '^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    python = SKILL/'.runtime/embedding-python/bin/python'
    worker = ROOT/'docs/research-evidence/photo-prompt/runtime-legacy-post-four-20261019/camera_worker.py'
    commands = [([str(worker),str(skill)],'camera'),
                (['-c',four_patch.SMOKE,str(skill),'{}'],'guard')]
    results = {}
    for args,label in commands:
        process = subprocess.run(['/usr/bin/sandbox-exec','-p',policy,str(python),'-I','-B',*args],
            env=checks.environment(),capture_output=True,text=True,timeout=90)
        if process.returncode:raise ValueError(label+' smoke failed: '+process.stderr+process.stdout)
        results[label] = json.loads(process.stdout)
        if results[label]['status']!='PASS':raise ValueError(label+' smoke failed')
    expected = state.read(E/'TARGETS.json')
    sha = expected['original'][IMPORTER]['sha256'] if kind=='control' else expected['candidate'][IMPORTER]
    if results['guard']['loaded_modules']['photo_camera_evidence']['sha256']!=sha:
        raise ValueError('unexpected source loaded')
    if results['camera']['camera_clauses_loaded'] != (kind=='control'):
        raise ValueError('unexpected camera parser import')
    new(output,{'status':'PASS','case':kind,'results':results,'camera_contract_cases':10,
        'actual_source_sha256':sha,'bytecode_reads_denied':kind=='applied',
        'network_denied':True,'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    print(kind,'camera and implementation guard smoke PASS',flush=True)


def verify(output, *, full=False):
    before = baseline();application = E/'APPLICATION.json'
    candidate = state.read(application)['applied'] if application.exists() else {}
    if set(candidate) - TARGETS:raise ValueError('unapproved application')
    selected = before['files'] if full else {p:s for p,s in before['files'].items()
        if p in before['pointers'] or Path(p).is_relative_to(SKILL/'scripts')
        or Path(p).is_relative_to(SKILL/'precore') or Path(p).name in {
            'retrieval-runtime.json','embedding-default.json','embedding-runtime.lock.json'}}
    paths = sorted(selected); failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(paths,pool.map(state.stamp,paths)):
            relative = str(Path(path).relative_to(ROOT)) if Path(path).is_relative_to(ROOT) else None
            if relative in candidate:
                good = actual.get('kind')=='absent' if candidate[relative] is None else (
                    actual.get('sha256')==candidate[relative] and all(actual.get(k)==selected[path].get(k)
                        for k in ('mode','links')))
            else:good = actual == selected[path]
            if not good:failures.append(path)
    for work,row in before['repositories'].items():
        dirty = state.status(work)
        if work == str(ROOT):dirty = {p:s for p,s in dirty.items() if not owned(p) and p not in candidate}
        if dirty != row['status']:failures.append(work+':existing work')
        if state.git(work,'diff','--cached','--raw','-z').decode()!=row['staged']:failures.append(work+':staging')
        if work != str(ROOT) and (state.git(work,'rev-parse','HEAD').decode().strip()!=row['head']
                                  or state.sha(row['index_path'])!=row['index_sha256']):
            failures.append(work+':other worktree')
    if pointers()!=before['pointers']:failures.append('CURRENT inventory')
    for path in before['previous_absent']:
        if Path(path).exists() or Path(path).is_symlink():failures.append(path+':removed cache reappeared')
    result = {'status':'FAIL' if failures else 'PASS','full':full,'checked_paths':len(paths),
        'CURRENT_count':len(before['pointers']),'approved_source_paths':sorted(candidate),
        'failures':failures,'Gemini_calls':0,'CURRENT_writes':0}
    new(output,result);print(json.dumps(result),flush=True)
    if failures:raise ValueError('preservation failed')


def apply():
    if (E/'APPLICATION.json').exists() or (E/'APPLY-INTENT.json').exists():
        raise FileExistsError('application already started; inspect, never repeat')
    gates = ['SOURCE-SMOKE-control.json','SOURCE-SMOKE-combined.json',
             'SOURCE-operating.json','SOURCE-native.json','MANAGED-control.json','MANAGED-combined.json',
             'INSTALLED.json','HISTORY-frozen.json','HISTORY-archive.json','HISTORY-negative.json','HISTORY-native-view.json']
    if any(state.read(E/name)['status']!='PASS' for name in gates):raise ValueError('failed gate; defer')
    targets = state.read(E/'TARGETS.json');dirty = state.status(ROOT)
    if state.git(ROOT,'diff','--cached','--name-only'):raise ValueError('preserve staging')
    for rel,stamp in targets['original'].items():
        if rel in dirty or state.stamp(ROOT/rel)!=stamp:raise ValueError('target drift; defer')
    compressed = E/'PATCH.patch.gz'
    if state.sha(compressed)!=targets['patch_sha256']:raise ValueError('patch changed')
    raw = gzip.decompress(compressed.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=targets['raw_patch_sha256']:raise ValueError('raw patch changed')
    with tempfile.TemporaryDirectory(prefix='camera-apply-') as temp:
        p = Path(temp)/'qualified.patch';p.write_bytes(raw)
        subprocess.run(['git','-C',str(ROOT),'apply','--check',str(p)],check=True)
        new(E/'APPLY-INTENT.json',{'candidate':targets['candidate'],'gate_sha256':{n:state.sha(E/n) for n in gates}})
        subprocess.run(['git','-C',str(ROOT),'apply',str(p)],check=True)
    if (ROOT/MODULE).exists() or state.sha(ROOT/IMPORTER)!=targets['candidate'][IMPORTER]:
        raise ValueError('applied bytes do not match tested source')
    stat = state.git(ROOT,'diff','--numstat','--',*sorted(TARGETS)).decode().splitlines()
    if sum(int(r.split('\t')[0]) for r in stat)!=0 or sum(int(r.split('\t')[1]) for r in stat)!=187:
        raise ValueError('source diff exceeds approved 187 lines')
    new(E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','applied':targets['candidate'],
        'removed_lines':187,'modules_removed':1,'imports_removed':2,'source_publish_calls':0,
        'Gemini_calls':0,'CURRENT_writes':0})
    print('Applied qualified camera module and two imports: 187 lines',flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command');p.add_argument('--private',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--full',action='store_true');a = p.parse_args()
    if a.command=='prepare':prepare(a.private)
    elif a.command in checks.GROUPS:source(a.command)
    elif a.command.startswith('smoke-'):smoke(a.command.removeprefix('smoke-'))
    elif a.command=='verify':verify(a.output,full=a.full)
    elif a.command=='apply':apply()
    else:delegate(a.command)
