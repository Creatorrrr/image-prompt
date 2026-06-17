# photo-prompt-image-generator 아키텍처 분석 및 개선 제안

- 작성일: 2026-06-10
- 분석 기준(스킬의 의도): **"제공한 키워드를 중심으로, 어느 정도 연관성이 있는 범위에서 랜덤하게 프리셋과 키워드를 선정하여 이미지 생성용 텍스트 프롬프트를 만든다. 원하는 주제 범위 내에서 모순되지 않는 선에서 최대한의 창의성을 발휘하게 한다."**
- 분석 방법: 코드·데이터 직접 검증(라인 단위), git 이력 통계, 기존 eval/validation 인프라 점검

---

## 1. 현재 아키텍처 요약

### 1.1 컴포넌트 구조

```
사용자 키워드 / --concept / --intent
        ↓
generate_photo_prompt.py (1,379줄 — 래퍼)
  · concept_recipes.json 기반 컨셉 해석 (역할 + 믹스인 분리)
  · 믹스인/번들을 SHA256(concept|mixin|seed) 해시로 결정적 샘플링
  · 강제 슬롯(--set), soft anchor spec, intent axis로 변환
        ↓
prompt_generator.py (8,100줄 — 엔진)
  · 프리셋 선택 → 슬롯별 항목 선택 → 충돌 해결 → 렌더링
  · semantic 모드: Gemini 768차원 임베딩 코사인 유사도 + MMR + 온도 softmax
  · rule 모드: 가중치 추첨 (임베딩/API 불필요)
        ↓
prompt_en / prompt_ko / negative + provenance(prompt_id)
```

### 1.2 데이터 자산

| 자산 | 규모 | 역할 |
|---|---|---|
| `photo_prompt_tags.json` (3.4MB) | 74개 슬롯, 4,000+ 항목, 441개 프리셋, facet 어휘 14종 135개, coherence_rules, semantic_policy | 태그 사전 + 정책 |
| `concept_recipes.json` | 역할 105, 믹스인 92, 다양성 정책 63, 별칭 278 | 짧은 한국어 컨셉 → 생성기 인자 |
| `photo_prompt_semantic_index.json` (56MB) | 4,001개 항목 × 768차원 | 의미 기반 선택용 임베딩 |

### 1.3 모순 방지 메커니즘 — 이미 4개 층이 존재

흔히 "family 충돌 규칙뿐"이라고 생각하기 쉬우나, 실제로는 4개 층이 있다. **문제는 메커니즘의 부재가 아니라 데이터 커버리지 부재와 정밀 규칙의 하드코딩이다.**

| 층 | 위치 | 실제 사용량 |
|---|---|---|
| `family_conflicts` (소프트 페널티 0.38~0.62) | `prompt_generator.py:2136-2152`, `:2166-2213` | **horror 1개 family만 등재** |
| 항목 단위 페어 규칙 (`requires_any_tags` / `exclude_any_tags`) | `prompt_generator.py:5604-5695` | requires 125건 / **exclude 0건** (3,559항목 중) |
| facet 하드 가드 (`requires_facets` / `exclude_facets`) | `prompt_generator.py:1458-1495` | facet 보유 항목 211/3,559 (**6%**), 프리셋 1/441 |
| 슬롯 쌍 규칙 (headlights↔street, moonlight↔night 등) | `prompt_generator.py:5619-5656` | **Python 분기문에 하드코딩** — 데이터로 확장 불가 |

### 1.4 창의성/랜덤성 제어 레버 — 다층 분산

- 온도 = `novelty_settings`(`:1498`) × 프로필 `temperature_multiplier`(`SEMANTIC_PROFILE_CONFIGS:82-170`) × `SLOT_TEMPERATURE_MULTIPLIERS`(`:261`) — **3층 곱셈**
- 그 외 독립 축: `semantic_weight`(MMR 관련성/중복 균형), `filter_strictness`, 배치 다양성 페널티(`BATCH_DIVERSITY_CONFIGS:194`)
- 슬롯 점수 가중치(0.72/0.18/0.10, 0.36/0.12/0.24 등)는 `semantic_candidate_weight`(`:2671-2752`)에 리터럴로 하드코딩

