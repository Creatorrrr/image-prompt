# 슬롯별 독립 하이브리드 검색과 필요한 shard 적재 계획

작성일: 2026-10-13. 기준 커밋: `642b33241de31000411a88702b38103050f50d9c`.
상태: **계획 작성 완료, 구현 미착수**. 이전 공통 후보풀 전환 1–9단계의 후속 계획이며, 아래 단계 번호는 새 작업에 해당한다.

## 목표와 현재 기준

요청에서 활성화한 각 슬롯이 공통 positive 후보풀 전체를 독립적으로 BM25F와 embedding으로 검색한다. 슬롯 태그는 기존 연결 및 역할 적합성의 근거로 사용하며 검색 공간을 나누지 않는다. 전체 검색을 보장하면서 결과에 필요하지 않은 shard의 본문은 읽거나 메모리에 적재하지 않는다.

[직전 검증 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/post-migration-slot-shard-audit-20261013/REPORT.md)의 기준은 다음과 같다.

| 항목 | 현재 상태 | 목표 |
|---|---|---|
| 원본 후보 | canonical 18,250건, 슬롯 연결 12,020건 | 후보의 단일 소유권·다대다 연결 유지 |
| 검색 문서 | positive 18,186건; diagnostic 64건은 별도 | 모든 슬롯이 같은 positive 전체 공간 검색 |
| 관리 슬롯 태그 | 112개 | 모든 등록 슬롯을 직접 지정하여 검색 가능 |
| 검색 실행 | frozen-core 쿼리 1개로 전역 검색 후 기존 태그별 표시 | 슬롯별 쿼리·두 lane·순위·결과·실행 상태 독립 |
| 벡터 저장 | gzip 143개, 압축 총 50,082,818바이트 | 검색 가능한 공간 분할과 읽기 생략 근거 추가 |
| 벡터 적재 | 최초 모든 shard 적재, worker 내 재사용 | 작은 routing metadata와 필요한 shard 적재 |
| BM25F | 전체 JSON cache 1개 | 전체 통계 + 필요한 term/posting block 적재 |
| freshness / 감사 | source capture에서 모든 shard SHA 확인; 전체 재계산 경로 존재 | 게시 시 전체 검증, 요청 시 필요한 자료 검증·증명 재생 |

등록 태그 수나 연결 수가 검색 대상 수를 결정하지 않는다. `adult_context`의 기존 연결 3건, `fetish_styling`의 1건을 해당 슬롯의 검색 상한으로 사용하지 않는다. `safety_profile`, `costume_absorption_guard`는 현재 슬롯 catalog에 없으므로 기존 제어 규칙과 구분한다. 새 후보 슬롯으로 추가하려면 별도 역할 정의가 필요하다.

## 반드시 유지할 계약

1. 슬롯마다 **전역 64개 선별 이전**에 전체 positive 후보풀을 검색한다. 대상 슬롯 태그의 존재 여부, 기존 binding 유무, 다른 슬롯의 검색 결과로 검색 공간을 제한하지 않는다.
2. 각 슬롯에서 BM25F와 실제 provider query embedding을 모두 실행하여 RRF로 결합한다. BM25F의 IDF·평균 field 길이 등은 전체 corpus 통계를 사용한다. embedding lane을 lexical hit가 나온 shard에만 제한하지 않는다.
3. frozen core, 사용자 제외 조건, 성인 조건, owner·관계·효과·prerequisite와 원본 guard는 보존한다. 역할 적합성 검사는 검색 공간을 슬롯 태그로 제한하는 대체 수단이 아니다.
4. 기존 태그가 없거나 다른 태그만 가진 후보도 대상 슬롯의 역할 제안에 포함할 수 있다. 발견, 역할 제안, 실제 채택을 구분하고 원본 의미를 변경하거나 persistent binding을 자동 생성하지 않는다.
5. 한 후보는 canonical ID·문서·벡터를 하나씩 가진다. 여러 슬롯에서 반환되더라도 payload와 unique 예산은 한 번만 계산한다. 재샤딩 때문에 후보 ID나 embedding text를 바꾸지 않는다.
6. 원본부터 만들었던 슬롯 트리와 레거시 호환 경로를 복구하지 않는다. 최종 운영 경로는 새 계약으로 교체하고, 전체 스캔 구현은 오프라인 검증 기준으로만 남긴다.

