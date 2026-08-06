# Photo Prompt Creative Discovery Goal

- 작성: 2026-08-06 16:53 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 권위 문서: 이 파일이 목표의 범위, 완료 기준, 중단 조건을 정의한다.

## 1. 목표와 실제 산출물

기본 생성 결과와 기존 회귀 계약을 그대로 보존하면서, 사용자가 명시적으로 선택할 수 있는 창의 탐색 경로를 제공한다. 이 경로는 관련성을 잃지 않은 더 다양한 candidate pack 대안과 대표 role의 복수 atomic scene을 노출해, 같은 주제에서도 구조적으로 다른 사진 콘셉트를 만들 수 있게 해야 한다.

실제 산출물은 다음 네 가지다.

1. 선호 wrapper와 스킬 문서에서 발견하고 사용할 수 있는 창의성 옵션.
2. 서로 다른 주제군을 대표하는 role 10개의 `identity_core + scene_variants` 전환.
3. 기존 eligible pool 안에서만 작동하는 deterministic opt-in candidate 다양화.
4. 기본 경로 보존과 창의 경로의 실질적 구조 다양성 증가를 입증하는 회귀·holdout 증거.

## 2. 진척 계약

- 첫 checkpoint에서만 기준선과 pilot 범위를 고정한다.
- 이후 각 checkpoint는 반드시 사용자 또는 런타임이 관찰할 수 있는 기능 변화, 측정 가능한 후보 변화, 또는 다음 구현 방향을 구속하는 결정을 포함한다.
- 연속된 verification-only checkpoint는 허용하지 않는다.
- 검증 도구는 기존 테스트와 evaluator를 우선 재사용하며, 제품 변화보다 큰 별도 평가 시스템을 만들지 않는다.
- 범위나 목표 수치는 도중에 자동으로 상향하지 않는다.

## 3. 현재 기준선과 미지수

현재 확인된 기준선:

- `--creativity`는 엔진에 구현되어 있고 wrapper를 통해 전달되지만 스킬의 주 사용 흐름에서 발견하기 어렵다.
- role recipe 105개 중 `identity_core + scene_variants` 구조는 2개뿐이다.
- narrative/material/temporal 관련 slot은 존재하지만 preset/recipe 도달성이 낮은 축이 있다.
- candidate pack은 relevance 순위 중심의 고정 상한을 사용하며, 명시적인 다양성 대안은 제공하지 않는다.
- semantic index는 `slot`, `preset`, `virtual_preset` entry를 가지며 family centroid는 사전 계산되어 있지 않다.

첫 checkpoint에서 확정할 미지수:

- 대표 role 10개의 정확한 목록과 각 role에 재사용 가능한 기존 slot ID.
- 고정 fixture에서 candidate pack의 구조적 중복도 및 opt-in 후보 개선 목표치.
- opt-in API를 별도 flag로 둘지 기존 `--creativity`의 명시적 고구간에 결합할지 여부. 기본 출력 byte parity가 더 명확한 별도 flag를 우선 검토한다.

## 4. 실행 단계

### Stage 1 — 기준선과 pilot 고정 (`completed`)

- 현재 dictionary, candidate-pack 경로, wrapper 전달, 테스트 surface를 재확인한다.
- 고정 seed와 대표 intent로 role 구조 비율, scene 다양성, candidate 구조 중복도를 측정한다.
- 기존 ID만으로 atomic scene을 만들 수 있는 서로 다른 주제군의 role 10개를 확정한다.
- 산출물: 이 문서의 진행 기록에 기준선, pilot 목록, 구속 결정을 남긴다.

### Stage 2 — 사용자가 발견할 수 있는 창의 탐색 경로 (`completed`)

