---
id: subject.architecture-interior
version: 2
priority: 62
type: subject
tier: 2
facet: subject
facet_values:
  - architecture
  - interior
  - room
  - building
  - street-architecture
  - structure
triggers:
  - building, interior, room, street architecture, structural perspective
avoid_when:
  - no architectural or interior fidelity need
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.background-color
conflicts: []
provides_anchors: []
---

# Subject: architecture, street structure, and interiors

## When to load

Load when buildings, interiors, rooms, corridors, streetscapes, furniture layout, or structural perspective are important.

## Prompt additions

- Describe space by zones: foreground, midground, background, left, right, top, bottom.
- Lock horizon, vanishing direction, wall/floor/ceiling planes, doorway/window positions, vertical lines, arches, stairs, railings, columns, furniture seams, countertops, table edges, shelves, and floor/wall transitions.
- State camera height, tilt, roll, and perspective distortion. Preserve vertical convergence or skew when visible.
- Describe materials: concrete, brick, tile, wood, plaster, glass, metal, fabric, stone, painted surface, worn/clean/reflective/matte.
- Preserve clutter, partial objects, edge cuts, occlusion, and imperfect room lighting. Do not turn an ordinary room or street into a clean architectural visualization.
- For signs/posters/labels, combine with `detail.text-logo-label`.

## Negative additions

Reject straightened perspective if source is tilted, clean interior render, added windows/doors/furniture, removed clutter, wrong room type, sharper background than source, postcard-like architecture, perfect symmetry, extra people, and completed cropped structural elements.

## Settings additions

- Category-specific locks: structural planes, perspective, material, room/street zoning, and architectural crop.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy background zoning, structural surfaces, lighting, and perspective rules

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
