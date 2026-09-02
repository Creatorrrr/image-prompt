# ReactorPrompt 증분 코퍼스 시각 의미·후보팩 강화 종합 리서치

- 상태: `proposed`
- 모드: 연구·설계 전용
- 조사일: 2026-09-02
- 대상 스킬: `skills/photo-prompt-image-generator`
- 비교 기준: 연구 시작 시 동결한 revision `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab` 및 아래 authored-source 해시
- authored-source snapshot commit: `401f450e4c0ec32ef79c502e3c6a6666c9a106c4` — 아래 source 해시가 정확히 재현되는 고정점
- 런타임 구현, 생성 인덱스 갱신, 신규 이미지 생성, 승격 판정: 수행하지 않음

## 결론

새로 수집한 ReactorPrompt 자료는 후보 단어를 대량 추가해야 한다기보다, 이미 풍부한 어휘를 **관찰 가능한 관계와 단일 소유권**으로 묶어야 한다는 근거를 준다. 16개 독립 주제에서 반복된 가장 큰 공백은 다음 다섯 가지다.

1. 장르·분위기·장비·렌즈·소재·감정 이름이 실제 가시 결과를 대신한다.
2. 동일한 장면 의미가 여러 슬롯에 중복되어 어느 레이어가 책임지는지 불명확하다.
3. 크롭·가림·해상도 때문에 검토할 수 없는 의무를 실패나 성공으로 잘못 판정할 수 있다.
4. 긴 negative 목록이 원인과 양성 목표를 설명하지 못한 채 누적된다.
5. 프롬프트 문구, 코퍼스 픽셀, 패키지 동작, 새 렌더, 사용자 판단이 서로 다른 증거층인데 쉽게 섞인다.

따라서 우선순위는 새 기본 스타일이나 광범위 hard profile이 아니다. 먼저 공통 `photo-visual-relation/v1` 메타 계약, 출처·소유자·관찰성 필드, 정확 활성화 가드, causal-pair/held-out fixture를 만든 뒤, 각 주제의 좁은 제안을 단계적으로 자격 평가해야 한다.

## 동결 근거와 조사 범위

| 항목 | 값 |
|---|---:|
| 증분 게시물 | 1,182 |
| 저장 이미지 | 4,908 |
| 비어 있지 않은 프롬프트 | 924 |
| 고유 프롬프트 본문 | 904 |
| 프롬프트 누락 | 258 |
| 게시물 ID | 1565–2746 |
| manifest SHA-256 | `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732` |
| gallery SHA-256 | `35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f` |
| translations SHA-256 | `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586` |
| visual obligations SHA-256 | `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc` |
| tags/candidates SHA-256 | `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00` |
| quality layers SHA-256 | `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f` |
| generated visual-profile index SHA-256 | `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626` |

각 주제는 924개 프롬프트 전수를 별도로 스캔했다. 16개 보고서의 표본 합은 게시물 검토 301회·이미지 검토 593회다. 이미지 표본은 빈도 추정용 무작위 표본이 아니라 양성·근접 대조·혼동 사례를 찾는 목적 표본이다. 같은 게시물과 이미지가 여러 주제에서 다시 검토되므로 이 합은 고유 파일 수가 아니다.

연구 시작 뒤 작업 트리에는 별도 작업의 런타임 변경이 존재했다. 이 리서치는 이를 기준선에 섞지 않았고, 새 산출물을 이 디렉터리 아래에만 작성했다. generated index는 authored source가 아니라 파생물로만 취급했다.

## 공통 진단

### 1. 명사 목록보다 타입형 인과 관계가 부족하다

장소 576개, 의상·소재 후보 수백 개, 카메라·필름·조명 표현 수백 건이 이미 존재한다. 추가 명사보다 다음 형태의 관계가 더 잘 재사용된다.

```text
source/provenance
-> owner axis
-> entities or visible regions
-> vector/contact/state/topology
-> visible effect or consequence
-> confusion negatives
-> observability and review scale
```

예를 들어 `85mm`, `iPhone`, `RAW`, `silk`, `confident`, `cinematic lighting`은 입력 라벨이나 힌트일 수 있지만, 각각 원근·캡처 응답·표면 거동·얼굴 동작·광원 인과를 자동으로 증명하지 않는다.

### 2. 정확 요청과 검색 발견은 다른 권한을 가져야 한다

- 요청자 또는 authorial core가 정확히 잠근 관계: request-scoped hard obligation 후보
- 기존 exact profile의 exact term: 현재 계약에 따라 hard activation 가능
- BM25F/embedding hit, 코퍼스 빈도, 장르 연상: advisory candidate만 가능
- 픽셀에서 우연히 보인 관계: 요청 의미로 역추론 금지

후보 검색 점수가 높아도 출처 문구와 exact activation 근거가 없으면 hard duty를 만들면 안 된다.

### 3. 관찰성은 품질 점수보다 먼저 판정해야 한다

각 의무에는 최소한 다음이 필요하다.

- `required_visible_regions`
- `minimum_review_scale`
- `crop_and_occlusion_policy`
- `proof_budget`
- `visibility_eligibility`

필수 영역이 프레임 밖이거나 가려졌거나 해상도가 부족하면 해당 축은 `UNSCORED`다. 보이는 일부 구성만 통과하면 strict profile에서는 `partial_is_fail`이다. 둘은 서로 다른 상태다.

### 4. 입력 메타데이터와 픽셀 효과를 분리해야 한다

- 렌즈 수치·조리개·센서·브랜드·RAW: 요청에 있으면 보존할 수 있는 입력 메타데이터
- 원근·왜곡·초점면·선명도 분포: 픽셀에서 검사할 가시 효과
- 소재·섬유·브랜드·가격: 단일 이미지에서 확정하기 어려운 라벨
- 광택 방향·파일/냅·직조/오픈워크·드레이프: 픽셀에서 검사할 표면 효과
- 관계·감정·직업·신원: 화면상 기하나 동작을 넘어서 추론하지 않는 비시각 주장

### 5. negative는 양성 관계의 대체물이 아니다

`no plastic skin`, `no waxy skin`, `no beauty filter`처럼 중복된 negative가 많아도 픽셀 결과는 크게 갈렸다. 자동 negative에는 좁고 의도 중립적인 결함만 남기고, 목표는 미세형상·국소 색·정반사·하이라이트 롤오프·경계 보존처럼 양성 구성요소로 작성해야 한다.

## 공통 메타 계약 제안

다음은 주제별 IR을 대체하는 새 만능 슬롯이 아니라, 각 IR이 공유해야 할 최소 메타 계약이다.

```json
{
  "schema": "photo-visual-relation/v1",
  "status": "advisory_or_request_scoped",
  "source": {
    "kind": "request_exact | authorial_core | reference_observation | advisory_candidate",
    "literal_evidence": [],
    "priority": "P0 | P1 | P2",
    "confidence": "high | medium | low"
  },
  "owner_axis": "one canonical owner",
  "entities": [],
  "visible_regions": [],
  "relations": [],
  "observable_effects": [],
  "confusion_negatives": [],
  "observability": {
    "required_visible_regions": [],
    "minimum_review_scale": "thumbnail | native | both",
    "crop_policy": "",
    "occlusion_policy": "",
    "ineligible_state": "UNSCORED"
  },
  "activation": {
    "hard_only_from_exact_source": true,
    "embedding_only_is_advisory": true,
    "all_required_components_coexist": true
  },
  "invariant_fields": [],
  "flexible_fields": []
}
```

주제별 카메라·조명·색·관계·재질 IR은 위 공통 필드를 공유하되, 실제 의미축은 각자의 단일 소유 레이어에 남아야 한다.

## 주제별 결과

