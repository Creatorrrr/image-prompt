"""Qualify exactly 14 constants and 6 function-local import bindings."""
import ast,contextlib,difflib,gzip,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path('/Users/chasoik/Projects/image-prompt');SKILL=ROOT/'skills/photo-prompt-image-generator';E=Path(__file__).parent
ANALYSIS=ROOT/'docs/research-evidence/photo-prompt/runtime-skill-remaining-after-bindings-20261020'
PARENT=ROOT/'docs/research-evidence/photo-prompt/runtime-generator-bindings-cleanup-20261020'
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import state,checks,four_patch,four_checks,four_state,small_cleanup,search_helpers_cleanup as helpers
from history_state import new,pointers
os.environ['GIT_OPTIONAL_LOCKS']='0';os.environ['GIT_NO_LAZY_FETCH']='1'
spec=importlib.util.spec_from_file_location('last_binding_cleanup',PARENT/'run.py');parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
REVIEW=state.read(ANALYSIS/'CANDIDATES.json');CONSTANTS=REVIEW['constants'];IMPORTS=REVIEW['local_imports']
BY_PATH={}
for row in CONSTANTS:BY_PATH.setdefault(row['path'],{'constants':[],'imports':[]})['constants'].append(row)
for row in IMPORTS:BY_PATH.setdefault(row['path'],{'constants':[],'imports':[]})['imports'].append(row)
TARGETS=set(BY_PATH);MODULE_PATHS={Path(p).stem:p for p in TARGETS}
MESSAGE='refactor(photo): remove unused constants and local imports'
TESTS=['tests.test_photo_bm25f_retrieval','tests.test_photo_contextual_source_effects','tests.test_photo_workflow_precore','tests.test_photo_precore_feature_selection','tests.test_photo_retry_context']
EXTRA=['tests.test_photo_native_permission_envelope','tests.test_photo_realization_content','tests.test_photo_candidate_realizations','tests.test_photo_image_attempt_evidence']

def digest(raw):return hashlib.sha256(raw).hexdigest()
OWNED_PRIOR=ROOT/'docs/research-evidence/photo-prompt/runtime-constants-local-imports-cleanup-20261020'
def owned(p):return p.startswith((str(E.relative_to(ROOT))+'/',str(OWNED_PRIOR.relative_to(ROOT))+'/'))
def parent_files():
    files=dict(parent.baseline()['files'])
    for p,row in state.read(PARENT/'AFTER-DELTA.json.gz')['source_replacements'].items():
        assert files[p]==row['before'];files[p]=row['after']
    return files

def baseline():
    d=state.read(E/'BASELINE-DELTA.json.gz');assert all(state.sha(PARENT/n)==h for n,h in d['parent_sha256'].items())
    files=parent_files()
    for p,r in d['preexisting_replacements'].items():assert files[p]==r['prior'];files[p]=r['current']
    assert not set(files)&set(d['additional_files']);files.update(d['additional_files'])
    return {**d,'files':files}

