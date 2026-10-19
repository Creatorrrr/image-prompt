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
import import_seventeen_cleanup as scope
from history_state import new,pointers
import state

os.environ['GIT_OPTIONAL_LOCKS']='0'; os.environ['GIT_NO_LAZY_FETCH']='1'
E=scope.E
POST_GATES=['SMOKE-applied.json','MANAGED-applied.json','HISTORY-native-view-applied.json','AFTER-PRESERVATION.json']
MESSAGE='refactor(photo): remove unused imports and Gemini helpers'


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
    results={'status':'PASS','state':'QUALIFIED_AND_APPLIED_READY_FOR_SCOPED_LOCAL_COMMIT',
        'source_files':len(scope.TARGETS),'import_bindings_removed':17,'functions_removed':4,
        'source_added_lines':1,'source_deleted_lines':55,'net_removed_lines':54,
        'operating_tests':48,'native_tests':70,'skipped':0,
        'HEAD_differential':{'tests_each':35,'passed_each':33,'preexisting_failures_each':2,'new_failures':0},
        'managed_cli_arms':['control','combined','applied'],'commands_per_arm':5,
        'whole_pool':state.read(E/'INSTALLED.json')['whole_pool'],
        'archive_orders':450,'archive_tests':17,'archive_quality':'HOLD preserved',
        'gate_sha256':{n:state.sha(E/n) for n in [*scope.GATES,*POST_GATES]},
        'protected_paths':len(before['files']),'CURRENT_count':len(before['pointers']),
        'original_dirty_paths':{r:len(v['status']) for r,v in before['repositories'].items()},
        'original_dirty_payload_preserved':True,'partial_index_dry_run':'PASS',
        'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0,'runtime_publish_calls':0,'pushes':0}
    new(E/'RESULTS.json',results)
    new(E/'COMMIT-PLAN.json',{'message':MESSAGE,'base_head':targets['base_head'],
        'source_paths':sorted(scope.TARGETS),'helper':scope.HELPER,'evidence_prefix':str(E.relative_to(ROOT))+'/',
        'existing_analysis_files_excluded':str(scope.ANALYSIS.relative_to(ROOT))+'/',
        'stage_existing_generator_file_whole':False,'index_patch':'INDEX.patch.gz',
        'expected_index_blobs':targets['index'],'push':False,'CURRENT_writes':0})
    report='''# import 17개와 구 Gemini helper 4개 정리

상태: 승인한 범위의 구현·검증 완료. 검증된 소스와 이번 helper·증거만 로컬 커밋 대상으로 확정했다. CURRENT 전환과 push는 수행하지 않는다.

## 변경

소스 10파일에서 표준 라이브러리 import 바인딩 17개와 미사용 함수 4개를 제거했다. Git 기준 1행 추가·55행 삭제, 순감소 54행이다. 함수·모듈의 실제 계약, 공통 후보풀 검색과 H 단독+F2 정책은 유지한다.

| 파일 | 제거한 항목 |
|---|---|
| `scripts/photo_contextual_appeal.py` | `math` |
| `scripts/photo_global_index.py` | `Path` |
| `scripts/photo_candidate_semantics.py` | `re` |
| `scripts/qualify_local_embeddings.py` | `collections`, `time` |
| `scripts/install_photo_h_f2_runtime.py` | `sys` |
| `scripts/audit_moe_render_review.py` | `sys` |
| `scripts/photo_search_reader.py` | `array` |
| `scripts/validate_precore_feature_selection.py` | `hashlib`, `re` |
| `precore/photo_feature_selection.py` | `json` |
| `scripts/prompt_generator.py` | `argparse`, `secrets`, `time`, `Counter`, `Callable`, `os`; Gemini helper 4개 |

경로는 `skills/photo-prompt-image-generator/` 기준이다. 구 helper는 `get_gemini_api_key`, `cached_gemini_client`, `extract_embedding_values`, `round_embedding_vector`이며 decorator를 포함해 38행이다. `os`는 제거한 키 조회 helper만 사용했다. typing 목록에서는 `Callable`만 뺐다.

원본과 제거본의 AST는 승인한 import·함수만 제외하면 같고, private patch를 역적용하면 원본 bytes가 정확히 복원됐다. 이전 분석에서 현재 참조를 조사한 결과와 대상 원본·제거본 SHA가 일치함을 이번에도 확인했다. 이전 분석의 5조건×35검사는 재사용 근거이며 이번 전체 검사를 대신하지 않는다. 실제 사용하는 `photo_contextual_appeal.compile_context` 재export, local embedding provider·batch/cache와 과거 Gemini receipt/응답/공간·transport 코드는 보존했다.

## 검증 결과

현재 작업본을 복사한 독립 private 소스에서 운영 회귀 48개와 native 회귀 70개, 총 118개가 skip 없이 통과했다. 모델·assets는 APFS 독립 clone이고 원본과 hardlink하지 않았다. 고정 Python과 `-I -B`를 사용했으며 원본 scripts/precore 읽기 fallback·원본과 cache 쓰기·네트워크·torch 읽기를 OS sandbox로 차단했다. 실제 로딩 경로·SHA, 제거 대상 부재, 코드 76개와 일치 구현 허용·불일치 구현 거부를 확인했다.

원본·private 제거본·원본 적용본에서 실제 `photo_workflow.py`의 `view → retrieve → view → compose-audit → deliver`를 각각 실행해 총 15명령이 통과했다. composition·lighting 목표 각각 BM25F 1회·로컬 cosine 1회를 유지했고 top 8·전체 순서/점수 digest와 전달 완료 상태가 같았다. 기존 로컬 query vector를 재사용해 새 임베딩 추론은 없었다. 네 개의 import 영향 CLI도 원본/제거본의 `--help` 출력이 동일했다.

원래 설치된 kernel과 발급 영수증은 전체 CID 18,180개·RID 18,182개 검색의 점수·전체 순서가 같았고 native audit도 통과했다. frozen audit, 별도 파생 native public view, archive 검색 순서 450개와 평가 검사 17개, 누락·변조 거부 CLI 4개도 요구 결과를 유지했다. archive의 기존 품질 HOLD는 그대로 재현했으며 이를 품질 통과로 해석하지 않는다. 파생 native view를 새 과거 원본 실행으로 세지 않는다.

커밋될 HEAD 기반 소스와 동일 시점의 tracked 테스트를 별도 검사했다. 35개 중 정리 전후 각각 33개 통과·동일한 기존 실패 2개이며 새 실패/오류는 없다. 현재 작업본에서 통과하는 contextual 관련 미커밋 수정은 이번 커밋에 포함하지 않는다. 최초 비교 harness가 JSON list와 tuple의 표현 차이를 실패로 잡은 문제를 고쳤으며, raw 실패 ID·traceback이 양쪽에서 같다는 근거를 `HEAD-HARNESS-REVIEW.json`에 보존했다. 최종 차등 검사는 별도 HEAD 복사본으로 다시 실행했다.

## 기존 작업·CURRENT·커밋 경계

보호 경로 139,411개와 CURRENT 168개를 원본 적용 전후 대조했다. 허용한 소스 10파일 외의 bytes·mode·inode·links는 동일하다. 루트의 기존 변경·미추적 40,586경로와 다른 worktree 6,161경로를 보존했다. 직전 분석의 미추적 25파일도 원래 작업으로 보호했으며 이번 stage에서 제외한다. 이전 제거 경로 293개도 계속 부재다.

generator는 기존 미커밋 변경이 있어 파일 전체를 stage하지 않는다. 기존 HEAD에서 승인한 정리만 적용한 index patch와 현재 작업본용 patch를 따로 만들었다. HEAD/작업본 양쪽에서 변환 전후 기존 dirty diff payload SHA가 같고, private index에서 정확한 staged blob과 1행 추가·55행 삭제를 확인했다. 실제 stage도 이 HEAD patch와 이번 helper·증거만 허용한다.

검증한 소스 해시와 staged blob을 확인한 뒤 로컬 커밋한다. 기존 후보 데이터, installed/frozen source·영수증·모델·archive와 두 작업공간의 기존 변경을 함께 커밋하지 않는다. source 구현 해시가 바뀌었다는 이유로 CURRENT를 재발행하거나 코드 불일치 거부를 약화하지 않았다. 기존 native CURRENT의 74파일과 현재 작업 소스 76파일 차이는 그대로다.

남은 구 검색·그래프 함수, 관련 상수, 수동 `validate_visual_profile_source`, 프로젝트 모듈 import 보류분, bytecode 21개, root shard 5세대와 원래 store가 없는 과거 실행 41건은 이번 범위가 아니다. Gemini·이미지 생성·새 임베딩 호출과 전수 의미 검토, 운영 generation 발행, CURRENT 쓰기와 push는 없다.

`BASELINE-DELTA.json.gz`는 직전 분석의 pinned protection chain과 추가 보호 25경로로 시작 상태를 재구성한다. `AFTER-DELTA.json.gz`에는 이번 허용 소스 10개만 정확한 before/after stamp를 기록했다. 완료 evidence는 덮어쓰지 않으며 private 폴더는 실행 scratch로만 사용한다. 상세 결과는 `RESULTS.json`, `TARGETS.json`, `SOURCE-*.json`, `HEAD-COMPARISON.json`, `MANAGED-*.json`, `HISTORY-*.json`, `AFTER-PRESERVATION.json`, `STAGED-CHECK.json`에 기록한다.
'''
    with (E/'REPORT.md').open('x') as stream: stream.write(report)
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
        'source_index_blobs':targets['index'],'source_added_lines':1,'source_deleted_lines':55,
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
    assert sum(int(r.split('\t')[0]) for r in stats)==1 and sum(int(r.split('\t')[1]) for r in stats)==55
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
        'source_added_lines':1,'source_deleted_lines':55,'pushes':0,'Gemini_calls':0,'CURRENT_writes':0}
    new(private/'POST-COMMIT.json',result)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    {'summary':summary,'stage':stage,'commit':commit,'postcheck':postcheck}[sys.argv[1]]()
