# 메디컬 호러 시각 의미·후보 데이터 리서치

2026-10-22 KST. 참조 대화의 키워드를 바탕으로 조사 결과와 실제 데이터 반영 계획을 작성했다. [리서치 본문](RESEARCH.md)과 [반영 계획](IMPLEMENTATION-PLAN.md)을 먼저 읽으면 된다.

| 산출물 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 공간·기구·상처·의식·감염·이식·동의·성·생식·역사의 주요 발견과 보강 방향 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 재사용/수정/신규/문맥/보류, P0–P2 우선순위, 예상 파일, 검색·이미지·설치·롤백 기준 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 대화 181개 용어 전체 연결. 개별 임상 정의·native 승인 완료를 뜻하지 않음 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 가시 실현 64개와 문맥 경계 22개. 소유·관계·혼동·출처·주장 한계·가시 gate |
| [candidate-drafts.json](candidate-drafts.json) | 한영 후보 초안 64개. 운영 스키마·CID/RID·native proof가 아님 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 출처 51개와 실제 접근 범위·확인한 주장·한계 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 기존 전체 원문·조건·효과·binding의 재사용 가능성과 차이 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | 지정 필드의 어구 검사. 실제 hybrid 검색과 구별 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 후보의 full record·owner 파일·해시·binding 스냅샷 |
| [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md) | 원 대화의 일곱 조합을 가시 관계와 남는 문맥으로 전개 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 24·경계 20·일반 12·비가시 8, 64사례/128개 한영 질의. 전부 NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 초기 12사례×3 arms=36개 생성 비교 제안. 아직 미실행 |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 논문/책 초록·검색 본문·페이지 읽기의 차이와 미검증 영역 |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) | 시작 상태·보호 파일 해시와 연구 무결성·동시 소스 변화 기록 |

이번 작성 범위는 이 연구 폴더다. 운영 데이터 등록·검색 인덱스 갱신·설치/활성화·임베딩/이미지 호출·commit/push는 수행하지 않았다. 다른 작업에 의한 소스 변화가 있으므로 후속 구현 직전에 재기준화한다. 최신 수량은 [SUMMARY.json](SUMMARY.json), 검증 경계는 [VALIDATION.md](VALIDATION.md)를 확인한다.

연구 데이터 재생성과 무결성 확인:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-horror-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-horror-20261022/make_evaluation.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/medical-horror-20261022/validate_research.py
```

스크립트는 연구 폴더에만 기록한다. build는 당시 코퍼스를 다시 읽으므로 동시 작업 이후에는 기존 audit의 수량·해시가 달라질 수 있다. 단순한 파일 무결성 PASS는 출처의 모든 주장·운영 채택·검색·이미지·사용자 수락의 PASS가 아니다. `SHA256SUMS`는 이 폴더에서 `shasum -a 256 -c SHA256SUMS`로 확인한다.
