# Visual Profile Hybrid Retrieval Goal

## 목표와 실제 산출물

- 원래 사용자 요청: 시각 프로필을 하나의 원본 데이터로 관리하면서 exact 용어 매칭과 embedding 유사도 조회를 한 전용 인덱스·resolver에서 함께 수행하고, 설명형 요청도 관련 프로필 후보를 찾게 한다.
- 최종 제품/결과: `photo-prompt-image-generator`가 authorial core를 동결한 뒤에만 registry-hash-bound 시각 프로필 인덱스를 조회한다. 명시적 프로젝트 용어는 deterministic exact hit로 유지하고, 일반 설명·의역은 embedding hit로 찾아 선택 가능한 의미/강화 후보로만 노출한다.
- 범위: 시각 프로필 registry schema, 생성형 sidecar index와 builder, 단일 resolver, candidate-pack v5의 `visual_obligations`·`visual_concept_candidates`·`semantic_clarification` projection, validator/tests/reference 계약.
- 비목표:
  - 최초 의미 해석이나 기본 프롬프트 작성 전에 registry/index/candidate pack을 읽는 동작
  - embedding-only hit를 자동 hard obligation으로 승격하는 동작
  - creativity나 seed로 의미 조회 결과를 바꾸는 동작
  - 이미지 생성·픽셀 품질 평가, 일반 semantic index 재설계, v2/v3 제거
  - 새로운 성인/안전 필터·분류기·차단 조건을 추가하거나 기존 차단을 강화하는 변경. 기존 경계는 유지할 수 있고, 문맥상 명확한 성인 표현을 더 인정해 허용 범위를 넓히는 변경만 가능하다.

## 진척 계약

- 진척으로 인정: 단일 원본 registry에서 exact/semantic index가 생성됨, 한 resolver의 결과가 실제 pack 세 projection을 구동함, 설명형 입력에서 embedding-only optional 후보가 나타남, exact 용어와 user definition 우선순위가 실제 동작함.
- 진척으로 인정하지 않음: 문서·schema·index 파일·테스트만 추가되고 runtime 조회가 기존 중복 matcher를 계속 사용하는 상태, 실제 vector를 사용하지 않는 이름뿐인 embedding 경로, 성인/안전 차단만 늘어난 상태.
- 검증-only 작업 상한: 단계별 focused 검증 1회와 최종 affected suite 1회. 연속 두 checkpoint를 검증-only로 쓰지 않는다.
- 실행 지식 작업 상한: 후보 기본 15건, 관련도순 전문 최대 5건/조회, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.

## 기준선과 고정 결정

- 현재 기준선:
  - v5는 pre-core 지식 격리와 frozen authorial core를 이미 사용한다.
  - `photo_prompt_visual_obligations.json`이 6개 프로필의 exact term, 구성요소 lexicon, 설명, obligation/render gate를 함께 보유한다.
  - hard activation, indirect concept matching, semantic clarification이 비슷한 매칭을 별도로 재계산하며 visual-profile embedding index는 없다.
  - `허벅지 사이의 공간` 같은 일반 설명도 현재 exact hard term에 포함돼 있어 optional semantic discovery와 구분되지 않는다.
- 고정 설계:
  - 사람이 편집하는 원본은 registry 하나다. index는 registry hash와 text recipe에 묶인 재생성 가능한 파생물이다.
  - index는 exact alias lookup과 profile semantic vectors를 함께 가진다. runtime은 한 `resolve_visual_profile_hits` 결과만 계산하고 public pack 필드는 이를 projection한다.
  - exact hit는 기존 요청·문맥·성인 조건을 만족할 때만 기존 hard semantics를 유지한다. embedding-only hit는 항상 optional/eligible이며 선택 전에는 prompt duty나 render gate를 만들지 않는다.
  - user definition과 explicit visual intent가 registry보다 우선한다. authorial-core 필드는 exact hard activation의 소스가 될 수 없고 embedding query 문맥으로만 쓰인다.
  - semantic profile retrieval은 deterministic하고 creativity/seed와 독립이다. 창의성 범위·sampling은 기존 `creative_augmentation`에서만 다룬다.
  - 일반 설명형 표현은 exact activation 목록에서 semantic examples로 이동한다. `절대공역`처럼 의도적으로 유지하는 프로젝트 용어는 exact alias로 남는다.
