---
name: reverse-image-prompt
description: Reverse engineer a faithful standalone English text-to-image prompt from a provided or attached image. Use when the user asks to analyze a reference image, extract or reconstruct an image-generation prompt, create a GPT Image 2 prompt, write a negative prompt, or produce recommended generation settings from visible image evidence.
---

# Reverse Image Prompt

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

3. Silently analyze in this priority order:
   1. Primary visual concept, perceived intent, and perceptual relationships: separately from any object inventory, identify what the image is arranged to make a viewer perceive. Form at least one literal object-level reading and, when visible relationships support it, one relationship/effect-level reading. Decide which reading is dominant and name the visible cues that force it, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, foreground/background ordering, occlusion, replacement, reflection, screen-within-screen, mixed media, or scale contrast. If the relationship/effect reading is dominant, every object is subordinate to it and should be described by visual role, not only by category.
   2. Composition, aspect ratio, orientation, crop, subject scale, frame placement, and spatial layout.
   3. Human appearance fidelity when people are visible: face, skin tone, broad apparent visual ancestry or race-coded appearance when visually evident, hair, visible body proportions, clothing-shaped silhouette, pose, and occlusion.
   4. Pose mechanics, gesture, limb placement, hand placement, negative space, and crop boundaries.
   5. Camera distance, height, angle, lens impression, perspective distortion, focus target, depth of field, sharpness, blur, camera shake, and optical behavior.
   6. Lighting direction, atmosphere, color grading, contrast, highlights, cast shadows, self-shadowing, contact shadows, occlusion shadows, shadow edge quality, shadow density, shadow direction, flash behavior, and lighting-to-volume effects.
   7. Background zoning, objects, depth layers, and environmental details.
   8. Medium, texture, grain, noise, compression, imperfections, and processing artifacts.

4. Use approximate normalized coordinates when useful:
   - `x=0%` is the far left edge; `x=100%` is the far right edge.
   - `y=0%` is the top edge; `y=100%` is the bottom edge.
   - Use coordinates for major anchors such as face center, eye line, head, shoulders, torso, waist, hips, elbows, hands, knees, feet, held objects, important foreground/background objects, horizon line, light sources, highlights, shadow boundaries, receiving surfaces, contact shadows, shadow-hidden contours, focus zones, blur zones, crop edges, and occluding objects.
   - Use coordinates for concept-critical relationships such as shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.

5. Before writing any output, lock the concept:
   - Commit to the dominant reading in one internal sentence of perceived intent.
   - Identify at least one literal object-level reading and one relationship/effect-level reading when the image contains overlaps, occlusion, scale contrast, framing, insertion, replacement, reflection, screen-within-screen, or mixed media.
   - Name the visible cues that make the dominant reading work, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, or foreground/background ordering.
   - If the image contains an integrated illusion, replacement surface, reflection, screen- or frame-within-frame structure, mixed-media composite, scale-contrast interaction, subject/object completion, or any case where separate elements must read as one effect, build an internal Concept Spec. If the image is ordinary, do not invent a special relationship; use a one-line ordinary premise.
   - In the Concept Spec, name the relationship type, contributing surfaces/elements and their visual roles, join geometry, completion/missing-side logic, coherence or realism ceiling, and the top 1-3 failure modes.
   - Completion/missing-side logic must state what visible features each surface carries, what hidden or counterpart features another surface supplies, whether side references use subject-side or viewer-side perspective when that could be confused, and which shared lines, contours, proportions, or contact points must match.
   - Coherence or realism ceiling must state whether the effect depends on implausibility, uncanniness, mixed-media contrast, low fidelity, or scale incongruity, so the scene is not normalized into a more plausible physical setup.
   - Treat Concept Spec items as required content for `PROMPT:` section 2 and the relevant `RECOMMENDED SETTINGS:` locks. Treat failure modes as the first inputs to the negative prompt.

6. Output gate before finalizing:
   - Re-read the drafted `PROMPT:` as if the image is no longer available. If the text would recreate only the object inventory, but not the relationship/effect, revise it before emitting.
   - If any Concept Spec item is missing from `PROMPT:` section 2 or the settings locks, revise before emitting.

7. Write only the required output sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

Do not include hidden analysis, checklist text, caveats, explanations, or references to the source image still being attached.

## Visual Evidence Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or any wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, sizes, age, weight, height, camera metadata, or private identity.
- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- Preserve light-created shadows instead of brightening, erasing, retouching, or normalizing them. Do not invent contours, body shape, surface detail, or environmental structure hidden by shadow.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or a deliberately awkward capture, preserve that relationship above realism and plausibility. Do not promote a stylized, composited, inserted, reflected, or screen-contained element into a normal physical object unless it visibly is one.
- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.

