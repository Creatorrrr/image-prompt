# 슬롯 후보 조회 수정 — 0·1단계

2026-10-11 · 상태: 0·1단계 수정·검증·현재 작업 폴더 반영 및 기본 runtime 활성화 완료

이번 작업은 [수정 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/FIX-PLAN.md)의 첫 묶음인 **0단계 비교 기준 마련과 1단계 `occasion_context` 복구**다. 모든 수정 단계를 완료한 보고서가 아니다.

## 결과

| 검사 | 결과 |
|---|---|
| 실제 source → loader → slot index → semantic index | 114개 슬롯, 12,043개 후보; 누락·추가 ID 0 |
| 같은 frozen 입력의 행사 후보 조회 | 수정 전 0/7 → 수정 후 7/7 |
| 행사 없는 장면 | 13/13에 행사 후보 추가 없음 |
| 공개 CLI·composer view·retrieval 재계산 | 20/20 통과; candidate 삭제 20/20 탐지 |
| 수정 전후 core 해시 | 20/20 동일 |
| 전체 정확 표기 검색 | 40,638/40,643 조회; 기존 native alias 실패 5개 유지 |
| 최종 코드 관련 회귀 검사 | 99개 통과: context·data 검사 71개 + core·worker 검사 28개 |
| 전체 composed audit | 채택 4건·후보 전부 거절 5건 통과; 문맥 증거 누락 2건 모두 차단 |
| 반영 후 현재 작업 폴더 | 공개 CLI 4건 통과, 격리된 결과와 pack 바이트 동일; 채택·거절·누락 audit 재확인 |

40,599개 동일 질의에서 조회 가능성의 신규 손실은 0이다. 44개 문구는 이번 source 의미 정리에 따라 바뀌었다. 좁은 cap 기준에서는 `harvest_market_day`의 일반 alias `day`가 3위에서 5위로 내려간 1건이 있다. 의미를 특정하지 않는 표기의 순위 변화도 기록했으며 cap을 확대하지 않았다. 원본 후보의 정확한 행사 문구는 조회된다. [질의별 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/exact-query-comparison.json)

## 무엇을 수정했는가

- 기본 tags 24개, worldbuilding 36개, CJK worldbuilding 46개, **합계 106개 occasion 후보**에 실제 효과의 차원과 property를 선언했다. 시점 외의 참가자·물체·동작·관계·문자·재질·조명·계절 효과도 해당 문구에 따라 기록했다. 슬롯 focus는 `event`와 `timing`에 연결했다.
- 기본 행사 후보의 positive 문구에서 `no readable`, `non-graphic` 등의 제어 지침을 제거하고 행사 자체를 기술했다. ID와 weight는 유지했다. 세 source에서 occasion 외의 데이터는 동일하다.
- 일반 행사는 graduation/workshop 등의 주체 맥락을 요구한다. 단순 `day`, `light`, `window`의 겹침만으로 행사 후보를 붙이지 않는다.
- 두 세계관 후보에는 source가 선언한 AND 묶음을 OR 대안으로 허용하는 `primary_context_alternatives`를 추가했다. 기존 scene marker 조건은 보존했다. 조건은 frozen subject/setting/event에서만 충족하며 다른 optional 후보의 태그를 빌리지 않는다.
- 기존 domain 경로에 `live-action roleplaying`, `live action roleplaying`, `isekai frontier`, `이세계 변경 길드` 네 표기를 연결했다. 기존 exclusion/subject/domain/property guard는 유지했다. 광범위한 adult routing 변경은 이번 범위에 포함하지 않았다.
- 새 조건은 `photo-candidate-context/v2`로 source와 hash에 연결된다. pack metadata를 지우거나 바꾸면 retrieval 재계산에서 탐지한다. 실제 채택 시에는 ordinary interpretation 또는 transformed augmentation decision의 `context_review`로 대안 한 묶음의 모든 사실을 최종 문구에 연결해야 한다. 미채택에는 증거를 요구하지 않는다. 기존 v1 계약은 유지한다.

완전한 106개 before/after 필드 기록: [scope review](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/occasion-scope-review.json). 코드에 후보별 ID 분기는 추가하지 않았다.

## 실제 비교 입력

| 고정한 요청의 행사 의미 | 반환한 실제 source ID |
|---|---|
| 졸업식 직후 꽃다발을 든 졸업생 | `graduation_after_ceremony` |
| 목공 수업 중 도구를 공유하는 성인들 | `workshop_class_session` |
| 개점 첫날 진열 준비 | `opening_day_setup` |
| 저녁 일식 관찰 | `eclipse_evening_watch` |
| 역할극 세계에서 이전 캠페인의 국경 변화를 반영하는 조약 검토 | `diegetic_larp_world_checkpoint_occasion` |
| 이세계 변경 길드의 계절 이동 상단 출발 전 의뢰·통행 검토 | `isekai_frontier_guild_frontier_occasion` |
| 방문객이 떠난 폐점 후 정리 | `closing_cleanup_after_hours` |

8개 개발 사례와 새 holdout 12개를 patch 전에 고정했다. 전후 요청·controls·baseline/core·property lock·embodiment 입력과 seed 17은 같다. controls는 이 benchmark의 명시적 neutral override이며 프로젝트 저장 기본값을 대표하지 않는다.

