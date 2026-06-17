# soft 아키타입 배치 상세 개선안 (2026-06-11)

## 대상 산출물

codex 위임 실행으로 검증된 배치 `generated_prompts/idol-role-mixins-semantic-soft-20260611_154748/`
(8컨셉, semantic+soft, 시드 9101~9108) 및 이미지 6장(`generated_images/*-20260611_154748/`).
codex 자체 평가(evaluation.md)와 본 세션의 독립 시각 검토가 일치:
강한 통과 4(메이드 흡혈귀·간호사 얀데레·경찰 팜므파탈·공주 츤데레), 부분 통과 2(광부 악마·사복여친 천사),
미렌더 2(바니걸 멘헤라=sexual 차단, 고스로리 로봇=서버 오류).

## 근본 원인 진단 (산출물에서 실측)

| # | 증상 | 근본 원인 (코드/데이터 확정) |
|---|---|---|
| R1 | **8/8 케이스 subject 이탈**: 경찰→street_vendor, 공주→bottle_service_waitress, 광부→holographic_assistant_projection, 사복여친→young_actor 등 | `soft_anchor_defaults.anchor_slots`에 **subject 부재** — 역할 정체성 주어가 soft에서 자유 슬롯이 되어 의미 추첨으로 이탈. 게이트가 못 잡는 이유: 앵커 슬롯이 아니라 selected_anchor_rate 채점 대상 밖 |
| R2 | 공주 의상이 한복이 아닌 한푸/혼례풍으로 렌더, 광부의 분위기 지시 부재 | soft 분기(resolve_concepts)가 **safety_requirements만 전달하고 recipe `additional` 지시문 전체 누락** — 공주의 "Joseon court 지배·cheopji/binyeo" 문구, 광부의 "coal miner atmosphere" 문구가 프롬프트에 없음(04 프롬프트 실측: Additional에 safety 문구만 존재) |
| R3 | 프리셋 오프도메인: 광부 악마→`disembodied_ai_interface`, 메이드 흡혈귀→`obsession_wall_shrine_portrait`, 고스로리 로봇→`magician_misdirection_backstage` | soft는 프리셋 비강제 + `preset_affinity` 가중이 약해 의미 유사만으로 선택 |
| R4 | 광부 악마 이미지가 홀로그램/스캔라인 SF로 침식 | R1(홀로그램 subject)+R3(AI 프리셋)의 합성 + **악마 mixin에 render_suppress_terms 없음**(마법사의 tech-suppress 패턴 부재) |
| R5 | 사복여친 천사: 피사체가 매우 어려 보이고 다리 전면 셀피 — adult 플로어·anti-body-display 위협 | R1(young_actor subject) + 천사 결합에 body-framing 가드 부재 |
| R6 | 07/08의 앵커 미스 다수(expression/location/prop 풀 밖) | 배치가 soft 신뢰성 개선(앵커 enforcement·재주입·보상) **이전** 생성분 — 현행 코드로 재생성 시 해소(게이트 28/28로 입증) |
| R7 | 바니걸 멘헤라 sexual 차단 누적 7회(v5/v8/직접API/금회) | 무대의상+정서취약 결합의 시각 문법 자체가 이미지 필터 트리거 |
| R8 | codex exec에서 이미지 재시도 전부 DNS 실패 | exec 샌드박스가 외부 API를 차단 — 이미지 단계가 에이전트 환경에 종속 |

## 개선안 (우선순위순)

### A. soft 모드 보편 수정 (효과 최대)

**A1. subject를 soft 앵커 슬롯에 추가** — `concept_recipes.json`의 `soft_anchor_defaults.anchor_slots`에 `"subject"` 1줄 추가.
- 역할 set의 subject(nurse_role, police_officer_role, …)가 앵커 풀이 되어 enforcement로 풀 내 보장.
- R1·R4·R5의 직접 해소. 부수효과: 믹스인 subject(beastkin_subject 등)와 union 풀이 되어 둘 중 하나 선택 — 의도와 부합.
- 검증: 게이트 4런 재실행(soft 28/28 유지 확인) + 8컨셉 재생성에서 subject 정합 8/8.

