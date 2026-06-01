---
id: concept.reflection-mirror
version: 2
priority: 90
type: concept
tier: 1
facet: relationship
facet_values:
  - reflection
  - mirror
  - glass-reflection
  - water-reflection
  - duplicated-layer
triggers:
  - mirror, reflective surface, water/glass reflection, duplicated reflected layer
avoid_when:
  - no reflection or mirror logic
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: reflection and mirror fidelity

## When to load

Load when reflection is a meaningful part of the image: mirror selfie, reflective product, water reflection, window reflection, glass overlay, glossy metal highlight, or reflected background layer.

## Detection cues

- Duplicated but softened or distorted subject/object.
- Visible mirror/window/glass edge or reflective plane.
- Reversed orientation, offset, transparency, blur, color shift, glare, or partial occlusion.
- Reflection contains only fragments, not a complete second scene.

## Prompt additions

- Name the reflecting surface as a visual role: mirror plane, glass overlay, water reflection, glossy material, metallic highlight, or secondary reflected layer.
- Lock the reflection plane coordinates, crop, angle, opacity, blur, distortion, color shift, and brightness relative to the real layer.
- State whether reflection content is reversed, offset, partial, cropped, shadowed, or low-legibility.
- Keep reflected faces, objects, text, and background fragments as fragments unless the source clearly shows a complete reflected object.
- If reflection and real subject align, preserve shared lines, eye lines, edges, contact points, and scale match.

## Negative additions

Reject a complete duplicate subject when only a fragment exists; wrong mirror side; reflection becoming a separate physical object; removing glass glare; making reflection too sharp, bright, centered, complete, or readable; inventing missing reflected features; eliminating the reflective surface.

## Settings additions

- Perceptual relationship locks: real layer and reflection layer remain distinct but aligned.
- Completion/seam continuity locks: reflected fragments stay cropped/blurred/partial.
- Lighting-to-volume fidelity locks: preserve glare, highlight streaks, reflection brightness, and surface sheen only as visible.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy reflection and secondary-layer completion rules

## Primary Visual Concept and Perceptual Relationship Fidelity

Before listing visible objects, identify the primary visible concept that makes the image recognizable. Treat this as the highest-priority fidelity target. The primary concept may be an illusion, a mixed-media relationship, a frame-within-frame structure, a scale contrast, an interaction, a deliberately imperfect capture mode, or another visible relationship between elements.

Separate intent from inventory: an inventory lists what objects are present, while intent states what those objects are arranged to make the viewer perceive. When the two diverge, intent governs. Never let a complete object inventory substitute for the perceptual relationship; an image where every object is named but the intended relationship is absent has failed, even if no object is missing.

Describe each concept-critical element by its visual role, not only by its object category. Examples of roles include replacement surface, continuation plane, occluder, scale anchor, foreground interaction target, UI frame, reflection, inserted image, stylized overlay, physical prop, or medium-contrast anchor.

If two visible elements are meant to read as one continuous subject, preserve the alignment, scale, contour continuation, crop boundary, and feature proportions that create that perception. If one visible element replaces part of another subject, describe exactly which part is replaced, how the replacement aligns, and what would break the illusion.

When a replacement, reflection, screen, frame, overlay, occluder, or continuation plane completes another element, write it as a construction recipe rather than a prop list. State what content each surface carries, what hidden or counterpart features the completing surface supplies, and how the union avoids duplicated or missing features across the seam. Preserve shared eye lines, centerlines, contact points, contour junctions, feature scale, crop boundaries, and medium contrast that make the surfaces fuse or interact.

For handheld-screen or phone-screen replacement portraits, the screen is not merely a prop. Lock the screen as the active replacement surface with its approximate corner coordinates, diagonal or rotation angle, border thickness, image-plane area, and overlap boundary over the real subject. State which real face features remain visible outside the screen, which real features are hidden by the screen, and which screen-contained features visually substitute for the hidden side. If the source has only one real eye or a narrow facial sliver visible, make that visibility budget explicit and reject a fuller real face. If the screen is steeply diagonal, prevent the generator from flattening it into a generic horizontal selfie-phone pose or upright product-like phone.

