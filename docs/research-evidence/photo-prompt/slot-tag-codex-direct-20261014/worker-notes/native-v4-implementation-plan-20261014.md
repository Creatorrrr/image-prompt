# Native v4 implementation plan — frozen v3 starting point

Root authorized the generic guard/inventory/profile extension, with no candidate-ID or meaning-hash whitelist. This is a contract/fixture implementation plan, not approval of any actual source/proof.

The current v3 recovery snapshot is `native-v3-pre-v4-backup-20261014/MANIFEST.json`, byte SHA256 `5d19dcd9e3c01f906bf02e17da5fb50de4ef4ad784b407fcca50d393800ee0cd`. Its 24 byte-identical files include 14 production files, six related tests and both research consumers/their tests. Before editing the newly authorized CLI/workflow test, add their exact current bytes to a separate supplemental backup; the original snapshot stays immutable.

## Source proof v4

`photo-candidate-role-evidence/v4` keeps the existing exact v3 fact/mode/unit/owner/dependency/review contracts and adds two mandatory exact RID maps:

- `guard_sets[RID] = {source_conditions: [intrinsic_conditions, selected_branch_conditions_or_empty_object], member_conditions: {childCID: [explicit_pointer_conditions_or_empty_object, explicitly_consumed_binding_conditions_or_empty_object]}}`.
- `profile_contracts[RID]` is null for nonprojected sources, or a `photo-selected-visual-profile/v1` binding of CID, actual RID, meaning SHA, selected seven-field projection SHA and compiled obligation SHA.

Both maps exactly match the complete current source. Whole meaning/proof/reference hashes bind all conditions, referenced source records and any consumed temporary binding definitions. Root's explicit v4 review signature is mandatory; v3/invalid present proof never falls back to completion. Existing absent proof remains stage-5C retrieval-only unqualified; final adoption continues rejecting it.

Native source guard blocks use `photo-native-source-guards/v1`, exact `{schema,rules}`. Each rule has a unique ID and one exact shape from the draft: `preserve_established_scope`, `owner_relation` (part_of/disjoint), `frozen_value` or `frozen_entity_relation`. Roles must be explicit neutral canonical role IDs. Guards create neither owners, anatomy, effects nor permissive aliases. Common source, selected actual RID, selected presentation and selected dependency conditions are conjunctive, evaluated by one runtime reader. Optional dependencies contribute only after explicit selection. Presentation conditions never replace intrinsic or branch conditions.

Caps: actual RIDs 32, source-unit rows 2048, facts 4096. No truncation, inferred fact generation, CID exception, or owner/member/depth/core-assertion cap increase. 33/2049/4097 must fail.

## Independent candidate-free input and scope inventories

The request envelope gains an optional explicitly supplied `input_inventory` object, version `photo-request-input-inventory/v1`: exact `{schema,complete,items}`, each item exact `{id,kind,sha256}`. It permits text/request text as well as reference/identity inputs; file absence does not prove identity/reference absence. IDs and byte hashes remain exact. Caller-supplied completeness is an assertion, not independently observed tool truth. Missing inventory stays missing; never synthesize `[]`. Incomplete inventory can remain a valid frozen input but cannot satisfy a preserve guard. Envelope canonical SHA and the exact inventory are carried into `request_binding`.

A new native assertion kind `scope_inventory` uses existing required/subject/span/evidence grounding with axes `{native_schema,kind,owner,scope_kind,inventory}`. `inventory` is an **exact canonical JSON string**, not coerced or whitespace-normalized. Its bounded payload is:

```
{schema: photo-frozen-scope-inventory/v1,
 complete: boolean,
 input_binding: {request_sha256, request_envelope_sha256, input_inventory_sha256},
 reviewed_input_ids: [every input ID in the exact caller inventory],
 state: known_absent | known_present | unknown,
 items: [{assertion_id,dimension,target,property,value}]}
```

`scope_kind` is reference_appearance/requester_identity and owner is the actual explicitly declared core owner. Protected items exactly repeat independently frozen fact IDs, owner, dimension, property and typed value; present inventories must be nonempty and every item must be supported by existing whole locks or exact/narrower requester property anchors. Protected parts require explicit core ownership/part relations. Scope facts can explicitly annotate `scope_kinds` and `source_input_ids` on the existing typed fact axes; when supplied these are exact input-bound provenance, never inferred from category/tag/candidate words. Complete inventories must account for the complete set of those explicitly scoped facts for that owner/owned parts; absent cannot contradict an explicitly scoped fact. Item/source/owner mismatch, unknown/missing/incomplete scope, stale input binding or incomplete present inventory denies the guard.

