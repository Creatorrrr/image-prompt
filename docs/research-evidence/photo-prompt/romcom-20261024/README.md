# 러브코미디 시각 의미·후보 데이터 리서치

2026-10-24. 원 대화의 전체 범위를 복구하고 현재 저장소 source와 비교한 **조사·초안·반영 계획**이다. 운영 반영·검색 평가·이미지 생성은 수행하지 않았다.

먼저 [상세 리서치](RESEARCH.md), [반영 계획](IMPLEMENTATION-PLAN.md)을 읽는다.

|자료|내용|
|---|---|
|[전체 용어 지도](KEYWORD-ATLAS.md)|원 용어 317개·설명·문맥 경로·시각 카드·근거 수준|
|[시각·문맥 카드](VISUAL-CARDS.md)|시각 카드 99개, 문맥 경계 19개|
|[후보 초안](candidate-drafts.json)|99개 연구 대안; 운영 CID·binding·index 없음|
|[기존 source 비교](existing-source-decisions.json)|기존 CID 37건의 원문·조건·효과·binding과 판단|
|[출처](SOURCES.md)|외부 자료 26개와 원 대화; 주장별 지원 범위·한계|
|[현재 corpus 관찰](CORPUS-FINDINGS.md)|working-tree 기준, lexical audit의 범위와 보강 우선순위|
|[픽셀 계획](PIXEL-PLAN.md)|사진 12장면×baseline/stage 비교 설계; 미실행|
|[혼동 경계](boundary-cases.tsv)|46쌍의 양성/혼동 요청과 기대 구별|
|[검증 결과](VALIDATION.json)|연구 자료의 구조·참조·현재 source 해시 비교|

원문 보존 317개는 개별 용어의 독립 사전 검증 완료를 뜻하지 않는다. 특정 출처로 확인한 어휘 주장은 41개, 선택적/인접 시각 카드가 연결된 항목은 136개다. 나머지 문맥·용례·형태 확장 상태는 항목별로 남겼다. 출처는 어휘·맥락의 근거이며 연구자가 작성한 모든 기하의 보증이 아니다.

원 대화 도구 조회는 20,000자에서 잘렸고 Chrome 렌더링 본문 26,751자·23개 표를 복구했다. [reference-browser.json](reference-browser.json)에 전체 텍스트·표·보이는 출처 링크를 보존했다. [SOURCE-CAPTURE.md](SOURCE-CAPTURE.md)에 완전성 확인과 접근 실패의 대체 근거를 기록했다.

재현은 이 폴더의 `build_research.py`, `validate_research.py` 순서다. `audit_corpus.py`는 현재 source를 읽는 별도 기준 수집이며 이미 존재하는 snapshot을 덮어쓰지 않는다. 개발 질의 290개는 작성 데이터에 노출된 개발셋이며 독립 holdout이 아니다. 연구 validator는 원어 의미의 정확성·native qualification·검색·이미지를 승인하지 않는다.

실제 기록: [BUILD-SUMMARY.json](BUILD-SUMMARY.json), [corpus-snapshot.json](corpus-snapshot.json), [semantic-cards.json](semantic-cards.json), [keyword-routes.json](keyword-routes.json), [development-cases.json](development-cases.json). 커밋·push·운영 설치 선택 변경은 하지 않았다.
