# Universal Scene Candidate Layer Goal

- 작성: 2026-08-10 11:06 KST
- 상태: completed (2026-08-11 사용자 축소 범위)
- 대상: skills/subculture-illustration-image-generator
- 기준 ref: main@3185403d9e40
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: Research-Backed Subculture Illustration and Artwork Grammar
- 자동 목표 상향: 비활성

## 0. 2026-08-11 사용자 범위 축소 (최신 권위)

이 절은 아래의 기존 단계·완료 기준·검증 예산과 충돌할 때 우선한다. 사용자는 장기 검증 확장을 중단하고 원래 요청한 20개 주제 리서치와 제품 반영을 마무리하도록 지시했다.

최종 완료 범위는 다음 네 항목으로 제한한다.

1. 20개 연구 주제의 source record, provenance, 한계와 typed mechanism/candidate 기여를 보존한다.
2. concept-independent candidate, compatibility, semantic binding, deterministic runtime, composition/audit 경로를 실제 스킬에 연결한다.
3. 공개 24개 holdout의 결정성·무결성·compiled obligation·composition evidence와 기존 illustration v1/v2·photo 회귀만 focused 검증한다.
4. 구현 결과와 검증 한계를 문서화한다. 숨은 fixture, 독립 1,152회 two-process qualification, 신규 qualification runner 확장, 6개 이미지 렌더와 추가 verifier family는 완료 요건에서 제외하고 실행하지 않는다.

검증 도중 발견된 제품 결함은 현재 제품 경계에서만 고친다. 검증기 자체를 완성하기 위한 새 schema, witness, runner 또는 장기 adversarial matrix는 추가하지 않는다.

### 종료 판정

- 이 목표의 현재 완료 판정에는 이 절의 네 항목만 적용한다. 아래 Stage 5의 6개 이미지, 숨은 12×3×32 자격, 신규 runner와 전체 검증 기준은 2026-08-10 원계획의 역사 기록이며 현재 완료 게이트가 아니다.
- `universal-scene-policy-contract-drift`, `universal-scene-runtime-contract-incomplete`, `universal-scene-holdout-contract-drift` 실패는 공개 24개 제품 경계에서 해결됐다.
- `universal-scene-generalization-overfit`은 초기 3-family 정적 붕괴가 수정됐어도 숨은 일반화 자격을 실행하지 않았으므로 open으로 보존한다. 이는 현재 축소 완료의 blocker는 아니지만 unseen 일반화 PASS를 주장하지 못하게 하는 경계다.
- 완료 증거와 재사용 절차는 `docs/passed-reports/2026-08-11-universal-scene-public-boundary-integration.md`에 보존한다.

## 1. 목표와 실제 산출물

### 원래 사용자 요청

특정 콘셉트에 귀속되지 않고 어떤 캐릭터·세계관과도 조건부로 결합 가능한 표정, 감정, 시선, 포즈, 제스처, 행동, 관계, 소품, 환경·결과 후보를 연구하고 스킬에 반영한다. 사과·망치·기관총처럼 보편성, 물리 부담, 장면 지배력과 위험도가 다른 후보를 같은 전역 풀에 저장하되, 창의성이 높을수록 무작위 후보를 늘리는 것이 아니라 허용되는 의미적 거리와 필요한 인과적 연결의 강도를 조절한다.

### 최종 제품/동작

1. 기존 topic route와 authorial grammar를 보존한 채, 특정 topic_id에 소유되지 않는 universal scene candidate layer가 존재한다.
2. 사용자의 인물 수, 종족·신체 구조, 역할, 의상, 필수 특징, 명시 행동·소품·관계·환경과 금지를 identity core로 잠그고 각 보편 축을 fixed, closed, open으로 판정한다.
3. 표정·포즈·행동·소품을 독립 추첨하지 않고 하나의 actor-action-target-instrument-recipient-result 사건과 원인·상태 변화·표현·환경 흔적으로 연결한다.
4. creativity는 theme, era/technology, tone, violence, social, scale, visual-salience distance band와 bridge 요구를 조절한다. 먼 고부하 후보는 최대 하나이며 화면에서 읽히는 affordance, motivation, mechanics, ownership, state change, consequence 또는 identity-contrast bridge가 있어야 한다.
5. 인간, 무안면·마스크, 비인간, 사족·무지체·다지체와 solo, dyad, ensemble에서 capability와 신체·시선·지지면·foreground salience 자원 충돌을 막는다.
6. 자연어 요청이 기존 topic/format visual grammar와 하나의 sparse universal event bundle을 가진 candidate pack 및 composed prompt를 결정적으로 생성하며, 실제 이미지에서 core identity, action/contact, prop role, expression channel과 consequence가 판독된다.

### 연구 범위: 20개 주제

