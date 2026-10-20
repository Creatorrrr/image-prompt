"""Finalize only this qualified cleanup and stage reviewed paths explicitly."""
import ast,gzip,json,os,subprocess,sys
from pathlib import Path
import run
from history_state import new

E=run.E;ROOT=run.ROOT
def finish():
    t=run.state.read(E/'TARGETS.json');b=run.baseline()
    assert all(run.state.read(E/n)['status']=='PASS' for n in [*run.GATES,*run.POST])
    assert all(run.state.sha(ROOT/p)==h for p,h in t['working'].items())
    assert not run.state.git(ROOT,'diff','--cached','--name-only')
    new(E/'AFTER-DELTA.json.gz',{'source_replacements':{str(ROOT/p):{'before':b['files'][str(ROOT/p)],'after':run.state.stamp(ROOT/p)} for p in sorted(run.TARGETS)},
        'unchanged_protected_paths':len(b['files'])-3,'CURRENT_count':len(b['pointers'])})
    counts={label:{g:run.state.read(E/('SOURCE-'+label+'-'+g+'.json'))['tests'] for g in ('operating','native')} for label in ('control','combined','applied')}
    assert counts['control']==counts['combined']
    identities=[run.state.read(E/('SOURCE-'+label+'-'+group+'.json'))['algorithm_without_code'] for label in counts for group in ('operating','native')]
    assert all(v==identities[0] for v in identities)
    results={'status':'PASS','state':'QUALIFIED_AND_APPLIED_READY_FOR_SCOPED_LOCAL_COMMIT','source_files':3,'import_bindings_removed':5,'source_added_lines':2,'source_deleted_lines':5,'net_removed_lines':3,
        'tests':counts,'HEAD_differential':{'tests_each':43,'passes_each':41,'same_preexisting_failures_each':2,'new_failures':0},
        'managed_commands_each':5,'managed_arms':['control','combined','applied'],'managed_lane_budget':run.state.read(E/'MANAGED-applied.json')['actual_lane_calls'],
        'positive_common_pool':{'CIDs':18180,'RIDs':18182},'new_query_inference_calls':0,
        'history':['original sealed native receipt/composed audit','archive full-order and aggregate/test replay','negative CLI','derived native public views'],
        'all_provider_definitions_and_other_bindings_retained':True,'archive_quality':'HOLD preserved',
        'gates_sha256':{n:run.state.sha(E/n) for n in [*run.GATES,*run.POST]},'protected_paths':len(b['files']),'CURRENT_count':len(b['pointers']),
        'original_dirty_paths':{k:len(v['status']) for k,v in b['repositories'].items()},'original_dirty_payload_preserved':True,
        'source_data_or_frozen_generations_modified':False,'deferred_requested_bindings':[],'deferred_unrequested_imports':26,'deferred_local_worker_imports':2,
        'Gemini_calls':0,'new_embedding_calls':0,'image_calls':0,'CURRENT_writes':0,'publishes':0,'pushes':0}
    new(E/'RESULTS.json',results)
    report=f'''# import 바인딩 5개·3파일 정리

승인된 import 바인딩 5개만 제거했다. 작업 소스와 커밋용 HEAD 패치를 별도로 검증했고 기존 미커밋 수정은 커밋에 넣지 않는다. 운영 선택과 CURRENT는 변경하지 않는다.

| 파일 | 제거 바인딩 |
|---|---|
| `scripts/photo_workflow_worker.py` | `WorkflowError` |
| `scripts/generate_images_via_api.py` | `PreflightError` |
| `scripts/audit_composed_prompt.py` | `AUTHORIAL_CORE_CONTRACT_VERSION`, `DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION`, `property_effects_allowed` |

경로는 `skills/photo-prompt-image-generator/` 기준이다. 공급 모듈의 실제 정의와 나머지 import는 유지했다. 3파일에서 2행 추가·5행 삭제, 순감소 3행이며 나머지 AST는 같다. 나머지 미확정 module import 26개와 해시가 설치본에 결합된 local worker import 2개는 범위 밖에 두었다. 승인한 5개 중 보류한 항목은 없다.

## 검증

- 현재 Python 188개에서 재참조를 확인했다. 보존 Python 10,147개의 분석 이후 SHA가 그대로였고, 신규 자료도 확인했다. 보고서 문자열·namespace 복사·입력이 제한된 CHARACTER_* 검사를 실제 named 소비자와 구분했다. 알 수 없는 외부 reflection의 부재까지 증명하지 않는다.
- source 원본·제거 복사본 각각 운영 계약 {counts['control']['operating']}개·native/API {counts['control']['native']}개를 통과했다. 실제 적용본은 전체 파일 SHA가 검증 복사본과 같음을 확인하고 운영 {counts['applied']['operating']}개·관련 API/worker/source 검사 {counts['applied']['native']}개를 추가 통과했다. 무관한 전체 native 검사는 반복하지 않았다. 실제 class/다른 binding의 원래 공급자, implementation guard와 정책 identity를 확인했다. API 검사는 실제 preflight·fake provider 경로이며 실제 외부 이미지 호출이 아니다.
- 커밋될 HEAD 기반은 양쪽 43검사 중 기존 실패 2건이 동일했다(41 PASS, 신규 회귀 0). 미커밋 source-effects 보정이 HEAD에 없기 때문에 발생한 기존 `test_complete_source_footprint_survives_native_and_augmentation_views`, `test_unknown_effects_do_not_become_material_scope` 실패다. 이를 전체 HEAD suite PASS로 표시하지 않는다. 원래 보정을 이번 커밋에 섞지 않는다.
- 실제 현재 H-F2 release의 control·제거·적용 front end에서 기존 issued view, 새 retrieve, view, compose-audit, deliver 5명령씩 PASS했다. 원래 query 벡터만 재사용했고 18,180 CID·18,182 RID 전체 풀, 슬롯당 BM25F 1회·local cosine 1회, 원래 top8와 전체 순위 digest/목표 결과가 같았다.
- 기존 설치 kernel의 정확한 점수/전체 순위와 원래 H/native receipt·구성 감사를 재실행했다. 별도로 원래 봉인 코드의 native 감사, archive 순위/집계/전용 테스트 재현, negative CLI, 파생 native view의 원본/제거/적용 출력을 확인했다. 원래 store가 없는 과거 실행을 새로 복구했다는 뜻은 아니다. archive 품질 HOLD를 유지했다.
- 네트워크·원본 파일 쓰기·원본 source로의 fallback을 차단하고 독립 복사본에서 검사했다. 데이터/봉인 source·알고리즘 가드를 약화하지 않았다. 임시 index에 커밋용 패치를 적용해 source 3개만 +2/-5이고 기존 미커밋 수정이 stage되지 않음을 확인했다.

## 보존·커밋 경계

보호 {len(b['files']):,}경로와 CURRENT {len(b['pointers'])}개를 비교했다. 3개 승인 소스만 교체를 허용하고 나머지 bytes·mode·inode·link와 두 worktree의 원래 dirty 상태·payload를 보존했다. 이번 evidence 디렉터리와 source 3개만 명시적 allowlist/부분 index 패치로 커밋한다. 이전 분석 디렉터리, 기존 후보·태그·index·runtime config·독립 작업의 미커밋 수정은 stage하지 않는다.

Gemini·새 임베딩·실제 이미지 호출·CURRENT 쓰기·runtime 발행·push는 0회다. 현재 선택은 H `{b['installed']['config']['generation_id']}`, native `{b['installed']['config']['native_generation_id']}` 그대로다. 보호 비교와 staged 검토는 각각 `AFTER-PRESERVATION.json`, `STAGED-CHECK.json`에 있다. 커밋 후 확인은 별도 private 결과에 보존한다.
'''
    with (E/'REPORT.md').open('x') as f:f.write(report)
    print('finalized; source counts',counts,flush=True)
