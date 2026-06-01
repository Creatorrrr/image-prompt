---
id: concept.occlusion-replacement
version: 2
priority: 95
type: concept
tier: 1
facet: relationship
facet_values:
  - occlusion
  - replacement
  - hidden-counterpart
  - foreground-blocking
  - partial-completion
triggers:
  - opaque occluder, replacement surface, hidden features, foreground prop blocking subject
avoid_when:
  - no occlusion or replacement logic
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Concept: occlusion and replacement surfaces

## When to load

Load when an object, hand, phone, screen, sign, book, card, foreground prop, shadow, hair, crop edge, or frame boundary hides a concept-critical area or substitutes for part of another subject.

## Detection cues

- Opaque rectangle or prop crossing a face, torso, product, label, or background.
- Only a sliver of a counterpart feature remains visible.
- A phone/screen/card/frame supplies content that visually replaces hidden features.
- The image would become a different scene if the occluder moved, shrank, rotated, or became transparent.

## Prompt additions

- Describe the occluder before attractiveness, product clarity, garment labels, or scene completion.
- Lock the occluder's image-plane footprint, approximate corners, rotation, border thickness if visible, and overlap boundary.
- State which real-layer features remain visible outside the occluder and which features are hidden by it.
- If a surface replaces hidden content, state what the replacement surface carries and how it lines up with the hidden area.
- State hidden features as absent in the real layer when supported by visible evidence. Do not let them reappear around the edges.
- Use an overlap polygon when needed: containing surface corners, edge crossing the subject, lower/inner edge hiding features, and maximum reveal outside the polygon.
- Preserve awkwardness. If a prettier or more plausible image requires moving the occluder away, keep the occluder and accept the awkward crop.

## Negative additions

Reject moved, smaller, higher, lower, transparent, recentered, or cleaned-up occluders; hidden face/body/product/text features reappearing; full counterpart completion; conventional portrait/product clarity replacing the blocked view; seam mismatch; duplicate features on both sides of the occluder.

## Settings additions

- Occlusion fidelity locks: occluder footprint, corners, rotation, edge crossings, hidden-feature budget.
- Completion/seam continuity locks: which hidden/counterpart features remain absent.
- Boundary and visibility-budget locks: slivers remain slivers; cropped areas stay cropped.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy occlusion, replacement, boundary, and completion rules

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

## Pose, Occlusion, and Clothing

For each visible person, describe precise mechanics rather than only generic pose labels:

- Body crop and visible body parts.
- Head direction, head tilt, chin angle, gaze, neck visibility, shoulder line angle, torso orientation, twist, lean, posture, and spine/action line.
- Shoulder height difference, hip height difference, weight distribution, arm direction, elbow bend, forearm angle, wrist angle, hand placement, finger visibility, object grip, leg placement, knee bend, ankle/foot placement, and negative space.
- Occlusion relationships between limbs, clothing, body, face, objects, cast shadows, self-shadowing, contact shadows, blur, and crop.
- Approximate pose landmark coordinates when helpful.

Describe clothing as it affects visible silhouette:

- Fit, fabric type and thickness, opacity/transparency, stiffness/looseness, fabric tension, wrinkles, folds, neckline depth and width, strap position, sleeve position, seam placement, waist seam, under-bust seam if visible, buttons, lace, pattern scale, garment layers, and interaction with body shape and pose.
- Prefer visible garment geometry over broad fashion-category labels when fidelity matters. If a category label such as dress, crop top, off-shoulder, uniform, robe, jacket, or swimsuit would cause the generator to normalize the garment, describe the exact visible edges, coverage bands, straps, sleeve openings, crop boundaries, fabric opacity, and occlusions first, and use the category label only as secondary shorthand.
- Do not let a broad garment or portrait label dominate the first sentence when the source depends on awkward crop, low camera angle, partial visibility, or non-editorial styling. Put the visible coverage geometry and camera crop first, then use the category label only after those constraints are established.
- Create a coverage map for exposed skin, fabric, and occluded regions when clothing placement is important. State which image regions are skin, which are fabric, which are shadow-hidden, and which must remain outside the crop. Reject expanding exposed skin or completing hidden garment/body regions beyond the source.
- Do not make clothing tighter, looser, more structured, more corseted, more revealing, more transparent, more padded, more lifted, more sculpted, more modest, more fashion-editorial, more lingerie-like, more body-hugging, or more generic than the source.

For close upper-torso crops with scoop necklines, collars, straps, hems, shirt openings, jackets, or layered garment edges, treat the visible edge as a measured boundary band rather than a fashion label. Lock the neckline or garment-edge width, lowest y-position, visible skin or underlayer area above and below it, sleeve or shoulder fabric area, and bottom crop. If the source is covered or only mildly open, avoid words that can deepen the neckline, lower a garment edge, or recenter the torso; phrase the region as an opaque garment boundary, covered torso plane, or interrupted edge band when that is what the source shows. Reject deeper neckline drift, larger exposed skin bands, tighter fabric, added contour emphasis, and any attempt to make the torso a cleaner fashion subject when it is secondary to another visual concept.