**전체 후보 검색은 모든 본문의 선적재를 뜻하지 않는다.** 모든 shard를 routing 대상으로 두고, 결과에 들어올 가능성이 없다는 상한 증명이 있을 때만 읽기를 생략한다. 증명이 부족한 쿼리는 모든 shard를 순차적으로 읽을 수 있다. 임의의 상위 centroid 몇 개만 선택하는 방식으로 전체 공간 검색을 보장했다고 주장하지 않는다.

## 단계별 수정과 완료 조건

### 1단계 — 검증 기준·실행 범위·I/O 기준선 고정

- 현재 호출 경로의 쿼리 생성, eligibility, source capture, index loader, profile assembly, 감사 및 receipt 재생을 조사하여 전체 본문을 읽는 지점을 목록화한다.
- 112개 슬롯 각각의 한국어·영어 의미 요청과 기대 후보·부적합 후보를 고정한다. 무태그·다른 태그·다대다 후보, 방향·owner 혼동, guard 거부, 사용자 제외, 필수 의무를 포함한다. 기존 자연 요청 20건도 유지한다. 기존 태그를 정답 생성 규칙으로 사용하지 않는다.
- 슬롯 활성화는 동결된 요청과 역할 정의로 결정한다. 일반 생성은 필요한 슬롯을 실행하며, 명시적으로 112개 전체를 지정하는 검사도 지원한다. 비활성·미실행·검색 결과 없음·조건 거부·표시 예산 제외를 구분한다.
- 같은 슬롯 쿼리를 입력받는 독립적인 전체 스캔 기준 구현을 준비한다. 2단계에서 쿼리 계약을 고정한 후 이 기준 구현으로 정답 순위를 기록한다. 기존 단일 쿼리 결과는 회귀 참고 자료이며 새 슬롯별 순위의 정답으로 사용하지 않는다.
- cold/warm, 단일 슬롯, 일반 활성 슬롯 집합, 112개 전체, 동시 요청에서 파일 stat·hash·read·decompress, 읽은 바이트, cache, peak RSS, lane 시간, provider 호출 수를 측정한다. 기준선 측정 후 신규 구현을 측정하기 전에 성능 목표 수치와 cache 상한을 문서로 확정한다. 비교 대상은 동일한 슬롯 쿼리 집합의 전체 스캔이며, API 시간이 순수 검색 성능 차이를 가리지 않도록 분리한다.

**검증/완료:** 슬롯별 검증 행렬, 정확 순위 비교 도구, I/O 계측 및 목표 수치 저장. 기존 무결성/freshness 회귀 통과. 실제 provider 근거와 합성 벡터 단위 검사를 구분한다.

**커밋:** `test(photo): freeze per-slot hybrid retrieval and shard baselines`

### 2단계 — 슬롯 쿼리·역할 제안 계약 정의

- 중립적인 슬롯 정의에 원하는 시각 속성, owner, 관계, 허용 효과 및 제외 조건을 명시한다. 후보 조회 이전에 frozen core와 creative controls를 확정하고 이후 슬롯 쿼리를 만든다. 검색된 후보 문구를 이용하여 필수 조건이나 원래 의도를 새로 만들지 않는다.
- `global_context`와 `slot_focus`의 BM25F query field, 가중치 및 embedding 입력 조합을 버전으로 고정한다. 두 lane이 같은 슬롯 의도를 사용하도록 한다. 초기값과 변경 근거를 기록하고 scoring recipe 변경 시 정답도 새 버전으로 생성한다.
- private query context에 슬롯 ID·정의 SHA·template/recipe·core/controls SHA·전체 입력 SHA·provider/model/dimensions·실제 응답/vector SHA를 결합한다. cache는 정확히 같은 입력과 embedding space에만 재사용한다. 다른 슬롯의 벡터를 쿼리 SHA 확인 없이 재사용하지 않는다.
- 역할 제안에 `target_slot_id`, `candidate_id`, 기존 `binding_id`(있을 때), source 의미 근거, owner/effect/prerequisite, 적합·검토 필요·거부 상태를 둔다. 원본에 역할별 guard가 있을 때 새 target으로 바꾸어 우회할 수 없도록 한다. 의미 근거가 부족한 후보는 검토 대상으로 남기고 자동 채택하지 않는다.
- keyword-only는 명시적인 진단 모드로 제한한다. 운영 슬롯 검색의 한 lane이 실패하면 정상 hybrid 결과로 발급하지 않는다.

