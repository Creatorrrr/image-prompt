---
id: detail.pose-hands-gesture
version: 3
priority: 78
type: detail
tier: 3
facet: detail-risk
facet_values:
  - hands
  - pose
  - gesture
  - grip
  - contact
  - limb-mechanics
  - negative-space
triggers:
  - sensitive visible pose, hands, grip, limb mechanics, contact gesture
avoid_when:
  - hands/gesture/pose mechanics are not important or not visible
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors: []
---

# Detail: pose, hands, gesture, and contact

## When to load

Load when pose mechanics, hands, fingers, object grip, contact, limb placement, or crop-sensitive body orientation can drift.

## Prompt additions

Describe mechanics rather than generic pose labels:

- body crop and visible body parts
- head direction, head tilt, chin angle, gaze, neck visibility
- shoulder line angle, torso orientation, twist, lean, posture, spine/action line
- shoulder/hip height difference, weight distribution
- arm direction, elbow bend, forearm angle, wrist angle
- hand placement, finger visibility, object grip, contact point
- leg placement, knee bend, ankle/foot placement if visible
- negative space and crop boundaries
- approximate pose landmark coordinates when helpful

For side/back, over-shoulder, profile-glimpse, or partly turned human poses, preserve asymmetry separately from category labels. State which side profile, shoulder edge, torso twist, cropped limb, visible side/back/front plane, and hidden planes are present. Avoid summarizing as `back view`, `rear view`, `over shoulder`, or a generic fashion pose if that would square the body to camera, lose the visible face/profile evidence, or complete hidden regions.

For contact gestures, describe the contact as a spatial relationship:

- approximate size and angle of each contacting part
- visible fingers or endpoints
- contact point and compression
- overlap and hidden portions
- where the interacting element begins and ends
- whether there is pinch gap, pulling tension, weight, pressure, support, or only passive touch

If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

## Negative additions

Reject mirrored pose, changed head tilt/gaze/shoulder angle/torso lean, altered arm/elbow/wrist/hand/finger positions, added or removed hands, extra/missing fingers, malformed grip, generic fashion/action pose, contact point moved, pinching/pulling/holding invented, longer limbs or props, and occlusion changes that reveal hidden areas.

## Settings additions

- Pose fidelity locks:
- Scale/interaction anchor locks:
- Coordinate and anchor locks:

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy Pose, Occlusion, and Clothing

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