- 스킬 주 사용 흐름에 `--creativity`의 의미, 재현 가능한 예시, 보수적/균형/탐색적 선택 기준을 추가한다.
- 실제 data와 불일치하는 quality-profile 문서를 바로잡는다.
- opt-in candidate 다양화의 CLI 계약을 확정하고 help/wrapper 경로에 노출한다.
- 제품 delta: 사용자가 소스 코드를 읽지 않고 창의 경로를 선택할 수 있다.

### Stage 3 — 대표 role의 복수 atomic scene (`completed`)

- 대표 role 10개를 `identity_core + scene_variants`로 전환한다.
- role당 최소 2개 scene을 두고, 한 variant 안에서 별개의 활동·장소·시간을 합치지 않는다.
- 기존 slot ID만 재사용하고, identity는 seed가 달라도 유지되며 scene 하나만 선택되도록 한다.
- 제품 delta: 같은 role이 정체성을 유지하면서 서로 다른 사진적 순간으로 회전한다.

### Stage 4 — relevance-preserving candidate 다양화 (`completed`)

- 명시적 `--creativity 0.75..1.0`일 때만 candidate pack에 deterministic contrast guidance를 포함한다.
- 대비 후보는 이미 노출된 sampler의 정확한 eligible pool에서만 고르며 conflict, theme-family, required-slot, safety 계약을 우회하지 않는다.
- relevance와 기존 선택을 anchor로 유지하고, 구조적 facet/term 거리가 충분한 후보만 `creative_exploration.contrast_candidates`로 표시한다.
- 기존 후보 membership·순서·sampler 선택은 재정렬하지 않는다. 기준선에서 lexical 중복이 낮았으므로 전면 MMR은 적용하지 않는다.
- creativity가 없거나 0.75 미만이면 해당 필드를 내보내지 않고 기존 candidate pack을 그대로 보존한다.
- 제품 delta: 후보팩이 관련성 손실 없이, 실제로 선택 가능한 대비 지점을 agent에게 명시한다.

### Stage 5 — holdout 통합과 최종 자격 판정 (`completed`)

- role scene 회전, opt-in 다양화, theme 누출 방지, default parity를 고정 fixture로 검증한다.
- 기존 dictionary validator와 집중 테스트 후 전체 테스트를 한 차례 실행한다.
- 목표 기준을 통과한 경우에만 완료 처리한다. 프롬프트 구조 품질까지만 주장하며, 유료 이미지 생성 없이 렌더링 품질 향상은 주장하지 않는다.

## 5. 완료 기준

1. 선호 wrapper와 `SKILL.md`에서 창의성 경로와 재현 가능한 사용 예시를 바로 찾을 수 있다.
2. 서로 다른 주제군의 role 10개가 `identity_core`와 최소 2개의 atomic `scene_variants`를 가지며 dictionary validation을 통과한다.
3. 고정 seed 집합에서 각 pilot role은 identity를 유지하고 둘 이상의 scene variant에 도달한다.
4. `--creativity 0.75..1.0`의 opt-in contrast guidance는 동일한 eligible pool과 기존 계약 안에서 qualifying pack마다 최소 하나의 relevance-preserving 대안을 표시하며 deterministic하다.
5. pilot fixture에서 opt-in contrast coverage가 기준선 0보다 증가하고, 표시된 후보의 선택 결과 대비 feature distance가 정한 floor를 만족하며 theme leakage와 candidate-contract failure는 0이다.
6. creativity 미지정 경로의 candidate-pack algorithm과 기존 golden fixture는 기준선과 동일하며, pilot role의 의도된 scene 회전 외에 rule mode의 명시적 요청어 우선순위도 유지된다.
7. 관련 집중 테스트, dictionary validator, 기존 semantic/generalization gate, 전체 단위 테스트가 통과한다.
8. 외부 모델 전송, semantic index 재생성, 유료 이미지 생성 없이 완료된다. 필요해지면 자동 진행하지 않고 중단 조건으로 처리한다.

## 6. 검증 전략

