---
id: subject.document-data-diagram
version: 2
priority: 62
type: subject
tier: 2
facet: subject
facet_values:
  - document
  - data
  - diagram
  - chart
  - map
  - poster
  - table
  - graph
triggers:
  - document, poster, table, graph, chart, map, diagram, interface layout with data
avoid_when:
  - no document/data/diagram subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - detail.text-logo-label
conflicts: []
provides_anchors: []
---

# Subject: documents, data, diagrams, maps, and layouts

## When to load

Load when the source contains a document, poster, graph, chart, table, map, technical diagram, scientific/medical visualization, infographic, or layout where geometry and text/data placement matter.

## Prompt additions

- Decide whether the document/data/diagram is the main subject, secondary layer, screen-contained content, or background fragment.
- Lock page/screen/poster aspect, rotation, perspective, margins, grid, panels, title area, axes, legends, callouts, arrows, tables, rows/columns, icons, blocks, labels, and whitespace.
- Preserve exact readable text only when clear and central. For small or ambiguous text, describe it as low-legibility marks with approximate placement, length, density, and contrast.
- For charts, describe chart type, axis placement, line/bar/point density, legend position, color grouping only if visible, and whether values are readable.
- For maps, describe land/water blocks, roads/paths, boundary lines, labels, markers, north/legend if visible, and scale of detail.
- For technical/scientific diagrams, preserve visual structure: nodes, arrows, layers, anatomy/parts only as visible, schematic vs realistic rendering, annotation density.
- Do not invent data, legible numbers, axis labels, or precise scientific meaning that is not visible.

## Negative additions

Reject crisp invented text, random letters, fake labels, altered chart type, invented data values, extra legends, completed tables, wrong panel layout, centered clean poster redesign, infographic beautification, and document flattening when source has perspective/crop.

## Settings additions

- UI/text/label locks when relevant: legibility ceiling, layout, grid, panels, axes, labels, and data mark density.
- Category-specific locks: document/diagram layout and perspective.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy low-legibility document, text, label, and diagram mark rules


When a body area or garment gap is only a thin bottom-edge or side-edge sliver, avoid making it sound like a subject. Prefer wording such as `a narrow edge band/gap remains at the crop boundary`, `a thin skin-toned edge strip`, or `a barely visible cropped gap` over labels such as `visible abdomen`, `visible midriff`, or `visible waist` unless that area is actually central and materially visible. If a prompt uses a body-part label for a sliver, immediately qualify that it is not a subject region and should not expand inward.

If the source garment is cropped near the bottom and a broad clothing category such as `crop top` would invite a fashion-style exposed abdomen composition, describe the visible hem and frame cut first, and use the category label only as secondary shorthand or omit it when the hem/crop is the important evidence. Never let bottom-edge garment wording imply that the lower body should be completed or that a larger skin band should be centered.

For small text marks, logos, labels, signatures, UI text, or incidental lettering, preserve location, size, contrast, and readability level over exact transcription unless the exact readable text is central to the image. If it is small, partial, distorted, or low confidence, describe it as an indistinct mark and prevent the generator from enlarging it or turning it into prominent clean typography.

For watermarks, product labels, package labels, background signs, reflected marks, engraved marks, and decorative monograms in photographic scenes, distinguish text-plane role from exact text content. If the mark is secondary, soft, transparent, curved, reflected, low-resolution, or partially legible, write it as a faint graphic or label artifact with approximate placement and legibility ceiling. Do not over-transcribe low-confidence letters in `PROMPT:` unless exact readability is central; over-transcription often makes generators create a crisp logo, clean sign, or new prominent text object.

For incidental text that is visible but compressed or small, lock it as low-legibility. Do not request crisp typography unless the source clearly centers readable text as the subject.

When incidental UI text is clearly readable despite being small, preserve the exact visible characters and their low-legibility rendering together. Do not let the generator substitute a plausible different time, placeholder, number, brand, or label. Exact text locks should still emphasize small size, soft edges, and secondary priority, not clean typography.

When incidental text is near a garment or object edge, describe it as a small, soft mark anchored to that edge. Avoid repeating the exact text in ways that make the model prioritize clean lettering over edge placement, size, softness, and low contrast.

For incidental interface overlays, screenshot controls, camera controls, reaction marks, low-confidence symbols, small badges, or cropped graphic marks, preserve them as low-legibility artifacts unless their exact symbol is central and clearly readable. Describe approximate shape, size, opacity, edge distance, internal contrast, and ambiguity. If the internal mark is unclear, call it an abstract mark rather than a named icon, arrow, logo, or app control. Reject conversion into clean readable typography, a brand mark, a watermark, a caption, or an enlarged interface element.

For progress lines, scrub bars, separators, or edge slivers, preserve the observed length and discontinuity. If the source shows only a tiny partial line at an edge or a short pale segment, do not describe it as a full progress bar; explicitly reject full-width bars, timeline tracks, knobs, home indicators, or completed app controls unless they are visible.

For ambiguous tiny UI edge marks that are not central to recognition, do not over-promote them in `PROMPT:`. It is safer to say that no full progress bar or timeline is visible than to positively request a mark that may expand into a complete control. Mention the tiny mark only as a cropped edge artifact when it is visually clear and bounded.

For secondary objects such as bags, straps, jewelry, tools, handheld items, furniture fragments, signs, UI controls, props, or cropped products, create a secondary-object budget. Lock edge distance, bounding box, overlap with the primary subject or containing surface, visible crop, occlusion, and relative size against nearby body, object, frame, or background anchors. If the object is secondary or edge-adjacent in the source, describe it as partial, tucked, compressed, low-priority, obscured, or low-detail as supported by evidence; prevent it from becoming larger, cleaner, front-facing, product-like, fully readable, or more central than the source.

Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. In `PROMPT:`, lock each such region as partial or cropped; in `NEGATIVE PROMPT:`, reject completing, recentering, expanding, or clarifying those regions.
