# 후보 함수 4개·50행 정리 결과

2026-10-19 · H 단독+F2 유지 · 기존 작업/CURRENT 보존 · 단계별 로컬 커밋

**대상 함수 4개를 작업 소스에서 제거했다. 운영 소스 diff는 추가 0행·삭제 50행이며
대상 함수 보류는 0개다.** 설치된 H 단독+F2와 과거 실행의 봉인 소스에는 원래
코드를 유지했다. 검색 정책·후보 데이터·모델·설치 선택·CURRENT는 변경하지 않았다.

## 실제 제거 범위

| 함수 | 파일 | 제거 행수 | 처리 |
|---|---|---:|---|
| `_normalized_lexicon` | `scripts/bm25f_retrieval.py` | 2 | REMOVED |
| `resolve_rows` | `scripts/photo_native_pack.py` | 12 | REMOVED |
| `legacy_camera_clauses` | `scripts/photo_camera_evidence.py` | 28 | REMOVED |
| `publish_if_ready` | `scripts/photo_runtime_sources.py` | 8 | REMOVED |

파일은 `skills/photo-prompt-image-generator/` 기준이다. 함수 밖 AST는 동일하며
import·다른 함수·포맷 변경을 확대하지 않았다. module 자체와 현재 camera authoring,
prepared lexicon, WorkingPack·role view, 명시적 source publication·freshness 검사는 유지했다.

`TARGETS.json`은 원래 파일/함수/AST hash와 범위, `PATCHES.json`은 독립 제거 및
전체 제거 patch와 적용 결과 hash를 고정한다. patch는 원문 bytes를 보존해 gzip으로
저장했다. private 복사본에서 역적용한 원본 bytes가 정확히 일치했다.
실제 적용 파일은 검증한 private 파일과 SHA가 동일하다(`APPLICATION.json`).

## 단계별 처리와 커밋

| 단계 | 결과 | 로컬 커밋 |
|---|---|---|
| 1 보호 고정 | 원래 139,153경로·CURRENT 168개·정확한 4함수/50행 고정 | `cd6862350` |
| 2 소비자 확인 | 현재 source/test 188파일의 직접/별칭/문자열 참조 없음, 과거 사본 보존 | `2cf5d1d98` |
| 3 private patch | 대조군·함수별 4개·전체 제거 6경우의 기본 기능/역적용 검사 통과 | `6a126ea1b` |
| 4 수정 소스 회귀 | 실제 제거본 모듈로 operating 48개/native 70개, skip 0 | `1bbdd0de9` |
| 5 설치 기본 경로 | 두 비교군의 일반 CLI 10명령과 실제 설치 커널 점수/순서 일치 | `b09bf9717` |
| 6 과거 재현 | 원래 native receipt·구성 감사, archive 450순서/17검사, 공개 조회/거부 검사 | `0587a450f` |
| 7 원본 적용 | 4함수/50행 제거, 실제 소스·H+F2 CLI·native 공개 조회 재확인 | `5769e6642` |
| 8 보존/결과 | 전체 보호 검사, 함수별 결과·보류·커밋 범위 기록 | 이 보고서의 커밋 |

각 단계의 구현 또는 판정과 검증 후 해당 경로만 stage하여 커밋했다. 기존
미커밋·미추적 작업을 함께 stage하지 않았다. 이번 작업에서는 push하지 않았다.

## 검증 결과와 범위

