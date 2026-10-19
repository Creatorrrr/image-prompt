# 후보 함수 4개·50행 정리 계획

2026-10-19 · 8단계 실행 · 함수 4개·50행 제거 · H 단독+F2/CURRENT 유지

실제 적용·검증·단계별 커밋은
`docs/research-evidence/photo-prompt/runtime-four-functions-20261019/REPORT.md`를 따른다.
작업 소스의 네 함수만 제거했고 봉인된 설치본과 과거 소스는 유지했다.
아래는 승인된 계획 원문이다. 실행 단계와 최종 보존 검사 결과는 위 보고서에 기록한다.

## 목표와 적용 범위

현재 작업 소스에서 아래 함수만 정리한다. 설치된 H 단독+F2의 검색 결과와 호출
예산, 과거 실행의 원래 코드·receipt·감사 결과, 기존 미커밋 작업과 CURRENT를 보존한다.
검증을 통과한 함수만 제거하고 나머지는 원래 상태에 남긴다.

근거는 `docs/research-evidence/photo-prompt/runtime-legacy-followup-20261019/REPORT.md`다.
이 계획은 이전 9개 함수·provider/공개 routing 분리 계획을 다시 실행하는 것이 아니다.
대상 4개 밖의 함수, provider, dispatcher, CLI 계약, 캐시·shard·역사 store 정리는 포함하지 않는다.

| 순서 | 함수 | 파일:현재 행 | 함수 행수 |
|---|---|---|---:|
| 1 | `_normalized_lexicon` | `scripts/bm25f_retrieval.py:177` | 2 |
| 2 | `resolve_rows` | `scripts/photo_native_pack.py:34` | 12 |
| 3 | `legacy_camera_clauses` | `scripts/photo_camera_evidence.py:20` | 28 |
| 4 | `publish_if_ready` | `scripts/photo_runtime_sources.py:441` | 8 |
| 합계 | 4개 | 모두 `skills/photo-prompt-image-generator/` 아래 | 50 |

작성 시점 HEAD는 `6bb941d60e39baac288de085c1e31d2919cb3e85`이며 네 파일은 모두
미커밋 변경이 없다. main의 기존 변경/미추적 경로는 40,499개, 다른 worktree는
6,161개, CURRENT는 168개다. 실행 직전에 다시 수집하며 현재 수치를 고정 가정으로 쓰지 않는다.

## 고정 조건과 지문 검사 해석

- 공통 positive 풀 전체, 슬롯별 H 질의, BM25F 1회·로컬 embedding/cosine 검색
  1회, F2·RRF10·CID 중복 제거·top8을 유지한다. 검색 정책이나 후보 내용을 바꾸지 않는다.
- 모든 CURRENT의 경로·내용·권한·inode·링크, `retrieval-runtime.json`, 설치된
  H/native 세대의 코드·데이터·manifest·모델·receipt와 원래 run을 보존한다.
  운영 세대 발행·활성화·설치 선택 변경은 없다.
- 기존 modified/staged/untracked 작업과 다른 worktree를 보존한다. 해당 네 파일에
  새 기존 작업이 생겼거나 patch가 겹치면 관련 항목은 보류한다. stash/reset/clean은 사용하지 않는다.
- Gemini, 새 임베딩 추론, 새 의미 판정·전수 의미 검토는 하지 않는다.
  기존 query vector·판정·입력과 오프라인 fixture를 재사용한다.
- source/algorithm 지문 검사를 약화하거나 원래 manifest·receipt를 재계산하지 않는다.
  새로운 운영 코드나 호환 stub을 scripts/precore에 추가하지 않는다.
- 예전 CURRENT의 코드 74개와 작업 소스 77개 사이의 기존 차이는 이번에 고치지 않는다.

이전 실험은 작업 소스에서 함수 19개를 제거해도 별도 봉인된 H+F2가 실행된다는
것을 확인했다. 그러나 대상 4개만 제거한 수정 소스 전체 회귀를 대신하지는 않는다.
작업 소스 회귀, 실제 설치본, 과거 봉인 코드 재현을 각각 검증해야 한다.

변경된 작업 소스로 원래 세대를 직접 읽으려 할 때 지문 검사가 거부하는 것은
예상되는 부정 테스트다. 이것만으로 H+F2 회귀라고 판단하지 않는다. 반대로 원래
성공해야 하는 공개 명령이 실패하는 것을 정상 거부로 재분류해서도 안 된다.
성공이 필요한 관련 기준선 검사가 실패하면 해당 항목은 보류한다. 무관한 기존
실패는 근거를 분리해 기록하고 성공 수에 포함하지 않는다.

## 1단계 — 대상과 보존 기준선 고정

함수별 파일 SHA, 함수 원문·AST SHA, decorator와 정확한 제거 범위, HEAD와
작업 소스 차이를 기록한다. 네 함수 총 50행을 상한으로 삼고 인접 빈 줄 외의
import 정리·포맷 변경·다른 함수 삭제는 확대하지 않는다.

