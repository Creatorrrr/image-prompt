---
id: medium.photographic-capture
version: 6
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
  - medium.unspecified-visual
provides_anchors:
  - sharpness_topology
  - contrast_topology
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

Map sharpness separately across the primary subject, secondary details, foreground, and background.

Map contrast topology separately at the global scene, major subject masses, local form transitions, and surface/material boundaries.

- Identify the largest continuous bright shapes and darkest framing masses before listing small highlights or shadows.
- Separate overall tonal range from local subject contrast. A low-contrast scene can still have one crisp boundary; a high-contrast scene can retain soft internal form.
- State whether shadows flatten volume, softly imply it, separate overlapping planes, or hard-sculpt contours. Do not let `dramatic lighting` stand in for that behavior.
- Distinguish diffuse, matte, translucent, oily, glossy, metallic, woven, and absorbent responses only when visible; different surfaces under one light need not share highlight width or black level.

Distinguish global low acutance, diffusion, haze, compression, or processing softness from depth-of-field blur. Use `shallow depth of field` or premium-looking bokeh only when a visibly sharper focus plane is separated from defocused layers. If the nominal focus subject is also soft, preserve that softness instead of sharpening it while blurring only the background.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Do not relight into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes visible structure.

## Optional negative contribution

Reject wrong camera distance/height/angle/lens perspective, wrong focus target/depth of field, background too sharp, soft photo becoming overly sharp, sharp photo becoming blurry, added/removed camera shake, wrong blur direction, wrong grain/sharpening/flash/color cast/dynamic range/highlight rolloff, polished studio quality when source is casual, and relighting that changes apparent proportions.

## Optional settings contribution

- Camera/film/rendering target:
- Lighting/rendering target:
- Lighting-to-volume fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