이 사례들은 유지보수를 위해 작성한 문장과 계약 검토다. 새 holdout도 이번 작업자가 작성했으므로 blind 창작 연구가 아니다. workflow freeze는 입력과 순서의 구조적 기록이며 후보 지식을 몰랐다는 독립 증명이 아니다. 이번 7개 occasion 의미의 적합성과 13개 비행사 경계를 검토했으며, 나머지 슬롯 후보 전체의 자연어 precision을 측정했다고 주장하지 않는다.

[고정 fixture](/Users/chasoik/Projects/image-prompt/tests/fixtures/photo_prompt/slot_retrieval_natural_v1/README.md), [역할표 114행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/slot-role-matrix.json), [최종 공개 CLI 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/after-benchmark.json)

## 최종 composition 검증

검증 중 새 v2 조건의 final witness 하나를 지워도 기존 audit이 통과하는 빈틈을 발견했다. 이를 실제 receipt-bound CLI로 재현하고, ordinary·augmentation 공통 semantic audit에 조건 검사를 연결했다. 최종 11개 결과는 예상과 모두 일치했다. 채택 4건과 전부 거절 5건은 통과하고 문맥 증거 누락 2건은 `candidate_context_prerequisites`로 차단됐다. [composition summary](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/after-composition-summary.json)

채택 검증은 독립 baseline의 행사 시점 의미를 해석하여 사용하는 경우다. 전체 후보를 거절하는 composition도 별도로 검사한다. 최종 prompt의 support/reach/contact/visibility를 다시 검토하여 `agent_postcomposition` 기록으로 연결했다. 구조·literal witness·scope 검사는 증거 문구가 시각적으로 참이라는 판정이나 이미지 품질을 대신하지 않는다.

## index와 runtime

- 의미 문구가 바뀐 24개 문서의 임베딩을 갱신하고 나머지 12,055개를 재사용했다. 이후 context/policy/audit 보완에서는 12,079개 모두 재사용하여 추가 vector 변경은 0이다.
- semantic index를 공식 builder로 생성했다. visual sidecar는 check를 통과하여 재생성하지 않았다. dictionary validator와 publisher로 정합성이 확인된 generation을 생성했다.
- 최종 격리 generation: `a18d6cb39aa3191e6d186e0cd3ec0df1e40e0b0ced448286cd4c0e704f1117d1`
- source fingerprint: `043f4bf9b194c69fc101c24781e73fc684b4b735c76b68ad68a463f297e5c6ac`
- 현재 작업 폴더와 기본 store `/Users/chasoik/.cache/image-prompt/photo-runtime`에서도 동일 generation을 활성화했다. 3개 source의 대표 행사와 비행사 컵 사례를 다시 실행하여 CLI/view/재계산/삭제 탐지가 모두 통과했다. 4개 public pack은 격리된 결과와 바이트까지 동일하다. 역할극 사례에서는 채택·전부 거절·문맥 사실 누락의 세 audit도 다시 확인했다. [primary 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/primary-benchmark.json), [활성화 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/primary-publication.json)

## 보존과 남은 범위

원래 22개 tracked 변경과 untracked 작업이 있는 기준선을 격리 worktree에 재현했다. 원본 검증 디렉터리, 구 generation/receipt, 수정 중간 결과를 보존했다. 재현 중 누락된 maintenance evidence 파일은 원본과 동일하게 복사했고, 불필요하게 바꾼 기존 폐점 한국어 phrase는 원상복구했다. 신규 nearest-negative 검사에서 길드 참가자를 남겨둔 잘못된 음성 사례를 수정한 기록도 보존했다. 최종 회귀 99개는 해당 보완 후 통과했다. 전체 test suite는 실행하지 않았다.

반영은 검토한 source/code/reference 10개와 active semantic shard 16개, 신규 test 및 frozen fixture 42개 경로로 한정했다. 기존 dirty semantic index는 이번 변경을 포함하여 재생성하고 수정 전 바이트를 `primary-before`에 저장했다. 그 외 dirty tracked 21개와 비대상 source/code 187개는 기존 해시와 같다. 원래 검증 디렉터리의 top-level 38개 파일도 동일하다. [보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-stage01-20261011/integration-preservation.json)

반영한 코드·데이터는 현재 작업 폴더에 있다. 격리 worktree도 다음 단계와 재현을 위해 유지한다. 재현 helper는 evidence 디렉터리에 두고, test fixture에는 frozen `fixture.json`과 원문 `request.txt`만 반영했다. 준비 입력과 실패 로그는 별도 evidence에 보존했다.

106개는 소유 범위 정리의 분모다. 106개 모두의 자연어 가족별 조회를 입증한 분모가 아니다. 확장 데이터의 나머지 80개는 기존 scene marker prerequisite를 유지하며 별도의 자연어 경로 개선·평가가 남아 있다.

계획의 다음 단계는 `safety_profile`/`costume_absorption_guard` 역할 정리다. adult/domain 전체 연결, 5개 native alias 토큰화, 다른 슬롯의 주체·owner·문맥 precision, 필요한 경우 fusion/cap 조정도 후속 단계다. 이번 작업은 이미지 생성·픽셀 검증·사용자 선호 평가를 수행하지 않았다. 커밋·푸시·PR은 수행하지 않았다.
