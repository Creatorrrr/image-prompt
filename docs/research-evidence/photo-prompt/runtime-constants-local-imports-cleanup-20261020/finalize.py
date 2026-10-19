"""Commit only the qualified eight-path patch and new evidence."""
import gzip,json,subprocess,sys
from pathlib import Path
import run
from history_state import new
E=run.E;ROOT=run.ROOT;state=run.state

def qualified():
    for n in [*run.GATES,*run.POST]:assert state.read(E/n)['status']=='PASS',n
    for k in ('algorithm_without_code','algorithm_binding_signature','active_contract_checks'):
        assert len({json.dumps(state.read(E/('SMOKE-'+label+'.json'))[k],sort_keys=True) for label in ('control','combined','applied')})==1,k
    assert all(state.read(E/('MANAGED-'+label+'.json'))['exact_top8_and_full_order_digests_preserved'] for label in ('control','combined','applied'))
    assert state.read(E/'HISTORY-archive.json')['latest_gate']=='HOLD'
    targets=state.read(E/'TARGETS.json')
    for label in ('control','combined','applied'):
        loaded=state.read(E/('SMOKE-'+label+'.json'))['loaded_modules']
        expected={p:r['sha256'] for p,r in targets['original'].items()} if label=='control' else targets['working']
        assert all(loaded[Path(p).stem]['sha256']==h for p,h in expected.items())
    return targets,run.baseline()

def payloads(t):
    return {p:run.small_cleanup.dirty_payload(run.transform(state.git(ROOT,'show',t['base_head']+':'+p),Path(p).stem),(ROOT/p).read_bytes()) for p in run.TARGETS}

def summary():
    t,b=qualified();assert payloads(t)==t['original_dirty_payload_sha256']
    new(E/'AFTER-DELTA.json.gz',{'source_replacements':{str(ROOT/p):{'before':b['files'][str(ROOT/p)],'after':state.stamp(ROOT/p)} for p in run.TARGETS},
        'unchanged_other_protected_paths':len(b['files'])-len(run.TARGETS),'CURRENT_count':len(b['pointers'])})
    new(E/'RESULTS.json',{'status':'PASS','state':'QUALIFIED_AND_APPLIED_READY_FOR_SCOPED_LOCAL_COMMIT',
        'source_paths':sorted(run.TARGETS),'constants_removed':14,'constant_lines':178,'local_import_bindings_removed':6,
        'source_added_lines':1,'source_deleted_lines':184,'net_removed_lines':183,'remaining_AST_equal':True,
        'source_test_counts':{g:state.read(E/('SOURCE-'+g+'.json'))['tests'] for g in ('operating','related','extra-complete')},
        'HEAD_differential':{'tests_each':43,'passes_each':41,'same_preexisting_failures_each':2,'new_failures':0},
        'native_branch_checks':state.read(E/'NATIVE-BRANCH-COMPARISON.json'),
        'managed_commands_per_arm':5,'managed_arms':['control','combined','applied'],'whole_pool':state.read(E/'INSTALLED.json')['whole_pool'],
        'archive_orders':450,'archive_tests':17,'archive_quality':'HOLD preserved','protected_paths':len(b['files']),'CURRENT_count':len(b['pointers']),
        'original_dirty_paths':{r:len(row['status']) for r,row in b['repositories'].items()},'original_dirty_payload_preserved':True,
        'deferred_requested_targets':[],'unrequested_policy_data_and_module_imports_unchanged':True,
        'gate_sha256':{n:state.sha(E/n) for n in [*run.GATES,*run.POST]},'Gemini_calls':0,'new_embedding_calls':0,'actual_image_calls':0,'CURRENT_writes':0,'pushes':0})
    new(E/'COMMIT-PLAN.json',{'message':run.MESSAGE,'base_head':t['base_head'],'source_paths':sorted(run.TARGETS),
        'index_patch':'INDEX.patch.gz','source_blobs':t['index'],'whole_dirty_files_staged':False,'evidence_prefix':str(E.relative_to(ROOT))+'/',
        'existing_analysis_excluded':str(run.ANALYSIS.relative_to(ROOT))+'/','push':False})
    with (E/'REPORT.md').open('x') as f:f.write((E/'REPORT-TEMPLATE.md').read_text().replace('상태: 검증 완료 후 확정한다.','상태: 구현·검증 완료, 이번 변경만 로컬 커밋 대상으로 확정했다.'))
    print('qualified report and scoped commit plan ready',flush=True)