def freeze():
    expected=parent_files();paths=set(expected);repos={}
    for work in state.worktrees():
        dirty={p:s for p,s in state.status(work).items() if work!=ROOT or not owned(p)}
        index=Path(state.git(work,'rev-parse','--git-path','index').decode().strip());index=index if index.is_absolute() else work/index
        staged=state.git(work,'diff','--cached','--raw','-z').decode();assert not staged
        repos[str(work)]={'head':state.git(work,'rev-parse','HEAD').decode().strip(),'status':dirty,'staged':staged,'index_path':str(index),'index_sha256':state.sha(index)}
        tracked=set(state.git(work,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(work/p) for p in tracked|set(dirty) if work!=ROOT or not owned(p))
    assert repos[str(ROOT)]['head']=='8563499f95da42bfff2c9448057cadff18ba600f'
    current=pointers();assert current==parent.baseline()['pointers'];paths.update(current)
    paths=sorted(paths);print('capturing fresh protection:',len(paths),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:actual=dict(zip(paths,pool.map(state.stamp,paths)))
    drift={p:{'prior':s,'current':actual[p]} for p,s in expected.items() if actual[p]!=s}
    approved=state.read(E/'INPUT-CONCURRENT-SOURCE-CHANGE.json')['changes']
    assert all(actual[str(ROOT/p)]==row['current'] for p,row in approved.items())
    assert not set(drift)&(set(current)|{str(ROOT/p) for p in TARGETS if p not in approved}),list(drift)[:5]
    new(E/'BASELINE-DELTA.json.gz',{'parent':str(PARENT),'parent_sha256':{n:state.sha(PARENT/n) for n in ('run.py','BASELINE-DELTA.json.gz','AFTER-DELTA.json.gz')},
        'preexisting_replacements':drift,'additional_files':{p:actual[p] for p in paths if p not in expected},
        'repositories':repos,'pointers':current,'previous_absent':parent.baseline()['previous_absent']})
    for n in ('CANDIDATES.json','INVENTORY.json','PRIVATE-PROBE.json','PRESERVATION.json','FINAL-CHECK.json'):shutil.copy2(ANALYSIS/n,E/('INPUT-'+n))
    print('frozen',len(paths),'paths;',len(current),'CURRENT; dirty',{r:len(v['status']) for r,v in repos.items()},'; preexisting drift',list(drift),flush=True)

def transform(raw,module):
    path=MODULE_PATHS[module];rows=BY_PATH[path];tree=ast.parse(raw);lines=raw.splitlines(keepends=True);remove=set();found=[]
    for row in rows['constants']:
        node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==row['name'] for t in n.targets))
        assert digest(b''.join(lines[node.lineno-1:node.end_lineno]))==row['raw_sha256']
        remove.update(range(node.lineno,node.end_lineno+1));tree.body.remove(node)
    parents={c:n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
    for row in rows['imports']:
        owner=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==row['owner'])
        matches=[n for n in ast.walk(owner) if isinstance(n,(ast.Import,ast.ImportFrom)) and any((a.asname or a.name.split('.')[0])==row['binding'] for a in n.names)]
        assert len(matches)==1;node=matches[0];assert ast.get_source_segment(raw.decode(),node)==row['statement']
        assert not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id==row['binding'] for n in ast.walk(owner))
        alias=next(a for a in node.names if (a.asname or a.name.split('.')[0])==row['binding'])
        if len(node.names)>1:
            token=b', '+alias.name.encode();assert lines[node.lineno-1].count(token)==1
            lines[node.lineno-1]=lines[node.lineno-1].replace(token,b'',1);node.names.remove(alias)
        else:
            par=parents[node]
            field=next(k for k in ('body','orelse','finalbody') if node in getattr(par,k,[]));getattr(par,field).remove(node)
            remove.update(range(node.lineno,node.end_lineno+1))
    changed=b''.join(v for i,v in enumerate(lines,1) if i not in remove)
    assert ast.dump(tree,include_attributes=False)==ast.dump(ast.parse(changed),include_attributes=False)
    return changed

def patch(private,label,before,after):
    out=[]
    for path in sorted(TARGETS):
        d=private/'patch-input'/label/Path(path).stem;d.mkdir(parents=True);a=d/'before.py';b=d/'after.py';a.write_bytes(before[path]);b.write_bytes(after[path])
        p=subprocess.run(['git','diff','--no-index','--no-ext-diff','--no-color','--diff-algorithm=myers','--',str(a),str(b)],capture_output=True,text=True);assert p.returncode==1
        for line in p.stdout.splitlines(keepends=True):
            if line.startswith('diff --git '):line='diff --git a/'+path+' b/'+path+'\n'
            elif line.startswith('--- '):line='--- a/'+path+'\n'
            elif line.startswith('+++ '):line='+++ b/'+path+'\n'
            out.append(line)
    raw=''.join(out).encode();(private/(label+'.patch')).write_bytes(raw);(E/(label+'.patch.gz')).write_bytes(gzip.compress(raw,mtime=0))
    return {'raw_sha256':digest(raw),'sha256':state.sha(E/(label+'.patch.gz'))}