**A2. soft 분기에서 recipe `additional` 지시문 전달** — `resolve_concepts`의 soft 분기(현재 `soft_safety_requirements`만 forward)에 역할/믹스인/번들 `additional`을 `--additional-requirement`로 함께 전달.
- additional은 서술 지침이지 슬롯 강제가 아니므로 soft 철학(강제 최소화)과 충돌하지 않음.
- R2 직접 해소(공주 anti-hanfu 문구 복원, 광부 분위기 문구 복원).
- 주의: 살리언스 예산과 별개 채널이므로 길이 증가 — `conditional_additional`은 explicit_user_set 조건 로직 재사용.

**A3. 프리셋 친화 강화** — soft에서 역할/번들의 `preset` id를 `preset_affinity.preferred`에 자동 포함하고 프리셋 점수 가중(예: ×1.5~2.0)을 semantic_policy 키로 노출. 최소 구현: 친화 프리셋이 후보에 있으면 확률 플로어(앵커 슬롯 플로어와 동일 패턴) 적용.
- R3 해소. 완전 강제가 아니므로 soft의 프리셋 탐색은 유지.

### B. 컨셉 데이터 보강

**B1. 악마 mixin에 `render_suppress_terms` 추가**: `hologram`, `holographic projection`, `scanline`, `AR interface`, `sci-fi HUD` — 마법사 mixin의 tech-suppress 패턴 준용(R4 보강).

**B2. 사복 여친 성인 명시·바디 가드**: (a) safety_requirements에 "mature adult woman in her twenties, age unambiguous" 명문화, (b) 천사 등 결합용 free_slot_constraints로 `subject_framing` waist_up 이상 고정 + 앉은 다리 전면 셀피 구도(deny) — R5의 데이터 측 방어선. likeness inspired는 유지.

**B3. 공주 negative 보강(보조)**: negative_prompt 풀에 "Chinese hanfu costume drift" 계열 1항 — A2가 주 해결책이고 이것은 이중 안전판.

**B4. 바니걸 멘헤라 재구성 과제(분석 후 결정)**: 완화가 아니라 *같은 의도(백스테이지 소진·취약)를 다른 시각 문법으로* — 후보: 가운/담요 오버레이 앵커 추가, costume 항목 en 표현에서 필터 트리거 어휘 점검, 거울 분장대 클로즈업(얼굴·손 중심) 프레이밍 강제. 차단 이력 7회의 공통 어휘 분석을 선행.

### C. 운영/워크플로우

**C1. 이미지 생성 스크립트 승격**: 세션 임시본(`eval_tmp/generate_direct_api.py`, gpt-image-2 직접 호출·무변형 보장·레저 기록)을 `skills/photo-prompt-image-generator/scripts/generate_images_via_api.py`로 승격하고 SKILL.md Default Workflow에 등재 — 에이전트 샌드박스(DNS 차단)와 무관하게 이미지 단계가 동작(R8).

**C2. 아키타입 배치 채점기**: beastkin 채점기 패턴으로 `subject-역할 정합`, `프리셋 도메인 정합`, `additional 전달 여부`, `body-forward 구도 금지`를 자동 채점하는 eval 추가 — 본 배치의 결함 4종이 전부 자동 검출 가능해짐.

### D. 검증 계획 (반영 시)

1. A1+A2 반영 → validator + 전체 pytest + 골든 재생성(설명 골든 변경 예상) → `--quality-gate --quality-require-soft --quality-runs 4` (soft 28/28 유지 + legacy 불변).
2. 동일 8컨셉 soft 재생성(시드 고정) → 채점: subject 정합 8/8, 프리셋 도메인 정합, 공주 프롬프트에 Joseon/hanbok 문구 존재, 광부 프롬프트에 SF 어휘 무.
3. 이미지 재생성(C1 경로) → 시각 검토 항목: 광부 악마의 underworld 우위(SF 침식 무), 사복여친의 성인·비바디포워드, 공주의 한복 정합, 07/08 렌더 여부.

### 우선순위 요약

**A1(데이터 1줄, 최대 효과) → A2 → B1·B2 → A3 → C1 → B3 → C2 → B4(분석 과제)**

---

# v2 — codex 강제 신규 실행(20260611_200153) 결과 반영 (최종)

## 신규 배치 결과 (새 시드 6111xx, 이미지 7/8 성공)

