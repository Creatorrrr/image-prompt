# 리프의 선택된 파랑 관계를 완전한 후보 문장으로 전달

이번에는 reef_flat_crest_forereef_wave_gradient 한 행의 영어·한국어 라벨을 이전에 검토한 수정 문구로 바꾸고, 그 26단어 영어 문장을 그대로 concept_units 하나에 넣었다. 나머지 16개 inventory 행, 별도 공간 구역 설명, 조석·썰물 대안, aliases·keywords·embedding_text·weights·applicability·guard와 역사적 maintenance 기록은 유지했다. Parser, schema, 검색 로직이나 scope는 바꾸지 않았다.

이전 labels-only trial은 계속 deferred다. 그 당시의 결과를 accepted로 바꾸거나 해당 branch를 main에 합친 작업이 아니다. 새로운 명시적 unit 표현을 별도 계획·질의·예산·측정으로 검토한 결과다. PLAN과 frozen 상태값은 측정 이전 시점의 기록이며, 최종 판단은 acceptance-decisions.json에 있다.

## 이번에는 무엇이 실제로 달라졌는가

기존 18단어 영어 후보는 flat→crest→fore-reef라는 공간 구역 순서를 선택된 입사파의 과정처럼 읽히게 했다. 이전 수정 문장은 지지할 수 있는 crest-breaking / landward-flat 관계를 담았지만 24단어 fallback 한도를 넘어 최종 V6에서는 기존 keyword 네 개만 남았다. 그 표현은 완전한 관계를 전달하지 못했다.

새 제안은 같은 수정 문장을 다시 쓰거나 짧게 자르지 않고, 기존 schema의 명시적 unit으로 보존한다. 실제 production pack, 검증된 full detail과 mandatory overview에서 다음 문장이 통째로 유지된다.

“showing waves breaking at the reef crest above the seaward fore-reef slope, with reduced wave energy over the sheltered shallow reef flat on the landward side”

후보는 optional/action-only이며 typed relations는 빈 배열 그대로다. 원래 authorial core, mandatory intent, control candidate와 guard도 유지된다. 최종 영어 문장 전달을 검증한 것이며, 한국어 최종 unit coverage 증가나 자연 질의의 노출·채택, 최종 composed prompt, 실제 이미지 품질을 검증한 결과는 아니다.

