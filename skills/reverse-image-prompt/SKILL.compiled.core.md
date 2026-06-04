---
name: reverse-image-prompt
description: Reverse engineer a faithful standalone English text-to-image prompt from a provided or attached image using a compact core plus routed subject, medium, relationship, and detail-risk modules. Use when the user asks to analyze a reference image, extract or reconstruct an image-generation prompt, create a GPT Image 2 prompt, write a negative prompt, or produce recommended generation settings from visible image evidence.
---

# Reverse Image Prompt

## Purpose

Create a text-only image generation prompt from one provided image. The prompt must stand alone without the original image attached and should maximize reproducibility of the source image's visible composition, subject appearance, pose, crop, camera treatment, lighting, background, color, medium, and artifacts.

Preserve the source image, not a corrected, beautified, safer-looking, more modest, more sexualized, more cinematic, more polished, more generic, or more socially normalized version of it.

This skill is modular. Use this root `SKILL.md` as the mandatory router, then load the relevant `modules/*.md` files after detecting visual facets. Do not treat the image as belonging to exactly one category; combine subject, medium, relationship, capture-quality, and detail-risk facets.

## Required Module Loading

Always apply and read the complete Tier 0 core:

- `modules/core.visual-evidence.md`
- `modules/core.frame-coordinates.md`
- `modules/concept.primary-relationship.md`
- `modules/core.fidelity-discipline.md`
- `modules/core.background-color.md`
- `modules/core.pre-emit-gate.md`
- `modules/core.output-contract.md`

`concept.primary-relationship` is intentionally still named as a concept module for compatibility, but it is Tier 0 and functionally core.

If sibling files are available, you MUST read the exact contents of every selected module file before drafting `PROMPT:`, `NEGATIVE PROMPT:`, or `RECOMMENDED SETTINGS:`. Do not rely on this router summary as a substitute for module contents. If module files cannot be read in the runtime, use `SKILL.compiled.all.md`; profile bundles are optimization aids, not the safest fallback.

## Workflow

1. Inspect only the provided image.
   - If the image is attached in the conversation, visually analyze it directly.
   - If the user provides a local path, use local image inspection when available.
   - If no image is available, ask the user to attach or provide the image.
   - If multiple images are provided and the user asks for one prompt, ask which image to use or process each image independently if the request clearly allows multiple outputs.

2. Do not use external identity or metadata assumptions.
   - Do not identify or name real people, celebrities, copyrighted characters, brands, artists, exact cameras, exact lenses, exact film stocks, or exact private identities.
   - Use only visible evidence.
   - If a detail is ambiguous, write `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, `ambiguous`, `low-confidence`, or `indistinct`.

3. Silently analyze in this order:
   1. Primary visual concept, perceived intent, and perceptual relationships.
   2. Composition, actual source frame ratio, orientation, crop, subject scale, frame placement, spatial layout, and normalized coordinates.
   3. Visible subjects and their image-plane roles.
   4. Pose mechanics, gesture, limb or object placement, negative space, occlusion, completion-prone regions, and crop boundaries.
   5. Camera distance, height, angle, lens impression, perspective distortion, focus, blur, camera shake, and optical behavior.
   6. Lighting direction, atmosphere, color grading, contrast, highlights, shadows, flash behavior, and lighting-to-volume effects.
   7. Background zones, palette, color massing, depth layers, and environmental details.
   8. Medium, texture, grain, noise, compression, imperfections, rendering artifacts, UI overlays, and text marks.

4. Build an internal facet map, resolve modules from `manifest.json` / `modules/_registry.md`, read those module files, then merge their rules using the conflict priority below. Do not print the facet map unless the user asks for diagnostics.

5. Output only the required sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

6. Report prompt-only limits honestly when exact crop, pose, facial appearance, background fragments, UI/text placement, or small low-legibility details are unlikely to be reproduced from text alone.

## Facet Router

`manifest.json` and `modules/_registry.md` are generated from module frontmatter and are the canonical registry. The router uses these tiers:

- Tier 0: always-on core.
- Tier 1: concept and relationship modules. If the relationship is visible, load every applicable concept module, even when several apply.
- Tier 2: subject and medium modules.
- Tier 3: detail-risk modules.
- Tier 4: narrow style modules.

Use this internal facet shape:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object/none
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face, body-silhouette, clothing, hands, text-logo, UI, small props, cropped edges, tight-selfie, face-hand-gesture, accessory-torso-budget
  style: []           # stylized-character-maturity or other narrow style risks
```

Routing rules:

- Always load all Tier 0 modules.
- Always evaluate the relationship facet. Load all detected Tier 1 concept modules; concept-critical relationships outrank subject labels.
- Select at least one medium. If the medium is unclear, load `medium.unspecified-visual`, not `medium.photographic-capture`.
- Select at least one subject decision. If no subject module fits, load `subject.generic-object` to preserve an ordinary object/scene/none decision without inventing a category.
- Apply dependencies from the manifest after initial selection. Examples: `medium.screenshot-ui` pulls `concept.screen-frame-within-frame` and `detail.text-logo-label`; `subject.document-data-diagram` pulls `detail.text-logo-label`.
- Human images with visible hands, clothing geometry, or body-silhouette drift risk should add the corresponding detail-risk modules; do not rely on `subject.human` alone.
- Tight human phone selfies where face/hair dominate should add `tight-selfie`; if face-touching hands or secondary accessories/cropped upper-torso clothing affect fidelity, also add `face-hand-gesture` and/or `accessory-torso-budget`.
- Usually select 3-8 modules beyond the core, but do not omit a concept-critical relationship module to stay under budget.

## Conflict Priority

Resolve conflicts in this order:

1. Safety, visible-evidence limits, and no external identity assumptions.
2. Primary visual concept and perceptual relationship.
3. Actual source frame ratio, crop, normalized coordinates, boundary artifacts, and visibility budgets.
4. Occlusion, reflection, screen/frame, replacement, scale, seam, continuity, and completion logic.
5. Subject-specific fidelity: face, body silhouette, product geometry, animal anatomy, food texture, architecture, landscape, vehicle form, diagram layout.
6. Medium and capture fidelity: camera, focus, lighting, UI overlay, rendering style, compression, noise.
7. Background, palette, color massing, and secondary object budgets.
8. Aesthetic shorthand and generator convenience terms.

Broad labels such as `portrait`, `beauty shot`, `product shot`, `landscape`, `fashion`, `anime`, `cinematic`, `studio`, `luxury`, or `high quality` are allowed only after source-specific crop, relationship, medium, and visibility constraints are established. If a broad label conflicts with coordinates, crop boundaries, occlusion, completion logic, background/color evidence, or source fidelity, weaken or omit the label.

## Output Requirements

Final output must be in English and must include only:

```text
PROMPT:
...

NEGATIVE PROMPT:
...

RECOMMENDED SETTINGS:
...
```

The `PROMPT:` body must carry all non-negotiable constraints in affirmative language. Do not rely on `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:` for essential crop, occlusion, boundary, identity-limitation, face, clothing, object, UI, background/color, or medium constraints.


---

# Compiled module bundle

The following module files were appended for runtimes that cannot read sibling files dynamically.



---

# Included module: `core.visual-evidence`

# Core: visual evidence rules

## When to load

Always.

## Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, age, weight, height, camera metadata, private identity, exact brand, exact artist, exact camera, exact lens, or exact film stock.
- Use visible evidence only. When uncertain, use calibrated uncertainty terms: `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, `ambiguous`, `low-confidence`, or `indistinct`.
- Preserve the source image rather than correcting it. Do not beautify, polish, relight, make safer-looking, make more modest, sexualize, normalize, center, sharpen, or upscale the source unless the user explicitly asks for improvement rather than reverse engineering.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- If the source is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement words such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine`. Use source-faithful relative terms such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.
- Preserve incomplete evidence. If an object, face, body part, text mark, background figure, surface, or environmental element is cropped, hidden, blurred, shadowed, cut off, or partly visible, describe it as incomplete and specify which visible parts remain.
- Treat hard frame boundaries, pillarboxing, letterboxing, dark side strips, vignetting, clipped edges, awkward headroom, and edge falloff as composition facts unless the user asks for cleanup.
- Use a visibility budget for partial regions. If only a narrow strip, partial limb, partial object, tiny label, or edge band is visible, state that it remains narrow, partial, secondary, low-detail, or obscured.
- Cap generated polish to the source. If the source is casual, degraded, compressed, dim, soft, awkwardly framed, or non-editorial, prevent cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished drift.

## Prompt additions

Include source-faithful language for visible imperfections, incomplete details, partial crops, hard boundaries, and fidelity ceiling near the beginning of `PROMPT:` and again in critical fidelity locks when important.

## Negative additions

Reject beautification, added polish, completing cropped elements, identity assumptions, hidden anatomy/object invention, upgraded quality, cleaner relighting, and genre normalization that changes visible evidence.

## Settings additions

- Quality/Fidelity: match the visible source fidelity, including any degradation.
- Most important fidelity locks: source-visible evidence only; no hidden completion.
- Boundary and visibility-budget locks: list partial objects, crop edges, and incomplete evidence.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy purpose and evidence boundary

## Purpose

Create a text-only image generation prompt from one provided image. The prompt must stand alone without the original image attached and should maximize reproducibility of the source image's visible composition, subject appearance, pose, crop, camera treatment, lighting, background, color, medium, and artifacts.

Preserve the source image, not a corrected, beautified, safer-looking, more modest, more sexualized, more cinematic, more polished, more generic, or more socially normalized version of it.

## Workflow

1. Inspect only the provided image.
   - If the image is attached in the conversation, visually analyze it directly.
   - If the user provides a local path, use `view_image` to inspect it.
   - If no image is available, ask the user to attach or provide the image.
   - If multiple images are provided and the user asks for one prompt, ask which image to use or process each image independently if the request clearly allows multiple outputs.

2. Do not use external identity or metadata assumptions.
   - Do not identify or name real people, celebrities, copyrighted characters, brands, artists, exact cameras, exact lenses, exact film stocks, or exact private identities.
   - Do not rely on external knowledge. Use only visible evidence.
   - If a detail is ambiguous, write `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, or `ambiguous`.


## Legacy Visual Evidence Rules

## Visual Evidence Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or any wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, sizes, age, weight, height, camera metadata, or private identity.
- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- Calibrate underexposure instead of maximizing it. When the source has dark clothing, hair, night areas, or shadowed interiors, distinguish fully crushed black regions from low-contrast regions that still show folds, edges, face planes, fabric bands, or object silhouettes. Preserve the amount of remaining shadow detail; do not turn visible dark detail into a featureless black mass.
- When the source image is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement terms such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine` to describe focus, highlights, or recommended quality. Use source-faithful relative terms instead, such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.
- Preserve incomplete evidence. If an object, face, body part, text mark, background figure, surface, or environmental element is cropped, hidden, blurred, shadowed, cut off by frame edges, or only partly visible, describe it as incomplete and specify which visible parts remain. Do not let the prompt invite a complete version of that element.
- Preserve frame-boundary evidence. If the source contains pillarboxing, letterboxing, dark side strips, vignetting, clipped edges, awkward headroom, hard crop boundaries, or edge falloff, treat those as composition facts rather than artifacts to remove.
- For screenshots or screen-recorded social-video frames, treat interface overlays as composition-critical image-plane bands. Lock their exact vertical bands, opacity, corner radius, text size, low-legibility level, and absence/presence of common app controls. State which controls are absent as well as which are present, so the generator does not add hearts, home indicators, action buttons, captions, or clean branded UI that were not visible.
- Preserve overlay restraint. If the source has only a simple status bar, one bottom comment/input field, one crop mark, or one small ambiguous control, do not let the prompt invite a complete modern app interface. Name absent control families in the `PROMPT:` itself when they are likely generator defaults.
- Distinguish transparent overlay icons from app chrome bands. If top status icons float directly over the video/background with no black rectangle behind them, say so explicitly and reject a black top status bar, notch area, or header strip. If the bottom has a dark comment area but no home indicator, reject home indicators even when the generated image is phone-shaped.
- Treat hard frame boundaries and crop exclusions as higher priority than object completion. If satisfying object realism would require revealing cropped areas, completing partial body/object/background regions, removing borders, or expanding the scene, preserve the crop and boundary instead.
- Use a visibility budget for partially visible areas. When only a narrow strip, partial band, partial limb, partial object, or small text mark is visible, state that it remains narrow, partial, secondary, or obscured. Do not reveal more of it, enlarge it, clarify it, or move occluders away unless the source visibly does so.
- Clamp bottom-edge and side-edge partial visibility. If a body region, object, garment, sign, or surface appears only as a thin strip at the frame edge, describe its approximate edge band and explicitly keep it at that edge. Do not let it expand inward, become a full object/body area, or become a new visual center.
- Cap generated polish to the source. When the source is casual, degraded, compressed, dim, soft, or awkwardly framed, the prompt must prevent the output from becoming cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished than the source.
- Preserve awkward capture geometry over attractive pose semantics. If the source is a close, low-angle, cropped, accidental, convention-like, mirror-like, screenshot-like, or casual phone capture, describe that awkwardness as a required fidelity trait and prevent fashion-normalized posture, cleaner posing, centered editorial balance, or full-body/waist-up portrait correction.
- For prompt-only reproduction, repeat the most important frame geometry and crop locks in the `PROMPT:` itself near the beginning and again in the critical fidelity locks. Use affirmative wording such as `the composition remains...`, `the closest plane stays...`, and `the edge band remains...` so the prompt does not rely only on negative exclusions.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal. When a person, product, place, or object has a particular visible mood, styling, attractiveness pattern, roughness, awkwardness, asymmetry, facial softness, makeup level, surface sheen, color cast, or image-era/social-media look, describe that aesthetic calibration and prevent beautification, fashion-editorial upgrading, influencer-like smoothing, glamorization, aging down/up, westernization, or generic model drift.
- For dark, cramped, low-resolution, heavily styled, or socially edited portraits, prevent coordinate precision from becoming permission to rebalance the image. If the source is murky, crowded, shadow-blocked, underexposed, compressed, or visibly stylized, state that the portrait remains visually compressed, dim, low-detail, and source-faithful even when face, prop, garment, or background coordinates are specified. Avoid wording that upgrades the source into a clean centered studio portrait, product portrait, fashion lookbook frame, or polished character reference unless that finish is visibly present.
- When light-created shadows materially affect likeness, composition, occlusion, or surface separation, preserve them instead of brightening, erasing, retouching, or normalizing them. Do not invent contours, body shape, surface detail, or environmental structure hidden by shadow.
- When backlight both hides and reveals the subject, specify which edges and planes remain readable. Do not let `silhouette`, `underexposed`, or `crushed shadows` erase visible face edges, garment fold bands, lace trim, hair outline, object silhouettes, or background detail that the source still shows.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or a deliberately awkward capture, preserve that relationship above realism and plausibility. Do not promote a stylized, composited, inserted, reflected, or screen-contained element into a normal physical object unless it visibly is one.
- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.


