---
id: concept.scale-miniature
version: 4
priority: 88
type: concept
tier: 1
facet: relationship
facet_values:
  - scale-miniature
  - miniature-in-real
  - toy-scale
  - figurine
  - small-figure-real-environment
triggers:
  - small physical figure, toy, figurine, plush, miniature, or scale contrast in a real environment
avoid_when:
  - ordinary full-scale subject with no scale contrast
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - miniature_scale
  - endpoint_sensitive
  - polish_amplifying
---

# Concept: stylized miniatures in real environments

## When to load

Use only when visible evidence supports a small stylized physical figure, doll, figurine, plush, toy, collectible, or CG-like miniature placed inside a real photographed environment. Treat miniature-vs-real-world scale as a first-order concept lock, not a style detail.

## Detection cues

- Toy-scale subject near real hands, fingers, household objects, table edges, bedding, screens, or room elements.
- Molded, plush, synthetic, or stylized material visible under real-world lighting.
- Tight crop where the miniature's head/body is large in frame but real-world anchors reveal small scale.
- Casual phone-video compression or low-detail edges around a miniature object.

## Prompt additions

- Treat the scale relationship as a first-order concept lock.
- Treat a cropped or obscured appendage as endpoint-sensitive.
- Audit for polish-amplifying phrases.
- Lead with measured frame shape, casual capture fidelity, and miniature-vs-real-world scale relationship before attractive character design.
- If a real hand, finger, tool, household object, support surface, or foreground prop interacts with the miniature, lock the contact point, contact area, contact direction, touched endpoint, overlap, untouched regions, and whether anything is lifted or under tension.
- Distinguish passive contact from active manipulation. Avoid `pinch`, `hook`, `pull`, `grip`, `hold`, or `petting` unless visible.
- Contact correction must not widen the shot. Keep tight subject scale, edge cuts, foreground support height, incomplete body visibility, and awkward close-camera framing.
- Describe support geometry before gesture when a hand or prop rests on a cushion edge, blanket fold, table edge, ledge, step, ridge, or raised foreground boundary.
- Preserve the subject as a photographed or captured object when supported: synthetic material, molded surface, seam-like construction, toy scale, real room lighting, mixed-media insertion. Reject life-size human or polished product render drift.
- For low-resolution or casual phone-video captures, put compression softness, focus hierarchy, motion softness, low-detail edges, imperfect room lighting, and casual capture noise near the beginning and in critical locks.
- For small appendages, plush extensions, fuzzy tails, wires, antennae, ornaments, ribbons, straps, cords, tags, or endpoints, lock bounded footprint, path, width budget, endpoint, contact point, and low-detail scale before category nouns.

## Optional negative contribution

Reject life-size human, pure 2D illustration if the source is physical, polished product render, complete seated figure when cropped, full-body product view, zoomed-out scene, added floor, extra environmental breathing room, larger appendages, full loops/ropes/scarves replacing narrow endpoints, high-polish collectible sharpness when source is compressed.

## Optional settings contribution

- Scale/interaction anchor locks: miniature scale relative to hand/object/surface.
- Coherence/realism ceiling locks: captured toy-scale object in real environment; no life-size normalization.
- Focus and depth-of-field locks: phone/compression softness if present.
