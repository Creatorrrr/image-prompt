# Hybrid Augmentation Contract

Use this contract when the candidate pack contains `hybrid_augmentation.enabled: true`. Treat the pack as a bounded idea amplifier: keep the agent-authored concept core, inspect all three candidate-sourced routes, and selectively accept, modify, or reject their details. Validation and provenance protect this creative step; they do not replace it.

## Activation

The contract is present when `--hybrid-augmentation` is explicit, when high creative direction requires it, or when an eligible adult-appeal axis is active. The default skill workflow passes `--hybrid-augmentation`. Eligible human candidate packs also activate the configured `1/1` adult-fashion default; no-people, non-human, and youth-coded packs do not activate it.

## Candidate Routes

The pack exposes three routes assembled from actual eligible candidate IDs:

- `material_world`: material, garment, texture, color, prop, and world specificity;
- `action_camera`: action, pose, gaze, framing, camera, and composition consequences;
- `light_second_reading`: light, focus, mood, traces, particles, and reinspection evidence.

Each route contains two to four details. A detail declares its candidate ID, slot, intended function, label, and source. Candidate labels are ideas, not mandatory text. Do not merge routes. Consider every route, then select exactly one or reject all three with a concrete reason.

When a route is selected, decide every detail as `accepted`, `modified`, or `rejected`. Accept or modify two to five details. Include accepted and modified IDs in `chosen_candidate_ids`, bind one literal visible phrase for each, and record the marginal contribution. Keep rejected IDs out of `chosen_candidate_ids`. A modified detail retains its source candidate ID and records what changed.

Use this composed shape beside the ordinary fields:

```json
{
  "augmentation_brief": {
    "concept_core": "The agent-authored governing idea.",
    "routes_considered": [
      {"route_id": "material_world", "decision": "selected", "reason": "Why it fits."},
      {"route_id": "action_camera", "decision": "rejected", "reason": "Why it does not."},
      {"route_id": "light_second_reading", "decision": "rejected", "reason": "Why it does not."}
    ],
    "selected_route_id": "material_world",
    "decisions": [
      {
        "candidate_id": "slot:texture:example",
        "decision": "modified",
        "function": "material_detail",
        "rationale": "Why it supports the core.",
        "marginal_contribution": "What becomes less distinctive if removed.",
        "modification": "How it was adapted.",
        "prompt_evidence": "literal visible prompt phrase"
      }
    ]
  }
}
```

To reject all routes, set `selected_route_id` to `none`, mark every route rejected, provide `all_rejected_reason`, and leave `decisions` empty. This is valid when every candidate would weaken the core concept.

## Adult Appeal Axes

The axes are independent and may run together. For eligible human candidate packs, both default to intensity `1` with balanced emphasis:

- `sensual_editorial` controls gaze, pose, lighting, framing, and silhouette;
- `fetish_fashion` controls material, garment layering, accessories, and footwear.

Use `--sensual-editorial-intensity 0..3` and `--fetish-fashion-intensity 0..3`. Omitted controls resolve to `1` and `1`; equal intensities resolve to `balanced`. When both are active, `--adult-appeal-emphasis sensual_led|balanced|fetish_led` can override the emphasis. The global off state is both intensities at zero; there is no mutually exclusive mode enum.

These defaults operate in candidate-pack composition. A direct final-prompt CLI call records the configuration but does not claim that the adult-appeal candidates were applied.

The configured default activates only when the resolved subject category is human. Explicit no-people, non-human, or youth-coded requests suppress it. This default is policy configuration, never a demographic or popularity inference from the reference image. Explicit controls may increase, reduce, rebalance, or disable the axes; no-people and youth-coded requests remain ineligible.

Candidate entries may declare a minimum intensity. At intensity `1`, the fetish-fashion default keeps only its lower tier; intensities `2` and `3` widen the eligible material and garment inventory. Never reconstruct an entry hidden by the intensity threshold.

Every active axis contributes at least one accepted or modified candidate. Add this block inside `augmentation_brief`:

```json
{
  "adult_appeal": {
    "adult_subject_phrase": "literal phrase explicitly identifying an adult original subject",
    "agency_phrase": "literal phrase showing self-directed agency",
    "axes": {
      "sensual_editorial": {"intensity": 2},
      "fetish_fashion": {"intensity": 2}
    },
    "blend": {"emphasis": "balanced"}
  }
}
```

Keep the subject unambiguously adult and original. Do not infer adulthood from face, body, clothing, ethnicity, or market origin. Keep adult styling intentional and subordinate to the concept core; do not activate it automatically from a presumed popularity benefit.

## Combination Audit and Review Boundary

Audit styling, pose, framing, and camera together. The current hard rule rejects sheer or lingerie-coded styling combined with an extreme ground-level angle. Stacked body emphasis plus a lower angle is a quality warning requiring intentional review. These project checks do not override platform policy or image-tool enforcement.

Audit PASS proves candidate provenance, selective decisions, budgets, and literal prompt binding. It does not prove rendered detail, tasteful balance, safety-tool acceptance, popularity, or audience response. Review generated pixels without prompt metadata; validate audience appeal through separate human or engagement evaluation.