| 컨셉 | codex 판정 | 본 세션 독립 판정 | 핵심 관찰 |
|---|---|---|---|
| 메이드 흡혈귀 | pass | **pass** | 거울 반사 앵커 안정 재현(2배치 연속) |
| 간호사 얀데레 | partial | **fail에 가까움** | `pocket_tide_jar_portrait` 프리셋 드리프트가 렌더 지배 — **유리병 속 구름이 주인공**, 간호사복 희미, 얀데레 증거 부재 |
| 경찰 팜므파탈 | pass | pass | 봉투+복도 누아르 안정 |
| 광부 악마 | partial | **개선됨(partial+)** | 이전 SF 침식 해소. 뿔+왁스 봉인 두루마리로 악마 읽기 성립. 단 뿔이 **헬멧 장식**이라 decoration-absorption 경계 |
| 사복여친 천사 | pass | pass(-) | 다리 전면 구도는 해소, 그러나 크롭탑 복부 노출+연령 모호 잔존 |
| 공주 츤데레 | pass | pass(-) | 한복 정합 개선. 그러나 `product_packshot` 프리셋 침투 — **전경 스마트폰 거치대+상품 테이블**이 시대극 정합 훼손 |
| 고스로리 로봇 | pass | **strong pass** | 목 케이블·안면 기계·진단 환경 — 가이드의 deep/structural 앵커 모범 |
| 바니걸 멘헤라 | blocked | blocked | 3회 차단(누적 10회) |

## 신규 증거로 확정/추가된 사실

1. **R1(subject 이탈) 8/8 재현**: 간호사→researcher_role, 공주→fashion_influencer, 광부→influencer_creator… 두 배치 연속 100% 재현 — A1의 필요성 확정.
2. **R3(프리셋 드리프트)이 이미지 품질 훼손으로 직결됨을 입증**: 02(유리병 포트레이트), 06(제품 팩샷 문법 침투). 이전 배치에서는 "프롬프트 드리프트가 렌더에서 억제"됐지만 이번에는 그대로 침투 — **A3의 우선순위를 B군 위로 상향**.
3. **신규 관찰 — 악마 decoration-absorption**: 뿔이 헬멧 장식으로 렌더 — 로봇 가이드의 decoration-absorption 테스트를 악마 guide의 manual gate에도 추가할 것(B1에 병합).
4. **B2(사복여친 성인·바디 가드) 필요성 재확인**: 구도는 개선됐으나 크롭탑+연령 모호 — `wardrobe_style`에서 crop-top류 deny 또는 covered 풀 강제 추가.
5. **바니걸 멘헤라 누적 10회 차단**: B4를 "분석 과제"에서 "필수 재구성"으로 격상. 차단은 프롬프트 어휘 단계(입력 차단)이므로 costume_style(`bunny_girl_costume`)의 en 표현과 멘헤라 취약 어휘의 결합이 유력 — 표현 재작성(covered stage uniform 중심) + 백스테이지 가운 레이어 앵커.

## 최종 우선순위 (v2)

| 순위 | 항목 | 유형 | 기대 효과 |
|---|---|---|---|
| 1 | **A1** subject를 soft anchor_slots에 추가 | 데이터 1줄 | 8/8 이탈 해소, 02·04·05·06의 공통 원인 제거 |
| 2 | **A3** 프리셋 친화 강화(역할/번들 preset 가중·플로어) | 엔진+정책 | 02·06형 렌더 훼손 차단 |
| 3 | **A2** soft에서 additional 지시문 전달 | 래퍼 | 공주 anti-hanfu·광부 분위기 문구 복원 |
| 4 | **B2** 사복여친 성인 명시+커버드 wardrobe 가드 | 데이터 | 연령·노출 리스크 차단 |
| 5 | **B1** 악마 render_suppress + decoration-absorption 게이트 | 데이터 | SF 억제(이미 개선) + 뿔=장식 흡수 감시 |
| 6 | **B4** 바니걸 멘헤라 시각 문법 재구성(필수로 격상) | 데이터 | 10회 연속 차단 해소 |
| 7 | **C1** 직접 API 이미지 스크립트 정식화 | 운영 | codex 샌드박스 의존 제거(이번 런은 network_access 허용으로 우회 성공) |
| 8 | **C2** 아키타입 배치 자동 채점기 | 운영 | 결함 4종 자동 검출 |

