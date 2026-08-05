---
id: concept.mixed-media-illusion
version: 4
priority: 84
type: concept
tier: 1
facet: relationship
facet_values:
  - mixed-media
  - illusion
  - sticker-overlay
  - decal
  - collage
  - medium-contrast
triggers:
  - flat sticker, decal, graphic overlay, collage, medium contrast illusion, inserted graphic surface
avoid_when:
  - single coherent medium with no mixed-media contrast
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: mixed media, flat overlays, and illusion fidelity

## When to load

Load when the image combines different media or realism levels, such as a flat sticker on a photo, cel-shaded graphic over a real subject, printed insert, collage panel, stylized overlay, or composited element whose contrast is visually important.

## Detection cues

- Hard simplified contours, outline style, color blocks, or limited shading against a photographic subject.
- Inserted element has different resolution, lighting, perspective, grain, or material behavior.
- The source depends on the mismatch rather than seamless realism.

## Prompt additions

- Describe the element's visual role first: flat graphic overlay, sticker, decal, printed mark, cel-shaded insert, collage fragment, or stylized overlay.
- Lock simplified contour, outline weight, shape count, color-block treatment, limited shading, flatness, and exact overlap with the real subject.
- If related stems, labels, marks, leaves, symbols, or secondary shapes share the same graphic treatment, treat them as part of the same overlay family.
- Preserve the coherence ceiling: do not make the mixed-media element physically plausible, seamlessly 3D, or material-matched unless the source is visibly that way.

## Optional negative contribution

Reject conversion into realistic physical props, botanical objects, jewelry, polished 3D accessories, clean product graphics, seamless CG, or fully integrated realistic objects when the source depends on medium contrast.

## Optional settings contribution

- Coherence/realism ceiling locks: preserve medium mismatch and source-level implausibility.
- Style/rendering target: specify each medium layer separately when needed.