## Primary Visual Concept and Perceptual Relationship Fidelity

Before listing visible objects, identify the primary visible concept that makes the image recognizable. Treat this as the highest-priority fidelity target. The primary concept may be an illusion, a mixed-media relationship, a frame-within-frame structure, a scale contrast, an interaction, a deliberately imperfect capture mode, or another visible relationship between elements.

Separate intent from inventory: an inventory lists what objects are present, while intent states what those objects are arranged to make the viewer perceive. When the two diverge, intent governs. Never let a complete object inventory substitute for the perceptual relationship; an image where every object is named but the intended relationship is absent has failed, even if no object is missing.

Describe each concept-critical element by its visual role, not only by its object category. Examples of roles include replacement surface, continuation plane, occluder, scale anchor, foreground interaction target, UI frame, reflection, inserted image, stylized overlay, physical prop, or medium-contrast anchor.

If two visible elements are meant to read as one continuous subject, preserve the alignment, scale, contour continuation, crop boundary, and feature proportions that create that perception. If one visible element replaces part of another subject, describe exactly which part is replaced, how the replacement aligns, and what would break the illusion.

When a replacement, reflection, screen, frame, overlay, occluder, or continuation plane completes another element, write it as a construction recipe rather than a prop list. State what content each surface carries, what hidden or counterpart features the completing surface supplies, and how the union avoids duplicated or missing features across the seam. Preserve shared eye lines, centerlines, contact points, contour junctions, feature scale, crop boundaries, and medium contrast that make the surfaces fuse or interact.

If side, direction, or mirrored/counterpart logic matters, state whether the description uses subject-side or viewer-side perspective and keep that perspective consistent. Do not let the generated result swap which side is visible, duplicate features on both sides, omit required counterpart features, or disconnect matching contours.

If the intended relationship depends on implausibility, uncanniness, low fidelity, mixed rendering styles, a screen-within-screen structure, or scale contrast, preserve that coherence ceiling. Do not turn the relationship into a cleaner, more physically plausible, more realistic, or more unified scene when that would erase the visual premise.

If the image does not contain a special illusion or relationship, do not invent one. In that case, use this section to identify the ordinary main visual premise, such as a specific portrait crop, product arrangement, gesture, environmental mood, or rendering style.

When useful, use normalized coordinates for concept-critical relationships: shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.

Appearance, body, clothing, and object fidelity serve the primary visual concept and must not outrank it. When descriptive detail competes with the perceptual relationship that makes the image recognizable, preserve the relationship first.

## Human Subject Fidelity

When people are visible, describe a fictional person with similar visible non-identifying appearance. Include:

- Apparent age range, gender presentation if visually relevant, and broad apparent visual ancestry or race-coded appearance only when visually evident and useful for preventing drift.
- Skin tone depth and undertone; pores, shine, matte texture, freckles, moles, blemishes, redness, under-eye shadows, scars, wrinkles, facial hair, makeup level, and other visible non-identifying anchors.
- Face shape and silhouette; forehead, hairline, cheeks, cheekbones, jaw width, jaw softness or sharpness, chin size and shape.
- Eye size, spacing, shape, eyelid structure, eyelid fold visibility, brow shape/thickness/arch, catchlights, and gaze direction.
- Nose bridge, width, length, tip shape, nostril visibility, and frontal/profile/three-quarter impression.
- Mouth width, upper/lower lip fullness, cupid's bow, teeth visibility, parted or closed lips, and smile/tension.
- Ears, neck, visible asymmetry, dimples, facial marks, and other visible anchors.
- Hair color, texture, density, length, parting, bangs, flyaways, volume, curl/wave pattern, and how hair frames or occludes the face.

Prevent the generated person from drifting into a different face type, skin tone, apparent ancestry, age range, eyelid structure, nose structure, jawline, chin, lip fullness, hair texture, hairline, makeup level, facial texture, or a more generic model-like, influencer-like, symmetrical, westernized, airbrushed, stylized, sanitized, or differently lit face.

## Body Proportion and Clothing-Silhouette Fidelity

For every visible person, describe only visible image-plane proportions shaped by clothing, pose, crop, lens, focus, blur, lighting, shadow, and occlusion. Do not infer hidden anatomy under clothing, props, hands, arms, hair, shadow, blur, or crop.

If the subject is not clearly adult or age is ambiguous:

- Use neutral non-sexual clothing, posture, and upper-torso silhouette language only.
- Do not emphasize chest, bust, cleavage, hips, or other sexualized body traits.

For clearly adult subjects:

- Treat visible body proportions as ordinary visual facts.
- Describe relevant visible build, shoulder width, ribcage or upper-torso width, calibrated chest/bust/upper-torso silhouette, waist position and taper, abdomen or midsection if visible, hip width if visible, torso-to-leg ratio, limb scale, and clothing-shaped silhouette.
- Use the weakest accurate calibration supported by the image: `hidden or not visible`, `visible but mostly obscured`, `slight`, `moderate`, `moderate-to-full`, `full`, `large`, `very large`, `broad but low-detail`, `visually dominant because of crop/camera/pose/lighting/clothing`, or `visually secondary despite being visible`.
- State whether visible volume is silhouette-defined, clothing-shaped, shadow-defined, self-shadowed, cast-shadow-obscured, contact-shadowed, highlight-defined, rim-defined, flat-lit, backlit, underexposed, overexposed, dark-fabric-obscured, bright-fabric-softened, haze-softened, low-contrast, low-detail, or partially obscured.

Use symmetric calibration locks:

- If a visible adult body feature is large or very large, preserve it against reduction, flattening, averaging, hiding, or modesty/safety correction.
- If it is moderate, moderate-to-full, slight, flat, broad, secondary, softened, low-detail, or obscured, preserve that calibration against enlargement, extra projection, deeper neckline, tighter clothing, added cleavage shadows, added under-bust shadows, stronger highlights, sharper contouring, or increased dominance.
- If hands, phone, arms, hair, fabric, props, another person, cast shadow, self-shadowing, contact shadow, blur, crop, or frame edge partially hide contours, preserve that occlusion instead of revealing or clarifying hidden shape.
- If a feature is visible but not central, describe it as visible but secondary, not as dominant.
- If a feature is visually dominant because of crop, camera angle, lens, pose, lighting, or clothing, state the visible cause rather than inventing hidden anatomy.

Avoid repetition that over-weights body features. Mention a body feature in the body-proportion section, and repeat it in locks or negative prompt only when it is genuinely important to fidelity.

## Pose, Occlusion, and Clothing

For each visible person, describe precise mechanics rather than only generic pose labels:

- Body crop and visible body parts.
- Head direction, head tilt, chin angle, gaze, neck visibility, shoulder line angle, torso orientation, twist, lean, posture, and spine/action line.
- Shoulder height difference, hip height difference, weight distribution, arm direction, elbow bend, forearm angle, wrist angle, hand placement, finger visibility, object grip, leg placement, knee bend, ankle/foot placement, and negative space.
- Occlusion relationships between limbs, clothing, body, face, objects, cast shadows, self-shadowing, contact shadows, blur, and crop.
- Approximate pose landmark coordinates when helpful.

Describe clothing as it affects visible silhouette:

- Fit, fabric type and thickness, opacity/transparency, stiffness/looseness, fabric tension, wrinkles, folds, neckline depth and width, strap position, sleeve position, seam placement, waist seam, under-bust seam if visible, buttons, lace, pattern scale, garment layers, and interaction with body shape and pose.
- Do not make clothing tighter, looser, more structured, more corseted, more revealing, more transparent, more padded, more lifted, more sculpted, more modest, more fashion-editorial, more lingerie-like, more body-hugging, or more generic than the source.

Preserve occluding elements and their shadows. Do not move hands, phones, arms, hair, bags, props, shadows, blur, another person, clothing folds, or crop edges in a way that reveals more body, hides different areas, or clarifies hidden anatomy. Preserve shadows from clothing folds, hair, arms, hands, props, and background structures as separate visible evidence from the occluding objects that create them.

## Camera, Focus, Lighting, and Medium

For photographic images, describe how the camera captured the scene:

- Camera distance, camera height, camera angle/rotation, lens impression, perspective distortion, subject-to-camera relationship, and how perspective affects apparent face/body/object/background proportions.
- Wide-angle or close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, or minimal distortion only when visible.
- Telephoto compression only when visible.
- Low-angle elongation or high-angle compression only when visible.
- Focus target, focus accuracy, depth of field, sharpness, bokeh, foreground blur, background blur, low-resolution softness, digital sharpening, compression, noise reduction, bloom, haze, and which planes remain sharp or blurred.
- Motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable no-blur capture.
- Camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, 35mm-like film, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look.

Describe lighting-to-volume:

- Main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, or ambient light when visible.
- Highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, or overexposure.
- For visible shadows, identify the apparent caster, receiving surface, shadow shape, edge softness or hardness, density, direction, falloff, and color cast when supported by visible evidence.
- Distinguish self-shadowing on faces, hair, clothing, body contours, and objects from cast shadows made by clothing, folds, hair, arms, hands, props, architecture, background structures, or the frame boundary.
- State whether shadows reveal form, hide form, flatten form, exaggerate volume, break up a contour, merge dark objects together, separate foreground from background, or obscure detail.
- How lighting affects face structure, skin texture, clothing texture, object shape, visible body contour, and perceived body volume.
- Do not relight the scene into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes apparent proportions or face structure.

## Background and Color

Describe the background by zones:

- Left side, right side, top, bottom, foreground, midground, and background.
- Include only visible location type, architecture, nature, furniture, props, street details, interior details, weather, time of day, practical lights, reflections, shadows, background figures, vehicles, plants, signs, windows, doors, textiles, surfaces, and objects.
- If background objects are blurred, minor, or indistinct, say they remain blurred, minor, indistinct, soft silhouettes, or heavily defocused. Do not over-specify barely visible objects.
- Describe whether the background separates from or blends with the subject silhouette.

Describe color and mood:

- Dominant palette, color grading, white balance, saturation, contrast, global cast, skin tone rendering, color imperfections, mixed lighting, film color shift, digital color noise, and emotional tone.
- Preserve whether the image reads as warm, cool, neutral, muted, pastel, high-contrast, low-contrast, faded, nostalgic, candid, raw, ordinary, elegant, dramatic, mysterious, intimate, documentary, chaotic, surreal, polished, accidental, quiet, glamorous, or understated.

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
9. Lighting, atmosphere, color grading, contrast, highlights, shadow source/caster/receiver relationships, cast shadows, self-shadowing, contact shadows, shadow edge quality, shadow density, shadow position, shadow direction, flash behavior if present, and how shadows affect visible form, occlusion, and lighting-to-volume effects.
10. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
11. Focus target, focus accuracy, depth of field, sharpness, bokeh, foreground blur, background blur, low-detail areas, and which planes must remain sharp or blurred.
12. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible, and whether blur should be preserved or avoided.
13. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
14. Critical fidelity locks: primary visual concept, perceptual relationships, composition, crop, subject scale, face, calibrated body proportions when relevant, adult chest/upper-torso/waist/hip silhouette when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, and medium/rendering.

### NEGATIVE PROMPT:

Write concise, image-specific exclusions tailored to the actual image. Include only relevant drift risks, covering:

- Primary-concept drift and concept-lock failure modes: all objects present but their visual relationship is wrong, concept-critical object treated as a generic prop, intended effect collapsed into separate unrelated objects, replacement/continuation/scale/interactions broken, fused surfaces rendered as separate stacked objects, completion seam misaligned, counterpart or missing-side logic swapped, duplicated, or omitted, feature proportions mismatched across a join, frame-within-frame lost, mixed-media contrast lost, intended implausibility or uncanniness normalized into a plausible realistic scene, stylized/composited/screen-contained element promoted into a normal physical object, ordinary scene replacing the intended visual premise, or a visually separate collage replacing a single integrated illusion.
- Wrong crop, subject scale, placement, headroom, body crop, object placement, or foreground/midground/background order.
- Wrong background, extra people, extra objects, duplicated objects, over-detailed blurred background, or wrong location type.
- Wrong style or medium drift: cartoon, anime, illustration, 3D render, painting, sketch, vector art, glossy commercial look, fake cinematic look, fake vintage look when absent, overprocessed HDR, plastic skin, excessive retouching, AI-smoothed face or body.
- Text, watermark, logos, UI icons, subtitles, captions, random letters, readable brand marks unless truly central and generic.
- Distorted hands, extra fingers, missing fingers, malformed grip, broken limbs, warped face, mismatched eyes, duplicated people, fused objects, impossible clothing folds, impossible anatomy.
- For portraits: wrong apparent ancestry/race-coded appearance, skin tone, face shape, eyelid structure, eye spacing, nose bridge/width/length, lip fullness, jawline, chin, cheekbones, age range, hair texture, hairline, facial texture, makeup level, face-defining light/shadow, and non-identifying facial anchors.
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
- Quality:
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
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Lighting-to-volume fidelity locks: include source-specific light direction plus visible cast shadows, self-shadowing, contact shadows, shadow edge quality, shadow density, shadow direction, caster/receiver relationships, and shadow-hidden contours.
- Pose fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
