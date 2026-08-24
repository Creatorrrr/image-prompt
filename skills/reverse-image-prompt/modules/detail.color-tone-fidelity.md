---
id: detail.color-tone-fidelity
version: 7
priority: 79
type: detail
tier: 3
facet: detail-risk
facet_values:
  - color-tone
  - color-fidelity
  - tone-fidelity
  - surface-color
  - global-cast
  - white-balance
  - exposure-tone
  - palette-relationship
triggers:
  - user explicitly prioritizes faithful color or tonal reproduction
  - value, chroma, hue, cast, exposure, or tone response materially carries the image
  - intrinsic surface color may be confused with illumination, global cast, or processing
avoid_when:
  - color is incidental and ordinary core color handling is sufficient
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
  - core.background-color
conflicts: []
provides_anchors:
  - color_tone_contract
  - color_causal_layers
  - relative_color_calibration
  - neutral_anchor_confidence
  - aggregate_color_effect_budget
  - tone_zone_response
  - color_measurement_limits
  - display_color_scope
  - region_group_color_comparison
  - color_axis_emission_coverage
  - color_actuation_contract
  - color_control_effectiveness
  - render_color_verification
  - displayed_tone_response
  - surface_color_language_translation
  - friendly_label_review
  - friendly_label_external_source
---

# Detail: color and tone fidelity

## When to load

Load only when color/tone is an invariant, the user requests fidelity, or a causal mix-up could materially change the image. Do not load merely because an image contains color.

## Three-stage Color/Tone Contract

Build a source-relative Color/Tone Contract only when color or tonal behavior materially carries fidelity.

Keep three stages separate:

1. **Observation:** what the source visibly supports.
2. **Actuation:** which literal prompt control carries each material source axis to the named generator.
3. **Verification:** what a delivered render actually reproduced. Prompt validation never substitutes for rendered-pixel verification.

Set scope to `source-visible`, `color-managed` only with trustworthy calibration evidence, or `user-specified` for an explicit external target. Treat sampled pixels as source-visible display color, not proof of biological, material, or scene-referred true color. For human surfaces, use observable evidence rather than demographic identity labels.

For each important region:

- separate value/lightness, chroma/saturation, and hue family/undertone;
- record role, relation to another region, confidence, and uncertainty;
- separate intrinsic surface from illumination, global cast/palette, exposure/tone curve, and processing.

For every intrinsic value, chroma, or hue axis, record `role`, `evidence_scope`, and `emission`. Use `required` only when the axis materially needs a final prompt control. Use `diagnostic-only` with a concrete non-emission reason when an axis is low-confidence, incidental, or already unsupported at prompt precision. Link every required intrinsic axis to exactly one same-region, same-axis aggregate effect.

Assign every material color or tone observation to intrinsic surface, illumination, global cast or palette shift, exposure or tone curve, or processing.

Describe important regions through separate value, chroma, and hue observations plus source-visible relations to other regions. Do not let one broad adjective silently determine all three axes.

Decompose an appearance metaphor into value, chroma, hue, surface, and light response. Mark it `explanation-only`, `unverified`, or `model-calibrated`; only the last may appear once as a summary of already-owned controls, with evidence for the exact generator/version. Treat control effectiveness as generator-and-version-specific evidence.

When measured surface color needs natural language, read `references/surface-color-language.md`. Classify value depth, chroma, undertone, and optional separately observed finish independently. Compose stable axes in canonical order, omitting unresolved axes without invention. A boundary-only result stays diagnostic until exact model calibration. The descriptor is not a friendly label and may emit only as one wrapper containing the exact included axis-control excerpts.

Friendly labels remain separate: review only user-supplied or explicitly versioned vocabulary candidates, and emit only a compatible exact-generator/version-calibrated summary. Never map surface axes to demographic identity.

Map highlight, midtone, shadow, or flat-field behavior only at the granularity the source supports. Do not pool tone zones into an intrinsic target: use comparable midtone or flat patches for displayed intrinsic axes and separate groups for highlight and shadow response. Retain uncertainty for clipping, compression, mixed light, and low legibility.