All existing 64 total assertions / 32 owners and per-axis list bounds remain. The wire preserves serialized JSON exactly and checks raw versus normalized equality. Candidate-free build/audit/replay rechecks envelope, request binding, scoped facts and owner graph; no candidate import is added to neutral code.

## Runtime and final preservation

The common guard evaluator resolves exact frozen roles/facts and explicit part/disjoint evidence. `frozen_entity_relation` compares an existing left-owner fact of the explicit type to the resolved right actual owner ID. `frozen_value` compares exact dimension/property/owner/typed value. Identity/part unknown is denial.

For present conditional scopes, compare every protected item against the **whole selected effect closure**, including effect receivers and selected dependencies, using explicit neutral owner relations and existing property-overlap logic. Equal proposed values do not bypass a lock. Absence yields only a not-applicable guard receipt, never a presence/context fact. Guard receipts preserve the exact scope/items/input binding.

Final composition recomputes admission from canonical source/core and requires exact per-item `scope_preservation_evidence` in the selected interpretation for every present scope: `{scope_assertion_id: {fact_assertion_id: {owner,value,prompt_evidence}}}`. Owner/typed value must equal the frozen receipt; nonblank evidence must occur literally in final prompt. Scope/fact omissions and foreign extras fail. This is explicit intent-preservation evidence, not automatic text entailment or pixel proof. Existing independent baseline/intention/property audits continue to apply.

## Profile projection and compilation

The visual_profile selected source has exactly seven fields: `en,ko,embedding_text,concept_units,relations,authored_components,semantics`; semantics exactly `definition,paraphrase_examples`. Grouped component definitions/discovery and original common obligation/evidence must remain exact; selected additional obligations are explicitly authored, compiled only from the chosen RID and hashed with CID/RID/meaning. Unexpected unprojected positive rendering fields reject. Canonical activation, conditions, effects, identities and dependency selection cannot be overridden by selected content.

Validate every source projection at source load and again on direct entry; compact selections check the pinned per-RID projection/compiled hashes. Candidate-pack profile obligation compilation consumes this selected compiled payload instead of registry common duties, and final audit verifies the same selected contract. Common seven-component membership alone must not force all optional incidents.

## Files and consumers

- Neutral `precore/photo_semantic_witnesses.py`, `photo_authoring_wire.py`: versioned input/scope read, exact JSON transport, input/owner/fact grounding and bounded lock support.
- Newly authorized `precore/prepare_photo_run.py` and related workflow test: explicit `--input-inventory` input path; never defaults from a candidate or missing file.
- `photo_semantic_evidence.py`: v4 exact maps, caps, common evaluator, whole effect/receiver/dependency preservation and final receipt checks.
- `photo_candidate_corpus.py`, `photo_candidate_realizations.py`: typed source conditions, exact profile projection, selected entry metadata and presentation conjunction.
- `photo_search_layout.py`, `photo_search_reader.py`, `photo_shared_views.py`, `photo_slot_semantics.py`, `photo_role_proposals.py`, `photo_candidate_semantics.py`: retain the same v4 guard/profile contract through compact/lazy/materialized/public consumers; no retrieval-pool shrinkage from absent native proof.
- `prompt_generator.py`, `audit_composed_prompt.py`, `photo_contracts.py`: shared admission/condition hooks, selected-profile obligation binding, final scope-preservation evidence and core validation.
- Research **only** `native_reviews.py`, `native_adoption.py` plus their tests: consume v4; replace the preview-v2 `141` count hardgate with exact current approved roster/count/hash checks, without hardcoding `142` or changing actual approval/source files.
- Existing six native tests plus focused new fixtures as needed: full/compact and lazy/materialized/final parity; absence/presence/unknown, wrong/stale input, incomplete inventory, wrong owner/part/alias, receiver/dependency overlap, equal-value mutation, selected-only helpers/relations, projection leakage/hash mismatch, 32/33 RIDs, 2048/2049 units and 4096/4097 facts.

Root owns product documentation, actual source/proof review, catalog approval, runtime rebuild/publication and Git. The plan does not approve the draft's common peer-rival restriction; the evaluator enforces only the actual explicitly authored selected guard. No candidate IDs will appear in production logic.