def check_index(t,allowed):
    actual=set(state.git(ROOT,'diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert actual==allowed,actual^allowed
    assert {p:run.digest(state.git(ROOT,'show',':'+p)) for p in run.TARGETS}==t['index']
    rows=state.git(ROOT,'diff','--cached','--numstat','--',*sorted(run.TARGETS)).decode().splitlines()
    assert {r.split('\t')[2] for r in rows}==run.TARGETS and sum(int(r.split('\t')[0]) for r in rows)==1 and sum(int(r.split('\t')[1]) for r in rows)==184
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],check=True)

def stage():
    t,b=qualified();row=b['repositories'][str(ROOT)]
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==t['base_head'];assert state.sha(row['index_path'])==row['index_sha256']
    assert not state.git(ROOT,'diff','--cached','--name-only');assert all(state.sha(ROOT/p)==h for p,h in t['working'].items())
    assert payloads(t)==t['original_dirty_payload_sha256']
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes());assert run.digest(raw)==t['patches']['INDEX']['raw_sha256']
    for args in [('apply','--cached','--check','-'),('apply','--cached','-')]:subprocess.run(['git','-C',str(ROOT),*args],input=raw,check=True)
    evidence=sorted(str(p.relative_to(ROOT)) for p in E.rglob('*') if p.is_file());subprocess.run(['git','-C',str(ROOT),'add','--',*evidence],check=True)
    allowed={*run.TARGETS,*evidence,str((E/'STAGED-CHECK.json').relative_to(ROOT))}
    check_index(t,allowed-{str((E/'STAGED-CHECK.json').relative_to(ROOT))})
    new(E/'STAGED-CHECK.json',{'status':'PASS','allowed_paths':sorted(allowed),'source_blobs':t['index'],'source_added_lines':1,'source_deleted_lines':184,
        'original_dirty_changes_staged':False,'original_dirty_payload_preserved':True,'base_head':t['base_head'],'message':run.MESSAGE,'Gemini_calls':0,'CURRENT_writes':0,'push':False})
    subprocess.run(['git','-C',str(ROOT),'add','--',str(E/'STAGED-CHECK.json')],check=True);check_index(t,allowed)
    print('staged exact allowed paths:',len(allowed),flush=True)

def commit():
    t,b=qualified();check_index(t,set(state.read(E/'STAGED-CHECK.json')['allowed_paths']))
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==t['base_head'];assert all(state.sha(ROOT/p)==h for p,h in t['working'].items())
    assert payloads(t)==t['original_dirty_payload_sha256'];subprocess.run(['git','-C',str(ROOT),'commit','-m',run.MESSAGE],check=True)

def postcheck():
    t,b=qualified();head=state.git(ROOT,'rev-parse','HEAD').decode().strip()
    assert state.git(ROOT,'rev-parse','HEAD^').decode().strip()==t['base_head']
    assert set(state.git(ROOT,'diff-tree','--no-commit-id','--name-only','-r','HEAD','-z').decode().split('\0'))-{''}==set(state.read(E/'STAGED-CHECK.json')['allowed_paths'])
    assert {p:run.digest(state.git(ROOT,'show','HEAD:'+p)) for p in run.TARGETS}==t['index']
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent']);run.verify(private/'POST-COMMIT-PRESERVATION.json',full=True,committed=True)
    new(private/'POST-COMMIT.json',{'status':'PASS','commit':head,'parent':t['base_head'],'source_paths':sorted(run.TARGETS),
        'constants_removed':14,'local_import_bindings_removed':6,'source_added_lines':1,'source_deleted_lines':184,
        'protected_paths':len(b['files']),'CURRENT_count':len(b['pointers']),'staging_empty':True,'original_dirty_payload_preserved':True,
        'Gemini_calls':0,'CURRENT_writes':0,'pushes':0})
    print('POST-COMMIT PASS',head,flush=True)

if __name__=='__main__':{'summary':summary,'stage':stage,'commit':commit,'postcheck':postcheck}[sys.argv[1]]()
