# Native v3 final contract supplement — 2026-10-14

This supplements the frozen `native-v3-authoring-guide-20261014_v2.md` and its `_v2.json` primitive fixture. Preserve both earlier guide versions and examples. The primitive fact/proof shape and owner-bindings/v2 shape remain unchanged. This note corrects the guide's blanket whole-dimension-lock statement and defines the implemented compound contract. It does not qualify any canonical source.

## Frozen facts under partial requester locks

A required native `kind: fact` can be frozen when its affected dimensions are already wholly locked. It can also use a one-item `affected_dimensions: [dimension]` when an existing requester property anchor protects that same dimension, exact actual owner and property or an ancestor property. For example, an open appearance dimension with `primary_garment/wardrobe.color` protected can retain an exact white color fact while allowing a separately reviewed neckline change. An anchor for wardrobe.color cannot freeze a broader wardrobe fact.

Owner identity resolves only through explicitly declared neutral roles and equivalence. Owned-part containment does not make two endpoints identical for this exception. Unknown identity, missing anchor, wrong owner, advisory witness and a broader fact fail. Owner, role and relationship declarations still require the whole subject dimension locked. The validator never adds or opens a dimension or manufactures an anchor. Wire normalization, the independent core auditor and runtime admission call the same candidate-free lock-support validator. Source prerequisites must still match the exact typed frozen value at the exact same entity; a non-effect fact grants no permission to change that value.

Root owns the product instructions in `SKILL.md`, `precore/photo_semantic_witnesses.md` and `references/photo-workflow.md`. Their final guidance was checked against this implementation. Candidate source guides and examples remain unavailable before core freeze.

## Explicit dependency selection

For every potential member actually available under a parent actual RID, `dependencies[rid]` contains exactly:

```json
{
  "candidate_id":"cand_...",
  "realization_ids":["actual_child_rid"],
  "meaning_sha256":"<child complete meaning hash>",
  "qualification_sha256":"<child complete native proof digest>",
  "selection":"required"
}
```

`selection` is `required` or `explicit_optional`. Required is permitted only when the canonical member explicitly says adoption required/mandatory. Explicit optional requires canonical adoption optional. There is no default-all conversion or invented mandatory adoption. Every potential dependency is qualified and source-bound; only adopted dependencies contribute runtime obligations. A required single actual child choice is unambiguous; multiple admissible actual child choices require a composed `dependency_selections` mapping from CID to actual child RID. An optional child is omitted unless its CID and actual RID are explicitly selected, even when it has just one RID. Empty selections do not adopt optional members.

The full local `effect_sets[rid]` always retains the parent's own source effects, selected branch and explicitly consumed profile projection. Selected child effects are additional source/RID-addressed closure rows. Never erase a parent effect because a child was omitted, or hide a parent joint effect behind complete child proofs. A declared/prerequisite/preservation/context label cannot waive an actual source effect. The public `photo-native-selected-members/v1` bundle view exposes parent components, actual selected members, bounded potential choice inventory and selected effect closure separately. Missing required actual choices remain review_required; it never publishes a union of mutually exclusive child effects as eligible. Entity/composite bundles use the canonical record kinds already supported by the corpus, including visual_bundle; no new record_kind or source mutation was introduced.

Explicit optional selection is not itself independent requester evidence. Source-specific independently requested component/profile conditions still require their real grounded witnesses and full source review. Associated profiles are never promoted through membership. If existing source declarations or root effects cannot represent the intended selected scope, retain it as unqualified/pending and explicitly correct/review the source before native qualification.

Source 15166 (`cand_10e70faca7705a7aa70b4dc580194f29`) was reread directly from frozen SOURCE: five optional member refs, profile_activation independent_request_evidence_only, fifteen positive parent component units and eight root appearance effects. It cannot be made base-only by simply omitting five optional children: the parent positive units and root effects remain independently binding. Its correction/selection design and semantic rereview belong to root's source phase; this worker did not change or qualify it.

## Positive member requirements

Frozen SOURCE was mechanically inspected without changing it: member requirements use only concept_units and relations (1067 member dictionaries contain relations; 572 contain concept_units). Source 12751 has a positive waistband/visible-navel unit and an explicit relations: [] member requirement; 15166's five requirement dictionaries are {}. These fields are semantic/render obligations, not applicability conditions. Their wording/relations remain separate as member_requirements and never overwrite the child's original body or erase its original relations. No automatic prerequisite/context/effect classification is performed.

A dependency with a nonempty canonical requirements dictionary additionally requires manually authored requirement_bindings with exact source_sha256 and realizations keyed by its explicitly admissible actual child RIDs. Each binding contains child_fact_id, a positive parent requirements pointer/quote, and the explicitly reviewed dimension/target/property/mode/value/requires plus effect operation/receivers when applicable. Those semantic fields must equal the referenced fact in that actual child's complete qualified proof. Every positive requirement path needs an explicit binding; no reference may borrow another CID/RID, invent a new mutation footprint, or change an actual effect to context. Empty positive paths, such as relations: [], still require explicit reviewed empty bindings for that nonempty requirements dictionary. Plain {} has no invented requirement_bindings field.

