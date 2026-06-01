---
id: subject.product
version: 2
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

## Negative additions

Reject product-shot normalization, centered clean hero object, enlarged secondary prop, invented brand labels, crisp unreadable marks, more premium materials, different package shape, wrong rotation/perspective, completed cropped object, duplicated products, removed hand/object overlap, and studio lighting when source is casual.

## Settings additions

- Category-specific locks: product/object geometry, material, scale, crop, and label legibility.
- Coordinate and anchor locks: object bounding box and edge placement.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy foreground prop, product-adjacent, secondary-object, and text-budget rules


- If a visible adult body feature is large or very large, preserve it against reduction, flattening, averaging, hiding, or modesty/safety correction.
- If it is moderate, moderate-to-full, slight, flat, broad, secondary, softened, low-detail, or obscured, preserve that calibration against enlargement, extra projection, deeper neckline, tighter clothing, added cleavage shadows, added under-bust shadows, stronger highlights, sharper contouring, or increased dominance.
- If hands, phone, arms, hair, fabric, props, another person, cast shadow, self-shadowing, contact shadow, blur, crop, or frame edge partially hide contours, preserve that occlusion instead of revealing or clarifying hidden shape.
- If a feature is visible but not central, describe it as visible but secondary, not as dominant.
- If a feature is visually dominant because of crop, camera angle, lens, pose, lighting, or clothing, state the visible cause rather than inventing hidden anatomy.
- Avoid words that over-sculpt a covered or shadow-obscured body area. If the visible area reads mainly as a dark near-camera garment mass, say `covered near-field torso mass`, `clothing-shaped foreground area`, or `dark fabric plane` instead of repeated anatomy labels such as `chest`, `bust`, `abdomen`, `midriff`, or `waist`, unless those anatomical regions are visibly distinct and central.

Avoid repetition that over-weights body features. Mention a body feature in the body-proportion section, and repeat it in locks or negative prompt only when it is genuinely important to fidelity.

For crop-sensitive, near-frame, or garment/prop-dominant human images, lock relative image-plane widths and areas instead of relying on broad body or fashion labels. Compare visible shoulder/torso width, waist or closure-band width, garment-panel width, prop/accessory width, and nearby fixed anchors such as rails, furniture edges, mirrors, doors, horizons, or frame edges. State whether a visible body or garment region is actually dominant, or only appears prominent because of crop, camera distance, lens perspective, pose, lighting, or occlusion. Prefer visible construction anchors such as seams, pockets, straps, hems, closures, folds, coverage bands, narrow gaps, and cropped edges over repeated anatomy labels when the source is a clothing/crop composition. Prevent the generator from widening, narrowing, sculpting, glamour-posing, flattening, completing, or modestly hiding that silhouette unless those changes are visible in the source.

For close portrait or product-adjacent crops where a held foreground object, package, cup, phone, toy, bouquet, charm, ornament, or other small prop overlaps the torso or face, treat the prop as a measured foreground anchor rather than a category label. Lock its bounding box, top edge, bottom edge, hand overlap, rotation, visibility budget, and scale relative to the face, shoulders, nearby body regions, and crop. If tiny decorative figures or attachments sit on the prop, describe them as small attached ornaments with their actual count, silhouette height, and low-detail material treatment; do not let the wording promote them into full separate subjects. Put these locks in `PROMPT:` affirmative language, because downstream generation may ignore `NEGATIVE PROMPT:` and `RECOMMENDED SETTINGS:`.


For progress lines, scrub bars, separators, or edge slivers, preserve the observed length and discontinuity. If the source shows only a tiny partial line at an edge or a short pale segment, do not describe it as a full progress bar; explicitly reject full-width bars, timeline tracks, knobs, home indicators, or completed app controls unless they are visible.

For ambiguous tiny UI edge marks that are not central to recognition, do not over-promote them in `PROMPT:`. It is safer to say that no full progress bar or timeline is visible than to positively request a mark that may expand into a complete control. Mention the tiny mark only as a cropped edge artifact when it is visually clear and bounded.

For secondary objects such as bags, straps, jewelry, tools, handheld items, furniture fragments, signs, UI controls, props, or cropped products, create a secondary-object budget. Lock edge distance, bounding box, overlap with the primary subject or containing surface, visible crop, occlusion, and relative size against nearby body, object, frame, or background anchors. If the object is secondary or edge-adjacent in the source, describe it as partial, tucked, compressed, low-priority, obscured, or low-detail as supported by evidence; prevent it from becoming larger, cleaner, front-facing, product-like, fully readable, or more central than the source.

Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. In `PROMPT:`, lock each such region as partial or cropped; in `NEGATIVE PROMPT:`, reject completing, recentering, expanding, or clarifying those regions.
