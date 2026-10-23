# 군대물·밀리터리물 연구 패키지

2026-10-24 KST. 참조: [군대물 용어 조사](https://chatgpt.com/c/6adb70a2-a2f8-83ec-ac21-6ec6a88f3c9d).

도구 응답의 본문 잘림을 Chrome에서 보완하여 1~16절·전체 24개 표·393행을 확보했다. 최초 연구 단계에서는 시각 의미·후보 강화의 연구와 반영 계획만 작성했다. 당시 운영 사전·manifest·설치된 검색 변경과 이미지·embedding 호출은 없었다. 이후 사용자의 추가 요청으로 운영 데이터 반영과 독립된 세 이미지 테스트를 진행했으며, 최종 범위와 결과는 [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md)에 기록한다. 통합시험 종료 시에는 commit·push를 수행하지 않았다. 후속 발행 상태는 [PUBLISHING.md](PUBLISHING.md)에 기록한다.

| 읽을 자료 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 핵심 조사 결과·근거·혼동 지점·기존 데이터 문제 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 우선순위·재사용/보완/신규 기준·운영 반영·검증·복구 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) | 원문 393행의 전체 대응표 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) | 한영 완결 시각 대안 104개와 관계·화면 확인점 |
| [CONTEXT-DISTINCTIONS.md](CONTEXT-DISTINCTIONS.md) | 제도·임무·법·진단·동의·비평·시간·소리 등 52개 구분 |
| [SOURCES.md](SOURCES.md) | 40개 출처의 확인 범위와 미확인·접근 제한 |
| [EVALUATION-PLAN.md](EVALUATION-PLAN.md) | 개발용 24사례/한영 48질의, 전체 256질의, 이미지 12쌍 제안 |
| [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md) | 운영 시각 의미·후보 반영, 설치 검증, 독립된 세 이미지 테스트의 실제 결과 |

기계 판독용 자료: `keyword-atlas.json`, `semantic-cards.json`, `context-distinctions.json`, `sources.json`, `evaluation-cases.json`, `evaluation-queries.json`. 이 원본 자료는 연구용이며 runtime import·native approval을 부여하지 않는다. 운영 반영은 별도 후보·binding·시각 의미 모듈과 검증된 설치 세대로 구분한다.

기존 corpus 감사는 authored 후보 21,883개·binding 16,698개를 대상으로 지정 어휘를 검색했다. 인접 후보 47개의 전체 원문·조건·효과·binding snapshot과 module hash를 보존했다. 이 감사는 의미 검색 성능이나 신규 데이터의 필요성을 자동 증명하지 않는다.

정확한 건수는 [research-counts.json](research-counts.json), 검증 범위와 결과는 [validation.json](validation.json), 입력·도구 확인 경위는 [provenance.json](provenance.json)에 기록한다. 특정 군복·장비 도판, 한국군 현행 복제, 일부 비평·절차어 정의는 후속 확인 대상이다.

원 연구의 checksum은 최초 연구 스냅샷용이다. 운영 반영과 세 이미지 테스트 이후의 현재 근거는 [INTEGRATION-RESULTS.json](INTEGRATION-RESULTS.json)과 [원래 단계 체크섬](INTEGRATION-SHA256SUMS.original.txt)로 구분한다.
