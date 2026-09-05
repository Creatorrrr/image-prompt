---
id: core.frame-coordinates
version: 15
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

In `prompt`, emit one P0/P1 macro plus decisive residuals. Placement proves no orientation. Treat alignment wording as positive control and enumerate every affected axis.

<!-- profile:audited -->
In `audited`, disposition every axis. `flexible` or `not-material` needs isolated neutralization; uncertain evidence stays uncertain unless coupled. Run both human counterfactuals, merge joint effects once, and block unowned spatial pulls.
<!-- /profile -->

## Relational coordinate frames

- Frame placement references the frame. Cross-component placement references another region and separates direction, proximity, overlap, and surviving visibility.
- If direction survives material displacement, close subject-to-frame, reference-to-frame, and inter-region relations, then test residual drift with direction held.
- Use frame-relative directions for composition and scene-relative zones for physical relations. Qualify viewpoint-dependent sides.
- Establish a visible support plane only when it disambiguates the scene.
- Separate 2D overlap from contact, containment, support, and depth order.
- Prefer stable natural language; coordinates lock frame position, not physical topology.

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
