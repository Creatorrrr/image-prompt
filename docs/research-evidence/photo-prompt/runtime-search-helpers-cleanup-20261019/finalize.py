"""Close qualified evidence, stage the exact HEAD patch, and verify the local commit."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import search_helpers_cleanup as scope
from history_state import new,pointers
import state

os.environ['GIT_OPTIONAL_LOCKS']='0'; os.environ['GIT_NO_LAZY_FETCH']='1'
E=scope.E
POST_GATES=['SMOKE-applied.json','MANAGED-applied.json','HISTORY-native-view-applied.json','AFTER-PRESERVATION.json']
MESSAGE='refactor(photo): remove unused search helpers and import bindings'


def qualified():
    for name in [*scope.GATES,*POST_GATES]:
        assert state.read(E/name)['status']=='PASS',name
    targets=state.read(E/'TARGETS.json')
    for label in ('control','combined','applied'):
        assert state.read(E/('MANAGED-'+label+'.json'))['exact_top8_and_full_order_digests_preserved']
    assert state.read(E/'HISTORY-archive.json')['latest_gate']=='HOLD'
    return targets,scope.baseline()


def summary():
    targets,before=qualified()
    new(E/'AFTER-DELTA.json.gz',{'source_replacements':{str(ROOT/p):{'before':before['files'][str(ROOT/p)],
        'after':state.stamp(ROOT/p)} for p in sorted(scope.TARGETS)},
        'unchanged_other_protected_paths':len(before['files'])-len(scope.TARGETS),
        'CURRENT_count':len(before['pointers']),'original_dirty_payload_sha256':targets['original_dirty_payload_sha256']})
    new(E/'RESULTS.json',{'status':'PASS','state':'QUALIFIED_AND_APPLIED_READY_FOR_SCOPED_LOCAL_COMMIT',
        'source_files':6,'import_bindings_removed':6,'functions_removed':4,'function_lines_removed':131,
        'source_added_lines':4,'source_deleted_lines':136,'net_removed_lines':132,
        'operating_tests':48,'native_tests':70,'closed_retry_tests':8,'total_current_working_tests':126,'skipped':0,
        'HEAD_differential':{'tests_each':43,'passed_each':41,'preexisting_failures_each':2,'new_failures':0},
        'managed_cli_arms':['control','combined','applied'],'commands_per_arm':5,
        'whole_pool':state.read(E/'INSTALLED.json')['whole_pool'],
        'archive_orders':450,'archive_tests':17,'archive_quality':'HOLD preserved',
        'gate_sha256':{n:state.sha(E/n) for n in [*scope.GATES,*POST_GATES]},
        'protected_paths':len(before['files']),'CURRENT_count':len(before['pointers']),
        'original_dirty_paths':{r:len(v['status']) for r,v in before['repositories'].items()},
        'original_dirty_payload_preserved':True,'partial_index_dry_run':'PASS',
        'provider_imports_retained':True,'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0,
        'runtime_publish_calls':0,'pushes':0})
    new(E/'COMMIT-PLAN.json',{'message':MESSAGE,'base_head':targets['base_head'],
        'source_paths':sorted(scope.TARGETS),'helper':scope.HELPER,'evidence_prefix':str(E.relative_to(ROOT))+'/',
        'existing_analysis_files_excluded':str(scope.ANALYSIS.relative_to(ROOT))+'/',
        'stage_existing_generator_file_whole':False,'index_patch':'INDEX.patch.gz',
        'expected_index_blobs':targets['index'],'push':False,'CURRENT_writes':0})
    report=(E/'REPORT-TEMPLATE.md').read_text().replace(
        '상태: 승인 범위 구현·검증 완료 후 REPORT.md로 확정하는 템플릿. RESULTS.json과 적용 후 검증이 모두 PASS일 때만 최종 보고서와 stage 계획을 생성한다. push와 CURRENT 전환은 수행하지 않는다.',
        '상태: 승인 범위 구현·검증 완료. RESULTS.json과 적용 후 검증이 모두 PASS이며 이번 변경만 로컬 커밋 대상으로 확정했다. push와 CURRENT 전환은 수행하지 않는다.')
    report+='\n## 최종 결과\n\n현재 작업본 126개가 skip 없이 통과했다. 원본·private 제거본·원본 적용본의 CLI 15명령, installed/frozen·archive 검색 순서 450개·평가 검사 17개·부정 CLI 4개가 요구 결과를 유지했다. HEAD 비교는 각 41개 통과·동일한 기존 실패 2개와 새 실패 0개다. 원본 적용 후 보호 139,480경로와 CURRENT 168개 대조가 통과했고, generator의 기존 dirty diff payload도 보존했다. 이번 소스 diff는 정확히 4행 추가·136행 삭제다.\n'
    with (E/'REPORT.md').open('x') as stream:stream.write(report)
    print('qualified summary and commit plan written',flush=True)


def stage():
    targets,before=qualified(); row=before['repositories'][str(ROOT)]
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head']
    assert state.sha(row['index_path'])==row['index_sha256'] and not state.git(ROOT,'diff','--cached','--name-only')
    assert all(state.sha(ROOT/p)==sha for p,sha in targets['working'].items())
    assert all(small_payload(targets,p)==targets['original_dirty_payload_sha256'][p] for p in scope.TARGETS)
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    assert scope.digest(raw)==targets['patches']['INDEX']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','--check','-'],input=raw,check=True)
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','-'],input=raw,check=True)
    evidence=sorted(str(p.relative_to(ROOT)) for p in E.rglob('*') if p.is_file())
    subprocess.run(['git','-C',str(ROOT),'add','--',scope.HELPER,*evidence],check=True)
    allowed=scope.TARGETS|{scope.HELPER}|set(evidence)|{str((E/'STAGED-CHECK.json').relative_to(ROOT))}
    check_index(targets,allowed-{str((E/'STAGED-CHECK.json').relative_to(ROOT))})
    new(E/'STAGED-CHECK.json',{'status':'PASS','allowed_paths':sorted(allowed),
        'source_index_blobs':targets['index'],'source_added_lines':4,'source_deleted_lines':136,
        'original_dirty_changes_staged':False,'original_dirty_payload_preserved':True,
        'base_head':targets['base_head'],'message':MESSAGE,'Gemini_calls':0,'CURRENT_writes':0,'push':False})
    subprocess.run(['git','-C',str(ROOT),'add','--',str(E/'STAGED-CHECK.json')],check=True)
    check_index(targets,allowed)
    print('staged exact approved paths:',len(allowed),'; existing work excluded',flush=True)


def small_payload(targets,path):
    from small_cleanup import dirty_payload
    return dirty_payload(state.git(ROOT,'show',targets['base_head']+':'+path) if not (E/'APPLICATION.json').exists()
        else scope.transform(state.git(ROOT,'show',targets['base_head']+':'+path),Path(path).stem),(ROOT/path).read_bytes())


def check_index(targets,allowed):
    actual=set(state.git(ROOT,'diff','--cached','--name-only','-z').decode().split('\0'))-{''}
    assert actual==allowed,actual^allowed
    for path,sha in targets['index'].items():
        assert scope.digest(state.git(ROOT,'show',':'+path))==sha,path
    stats=state.git(ROOT,'diff','--cached','--numstat','--',*sorted(scope.TARGETS)).decode().splitlines()
    assert sum(int(r.split('\t')[0]) for r in stats)==4 and sum(int(r.split('\t')[1]) for r in stats)==136
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],check=True)


def commit():
    targets,before=qualified(); staged=state.read(E/'STAGED-CHECK.json')
    check_index(targets,set(staged['allowed_paths']))
    assert state.git(ROOT,'rev-parse','HEAD').decode().strip()==targets['base_head']
    assert all(state.sha(ROOT/p)==sha for p,sha in targets['working'].items())
    assert all(small_payload(targets,p)==targets['original_dirty_payload_sha256'][p] for p in scope.TARGETS)
    subprocess.run(['git','-C',str(ROOT),'commit','-m',MESSAGE],check=True)


def postcheck():
    targets,before=qualified(); head=state.git(ROOT,'rev-parse','HEAD').decode().strip()
    assert state.git(ROOT,'rev-parse','HEAD^').decode().strip()==targets['base_head']
    expected=set(state.read(E/'STAGED-CHECK.json')['allowed_paths'])
    actual=set(state.git(ROOT,'diff-tree','--no-commit-id','--name-only','-r','HEAD','-z').decode().split('\0'))-{''}
    assert actual==expected
    for path,sha in targets['index'].items(): assert scope.digest(state.git(ROOT,'show','HEAD:'+path))==sha
    failures=[]
    applied=state.read(E/'AFTER-DELTA.json.gz')['source_replacements']
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path,stamp in zip(before['files'],pool.map(state.stamp,before['files'])):
            expected_stamp=applied[path]['after'] if path in applied else before['files'][path]
            if stamp!=expected_stamp: failures.append(path)
    for work,row in before['repositories'].items():
        assert state.status(work)==row['status'],work+': original Git status changed'
        assert not state.git(work,'diff','--cached','--raw','-z')
        if work!=str(ROOT):
            assert state.git(work,'rev-parse','HEAD').decode().strip()==row['head']
            assert state.sha(row['index_path'])==row['index_sha256']
    assert all(small_payload(targets,p)==targets['original_dirty_payload_sha256'][p] for p in scope.TARGETS)
    assert pointers()==before['pointers']
    assert not any(Path(p).exists() or Path(p).is_symlink() for p in before['previous_absent'])
    assert not failures,failures[:10]
    private=Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent'])
    result={'status':'PASS','commit':head,'parent':targets['base_head'],'committed_paths':len(actual),
        'protected_paths_checked':len(before['files']),'CURRENT_count':len(before['pointers']),
        'staging_empty':True,'original_dirty_payload_preserved':True,'both_original_Git_statuses_equal':True,
        'source_added_lines':4,'source_deleted_lines':136,'pushes':0,'Gemini_calls':0,'CURRENT_writes':0}
    new(private/'POST-COMMIT.json',result)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    {'summary':summary,'stage':stage,'commit':commit,'postcheck':postcheck}[sys.argv[1]]()