검증 계획은 v1의 D와 동일하되, 채점 항목에 "프리셋 도메인 정합(컨셉당 허용 패밀리 화이트리스트)"과 "decoration-absorption(뿔/기계가 의상 장식으로만 읽히는지)" 수동 게이트를 추가한다.

## 반영 후 게이트 회귀와 후속 수정 (2026-06-12)

v2 반영 직후 품질 게이트(`--quality-require-soft --quality-runs 4`)에서 soft 실패 5런이
새로 발생했고, 분석 결과 모두 엔진의 보편 결함이었다. 세 가지를 수정했다.

### F1. intent steering의 앵커 풀 전멸 (윈터 간호사 얀데레 4/4 결정적 실패)
- 증상: `clinical-observation-semantic-policy-v1` steering이 location 후보를 424→1
  (`clinical_observation_lab`)로 좁혀 role 앵커 풀 5개가 가중·승격·enforcement에
  도달하기 전에 제거됨. 후보 1개라 4시드 모두 동일 실패.
- 수정: `steer_semantic_candidate_pool(slot, pool, context, anchor_ids=...)` —
  steering 결과에서 빠진 soft 앵커 풀 멤버를 보존(재합류)하고 decision에
  `anchor_preserved`/갱신된 `after`를 기록. 하드 가드의 앵커 면제,
  후보 컷 재주입과 동일 원칙의 보편 수정.

### F2. repair 계약과 게이트 플로어 불일치 (메이드 흡혈귀 mixin 1런)
- 증상: 게이트는 rate 플로어(role ≥0.90, mixin ≥0.80)인데 엔진 repair 트리거는
  count 플로어(`source_floors` 정수)만 봐서 mixin 3슬롯 중 1슬롯 미스(0.667)가
  repair 없이 통과 후 게이트에서 실패.
- 수정: `soft_anchor_match_status`에 소스별 슬롯 매치 rate 산출 +
  `DEFAULT_SOFT_ANCHOR_SOURCE_RATE_FLOORS = {role: 0.90, mixin: 0.80}`
  (spec `source_rate_floors`로 오버라이드). 미달 시 failure_reasons에 추가되어
  기존 repair 루프가 자동 발동.

### F3. 도메인 오분류 + contract 지연 차단 (jewelry diversity, 사전 존재)
- 증상 1: `infer_preset_domains`가 "cafe" 문자열만으로 food 도메인을 부여 →
  `maid_cafe_cosplay_portrait` 등 인물 프리셋 4종에서 hair/makeup/appearance/body
  슬롯이 `slot_applicability` deny로 차단. → food 신호에서 "cafe" 제거
  (실제 음식 프리셋은 food/street_food/pojangmacha/tteokbokki로 매치).
- 증상 2: subject 확정 전에 뽑힌 genre(beauty/portrait)가 subject_category=object
  확정 후 렌더에서만 억제(`render_suppressed_slots`)되어 jewelry diversity 케이스의
  억제율 0.3 > 0.25. → `reconcile_contract_blocked_picks` 신설: 슬롯 픽 완료 후
  contract 차단된 픽을 재선택(불가 시 드롭), `reselect_events`에
  `contract_reselected`/`contract_dropped` 기록. 억제율 0.3 → 0.0.

### 최종 게이트 결과
- qg_v2_final4: 컨셉 벤치마크 56/56 통과(soft 28/28), legacy_passed=True,
  soft_promotion_ready=True. 잔여 실패는 jewelry diversity(F3, 사전 존재) 1건.
- qg_v2_final5: F1~F3 반영 후 전체 게이트 **PASSED=True** — 컨셉 벤치마크 56/56
  (soft 28/28 + legacy 28/28), diversity 3/3, bleed 4/4, preset_guards·multi_axis 통과.
  사전 존재하던 jewelry diversity 실패까지 포함해 잔여 실패 0.
- 테스트: 304 passed (신규: steering 보존 2, source rate 플로어 3, 도메인 추론 2,
  reconcile 4). 골든 갱신 3건(메이드 2건 — hair/makeup 슬롯 복원,
  magazine_fashion seed42 — 억제되던 genre가 유효 장르로 재선택).