| 검사 | 결과와 증거 |
|---|---|
| 변경된 작업 소스 operating | 48개 통과, skip 0 — `SOURCE-operating-final.json` |
| 변경된 작업 소스 native | 70개 통과, skip 0 — `SOURCE-native-qualified.json` |
| 실행 소스 확인 | 네 모듈의 실제 `__file__`과 SHA가 private 제거본임을 확인 |
| 기본 기능/지문 보호 | lexicon 경계, working/wire role card, camera 선언, 일치/불일치 구현 검사 통과 |
| 실제 설치된 커널 | 기존 2목표의 BM25F/cosine 전체 배열과 CID 중복 제거 순서가 원래 issued 자료와 정확히 일치 |
| 일반 H+F2 CLI | 대조군·private 제거본·원본 적용 후 각각 5명령, 합계 15명령 통과 |
| 적용 후 H+F2 결과 | 원래 top8·전체 순서/점수 digest·목표 메타데이터 일치, 최종 prompt_delivered |
| 검색 대상/예산 | 18,180 CID/18,182 RID 공통 풀, 목표별 BM25F 1회/local cosine 1회 유지 |
| 원래 봉인 감사 | 기존 설치 run 1건의 원래 native receipt와 구성 감사 PASS, 코드 94개/전체 863멤버 검증 |
| archive | 225+225=450 저장 순서 재현, 전용 검사 17개 통과, 기존 품질 HOLD 유지 |
| 공개 native 조회 | 파생 private fixture에서 대조군·제거본·원본 적용본의 출력이 정확히 일치 |
| 변조/누락 거부 | 원본 run·issued receipt 누락, receipt·manifest 변조 4종 거부 유지 |
| 최종 보존 | `VERIFY-08.json`의 전체 대조와 최종 checkpoint 참조 |

모든 실제 실행 worker는 네트워크와 원래 프로젝트·다른 worktree·공유 cache
쓰기를 OS sandbox로 차단했다. 수정 소스 검사는 원래 scripts/precore 읽기도
막아 fallback을 방지했다. H+F2는 기존 query vector/cache를 재사용하고 torch
모듈 읽기를 차단했다. 새 모델 추론·Gemini·이미지 요청·새 의미 판정은 없다.

설치 커널 배열 대조는 원본 적용 전 검증이다. 원본 적용 후에는 같은 설치/세대
binding과 원문을 유지한 상태에서 일반 CLI 결과와 전체 순서/점수 digest를 다시
확인했다. 같은 배열 검사를 다시 실행했다고 보고하지 않는다.

수정 소스 회귀와 설치 커널 검사를 구분했다. 봉인된 설치본의 성공만으로
제거한 작업 소스도 검증됐다고 주장하지 않는다. 적용 후에는 원래 bytecode 읽기를
차단한 actual source smoke도 수행했다(`APPLIED-SOURCE-SMOKE.json`). 검증한 소스와
실제 적용 소스가 정확히 같아 118개 회귀를 다시 실행하지 않았다.

archive 재현은 원래 작업 scripts/precore 읽기를 차단한 상태에서 통과했다.
원래 봉인 감사도 현재 코드로의 읽기 fallback을 차단했다. 따라서 원본 적용 후
바뀐 네 파일을 과거 코드처럼 사용해 성공시킨 검사가 아니다.

native 공개 조회 검사는 기존 issued native pack을 보존한 채 H binding만 제거한
private 파생 workflow를 사용했다. 이는 공개 native branch 대조이며 원래 native
역사 실행을 여러 건 추가로 재현했다는 뜻은 아니다. 실제 과거 run 감사 범위는
위의 기존 설치 run 1건이다. 모든 과거 실행이나 이미지 품질을 전수 검증하지 않았다.

## 보존한 항목과 남은 범위

- H 세대 `663038595155d8d48bfa20339bbe7a5c3128eea4ce504900c9a8fdadd34c152b`,
  native 세대 `9649504ffbcd1ebe7d9aedf9eab821fc18aa0300a8f70b65dbdd145b435ec1da`,
  설치 코드 집합 hash `493f1830db1f564c8acfe0218a24c8445990aa3ec968b948e80d187cfa9f7f90`를 유지했다.
- 원래 CURRENT 168개와 설치 선택·모델 lock·원래 store/run·receipt·판정·벡터를 유지했다.
  새 generation 발행·설치·활성화는 없다.
- main의 원래 변경/미추적 40,499경로와 다른 worktree 6,161경로를 보존했다.
  기존 staged 내용과 다른 worktree의 HEAD/index도 같다. main HEAD는 이번 단계별
  커밋만 진행했다. `prompt_generator.py`, `audit_composed_prompt.py`의 기존 작업은 그대로다.
