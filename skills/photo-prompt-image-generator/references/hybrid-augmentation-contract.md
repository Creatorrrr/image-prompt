# Hybrid Augmentation Contract

Use this contract when the candidate pack contains `hybrid_augmentation.enabled: true`. In the default `photo-hybrid-augmentation/v2` contract, treat the pack as optional source vocabulary: keep the agent-authored concept core, inspect all three candidate-sourced routes, and artistically transform or reject their details. The pack never supplies final prompt prose. Validation and provenance protect this creative step; they do not replace the agent's authorship.

## Activation

The contract is present when `--hybrid-augmentation` is explicit, when high creative direction requires it, or when an eligible adult-appeal axis is active. The default skill workflow passes `--hybrid-augmentation`. Eligible human candidate packs also activate the configured `sensual_editorial=1`, `fetish_fashion=0` adult-fashion default; no-people and non-human packs do not activate it.

## Candidate Routes

The pack exposes three routes assembled from actual eligible candidate IDs:

- `material_world`: material, garment, texture, color, prop, and world specificity;
- `action_camera`: action, pose, gaze, framing, camera, and composition consequences;
- `light_second_reading`: light, focus, mood, traces, particles, and reinspection evidence.

Each route contains two to four details. A detail declares its candidate ID, slot, intended function, source, and unordered `concept_terms`. These are semantic ingredients, not a phrase template and not a checklist that must all appear. Do not restore their source order, join them into pseudo-prose, or merge routes. Consider every route, then select exactly one or reject all three with a concrete reason.

When a route is selected, decide every detail as `transformed` or `rejected`. Transform one to three details. Include transformed IDs in `chosen_candidate_ids`; for each, state the artistic interpretation, what changed, which context/causality/gesture/material/framing/light/mood/timing dimension changed, and what marginal value it adds. Bind a newly authored literal phrase that gives the cue a concrete relation or consequence beyond its source terms. Keep rejected IDs out of `chosen_candidate_ids`.

These transformed rows already satisfy the v4 authorship requirement, so do not duplicate them in top-level `candidate_interpretations`. That top-level field covers ordinary chosen candidates outside `augmentation_brief`.

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
        "decision": "transformed",
        "function": "material_detail",
        "rationale": "Why it supports the core.",
        "marginal_contribution": "What becomes less distinctive if removed.",
        "artistic_interpretation": "What the ingredient means in this authored scene.",
        "transformation": "How its context or relationship was changed.",
        "transformation_dimensions": ["material", "causality"],
        "prompt_evidence": "newly authored literal visible prompt phrase with a relation or consequence"
      }
    ]
  }
}
```

To reject all routes, set `selected_route_id` to `none`, mark every route rejected, provide `all_rejected_reason`, and leave `decisions` empty. This is valid when every candidate would weaken the core concept.

## Adult Appeal Axes

The axes are independent and may run together. For eligible human candidate packs, `sensual_editorial` defaults to intensity `1`, `fetish_fashion` defaults to `0`, and the default emphasis is `sensual_led`:

- `sensual_editorial` controls gaze, pose, lighting, framing, and silhouette;
- `fetish_fashion` controls material, garment layering, accessories, and footwear.

Use `--sensual-editorial-intensity 0..3` and `--fetish-fashion-intensity 0..3`. Omitted controls resolve to `1` and `0`; fetish fashion therefore requires an explicit positive intensity. Equal positive intensities resolve to `balanced`. When both are active, `--adult-appeal-emphasis sensual_led|balanced|fetish_led` can override the emphasis. The global off state is both intensities at zero; there is no mutually exclusive mode enum.

These defaults operate in candidate-pack composition. A direct final-prompt CLI call records the configuration but does not claim that the adult-appeal candidates were applied.

The configured default activates only when the resolved subject category is human. Explicit no-people and non-human requests suppress it. This default is policy configuration, never a demographic or popularity inference from the reference image. Explicit controls may increase, reduce, rebalance, or disable the axes; no-people requests remain ineligible.

Candidate entries may declare a minimum intensity. When fetish fashion is explicitly enabled at intensity `1`, only its lower tier is eligible; intensities `2` and `3` widen the material and garment inventory. Never reconstruct an entry hidden by the intensity threshold.

Candidate adoption is optional even when an axis is active. The agent must instead author one scene-specific interpretation for every active axis, keeping the abstract intensity and blend while avoiding a fixed inventory phrase. Add this block inside `augmentation_brief`:

```json
{
  "adult_appeal": {
    "adult_subject_phrase": "literal phrase explicitly identifying an adult original subject",
    "agency_phrase": "literal phrase showing self-directed agency",
    "axes": {
      "sensual_editorial": {
        "intensity": 2,
        "artistic_interpretation": "How this axis serves the concept rather than replacing it.",
        "prompt_evidence": "newly authored literal scene phrase"
      },
      "fetish_fashion": {
        "intensity": 2,
        "artistic_interpretation": "A separate material-led interpretation.",
        "prompt_evidence": "newly authored literal material phrase"
      }
    },
    "blend": {"emphasis": "balanced"}
  }
}
```

Keep the subject unambiguously adult and original. Do not infer adulthood from face, body, clothing, ethnicity, or market origin. Keep adult styling intentional and subordinate to the concept core; do not activate it automatically from a presumed popularity benefit.

## Combination Audit and Review Boundary

Audit styling, pose, framing, and camera together. The current hard rule rejects sheer or lingerie-coded styling combined with an extreme ground-level angle. Stacked body emphasis plus a lower angle is a quality warning requiring intentional review. These project checks do not override platform policy or image-tool enforcement.

Audit PASS proves candidate provenance, explicit artistic decisions, transformation budgets, newly authored context, and literal prompt binding. It does not prove rendered detail, tasteful balance, safety-tool acceptance, popularity, or audience response. Review generated pixels without prompt metadata; validate audience appeal through separate human or engagement evaluation.

## Legacy Replay

`photo-hybrid-augmentation/v1` appears only in `--candidate-pack-version v3|v2` replay packs. It retains the older `accepted|modified|rejected` states, two-to-five adoption budget, literal candidate labels, and one adopted inventory candidate per active axis. Do not use that contract for new composition; it exists so historical packs and consumers remain auditable.