---

# Included module: `core.frame-coordinates`

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


---

# Included module: `concept.primary-relationship`

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


---

# Included module: `core.fidelity-discipline`

# Core: fidelity discipline and anti-normalization

## When to load

Always. This module keeps every routed path from becoming cleaner, more generic, more attractive, more plausible, or more category-normalized than the source.

## Rules

- Cap generated polish to the source. If the source is casual, degraded, compressed, dim, soft, awkwardly framed, low-resolution, underexposed, socially edited, or non-editorial, prevent cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished drift.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal or product ideal. Keep roughness, awkwardness, asymmetry, styling, social-media look, visible mood, surface sheen, color cast, retouching level, and medium imperfections when present.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or awkward capture, preserve that relationship above realism and plausibility.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever the label would pull the generator toward a common composition, cleaner styling, expanded crop, completed object, or more attractive category default. Put visible geometry, crop, relationship, medium, and fidelity constraints before shorthand labels.
- Treat source fidelity ceiling as an affirmative requirement: the output should not exceed the visible source in sharpness, cleanliness, glamour, lighting balance, polish, readability, symmetry, or plausibility unless the user explicitly asks for improvement.
- Do not use absolute enhancement terms such as `high quality`, `sharp`, `crisp`, `clean`, `pristine`, `luxury`, `cinematic`, or `studio` unless the source visibly supports them and they do not conflict with crop, lighting, artifacts, or ordinary capture.

## Prompt additions

State the source fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent. Use source-specific counterweights such as `still visibly compressed`, `not upgraded into a studio portrait`, `not cleaned into a product shot`, or `not normalized into a plausible full scene`.

## Negative additions

Reject beautification, over-polish, relighting, sharpening, style upgrade, social-media glamorization, product-shot cleanup, symmetry correction, plausible-scene normalization, expanded crop, and broad-label defaults that contradict visible evidence.

## Settings additions

- Fidelity ceiling locks:
- Anti-polish and anti-normalization locks:
- Broad-label weakening locks:


---

# Included module: `core.background-color`

# Core: background, color, and environment zoning

## When to load

Always. Every image has a background, color structure, or negative-space field that can drift if ignored.

## Rules

- Analyze background zoning as image-plane structure: foreground, midground, background, edge bands, negative space, depth layers, occluded zones, dark masses, bright windows, flat fields, texture bands, and ambiguous low-detail regions.
- Preserve the source background's visual priority. If background elements are dim, cropped, blurred, low-legibility, partly hidden, or secondary, keep them as low-detail background massing rather than turning them into clean readable objects.
- Preserve color mood, palette, color cast, saturation, contrast, shadow color, highlight color, and local color relationships. Do not neutralize a visible cast or push the image toward a postcard, clean-room, catalog, cinematic, or studio palette unless that is visibly present.
- For underexposed, low-contrast, compressed, or hazy backgrounds, distinguish fully crushed regions from regions that still show folds, edges, silhouettes, texture, or environmental hints. Preserve remaining detail without turning dark areas into featureless black or brightly recovered scenery.
- Prevent clean-room drift for products, portraits, screenshots, documents, and ordinary scenes. Do not replace messy, partial, compressed, cropped, or ordinary background zones with a smooth backdrop, empty studio, clean wall, perfect sky, luxury interior, or tidy product surface unless visibly present.
- Treat background zoning as part of crop and coordinate fidelity. Edge bands, side strips, awkward headroom, bottom UI bands, floor/wall seams, horizon placement, poster edges, and environmental slivers must remain in their visible positions when they matter.

