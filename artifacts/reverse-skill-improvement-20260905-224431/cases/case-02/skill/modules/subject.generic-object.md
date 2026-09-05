---
id: subject.generic-object
version: 4
priority: 50
type: subject
tier: 2
facet: subject
facet_values:
  - generic-object
  - ordinary-object
  - ordinary-scene
  - object
  - none
triggers:
  - no specific subject module fits but a subject/ordinary-scene decision is still needed
avoid_when:
  - a more specific subject module clearly applies
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - generic_subject_fallback
---

# Subject: generic object or ordinary scene fallback

## When to load

Load when no specific subject module fits, but the router still needs a subject decision for an ordinary object, partial prop, abstract surface, empty scene, or visually simple arrangement.

## Rules

- When no specific subject module fits, preserve the main visible object or ordinary scene as a generic object/scene without inventing a category.
- Describe image-plane role, position, scale, crop, material, color, occlusion, edge contact, and visibility level before naming a broad object category.
- If the subject is absent, abstract, mostly background, or only a partial edge element, say so and avoid promoting it into a central object.
- Do not add a person, product, animal, vehicle, document, architecture, landscape, food, or brand category just to make the prompt sound complete.

## Prompt additions

Use direct visible descriptions such as `ordinary partial object`, `simple cropped surface`, `abstract/ambiguous foreground shape`, or `mostly empty scene` when that is more faithful than a category label.

## Optional negative contribution

Reject invented categories, added subjects, object completion, product-shot conversion, and subject centralization that is not visible.

## Optional settings contribution

- Generic subject fallback locks:
