# 네코미미 인간 요청의 동물 품질 라우팅 후속 교정안

작성일: 2026-09-06 KST. 상태: 원인 조사와 교정안 작성 완료, **교정 구현 및 추가 이미지 실험은 하지 않음**.

`arm-03-tsundere`에서 고양이 귀 **소품의 형태**가 실제 동물 **피사체의 종류**로 라우팅된다. `quality_profile`이 negative를 직접 선택하는 것은 아니다. 잘못 라우팅된 내부 subject 선택을 공통 입력으로 animal 품질 facet과 animal negative pool이 각각 만들어지고, public projection과 negative guard가 이 불일치를 남긴다. 동결된 성인 인간 코어 자체는 유지되었다.

우산 동작의 픽셀 미재현은 별도 관측이다. 이번 자료만으로 동물용 negative가 우산 실패를 일으켰다고 판단할 근거는 없다.

## 조사 범위와 관측 근거

다음 4개 실험 파일과 root의 관련 코드·데이터·기존 테스트만 읽었다. 이미지, 과거 생성물, 다른 arm의 입력·출력은 열지 않았다. Python `-B`로 메모리 내 함수 검증을 수행했으며 런타임·데이터·동결 입력은 수정하지 않았다.

| 자료 | 이번에 직접 확인한 내용 |
| --- | --- |
| [authorial_core.json](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/authorial_core.json) | `subject`는 고양이 귀 소품과 메이드 복장을 착용한 성인 여성 및 성인 단골이다. 해석 근거에도 `Nekomimi denotes cat ears in a human costume presentation`이 명시되어 있다. |
| [candidate_pack.json](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/candidate_pack.json) | 배열의 첫 pack `2051e68e7f55e5f8`에서 `quality_profile.facets.subject_kind == ["animal"]`. `coverage.intent_constraints`에는 animal·human이 함께 있고, animal subject route의 alias `cat`이 기록되어 있다. |
| [runtime_request.json](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/runtime_request.json) | `runtime_negative_en`이 pack의 `negative_en`과 정확히 일치한다. 같은 문자열이 `runtime_prompt_en` 끝의 `Avoid:`에도 들어 있다. |
| [evaluation.json](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/evaluation.json) | 기존 독립 평가가 prompt/runtime PASS, 픽셀 9개 gate 중 4 PASS·5 FAIL을 기록했다. 성인 인간 actor와 네코미미 소품은 PASS, 우산의 불균등한 보호 관계는 FAIL이다. 이번 조사의 독립 픽셀 판정은 아니다. |

문제가 된 negative의 전체 문자열은 다음과 같다.

```text
illustration look, cartoon style, overly smooth fur, awkward animal anatomy, low resolution, excessive HDR, over-processed retouching, fake-looking background, 3D render look
```

코어의 `user_exclusions`는 빈 배열이다. 따라서 두 동물용 항목은 사용자가 직접 요청한 제외가 아니다. `overly smooth fur`가 소품의 인조 털에 국소적으로 유용할 가능성과, 실제로 소품의 재질을 근거로 선택되었다는 주장은 구분해야 한다. 현재 코드에는 이 소품 소유자·재질 적용 근거가 없으며 animal pool에서 선택된다. `awkward animal anatomy`는 이 인간 복장 요청에 실제 동물 해부 대상이 없는 명백한 적용 대상 불일치다.

## 실제 전파 경로

### 1. typed core의 평문 필드에 종 alias를 다시 적용한다

[resolve_request_intent_constraints](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:5115)는 v3 코어를 받으면 `interpreted_intent`, `subject`, `setting`, `event`, `visual_priorities`, 제외되지 않은 semantic assertion의 모든 `axes` 값을 텍스트 목록으로 만든다. 그 뒤 `subject_routes`와 `subject_categories`의 alias를 같은 목록 전체에 대입한다.

[intent_alias_matches](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:5085)는 하이픈을 공백으로 바꾸므로 `cat-eared`가 `cat eared`가 되고, `cat` 전체 단어가 일치한다. `plush cat ears`도 같은 alias와 일치한다. 이것은 단순 부분 문자열 오탐보다 **어떤 개체의 어떤 속성인지 구분하지 않는 범위 오류**다. 단어 경계나 부정어 처리만 강화해도 해결되지 않는다.

