# 슬롯 후보 검색 개선 5단계 리포트

고정 자연어 20건에서 원문 근거가 없는 특수 주체·문맥 후보 노출은 **18/20 → 2/20**으로 감소했다. 개발 사례는 **7/8 → 0/8**, 고정 holdout은 **11/12 → 2/12**이다. 필수 호환 후보는 **7/13 → 13/13**으로 개선됐고 기존에 노출되던 필수 후보 손실은 없다. **주체 의미 문제를 전부 해결했다고 판정하지 않는다.**

명시한 특수 주체 14건은 **14/14 cap 내 검색**, 별도 인쇄 카드에만 해당 말이 있는 14건은 **0/14 대상 오검색**이다. 공개 CLI 총 **48건**에서 원래 core hash, receipt/pack hash, cap, composer view, source 재계산, 누락 변조 감지를 확인했다. 관련 unittest **125건 통과**.

## 변경과 원인

- 기존 subject 후보 **139개**의 실제 subtype·직업·상황 조건을 `primary_context_alternatives`에 선언했다. 후보의 문구를 바꾸거나 fantasy 전체를 제외하지 않았다.
- 일반 찻잔·새·회로·잎·성인 인물 후보 **5개**에 관찰 가능한 부품과 같은 몸/소유자에 이어지는 관계를 넣었다. 일반 인물 후보는 직업·세계관·인원 수를 추가하지 않는다. 성인 연령은 실제 frozen 문구에 있어야 한다.
- `coffee_cup`은 용기인 object, `neon_sign`은 기존 sign 해석을 명시한 override로 보존했다. 나머지는 하나로 명시된 지원 `kind`를 키워드 추정보다 먼저 사용한다. 블랙홀의 `sign`이 `ring` 때문에 object가 되거나 로봇 개가 animal이 되는 오분류를 고쳤다. 복수 food/object kind는 기존 fallback을 유지해 bubble tea·sushi·bibimbap을 food로 남겼다.
- frozen subject/setting/event의 owner별 literal witness를 보존했다. primary subtype은 typed `subject_phrase`를 우선하고, subject의 `for_any`·`for_all`·`not_for`를 실제 primary와 비교한다. 다른 선택 후보의 tags/facets로 전제를 스스로 충족시키지 않는다.
- material/light/action query는 해당 target/property family를 사용한다. 다른 owner·다른 속성·unscoped assertion이 섞이지 않고, 제외된 owner 문구의 잔여 조각이나 긴 scene으로 돌아가지 않는다. 카메라 owner 회귀 검사를 유지했다.
- 카메라 `viewpoint.orientation_to_cup`의 기존 방향 경로를 보존했다. 방향과 무관한 typed height anchor가 있을 때 소유자 없는 일반 lighting anchor로 우회하지 못하도록 추가 회귀 검사를 넣었다. 기존 owner fixture 12개와 입력 분모는 수정하지 않았다.
- 위 제한은 선언된 속성 소유 범위와 일반 슬롯의 effect-dimension fallback을 구분한다. `prop`처럼 속성 소유 범위가 없는 슬롯은 원래의 grounded carrier anchor를 유지한다. 중간 구현에서 찻잔 prop이 누락된 기록과 수정 후 재검증을 보존했으며 최종 필수 후보 측정에 중간 결과를 섞지 않았다.
- 12개 변경 source의 정확한 필드 차이와 전후 hash를 별도 보정 기록으로 봉인했다. 기존 maintenance reference 6개를 새 record에 연결했고, 이전 record의 bytes를 유지했다. 과거 source 검사는 이 봉인된 차이만 되돌려 비교하며, 임의 alias·label·조건 변경은 실패한다.
- applicability hash에 subject category override까지 포함해 변경된 정책의 receipt를 이전 정책으로 재계산하지 않게 했다. cap **전체 64 / core 4 / support 2**와 tokenizer/rank recipe는 유지했다.

## source와 코드의 분리 검증

초기 source-only 공개 CLI 20건 기록을 보존했다. 최종 비교는 **동일한 최종 merged source와 runtime quality/obligation layer**를 변경 전·후 코드에 직접 전달했다. 전제 검사는 명시 양성 **0/14 → 14/14**, 카드 음성 **0/14 → 0/14**, owner query는 **0/12 → 12/12**이다. source-only의 음성 0은 양성도 차단한 결과이므로 개선 PASS로 해석하지 않는다.

이 비교는 production 함수의 private 실험이다. vector cache를 제거한 직접 호출과 공개 runtime의 모든 슬롯 순위가 같다고 주장하지 않는다. 최종 노출·cap 판정은 실제 공개 CLI와 matching sealed source/index에 대한 재계산으로 확인했다. 대표 현재 receipt 3건은 cache와 분리한 generation 로드 후에도 재계산 문제가 없었고, 이전 pack 2건은 matching historical worker에서 완전 재계산됐다. 현재 worker는 이전 구현의 receipt를 2/2 `runtime_restart_required`로 거부했다.

## 고정 입력의 subject 결과

