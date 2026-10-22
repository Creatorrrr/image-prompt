# 메타픽션·실존공포·LitRPG 리서치 패키지

2026-10-22 KST. 참조 대화의 130개 용어 전체를 복원하고 외부 자료와 현재 저장소 원문을 대조해, 시각 의미·후보 데이터의 보강안과 반영 계획을 작성했다.

먼저 [리서치 본문](RESEARCH.md), 다음으로 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

| 산출물 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 정의·시각화·서사/철학적 주장 한계·작품별 참고 범위 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 재사용/정밀화/새 관계/문맥/보류 심사 → 소스 → 별도 인덱스 → 실제 검색 → 이미지 비교 → 설치·복구 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 용어 130개 전부의 경로와 원 정의, 창작명 14개의 지위 보존 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 가시 제안 64개 + 문맥 10개. 소유자·관계·혼동·주장 한계·성분·관계별 검토 항목 |
| [candidate-drafts.json](candidate-drafts.json) | 한영 후보 초안 64개, 현재 36개 슬롯에 대한 역할 참고. native CID/RID/승인 없음 |
| [adoption-ledger.json](adoption-ledger.json) | 카드 74개 전체의 잠정 반영 경로와 기존 CID 연결 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 기존 데이터의 오탐·재사용·추가 관계를 구체적으로 비교 |
| [reviewed-neighbors.json](reviewed-neighbors.json) | 기존 소스 17개 지정 필드 심사, 전체 레코드·조건·효과·바인딩 스냅샷과 해시 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) / [existing-source-mapping.json](existing-source-mapping.json) | 첫 시점 19,471개 레코드의 제한 어휘 감사와 40개 진단 표본. 실제 검색 순위가 아님 |
| [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md) | 원 대화 조합 방향 6개와 새 제안 2개, 창작명 14개의 장면 연결 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 외부 출처 40개와 실제 읽은 범위·주장 한계 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 64·경계 32·일반 16·비가시 12 = 124사례/248개 한영 질의. 모두 NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 핵심 12개 × 3 arms = 첫 36개 결과 비교 계획. NOT_RUN |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 원 대화 복원, 원전/소개문/PDF 접근 범위, 실패와 남은 검증 |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 시작 상태·무결성 검사·동시 변경 관찰·연구 파일 해시 |

64개 후보 초안은 74개 카드 가운데 가시 제안 부분이므로 두 수를 합산하지 않는다. 이 폴더는 운영 loader 입력이 아니며 운영 후보·의미 레지스트리·인덱스·활성 pointer에 등록하지 않았다. 외부 모델/임베딩/이미지 호출, 검색 성능 측정, native 픽셀 검토, 커밋·푸시는 수행하지 않았다. 공공 웹 검색과 자료 읽기는 수행했다.

재생성·무결성 확인:

```sh
python3 docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/validate_research.py
```

`build_research.py`는 이 폴더의 구조화 초안과 파생 문서를 생성하고 현재 slot catalog를 읽는다. `validate_research.py`는 이 폴더에 검사 결과·해시를 쓰고 운영 파일은 읽기만 한다. 둘 다 이미지/임베딩/인덱스 빌드/게시를 수행하지 않는다.

`audit_corpus.py`는 소스를 다시 읽고 이 폴더의 감사 증거를 갱신한다. 옛 비교 근거를 보존하려면 재실행 전 기존 스냅샷을 별도로 보관해야 한다. 동시 변경이 관찰되면 실제 구현 직전에 baseline을 다시 고정한다. 연구 무결성 PASS는 운영 품질이나 사용자 수용의 PASS가 아니다.