[intent_routing 원자료](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json:134)는 `cat`, `cats`, `고양이` 등을 `stray_cat` / `animal`로 연결한다. human category alias에는 `portrait`가 있으며, 이 실행의 human hit는 성인 여성이라는 주어가 아니라 첨부 `portrait`를 설명한 문구에서 나온다. `adult woman`이나 단독 `human`은 해당 human alias 목록에 없다. alias를 보충해도 animal hit가 함께 남으므로 근본 교정이 되지 않는다.

실제 코어에서 alias가 일치한 필드는 다음과 같다.

| 코어 경로 | 일치 | 실제 의미 |
| --- | --- | --- |
| `interpreted_intent` | `cat`, `portrait` | `photographic cat-eared maid`, 외모 참고 portrait |
| `subject` | `cat` | `adult woman wearing plush cat ears` |
| `visual_priorities[2]` | `cat`, `portrait` | 얼굴 참고와 소품의 가독성 |
| `semantic_assertions[1].axes.cat_ears` | `cat` | `Plush black cat ears ... on a human costume presentation` |
| `semantic_assertions[2].axes.appearance_use` | `portrait` | 참고 이미지에서 관측할 외모 |

`routing_input = authorial_core_typed_semantics`는 입력을 가져온 위치를 나타낼 뿐, subject가 타입과 소유 관계를 가진 개체로 해석되었다는 보장은 아니다. v6가 legacy MOE router를 호출하지 않는 것과 이 subject alias 경로가 실행되지 않는 것도 별개다.

### 2. 정확한 subject entry 경로가 human category보다 먼저 후보를 좁힌다

[choose_slot](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:23625)는 subject slot에서 `subject_entry_ids`와 일치하는 후보가 있으면 먼저 해당 후보들로 pool을 줄인다. 이후 `subject_categories`의 animal·human 중 하나에 속하는지 검사한다. 이미 고양이 후보 하나로 좁혀진 pool에서 animal·human의 합집합 검사는 인간 후보를 복구하지 않는다.

원자료 [stray_cat](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json:107978)은 `a stray cat`, tags `animal`, `pet`, `urban`이다. [subject_category](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:3221)는 선택된 subject의 override/tags/facets를 읽고 animal을 반환하며, frozen core의 인간 주어와 대조하지 않는다.

공개 pack은 private subject 선택 ID와 preset을 지운다. 따라서 **원래 실행에서 선택된 내부 ID를 공개 pack만으로 직접 읽었다고 주장하지 않는다**. 다만 공개된 `cat` route 흔적과 animal 결과, 실제 코어를 사용한 함수 재계산, 아래 제한된 메모리 내 선택 검증이 이 전파 경로를 뒷받침한다. 전체 semantic sampler를 다시 실행한 결과로 취급하지 않는다.

### 3. 품질 facet을 sampler에서 가져온 뒤 authorial로 표시한다

[candidate_pack_quality_profile](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:13664)은 선택된 subject entry의 facet/tag로 `subject_kind`를 구성한다. `candidate_pack_quality_add_intent_facets`의 보완 경로는 uncovered intent 전체 문자열이 `portrait`, `person` 등의 짧은 alias와 정확히 같아야 동작한다. 실제 7개 mandatory intent는 완성된 증거 문구여서 이 보완 경로가 human을 복원하지 않는다. literal subject label 보완도 실제 문구를 human entity로 해석하지 못한다.

[candidate_pack_v4_project_quality_profile](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:15397)은 기존 `subject_kind`를 그대로 복사하면서 `profile_id = authorial`, `selection_mode = agent_authored`를 붙인다. v6 → v5 → v4 projection 체인이 이를 사용한다. 따라서 공개 결과의 `agent_authored`는 이 facet이 코어의 실제 인간 개체에서 만들어졌다는 정확한 provenance가 아니다. sampled style profile을 숨기는 목적과 의미의 작성 주체를 정확하게 표시하는 목적을 함께 충족하도록 후속 교정이 필요하다.

### 4. 같은 내부 subject가 animal negative pool도 선택한다

[choose_negative_entries](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:25472)는 `quality_profile`이 아니라 `picked`의 `subject_category`를 읽고 base에 animal pool을 추가한다. [animal negative 원자료](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json:198744)에 `awkward animal anatomy`, `unrealistic eyes`, `overly smooth fur`가 있다.

