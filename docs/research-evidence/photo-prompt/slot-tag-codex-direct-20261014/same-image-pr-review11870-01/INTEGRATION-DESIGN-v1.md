# Same-image PR와 필수 permission envelope 통합 설계

검토자 `/root/review_11870_12250`, gpt-6.1-sol/high. 실제 구현이나 source 선택은 하지 않았다. Bulk는 [1500,1635) 135/750에서 동결했고 다음 위치는1635이다. 이번 문서와 독립 synthetic 실험은 그 집계를 늘리지 않는다.

## 1. 기존 guard로 해결할 수 있는 image 연결

`SOURCE-PROPOSAL-v1.json`은 현재 source65의1299(`8acdd741…`, record `e9870bd…`) 전문을 before로 고정하고, App에 same-item/same-selected-image 보존의 정확한 뜻을 보완한다. 기존 EN/KO, 세 canonical E 주소와 의미, App의 모든 실제 receiver, 다섯 v3 guard는 그대로다. 새 선택 효과나 실제 visibility 생성은 추가하지 않는다. 첫50 원문1299 보류/이전 배치와는 별도이며 root가 아직 선택하지 않은 source-only 후보이다.

추가 guard의 정확한 형태는 다음과 같다.

```json
{
  "id": "item_visible_in_selected_image",
  "kind": "frozen_entity_relation",
  "left": {"kind":"source_target","candidate_id":"cand_2e72784a26885ceaa1d645d25bd9a468","target":"exchange_item"},
  "right": {"kind":"source_target","candidate_id":"cand_2e72784a26885ceaa1d645d25bd9a468","target":"image"},
  "dimension": "framing",
  "property": "framing.visible_in",
  "value_type": "entity.owner_id/v1"
}
```

별도의 기존 literal PR은 `framing / exchange_item / subject.visibility / subject.visibility/v1 / visible`, mode=`preservation`으로 유지한다. Guard는 실제 item의 owner-valued frozen relation이 **선택된 실제 image**를 가리키는지 검사한다. PR은 같은 item의 별도 visible state를 검사한다. `entity.presence`나 이름이 image인 selector만으로 어느 조건도 충족하지 않는다. 실제 image라는 입력 의미와 owner 선택 역시 독립적으로 직접 읽어야 한다. 현재 proposal은 자동 image-kind 추론이나 새 중립 type convention을 만들지 않는다.

Frozen `photo_semantic_evidence.py:1736–1772`는 v3에서 scalar `frozen_entity_relation` atom을 허용한다. `1928–2023`, 특히1976–1983은 동일한 B1 resolved binding의 left/right owner를 사용해 exact dimension/property, `entity.owner_id/v1`, 실제 right owner를 비교한다. `_same_entity`는 명시적 equivalence만 허용한다. I2와 I가 다른 실제 image이면 global item-visible 값이 있어도 relation이 거절된다. `1030–1048`은 literal visible PR을 계속 별도로 소비하므로 relation만으로 누락·hidden 상태를 대체할 수 없다.

이 guard를 tag의 긍정 역할 근거로 포장하지 않는다. Frozen `_guard_support_rule:78–100`의 역할 근거 opt-in은 v1/v2만 지원한다. v3 guard는 기존 source 조건으로 실행할 수 있으나 새 guard_support role claim을 자동 생성할 수 없다. Fresh proof에서는 App 전체 source unit, 기존 fact/PR와 실제 guard 의무가 어떤 뜻을 보존하는지 수동으로 확인해야 한다.

### 독립 실험과 한계

`guard_experiment_v3.py`는 현재1299 pseudo proof를 qualified라고 가정하지 않았다. 별도 synthetic CID/소스·작은 fixture catalog·one-E macro fixture를 수동 작성해 기존 fixture serializer로 구조를 만들었다. 이 synthetic fixture의 리뷰 메타데이터는 root의 독립 source 권위가 아니며 실제1299 승인으로 재사용할 수 없다. 원1299의 세 효과와 전체 member scope/five guards를 이 작은 fixture로 모두 검증했다고 주장하지 않는다.

실제 frozen50fd92의 corpus schema, B1, B2 `admission`, full/compact entry, `core_entry_eligible`로24개 조건을 확인했다. 같은 I, 같은 I2 선택, 실제 alias는 통과한다. 다른 image, relation 누락, literal PR 누락/hidden, exact type 오류, item/image presence 누락, alias 없는 이름 유사성은 거절한다. 원 `shot.scale` 잠금은 admission과 별개의 실제 consumer permission 단계에서 거절되며 guard가 이를 면제하지 않는다.

추가4개 대조는 안전성 성공에 포함하지 않는다. 실제 I2 source 문장인데 typed value를 I라고 거짓 기재하거나 무관한 active span을 인용하면 현재 tuple matcher는 그 자연어 의미를 증명하지 못한다. 이들은 독립 core 작성자가 잘못된 증거를 승인한 테스트이며 candidate가 retained pin을 위조한 사례가 아니다. 실제 core freeze 전 전체 입력·source span·image 대응의 직접 검토가 필요하다. 실제 normalized workflow freeze를 실행한 결과도 아니며, full final audit/pixels/runtime 보존을 검증하지 않았다.

따라서 root의 source 선택 → exact 새 ASSIGNMENT/INPUT → 전체 current/원문/5B/bindings/closure/spec/guard/P/PR/E/Rx fresh proof → 실제 독립 core admission이 필요하다. 현 proposal과 synthetic 통과만으로 actual1299를 승인할 수 없다.

## 2. Prototype02를 필수 native 계약으로 연결하는 최소 선택안

현재 working 파일과 frozen50fd92의 native, prompt, audit, owner resolver, property contracts, witness 파일은 각각 byte-identical함을 확인했다. 아래 범위는 실제 읽은 해당 함수에 근거한다. Working tree에 envelope 기능이 이미 존재한다고 보지 않는다.

| 단계 | 현재 실제 경계 | 최소 필수 연결 |
|---|---|---|
| Source 선택/권위 | `native_contract_sha256:174–179`는 review binding과 proof bytes를 묶지만 self-hash가 source 진실을 증명하지 않는다. Prototype의 BoundSource도 구조 binding이다. | Root가 App의 envelope 허용 뜻과 versioned 실행 계약을 먼저 선택한다. 실제 source snapshot/CID/RID/catalog/전체 positive units/whole guards/profile/ownbindings/selected closure/E3를 독립 trusted source manifest에 고정한다. Candidate가 내는 expected pins를 권위로 받지 않는다. |
| Schema/qualification | `_proof_fields_valid:65–66`는 현재 정확히 v4 필드와 guard_supports/manual_role_views만 허용한다. | Versioned 필드나 명시 opt-in을 엄밀하게 추가한다. Source가 envelope 필수라고 선언한 경우 proof/선택 계획이 없으면 strict adoption 거절. Unknown 필드를 무시하거나 self-hash optional field만으로 통과시키지 않는다. App ordinary positive anchor가 있어야 하며 metadata/tag만으로 overlap을 승인하지 않는다. |
| Compact/closure | `compact:855–893`는 full source/catalog로 validate한 뒤 units/review/quotes를 제거하고 dependency guards와 qualification hash를 봉인한다. | Full source에서만 검증 가능한 envelope 권위·ordinary-unit anchor와 exact closure를 먼저 검사해 source-bound compact binding으로 보존한다. Parent/child actual RID 및 required/explicit optional 선택마다 다시 묶는다. Compact의 self-report나 누락된 optional member를 full 의미로 사용하지 않는다. |
| 독립 입력/plan | Prototype inventory의 complete/hash는 의미 완전성을 증명하지 않는다. | Discovery 전 실제 request/reference/input 전체에서 owner/part/alias/actual affected scope와 protected property/whole locks를 작성한다. Source별 impact plan은 이후 실제 source와 대조해 수동 심사하되 이 pre-discovery inventory를 축소할 수 없다. Unknown/incomplete/unread/empty-unaddressable branch는 final ineligible. 새 hash로 빠진 face/마지막 손을 정당화하지 않는다. |
| 같은 B1 view | `_resolve_selected_native_contracts:1260–1322`는 qualified-source-checked selected closure에서 projection을 만들고 B1을 호출한다. | Envelope도 이 coordinator가 만든 동일한 all-selected-roots view만 소비한다. 별도의 selector/descendant lookup 금지. Outer B2 context에 exact source authority·inventory·manual plan·view binding을 붙일 수 있으나 B1 E ledger나 node schema에 가짜 E를 넣지 않는다. Context reuse/cache key에 새 binding이 포함되어 stale 계획을 재사용하지 않아야 한다. |
| Admission/permission | `admission:965–1095`는 P/PR/guards와 owner 선택을 소비한다. `_collect_permission_scope:1423–1446`는 실제 E/Rx만의 triple union을 반환한다. | 기존 P/PR/guard admission, 모든 E/Rx 및 기존 property/whole 검사와 **항상 conjunction**한다. Envelope는 추가 permission receipt/거절이며 E triple이나 값 대입으로 위장하지 않는다. `permission_scope`의 원 E 집합을 대체·축소하지 않는다. Strict envelope plan이 없으면 search-only와 final adoption을 분리한다. |
| Consumer | `core_entry_eligible:8345–8385`는 admission → condition layers → 원 open dimensions/property 검사 순서다. | 최종 consumer는 필수 envelope receipt까지 확인한다. 내부 condition-layer의 check_effect_scope=False, lazy/compact 경로, 다른 role route로 빠져나갈 수 없어야 한다. Full/compact 결과와 기존 binding gate를 모두 검증한다. |
| Joint 선택 | `validate_joint_effect_assignments:1418–1420`은 기존 B1 assignment ledger 경계다. | Prototype02의 additional E×anchor/whole 및 cross-source E/Rx 검사를 선택된 모든 roots의 동일 view에 필수 적용한다. Exact/parent/child/wildcard path와 actual alias/ancestor/unknown-owner separation은 동일 frozen primitive로 검사한다. Unrelated property여도 수동 영향이 unknown이면 fail closed. Manual disjoint는 기계적으로 알려진 겹침을 면제하지 못한다. |
| Final audit/PR | `audit_composed_prompt.py:5965–6044`는 pinned full source를 재검증하고 corpus.entry/admission/whole closure/consumer/permission/joint를 다시 수행한다. `audit_scope_preservation:1697–1718`은 preserve_established_scope inventory 전용이다. | Final 단계도 동일 envelope authority/plan/view를 다시 결합해 검사한다. Same-image relation guard와 scalar visible PR이 있다고 해서 scope-preservation helper가 모든 scalar PR의 최종 상태를 증명했다고 보지 않는다. 실제 selected item/image, original assertion IDs, PR/guard ref, value와 result evidence를 source-bound final obligation receipt로 보존하는 명시 계약이 필요하다. |

