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
   1. Composition, aspect ratio, orientation, crop, subject scale, frame placement, and spatial layout.
   2. Human appearance fidelity when people are visible: face, skin tone, broad apparent visual ancestry or race-coded appearance when visually evident, hair, visible body proportions, clothing-shaped silhouette, pose, and occlusion.
   3. Pose mechanics, gesture, limb placement, hand placement, negative space, and crop boundaries.
   4. Camera distance, height, angle, lens impression, perspective distortion, focus target, depth of field, sharpness, blur, camera shake, and optical behavior.
   5. Lighting direction, atmosphere, color grading, contrast, highlights, shadows, flash behavior, and lighting-to-volume effects.
   6. Background zoning, objects, depth layers, and environmental details.
   7. Medium, texture, grain, noise, compression, imperfections, and processing artifacts.

4. Use approximate normalized coordinates when useful:
   - `x=0%` is the far left edge; `x=100%` is the far right edge.
   - `y=0%` is the top edge; `y=100%` is the bottom edge.
   - Use coordinates for major anchors such as face center, eye line, head, shoulders, torso, waist, hips, elbows, hands, knees, feet, held objects, important foreground/background objects, horizon line, light sources, highlights, shadows, focus zones, blur zones, crop edges, and occluding objects.

5. Write only the required output sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

Do not include hidden analysis, checklist text, caveats, explanations, or references to the source image still being attached.

## Visual Evidence Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or any wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, sizes, age, weight, height, camera metadata, or private identity.
- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.

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

For every visible person, describe only visible image-plane proportions shaped by clothing, pose, crop, lens, focus, blur, lighting, and occlusion. Do not infer hidden anatomy under clothing, props, hands, arms, hair, shadow, blur, or crop.

If the subject is not clearly adult or age is ambiguous:

- Use neutral non-sexual clothing, posture, and upper-torso silhouette language only.
- Do not emphasize chest, bust, cleavage, hips, or other sexualized body traits.

For clearly adult subjects:

- Treat visible body proportions as ordinary visual facts.
- Describe relevant visible build, shoulder width, ribcage or upper-torso width, calibrated chest/bust/upper-torso silhouette, waist position and taper, abdomen or midsection if visible, hip width if visible, torso-to-leg ratio, limb scale, and clothing-shaped silhouette.
- Use the weakest accurate calibration supported by the image: `hidden or not visible`, `visible but mostly obscured`, `slight`, `moderate`, `moderate-to-full`, `full`, `large`, `very large`, `broad but low-detail`, `visually dominant because of crop/camera/pose/lighting/clothing`, or `visually secondary despite being visible`.
- State whether visible volume is silhouette-defined, clothing-shaped, shadow-defined, highlight-defined, rim-defined, flat-lit, backlit, underexposed, overexposed, dark-fabric-obscured, bright-fabric-softened, haze-softened, low-contrast, low-detail, or partially obscured.

Use symmetric calibration locks:

- If a visible adult body feature is large or very large, preserve it against reduction, flattening, averaging, hiding, or modesty/safety correction.
- If it is moderate, moderate-to-full, slight, flat, broad, secondary, softened, low-detail, or obscured, preserve that calibration against enlargement, extra projection, deeper neckline, tighter clothing, added cleavage shadows, added under-bust shadows, stronger highlights, sharper contouring, or increased dominance.
- If hands, phone, arms, hair, fabric, props, another person, shadow, blur, crop, or frame edge partially hide contours, preserve that occlusion instead of revealing or clarifying hidden shape.
- If a feature is visible but not central, describe it as visible but secondary, not as dominant.
- If a feature is visually dominant because of crop, camera angle, lens, pose, lighting, or clothing, state the visible cause rather than inventing hidden anatomy.

Avoid repetition that over-weights body features. Mention a body feature in the body-proportion section, and repeat it in locks or negative prompt only when it is genuinely important to fidelity.

## Pose, Occlusion, and Clothing

For each visible person, describe precise mechanics rather than only generic pose labels:

- Body crop and visible body parts.
- Head direction, head tilt, chin angle, gaze, neck visibility, shoulder line angle, torso orientation, twist, lean, posture, and spine/action line.
- Shoulder height difference, hip height difference, weight distribution, arm direction, elbow bend, forearm angle, wrist angle, hand placement, finger visibility, object grip, leg placement, knee bend, ankle/foot placement, and negative space.
- Occlusion relationships between limbs, clothing, body, face, objects, shadow, blur, and crop.
- Approximate pose landmark coordinates when helpful.

Describe clothing as it affects visible silhouette:

- Fit, fabric type and thickness, opacity/transparency, stiffness/looseness, fabric tension, wrinkles, folds, neckline depth and width, strap position, sleeve position, seam placement, waist seam, under-bust seam if visible, buttons, lace, pattern scale, garment layers, and interaction with body shape and pose.
- Do not make clothing tighter, looser, more structured, more corseted, more revealing, more transparent, more padded, more lifted, more sculpted, more modest, more fashion-editorial, more lingerie-like, more body-hugging, or more generic than the source.

Preserve occluding elements. Do not move hands, phones, arms, hair, bags, props, shadows, blur, another person, clothing folds, or crop edges in a way that reveals more body, hides different areas, or clarifies hidden anatomy.

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

1. Overall image type, aspect ratio, orientation, realism level, medium/rendering type, and mood.
2. Exact composition, crop, subject size, frame placement, bounding box, and approximate coordinates.
3. Subject face and human appearance fidelity when people are visible.
4. Subject visible body proportions and physique fidelity when people are visible, including adult calibration locks when relevant and safe.
5. Exact pose, body orientation, head angle, gaze, shoulder line, torso lean, arms, elbows, wrists, hands, fingers, object grip, legs, stance, weight distribution, occlusion, negative space, crop boundaries, and pose landmark coordinates.
6. Clothing, accessories, and held objects, including how they reveal, obscure, flatten, soften, follow, compress, stretch over, widen, narrow, or visually define the body or pose.
7. Background by screen zones: left, right, top, bottom, foreground, midground, and background.
8. Lighting, atmosphere, color grading, contrast, highlights, shadows, flash behavior if present, and lighting-to-volume effects.
9. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
10. Focus target, focus accuracy, depth of field, sharpness, bokeh, foreground blur, background blur, low-detail areas, and which planes must remain sharp or blurred.
11. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible, and whether blur should be preserved or avoided.
12. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
13. Critical fidelity locks: composition, crop, subject scale, face, calibrated body proportions when relevant, adult chest/upper-torso/waist/hip silhouette when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, and medium/rendering.

### NEGATIVE PROMPT:

Write concise, image-specific exclusions tailored to the actual image. Include only relevant drift risks, covering:

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
- Lighting drift: wrong light direction, highlight placement, shadow falloff, exposure, contrast, black-level handling, bloom, dark-fabric absorption, rim light, frontal flattening, contour lighting, haze-softened contours becoming sharp, low-contrast contours becoming high-contrast, or lighting that changes visible proportions.
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
- Most important fidelity locks:
- Face fidelity locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Lighting-to-volume fidelity locks:
- Pose fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
