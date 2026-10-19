# 미사용 함수 9개 정리와 과거 재현 로직 분리 계획

2026-10-19 · 계획 작성 · 구현·제거·커밋 미실행

## 목적과 고정 조건

현재 유지보수하는 소스에서 사용하지 않는 함수를 정리하고, 과거 실행을 읽고
재현하는 경로를 명확히 분리한다. 현재 설치된 H 단독+F2와 기존 실행의 의미·순위·
receipt·감사 결과를 보존한다. 제거 개수보다 보존과 재현 검증을 우선한다.

- 공통 positive 풀 전체, 슬롯별 동일한 H 질의, BM25F 1회·로컬 임베딩/cosine
  검색 1회, F2·RRF10·realization 결합 후 CID 중복 제거·top8을 유지한다.
- 모든 CURRENT의 경로·내용·권한·inode·링크, `retrieval-runtime.json`, 설치된
  H/native 세대의 코드·데이터·manifest·모델·receipt를 유지한다. 새 세대를
  publish/activate하거나 hash 검사를 약화해서 정리를 통과시키지 않는다.
- 기존 modified·staged·untracked 작업과 별도 작업 트리를 보호한다.
  stash/reset/clean, 원래 실행의 재작성, 다른 작업 트리의 자동 병합은 하지 않는다.
- Gemini·새 임베딩 추론·후보 수정·새 의미 판정·전수 의미 검토는 하지 않는다.
  기존 질의·벡터·판정·검색 결과와 오프라인 fixture를 재사용한다.
- 정리 후보는 아래 9개와 그 제거/분리에 직접 필요한 경계 코드로 한정한다.
  bytecode 21개, shard, 역사 store, 사용자 출력·이미지·ledger는 별도 정리하지 않는다.
- 참조·출처·변경 충돌이 불명확하거나 검증에 실패한 항목은 원래 경로에 남긴다.
  단계 종료와 전체 후보의 제거 완료를 구분하며, 보류 수를 숨기지 않는다.

## 현재 확인한 범위와 중요한 제약

계획 작성 기준 HEAD는 `bda1a22d1da5a6af014dbdeb05bf561b622a8873`다.
main 기존 변경/미추적 경로는 40,478개, 별도 작업 트리는 6,161개,
CURRENT는 168개다. 실행 직전에 다시 수집하며 이 숫자를 고정 가정으로 쓰지 않는다.

현재 scripts/precore Python 소스는 77개, 설치된 소스는 94개다. 설치된 코드와
main을 같은 것으로 간주하지 않는다. 기본 설치 H 세대는 `663038595155…`, native는
`9649504ffbcd…`이며 전체 ID는 `retrieval-runtime.json`에서 고정한다.

| 파일 | 함수 | 분류 |
|---|---|---|
| `scripts/photo_camera_evidence.py` | `legacy_camera_clauses` | 과거 literal camera fallback |
| `scripts/prompt_generator.py` | `get_gemini_api_key` | 과거 Gemini key 보조 |
| 위와 같음 | `cached_gemini_client` | 과거 Gemini client 보조 |
| 위와 같음 | `extract_embedding_values` | 과거 응답 변환 |
| 위와 같음 | `round_embedding_vector` | 과거 벡터 변환 |
| 위와 같음 | `_bm25f_lexicon_from_documents` | 과거 검색 어휘 보조 |
| 위와 같음 | `candidate_pack_float` | 과거 후보 숫자 처리 |
| 위와 같음 | `candidate_pack_assertion_discovery` | 과거 assertion discovery |
| 위와 같음 | `authorial_core_bm25f_query_fields` | 전체 core 기반 검색 필드 생성 |

파일 경로는 `skills/photo-prompt-image-generator/` 기준이다.
현재 소스·테스트 188파일, 설치 소스 94파일, 운영 소스 archive 94파일과 실험
archive Python 20파일에서 이 함수의 정적 참조를 찾지 못했다. 이는 미사용 후보의
근거이며 동적/외부 호출 부재나 제거 후 동작을 입증한 결과는 아니다.

`prompt_generator.py`에는 기존 미커밋 변경이 있다. 후보 8개의 함수 AST는
HEAD와 같지만, 이 사실만으로 파일 전체를 수정·stage할 수는 없다.
또한 `photo_runtime_sources.code_inventory()`는 scripts/precore 전체를 지문에
포함하고, `load_generation()`은 로드한 구현과 원래 세대의 알고리즘을 대조한다.
미사용 함수 삭제나 새 모듈 추가도 과거 receipt와 CURRENT의 사용 경로를 막을 수 있다.

