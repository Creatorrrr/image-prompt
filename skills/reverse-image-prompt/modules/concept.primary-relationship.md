---
id: concept.primary-relationship
version: 6
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
  - dominant_fidelity_axis
  - aesthetic_invariants
  - flexible_dimensions
---

# Concept: primary perceptual proposition and relationship

## When to load

Always. Apply spatial analysis more deeply to occlusion, replacement, reflection, frame-within-frame, miniature scale, mixed media, collage, and other relationship-led images. Do not assume every image is relationship-led.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed` before deciding prompt order.

- `relationship-led`: topology or interaction carries the image.
- `appearance-led`: form, surface, light, color, or visible gestalt carries it despite modest pose variation.
- `information-led`: layout, legibility, sequence, or data hierarchy carries it.
- `mixed`: two named axes are genuinely co-primary.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. The visible elements, hierarchy, and primary perceptual proposition: what makes the image itself or compelling, beyond object inventory.
2. The dominant fidelity axis and smallest causal cue set.
3. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it.
4. For relationship-led or mixed images, the stable zones and each critical pair's side, containment, contact, support, depth, occlusion, and boundary crossing.
5. One to three likely failures, including a category default replacing source-specific evidence.

Build a sparse relation graph, grouping repeated elements that share a relation. For ordinary images, keep an ordinary premise. In appearance-led images, preserve spatial facts without letting minor pose coordinates outrank form, surface, light, color, or hierarchy. In information-led images, prioritize layout and legibility.

Distinguish image-plane overlap from scene-space containment, contact, and support. A bare verb such as `holding`, `leaning`, or `sitting` is insufficient when the geometry could plausibly invert. Record contact, visible weight support, and relation to the boundary or support plane. Use object- or scene-relative zones when screen directions are ambiguous.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record join, overlap, contact, containment, hidden or partial regions, boundary side, support, layer order, scale, and coherence ceiling.

## Prompt contribution

Write a construction recipe, not a prop list. Lead with the dominant axis and invariants; spend more words on topology only when it is first-order.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Normally one to three interaction sentences suffice. Avoid redundant coordinates.

## Optional negative contribution

When supported, reject only likely drift: broken seams, wrong boundary side, inverted containment or support, wrong layer order, completed hidden regions, normalized appearance, or a primary invariant demoted to generic detail.