- bytecode 21개·root shard 5세대·역사 store/복구 자료는 정리하지 않았다.
  원래 store가 없는 기존 41건과 대체 manifest 7개는 계속 보존하며 재현 성공에 세지 않았다.
- 이전 분석의 나머지 함수 15개는 범위 밖이다. 미커밋 파일 안의 14개와 과거 수동
  검증 계약이 있는 `validate_visual_profile_source`는 그대로 남겼다.
- 작업 소스 77개와 원래 CURRENT 세대 74개 사이의 기존 차이를 해결하거나,
  변경된 작업 소스로 원래 세대를 읽도록 지문 검사를 약화하지 않았다.

원본 보호 목록에서 수정 예외는 네 파일의 승인된 hash와 동일한 결과뿐이다.
그 밖의 내용·권한·inode·링크, 원래 Git 상태와 pointer inventory는 정확히 비교했다.
`AFTER-DELTA.json.gz`는 원래 baseline을 수정하지 않고 승인된 네 파일의 새 stamp만
덧붙여 후속 점검에서 사용할 수 있게 한다. 기존 분석 자료도 함께 커밋하지 않고 보존했다.

## 검사 도구 보완 기록

기능 회귀와 하네스 오류를 구분하고 원래 실패 자료를 남겼다.

- 3단계 대조군의 `/var`와 `/private/var` 표기 차이는 비교 root를 resolve하여 고쳤다.
  수정 후 6경우를 다시 검사했다(`SMOKE-HARNESS-03.json`).
- unified patch의 공백 문맥 행은 유효한 patch bytes다. Git whitespace 검사에
  source처럼 집계되어 commit이 중단되어, 원문을 바꾸지 않고 gzip 보관으로 전환했다.
  이번에 stage했던 경로만 unstage한 뒤 재검사·커밋했다(`PATCH-STORAGE.json`).
- 초기 private 복사본의 `precore/creative_controls.json` 등 비Python 메타데이터
  누락으로 두 suite가 테스트 로딩 전에 중단됐다. 원래 메타데이터만 복사했고
  테스트/운영 코드를 수정하지 않았다(`FIXTURE-METADATA-04.json`).
- native 테스트는 자체 기록을 stdout에 출력한다. 실행 중인 집계기는 전체 stdout을
  한 JSON으로 읽어 최종 요약 파싱을 실패했지만 worker는 exit 0, 70개/skip 0이었다.
  원시 `SOURCE-native-final.json`을 보존하고 마지막 요약·unittest 로그·네 모듈
  path/hash를 독립 확인한 `SOURCE-native-qualified.json`으로 판정했다. 테스트 결과를
  바꾸거나 긴 suite를 다시 실행하지 않았다. 집계기는 마지막 요약을 읽도록 수정했다.

초기 하네스 자료의 FAIL을 성공한 기능 검사로 세지 않았다. 최종 통과와 실제
적용 여부는 STAGE01–08, APPLICATION 및 최종 보호 검사로 확인한다.

## 복원과 재현

원래 네 파일은 시작 commit `6bb941d60e39baac288de085c1e31d2919cb3e85`와 함수별
원문 hash로 식별할 수 있다. patch gzip을 풀면 SHA가 고정된 원문 patch이며 역적용은
private 복사본에서 검증했다. 나중에 되돌릴 때는 현재 bytes와 patch 역적용 가능성을
먼저 확인하고 이번 patch만 되돌린다. 전체 파일 checkout/reset으로 이후 작업을 덮지 않는다.

PRIVATE-PROJECTS 및 progress 자료의 임시 경로는 실행 당시 scratch다. 원본 복구에
필요한 유일한 자료로 취급하지 않는다. 전체 unittest 로그는 최종 JSON에 보존했다.
완료된 freeze/apply 명령을 그대로 반복하지 않는다. 새로운 검증이 필요하면 새
임시 환경을 준비하고 원본/후보 hash 및 기존 검증 도구를 명시적으로 사용한다.
