---
id: subject.product
version: 4
priority: 65
type: subject
tier: 2
facet: subject
facet_values:
  - product
  - package
  - object-arrangement
  - foreground-object
  - prop-anchor
triggers:
  - product, package, object arrangement, prop as foreground anchor
avoid_when:
  - no product/object fidelity requirement
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Subject: product and object fidelity

## When to load

Load when a product, package, tool, container, collectible, appliance, object arrangement, or foreground prop is a main subject or important anchor.

## Prompt additions

- State whether the object is the hero subject, co-dominant, secondary anchor, or incidental prop.
- Lock bounding box, rotation, perspective skew, top/bottom/side edges, visible face planes, crop, scale relative to hands/body/table/frame, and overlap.
- Describe geometry before brand/category: rectangular box, cylinder, soft pouch, transparent bottle, curved device, rigid package, folded fabric object, glossy prop, etc.
- Describe materials and surface behavior: matte/glossy, transparent, translucent, metallic, plastic, paper, cardboard, fabric, ceramic, glass, liquid, worn, scratched, wrinkled, compressed, low-res.
- For labels or packaging text, combine with `detail.text-logo-label`. Treat text as low-legibility graphic marks unless exact text is central and clearly readable.
- If decorative small details exist, keep them subordinate to object size. Do not let detail count turn a prop into a product hero.
- Preserve ordinary, candid, cluttered, awkward, cropped, or low-quality product evidence. Do not turn it into clean commercial product photography unless visible.

## Optional negative contribution

Reject product-shot normalization, centered clean hero object, enlarged secondary prop, invented brand labels, crisp unreadable marks, more premium materials, different package shape, wrong rotation/perspective, completed cropped object, duplicated products, removed hand/object overlap, and studio lighting when source is casual.

## Optional settings contribution

- Category-specific locks: product/object geometry, material, scale, crop, and label legibility.
- Coordinate and anchor locks: object bounding box and edge placement.