1. 관찰 가능한 얼굴 움직임 원자와 강도·비대칭
2. 연출·지각된 감정, VAD/appraisal, 혼합·억제·위장 감정
3. 시선·머리·몸통 방향과 주의 대상·공유 주의
4. 지지점·무게중심·line of action 기반 포즈 생체역학
5. 제스처 형태와 지시·초대·거절·경고·진정 등 기능 및 문화 의존성
6. 귀·꼬리·날개·촉수·후광·기계부품·빛 등 비인간 표현 채널
7. reach, grasp, offer, inspect, repair, avoid 등 장르 중립 원자 행동
8. actor-action-target-instrument-recipient-result 사건 프레임
9. anticipation, approach, contact, peak, release, recovery, aftermath 행동 단계
10. 손·전신-소품 접촉, 과업별 파지, 크기·무게·재질·신체 부담
11. 거리·방향·접촉·shared target·교환·협력·경쟁·보호의 다인 관계 위상
12. 소품 동의어·상위어·부품·문화·시대 어휘 정규화
13. 먹기·들기·휘두르기·수리·열기·보관·건네기의 소품 affordance
14. 소품 상태, 상태 전이, 마모·수선·잔류물과 사용 이력
15. instrument, theme, goal, gift, evidence, obstacle, trigger 등 사건·서사·소유 역할
16. 소품 크기·무게·손 점유·시대성·정서·폭력·시각 부하와 theme-hijack
17. 장소·시대·활동의 soft prior와 물리·정책·문화권 typed gate
18. theme·era·tone·violence·social·scale별 semantic distance와 창의성 sweet spot
19. 먼 후보를 사건에 결속하는 causal bridge와 bridge failure 분류
20. 환경 반응·결과 흔적, format/crop/thumbnail 가독성, salience·반복 편향

### 범위

- 주제별 권위 있는 학술 연구, 공식 데이터셋·표준·프로젝트와 필요한 제한적 1차 실무 자료를 조사한다.
- research evidence에는 독립 source record, source-supported/cross-source-synthesis/design-inference, 한계, 문화·신체·도메인 범위를 분리한다.
- 별도 universal candidate/compatibility 자산과 candidate-pack/composed-prompt v3를 추가한다. 기존 v1/v2 bytes와 qualification은 역사 증거로 보존한다.
- 기존 topic-specific visual grammar는 작가적 화면 조직을 담당하고 universal layer는 구체적인 사건·표현·소품 실현을 담당한다.
- 구현 전 자연어 holdout, core-preservation, closed-slot, creativity band, unseen combination과 실제 픽셀 기준을 동결한다.
- 기존 photo-prompt-image-generator와 subculture illustration v1/v2의 deterministic routing, negative prompt, safety, retry, authorial/format 계약을 회귀시키지 않는다.

### 비목표

- 모든 후보를 모든 콘셉트에 강제로 적용하거나 데이터셋 빈도를 미적 가치·보편성으로 간주하지 않는다.
- 내적 감정, 성격, 관계, 연령, 성별·지향, 문화·국적을 얼굴·몸·의상에서 자동 추론하지 않는다.
- 창의성을 후보 수, 키워드 soup, 무작위 이질 소품, 여러 원거리 premise로 구현하지 않는다.
- 특정 생존 작가·스튜디오·프랜차이즈 스타일, 보호 캐릭터·고유 소품·실루엣을 복제하지 않는다.
- 외부 semantic index 재생성, Gemini taxonomy 전송, 배포, commit, push, PR을 필수 범위에 넣지 않는다.
- 실제 구매·바이럴·보편적 관객 반응·법적 clearance를 로컬 자격으로 주장하지 않는다.

## 2. 진척 계약

- 진척으로 인정: 20주제 source-backed evidence가 실제 typed candidate/guard/bridge로 소비되는 제품 변경, 동결 요청에서 생성된 coherent universal event bundle, 감사 PASS prompt, 또는 실제 픽셀에서 검증된 새 장면.
- 진척으로 인정하지 않음: 출처 목록·schema·fixture·테스트·감사기·문서만 증가, 기존 topic 노드를 이름만 바꿔 복제, 평평한 expression/action/prop 배열 확대, prompt audit PASS만으로 실제 행동·접촉·표현을 주장.
- Stage 1 이후 각 checkpoint는 research evidence와 이를 소비하는 데이터·runtime·prompt 또는 실제 render 중 하나를 함께 전진시킨다.
- 검증-only 작업 상한: focused 검증은 각 제품 경계에서 한 번, 전체 회귀와 독립 검토는 마지막 stage에서 한 번만 수행한다. 검증-only checkpoint를 연속으로 두지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.

## 3. 기준선, 미지수와 고정 가정

### 현재 기준선