이 문구는 선택된 장면을 기술한다. 모든 파랑이나 조류가 한 방향이어야 한다거나, 감쇠가 육지 쪽에서만 일어난다는 주장이 아니다. 공간 구역은 [NOAA의 reef zones](https://oceanservice.noaa.gov/education/tutorial_corals/media/supp_coral04b.html), 파랑 감쇠는 [USGS의 coral reef 연구](https://www.usgs.gov/programs/coastal-and-marine-hazards-and-resources-program/science/coral-reefs), 조석·외향 흐름의 공존은 [USGS Molokai 관측](https://www.usgs.gov/publications/wave-and-tidally-driven-flow-and-sediment-flux-across-a-fringing-coral-reef-southern)과 함께 검토했다. 기존 fore-reef 감쇠와 ebb/tide 대안을 금지하지 않는다.

## 세 상태를 같은 corpus에서 비교

Baseline은 98619e72b07d623e01de65b352cb8188d919901f다. 현재 baseline, 이전 corrected-label comparator, 새 explicit-unit proposal의 세 상태를 비교했다. 과거 reef 질의 14개와 기존 action 질의 16개를 원문 그대로 재사용했으며, 새 blind holdout이 아니다.

총 180개 method/query/state 행에 primary target과 secondary reef의 전체 순위·점수, top5/top12 포함 여부와 실제 top12 결과를 보존했다. 한 행의 수정으로 모든 검색 품질이 개선되었다고 주장하지 않는다.

좋은 변화와 유지된 결과:

- 실제 최종 후보/detail에서 지지할 수 있는 전체 파랑 관계가 처음으로 보존됨
- 양성·공존·기존 action 통제군의 primary target 순위는 baseline과 같음. 기존 lexical no-hit도 그대로인 경우가 있으므로 모두 1위라는 뜻은 아님
- 30개 질의에서 baseline 대비 top5와 top12의 구성원 변화는 없음. 순서 변화는 method/query 비교 기준 각각 6개와 7개
- 영어 aquarium near-miss의 reef는 dense 3→4위, lexical 600→638위로 낮아짐
- 기존 action 통제 질의 16개는 primary target 순위와 top12 ID 순서가 동일함

불리한 결과도 채택 근거에서 제외하거나 숨기지 않았다:

- 한국어 aquarium q04에서 reef가 dense 4→2위, cosine .596789→.601540으로 상승
- 영어 dune q05에서 secondary reef가 lexical 4→2위, 점수 21.607297→38.922125로 상승
- 한국어 dune q06에서 secondary reef가 dense 3→2위, .662930→.674515로 상승
- 영어·한국어 intertidal q07/q08에서 secondary reef가 각각 dense 3→2위, .707043→.719958 / .669275→.684996으로 상승
- 방향을 거꾸로 쓴 q11/q12는 두 방식 모두 여전히 reef 1위다. Dense 점수도 .870197→.877492 / .826862→.837865로 상승하므로 방향 판별이 개선되었다고 볼 수 없음
- Café pickup 질의의 secondary reef lexical 순위는 204→15위, 점수는 6.433671→16.550679로 상승. Top12 밖이지만 실제 시스템의 다른 후보 폭이나 자연 노출에 영향이 없다는 증거는 아님
- 한국어 aquarium q04와 한국어 intertidal q08의 lexical primary target은 검색되지 않는 기존 상태를 유지

채택 판단은 source-correctness tradeoff다. 이전 표현에서는 전달되지 않던 완전한 물리 관계를 실제 후보에 제공하는 이익이 있고, 고정 진단의 양성·통제 target 순위와 top5/top12 구성원은 유지된다. 동시에 위의 순위·점수 손해와 관측하지 않은 질의·선택 확률의 위험은 남는다. 따라서 전체 retrieval 개선, 방향 이해, 자연 채택 또는 렌더 품질 개선이라는 결론으로 확대하지 않는다.

## 독립 검증·테스트·재현

독립 검토가 180개 결과 행을 별도로 재구성하고 모든 물리 index/BM25 기록을 확인했다. 문서 수는 10,174개이고 새 벡터 1개, 정확한 baseline 벡터 재사용 10,173개다. 새 source/unit의 실제 V6 pack ID는 4ecb74345aaab8c4다.

- DATA/natural-environment 192개와 의미·effect·profile-index 28개, 총 220개 관련 테스트 통과
- 별도 role 모듈은 8개 중 7개 통과, 기존 지역 평판 fixture 1개 실패. Recognition 후보가 7위라 요구 top6를 못 채우는 기존 문제이며, 수정 전후 세 질의의 top12 ID 순서가 동일함
- 기대값이나 과거 fixture를 완화하지 않았고, 전체 저장소 green이나 CI green을 주장하지 않음
- 원래 deferred 결과와 동결 질의·cache의 정확한 사본을 포함했다. 로컬 private branch가 없는 환경에서도 hash-bound 사본을 검증할 수 있음
- 해당 publication의 source/runtime snapshot에서 evaluate_cycle.py --replay로 180개 행과 현재 물리 index를 API 없이 재현할 수 있음

## 비용과 공개 단계

새 991-byte 문서 입력 한 번만 요청했고 성공했다. 질의 30개와 이전 comparator 벡터는 재사용했으며 자동 retry는 없었다. 추가 비용의 보수적 상한은 $0.0016384, 추적 누적 상한은 $1.2091392다. 청구서 실측이 아니고 별도 upstream 사용액과는 대조하지 않았다. 이미지 생성은 하지 않았다.

최종 commit 이후 최신 origin/main을 pull하고 적절한 후속 검사를 거쳐 정상 push와 정확한 remote commit/CI 확인을 수행한다. 공개 판단은 이 새 표현에만 적용되며, 과거 labels-only trial의 deferral은 유지한다.
