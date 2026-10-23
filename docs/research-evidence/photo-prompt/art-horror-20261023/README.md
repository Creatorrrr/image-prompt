# Art Horror 리서치와 데이터 반영 계획

2026-10-23. 원 대화 전체를 크롬으로 확인하고 **용어 154개·영화 12편·미술/퍼포먼스 사례 7개·조합 6개**를 대조했다. 시각적 의미를 소유자·매체·관계·혼동 경계로 풀고, 문맥/시간/음향과 구별한 연구 결과다.

먼저 [RESEARCH.md](RESEARCH.md), 이어서 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 읽으면 된다.

|자료|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|주요 개념 구별·8개 보강 영역·성적/폭력적 용어 보존·증거 한계|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|중복 판정 → 원문/역할 검토 → index/설치 → 검색/회귀 → 이미지 평가|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|154개 원 대화 용어의 카드 연결. advisory only|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|시각 64·문맥 29개, 한영·소유자·방향 관계·206개 미실행 gate|
|[candidate-drafts.json](candidate-drafts.json)|시각 카드의 한영 초안 64개. 운영 모듈이 아니며 카드 수와 중복 합산하지 않음|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|후보 20,341개 지정 필드 검사·기존 CID 15개와의 차이·149슬롯 연결 검토|
|[existing-source-snapshots.json](existing-source-snapshots.json) / [slot-mapping.json](slot-mapping.json)|실제 원문·binding·해시·재사용 검토 대상과 슬롯 대안|
|[REFERENCE-MAPPING.md](REFERENCE-MAPPING.md)|영화 12편·미술 사례 7개·원 대화 조합 6개의 반영과 비가시성|
|[SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json)|출처 47개의 실제 열람 범위·지원 의미·한계. 원전 47권 완독이 아님|
|[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) / [evaluation-cases.json](evaluation-cases.json)|113개 미실행 명세: 개발 probe 64·경계 통제 20·문맥 probe 29|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|첫 8장면군의 A/B 비교 제안·선택과 픽셀/미적 판단의 구분|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md) / [browser-supplement.json](browser-supplement.json)|20,000자 제한을 크롬으로 복원한 기록·접근 실패·원전 공백|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|연구 자료의 참조·graph·수량·hash와 동시 source 변경 관찰|

**현재 상태:** 연구와 반영 계획 작성. 운영 source 등록·index 생성/게시·임베딩·검색 실행·native 승인·이미지 생성·픽셀 평가·설치/활성화·commit/push는 수행하지 않았다. 검증 결과가 PASS여도 그 의미는 연구 자료의 구조적 무결성에 한정된다.

재생성과 검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/art-horror-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/art-horror-20261023/validate_research.py
```

현재 source를 새로 관찰하려면 `audit_corpus.py`를 실행한다. 이는 현재 원문을 읽고 이 연구 폴더의 스냅샷을 다시 쓰므로 이후 반영 전후 비교에서는 이전 증거를 먼저 보존해야 한다. 세 스크립트는 운영 assets·런타임·기존 연구 자료를 수정하지 않는다. 연구용 파일은 runtime에서 import/등록하지 않는다.
