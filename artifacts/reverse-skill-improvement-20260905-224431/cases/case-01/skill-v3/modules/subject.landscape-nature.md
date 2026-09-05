---
id: subject.landscape-nature
version: 4
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

## Optional negative contribution

Reject altered horizon, added sun/moon/rainbows, extra people/animals/boats/buildings, over-detailed distant objects, HDR postcard lighting, wrong weather/time of day, sharpened haze, changed terrain band proportions, and cleaned-up composition.

## Optional settings contribution

- Category-specific locks: horizon, terrain layers, atmosphere, weather, natural textures, and fidelity ceiling.
