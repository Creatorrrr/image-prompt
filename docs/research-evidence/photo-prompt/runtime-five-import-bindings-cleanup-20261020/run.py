"""Qualify exactly five import bindings; keep dirty source and all sealed data."""
import ast,contextlib,difflib,gzip,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT=Path('/Users/chasoik/Projects/image-prompt');SKILL=ROOT/'skills/photo-prompt-image-generator';E=Path(__file__).parent
ANALYSIS=ROOT/'docs/research-evidence/photo-prompt/runtime-skill-remaining-after-constants-20261020'
PARENT=ROOT/'docs/research-evidence/photo-prompt/runtime-constants-local-imports-cleanup-rebased-20261020'
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import state,checks,four_patch,four_checks,four_state,small_cleanup
from history_state import new,pointers
os.environ.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1')
ROWS=state.read(ANALYSIS/'INVENTORY.json')['priority_imports'];assert len(ROWS)==5
BY_PATH={}
for row in ROWS:BY_PATH.setdefault(row['path'],[]).append(row)
TARGETS=set(BY_PATH);assert len(TARGETS)==3
MESSAGE='refactor(photo): remove five unused import bindings'
TESTS=['tests.test_photo_bm25f_retrieval','tests.test_photo_contextual_source_effects','tests.test_photo_workflow_precore','tests.test_photo_precore_feature_selection','tests.test_photo_retry_context']
NATIVE=list(dict.fromkeys([*checks.GROUPS['native'],'tests.test_photo_api_render_preflight','tests.test_photo_native_permission_envelope','tests.test_photo_image_attempt_evidence']))
APPLIED_NATIVE=['tests.test_photo_contextual_source_effects','tests.test_photo_workflow_runtime_bridge','tests.test_photo_workflow_transport_bindings','tests.test_photo_api_render_preflight']
def digest(raw):return hashlib.sha256(raw).hexdigest()
def owned(p):return p.startswith(str(E.relative_to(ROOT))+'/')
def previous():
    spec=importlib.util.spec_from_file_location('qualified_constants_scope',PARENT/'run.py');scope=importlib.util.module_from_spec(spec);spec.loader.exec_module(scope)
    b=scope.baseline();files=dict(b['files'])
    for path,row in state.read(PARENT/'AFTER-DELTA.json.gz')['source_replacements'].items():
        assert files[path]==row['before'];files[path]=row['after']
    return {**b,'files':files}
def baseline():
    d=state.read(E/'BASELINE-DELTA.json.gz')
    assert all(state.sha(PARENT/n)==h for n,h in d['parent_sha256'].items())
    files=dict(previous()['files'])
    for p,row in d['preexisting_replacements'].items():assert files[p]==row['before'];files[p]=row['after']
    assert not set(files)&set(d['additional_files']);files.update(d['additional_files'])
    return {**d,'files':files}