입력은 변경 전부터 고정한 개발 8개 + 과거 holdout 12개다. 새로운 blind holdout이 아니다. 다음 판정은 결과를 본 뒤 source의 실제 뜻과 frozen primary·setting·event를 대조한 유지보수 검토다. 부적합은 근거 없는 특정 identity/직업/필수 문맥 또는 다른 구조의 주체 제안을 뜻하며, 최종 prompt나 이미지가 실제 바뀌었다는 증거는 아니다. subject가 비어 있는 4개는 별도 표시한다. 다른 모든 슬롯의 의미까지 검증한 결과가 아니다.

| 입력 | 변경 전 subject | 변경 후 subject | 판정 |
|---|---|---|---|
| dev-01-rain-portrait-ko | witch_practitioner_role_model | adult_woman_lifestyle_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-02-blue-cup-en | single_camera_drone, ceramic_automaton_figure | teacup_vessel_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-03-coast-fog-ko | 미노출 | 미노출 | subject 미노출 |
| dev-04-small-bird-ko | phoenix_rebirth_subject, earth_diver_creation_subject | bird_connected_body_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-05-greeting-en | photobooth_friend_pair | adult_human_body_continuity_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-06-circuit-en | hollow_living_armor_subject | terminal_gap_circuit_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-07-dew-leaf-ko | water_w093, mycelium_forest_floor | veined_leaf_subject | 일반 구조 또는 요청한 주체와 호환 |
| dev-08-fashion-en | doctor_role_model | fashion_model | 일반 구조 또는 요청한 주체와 호환 |
| holdout-01-graduation-ko | local_legend_teller_subject | adult_human_body_continuity_subject | 일반 구조 또는 요청한 주체와 호환 |
| holdout-02-workshop-en | photobooth_friend_pair | 미노출 | subject 미노출 |
| holdout-03-opening-en | glassblower_role_model | adult_human_body_continuity_subject | 일반 구조 또는 요청한 주체와 호환 |
| holdout-04-eclipse-ko | photobooth_friend_pair | 미노출 | subject 미노출 |
| holdout-05-world-treaty-en | adult_royal_heir_role | conworld_cartography_world_survey_subject | 잔여 문제 |
| holdout-06-isekai-ko | hunter_gate_breach_recovery_subject | isekai_frontier_guild_frontier_subject | 일반 구조 또는 요청한 주체와 호환 |
| holdout-07-cup-ko | hr_dokkaebi_object_origin, ceramic_automaton_figure | teacup_vessel_subject, coffee_cup | 일반 구조 또는 요청한 주체와 호환 |
| holdout-08-bird-en | sleeping_dog, earth_diver_creation_subject | bird_connected_body_subject | 일반 구조 또는 요청한 주체와 호환 |
| holdout-09-landscape-en | 미노출 | 미노출 | subject 미노출 |
| holdout-10-fantasy-ko | legendary_trace_boulder_subject, constructed_golem_subject | planetary_rover_operation_subject, constructed_golem_subject | 잔여 문제 |
| holdout-11-neutral-fashion-en | doctor_role_model | fashion_model | 일반 구조 또는 요청한 주체와 호환 |
| holdout-12-after-hours-ko | maid_cafe_staff | adult_human_body_continuity_subject | 일반 구조 또는 요청한 주체와 호환 |

잔여 `holdout-05-world-treaty-en`의 source는 가상의 항구에 있는 현장 측량자·항해 기록관을 제안한다. frozen 입력의 대표단·조약 검토만으로 그 역할과 장소가 확보되지 않는다. `holdout-10-fantasy-ko`의 planetary rover는 돌 골렘과 다른 이동계·과학 장비 주체다. 두 문제를 다음 단계의 동일 입력 trace에서 추적한다. 조건·순위·공유 cap 원인을 분리하며 core나 검사 분모를 바꾸지 않는다.

## 전수 로딩과 저장 보존

실제 source→loader→lexical/semantic index의 **112 슬롯 / 11,977 후보**를 대조했다. ID 중복·누락·라벨 변경은 0이다. semantic 문서는 12,013개이며 36개는 일반 슬롯 외 문서다.

모든 실제 EN·KO·명시 alias **40,380/40,380**이 production same-slot ranker에서 검색된다. cap 내 **40,148**, top1 **39,346**, top24 **40,339**이다. 이전 40,370개 동일 query 모두 유지되며 기존 cap 내 query 손실은 **0**이다. 이것은 source 자신의 문구로 주소를 찾는 검사이며 임의 자연어 요청의 의미 정확도나 모든 후보의 실제 public eligibility를 증명하지 않는다.

이 순수 same-slot 전수 조회는 마지막 일반 prop 보정 전에 실행했다. 최종 runtime에서 loader/index ID 정합성을 다시 확인했고, 전수 조회에 사용한 모든 slot 데이터와 semantic entry 12,013개, production ranker bytes, cap 함수가 동일함을 검증했다. 이후 바뀐 함수는 이 전수 조회가 호출하지 않는 `core_slot_focus_queries` 하나다. 최종 core retrieval 동작은 새 generation의 공개 CLI 48건으로 다시 검증했다. `final-inventory/exact-run-runtime.json`과 `EXACT-RUNTIME-REBINDING.json`에 두 generation을 구분해 기록했다.

