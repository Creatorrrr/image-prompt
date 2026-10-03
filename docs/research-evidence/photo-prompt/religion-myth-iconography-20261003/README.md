# 종교·신화 시각자료 연구 패키지

2026-10-03 작성. [참고 대화](chatgpt-conversation://6ac0522b-b354-83ec-a3ea-b51dd34dcd46)의 286개 키워드 행을 추적한 상세 조사와 데이터 반영 계획이다.

먼저 [리서치 보고서](RESEARCH.md)를 읽고, 실행 범위는 [반영 계획](IMPLEMENTATION-PLAN.md), 개별 구성 요소와 출처는 [상세 카탈로그](CATALOG.md)에서 확인한다.

| 파일 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 현재 데이터의 빈틈, 변형·지물·신체 연결·매체·도표 조사, 설계 결론과 한계 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 기존 의미 소유자 재사용, 슬롯/property 설계, 작성 파일, 단계별 검증·회복 |
| [CATALOG.md](CATALOG.md) | 시각 의미 140개 단위별 범위·관찰 요소·관계·혼동·출처 |
| [SEMANTIC-UNITS.json](SEMANTIC-UNITS.json) | 140개 연구 단위. 운영 반영 전 데이터 |
| [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json) | 110개 optional 후보 관찰 초안과 보류 조건 |
| [VARIANT-RELATIONS.json](VARIANT-RELATIONS.json) | 39쌍의 구별·변형 관계 |
| [BATCH-PLAN.json](BATCH-PLAN.json) | A 41 / B 47 / C 22개 초안의 작업 묶음과 선행 조건 |
| [FOLLOWUP-RESEARCH.md](FOLLOWUP-RESEARCH.md) | 관찰 초안이 없는 94행의 조사 질문, 맥락 수준 62행의 보강 범위 |
| [REFERENCE-KEYWORDS.json](REFERENCE-KEYWORDS.json) | 원 대화의 286행. 중복 색인을 보존 |
| [TERM-DECISIONS.json](TERM-DECISIONS.json) | 모든 참고 행의 처리·연결·추가 조사 판단 |
| [SOURCES.json](SOURCES.json) | 출처 111건의 URL·적용 범위·접근 상태·수집 영수증 |
| [REGRESSION-PROPOSALS.json](REGRESSION-PROPOSALS.json) | 미실행 회귀 설계 387건 |
| [PIXEL-GATES.json](PIXEL-GATES.json) | 미실행 ALL_OF 픽셀 검증 계획 110건 |
| [LIVE-AUDIT.json](LIVE-AUDIT.json) | 실제 로더 읽기, Git SHA, 입력 해시, 긍정 필드 문자열 단서 |
| [VALIDATION.json](VALIDATION.json) | 연구 파일 정합성과 각 증거 단계의 상태 |
| [MANIFEST.json](MANIFEST.json) | 이 폴더의 파일별 SHA-256 |
| [REQUEST.json](REQUEST.json) | 요청과 조사 범위 |
| [UNIT-SEEDS.json](UNIT-SEEDS.json), [SUPPLEMENT-UNIT-SEEDS.json](SUPPLEMENT-UNIT-SEEDS.json) | 작성한 연구 단위의 입력 원본 |
| [build_research_package.py](build_research_package.py) | 연구 파일·카탈로그·묶음·후속 질문 생성 및 정합성 확인 |

## 상태

출처 본문 반환 90건, 검색 발췌만 20건, 유효 본문 미확보 1건이다. 본문 반환은 관련 도판의 직접 픽셀 검토와 다르다. 참고 대화의 설명은 조사 단서로만 사용한다.

140개 연구 단위 중 30개는 맥락만 기록했고, 110개 초안에는 실제 core target/property 연결과 원본 대조 조건을 붙였다. 특히 `prop` 27건은 현재 슬롯의 허용 차원이 없으므로 소유권 해결 전 채택 보류다. 연구 JSON은 runtime extension/profile 스키마가 아니다.

이번 작업은 이 폴더에만 파일을 쓴다. 운영 자산·스크립트·테스트 변경, 파생 인덱스 재생성, 후보팩 실행, 제안 회귀 실행, 원본 도판 픽셀 대조, 이미지 생성·네이티브 픽셀 qualification, 사용자 수용 평가는 수행하지 않았다.

## 재현

저장소 루트에서 다음을 실행한다. 현재 로더를 읽고 이 연구 폴더의 파생 결과를 갱신한다. 네트워크·임베딩·이미지 API를 호출하지 않는다. 입력 출처와 단위 seed는 그대로 사용한다.

```sh
.venv/bin/python docs/research-evidence/photo-prompt/religion-myth-iconography-20261003/build_research_package.py
```

다른 작업이 운영 자산을 바꾸었다면 새 `LIVE-AUDIT.json`의 시점·해시·수량을 기준으로 정적 보고서의 수치를 재확인한다. 변경 중인 입력으로 얻은 audit나 원래 baseline 실패를 연구 성공으로 간주하지 않는다.

