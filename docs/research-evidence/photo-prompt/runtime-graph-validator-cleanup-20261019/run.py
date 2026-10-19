"""Qualify one exact legacy-validator deletion, preserving concurrent work."""
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import contextlib
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path('/Users/chasoik/Projects/image-prompt')
SKILL=ROOT/'skills/photo-prompt-image-generator'
E=Path(__file__).parent
ANALYSIS=ROOT/'docs/research-evidence/photo-prompt/runtime-skill-logic-data-review-20261019'
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import checks
import four_checks
import four_patch
import four_state
import search_helpers_cleanup as previous
import small_cleanup
import state
from history_state import new,pointers

os.environ['GIT_OPTIONAL_LOCKS']='0'
os.environ['GIT_NO_LAZY_FETCH']='1'
FUNCTIONS={'character_runtime_node_topic_ids','character_runtime_node_family_ids','validate_character_mechanism_graph'}
CONSTANTS={'CHARACTER_MECHANISM_GRAPH_SCHEMA','CHARACTER_RESPONSE_RELATION_FIELDS','CHARACTER_CONCEPT_EVIDENCE_ROLES'}
SYMBOLS=FUNCTIONS|CONSTANTS
SOURCE='skills/photo-prompt-image-generator/scripts/prompt_generator.py'
TARGETS={SOURCE}
MESSAGE='refactor(photo): remove obsolete character graph validator'
TESTS=['tests.test_photo_bm25f_retrieval','tests.test_photo_contextual_source_effects',
    'tests.test_photo_workflow_precore','tests.test_photo_precore_feature_selection','tests.test_photo_retry_context']


def digest(raw):return hashlib.sha256(raw).hexdigest()


def owned(relative):return relative.startswith(str(E.relative_to(ROOT))+'/')


def previous_files():
    protection=E/'PREVIOUS-PROTECTION.json.gz'
    delta=state.read(protection if protection.exists() else ANALYSIS/'PROTECTION-DELTA.json.gz')
    parent=Path(delta['parent']);assert parent==previous.E
    assert state.sha(parent/'BASELINE-DELTA.json.gz')==delta['parent_baseline_sha256']
    assert state.sha(parent/'AFTER-DELTA.json.gz')==delta['parent_after_sha256']
    files=dict(previous.baseline()['files'])
    for path,row in state.read(parent/'AFTER-DELTA.json.gz')['source_replacements'].items():
        assert files[path]==row['before'];files[path]=row['after']
    assert not set(files)&set(delta['additional_files'])
    files.update(delta['additional_files'])
    return files


def baseline():
    delta=state.read(E/'BASELINE-DELTA.json.gz')
    assert state.sha(E/'PREVIOUS-PROTECTION.json.gz')==delta['analysis_protection_sha256']
    files=previous_files()
    assert not set(files)&set(delta['additional_files'])
    files.update(delta['additional_files'])
    return {**delta,'files':files}


def freeze():
    assert state.read(ANALYSIS/'PRESERVATION.json')['status']=='PASS'
    expected=previous_files();paths=set(expected);repositories={}
    for work in state.worktrees():
        dirty={p:s for p,s in state.status(work).items() if work!=ROOT or not owned(p)}
        head=state.git(work,'rev-parse','HEAD').decode().strip()
        staged=state.git(work,'diff','--cached','--raw','-z').decode();assert not staged
        index=Path(state.git(work,'rev-parse','--git-path','index').decode().strip())
        if not index.is_absolute():index=work/index
        repositories[str(work)]={'head':head,'status':dirty,'staged':staged,
            'index_path':str(index),'index_sha256':state.sha(index)}
        tracked=set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked|set(dirty) if work!=ROOT or not owned(p))
    assert repositories[str(ROOT)]['head']=='7c536d9b6084226ff6a8941de9718c9a78ffd218'
    current=pointers();assert current==state.read(ANALYSIS/'PROTECTION-DELTA.json.gz')['pointers']
    paths.update(current)
    for old,new_name in [('PROTECTION-DELTA.json.gz','PREVIOUS-PROTECTION.json.gz'),
            ('GRAPH-PRESERVED.json','INPUT-GRAPH-PRESERVED.json'),('REFERENCES.json','INPUT-REFERENCES.json')]:
        shutil.copy2(ANALYSIS/old,E/new_name)
    additions={p:state.stamp(p) for p in sorted(paths-set(expected))}
    new(E/'BASELINE-DELTA.json.gz',{'additional_files':additions,'repositories':repositories,
        'pointers':current,'previous_absent':state.read(ANALYSIS/'PROTECTION-DELTA.json.gz')['previous_absent'],
        'analysis_protection_sha256':state.sha(ANALYSIS/'PROTECTION-DELTA.json.gz')})
    print('frozen',len(expected)+len(additions),'protected paths;',len(current),'CURRENT;',
        {r:len(v['status']) for r,v in repositories.items()},flush=True)


