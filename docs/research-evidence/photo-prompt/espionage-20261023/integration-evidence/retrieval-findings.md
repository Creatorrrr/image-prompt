# 고정 이미지 테스트 설치본의 검색 관찰

대상 H-F2: `3300bd369483c394610b29a53b8421934dacba4a9039e6cdd017deec7c4c26b7`.
206개 연구 사례의 412개 한영 질의를 전체 positive pool 20,235 CID에서 실행했다. 각 질의는 실제 BM25F 1회 + local cosine 1회를 사용했다. 별도로 이전 설치본에서 boundary/ordinary/nonvisual 88개 질의를 실행했다. 검색에 image API는 사용하지 않았다.

| 집합 | 질의 | exact-CID 평가 대상 | 상위 8 | 상위 32 |
|---|---:|---:|---:|---:|
| 원문 문장 smoke | 276 | 256 | 251 | 254 |
| 연구자가 작성한 자연어 표현 | 48 | 48 | 38 | 45 |
| 경계/일반/비시각 대조 | 88 | 0 | 미채점 | 미채점 |

smoke의 20개 질의는 세부 형태 확인을 보류한 10개 카드의 한영 표현으로, 등록된 positive target이 없다. 이들을 통과로 합산하지 않았다. 자연어 상위 8 결과는 한국어 17/24, 영어 21/24다. 한국어 Oxford closure(78위), Derby closure(40위), stocking support(38위) 등의 회수 약점이 남아 있다. 원문 smoke와 카드 작성자의 자연어는 독립 holdout이 아니므로 일반 정확도나 인과적 개선 수치로 사용할 수 없다.

대조 질의 88개 중 69개는 이전/후속 top1이 같고, 18개에는 이번 시각 후보가 top1으로 등장한다. 대부분 귀 장치 접촉, 자기 커프/타인 넥타이, 수갑의 사슬, 검은 막대 등 직접적인 경계 질의다. 다만 ‘사람 없이 보관 홈 안의 봉투’에 손으로 내려놓는 후보가 노출되거나 금융 보고서 질의에 앉은 사람과 두 보고서 후보가 노출되는 사례도 있다. 원문에 없는 사람·동작·시선은 자동 승인할 수 없다. 이 비교는 필터 전 선택지 노출만 측정하며, 개별 요청에 대한 선택/조건 검토나 최종 프롬프트 검증을 대체하지 않는다. exact-CID gold가 없는 대조군을 성공률 100%로 보고하지 않는다.

182개 diagnostic 기록은 positive 대상이 아니다. 의미 그래프/연구 키워드/role 태그는 원문 조건이나 소유자 사실, profile, hard activation을 만들지 않는다. 근거는 `control-exposure-comparison.json`, `focused-tests.log`, `dictionary-validation.final.json`, generated maintenance의 `probe-after.json`, `probe-before.json`, `retrieval-qualification.json`에 있다.

이 결과는 고정 테스트 설치본의 관찰이다. 다른 작업을 보존한 재기반 설치본의 후보 전체 집합은 다르므로 그 설치본의 재실행 결과를 별도로 기록한다.
