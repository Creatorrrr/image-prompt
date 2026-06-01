---
id: subject.animal
version: 2
priority: 65
type: subject
tier: 2
facet: subject
facet_values:
  - animal
  - pet
  - wildlife
  - creature-as-animal
triggers:
  - animal, pet, wildlife, or creature treated visually as an animal
avoid_when:
  - no animal-like subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Subject: animal fidelity

## When to load

Load when an animal, pet, wildlife subject, or animal-like creature is visually important.

## Detection cues

Species or type may be clear, ambiguous, stylized, cropped, or partially hidden. Use broad visual description if exact species/breed is uncertain.

## Prompt additions

Describe only visible animal evidence:

- species/type or broad animal class when clear; otherwise `small animal`, `large animal`, `bird-like`, `dog-like`, `cat-like`, etc.
- head shape, muzzle/beak/snout, ear shape, eye placement, whiskers, horns/antlers, tail, paws/hooves/claws/fins/wings if visible
- fur/feather/scale/skin texture, length, pattern, matting, wetness, sheen, color distribution
- body posture, weight distribution, gait, curled/sitting/standing/flying/swimming mechanics
- gaze, mouth position, tongue/teeth visibility, expression-like cues without assigning human intent
- scale relative to hands, furniture, environment, other animals, or frame
- crop and hidden limbs/tail/wings

For pets, preserve candid capture and ordinary body shape. Do not make the animal cuter, cleaner, fluffier, more symmetrical, more puppy/kitten-like, more studio-lit, or more breed-standard than the source.

## Negative additions

Reject wrong species/breed-like drift, extra limbs/wings/tails, humanized expression, over-cute pet photography, cleaned fur, over-sharp eyes, changed coat pattern, full body when cropped, missing visible tail/ears/paws, and background/scale changes that alter animal size.

## Settings additions

