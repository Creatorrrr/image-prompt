# 캐릭터 헤어 연구 자료

기준일: 2026-10-08. 연구·반영 설계 자료이며 runtime 로더에 등록하지 않았다.

읽는 시작점은 [통합 보고서](/Users/chasoik/Projects/image-prompt/docs/researches/2026-10-08-character-hair-visual-semantics.md)다.

| 자료 | 내용 |
|---|---|
| `reference/keyword-inventory.tsv`, `SOURCE-RECEIPT.json` | 원본 UI의 H001–H454 전사와 provenance. 원본 파일 bytes와는 구분 |
| `CURRENT-DATA-AUDIT.json`, `KEYWORD-CROSSWALK.json/tsv` | 전체 등록 authored source의 raw 현황과 제한된 문자열 대조 |
| `SEMANTIC-MODEL.md` | 관찰 축·소유자·방향 관계·중의성과 검증 경계 |
| `specialist-cuts.md`, `cuts-cards.json`, `cuts-sources.json` | 커트·앞머리·가르마·페이드 |
| `cuts-supplement.md`, `cuts-supplement-cards.json`, `cuts-supplement-sources.json` | 쇼트컷·투블럭·보브 보완 |
| `specialist-topology.md`, `topology-cards.json`, `topology-sources.json` | 묶음·땋기·컬·밀도·부피 |
| `specialist-color-state.md`, `color-state-cards.json`, `color-state-sources.json` | 색·표면·사건 원인·플랫폼 정의 |
| `main-cards.json`, `main-sources.json`, `ACCESSORY-DISPOSITION.json` | 재료 충돌·헤어라인·장식 접합·문화 구조 |
| `RESEARCH-CROSSWALK.json`, `SOURCE-CATALOG.json` | 전체 키워드→연구 경로와 출처의 주장·접근 범위 |
| `CANDIDATE-DRAFTS.json` | 32개 runtime-shaped 후보 review 초안; wrapper는 runtime schema가 아님 |
| `PROFILE-AND-BUNDLE-PLAN.json` | 16개 의미 계열의 재사용·새 구조·관계 의무 설계 |
| `VALIDATION-CASES.jsonl` | 실행 전 최소 대조와 경계 검증 설계 |
| `INTEGRATION-PLAN.md` | source authoring→index→조회/선택→픽셀 채택 계획 |
| `ASSEMBLY-SUMMARY.json`, `RESEARCH-VALIDATION.json` | 집계와 연구 파일 참조·원본 매핑·보존 검사 |

재현 helper는 `audit_keyword_coverage.py`, `build_main_research.py`, `assemble_research.py`, `validate_research.py`다. 모든 output은 이 연구 폴더에 한정한다. 기존 런타임·인덱스·tests를 쓰지 않는다. 입력 source가 바뀌면 집계도 달라지므로 각 receipt의 시점을 확인한다.
