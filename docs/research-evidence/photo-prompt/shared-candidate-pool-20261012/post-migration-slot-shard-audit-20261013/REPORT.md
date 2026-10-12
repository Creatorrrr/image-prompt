# 슬롯 조회 및 샤딩 재점검

2026-10-13, main `277a4802`. 코드와 데이터는 변경하지 않고 현재 원본·인덱스를 직접 검증하고, 현재 native generation에서 실제 provider 벡터가 기록된 요청 2개를 재조회했다. 신규 embedding/image API 호출은 없다.

## 슬롯별 후보 조회

전역 검색과 슬롯별 표시 연결은 정상이다. 관리 태그 112개, 연결 12,020건 모두 공통 positive index의 후보를 참조하며 인덱스에서 누락된 연결 대상은 0건이다. 기존 동결 요청 20건의 모든 역할 참조가 실제 원본·binding과 일치했다. 이 20건에서 반환된 슬롯 종류는 62개이며, 나머지 50개는 이 입력들에서 노출되지 않았다. 이 사실은 나머지 슬롯의 오류를 뜻하지 않으며, 112개 전부의 자연 요청 의미 정확도를 검증했다는 뜻도 아니다.

현재 조회는 하나의 frozen-core 검색어로 전체 eligible 후보에 BM25F와 embedding을 실행하고, RRF 결과를 태그별 role view로 나누는 방식이다. 전체 unique 64개, 역할별 core 4개/support 2개 예산을 적용한다. 슬롯마다 특화된 검색어를 만들어 독립적으로 조회하거나 빈 슬롯을 재검색하여 채우지는 않는다. `POLICY.query_fields.slot_focus`는 선언되어 있지만 실제 호출은 `frozen_core`만 전달한다. 슬롯별 검색·recall 보장이 필요하다면 이 부분은 추가 구현·검증 대상이다.

태그 없는 후보도 global 결과에서 발견된다. 다만 해당 후보를 임의의 슬롯 태그로 자동 분류하지 않고 `unbound_candidate_refs`로 제공한다. blue-cup 재조회는 슬롯 16종·unique 64개·unbound 36개, 골렘 재조회는 슬롯 12종·unique 64개·unbound 42개였다. 실제 issued receipt와 current source를 사용한 전역 순위·배분 및 슬롯 참조 재계산이 기존 결과와 정확히 일치했고 두 lane이 실행됐다.

앞서 질문한 이름들의 현재 상태도 확인했다.

| 이름 | 현재 catalog 등록 | 등록 연결 | 동결 20건의 반환 횟수 |
|---|---:|---:|---:|
| occasion_context | 있음 | 106 | 7 |
| adult_context | 있음 | 3 | 0 |
| fetish_styling | 있음 | 1 | 0 |
| safety_profile | 없음 | 해당 없음 | 해당 없음 |
| costume_absorption_guard | 없음 | 해당 없음 | 해당 없음 |

등록 연결 수는 검색 가능한 전체 의미 후보 수가 아니다. 예를 들어 다른 태그의 관련 의복·재질 후보도 전역 검색에 들어온다. 그러나 adult_context/fetish_styling의 특정 role view가 충분히 채워진다는 검증은 위의 20건만으로 성립하지 않는다. safety_profile과 costume_absorption_guard는 현재 candidate slot catalog 항목이 아니므로 이 이름으로 후보 slot view를 반환하는 경로가 없다.

## 샤딩

공통 벡터 인덱스는 gzip shard 143개다. 142개에는 각각 128건, 마지막 1개에는 10건이 있어 총 18,186건이다. 압축 파일 총 크기는 50,082,818바이트다. 모든 manifest 참조 파일의 SHA·행 수·중복 ID·전체 candidate coverage·원본 text/recipe·유효 768차원 벡터 검증이 통과했다. 현재 shard 143개 모두 Git 추적 대상이며 ignore되는 파일은 없다. 원본은 candidate 모듈 16개, binding 모듈 16개, catalog 1개, policy 1개로 분리되어 있다.

샤딩은 파일 저장·버전 관리·snapshot 복사 단위다. 최초 적재 때 모든 벡터 shard를 읽고 하나의 메모리 인덱스로 합치며, 이후 해당 worker의 snapshot은 재사용한다. cosine은 요청별 eligible 후보 전체를 순회한다. BM25F runtime cache도 공통 JSON 한 개다. 필요한 shard만 선택하는 lazy loading, shard별 검색/merge, 분산 ANN 검색은 구현되어 있지 않다. 따라서 파일 샤딩의 무결성과 검색 단계의 메모리·분산 최적화는 구분해야 한다.

현재 source capture는 warm snapshot이 있어도 manifest가 참조하는 shard의 존재·SHA를 다시 확인한다. 필수 shard가 없어지면 이전 snapshot으로 성공시키지 않는다. native index·global retrieval·runtime freshness 회귀 25건을 다시 실행하여 통과했다. 이 검사에는 shard 변조·누락 거부, 다대다/무태그 발견, 태그 변경·guard 보존, 잘못된 query vector와 구 receipt 거부가 포함된다.

재현 근거는 `DATA-SHARD-RESULTS.json`과 `LIVE-RETRIEVAL-REPLAY.json`에 저장했다. 의미 순위 품질과 모든 슬롯의 자연 요청 recall, 큰 corpus에서의 메모리/latency 한계는 별도 검증 대상이다.
