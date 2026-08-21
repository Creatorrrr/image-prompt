---
id: medium.photographic-capture
version: 11
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
  - photographic_causal_decomposition
  - color_light_decomposition
  - light_to_form_strength
  - white_balance_exposure_separation
  - photographic_tone_response
  - tone_zone_sampling_separation
  - global_local_color_residual
---

# Medium: photographic capture, camera, focus, lighting

## When to load

Load for photographs, phone captures, snapshots, camera previews, scanned photos, and photorealistic images whose camera/focus/lighting behavior should be preserved.

## Evidence contribution

Contribute only photographic controls that materially affect an invariant or likely drift. Describe:

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

Decompose photographic appearance into intrinsic subject evidence, pose or deformation, perspective, illumination and shadow, material interaction or occlusion, and capture or processing. Preserve their combined visible result, but do not let one cause rewrite another.

Record important color relationships as intrinsic surface hue, illumination color, global cast, and exposure response. Assign the consolidated hue instruction to one semantic slot; this module should describe the photographic shift rather than repeat another module's color target.

Treat the image's sampled or visually read color as displayed capture output. Without calibrated scene data, it does not establish scene reflectance, material true color, or a person's biological color independently of illumination, white balance, exposure, tone mapping, and profile handling.

Separate photographic white balance or global cast from exposure and tone-curve behavior. A warmer or cooler capture shift must not silently darken, brighten, saturate, or desaturate an intrinsic surface unless the source supports each change.

Map source-visible highlight, midtone, and shadow response separately when tonal reproduction is material. Use comparable midtone or flat patches for displayed intrinsic color and separate highlight or shadow patches for response; never widen an intrinsic target by pooling several illumination zones. Preserve clipping, rolloff, lifted or crushed shadows, and local tone compression without using them as substitutes for intrinsic surface lightness or chroma.

Use reliable neutral anchors or consistent multi-region behavior to support a global white-balance claim. When the evidence is mixed or weak, contribute the observed local shifts and uncertainty to the shared Color/Tone Contract rather than forcing a global cast.

In source/render comparison, compare several target patches with contextual or neutral patches. Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. A common direction across both groups supports a global exposure, cast, or processing explanation; a target-only residual supports a local or intrinsic explanation; mixed directions stay unresolved. Do not declare pixel fidelity without an explicit tolerance policy or user judgment.

Distinguish global low acutance, diffusion, haze, compression, or processing softness from depth-of-field blur. Use `shallow depth of field` or premium-looking bokeh only when a visibly sharper focus plane is separated from defocused layers. If the nominal focus subject is also soft, preserve that softness instead of sharpening it while blurring only the background.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Keep global contrast distinct from local form contrast so a dark frame or wide tonal range does not automatically create hard internal definition.

When lighting itself is first-order, contribute capture evidence to `detail.light-form-fidelity` instead of independently owning source geometry, fill, shadow topology, material response, or background spill. Keep exposure, tone curve, white balance, and illumination color in the photographic Color/Tone handoff so the two contracts do not repeat one visible pull.

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
