---
id: medium.photographic-capture
version: 13
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

Load for photographic images whose camera, focus, lighting, or processing behavior matters.

## Evidence contribution

Contribute only photographic controls that materially affect an invariant or likely drift. Describe:

- camera distance, height, angle, roll, perspective, and resulting scale or foreshortening
- focus target, depth of field, layer blur, global softness, sharpening, compression, bloom, and haze
- motion blur, shake, ghosting, smear, rolling-shutter, or stable capture
- visible medium impression and its fidelity ceiling. For casual or compressed capture, preserve handheld asymmetry, softness, bloom, clipping, low-legibility, and ordinary framing before genre shorthand.

Map sharpness separately across the primary subject, secondary details, foreground, and background.

Map contrast topology separately at the global scene, major subject masses, local form transitions, and surface/material boundaries.

- Identify the largest bright and dark masses before small accents.
- Separate global range from local contrast; either can be strong while the other is soft.
- State whether shadows flatten, reveal, separate, or sculpt form. Distinguish material responses only when visible.
- For a large dark photographic mass, separate its displayed shadow floor, spatial black-level distribution, and capture-level texture or microcontrast visibility. Similar darkness can hide materially different gradients or surface detail, and soft light does not by itself determine any of those three results.

Decompose photographic appearance into intrinsic subject evidence, pose or deformation, perspective, illumination and shadow, material interaction or occlusion, and capture or processing. Preserve their combined visible result, but do not let one cause rewrite another.

For humans, keep cosmetic visibility, displayed-skin finish, optical softness/bloom, and retouching or editorial polish as separate effects. A person-aesthetic anchor may own capture treatment only when declared in its intended budget and decomposed here; it cannot turn diffused softness into glossy beauty lighting, stronger makeup, sharper facial sculpture, or premium studio finish.

Record important color relationships as intrinsic surface hue, illumination color, global cast, and exposure response. Assign the consolidated hue instruction to one semantic slot; this module should describe the photographic shift rather than repeat another module's color target.

Treat the image's sampled or visually read color as displayed capture output. Without calibrated scene data, it does not establish scene reflectance, material true color, or a person's biological color independently of illumination, white balance, exposure, tone mapping, and profile handling.

Separate photographic white balance or global cast from exposure and tone-curve behavior. A warmer or cooler capture shift must not silently darken, brighten, saturate, or desaturate an intrinsic surface unless the source supports each change.

Map source-visible highlight, midtone, and shadow response separately when tonal reproduction is material. Use comparable midtone or flat patches for displayed intrinsic color and separate highlight or shadow patches for response; do not pool illumination zones or substitute capture response for intrinsic surface axes.

Require neutral anchors or consistent multi-region behavior for global white balance; otherwise report local shifts and uncertainty.

In source/render comparison, compare target and contextual patches. Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. Shared movement supports a global cause; target-only movement supports a local cause; mixed results remain unresolved.

Distinguish global softness, diffusion, haze, or compression from depth-of-field blur. Invoke shallow depth only when a sharper focus plane separates from defocused layers; if the subject is also soft, preserve it.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter. Hand displayed shadow floor, highlight rolloff, and microcontrast to Color/Tone, while Light/Form owns where dark and bright masses fall and how their transition traverses the surface.

Describe lighting-to-volume:

- main direction, softness, temperature, fill, back/rim/flash contribution
- highlight placement, shadow falloff, black level, bloom, haze, clipping, and local contrast
- cast, self, and contact shadows only when they affect form, separation, or composition

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Keep global contrast distinct from local form contrast so a dark frame or wide tonal range does not automatically create hard internal definition.

When lighting itself is first-order, contribute capture evidence to `detail.light-form-fidelity` instead of independently owning source geometry, fill, shadow topology, material response, or background spill. Keep exposure, tone curve, white balance, and illumination color in the photographic Color/Tone handoff so the two contracts do not repeat one visible pull.

Do not relight into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes visible structure.

## Optional negative contribution

Reject wrong perspective, focus hierarchy, blur direction, sharpness, shake, grain, flash, cast, tonal response, polished quality beyond the source, and relighting that changes proportions.

## Optional settings contribution

- Camera/film/rendering target:
- Lighting/rendering target:
- Lighting-to-volume fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
