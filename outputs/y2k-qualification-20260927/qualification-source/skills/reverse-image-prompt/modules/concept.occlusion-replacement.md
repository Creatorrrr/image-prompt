---
id: concept.occlusion-replacement
version: 4
priority: 95
type: concept
tier: 1
facet: relationship
facet_values:
  - occlusion
  - replacement
  - hidden-counterpart
  - foreground-blocking
  - partial-completion
triggers:
  - opaque occluder, replacement surface, hidden features, foreground prop blocking subject
avoid_when:
  - no occlusion or replacement logic
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: occlusion and replacement surfaces

## When to load

Load when an object, hand, phone, screen, sign, book, card, foreground prop, shadow, hair, crop edge, or frame boundary hides a concept-critical area or substitutes for part of another subject.

## Detection cues

- Opaque rectangle or prop crossing a face, torso, product, label, or background.
- Only a sliver of a counterpart feature remains visible.
- A phone/screen/card/frame supplies content that visually replaces hidden features.
- The image would become a different scene if the occluder moved, shrank, rotated, or became transparent.

## Prompt additions

- Describe the occluder before attractiveness, product clarity, garment labels, or scene completion.
- Lock the occluder's image-plane footprint, approximate corners, rotation, border thickness if visible, and overlap boundary.
- State which real-layer features remain visible outside the occluder and which features are hidden by it.
- If a surface replaces hidden content, state what the replacement surface carries and how it lines up with the hidden area.
- State hidden features as absent in the real layer when supported by visible evidence. Do not let them reappear around the edges.
- Use an overlap polygon when needed: containing surface corners, edge crossing the subject, lower/inner edge hiding features, and maximum reveal outside the polygon.
- Preserve awkwardness. If a prettier or more plausible image requires moving the occluder away, keep the occluder and accept the awkward crop.

## Optional negative contribution

Reject moved, smaller, higher, lower, transparent, recentered, or cleaned-up occluders; hidden face/body/product/text features reappearing; full counterpart completion; conventional portrait/product clarity replacing the blocked view; seam mismatch; duplicate features on both sides of the occluder.

## Optional settings contribution

- Occlusion fidelity locks: occluder footprint, corners, rotation, edge crossings, hidden-feature budget.
- Completion/seam continuity locks: which hidden/counterpart features remain absent.
- Boundary and visibility-budget locks: slivers remain slivers; cropped areas stay cropped.
