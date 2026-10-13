# 8단계 — 실제 쿼리·무결성·shard 자격 검증

112개 슬롯의 영어·한국어 224개 실제 provider 쿼리에서 전역 BM25F, 원본 정밀도 cosine, RRF 순위가 독립 전체 스캔과 모두 일치했다. 인덱스 분할 때문에 누락된 후보나 점수 차이는 0건이다. 전 슬롯의 실제 실행·역할 배분·생략 증명도 양 언어에서 독립 감사를 통과했다.

공통 원본은 후보 18,250개, 검색 positive 18,186개, binding 12,020개, 슬롯 112개다. 모든 원본·guard·정밀 벡터·전역 DF/TF 및 SQ residual 경계를 완전 검증했다. 문서 재임베딩과 이미지 호출은 0건이다. 실제 응답의 private context와 provider 실행 근거는 query-contexts 및 natural 하위에 보존한다.

## 검증 근거

- MATRIX.json: 224개 언어/슬롯의 쿼리 SHA, 두 lane/RRF SHA, top5, 실제 읽기, 생략 증명과 source oracle 대조.
- ALL-SLOTS-en.json / ALL-SLOTS-ko.json: 112개 실제 검색 후 배분한 전체 pack과 source audit. 찻잔 맥락의 영어 결과는 본문 11개, 역할 참조 172개, available 63개와 blocked 49개다. blocked도 두 검색 lane을 실행했다. 등록 tag나 이전 global top64로 검색 대상을 제한하지 않았다.
- NATURAL.json / SEMANTIC-EXPECTATIONS.json: 동결한 자연 요청 20건의 새 슬롯 쿼리, source oracle, 기존 필수 의무·hard gate 보존. 기대 자료는 이전 동결 core/필수 계약이며 신규 검색의 tag나 순위를 정답으로 쓰지 않는다.
- STABLE-REGRESSION.log: 사진 관련 333개 검사, subtest 309개 통과. 추가 WORST-CASE.log와 FINAL-SEARCH-TESTS.log는 전 영역 streaming 및 최종 검색 구현을 확인한다.
- EXTENT-REBUILD.json: 원본 벡터를 변경하지 않은 lossless 재분할 및 완전 source/통계/경계 검증.

## I/O와 시간

cold Reader는 metadata 22,179,167바이트만 읽고 payload·posting·vector 본문을 읽지 않는다. 실행 시간은 1.614초, peak RSS는 606,912,512바이트다. 기존 eager baseline은 15.169초와 1,440,366,592바이트였다. 압축 metadata와 디코딩 JSON 73,455,351바이트는 구분해야 한다.

전 슬롯 쿼리에서 최종 인덱스 전체 vector 읽기 대비 선택 extent 바이트 절감 중앙값은 약 45.6%다. 모든 사례가 vector 영역 일부를 생략했고 cache는 64MiB를 넘지 않았다. 3,850개 논리 leaf를 61개 물리 파일에 묶되 `pread`로 필요한 extent만 읽는다. 물리 파일 전체 적재가 아니다. 파일 descriptor도 최대 64개로 제한한다. 필요한 posting page와 선택/필수 candidate payload만 읽는다.

TF page는 공유 positive ordinal과 원래 float64 TF로 저장한다. 원본 float64 vector를 직접 보존하여 복원 CPU와 작은 파일 open 비용을 줄였다. 이 선택은 저장량을 늘린다. 대표 선택 vector 바이트 중앙값 50,756,537은 기존 gzip JSON vector 전체 50,082,818보다 약 1.3% 크다. 따라서 **최종 인덱스의 full scan 대비 읽기 생략, 초기 적재/RSS 개선, 기존 gzip과의 절대 vector 바이트 비교는 별개**다. 다중 독립 쿼리는 이전 단일 쿼리보다 더 많은 작업을 한다.

PERFORMANCE-REPEATED.json은 쿼리별 3회 중앙값을 사용한다. 빈 Reader로 cold를 만들며 OS cache를 강제로 비우지는 않는다. API와 metadata 시작 시간은 양쪽 검색 timer에서 제외한다. 가장 큰 중앙값 비율은 1.182로 고정 기준 1.2를 통과했다. 동시 CPU 작업 중 단일 표본은 1.2를 넘기도 했다. 이 표본과 이전 느린 구현의 결과도 evidence에 보존했다.

## 의미 품질과 증명 범위

224개 top-two 정의를 동결 요청과 비교해 검토했다. 찻잔 요청에서는 core 문맥이 중립적인 slot focus보다 강해, 영어 112개 중 69개 슬롯이 같은 top1을 가진다. source tag 수나 hash 일치로 역할 적합성을 통과 처리하지 않는다. `review_required`와 맥락상 blocked를 그대로 유지한다. 슬롯별 정밀도·의미 recall의 완전한 labeled benchmark와 이미지/native pixel 검증은 확보되지 않았다. 관련 한계는 SEMANTIC-REVIEW.json에 명시했다.

이 단계는 독립 전역 검색·정확 pruning·원본 계약 보존의 자격을 확인한다. 검색 점수가 역할 적합성을 자동 승인하거나 core의 소유자·색·관계·방향을 바꿀 권한을 주지 않는다. optional 후보를 전부 거절해도 기존 요청의 필수 의미가 유지되어야 한다.

최종 실제 query context는 자연 요청 1,366개와 bilingual matrix 224개다. 정확 cache 재사용을 제외한 신규 provider 호출은 1,544회이며 문서·이미지 호출은 0회다. 자연 요청 20건 모두 두 lane/RRF 및 기존 필수 의무·hard gate 대조를 통과했다.