- 변경 전: 고정 seed candidate pack과 role scene 도달성을 기록한다.
- Stage 2–4: 변경 영역별 기존 단위 테스트와 최소 신규 fixture를 실행한다.
- 최종: dictionary validator → 집중 candidate/scene/creativity 테스트 → 기존 semantic/generalization gate → 전체 `unittest` 순서로 한 차례 닫힌 자격 판정을 수행한다.
- 성능은 고정 fixture의 반복 실행으로 전후를 비교하되, 환경 잡음을 감안해 명백한 퇴행만 차단한다.
- 이미지 API 기반 visual review는 완료 기준에 포함하지 않는다.

## 7. 실패·재시도 계약

- 같은 실패 원인에 대한 구현 재시도는 최대 3회다.
- material failure는 재시도 전에 `docs/failed-reports/`에 sanitized evidence와 함께 기록한다.
- 세 번째 시도 뒤에도 해결되지 않으면 목표를 임의 축소하지 않고 현재 증거와 다음 안전한 선택지를 보고한다.
- 단순 오타, 즉시 수정되는 로컬 테스트 실수, 비결정적 일시 오류는 material failure가 아니다.

## 8. 중단 조건과 비목표

다음 상황에서는 자동 확장하지 않고 사용자 결정을 요청한다.

- 새 taxonomy schema 또는 대규모 slot 데이터 추가가 필요함.
- taxonomy text의 외부 모델 전송 또는 semantic index 재생성이 필요함.
- 기본 selection 의미나 golden output을 의도적으로 바꿔야 함.
- 유료 이미지 생성, 배포, 원격 publication이 필요함.
- 전체 105개 role 마이그레이션이나 broad multi-probe retrieval로 범위를 넓혀야 함.

이번 목표의 비목표:

- 모든 role 전환, 새 `activity_frame` schema, family centroid index, 기본 semantic multi-probe, 광범위 semantic dropout, 이미지 렌더 품질의 정량 주장.

## 9. 실행 지식 계약

