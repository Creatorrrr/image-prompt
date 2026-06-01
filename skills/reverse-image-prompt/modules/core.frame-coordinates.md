---
id: core.frame-coordinates
version: 3
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
---

# Core: frame ratio, crop, and coordinates

## When to load

Always.

## Frame ratio audit

- If file dimensions are available, compute the actual width:height relationship before drafting.
- Treat verified file dimensions as invariants. When pixel width, pixel height, and width/height ratio are known, copy those values exactly wherever concrete size or ratio appears in `PROMPT:` or `RECOMMENDED SETTINGS:`. Do not infer, round, substitute a common ratio, use a preview size, or switch to a generator-preferred canvas because it looks close.
- If dimensions are not verified, describe aspect and crop qualitatively or mark numeric values as approximate. Do not invent exact pixel dimensions for an unverified source.
- Keep aspect ratio and output size conceptually separate. Report measured source dimensions as `width x height`, decimal width/height ratio, and nearest plain-language shape.
- Do not normalize to common ratios such as `2:3`, `3:4`, `4:5`, `9:16`, `16:9`, or `1:1` unless the source is actually close.
- If no standard ratio is close, use `source-specific portrait crop`, `source-specific landscape crop`, or `source-specific square-adjacent crop` with the approximate ratio.
- Put measured frame treatment in the first sentence of `PROMPT:` before broad labels such as portrait, product shot, screenshot, or landscape.
- Repeat measured ratio in `RECOMMENDED SETTINGS:` and list nearest standard size only as a fallback.
- Before emitting, scan every size and ratio mention for consistency with verified metadata. Any mismatch is a hard fidelity failure to correct before final output.
- Treat aspect-ratio drift as a major failure because it changes subject scale, edge crops, object placement, and visibility budgets.

## Normalized coordinates

Use coordinates when useful:

- `x=0%` is far left; `x=100%` is far right.
- `y=0%` is top; `y=100%` is bottom.
- Use approximate ranges rather than false precision when uncertain.
- Use coordinates for face center, eye line, head, shoulders, torso, waist, hips, elbows, hands, knees, feet, held objects, important foreground/background objects, horizon, light sources, highlights, shadow boundaries, receiving surfaces, focus zones, blur zones, crop edges, and occluding objects.
- Use coordinates for concept-critical relationships: shared eye lines, centerlines, contour junctions, screen/frame edges, contact points, overlap boundaries, replacement zones, and scale-reference points.

## Coordinate-lock passage

For high-fidelity reconstruction, include a dedicated coordinate-lock passage in `PROMPT:` that covers:

- dominant foreground subject anchors
- important background or secondary-layer anchors
- frame-edge artifacts and crop boundaries
- small text/mark locations
- dominant overlap boundaries and occluder footprints
- edge-adjacent subject visibility budgets, including whether hair/head outline, clothing, props, or background are cropped while important facial features remain inside the frame

Coordinates describe placement and relative dominance, not only object presence.

When a source depends on full-frame scale, describe the visible top/middle/bottom or left/center/right bands and the required negative space/context before salient local details. Explicitly prevent zooming into a high-salience face, hand, hair, prop, garment edge, text mark, UI control, or product detail when that would remove source-visible background, lower-frame, or edge evidence.

For tight portraits, partial faces, selfies, and other edge-adjacent subjects, separate head/hair clipping from facial-feature clipping. If the frame cuts hair, head outline, shoulder, garment, prop, or background while keeping eyes, nose, mouth, cheek, chin, or jawline inside the image, state that distinction directly. Do not let an off-center or edge-biased face become a sliced half-face unless the source actually cuts through facial features. Lock which features are fully visible, which are hidden by hair/hand/shadow/object, and which are outside the frame.

## Consistency audit

Before finalizing, check whether coordinates contradict plain-language placement. If face center, eye line, prop box, hand box, text mark, background seam, or crop coordinates disagree with words such as `centered`, `slightly right`, `lower-left`, `near`, `below`, `wide`, `small`, or `dominant`, revise until both describe the same layout.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy coordinate and frame-ratio audit

4. Use approximate normalized coordinates when useful:
   - `x=0%` is the far left edge; `x=100%` is the far right edge.
   - `y=0%` is the top edge; `y=100%` is the bottom edge.
   - Use coordinates for major anchors such as face center, eye line, head, shoulders, torso, waist, hips, elbows, hands, knees, feet, held objects, important foreground/background objects, horizon line, light sources, highlights, shadow boundaries, receiving surfaces, contact shadows, shadow-hidden contours, focus zones, blur zones, crop edges, and occluding objects.
   - Use coordinates for concept-critical relationships such as shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.
   - For high-fidelity reconstruction, include a dedicated coordinate-lock passage in `PROMPT:` that covers the dominant foreground subject, the most important background or secondary-layer anchors, frame-edge artifacts, crop boundaries, and any small text/mark locations. Coordinates should describe placement and relative dominance, not only object presence.

