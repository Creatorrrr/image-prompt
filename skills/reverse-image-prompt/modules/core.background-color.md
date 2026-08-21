---
id: core.background-color
version: 7
priority: 102
type: core
tier: 0
facet: core
facet_values:
  - background
  - color
  - palette
  - environment-zoning
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - background_zoning
  - low_legibility_background
  - color_mood
  - background_legibility_ceiling
  - color_causality
  - global_cast_consistency
  - neutral_reference_anchor
---

# Core: background, color, and environment zoning

## When to load

Always. Every image has background, color, or negative-space structure.

## Rules

- Analyze background zoning as image-plane layers, edge bands, negative space, dark or bright masses, texture, and low-detail regions; preserve their crop positions.
- Preserve background priority. Keep dim, cropped, blurred, hidden, or secondary elements as low-detail massing.
- Treat background legibility and information density as part of the source aesthetic. Named elements inherit source blur, haze, contrast, and detail limits.
- Preserve color mood, cast, saturation, contrast, shadow/highlight color, and local relationships; do not normalize them toward genre defaults.
- Separate intrinsic surface color from illumination color, global color cast or palette shift, exposure or tone curve, and processing. Consolidate each important surface or region into one owned color instruction; other modules may describe how light shifts it but must not restate the same perceptual direction as additional emphasis.
- Keep global cast consistent with the source-visible behavior of multiple regions rather than inferring it from one salient surface. When a global shift is uncertain, preserve relative region relationships instead of forcing a white balance or palette grade.
- Treat a possible neutral reference as evidence only when its low-chroma appearance survives visible illumination, reflection, exposure, clipping, compression, and processing. Record confidence rather than assuming that white, gray, black, or metal is neutral.
- Keep value, chroma, and hue relationships separate. A hierarchy statement may own relative brightness, saturation, area, or contrast, but must not restate a region's intrinsic hue unless hue contrast itself carries the hierarchy.
- In dark, compressed, or hazy areas, distinguish crushed regions from remaining folds, edges, silhouettes, texture, or hints; neither erase nor brightly recover them.
- Prevent clean-room drift: do not replace messy, partial, compressed, or ordinary zones with a tidy backdrop unless visible.

## Prompt additions

Describe zones by position, mass, contrast, legibility, depth, and color behavior before setting labels.

## Optional negative contribution

Reject source-likely cleanup, recovery, invented legibility, removed clutter, added depth, or priority drift.

## Optional settings contribution

- Background, palette/cast, and low-legibility locks:
