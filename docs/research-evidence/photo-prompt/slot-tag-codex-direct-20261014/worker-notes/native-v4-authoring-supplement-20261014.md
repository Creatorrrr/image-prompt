# Native v4 authoring and consumer supplement (2026-10-14)

This supplements the immutable v3 guides and the v4 implementation plan. It supersedes their native proof **version/guard/profile** instructions only. It does not reinterpret, convert, approve or qualify an existing source judgement. Complete manual body/spec/condition/actual-RID/dependency review, the original compiled-review locator and exact before/after source correction provenance remain mandatory. Operating source/catalog/qualified-count changes are root-owned. The executable synthetic examples are `tests/test_photo_native_v4_guards.py: guarded/scoped_core/profile_source`; they are fixtures, not reviewed corpus records or photographic truth.

## Exact source proof and guards

The only completed proof schema is `photo-candidate-role-evidence/v4`. It retains the exact v3 fields and adds mandatory `guard_sets` and `profile_contracts`. Each map covers **every actual RID exactly once**, including optional `base` when present. A present v3/invalid proof cannot fall back to approval. Absent proof is still explicitly unqualified for stage-5C retrieval only; final adoption rejects it.

`guard_sets[RID]` is exactly:

```json
{"source_conditions":[{},{}],"member_conditions":{}}
```

The first two objects repeat the actual intrinsic source conditions and actual selected-branch conditions (empty only when actually absent). Each eligible child CID maps to a two-object array repeating the explicit member-pointer conditions and any explicitly consumed temporary old-binding conditions. Never rename positive member `requirements` into conditions. Member requirements remain selected semantic/render duties with the existing manual requirement→actual-child-RID/fact/effect bindings. All consumed source references and temporary binding definitions remain in exact reference closure; old binding IDs are neither native identity nor effect sources.

Native conditions use `native_guards: {schema:"photo-native-source-guards/v1",rules:[...]}`. Rules are nonempty, unique-ID and bounded to 64. Exact allowed rule shapes:

```json
{"id":"keep_reference","kind":"preserve_established_scope","owner_role":"main_subject","scope_kind":"reference_appearance","known_absent":"not_applicable","known_present":"preserve_all_frozen_items","unknown":"review_required"}
{"id":"face_belongs","kind":"owner_relation","relation":"part_of","left_role":"primary_face","right_role":"main_subject"}
{"id":"distinct_people","kind":"owner_relation","relation":"disjoint","left_role":"main_subject","right_role":"secondary_subject"}
{"id":"declared_adult","kind":"frozen_value","owner_role":"main_subject","dimension":"age","property":"age.declared","value":{"type":"age.declared/v1","value":"adult"}}
{"id":"existing_relation","kind":"frozen_entity_relation","left_role":"main_subject","right_role":"secondary_subject","dimension":"relationship","property":"relationship.peer_to","value_type":"entity.owner_id/v1"}
```

These are independent examples, not a bundle of default requirements. Use only the rule the source actually requires. `owner_relation` supports explicit `part_of`/`disjoint`; `frozen_entity_relation` requires the left frozen property's exact typed value to equal the resolved right **actual owner ID**. No string/keyword/category guess creates a role, anatomy, alias, disjointness or existence. Intrinsic, selected actual RID, explicit presentation and selected dependency rules are ANDed. A prerequisite/context/preservation mode cannot exempt an actual canonical mutation; complete effect-mode coverage and permission checks remain separate.

Caps are generic: **32 actual RIDs** (including optional base), **2048 source units**, **4096 facts**. No truncate/autofill; one over rejects. Member 8, dependency depth 8, total native core assertions 64 and owners 32 remain unchanged. No CID/meaning-specific exception exists. Positive `field`/`review_scale` labels are validation metadata, alongside the existing routing/discovery deny keys; instruction/description/body clauses still require complete manually authored source-unit dispositions and grounded facts.

## Candidate-free caller input and scope inventory

`prepare_photo_run.py init --input-inventory FILE` accepts an explicitly caller-authored JSON object; omission stays omitted. The immutable request envelope and frozen request binding retain this exact object and hash it. Its exact fields are:

```json
{"schema":"photo-request-input-inventory/v1","complete":true,"items":[{"id":"request","kind":"request_text","sha256":"<actual request bytes SHA256>"}]}
```

Each item is exactly `id,kind,sha256`, unique ID, lowercase 64-digit SHA. Allowed kinds are `request_text,text,reference_image,identity_reference,other`; at most 32 entries. A complete inventory explicitly includes the exact request-text hash once. Any additional text, image or identity input must be explicitly listed with its actual hash; an empty array is not a fabricated absence certificate. Input kind/hash completeness is the caller's assertion, **not an independently observed tool claim**. No reference-file absence implies identity/reference appearance absence: text can establish either.