[생성기의 negative 처리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:26381)는 `render_picked`로 이를 선택한 후 authorial negative filter를 거쳐 `negative_en`과 hash-bound guard를 만든다. 품질 facet과 negative는 잘못된 subject 선택의 두 결과다. 여기서 quality facet 문자열만 human으로 덮어써도 negative 선택의 원인은 남는다.

### 5. intent-neutral allowlist가 적용 대상 불일치를 통과시킨다

[AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_contracts.py:183)에 두 동물용 문구가 전역적으로 들어 있다. [생성기의 허용 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:2979)와 [감사기의 허용 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py:290)는 이 집합에 있으면 subject와 무관하게 먼저 `True`를 반환한다.

[negative guard 감사](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py:378)는 hash와 emitted terms, allowlist, 제외 및 blanket directive를 검사한다. [runtime 입력 감사](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_image_render_request.py:171)는 pack·composed·runtime negative의 바이트 일치를 요구한다. 잘못 선택된 항목도 이 계약을 충족할 수 있다. 정확히 보존된 입력이라는 PASS와 피사체에 적합한 negative라는 PASS는 별개의 검사가 필요하다.

## 실행한 read-only 검증

현재 root 코드로 `.venv/bin/python -B`를 실행하고 실제 pack 안의 normalized core를 `resolve_request_intent_constraints(data, None, None, authorial_core=core)`에 전달했다. tag data는 실제 `load_json`의 extension merge를 포함해 읽었고 quality-layer 원자료를 로드했다. 네트워크·이미지·파일 출력 경로는 호출하지 않았다.

```json
{
  "subject_entry_ids": ["stray_cat"],
  "subject_categories": ["animal", "human"],
  "source_text_count": 20,
  "routing_input": "authorial_core_typed_semantics",
  "subject_route_hit": {"value": "stray_cat", "category": "animal", "aliases": ["cat"]},
  "human_category_hit": {"aliases": ["portrait"]}
}
```

다음 검증은 **전체 실험 replay가 아닌 메모리 내 함수 연결 검증**이다. semantic context 없이 빈 필터의 조사용 preset과 재계산된 intent constraints를 사용했다.

| 검증 | 실제 결과 |
| --- | --- |
| `choose_slot("subject", ...)`, seed 6103 | `stray_cat`; explicit subject route 뒤 후보 1개, category 검사 뒤에도 1개 |
| 그 subject + 실제 pack의 7개 mandatory intent로 quality profile 생성 | animal facet, `matched_uncovered_intent_facets = []`, `matched_literal_subject_entries = []` |
| 생성된 profile을 public projection에 전달 | animal facet을 유지한 채 `profile_id = authorial`, `selection_mode = agent_authored` |
| 같은 subject로 negative 후보 전체를 검사하고 실제 core로 필터링 | 두 동물용 문구 모두 유지됨. 순서·샘플 개수는 원래 실행 replay가 아님 |
| 두 문구에 생성기 및 감사기의 `authorial_negative_term_allowed` 적용 | 각각 모두 `True` |
| 실제 pack과 그 core의 baseline에 `audit_negative_intent_guard` 적용 | 실패 목록 `[]`. 전체 prompt/runtime 감사 재실행을 의미하지 않음 |
| 실제 `pack.negative_en == runtime.runtime_negative_en` | `True` |

## 후속 교정안

