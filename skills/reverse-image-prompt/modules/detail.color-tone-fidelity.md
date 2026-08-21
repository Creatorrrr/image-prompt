---
id: detail.color-tone-fidelity
version: 2
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
---

# Detail: color and tone fidelity

## When to load

Load only when color or tonal behavior is a primary or supporting invariant, the user explicitly asks for tone fidelity, or a likely causal mix-up could materially change the image. Do not load merely because an image contains color.

## Color/Tone Contract

Build a source-relative Color/Tone Contract only when color or tonal behavior materially carries fidelity.

Set its observation scope first: `source-visible` for ordinary image evidence, `color-managed` only when trustworthy profile/calibration evidence exists, or `user-specified` for an explicit external target. Treat sampled pixels as source-visible display color, not proof of biological, material, or scene-referred true color. For human surfaces, never substitute racial, ethnic, or demographic identity labels for observable color evidence.

For each important region, record only observable evidence:

- separate value or lightness, chroma or saturation, and hue family or undertone
- identify the region's visual role and source-visible relation to another region
- distinguish intrinsic surface behavior from illumination, global cast or palette shift, exposure or tone curve, and processing
- record confidence and uncertainty instead of inventing a missing color cause

Assign every material color or tone observation to intrinsic surface, illumination, global cast or palette shift, exposure or tone curve, or processing.

Describe important regions through separate value, chroma, and hue observations plus source-visible relations to other regions. Do not let one broad adjective silently determine all three axes.

Treat an appearance metaphor as a hypothesis that may mix color, finish, illumination, and polish. Decompose it into value, chroma, hue, surface behavior, and light response first. If it remains useful, emit it once only as a non-directional summary of those already-owned controls.

Map highlight, midtone, shadow, or flat-field behavior only at the granularity the source supports. A flat graphic need not acquire photographic tone zones, and a clipped, compressed, mixed-light, or low-legibility region must retain that uncertainty.

## Calibration evidence

Treat a possible neutral as a calibration anchor only with visible evidence and an explicit confidence level. A white, gray, black, metallic, or low-chroma region may still be shifted by colored illumination, reflection, exposure, clipping, compression, or grading.

When no reliable neutral exists, preserve relative color relationships and mark global-cast uncertainty rather than inventing a white balance. In photographs, translate a supported global cast into white-balance or capture language; in non-photographic work, treat it as a palette or rendering shift.

Use more than one representative patch when measurement tools are available and tone is first-order. Prefer robust region summaries over a single pixel. Inspect embedded color-profile status, and disclose any assumed display space or missing profile.

Compare multiple target patches with contextual or neutral groups before attributing a color difference to an intrinsic surface or a global cause. Equal-weight region summaries prevent one large patch from dominating. Shared movement across target and context supports a global cast, exposure, or processing cause; target-only movement supports a local or intrinsic cause; mixed evidence remains uncertain.

For an exact local file, the optional probe accepts analyst-selected normalized regions and never chooses semantic targets itself:

```bash
python tools/color_probe.py IMAGE --region name=x0,y0,x1,y1
python tools/color_probe.py SOURCE --region name=x0,y0,x1,y1 \
  --compare RENDER --compare-region name=x0,y0,x1,y1
python tools/color_probe.py SOURCE \
  --region target-a=x0,y0,x1,y1 --region target-b=x0,y0,x1,y1 \
  --region context-a=x0,y0,x1,y1 --region context-b=x0,y0,x1,y1 \
  --group target=target-a,target-b --group context=context-a,context-b \
  --compare RENDER
```

Use matching region names for comparison. Select bounds from visible evidence and keep differently posed or cropped images on independently chosen bounds.

Use measurements as diagnostic evidence, never as automatic prompt wording or proof of intrinsic color. Exact RGB, hex, Lab, or temperature values should not enter a production prompt unless the downstream generator genuinely supports them and the source evidence justifies that precision.

## Cross-layer effect budget

Merge color and tone claims by their shared perceptual effect across causal layers, not only by semantic-slot name.

Give material effects a canonical source-relative effect identifier covering the affected region, perceptual axis, direction, and aggregate strength. If intrinsic color, illumination, global cast, exposure, processing, or hierarchy all push the same region in the same direction, require independent evidence for each layer and judge their combined pull against one aggregate target.

- Merge unsupported repetition into one owned control.
- Preserve genuinely multi-layer color only when the source supports every layer and their aggregate result.
- Let hierarchy own relative area, value, chroma, or contrast. It may own hue only when hue contrast itself is an invariant; it must not repeat another region's intrinsic hue for emphasis.
- Treat free-floating color or mood words as unowned until assigned to one causal layer.

## Final prompt control ledger

After drafting, copy every exact final-prompt excerpt that can change value, chroma, hue, contrast, cast, exposure, finish, or grading into `emitted_controls`. Give each excerpt one emitted claim, one causal layer, and the complete aggregate-effect list referenced by that claim. Split an ambiguous compound when a modifier could apply to intrinsic surface, illumination, exposure, or processing simultaneously. Every color/tone claim must be covered exactly once; do not merely copy the earlier analysis wording.

When a final draft over-pulls an axis, replace or remove the responsible positive control. Do not append an opposing negative instruction. This ledger is semantic and source-relative: it requires neither a fixed adjective list nor a preferred numeric target.

## Evidence contribution

When color or tone is primary, contribute one compact causal signature before flexible pose or inventory. Normally cover the dominant region's intrinsic value/chroma/hue, the supported light or global shift, and its highlight-to-shadow or flat-field response without repeating a direction.

When color is supporting, contribute only the smallest relational cue needed to preserve it. Use one source-likely drift boundary only when replacing or merging the affirmative wording does not already control the risk.

## Diagnostic mode

State whether the observed difference is principally intrinsic color, illumination, global cast, exposure or tone curve, processing, or an unresolved combination. Keep profile and measurement uncertainty separate from visual judgment.

## Optional negative contribution

Reject only source-likely drift in relative value, chroma, hue direction, global cast, exposure response, tone-zone behavior, or unsupported uniform grading. Do not install fixed color-word blacklists or example-specific desired values.
