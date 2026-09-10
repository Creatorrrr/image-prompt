# 수영복 데이터 반영 및 독립 3개 이미지 검증

상태: 데이터 구현 완료. 이미지 qualification 미달 — 3회 모두 생성 차단으로 픽셀 미평가.

- 기준 커밋: b6e70b787c083bbd9c472488875a028d28fbd2a8
- 65 selected visual profiles / 130 component gates / 65 new candidates / 88 optional bundles.
- 88 bundles = 65 single-variant bundles + 23 research combination bundles.
- 기존 high_rise_waist_navel_relation 재사용. 기존 후보의 body_geometry 차원 조건도 유지하므로 잠긴 차원을 침범하지 않는다.
- Racerback sports-bra의 특정 Y 요크를 일반 수영복으로 자동 전용하지 않아 연구 묶음 1개는 미이식.
- 내부 패드, UPF/기능, 섬유 조성, 시대, 모노키니 다의어, 브랜드 간 coverage 수치, bralette/balconette/underwire 명세는 broad hard profile로 만들지 않았다.
- 표면 후보는 선택한 관찰 가능한 변형이며 제조 공정이나 섬유 조성의 보증이 아니다.
- 인덱스: visual 502 profiles / 2007 exact terms; semantic 8443 entries. 모두 batch-size 1로 갱신했고 stale-source 검사 통과.

## 테스트 범위

각 에이전트는 fork_turns=none으로 시작하고 서로 다른 의복 범위와 독립 seed를 받아 core/testcase를 후보 데이터 열람 전에 고정했다. arm-01과 arm-02는 독립 추첨 결과 온실 수영장 계열 배경이 겹쳤지만, 투피스/원숄더 원피스와 물줄기/타월 사건 및 구조 게이트가 다르다. 서로의 컨셉을 보고 재선택하지 않았다. arm-03은 맹그로브 수역의 래시가드·서프보드 장면이다.

참조 이미지는 외형 참조로 사용하며 실제 인물의 신원은 추론하지 않는다. 각 arm native image_gen 1회, retry/fallback 0회. 후보 노출·채택과 픽셀 성공은 분리한다. 이번은 서로 다른 세 사례의 qualification이며 변경 전/후 같은 프롬프트의 대조 렌더는 아니므로 일반적인 개선 인과를 주장하지 않는다.

결과 산출물: artifacts/photo-runs/swimwear-three-arm-20260909/

## 독립 생성 결과

| Arm | 구조/사건 | 새 일반 후보·묶음 | 새 visual concept 노출/채택 | 감사 | 생성 | 픽셀 |
|---|---|---|---|---|---|---|
| 01 | 홀터 스트링 투피스, 홈통 물줄기 | 0 / 0 | sw_bikini 1 / 1 | composed/runtime PASS | input moderation blocked | not_run |
| 02 | 원숄더 랩 원피스, 타월 잡기 | 0 / 0 | 0 / 0 | composed/runtime PASS | output moderation blocked | not_run |
| 03 | 래시가드+별도 하의, 보드 회수 | 0 / 0 | 0 / 0 | composed/runtime PASS | output moderation blocked | not_run |

세 도구 응답의 보고 분류는 sexual이며 이미지 파일이 반환되지 않았다. 이는 사용자 사진 또는 요청의 의미가 그러하다는 판정으로 전용하지 않는다. 입력/출력 차단을 생성 시스템 결과로만 기록한다. 시각 품질이 좋다거나 나쁘다는 픽셀 판정은 불가능하다.

일반 후보 및 묶음의 실전 노출은 3개 arm 모두 0이었다. 인덱스에 등록된 것과 실제 공개 pack에서 발견·채택되는 것은 다르다. arm-01의 sw_bikini는 실제 opt-in 계약을 적용했으나 baseline에도 분리 구조가 이미 있었고 이미지가 없어 개선 인과를 입증하지 못한다. arm-02/03의 구조는 독립 core에서 온 것이므로 새 데이터 효과로 계산하지 않는다.

