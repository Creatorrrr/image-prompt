# 키워드 기반 시각 의미·후보 데이터 강화 연구

작성일: 2026-10-10 KST. 원본 503개 표제어를 기반으로 125개 카드, 150개 후보 초안, 20개 조합 분석, 23개 문맥별 제외 경계를 만들었다. 공개 근거는 26건이다. 런타임 반영과 이미지 검증은 미실행이다.

- [상세 리서치](RESEARCH.md)
- [반영 순서·첫 16개 범위·완료 조건](IMPLEMENTATION-PLAN.md)
- [125개 카드 설명](CARD-CATALOG.md) / [JSON](SEMANTIC-CARDS.json)
- [150개 후보 초안](CANDIDATE-BLUEPRINTS.json)
- [503개 키워드의 현재 데이터 대조·반영 경로](KEYWORD-COVERAGE.json)
- [간단한 CSV](KEYWORD-RESEARCH-ROUTING.csv)
- [20개 선택 조합 분석](COMBINATION-ANALYSIS.json)
- [23개 출처 한정 제외 경계](CONTEXT-BOUNDARIES.json)
- [공개 근거와 읽은 범위](SOURCES.json)
- [48개 회귀 시나리오](REGRESSION-PLAN.json)
- [8개 이미지 비교 계획](NATIVE-VALIDATION-PLAN.json)
- [구조 검증·보존 확인](PACKAGE-VALIDATION.json)
- [파일 해시 목록](MANIFEST.json)

`inputs/`는 복구한 사전과 접근 근거이다. `web-evidence/`는 이번 공개 조사에서 채택한 짧은 사실·URL·접근 범위·근거 한계의 기록이며, 전체 기사나 긴 인용을 복제하지 않았다. 지시로 해석하지 않는다. `CURRENT-*`는 로컬 원본의 어휘 대조 근거이며 런타임 세대나 전체 의미 충족을 증명하지 않는다.

재현은 `audit_inventory.py → build_research.py → build_validation_plan.py → validate_package.py` 순서이다. 첫 도구는 실행 시점의 로컬 원본을 새로 읽어 현재 스냅샷을 교체하므로, 과거 증거 보존이 필요한 경우 이 패키지 복사본 또는 새 폴더에서 실행한다. 도구들은 이 연구 폴더에만 작성하며 런타임·임베딩·이미지 API를 호출하지 않는다.
