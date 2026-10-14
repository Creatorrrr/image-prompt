# Native v3 authoring guide v2 — canonical role binding, 2026-10-14

**Supersedes** `native-v3-authoring-guide-20261014.md` and its original fixture. Preserve those historical files; use this guide and `native-v3-primitive-fixture-20261014_v2.json` for new authoring. The previous `core_owner` shape is rejected. No canonical source is qualified by either guide.

This guide describes the implemented primitive contract in `photo_semantic_evidence.py`, schema `photo-candidate-role-evidence/v3`. It is a manual authoring handoff, not corpus qualification. The example JSON beside this note is an unregistered synthetic fixture, not an approved canonical candidate. Canonical native-qualified count remains 0. Primitive, visual_profile, relationship_concept/mechanism, entity_bundle and visual_bundle use the same modes plus explicit selected source dependencies. Compound closure is implemented; final integration verification is in progress.

## Review each complete source again

For each CID, reopen the original complete source, the registered original judgement and its provenance, every proposed correction, the exact current catalog/specs, actual RIDs/render projections, all positive body fields, intrinsic conditions, profile/concept effects, members and semantic references. Apply an already approved correction only in a review-side copy and reread that complete resulting record. Preserve original record/decision/catalog hashes and original artifact location. Do not copy original source judgements through a standard converter into effect mode, `requires: []`, owner bindings, or source-unit dispositions. Those are new semantic decisions. A role word/property or human/adult/animal/robot category is not anatomy or prerequisite evidence.

For every complete positive source string, identify the actual semantic clauses and explicitly classify them. Strings are accounted for by `source_units` with full exact quote and fact refs; glue/format-only strings can have an explicitly reviewed `nonsemantic` disposition. A path-coverage checker cannot prove that you extracted every clause: read every clause, condition and preservation/negative obligation. Claim limits, negative/confusion/routing/review metadata cannot supply a positive role fact. In native v3 the entire activation subtree and match_terms/any_terms/all_terms/exact_terms/evidence_terms/must_mention_any/context_terms/project_glossary_aliases/aliases/keywords/terms/concept_terms/evidence_fields/required_evidence_fields are excluded even if a label exactly matches a role word. These keys are also excluded from required semantic-body path coverage. Rendered instructions, definitions, actual positive concept_units and relationship prose remain reviewable. Existing historical 5B label pointers are evidence-strengthening targets, not an assertion that all original judgements were wrong; manually reanchor to actual positive body text or explicitly correct the source and reread it. Never automatically convert metadata quotes into facts. They must still be preserved as constraints where applicable, not discarded.

## Exact fact shape

Each fact has exactly these common fields:

`id, realization_id, pointer, quote, dimension, target, property, mode, value, requires`.

- `id` is unique within the candidate's complete inventory. `realization_id` is an actual canonical RID, not a fabricated use mode.
- `pointer` addresses a primary positive source string. `quote` is an exact nonempty substring. A realization_content pointer must name that fact's exact RID.
- `dimension/target/property` preserve the concrete authored spelling; no automatic lowercasing/renaming/owner aliasing. No wildcard or trailing-dot owner/property is permitted.
- `value` has exactly `{type, value}`. Its value is one nonblank string or a distinct list of 1–8 nonblank strings, with an explicitly reviewed namespace such as `age.declared/v1` or `surface.material/v1`. Equality is exact; no synonym, numeric-age, category or carrier entailment is performed.
- `requires` is a unique list of same-RID fact IDs whose modes are prerequisite/preservation. `[]` is an explicitly reviewed absence of extra obligations, not a default. All prerequisite/preservation facts are checked for the whole cue even if not referenced by a displayed role.

`mode` is one of:

1. **effect**: an actual mutation/added constraint. Additional mandatory fields are `operation` and `receivers`. Operation is `set_value`, `add_entity`, `remove_entity`, `relocate` or `select_plane`, explicitly judged from source meaning; never inferred from the property name. `receivers` is a unique list of additionally affected source-owner targets; [] explicitly declares target-only scope. Every effect fact must match an actual source effect; every actual effect and affected dimension must be covered independently of displayed roles. Coarse effects cannot simply be erased/narrowed by the native proof.
2. **prerequisite**: exact already frozen owner/property/value or relation must exist. It adds no mutation permission. Adult declaration, existing face, and existing object identity must use their own exact typed facts; a generic `carrier: face` or `already_exists: true` does not witness age, skin state, prop identity, focus or any other fact.
3. **preservation**: preserve an exact already frozen value/relation. Either use its explicit typed value, or the reserved `{type: frozen_property_reference/v1, value: same}` to bind the frozen property at that exact owner/dimension/property. A missing core fact fails. Source must actually support preservation; plain “precise focus on the eyes” cannot be relabeled preservation to waive camera locks.
4. **context**: source-stated interpretation/context with no automatic visible consequence. It supplies no change permission. A required contextual condition needs an explicit prerequisite as well. Context fact role support is restricted to contextual specs. Office-clothing usage does not add an office; a contextual role is distinct from a mutation mode or optional adoption policy.

For example, the 11128 source's adult declaration is a prerequisite if the complete reviewed use requires an already adult subject; wardrobe/posture are still actual effects. Its existing root age effect proposal must be explicitly corrected and rereviewed before qualification. Native mode labels do not change canonical effects. Existing `adult_allowed` means permitted treatment/domain/intensity, not declared adult-age evidence.

## Exact owner maps and frozen core witnesses

`owner_maps` is keyed by every actual RID. Each value has exactly:

```json
{"schema":"photo-native-owner-bindings/v2","bindings":[
  {"target":"source_owner","core_role":"main_subject","origin":"existing","introduced_by":null}
]}
```

The map covers exactly the active fact targets and additional effect receivers. `core_role` is a stable common protocol address, never a future request UUID or source-specific alias. The candidate-free core independently authors a required grounded role assertion mapping that role to its actual owner ID. Resolution is exactly source target → declared common role → declared actual owner; no first match, automatic primary assignment, noun/classification/tag inference or string aliases. The same source can be reused for different actual UUIDs only when each request explicitly binds the required role. A source with no intrinsic primary designation must have its applicable role chosen explicitly during native whole-source review; an ambiguity about the owner or role is a review blocker. This does not invent an original claim that the source said “primary”. Different source application scopes need separately authored actual source realizations/conditions; do not fabricate RIDs or automatically map every unspecified owner to main_subject.

The bounded protocol vocabulary is exactly `main_subject, secondary_subject, scene, image, recording_camera, primary_face, secondary_face, primary_hair, secondary_hair, primary_hands, secondary_hands, primary_garment, secondary_garment, primary_prop, secondary_prop, foreground_surface, background_surface, light_source, light_receiver, relationship_target`. These names declare addresses only: primary_face still needs its own typed face-presence witness when the source requires a face. A primary object may have a separately declared face-bearing depiction; its explicit primary_face binding can name that declared secondary owner. Role names alone do not prove anatomy, existence of a semantic property, or disjointness. Unknown protocol roles fail rather than creating an ad hoc source-specific role for the core author.

An introduced owner has `origin: introduced` and `introduced_by` names its same-RID effect/add_entity fact. Its declared role must be unoccupied in the frozen core. Its mechanical runtime address is `native-introduced:<meaning_sha256>:<actual RID>:<source target>`; it cannot self-witness a frozen prerequisite, acquire alias equivalence/disjointness, or evade a locked property. A legitimate new prop still requires explicit actual add effects and permission. Do not use fake introduction to avoid an existing owner's locks.

Core witnesses use existing `semantic_assertions` with `axes.native_schema = photo-frozen-semantics/v1`. Each is required, has active exact `source_span_ids`, frozen baseline evidence, and affected dimensions that are locked. Supported exact axis shapes are:

- owner: `{native_schema, kind: owner, owner, owner_kind}`.
- role: `{native_schema, kind: role, role: main_subject, owner: actual_request_owner_id}`; subject/[subject], grounded independently from any source candidate.
- typed fact: `{native_schema, kind: fact, owner, property, value_type, value}`; assertion dimension is the fact dimension.
- explicit relationships: `{native_schema, kind: equivalent|part_of|disjoint, left, right}`; assertion dimension/affected dimensions are subject/[subject].

Owners/roles/relationships require subject grounding. Every role resolves to a declared actual owner; duplicate/unknown roles or a conflicting role/node spelling are rejected. Same owner equivalence and owned-part hierarchy are distinct. An explicitly separate secondary actor/face remains distinct; unknown overlap with a locked property is denied, not guessed from strings. All referenced owners must be declared. Cycles, dangling relations, contradictory aliased facts and conflicting disjointness fail. Native axes must survive raw-to-normalized wire conversion exactly: object/bool/number coercion or whitespace loss is rejected. No native schema is transported as an unvalidated JSON string.

Limits: at most 64 total core assertion rows (including nonnative rows) and 32 declared frozen owners; typed value lists have at most 8 items. Author only grounded necessary facts/relations; do not collapse multiple owners to fit a limit.

## Roles and complete source coverage

`roles[tag]` has exactly:

`spec_sha256, scope, realization_ids, fact_refs, support_modes`.

`scope` is whole_record or positive_alternative. Every listed RID needs its own referenced fact. Each support fact must fit that actual role's dimension/property contract and its explicitly reviewed support modes. Different RIDs can have different facts. Role facts no longer own duplicate fact bodies. A role's semantic support may be declared/preserved meaning while the complete source still has other actual effects. Choosing an age role never strips wardrobe/posture/member effects from the same cue.

`effect_sets[rid]` is the exact sorted complete local `{dimensions, properties}` footprint (root + selected branch + explicitly consumed concept_candidate projection). A root/joint effect needs its own effect-mode fact even when every child is covered. All selected member proofs and actual child choices are bound separately in `dependencies`. References are CID/RID based; a binding ID is not entity, effect or owner identity.

`source_units` rows have exactly `{realization_id, pointer, quote, fact_refs, disposition}`. Quote is the complete exact addressed string; disposition is semantic (nonempty fact refs) or nonsemantic (empty fact refs). Every fact is referenced by its own string/RID, and all required selected positive source paths have dispositions. Preserve all remaining conditions and full-cue constraints during whole-source review.

## Proof and provenance shape

Top-level proof keys are exactly:

`schema, meaning_sha256, catalog_sha256, complete, facts, roles, owner_maps, source_units, effect_sets, dependencies, reference_sha256, review`.

`meaning_sha256` binds ID/kind/complete content excluding role_evidence and semantic_review, plus intrinsic conditions and canonical effects. `catalog_sha256` binds the entire current catalog; role `spec_sha256` binds its exact spec. `reference_sha256` binds the complete referenced source-meaning closure, not retrieval results or a truncated packet. `dependencies[rid]` is [] only after reviewing that no member is adopted; otherwise each actual selected member has CID, all actual child RID choices, meaning_sha256 and qualification_sha256. Every adopted child must itself have valid complete native proof. Unselected source members are not adopted effects.

`review` has exactly:

```json
{
  "basis":"Complete source/spec/dependency reread and explicit mode/owner/value judgements",
  "whole_source_reviewed":true,
  "source_correction":null,
  "original_review":{
    "candidate_id":"cand_...",
    "source_record_sha256":"<original full source record digest>",
    "catalog_sha256":"<original judgement catalog digest>",
    "decision_sha256":"<original complete registered judgement digest>",
    "artifact":"<original registered judgement file and item locator>"
  },
  "native_review":{
    "reviewer":"<direct reviewer identity>",
    "method":"codex_direct_source_read",
    "native_contract_sha256":"<native_contract_sha256(proof)>"
  }
}
```

Subagents use method `codex_subagent_direct_source_read`. `native_contract_sha256` binds the complete newly authored native inventory, role modes, owner maps, units, effect sets, dependencies, reference hashes, source/catalog bindings, original-review provenance and source-correction binding. It is computed after authoring decisions; computing the digest makes no semantic decisions. Original source/decision/catalog digests are preserved, not overwritten with current values. Pure runtime validation checks shape/bindings; root registration must independently verify that the referenced actual original artifacts/digests/provenance match. An attestation or hash is not proof that a reader interpreted the source correctly.

If source body/kind/effects/conditions change, `source_correction` instead has exactly `{before_sha256, after_sha256, rationale}`. These are distinct complete `meaning_sha256` values; after must equal the resulting record's current meaning hash. Keep the exact original/corrected record snapshots and correction provenance beside the authored review. Reread the whole resulting source, not just the delta; rebind all facts/specs/conditions/dependencies. Never remove a locked mutation merely by changing fact mode. Runtime and compact guards cannot authorize a source correction.

## Delivery and verification boundary

Deliver an authored source-copy/proof and review note under assigned evidence paths. Do not edit canonical candidates, bindings/catalog, index/CURRENT/runtime or register a review yourself unless separately assigned. Root will apply approved source corrections, validate full corpus/dependencies and publish closure/runtime as a separate step.

Validation helpers may calculate exact hashes, canonical actual RID/effect/path sets and detect missing rows. They must not populate modes/values/owners/prerequisites/[]/semantic dispositions automatically from prior judgements, tags, keywords or categories. For a primitive fixture, run native full validation and full/compact parity with exact positive/negative frozen-core examples. Fixtures and mechanically bound metadata do not prove corpus semantic truth or image pixels. Missing/invalid/v2 proof never becomes native success; stage-5C absent proof is explicitly unqualified and kept in the shared discovery pool only. Remove that temporary search-only accommodation at the agreed corpus-completion gate, not by claiming all existing rows are qualified.