Record displayed key level, shadow floor, highlight rolloff, and microcontrast as separate tone-response axes. Give every Color/Tone region a non-trivial prompt anchor. Each required control declares global, region, or declared region-group scope, affected/protected regions, evidence, and reuses the declared exact anchor in its prompt excerpt. Split mixed bright/dark coarse regions before applying one shadow floor. Light/Form separately owns bright-plane coverage and spatial gradients.

## Calibration evidence

Treat a possible neutral as a calibration anchor only with visible evidence and an explicit confidence level. Nominal white, gray, black, metallic, or low-chroma regions may still be shifted by light, reflection, exposure, clipping, compression, or grading.

Without a reliable neutral, preserve relative relationships and mark global-cast uncertainty. Translate photographic cast into white-balance/capture language and non-photographic cast into palette/rendering language.

When measurement is justified, use multiple representative patches, robust summaries, profile status, and disclosed display-space assumptions.

Classify auxiliary references as `calibrated-color-target`, `color-managed-reference`, `uncalibrated-vocabulary-chart`, or `photographic-example`. Only the first two establish numeric targets; inconsistent labels remain vocabulary.

Compare multiple target patches with contextual or neutral groups before attributing a color difference to an intrinsic surface or a global cause. Use equal-weight summaries. Shared movement supports global cast/exposure/processing; target-only movement supports a local cause; mixed evidence remains uncertain.

The optional probe accepts analyst-selected normalized regions and never chooses semantic targets:

```bash
python tools/color_probe.py SOURCE --compare RENDER --spec SAMPLING.json
python tools/color_fidelity_eval.py COMPARISON.json --policy POLICY.json
python tools/color_language.py OBSERVATION.json --policy references/surface-color-language-policy.json --compose-for "<analyst-supplied-surface>" --candidates LABELS.json
```

Use measurements as diagnostic evidence, never as proof of intrinsic color. The language tool can return reviewable axes, a deterministic descriptor candidate, and label compatibility; the plan still decides emission and supplies semantic region ownership. Keep exact values out unless the generator supports them and evidence justifies the precision.

Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. Without an explicit tolerance policy, report the decomposition as unscored.

## Cross-layer effect budget

Merge color and tone claims by their shared perceptual effect across causal layers, not only by semantic-slot name.

Give each material effect a source-relative identifier covering region, axis, direction, and aggregate strength. Multiple causal layers pushing one region/axis require independent evidence and one aggregate target.

- Merge unsupported repetition into one owned control.
- Preserve multi-layer color only when every layer and the aggregate result are supported.
- Let hierarchy own relative area, value, chroma, or contrast; let it own hue only when hue contrast is invariant.
- Treat free-floating color or mood words as unowned until assigned to one causal layer.

## Final prompt control ledger

Copy every exact prompt excerpt that changes color/tone into `emitted_controls`. Give an `axis-control` one claim, causal layer, region, axis, and complete effect list. A required intrinsic axis needs its own intrinsic axis-control; hierarchy, exposure, or illumination cannot substitute. A composed descriptor must reproduce those literal excerpts exactly once. A secondary `compound-control` cannot satisfy a required axis.

When a draft over-pulls an axis, replace or remove its positive control rather than appending an opposing negative.

## Output and diagnosis

When color is primary, emit one compact causal signature before flexible inventory: dominant-region axes, supported global/light shift, and tone response without repeated direction.

When supporting, emit only the smallest relational cue. Diagnose differences as intrinsic, illumination, global cast, exposure/tone curve, processing, or unresolved; keep profile/measurement uncertainty separate from visual judgment.

For render comparisons, report prompt validity, pixel availability, evaluation status, global component, target-local residual, and user judgment separately. An identical-prompt retry is not a color correction. Revise one dominant residual axis at a time only with permission, then freeze a new version.

## Optional negative contribution

Reject only source-likely drift in relative value, chroma, hue direction, global cast, exposure response, tone-zone behavior, or unsupported uniform grading. Do not install fixed color-word blacklists or example-specific desired values.
