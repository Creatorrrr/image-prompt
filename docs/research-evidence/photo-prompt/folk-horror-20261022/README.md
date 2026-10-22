# 포크 호러 시각 의미·후보 데이터 리서치

2026-10-22. 참조 대화의 키워드로 심화 조사한 뒤, 후속 요청에 따라 운영 데이터 반영과 독립 3개 arm의 참조 이미지 생성 테스트까지 진행한 패키지다.

현재 결과는 [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md)와 [IMAGE-TEST-RESULTS.md](IMAGE-TEST-RESULTS.md)에서 확인한다. 신규 가시 후보 69개·진단 19개·optional binding 133개를 반영하고 기존 후보 1개를 재사용했다. 작업 검색 인덱스와 설치 H-F2 기본 세대를 갱신했다. 별도 native CURRENT와 기존 source·중립 저작 파일은 보존했다. commit/push는 수행하지 않았다.

아래 연구 문서와 초기 `VALIDATION.json`의 NOT_RUN은 첫 단계의 기록이다. 처음에는 이 폴더만 작성하고 운영 데이터·임베딩·이미지 호출 없이 계획을 세웠다. 당시 README 원본은 [스냅샷](integration-evidence/README.research-only.md.snapshot)에 보존했다. 후속 결과와 초기 계획을 합산해 36장 A/B/C 또는 모든 카드의 픽셀 테스트를 완료했다고 해석하지 않는다.

| 산출물 | 내용 |
|---|---|
| [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md) | 실제 반영 파일·수량·검색 104질의/208실행·대조 의미 검토·설치와 보존 경계 |
| [IMAGE-TEST-RESULTS.md](IMAGE-TEST-RESULTS.md) | 독립 3개 컨셉·프롬프트·원본 이미지·source별 가시 판정 |
| [integration-evidence](integration-evidence/) | source 보존·인덱스·설치·실제 질의/순위·대조 판정·최종 무결성 증거 |
| [RESEARCH.md](RESEARCH.md) | 주요 발견, 형태·관계·문화·역사·비가시 의미 구분과 보강 방향 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 우선순위, 기존 데이터 재사용, 반영 파일, 번역·조건·effects·역할 검토, 검색·설치·롤백 계획 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 대화의 150개 항목 전체 연결. 어휘별 운영 승인 또는 개별 사실검증 완료를 뜻하지 않음 |
| [seed-keywords.json](seed-keywords.json) | 원 대화 제목·번호와 연결 도구의 잘림 및 브라우저 복원 범위 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 가시 실현 70개 + 문맥 경계 19개. 소유·관계·혼동·출처·주장 한계·가시 gate |
| [candidate-drafts.json](candidate-drafts.json) | 같은 가시 카드에서 저술한 한영 70개 초안. runtime CID/RID/native proof가 아님 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 출처 43개, 읽은 범위와 확인 가능한 주장·한계 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 기존 후보 원문과의 재사용/차이 판단 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | unique 후보 19,471개/59개 모듈의 지정 필드 어구 진단. 실제 hybrid 검색은 아님 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 후보 9개 full record·조건·효과·해시 스냅샷 |
| [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md) | 원 대화의 여섯 창작 조합을 관측 가능한 관계와 남은 서사 의미로 전개 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 24·경계 16·일반 대조 8·비가시 대조 4, 52사례/104개 한영 질의. NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 필수 12사례의 A/B/C 36장 비교 및 후속 채택별 gate. NOT_RUN |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 대화 복원, 접근 실패, 발췌/소개만 읽은 자료, 후속 개별 원전 조사 |
| [BASELINE.json](BASELINE.json) | 시작 HEAD·dirty 상태와 보호 대상 source/index/runtime 63개 파일 해시 |
| [RUNTIME-CHECK.json](RUNTIME-CHECK.json) | 읽기 전용 설치 recorder/의존성 검사. 연구 자료의 운영 반영 증거가 아님 |
| [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 연구 구조 검사·원본 해시 비교·이 폴더 파일 무결성 |

70개 가시 카드와 70개 후보 초안은 같은 연구 단위이므로 합산하지 않는다. 정확한 신규 후보 수와 재사용 수는 full source/native 검토 후 결정한다. 43개 출처는 150개 모든 용어의 개별 원전·문화적 진위를 확정한 수가 아니다. 구체적인 장면은 출처의 정의·물체·비평 구분을 바탕으로 저술한 선택형 제안이다.

## 재생성과 검증

```sh
python3 docs/research-evidence/photo-prompt/folk-horror-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/folk-horror-20261022/build_evaluation.py
python3 docs/research-evidence/photo-prompt/folk-horror-20261022/validate_research.py
```

이 세 스크립트는 이 폴더의 파생 JSON·Markdown·TSV·검증 결과만 쓴다. `build_research.py`는 현재 slot catalog를 읽어 역할 이름의 존재를 확인하므로 재생성 시 현재 기준이 달라질 수 있다. 과거 evidence를 덮기 전에 스냅샷을 보존한다. `BASELINE.json`과 기존 소스 스냅샷은 위 명령으로 재수집하지 않는다.

초기 검증 PASS의 범위는 참조 연결·번호 커버리지·한영 초안 보존·owner graph·문맥 비승격·평가 사례 구성·해시 무결성이었다. 후속 검색·선택·프롬프트·원본 픽셀 증거는 각각 위 결과 문서의 실제 실행 범위만 인정한다. native 의미 자격이나 요청 사용자의 선호 검증으로 승격하지 않는다.

`SHA256SUMS`는 초기 연구 파일의 기록이며 README는 후속 결과를 위해 갱신했다. 현재 파일의 무결성은 이 폴더에서 `shasum -a 256 -c APPLY-SHA256SUMS`로 확인한다.
