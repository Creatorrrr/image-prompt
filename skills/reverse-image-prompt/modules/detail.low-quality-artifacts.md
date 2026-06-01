---
id: detail.low-quality-artifacts
version: 3
priority: 70
type: detail
tier: 3
facet: detail-risk
facet_values:
  - low-quality
  - compressed
  - underexposed
  - motion-blurred
  - noise
  - haze
  - soft-focus
  - artifact
  - low-resolution
triggers:
  - low-res, compression, blur, noise, underexposure, artifacts, casual capture
avoid_when:
  - clean high-detail source without degradation
dependencies:
  - core.visual-evidence
  - core.fidelity-discipline
conflicts: []
provides_anchors: []
---

# Detail: low-quality, compression, blur, and artifact fidelity

## When to load

Load when degraded capture quality is visually important or when a generator is likely to over-polish the image.

## Detection cues

- compression blocks, social-media softness, small image upscaling, smeared edges
- low-light noise, chroma noise, crushed shadows, clipped highlights
- motion blur, camera shake, rolling-shutter smear
- haze, bloom, low contrast, sharpening halos, noise reduction plasticity
- low-legibility text or background due to resolution

## Prompt additions

- Put fidelity ceiling near the beginning of `PROMPT:` when degradation controls the look.
- State relative focus hierarchy: what is least soft, what is heavily blurred, what remains indistinct.
- Calibrate underexposure. Distinguish fully crushed black regions from dark low-contrast regions that still show folds, edges, face planes, object silhouettes, or background detail.
- Preserve haze, softness, noise, compression, and low-detail edges. Do not request `crisp`, `pristine`, `sharp`, `clean`, or `high quality` unless the source is actually clean.
- Mention artifact distribution: edges, shadows, flat color areas, UI bands, background, skin/hair, text, motion direction.
- For phone-video, screenshots, social-media captures, or compressed casual sources, promote visible imperfections into positive prompt constraints before any aesthetic or material polish. Name low-resolution edge softness, compression smearing, motion-soft groups, flattened background massing, haze, bloom, clipped highlights, low-legibility marks, and sensor/app artifacts when visible.
- Treat distant or secondary background elements in degraded captures as massing and artifact planes before category labels. Lock them as blurred, low-legibility, compressed, partially cropped, or secondary unless the source clearly makes them the subject.

## Negative additions

Reject over-sharpening, clean studio quality, HDR upgrade, noise removal, plastic smoothing, brightening shadows into invented detail, erasing compression, perfect focus, clean text, detailed background, polished render, and making the image more cinematic or commercial than the source.

## Settings additions

- Quality/Fidelity: degraded/soft/compressed/noisy/hazy/underexposed as visible.
- Focus and depth-of-field locks: relative focus hierarchy.
- Film/camera/sensor or medium artifact locks: artifact types and distribution.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy low-quality, compression, exposure, focus, and artifact rules

- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- Calibrate underexposure instead of maximizing it. When the source has dark clothing, hair, night areas, or shadowed interiors, distinguish fully crushed black regions from low-contrast regions that still show folds, edges, face planes, fabric bands, or object silhouettes. Preserve the amount of remaining shadow detail; do not turn visible dark detail into a featureless black mass.
- When the source image is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement terms such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine` to describe focus, highlights, or recommended quality. Use source-faithful relative terms instead, such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.

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