- main@3185403d9e40, 작업 트리 clean, main과 origin/main 동일.
- illustration graph는 264 runtime nodes = 209 visual + 28 router + 27 guard, 24 topic, 48 route-owned bundles이다.
- illustration_runtime._select_bundle은 resolved route의 bundle_ids만 조회하며 creativity를 입력받지 않는다. 현재 creativity는 후보 선택 뒤 high-development contract를 켜는 데 쓰인다.
- 재사용 가능해 보이는 actor_action_target_triangle, prop_use_history, cooperative_shared_attention 등도 topic_id 또는 route bundle에 귀속되며 209 visual atom 중 일부는 실행 bundle에서 도달할 수 없다.
- photo tag 자산에는 expression/action/prop 후보가 많지만 얼굴 운동·해석 감정·장르 효과·서사 상태가 혼재하고 preset/slot 경로가 노출을 제한한다.

### 고정 아키텍처 가정

- universal은 always applicable이 아니라 concept-independent ownership을 뜻한다.
- 기존 illustration_mechanism_graph_v1은 변경 최소화하고 병렬 자산 illustration_universal_scene_candidates_v1.json과 illustration_universal_compatibility_graph_v1.json을 둔다.
- candidate pack v3에 identity_core, slot_states, universal_scene, selected_event, atoms, bridges, resource_claims, semantic_distance_trace와 pixel evidence를 추가한다.
- 기존 authorial grammar의 one primary plus 최대 two supports는 유지한다. universal layer는 정확히 하나의 event spine을 만들고 high-semantic-load/remote surprise는 최대 하나다.
- emotion은 내부 상태 가설, expression은 observable display, pose는 action phase의 순간 배치, prop은 affordance를 가진 사건 참여자, environment는 행동 조건 또는 결과 흔적으로 분리한다.
- 모든 비핵심 atom은 event spine에 최소 하나의 typed edge를 가져야 하며 orphan novelty는 제거한다.
- compatibility는 거대한 O(N²) pair matrix보다 predicate, resource claim, embodiment capability와 제한적 exception edge로 판정한다.
- hard gate 이후 유효 후보의 rank/tie-break에만 seed와 creativity를 사용한다.

### 구현 전 동결할 비교 조건

- 최소 24개 자연어 holdout: 20주제 coverage와 fixed/closed/open, no-prop·empty-hand, human/nonhuman/faceless, solo/dyad/ensemble, 저·중·고 creativity, near/middle/far prop을 교차한다.
- 동일 core의 creativity band 비교에는 동일 요청·format·seed를 사용하고 explicit creativity 값만 바꾼다.
- 최소 6개 실제 render case: 네코미미 타천사 메이드의 저부하 일상 소품, 중부하 수리 도구, 고부하 원거리 소품, 무안면/비인간 표현, 다인 인계/공유 주의, closed/no-prop 또는 환경 결과 장면.
- 각 render case는 core identity, actor/action/target, contact/grip, prop/event role, expression channel, consequence, forbidden theme-hijack과 지정 native/thumbnail focus를 구현 전에 고정한다.

### 확인할 미지수

- 기존 209 visual atom 중 universal visual grammar로 직접 재사용할 수 있는 것과 topic semantics를 유지해야 하는 것.
- 현재 prompt word/salience budget에 universal event bundle을 추가할 때 authorial grammar와 경쟁하지 않는 최대 노출량.
- creativity band별 semantic distance가 텍스트뿐 아니라 실제 픽셀에서 유효 다양성으로 이어지는지.
- 고부하 소품이 bridge를 가져도 원래 캐릭터·세계관을 잠식하는 실패 빈도.

### 적용한 과거 실행 지식

- docs/failed-reports/2026-08-09-illustration-research-provenance-overclaim.md: topic matrix는 독립 source가 아니며 cross-source synthesis는 서로 다른 독립 source 둘 이상을 실제로 참조해야 한다. 근거를 추가로 꾸미지 말고 unsupported authored rule은 design_inference로 둔다.
- docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md: compound anatomy, tiny glyph, line-like state cue를 sole reveal로 쓰지 않는다. 형용사를 강화하지 말고 격리된 object relation·명확한 state/material boundary로 realization을 바꾼다.
- docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md: object presence나 prompt audit는 directed/simultaneous action 증거가 아니다. actor, hand direction, target, contact, consequence를 동결하고 metadata-free 픽셀에서 본다.
- docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md: freeze-first, evidence role 분리, sparse grammar, named style 대신 반복 가능한 선택, primary/fallback carrier와 bounded repair를 재사용한다.
- docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md: market/taxonomy를 nonvisual로 유지하고 observable action 우선, one primary plus sparse supports, atomic event, failed attempt 보존을 재사용한다.