따라서 과거 재현 경로의 검증을 함수 제거보다 먼저 진행한다. 현재 설치된 세대와
기존 source archive에는 당시 함수가 그대로 남는다. 그 봉인물을 편집하거나
새 코드로 바꾸는 작업은 이번 계획에 포함하지 않는다.

## 1단계 — 함수 목록·기존 작업·운영 기준선 고정

9개 함수별로 전체 이름, 파일, decorator를 포함한 원문 범위와 SHA, HEAD/작업
소스의 AST 및 내용 차이를 고정한다. 보호 baseline에는 다음을 포함한다.

- 두 작업 트리의 HEAD/index/staged 내용, 기존 변경·미추적 파일의 hash와 상태.
- 모든 CURRENT, 설치 선택, 실제 선택된 세대와 코드 집합, 모델/실행 환경 lock.
- 기존 run의 source binding·receipt/index·원본 출력과 source archive/복원 lock.
- 수정 가능한 정확한 함수·경계 코드 범위와 수정하면 안 되는 기존 변경 범위.

작업은 별도의 임시 소스 복사본에서 준비한다. 기존 dirty 파일은 원본 bytes와
기존 diff를 보존한 뒤 이번 변경만 독립 patch로 만들 수 있는지 확인한다.
완료된 cleanup의 freeze/삭제 도구를 다시 실행하지 않는다.

**통과 기준:** 새 기준선이 기존 보호 증거와 일치하고, 이번 patch를 역적용하면
분석 전 원본 bytes와 기존 diff가 정확히 복원된다. 겹치는 함수 변경이나 충돌이
있으면 해당 항목은 보류한다. 깨끗한 파일만 먼저 진행할 수 있다.

## 2단계 — 함수·진입점별 실제 의존성 판정

정적 호출 외에 import/export, decorator, getattr/문자열 registry, CLI/subprocess,
문서 명령, fixture, serialized binding과 봉인 소스/manifest 참조를 확인한다.
진입점은 새 H-F2 요청, 기존 H-F2 run, 기존 native run, 유지보수·과거 평가로 나눈다.

함수마다 REMOVE_CANDIDATE / KEEP_SHARED / KEEP_REPLAY / DEFER로 판정하고,
근거·호출자·보호 충돌·해당 함수를 다루는 검사 목록을 기록한다. 참조가 있다는
이유만으로 호출자를 연쇄 삭제하거나 이번 대상을 9개 밖으로 늘리지 않는다.

**통과 기준:** 제거 후보의 알려진 소비자가 없거나, 과거 소비자가 검증된 봉인
소스를 사용한다는 근거가 있다. 조사할 수 없는 소비자와 불명확한 동적 호출은
DEFER다. `legacy`, `Gemini`, `SPACE`라는 이름만으로 제거하지 않는다.

## 3단계 — 과거 재현 소스와 실행 경계부터 검증

기존 `SOURCE-LOCK.json`, 운영 소스 archive, 실험 archive와 run별 봉인 세대를
우선 재사용한다. 같은 소스 전체를 새 날짜 폴더로 중복 복사하지 않는다.

과거 실행은 검증한 receipt의 store/generation과 코드 집합으로 정확히 해결하는
작은 재현 진입점을 `tools/photo_runtime_maintenance/native_replay.py` 같은 별도
유지보수 모듈에 준비한다. 정확한 파일명은 2단계 참조 판정 후 확정한다. 상대 경로와 환경을 private 임시
루트에서 복원하고, 원래 Python/모델·정본 binding과 hash 검사를 유지한다.
run에 기록된 경로를 검증 없이 실행하거나 현재 소스를 과거 코드처럼 전달하지 않는다.

이 경계는 먼저 임시 소스에서 시험한다. 이미 pack이 있는 native run의 기존
retrieve/resume/view/compose-audit/deliver가 어떤 코드를 사용하는지 확인하고,
기존 명령의 동작을 보존할 수 있는 작은 routing 변경을 같은 단계에서 검증한다.
직접 native CLI와 CURRENT를 읽는 유지보수 경로도 따로 확인한다. 통과한 경계
변경을 먼저 적용·검증·커밋한 뒤 함수 제거 단계로 진행한다. 함수 제거를 먼저
반영하고 후속 단계에서 과거 실행 경로를 고치는 순서로 진행하지 않는다.

**통과 기준:** 원래 코드로 실행한 결과·receipt 검증·감사/권한 판단이 baseline과
같고, 네트워크·연구 checkout·새 모델 호출 없이 재현된다. 잘못된 세대/receipt나
누락 파일은 기존처럼 거부한다. 실행기 재귀 호출과 현재 소스로의 fallback이 없다.

