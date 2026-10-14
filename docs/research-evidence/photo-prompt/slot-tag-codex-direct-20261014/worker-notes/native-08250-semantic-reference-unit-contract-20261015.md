# Single-hop manual semantic references

This is an authoring contract, not an automated natural-language entailment
test. The reviewer must directly read the whole source, exact local clause,
canonical fact anchor, selected realization, owners, guards and effects.
No existing source or proof is approved or automatically converted by this
implementation. In particular, review08250-17437-03 remains frozen and no
formal04 batch is created here.

The existing normal `semantic` and `nonsemantic` source-unit shapes and their
direct-fact requirements remain unchanged. The new exact unit shape is:

```json
{
  "realization_id": "the_actual_selected_rid",
  "pointer": "/content/render_gates/0",
  "quote": "The complete exact primary field string.",
  "fact_refs": ["an_already_directly_supported_canonical_fact_id"],
  "disposition": "semantic_reference",
  "reference_relation": "selected_output_constraint",
  "retained_constraint_rationale": "Manual explanation of the local condition, its exact referent and the constraints retained."
}
```

`reference_relation` is exactly one of `partial_restatement`,
`selected_output_constraint`, or `same_selected_owner`. The nonblank rationale
records the reviewer's interpretation. Neither this enum nor the rationale is
a new executable predicate, fact, role, effect or permission. Existing source
conditions, render/profile obligations, owner rules, effects and locks remain
independently represented and consumed. A new substantive local fact or guard
cannot be hidden in a rationale or treated as already covered by a reference.

Both the reference pointer and every canonical anchor pointer must be in the
current actual RID's positive `primary_paths`. The quote is the entire exact
field, not merely a matching substring. Metadata, unknown extra content
surfaces, another CID, another RID and an unselected sibling are not anchors.
Common source fields still need separate same-RID fact and unit bindings.

Every referenced fact must already be directly covered by a normal `semantic`
unit in this same candidate proof and RID, at the fact's own exact pointer,
with its fact quote inside that unit's exact full field. The reference pointer
must differ from each canonical anchor pointer. Only direct normal units
count toward complete fact coverage. Reference-to-reference chains, cycles,
self references, unknown IDs and reference-only orphan facts therefore fail.
There is no cross-record lookup, relation inference or sibling fallback.

There may be one normal unit and one reference unit for a given `(RID,pointer)`
when the normal semantic unit directly supports other local clauses. Duplicate
normal units and duplicate reference units each fail. A `nonsemantic` normal
unit cannot coexist with a reference at the same pointer. A reference-only
field can contribute to whole positive-path coverage, but never to the set of
facts that has been directly grounded. Both kinds count toward the existing
MAX_UNITS=2048 budget; MAX_FACTS=4096 and MAX_REALIZATIONS=32 do not change.

The source validator checks these constraints before any compact seal is
created. `c.entry` and `photo_search_layout.guard_record` both call `compact`,
which validates the full source. Compact guards continue to omit all source
units and quotes; their exact `qualification_sha256` binds the complete proof,
including the reference text/relation/rationale, and `compact_sha256` seals
that projected guard. `native_contract_sha256` already hashes all non-review
proof fields, so reference changes invalidate the full authoring signature.
Role qualification still uses directly grounded canonical fact IDs and the
same spec/mode/RID rules. Admission, effect scope, property and whole-dimension
permission checks receive the unchanged canonical facts/guards/effects.

Offline synthetic tests cover all three generic relations, order independence,
normal/reference coexistence, complete quote/shape boundaries, metadata,
duplicate/self/chain/cycle/orphan/foreign cases, independent source guards,
same-RID common fields, full/compact qualification and admission, permissions,
fingerprint changes and the shared unit budget. Passing these structural
tests does not establish that a human-authored local phrase actually refers
to the intended canonical fact. That judgement remains a direct review duty.