def freeze():
    prior=previous();paths=set(prior['files']);repos={}
    for wt in state.worktrees():
        status={p:s for p,s in state.status(wt).items() if wt!=ROOT or not owned(p)}
        staged=state.git(wt,'diff','--cached','--raw','-z').decode();assert not staged
        idx=Path(state.git(wt,'rev-parse','--git-path','index').decode().strip());idx=idx if idx.is_absolute() else wt/idx
        repos[str(wt)]={'head':state.git(wt,'rev-parse','HEAD').decode().strip(),'status':status,'staged':staged,'index_path':str(idx),'index_sha256':state.sha(idx)}
        tracked=set(state.git(wt,'ls-files','-z').decode().split('\0'))-{''}
        paths.update(str(wt/p) for p in tracked|set(status) if wt!=ROOT or not owned(p))
    assert repos[str(ROOT)]['head']=='09a12e6a359689acc166efb3ff934e5b0e9015a3'
    cur=pointers();assert cur==prior['pointers'];paths.update(cur);paths=sorted(paths)
    print('capturing',len(paths),'protected paths',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:actual=dict(zip(paths,pool.map(state.stamp,paths)))
    drift={p:{'before':v,'after':actual[p]} for p,v in prior['files'].items() if actual[p]!=v}
    assert not set(drift)&set(cur), 'CURRENT drift before this task must be inspected'
    for row in ROWS:assert actual[str(ROOT/row['path'])]['sha256']==row['source_sha256']
    cfg=state.read(SKILL/'retrieval-runtime.json');store=state.SHARED/cfg['store_subdirectory']
    fixture=ROOT/'docs/research-evidence/photo-prompt/candidate-contract-source-repair-20261020/installed-managed/run'
    assert state.read(fixture/'workflow.json')['phase']=='prompt_delivered'
    new(E/'BASELINE-DELTA.json.gz',{'parent':str(PARENT),'parent_sha256':{n:state.sha(PARENT/n) for n in ('run.py','BASELINE-DELTA.json.gz','OPERATING-BASELINE-DELTA.json.gz','AFTER-DELTA.json.gz')},
        'preexisting_replacements':drift,'additional_files':{p:actual[p] for p in paths if p not in prior['files']},'repositories':repos,'pointers':cur,
        'previous_absent':prior['previous_absent'],'installed':{'store':str(store),'native':str(store/'generations'/cfg['native_generation_id']),
            'hroot':str(store/'h-f2-generations'/cfg['generation_id']),'config':cfg},'fixture':str(fixture)})
    for name in ('INVENTORY.json','PRIVATE-PROBE.json','DOC-REFERENCES.json','DATA-v2.json','PRESERVATION.json','SUMMARY.json'):
        shutil.copy2(ANALYSIS/name,E/('INPUT-'+name))
    print('frozen',len(paths),'CURRENT',len(cur),'prior drift',list(drift)[:8],flush=True)
def transform(raw,module):
    rel=next(p for p in TARGETS if Path(p).stem==module);rows=BY_PATH[rel]
    tree=ast.parse(raw);lines=raw.splitlines(keepends=True);removed=set()
    for row in rows:
        matches=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module==row['provider'] and any((a.asname or a.name)==row['binding'] for a in n.names)]
        assert len(matches)==1;node=matches[0];assert len(node.names)>1
        assert not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id==row['binding'] for n in ast.walk(tree))
        alias=next(a for a in node.names if (a.asname or a.name)==row['binding'])
        if node.lineno==node.end_lineno:
            line=lines[node.lineno-1];token=alias.name.encode()
            if b', '+token in line:line=line.replace(b', '+token,b'',1)
            elif token+b',' in line:line=line.replace(token+b',',b'',1)
            else:raise AssertionError('ambiguous inline import edit')
            lines[node.lineno-1]=line
        else:
            assert lines[alias.lineno-1].strip()==(alias.name+',').encode();removed.add(alias.lineno)
        node.names.remove(alias)
    after=b''.join(v for i,v in enumerate(lines,1) if i not in removed)
    assert ast.dump(tree,include_attributes=False)==ast.dump(ast.parse(after),include_attributes=False)
    return after
def patch(private,label,before,after):
    out=[]
    for rel in sorted(TARGETS):
        d=private/'patch-input'/label/Path(rel).stem;d.mkdir(parents=True);a=d/'before.py';b=d/'after.py';a.write_bytes(before[rel]);b.write_bytes(after[rel])
        p=subprocess.run(['git','diff','--no-index','--no-ext-diff','--no-color','--diff-algorithm=myers','--',str(a),str(b)],capture_output=True,text=True);assert p.returncode==1
        for line in p.stdout.splitlines(keepends=True):
            if line.startswith('diff --git '):line='diff --git a/'+rel+' b/'+rel+'\n'
            elif line.startswith('--- '):line='--- a/'+rel+'\n'
            elif line.startswith('+++ '):line='+++ b/'+rel+'\n'
            out.append(line)
    raw=''.join(out).encode();(private/(label+'.patch')).write_bytes(raw);(E/(label+'.patch.gz')).write_bytes(gzip.compress(raw,mtime=0))
    return {'raw_sha256':digest(raw),'sha256':state.sha(E/(label+'.patch.gz'))}