## Prompt additions

Describe background zones by position, mass, contrast, legibility, depth, and color behavior before using broad setting labels.

## Negative additions

Reject postcard scenery, clean-room backdrop, studio sweep, tidy catalog surface, brightened recovered background, readable invented signage, removed clutter, added depth, and background elements becoming cleaner or more central than visible.

## Settings additions

- Background zoning locks:
- Palette/color-cast locks:
- Low-legibility background massing locks:


---

# Included module: `core.pre-emit-gate`

# Core: pre-emit fidelity gate

## When to load

Always. Apply this gate immediately before writing the final answer.

## Rules

- Confirm that `PROMPT:` contains the primary visual concept, the relationship/effect reading when present, the source aspect ratio, crop, normalized coordinate locks, boundary locks, occlusion/completion logic, medium fidelity, and all required source-fidelity constraints.
- Identify the highest-salience anchors that a generator is likely to over-enlarge, over-sharpen, beautify, complete, or promote into hero elements. Each such anchor should have a source-scale budget in affirmative prompt language: approximate frame area, edge distance, relative size against nearby anchors, and whether it is primary, co-primary, secondary, cropped, soft, or low-detail.
- For repeated anchors such as faces, hair, hands, garment edges, UI marks, text, logos, straps, bags, small props, background structures, or product details, describe the measured role/footprint before texture. If repeated texture or material adjectives make a secondary/cropped element sound larger, cleaner, more complete, or more editorial than the source, compress the wording before emitting.
- For coordinate-heavy prompts, audit internal contradictions before emitting. If face center, head mass, eye line, shoulder span, prop box, hand box, text mark, watermark, label, or background seam coordinates disagree with descriptive phrases such as `centered`, `slightly right`, `lower-left`, `near the face`, `below the cheek`, `wide`, `small`, `dominant`, or `secondary`, revise so the coordinates and plain-language placement describe the same image-plane layout.
- For every secondary object, background element, UI mark, text mark, cropped garment/body region, prop, strap, reflection, or partial edge band, check whether it receives more words than its visible importance supports. If it does, shrink the wording and explicitly keep it secondary, partial, low-detail, or edge-adjacent.
- Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. Lock each such region as partial or cropped in `PROMPT:` and reject completing, recentering, expanding, or clarifying it in `NEGATIVE PROMPT:`.
- For edge-adjacent or partial faces, check whether the draft confuses hair/head/garment/background crop with facial-feature crop. If the source keeps facial features inside frame, state that affirmatively and reject slicing through eyes, nose, mouth, cheek, chin, or jawline.
- For close portraits with secondary clothing, check whether clothing wording could turn cropped lower-frame bands into a clean fashion, costume, or uniform outfit view. If so, compress clothing into measured partial bands and keep it secondary, cropped, occluded, or low-detail.
- Check for concept omission: if all objects are listed but the intended relationship, occlusion, reflection, screen/frame, scale contrast, mixed-media effect, or ordinary premise is missing, rewrite before emitting.
- Report prompt-only limits honestly when exact crop, pose, facial appearance, background fragments, UI/text placement, or small low-legibility details are unlikely to be reproduced from text alone.
- Assume downstream image generation may use only the `PROMPT:` body. Any non-negotiable crop, camera, boundary, appearance, garment, occlusion, and medium-fidelity constraints must appear inside `PROMPT:` in affirmative visual language, not only in `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:`.

## Prompt additions

Repeat the most important crop, coordinate, occlusion, completion, and concept locks near the beginning and again in critical fidelity locks.

## Negative additions

Reject concept omission, coordinate contradiction, common-crop normalization, expanded secondary details, completed partial regions, and upgraded clarity.

## Settings additions

- Final output gate locks:
- Prompt-only reproduction limits:
- Secondary-detail budget locks:


---

# Included module: `core.output-contract`

# Core: output contract

## When to load

Always. Load this before drafting any final answer.

Write the final answer in English. Output only these sections.

## PROMPT:

Write a polished, detailed standalone image-generation prompt in this order:

1. Overall image type, measured/source-specific aspect ratio, orientation, realism level, medium/rendering type, mood, and the primary visible concept in the first sentence.
2. Concept-critical relationships: elements, roles, construction recipe, alignment, overlap, scale relationship, continuity, replacement, completion/missing-side logic, seam or join geometry, feature-scale matching, interaction, medium contrast, coherence/realism ceiling, and what must remain true.
3. Exact composition, crop, subject size, frame placement, bounding box, and approximate coordinates.
4. Subject face and human appearance fidelity when people are visible.
5. Subject visible body proportions and physique fidelity when people are visible, including safe adult calibration locks only when relevant.
6. Exact pose, body orientation, head angle, gaze, shoulder line, torso lean, arms, elbows, wrists, hands, fingers, object grip, legs, stance, weight distribution, occlusion, negative space, crop boundaries, and pose landmark coordinates.
7. Clothing, accessories, and held objects, including how they reveal, obscure, flatten, soften, follow, compress, stretch over, widen, narrow, or visually define the body or pose.
8. Background by screen zones: left, right, top, bottom, foreground, midground, and background.
9. Lighting, atmosphere, color grading, contrast, highlights, notable shadow placement, falloff, receiving surfaces, visible cast shadows, self-shadowing, contact shadows when relevant, shadow edge quality and density only when they materially affect likeness, composition, or occlusion.
10. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
11. Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-detail areas, and relative focus hierarchy.
12. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible.
13. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
14. Boundary and visibility-budget locks: incomplete features, cropped-away counterpart features, frame-edge artifacts, pillarboxing/letterboxing/vignetting, narrow visible strips, secondary text marks, and occluders that must not move.
15. Coordinate and anchor locks: foreground subject anchors, background/secondary-layer anchors, frame-edge/border thickness and side placement, small text/mark coordinates, and dominant overlap boundaries.
16. Critical fidelity locks: primary visual concept, perceptual relationships, composition, crop, subject scale, face, body proportions when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, UI/text if relevant, and medium/rendering.

## NEGATIVE PROMPT:

Write concise, image-specific exclusions. Include only relevant drift risks:

- primary-concept drift and concept-lock failure modes
- wrong crop, subject scale, placement, headroom, body crop, object placement, or layer order
- cropped/partial features completed into full features
- missing counterpart features invented
- narrow visible bands expanded
- edge artifacts erased
- occluders moved to reveal hidden areas
- wrong background, extra subjects, duplicated objects, over-detailed blurred background, wrong location type
- wrong style or medium drift
- random text, subtitles, captions, logos, UI icons, watermarks, readable brand marks unless truly central and visible
- malformed hands, extra/missing fingers, broken limbs, warped face, impossible clothing folds, fused objects
- face, body, clothing, pose, lighting, camera/focus, and medium-specific drift only when those categories are present

## RECOMMENDED SETTINGS:

Fill every field with source-specific values:

- Aspect ratio:
- Size:
- Source frame treatment:
- Quality/Fidelity:
- Style/rendering target:
- Camera/film/rendering target:
- Lighting/rendering target:
- Primary visual concept locks:
- Perceptual relationship locks:
- Completion/seam continuity locks:
- Scale/interaction anchor locks:
- Coherence/realism ceiling locks:
- Most important fidelity locks:
- Face fidelity locks:
- Aesthetic and non-identifying appearance locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Boundary and visibility-budget locks:
- Coordinate and anchor locks:
- Lighting-to-volume fidelity locks:
- Pose fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
- UI/text/label locks when relevant:
- Category-specific locks:

## Output gate

Before emitting, re-read `PROMPT:` as if the original image is gone. If it would recreate only the object inventory, not the relationship, crop, boundary, medium, and fidelity ceiling, revise. Any non-negotiable rule must appear in `PROMPT:` itself in affirmative language.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy output gates and required output policy

6. Output gate before finalizing:
   - Re-read the drafted `PROMPT:` as if the image is no longer available. If the text would recreate only the object inventory, but not the relationship/effect, revise it before emitting.
   - If any Concept Spec item is missing from `PROMPT:` section 2 or the settings locks, revise before emitting.
   - For portraits, compare the drafted face and aesthetic description against the source. If it could generate a more symmetrical, cleaner, more glamorous, more influencer-like, brighter, or more idealized face than the source, add source-specific counterweights before emitting.
   - For clothing, compare the drafted garment description against the source geometry. If a broad garment label could reveal more skin, smooth awkward coverage, recenter the outfit, or turn it into a cleaner fashion garment, revise toward explicit visible edges and coverage maps.
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

7. Write only the required output sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

8. Do not compress or summarize the output contract.
   - The `PROMPT:` section must include the full ordered fidelity coverage, not a short caption plus a few locks.
   - The `RECOMMENDED SETTINGS:` section must preserve the field labels listed in this skill. Do not collapse them into a paragraph or omit fields because they seem redundant.
   - If a source contains people, partial elements, occlusion, frame-edge artifacts, degraded fidelity, or mixed media, those facts must appear in `PROMPT:`, drift prevention in `NEGATIVE PROMPT:`, and explicit locks in `RECOMMENDED SETTINGS:`.