1. **core를 동결하기 전에 실제 장면 개체와 속성의 소유 관계를 구조화한다.** 예를 들어 인간 actor와 인간 target은 각각 `entity_kind: human`, 고양이 귀는 actor에게 `worn_by`로 연결된 accessory, 외모 참고 portrait는 장면 개체와 다른 reference scope로 표현한다. source span/anchor와 literal evidence를 함께 바인딩한다. 실제 동물이 함께 있는 장면에서는 별도 animal entity를 보존한다. 새 필드의 이름·contract version은 구현 시 확정한다.
2. **v6 이후 authoritative subject routing은 이 개체 계약을 소비하게 한다.** costume, print, depicted image, reference, 배경 설명의 종 단어를 실제 동물 subject로 승격시키지 않는다. alias 검색은 관련 후보를 찾는 보조 수단으로 남길 수 있지만 frozen entity type을 바꾸는 근거로 쓰지 않는다. 기존 코어에 타입 근거가 없으면 임의의 인간/동물 추측 대신 `unresolved/generic`을 남기고 자동 유형 전용 negative를 생략한다. 필요하면 새 실행의 pre-core 단계에서 해석을 명시한다.
3. **품질 정보와 negative가 같은 검증된 개체·재질 적용 계약을 읽게 한다.** 전역 intent-neutral 허용 여부와 적용 대상을 분리한다. animal anatomy는 실제 animal entity, fur defect는 관측 가능하고 의도된 fur material 및 소유자 범위가 있어야 자동 적용한다. 인간 얼굴·피부, 식품·증기, 제품·벽 등 다른 유형 전용 항목도 같은 generic applicability 구조로 다룬다. 동물용 negative의 전역 삭제나 네코미미 전용 예외 분기는 해결책으로 삼지 않는다.
4. **public provenance와 감사 범위를 맞춘다.** 공개 quality facet에는 core entity binding/hash와 실제 도출 출처를 기록하고, private sampler에서 온 정보를 `agent_authored`로 재명명하지 않는다. 자동 negative별 적용 entity/material 근거를 recomputable guard에 포함한다. 생성기·감사기는 공용 의미 판정기를 사용하며, guard를 다시 hash해도 subject 범위가 모순이면 감사가 실패해야 한다. 사용자가 명시한 제외와 identity opt-in의 기존 별도 경로는 유지한다.
5. **새 계약·실행으로 검증한다.** 이번 `working-tree:c0eeb2bf23fc913b79a4161361d9da305c89cd4ce4a277dae77d06f5d6a727c6` snapshot, 코어, runtime negative, 생성 결과는 수정하지 않는다. 후속 버전에서 교정 후 새로운 run/hash로 검증하고 기존 실패 기록을 보존한다. `cat` 문자열 삭제, 사람을 항상 우선하는 규칙, 공개 facet 덮어쓰기, 기존 expected를 동물로 바꾸기는 피한다.

## 최소 회귀 범위

현재 [v6 라우팅 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core_v6.py:1394)는 legacy MOE router의 미호출과 라우팅 표식을, [negative 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core_v6.py:838)는 일반 의미 억제의 필터링을, [vocabulary 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core_v6.py:963)는 양쪽 집합의 일치를 검사한다. 이들만으로 accessory/actor 구분과 negative applicability는 검증되지 않는다. 기존 고양이 실제 피사체의 [양성 회귀](/Users/chasoik/Projects/image-prompt/tests/test_photo_prompt_contract_v2.py:1035)는 유지할 필요가 있다.

| 묶음 | 최소 입력 쌍·조작 | 교정 후 관측해야 할 불변 조건 |
| --- | --- | --- |
| 실제 결함 | 이 arm의 인간 코어 의미 / 동일 인간 + 귀 소품 표현만 변형 | 인간 actor·target을 보존하고 animal subject route와 anatomy negative가 생기지 않는다. `cat-eared`, `plush cat ears`, 명시된 네코미미/고양이 귀/猫耳 해석을 매개변수화한다. 실제 증거 문구를 테스트 편의상 삭제하지 않는다. |
| 소유·표현 범위 | 고양이 귀·토끼 귀 소품, 동물 무늬 옷·그림·reference / 실제 고양이·새가 주어 | 소품·그림·참고 이미지가 실제 animal entity가 되지 않는다. 실제 동물은 animal 품질과 적합한 negative가 유지된다. |
| 혼합 장면 | 인간 + 고양이 귀 / 인간 + 실제 고양이 | 후자만 human·animal 개체를 모두 보존한다. 무조건 human 우선 또는 animal 전체 금지 방식의 잘못된 수정을 잡는다. |
| 재질 적용 | 인조 털 귀 소품 / 털 있는 실제 동물 / 매끈한 털이 명시된 연출 | anatomy의 대상과 fur 재질의 소유자를 구분한다. 요청한 재질을 자동 negative로 지우지 않는다. 재질 근거가 없으면 해당 자동 문구를 내보내지 않는다. |
| 후보·작성 권한 | 인간 frozen core에 동물 sampled subject/optional 후보를 주입 | 품질과 자동 negative가 authoritative entity를 따른다. sampler를 바꾸거나 후보를 모두 거절해도 frozen actor의 종류가 달라지지 않는다. |
| 감사 반례 | 인간 pack에 animal facet/negative를 삽입하고 guard hash까지 재계산 / 정상 실제 동물 pack | 전자는 의미 범위 검사에서 실패하고 후자는 통과한다. 생성기와 감사기 함수가 같은 코드를 공유한다는 확인만으로 대신하지 않는다. |
| 통합 보존 | 같은 요청의 새 버전 pack → composition → runtime | 인간 facet, 적용 가능한 negative, 정확한 bytes, core/lock hash, 동일 대상의 보호 동작·결과·시간 관계가 함께 유지된다. quality만 수정하고 negative를 남기는 부분 수정을 검출한다. |
| 호환 경계 | 기존 실제 고양이/사람 없는 제품 회귀, 명시적 제외·identity opt-in | 기존 의미와 구버전 판독이 보존되고, 새 계약의 적용 범위를 버전으로 명시한다. 동결 arm 결과를 새 expected로 소급 교체하지 않는다. |