---

## 2. 의도 대비 격차 분석

### 격차 1 — "모순되지 않는 선에서": 선언 불가능한 충돌 규칙

- "정오 + 달빛" 같은 슬롯 쌍 모순을 막는 코드는 이미 있으나(`:5619-5656`) Python 분기문이라 **새 충돌을 데이터 1줄로 선언할 수 없다.** 새 모순이 발견될 때마다 코드 수정 또는 `visual_guard` 사후 땜질로 대응 중.
- 검사가 단방향: 나중에 뽑히는 슬롯이 먼저 뽑힌 컨텍스트만 검사(`slot_pick_order:3951` 의존). 선택 순서에 따라 같은 모순이 잡히기도, 새기도 한다.
- 선언적 데이터 층(`family_conflicts`)은 horror 1건만 등재되어 사실상 비어 있고, facet 커버리지 6%가 정밀 규칙 작성의 실질적 병목.
- **임베딩은 이 문제를 풀 수 없다**: 코사인 유사도는 주제적 연관성이라 "noon"과 "moonlight"는 오히려 유사도가 높다(둘 다 시간·빛 개념). 모순 방지는 선언적 데이터에 의존할 수밖에 없다.

### 격차 2 — "연관 범위에서 랜덤하게": 컨셉 번들이 고정값 위주

의도는 "연관 풀에서 랜덤 선택"인데, 현재 컨셉 경로의 실체는 "고정값 강제"다.

- 컨셉 번들의 `set` 슬롯 값 606개 중 **592개(97.7%)가 단일 고정값**. 같은 컨셉이면 다양성은 번들 추첨(해시 샘플링)에만 의존.
- 풀 기반 경로는 **이미 절반 구현되어 있다**: `--concept-mode soft`(`generate_photo_prompt.py:26,689`)가 forced set을 pool 기반 soft anchor spec으로 변환하고(`:361-469`), 엔진은 가중치 승수 24/36/64배(`prompt_generator.py:76-78`, `apply_soft_anchor_bias:5512`)·확률 플로어·사후 리페어로 처리한다. `eval_semantic.py`에는 승격 게이트(`--quality-require-soft`, `evaluate_concept_benchmark:1023` — coverage ≥0.85 등)까지 준비되어 있다.
- 그러나 데이터가 미완성: `anchor_pool`은 역할 40/105, 믹스인 75/92에만 존재하고 **평균 풀 크기 1.77개**로 퇴화 상태. SKILL.md:98도 "벤치마크 통과 전까지 soft를 기본값으로 만들지 말 것"이라고 못박고 있다.
- 결론: **격차 2는 신규 설계 과제가 아니라 "이미 설계된 마이그레이션의 데이터 완성" 과제다.**

### 격차 3 — "최대한의 창의성": 레버가 분산되어 제어 불가

- 창의성을 올리려면 novelty, semantic-profile, semantic-weight, filter-strictness를 각각 이해해야 하고, 온도는 3층 곱셈이라 한 슬롯(`mood` ×1.28, `surreal_concept` ×1.34)의 실효 온도를 예측하기 어렵다.
- 점수 가중치·프로필·온도 배수가 코드에 하드코딩되어 **튜닝하려면 8,100줄 파일을 수정**해야 한다. 반면 `semantic_policy` JSON 섹션과 리더 함수(`semantic_policy_float:1125`)라는 외부화 선례가 이미 있고, `semantic_policy_hash` 분리 덕에 **정책 수정은 56MB 인덱스 재빌드를 요구하지 않는다**(검증 완료).

### 격차 4 — 의미 기반 연관성이 정작 컨셉 워크플로우에서 배제됨