| # | 주제·보고서 | 프롬프트 / 픽셀 표본 | 핵심 공백 | 제한된 제안 |
|---:|---|---|---|---|
| 1 | [구도·프레이밍](topics/01-composition-framing.md) | 924 / 20게시물·40장 | scale/placement 후보가 crop boundary와 panel topology를 소유하지 못함 | 기존 12개 exact 재사용, `crop_boundary_anchor_integrity`, `multi_panel_count_layout_sequence`, anchor/exit/forbidden-cut 필드 제안 |
| 2 | [포즈·신체 역학](topics/02-pose-body-mechanics.md) | 924 / 16게시물·32장 | 지지점·비지지 사지·접촉 역할·프레임 관찰성이 분리됨 | 새 exact 없음. broad 후보 3개, 기존 7개 보강, `contact_point` 라우팅과 일반 observability guard 제안 |
| 3 | [카메라·광학·초점](topics/03-camera-optics-focus.md) | 924 / 17게시물·34장 | 수치 렌즈·거리·투영·심도·초점 대상이 한 슬롯에 섞임 | `photo-camera-optics/v1`, `optical_coherence`; 수치 입력과 가시 효과를 분리하고 새 전역 optics exact는 만들지 않음 |
| 4 | [조명·노출·재질 반응](topics/04-lighting-exposure-material-response.md) | 924 / 20게시물·40장 | 분위기 라벨이 source–receiver–shadow–fill–material 인과를 대신함 | causal advisory records, `patterned_cast_shadow_receiver_continuity`, `daylight_fill_flash_balance_relation` 제안 |
| 5 | [색·화이트밸런스·톤](topics/05-color-palette-tone-grading.md) | 924 / 12게시물·24장 | 고유색·광원색·WB·전역/지역 grade·tone response 소유자가 섞임 | `color_effect_contract`와 exact 후보 3개; mixed-WB·rolloff·high/low-key·halation은 기존 profile 재사용 |
| 6 | [환경·깊이·대기](topics/06-environment-depth-atmosphere.md) | 924 / 32게시물·47장 | 장소 명사는 풍부하지만 subject–environment 역할, 독립 깊이 단서, 날씨 결과 사슬이 약함 | `subject_environment_role`, `depth_cue`, 3평면 깊이와 날씨-재질-피사체 결과 exact 후보 2개 |
| 7 | [피사체–소품 상호작용](topics/07-subject-prop-interaction.md) | 924 / 15게시물·30장 | 소품 존재와 접촉·하중·도구 사용·상태 변화가 분리됨 | `photo-object-interaction/v1`, coordinated advisory bundles, 기존 no-removal/no-transfer repair 경계 유지 |
| 8 | [다중 피사체 관계](topics/08-multi-subject-staging-relations.md) | 924 / 23게시물·43장 | 관계 라벨이 actor 수·시선·접촉·가림·공유 표적·반응을 대신함 | 주제 중립 `relation_graph`, 관계 exact 후보 4개, panel/crowd/off-frame camera 혼동 가드 |
| 9 | [표정·시선 가독성](topics/09-expression-gaze-readability.md) | 924 / 18게시물·36장 | 감정 동의어는 많지만 head/eye/local action/target/occlusion/readability 소유가 없음 | `photo-facial-display/v1`, `head_eye_counterorientation_relation`, 조건부 `facial_display_readability` |
| 10 | [의상·소재·드레이프](topics/10-wardrobe-material-drape.md) | 924 / 14게시물·28장 | garment/component/material/force/drape/proof scale가 평면 후보로 흩어짐 | `photo-wardrobe-material-relation/v1`, satin/velvet의 좁은 표면 exact 후보 2개 |
| 11 | [헤어·메이크업·피부](topics/11-hair-makeup-skin-beauty-capture.md) | 924 / 15게시물·30장 | 헤어 컷과 순간 상태가 섞이고 anti-plastic negative가 양성 구조 없이 누적됨 | `hair_motion_state`, `skin_microtexture`, `human_surface_response`, `wind_displaced_hair_coherence`; blanket negative 수입 거부 |
| 12 | [촬영 매체·처리](topics/12-capture-medium-processing.md) | 924 / 25게시물·50장 | 장비·브랜드·RAW 라벨이 근거리 기하·광원·신호·압축 응답을 대신함 | 조건부 `capture_response`, effect metadata; 기존 compact/flash/rolloff/halation 재사용, front-camera low-light는 advisory only |
| 13 | [서사 사건 타이밍](topics/13-narrative-event-timing.md) | 924 / 16게시물·29장 | 단계 단어·모션 블러가 actor/contact/cause/trajectory/consequence를 대신함 | 기존 `peak_action_event_phase` 재사용, 접촉 직전·이송 중·해제 후·수습·잔여 여파 advisory 후보 8개와 crop/cause/motion-owner gate 제안 |
| 14 | [negative·실패 예방](topics/14-negative-constraints-failure-modes.md) | 924 / 21게시물·42장 | semantic exclusion, 일반 결함, 요청된 artifact, profile-local substitute가 한 negative footer에 섞임 | `photo-failure-prevention/v1`, `photo-negative-term-policy/v1`, surface-local text mode와 조건부 `fp_*` gate; 새 broad artifact exact는 추가하지 않음 |
| 15 | [프롬프트 언어 아키텍처](topics/15-prompt-language-architecture.md) | 924 / 14게시물·28장 | payload role·출처·scope·polarity·variant가 없어 반복·모순·번역 drift·option branch를 구분하기 어려움 | `photo-prompt-clause-ledger/v1`, `photo-prompt-clause-consistency/v1`, `photo-corpus-prompt-lineage/v1`; 기존 budget 보강, 새 exact visual profile 없음 |
| 16 | [비인물 도메인](topics/16-nonportrait-domain-coverage.md) | 924 / 23게시물·60장 | 인물 우선 가정과 도메인 명사가 제품/음식/건축/자연/시스템/증거 관계를 대신함 | `nonportrait_subject_relation_budget`와 좁은 exact 후보 6개. 제품·음식·mode-split 자연은 proposed, 건축·증거는 revise, 시스템 기능 진실은 `UNSCORED` |