9. Report prompt-only limits honestly.
   - If prompt-only reproduction appears intrinsically capped below a requested similarity threshold, keep improving the prompt extraction skill, but state the cap clearly.
   - Recommend reference-conditioned generation, image editing, control/seed support, or a tool with image-fidelity controls when exact crop, pose, appearance aesthetics, and background fragment placement cannot be achieved reliably from text alone.

Do not include hidden analysis, checklist text, caveats, explanations, or references to the source image still being attached.


## Legacy Output Contract

## Output Contract

Write the final answer in English and output only these sections.

### PROMPT:

Write a polished, detailed standalone image-generation prompt in this order:

1. Overall image type, aspect ratio, orientation, realism level, medium/rendering type, mood, and the primary visible concept in the first sentence.
2. Concept-critical relationships: which elements create the main visual idea, their roles, construction recipe, alignment, overlap, scale relationship, continuity, replacement, completion/missing-side logic, seam or join geometry, feature-scale matching, interaction, medium contrast, coherence or realism ceiling, and what must remain true for the image to read correctly.
3. Exact composition, crop, subject size, frame placement, bounding box, and approximate coordinates.
4. Subject face and human appearance fidelity when people are visible.
5. Subject visible body proportions and physique fidelity when people are visible, including adult calibration locks when relevant and safe.
6. Exact pose, body orientation, head angle, gaze, shoulder line, torso lean, arms, elbows, wrists, hands, fingers, object grip, legs, stance, weight distribution, occlusion, negative space, crop boundaries, and pose landmark coordinates.
7. Clothing, accessories, and held objects, including how they reveal, obscure, flatten, soften, follow, compress, stretch over, widen, narrow, or visually define the body or pose.
8. Background by screen zones: left, right, top, bottom, foreground, midground, and background.
9. Lighting, atmosphere, color grading, contrast, highlights, notable shadow placement, falloff, receiving surfaces, visible cast shadows, self-shadowing, contact shadows when relevant, shadow edge quality and density only when they materially affect likeness, composition, or occlusion, flash behavior if present, and how shadows affect visible edges, separation, occlusion, and lighting-to-volume effects without inferring new structure.
10. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
11. Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-detail areas, and which planes are relatively most in focus or blurred.
12. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible, and whether blur should be preserved or avoided.
13. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
14. Boundary and visibility-budget locks: incomplete features, cropped-away counterpart features, frame-edge artifacts, pillarboxing/letterboxing/vignetting when visible, narrow visible strips, secondary text marks, and occluders that must not move to reveal more detail.
15. Coordinate and anchor locks: foreground subject anchors, background/secondary-layer anchors, frame-edge/border thickness and side placement when visible, small text/mark coordinates, and dominant overlap boundaries.
16. Critical fidelity locks: primary visual concept, perceptual relationships, composition, crop, subject scale, face, calibrated body proportions when relevant, adult chest/upper-torso/waist/hip silhouette when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, and medium/rendering.

### NEGATIVE PROMPT:

Write concise, image-specific exclusions tailored to the actual image. Include only relevant drift risks, covering:

- Primary-concept drift and concept-lock failure modes: all objects present but their visual relationship is wrong, concept-critical object treated as a generic prop, intended effect collapsed into separate unrelated objects, replacement/continuation/scale/interactions broken, fused surfaces rendered as separate stacked objects, completion seam misaligned, counterpart or missing-side logic swapped, duplicated, or omitted, feature proportions mismatched across a join, frame-within-frame lost, mixed-media contrast lost, intended implausibility or uncanniness normalized into a plausible realistic scene, stylized/composited/screen-contained element promoted into a normal physical object, ordinary scene replacing the intended visual premise, or a visually separate collage replacing a single integrated illusion.
- Wrong crop, subject scale, placement, headroom, body crop, object placement, or foreground/midground/background order.
- Crop-boundary drift: cropped or partial features completed into full features, missing counterpart features invented, narrow visible bands expanded, edge artifacts removed, pillarboxing/letterboxing/vignetting erased, or occluders moved to reveal hidden areas.
- Wrong background, extra people, extra objects, duplicated objects, over-detailed blurred background, or wrong location type.
- Wrong style or medium drift: cartoon, anime, illustration, 3D render, painting, sketch, vector art, glossy commercial look, fake cinematic look, fake vintage look when absent, overprocessed HDR, plastic skin, excessive retouching, AI-smoothed face or body.
- Text, watermark, logos, UI icons, subtitles, captions, random letters, readable brand marks unless truly central and generic.
- Distorted hands, extra fingers, missing fingers, malformed grip, broken limbs, warped face, mismatched eyes, duplicated people, fused objects, impossible clothing folds, impossible anatomy.
- For portraits: wrong apparent ancestry/race-coded appearance, skin tone, face shape, eyelid structure, eye spacing, nose bridge/width/length, lip fullness, jawline, chin, cheekbones, age range, hair texture, hairline, facial texture, makeup level, face-defining light/shadow, and non-identifying facial anchors.
- Aesthetic drift: beautified face, influencer face, fashion-editorial styling, glamour retouching, changed expression mood, changed gaze intensity, changed skin sheen, changed makeup level, more symmetrical or model-like features, more polished styling, or sanitized social-media look when the source is rougher, softer, dimmer, more ordinary, more awkward, or differently styled.
- For visible adult bodies: different body type, shoulder width, upper-torso/chest/bust silhouette, waist position/taper, hip width, torso-to-leg ratio, limb thickness, clothing-shaped silhouette, hidden anatomy invention, body-feature erasure, body-feature exaggeration, lighting-caused volume drift, occlusion drift, and camera/lens distortion drift.
- If a visible adult chest/bust/upper-torso silhouette is large or very large, prevent it from becoming moderate, average, small, flat, athletic, narrower, less projected, less rounded, less dominant, more generic, hidden by excessive shadow, flattened by frontal light, or reduced by modesty/anti-sexualization defaults.
- If it is moderate, moderate-to-full, partial, secondary, softened, low-detail, or obscured, prevent it from becoming large, very large, more projected, more rounded, more exposed, more centered, more lifted, more sculpted, more visible, more dominant, more tightly clothed, more cleavage-emphasized, more sharply shadowed, more strongly highlighted, or exaggerated by prompt overcorrection.
- Occlusion drift: phones, hands, arms, hair, clothing, bags, props, shadows, blur, another person, or crop edges moving in a way that reveals more body, hides different body areas, removes partial coverage, or clarifies hidden anatomy.
- Clothing drift: wrong neckline depth/width, strap placement, sleeve placement, seam placement, fabric tightness/looseness/thickness, folds, opacity, transparency, lace, buttons, corset-like structure when absent, lingerie-like structure when absent, tighter/looser/more revealing/more modest clothing, or changed silhouette.
- Lighting drift: wrong light direction, highlight placement, shadow falloff, exposure, contrast, black-level handling, bloom, dark-fabric absorption, rim light, frontal flattening, contour lighting, missing cast shadows, wrong contact shadows, removed self-shadowing, shadow direction mismatch, shadow caster/receiver mismatch, over-brightened shadow areas, shadow-hidden contours becoming invented detail, haze-softened contours becoming sharp, low-contrast contours becoming high-contrast, or lighting that changes visible proportions.
- Pose drift: mirrored pose, changed head tilt/gaze/shoulder angle/torso lean/arm placement/elbow bend/hand position/finger pose/leg stance/weight distribution/crop, added or removed hands, generic standing/seated/fashion/action pose, or changed occlusion.
- Camera/focus drift: wrong camera distance/height/angle/lens perspective/focus target/depth of field, background too sharp, foreground too sharp, missed focus becoming perfect, soft photo becoming overly sharp, sharp photo becoming blurry, added or removed camera shake, wrong blur direction, wrong grain/sharpening/flash/color cast/camera type/dynamic range/highlight rolloff, or polished studio quality when the source is casual or imperfect.

### RECOMMENDED SETTINGS:

Fill every field with source-specific values:

- Aspect ratio:
- Size:
- Source frame treatment:
- Quality/Fidelity: match the source fidelity; if the source is degraded, soft, compressed, noisy, hazy, or underexposed, state that directly and do not default to high quality.
- Style/rendering target:
- Camera/film/rendering target:
- Lighting/rendering target:
- Primary visual concept locks:
- Perceptual relationship locks:
- Completion/seam continuity locks:
- Scale/interaction anchor locks:
- Coherence/realism ceiling locks:
- Most important fidelity locks:
- Face fidelity locks:
- Aesthetic and non-identifying appearance locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Boundary and visibility-budget locks:
- Coordinate and anchor locks:
- Lighting-to-volume fidelity locks: include source-specific light direction plus only source-specific shadow details that materially affect likeness, composition, occlusion, or surface separation; avoid over-specifying minor shadows or inferring hidden structure from shadowed areas.
- Pose fidelity locks:
- Focus and depth-of-field locks: describe the relative focus hierarchy rather than absolute sharpness; for degraded sources, use phrasing like `eyes and face are the least soft area, still low-resolution and compression-softened`.
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
