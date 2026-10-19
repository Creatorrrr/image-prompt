"""Exact four-line generator cleanup; reuse qualified runtime/replay checks."""
import ast
from concurrent.futures import ThreadPoolExecutor
import gzip
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path('/Users/chasoik/Projects/image-prompt');E=Path(__file__).parent
PARENT=ROOT/'docs/research-evidence/photo-prompt/runtime-graph-validator-cleanup-20261019'
ANALYSIS=ROOT/'docs/research-evidence/photo-prompt/runtime-skill-remaining-after-graph-20261019'
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import state,small_cleanup
from history_state import new,pointers
os.environ['GIT_OPTIONAL_LOCKS']='0';os.environ['GIT_NO_LAZY_FETCH']='1'

def load(name):
    spec=importlib.util.spec_from_file_location(name,PARENT/'run.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
parent=load('previous_graph_qualification');scope=load('bindings_qualification')
SKILL=scope.SKILL;SOURCE=scope.SOURCE;TARGETS={SOURCE}
IMPORTS={'CHARACTER_RESPONSE_RELATION_MEMBERS','CHARACTER_RESPONSE_REQUIRED_AXES','CHARACTER_RESPONSE_REQUIRED_EVIDENCE'}
CONSTANTS={'VISUAL_RELATION_CONTRACT_VERSION'};SYMBOLS=IMPORTS|CONSTANTS
MESSAGE='refactor(photo): remove unused generator bindings'
digest=scope.digest;four_patch=scope.four_patch;worker=scope.worker

def parent_files():
    files=dict(parent.baseline()['files'])
    for p,row in state.read(PARENT/'AFTER-DELTA.json.gz')['source_replacements'].items():
        assert files[p]==row['before'];files[p]=row['after']
    return files

def baseline():
    delta=state.read(E/'BASELINE-DELTA.json.gz')
    assert {n:state.sha(PARENT/n) for n in delta['parent_sha256']}==delta['parent_sha256']
    files=parent_files()
    for p,row in delta['preexisting_replacements'].items():
        assert files[p]==row['prior'];files[p]=row['current']
    assert not set(files)&set(delta['additional_files']);files.update(delta['additional_files'])
    return {**delta,'files':files}

def freeze():
    expected=parent_files();paths=set(expected);repositories={}
    for work in state.worktrees():
        dirty={p:s for p,s in state.status(work).items() if work!=ROOT or not scope.owned(p)}
        head=state.git(work,'rev-parse','HEAD').decode().strip()
        staged=state.git(work,'diff','--cached','--raw','-z').decode();assert not staged
        index=Path(state.git(work,'rev-parse','--git-path','index').decode().strip())
        if not index.is_absolute():index=work/index
        repositories[str(work)]={'head':head,'status':dirty,'staged':staged,'index_path':str(index),'index_sha256':state.sha(index)}
        tracked=set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked|set(dirty) if work!=ROOT or not scope.owned(p))
    assert repositories[str(ROOT)]['head']=='0b041177cb9556c1a3e333c0808ff3bc1a480a47'
    current=pointers();assert current==parent.baseline()['pointers'];paths.update(current)
    ordered=sorted(paths);print('capturing fresh protected bytes:',len(ordered),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:actual=dict(zip(ordered,pool.map(state.stamp,ordered)))
    changed={p:{'prior':expected[p],'current':actual[p]} for p in expected if actual[p]!=expected[p]}
    # Existing independent work is the starting state, never reset to an older analysis snapshot.
    assert not set(changed)&({str(ROOT/SOURCE)}|set(current)),list(changed)[:10]
    new(E/'BASELINE-DELTA.json.gz',{'parent':str(PARENT),'parent_sha256':{n:state.sha(PARENT/n) for n in ('run.py','BASELINE-DELTA.json.gz','AFTER-DELTA.json.gz')},
        'preexisting_replacements':changed,'additional_files':{p:actual[p] for p in sorted(paths-set(expected))},
        'repositories':repositories,'pointers':current,'previous_absent':parent.baseline()['previous_absent'],
        'fresh_starting_state':True,'earlier_concurrent_work_restored':False})
    for name in ('REFERENCES.json','PRIVATE-PROBE.json'):shutil.copy2(ANALYSIS/name,E/('INPUT-'+name))
    print('frozen',len(paths),'paths;',len(current),'CURRENT; original dirty',
        {r:len(v['status']) for r,v in repositories.items()},'; preexisting drift',list(changed),flush=True)

def transform(raw,module=None):
    tree=ast.parse(raw);lines=raw.splitlines(keepends=True);remove=set();found=set()
    for node in list(ast.walk(tree)):
        if isinstance(node,ast.ImportFrom) and node.module=='photo_contracts':
            for alias in list(node.names):
                if alias.name in IMPORTS:
                    assert alias.lineno==alias.end_lineno and lines[alias.lineno-1].strip()==alias.name.encode()+b','
                    remove.add(alias.lineno);found.add(alias.name);node.names.remove(alias)
            assert node.names
    for node in list(tree.body):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in CONSTANTS for t in node.targets):
            assert node.lineno==node.end_lineno
            name=next(t.id for t in node.targets if isinstance(t,ast.Name) and t.id in CONSTANTS)
            remove.add(node.lineno);found.add(name);tree.body.remove(node)
    assert found==SYMBOLS and len(remove)==4
    changed=b''.join(line for i,line in enumerate(lines,1) if i not in remove)
    assert ast.dump(tree,include_attributes=False)==ast.dump(ast.parse(changed),include_attributes=False)
    return changed

