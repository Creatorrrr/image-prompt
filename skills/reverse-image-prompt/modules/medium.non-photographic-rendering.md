---
id: medium.non-photographic-rendering
version: 2
priority: 72
type: medium
tier: 2
facet: medium
facet_values:
  - non-photographic
  - illustration
  - painting
  - 3d-render
  - anime
  - vector
  - cel-shading
  - game-engine
triggers:
  - illustration, painting, 3D render, anime, vector, cel shading, game-engine image
avoid_when:
  - clearly photographic source
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts:
  - medium.photographic-capture
  - medium.unspecified-visual
provides_anchors: []
---

# Medium: non-photographic rendering fidelity

## When to load

Load for illustration, painting, 3D rendering, anime/cel shading, vector art, sketches, concept art, pixel art, game-engine images, diagrams with stylized rendering, or mixed media with clear non-photographic layers.

## Prompt additions

Adapt fidelity rules to the visible medium:

- virtual camera, perspective, crop, depth layering, and composition
- stylized proportions and shape language
- edge quality: hard vector edges, soft painterly edges, sketch lines, inked contours, anti-aliasing, pixel edges
- linework: thickness, taper, pressure, wobble, clean/rough quality, hatch density
- brush texture, paint thickness, canvas/paper grain, wash, dry-brush, impasto, airbrush, marker, watercolor bleed
- value structure, shadow style, cel-shading steps, gradients, ambient occlusion, rim lines, highlights
- 3D material treatment: plastic, clay, metal, skin shader, subsurface, roughness, specular, depth of field, render noise, game-engine lighting
- composition and crop over style shorthand; do not use a famous artist or copyrighted character name

If the image mixes photographic and non-photographic layers, combine with `concept.mixed-media-illusion`.

## Negative additions

Reject wrong medium: photo realism when source is illustration, cartoon/anime when source is realistic, 3D render when source is painting, vector clean-up when source is hand-drawn, painterly blur when source is crisp cel-shaded, excessive detail, famous-artist style drift, and polishing rough linework or texture.

## Settings additions

- Style/rendering target:
- Film/camera/sensor or medium artifact locks:
- Coherence/realism ceiling locks when mixed media is present.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy non-photographic adaptation rules

- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.


For small side-profile or over-shoulder faces, lock the gaze geometry as image-plane evidence. State whether the nose points left or right, how much of each eye is visible, whether the far eye is hidden by hair/shadow/profile angle, and whether the mouth reads as a small side contour. Reject turning this into a clearer direct-gaze portrait even when the source appears to look toward the camera.

If the source face reads closer to a side profile than a portrait glance, lead with the profile evidence before any gaze wording. A tiny visible eye or cheek highlight should not be enough to request direct eye contact. Prefer `small side-profile facial sliver`, `near eye barely readable`, and `gaze ambiguous through shadow` over `looking at camera` when the camera-facing evidence is weak.

For contact gestures where a hand, limb, hair, clothing, tool, prop, or other occluder touches or grips another visible element, describe the contact as a spatial relationship, not just as a generic gesture. Lock approximate size, angle, visible fingers or endpoints, contact point, compression, overlap, hidden portions, loose or displaced material, and where the interacting element begins and ends. If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.
