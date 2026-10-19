"""Commit only the qualified generator binding deletion and its new evidence."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
from pathlib import Path
import subprocess
import sys

import run as wrapper
scope=wrapper.scope
scope.TARGETS=wrapper.TARGETS
from history_state import new,pointers
import state

E=scope.E;ROOT=scope.ROOT;SOURCE=scope.SOURCE
POST=['SMOKE-applied.json','MANAGED-applied.json','HISTORY-native-view-applied.json','AFTER-PRESERVATION.json']


def qualified():
    for name in [*scope.GATES,*POST]:assert state.read(E/name)['status']=='PASS',name
    for key in ('algorithm_without_code','algorithm_binding_signature','active_graph_checks'):
        assert state.read(E/'SMOKE-control.json')[key]==state.read(E/'SMOKE-combined.json')[key]==state.read(E/'SMOKE-applied.json')[key]
    for label in ('control','combined','applied'):
        assert state.read(E/('MANAGED-'+label+'.json'))['exact_top8_and_full_order_digests_preserved']
    assert state.read(E/'HISTORY-archive.json')['latest_gate']=='HOLD'
    return state.read(E/'TARGETS.json'),scope.baseline()


def payload(targets):
    from small_cleanup import dirty_payload
    original=scope.transform(state.git(ROOT,'show',targets['base_head']+':'+SOURCE))
    return dirty_payload(original,(ROOT/SOURCE).read_bytes())


def summary():
    targets,before=qualified()
    new(E/'AFTER-DELTA.json.gz',{'source_replacements':{str(ROOT/SOURCE):{
        'before':before['files'][str(ROOT/SOURCE)],'after':state.stamp(ROOT/SOURCE)}},
        'unchanged_other_protected_paths':len(before['files'])-1,'CURRENT_count':len(before['pointers'])})
    new(E/'RESULTS.json',{'status':'PASS','state':'QUALIFIED_AND_APPLIED_READY_FOR_SCOPED_LOCAL_COMMIT',
        'source_paths':[SOURCE],'import_bindings_removed':3,'constants_removed':1,
        'source_added_lines':0,'source_deleted_lines':4,'remaining_AST_equal':True,
        'working_source_tests':{'operating':48,'related_including_retry':43,'skipped':0,
            'note':'Execution counts; BM25F modules overlap between these two groups.'},
        'HEAD_differential':{'tests_each':43,'passed_each':41,'preexisting_failures_each':2,'new_failures':0},
        'active_graph_checks':state.read(E/'SMOKE-applied.json')['active_graph_checks'],
        'managed_cli_arms':['control','combined','applied'],'commands_per_arm':5,
        'whole_pool':state.read(E/'INSTALLED.json')['whole_pool'],'archive_orders':450,
        'archive_tests':17,'archive_quality':'HOLD preserved',
        'protected_paths':len(before['files']),'CURRENT_count':len(before['pointers']),
        'original_dirty_paths':{r:len(v['status']) for r,v in before['repositories'].items()},
        'original_dirty_payload_preserved':payload(targets)==targets['original_dirty_payload_sha256'][SOURCE],
        'partial_index_dry_run':'PASS','gate_sha256':{n:state.sha(E/n) for n in [*scope.GATES,*POST]},
        'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0,'runtime_publish_calls':0,'pushes':0})
    new(E/'COMMIT-PLAN.json',{'message':scope.MESSAGE,'base_head':targets['base_head'],
        'source_paths':[SOURCE],'index_patch':'INDEX.patch.gz','expected_source_blob':targets['index'][SOURCE],
        'stage_existing_generator_file_whole':False,'evidence_prefix':str(E.relative_to(ROOT))+'/',
        'existing_analysis_excluded':str(scope.ANALYSIS.relative_to(ROOT))+'/',
        'Gemini_calls':0,'CURRENT_writes':0,'push':False})
    with (E/'REPORT.md').open('x') as stream:
        stream.write((E/'REPORT-TEMPLATE.md').read_text().replace('상태: 검증 완료 후 확정한다.',
            '상태: 구현·검증 완료, 이번 변경만 로컬 커밋 대상으로 확정했다.'))
    print('qualified summary and scoped commit plan written',flush=True)


def check_index(targets,allowed):
    actual=set(state.git(ROOT,'diff','--cached','--name-only','-z').decode().split('\0'))-{''}
    assert actual==allowed,actual^allowed
    assert scope.digest(state.git(ROOT,'show',':'+SOURCE))==targets['index'][SOURCE]
    assert state.git(ROOT,'diff','--cached','--numstat','--',SOURCE).decode().splitlines()==['0\t4\t'+SOURCE]
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],check=True)


def stage():
    targets,before=qualified();row=before['repositories'][str(ROOT)]
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head']
    assert state.sha(row['index_path'])==row['index_sha256'] and not state.git(ROOT,'diff','--cached','--name-only')
    assert state.sha(ROOT/SOURCE)==targets['working'][SOURCE]
    assert payload(targets)==targets['original_dirty_payload_sha256'][SOURCE]
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    assert scope.digest(raw)==targets['patches']['INDEX']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','--check','-'],input=raw,check=True)
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','-'],input=raw,check=True)
    evidence=sorted(str(p.relative_to(ROOT)) for p in E.rglob('*') if p.is_file())
    subprocess.run(['git','-C',str(ROOT),'add','--',*evidence],check=True)
    allowed={SOURCE,*evidence,str((E/'STAGED-CHECK.json').relative_to(ROOT))}
    check_index(targets,allowed-{str((E/'STAGED-CHECK.json').relative_to(ROOT))})
    new(E/'STAGED-CHECK.json',{'status':'PASS','allowed_paths':sorted(allowed),
        'source_index_blob':targets['index'][SOURCE],'source_added_lines':0,'source_deleted_lines':4,
        'original_dirty_changes_staged':False,'original_dirty_payload_preserved':True,
        'base_head':targets['base_head'],'message':scope.MESSAGE,'Gemini_calls':0,'CURRENT_writes':0,'push':False})
    subprocess.run(['git','-C',str(ROOT),'add','--',str(E/'STAGED-CHECK.json')],check=True)
    check_index(targets,allowed)
    print('staged exact allowed paths:',len(allowed),flush=True)


def commit():
    targets,before=qualified();check_index(targets,set(state.read(E/'STAGED-CHECK.json')['allowed_paths']))
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head']
    assert state.sha(ROOT/SOURCE)==targets['working'][SOURCE]
    assert payload(targets)==targets['original_dirty_payload_sha256'][SOURCE]
    subprocess.run(['git','-C',str(ROOT),'commit','-m',scope.MESSAGE],check=True)


def postcheck():
    targets,before=qualified();head=state.git(ROOT,'rev-parse','HEAD').decode().strip()
    assert state.git(ROOT,'rev-parse','HEAD^').decode().strip()==targets['base_head']
    expected=set(state.read(E/'STAGED-CHECK.json')['allowed_paths'])
    actual=set(state.git(ROOT,'diff-tree','--no-commit-id','--name-only','-r','HEAD','-z').decode().split('\0'))-{''}
    assert actual==expected
    assert scope.digest(state.git(ROOT,'show','HEAD:'+SOURCE))==targets['index'][SOURCE]
    applied=state.read(E/'AFTER-DELTA.json.gz')['source_replacements'];failures=[]
    print('post-commit protected-path comparison:',len(before['files']),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,stamp in zip(before['files'],pool.map(state.stamp,before['files'])):
            expected_stamp=applied[path]['after'] if path in applied else before['files'][path]
            if stamp!=expected_stamp:failures.append(path)
    for work,row in before['repositories'].items():
        current=state.status(work)
        assert all(current.get(p)==v for p,v in row['status'].items()),work+': original Git status changed'
        extra={p:v for p,v in current.items() if p not in row['status']}
        assert all(work==str(ROOT) and p.startswith(wrapper.CONCURRENT_PREFIX) and v=='??' for p,v in extra.items()),extra
        assert not state.git(work,'diff','--cached','--raw','-z')
        if work!=str(ROOT):
            assert state.git(work,'rev-parse','HEAD').decode().strip()==row['head']
            assert state.sha(row['index_path'])==row['index_sha256']
    assert payload(targets)==targets['original_dirty_payload_sha256'][SOURCE]
    assert pointers()==before['pointers']
    assert not any(Path(p).exists() or Path(p).is_symlink() for p in before['previous_absent'])
    assert not failures,failures[:10]
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent'])
    result={'status':'PASS','commit':head,'parent':targets['base_head'],'committed_paths':len(actual),
        'protected_paths_checked':len(before['files']),'CURRENT_count':len(before['pointers']),
        'staging_empty':True,'original_dirty_payload_preserved':True,'both_original_Git_status_entries_equal':True,'concurrent_additions_preserved_and_excluded':True,
        'source_added_lines':0,'source_deleted_lines':4,'Gemini_calls':0,'CURRENT_writes':0,'pushes':0}
    new(private/'POST-COMMIT.json',result);print(json.dumps(result),flush=True)


if __name__=='__main__':
    {'summary':summary,'stage':stage,'commit':commit,'postcheck':postcheck}[sys.argv[1]]()