def transform(raw,module=None):
    tree=ast.parse(raw);lines=raw.splitlines(keepends=True);remove=set();found=set()
    for node in list(tree.body):
        name=node.name if isinstance(node,ast.FunctionDef) else None
        if isinstance(node,ast.Assign):
            name=next((target.id for target in node.targets if isinstance(target,ast.Name)),None)
        if name in SYMBOLS:
            assert (isinstance(node,ast.FunctionDef) and name in FUNCTIONS) or (isinstance(node,ast.Assign) and name in CONSTANTS)
            remove.update(range(node.lineno,node.end_lineno+1));tree.body.remove(node);found.add(name)
    assert found==SYMBOLS and len(remove)==397
    changed=b''.join(line for i,line in enumerate(lines,1) if i not in remove)
    assert ast.dump(tree,include_attributes=False)==ast.dump(ast.parse(changed),include_attributes=False)
    return changed


def patch(private,label,before,after):
    directory=private/label;directory.mkdir()
    a,b=directory/'before.py',directory/'after.py';a.write_bytes(before);b.write_bytes(after)
    child=subprocess.run(['git','diff','--no-index','--no-ext-diff','--no-color','--diff-algorithm=myers','--',str(a),str(b)],capture_output=True,text=True)
    assert child.returncode==1
    output=[]
    for line in child.stdout.splitlines(keepends=True):
        if line.startswith('diff --git '):line='diff --git a/'+SOURCE+' b/'+SOURCE+'\n'
        elif line.startswith('--- '):line='--- a/'+SOURCE+'\n'
        elif line.startswith('+++ '):line='+++ b/'+SOURCE+'\n'
        output.append(line)
    raw=''.join(output).encode();(E/(label+'.patch.gz')).write_bytes(gzip.compress(raw,mtime=0))
    path=private/(label+'.patch');path.write_bytes(raw)
    return {'raw_sha256':digest(raw),'sha256':state.sha(E/(label+'.patch.gz'))}