- Category-specific locks: animal type, texture, posture, crop, scale, and visible markings.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy general visual-evidence and frame-drift rules for new category modules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or any wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, sizes, age, weight, height, camera metadata, or private identity.
- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- Calibrate underexposure instead of maximizing it. When the source has dark clothing, hair, night areas, or shadowed interiors, distinguish fully crushed black regions from low-contrast regions that still show folds, edges, face planes, fabric bands, or object silhouettes. Preserve the amount of remaining shadow detail; do not turn visible dark detail into a featureless black mass.
- When the source image is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement terms such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine` to describe focus, highlights, or recommended quality. Use source-faithful relative terms instead, such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.
- Preserve incomplete evidence. If an object, face, body part, text mark, background figure, surface, or environmental element is cropped, hidden, blurred, shadowed, cut off by frame edges, or only partly visible, describe it as incomplete and specify which visible parts remain. Do not let the prompt invite a complete version of that element.
- Preserve frame-boundary evidence. If the source contains pillarboxing, letterboxing, dark side strips, vignetting, clipped edges, awkward headroom, hard crop boundaries, or edge falloff, treat those as composition facts rather than artifacts to remove.
- For screenshots or screen-recorded social-video frames, treat interface overlays as composition-critical image-plane bands. Lock their exact vertical bands, opacity, corner radius, text size, low-legibility level, and absence/presence of common app controls. State which controls are absent as well as which are present, so the generator does not add hearts, home indicators, action buttons, captions, or clean branded UI that were not visible.
- Preserve overlay restraint. If the source has only a simple status bar, one bottom comment/input field, one crop mark, or one small ambiguous control, do not let the prompt invite a complete modern app interface. Name absent control families in the `PROMPT:` itself when they are likely generator defaults.
- Distinguish transparent overlay icons from app chrome bands. If top status icons float directly over the video/background with no black rectangle behind them, say so explicitly and reject a black top status bar, notch area, or header strip. If the bottom has a dark comment area but no home indicator, reject home indicators even when the generated image is phone-shaped.
- Treat hard frame boundaries and crop exclusions as higher priority than object completion. If satisfying object realism would require revealing cropped areas, completing partial body/object/background regions, removing borders, or expanding the scene, preserve the crop and boundary instead.
- Use a visibility budget for partially visible areas. When only a narrow strip, partial band, partial limb, partial object, or small text mark is visible, state that it remains narrow, partial, secondary, or obscured. Do not reveal more of it, enlarge it, clarify it, or move occluders away unless the source visibly does so.
- Clamp bottom-edge and side-edge partial visibility. If a body region, object, garment, sign, or surface appears only as a thin strip at the frame edge, describe its approximate edge band and explicitly keep it at that edge. Do not let it expand inward, become a full object/body area, or become a new visual center.
- Cap generated polish to the source. When the source is casual, degraded, compressed, dim, soft, or awkwardly framed, the prompt must prevent the output from becoming cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished than the source.
- Preserve awkward capture geometry over attractive pose semantics. If the source is a close, low-angle, cropped, accidental, convention-like, mirror-like, screenshot-like, or casual phone capture, describe that awkwardness as a required fidelity trait and prevent fashion-normalized posture, cleaner posing, centered editorial balance, or full-body/waist-up portrait correction.
- For prompt-only reproduction, repeat the most important frame geometry and crop locks in the `PROMPT:` itself near the beginning and again in the critical fidelity locks. Use affirmative wording such as `the composition remains...`, `the closest plane stays...`, and `the edge band remains...` so the prompt does not rely only on negative exclusions.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal. When a person, product, place, or object has a particular visible mood, styling, attractiveness pattern, roughness, awkwardness, asymmetry, facial softness, makeup level, surface sheen, color cast, or image-era/social-media look, describe that aesthetic calibration and prevent beautification, fashion-editorial upgrading, influencer-like smoothing, glamorization, aging down/up, westernization, or generic model drift.
- For dark, cramped, low-resolution, heavily styled, or socially edited portraits, prevent coordinate precision from becoming permission to rebalance the image. If the source is murky, crowded, shadow-blocked, underexposed, compressed, or visibly stylized, state that the portrait remains visually compressed, dim, low-detail, and source-faithful even when face, prop, garment, or background coordinates are specified. Avoid wording that upgrades the source into a clean centered studio portrait, product portrait, fashion lookbook frame, or polished character reference unless that finish is visibly present.
- When light-created shadows materially affect likeness, composition, occlusion, or surface separation, preserve them instead of brightening, erasing, retouching, or normalizing them. Do not invent contours, body shape, surface detail, or environmental structure hidden by shadow.
- When backlight both hides and reveals the subject, specify which edges and planes remain readable. Do not let `silhouette`, `underexposed`, or `crushed shadows` erase visible face edges, garment fold bands, lace trim, hair outline, object silhouettes, or background detail that the source still shows.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or a deliberately awkward capture, preserve that relationship above realism and plausibility. Do not promote a stylized, composited, inserted, reflected, or screen-contained element into a normal physical object unless it visibly is one.
- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.

4a. Audit the source frame ratio before drafting:
   - If image file dimensions are available in the conversation or from local inspection, compute or preserve the actual width:height relationship in plain terms, such as `aspect about 0.69, taller than 3:4 but wider than 9:16`.
   - When a local source file path is available, check the actual pixel dimensions with a local metadata tool before drafting. If the visible frame is meaningfully narrower, taller, squarer, letterboxed, cropped, or otherwise different from a common ratio, do not normalize it to the common ratio.
   - Keep aspect ratio and output size conceptually separate. Report the measured source pixel dimensions as `width x height`, the decimal width/height ratio, and the nearest plain-language shape.
   - Do not substitute common portrait or landscape labels such as `2:3`, `3:4`, `4:5`, `9:16`, `16:9`, or `1:1` unless that label is close to the measured frame. If no common label is close, say `source-specific portrait crop`, `source-specific landscape crop`, or `source-specific square-adjacent crop` and give the source dimensions or approximate aspect.
   - Do not substitute a generator-preferred size, downscaled preview size, reduced fraction, conversation preview, viewer downscale, model output default, or common 1024-based canvas for the source ratio. If the source file is available, file metadata wins over visible preview dimensions.
   - Put the measured frame treatment in the first sentence of `PROMPT:` before broad labels such as beauty portrait, cosplay portrait, editorial portrait, product shot, screenshot, or landscape.
   - Repeat the measured ratio in `RECOMMENDED SETTINGS:` and list the nearest standard size only as a fallback, clearly saying it is a fallback.
   - Treat aspect-ratio drift as a major fidelity failure because it changes subject scale, edge crops, object placement, and visibility budgets.