### 필요한 데이터와 금지된 우회

Source 계약은 actual CID/RID, source record/positive ordinary-unit App hash, original canonical E set/modes/op/value/requires/all source Rx, whole conditions·profile·ownbinding·selected references와 실행 version을 묶어야 한다. 실행 plan은 exact core/input inventory/topology/B1 view, source authority, pre-discovery inventory, source별 E×protected address와 whole-dimension 영향, 다른 선택 source의 E/Rx와 joint 영향, input span/ID·검토자·이유를 묶어야 한다. 원 E와 Rx 전체가 남는지를 기계적으로 비교한다.

필수 plan의 expected binding은 run의 독립 검토/동결 자료 또는 검증된 trusted source publication에서 주입해야 한다. Entry나 candidate-provided receipt가 expected 값을 다시 만들면 self-hash만 남는다. 임의 경로의 JSON이나 caller boolean을 qualified 권위로 인정해서는 안 된다. Semantic review 자체를 hash 검사가 대신할 수 없다는 경계도 유지한다.

Envelope는 추가 permission 관계다. `framing.coverage`를 `subject.visibility`로 rename하거나 alias하지 않고, macro/coverage E를 삭제하지 않으며, desired hands-only를 P/context/no-op로 미리 고정하지 않는다. 실제 crop이 유발하는 visibility/body coverage 변화는 원 의미의 effect/permission 면으로 정당화할 수 있으나, envelope가 임의 새 invisible 값을 생성했다고 주장하면 안 된다. 실제 값 변경을 소스에 추가하려면 별도의 직접 E 의미·target·receiver·lock 심사가 필요하다.

Nonempty scope를 채우려고 얼굴/몸통/손/새 carrier를 만들지 않는다. Native가 지원하는 known-present/nonempty scope와 absence branch는 다르다. 실제 없는 scope라면 root가 명시적인 absence/bounded application을 선택하거나 pending으로 남겨야 한다. Prototype cap은 native 최대4096 facts와 같지 않다. 실제 E/anchor/joint 전체가 cap에 들어가지 않으면 일부를 잘라 허용하지 말고 해당 application을 보류한다.

## 3. Final same-image PR 검증안과 인계 순서

Final obligation은 exact CID/RID, source PR/guard locator, actual item/image canonical IDs와 명시 alias 근거, core frozen assertion ID/source span/input binding, literal visible 값, typed visible_in image 대응, unchanged topology와 선택된 output scope를 포함해야 한다. 후보 선택 전 참이었던 관계/visible 상태와 최종 유지됐다는 증거를 분리한다. 최종 prompt evidence나 별도 typed after-state inventory가 실제 같은 item/image를 지칭하는지 독립적으로 읽어야 하며, 단순 substring·ID label·새 hash는 의미 보존 증명이 아니다. Render/pixel 보존은 별도 증거 경계다.

권장 순서는 ① root가 현재 source-only same-image refinement를 선택해 fresh input 준비 ② 원 전체 source/RID/5B/ownbindings/closure/모든 P/PR/guards/E/Rx fresh proof ③ 실제 same-image/missing/wrong-image/hidden/alias/span 반례 full/compact/admission/consumer ④ root가 source-authorized envelope 계약과 trusted injection 경로 선택 ⑤ schema/compact/coordinator/consumer/joint/final PR 구현과 독립 negative tests이다. 현재 작업에서는④ 이후 코드를 수정하지 않았다.

최소 regression은 두 carrier/같은 carrier·3손·모든 실제 parts·unknown/absent scope, 모든 original E/Rx/alias/ancestor/parent-child/whole locks, frame 외 custom property, 자기재해시 누락/미검토 입력/다른 RID·source authority, same-item 다른 image·잘못된 actual source span·PR hidden, full/compact/old-binding/lazy/final-root/joint symmetry를 포함해야 한다. Prototype02의64/222를 actual149/1299 full integration 성과로 이름만 바꾸어 재사용하지 않는다.
