---
id: concept.reflection-mirror
version: 4
priority: 90
type: concept
tier: 1
facet: relationship
facet_values:
  - reflection
  - mirror
  - glass-reflection
  - water-reflection
  - duplicated-layer
triggers:
  - mirror, reflective surface, water/glass reflection, duplicated reflected layer
avoid_when:
  - no reflection or mirror logic
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: reflection and mirror fidelity

## When to load

Load when reflection is a meaningful part of the image: mirror selfie, reflective product, water reflection, window reflection, glass overlay, glossy metal highlight, or reflected background layer.

## Detection cues

- Duplicated but softened or distorted subject/object.
- Visible mirror/window/glass edge or reflective plane.
- Reversed orientation, offset, transparency, blur, color shift, glare, or partial occlusion.
- Reflection contains only fragments, not a complete second scene.

## Prompt additions

- Name the reflecting surface as a visual role: mirror plane, glass overlay, water reflection, glossy material, metallic highlight, or secondary reflected layer.
- Lock the reflection plane coordinates, crop, angle, opacity, blur, distortion, color shift, and brightness relative to the real layer.
- State whether reflection content is reversed, offset, partial, cropped, shadowed, or low-legibility.
- Keep reflected faces, objects, text, and background fragments as fragments unless the source clearly shows a complete reflected object.
- If reflection and real subject align, preserve shared lines, eye lines, edges, contact points, and scale match.

## Optional negative contribution

Reject a complete duplicate subject when only a fragment exists; wrong mirror side; reflection becoming a separate physical object; removing glass glare; making reflection too sharp, bright, centered, complete, or readable; inventing missing reflected features; eliminating the reflective surface.

## Optional settings contribution

- Perceptual relationship locks: real layer and reflection layer remain distinct but aligned.
- Completion/seam continuity locks: reflected fragments stay cropped/blurred/partial.
- Lighting-to-volume fidelity locks: preserve glare, highlight streaks, reflection brightness, and surface sheen only as visible.