A `photo-frozen-semantics/v1` required subject assertion of kind `scope_inventory` has exact axes `native_schema,kind,owner,scope_kind,inventory`. It still needs active source spans, literal frozen-baseline evidence and subject lock. `scope_kind` is exactly `reference_appearance` or `requester_identity`. `inventory` is an exact canonical JSON **string** (sorted keys, compact separators, Unicode unescaped, no NaN/duplicate keys, at most 65536 characters); raw and normalized wire values must remain equal. Its decoded shape:

```json
{"schema":"photo-frozen-scope-inventory/v1","complete":true,"input_binding":{"request_sha256":"<SHA>","request_envelope_sha256":"<SHA>","input_inventory_sha256":"<SHA>"},"reviewed_input_ids":["request"],"state":"known_present","items":[{"assertion_id":"declared_color","dimension":"appearance","target":"actual_garment_owner","property":"wardrobe.color","value":{"type":"wardrobe.color/v1","value":"white"}}]}
```

This snippet shows shape only; placeholders are invalid proof. `known_present` lists a nonempty complete set of explicitly scoped frozen facts. `known_absent` lists no items and may not contradict any explicitly scoped fact. `unknown`/incomplete inventory is retained as such and cannot satisfy a conditional preserve guard. Missing input/scope inventory also requires review; ordinary text-only cores remain valid when they do not seek that guard evidence.

Each protected native fact explicitly carries **both** `scope_kinds:[...]` and `source_input_ids:[...]` in its otherwise existing exact axes. These are manual provenance/coverage declarations, not candidate-driven classifications. Items repeat its exact assertion ID/dimension/actual owner/property/typed value and must account for every scoped fact for that owner or an explicitly grounded owned part. Source IDs exactly reference caller inventory entries. Same-owner/equivalence/part relationships come only from the frozen explicit graph. Required facts may use the existing partial property-anchor exception: an exact/safely narrower same-dimension and same-owner property must be protected; a narrower anchor cannot freeze a broader fact. Owner/role/relation/scope assertions still need subject lock. No dimension is opened or locked automatically.

For a present scope, the evaluator compares all protected facts with the **whole selected** effect closure, including root/joint effects, effect receivers and explicitly adopted dependencies. Equal proposed values do not bypass mutation locks. A missing mandatory child RID can remain explicitly search-only while awaiting choice, never completed final admission. Optional unselected children add no effect/guard/duty. Final interpretation supplies exactly:

```json
{"scope_preservation_evidence":{"scope_assertion_id":{"fact_assertion_id":{"owner":"actual_garment_owner","value":{"type":"wardrobe.color/v1","value":"white"},"prompt_evidence":"The same white garment color remains visible."}}}}
```

Every required scope/item is covered with exact owner/value and a nonblank literal phrase in the final prompt; foreign or missing items reject. This proves supplied intent/evidence binding, not semantic entailment or rendered pixels.

## Exact selected profile and final render duties

A conditional visual profile's `realization_content[RID]` contains exactly `en,ko,embedding_text,concept_units,relations,authored_components,semantics`; semantics exactly `definition,paraphrase_examples`. Grouped v2 component definitions/discovery and common obligations must be identical. Selected additional obligations must be explicitly authored. A branch may repeat matching selected concept units but cannot override them or inject component units. Known unprojected positive fields reject. Shared canonical member declarations remain subject to exact selected CID/RID/requirement bindings; content projection cannot override identity/conditions/effects/dependencies.

`profile_contracts[RID]` is null for nonprojected sources. Otherwise it is exactly `schema,candidate_id,realization_id,meaning_sha256,projection_sha256,compiled_sha256`, schema `photo-selected-visual-profile/v1`. Hashes cover full meaning, the selected seven-field body and compiled instruction/required evidence/evidence rules/render gates/component semantics. Hash calculation/metadata extraction may be mechanical **after** a manual source judgement; they cannot author fact modes, guards, units, scopes or a source correction.

A public pack carries `native_profile_choices` (`photo-native-profile-choices/v1`): exact `schema,profiles`; each profile exact `candidate_id,required,source_record_sha256,choices`. Each choice exactly `realization_id,qualification,selected_profile_contract,obligation,en,ko,concept_units,relations,affected_dimensions,affected_properties`. Actual eligible RIDs are shown separately; no first/default branch is selected. Qualified selected duties compile from that RID. Unqualified source remains discoverable but has no completed obligation certificate. Existing exact request activation is recomputed from the frozen request; required profiles cannot be omitted or downgraded. Selection is still explicit. Candidate views retain the same selected payload through compact/lazy/materialized consumers.

Final `candidate_interpretations` or transformed augmentation decision adds exact `realization_id`, `selected_profile_contract` and `selected_profile_evidence:{required_field:literal_phrase}` for a chosen projected profile. Canonical admission and selected compilation are recomputed, and the phrase must satisfy its declared exact field/rule. The effective existing visual-obligation contract promotes **only this actual chosen** compiled obligation into render gates, so existing render-request/review consumers receive the selected gate set. Local selected-profile evidence also feeds the existing visual-obligation audit; if a duplicate global evidence object is supplied it must agree. Unselected optional helpers add no duty. Missing chosen inventory, stale source/RID/meaning/compiled hash, unprojected body or undisclosed obligations fail.

