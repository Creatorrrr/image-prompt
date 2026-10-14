# 집행된 관계 guard를 명시적인 역할 근거로 연결하는 최소 계약안

2026-10-15, `/root/review_07250_08250`, gpt-6.1-sol/high. 읽기 전용 설계이며 구현·source 보정·proof 작성·승인·등록·배포를 수행하지 않았다. 기존 bulk `[7250,7340)` 90개는 불변이며 다음 미독 ordinal은 7340이다.

## 실제 입력과 현재 막힘

GEN `2ad7b2bfd3f4d730985c23ed89e3513a326a0a2ceea22aecfe28cb5d05c98ac9`의 실제 import 파일과 SHA는 동명 `.repro.json`에 고정했다. Working module을 이 GEN으로 바꿔 부르지 않았다. Root의 phrase/global-index working patch는 본 설계의 실행 기준이 아니다.

146V5 `anatomical_connection`, `body_form`, `action`, `relational_action` 전체 명세를 새로 읽었다. 이 네 항목은 실제144V4와 JSON 값이 같다. 146 review의 anatomical_connection historical-before/after/reason도 읽었다. 그 before는 historical139에 대한 것이므로 144→146의 새 변경으로 오인하지 않는다. 나머지146 전체 명세를 새로 읽었다는 주장은 하지 않는다.

17437-03 전체 common와 baseline은 재독했다. 이전 독립 메모의 18 RID whole-body/조건/효과와 정확 반복군 읽음 범위는 그대로 참조한다. 이번04 prepared current는03 `source_after`와 전체 JSON이 정확히 같음을 확인했다. 따라서 이번에 3633 fact raw occurrence를 전수 재독했다는 주장은 없다. Reference candidate/binding closure는 여전히 모두 비어 있다.

실제17437 source는 여전히 `photo-native-source-guards/v1`이고 `rival_owned_face`는 `left_role=primary_face, relation=part_of, right_role=main_subject`다. v2 source-target로 바뀌지 않았다. 실제 긍정 본문 `/content/authored_components/obligations/0/render_gates/1/description`은 `its face is explicitly part of that actor`라고 명시한다. 이 문장은 소유 관계이며 얼굴 형태·피부·표정만으로 유추한 관계가 아니다. 원래 adult/peer-rival/identity 보존과 선택적인 helper/setback/warmth/recovery 조건은 모두 계속 필요하다.

`validate()`의 role은 정확한 다섯 key와 nonempty `fact_refs`만 허용한다. `qualification()`도 selected fact가 없으면 거부한다. 현재 scalar fact shape는 typed string/list value만 받으므로 관계를 표시하려고 actual frozen owner ID를 scalar P로 상수화하거나 의미 없는 `present`를 복제하면 안 된다. Guard는 이미 관계를 집행하지만 표시 역할 근거에 그 집행을 연결할 통로가 없다.

## 권장 형태: 선택적으로 추가하는 별도의 관계 근거

기존 v4 proof를 자동 재작성하지 않는다. 새 근거가 없는 proof의 shape·bytes·의미·hash와 결과 key를 그대로 보존한다. 구현 시 exact accepted-shape 두 종류를 명시한다. 필드가 없을 때 빈 배열을 주입하거나 canonical material에 새 default를 넣지 않는다. 현 `native_contract_sha256()`는 실제 존재하는 key를 해시하므로 이 원칙에 맞는다.

새 근거를 실제 작성한 proof에만 bounded `guard_supports` 배열을 추가한다. 예시 아래는 **설계용 부분 shape**이며 complete native proof가 아니다. 해시 자리표시는 실제 산출물 값이 아니다.

```json
{
  "id": "gs_face_owned_by_actor_baseline",
  "realization_id": "baseline",
  "pointer": "/content/authored_components/obligations/0/render_gates/1/description",
  "quote": "its face is explicitly part of that actor",
  "mode": "prerequisite",
  "guard": {
    "schema": "photo-native-source-guards/v1",
    "declaring_candidate_id": "cand_d15b4c6334a45b61a7407a022a2cc8e0",
    "declaring_realization_id": "baseline",
    "source_condition_index": 0,
    "conditions_sha256": "<actual sealed source_conditions[0] digest>",
    "rule_id": "rival_owned_face",
    "rule_sha256": "<actual complete rule digest>"
  },
  "endpoints": {
    "left_role": {"candidate_id": "cand_d15b4c6334a45b61a7407a022a2cc8e0", "target": "actor_face"},
    "right_role": {"candidate_id": "cand_d15b4c6334a45b61a7407a022a2cc8e0", "target": "actor"}
  },
  "semantic_projection": {
    "dimension": "body_geometry",
    "target": "actor_face",
    "property": "anatomy.connection.ownership"
  }
}
```

`semantic_projection`는 사람이 전체 원문과 role 명세를 읽고 작성한 관계의 표시 분류다. 새로운 scalar fact/value, E, actual owner ID, anatomy 생성 또는 permission이 아니다. `mode`는 우선 prerequisite 하나만 허용한다. 실제 현재 존재 관계를 요구하는 guard를 새로운 관계 생성 E나 context로 바꾸지 않는다. 이 설계는 E/preservation 관계의 일반 표현까지 해결했다고 주장하지 않는다.

v2 row는 실제 `schema=v2`와 같은 locator를 사용하고 `endpoints`의 key를 실제 rule대로 `left/right`로 쓴다. 각 값은 실제 rule의 `source_target` 주소와 정확 일치해야 한다. v1에는 실제 `left_role/right_role` key와 source-local owner의 명시적인 수동 대응이 있다. v1→v2 자동 변환, key 이름만 바꿔 동일하다고 인정하는 처리, 현재 core owner ID의 상수 저장은 없다.

`owner_relation`과 `frozen_entity_relation`만 지원한다. v1/v2의 실제 rule 전체를 hash로 결합하고 kind·relation·방향·endpoints를 그 rule에서 검증한다. `frozen_entity_relation`은 actual rule의 dimension/property/value_type을 그대로 요구하며 semantic projection의 dimension/property도 원 rule과 같아야 한다. Prefix가 안 맞으면 별도 taxonomy 검토가 필요하다. `owner_relation`에만 dimension/property가 없으므로 수동 projection을 허용한다. Guard 이름, neutral role 이름, owner kind, slot 이름에서 이 projection을 계산하지 않는다.

최소 scope는 **동일 proof CID의 해당 actual RID에서 source_conditions[0] 또는 [1]에 실제 집행되는 source_common/source_branch rule**이다. 다른 CID proof의 support ID, 단순 presentation 조건, member-pointer 조건을 부모의 긍정 의미로 빌려오는 것은 허용하지 않는다. 이 조건들은 기존대로 admission에서 conjunctively 집행한다. Required dependency를 endpoint로 명시한 v2 source rule은 기존 source-target namespace/closure에 실제 허용될 때만 가능하며 그 관계 본문도 이 CID에 직접 있어야 한다. Optional child가 선택되지 않았는데 endpoint를 끌어오거나 child role을 부모에 합산하지 않는다. 나중에 member/presentation guard 자체를 semantic support로 허용하려면 별도의 명시적인 provenance/activation 계약 검토가 필요하다.

상한 제안은 source/RID당64, proof 전체512 support row이며 모든 ID는 proof 내 고유해야 한다. Fact ID와 support ID의 namespace도 충돌하지 않게 검증한다. 부풀린 반복에 필요한 상한 증가는 실제 입력을 보고 따로 결정한다.

## Role과 ordinary semantic source-unit의 직접 연결

Role에 선택적으로 nonempty `guard_refs`를 추가한다. 모든 ref는 같은 proof의 직접 검증된 support ID여야 한다. `fact_refs`는 기존 type을 유지하되 guard_refs가 실제 존재하고 유효할 때만 빈 배열을 허용한다. RID별 coverage는 **직접 검증된 scalar fact와 직접 검증된 guard support의 합집합**으로 확인한다. 각 support projection의 dimension/property는 exact full spec에 맞고 mode도 명시적으로 허용되어야 한다. 역할어/키워드로 자동 역할을 생성하지 않는다. Pure guard role은 support_modes=[prerequisite]이며 mixed role은 실제 fact modes와의 정확한 합집합이다.

Ordinary semantic source-unit에 선택적으로 `guard_refs`를 허용한다. 기존 `fact_refs`와 fact direct-anchor 규칙은 한 글자도 완화하지 않는다. 기존 의미 단위가 fact만 받으면 기존 shape 그대로다. Guard-only ordinary unit은 disposition=semantic, fact_refs=[], guard_refs=[정확 ID]이며 **whole field quote**를 기존대로 가진다. 각 support는 같은 RID·같은 pointer이고 support.quote가 이 whole quote에 실제 포함되어야 한다. Fact_refs와 guard_refs가 모두 비면 semantic 단위로 인정하지 않는다. Nonsemantic 단위에는 어느 쪽도 들어갈 수 없다.

모든 scalar fact는 여전히 자기 primary field의 ordinary semantic unit에 직접 anchor된다. 모든 guard support도 자기 primary field의 ordinary semantic unit에 직접 anchor된다. `semantic_reference`에 guard_refs를 추가하지 않는 것이 첫 구현의 최소안이다. Reference는 기존 one-hop fact constraint 보존만 수행하며 guard support/role을 만들지 않는다. 다른 필드의 관계 paraphrase를 허위 nonsemantic으로 만들지 않는다. 필요하면 그 필드에 별도의 직접 support ID와 실제 같은 집행 guard locator를 수동 작성한다. Literal 반복은 준비 도구일 뿐 직접 읽음을 대신하지 않는다.

`positive_string()`/`primary_paths()`의 실제 positive field를 그대로 적용한다. Conditions/activation/alias/tag/validation label을 quote로 쓰지 않는다. Phrase patch가 publish되면 실제 그 GEN의 field inventory를 사용하고, 해당 구간의 본문은 직접 재독해야 한다.

## 전체 validator와 집행 receipt의 결합

Qualification은 현재처럼 core 이전의 source 검증이다. 집행 receipt는 request-local core가 주어진 admission 시점에만 생긴다. 이 두 시점을 섞지 않는다.

1. Full authoring validate는 모든 actual RID의 source guard inventory, selected profile contract, dependency/references를 기존대로 exact 검증한다. 그 뒤 support locator가 자신의 sealed source_conditions의 실제 rule 하나를 지목하는지 확인한다. 중복 rule ID가 다른 layer에 있어도 source_condition_index와 condition hash가 다르면 대체할 수 없다. 모든 support의 직접 positive anchor와 owner map/endpoints/semantic projection을 검증한다.
2. v1 owner_relation support의 source-local endpoint를 owner_map에 명시적으로 추가한다. 현재 `_validate_owner_map()`의 wanted 집합은 facts/receivers/v2 own guard targets만 보므로, **검증된 support endpoint**도 합친다. v1에서 protocol role이 있다고 anatomy가 생기지 않으며 source quote와 explicit existing binding이 함께 필요하다. Introduced owner는 frozen guard support endpoint로 금지한다. Guard-only owner를 뒷받침하려고 가짜 presence fact를 추가하지 않는다.
3. Admission은 기존 whole-cue scalar P/preservation·모든 E·guards·dependency·joint assignment 검사를 먼저 수행한다. 그 실제 실행에서 얻은 receipt와 role support locator를 대조한다. Evaluator를 통과했다는 boolean, schema만 같음 또는 후보가 source-qualified임만으로 통과시키지 않는다. Unresolved owner selection/dependency/search probe는 기존처럼 search_only/review_required다.
4. v2는 `_guard_context()`가 재구성한 선언 CID/RID, activation CID/RID, source layer/pointer, conditions hash, meaning/qualification/reference closure 및 실제 rule_id에 정확 결합한다. Runtime receipt에 guard schema, full rule_sha256, relation predicate와 canonical actual endpoint도 추가하는 것이 명확하다. 기존 `owners` raw address도 보존한다. `owner_relation`은 graph canonical/ancestor closure와 graph hash, `frozen_entity_relation`은 exact core_assertion_id와 canonical right endpoint/value를 결합한다.
5. **v1 현재 receipt는 부족하다.** `_evaluate_role_guards()`는 layer index/rule_id/kind/raw-role owners만 내며 declaring CID/RID·condition/rule hash·graph hash가 없다. v1을 v2로 shim하지 말고, source_guard_set에서 얻은 source_common/source_branch provenance를 명시적으로 재구성하여 해당 실행 receipt에 결합한다. Flattened condition_layers의 숫자 index만 신뢰하지 않는다. Presentation/extra layers는 그 자체로 source support가 될 수 없다. v1 frozen_entity_relation은 현재 raw actual-owner typed value equality를 사용하며 v2의 canonical _same_entity 비교와 다르다. 이 안에서 그 원래 predicate를 자동 완화하지 않는다. Alias를 수용하지 못하는 v1 case는 그대로 실패/보류다.
6. Guard support가 endpoint를 알려준다는 이유로 새 guard, owner, core assertion, permission, action receiver를 생성하지 않는다. 지원하는 role로 선택되었더라도 전체 source guards는 항상 conjunctive다. 관계 role의 ref만 남기고 다른 guard를 생략하지 않는다.

