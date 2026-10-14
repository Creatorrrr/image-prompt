# 1299 실제 가시성·프레이밍 영향: A/B 설계 제안

대상은 선택된 `8acdd741…`의 1299 한 건이며, catalog149V6와 frozen `50fd92…`를 기준으로 한다. 이 문서는 코드·소스 변경이나 native 승인이 아니다. 원래 세 효과인 image의 `shot.scale`, image의 `framing.coverage`, item의 `action.interaction.exchange`와 각각의 실제 receiver union, mode, operation, P, 다섯 source guard를 그대로 유지한다. 첫50-05/06의 원문1299 보류와도 별개다.

## 관찰한 한계

`FOOTPRINT-COUNTEREXAMPLE-v2.json`은 **승인되지 않은 literal projection**을 frozen B1 resolver와 실제 property 검사 함수에 전달한 연구 재현이다. Native source qualification, B2 P/PR/guard matching, full/compact admission이나 실제 운영 소비 성공을 뜻하지 않는다.

명시적으로 선언한 3개 손, item, 두 얼굴, 두 몸통 부위와 같은/다른 carrier의 두 fixture에서, 겹치는 item/hand/frame-inventory receiver는 정확한 합집합으로 확장됐다. 선언된 세 속성의 각 실제 잠금은 거절됐다. 그러나 그 합집합 안의 F1 `subject.visibility`, F2 `body.framing`, R1 `framing.inclusion`, U `subject.visibility` 잠금은 두 fixture 모두에서 property primitive를 통과했다. 이미 포함된 부위의 이런 속성을 실제 crop이 바꾸더라도, receiver 확장은 기존 속성명 세 개를 반복할 뿐이다.

또한 실제 요청 전문에는 있는 F2를 inventory에서 빼고 새 hash를 계산하면 B1 구조 검사는 통과했다. 잘못된 hash·누락된 scope·원자적 presence 누락을 거절하는 것은 필요하지만, 의미상 완전함을 증명하지 않는다. v1의 독립 fixture evidence가 baseline에 없어서 올바르게 거절된 실패도 별도로 보존했다.

따라서 문제를 나누어야 한다.

- 이미 선택된 **물체 handoff, macro, hands-only participant anatomy**의 의미는 이제 분명하다. 원래 ambiguous exchange label만의 문제로 돌릴 수 없다.
- 실제 요청의 affected owner/part 목록과 각 속성의 변화·보존 여부는 아직 제공되지 않았다. 이것은 **독립 입력·직접 읽기 부족**이다.
- 현재 kernel은 exact property path의 동일·부모/자식 겹침과 실제 alias/ancestor를 검사하지만, `framing.coverage`가 별도 `subject.visibility`까지 영향을 준다는 source별 관계를 표현·소비하지 않는다. 이것은 **표현/소비 계약의 공백**이다. 전역 substring alias로 고치면 안 된다.

## A. 실제 scope별 가시성·crop 효과/보존을 source에 직접 명시

각 실제 요청에서 independently declared image, hands, item, carrier, nonhand regions와 그 topology를 먼저 읽고, **실제로 발생하는** 변경을 추가한다. 새 부위나 사람을 만들어 scope를 채우지 않는다.

| 실제 의미 | 가능한 직접 기록 | 주의점 |
|---|---|---|
| 참여 손의 frame 포함·가시성을 선택 | 실제 participating-hand scope의 `subject.visibility=visible` E | 손 type/presence·실제 image 대응은 독립 P. desired hands-only를 P로 얼리지 않는다. |
| 기존 얼굴·몸통 등 참여자 비손 부위를 crop으로 제외 | 정확한 actual nonhand-region scope의 `subject.visibility=excluded_from_selected_frame` E | 기존 포함 상태를 바꾸는 실제 선택이다. 얼굴과 몸통 전체가 없다고 하거나 carrier를 손과 동일시하지 않는다. |
| carrier의 신체 포함 범위를 손으로 제한 | actual carrier의 `body.framing=participating_hands_only` E | carrier 전체가 invisible이라는 거짓 효과와 구별한다. 여러 carrier는 실제 연결별로 묶는다. |
| 별도의 실제 frame inclusion 주소가 보호됨 | 그 inclusion 범위에 실제로 일어나는 변경을 정확한 `framing.inclusion` 주소로 기록 | visibility와 동일한 한 변경의 다른 이름뿐이면 추가 동작을 발명하지 않는다. 아래 B의 source별 permission 관계가 더 적합할 수 있다. |
| 같은 item이 계속 visible | 정확한 same-item/same-image `subject.visibility=visible` PR | physical presence와 다르다. 이미 visible이라는 독립 witness가 없으면 PR은 불충족이다. |

이는 원래 image framing E를 삭제·재명명하는 방법이 아니다. Crop이 실제 body-region visibility와 carrier coverage를 바꾼다면 그것은 이미 선택된 의미의 빠진 효과면/permission projection이며, 새 손동작·카메라 이동을 덧붙이는 것과 다르다. 다만 같은 의미를 임의 property 세 개에 복제해 role 수를 늘리는 것은 정당하지 않다. 각 주소가 실제 요청에서 어떤 상태를 가리키고 무엇이 바뀌는지 먼저 직접 판정해야 한다. 한 물리 선택에 여러 permission projection이 필요하다는 사실과 여러 독립 동작이 있다는 주장을 구분한다.