When a neckline, collar, or garment opening is dark, shadowed, cropped, low-contrast, or interrupted by hair, prop, jewelry, accessory, hand, or blur, describe it as an interrupted covered band before using any fashion category. Avoid `low neckline`, `off-shoulder`, `camisole`, `dress`, `lingerie`, or similar labels if they would invite a wider, clearer, deeper, or more centered exposed region than the source. The positive prompt should state the visible covered band and occluders, not only negative exclusions.

For chokers, collars, necklaces, straps, lace trim, bows, and shoulder accessories in tight portraits, describe only the visible silhouette and approximate density. If the source accessory is dark, low-contrast, partly hidden by hair, shadow, blur, or foreground objects, do not upgrade it into a crisp ornate necklace, symmetrical pendant system, decorative collar set, or clean fashion accessory. Lock whether the accessory is a narrow band, scalloped edge, bead cluster, dangling center detail, loose tie, or shadowed texture, and preserve its incompleteness and low legibility.

When a foreground object, hair mass, arm, hand, prop, shadow, blur, or crop hides part of a neckline, shirt opening, garment hem, or upper torso, make that occlusion part of the clothing map. State which garment edges are interrupted, softened, shadowed, cropped, or blocked, and prevent the generator from lowering, widening, clarifying, or completing the garment edge in a way that shows a larger uninterrupted skin or fabric area than the source.

For flat graphic accessories, stickers, printed marks, cel-shaded overlays, decals, patches, or stylized props attached to or overlapping a photoreal subject, describe their graphic flatness, simplified shape, outline style, color patches, limited shading, and medium contrast before giving the object category. Prevent the generator from converting them into realistic physical props, botanical objects, jewelry, polished 3D accessories, or clean product graphics unless the source visibly has that material realism.

When a graphic accessory or stylized overlay overlaps a real subject, put its medium constraints in the first mention. Lock the accessory's simplified contour, outline, shape count or part count if visible, color-block treatment, low-realism shading, and exact overlap with the real subject. If related stems, leaves, labels, marks, or secondary shapes share the same graphic treatment, lock them as part of the same flat overlay rather than separate realistic objects.

Preserve occluding elements and their shadows. Do not move hands, phones, arms, hair, bags, props, shadows, blur, another person, clothing folds, or crop edges in a way that reveals more body, hides different areas, or clarifies hidden anatomy. Preserve shadows from clothing folds, hair, arms, hands, props, and background structures as separate visible evidence from the occluding objects that create them.

For crop boundaries, state the visible absence. If hands, feet, waist, hips, lower body, object ends, background details, or text are outside the frame or only barely visible, say so directly and keep them cropped, narrow, or secondary. Do not use wording that would encourage the generator to reveal, center, enlarge, complete, or beautify the missing or partial area.

For every boundary-sensitive crop, include both positive and negative wording: the positive prompt states exactly what remains visible and how much frame area it occupies, while the negative prompt rejects expanded visibility, recentered missing parts, completed limbs, completed bodies, extra exposed bands, extra readable text, and moved occluders.

For partial turned-face portraits, including over-shoulder, mirror, profile-glimpse, reflection, screen, or occluded-face views, distinguish the actual face evidence from a generic clean portrait. State whether the visible face is frontal, strict profile, partial three-quarter, small cheek-and-eye glimpse, mostly hidden by hair/objects/shadow, or only a narrow facial sliver. Lock face size relative to the head, hair, body, frame, or containing surface; visible gaze direction; nose/lip/chin/eye visibility; occlusion; and whether the head turn reads candid, posed, reflected, screened, or interrupted. Reject turning a small obscured glance into a cleaner, larger, more frontal, brighter, or more complete face than the source supports.

For small, partial, or occluded faces in portraits, reflections, screens, mirrors, background layers, or over-shoulder views, create a face exposure budget. State which facial features are visible, hidden, cropped, shadowed, blurred, or obscured; how much frame area the face occupies relative to the head, hair, body, containing surface, or nearby anchors; and which tempting features must remain absent or ambiguous. If the source supports only a small glance or facial fragment, avoid enough feature enumeration to invite a larger clean portrait, clearer far eye, more exposed cheek or jaw, brighter beauty lighting, or a more readable expression than the source supports.

For over-shoulder glances, separate head turn from facial exposure. State whether the viewer sees a cheek-and-nose sliver, a partial three-quarter face, or a nearly frontal face. If the source only shows a small side-leaning glimpse, reject direct eye-contact glamour, a large centered face, two fully clear eyes, fully lit cheeks, and a portrait-style head angle.