### F4·F5. 듀얼 정체성 컨셉(고스로리 로봇)의 앵커 도달성 (2026-06-12 추가)
게이트 벤치마크 밖 컨셉인 "아이유 고스로리 로봇"을 새 rate 플로어로 점검한 결과
6시드 중 5시드가 role 플로어 미달이었고, 두 가지 보편 결함을 추가 수정했다.

- **F4. 프리셋 도메인이 앵커 슬롯을 차단**: documentary 도메인 프리셋이 선택되면
  role 앵커인 makeup_style 슬롯이 `slot_applicability` deny로 통째로 스킵됨
  (repair는 거부된 슬롯을 채울 수 없어 영구 미달). →
  `preset_denied_anchor_slot` 신설: choose_preset 가드 패스에서 앵커 슬롯을
  도메인 거부하는 프리셋을 제외(거부 사유 `anchor_slot_domain:<slot>` 집계).
  레시피가 명시한 affine 프리셋 구출 패스에는 적용하지 않음(레시피 명시 우선).
- **F5. subject 선택의 앵커 도달성 look-ahead**: subject 슬롯에 role(인간 인형
  코스플레이어)과 mixin(세라믹 오토마톤) 앵커가 공존할 때, 오토마톤이 이기면
  subject_category=object가 되어 인간 전용 앵커 3개(costume/expression/makeup)가
  영구 차단. → `apply_anchor_reachability_guard` 신설: subject 후보별로 차단하게
  될 앵커 슬롯 수를 세어 **최소 차단 후보만 생존**(동수면 무필터, 전멸 방지 폴백).
  trace `reselect_events`에 `anchor_reachability_filtered` 기록.
  결과: 로봇 6시드 1/6 → 6/6 PASS, mixin 로봇 정체성은 유지
  (mixin rate 0.857, 프롬프트에 android/automaton/actuator 등 보존,
  로봇 전용 surface_material 1슬롯만 구조적 트레이드오프로 스킵).

### 최종 상태 (F1~F5 반영)
- qg_v2_final6: 전체 게이트 **PASSED=True** (벤치마크 56/56, diversity 3/3,
  bleed 4/4, preset_guards·multi_axis 통과).
- 아키타입 8종(r3, 시드 6121xx): C2 채점 8/8 PASS + 엔진 soft 계약 8/8 PASS.
- 테스트 311 passed (F4/F5 단위 테스트 포함).

## 바니걸 멘헤라 이미지 차단 분석 (2026-06-12, 레저 데이터 기반 — 신규 API 호출 없음)

run ledger의 바니걸 137건(성공 36 / safety_block 69 / error 32)을 대조 분석했다.
차단 사유는 전건 `sexual` 판정.

성공군 vs 차단군을 가르는 요인 (프롬프트 보유 105건 기준):

| 요인 | 성공군 | 차단군 |
|---|---|---|
| "no sexualized framing / no pin-up" 류 명시 가드 문구 | 0.50 | 0.09 |
| upper-body 크롭 | 0.25 | **0.71** |
| full-body(무대 전신 맥락) | **0.58** | 0.29 |
| head-and-shoulders 크롭 (B4) | 0.25 | 0.09 |
| legs 언급(전신 의상 맥락 동반) | 0.61 | 0.13 |

해석: ① 명시적 비성애화 가드 문구는 모델에 안전한 구도를 직접 지시해 가장 강한
성공 신호. ② 바니 코스튬 + upper-body 크롭 조합이 차단의 주 패턴(가슴 중심
프레이밍으로 읽힘). 전신 무대 맥락이나 두상 크롭은 통과 경향. ③ menhera 소품
(pill/wrist/bandage)은 성공·차단군 비율 차이가 작아 주 요인이 아님.

현 r3 프롬프트(07)는 가드 문구를 포함해 성공 프로파일에 가까우나 upper-body
토큰도 포함. **후속 조치는 사용자 결정 사항**: 사용자 지시("안전 목적으로
프롬프트를 완화하지 말 것")에 따라 구도 슬롯을 차단 회피 방향으로 기울이는
조치는 적용하지 않았다. 선택지: (a) 현행 유지+차단률 수용, (b) 구도 풀 가중만
조정(컨셉 어휘 무변경) 승인, (c) 다른 생성 도구/정책 티어 사용.