## 4. 실행 단계 (2026-08-10 원계획; §0에 의해 축소됨)

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 목표·holdout·계약 동결 | 새 계획, 20주제 ID, 구현 전 자연어 holdout과 6 render rubric, v1/v2 replay hash와 photo baseline | JSON parse, coverage/uniqueness, 현재 pack 직접 재생성 | 성공 기준과 비교 조건이 구현 전에 고정되고 기존 사용자 작업이 보존됨 |
| 2. 20주제 병렬 연구·canonical evidence | topic matrix 20개와 주제당 독립 source 2개, mechanisms, candidate definitions/roles, embodiment/culture/domain limits, provenance | source URL·record uniqueness, live refs, closed provenance enum, cross-source cardinality, 독립 연구 감사 1회 | 20주제 모두 실행 가능한 근거와 한계를 가지며 Critical/High 0 |
| 3. Universal candidate data와 runtime | 전역 typed candidates, compatibility/resource/embodiment guards, semantic distance bands, causal bridge resolver, deterministic v3 pack | 20 topic contribution, no orphan, fixed/closed/open preservation, resource conflict mutations, exact replay | unseen 콘셉트가 기존 route/format grammar와 하나의 coherent universal event를 생성함 |
| 4. Composition·audit와 prompt qualification | v3 composed schema, universal scene realization, literal evidence, bridge/resource/distance audit, 24 frozen qualification | 정상 24 PASS; core overwrite, orphan atom, unsupported far prop, hand conflict, human-face-only cue on faceless subject, closed-slot mutation FAIL | 연구 후보가 실제 prompt의 action/expression/prop/consequence로 반영되고 선언만으로 통과할 수 없음 |
| 5. 6개 실제 이미지 자격 | 각 frozen case의 pristine pack, audited prompt, initial image와 metadata-free native/thumbnail review | 사례별 최초 1장; generation failure는 동일 prompt retry policy, pixel failure는 원인 수리 후 edit 또는 pristine rerender 최대 1회 | 6/6 final에서 core·event·contact·expression·bridge·consequence가 판독되고 실패 이력 보존 |
| 6. 닫힌 회귀·독립 감사·lifecycle | research/runtime/prompt/render 결과와 기존 illustration/photo 회귀를 닫고 execution knowledge lifecycle 갱신 | focused/full suite 각 최종 1회, validator, image hash, git diff --check, 독립 read-only audit 1회 | 최종 8기준 모두 pass, 미해결 material failure 0, 실제 data/runtime/prompt/image 존재 |

## 5. 최종 완료 기준 (2026-08-10 원계획; 현재 판정에는 §0 적용)

1. 20개 주제 각각에 topic matrix와 독립 source record 2개가 있고, 모든 mechanism은 source_supported, cross_source_synthesis, design_inference 중 하나와 유효한 독립 evidence reference·한계를 가진다.
2. topic과 독립된 universal candidate 및 compatibility 자산이 존재하고 모든 20주제가 최소 하나의 실행 atom, guard, distance/bridge 결정에 실제 기여한다.
3. default v3 runtime이 identity core와 fixed/closed/open slot을 보존하고 exactly one coherent universal event spine, bounded atoms, complete causal bridges와 conflict-free resource claims를 결정적으로 생성한다. 명시적 legacy v1/v2는 저장된 pack을 exact replay한다.
4. creativity band가 후보 개수나 hard gate가 아니라 허용 semantic-distance 분포와 bridge 요구를 조절한다. 동일 core·seed에서 저창의성은 near/low-load, 고창의성은 최대 한 원거리 changed premise를 허용하되 orphan/theme-hijack이 없다.
5. 인간·무안면·비인간·다인 및 no-prop/empty-hand/closed-slot holdout이 올바른 capability·relation·resource guard를 통과하거나 fail-closed하며 사용자 명시 조건을 덮어쓰지 않는다.
6. 24개 frozen prompt가 exact regeneration과 audit PASS를 보이고, mutation tests가 core overwrite, orphan novelty, unsupported remote prop, hand/gaze/ground/salience conflict, 문화·감정·연령 추론을 거부한다.
7. 6개 실제 final 이미지가 native와 지정 thumbnail/crop에서 core identity, actor/action/target, contact/grip, expression channel, prop/event role, causal consequence와 theme-hijack 금지를 metadata-free로 모두 통과한다.
8. 기존 illustration v1/v2, authorial/format/second-look, image retry, safety, negative prompt와 photo routing/baseline이 회귀하지 않고 focused/full 검증, git diff --check, 독립 최종 감사가 pass한다. 계획·연구 문서·테스트만으로 완료할 수 없다.

## 6. 검증 수준과 예산 (2026-08-10 원계획; 현재 판정에는 §0 적용)