최소 자동 검증은 resolver·quality·negative·감사 반례 및 이미지 호출 없는 pack→runtime 통합까지다. 위 표는 앞으로 작성할 테스트 범위이며, 이번 조사에서 모두 실행해 PASS했다는 뜻이 아니다.

## 우산 픽셀 결과와 인과 경계

기존 `evaluation.json`은 거의 수직인 우산 축과 두 사람을 함께 덮는 넓은 덮개, 보이지 않는 단골의 내린 손, 명확하지 않은 보호 경계 밖 젖은 소매를 기록했다. 동시에 actor는 성인 인간으로 보이고 고양이 귀는 소품으로 남았다고 기록했다. 이 두 관측으로 말할 수 있는 것은 **부적합한 animal metadata/negative와 우산 관계의 픽셀 실패가 같은 실행에 함께 있었다**는 사실까지다.

동물용 negative 제거만 바꾼 대조군, 반복 생성 또는 다른 조건 통제가 없다. 따라서 이 결함 교정이 우산 기울기·보호 대상·젖는 대가·손 반응을 개선한다고 예측하거나 이번 FAIL을 PASS로 변경하지 않는다. 향후 인과를 조사하려면 동일 core·참고 이미지·양성 prompt를 유지하고 변경 요인, 이미지 호출 수, 모든 결과를 별도로 기록해야 한다. 현재 조사의 교정 수용 조건은 의미 라우팅과 입력의 일치이며, 관계의 픽셀 재현 및 사용자 평가는 계속 별도의 판정이다.

## 해시 기록

아래는 이번 조사 시 직접 읽어 계산한 파일 SHA-256이다. 코어 JSON의 파일 hash와 pack 안 canonical core hash는 직렬화 범위가 달라 별개다.

| 파일 또는 바인딩 | SHA-256 |
| --- | --- |
| arm `authorial_core.json` | `09d05850d37c6099881e53ebff3521c75ada1b53d89b2a6e793d36717e6bb8f0` |
| arm `outputs/candidate_pack.json` | `ff6532f811b041cce3f5d7d9ab9edd343ba56e51265284c909b7494b914cbb50` |
| arm `outputs/runtime_request.json` | `9f4df98d2298e6fec0336a0169623965d3e785c8a9d1250fd86b597ed70d0daf` |
| arm `outputs/evaluation.json` | `61ae6a22f004aef9817327af7eebe0b7a24b3c3ee79b4c4899057651af7fffce` |
| pack canonical core | `35aeca8d11995c76a73ddeef823421b1195f903e2e49172ca10e312930420da9` |
| pack canonical intent lock | `1d44ca3b896b74da2563447b07a86196150e949cbe2e02809cf1bbb1378b650a` |
| root `scripts/prompt_generator.py` | `05d8daad5a6fb412c5b8d9bc8ae80c37614eea6bb7b468fd434272374112589a` |
| root `scripts/photo_contracts.py` | `406097052023ab4be065d0e79583c1a3836ed4faac656c406dddcc6bb1f05b05` |
| root `scripts/audit_composed_prompt.py` | `6ac5d931059b6f667e9f8814166b0e2cd36bfea63b76a3b2dfadee92fdd93cb4` |
| root `assets/photo_prompt_quality_layers.json` | `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f` |
| root `assets/photo_prompt_tags.json` | `30ece1938fe78f57abb9944196320528ddb8d79bfeb33a28bb03d89b729ae639` |

root 소스의 단일 파일 hash와 실험의 전체 skill snapshot hash는 서로 다른 범위다. 위 함수 검증은 현재 root 코드에서 수행했고, 동결 skill 전체 tree를 별도로 재검증했다는 의미는 아니다. 실험 snapshot의 전후 불변은 제공된 evaluation의 기록에 근거한다.