def prepare():
    before=baseline();private=Path(tempfile.mkdtemp(prefix='photo-generator-bindings-'))
    raw=(ROOT/SOURCE).read_bytes();head=before['repositories'][str(ROOT)]['head'];committed=state.git(ROOT,'show',head+':'+SOURCE)
    assert state.stamp(ROOT/SOURCE)==before['files'][str(ROOT/SOURCE)]
    probe=state.read(E/'INPUT-PRIVATE-PROBE.json');assert digest(raw)==probe['working_source_sha256']
    after,index=transform(raw),transform(committed);assert digest(after)==probe['candidate_sha256']
    refs=state.read(E/'INPUT-REFERENCES.json');assert refs['status']=='PASS' and not refs['parse_failures']
    assert {r['name'] for r in refs['rows']}==SYMBOLS
    assert all(not r['local_loads'] and not r['current_named_consumers'] for r in refs['rows'])
    loads={n.id for n in ast.walk(ast.parse(raw)) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
    assert not loads&SYMBOLS
    payload=small_cleanup.dirty_payload(committed,raw);assert small_cleanup.dirty_payload(index,after)==payload
    patches={label:scope.patch(private,label,a,b) for label,a,b in [('WORKING',raw,after),('INDEX',committed,index)]}
    projects={}
    for label in ('control','combined'):
        project=private/label;skill=four_patch.copy_code(project);projects[label]=str(project)
        if label=='combined':
            (project/SOURCE).write_bytes(after)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/'assets'),str(skill/'assets')],check=True)
            shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
            (project/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
            lock=state.read(SKILL/'embedding-runtime.lock.json');package=skill/lock['package'];package.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(package)],check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
        else:(skill/'.runtime').symlink_to(SKILL/'.runtime',target_is_directory=True)
    project=Path(projects['combined'])
    subprocess.run(['git','-C',str(project),'apply','--reverse',str(private/'WORKING.patch')],check=True)
    assert (project/SOURCE).read_bytes()==raw
    subprocess.run(['git','-C',str(project),'apply',str(private/'WORKING.patch')],check=True)
    new(E/'TARGETS.json',{'base_head':head,'symbols':sorted(SYMBOLS),'functions':[],'constants':sorted(CONSTANTS),
        'imports':{'prompt_generator':sorted(IMPORTS)},'import_bindings_removed':3,'removed_lines':4,'source_added_lines':0,'source_deleted_lines':4,
        'original':{SOURCE:before['files'][str(ROOT/SOURCE)]},'working':{SOURCE:digest(after)},'index':{SOURCE:digest(index)},
        'original_dirty_payload_sha256':{SOURCE:payload},'patches':patches,'remaining_AST_equal':True,
        'working_patch_inverse_exact':True,'original_dirty_payload_equal':True,'provider_import_statement_retained':True})
    new(E/'PRIVATE-PROJECTS.json',{'projects':projects,'private_parent':str(private),'source_files':76,
        'model_and_assets_independent_APFS_clones':True,'original_models_readonly':True,'scratch_is_not_unique_recovery_material':True})
    print('prepared exact four-line HEAD/working patches, original source unchanged',flush=True)