**검증/완료:** 서로 다른 슬롯이 서로 다른 쿼리 context를 갖는지, 동일 입력은 재현되는지, 슬롯/space/core 변조를 거부하는지 검증. 무태그 및 다른 태그 후보의 역할 제안과 원본 guard 보존을 함께 증명한다.

**커밋:** `feat(photo): define independent slot query and role proposal contracts`

### 3단계 — 검색용 shard·전역 통계·locator 생성

- authored corpus는 그대로 두고 파생 인덱스에 candidate ID → payload locator, source/row SHA, 필요한 guard projection을 만든다. 원본을 두 군데서 수정하는 구조를 만들지 않는다.
- BM25F 인덱스를 전역 문서 수·term DF·field 평균 길이·lexicon과 term별 posting block으로 나눈다. 슬롯별/물리 shard별 IDF를 만들지 않는다. field/term 합산 순서, score 정밀도 및 ID tie-break를 고정한다.
- 벡터는 슬롯 태그나 UUID 순서에 의존하지 않는 공간 분할로 구성한다. query와 관련된 영역을 찾아 읽을 수 있게 하고 모든 후보를 정확히 한 leaf shard에 배치한다. 필요하면 계층적인 영역 경계를 둔다.
- 기존 문서 embedding은 ID·전체 text·recipe·provider/model/dimensions가 모두 일치할 때 재사용한다. 재샤딩만을 위해 재임베딩하지 않는다. 저장 표현을 바꿀 때 기존 수치와 순위를 손실하지 않는지 검증한다.
- 각 영역에 실제 벡터를 포함하는 안전한 score 상한을 저장한다. 예를 들어 정규화한 문서 벡터의 중심 `c`와 모든 벡터를 포함하는 반경 `r`에 대해 단위 query `q`의 상한은 `min(1, q·c + r)`이다. build에서 포함 관계와 수치 오차를 검증하고, 직렬화/계산 오차를 바깥 방향으로 보정한다. 더 촘촘한 분할이나 추가 상한을 사용할 때도 포함 증명을 유지한다.
- manifest에 layout/recipe/space/source SHA, 전역 통계 SHA, routing 경계 SHA, shard path/SHA/count, locator coverage를 연결한다. routing metadata에 전체 원본 벡터를 복제하여 선적재하는 편법을 쓰지 않으며 metadata 크기도 성능 계측에 포함한다.
- 새 layout은 별도 산출 디렉터리와 manifest에서 생성·검증한다. 8단계 자격 검증까지 명시적인 검증 generation을 사용하고, 현재 운영 manifest/CURRENT를 덮어쓰지 않는다. 9단계에서 새 계약으로 원자 교체하고 전환용 선택 경로도 제거한다.

**검증/완료:** 누락·중복·dangling locator 0건, 기존 positive coverage 동일, source text/guard projection 보존. shard 재배치에도 후보 ID와 전역 BM25F/embedding 점수·순위가 동일하다. 모든 영역의 상한이 모든 소속 벡터를 포함한다.

**커밋:** `feat(photo): build global searchable shard manifests and bounds`

### 4단계 — 필요한 자료만 읽는 저장소와 generation 수명 관리

- runtime 시작 시 manifest, 전역 통계, routing 및 최소 guard metadata를 적재한다. lexical posting, vector, candidate payload는 필요할 때 읽고 generation+SHA로 구분하는 용량 제한 cache를 사용한다.
- typed candidate repository를 도입한다. 전체 `.items()` 순회, corpus 직렬화, 전체 profile 조립, activation 검사 등이 우회적으로 모든 payload를 읽지 않도록 호출자를 바꾼다. 필요한 필수 profile의 정확 조회와 optional retrieval을 분리한다.
- generation 생성 및 전체 검증은 게시 경로에서 수행한다. 요청 cache miss가 전체 인덱스 재생성으로 이어지지 않도록 한다. 미게시 source 변경은 stale generation으로 명확히 처리하며 검증되지 않은 이전 세대를 새 source의 결과로 사용하지 않는다.
- 게시 시 모든 manifest closure의 SHA·coverage·경계를 검증한다. 요청에서는 필수 경로 존재/파일 identity와 작은 source/manifest의 변경을 확인하고, 실제 읽는 shard의 SHA·행·vector를 검증한다. cache hit도 해당 identity 변경에 따라 무효화한다. 읽지 않은 shard 본문까지 그 요청에서 SHA 검증했다고 표시하지 않는다.
- source/manifest 변경, 같은 mtime의 source/적재 shard 변경, 누락된 필수 shard, cache 변조 및 게시 경쟁을 검사한다. 요청 중 generation을 고정하여 query·routing·벡터·payload가 서로 다른 세대에서 섞이지 않게 한다.