## Compact/lazy/pack/rolefit/fingerprint

Full proof에서는 positive pointer/quote가 직접 검증된다. `compact()`는 기존처럼 whole-source validate 뒤 seal을 만든다. 새 support가 있는 경우에만 그 **실제 locator/endpoints/manual projection/mode**를 유지하고 raw quote/pointer는 fact와 같은 방식으로 제거할 수 있다. 원 full-proof qualification_sha256가 직접 근거를 seal하며 compact_sha256가 새 compact support material을 seal한다. Compact는 raw quote를 다시 검증했다고 주장하지 않는다. Source-unit은 기존대로 compact에서 제거된다. 새로운 hash는 새 proof에만 생긴다.

`qualification()`/slot_semantics.fit는 guard-only role도 source-reviewed prerequisite support로 보고하되 actual guard admission 전에는 `source_guard_admission_required`를 명시해야 한다. `matched_properties`에 scalar effect처럼 섞지 않고 optional `guard_refs`/`matched_guard_supports`로 표시한다. No-extra-field proof에서는 기존 반환 shape를 유지한다. Rolefit의 source 의미 적합과 request admission 가능성은 분리한다.

Lazy `guard_record`는 compact support가 보존된 proof와 기존 sealed source/member conditions를 유지한다. Required dependency의 child support도 child compact에 남고 선택된 closure를 통해서만 검증된다. Reader meta record_sha256와 payload hash는 full source를 계속 결합한다. Large body를 lazy guard에 되살리거나 role별 source 복사본을 만들지 않는다.

`photo_role_proposals.propose()`는 새 support가 있으면 새 semantic_fit 값을 proposal_id material에 포함한다. Source_record_sha256, full effects, source/binding conditions, eligible RID/dependency choices는 그대로 보존한다. `photo_native_pack` candidate_pool은 하나의 authored_record를 유지하고 role별 guard evidence를 별도 source처럼 증식시키지 않는다. 최종 audit은 proposal 재계산, selected closure와 owner selection, actual admission receipt를 재검증해야 한다. Pack의 semantic_fit만 수정해 support를 주입할 수 없어야 한다.

`meaning_sha256`는 source/body/conditions/effects가 바뀌지 않으므로 변하지 않는다. 새 proof의 `native_contract_sha256`, full qualification digest, compact digest, role proposal ID, corpus/layout digest는 실제 새 material을 포함한다. Runtime `code_inventory`/algorithm/source_fingerprint는 구현 변경을 기존대로 잡고, source code 변경은 root가 별도 publication해야 한다. 기존 frozen source/proof/decision/catalog hash를 자동 갱신하거나 현재 운영 qualified count를 올리지 않는다.

## 독립 taxonomy 문제와 안전 경계

1255 원문 `held neutrally near the subject` / `자기 쪽에 중립적으로 들고 있는`은 실제 holder/object 관계 가능성과 EN/KO 방향 범위가 있다. 1258 `checking voltage safely with a tester` / `테스터로 전압을 안전하게 확인하는`은 actor↔tester 사용 행위를 명시한다. 두 current 전체·historical5B·formal03 proof=null 상태를 직접 확인했다. 이 둘에는 관계 guard를 추가했다고 source 효과/행위 분류가 저절로 해결되지 않는다.