def prepare():
    b=baseline();head=b['repositories'][str(ROOT)]['head'];private=Path(tempfile.mkdtemp(prefix='photo-five-import-qualification-'))
    original={p:(ROOT/p).read_bytes() for p in TARGETS};heads={p:state.git(ROOT,'show',head+':'+p) for p in TARGETS}
    assert all(state.stamp(ROOT/p)==b['files'][str(ROOT/p)] for p in TARGETS)
    working={p:transform(raw,Path(p).stem) for p,raw in original.items()};index={p:transform(raw,Path(p).stem) for p,raw in heads.items()}
    payloads={p:small_cleanup.dirty_payload(heads[p],original[p]) for p in TARGETS}
    assert all(small_cleanup.dirty_payload(index[p],working[p])==payloads[p] for p in TARGETS)
    patches={label:patch(private,label,a,c) for label,a,c in [('WORKING',original,working),('INDEX',heads,index)]};projects={}
    for label in ('control','combined'):
        project=private/label;skill=four_patch.copy_code(project);projects[label]=str(project)
        if label=='combined':
            for p,raw in working.items():(project/p).write_bytes(raw)
        subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/'assets'),str(skill/'assets')],check=True)
        shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
        (project/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
        (skill/'references').mkdir();shutil.copy2(SKILL/'references/image-runtime.md',skill/'references/image-runtime.md')
        lock=state.read(SKILL/'embedding-runtime.lock.json');dest=skill/lock['package'];dest.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['/bin/cp','-c','-R','-p',str(SKILL/lock['package']),str(dest)],check=True)
        (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python',target_is_directory=True)
    project=Path(projects['combined']);subprocess.run(['git','-C',str(project),'apply','--reverse',str(private/'WORKING.patch')],check=True)
    assert all((project/p).read_bytes()==raw for p,raw in original.items())
    subprocess.run(['git','-C',str(project),'apply',str(private/'WORKING.patch')],check=True)
    new(E/'TARGETS.json',{'base_head':head,'imports':ROWS,'source_paths':sorted(TARGETS),'original':{p:b['files'][str(ROOT/p)] for p in TARGETS},
        'working':{p:digest(raw) for p,raw in working.items()},'index':{p:digest(raw) for p,raw in index.items()},'original_dirty_payload_sha256':payloads,
        'patches':patches,'source_added_lines':2,'source_deleted_lines':5,'remaining_AST_equal':True,'inverse_exact':True,'dirty_payload_preserved':True})
    new(E/'PRIVATE-PROJECTS.json',{'projects':projects,'private_parent':str(private),'source_files':76,'independent_assets_and_models':True,'scratch_is_not_unique_recovery_material':True})
    print('prepared exact 5 imports in 3 paths; partial HEAD and working patches',flush=True)
def worker(project,removed,modules,policy,timeout=900,log=None):
    command=['/usr/bin/sandbox-exec','-p',policy,str(SKILL/'.runtime/embedding-python/bin/python'),'-I','-B',str(E/'worker.py'),str(project),'1' if removed else '0',*modules]
    env=checks.environment()
    with tempfile.TemporaryDirectory(prefix='photo-five-import-tests-') as store:
        env['PHOTO_RUNTIME_STORE']=store
        p=subprocess.run(command,cwd=project,env=env,capture_output=True,text=True,timeout=timeout)
    try:r=json.loads(p.stdout.splitlines()[-1])
    except (ValueError,IndexError):r={'status':'HARNESS_UNAVAILABLE'}
    return {**r,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'network_denied':True,'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0}
def source(label,group):
    projects=state.read(E/'PRIVATE-PROJECTS.json')['projects'];project=ROOT if label=='applied' else Path(projects[label]);mods=checks.GROUPS['operating'] if group=='operating' else APPLIED_NATIVE if label=='applied' else NATIVE
    policy=checks.profile() if label=='applied' else four_patch.policy();r=worker(project,label!='control',mods,policy+'(deny file-read* (regex "/site-packages/torch(/|$)"))')
    r.update(modules=mods,scope='focused applied source checks; full private checks reuse exact qualified source hashes' if label=='applied' and group=='native' else 'private source regression')
    new(E/('SOURCE-'+label+'-'+group+'.json'),r);print(label,group,r.get('status'),r.get('tests'),flush=True)
    assert r['status']=='PASS' and r['exit_code']==0 and r['skipped']==0,r['stderr'][-4000:]
    if group=='operating':assert r['tests']==48
def delegate(command):
    old=four_state.E;four_state.E=E
    try:
        if command=='installed':four_checks.installed()
        elif command.startswith('history-'):four_checks.history(command.removeprefix('history-'))
        else:raise ValueError(command)
    finally:four_state.E=old
def index_check():
    b=baseline();r=b['repositories'][str(ROOT)];t=state.read(E/'TARGETS.json');assert state.sha(r['index_path'])==r['index_sha256']
    idx=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent'])/'qualified.index';shutil.copy2(r['index_path'],idx);env={**os.environ,'GIT_INDEX_FILE':str(idx)}
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:subprocess.run(['git','-C',str(ROOT),*args],input=raw,env=env,check=True)
    blobs={p:digest(subprocess.check_output(['git','-C',str(ROOT),'show',':'+p],env=env)) for p in TARGETS};assert blobs==t['index']
    stats=subprocess.check_output(['git','-C',str(ROOT),'diff','--cached','--numstat'],env=env).decode().splitlines()
    assert {v.split('\t')[2] for v in stats}==TARGETS and sum(int(v.split('\t')[0]) for v in stats)==2 and sum(int(v.split('\t')[1]) for v in stats)==5
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],env=env,check=True);assert state.sha(r['index_path'])==r['index_sha256']
    new(E/'INDEX-DRY-RUN.json',{'status':'PASS','source_blobs':blobs,'source_added_lines':2,'source_deleted_lines':5,'real_index_unchanged':True,'original_dirty_changes_staged':False})