- 56MB 임베딩 인덱스와 semantic 모드가 "키워드 연관 확장"의 핵심 자산인데, SKILL.md의 컨셉별 예시는 **rule 모드 19곳 vs semantic 4곳**으로 rule 편향.
- 모든 역할(105)·믹스인(92)에 `intent_axis`가 이미 정의되어 있어 의미 축 인프라는 컨셉에 연결되어 있으나, 슬롯 풀을 의미적으로 "넓히는" 경로는 없다 — 연관 확장은 사람이 anchor_pool에 손으로 적은 것이 전부.

### 격차 5 — 지식의 이중 관리: SKILL.md 비대화

- SKILL.md 926줄 중 **~470줄(L100–138, L213–596, L834–848)이 컨셉별 플레이북 프로즈**이고, 그 대부분은 `concept_recipes.json`에 이미 있는 필드(`safety_requirements`, `salience_cues`, `render_priority_terms`, `dual_read_requirement`, `forbidden_slot_values`, `concept_safety` 8종, `mixin_diversity_policy` 63종)의 사람용 재서술이다.
- git 이력으로 확인된 변경 핫스팟: 최근 SKILL.md 42회 > concept_recipes.json 34회 > prompt_generator.py 18회. **새 컨셉마다 프로즈가 수십 줄씩 누적되는 구조.**
- 데이터에 없는 유일한 지식은 검수 게이트("applied_mixins가 [흡혈귀] 하나인가", costume-swap 테스트 등)인데, `--explain-concept`(`generate_photo_prompt.py:1267-1284`)는 raw dump만 출력하므로 LLM 소비자가 926줄 프로즈와 수동 대조해야 한다.
- 영향: 스킬 소비 토큰 비용 증가, 데이터↔프로즈 불일치(doc rot) 위험, 컨셉 추가 비용 증가.

### 격차 아님 (잘 설계된 부분)

- **결정적 해시 샘플링**(`select_bundle_for_mixin:996-1005`): 동일 concept+seed → 동일 번들이라는 재현성은 가치다. 다양성 부족의 원인은 샘플링이 아니라 풀의 퇴화이므로, 비결정화가 아니라 풀 확장으로 풀어야 한다.
- **rule/semantic 이원화 자체**: rule 모드는 API 키·56MB 인덱스 없이 동작하는 오프라인/CI 경로로 존재 가치가 있다. 문제는 이원화가 아니라 컨셉 워크플로우의 rule 편향이다.
- **데이터 무결성**: `validate_photo_prompt_dictionary.py`의 recipes↔tags 교차 참조는 이미 강력하다(preset id, set 값, anchor_pool, forbidden_slot_values 등 대조).

---

## 3. 개선 제안 (우선순위 로드맵)

### P0 — 회귀 안전망: 골든 스냅샷 테스트 (노력 小 / 모든 후속 작업의 전제)

이후 모든 변경("출력 불변" 리팩토링, 데이터 이관)의 보험.

- rule 모드 + 고정 seed 케이스 20~40개(대표 프리셋 5×seed 2 + 대표 컨셉 15개 내외)의 `prompt_en`/`negative_en`/선택 슬롯 id를 `tests/golden/`에 JSON으로 저장. `provenance.prompt_id`(`stable_text_id`)가 결정적 해시를 이미 제공하므로 경량 체크섬 모드도 가능.
- **`--explain-concept` JSON도 골든화** — 완전 결정적이며 recipes 데이터 회귀를 가장 싸게 잡는다.
- semantic 모드는 임베딩 의존이므로 제외하거나 `eval_semantic.py`의 mock 인프라 재사용.
- 의도적 변경은 `--update-golden`으로 재생성하고 PR diff로 리뷰.

### P1 — 모순 방지 선언화: `slot_conflicts` 레이어 (의도 격차 1 해소)

기존 `coherence_rules`에 추가 키로 도입(additive — 키 부재 시 동작 불변):

