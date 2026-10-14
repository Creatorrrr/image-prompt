# Source-local native guards v2: read-only contract proposal

Status: proposed design only, 2026-10-15. No production, test, source, proof, catalog, runtime, Git, provider, or network changes. This note and its JSON companion are new immutable research files. No tests or admission experiments were run for this design. Source truth, shape/hash validity, request admission, and final image pixels remain separate claims.

## Recommendation and compatibility

Add an explicit opt-in `photo-native-source-guards/v2` nested block under `conditions.native_guards`. Keep top-level role evidence v4, valid owner-map v2/v3, owner selections v1, immutable pack and outer owner-resolution receipt contracts. A valid v1 guard retains its exact fixed-role and literal-value semantics, including its existing entity-relation RHS comparison. Dispatch by the exact schema tag; malformed v2 never retries v1 or an old condition tree. Ordinary source intrinsic human/adult/domain conditions and each applicable layer remain AND constraints.

The endpoint is exactly `{kind: "source_target", candidate_id: <CID>, target: <source-local target>}`. It never contains a caller owner ID, a guessed neutral role, a path to the first matching owner, or a fabricated anatomy label. CID follows the existing candidate-ID contract. Target follows the existing concrete nonblank/no-wildcard/no-trailing-dot rule, including specific names and Korean strings; no new lowercase naming restriction. Resolve it through that exact selected node's native owner map and the existing caller mapping, using the graph's explicit equivalent canonicalization only. Actual RID is obtained from the checked selected closure, never inferred from the endpoint or chosen as the first available branch.

The source declares the requirement; the caller supplies existing `owner_selections`; the auditor resolves and verifies it. This does not supplement the candidate-free core or mutate/reissue the one public pack.

## Exact tagged shapes

A v2 block has only `schema` and `rules` (1..64, unique rule IDs). Each rule has exactly these fields:

* `owner_relation`: `id, kind, relation, left, right`; relation is `part_of` or `disjoint`; endpoints are source-target objects.
* `frozen_value`: `id, kind, owner, dimension, property, value`; value uses the existing exact typed-value contract.
* `frozen_entity_relation`: `id, kind, left, right, dimension, property, value_type`; value_type is exactly `entity.owner_id/v1`.
* `preserve_established_scope`: `id, kind, owner, scope_kind, known_absent, known_present, unknown`; existing exact flags remain `not_applicable`, `preserve_all_frozen_items`, `review_required`.

No mixed role/target endpoint fields, shorthand, default CID, target aliases, unknown fields, count predicates, OR, quantifiers, or new owner creation. Dimensions/property/type restrictions remain existing contract restrictions. The companion JSON contains illustrative guard blocks, not authored candidate proofs.

For v2 frozen_entity_relation only, find exactly one required frozen fact on the resolved left entity with exact dimension/property/type. Its value must be a real graph owner ID whose explicit-equivalence canonical ID equals the resolved right owner. Do not treat part_of as equality, parse role words from values, or canonicalize arbitrary typed literals. A fixed opaque string is a frozen_value, not an implicit owner pointer. Preserve v1 behavior byte-for-byte.

## Selected closure and condition provenance

Build one checked context from pinned source/proof, the root's actual RID, exact dependency choices, and source-bound presentation. A CID maps to one actual selected RID; conflicting reuse fails. A CID address cannot adopt a child or cause a catalog/global lookup. Every reference must already be in the qualified selected dependency closure; selected optional branches are explicit, never all adopted by default. No extra unused owner bindings or inactive child selections are silently ignored.

Use these bounded endpoint namespaces:

| Condition layer | Declaration / activation | Allowed source-target CIDs |
| --- | --- | --- |
| Source common | Own CID; evaluated for actual own RID | Self and required direct children declared for that RID |
| Actual branch | Own CID + actual own RID | Self and required direct children of that branch |
| Parent member pointer | Parent CID/RID; activates for exactly that selected child CID/RID | Parent and that child only |
| Source-owned presentation binding | Presented child's CID/RID, AND with its source | Presented child and its required direct children only |
| Explicit old binding on a member | Parent member frame plus binding's presented child CID/RID | Presented child and its required direct children only |

The parent member-pointer layer can express a parent-to-selected-child relation. The old-binding layer cannot silently acquire that parent namespace. Nested relationships are expressed at the relevant parent layer. A common guard referring to a required child must be well formed for every RID where the common guard applies. Optional child conditions activate only upon selection; a parent common guard cannot make an optional child implicitly mandatory. Cross-sibling/ancestor/external references are outside this minimum contract. Ambiguous owner/branch choice stays pending rather than choosing a source interpretation.

Represent each internal condition frame with declaring CID/RID, activation CID/RID, layer kind, exact sealed guard-set JSON pointer and condition hash. Member frames also bind the declaring parent's meaning/qualification/reference closure and selected child projection; explicit presentation binds its actual pinned binding/proposal ID and canonical hash. For compact sealed member guard sets, `/member_conditions/<childCID>/0` and `/1` distinguish member-pointer and consumed old-binding layers, bound by the parent proof/reference hashes; a display binding is not semantic identity. Source common/branch use `/source_conditions/0` and `/1`. Rule identity is frame identity plus rule ID, never a bare ID or array index alone.

The caller cannot submit trusted frames. Full and compact consumers reconstruct or verify them from pinned/sealed sources; anonymous `_native_extra_conditions` is insufficient for v2 and must fail if no checked origin frame exists. A standalone child entry must not reinterpret a parent-authored condition as a self-authored condition. `requirements.concept_units/relations` remain positive render/semantic obligations, not auto-renamed guard predicates or inferred P facts.

## Guard-only owner inventory without fake facts

Current owner-map validation requires exactly active fact targets plus E receivers, so a holder used only in a part_of guard has no honest map row. Extend the wanted target set only with self-CID endpoints from that node's own sealed common/actual-branch v2 guards. The map still has no unused rows. It is unnecessary and misleading to invent a dummy P/E fact to admit a guard-only owner.

A member-pointer/presentation layer may reference only targets already present in the parent/child qualified map. It cannot inject new map rows or conditional bindings into another proof. In particular, a parent owner used only by an optional member condition must already be justified by a parent fact or own common/branch guard; otherwise this minimum design rejects it for explicit reauthoring. This avoids changing the existing exact active owner-selection inventory and avoids forcing unused optional-only caller bindings.

Every v2 endpoint must resolve through an `origin: existing` row and an actual frozen graph owner. Selected-existing mappings retain the existing exact required `subject/entity.presence`, `entity.presence/v1`, `present` witness. Fixed existing roles retain their explicitly grounded graph-role contract. Neither role labels nor generic presence prove face, hand, mug material, count, or any anatomy; each concrete prerequisite still needs exact source-authored typed evidence. An introduced map row fails a frozen guard by its declared origin, not by a substring/prefix guess about the actual owner name. Its synthetic address/add_entity cannot self-witness a frozen relation.

Keep all current caps: 64 selections, 32 bindings/node, 32 graph owners, 64 core assertions, depth8, edges8, 32 RIDs, 2048 source units, 4096 facts, 64 guards/block. No truncation or auto-fill. The endpoint reference set is bounded by those existing nodes/maps and rule count.

## Grounded semantics and mutation boundaries

`part_of` needs the explicit graph path in the stated direction, after explicit equivalence only. Same entity is not a strict part of itself; an equivalent alias alone cannot satisfy containment. `disjoint` uses the existing explicit graph witness semantics, including already-supported enclosing-scope disjoint edges; siblinghood, different IDs, same holder, and graph absence are insufficient. Preserve exact supporting graph edges/core assertion IDs when available, with graph/core hash as the binding. Do not invent relation assertions to make a case pass.

frozen_value requires one exact owner/dimension/property/type/value fact. Generic atomic presence is separate from body-part owner identity: face-presence on a character does not create a face owner or part_of edge. Existing common protocol is subject/entity.presence and subject/anatomy.face/hair/nails/eyes/mouth/lips.presence, each matching type `<property>/v1` and `present`; age.declared is age. New source-specific hand/material prerequisites require independent exact typed facts, not a fabricated common alias. body.parts arrays remain exact, never subset/minimum tests.

A guard is a condition, not permission to mutate a locked property. Retain source-local E consistency, resolved actual canonical owner E consistency (value/type/operation/canonical receiver set), exact P and preservation checks, whole selected effects/receivers and all lock relations. Do not compare a prerequisite's old value with an E new value as if they were duplicate assignments. Unknown overlap still denies. Part and whole locks retain existing overlap semantics; disjoint owners remain distinct.

Current preservation calls `permission_scope()` to collect whole effects. Making that public function validate v2 guards directly would recurse. Use two internal phases: (1) checked node/condition context, exact owner resolution and pure whole-selected-effect collection; (2) common guard evaluation consuming that resolved footprint. The public permission_scope path must require successful v2 guards before returning a usable scope, but preservation must call the pure collector, not the checked public function. Keep the pure lock predicate pure; a record-aware permission entry point must use the common checked context. No public final skip-guards switch. This is the main implementation coordination point.

## Search, composition, audit and receipts

Unselected owner or required dependency choices are explicitly unresolved: discovery may return search_only/review_required plus source-target requirements, with no qualified-guard claim. Any independently resolvable failed condition still rejects. A choice may not turn a failed frozen relation into a fallback. Strict admission, permission, member adoption, compose-audit and final render require every active endpoint and condition resolved and verified.

The immutable retrieval pack retains the raw v2 condition and unresolved descriptors. Composer supplies the unchanged owner_selections payload before lock checks. compose-audit reconstructs exact root/selected-child frames from the pinned pack/source/proof, verifies all guards/effects/locks, then emits the existing owner-resolution receipt with its composed/core/graph/mapping/selected-closure hashes. Runtime fresh audit recomputes the same mapping and selected closure from the same composed hash and rejects stale receipts or post-success rebinding. Failed-audit correction and identical-input replay remain supported.