- 관련 과거 실행 보고서와 적용 교훈:
  - `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`: Gemini index 생성은 검증된 batch size 1과 cardinality check를 유지한다.
  - `docs/failed-reports/2026-08-07-worldbuilding-scoped-route-semantic-competition.md`: 사용자 exact typed hit가 embedding 유사도보다 우선하며 generic semantic 결과가 이를 덮지 못하게 한다.
  - `docs/failed-reports/2026-08-13-scene-blueprint-substring-relevance-collision.md`: 긴 authored prose나 raw substring을 직접 relevance 근거로 쓰지 않고 boundary-aware exact lookup과 전용 semantic text를 분리한다.
  - `docs/failed-reports/2026-08-11-photo-mandatory-intent-polarity-contamination.md`: 요청의 positive/negative/provenance를 보존하고 exclusion을 positive retrieval 신호로 승격하지 않는다.
  - `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`: user hard phrase와 no-people 의미는 권위 있게 유지하고 optional guidance를 hard duty로 바꾸지 않는다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 원본 schema와 파생 index | registry를 exact activation과 semantic definition/examples/components가 구분되는 단일 원본으로 바꾸고, registry hash·text recipe·exact lookup·Gemini vectors를 가진 `photo_prompt_visual_profile_index.json` 및 builder를 만든다 | validator와 builder의 cache/hash/cardinality focused test | broad descriptive phrase는 semantic source에만 있고 명시적 프로젝트 용어는 exact lookup에 있으며 stale index가 거부됨 |
| 2. 단일 hybrid resolver | exact, exclusion/context, user-definition precedence, cosine semantic retrieval을 한 resolver로 합치고 post-core query vector를 재사용한다 | fake-vector exact/embedding/negation/context cases | exact와 embedding 결과가 typed basis를 가지며 embedding-only는 hard가 될 수 없고 pre-core 경로에서는 index를 조회하지 않음 |
| 3. pack projection 전환 | `visual_obligations`, `visual_concept_candidates`, `semantic_clarification`이 같은 resolution 객체를 projection하고 기존 중복 component/direct scan을 정상 경로에서 제거한다 | 대표 exact 용어와 설명형 paraphrase v5 pack | exact는 기존 hard obligation, paraphrase는 optional concept+clarification, unselected optional은 gate 0개 |
| 4. 계약·호환 경계 정리 | skill/reference/validator/audit provenance를 새 index/resolver 계약에 맞추고 v4 exact/explicit replay를 유지한다 | focused v4/v5 contract tests와 public privacy check | public pack에 vector/score/matched term이 노출되지 않고 user definition, negative, exact visual intent가 보존됨 |
| 5. 실제 index와 최종 통합 | 실제 768차원 visual index를 생성하고 representative runtime 및 affected regression을 완료한다 | 실제 score replay, 관련 unit/validator/index integrity, compile, `git diff --check` | 설명형 입력이 관련 optional 프로필을 찾고 무관 control은 찾지 않으며 모든 최종 기준 통과 |

## 최종 완료 기준

1. 사람이 유지보수하는 시각 프로필 의미·alias·obligation 데이터는 registry 하나이며, 전용 index는 registry hash가 맞아야 로드되는 재생성 파생물이다.
2. exact lookup과 embedding similarity가 하나의 resolver에서 한 번 계산되고 세 candidate-pack 필드는 동일 resolution을 projection한다.
3. `절대공역` 같은 exact 프로젝트 용어는 authorial core 이후 deterministic direct hit가 되고, `허벅지 사이의 공간이 매력적인 성인 여성` 같은 설명형 요청은 관련 프로필을 embedding-only optional 후보로 찾을 수 있다.
4. embedding-only hit는 자동 hard obligation, prompt evidence duty, render gate를 만들지 않는다. composer가 명시적으로 선택한 경우에만 기존 opt-in obligation 전체가 활성화된다.
5. user definition·explicit visual intent·negation·context disambiguation이 우선하며 authorial-core 서술만으로 exact hard activation을 만들지 않는다. retrieval은 creativity와 seed에 불변이다.
6. 새 성인/안전 차단 조건이나 강화된 gate가 없고, 기존 adult/safety 회귀가 유지되거나 명확한 adult 문맥 인정 범위만 넓어진다.
7. 실제 visual-profile index integrity, focused exact/embedding/runtime tests, affected photo regression, dictionary/scene checks, compile과 diff check가 통과한다. 결과는 prompt/routing 계약까지만 주장한다.

