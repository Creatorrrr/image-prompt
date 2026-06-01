---
id: subject.landscape-nature
version: 2
priority: 62
type: subject
tier: 2
facet: subject
facet_values:
  - landscape
  - nature
  - outdoor
  - sea
  - sky
  - mountain
  - forest
triggers:
  - outdoor land, sea, sky, weather, or nature scene
avoid_when:
  - no landscape/nature subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.background-color
conflicts: []
provides_anchors: []
---

# Subject: landscape and natural environment

## When to load

Load when the image is primarily or substantially about an outdoor natural environment.

## Prompt additions

- Lock horizon height, terrain bands, sky area, waterline, mountain/forest/building silhouettes, foreground texture, midground layers, and background haze.
- Describe weather and atmosphere only as visible: clouds, fog, rain, snow, mist, dust, smoke, humidity, harsh sun, overcast light, sunset/sunrise color, night darkness.
- Describe natural textures: foliage density, grass length, rock surfaces, sand, mud, water ripple, wave foam, snow crust, cloud edge softness.
- Preserve low-legibility distant features as massing, not detailed postcard scenery.
- State absent object classes when generators might add them: no people, no boats, no buildings, no birds, no signs, if absent and relevant.
- Preserve ordinary or degraded capture. Do not beautify into a travel-poster, HDR landscape, dramatic cinematic sky, or saturated postcard unless source is visibly that way.

## Negative additions

Reject altered horizon, added sun/moon/rainbows, extra people/animals/boats/buildings, over-detailed distant objects, HDR postcard lighting, wrong weather/time of day, sharpened haze, changed terrain band proportions, and cleaned-up composition.

## Settings additions

- Category-specific locks: horizon, terrain layers, atmosphere, weather, natural textures, and fidelity ceiling.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy landscape/background massing, color, atmosphere, and softness rules

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