- 목표 생성·시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/`의 파일명과 header metadata를 먼저 검색한다.
- 정확한 module/path, 오류, 환경, 접근법이 맞는 최신 non-superseded 보고서를 우선하며, 전문은 최대 5개만 읽는다.
- 현재 소스와 직접 측정한 증거가 과거 보고서보다 우선한다.
- 보고서와 진행 기록에는 credential, token, secret, 민감한 endpoint, 고객 또는 개인 데이터를 저장하지 않는다.
- passed report는 최종 완료 기준을 모두 통과하고, material failure 해결·기본 접근 실패 후의 비자명한 대안·비용 높은 재현 절차 중 정확히 하나의 자격을 만족할 때만 목표당 최대 1개 작성한다.
- failed/passed 보고서가 서로를 해결하거나 대체하면 양쪽 lifecycle link를 갱신한다.

## 10. 진행 기록

각 checkpoint는 다음 형식으로 추가한다.

- 시각 / stage
- 제품 또는 사용자 관찰 delta
- 직접 증거와 결과
- 구속 결정과 다음 단계
- 열린 위험 또는 중단 조건

### 2026-08-06 17:02 KST / Stage 1

- 제품 또는 사용자 관찰 delta: 아직 사용자 기능을 바꾸지 않는 유일한 기준선 checkpoint를 완료하고, 다음 구현을 대표 role scene과 opt-in contrast guidance로 구속했다.
- 직접 증거와 결과:
  - 현재 role recipe는 105개이며 `identity_core + scene_variants`는 `회사원`, `제빵사` 2개다.
  - seed 42, rule mode의 pilot 후보팩은 role당 17–18개 multi-candidate slot과 28–29개 selected-vs-alternative pair를 노출했다.
  - tag/kind feature set이 서로 다른 slot 비율은 82–89%였다.
  - selected-vs-alternative lexical/tag Jaccard 평균은 role별 8.98–12.73%였고, 0.5 이상 pair는 전체 281개 중 1개뿐이었다.
  - 아래 pilot의 모든 제안 scene slot ID가 현재 dictionary에 존재함을 확인했다.
- pilot role 10개: `사진작가`, `바리스타`, `도예가`, `농부`, `기자`, `우주비행사`, `큐레이터`, `정비사`, `도서관 사서`, `플로리스트`.
- 구속 결정:
  - 새 CLI flag를 추가하지 않고 명시적 `--creativity >= 0.75`를 opt-in 경계로 사용한다.
  - 후보 membership이나 순서를 전면 MMR로 바꾸지 않는다. 기존 exposed eligible 후보 중 relevance rank와 feature distance를 함께 만족하는 contrast 후보를 별도 guidance로 표시한다.
  - role identity는 현재 subject와 역할 전용 wardrobe/costume에만 두고, location/action/prop/procedure는 atomic scene으로 이동한다.
- 다음 단계: Stage 2에서 `SKILL.md`에 창의성 사용 경로를 추가하고 실제 13개 quality profile과 맞지 않는 composition 문서를 수정한다.
- 열린 위험 또는 중단 조건: semantic mode 실측은 외부 embedding 호출 없이 수행하지 않는다. semantic 경로는 synthetic/frozen fixture로만 회귀를 검증한다.

### 2026-08-06 17:05 KST / Stage 2

- 제품 또는 사용자 관찰 delta: `SKILL.md`의 주 흐름에서 `--creativity`를 바로 발견할 수 있고, 보수적·균형·탐색적 범위와 offline rule-mode 사용법, seed 기반 atomic scene 탐색법을 실행 예시로 확인할 수 있다.
- 직접 증거와 결과:
  - `Creative Discovery Workflow`를 추가하고 `--creativity 0.85` 예시 및 coherence 불변 조건을 문서화했다.
  - composition 계약의 quality profile 목록을 실제 data의 13개 profile과 일치시켰다.
  - `tests.test_creativity`와 `tests.test_prompt_expansion_routes`의 19개 테스트가 통과했고 `git diff --check`도 통과했다.
- 구속 결정과 다음 단계: 새 사용자 flag는 추가하지 않는다. Stage 3에서 pilot 10개 role만 전환하고 기존 slot ID를 재사용한다.
- 열린 위험 또는 중단 조건: 없음.

### 2026-08-06 17:10 KST / Stage 3

- 제품 또는 사용자 관찰 delta: pilot role 10개가 고정된 역할 정체성을 유지하면서 seed에 따라 2–3개의 서로 다른 atomic scene으로 회전한다.
- 직접 증거와 결과:
  - 10개 role 모두 `identity_core + scene_variants`로 전환했으며 총 28개의 scene을 구성했다.
  - 모든 scene은 현재 dictionary의 기존 slot ID만 사용하고 location/action/prop 및 필요한 procedure/relational slot을 한 순간으로 묶었다.
  - seed 1–64의 resolver 테스트에서 각 role의 정의된 variant가 모두 관찰됐고 identity slot은 모든 seed에서 동일했다.
  - 각 선택 scene의 anchor pool, `variant_group`, `atomic_scene` strategy를 자동 검증했다.
  - dictionary validator, 기존 scene/golden 집중 테스트 13개, 신규 pilot 테스트가 통과했다.
  - seed 7의 실제 candidate pack 10개가 각각 scene contract group 1개와 safety pass를 반환했다.
- 구속 결정과 다음 단계: role별 새 taxonomy나 index entry를 추가하지 않았다. Stage 4에서는 creativity 미지정 pack의 후보 membership·순서·선택을 보존하는 conditional field만 추가한다.
- 열린 위험 또는 중단 조건: pilot role의 출력 변화는 의도된 scene 회전이다. 기존 golden fixture에는 해당 role이 없어 snapshot 변경은 발생하지 않았다.

### 2026-08-06 17:18 KST / Stage 4

- 제품 또는 사용자 관찰 delta: 명시적 `--creativity >= 0.75` candidate pack에 `creative_exploration`이 추가되어, agent가 sampler-selected subject와 scene을 유지하면서 바꿀 수 있는 대비 slot을 즉시 찾을 수 있다.
- 직접 증거와 결과:
  - contrast candidate는 현재 pack에 이미 노출된 `sampler_eligible_pool` entry만 사용하고 다른 slot의 선택 후보와 충돌하면 제외한다.
  - membership·순서·selected ID를 base pack과 비교하는 통합 테스트, 임계값 0.74에서 field 부재, 0.85 반복 실행 결정성을 검증했다.
  - pilot 10개 seed 42 pack 모두 contrast 6개를 제공했다. 최소 feature distance는 0.947368이었고 source/applicability 위반은 0이었다.
  - 신규·기존 creativity/scene/atomic-contract 집중 테스트 13개가 통과했다.
- 구속 결정과 다음 단계: 후보 재정렬이나 cap 확대는 하지 않는다. Stage 5에서 기존 gate와 전체 테스트만 실행하고 실패 시 원인을 제품 변경에서 수정한다.
- 열린 위험 또는 중단 조건: feature distance는 lexical/tag/facet 대조 지표이며 렌더링 품질을 의미하지 않는다.

### 2026-08-06 17:29 KST / Stage 5

- 제품 또는 사용자 관찰 delta: 목표 산출물과 회귀 증거가 닫혔으며, 기본 경로를 유지한 opt-in 창의 탐색 기능을 로컬 작업트리에 완성했다.
- 직접 증거와 결과:
  - dictionary validator: pass.
  - semantic index metadata: 5,304 entries, 16 shards, dictionary/policy/text-recipe integrity pass. index와 shard content diff는 없음.
  - contradiction check: 555 presets × 3 runs = 1,665 generations, violation 0.
  - public generalization: 60/60 pass.
  - frozen holdout: 24/24 pass.
  - operational-domain holdout v2: 6/6 pass.
  - candidate-pack coverage: 6/6 pass.
  - 전체 unit suite: 387 tests, 630.948s, pass.
  - `git diff --check`: pass.
- 완료 기준 판정:
  1. creativity workflow discovery와 실행 예시: pass.
  2. pilot role 10개, 28 atomic scenes, dictionary validation: pass.
  3. seed 기반 identity 고정 및 정의 variant 전부 도달: pass.
  4. deterministic opt-in contrast guidance와 exact eligible source: pass.
  5. pilot contrast coverage 0→10/10 packs, 60 candidates; minimum feature distance 0.947368; source/applicability 위반 0: pass.
  6. creativity 미지정 pack shape, existing golden, rule priority 보존과 pilot role의 의도된 scene 회전 분리: pass.
  7. 집중·gate·전체 회귀: pass.
  8. 외부 taxonomy 전송, 유료 image API, semantic index content 재생성 없이 완료: pass.
- 구속 결정: `creative_exploration`은 candidate-pack v2의 conditional additive field로 유지한다. 전체 MMR, cap 확대, 새 taxonomy schema는 후속 목표가 명시적으로 승인하기 전에는 추가하지 않는다.
- 제외된 주장: prompt/candidate 구조의 개선만 입증했다. 렌더링된 이미지 품질 개선은 visual review를 실행하지 않았으므로 주장하지 않는다.
- 실행 지식: material failure가 없었고 기본 접근 실패 후의 비자명한 대안도 아니므로 goal-planner 자격 계약에 따라 별도 passed report를 작성하지 않았다.

## Codex 실행 프롬프트

`/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Resume from its latest checkpoint, scan only relevant report metadata before acting, deliver product deltas before expanding verification, persist material failures before retry, obey the stop conditions, and mark the goal complete only when every completion criterion has direct evidence.`
