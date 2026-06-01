---
id: concept.primary-relationship
version: 2
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
---

# Concept: primary visual concept and perceptual relationship

## When to load

Always. Use this module more heavily when the image contains an illusion, overlap, occlusion, scale contrast, reflection, frame-within-frame, replacement surface, inserted media, or mixed-media relationship.

## Core principle

Identify what the image is arranged to make a viewer perceive before listing objects. An object inventory is not enough. If all objects are present but the intended relationship is absent, the reconstruction has failed.

## Analysis recipe

Internally form:

1. A literal object-level reading.
2. A relationship/effect-level reading when visible cues support one.
3. The dominant reading.
4. The visible cues that force it: alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, foreground/background ordering, occlusion, replacement, reflection, screen-within-screen, mixed media, or scale contrast.

If the image is ordinary, do not invent a special relationship. Use a one-line ordinary premise such as a portrait crop, product arrangement, gesture, environmental mood, or rendering style.

## Concept Spec for special relationships

When special relationship evidence exists, build an internal Concept Spec:

- relationship type
- contributing surfaces/elements and their visual roles
- join geometry, seam, overlap, or contact point
- completion/missing-side logic
- feature-scale matching
- foreground/background ordering
- coherence or realism ceiling
- top 1-3 failure modes

Use visual-role words: replacement surface, continuation plane, occluder, scale anchor, foreground interaction target, UI frame, reflection, inserted image, stylized overlay, physical prop, medium-contrast anchor.

## Prompt additions

In `PROMPT:` section 2, write the construction recipe for the relationship, not a prop list. State what each element contributes, how the overlap or seam works, what must stay hidden or incomplete, and what would break the perceptual effect.

## Negative additions

Start the negative prompt with concept failure modes: all objects present but relationship wrong; concept-critical object treated as generic prop; intended effect collapsed into unrelated objects; seam misaligned; counterpart logic swapped; frame-within-frame lost; mixed-media contrast lost; intended implausibility normalized.

## Settings additions

- Primary visual concept locks:
- Perceptual relationship locks:
- Completion/seam continuity locks:
- Scale/interaction anchor locks:
- Coherence/realism ceiling locks:

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy analysis order and concept lock workflow

3. Silently analyze in this priority order:
   1. Primary visual concept, perceived intent, and perceptual relationships: separately from any object inventory, identify what the image is arranged to make a viewer perceive. Form at least one literal object-level reading and, when visible relationships support it, one relationship/effect-level reading. Decide which reading is dominant and name the visible cues that force it, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, foreground/background ordering, occlusion, replacement, reflection, screen-within-screen, mixed media, or scale contrast. If the relationship/effect reading is dominant, every object is subordinate to it and should be described by visual role, not only by category.
   2. Composition, aspect ratio, orientation, crop, subject scale, frame placement, and spatial layout.
   3. Human appearance fidelity when people are visible: face, skin tone, broad apparent visual ancestry or race-coded appearance when visually evident, hair, visible body proportions, clothing-shaped silhouette, pose, and occlusion.
   4. Pose mechanics, gesture, limb placement, hand placement, negative space, and crop boundaries.
   5. Camera distance, height, angle, lens impression, perspective distortion, focus target, depth of field, focus clarity, blur, camera shake, and optical behavior.
   6. Lighting direction, atmosphere, color grading, contrast, highlights, visible shadows when relevant, shadow falloff, flash behavior, and lighting-to-volume effects.
   7. Background zoning, objects, depth layers, and environmental details.
   8. Medium, texture, grain, noise, compression, imperfections, and processing artifacts.

5. Before writing any output, lock the concept:
   - Commit to the dominant reading in one internal sentence of perceived intent.
   - Identify at least one literal object-level reading and one relationship/effect-level reading when the image contains overlaps, occlusion, scale contrast, framing, insertion, replacement, reflection, screen-within-screen, or mixed media.
   - Name the visible cues that make the dominant reading work, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, or foreground/background ordering.
   - If the image contains an integrated illusion, replacement surface, reflection, screen- or frame-within-frame structure, mixed-media composite, scale-contrast interaction, subject/object completion, or any case where separate elements must read as one effect, build an internal Concept Spec. If the image is ordinary, do not invent a special relationship; use a one-line ordinary premise.
   - In the Concept Spec, name the relationship type, contributing surfaces/elements and their visual roles, join geometry, completion/missing-side logic, coherence or realism ceiling, and the top 1-3 failure modes.
   - Completion/missing-side logic must state what visible features each surface carries, what hidden or counterpart features another surface supplies, whether side references use subject-side or viewer-side perspective when that could be confused, and which shared lines, contours, proportions, or contact points must match.
   - Coherence or realism ceiling must state whether the effect depends on implausibility, uncanniness, mixed-media contrast, low fidelity, or scale incongruity, so the scene is not normalized into a more plausible physical setup.
   - Treat Concept Spec items as required content for `PROMPT:` section 2 and the relevant `RECOMMENDED SETTINGS:` locks. Treat failure modes as the first inputs to the negative prompt.


## Legacy Primary Visual Concept and Perceptual Relationship Fidelity

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
