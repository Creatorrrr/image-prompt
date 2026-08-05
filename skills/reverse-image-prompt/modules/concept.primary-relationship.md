---
id: concept.primary-relationship
version: 5
priority: 106
type: concept
tier: 0
facet: core
facet_values:
  - primary-relationship
  - concept-lock
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - primary_visual_concept
  - concept_spec
  - major_component_relation_graph
  - major_component_topology
  - interaction_geometry_sentence
  - image_scene_space_distinction
---

# Concept: primary visual relationship

## When to load

Always. Apply more deeply to occlusion, replacement, reflection, frame-within-frame, miniature scale, mixed media, collage, or other relationship-led images.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

An object-complete prompt can still fail when the overlap, alignment, scale, seam, replacement, foreground/background ordering, side of a boundary, or support relationship is wrong.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. Literal visible elements.
2. The relationship viewers are meant to perceive.
3. The stable reference zones: visible floor/ground/support plane, interior or exterior region, near or far side, foreground or background layer, and any frame, barrier, opening, or container boundary.
4. For each concept-critical pair, the participating parts, relative side or containment, contact point, support or load-bearing role, depth order, occlusion, and whether either element crosses the boundary.
5. The cues that create it: alignment, contour continuation, overlap, shared line, crop boundary, contact, scale match, reflection, replacement, frame, or medium contrast.
6. The one to three most likely failure modes.

Build a sparse relation graph rather than an inventory: connect each major component or coherent repeated group to at least one other major component or stable reference zone. Group crowds, repeated objects, or background clusters when they share the same relation. Do not enumerate every possible pair.

For ordinary images, state an ordinary premise and do not invent a special effect.

Distinguish image-plane overlap from scene-space containment, contact, and support.

Contact alone is underspecified. `Holding`, `leaning`, `resting`, `sitting`, `standing against`, or similar interaction verbs must not replace the visible geometry when a plausible spatial inversion would change the scene. Record which part touches which surface or edge, which element carries visible weight, and where the remainder of the subject sits relative to the boundary or support plane.

Use object- or scene-relative zones when screen left/right would be ambiguous. Prefer a visible shared reference such as the same side as the floor or platform, within an enclosure, outside an opening, or on the near/far side of a structure. Name a semantic side only when the image actually supports it.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record the join, seam, overlap, contact, or containment geometry.
- Record what stays hidden, partial, or absent.
- Record the required boundary side, support relation, layer order, scale relationship, and coherence ceiling.

## Prompt contribution

Write a construction recipe, not a prop list. Explain what each element contributes and the minimum geometry required for the effect to read correctly. Spend more words on the relationship than on secondary textures or labels.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Keep this selective: normally one to three interaction sentences are enough. Do not enumerate every pair of objects, and do not add coordinates when the topological relationship is already clear in natural language.

## Optional negative contribution

When a negative prompt is supported, reject only likely concept and fidelity drift: broken seams, wrong boundary side, inverted containment or support, implausible boundary crossing, wrong layer order, duplicated counterparts, completed hidden regions, normalized medium contrast, or a concept-critical element demoted to a generic prop.