For small side-profile or over-shoulder faces, lock the gaze geometry as image-plane evidence. State whether the nose points left or right, how much of each eye is visible, whether the far eye is hidden by hair/shadow/profile angle, and whether the mouth reads as a small side contour. Reject turning this into a clearer direct-gaze portrait even when the source appears to look toward the camera.

If the source face reads closer to a side profile than a portrait glance, lead with the profile evidence before any gaze wording. A tiny visible eye or cheek highlight should not be enough to request direct eye contact. Prefer `small side-profile facial sliver`, `near eye barely readable`, and `gaze ambiguous through shadow` over `looking at camera` when the camera-facing evidence is weak.

For contact gestures where a hand, limb, hair, clothing, tool, prop, or other occluder touches or grips another visible element, describe the contact as a spatial relationship, not just as a generic gesture. Lock approximate size, angle, visible fingers or endpoints, contact point, compression, overlap, hidden portions, loose or displaced material, and where the interacting element begins and ends. If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

When a body area or garment gap is only a thin bottom-edge or side-edge sliver, avoid making it sound like a subject. Prefer wording such as `a narrow edge band/gap remains at the crop boundary`, `a thin skin-toned edge strip`, or `a barely visible cropped gap` over labels such as `visible abdomen`, `visible midriff`, or `visible waist` unless that area is actually central and materially visible. If a prompt uses a body-part label for a sliver, immediately qualify that it is not a subject region and should not expand inward.

If the source garment is cropped near the bottom and a broad clothing category such as `crop top` would invite a fashion-style exposed abdomen composition, describe the visible hem and frame cut first, and use the category label only as secondary shorthand or omit it when the hem/crop is the important evidence. Never let bottom-edge garment wording imply that the lower body should be completed or that a larger skin band should be centered.

For small text marks, logos, labels, signatures, UI text, or incidental lettering, preserve location, size, contrast, and readability level over exact transcription unless the exact readable text is central to the image. If it is small, partial, distorted, or low confidence, describe it as an indistinct mark and prevent the generator from enlarging it or turning it into prominent clean typography.

For watermarks, product labels, package labels, background signs, reflected marks, engraved marks, and decorative monograms in photographic scenes, distinguish text-plane role from exact text content. If the mark is secondary, soft, transparent, curved, reflected, low-resolution, or partially legible, write it as a faint graphic or label artifact with approximate placement and legibility ceiling. Do not over-transcribe low-confidence letters in `PROMPT:` unless exact readability is central; over-transcription often makes generators create a crisp logo, clean sign, or new prominent text object.

For incidental text that is visible but compressed or small, lock it as low-legibility. Do not request crisp typography unless the source clearly centers readable text as the subject.

When incidental UI text is clearly readable despite being small, preserve the exact visible characters and their low-legibility rendering together. Do not let the generator substitute a plausible different time, placeholder, number, brand, or label. Exact text locks should still emphasize small size, soft edges, and secondary priority, not clean typography.

When incidental text is near a garment or object edge, describe it as a small, soft mark anchored to that edge. Avoid repeating the exact text in ways that make the model prioritize clean lettering over edge placement, size, softness, and low contrast.

For incidental interface overlays, screenshot controls, camera controls, reaction marks, low-confidence symbols, small badges, or cropped graphic marks, preserve them as low-legibility artifacts unless their exact symbol is central and clearly readable. Describe approximate shape, size, opacity, edge distance, internal contrast, and ambiguity. If the internal mark is unclear, call it an abstract mark rather than a named icon, arrow, logo, or app control. Reject conversion into clean readable typography, a brand mark, a watermark, a caption, or an enlarged interface element.

For progress lines, scrub bars, separators, or edge slivers, preserve the observed length and discontinuity. If the source shows only a tiny partial line at an edge or a short pale segment, do not describe it as a full progress bar; explicitly reject full-width bars, timeline tracks, knobs, home indicators, or completed app controls unless they are visible.

For ambiguous tiny UI edge marks that are not central to recognition, do not over-promote them in `PROMPT:`. It is safer to say that no full progress bar or timeline is visible than to positively request a mark that may expand into a complete control. Mention the tiny mark only as a cropped edge artifact when it is visually clear and bounded.

For secondary objects such as bags, straps, jewelry, tools, handheld items, furniture fragments, signs, UI controls, props, or cropped products, create a secondary-object budget. Lock edge distance, bounding box, overlap with the primary subject or containing surface, visible crop, occlusion, and relative size against nearby body, object, frame, or background anchors. If the object is secondary or edge-adjacent in the source, describe it as partial, tucked, compressed, low-priority, obscured, or low-detail as supported by evidence; prevent it from becoming larger, cleaner, front-facing, product-like, fully readable, or more central than the source.

Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. In `PROMPT:`, lock each such region as partial or cropped; in `NEGATIVE PROMPT:`, reject completing, recentering, expanding, or clarifying those regions.