def index_check():
    before=baseline();row=before['repositories'][str(ROOT)];targets=state.read(E/'TARGETS.json')
    assert state.sha(row['index_path'])==row['index_sha256']
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent']);index=private/'qualified.index'
    shutil.copy2(row['index_path'],index);env={**os.environ,'GIT_INDEX_FILE':str(index)}
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:
        subprocess.run(['git','-C',str(ROOT),*args],input=raw,env=env,check=True)
    blob=digest(subprocess.check_output(['git','-C',str(ROOT),'show',':'+SOURCE],env=env));assert blob==targets['index'][SOURCE]
    assert subprocess.check_output(['git','-C',str(ROOT),'diff','--cached','--numstat'],env=env).decode().splitlines()==['0\t4\t'+SOURCE]
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],env=env,check=True)
    assert state.sha(row['index_path'])==row['index_sha256']
    new(E/'INDEX-DRY-RUN.json',{'status':'PASS','source_index_blob':blob,'source_added_lines':0,'source_deleted_lines':4,
        'real_index_unchanged':True,'original_dirty_changes_staged':False})

scope.E=E;scope.ANALYSIS=ANALYSIS;scope.MESSAGE=MESSAGE;scope.FUNCTIONS=set();scope.CONSTANTS=CONSTANTS;scope.SYMBOLS=SYMBOLS
scope.baseline=baseline;scope.transform=transform
GATES=scope.GATES

def apply():
    assert not (E/'APPLICATION.json').exists() and all(state.read(E/n)['status']=='PASS' for n in GATES)
    targets=state.read(E/'TARGETS.json');assert state.stamp(ROOT/SOURCE)==targets['original'][SOURCE]
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head']
    assert not state.git(ROOT,'diff','--cached','--name-only')
    raw=gzip.decompress((E/'WORKING.patch.gz').read_bytes());assert digest(raw)==targets['patches']['WORKING']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--check','-'],input=raw,check=True)
    new(E/'APPLY-INTENT.json',{'gates':{n:state.sha(E/n) for n in GATES},'source_candidate':targets['working']})
    subprocess.run(['git','-C',str(ROOT),'apply','-'],input=raw,check=True)
    assert state.sha(ROOT/SOURCE)==targets['working'][SOURCE]
    new(E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','removed_symbols':sorted(SYMBOLS),
        'source_deleted_lines':4,'source_added_lines':0,'runtime_publish_calls':0,'CURRENT_writes':0,'Gemini_calls':0})
    print('applied exact four-line deletion',flush=True)