후속 과제는 노출 실패의 request/core relevance, preset/slot 범위, intent dimension gating을 분리 조사하는 것이다. 이번 검증을 통과시키기 위해 동결 core를 수정하거나 pack에 후보를 수동 삽입하지 않았다. 최종 결론은 implemented / not qualified이며 promote가 아니다.

arm-03은 pack 생성 셸 세션 관리를 놓쳐 같은 seed/core 명령을 두 번 시작한 사실을 보존했다. 이미지 호출은 1회이고, 대안 결과 선택이나 core 변경은 없었다.

## 코드 검증

- 수영복 전용 9개 테스트 통과: 완전 관계/부분 관계, 부정, 다의어, 독립 축, embedding-only authority, bundle member completeness, locked dimension gating, source hash, 실제 인덱스 포함.
- 사전 실행은 갱신 중 인덱스의 stale hash 오류와 테스트의 기존 후보 차원/부분 증거 기대 차이로 실패했다. 갱신 완료 후 테스트 전제를 수정했고 전용 9개를 다시 모두 통과했다. 제품 의무나 holdout을 약화하지 않았다.
- Dictionary metadata, visual profile stale hash, semantic index hash 검사 통과. Scene routes 112/112 통과.
- 전체 스위트 1128개 중 54개까지 실행해 12개 실패 확인. 같은 12개를 변경 전 b6e70b7 git-archive 사본에서 재실행해 12/12 실패 재현. 대상은 beastkin 2, golden snapshots 3, makeup dictionary 7이다. 전체 실행은 이 확인 후 중단했으며 전체 green 또는 full-suite 완료를 주장하지 않는다.
- 증거: checks/full-suite-status.json, checks/baseline-failures.log, checks/focused-tests.log.

## 노출 조건 추가 확인

실제 pack의 open_dimensions를 확인한 결과 세 arm 모두 appearance가 열려 있지 않았다(arm-02는 명시 locked, arm-01/03은 non-open). 신규 일반 후보 65개는 affected_dimensions=[appearance]이므로 해당 차원이 열려 있어야 public bundle에 들어가는 기존 정책이 작용한다. 이는 ordinary bundle 0의 확인된 제한 조건이며 모든 retrieval 경로의 유일 원인이라고 단정하지 않는다. visual concept는 별도 opt-in 경로라 arm-01의 sw_bikini만 선택될 수 있었다.

사용자는 에이전트가 테스트 컨셉을 정하도록 위임했다. 각 arm의 구체적인 의복 형태는 사용자 직접 지정이 아니라 독립 창작 선택이다. 이번 동결은 재현성 확보를 위한 테스트 설계였고, 그 결과 일반 후보의 변형 자유를 닫은 검증이 되었다. 후보 데이터의 추가 조합 효과를 검증하려면 별도 사전 설계에서 의복 차원의 열린 부분과 보존 부분을 명시해야 하며, 이번 사후 단계에서 이를 바꾸지는 않았다.

관련 회귀 중 test_prepack_visual_intent_is_hash_bound_and_source_grounded 실패도 기준 커밋에서 같은 chosen_visual_concept_ids 오류로 재현했다. 이 기존 테스트 기대를 이번 변경에서 수정하지 않았다. 전용 수영복 테스트의 통과와 관련 전체 회귀의 비정상을 구분한다.

관련 회귀는 총 계획 101개 중 완료된 65개 통과·1개 실패 상태에서 기존 라우팅 fixture의 추가 7개 실패를 확인했다. 이 7개 원본 fixture 행도 변경 전 사본에서 모두 실패 재현했다. 기존 실패 확인 후 나머지 관련 회귀는 중단했으며, 관련 스위트 전체 완료/통과를 주장하지 않는다. 상세 완료 범위는 checks/related-suite-status.json에 기록했다.

최종 검증 요약: 수영복 전용 9/9 PASS; metadata/index/scene audit PASS; 광범위 검사 non-green 및 부분 실행; 3 composed + 3 runtime audits PASS; generation 3/3 blocked; delivered image 0; pixel unscored; user judgment pending.
