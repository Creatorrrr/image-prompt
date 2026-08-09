# Candidate-Pack and Composition Contract

## Candidate Pack

The generator emits one `subculture-illustration-candidate-pack/v2` object containing:

- `pack_id` and exact `negative_en`;
- `request_contract` with original text, route, and mandatory visible intents;
- one resolved `format_profile`;
- `visual_grammar` with exactly one primary visual atom and zero to two compatible supports;
- `authorial_contract`, `viewer_contract`, and `guard_contract`;
- `composition_contract.composed_schema = subculture-illustration-composed-prompt/v2`;
- a closed `viewer_contract.second_look_plan_contract` with carrier kinds, risk flags, and format-derived inspection-scale IDs;
- automatic-pass safety metadata unless explicit evaluation was requested;
- asset hashes and deterministic provenance.

Only `visual_atom` nodes may be selected as prompt candidates. Router and guard nodes remain metadata.

The explicit legacy runtime can reproduce `subculture-illustration-candidate-pack/v1` for immutable historical qualification. New composition always uses v2. Never rewrite a v1 pack, audit, result, or image as v2 evidence.

## Composed Object

Write one JSON object:

```json
{
  "schema": "subculture-illustration-composed-prompt/v2",
  "pack_id": "exact pack id",
  "prompt_en": "one standalone English image prompt",
  "negative_en": "byte-identical pack negative",
  "chosen_candidate_ids": ["route:...", "format:...", "visual:..."],
  "composer": "agent",
  "visual_evidence": {
    "evidence_type": "literal prompt phrase"
  },
  "authorial_grammar": {},
  "viewer_evidence": {},
  "second_look_plan": {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "exact selected proposal id, or null when creative development is not required",
    "reveal_phrase": "exact viewer and selected-proposal reveal",
    "review_scale_ids": ["pack-declared inspection scale"],
    "primary_carrier": {
      "carrier_kind": "material_boundary",
      "carrier_phrase": "literal prompt phrase",
      "protected_locus_phrase": "literal prompt phrase",
      "consequence_phrase": "literal selected-proposal consequence",
      "risk_flags": []
    },
    "fallback_carrier": {
      "carrier_kind": "environmental_trace",
      "carrier_phrase": "different literal prompt phrase",
      "protected_locus_phrase": "different literal prompt phrase",
      "consequence_phrase": "different literal selected-proposal consequence",
      "risk_flags": []
    }
  },
  "format_evidence": {},
  "reference_boundary": {
    "original_design": true,
    "named_style_references": [],
    "protected_ip_references": []
  }
}
```

Every evidence value that claims a visible result must be a nonempty scalar substring of `prompt_en`. Do not hide evidence in metadata.

`carrier_kind` is one of `surface_state`, `material_boundary`, `isolated_contour`, `object_relation`, `environmental_trace`, `projected_form`, or `dedicated_panel`. Closed risk flags are `compound_anatomy`, `subscale_symbol_decode`, and `overlapping_multi_limb_projection`. Primary and fallback carrier, locus, and consequence phrases must differ after normalization. The fallback has no risk flags; a risky primary also requires a different fallback kind. Every declared scale becomes a later pixel-review obligation.

## Selection Rules

- Choose the pack's route and format IDs.
- Choose exactly the selected primary runtime ID and the selected support IDs; do not add unexposed siblings.
- Keep the primary meaning visually dominant. Supports may clarify action, relation, state, or format, but cannot introduce another premise.
- Preserve user-visible mandatory intents. A synopsis, lore label, market term, or emotion outcome does not cover a visual intent.

## Prompt Priorities

Write in this order unless the format contract requires a sequence:

1. original subject and decisive event;
2. actor, directed action, target, and consequence;
3. first-glance hierarchy and second-look reveal;
4. primary second-look carrier, its distinct safe fallback, and the selected visible consequences they realize;
5. primary visual atom and sparse supports;
6. authorial omission, edge/mark, and repeated motif/material rule;
7. format-specific crop, panel, safe-area, or scale behavior;
8. text/logo/IP and other visible exclusions.

Avoid camera-brand, lens, and photoreal capture formulas unless the user explicitly requests a hybrid medium. Illustration rendering language must remain dominant.

## Audit Boundary

The audit verifies integrity, candidate eligibility, sparse compatibility, literal evidence, format behavior, reference boundaries, and second-look plan binding. It cannot prove that either carrier rendered legibly or that viewers will respond as intended.