현재 소스를 바꾼 상태에서 기존 CURRENT 경로의 유효성을 유지할 수 없다면,
관련 함수·routing 변경은 보류한다. 새 세대 발행, hash 검사 예외, CURRENT 수정으로
해결하지 않는다. 원래 store를 찾지 못한 실행 41건은 성공으로 집계하지 않고,
연결된 원본·대체 manifest 7개를 유지한다.

## 4단계 — 검증된 미사용 함수만 작은 묶음으로 제거

camera 함수 1개, Gemini 보조 4개, 검색/후보 보조 4개를 독립적인 patch로 만든다.
2–3단계를 통과한 함수만 제거하며 각 묶음마다 다음을 확인한다.

- 함수 본문·decorator 밖에 필요한 변경이 없는지 확인한다. import 정리를
  자동으로 확대하지 않는다. 남은 camera authoring export와 공용 기능을 유지한다.
- 테스트는 실제 변경된 임시 소스를 로드한다. 기존 설치 세대의 검사만 통과하고
  수정 소스도 검증했다고 보고하지 않는다.
- 기존 수정 파일은 이번 patch를 역적용한 결과가 원래 bytes와 같아야 한다.
  후보 함수가 HEAD와 같더라도 다른 미커밋 변경을 섞어 stage하지 않는다.
- 사라진 API를 조용히 다른 동작으로 대체하는 stub이나 새 compatibility alias를
  만들지 않는다. 그런 호환이 필요한 소비자는 KEEP_REPLAY 또는 DEFER로 재분류한다.

**통과 기준:** 해당 묶음의 기능·운영·재현 검사가 통과하고 기존 작업의 원래
내용이 보존된다. 실패한 patch만 작업 복사본에서 배제하고 원본에는 적용하지 않는다.
9개 전부 제거를 완료 조건으로 강제하지 않는다.

## 5단계 — 과거 provider·검증·유지보수 책임 분리

다음 경계를 함수/API와 명시적 유지보수 진입점으로 구분한다.

| 책임 | 처리 방향 |
|---|---|
| 로컬 임베딩·벡터/space 검증·공통 저장 | 현재 공용 기능 유지 |
| 기존 Gemini receipt/space/실행 증거 읽기 | 네트워크 없는 과거 증거 검증으로 보존 |
| 과거 Gemini 신규 요청·재시도·응답 보관 구현 | 기존 봉인 소스에 보존하고 재현/유지보수 경계로 분리 |
| activation/rollback·qualification CLI | 기존 계약을 보존하며 현재 검색과 분리해 문서화/검증 |
| 기존 native 검색·구성·권한 감사 | 과거 binding과 현재 공용 감사의 역할을 구별해 보존 |

`photo_embedding_provider.py` 전체를 옮기지 않는다. `atomic`, 벡터 검증,
현재 로컬 batching과 cache 계약은 실제 호출자와 함께 유지한다. Gemini 증거 읽기와
새 원격 요청을 혼동하지 않는다. 분리할 수 있다면 과거 CLI가 검증된 원래 소스를
명시적으로 사용하도록 하고, 정상 H-F2가 그 실행기를 import/호출하지 않게 한다.

소스 설정이 없을 때 Gemini를 기본으로 고르는 옛 분기도 정리 검토에 포함한다.
현재 로컬 경로에서 설정 누락/오염은 명확히 거부하는 방향으로 설계하되, 이것이
과거 fixture·CLI 계약 변경이라면 2–3단계의 재현 증거 없이는 적용하지 않는다.
Gemini transport와 rollback은 실제로 호출하지 않고 고정 증거·격리 fixture로 검증한다.

**통과 기준:** 현재 로컬 기능과 과거 기록 해석 결과가 같고, 새 요청이 Gemini나
과거 검색으로 자동 연결되지 않는다. 원래 경로에 유지보수 의존성이 있거나 작은
분리로 끝낼 수 없는 부분은 구현을 남기고 정확한 이유와 실행 경계를 문서화한다.

## 6단계 — 공개 명령의 교차 검증과 실패 경로 검사

3단계의 재현 경계와 4–5단계의 함수/책임 분리를 공개 진입점에서 함께 검증한다.
새 요청은 현재 설치된 H-F2, 이미 binding된 실행은 해당 세대/receipt를 사용하는 동작을 유지한다.
명령 이름, 기본 옵션, 공개 pack/receipt 형식과 선택 세대를 바꾸지 않는다.

검사는 새 요청·기존 H-F2·기존 native run을 각각 포함한다. 설정/세대 누락,
manifest/코드 변조, receipt와 pack 불일치, 부적절한 store override, 재현 소스
미확보를 거부하고, 실패 시 다른 세대나 현재 소스로 우회하지 않는지 확인한다.