**검증/완료:** metadata만으로 초기화 가능하고 instrumented reader가 요청 밖의 본문 적재를 검출한다. cache 상한, eviction 후 재조회, cold/warm, 세대 변경·동시 게시 및 변조 거부 통과. 전체 검증 범위와 요청 검증 범위를 evidence에 구분한다.

**커밋:** `feat(photo): add lazy candidate and index shard readers`

### 5단계 — 전체 공간의 두 lane 검색과 증명 가능한 읽기 생략

- BM25F는 query term의 posting을 읽어 전역 통계로 점수를 계산한다. 추가 block 생략 최적화는 안전한 최대 점수 경계를 검증할 수 있을 때 적용한다. 처음에는 해당 term의 posting 전체를 읽는 정확한 구현부터 완성한다.
- embedding은 모든 공간 영역의 상한을 비교하여 순서대로 shard를 읽고 정확 cosine top-K를 갱신한다. 현재 K번째 점수보다 안전하게 낮은 상한을 가진 영역만 건너뛴다. 동점/오차 경계는 읽고 기존 candidate ID tie-break를 유지한다. K개 미충족 시 최소 similarity 조건을 만족할 가능성이 남은 영역을 읽는다.
- lexical hit shard, 대상 슬롯 binding, 고정 centroid 개수로 vector 탐색을 제한하지 않는다. 상한이 느슨하면 더 읽거나 전체를 스트리밍한다. pruning 통과를 위해 정확도 조건을 낮추지 않는다.
- context 기반 제외/guard는 compact metadata에서 기존 의미와 동일하게 평가한다. 각 lane의 순위와 RRF 결합은 같은 입력의 전체 스캔과 일치해야 한다. score 반올림은 직렬화 계약을 따르며 replay 허용 오차를 넓혀 불일치를 숨기지 않는다.
- 읽은/생략한 영역, 상한, 종료 threshold, 실제 lane 실행, bytes/cache 상태를 기록한다. 여러 슬롯이 필요한 block을 공유하더라도 각 쿼리의 점수·top-K 상태는 독립적으로 유지한다.

**검증/완료:** 전체 스캔 대비 두 lane ID·점수·순위 차이 0건. shard 경계, outlier, 음수 cosine, 동점, threshold 근처, lexical miss/vector hit 및 전 영역을 읽어야 하는 경우 검증. 읽기를 생략한 각 영역에 종료 조건의 근거가 있다.

**커밋:** `feat(photo): search the full shared pool with certified shard pruning`

### 6단계 — 슬롯별 독립 실행·후속 검색·표시 예산

- 모든 활성/명시 슬롯이 자기 쿼리로 두 lane과 RRF를 실행한다. 이전 단일 검색의 상위 64개나 먼저 처리한 슬롯 결과를 다음 슬롯의 검색 대상으로 쓰지 않는다.
- 슬롯별 요청·완료·실패·hit 없음·role 적합성 거부 상태를 제공한다. 적합성 검토로 초기 결과가 모두 탈락하면 동일한 전역 공간에서 다음 순위를 이어서 조회한다. lane의 top-K를 확장할 때는 교차 lane 순위에 맞춰 RRF를 다시 결합하고 기존 목록에 단순히 덧붙이지 않는다. 중복 page/무한 반복을 방지하며 억지로 후보 수를 채우지 않는다.
- provider query 호출은 bounded concurrency와 정확 cache로 제어한다. 계획된 호출 수, 신규 호출 수, cache hit 및 실패를 기록한다. 요청 전체 상태에서 일부 슬롯 실패를 숨기지 않는다.
- 독립 검색 결과를 얻은 뒤 슬롯별 표시 예산과 요청 전체 unique 예산을 적용한다. 기존 core 4/support 2, 전체 unique 64 기본값의 유지/조정은 명시 정책으로 고정한다. 112개 전체 검색에서 모든 슬롯의 최대 표시 수를 보장할 수 없으므로 예산 제외와 검색 실패를 구분한다.
- 여러 역할에 적합한 같은 후보는 후보 본문 한 개와 역할 참조 여러 개로 표현한다. 태그 수를 RRF 투표 수나 unique 후보 수로 계산하지 않는다. 슬롯 처리 순서가 예산 배분을 우연히 바꾸지 않게 우선순위·공정 배분·tie-break를 고정한다.