```json
"coherence_rules": {
  "slot_conflicts": [
    {
      "id": "midday_vs_moonlight",
      "left":  {"slot": "time_of_day", "facets": ["time_context:midday"]},
      "right": {"slot": "lighting", "facets": ["light_source:moon"]},
      "severity": "hard",
      "penalty": 0.25,
      "symmetric": true
    }
  ]
}
```

- **hard**(후보 제외)는 `compatible_with_picked`(`:5661`)에서, **soft**(페널티)는 `semantic_coherence_factor`(`:2166`)에서 기존 이벤트/trace 패턴으로 처리. **양방향 검사**로 `slot_pick_order` 순서 의존성 제거.
- 하드코딩 규칙(`:5619-5656`)을 데이터로 이관, 전환기에는 `legacy_slot_context_rules` 플래그로 기존 경로 병행.
- **id 나열보다 facet 우선**: 4,000+ 항목 id 열거는 유지보수 불가. 모순 빈발 슬롯 ~10개(lighting, time_of_day, weather, location, action, subject, prop 등)에 facet 어휘를 보강하는 데이터 작업이 본체다(현재 커버리지 6%).
- 임베딩은 런타임 차단기로 부적합(유사도≠양립성) — `eval_semantic.py`에 "동일 facet 축 내 저공존·고유사 쌍" 감사 모드를 추가해 사람이 규칙으로 승격하는 **오프라인 큐레이션 보조**로만 사용.
- 검증: `validate_coherence_rules`(`validate_photo_prompt_dictionary.py:127`)에 slot/id/facet 실재 검증 추가, `eval_semantic.py`에 모순 골든 케이스 기반 `--contradiction-check` 추가.
- 리스크: hard 규칙 남발 시 후보 풀 고갈(`empty_candidate_pool` 폴백 `:5833-5848` 빈발) — **soft 기본, hard는 물리적 모순에만** 운영 규칙 필요.

### P2 — 컨셉 풀 확장: 고정 슬롯 → 풀+확률 (의도 격차 2 해소, 데이터 작업 위주)

1. **풀 확장**: 비정체성 슬롯(location, prop, expression, wardrobe_style)의 `anchor_pool`을 평균 ≥4개로 확장. 정체성 슬롯(costume_style 등)은 기존 `critical_anchor_slots`(`generate_photo_prompt.py:204`)로 좁게 유지.
2. **풀 내 가중치 스키마**: `anchor_pool: {"location": [{"id": "haunted_manor", "w": 3}, "foggy_forest"]}` — `anchor_pool_for_slot`(`:180`)과 `soft_anchor_pool_for_slot`/`apply_soft_anchor_bias`(`prompt_generator.py:4425/:5512`)에서 per-id 승수 반영.
3. **컨셉 단위 점진 승격**: 전역 기본값 전환 대신 recipe별 `"concept_mode_default": "soft"` 필드를 `resolve_concepts`(`:1013`)가 읽도록. 컨셉별로 기존 `--quality-require-soft` 게이트 통과 → 필드 부여 → 롤아웃.
- 동반 작업: 풀이 넓어지면 "선택 anchor 일치율" 메트릭(`minimum_soft_selected_anchor 0.60`, `SOFT_ANCHOR_SELECTED_RATE_FLOOR 0.80`)의 의미가 바뀌므로 **"풀 내 포함율"로 재정의**하는 eval 수정 필수.

### P3 — 창의성 레버 통합 + 매직넘버 외부화 (의도 격차 3 해소)

- `--creativity 0~1` 단일 레버 신설. 매핑을 단일 함수 `creativity_settings(c)`로 집중:
  - temperature = lerp(1.8→0.75), novelty_scale = lerp(0.05→0.45) 연속 보간
  - `SEMANTIC_PROFILE_CONFIGS` 3프로필을 c=0/0.5/1 앵커로 구간별 선형 보간, `BATCH_DIVERSITY_CONFIGS` 동일
  - **스코프 제한**: `semantic_weight`·`filter_strictness`는 창의성이 아니라 **정합성 축**이므로 초기 버전에서 제외 — 결합 시 상호작용 예측 불가가 현재 문제의 원인
  - 명시적 `--novelty`/`--semantic-profile`이 우선하며 trace에 기록