**통과 기준:** CURRENT·설치 선택·원래 run bytes를 쓰지 않고 기존 공개 명령의
결과를 보존한다. wrapper가 순환하거나 protected path를 수정하면 보류한다.
기존 검증기의 예외 처리·지문 범위를 축소하는 방식은 통과로 인정하지 않는다.

## 7단계 — 운영·실제 설치·과거 재현을 구분해 최종 검증

기존 검사 도구와 고정 입력을 재사용하되 새 결과는 새 경로에 저장한다.
삭제 완료 단계에 묶인 오래된 cleanup suite/freeze/GC 명령은 재실행하지 않는다.

| 검증 대상 | 확인할 내용 |
|---|---|
| 수정 소스 회귀 | 기존 operating/native 계약, 새 분리·라우팅의 실제 동작 |
| 실제 설치 H-F2 | 기존 두 목표의 전체 후보 점수·순서·top8·receipt/감사 동일성 |
| 검색 호출 예산 | search 슬롯당 BM25F 1회·로컬 embedding/cosine 1회, 추가 query 없음 |
| 일반 공개 CLI | private run 복사본의 retrieve/view/compose-audit/deliver 및 기존 native 재사용/resume |
| 과거 archive | 기존 450개 저장 순서와 17개 전용 검사, source/실험 archive 복원 |
| 보존·실패 경로 검사 | pointer/세대/기존 작업 동일성, 네트워크 차단·fallback 거부·변조 거부 |

직전 기준은 operating 48개, native 70개다. 실행 시 테스트 이름/수/skip을 다시
확인하며, 누락·skip·발견 실패를 성공으로 보지 않는다. 추가 검사는 실제로 바꾼
경계의 회귀를 입증하는 것만 작성한다. 검색 점수·판정 기준을 바꿔 통과시키지 않는다.

수정 소스를 검증한 실행과 봉인된 설치/과거 코드를 검증한 실행을 분리 기록한다.
함수 제거로 working source의 코드 지문은 바뀔 수 있으므로 의도한 diff를 기록하고,
설치/역사 세대의 지문은 동일성을 요구한다. 바뀐 working 지문으로 인해 보호된
CURRENT/기존 공개 경로가 실패하면 해당 변경은 보류한다.

**통과 기준:** 적용하는 각 항목의 필수 검사가 모두 통과하고 기존 실패 대비 새
회귀가 없다. baseline부터 실패한 관련 검사는 원인을 해결하거나 해당 항목을 보류한다.
모든 과거 실행이나 이미지 품질을 전수 검증한 것으로 확대 해석하지 않는다.

## 8단계 — 결과·보류 목록과 이번 변경만 정리

함수 9개 각각에 대해 제거/보존/보류, 적용 commit, 근거와 통과 검사를 기록한다.
provider/CLI별 현재 경로와 과거 재현 경로, 원본 복원 방법, 알려진 외부 의존성도
함께 남긴다. 불변 설치/역사 소스에 남아 있는 옛 함수는 보존 근거를 명시한다.

실행을 요청받으면 각 단계의 구현·검증 후 이번 변경만 커밋하고 다음 단계로 간다.
미커밋 변경이 있는 파일은 HEAD에 이번 patch만 반영한 index와 실제 작업 트리를
각각 확인한다. 전체 파일 `git add`로 기존 변경을 섞지 않는다. 필요한 경우 별도
commit 대상 복사본도 검증하며, 원래 파일과 기존 patch의 보존을 최종 대조한다.

범위를 벗어난 실패를 억지로 수정하지 않는다. 보류 항목은 원래 상태를 유지하고
그 단계는 보류 판정의 기록으로 끝낼 수 있다. push·운영 전환은 이번 계획에 없다.

**완료 기준:** 통과한 변경만 반영되고, 미해결 9개 항목의 처리 상태와 과거 로직의
실행 경계가 명확하며 H-F2·과거 재현·기존 작업·CURRENT가 보존된다. CURRENT를
유지하려면 제거할 수 없는 부분이 있으면 그대로 보류 결과를 보고한다.

## 권장 실행 순서와 산출물

`보호 고정 → 소비자 판정 → 봉인 소스 재현 검증 → 함수 제거 → 과거 책임 분리
→ 공개 경로 교차 검증 → 통합 검증 → 결과/보류 정리` 순서로 진행한다.

새 증거 디렉터리 하나에 함수/경계별 ACTION-LIST, 보호 baseline의 기존 증거 참조와
추가분, 이번 patch, 실행 코드·환경·fixture hash, 검사 결과, REPORT와 DEFER 목록을
모은다. 기존 archive·원문·실행 로그를 새 위치의 내용으로 덮어쓰지 않는다.

계획 작성 시에는 이 문서와 계획 목록만 변경한다. 함수 제거·provider 분리·검사
실행·커밋은 아직 하지 않았다.
