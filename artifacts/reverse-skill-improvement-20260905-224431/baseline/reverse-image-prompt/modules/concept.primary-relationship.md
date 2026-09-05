---
id: concept.primary-relationship
version: 11
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
  - appeal_render_separation
  - invariant_salience_ledger
---

# Concept: primary perceptual proposition and relationship

## When to load

Always. Apply deeper spatial analysis to relationship-led occlusion, replacement, reflection, frame-within-frame, miniature, mixed-media, or collage images; do not impose it on ordinary images.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed` before deciding prompt order.

Relationship-led means topology or interaction carries the image; appearance-led means form, surface, light, color, or gestalt survives modest pose variation; information-led means layout, legibility, sequence, or data hierarchy carries it; mixed names two genuinely co-primary axes.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. The visible elements, hierarchy, and primary perceptual proposition: what makes the image itself or compelling, beyond object inventory.
2. Record the direct appeal reading separately before deciding actuation. In generation, retain it once only as high-confidence P0/P1 source evidence whose omission causes material drift; immediately follow with visible mechanisms. Otherwise emit only the mechanisms.
3. The dominant fidelity axis and smallest causal cue set.
4. Rank visible effects by a viewer counterfactual: `P0` changes the source signature, `P1` changes structural identity, `P2` supports the read, and `P3` is incidental. Face, skin presentation, space, clothing, pose, topology, light, color, or capture may occupy any level; category and module count do not set priority.
5. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it. In `prompt`, retain only the smallest P0/P1 causal set and merge P2 support. In `audited`, build the full ledger. Build an invariant salience ledger. Bind retained atomic obligations.
6. For relationship-led or mixed images, the stable zones and each critical pair's side, containment, contact, support, depth, occlusion, and boundary crossing.
7. One to three likely failures, including a category default replacing source-specific evidence.

Merge synonymous non-color and non-light pulls into one source-relative aggregate effect with one claim and control.

Build a sparse relation graph and group elements sharing a relation. Keep ordinary premises ordinary. In appearance-led images, do not let minor coordinates or generic attractiveness outrank source-specific appearance; in information-led images, prioritize layout and legibility.

Distinguish image-plane overlap from scene-space containment, contact, and support. When geometry could invert, record contact, weight support, and the relevant boundary or support plane; use object- or scene-relative zones when screen directions are ambiguous.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record join, overlap, contact, containment, hidden or partial regions, boundary side, support, layer order, scale, and coherence ceiling.

## Prompt contribution

Contribute evidence candidates, not guaranteed prose. The central output contract merges candidates by semantic slot and assigns one clause owner. Write a construction recipe, not a prop list; lead with P0, then P1, and spend words only in proportion to viewer impact.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone. Multi-region form/topology retains its material region-to-region boundary.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Normally one to three interaction sentences suffice. Avoid redundant coordinates.

## Optional negative contribution

Reject only likely relationship, completion, normalization, or invariant-demotion drift.
