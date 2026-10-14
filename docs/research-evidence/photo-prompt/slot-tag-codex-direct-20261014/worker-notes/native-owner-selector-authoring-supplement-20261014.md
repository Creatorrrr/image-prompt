# Explicit existing-owner selection supplement (2026-10-14)

This supplements the frozen native v4 authoring guide and supersedes the transport portion of `native-explicit-existing-owner-selector-design-20261014.md`: **one immutable public pack stays unchanged throughout a run**. Resolution is an audit result associated with composed input, never a regenerated retrieval pack. Existing native v4 proof/schema and valid owner-map/v2 literals remain valid without rewriting. This is an opt-in source owner-map/v3 extension, not a blanket conversion of existing source owners.

## Source authoring

A manually reviewed existing-carrier application may retain a source-local target without inventing foreground/main applicability:

```json
{"schema":"photo-native-owner-bindings/v3","bindings":[
  {"target":"surface","origin":"existing","introduced_by":null,
   "selector":{"kind":"selected_existing_owner"}}
]}
```

Each v3 row has exactly target/origin/introduced_by/selector. `selector` is either exactly `{"kind":"selected_existing_owner"}` or `{"kind":"core_role","role":"<one existing neutral role>"}`. Fixed-role v3 rows retain the v2 origin/creator rules. Selected-existing rows require existing/null, have no role/default/owner-kind guess and cannot own an add_entity fact. Every active fact target and receiver still has exactly one owner-map row (32 bindings per node). Introduced entities, count/subject effects and noun creation are not implemented by this extension.

Source facts remain whole-source, manually authored v4 facts, source units, actual RID/effect/condition/profile/dependency closure and explicit review bindings. A selector never waives mutation coverage, expands a property prefix or permits material/anatomy inference. Source guards using neutral roles retain their existing exact role semantics; a new dynamically selected-target guard protocol is out of scope. Sources needing that protocol stay pending.

Each selected existing owner needs an independently frozen required `subject/entity.presence` fact of exact type `entity.presence/v1`, value `present`, on that exact entity (an explicit equivalent entity can supply the witness). Presence is distinct from owner declaration, role binding, planned placeholder, reference-file existence and noun spelling. Skin/hair/nails/face/material facts require their own exact authored prerequisites where relevant. Current common anatomy presence facts are subject/anatomy.face.presence, subject/anatomy.hair.presence, subject/anatomy.nails.presence, and root guide explicitly declares subject/anatomy.eyes.presence, subject/anatomy.mouth.presence and subject/anatomy.lips.presence, each with property + `/v1` type and `present`; age.declared belongs to age. A separately declared anatomical part owner still requires its own owner/equivalence/part-of facts; generic entity presence does not declare a face or part. No type/property synonym aliases are invented. `body.parts` list values still compare exactly, including order: broader anatomy information does not silently entail a narrower list. Prefer directly authored atomic presence facts where that is the intended condition.

Within one actual RID, repeated **effect-mode** facts with identical dimension/target/property must have identical canonical typed value and operation and the same unique receiver set. Language/source anchors may repeat the same assignment; they cannot encode conflicting values such as `natural_standing` and `standing`. Receiver order remains authored and is not rewritten. Different modes (prerequisite old value versus effect new value) are not compared as duplicate assignments. Partial merges and synonym conversion are unavailable: directly author narrower properties or one explicit aggregate typed value and reread the whole source.

## Independent core and composer input

The candidate-free core is frozen before retrieval. The caller must already have authored actual owners, explicit equivalence/part_of/disjoint relationships and exact frozen facts from request evidence. This extension does not modify precore, its 64 total native assertions, 32 owners or source grounding rules. `owner_kind=surface`, a role such as secondary_face, an item name, or a category does not establish material or anatomy.

The public pack includes only source-addressed `owner_selection_requirements` descriptors: CID/RID, meaning and full qualification hashes, exact local targets, prerequisite/preservation fact descriptors and whether a dependency is root/required/explicit_optional. It contains no request owner IDs. An unresolved candidate remains `review_required` / search-only; role qualification can remain qualified. Source qualification and actual application permission are separate. Search generation and independent rank replay explicitly allow this unresolved state; final eligibility does not.

The composer supplies this optional composed field **before** permission checks:

```json
{"owner_selections":{
  "schema":"photo-request-owner-selections/v1",
  "core_sha256":"<exact frozen canonical core SHA256>",
  "owner_graph_sha256":"<canonical frozen witness graph SHA256>",
  "entries":[{
    "candidate_id":"cand_<32 hex>","realization_id":"base",
    "meaning_sha256":"<current source meaning SHA256>",
    "qualification_sha256":"<canonical full native proof SHA256>",
    "bindings":[{"target":"surface","owner_id":"<explicit existing frozen owner ID>"}]
  }]
}}
```

The graph hash is `photo_candidate_corpus.digest(photo_semantic_evidence.frozen_witnesses(core)['graph'])`. Qualification SHA hashes the full v4 proof, including review provenance. It is not the compact guard hash. The selected CID/RID entry binds exactly the selected-existing targets for that source node. Fixed-role rows cannot be overridden. 1..64 entries are allowed; each has 1..32 unique local target bindings. Duplicate/conflicting CID/RIDs, foreign fields/owners, wrong/stale hashes, missing bindings and extra bindings reject. Global entries must equal the actually selected owner-selector node closure; unused optional child bindings and foreign nodes are rejected. No entries are truncated or silently ignored. Existing dependency caps (32 realizations, source units2048, facts4096, node edge8/depth8) are unchanged.

`candidate_interpretations` or the existing transformed decision row continues to select actual realization/dependency_selections and provide literal final-prompt/property/profile/member evidence. It does not provide trusted source facts. Parent own effects remain distinct from the extra effects of explicitly adopted children. Optional dependencies never default to selected. Full source, sealed compact guards, lazy retrieval, role proposals, member materialization, shared bundle and profile projection use the same resolver and explicit mapping. Search descriptors can advertise optional alternatives; only the actual selected closure creates obligations.

## Permission, receipt and runtime

Resolution checks exact frozen facts and then all whole selected effects/receivers against dimension locks and property locks. Explicit alias equivalence and part_of affect overlap; explicit disjointness permits distinct-owner applications; unknown overlap denies. Existing-carrier presence and even a same-value operation do not grant change permission. Selected profile projection/obligations, intrinsic/selected/presentation/dependency guards and final preservation remain conjunctive. Missing owner choice can be discoverable but cannot pass final adoption.

On a completely passing composed audit, the report contains `native_owner_resolution` with schema `photo-native-owner-resolution/v1`:

- exact public pack/composed/core/graph/owner_selections hashes;
- sorted unique selected node records, exact source qualification/meaning hashes, local-target→actual-owner bindings and presence assertion IDs;
- resolved prerequisite/preservation assertion IDs and typed frozen values;
- sorted root selected closures with actual CID/RID, dependency selections and source-addressed effects/owner maps;
- canonical_sha256 over the receipt excluding that field.

This receipt is auditor output. A composer-supplied `native_owner_resolution` or its hash is rejected. The immutable pack is not patched. Successful compose-audit stores composed input plus its report; thereafter a changed owner mapping requires a new run. Failed audit attempts do not commit composed input, so ordinary correction and identical replay remain possible. Same mapping with a revised prompt must pass a fresh audit and gets a distinct composed-bound receipt.

`prepare_render` copies the stored receipt hash to `native_owner_resolution_sha256` and its exact composed hash to `source_composed_sha256`. Caller transport parameters cannot override these. Runtime worker rereads pinned source and performs a fresh composed audit, compares the entire stored and fresh receipt, and the runtime request auditor checks the same exact public pack and composed mapping/hash. Rebinding or replaying a different composed prompt with an old receipt fails. API preflight/runtime_sources schemas have not changed; these paths consume the common runtime auditor.

## Isolated pilot and remaining approval boundaries

`tests/test_photo_native_owner_selection.py` embeds original CID `cand_4bf6badb8139555bbb907f10bf7f1ea6` (ordinal1272, cracked leather texture), original full-record SHA `ec33f6feefdd422d122c4a7b71972bc5d132b190e6dc8da2d3bf6b59c2989513`, and original meaning SHA `90bb27d0eaca5367b51884cb507744c07acfbc9bf2c0ce49fd03cb28b4883ce8`. Its original dimension-only effects are retained as an explicit rejected fixture. A separate manual **fixture-only source correction** declares existing-carrier application, leather prerequisite, cracked texture assignment and preservation of carrier/material identity, then tests secondary coat and background bench applications using independently authored request/core evidence. This does not approve, correct or narrow the operating source, invent an application RID for every noun, or prove image pixels.

Actual source/proof approval, corpus qualification, metadata/compact-guard rebuild with unchanged-space vectors, runtime publication/acquire and Git remain root work. Existing qualified=0 operating boundaries are unchanged by these fixtures. Whole-source semantic rereview remains required; the engine cannot infer physical completeness or semantic truth from structural validation. Old v4 recovery/handoff artifacts stay immutable.