현재 action의 action./activity./operation. 범위와 relational_action의 action.interaction/relation.action/interaction. 범위는 다르다. `action.holding`, `action.checking_voltage`를 전부 relational_action에 자동 승격하거나 동일 행위를 E 두 개로 복제하지 않는다. 1258 historical relation.action.testing_voltage는 그 당시의 제안이지 새 native source의 사실·새 operation 승인이 아니다. 명확한 동일 performed interaction을 새 authored property로 수동 표현하거나 명세 변경을 검토할 수 있지만, 이 설계에서 source/proof/catalog를 바꾸지 않는다. Missing action endpoint/receiver·안전 technique·voltage reading은 원문에 없는 값으로 메우지 않는다.

Guard part_of만으로 anatomical_connection을 자동 부여하지 않는다. Explicit biological/represented anatomical ownership이라는 positive 본문과 full spec가 함께 있어야 한다. 단순 object attachment, 얼굴 명사, 임의 owner kind, 다른 두 사람의 disjoint 조건은 그 역할 증거가 아니다. 단순 frozen_value와 preserve_established_scope는 이 relation support의 허용 kind가 아니다.

예상 거부 case는 foreign CID/RID/source pointer, alias/tag/condition quote, quote substring만 맞고 의미 불일치, stale condition/rule/spec hash, reversed endpoints, 다른 layer의 동명rule, optional child 미선택, introduced endpoint, 임의 owner selection, canonical graph 교체/순환/충돌, 누락된 core fact, ambiguous multiple frozen matches, v1/v2 predicate 혼용, reference-only 근거, unused support ID, partial RID coverage, diagnostic positive support, guard를 scalar E/권한으로 위장한 경우다. 기존 fact/source-unit 직접 근거·모든 effect의 complete coverage는 여전히 강제한다.

## 구현을 승인할 경우의 단계별 allowlist 제안 — 실행하지 않음

1. `scripts/photo_semantic_evidence.py`: optional exact shapes/상한/row 검증/direct unit anchor/role RID coverage/owner endpoint inventory, source-locator resolver, v1/v2 explicit runtime receipt match, compact/qualification. No automatic authored-data migration.
2. `scripts/photo_slot_semantics.py`, `scripts/photo_role_proposals.py`: only if optional guard support reporting/roundtrip needs explicit changes. Existing no-support return shape and proposal bytes remain unchanged.
3. `scripts/photo_search_layout.py`, `scripts/photo_search_reader.py`, `scripts/photo_native_pack.py`, `scripts/photo_candidate_corpus.py`: read/roundtrip and source namespace integration first; mutate only the file actually needing a new exact-shape consumer. Existing generic deepcopies may already carry optional fields. Do not broaden allowlist as a default.
4. New focused test file such as `tests/test_photo_native_guard_role_support.py`: source-only relation field + guard-only ordinary unit, mixed direct facts/guards, v1/v2 part_of/disjoint/frozen_entity_relation, all above fail-closed cases, full/compact/lazy/pack parity, identical old-proof bytes/hash/results, selected dependency and owner-selector probes. Add sourceguard test assertions only when evaluator receipt needs them. Tests are proposed, not written or run here.
5. Root separately decides review/publication/adoption. `precore/photo_semantic_witnesses.py`, core schema, point mapping/memberStageA, catalog/source/registered proofs/global status/runtime pointers/Git are outside this implementation allowlist. Existing canonical closure logic is reused rather than replaced. No new provider/model call or generation.

## 실행한 진단의 한계

동명 `.repro.py`는 GEN2ad7에서 실제 import하여 실제 source v1 rule과 positive quote를 확인했다. 독립 core가 아닌 작은 synthetic graph에 face part_of actor를 주면 low-level `_evaluate_role_guards()`가 통과하고, 그 edge만 없애면 `native_owner_relation_unverified`가 된다. 새 native proof를 만들지 않았고 admission/role qualification/runtime adoption도 실행하지 않았다. v2는 코드를 직접 읽었지만 가짜 complete proof를 만들어 실행했다고 주장하지 않는다. 17437-04의 source/E를 변경하지 않았고 pending/proof=null 상태를 유지한다.
