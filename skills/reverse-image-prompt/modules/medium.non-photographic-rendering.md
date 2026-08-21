---
id: medium.non-photographic-rendering
version: 5
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

When rendered or painted lighting is first-order, contribute the visible shading evidence to `detail.light-form-fidelity`. Treat physical lamp placement as optional and confidence-rated; for stylized media, preserve value grouping, gradient or cel-step structure, shadow ownership, material response, and spill as image-space results.

## Optional negative contribution

Reject wrong medium: photo realism when source is illustration, cartoon/anime when source is realistic, 3D render when source is painting, vector clean-up when source is hand-drawn, painterly blur when source is crisp cel-shaded, excessive detail, famous-artist style drift, and polishing rough linework or texture.

## Optional settings contribution

- Style/rendering target:
- Film/camera/sensor or medium artifact locks:
- Coherence/realism ceiling locks when mixed media is present.