### A의 최소 변경과 한계

1. Root가 실제 request-specific source after 또는 명시적인 actual branch를 선택한다. 새 E/PR의 target, 값, 양성 구절, exact property, receiver, mode와 P를 각기 명시하고 fullafter를 다시 읽는다. 기존 세 canonical E와 모든 이전 의무는 남는다.
2. Core에는 input-bound participating hands, affected nonhand regions, actual carrier topology가 따로 필요하다. 숨겨질 부위와 손·item은 동일한 상태를 받지 않으므로 혼합 union 전체에 `invisible` 같은 값을 일괄 적용할 수 없다.
3. 알려진 비어 있지 않은 균일 scope와 exact properties는 현재 member-scope/typed-fact 체계로 표현할 수 있다. 기존 E를 그대로 둔 추가 actual E/PR라면 기본 kernel의 exact-property·alias·ancestor 검사를 사용할 수 있다. **그 자체가 현 source/proof에 이미 구현되어 있다는 뜻은 아니다.** 새 source/input/proof가 필요하다.
4. 실제 비손 부위가 없거나 일부 carrier가 입력에 없는 경우도 원래 application은 허용한다. 현재 known-present 비어 있지 않은 member scope를 채우려고 가짜 부위를 만들면 안 된다. 독립적으로 확인된 absence branch가 필요하거나 그 좁은 application만 제한해야 한다. 이를 generic source에서 자동 분기할 수 있는지는 별도 표현력 문제다.
5. 각 요청의 다른 property 어휘까지 모두 보장하려면 actual address plan을 다시 작성해야 한다. 몇 개 표준 이름을 추가해 모든 미래 unknown/custom lock을 닫았다고 주장할 수 없다.

## B. Source가 명시적으로 허용한 permission footprint 계약을 소비

Source의 세 canonical 효과와 값은 유지하고, 그 **효과가 permission 검사에서 반드시 함께 대조해야 하는 실제 속성 범위**를 별도 명시한다. 예를 들면 coverage E와 macro E가 선택한 crop에 대해, source가 선언한 같은 actual frame union의 실제 visibility/body-coverage/inclusion 보호 주소를 추가로 대조한다. 이것은 새 효과 사실이나 role view가 아니며, 어떤 visible/invisible 값을 실제로 생성한다고 주장하는 도구도 아니다.

계약은 적어도 다음을 묶어야 한다.

- 정확한 CID/RID, 원 canonical fact/E-set hash, effect mode·operation, ordinary positive source-unit/전체 application hash.
- Source별로 수동 승인한 **방향성 affects/permission-overlap 관계**와 적용 이유. `framing.coverage`와 `subject.visibility`를 전역 동일어로 만들지 않는다. 기존 source/property 주소도 보존한다.
- Caller가 discovery 전에 독립 입력 전체에서 작성한 actual footprint plan: image, 모든 affected owner/region, 정확한 보호 property 주소, 적용되는 ancestor, 의미상 영향 설명, input spans/IDs, 검토자와 exact core/input/topology 해시.
- unknown·누락·stale·미검토 입력이 있으면 final adoption을 거절하는 상태. Unknown property를 모두 같은 것으로 단정하지 않고, **겹치지 않음이 증명되지 않아 보류**한다고 기록한다.
- Permission 검사에서 exact 기존 E/Rx 전체와 envelope를 **합집합으로** 대조한다. Envelope가 기존 target, receiver, lock 또는 whole dimension을 제거·축소할 수 없다. 이미 보호된 frame 속성에 대해 새 role이 우회 경로가 되지 않는다.

### B의 최소 구현 경계

1. Source 계약과 native proof의 수동 authored 필드·검증 규칙이 필요하다. 근거 없는 extra key나 prose만으로 소비됐다고 볼 수 없다. Envelope는 signature, compact representation, cache/source pins, root/dependency closure에 포함되어야 한다.
2. B2는 B1의 **동일한 resolved actual bindings/view**를 사용해 envelope를 소비해야 한다. 두 번째 owner lookup이나 source-created subset을 허용하지 않는다. 현재 B1 node/fact schema는 exact fields이고 permission scope는 expanded E 사실에서만 생성되므로, 새 필드를 그냥 전달하면 되는 구조가 아니다. Versioned protocol을 확장하거나, B1 view에 결합된 명시 B2 receipt가 필요하다.
3. 현재 `photo_contracts.property_effects_allowed`는 exact/parent path와 실제 owner overlap만 안다. Source별 envelope 검사 또는 새 명시 permission primitive가 필요하며 full/compact, old binding consumer, final audit가 같은 receipt를 써야 한다. 이 문서는 그 코드를 작성하지 않았다.
4. Envelope는 값 대입 사실이 아니므로 B1 effect-assignment ledger에 새 가짜 E를 넣어 conflict 검사를 통과시키면 안 된다. 다른 선택 후보가 같은 실제 부위의 visibility를 바꾸는 경우, envelope와 그 후보 E의 결합도 검사해야 한다. 값 호환성 근거가 없으면 conflict 여부를 unknown으로 두고 fail closed 한다. 같은 사실이라는 자동 alias를 만들지 않는다.
5. 단순한 conservative 규칙으로 union의 partial framing 보호를 모두 거절할 수도 있지만, item-visible PR처럼 **명시적으로 그대로 유지되는 속성**은 별도 독립 PR 근거로 구별해야 한다. 무조건적인 ‘모든 unknown property는 동일’ 판정은 금지한다.

