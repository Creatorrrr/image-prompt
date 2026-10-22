# 아톰펑크 리서치 패키지

2026-10-23. [RESEARCH.md](RESEARCH.md)에서 조사 결과를, [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에서 반영 순서를 읽을 수 있다. 연구용 산출물이며 운영 source·검색·설치에는 등록되지 않았다.

| 파일 | 내용 |
|---|---|
| [REFERENCE-COVERAGE.md](REFERENCE-COVERAGE.md) | 원 대화 191개 용어·작품 9개·조합 9개·검색 묶음 6개의 범위 대조 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) | 191개 항목의 경로·카드·주장 한계 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 101개 상세 카드와 소유·방향·검토 gate 제안 |
| [candidate-drafts.json](candidate-drafts.json) | 88개 연구용 구조 초안, runtime_importable=false |
| [REALIZATIONS.tsv](REALIZATIONS.tsv) | 한영 장면 예시 18개; 88개 초안과 중첩 |
| [SOURCES.tsv](SOURCES.tsv) / [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 53개 출처 항목과 실제 접근 범위·한계 |
| [EXISTING-DECISIONS.tsv](EXISTING-DECISIONS.tsv) / [existing-source-mapping.json](existing-source-mapping.json) | 기존 23레코드의 통합 triage 제안·전체 source/binding·해시 |
| [CORPUS-SNAPSHOT.json](CORPUS-SNAPSHOT.json) / [LEXICAL-AUDIT.json](LEXICAL-AUDIT.json) | 조사 시점 75모듈·20,054레코드·14,687binding 및 고정 필드 진단 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 60개 사례·120개 한영 질의, 모두 NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 36장·선택 확장 18장의 3 arms 비교 제안, NOT_RUN |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) | 시작 상태·기존 파일 대조·연구 구조 검증 |
| [SHA256SUMS](SHA256SUMS) | 연구 패키지 파일 체크섬 |

재생성·검증:

```sh
python3 docs/research-evidence/photo-prompt/atompunk-20261023/build_research.py
python3 docs/research-evidence/photo-prompt/atompunk-20261023/validate_research.py
```

두 스크립트는 이 연구 폴더에만 쓴다. builder는 현재 source/catalog를 읽으므로, 최초 snapshot 이후 corpus가 달라졌으면 덮어쓰지 않고 멈춘다. 후속 구현/재조사는 연구 snapshot을 보존한 뒤 successor 기준을 작성해야 한다. validator는 source/기존 파일 drift를 별도로 보고하며 원본 작업을 복구하지 않는다.

연구 구조 검증은 실제 의미·검색·이미지·native qualification·설치·사용자 수용의 검증을 대신하지 않는다. [PACKAGE-SUMMARY.json](PACKAGE-SUMMARY.json)에 수량과 근거 경계가 있다.
