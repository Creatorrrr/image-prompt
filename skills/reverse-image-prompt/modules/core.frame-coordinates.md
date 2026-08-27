---
id: core.frame-coordinates
version: 13
priority: 108
type: core
tier: 0
facet: core
facet_values:
  - frame-coordinates
  - aspect-ratio
  - coordinates
  - crop
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
conflicts: []
provides_anchors:
  - aspect_ratio_drift_major
  - normalized_coordinates
  - subject_environment_balance
  - major_region_hierarchy
---

# Core: frame, crop, and spatial anchors

## When to load

Always.

## Source frame

- Record exact source dimensions when available.
- Treat aspect-ratio drift as a major fidelity failure.
- Keep source dimensions separate from target size; do not assume generator support.
- Preserve measured ratio in plain language; add a decimal only to distinguish nearby shapes.
- Do not invent exact dimensions from a viewer preview.
- Put frame shape, crop, and edge interactions first. Lock subject frame share and negative-space share before adding face or object micro-detail.
- Describe which evidence occupies the frame zones, including any material source-visible axis offset.

## Major-region hierarchy

Map the few largest visually coherent regions as a major-region hierarchy before local detail. Record relative area, role, attention, legibility, and frame contact without fixed percentages.

Preserve region-share hierarchy when flexible pose, viewpoint, or placement changes; exact coordinates may move.

## Spatial language

In `prompt`, when orientation is P0/P1, emit one macro result plus decisive residual relations. Placement proves no orientation. Treat alignment semantics as positive controls; enumerate every axis each exact clause affects explicitly or implicitly.

In `audited`, disposition every spatial axis. `flexible` or `not-material` requires isolated neutralization with adjacent relations held; low-confidence or wholly confounded axes become uncertain unless coupled. Run both human counterfactuals, merge joint effects once, and block a spatial clause affecting any unowned axis.

## Relational coordinate frames

- Use frame-relative directions for composition and object- or scene-relative zones for physical relationships. Qualify `left`, `right`, `front`, or `behind` when viewpoint could reverse them.
- Establish a visible shared reference plane when it disambiguates the scene: floor, ground, seat, platform, tabletop, interior volume, or another support region.
- Record which side of a boundary holds the main mass and which parts cross it. Separate 2D overlap from contact, containment, support, and depth order.
- Prefer a stable natural-language relation over extra coordinates. Coordinates lock placement in the frame but cannot by themselves establish physical topology.

Use normalized coordinates only for concept-critical anchors.

- Use no more than five numeric anchors in a normal prompt.
- Reserve them for seams, screen corners, occluder boundaries, UI bands, reflection joins, replacement zones, or unusual scale relationships that natural language cannot lock clearly.
- Use approximate ranges rather than false precision.
- Do not repeat the same coordinate in prose, negative prompt, and settings.
- When coordinates and natural-language placement disagree, keep the visible relationship and revise or remove the numeric estimate.

## Crop and completion

- Separate hair/head-outline cropping from facial-feature cropping.
- Name which important features remain fully inside the frame and which regions are hidden, occluded, or outside it.
- Preserve unusual headroom, edge bias, negative space, or full-frame scale.
- Prevent a salient face, hand, product, or text mark from being enlarged when that would erase source-visible context.

## Target-size handoff

If settings are requested, report the source frame as metadata and the validated target size separately. Prefer `auto` without a valid deterministic adapter, and disclose ratio-preserving adjustments.