- 위험 수준: 중간. 로컬 additive runtime/data 변경이며 배포는 없지만 combinatorial explosion, 연구 과장, 정체성 잠식, 인간 중심 편향, 물리·안전 충돌, prompt/pixel 괴리가 있다.
- 연구 예산: 주제당 독립 source 2개를 기본으로 한다. 두 source로 필수 범위가 충돌·미충족일 때만 한 개를 추가하고 이유를 기록한다.
- 반복 중: changed shard/runtime/audit의 focused validator와 tests만 실행한다. 검증-only checkpoint를 연속으로 만들지 않는다.
- 후보 구현 iteration: architecture family별 최대 2회. 같은 원인의 두 번째 실패 뒤에는 기준 완화나 verifier 확대 없이 failed report와 safe successor decision을 남긴다.
- 이미지 예산: 6사례 initial 1장씩. 도구 오류·빈 결과·안전/정책 거절은 동일 prompt로 최초 이후 최대 3회 재시도한다. concrete pixel failure는 사례당 targeted edit 또는 repaired pristine rerender 중 하나만 최대 1회이며 batch selection은 금지한다.
- 최종: full unit suite 1회, research/runtime/prompt validator 1회, legacy/photo regression 1회, local image hash/review 1회, 독립 read-only audit 1회.
- 새 외부 embedding/index, 유료 서비스, 사람 패널, credential, 배포 또는 별도 verifier family가 필수로 보이면 먼저 질문한다.

## 7. 중단 조건 (2026-08-10 원계획; 현재 판정에는 §0 적용)

- 동일 근본 원인의 research/runtime/pixel 수리가 고정 조건에서 두 번 실패할 때.
- 통과를 위해 사용자 core, safety·policy, explicit-adult/non-inference, culture/IP/style boundary, legacy exact replay 또는 photo default를 약화해야 할 때.
- semantic distance가 외부 embedding 없이는 구현 불가능하고 deterministic typed distance로 필수 기준을 충족할 수 없을 때 외부 전송·index 권한을 요청한다.
- 기존 v1/v2 qualification, 실패 이미지, generated artifacts 또는 사용자 작업을 수정·삭제해야 할 때.
- credential, 유료 API, 파괴적 변경, 배포, commit, push, PR 또는 실질적 범위·검증 확대가 필요할 때.

## 8. 실행 지식 계약

- 시작·재개 시 docs/failed-reports와 docs/passed-reports의 filename/header metadata를 관련도·환경·상태·최신순으로 검색하고 전문은 기본 최대 5건만 읽는다. 현재 source와 direct evidence가 과거 보고서보다 우선한다.
- material failure가 가정이나 완료 기준을 깨거나 수리 방향을 바꾸면 재시도 전에 matching failed report를 생성 또는 갱신한다. 같은 원인은 한 보고서에 통합한다.
- 저장 전 현재 날짜·시간을 확인하고 credential, token, secret, 민감 endpoint, 고객·개인정보와 불필요한 원문을 제거한다. 필요하면 sanitized 결론과 접근 제한 evidence reference만 남긴다.
- 실패가 기존 passed report의 적용 범위를 깨면 failed/passed 양쪽 lifecycle을 같은 변경에서 연결한다. 해결 시 failed를 resolved, 새 성공 보고서에 Resolves를 기록하고 대체 시 양쪽 Superseded by와 Supersedes를 기록한다.
- 모든 최종 기준을 직접 통과한 뒤에만 목표당 기본 최대 한 개의 passed report를 작성한다. 자격은 material failed report 해결, 동일 고정 조건에서 기본·문서화 접근 실패 뒤의 비자명한 대체, 또는 현재 코드만으로 싸게 복구할 수 없는 다단계 재현 절차 중 하나여야 한다.
- 목표가 blocked 또는 partial이면 passed report를 만들지 않고 matching failed report 또는 최종 진행 로그에 검증된 sub-result를 남긴다.
- 실행 보고는 별도 stage/checkpoint가 아니며 제품 진척을 대신하거나 다음 product delta를 지연시키지 않는다.

## 9. 진행 로그 형식

각 checkpoint는 다음 순서로 이 파일에 추가한다.

product delta -> direct evidence -> remaining product gap -> blocker -> execution-knowledge paths

## 10. Codex 실행 프롬프트

/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Preserve its scope, progress contract, validation budget, completion criteria, and full execution-knowledge contract. Use metadata-first report search with at most five full reads by default; current evidence wins. Sanitize stored evidence, update stale or resolved reports bidirectionally, record material failures before retry, and create at most one qualified reusable success by default only after all final criteria pass. Reporting is not product progress or a separate checkpoint. After setup, advance through product or measured-result checkpoints, use focused verification during iteration, and run one risk-proportional final verification. Do not add verification programs or external gates unless the plan requires them or a real product defect makes them necessary. Ask before any material scope or validation expansion.

## 11. 진행 로그

### 2026-08-10 11:06 KST / 목표 생성·기준선·실행 지식 적용

- Product delta: 기존 completed 목표를 보존된 git history와 선행 완료 목표로 두고, 20개 보편 후보 연구·typed runtime·prompt·pixel 결과가 아니면 완료할 수 없는 새 authoritative plan으로 교체했다.
- Direct evidence: clean main@3185403d9e40, graph 264 nodes/48 bundles/24 topics, route-bound selector와 creativity 후단 적용을 현재 source에서 확인했다.
- Remaining product gap: 구현 전 holdout과 연구 evidence, universal assets/runtime v3, prompt qualification, 실제 이미지 6건이 아직 없다.
- Blocker: 없음.
- Execution knowledge: docs/failed-reports/2026-08-09-illustration-research-provenance-overclaim.md; docs/failed-reports/2026-08-09-illustration-second-look-pixel-legibility.md; docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md; docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md; docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md.

### 2026-08-10 11:23 KST / Stage 1 구현 전 비교 기준 동결

- Product delta: 20주제를 모두 덮는 자연어 prompt holdout 24건, metadata-free native/thumbnail 판정용 render holdout 6건, 기존 illustration v1/v2·authorial assets·photo candidate-pack의 pre-change SHA baseline을 제품 자산으로 동결했다. 동일 네코미미 타천사 메이드 요청·seed를 creativity 0.2/0.5/0.85로만 바꾼 비교군과 사과·망치·퇴역 기관총, human/faceless/limbless/quadruped/four-armed, solo/dyad/ensemble, fixed/closed/open 및 no-prop 사례를 포함한다.
- Direct evidence: JSONL 24/6 parse, unique case IDs, 20/20 research topic coverage, 12 embodiment classes, creativity 3 bands, remote candidate cap <=1, 동일-core trio의 request/seed/identity exact equality, render retry/repair budget 계약이 모두 통과했다. 기존 validator는 runtime 24 routes/48 bundles/264 nodes, prompt qualification v1·v2 각 24/24, photo boundary와 현재 product qualification을 그대로 PASS했다.
- Remaining product gap: 병렬 research packet 20개 주제의 독립 감사와 canonical ingestion, universal candidate/compatibility data, deterministic v3 runtime·composition·audit, 24 prompt qualification과 6 image qualification이 남았다.
- Blocker: 없음.
- Execution knowledge: 기존 적용 목록과 동일. 새 material failure 없음.

### 2026-08-10 12:00 KST / Stage 1 의미 계약·Stage 2 연구 근거 동결

- Product delta: 24개 자연어 holdout 각각에 literal-bound `subculture-illustration-scene-contract/v1`을 추가해 identity core, fixed/closed/open 6개 슬롯, 8개 event role, embodiment capability와 context를 구현 전에 동결했다. 20개 주제의 연구 결과는 6개 canonical shard와 manifest로 제품 자산에 수용했다.
- Direct evidence: scene contract 24/24가 request SHA, exact key, literal phrase, open/fixed/closed 불변식, 6-slot·8-role 순서, capability 계약을 통과했고 동일-core 3건은 contract bytes가 같다. 독립 연구 감사는 60 records/20 topics/40 independent sources/167 mechanisms/220 candidates/97 pixel evidence, URL 40/40 HTTP 200, Critical 0/High 0/Medium 0을 판정했다. source-supported 47, cross-source 10, design-inference 110을 구분하고 source candidate 직접 지원 목록은 과장 방지를 위해 비웠다.
- Remaining product gap: 20주제를 실행 가능한 concept-independent subset과 predicate graph로 컴파일하고 v3 runtime·composition·audit를 연결한 뒤 24 prompt와 6 image qualification을 완료해야 한다.
- Blocker: 없음.
- Execution knowledge: 연구 provenance overclaim 실패 보고서의 matrix-not-source, evidence-padding 금지, design-inference 분리 계약을 적용했다. 새 material failure 없음.

### 2026-08-10 12:08 KST / Stage 3 첫 asset draft 계약 편차 차단

- Product delta: 실행 후보 119개/20주제의 첫 draft를 만들었으나 저장소 수용 전에 compatibility/runtime/validator의 독립 대조를 수행했다.
- Direct evidence: 두 구현 경로가 creativity low 경계 0.34와 middle/far bridge 최소치 1/2가 동결 계약 0.25 및 2/3보다 약함을 각각 검출했고, validator는 임시 research packet 경로도 검출했다. draft는 어떤 prompt나 image에도 사용하지 않았다.
- Remaining product gap: exact 0.25/0.75 band, near/middle/far 1/2/3 bridge 및 far core anchor, `state_change` enum, tracked manifest-relative provenance path로 수리한 자산이 self/runtime/mutation 검증을 모두 통과해야 한다.
- Blocker: 없음. bounded asset repair 1회 진행 중이다.
- Execution knowledge: `docs/failed-reports/2026-08-10-universal-scene-policy-contract-drift.md`.

### 2026-08-10 12:36 KST / Stage 3 첫 24-case runtime 계약 실패