def prepare():
    before=baseline();private=Path(tempfile.mkdtemp(prefix='photo-graph-validator-'))
    working=(ROOT/SOURCE).read_bytes();head=before['repositories'][str(ROOT)]['head']
    committed=state.git(ROOT,'show',head+':'+SOURCE)
    assert state.stamp(ROOT/SOURCE)==before['files'][str(ROOT/SOURCE)]
    after,staged=transform(working),transform(committed)
    payload=small_cleanup.dirty_payload(committed,working)
    assert small_cleanup.dirty_payload(staged,after)==payload
    reviewed=state.read(E/'INPUT-GRAPH-PRESERVED.json')
    assert all(row['raw_bytes_equal_all_three'] for row in reviewed['targets'].values())
    approved=state.read(E/'INPUT-REFERENCES.json')['graph_candidates']
    assert {row['name'] for row in approved}==SYMBOLS and sum(row['lines'] for row in approved)==397
    for node in ast.parse(working).body:
        name=node.name if isinstance(node,ast.FunctionDef) else next((t.id for t in node.targets if isinstance(t,ast.Name)),None) if isinstance(node,ast.Assign) else None
        if name in SYMBOLS:
            raw=b''.join(working.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
            assert digest(raw)==reviewed['targets'][name]['working']
    patches={label:patch(private,label,a,b) for label,a,b in [('WORKING',working,after),('INDEX',committed,staged)]}
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
    assert (project/SOURCE).read_bytes()==working
    subprocess.run(['git','-C',str(project),'apply',str(private/'WORKING.patch')],check=True)
    new(E/'TARGETS.json',{'base_head':head,'symbols':sorted(SYMBOLS),'functions':sorted(FUNCTIONS),
        'constants':sorted(CONSTANTS),'imports':{'prompt_generator':[]},'removed_lines':397,
        'source_added_lines':0,'source_deleted_lines':397,
        'original':{SOURCE:before['files'][str(ROOT/SOURCE)]},'working':{SOURCE:digest(after)},
        'index':{SOURCE:digest(staged)},'original_dirty_payload_sha256':{SOURCE:payload},'patches':patches,
        'remaining_AST_equal':True,'working_patch_inverse_exact':True,'original_dirty_payload_equal':True,
        'reviewed_source_sha256':state.sha(E/'INPUT-GRAPH-PRESERVED.json')})
    new(E/'PRIVATE-PROJECTS.json',{'projects':projects,'private_parent':str(private),'source_files':76,
        'model_and_assets_independent_APFS_clones':True,'original_models_readonly':True,'scratch_is_not_unique_recovery_material':True})
    print('exact 397-line candidates prepared; original worktree unchanged',flush=True)


@contextlib.contextmanager
def check_scope():
    original=previous.E;previous.E=E
    try:yield
    finally:previous.E=original


def worker(*args,**kwargs):
    with check_scope():return previous.worker(*args,**kwargs)


def source(group):
    project=Path(state.read(E/'PRIVATE-PROJECTS.json')['projects']['combined'])
    modules=checks.GROUPS['operating'] if group=='operating' else TESTS
    expected=48 if group=='operating' else 43
    result=worker(project,True,modules,four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))',600)
    new(E/('SOURCE-'+group+'.json'),{**result,'network_denied':True,'original_source_reads_denied':True,
        'original_writes_denied':True,'torch_module_read_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    assert result.get('status')=='PASS' and result.get('tests')==expected and result.get('skipped')==0,result.get('stderr','')[-5000:]
    assert result['loaded_modules']['prompt_generator']['sha256']==state.read(E/'TARGETS.json')['working'][SOURCE]
    print(group,'PASS',result['tests'],'tests',flush=True)


def smoke(kind):
    project=ROOT if kind=='applied' else Path(state.read(E/'PRIVATE-PROJECTS.json')['projects'][kind])
    policy=checks.profile() if kind=='applied' else four_patch.policy()
    policy+='(deny file-read* (regex "/site-packages/torch(/|$)"))'
    if kind=='applied':
        policy+='(deny file-read* (regex '+json.dumps('^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    result=worker(project,kind!='control',[],policy,90)
    targets=state.read(E/'TARGETS.json')
    expected=targets['original'][SOURCE]['sha256'] if kind=='control' else targets['working'][SOURCE]
    assert result['loaded_modules']['prompt_generator']['sha256']==expected
    new(E/('SMOKE-'+kind+'.json'),{**result,'network_denied':True,'original_writes_denied':True,
        'actual_source_hash_verified':True,'original_bytecode_reads_denied':kind=='applied'})
    assert result['status']=='PASS'
    print(kind,'smoke PASS',flush=True)


def delegate(kind):
    with check_scope():previous.delegate(kind)


def index_check():
    before=baseline();row=before['repositories'][str(ROOT)];targets=state.read(E/'TARGETS.json')
    assert state.sha(row['index_path'])==row['index_sha256']
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent']);index=private/'qualified.index'
    shutil.copy2(row['index_path'],index);env={**os.environ,'GIT_INDEX_FILE':str(index)}
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:
        subprocess.run(['git','-C',str(ROOT),*args],input=raw,env=env,check=True)
    blob=digest(subprocess.check_output(['git','-C',str(ROOT),'show',':'+SOURCE],env=env))
    assert blob==targets['index'][SOURCE]
    stats=subprocess.check_output(['git','-C',str(ROOT),'diff','--cached','--numstat'],env=env).decode().splitlines()
    assert stats==['0\t397\t'+SOURCE],stats
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],env=env,check=True)
    assert state.sha(row['index_path'])==row['index_sha256']
    new(E/'INDEX-DRY-RUN.json',{'status':'PASS','source_index_blob':blob,'source_added_lines':0,
        'source_deleted_lines':397,'real_index_unchanged':True,'original_dirty_changes_staged':False})


def verify(output,full=False):
    before=baseline();targets=state.read(E/'TARGETS.json');applied=(E/'APPLICATION.json').exists()
    selected=before['files'] if full else {p:s for p,s in before['files'].items() if p in before['pointers'] or
        Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore') or Path(p).name in
        {'retrieval-runtime.json','embedding-default.json','embedding-runtime.lock.json'}}
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,actual in zip(selected,pool.map(state.stamp,selected)):
            good=actual==selected[path]
            if applied and path==str(ROOT/SOURCE):
                good=actual.get('sha256')==targets['working'][SOURCE] and all(actual.get(k)==selected[path].get(k) for k in ('mode','links'))
            if not good:failures.append(path)
    for work,row in before['repositories'].items():
        current={p:s for p,s in state.status(work).items() if work!=str(ROOT) or not owned(p)}
        if current!=row['status']:failures.append(work+': status')
        if state.sha(row['index_path'])!=row['index_sha256'] or state.git(work,'diff','--cached','--raw','-z').decode()!=row['staged']:failures.append(work+': index/staging')
        if state.git(work,'rev-parse','HEAD').decode().strip()!=row['head']:failures.append(work+': HEAD')
    if pointers()!=before['pointers']:failures.append('CURRENT inventory')
    failures.extend(p for p in before['previous_absent'] if Path(p).exists() or Path(p).is_symlink())
    if applied:
        raw=transform(state.git(ROOT,'show',targets['base_head']+':'+SOURCE))
        if small_cleanup.dirty_payload(raw,(ROOT/SOURCE).read_bytes())!=targets['original_dirty_payload_sha256'][SOURCE]:failures.append('original dirty payload')
    new(output,{'status':'FAIL' if failures else 'PASS','checked_paths':len(selected),'full':full,
        'CURRENT_count':len(before['pointers']),'failures':failures,'original_dirty_payload_preserved':applied,
        'Gemini_calls':0,'CURRENT_writes':0})
    print('preservation',len(selected),'paths','PASS' if not failures else failures[:8],flush=True)
    assert not failures


GATES=['SMOKE-control.json','SMOKE-combined.json','SMOKE-COMPARISON.json','SOURCE-operating.json','SOURCE-related.json',
    'HEAD-COMPARISON.json','INDEX-DRY-RUN.json','BEFORE-APPLICATION-FULL.json',
    'MANAGED-control.json','MANAGED-combined.json','INSTALLED.json','HISTORY-frozen.json',
    'HISTORY-archive.json','HISTORY-negative.json','HISTORY-native-view.json']


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
        'source_deleted_lines':397,'source_added_lines':0,'runtime_publish_calls':0,'CURRENT_writes':0,'Gemini_calls':0})
    print('applied exact approved 397-line deletion',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command');parser.add_argument('--output',type=Path);parser.add_argument('--full',action='store_true');args=parser.parse_args()
    if args.command=='freeze':freeze()
    elif args.command=='prepare':prepare()
    elif args.command in ('operating','related'):source(args.command)
    elif args.command.startswith('smoke-'):smoke(args.command.removeprefix('smoke-'))
    elif args.command=='verify':verify(args.output,args.full)
    elif args.command=='index-check':index_check()
    elif args.command=='apply':apply()
    else:delegate(args.command)
