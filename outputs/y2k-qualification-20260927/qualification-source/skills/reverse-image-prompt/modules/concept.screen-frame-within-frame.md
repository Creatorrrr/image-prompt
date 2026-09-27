---
id: concept.screen-frame-within-frame
version: 4
priority: 90
type: concept
tier: 1
facet: relationship
facet_values:
  - screen-frame-within-frame
  - phone-screen
  - poster-frame
  - inserted-image
  - contained-frame
triggers:
  - phone, screen, poster, frame, UI, or image plane containing important content
avoid_when:
  - no nested frame or screen-contained content
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: screen, poster, and frame-within-frame

## When to load

Load when a visible screen, poster, print, photograph, frame, UI preview, window, or picture plane contains important content, or when that plane completes/replaces another visible subject.

## Detection cues

- Rectangular plane with its own content and edges.
- Secondary face/object/scene inside a screen, poster, reflection, or frame.
- Contained content differs in medium, scale, sharpness, brightness, or perspective from the surrounding scene.
- The contained layer is partial or low-legibility.

## Prompt additions

- Separate canvas orientation from object orientation. For each major rectangle, state its long edge, short edge, corner order, and image-plane rotation.
- Lock the container's corner coordinates, border thickness, rotation, perspective skew, crop, and image-plane area.
- Describe contained content as contained content, not as an in-world object unless it visibly is one.
- State visible fragments inside the container and absent counterpart fragments.
- Preserve medium contrast: screen glow, print flatness, poster grain, frame border, glass glare, UI preview softness, or low-resolution contained image.
- If the screen/frame replaces hidden subject features, combine with `concept.occlusion-replacement` and state replacement logic explicitly.

## Optional negative contribution

Reject turning screen/poster content into a real physical subject; full second scene; complete body/object when only a fragment is visible; wrong rectangle rotation; flattening a diagonal screen upright; removing borders; adding full app chrome or clean product-screen UI when absent.

## Optional settings contribution

- Perceptual relationship locks: contained layer remains within the frame/screen/poster.
- Coordinate and anchor locks: container corners, border, rotation, and content crop.
- Coherence/realism ceiling locks: preserve mixed layer or screen-contained reading.