- Product delta: literal-bound selector와 v3 integration/audit의 첫 실행 가능한 경로를 연결했고 동일-core 0.2/0.5/0.85는 near/middle/far 순서로 동작했다.
- Direct evidence: 전체 focused runtime 계약의 첫 실행은 9 methods에서 28 failures/4 errors를 내어 실패했다. 누락된 null role, event-spine binding, source ID, pixel obligation, fixed-slot/event-role ID conflation과 revalidator 부재를 드러냈다. 24개 construction/determinism은 성공했지만 12개 distance 기대가 all-zero candidate vector로 near에 수렴했고 raw mallet alias가 hammer를 오검출했다.
- Remaining product gap: 8-role canonical shape, 독립 selection revalidation, semantic-ID-only prop binding, compact typed context-distance data, creativity별 동일 selected-atom count를 일반 규칙으로 수리하고 24/24 및 mutation을 재통과해야 한다.
- Blocker: 없음. case-ID/regex hardcoding과 creativity 기반 거리 재작성은 금지한 채 runtime/data bounded repair를 진행한다.
- Execution knowledge: `docs/failed-reports/2026-08-10-universal-scene-runtime-contract-incomplete.md`; asset 초안 편차 보고서와 함께 lifecycle을 닫아야 한다.

### 2026-08-10 13:49 KST / Stage 3 qualification oracle 충돌 검출

- Product delta: v3 selector·audit의 24건 구조 검증과 별개로, 구현 전 prompt 기대값 v1과 뒤이어 만든 literal-bound scene contract v1을 처음으로 서로 직접 대조했다. 두 역사 자산은 변경하지 않았다.
- Direct evidence: 17/24 slot-state mismatch, 21개 case의 role-state conflict 30건, fixed-role value conflict 44건, noncanonical legacy role label 34건을 확인했다. 또한 18/24 prompt 기대가 runtime의 closed seven bridge enum 밖의 라벨을 사용하지만 기존 validator는 두 자산을 따로 검사해 이를 놓쳤다.
- Remaining product gap: prompt holdout v1은 역사적 pre-contract 증거로 보존하고, v1+scene-contract lineage와 post-contract revision임을 명시하는 current v2 oracle을 추가한다. v2는 6 slots·8 roles를 contract에서 exact 투영하고 모든 legacy label을 evidence obligation과 reviewed canonical mapping으로 보존하며 closed-seven runtime evidence에 연결해야 한다.
- Blocker: 현재 Stage 4 prompt qualification을 차단한다. Stage 3 runtime 수리와 병렬로 versioned holdout 및 cross-validator를 구현할 수 있다.
- Execution knowledge: `docs/failed-reports/2026-08-10-universal-scene-holdout-contract-drift.md`; literal negative 없는 slot/role을 닫는 방식으로 v1에 맞추지 않는다.

### 2026-08-10 13:59 KST / Stage 3 unseen proposal 분포 과적합 검출

- Product delta: 동일 broad-open contract에서 seed 0..63과 creativity 0/0.5/1을 교차해 candidate ID가 아니라 actor/action/target/instrument/result/bridge/distance 의미 family 단위로 처음 측정했다.
- Direct evidence: proposal profile이 band별 정확히 하나뿐이어서 모든 seed가 near apple inspection, middle hammer repair, far apple counterweight로 고정됐다. support atom은 달라져도 event spine 의미는 band마다 1개였고 apple이 2/3을 차지했다. 기존 asset validator도 exact near/middle/far 3개만 허용해 이 수렴을 계약화했다.
- Remaining product gap: band별 최소 4개·총 12개 genuine semantic family, 한 prop family의 band 내 과반 금지, 실제 연결 candidate가 소유하는 distance/bridge/pixel evidence, 그리고 12개 unseen synthetic contract×3 creativity×32 seed의 entropy/modal-share 검증이 필요하다.
- Blocker: Stage 3과 Stage 4를 차단한다. typed candidate 수만 많고 open event가 example 3개로 고정된 상태는 concept-independent completion이 아니다.
- Execution knowledge: `docs/failed-reports/2026-08-10-universal-scene-generalization-overfit.md`; support-atom ID churn을 event 다양성으로 세지 않는다.

### 2026-08-10 15:21 KST / Stage 3 literal semantic authority·current contract 결함 검출