## 검증 수준과 예산

- 위험 수준: medium. 로컬 prompt retrieval과 public candidate-pack 의미가 바뀌지만 배포·이미지 API·외부 상태 변경은 없다.
- 반복 중 focused 검증: schema/index, resolver, projection마다 해당 test module만 실행한다.
- 최종 검증: visual-profile 실제 index replay, prepack/core/visual-obligation focused suite, affected photo suite, dictionary와 기존 semantic-index integrity, scene-expression current audit, compile, `git diff --check`를 한 번 수행한다.
- 검증 확장 전 질문 조건: 새 유료 서비스·새 embedding provider, 이미지 생성 campaign, v4 public 계약 파기, 별도 adult/safety 정책, 새 verifier artifact family가 mandatory criterion에 필요할 때 중단한다.
- 구현 iteration 한도: 같은 고정 입력에서 같은 원인의 제품 수정은 단계당 최대 3회. 초과 시 기준이나 안전 경계를 임의로 바꾸지 않고 material failure와 선택지를 보고한다.

## 중단 조건과 실행 지식

- 중단하고 질문할 조건: credential/유료 호출의 새 승인이 필요함, 파괴적 변경이나 외부 상태 mutation이 필요함, single-source와 호환성을 함께 달성하려면 public schema 파기가 불가피함, 또는 완료를 위해 성인/안전 차단 강화를 요구하는 상황.
- 시작·재개 시 current report index가 있으면 원문과 함께 검색하고, 없으면 전체 `docs/failed-reports/`·`docs/passed-reports/`의 filename·header metadata·raw text를 검색한다. exact error/problem signature, exact path/module/symbol/API/test, environment/version, approach/exclusion, lifecycle validity 순으로 관련도를 매기고 recency는 tie-breaker로만 쓴다. 전문은 조회당 기본 최대 5건이며 다른 mandatory criterion이나 material risk가 해결되지 않을 때만 이유를 밝히고 확장한다. 현재 source와 직접 evidence가 과거 보고서보다 우선한다.
- material failure는 재시도 전에 현재 시각을 확인하고 secret, token, credential, 민감 endpoint, 고객·개인정보를 제거한 뒤 matching failed report를 먼저 갱신한다. 같은 원인은 한 보고서에 통합하며 expected/observed, 재현 조건, 직접 evidence, cause confidence, failed attempts, resolution/next safe step, reuse guidance를 기록한다.
- lifecycle 변경은 양방향으로 같은 change에 반영한다. supersede 시 이전 보고서의 `Superseded by`와 새 보고서의 `Supersedes`를 함께 갱신하고, success가 failure를 해결하면 failed를 `resolved`로 바꾸고 양쪽을 연결한다. 현재 evidence가 active success를 깨면 success를 `superseded`로 표시하고 새 failure와 연결한다.
- 모든 최종 기준 통과 후에만 success report를 기본 최대 1건 작성한다. 자격은 (1) material failed report 해결, (2) 같은 고정 조건에서 기본·문서화된 접근 실패 뒤 발견한 비자명한 대안, (3) 현재 코드만으로 싸게 복원할 수 없는 필수 다단계 재현 절차 중 하나다. 중간 테스트, 문서, schema, 단순 명령 PASS는 자격이 아니다.
- 목표가 blocked/partial이면 passed report를 만들지 않는다. 검증된 부분 결과는 matching failed report의 resolution/workaround 또는 최종 진행 요약에 남긴다. 보고서 catalog가 활성 상태이면 수동 편집하지 않고 같은 change에서 재생성·검증한다.
- 실행 지식 보고는 별도 stage/checkpoint가 아니며 product delta를 대체하거나 다음 구현을 지연하지 않는다. 최종 보고에는 적용·생성·갱신한 모든 report 경로를 포함한다.