## Research-only root acceptance

`native_reviews.py` accepts root assignment `/root` only with exact reviewer `/root`, method `codex_direct_source_read`, model `session_model_unspecified` and effort `session_effort_unspecified`. The parent session model/effort were not observed by a tool. Any actual child assignment requires its exact task path, method `codex_subagent_direct_source_read` and the explicitly assigned `gpt-6.1-sol/high` pair. Root/child or mixed model/effort pairs cannot impersonate each other. `prepare_native_inputs.py` uses this same bounded identity check before emitting immutable inputs; `tests/test_photo_prepare_native_inputs.py` covers both accepted and rejected pairs. Existing historical root2 drafts are not rewritten or approved. Original review provenance and explicit new read attestations remain mandatory.

`native_adoption.py build_preview_v2` now requires explicit `catalog_approval` exactly `schema,actor,artifact,catalog_sha256,slot_count,slot_ids,reason`, schema `photo-native-catalog-approval/v1`, actor `/root`. Artifact is the existing exact `file,file_sha256,sha256` reference to the full approved current catalog. Both bytes/canonical SHA, complete catalog equality, sorted exact roster and integer count are verified. There is no 141/142 hardcoded count. Root approval of a catalog is separate from proof quality and from runtime publication.

## Deliberately unresolved authoring/application boundaries

Current owner maps still use the fixed 20 neutral canonical role addresses. No generic texture is automatically constrained to primary/main/foreground, and no source owner wording automatically becomes one of those roles. A future contract can let a caller explicitly bind a source target to an already frozen actual owner ID, or let manually authored applicability RIDs express legitimate alternate applications. Both require explicit bounded source/core ownership and lock checks; never first-match arbitrary owners. Neither is implemented here. A generic source that cannot be expressed faithfully remains native pending rather than being narrowed/approved as arbitrary foreground-only.

Current `introduced` owner mapping is **not** a preoccupied core role. Its role must be absent from the frozen graph, it must point to the same-RID actual `add_entity` effect, and it receives a source-meaning/RID/local-target synthetic address. An independently declared planned-placeholder owner occupying that role is rejected even without a presence fact. Introduced addresses cannot self-witness prerequisites or inherit guessed disjointness. Whole permission scope forwards those effects/receivers/dependencies into current property/dimension checks. Count/subject changes are **not inferred** from add_entity; if the noun's actual meaning changes count/subject, the manually reviewed full source effects/facts must say so and existing locks apply. A literal noun is not automatically existing-only or creation: any later two-application source pilot needs explicit manual source correction/review and positive/negative tests. No automatic corpus splitting was added.

The old explicit-binding condition path remains only the recorded migration boundary; final source condition separation and CID-only canonical member migration are root's later phase. This work does not qualify the corpus, tag-training data, source semantic truth, input-inventory observational completeness, provider execution, native pixels, or user acceptance. Root independently reviews sources/proofs and rebuilds/publishes/acquires runtime after this code handoff.


### Future explicit generic owner selection: minimal follow-up design, not implemented

An explicit caller choice of an already frozen actual owner is a sound way to preserve a generic source-local target without pretending the source said primary/main/foreground. It must be **selection**, not inference or a looser fallback. A future owner-map schema can add an exact tagged selector alternative to the current fixed-role binding; the proof manually declares its source target, existing/introduced origin and explicit owner/carrier applicability constraints. An arbitrary `owner_kind` string or generic carrier label alone cannot discharge semantic prerequisites: exact source-grounded fact/typed carrier witnesses, source guards and whole effects still apply. Existing fixed-role maps need no automatic conversion.

Minimum consumers to change together: `c.entry`/request role proposal/native bundle and profile choice envelopes carry explicit per-CID/per-actual-RID source-target→actual-core-owner selections; one `resolve_owner_bindings` validates exact allowed targets, actual frozen owner membership, explicit applicability/witnesses and alias/part-of/disjoint graph; admission receipts pin source/proof/meaning/RID/dependency hashes, frozen core/input/graph hashes and exact mapping. Both whole `permission_scope` and `property_scope_allowed` must use that same resolver, including receivers and child selections. Compact/full/lazy/materialized/final paths reproduce the same binding. Final interpretation repeats the selected mapping and cannot change it after lock checks. Missing/extra/stale mapping is review-required/denied; no dictionary-first or role-word match. An unchosen generic source remains discoverable without completed admission.

The separate applicability-RID alternative can be appropriate when the source really distinguishes existing-carrier application from entity introduction. It costs complete manually authored source projections, branch fact/effect/condition coverage and review for each actual RID; it is not automatic noun splitting and does not solve every generic existing-owner selection. The current introduced synthetic-address contract cannot be relabeled as a planned-placeholder owner. A single noun pilot should compare both exact applications, explicitly review count/subject/property permissions and evidence, and test owner absence/presence, occupied roles, aliases/parts, unknown overlap, secondary/background use and final receipt tampering before choosing a follow-up schema. Current canonical native-pending records are not approved by this proposal.