양쪽 worktree의 HEAD/index/staged·기존 변경/미추적 파일, CURRENT 전체,
설치 선택·코드 집합·모델 lock, 원래 run과 receipt/index, source/실험 archive 및
복원 lock을 보호한다. 기존 protection은 재사용하고 추가 경로만 별도 고정한다.
과거 baseline이나 분석 증거를 덮어쓰지 않는다.

**통과 기준:** 네 파일이 여전히 깨끗하고 함수·설치·보호 자료가 확인한 원본과
일치한다. 차이가 있으면 원인을 확인해 관련 항목을 보류한다. 다른 worktree의
HEAD/index와 기존 staged 내용을 변경하지 않는다.

**산출물:** 새 실행 증거 디렉터리의 TARGETS, 보호 delta, 입력/환경/검사 목록.

## 2단계 — 함수별 참조와 공개 경로 재확인

정적 호출뿐 아니라 import 별칭, export, 문자열/getattr/registry, 내장 Python,
CLI/subprocess, 문서 명령, fixture와 봉인 소스 참조를 점검한다. 같은 이름의
다른 함수 호출과 실제 대상 모듈의 소비자를 구분한다.

각 함수를 REMOVE_CANDIDATE / KEEP_SHARED / KEEP_REPLAY / DEFER로 분류한다.
새 H+F2 요청·기존 H+F2 run·기존 native run·유지보수 명령의 실제 소스 선택을
기록하고, 과거 소비자는 원래 봉인 코드로 해결되는지 확인한다. 이를 해결하려고
공개 routing이나 provider를 추가 변경하지 않는다.

**통과 기준:** 알려진 현재 소비자가 없고 필요한 과거 소비자의 코드가 보존된다.
해결하지 못한 동적 호출·문서 계약·외부 진입점은 해당 함수 DEFER다. 출처가 없는
실행을 새 코드로 대체하거나 호출자를 연쇄 제거하지 않는다.

## 3단계 — private 제거 patch와 대조군 준비

실제 소스와 필요한 fixture를 독립적인 임시 복사본에 준비한다. 원래 파일을
hardlink로 공유하지 않는다. 각 함수 제거 patch를 위 순서로 독립 작성하고,
먼저 함수별 문법/import 및 관련 기능 smoke를 수행한다. 통과한 조합으로 최종
수정 소스 복사본을 고정한다.

원문에서 해당 함수만 사라졌는지 AST·diff로 확인하고, 역적용하면 원래 파일
bytes와 기존 diff가 정확히 복원되는지 검증한다. 원래 함수를 남겨 놓은 대조군도 유지한다.

**통과 기준:** 정확한 제거 범위·역적용·import·대상 기능 검사가 통과한다.
실패한 함수는 원본에 적용하지 않는다. 조합 실패의 원인을 분리할 수 없으면
영향받은 조합을 보류하고 모든 함수를 제거하는 목표를 강제하지 않는다.

## 4단계 — 수정한 작업 소스 자체의 회귀 검증

실행 모듈의 `__file__`과 코드 hash를 기록하여 수정한 복사본이 실제 로드됐는지
확인한다. 설치된 원래 코드를 테스트한 결과로 수정 소스 검증을 대신하지 않는다.

| 제거 함수 | 유지해야 할 현재 기능 |
|---|---|
| `_normalized_lexicon` | prepared lexicon·cached normalization·BM25F 점수/정렬 |
| `resolve_rows` | WorkingPack·공통 후보 참조·pack 직렬화/조회 |
| `legacy_camera_clauses` | camera authoring 선언·요구 축·증거 전달과 구성 감사 |
| `publish_if_ready` | 명시적 publication·source update·freshness와 receipt 검증 |

기존 operating/native 회귀를 재사용한다. 직전 기준은 operating 48개, native
70개이며 이름·수·skip·실행 경로를 다시 확인한다. 필요한 private store/CURRENT는
fixture 안에서만 생성한다. 원래 store나 CURRENT에는 쓰지 못하게 한다.

**통과 기준:** 관련 기능과 선택한 회귀가 실제 수정 소스에서 통과하고, 성공
기능·거부 조건·권한 판단에 회귀가 없다. 테스트 누락/skip/하네스 실행 실패는
PASS가 아니다. 실패 원인이 범위를 벗어나면 해당 변경을 보류하고 범위를 넓히지 않는다.

## 5단계 — H 단독+F2 실제 기본 경로 대조

기존 설치본과 원래 2목표의 query vector·issued 결과를 재사용한다. 대조군과
수정 소스 복사본에서 일반 진입점의 기존 run `view`, 새 private run의
`retrieve → view → compose-audit → deliver`를 실행한다.

원래 검색 대상 전체와 질의를 유지하고 top8, CID 중복 제거 이후 전체 순서/점수
digest, 목표 메타데이터, receipt·구성 감사·최종 phase를 비교한다. 실제 설치
커널의 전체 RID 점수 배열과 순서 대조는 기존 installed 검사를 별도로 재사용한다.
실행 당시 공통 풀 수와 query별 BM25F/local cosine 호출 수를 기록한다.

실행 worker에서 네트워크·원래 프로젝트/다른 worktree/공유 cache 쓰기를 차단한다.
기존 query cache hit를 필수로 하고 추론 경로 실행도 차단한다. 과거 실험의
이중 sandbox 오류나 manifest/모델 무결성 읽기 차단을 반복하지 않는다.