## 우선순위

### P0 — 모든 후속 구현보다 먼저

1. `photo-visual-relation/v1` 공통 provenance/owner/observability 계약
2. exact source와 advisory retrieval의 activation guard
3. `required_visible_regions`, `minimum_review_scale`, `UNSCORED` eligibility
4. 원본 prompt/image/hash와 사람이 확인한 관계 그래프를 잇는 fixture ledger
5. generated index 직접 편집을 막고 authored source에서만 재생성하는 lineage check
6. package, prompt, request, render, user evidence를 분리하는 결과 스키마

### P1 — 주제별 IR과 기존 후보 보강

1. 카메라 광학, 조명 인과, 색 효과 소유권
2. 객체 상호작용과 다중 피사체가 공유하는 actor/target/contact/response primitive
3. 구도 crop/panel topology와 포즈 observability
4. 환경 깊이·날씨 결과 사슬
5. 얼굴 동작, 의상 재질, 헤어 상태, 피부 미세구조
6. 촬영 매체의 label/effect 분리
7. 사건 단계 후보, 실패 예방 정책, clause ledger/lineage, 비인물 주체 관계 예산

### P2 — 좁은 exact profile 자격 평가

exact 후보는 코퍼스에 존재하거나 설계가 그럴듯하다는 이유로 바로 registry에 넣지 않는다. 먼저 정확 활성화/근접 음성 static test, composed-prompt causal pairs, 독립 held-out render를 통과시킨다. 중복 의미는 기존 profile을 재사용한다.

세부 기계 판독 목록은 [candidate-backlog.json](candidate-backlog.json)에 정리한다.

## 명시적으로 하지 말아야 할 변경

- 코퍼스 빈도만으로 글로벌 카메라·조명·색·피부·스타일 기본값 추가
- bare `85mm`, `iPhone`, `RAW`, `CCD`, 필름/브랜드명에서 픽셀 효과 자동 추론
- 모든 소품을 손에 들게 하거나 모든 두 인물을 관계 쌍으로 만드는 규칙
- crop/가림으로 보이지 않는 신체·피부·표면 detail을 PASS/FAIL로 강제
- `no plastic skin`, `no waxy skin`, `no beauty filter` 등 코퍼스의 긴 negative footer 수입
- 생성 인덱스 직접 편집
- 인물 중심 face-first 가정을 제품·음식·건축·자연·시스템 장면에 적용
- prompt/package PASS를 픽셀 성공이나 사용자 선호로 보고

## 구현 후 자격 평가 순서

```text
authored schema/static validation
-> exact/advisory routing causal pairs
-> composed prompt and request lineage audit
-> independent held-out generation arms
-> thumbnail first-read gates
-> native structural/detail gates
-> user judgment
```

- exact profile은 필요한 모든 gate가 같은 결과에 공존해야 한다.
- 구현 실패와 관찰 불가능은 각각 `FAIL`과 `UNSCORED`로 분리한다.
- 독립 arm은 입력·모델·설정·참조 역할을 고정하고 arm당 기록된 생성 1회, 재시도·cross-arm 입력 없이 평가한다.
- 사용자 미감·유사성·채택 판단은 마지막에 별도로 남긴다.

## 제한된 결정

이번 단계의 결정은 **`proposed`**다. 16개 주제 리서치는 시각 의미 데이터와 후보팩을 강화할 구조적 방향, 좁은 exact 후보, confusion negatives, gate, 회귀 설계를 제공한다. 그러나 대상 스킬의 런타임 데이터·코드·테스트는 변경하지 않았고, 새 후보팩 생성이나 composed-prompt 감사, 독립 렌더, 사용자 평가는 하지 않았다. 따라서 package/prompt/render/user 승격 상태는 각각 `not-run`, `not-run`, `UNSCORED`, `UNSCORED`다.