def stage():
    assert run.state.read(E/'RESULTS.json')['status']=='PASS';t=run.state.read(E/'TARGETS.json');b=run.baseline()
    assert run.state.git(ROOT,'rev-parse','HEAD').decode().strip()==t['base_head'] and not run.state.git(ROOT,'diff','--cached','--name-only')
    assert all(run.state.sha(ROOT/p)==h for p,h in t['working'].items())
    raw=gzip.decompress((E/'INDEX.patch.gz').read_bytes());assert run.digest(raw)==t['patches']['INDEX']['raw_sha256']
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','--check','-'],input=raw,check=True)
    subprocess.run(['git','-C',str(ROOT),'apply','--cached','-'],input=raw,check=True)
    names=set(run.GATES+run.POST)|{'run.py','worker.py','references.py','managed.py','head_check.py','finalize.py','post_commit.py',
        'BASELINE-DELTA.json.gz','TARGETS.json','PRIVATE-PROJECTS.json','WORKING.patch.gz','INDEX.patch.gz','APPLY-INTENT.json','APPLICATION.json',
        'PRE-STAGE-PRESERVATION.json','AFTER-DELTA.json.gz','RESULTS.json','REPORT.md'}
    names.update('INPUT-'+name for name in ('INVENTORY.json','PRIVATE-PROBE.json','DOC-REFERENCES.json','DATA-v2.json','PRESERVATION.json','SUMMARY.json'))
    assert all((E/name).is_file() for name in names)
    evidence=sorted(str((E/name).relative_to(ROOT)) for name in names)
    assert all(not p.endswith(('.pyc','.pyo')) for p in evidence)
    private=Path(run.state.read(E/'PRIVATE-PROJECTS.json')['private_parent']);allow=private/'stage-evidence.paths0';allow.write_bytes(b'\0'.join(p.encode() for p in evidence)+b'\0')
    subprocess.run(['git','-C',str(ROOT),'add','--pathspec-from-file='+str(allow),'--pathspec-file-nul'],check=True)
    staged=set(run.state.git(ROOT,'diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert staged==run.TARGETS|set(evidence)
    assert all(run.digest(run.state.git(ROOT,'show',':'+p))==h for p,h in t['index'].items())
    for rel in run.TARGETS:assert run.small_cleanup.dirty_payload(run.state.git(ROOT,'show',':'+rel),(ROOT/rel).read_bytes())==t['original_dirty_payload_sha256'][rel]
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],check=True)
    approved=sorted([*staged,str((E/'STAGED-CHECK.json').relative_to(ROOT))])
    new(E/'STAGED-CHECK.json',{'status':'PASS','base_head':t['base_head'],'message':run.MESSAGE,'allowed_paths':approved,'source_index_blobs':t['index'],
        'source_added_lines':2,'source_deleted_lines':5,'original_dirty_payload_not_staged':True,'CURRENT_writes':0,'Gemini_calls':0,'push':False})
    subprocess.run(['git','-C',str(ROOT),'add','--',str((E/'STAGED-CHECK.json').relative_to(ROOT))],check=True)
    actual=set(run.state.git(ROOT,'diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert actual==set(approved)
    subprocess.run(['git','-C',str(ROOT),'diff','--cached','--check'],check=True)
    print('staged allowlist',len(actual),'paths, including 3 source paths; original dirty work excluded',flush=True)
if __name__=='__main__':
    if sys.argv[1]=='finish':finish()
    elif sys.argv[1]=='stage':stage()
    else:raise ValueError(sys.argv[1])
