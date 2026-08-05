---
id: subject.architecture-interior
version: 5
priority: 62
type: subject
tier: 2
facet: subject
facet_values:
  - architecture
  - interior
  - room
  - building
  - street-architecture
  - structure
triggers:
  - building, interior, room, street architecture, structural perspective
avoid_when:
  - no architectural or interior fidelity need
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.background-color
conflicts: []
provides_anchors: []
---

# Subject: architecture, street structure, and interiors

## When to load

Load when buildings, interiors, rooms, corridors, streetscapes, furniture layout, or structural perspective are important.

## Prompt additions

- Describe space by zones: foreground, midground, background, left, right, top, bottom.
- Lock horizon, vanishing direction, wall/floor/ceiling planes, doorway/window positions, vertical lines, arches, stairs, railings, columns, furniture seams, countertops, table edges, shelves, and floor/wall transitions.
- Treat a salient edge, barrier, wall, opening, counter, platform, seat, or ledge as a spatial boundary or support surface when it organizes an interaction. State which visible region it separates, which side contains each major subject, and whether contact is load-bearing, stabilizing, or merely overlapping in the image.
- State camera height, tilt, roll, and perspective distortion. Preserve vertical convergence or skew when visible.
- Describe materials: concrete, brick, tile, wood, plaster, glass, metal, fabric, stone, painted surface, worn/clean/reflective/matte.
- Preserve clutter, partial objects, edge cuts, occlusion, and imperfect room lighting. Do not turn an ordinary room or street into a clean architectural visualization.
- For signs/posters/labels, combine with `detail.text-logo-label`.

## Optional negative contribution

Reject straightened perspective if source is tilted, clean interior render, added windows/doors/furniture, removed clutter, wrong room type, sharper background than source, postcard-like architecture, perfect symmetry, extra people, and completed cropped structural elements.

## Optional settings contribution

- Category-specific locks: structural planes, perspective, material, room/street zoning, and architectural crop.