**검증/완료:** 슬롯 실행 순서 변경에도 슬롯별 검색 순위 동일. 기존 binding 밖의 적합 후보가 실제 슬롯 결과에 나타난다. 전역 cap 때문에 검색이 생략되지 않으며 예산 제외가 trace에 남는다. 한 슬롯의 query/vector 혼입, cache 실패, 빈 결과 및 후속 page 검사 통과.

**커밋:** `feat(photo): execute independent full-pool hybrid searches per slot`

### 7단계 — candidate pack·composer·receipt·감사 통합

- native pack과 retrieval/query/receipt/generation 계약 버전을 함께 올린다. 슬롯별 context/rank/role proposal, index/routing/source SHA 및 예산 결과를 결합하고 후보 본문은 한 번만 넣는다. 구체적인 버전 번호는 구현 시 확정한다.
- compose/view/workflow/API preflight가 새 역할 제안과 후보 source 의미를 사용하도록 바꾼다. 검색 점수가 높은 후보라도 core lock, owner, prerequisite, 사용자 제외 또는 원본 효과를 위반하면 채택을 거부한다. 필수 visual obligation의 정확 조회 경로는 유지한다.
- 운영 감사는 검증된 routing 경계, 실제 읽은 posting/vector 점수, 생략 상한 및 종료 조건을 독립적으로 확인한다. pack/render preflight나 receipt 재생이 전체 corpus를 다시 적재하는 경로를 제거한다. 감사자의 계산과 증명 검사로 구현자의 요약 trace만 믿는 문제를 피한다.
- 별도 오프라인 감사는 원본부터 전역 통계·모든 벡터·경계를 재계산하여 전체 스캔 정답을 만든다. 운영 증명 검증과 오프라인 완전 검증의 범위를 각각 기록한다.
- issued receipt의 실제 저장본, generation/context/index/pack SHA를 검증하고 새 worker에서도 슬롯별 결과·배분이 정확히 재생되도록 한다.

**검증/완료:** 공개 prepare/compose/view/preflight와 private query 전체 흐름 통과. 다른 슬롯 receipt/context, 임의 role proposal, 누락 lane, 허위 pruning 근거 및 source 변조를 거부한다. fresh worker 재생 정확 일치 및 감사 경로의 숨은 전체 적재 0건.

**커밋:** `feat(photo): integrate per-slot retrieval into native workflow and audits`

### 8단계 — 전 슬롯 품질·무결성·I/O 성능 자격 검증

- 112개 슬롯의 한국어·영어 검증 행렬과 기존 자연 요청 20건을 실행한다. 단위 테스트의 합성 벡터 외에 실제 provider query 응답 및 정확 cache 재생 근거를 저장한다. 신규 API 호출 계획과 비용을 실행 전에 산정하고 결과와 비교한다. 이미지 생성은 이 검색 검증에 필요하지 않다.
- 새 슬롯 쿼리에 대해 전체 스캔과 lazy 검색의 두 lane 순위, RRF, eligibility/role 적합성, 표시 배분이 일치하는지 검사한다. 모든 원본 후보·binding·guard·필수 의무의 보존도 별도로 확인한다.
- 슬롯별 의미 recall/적합성은 독립적으로 작성한 기대 자료로 평가한다. 태그 연결 수, hash 일치, 실제 API 실행만으로 의미 정확도를 통과 처리하지 않는다. owner·방향·관계·재질의 기존 혼동을 따로 보고한다.
- 동일 입력/동일 provider 벡터로 cold/warm 및 단일·일반 다중·112개·동시 요청을 비교한다. routing metadata, source capture, 감사, payload 조립까지 포함한 read/hash/decode bytes, 실제 touched shard, cache, peak RSS, 시간과 API 시간을 분리해서 보고한다.
- 대표 일반 요청에서 실제로 일부 shard 본문을 건너뛰고 1단계의 I/O/메모리 목표를 만족해야 한다. 모든 shard가 필요한 경우에도 정확성과 memory 상한을 만족해야 한다. 경계가 느슨해 대표 요청의 읽기가 줄지 않으면 3–5단계의 분할/상한을 개선하고 다시 검증한다. 전체 적재를 새 이름으로 포장하거나 근사 검색으로 조용히 전환하여 완료하지 않는다.

**검증/완료:** 정확 재생/원본 의미/필수 의무 실패 0건, 모든 슬롯의 실행·검증 근거 확보, I/O 및 memory 목표 충족. 의미 품질의 미해결 항목과 이미지/pixel 미검증 범위를 보고서에 명시한다.

**커밋:** `test(photo): qualify all-slot retrieval and lazy shard behavior`

### 9단계 — 새 runtime 게시·기존 운영 경로 제거

- 검증한 원본 → 파생 인덱스 → generation 순서로 게시한다. 이미 완료한 공통 후보풀 구조는 유지하고 새 query/index/pack 계약을 운영 기본값으로 고정한다.
- 기존 단일 frozen-core 검색 후 태그별 나눔, eager `_global_index.entries` 적재, monolithic BM25F 운영 cache, 구 query/receipt adapter 및 자동 fallback을 제거한다. 전체 스캔은 오프라인 build/평가/완전 검증에서만 사용할 수 있게 분리한다.
- 레거시 제거 대상은 새 manifest가 참조하지 않는 이전 운영 파일·파생 shard/cache로 특정한다. 정확한 목록과 hash/복구 자료를 남기고 필요한 현재 shard, 원본, fixture, 역사 증거와 다른 작업 파일을 보호한다. shared 디렉터리 전체를 삭제하거나 ignore하지 않는다.
- SKILL·maintenance·사용 예시를 새 슬롯별 흐름으로 갱신한다. 삭제 후 cold start, fresh worker, 새 issued receipt 재생과 구버전 receipt 거부, 전체 슬롯 replay, 공개 compose/preflight 및 source freshness를 다시 확인한다. 과거 증거 파일은 이력으로 보존하되 운영 호환 adapter를 두지 않는다.

**검증/완료:** 운영 코드에서 기존 단일 검색/eager/fallback 참조 0건, 신규 generation의 referenced closure 완전 검증, 삭제 후 공개 경로 및 슬롯별 회귀 통과. 결과·제약·성능·commit 상태를 최종 보고한다.

**커밋:** `refactor(photo): retire single-query and eager production retrieval`

## 주요 수정 위치

| 범위 | 현재 파일 |
|---|---|
| 슬롯 실행·RRF·예산 | [photo_global_retrieval.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_global_retrieval.py) |
| 슬롯 query와 provider/cache 결합 | [photo_frozen_query.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_frozen_query.py) |
| shard 생성·경계·reader·전역 lexical | [photo_global_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_global_index.py), [photo_global_index_storage.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_global_index_storage.py), [bm25f_retrieval.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/bm25f_retrieval.py) |
| 원본 projection·역할 view·payload | [photo_shared_views.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_shared_views.py), [photo_native_pack.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_native_pack.py) |
| generation·freshness·receipt | [photo_runtime_sources.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py) |
| 독립 감사·공개 흐름 | [audit_global_retrieval.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_global_retrieval.py), [photo_workflow.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_workflow.py), [generate_photo_prompt.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py) |

필요한 repository/router/slot executor 구현을 별도 모듈로 분리할 수 있다. 위 파일의 명칭을 바꾸는 것만으로 lazy loading이나 독립 검색이 구현됐다고 판단하지 않는다.

## 실행·커밋 규칙

- 실제 구현을 시작할 때 작업 트리와 최신 `origin/main`을 확인하고 다른 변경의 의도를 보존한다. authored source를 먼저 통합하고 파생 인덱스를 재생성한다. 현재 계획 작성으로 runtime·index·query 계약을 바꾸지는 않았다.
- **각 단계 구현 → 해당 검증 → evidence/리포트 → 변경 경로만 커밋 → 다음 단계** 순서로 진행한다. 전체 원본/경계 검증, 필요한 회귀 및 실제 provider 검증을 단계별로 구분한다. 미통과 단계는 완료 커밋으로 보고하지 않는다.
- 실행 evidence는 이 디렉터리의 `stage01/`부터 `stage09/`에 저장한다. 코드/원본/index SHA, query 입력/응답 근거, 두 lane·slot 결과, 읽기 범위와 실패 항목을 연결한다. 비밀 키를 저장하지 않는다.
- 운영 교체는 8단계 자격 검증 이후에 진행한다. 이전 호환 경로를 남기는 대신 새 운영 계약을 검증하며, 요청된 경우에만 merge/push 상태를 별도로 처리·보고한다.
