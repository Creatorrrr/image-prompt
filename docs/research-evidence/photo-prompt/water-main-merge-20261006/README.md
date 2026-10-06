# 물 데이터 main 병합 — 2026-10-06

로컬 main `199670d3`의 두 커밋과 원격 main `c5588d4f`의 11개 커밋을 함께 보존한 병합이다. 원격의 원본 등록 구조 정리, 사진 장면·프롬프트 예산 보강, CT073 소유 대상 수정, 색상 설명 보강, 검색 캐시·runtime 세대 관리와 로컬의 제어 정책 변경을 유지했다. 독립 작업 트리에서 병합했고 기존 작업 폴더의 다른 미완료 변경은 출판 범위에 넣지 않았다.

물 후보와 시각 의미 프로필은 각각 117개를 검증한 원본 그대로 추가했다. 원격 main의 기존 원본 JSON은 모두 보존했다. 등록 매니페스트의 기존 88개 행도 유지하고 물 파일 두 개를 각 종류의 끝에 추가했다. 로컬의 미완료 지적 이미지 확장을 포함하지 않아 등록 순서는 후보 53, 시각 프로필 35로 맞췄다. [원본 병합 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/AUTHORED-MERGE.json)에 두 파일의 SHA와 조정 이유가 있다.

합쳐진 원본에서 의미 인덱스 10,241개와 시각 프로필 인덱스 2,038개를 재생성했다. 양쪽에서 제공된 실제 벡터 중 ID·전체 입력 텍스트·제공자·모델·차원이 같은 것만 재사용하여 새 임베딩 호출은 없었다. 이전 shard 세대도 삭제하지 않았다. 이 수치는 출판하는 깨끗한 main의 수치이며, 미완료 확장이 들어 있는 기존 작업 폴더나 최초 물 렌더 snapshot의 수치와 구분한다. [재생성 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/INDEX-REBUILD.json)과 [runtime 등록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/runtime-publication.log)을 보존했다.

| 검증 | 결과 |
|---|---|
| 물·후보 계약·시각 검색·등록·제어·runtime 검사 | 125개, 유지보수 참조 계보 검사 1개를 수정 후 재검증 |
| V24–V28 및 새 V30의 과거 경계 검사 | 86개, 과거 인덱스를 사용하는 테스트 설정을 수정 후 해당 7개 재검증 |
| V29 원래 코드·후보팩·receipt 재현 | 6개 통과 |
| 창작 core와 V6 호출·재시도 계약 | 25개 통과 |
| 중복을 제거한 관련 검사 | **242개 모두 통과** |
| 사전·깊은 시각 인덱스 검사 | 통과 |

원래 실패한 로그도 남겼다. [최종 결과와 검사 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/VALIDATION.json), [125개 최초 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/focused-tests.log), [86개 최초 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/history-tests.log), [수정한 21개 검사 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/history-repair-tests.log), [core 검사 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/core-merge-tests.log)를 함께 확인할 수 있다. 전체 테스트 실행을 수행하거나 전체 통과로 보고하지 않았다.

V1–V29의 원본과 후보팩을 수정하지 않고 V30을 추가했다. 원격 V29의 원래 소스·의존성 1,253개는 Git blob, SHA-256, 크기와 모드로 고정했다. 변한 파일은 별도 원본 보존 경로에서 복원한다. V29 receipt는 원래 구현을 사용하는 새 Python 프로세스에서 검증한다. 현재 코드에 과거 코드를 혼합해 읽거나 임의의 최신 데이터로 재해석하지 않는다. [V29 원본 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/V29-PARENT-SOURCE.json), [V30 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/V30-WATER-MAIN-PROOF.json), [후보팩 차이 22개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-main-merge-20261006/PACK-DELTA.json)를 고정했다.

V30의 고정 장면·제어·신체 사전검토·프롬프트 예산·부정문은 유지된다. 후보 64개 중 선택적 질감 후보 한 개가 수증기 안개에서 연결된 표면 거품으로 바뀌었고, 나머지 후보 객체와 순서는 그대로다. 나머지 차이는 새 원본에 따른 검색·후보 수·해시와 로컬 제어 정책의 선언된 두 불리언이다. 이 차이 외의 후보 의미·순서·소유 대상·본문·예산·부정문 변경은 새 변조 검사에서 거부한다.

앞선 물 이미지 세 사례는 [원래 렌더 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/REPORT.md)의 데이터 세대에 계속 연결된다. 이번 병합에서 이미지 생성은 추가로 호출하지 않았다. 물 프로필 원본을 그대로 보존했다는 확인과 이번 main의 코드·데이터·runtime 검증을 기록했고, 이를 병합 후 새 이미지 검증이나 요청자 수용으로 확대하지 않았다.

원격 푸시와 로컬 main 동기화의 최종 상태는 같은 폴더의 `PUSH-VERIFICATION.json`, `PRIMARY-SYNC.json`, `PRIMARY-FINAL-VERIFICATION.json`에 기록한다. 기존 미완료 원본은 SHA로 보존하며 기존 작업 폴더에서 필요한 두 파생 인덱스만 해당 작업 원본에 맞게 재생성한다. 깨끗한 V30 main의 검증과 미완료 변경을 포함한 작업 폴더의 runtime 상태는 각각 기록한다.