4a. Audit the source frame ratio before drafting:
   - If image file dimensions are available in the conversation or from local inspection, compute or preserve the actual width:height relationship in plain terms, such as `aspect about 0.69, taller than 3:4 but wider than 9:16`.
   - When a local source file path is available, check the actual pixel dimensions with a local metadata tool before drafting. If the visible frame is meaningfully narrower, taller, squarer, letterboxed, cropped, or otherwise different from a common ratio, do not normalize it to the common ratio.
   - Keep aspect ratio and output size conceptually separate. Report the measured source pixel dimensions as `width x height`, the decimal width/height ratio, and the nearest plain-language shape.
   - Do not substitute common portrait or landscape labels such as `2:3`, `3:4`, `4:5`, `9:16`, `16:9`, or `1:1` unless that label is close to the measured frame. If no common label is close, say `source-specific portrait crop`, `source-specific landscape crop`, or `source-specific square-adjacent crop` and give the source dimensions or approximate aspect.
   - Do not substitute a generator-preferred size, downscaled preview size, reduced fraction, conversation preview, viewer downscale, model output default, or common 1024-based canvas for the source ratio. If the source file is available, file metadata wins over visible preview dimensions.
   - Put the measured frame treatment in the first sentence of `PROMPT:` before broad labels such as beauty portrait, cosplay portrait, editorial portrait, product shot, screenshot, or landscape.
   - Repeat the measured ratio in `RECOMMENDED SETTINGS:` and list the nearest standard size only as a fallback, clearly saying it is a fallback.
   - Treat aspect-ratio drift as a major fidelity failure because it changes subject scale, edge crops, object placement, and visibility budgets.


## Legacy coordinate and boundary output gates

   - For adjacent visual-band compositions, audit normalized vertical and horizontal bands before emitting. Check visible edges such as garment hems, material transitions, exposed or covered gaps, fasteners, prop boundaries, surface lines, horizons, rails, table edges, mirror seams, and crop boundaries. Do not let category labels, pose labels, garment-length labels, crop labels, or body-region labels shift those bands lower, higher, wider, narrower, taller, shorter, cleaner, or more centered than the source. When a broad label conflicts with a coordinate, bounding box, edge-band, or coverage-map lock, omit or weaken the broad label and keep the visible coordinate or band lock.
   - Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever they compete with source-specific visibility budgets. Labels such as `upper-body portrait`, `bare shoulder`, `off-shoulder`, `dress`, `corset`, `camisole`, `beauty portrait`, `product`, `fantasy`, or `character portrait` can pull the generator toward a conventional clean composition. Use them only as secondary shorthand after measured crop, occlusion, darkness, and edge-band locks; omit them if they cause a cleaner, more centered, more complete, or more revealing layout than the source.
   - For coordinate-heavy prompts, audit internal contradictions before emitting. If face center, head mass, eye line, shoulder span, prop box, hand box, text mark, watermark, label, or background seam coordinates disagree with descriptive phrases such as `centered`, `slightly right`, `lower-left`, `near the face`, `below the cheek`, `wide`, `small`, `dominant`, or `secondary`, revise so the coordinates and plain-language placement describe the same image-plane layout. Do not include multiple approximate ratio labels or centerline descriptions that could pull the generator toward a common crop or a more balanced portrait, fashion, or product composition.
   - For tight portraits, audit vertical face placement against frame budget. If the source face sits high, with substantial torso, prop, garment, or background detail below it, say that the face remains high and prevent the head from drifting downward to a balanced head-and-shoulders portrait. If the source face sits low or has unusual headroom, lock that instead. The face vertical anchor should agree with eye line, chin, top-of-head, shoulder, prop, and bottom-crop coordinates.
   - When estimating coordinates, trust the inspected source file and full image over a downscaled preview, crop-transformed viewer, or generator-friendly normalized composition. If coordinates are uncertain, use wider approximate ranges and relative anchors rather than overconfident exact centers that could shift the subject. Avoid letting a single coordinate estimate override the visible balance of face, foreground objects, shoulders, crop boundaries, and background.
   - For screenshots, screen recordings, app captures, camera previews, or social-video frames, audit the exact UI/content split before emitting. If a bottom input band, player control, crop bar, status overlay, or app overlay is present, state its measured y-start, height, opacity, and image-plane role.
   - For screenshot-like sources, explicitly reject common controls that are not visible, such as home indicators, heart/reaction buttons, share buttons, profile avatars, side action stacks, progress bars, captions, top app chrome, branded headers, or enlarged UI controls.
   - Assume downstream image generation may use only the `PROMPT:` body. Any non-negotiable crop, camera, boundary, appearance, garment, occlusion, and medium-fidelity constraints must appear inside `PROMPT:` in affirmative visual language, not only in `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:`.
   - Before finalizing, check whether any secondary prop, garment edge, accessory, text mark, label, watermark, or background object receives more words than its visible importance supports. If a secondary element has become over-described, compress it into one measured sentence plus one drift-prevention sentence. Spend the prompt's detail budget in the same hierarchy as the source image: dominant concept and composition first, primary subject and key occluders next, then secondary marks and background fragments.
   - If the source is a casual, awkward, low-angle, close-camera, screenshot-like, or otherwise non-editorial capture, the opening sentence should lead with frame geometry, camera height/angle, crop, subject scale, and fidelity ceiling before broad fashion, beauty, or genre labels that could normalize the image.