If a handheld screen covers the lower center of a face or torso, state the screen's lower and inner overlap as mandatory, not optional. Name hidden mouth, chin, nose, cheek, jaw, neckline, garment, or torso zones as absent in the real layer when supported by visible evidence, and repeat that those hidden features should not reappear around the screen edges. When the source screen sits low enough to cover a face boundary or upper-torso boundary, do not let the screen drift upward, outward, smaller, or to the side in a way that exposes a conventional portrait or fashion subject.

For any screen-replacement portrait or frame-replacement composition, draft an explicit replacement-overlap polygon before describing beauty, cosplay, character, fashion, product, or scenic cues. The polygon should include the containing surface corners, the edge that crosses the real subject, the lower or inner edge that hides visible features when present, and the maximum reveal outside that polygon. Use this polygon to constrain face visibility, hand placement, object scale, and screen/frame scale. If satisfying a prettier or more plausible scene would require moving the replacement surface away from the occluded zone, preserve the overlap and accept the awkward crop.

When an opaque rectangular occluder such as a phone, screen, card, sign, book, mirror panel, sticker, window frame, or foreground prop blocks a face, body, garment, product, or background region and defines the visible concept, prioritize the occluder's image-plane footprint, corners, lower and inner edges, and hidden-feature coverage before face attractiveness, garment readability, object completeness, or portrait symmetry. This is a general source-evidence rule: the occluder footprint outranks beauty, fashion, product clarity, and scene completion when the source visibly depends on that occlusion.

Separate canvas orientation from object orientation. A vertical source image may contain a landscape-oriented phone, screen, frame, card, book, sign, panel, label, package, window, or tabletop object rotated diagonally. For each major rectangular object, identify its own long edge, short edge, corner order, and rotation in the image plane before using labels like portrait, landscape, vertical, or horizontal. If the object's long edge runs lower-left to upper-right or upper-left to lower-right, say that directly and avoid shorthand that could rotate the object upright.

When a screen-contained face, poster face, reflection face, printed face, illustrated insert, UI panel, or framed secondary image supplies only a partial counterpart, describe it as partial content inside its containing surface. Name the visible eye, mouth, hair, highlight, object, text, or crop fragments and the absent counterpart fragments. Do not let the prompt invite a full in-world person, complete object, separate sticker outside the containing surface, or clean second subject unless those are visibly present.

If side, direction, or mirrored/counterpart logic matters, state whether the description uses subject-side or viewer-side perspective and keep that perspective consistent. Do not let the generated result swap which side is visible, duplicate features on both sides, omit required counterpart features, or disconnect matching contours.

If the intended relationship depends on implausibility, uncanniness, low fidelity, mixed rendering styles, a screen-within-screen structure, or scale contrast, preserve that coherence ceiling. Do not turn the relationship into a cleaner, more physically plausible, more realistic, or more unified scene when that would erase the visual premise.

If the image does not contain a special illusion or relationship, do not invent one. In that case, use this section to identify the ordinary main visual premise, such as a specific portrait crop, product arrangement, gesture, environmental mood, or rendering style.

When a background, reflection, poster, screen, printed surface, mirror, window, or other secondary layer contains partial human features, object fragments, text, or environmental details, write the visible fragments as fragments. State which counterpart features are absent, cropped away, obscured, or outside the frame so the generated image does not complete the layer into a fuller scene.

For secondary layers, prevent completion aggressively. A printed, reflected, screen-contained, blurred, or background-only face/object should not gain a complete body, missing eyes, missing limbs, readable full text, extra surroundings, or physical interaction unless those features are visibly present. Put these completion risks into the negative prompt.

For large secondary layers, distinguish dominant visible fragments from tempting but absent counterpart fragments. The prompt should name the 1-3 fragments that visually matter most, their approximate coordinates, and any counterpart details that should stay cropped, hidden, blurred, or absent.

For partial secondary-layer faces, preserve expression evidence conservatively. If mouth openness, teeth, eyes, gaze, or expression are cropped, blurred, ambiguous, or only partly visible, say so and prevent the generator from making them clearer, wider open, more expressive, more centered, or more complete than the source.

When useful, use normalized coordinates for concept-critical relationships: shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.

Appearance, body, clothing, and object fidelity serve the primary visual concept and must not outrank it. When descriptive detail competes with the perceptual relationship that makes the image recognizable, preserve the relationship first.
