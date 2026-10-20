# import 바인딩 5개·3파일 정리

승인된 import 바인딩 5개만 제거했다. 작업 소스와 커밋용 HEAD 패치를 별도로 검증했고 기존 미커밋 수정은 커밋에 넣지 않는다. 운영 선택과 CURRENT는 변경하지 않는다.

| 파일 | 제거 바인딩 |
|---|---|
| `scripts/photo_workflow_worker.py` | `WorkflowError` |
| `scripts/generate_images_via_api.py` | `PreflightError` |
| `scripts/audit_composed_prompt.py` | `AUTHORIAL_CORE_CONTRACT_VERSION`, `DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION`, `property_effects_allowed` |

경로는 `skills/photo-prompt-image-generator/` 기준이다. 공급 모듈의 실제 정의와 나머지 import는 유지했다. 3파일에서 2행 추가·5행 삭제, 순감소 3행이며 나머지 AST는 같다. 나머지 미확정 module import 26개와 해시가 설치본에 결합된 local worker import 2개는 범위 밖에 두었다. 승인한 5개 중 보류한 항목은 없다.

## 검증

- 현재 Python 188개에서 재참조를 확인했다. 보존 Python 10,147개의 분석 이후 SHA가 그대로였고, 신규 자료도 확인했다. 보고서 문자열·namespace 복사·입력이 제한된 CHARACTER_* 검사를 실제 named 소비자와 구분했다. 알 수 없는 외부 reflection의 부재까지 증명하지 않는다.
- source 원본·제거 복사본 각각 운영 계약 48개·native/API 117개를 통과했다. 실제 적용본은 전체 파일 SHA가 검증 복사본과 같음을 확인하고 운영 48개·관련 API/worker/source 검사 28개를 추가 통과했다. 무관한 전체 native 검사는 반복하지 않았다. 실제 class/다른 binding의 원래 공급자, implementation guard와 정책 identity를 확인했다. API 검사는 실제 preflight·fake provider 경로이며 실제 외부 이미지 호출이 아니다.
- 커밋될 HEAD 기반은 양쪽 43검사 중 기존 실패 2건이 동일했다(41 PASS, 신규 회귀 0). 미커밋 source-effects 보정이 HEAD에 없기 때문에 발생한 기존 `test_complete_source_footprint_survives_native_and_augmentation_views`, `test_unknown_effects_do_not_become_material_scope` 실패다. 이를 전체 HEAD suite PASS로 표시하지 않는다. 원래 보정을 이번 커밋에 섞지 않는다.
- 실제 현재 H-F2 release의 control·제거·적용 front end에서 기존 issued view, 새 retrieve, view, compose-audit, deliver 5명령씩 PASS했다. 원래 query 벡터만 재사용했고 18,180 CID·18,182 RID 전체 풀, 슬롯당 BM25F 1회·local cosine 1회, 원래 top8와 전체 순위 digest/목표 결과가 같았다.
- 기존 설치 kernel의 정확한 점수/전체 순위와 원래 H/native receipt·구성 감사를 재실행했다. 별도로 원래 봉인 코드의 native 감사, archive 순위/집계/전용 테스트 재현, negative CLI, 파생 native view의 원본/제거/적용 출력을 확인했다. 원래 store가 없는 과거 실행을 새로 복구했다는 뜻은 아니다. archive 품질 HOLD를 유지했다.
- 네트워크·원본 파일 쓰기·원본 source로의 fallback을 차단하고 독립 복사본에서 검사했다. 데이터/봉인 source·알고리즘 가드를 약화하지 않았다. 임시 index에 커밋용 패치를 적용해 source 3개만 +2/-5이고 기존 미커밋 수정이 stage되지 않음을 확인했다.

## 보존·커밋 경계

보호 153,760경로와 CURRENT 168개를 비교했다. 3개 승인 소스만 교체를 허용하고 나머지 bytes·mode·inode·link와 두 worktree의 원래 dirty 상태·payload를 보존했다. 이번 evidence 디렉터리와 source 3개만 명시적 allowlist/부분 index 패치로 커밋한다. 이전 분석 디렉터리, 기존 후보·태그·index·runtime config·독립 작업의 미커밋 수정은 stage하지 않는다.

Gemini·새 임베딩·실제 이미지 호출·CURRENT 쓰기·runtime 발행·push는 0회다. 현재 선택은 H `dc25145b60431e9f75856af4a6200a28874e2e500cd978cb804e3cee4c5005f2`, native `9d253c2ed263bd6c048b75f2dd593f6fcfc91cb96984622d8917de2e87e5dfd1` 그대로다. 보호 비교와 staged 검토는 각각 `AFTER-PRESERVATION.json`, `STAGED-CHECK.json`에 있다. 커밋 후 확인은 별도 private 결과에 보존한다.