This is a deliberate conservative representability boundary: new requirement meanings/effects/values/prerequisites not already represented in the actual child's qualified fact inventory cannot qualify through an overlay or silent override. Explicit source correction, complete reread and an appropriate actual source/RID/effect scope are required first. Parent joint effects retain their independent full coverage. This does not reject all compounds or infer meaning from tags. A child RID subset may be explicitly admitted for a nonempty source requirement; without requirements the dependency must retain all actual child choices. The full child proof remains bound in either case.

Example shape (all semantic fields are human-authored; ellipses are explanatory):

```json
{
  "candidate_id":"cand_...",
  "realization_ids":["base"],
  "meaning_sha256":"...",
  "qualification_sha256":"...",
  "selection":"explicit_optional",
  "requirement_bindings":{
    "source_sha256":"<digest of exact original requirements object>",
    "realizations":{"base":[{
      "child_fact_id":"underlight",
      "pointer":"/content/member_candidates/0/requirements/concept_units/0",
      "quote":"from below",
      "dimension":"lighting","target":"face_surface","property":"lighting.direction",
      "mode":"effect","value":{"type":"lighting.direction/v1","value":"below"},
      "requires":["face"],"operation":"set_value","receivers":[]
    }]}
  }
}
```

The selected composition must additionally provide literal render evidence on the actual selected parent-CID/child-CID edge. Put member_requirement_evidence in that chosen candidate interpretation or transformed decision:

```json
{"member_requirement_evidence":{"parent_cid":{"child_cid":{
  "concept_units":{"0":"<literal final prompt phrase>"},
  "relations":{"relation_id":"<literal final prompt phrase>"}
}}}}
```

Keys cover exactly the selected edges with positive requirements. Unit keys are their original zero-based string indices; relation keys are their source IDs. Empty kinds use {}. Unselected optional edges add neither carrier/effect nor render obligations. Literal coverage is a necessary authored receipt, not proof of semantic entailment or image pixels.

## CID identity and temporary presentation guards

A native member must have explicit candidate_id. A separately authored presentation_role may name an existing catalog role; absent presentation role stays absent rather than selecting the first old binding or guessing a role from words. A binding-only member cannot qualify through automatic CID resolution.

During the current pre-migration boundary, an explicitly present old binding_id is consumed only as an additional presentation-condition guard. Its candidate_id and any explicit presentation_role must agree exactly with the member's explicit CID/role. Native checks preserve source intrinsic conditions AND explicit old binding conditions. Member requirements are separate positive semantic/render obligations, not conditions or child-body replacements; the role is not source identity, anatomy or mutation authority.

`reference_sha256` binds every referenced CID's complete meaning and every explicitly referenced bind_* object's entire digest, following its actual CID references as well. A changed binding condition or resolved CID invalidates the native proof even when parent wording is unchanged. Native source validation rejects CID/binding disagreement. These temporary guards and the before/after binding digests must remain review evidence. Do not replace an old binding automatically or silently copy/delete its applicability conditions.

Final phase 6/8 cleanup must first manually transfer essential old-member conditions into explicit source/CID applicability with the original review ledger, then remove binding-ID membership/materialization/admission branches entirely. No compatibility fallback is needed after that transition. Parent publication must not describe this intermediate boundary as all-stage completion.

## Positive source boundaries and sealed compact guards

Native positive pointers exclude negative/confusion/claim-limit/review/routing metadata, the entire activation subtree, discovery/alias/validation fields, family/topic IDs and priority dimensions. Keys ending `_id`/`_ids` are identifiers, not positive clauses. Actual RID path components are explicitly exempt from this label rule and must still equal the selected RID; an actual branch named topic_ids is not routing metadata. Primary-path semantic body coverage excludes the same label fields. Rendered instructions, definitions, actual positive concept_units and relation prose remain reviewable.

Historical routing-pointer counts are evidence-strengthening targets, not counts of proven semantic mistakes. Root's expanded audit reports 625 facts in its 16,650-judgement snapshot, superseding its earlier narrower 339 count. Native rereview must manually reanchor to actual positive body text or explicitly correct and reread source/spec/conditions/dependencies. No metadata-to-fact converter is authorized.

Native compact sealing now requires the full current corpus/catalog and validates the full source first. Full source validation rejects a compact guard as a substitute for positive source. Search-layout build validates the source before emitting guards. Compact runtime admission retains complete fact modes/typed values/requires/receivers, owner bindings, actual effect sets, dependencies and reference bindings, and evaluates only actual chosen RIDs/children. It does not reclassify meanings or rely on discarded quotes. Final composed audit uses the pinned full source, revalidates the whole selected source/dependency closure, and enforces intrinsic/actual branch/presentation conditions plus full permission scope.

## Remaining completion gates

Canonical native-qualified count remains zero in root's unchanged source stage. Missing proof remains explicitly unqualified in discovery; present v2/null/empty/false proofs are invalid. Final native adoption rejects absent/v2/invalid proof, including cues presented as a visual concept or transformed augmentation. The temporary absent-proof allowance exists only to preserve the shared discovery pool during manual qualification.

Remove that search-only allowance only after every final positive source has full manual v3 qualification, all approved source/catalog corrections and dependency/condition migrations are applied and reviewed, old binding-ID paths are removed, full index/guard/source closure and runtime publication/acquire are checked, and the whole semantic review ledger is complete. Root owns these corpus/publication/commit gates. This worker used only authored fixtures and offline pure tests, with no canonical changes, model inference, network, publication or Git mutation. Fixture integrity and literal metadata bindings do not prove corpus semantic truth or image pixels.