def prepare():
    b=baseline();private=Path(tempfile.mkdtemp(prefix='photo-constants-local-imports-'));head=b['repositories'][str(ROOT)]['head']
    before={p:(ROOT/p).read_bytes() for p in TARGETS};heads={p:state.git(ROOT,'show',head+':'+p) for p in TARGETS}
    assert all(state.stamp(ROOT/p)==b['files'][str(ROOT/p)] for p in TARGETS)
    old=state.read(E/'INPUT-PRIVATE-PROBE.json');predicted={r['path']:r for r in old['details'] if r['variant']=='combined'}
    concurrent=state.read(E/'INPUT-CONCURRENT-SOURCE-CHANGE.json')['changes']
    assert all(digest(v)==(concurrent[p]['current']['sha256'] if p in concurrent else predicted[p]['before_sha256']) for p,v in before.items())
    work={p:transform(v,Path(p).stem) for p,v in before.items()};index={p:transform(v,Path(p).stem) for p,v in heads.items()}
    assert all(digest(v)==predicted[p]['candidate_sha256'] for p,v in work.items() if p not in concurrent)
    payloads={p:small_cleanup.dirty_payload(heads[p],before[p]) for p in TARGETS}
    assert all(small_cleanup.dirty_payload(index[p],work[p])==payloads[p] for p in TARGETS)
    patches={label:patch(private,label,a,b) for label,a,b in [('WORKING',before,work),('INDEX',heads,index)]};projects={}
    for label in ('control','combined'):
        project=private/label;skill=four_patch.copy_code(project);projects[label]=str(project)
        if label=='combined':
            for p,v in work.items():(project/p).write_bytes(v)
        subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/'assets'),str(skill/'assets')],check=True)
        shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
        (project/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
        (skill/'references').mkdir();shutil.copy2(SKILL/'references/image-runtime.md',skill/'references/image-runtime.md')
        if label=='combined':
            lock=state.read(SKILL/'embedding-runtime.lock.json');package=skill/lock['package'];package.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(package)],check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
        else:
            lock=state.read(SKILL/'embedding-runtime.lock.json');package=skill/lock['package'];package.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(package)],check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
    project=Path(projects['combined']);subprocess.run(['git','-C',str(project),'apply','--reverse',str(private/'WORKING.patch')],check=True)
    assert all((project/p).read_bytes()==v for p,v in before.items())
    subprocess.run(['git','-C',str(project),'apply',str(private/'WORKING.patch')],check=True)
    new(E/'TARGETS.json',{'base_head':head,'constants':CONSTANTS,'local_imports':IMPORTS,'source_paths':sorted(TARGETS),
        'constant_count':14,'constant_lines':178,'local_import_count':6,'source_added_lines':1,'source_deleted_lines':184,
        'original':{p:b['files'][str(ROOT/p)] for p in TARGETS},'working':{p:digest(v) for p,v in work.items()},'index':{p:digest(v) for p,v in index.items()},
        'original_dirty_payload_sha256':payloads,'patches':patches,'remaining_AST_equal':True,'working_patch_inverse_exact':True,'original_dirty_payload_equal':True})
    new(E/'PRIVATE-PROJECTS.json',{'projects':projects,'private_parent':str(private),'source_files':76,'independent_assets':True,'combined_model_APFS_cloned':True,'scratch_is_not_unique_recovery_material':True})
    print('exact 8-path HEAD/working candidates prepared: +1/-184',flush=True)

def worker(project,removed,modules,policy,timeout=900,log=None):
    old=helpers.E;helpers.E=E
    try:return helpers.worker(project,removed,modules,policy,timeout,log)
    finally:helpers.E=old