**통과 기준:** 두 비교군의 결과가 원래 결과와 정확히 같고 슬롯당 검색은
BM25F 1회·local cosine 1회다. 추가 검색·새 추론·다른 세대로의 fallback이 없다.
기존 H/native 설치 선택·봉인 코드와 데이터는 그대로다.

## 6단계 — 과거 실행과 지문 보호의 교차 검증

기존 `native_replay.py`와 source/실험 archive 복원을 사용한다. 원래 store와
코드가 있는 검증 대상 run을 먼저 고정하고, 원래 발행 receipt·pack·manifest·
전체 코드 집합과 구성 감사를 검증한다. 현재 작업 소스로의 읽기 fallback과
네트워크·새 임베딩을 차단한다.

기존 archive의 저장 순서 450개와 전용 검사 17개도 재사용한다. 결과 수가 달라지면
성공으로 간주하지 않는다. 검증한 과거 run의 일반 공개 명령 동작도 별도 대조하여,
명시적 frozen 감사의 성공만으로 공개 경로 전체가 검증됐다고 보고하지 않는다.

원래 세대/receipt 불일치·코드 변조·원본 누락의 거부가 유지되는지 확인한다.
다른 알고리즘 지문을 과거 코드처럼 받아들이도록 검사나 예외를 수정하지 않는다.

**통과 기준:** 선택한 과거 실행·archive 결과와 원래 거부 동작이 보존된다.
성공해야 할 관련 경로가 실패하거나 실행할 소스를 확정하지 못하면 해당 함수는
보류한다. 원래 store가 없는 41건은 재현 성공에 포함하지 않고 원래 자료와
대체 manifest 7개를 보존한다. 이 불완전한 기존 증거를 임의 복원해 통과시키지 않는다.

## 7단계 — 통과한 함수만 작업 소스에 적용

2–6단계를 통과한 함수의 patch만 적용한다. 적용 직전 대상 파일 SHA·깨끗한
상태·기존 작업을 재확인하고 달라졌다면 관련 항목을 보류한다. 다른 변경을
덮어쓰거나 원래 보류 함수를 함께 제거하지 않는다.

수정 파일의 최종 bytes가 private 검증본과 같은지 확인하고 관련 source smoke와
공개 진입점 검사를 수행한다. 이미 통과한 전체 suite는 코드·환경·입력이 같으면
증거를 재사용하며, 새 차이나 실패가 있을 때 필요한 검사만 다시 실행한다.

**통과 기준:** 적용 diff가 승인된 함수와 인접 빈 줄에 한정되고 남은 함수·import·
공개 형식이 유지된다. 작업 소스 지문 변경은 기록하되 설치/역사 지문과 CURRENT는
동일해야 한다. 적용 후 문제가 있으면 이번 patch만 되돌리고 관련 항목을 보류한다.
기존 작업을 포함한 파일 전체 checkout/reset으로 복구하지 않는다.

## 8단계 — 최종 보존 검사와 함수별 결과 보고

원래 보호 파일은 정확한 수정 allowlist 네 파일의 승인된 변경만 제외하고
내용·권한·inode·링크를 대조한다. CURRENT 전체·설치 선택·원래 세대/receipt와
기존 변경·미추적·staged 상태, 다른 worktree의 HEAD/index를 확인한다. bytecode
21개·shard 5세대·원래 store 없는 실행 자료도 그대로여야 한다.

함수별로 REMOVED / KEEP / DEFER, 실제 제거 행수, 근거, 검증한 구현·입력·결과,
적용 commit을 기록한다. 작업 소스에서 제거된 함수가 봉인된 설치/역사 소스에
남는다는 점을 명시한다. 단계 처리 완료와 네 함수 모두 제거 완료를 구분한다.

실행을 별도로 요청받으면 각 단계의 구현 또는 보류 판정과 검증 후 해당 변경만
커밋하고 다음 단계로 간다. 정확한 경로를 stage하고 cached diff를 검토한다.
원래 staged 작업을 보존하며 이번 변경만 커밋할 수 없다면 관련 단계는 보류한다.
현재 계획 작성에서는 커밋·push·설치 선택 변경을 하지 않는다.

**완료 기준:** 검증한 함수만 제거되고 보류 항목은 원래 상태로 남는다.
H 단독+F2 운영·선택한 과거 재현·기존 작업·CURRENT 보존의 증거와 한계가
명확하다. 0–4개 중 실제 통과한 수로 보고하며 제거 수를 맞추기 위해 범위를 확대하지 않는다.

## 실행 시 남길 자료

새 증거 디렉터리 하나에 보호 delta·TARGETS·참조별 ACTION-LIST·독립 patch·
실행 소스/환경/fixture hash·운영/작업 소스/과거 재현 검사·최종 PRESERVATION·
DEFER·REPORT를 모은다. 같은 운영 소스나 대형 데이터를 새 archive로 중복 복제하지 않는다.
기존 분석 증거·원래 로그·복구 lock·아카이브는 그대로 재사용한다.