CONCURRENT_PREFIX='docs/research-evidence/photo-prompt/candidate-baseline-20261020/'
def check_repositories(before,*,committed=False):
    additions={}
    for work,row in before['repositories'].items():
        current={p:s for p,s in state.status(work).items() if work!=str(ROOT) or not scope.owned(p)}
        assert all(current.get(p)==s for p,s in row['status'].items()),work+': original status changed'
        extra={p:s for p,s in current.items() if p not in row['status']}
        assert all(work==str(ROOT) and p.startswith(CONCURRENT_PREFIX) and s=='??' for p,s in extra.items()),extra
        additions[work]=extra
        assert not state.git(work,'diff','--cached','--raw','-z'),work+': staging changed'
        if not committed or work!=str(ROOT):
            assert state.sha(row['index_path'])==row['index_sha256'],work+': index changed'
            assert state.git(work,'rev-parse','HEAD').decode().strip()==row['head'],work+': HEAD changed'
    assert pointers()==before['pointers']
    assert not any(Path(p).exists() or Path(p).is_symlink() for p in before['previous_absent'])
    return additions

def preservation_review():
    raw=state.read(E/'BEFORE-APPLICATION-FULL.json');assert raw['full']
    assert raw['failures']==[str(ROOT)+': status']
    before=baseline();extra=check_repositories(before)
    new(E/'BEFORE-APPLICATION-REVIEWED.json',{'status':'PASS','protected_paths_checked':raw['checked_paths'],
        'original_bytes_all_unchanged':True,'original_status_entries_unchanged':True,
        'strict_check':'BEFORE-APPLICATION-FULL.json','strict_check_sha256':state.sha(E/'BEFORE-APPLICATION-FULL.json'),
        'strict_failure_review':'Only independently added untracked files; no original path/status/index/HEAD/pointer changed',
        'concurrent_additions':extra,'concurrent_additions_untouched_and_excluded':True,
        'Gemini_calls':0,'CURRENT_writes':0})
    print('preservation review PASS; original paths unchanged, concurrent additions excluded',flush=True)

def verify(output,full=False):
    before=baseline();targets=state.read(E/'TARGETS.json');applied=(E/'APPLICATION.json').exists()
    selected=before['files'] if full else {p:s for p,s in before['files'].items() if p in before['pointers'] or
        Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore')}
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(selected,pool.map(state.stamp,selected)):
            expected=selected[path];good=actual==expected
            if applied and path==str(ROOT/SOURCE):
                good=actual.get('sha256')==targets['working'][SOURCE] and all(actual.get(k)==expected.get(k) for k in ('mode','links'))
            if not good:failures.append(path)
    extra=check_repositories(before)
    if applied:
        raw=transform(state.git(ROOT,'show',targets['base_head']+':'+SOURCE))
        assert small_cleanup.dirty_payload(raw,(ROOT/SOURCE).read_bytes())==targets['original_dirty_payload_sha256'][SOURCE]
    new(output,{'status':'FAIL' if failures else 'PASS','checked_paths':len(selected),'full':full,
        'CURRENT_count':len(before['pointers']),'failures':failures,'original_dirty_payload_preserved':applied,
        'original_status_entries_equal':True,'concurrent_untracked_additions':extra,
        'Gemini_calls':0,'CURRENT_writes':0})
    print('preservation',len(selected),'paths','PASS' if not failures else failures[:8],flush=True)
    assert not failures

scope.GATES=[n if n!='BEFORE-APPLICATION-FULL.json' else 'BEFORE-APPLICATION-REVIEWED.json' for n in scope.GATES]
GATES=scope.GATES
scope.verify=verify

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('command');parser.add_argument('--output',type=Path);parser.add_argument('--full',action='store_true');args=parser.parse_args()
    if args.command=='preservation-review':preservation_review()
    elif args.command=='freeze':freeze()
    elif args.command=='prepare':prepare()
    elif args.command in ('operating','related'):scope.source(args.command)
    elif args.command.startswith('smoke-'):scope.smoke(args.command.removeprefix('smoke-'))
    elif args.command=='verify':scope.verify(args.output,args.full)
    elif args.command=='index-check':index_check()
    elif args.command=='apply':apply()
    else:scope.delegate(args.command)