- 하드코딩 상수를 `semantic_policy` JSON으로 이관: `SEMANTIC_PROFILE_CONFIGS`(`:82-170`), `SOFT_ANCHOR_*` 5종(`:76-80`), `novelty_settings`(`:1498`), `RULE_POLICY_WEIGHT_MULTIPLIERS`(`:5382`). **코드 상수는 기본값으로 유지하고 JSON이 있으면 오버라이드**(`semantic_policy_float:1125` 패턴 재사용) — 구버전 사전과 하위 호환, 인덱스 재빌드 불필요.
- 검증: `eval_semantic.py --diversity-check`(`:1265`, `shannon_entropy:589`)를 creativity 0.2/0.5/0.8에서 실행 — 엔트로피 단조 증가 + coverage 유지 확인.

### P4 — 의미 기반 hybrid: anchor 풀의 임베딩 확장 (의도 격차 4 해소, 옵트인)

"연관 범위 내 랜덤"의 의미적 실체. soft anchor 풀의 각 멤버에 대해 동일 슬롯 내 임베딩 top-k 이웃을 풀에 추가:

- 설정: `soft_anchor_defaults`에 `"anchor_expansion": {"enabled": false, "top_k": 3, "min_similarity": 0.78}` (recipe별 오버라이드, 기본 off).
- 구현: `generate_once`(`prompt_generator.py:7376`)의 semantic context 생성 후 `expand_soft_anchor_pools()` 호출. 확장 멤버는 기존 24/36/64 아래의 별도 승수 티어(예: 12배)로 처리하고, **P1의 slot_conflicts·facet 가드로 사전 필터**(P1이 전제 조건).
- creativity 연동: c가 높을수록 top_k↑/min_similarity↓ — P3 매핑에 1항목 추가. `critical_anchor_slots`는 확장 제외(정체성 보호).
- 검증: `evaluate_concept_benchmark`에 확장 on/off 비교, `coverage_preservation_rate`(`:598`) ≥0.85 게이트.
- SKILL.md의 rule 편향 예시 19곳을 semantic/soft 예시로 재작성하는 문서 작업 병행.

### P5 — SKILL.md 다이어트: 플레이북의 데이터화 (의도 격차 5 해소)

컨셉 플레이북 프로즈는 정확히 4패턴의 반복: ①개념 정의/지배 축 ②시각 앵커 ③안전 규칙 ④검수 게이트. ②③은 이미 데이터에 있으므로 **이전 대상은 ①④뿐**:

```json
// concept_recipes.json mixins.흡혈귀 에 추가
"guide": {
  "definition_ko": "역할 보존 + 일광거부/거울이상/창백함 등 비유혈 앵커",
  "anti_patterns": ["generic gothic fashion", "blood/fangs/victims"]
},
"review_gates": [
  {"id": "mixin_shape", "machine_checkable": true,
   "assert": {"path": "applied_mixins", "equals_or_role_plus": "흡혈귀"}},
  {"id": "costume_swap", "machine_checkable": false,
   "check": "역할 의상을 평상복으로 바꿔도 앵커 2개 이상 잔존"}
]
```

- `resolve_concepts`가 `--explain-concept` 출력에 `guide`/`review_gates`를 포함하고, `machine_checkable: true` 게이트는 **자동 평가하여 `gate_results: pass/fail` 출력**. LLM 소비자는 926줄 문서 대신 게이트 결과와 manual 항목만 검토.
- 마이그레이션: 스키마 검증 추가 → explain 확장(P0 골든이 보호) → 컨셉 1개 파일럿(흡혈귀) → 2~3개씩 배치 이전, 배치마다 해당 SKILL.md 프로즈 삭제 → 카탈로그(L100–138)·예시 압축. 목표 분량 **~250줄(약 70% 절감)**.
- 보조: `validate_photo_prompt_dictionary.py`에 SKILL.md 리터럴(`--set slot=id` 등) 추출·대조, aliases 278건의 해석 가능성 검증, `--check-index`(스테일 인덱스 CI 검출) 추가.

