# Moe Response Contract

For the normal v6 workflow, use `character_response` when the candidate pack contains `photo-character-response/v1`. Its semantics were authored and frozen in `photo-authorial-core/v3`; do not run the raw moe router or use any named-archetype mechanism/register below to reinterpret them. Only for a compatibility pack with `moe_response.enabled: true`, load [moe-response-legacy.md](moe-response-legacy.md). Its historical scene prescriptions are unavailable to the normal typed v6 workflow.

## Typed V6 Character Response

Copy the contract's nine `frozen_evidence` phrases into the final prompt exactly: actor, baseline, trigger, target, primary action, affect leak, visible response, immediate consequence, and continuity. Keep the declared semantic axes intact, use one primary action and exactly one primary affect-leak channel, and do not invent a relationship, emotion, gaze geometry, face landmark, pose, or story endpoint. `advisory_retrieval.candidates` are optional unordered support; they may all be rejected and can never replace or harden frozen evidence.

When the frozen assertion defines an affection-control relationship, preserve its same-target vector across the affection cue, primary action, and immediate consequence. Its `same_target` relation includes `relationship_target`, the affection surface or care, `primary_action`, and `immediate_consequence`; an affect leak supports the declared consequence rather than replacing it. Other character responses preserve their own frozen relations without acquiring this relationship type. Outward styling and expression can strengthen the reading, but hair, eye color, costume, a fixed stare, a smile, a weapon, or a role prop cannot replace target-directed behavior. When a post-core visual profile distinguishes essential relationship evidence from optional outward signals, keep that distinction intact in composition and pixel review.

For an elliptical retry, inspect only the parent hashes, preserved core fields, effective hard obligations, and relevant defect evidence allowed by the SKILL.md retry whitelist before freezing the new core. Do not read unselected concepts or optional prose from a parent pack. When lineage preserves the governing `concept` or `character_response` and the parent profile was already a hard visual obligation, recreate that profile through a hash-bound `photo-visual-intent/v1` using `agent_postcore_interpretation` and an exact current frozen core field. A BM25F or embedding hit remains optional and cannot stand in for this carry-forward. If the requester changes or excludes the meaning, rebuild the core and do not inherit the profile.

A `concept_profile` candidate comes from contrastive BM25F over one data-authored meaning and its data-authored confounders. Its `semantic_consistency` reports only whether the frozen typed assertion matches the profile's abstract axes and relations. `incomplete` and `conflicting` are diagnostics, not instructions to add missing geometry or rewrite the baseline; `consistent` is not a render gate. `conflicting` and `superseded_by_requester_definition` make the candidate `diagnostic_only`, suppress all linked behavior support, and forbid legacy fallback. Behavior-support candidates may come only from an eligible retained profile's optional runtime-node links, and all retrieval scores, ranks, matched terms, frequencies, and vectors remain private.

The composed object binds this without exposing retrieval scores:

```json
{
  "character_response": {
    "source_contract_sha256": "<character_response.canonical_sha256>",
    "evidence": {
      "actor_phrase": "<exact frozen phrase>",
      "baseline_phrase": "<exact frozen phrase>",
      "trigger_phrase": "<exact frozen phrase>",
      "target_phrase": "<exact frozen phrase>",
      "primary_action_phrase": "<exact frozen phrase>",
      "affective_leak_phrase": "<exact frozen phrase>",
      "visible_response_phrase": "<exact frozen phrase>",
      "immediate_consequence_phrase": "<exact frozen phrase>",
      "continuity_phrase": "<exact frozen phrase>"
    },
    "selected_advisory_candidate_ids": []
  }
}
```

The composed audit requires every evidence value to remain byte-identical to the core and literal in `prompt_en`. A BM25F or embedding hit is never proof that the image expresses the character response. Rendered-pixel review and requester judgment remain separate terminal evidence.


For pixel review, derive every hard gate from the frozen contract and audited composed selection. Do not add historical face, gaze, framing, species-reflex, or affection defaults by label. A source-bound visual-profile obligation may constrain geometry only when it is actually active. See `image-runtime.md` for request serialization, saving, audit records, and the separate requester-judgment boundary.
