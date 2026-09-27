---
id: subject.document-data-diagram
version: 4
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

## Optional negative contribution

Reject crisp invented text, random letters, fake labels, altered chart type, invented data values, extra legends, completed tables, wrong panel layout, centered clean poster redesign, infographic beautification, and document flattening when source has perspective/crop.

## Optional settings contribution

- UI/text/label locks when relevant: legibility ceiling, layout, grid, panels, axes, labels, and data mark density.
- Category-specific locks: document/diagram layout and perspective.