### 구조적 한계 (점진 개선으로 해소 불가, 명시적 보류)

1. **prompt_generator.py 8,100줄 단일 파일**: 당장 분리는 비권장. 4개 스크립트가 `from prompt_generator import ...`로 ~20개 심볼을 쓰고, 래퍼와 테스트는 `spec_from_file_location` 단일 파일 경로 로딩이라 패키지화가 "복사만으로 동작하는 스킬" 속성을 깨뜨린다. 대신 **공개 API 동결 테스트 + 섹션 경계 주석**만 정리하고, "골든 정착 + 상수 외부화 완료 + 10k줄 초과 또는 스코어링 대개편" 시점을 분리 트리거로 정의.
2. **임베딩의 본질적 한계**: 어떤 의미 모델도 "정오+달빛 불가"를 직접 학습하지 않았다. 모순 방지는 선언적 데이터(P1)와 facet 어휘 투자에 의존한다.
3. **회귀 리스크의 실제 원인은 코드가 아니라 데이터·프로즈 변경**(커밋 비율 18:34:42). P0·P5가 리스크의 대부분을 해소한다.

---

## 4. 실행 순서 요약

| 순위 | 작업 | 노력(추정) | 해소하는 격차 |
|---|---|---|---|
| P0 | 골든 스냅샷(rule + explain-concept JSON) | 1–2일 | 후속 작업 전체의 보험 |
| P1 | slot_conflicts 선언 레이어 + facet 어휘 보강 + 하드코딩 이관 | 3–5일(데이터 작업 비중 大) | 격차 1 (모순 방지) |
| P2 | anchor_pool 확장 + 풀 내 가중치 + recipe별 soft 승격 | 컨셉당 0.5일 (데이터 위주) | 격차 2 (연관 범위 내 랜덤) |
| P3 | --creativity 레버 + 상수의 semantic_policy 이관 | 2–3일 | 격차 3 (창의성 제어) |
| P4 | 임베딩 기반 anchor 풀 확장 (옵트인) | 2–3일 (P1·P3 이후) | 격차 4 (의미 연관 활용) |
| P5 | SKILL.md 다이어트 + review_gates 자동평가 | 인프라 2일 + 컨셉당 0.5일 | 격차 5 (이중 관리) |

**의존 관계**: P0 → (P1 → P4), (P2, P3, P5)는 P0 이후 병렬 가능. P4만 P1(충돌 가드)·P3(creativity 연동)에 의존.

## 5. 핵심 수정 대상 파일

- `skills/photo-prompt-image-generator/scripts/prompt_generator.py` — slot_conflicts 평가(`:2136/:2166/:5604-5695`), soft anchor(`:4425/:5512`), creativity 매핑(`:1498/:82-170`), 풀 확장 훅(`:7376`)
- `skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py` — 컨셉 해석(`:1013`), anchor_pool 정규화(`:180`), concept_mode 기본값(`:688`), explain 게이트 자동평가(`:1267-1284`)
- `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json` — `coherence_rules.slot_conflicts`, facet_vocab 확장, `semantic_policy` 오버라이드
- `skills/photo-prompt-image-generator/assets/concept_recipes.json` — anchor_pool 확장·가중치, `concept_mode_default`, `guide`/`review_gates`
- `skills/photo-prompt-image-generator/scripts/eval_semantic.py` — `--contradiction-check`, soft 메트릭 재정의(`:1023-1075`), diversity 게이트(`:1265`)
- `skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py` — slot_conflicts·review_gates·aliases·SKILL.md 리터럴 검증(`main:1133`)
- `skills/photo-prompt-image-generator/SKILL.md` — 다이어트 대상 L100–138, L213–596, L834–848
