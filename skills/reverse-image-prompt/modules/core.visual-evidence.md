---
id: core.visual-evidence
version: 2
priority: 110
type: core
tier: 0
facet: core
facet_values:
  - visual-evidence
triggers:
  - any image
avoid_when: []
dependencies: []
conflicts: []
provides_anchors:
  - standalone_reference_ban
  - visible_evidence_only
---

# Core: visual evidence rules

## When to load

Always.

## Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, age, weight, height, camera metadata, private identity, exact brand, exact artist, exact camera, exact lens, or exact film stock.
- Use visible evidence only. When uncertain, use calibrated uncertainty terms: `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, `ambiguous`, `low-confidence`, or `indistinct`.
- Preserve the source image rather than correcting it. Do not beautify, polish, relight, make safer-looking, make more modest, sexualize, normalize, center, sharpen, or upscale the source unless the user explicitly asks for improvement rather than reverse engineering.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- If the source is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement words such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine`. Use source-faithful relative terms such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.
- Preserve incomplete evidence. If an object, face, body part, text mark, background figure, surface, or environmental element is cropped, hidden, blurred, shadowed, cut off, or partly visible, describe it as incomplete and specify which visible parts remain.
- Treat hard frame boundaries, pillarboxing, letterboxing, dark side strips, vignetting, clipped edges, awkward headroom, and edge falloff as composition facts unless the user asks for cleanup.
- Use a visibility budget for partial regions. If only a narrow strip, partial limb, partial object, tiny label, or edge band is visible, state that it remains narrow, partial, secondary, low-detail, or obscured.
- Cap generated polish to the source. If the source is casual, degraded, compressed, dim, soft, awkwardly framed, or non-editorial, prevent cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished drift.

## Prompt additions

Include source-faithful language for visible imperfections, incomplete details, partial crops, hard boundaries, and fidelity ceiling near the beginning of `PROMPT:` and again in critical fidelity locks when important.

## Negative additions

Reject beautification, added polish, completing cropped elements, identity assumptions, hidden anatomy/object invention, upgraded quality, cleaner relighting, and genre normalization that changes visible evidence.

## Settings additions

- Quality/Fidelity: match the visible source fidelity, including any degradation.
- Most important fidelity locks: source-visible evidence only; no hidden completion.
- Boundary and visibility-budget locks: list partial objects, crop edges, and incomplete evidence.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy purpose and evidence boundary

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


## Legacy Visual Evidence Rules

## Visual Evidence Rules

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
