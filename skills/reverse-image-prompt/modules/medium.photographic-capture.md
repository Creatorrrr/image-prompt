---
id: medium.photographic-capture
version: 3
priority: 72
type: medium
tier: 2
facet: medium
facet_values:
  - photographic
  - photo
  - camera-capture
  - casual-phone
  - studio-photo
  - flash
  - low-light-photo
triggers:
  - photographic camera, focus, exposure, lighting, lens, or capture behavior matters
avoid_when:
  - clearly non-photographic source with no photo-like capture cues
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts:
  - medium.non-photographic-rendering
  - medium.unspecified-visual
provides_anchors: []
---

# Medium: photographic capture, camera, focus, lighting

## When to load

Load for photographs, phone captures, snapshots, camera previews, scanned photos, and photorealistic images whose camera/focus/lighting behavior should be preserved.

## Prompt additions

Describe photographic capture:

- camera distance, height, angle, roll/rotation, lens impression, perspective distortion
- subject-to-camera relationship and how perspective affects face/body/object/background proportions
- close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, telephoto compression, low-angle elongation, high-angle compression only when visible
- focus target, focus accuracy, depth of field, bokeh, foreground/background blur, low-resolution softness, sharpening, compression, noise reduction, bloom, haze
- motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable capture
- camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look
- For casual phone, screenshot, social-video, or compressed outdoor captures, state the capture imperfection ceiling before beauty, fashion, scenic, studio, or product shorthand. Preserve handheld asymmetry, preview/compression softness, flattened distant layers, bloom, haze, clipped highlights, low-legibility marks, and ordinary non-editorial framing when visible.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Do not relight into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes visible structure.

## Negative additions

Reject wrong camera distance/height/angle/lens perspective, wrong focus target/depth of field, background too sharp, soft photo becoming overly sharp, sharp photo becoming blurry, added/removed camera shake, wrong blur direction, wrong grain/sharpening/flash/color cast/dynamic range/highlight rolloff, polished studio quality when source is casual, and relighting that changes apparent proportions.

## Settings additions

- Camera/film/rendering target:
- Lighting/rendering target:
- Lighting-to-volume fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy Camera, Focus, Lighting, and Medium

## Camera, Focus, Lighting, and Medium

For photographic images, describe how the camera captured the scene:

- Camera distance, camera height, camera angle/rotation, lens impression, perspective distortion, subject-to-camera relationship, and how perspective affects apparent face/body/object/background proportions.
- Wide-angle or close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, or minimal distortion only when visible.
- Telephoto compression only when visible.
- Low-angle elongation or high-angle compression only when visible.
- For close low-angle or high-angle captures, state the image-plane scale hierarchy explicitly: which plane is nearest, which body/object region dominates the lower or upper frame, whether the face is relatively smaller/larger than expected, and which cropped regions must stay outside the frame. Preserve this hierarchy before any conventional portrait or product-photo balance.
- If the source has extreme perspective but not an extreme body-feature emphasis, separate `near-camera scale` from `anatomical size`. Describe the nearest covered surface as large in the image plane because of lens and crop, while preventing rounded, sculpted, exposed, or glamorized anatomy from replacing the flatter source evidence.
- Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-resolution softness, digital sharpening, compression, noise reduction, bloom, haze, and which planes are relatively most in focus or blurred.
- Motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable no-blur capture.
- Camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, 35mm-like film, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look.

Describe lighting-to-volume:

- Main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, or ambient light when visible.
- Highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, or overexposure.
- For visible shadows that materially affect likeness, composition, occlusion, or surface separation, note the apparent caster, receiving surface, shadow shape, edge softness or hardness, density, direction, falloff, and color cast when supported by visible evidence.
- When useful, distinguish self-shadowing on visible surfaces such as faces, hair, clothing, body contours, and objects from cast shadows made by clothing, folds, hair, arms, hands, props, architecture, background structures, or the frame boundary.
- State how shadows affect visible edges, detail, separation, and occlusion without inferring new structure from shadowed areas.
- How lighting affects face structure, skin texture, clothing texture, object shape, visible body contour, and perceived body volume.
- Do not relight the scene into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes apparent proportions or face structure.


## Legacy lighting, atmosphere, background, and color

## Background and Color

Describe the background by zones:

- Left side, right side, top, bottom, foreground, midground, and background.
- Include only visible location type, architecture, nature, furniture, props, street details, interior details, weather, time of day, practical lights, reflections, shadows, background figures, vehicles, plants, signs, windows, doors, textiles, surfaces, and objects.
- If background objects are blurred, minor, or indistinct, say they remain blurred, minor, indistinct, soft silhouettes, or heavily defocused. Do not over-specify barely visible objects.
- Describe whether the background separates from or blends with the subject silhouette.

For soft, distant, degraded, or low-legibility background layers, preserve massing before category. Describe blurry blocks, horizon bands, rhythm of repeated shapes, silhouette layers, transition lines, absent object classes, and softness level before asking for a generic scenic or realistic version of the location. If people, vehicles, signs, readable windows, landmarks, lights, or distinct small objects are not visible, explicitly keep them absent, indistinct, cropped, or low-priority. Prevent the generator from replacing a soft blocky background with a sharper postcard-like panorama, cleaner room, clearer street, or more complete environment.

Describe color and mood:

- Dominant palette, color grading, white balance, saturation, contrast, global cast, skin tone rendering, color imperfections, mixed lighting, film color shift, digital color noise, and emotional tone.
- Preserve whether the image reads as warm, cool, neutral, muted, pastel, high-contrast, low-contrast, faded, nostalgic, candid, raw, ordinary, elegant, dramatic, mysterious, intimate, documentary, chaotic, surreal, polished, accidental, quiet, glamorous, or understated.
