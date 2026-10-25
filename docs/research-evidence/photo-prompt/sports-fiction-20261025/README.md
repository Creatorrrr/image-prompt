# 스포츠물 시각 의미·후보 리서치

2026-10-25. 사용자 지정 대화를 Chrome에서 끝까지 복구한 뒤, 공식 종목 자료·코칭 자료·복장 규정·연구·비평을 대조해 작성했다. **리서치·초안·반영 계획만 작성했으며 운영 데이터와 이미지 검증은 미실행이다.**

먼저 [리서치 결과](RESEARCH.md), 이어서 [반영 계획](INTEGRATION-PLAN.md)을 읽으면 된다.

| 내용 | 파일 |
|---|---|
| 원문 330행의 반영 경로 | [KEYWORD-COVERAGE.md](KEYWORD-COVERAGE.md), [keyword-routes.json](keyword-routes.json) |
| 102개 시각 의미 카드·306개 관찰 요소 | [CARD-CATALOG.md](CARD-CATALOG.md), [semantic-cards.json](semantic-cards.json) |
| 종목별 복합 행에서 분해한 70개 기술 | [technique-atoms.json](technique-atoms.json) |
| 102개 후보·204개 선택형 바인딩 초안 | [candidate-drafts.json](candidate-drafts.json), [binding-drafts.json](binding-drafts.json) |
| 39개 출처의 지원 범위·판본·접근 상태 | [sources.json](sources.json), [web-access-log.json](web-access-log.json) |
| 기존 후보 재사용·보완·문맥 분리 판단 | [reuse-decisions.json](reuse-decisions.json), [reuse-inventory.json](reuse-inventory.json) |
| 후속 조사가 필요한 69행 | [followup-worklist.json](followup-worklist.json) |
| 설계한 회귀 64개·독립 픽셀 장면 12개 | [regression-cases.json](regression-cases.json), [pixel-evaluation-plan.json](pixel-evaluation-plan.json) |
| 원문 증거 | [conversation.browser.txt](conversation.browser.txt), [conversation-tables.json](conversation-tables.json), [conversation.accessibility.txt](conversation.accessibility.txt) |
| 로컬 구조·참조 검사 | [research-integrity.json](research-integrity.json) |

원문 330행 중 150행은 문맥·정의 중심, 20행은 문맥과 선택 실현, 79행은 시각 카드 연결, 69행은 표적 후속 조사, 12행은 창작 조합으로 분류했다. 후보 카드가 있다는 사실만으로 원문의 모든 정의나 전문 동작이 검증된 것은 아니다. 출처·형태 검토가 남은 항목을 상태에 보존했다.

재생성 순서는 `build_research.py`, `build_review_assets.py`다. 사람이 읽는 Markdown은 연구 결과의 검토용 뷰이며 운영 입력이 아니다. `verify_research.py`는 이 폴더의 구조·참조와 원문 보존을 확인하며, 실제 검색·팩·픽셀 테스트를 실행하지 않는다.
