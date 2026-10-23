# 의학물·메디컬물 시각 의미·후보 데이터 연구

2026-10-23 KST. [참조 대화](https://chatgpt.com/c/6adb5b1d-dee8-83e8-8152-98a2c2ed957c)를 Chrome에서 끝까지 읽고, 전체 용어 346개와 장면 조합 8개를 기반으로 연구했다. **[리서치 본문](RESEARCH.md)**과 **[반영 계획](IMPLEMENTATION-PLAN.md)**부터 읽으면 된다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|장르·직급·진료·체위·장비·복장·외형·정신의학·성/생식·성인 연출·법의학·돌봄의 주요 발견|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|재사용/신규/수정/문맥/보류, P0–P2 순서, 예상 파일, 검색·native·픽셀·설치·복구 기준|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|346개 원문 행 전체의 문맥·선택적 시각 후보·보류 연결|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|신규 100 + 기존 재사용 제안 22 + 문맥 42 + 보류 8 = 172개 연구 카드|
|[candidate-drafts.json](candidate-drafts.json)|선택적 한영 시각 후보 122개. 소유·관계·전체 문장·주장 한계를 가진 운영 비활성 초안|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|현재 manifest 코퍼스와 어휘·실제 의미·정본 소유자의 차이|
|[corpus-snapshot.json](corpus-snapshot.json) / [existing-source-mapping.json](existing-source-mapping.json)|95개 모듈 해시·지정 필드 검사·22개 정본의 full record와 모든 binding|
|[SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)|원 대화의 8개 조합을 장면의 관계와 비가시 문맥으로 전개|
|[SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json)|참조 대화 1개와 외부 49개 출처의 접근 범위·확인한 내용·한계|
|[VISUAL-REFERENCE-REVIEW.md](VISUAL-REFERENCE-REVIEW.md)|직접 픽셀을 본 체위 도판 3개와 관찰 한계|
|[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) / [evaluation-cases.json](evaluation-cases.json)|경계 48·일반 12, 한영 질의 120개. 모두 NOT_RUN, 독립 holdout 아님|
|[PIXEL-PLAN.md](PIXEL-PLAN.md) / [pixel-cases.json](pixel-cases.json)|16개 검증군과 첫 12장 비교 제안. 이미지 호출 0회|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md)|원문·본문·검색 노출·도판 관찰·접근 실패와 각 검증 단계의 구별|
|[BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json)|시작 상태·보호 파일 해시·무결성 검사와 정본 변화 기록|
|[SUMMARY.json](SUMMARY.json) / [SHA256SUMS](SHA256SUMS)|실제 수량과 연구 폴더 파일 무결성|

연구 문서와 초안의 작성 범위는 이 폴더다. 운영 소스 등록·인덱스 재구축·설치/활성화·임베딩·이미지 생성·commit/push는 수행하지 않았다. 읽기 전용 installed recorder 검사만 별도로 수행했다. 구조 검사 PASS는 임상적 정확성 전체·실제 검색·native 자격·픽셀 성공·미적 개선·사용자 수락의 PASS가 아니다.

재생성과 연구 무결성 확인:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-drama-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-drama-20261023/research_evaluation.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-drama-20261023/validate_research.py
```

build는 저장된 연구 입력에서 이 폴더의 파생 자료만 쓴다. validator는 보호 파일의 현재 SHA와 baseline을 비교해 외부 변화를 별도로 보고하며 reset/revert하지 않는다. 후속 구현 전에 코퍼스와 selected runtime을 다시 기준화한다.


## 2026-10-23 데이터 반영 및 독립 이미지 테스트

연구 단계의 원본과 당시 검증 결과는 그대로 보존합니다. 후속 반영 상태와
독립 생성 결과는 `INTEGRATION-RESULTS.md`, `integration-evidence/`,
`image-test-evidence/`에서 별도로 기록합니다. 연구 시점의 `NOT_RUN`이나
`native_approval: false`를 생성 성공으로 소급 변경하지 않습니다.