## Codex 실행 계약

- 이 파일의 범위, 진척 계약, 검증 예산, 완료 기준과 실행 지식 계약을 권위 있는 경계로 사용한다.
- setup 이후 각 checkpoint는 product delta나 measured behavior를 남긴다. focused 검증 후 다음 제품 변경으로 진행하고 마지막에만 전체 affected 검증을 수행한다.
- 테스트·문서·schema·index 파일만으로 완료하지 않으며 자동 target uplift를 하지 않는다.
- 사용자 작업과 현재 dirty worktree를 보존하고 이번 목표와 겹치는 파일만 신중하게 수정한다.
- 최종 보고에는 실제 runtime 산출물, 변경 파일, 핵심 검증 결과, 완료 기준별 pass/fail, 실행 지식 경로와 남은 위험을 포함한다.

## 진행 기록

- 2026-08-16 KST — 목표 생성 및 단계 1 진행 중.
  - product delta: 없음(기준선·완료 계약 동결).
  - direct evidence: 현재 registry의 중복 matcher, broad exact term, 전용 embedding index 부재를 source에서 확인했고 관련 failed/passed 보고서 5건을 적용했다.
  - remaining product gap: 단계 1~5 전체.
  - blocker: 없음.
- 2026-08-16 12:38 KST — 단계 1~5 및 visual-profile 목표 완료.
  - product delta: registry v3를 exact activation과 semantic material이 분리된 단일 원본으로 전환하고, registry SHA-256에 묶인 768차원 sidecar와 batch-size-one builder를 추가했다. 한 resolver가 exact·embedding·negation·context·user-definition 우선순위를 계산하고 `visual_obligations`, `visual_concept_candidates`, `semantic_clarification` 세 필드가 동일 결과를 투영한다.
  - direct evidence: actual index 6 profiles/27 exact terms. exact `절대공역`은 hard obligation 하나만, 설명형 허벅지 요청은 hard 0개와 optional `inner_thigh_negative_space` 하나만 생성했다. exact-free full-core 양성 6개는 모두 의도 프로필 1위/optional로 통과했고 최저 점수는 0.770205, 인접 대조군 6개는 모두 후보 0개이며 최고 점수는 0.681438이었다. public visual-profile blocks에 score/vector/rank/matched term/match basis가 없고 pack audit도 통과했다.
  - safety boundary: 새 성인/안전 차단·분류·gate를 추가하거나 강화하지 않았다. 기존 adult context가 `여성`, `女性`, `woman`, `women`, `lady`를 더 인정하도록 허용 범위만 넓혔고 관련 기존 계약 5개와 allowing-context 회귀가 통과했다.
  - validation: focused core/prepack/visual 31/31, adult/contract 5/5, dictionary valid, scene-expression 112/112, general semantic index 6,513 entries valid, compile/index/diff checks pass. repository-wide discovery는 584개 중 11 failures/5 errors였으나 동일 16건이 temporary clean `HEAD`에서도 재현되어 별도 subculture 기준선 결함으로 귀속했다.
  - execution knowledge: resolved `2026-08-16-visual-profile-exact-query-secondary-semantic-leak.md`, `2026-08-16-visual-profile-aligned-user-definition-suppression.md`, `2026-08-16-generic-adult-fashion-visual-profile-leak.md`, `2026-08-16-embedding-positive-blocked-by-lexical-context-guard.md`; active success `2026-08-16-visual-profile-hybrid-retrieval.md`; unrelated open baseline `2026-08-16-full-suite-subculture-boundary-failures.md`.
  - remaining product gap: 없음. 이미지 생성과 pixel 품질 판정은 원래 비범위이며 주장하지 않는다.
  - blocker: visual-profile 목표에는 없음. 저장소 전체 green은 별도 subculture 목표가 필요하다.