## Item visible과 complete inventory에 필요한 독립 근거

`remains visible`은 같은 active image에서 이미 visible인 같은 item을 유지한다는 PR로 읽는 것이 가장 좁다. `entity.presence=present`만으로 visible을 만들지 않는다. Core/입력에 정확한 image 대응과 독립적으로 frozen된 `framing / subject.visibility / subject.visibility/v1 / visible` witness가 있어야 하고, 실제 PR matching과 final output preservation 확인이 필요하다. 다중 image에서 전역적인 item-visible assertion만 있으면 image별 scope가 불분명하므로 보류한다. 숨겨진 item을 새로 보이게 하는 해석을 원하면 root가 source를 따로 바꾸어 actual visibility E와 모든 permission을 다시 심사해야 한다.

Complete inventory에는 실제 active request text, reference/input inventory, 실제 owner/part declarations와 selected crop에 대한 직접 검토가 필요하다. 각 member의 atomic presence, source span/input IDs, 실제 type, alias/equivalence와 part edges가 필요하다. Hands/item과 frame scope가 겹치면 canonical union은 중복 제거하되 원 provenance를 버리지 않는다. Carrier를 손으로 alias하거나 descendants를 자동 추론하지 않는다. 모든 실제 입력을 읽지 못했거나 실제 affected region을 주소화하지 못하면 ineligible이다. Complete flag·새 hash·문법 검사는 이 직접 검토를 대신하지 않는다.

## 테스트·bounded closure 계획

- 두 carrier와 같은 carrier 각각에서 initiating hand + 다른 손 두 개, item, 실제 faces/torso/전체 affected regions를 사전에 명시한다. 정확한 independent P와 모든 다섯 guard, source/ownbinding 조건을 full/compact admission과 실제 consumer에서 확인한다.
- 손·item의 반복 receiver와 inventory overlap이 정확히 합집합이 되는지, aliases가 새로운 member로 중복되지 않는지 검사한다. Each actual target/Rx/part ancestor의 각 선언 E와 추가 visibility/body-framing/inclusion 주소를 개별로 잠가 거절되는지 확인한다.
- Frame 전체 lock, 다른 차원에 기록된 같은 보호 속성, known custom property, 의미가 unknown인 보호 주소, 같은 E에 겹치는 다른 후보의 실제 변경을 포함한다. Unknown은 근거 없이 compatible로 처리하지 않는다.
- Item visible PR의 missing/wrong/stale/same-item-but-other-image 대조를 포함한다. Desired hands-only를 frozen P로 바꾼 거짓 우회 fixture는 거절한다.
- Missing/stale/incomplete scope, member presence/type 누락, 마지막 손/마지막 region 누락, 새로 hash한 거짓 complete 목록, 미검토 입력, 주소화 못한 carrier/region, 알려진 absent/empty branch를 분리한다. Hash-valid omission은 **semantic review gate**가 거절해야 하며 B1이 알아냈다고 꾸미지 않는다.
- CID/RID 하나와 실제 선택된 required/optional child/root만 bounded closure로 묶는다. 현재1299 required CID/binding closure는 비어 있다. 향후 compound는 동일 actual selected-closure의 guards, P/PR, E/Rx, profile/ownbindings와 envelope를 같이 pin하고 미선택 optional 의미를 끌어오지 않는다.
- 검증 단계는 source/literal 직접 검토 → shape/signature/compact → independent exact core admission → actual old-binding consumer → each-property/ancestor/whole locks → joint selection/final audit 순서로 구분한다. 실제 request/core freeze/render/pixels와 root acceptance는 별도다.

## 제안하는 진행 순서

먼저 A로 실제 한 요청의 각 visibility·carrier-coverage 영향을 명시해 비교 가능한 양성/음성 기준을 만든다. 이는 원 source를 몰래 일반화하지 않는 좁은 demonstrator다. Generic 1299가 요청별 다른 보호 주소와 비어 있는/nonhuman carrier 경우까지 다루려면 B 또는 동등한 명시 actual-property plan 계약이 추가로 필요하다. B는 permission의 보수적 확장일 뿐 새 상태 사실의 대체물이 아니므로, A의 실제 의미 검토를 생략할 수 없다.

두 경로 모두 현재는 **설계 제안**이다. Source-only clarification, B1 addressing 성공, shape PASS만으로 1299 native pending을 해제하지 않는다. Root가 source 선택과 구현 범위를 결정해야 한다.