기존 의미 문서·vector **12,008개**와 전체 visual payload **3,791개**를 보존했다. 새 일반 후보 5개와 중간 문구 보완 2건만 새 임베딩 계산 대상이었다. identity/full text/provider/model/dimensions/recipe가 일치할 때만 재사용했고, canonical semantic builder·visual check·dictionary validator가 통과했다. 이전 활성 semantic shard 16개도 SHA-256이 동일하다.

원본의 다른 tracked 수정 **22개**, 보호 source **210개**, Git index hash와 `main` HEAD를 보존했다. 두 checkout의 고정 48개 fixture와 owner 12개 입력도 동일하다. unrelated untracked 파일 전체의 hash 검증을 했다는 주장은 하지 않는다.

## 전체 테스트와 게시 상태

회귀 보정 전 전체 discovery 2088개를 모듈별 새 worker 8개로 실행했다. 실행 기록은 2004건이며 실패 33건, 오류 71건, skip 0건이다. collection/setup 실패로 모든 discovered case가 실행된 것은 아니다. 변경 전 단일 프로세스 실행은 1996건, 실패 28건, 오류 69건이다. 실패 parent selector 70개 중 64개는 기준선에서도 실패했다. 추가된 6개는 기존 source 보정 이력과 카메라 orientation 경로를 보존하는 수정 후 모두 통과했다. 최종 관련 검사 125건은 모두 통과했다. 영향받는 역사 source 모듈 3개와 source/metadata selector 6개의 검사 33건에서는 실패 2건, 오류 0건이었다. 두 실패는 기존 bundle 의미를 과거 snapshot과 비교하는 selector이며 기준선의 같은 selector에서도 같은 마지막 실패 메시지로 재현됐다. 최종 확인한 모듈에서 기준선에 없던 실패 parent selector는 0개다. 전체 suite는 green이 아니며 보정 후 전체 discovery를 다시 실행했다고 주장하지 않는다. 동일한 failed parent라도 모든 assertion/subtest 원인이 같다는 뜻은 아니다. checkout별 누락 artifact 경로, 최초 stale retained asset, narrative source diff 길이가 다른 사례를 별도 기록했다. 모듈 worker에서 collection 실패 모듈 이름이 축약되어 생긴 import wrapper 오류는 원래 discovery traceback과 구분해 보관했다.

구현은 `codex/slot-retrieval-stage05-subject-owner`의 격리 worktree에 있다. **이 단계의 commit/main merge/push는 하지 않았다.** 원본 main은 기준 `330fd9b548f5cc2282acd8655d360a23b78cd423`이며 실행 검증은 격리 store에서 했다. 원본의 사용 중인 private overlay나 default runtime를 이번 단계로 바꿨다는 주장은 하지 않는다.

generation: `3f6fe854a3fd1279c27c928aa65cf7d0e6d9c214ca29f520ca6bbed9297c6f79`
source fingerprint: `36a8c6e0374780d05351f2853fc46786b9f9e1aa2dd112320bc916df8c229593`
code SHA-256: `619549df14cebca754f5a76f292ce399852c847a651d209d4ffb926827b3ec0c`

단계 4의 `devanagari-sari-positive-en`·`thai-clothing-positive-en` 입력은 유지했다. 이 두 native EN 사례의 노출을 이번 단계에서 다시 판정하지 않았으며, 기존 순위·cap 증거를 다음 단계로 가져간다. 이 단계는 이미지 생성·native pixel·최종 composition·사용자 수용 검증을 수행하지 않았다.

재현 자료: `PLAN.md`, `NATURAL-FROZEN.json`, `CONTEXT-FROZEN.json`, `OWNER-FOCUS-FROZEN.json`, `qualified-natural/`, `qualified-context/`, `PUBLIC-VALIDATION.json`, `SEMANTIC-ADJUDICATION.json`, `NECESSARY-RETENTION.json`, `final-inventory/`, `EXACT-RETENTION.json`, `CONTROLLED-FINAL-METADATA.json`, `final-data-only-controlled.json`, `final-data-and-code-controlled.json`, `SOURCE-PRESERVATION.json`, `SOURCE-TRANSITION-SEAL.json`, `SOURCE-TRANSITION-VALIDATION.json`, `VECTOR-PRESERVATION.json`, `HISTORY-VALIDATION.json`, `INDEPENDENT-CURRENT-RECEIPT-VALIDATION.json`, `repaired-related-tests.json`, `repaired-source-history-tests.json`, `FULL-FAILURE-CLASSIFICATION.json`, 전체/기준선 로그와 실패 재현, `PRESERVATION-FINAL.json`, `VALIDATION-SOURCE-FREEZE.json`, `REVIEWED-SCOPE.json`, `SUMMARY.json`. 중간 수정 후 stale index로 실패하거나 종료한 실험은 최종 PASS에 합산하지 않았다.