Do not gratuitously version API preflight/runtime_sources or public pack transport. Existing receipt hashes bind the exact guard-bearing proof/pack and current frozen graph; fresh audit executes the guards again. Guard detail can be an audit-local native_guards.rules trace with exact frame/endpoint/actual owner and graph/fact witness references. If durable per-rule witness traces later become a product requirement, version that separate subreceipt explicitly rather than silently changing existing receipt v1. Do not treat an old successful audit from older code as new v2 validation; root must rebuild/publish the changed runtime contract before use.

## Case plans; source qualification remains separate

1278 original and formal02 source_after are still `blank face with warm helpful hands` / `무표정하지만 손은 따뜻한 인상`, intrinsic human; formal02 status pending. A future manually reviewed existing-character application can use local character, face, and hand-region targets, face part_of character and hand-region part_of character, with explicit disjoint face/hand regions if the actual scope requires it. A secondary/background character works equally if frozen graph and literal prerequisites support it. Source warmth is a presentation impression here; do not silently author measured temperature or a concrete helping action. An aggregate hand-region must not become two individual owners automatically. The relationship proposal does not cure missing contrast/hand effects, rewrite wording, or approve this source.

1296 original/formal02 source_after are still `warm mug held in both hands` / `두 손으로 감싼 따뜻한 머그`, no intrinsic category, pending incomplete application/effects/thermal meaning. An explicitly authored existing-owner-only pilot can bind holder, hand_a, hand_b and mug. Require hand_a part_of holder, hand_b part_of holder, hand_a disjoint hand_b and independent exact concrete carriers. This proves two selected distinct existing hand owners share a holder; it does not assert an exact total limb count. Holding is the actual adopted effect with explicit mug receivers and permissions, not a prerequisite that the mug must already be held. Only an explicit source requirement to preserve an already-established entity relation may use frozen_entity_relation. Actual warm temperature is also an effect unless a separately read source explicitly makes it an unchanged prerequisite. Source effects/count/subject/creation cannot be hidden by the selector or guard. Introducing a mug is a separate application contract, outside this proposal.

A frozen_entity_relation fixture should use a deliberately authored relation whose frozen RHS is a real owner ID (for example an exact fixture-specific relationship property), not infer ownership from the English word holder. This demonstrates mechanics without manufacturing a corpus semantic claim.

## Minimum implementation and test plan, not authorization

Required changes likely: photo_semantic_evidence.py (tagged validator, guard-only inventory, origin-aware shared resolver/effect collector/evaluator); photo_candidate_corpus.py (source/presentation frames); photo_shared_views.py (parent/member frame); photo_candidate_realizations.py (eligibility checked-root context); photo_candidate_semantics.py (bundle/member context); photo_search_layout.py (compact frame/seal preservation); prompt_generator.py (search-vs-strict conjunction); audit_composed_prompt.py (pinned reconstruction/final trace).

Verify existing pass-through paths before changing them: photo_role_proposals, global/slot retrieval, search reader, public pack, workflow coordinator/worker and audit_image_render_request. They already carry conditions/selections or freshly compare receipt/composed hashes. Modify only if focused parity tests demonstrate a dropped frame; root approval should set that exact allowlist first. Neutral core schema needs no candidate-aware axis or new owner vocabulary. Research native review/adoption tools should retain top proof v4 and consume the shared validator; no automatic source/proof migration helper is warranted.

Planned focused tests, all isolated source fixtures, not actual candidate approval:

1. Secondary/background positive with two explicitly selected hand owners, same holder part paths and explicit disjointness; equivalent aliases resolve canonically; full/compact/selected lazy/materialized/member/public-profile/final/runtime agree.
2. Wrong holder, reversed/missing part edge, equivalent-as-part, unknown siblings, same hand selected twice, absent disjointness and synthetic introduced endpoint all reject.
3. frozen_value wrong owner/property/type/value and frozen_entity_relation wrong/nonowner RHS reject; exact canonical alias RHS passes v2 only, v1 literal semantics unchanged. P old to E new remains valid.
4. Missing/stale/wrong/unused selections, wrong RID/CID/proof/core/graph/closure, forged condition frame, missing origin, changed explicit old-binding condition/hash reject; same CID cannot be silently used on two RIDs.
5. Optional unselected child has no guard/effect obligation; selected child/member requires its full guard and semantic requirements; parent pointers cannot borrow sibling/foreign targets. Common guard cannot implicitly adopt an optional child.
6. Partial locks, equivalent/part/disjoint receiver effects and established-scope inventory/final preservation behave identically; valid guard does not waive a receiver lock. Known absent/present/unknown remain distinct, and no recursive evaluation occurs.
7. Search-only unresolved remains retrievable with immutable pack bytes; final fails unresolved; supplied choices strictly recheck. Success rebind fails; failure correction and same-input replay pass; runtime demands exact composed/receipt equality.
8. v1 guards + v2 fixed maps unchanged, v3 fixed/selected mixtures valid, malformed version/extra field/unknown target/unused guard-only map fails. No renamed part aliases, anatomy inference, body.parts subset matching, count/OR, implicit parent/primary, or automatic source conversion.

Root must separately approve exact code scope and author actual source/proof revisions, then run focused plus integration tests and rebuild/publish/acquire. This design does not accept either pending source, change catalog approval, or claim whole-corpus native qualification.