def source(group):
    project=Path(state.read(E/'PRIVATE-PROJECTS.json')['projects']['combined']);mods=checks.GROUPS['operating'] if group=='operating' else TESTS if group=='related' else EXTRA
    r=worker(project,True,mods,four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))',900)
    new(E/('SOURCE-'+group+'.json'),{**r,'network_denied':True,'original_writes_denied':True,'original_source_reads_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    assert r['status']=='PASS' and r['exit_code']==0 and not r['skipped'],r.get('stderr','')[-4000:]
    if group in ('operating','related'):assert r['tests']==(48 if group=='operating' else 43)
    else:assert r['tests']==67
    print(group,'PASS',r['tests'],flush=True)

def smoke(label):
    project=ROOT if label=='applied' else Path(state.read(E/'PRIVATE-PROJECTS.json')['projects'][label])
    policy=checks.profile() if label=='applied' else four_patch.policy()
    if label=='applied':policy+='(deny file-read* (regex '+json.dumps('^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    r=worker(project,label!='control',[],policy+'(deny file-read* (regex "/site-packages/torch(/|$)"))',90)
    new(E/('SMOKE-'+label+'.json'),{**r,'network_denied':True,'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    assert r['status']=='PASS';print(label,'smoke PASS',flush=True)

def delegate(command):
    old=four_state.E;four_state.E=E
    try:
        if command.startswith('managed-'):four_checks.managed(command.removeprefix('managed-'))
        elif command.startswith('history-'):four_checks.history(command.removeprefix('history-'))
        elif command=='installed':four_checks.installed()
        else:raise ValueError(command)
    finally:four_state.E=old

def index_check():
    b=baseline();r=b['repositories'][str(ROOT)];t=state.read(E/'TARGETS.json');assert state.sha(r['index_path'])==r['index_sha256']
    index=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent'])/'qualified.index';shutil.copy2(r['index_path'],index);env={**os.environ,'GIT_INDEX_FILE':str(index)}
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:subprocess.run(['git','-C',str(ROOT),*args],input=raw,env=env,check=True)
    actual={p:digest(subprocess.check_output(['git','-C',str(ROOT),'show',':'+p],env=env)) for p in TARGETS};assert actual==t['index']
    stats=subprocess.check_output(['git','-C',str(ROOT),'diff','--cached','--numstat'],env=env).decode().splitlines()
    assert {s.split('\t')[2] for s in stats}==TARGETS and sum(int(s.split('\t')[0]) for s in stats)==1 and sum(int(s.split('\t')[1]) for s in stats)==184
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],env=env,check=True);assert state.sha(r['index_path'])==r['index_sha256']
    new(E/'INDEX-DRY-RUN.json',{'status':'PASS','source_blobs':actual,'source_added_lines':1,'source_deleted_lines':184,'real_index_unchanged':True,'original_dirty_changes_staged':False})

def repo_check(b,committed=False):
    extras={}
    for work,row in b['repositories'].items():
        current={p:s for p,s in state.status(work).items() if work!=str(ROOT) or not owned(p)}
        expected_status=dict(row['status'])
        if work==str(ROOT) and not committed and (E/'APPLICATION.json').exists():
            for rel in TARGETS:
                if rel not in expected_status:expected_status[rel]=' M'
        assert all(current.get(p)==s for p,s in expected_status.items()),work+': original/approved Git entries changed'
        extra={p:s for p,s in current.items() if p not in expected_status}
        assert all(s=='??' for s in extra.values()),extra;extras[work]=extra
        assert not state.git(work,'diff','--cached','--raw','-z'),work+': staging changed'
        if not committed or work!=str(ROOT):
            assert state.git(work,'rev-parse','HEAD').decode().strip()==row['head'];assert state.sha(row['index_path'])==row['index_sha256']
    assert pointers()==b['pointers'];assert not any(Path(p).exists() or Path(p).is_symlink() for p in b['previous_absent'])
    return extras

def verify(output,full=False,committed=False):
    b=baseline();t=state.read(E/'TARGETS.json');applied=(E/'APPLICATION.json').exists();files=b['files'] if full else {p:s for p,s in b['files'].items() if p in b['pointers'] or Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore')}
    failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for p,actual in zip(files,pool.map(state.stamp,files)):
            good=actual==files[p]
            rel=str(Path(p).relative_to(ROOT)) if Path(p).is_relative_to(ROOT) else None
            if applied and rel in TARGETS:good=actual.get('sha256')==t['working'][rel] and all(actual.get(k)==files[p].get(k) for k in ('mode','links'))
            if not good:failures.append(p)
    extras=repo_check(b,committed)
    if applied:
        assert all(small_cleanup.dirty_payload(transform(state.git(ROOT,'show',t['base_head']+':'+p),Path(p).stem),(ROOT/p).read_bytes())==t['original_dirty_payload_sha256'][p] for p in TARGETS)
    new(output,{'status':'PASS' if not failures else 'FAIL','checked_paths':len(files),'full':full,'failures':failures,'CURRENT_count':len(b['pointers']),
        'original_status_entries_equal':True,'concurrent_additional_untracked':extras,'original_dirty_payload_preserved':applied,'Gemini_calls':0,'CURRENT_writes':0})
    print('preservation',len(files),'PASS' if not failures else failures[:6],flush=True);assert not failures

GATES=['REFERENCE-CHECK.json','SMOKE-control.json','SMOKE-combined.json','SMOKE-COMPARISON.json','SOURCE-operating.json','SOURCE-related.json','SOURCE-extra.json','SOURCE-extra-control.json','HEAD-COMPARISON.json','NATIVE-BRANCH-COMPARISON.json','CONCURRENT-REBASE-CHECK.json','SOURCE-concurrent-control.json','SOURCE-concurrent-combined.json','INDEX-DRY-RUN.json','BEFORE-APPLICATION-FULL.json','MANAGED-control.json','MANAGED-combined.json','INSTALLED.json','HISTORY-frozen.json','HISTORY-archive.json','HISTORY-negative.json','HISTORY-native-view.json']
POST=['SMOKE-applied.json','MANAGED-applied.json','HISTORY-native-view-applied.json','AFTER-PRESERVATION.json']
def apply():
    assert not (E/'APPLICATION.json').exists();t=state.read(E/'TARGETS.json');assert all(state.read(E/n)['status']=='PASS' for n in GATES)
    assert all(state.stamp(ROOT/p)==t['original'][p] for p in TARGETS);assert not state.git(ROOT,'diff','--cached','--name-only')
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==t['base_head']
    raw=gzip.decompress((E/'WORKING.patch.gz').read_bytes());assert digest(raw)==t['patches']['WORKING']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--check','-'],input=raw,check=True)
    new(E/'APPLY-INTENT.json',{'gates':{n:state.sha(E/n) for n in GATES},'source_candidates':t['working']})
    subprocess.run(['git','-C',str(ROOT),'apply','-'],input=raw,check=True)
    assert all(state.sha(ROOT/p)==h for p,h in t['working'].items())
    new(E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','source_added_lines':1,'source_deleted_lines':184,'Gemini_calls':0,'CURRENT_writes':0,'publishes':0});print('applied exact qualified +1/-184',flush=True)

# The other task finished an independent source repair and installed its new release.
# Keep the original boundary and all failures intact; append a pinned current boundary.
initial_baseline=baseline
def operating_baseline():
    b=initial_baseline();path=E/'OPERATING-BASELINE-DELTA.json.gz'
    if not path.exists():return b
    d=state.read(path);assert d['parent_baseline_sha256']==state.sha(E/'BASELINE-DELTA.json.gz')
    files=dict(b['files'])
    for p,row in d['preexisting_external_replacements'].items():assert files[p]==row['before'];files[p]=row['after']
    assert not set(files)&set(d['additional_files']);files.update(d['additional_files'])
    return {**b,'files':files,'repositories':d['repositories'],'pointers':d['pointers'],'operating':d['installed']}
baseline=operating_baseline
GATES=[{'BEFORE-APPLICATION-FULL.json':'OPERATING-BEFORE-APPLICATION-FULL.json','MANAGED-control.json':'MANAGED-control-pinned.json','MANAGED-combined.json':'MANAGED-combined-pinned.json'}.get(n,n) for n in GATES]
GATES+=['OPERATING-BOUNDARY.json','CURRENT-FRONTENDS.json','MANAGED-control-CLOSURE.json','MANAGED-combined-CLOSURE.json']
POST=[n if n!='MANAGED-applied.json' else 'MANAGED-applied-pinned.json' for n in POST]+['MANAGED-applied-CLOSURE.json']

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command');p.add_argument('--output',type=Path);p.add_argument('--full',action='store_true');a=p.parse_args()
    if a.command=='freeze':freeze()
    elif a.command=='prepare':prepare()
    elif a.command in ('operating','related','extra'):source(a.command)
    elif a.command.startswith('smoke-'):smoke(a.command.removeprefix('smoke-'))
    elif a.command=='index-check':index_check()
    elif a.command=='verify':verify(a.output,a.full)
    elif a.command=='apply':apply()
    else:delegate(a.command)