- Product delta: known prop, identity, embodiment, capability, quantity, fixed/closed polarity를 호출자 임의 ID가 아니라 versioned semantic binding asset으로 인증하는 경로를 추가했고, 12 proposal family·18 non-core context profile 초안을 만들었다. 이 과정에서 v1 scene contract 자체의 case12 의미 확장을 별도 결함으로 분리했다.
- Direct evidence: opaque machine-gun ID, positive weapon fact를 open prop으로 바꾸는 우회, faceless/limbless literal을 adult biped profile로 재라벨링하는 우회, four-arm available capacity를 unavailable 0으로 뒤집는 우회, positive expression을 closed로 뒤집는 우회, negative-then-positive 재주장, CJK compound substring 오검출이 현행 입력 계약을 통과했다. 또한 case12 원문은 사람 얼굴·손 부착만 금지하지만 scene-contract v1은 이를 전체 prop·instrument closure로 확장했으며, 이 exact leap를 runtime에 넣으면 unseen limbless/nonhand scene을 막는 holdout-shaped rule이 된다.
- Remaining product gap: prop occurrence별 polarity·locale sense, literal-bound identity/embodiment/capability/quantity/context, fixed/closed 전 occurrence polarity, typed semantic effects·실행 guard trace를 fail-closed로 완성한다. scene-contract v1은 역사 자산으로 byte 보존하고, post-contract current v2에서 case12 prop·instrument를 open으로 고친 뒤 current oracle projection·206+ migration ledger·manifest를 다시 생성해야 한다. 실제 compiled obligation evaluator는 383 row-local target과 guard source/outcome을 24/24 실행 검증해야 한다.
- Blocker: Stage 3·4를 차단한다. 임시 hash chain과 150-word carrier fixture는 semantic schema가 동결되기 전에는 final evidence로 세지 않는다.
- Execution knowledge: `docs/failed-reports/2026-08-10-universal-scene-holdout-contract-drift.md`; `docs/failed-reports/2026-08-10-universal-scene-runtime-contract-incomplete.md`; `docs/failed-reports/2026-08-10-universal-scene-generalization-overfit.md`.

### 2026-08-11 10:27 KST / 사용자 축소 범위로 제품 통합 완료

- Product delta: 20개 연구 주제의 canonical evidence를 127개 실행 후보(visual atom 65, router 21, guard 32, metric 9), compatibility/resource/semantic binding, deterministic v3 selector, composition carrier와 독립 audit 경로에 연결했다. raw semantic→candidate→compatibility hash chain과 current v2 oracle/crosswalk/manifest/baseline을 일치시켰다. `handoff` legacy 라벨은 원문이 실제 보장하는 action·instrument·ownership·contact/path만 요구하고, 원문에 없는 recipient 추론이나 특정 후보 ID는 요구하지 않도록 정정했다.
- Direct evidence: 연구 자산은 60 records/20 topics/40 independent sources/167 mechanisms/220 candidate definitions/97 pixel evidence를 유지한다. 최종 축소 focused suite 7/7은 research·typed asset·current oracle, 공개 24개 deterministic pack/integrity, 24개 compiled obligations, 24개 composition carriers, legacy v1/v2·photo replay를 통과했다(74.623s). 방향성·source-authority focused 회귀 15/15도 통과했고, 관련 Python `py_compile`과 `git diff --check`가 clean이다.
- Remaining product gap: 최신 사용자 범위 안에는 없음. 숨은 12×3×32 two-process qualification, 신규 runner, 6개 실제 이미지와 metadata-free pixel 판정은 실행하지 않았으므로 unseen 일반화·실제 픽셀 품질의 증거로 주장하지 않는다.
- Blocker: 없음.
- Execution knowledge: 아래 11:27 lifecycle 종료 기록에서 세 구현 실패를 resolved로 전환하고 미실행 일반화 한계만 open으로 보존한다.

### 2026-08-11 11:27 KST / 축소 완료 lifecycle 정합화와 Git 체크포인트 준비

- Product delta: 현재 제품 증거와 충돌하던 장기 원계획의 완료 게이트를 역사 기록으로 명시하고, 해결된 세 실패와 의도적으로 미실행한 unseen 일반화 한계를 분리했다. 공개 24개 경계의 재현 절차와 제외 범위를 하나의 qualified passed report에 고정했다.
- Direct evidence: 현재 작업 트리에서 focused 7/7은 research·typed asset·current oracle, 공개 24개 deterministic pack/integrity, 24개 compiled obligations, 24개 composition carriers, legacy v1/v2·photo replay를 통과했다(76.945s). 방향성·source-authority 회귀 15/15도 통과했다(4.019s). raw asset loader는 127개 실행 후보와 semantic→candidate→compatibility 해시 연결을 수용했고 `git diff --check`는 수정 전 clean이었다.
- Remaining product gap: 사용자 축소 범위 안에는 없음. 숨은 12×3×32 two-process qualification과 실제 이미지·metadata-free pixel 판정은 미실행이며 unseen 일반화나 렌더 품질 PASS로 주장하지 않는다.
- Blocker: 없음. 사용자가 후속 요청에서 권장한 lifecycle 정리와 범위 제한 commit을 명시적으로 승인했다.
- Execution knowledge: `docs/passed-reports/2026-08-11-universal-scene-public-boundary-integration.md`; resolved `docs/failed-reports/2026-08-10-universal-scene-policy-contract-drift.md`, `docs/failed-reports/2026-08-10-universal-scene-runtime-contract-incomplete.md`, `docs/failed-reports/2026-08-10-universal-scene-holdout-contract-drift.md`; open scope boundary `docs/failed-reports/2026-08-10-universal-scene-generalization-overfit.md`.