def verify(output,full=False,committed=False):
    b=baseline();t=state.read(E/'TARGETS.json');applied=(E/'APPLICATION.json').exists();files=b['files'] if full else {p:s for p,s in b['files'].items() if p in b['pointers'] or Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore')}
    errors=[];extra={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for p,actual in zip(files,pool.map(state.stamp,files)):
            rel=str(Path(p).relative_to(ROOT)) if Path(p).is_relative_to(ROOT) else None
            good=actual==files[p]
            if applied and rel in TARGETS:good=actual.get('sha256')==t['working'][rel] and all(actual.get(k)==files[p].get(k) for k in ('mode','links'))
            if not good:errors.append(p)
    for wt,row in b['repositories'].items():
        current={p:s for p,s in state.status(wt).items() if wt!=str(ROOT) or not owned(p)};expected=dict(row['status'])
        if wt==str(ROOT) and applied and not committed:
            for rel in TARGETS:
                if rel not in expected:expected[rel]=' M'
        assert all(current.get(p)==s for p,s in expected.items()),wt+': original status changed'
        rest={p:s for p,s in current.items() if p not in expected};assert all(s=='??' for s in rest.values());extra[wt]=rest
        assert not state.git(wt,'diff','--cached','--raw','-z')
        if not committed or wt!=str(ROOT):
            assert state.git(wt,'rev-parse','HEAD').decode().strip()==row['head'];assert state.sha(row['index_path'])==row['index_sha256']
    assert pointers()==b['pointers'];assert not any(Path(p).exists() or Path(p).is_symlink() for p in b['previous_absent'])
    if applied:
        for rel in TARGETS:assert small_cleanup.dirty_payload(transform(state.git(ROOT,'show',t['base_head']+':'+rel),Path(rel).stem),(ROOT/rel).read_bytes())==t['original_dirty_payload_sha256'][rel]
    new(output,{'status':'FAIL' if errors else 'PASS','protected_paths':len(files),'full':full,'failures':errors,'CURRENT_count':len(b['pointers']),
        'original_dirty_payload_preserved':True,'original_status_preserved':True,'concurrent_additional_untracked':extra,'Gemini_calls':0,'CURRENT_writes':0})
    print('preservation',len(files),'PASS' if not errors else errors[:5],flush=True);assert not errors

GATES=['REFERENCE-CHECK.json','CLI-CHECK.json','SOURCE-control-operating.json','SOURCE-combined-operating.json','SOURCE-control-native.json','SOURCE-combined-native.json','HEAD-COMPARISON.json',
    'MANAGED-control.json','MANAGED-combined.json','MANAGED-control-CLOSURE.json','MANAGED-combined-CLOSURE.json','INSTALLED.json','HISTORY-frozen.json','HISTORY-archive.json','HISTORY-negative.json','HISTORY-native-view.json','INDEX-DRY-RUN.json','BEFORE-APPLICATION-FULL.json','PRE-APPLY-FINAL-FULL.json']
POST=['SOURCE-applied-operating.json','SOURCE-applied-native.json','MANAGED-applied.json','MANAGED-applied-CLOSURE.json','HISTORY-native-view-applied.json','AFTER-PRESERVATION.json']
def apply():
    assert not (E/'APPLICATION.json').exists();t=state.read(E/'TARGETS.json')
    assert all(state.read(E/n)['status']=='PASS' for n in GATES)
    assert all(state.stamp(ROOT/p)==t['original'][p] for p in TARGETS)
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==t['base_head'] and not state.git(ROOT,'diff','--cached','--name-only')
    raw=gzip.decompress((E/'WORKING.patch.gz').read_bytes());assert digest(raw)==t['patches']['WORKING']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--check','-'],input=raw,check=True)
    new(E/'APPLY-INTENT.json',{'gates':{n:state.sha(E/n) for n in GATES},'source_candidates':t['working']})
    subprocess.run(['git','-C',str(ROOT),'apply','-'],input=raw,check=True)
    assert all(state.sha(ROOT/p)==h for p,h in t['working'].items())
    new(E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','source_added_lines':2,'source_deleted_lines':5,'Gemini_calls':0,'CURRENT_writes':0,'publishes':0})
    print('applied exactly 5 import bindings',flush=True)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command');p.add_argument('--output',type=Path);p.add_argument('--full',action='store_true');p.add_argument('--committed',action='store_true');a=p.parse_args()
    if a.command=='freeze':freeze()
    elif a.command=='prepare':prepare()
    elif a.command.startswith('source-'):_,label,group=a.command.split('-');source(label,group)
    elif a.command=='index-check':index_check()
    elif a.command=='verify':verify(a.output,a.full,a.committed)
    elif a.command=='apply':apply()
    else:delegate(a.command)
