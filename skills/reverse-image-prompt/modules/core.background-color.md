---
id: core.background-color
version: 5
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
---

# Core: background, color, and environment zoning

## When to load

Always. Every image has a background, color structure, or negative-space field that can drift if ignored.

## Rules

- Analyze background zoning as image-plane structure: foreground, midground, background, edge bands, negative space, depth layers, occluded zones, dark masses, bright windows, flat fields, texture bands, and ambiguous low-detail regions.
- Preserve the source background's visual priority. If background elements are dim, cropped, blurred, low-legibility, partly hidden, or secondary, keep them as low-detail background massing rather than turning them into clean readable objects.
- Treat background legibility and information density as part of the source aesthetic. A named or distinctive background element must inherit the source-visible blur, haze, contrast, and detail ceiling rather than becoming a crisp landmark.
- Preserve color mood, palette, color cast, saturation, contrast, shadow color, highlight color, and local color relationships. Do not neutralize a visible cast or push the image toward a postcard, clean-room, catalog, cinematic, or studio palette unless that is visibly present.
- For underexposed, low-contrast, compressed, or hazy backgrounds, distinguish fully crushed regions from regions that still show folds, edges, silhouettes, texture, or environmental hints. Preserve remaining detail without turning dark areas into featureless black or brightly recovered scenery.
- Prevent clean-room drift for products, portraits, screenshots, documents, and ordinary scenes. Do not replace messy, partial, compressed, cropped, or ordinary background zones with a smooth backdrop, empty studio, clean wall, perfect sky, luxury interior, or tidy product surface unless visibly present.
- Treat background zoning as part of crop and coordinate fidelity. Edge bands, side strips, awkward headroom, bottom UI bands, floor/wall seams, horizon placement, poster edges, and environmental slivers must remain in their visible positions when they matter.

## Prompt additions

Describe background zones by position, mass, contrast, legibility, depth, and color behavior before using broad setting labels.

## Optional negative contribution

Reject postcard scenery, clean-room backdrop, studio sweep, tidy catalog surface, brightened recovered background, readable invented signage, removed clutter, added depth, and background elements becoming cleaner or more central than visible.

## Optional settings contribution

- Background zoning locks:
- Palette/color-cast locks:
- Low-legibility background massing locks:
