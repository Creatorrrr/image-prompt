# 퇴폐미·가정 스릴러·스플래터 리서치

2026-10-22. **호사스러운 표면·접근권·신체 경계의 소유 관계**를 중심으로 현재 시각 의미와 후보 데이터의 보강 방향을 조사했다.

먼저 [RESEARCH.md](RESEARCH.md), 이어서 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 읽으면 된다.

|자료|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|주요 문헌의 구분·아홉 데이터 영역·현재 원문 진단·반영 판단|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|참조의 17개 표·189행: 축3·용어170·창작 조합명8·참고 작품8|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|108개 카드: 가시 86·문맥 22, 소유자·방향 관계·혼동·주장 한계·252개 gate|
|[candidate-drafts.json](candidate-drafts.json)|가시 카드에서 만든 한영 초안 86개. 위 카드와 합산하지 않음|
|[SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json)|61개 출처 URL·읽은 범위·지원하는 의미와 한계|
|[REFERENCE-EXTENSIONS.md](REFERENCE-EXTENSIONS.md)|추가 서사·명암·음향·성유물함, 창작 조합명8·참고 작품8의 데이터 반영 대조|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md)|원 대화 20,000자 제한·초록/출판사 설명·검색 본문만 읽은 범위·직접 접근 실패|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|후보 19,275개 지정 본문 필드 검사·구체적 재사용/정제 제안|
|[existing-source-mapping.json](existing-source-mapping.json)|선택 CID 28개의 전체 원문·조건·효과·binding·hash 스냅샷. 자격 승인 아님|
|[SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)|이번에 저술한 12개 장면 제안. 원 대화의 잘린 조합명을 복원한 것이 아님|
|[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)|개발36·경계26·일반12·비가시14=88사례/한영176질의, 모두 NOT_RUN|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|첫 12장면군×3 arm=36장 비교 제안, NOT_RUN|
|[BASELINE.json](BASELINE.json)|시작 HEAD·기존 dirty 상태·추적 파일 6,139개 hash|
|[RUNTIME-OBSERVATION.json](RUNTIME-OBSERVATION.json)|기존 installed 의존성/recorder의 읽기 전용 관찰. 새 데이터의 실행 증거 아님|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|자체 자료 무결성·참조·graph·질의·hash·현재 원본 drift 관찰|

연결 도구에서 잘렸던 뒷부분은 브라우저의 렌더링 본문/표 셀로 복원했다. [보완 기록](REFERENCE-BROWSER-SUPPLEMENT.json)에 출처·표 수·추가 명칭과 설명 요약을 보존했다. 출처 61개는 원전 61권 완독이 아니며 189행의 개별 정의/작품 분석을 모두 독립 검증한 것도 아니다. 정확한 열람 범위는 source ledger를 따른다.

이번 연구에서는 운영 source 등록·인덱스 생성/게시·검색·임베딩·이미지 생성·픽셀 평가·설치/활성화·사용자 수용·commit/push를 수행하지 않았다. 연구 무결성 검증과 운영 품질 증거는 분리한다. 기존 source·dirty 변경·설치 상태를 보존했다. 동시 작업이 원본을 바꿨는지는 VALIDATION의 drift 항목을 따른다.

재생성·검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/validate_research.py
```

두 명령은 이 연구 폴더의 파생 문서/JSON/TSV와 검증 파일만 쓴다. `audit_corpus.py`는 현재 source를 다시 읽어 스냅샷 증거를 새로 쓰므로 구현 후에는 별도 evidence 디렉터리에서 새 관찰을 보존해야 한다. 연구 파일은 runtime에서 import/등록하지 않는다.
