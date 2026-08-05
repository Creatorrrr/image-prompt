---
id: core.fidelity-discipline
version: 6
priority: 104
type: core
tier: 0
facet: core
facet_values:
  - fidelity-discipline
  - anti-polish
  - anti-normalization
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
conflicts: []
provides_anchors:
  - anti_polish
  - broad_label_discipline
  - fidelity_ceiling
  - aesthetic_salience_gate
  - aesthetic_signature_early
  - detail_not_sharpness
  - attractiveness_polish_separation
---

# Core: fidelity discipline and anti-normalization

## When to load

Always. This module keeps every routed path from becoming cleaner, more generic, more attractive, more plausible, or more category-normalized than the source.

## Rules

- Cap generated polish to the source. If the source is casual, degraded, compressed, dim, soft, awkwardly framed, low-resolution, underexposed, socially edited, or non-editorial, prevent cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished drift.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal or product ideal. Keep roughness, awkwardness, asymmetry, styling, social-media look, visible mood, surface sheen, color cast, retouching level, and medium imperfections when present.
- Treat subject attractiveness and image polish as separate controls. A supported attractiveness anchor may describe the visible person gestalt, but it must not imply stronger symmetry, skin cleanup, makeup, styling, crop, focus, lighting, or editorial finish than the source.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or awkward capture, preserve that relationship above realism and plausibility.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever the label would pull the generator toward a common composition, cleaner styling, expanded crop, completed object, or more attractive category default. Put visible geometry, crop, relationship, medium, and fidelity constraints before shorthand labels.
- Treat source fidelity ceiling as an affirmative requirement: the output should not exceed the visible source in sharpness, cleanliness, glamour, lighting balance, polish, readability, symmetry, or plausibility unless the user explicitly asks for improvement.
- Do not use absolute enhancement terms such as `high quality`, `sharp`, `crisp`, `clean`, `pristine`, `luxury`, `cinematic`, or `studio` unless the source visibly supports them and they do not conflict with crop, lighting, artifacts, or ordinary capture.

## Aesthetic salience gate

Decide whether changing the global look while preserving the objects would materially change the image.

- **High-salience look:** select three to six mutually supporting anchors from tone curve and microcontrast; palette, cast, and saturation; sharpness distribution; diffusion, bloom, haze, grain, compression, or surface treatment; lighting character; and subject/environment hierarchy.
- **Neutral look:** use one or two ordinary visible cues. Do not create a special style block.
- **Ambiguous look:** describe only observed behavior and avoid named genre, camera, film, or era presets.

Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues.

Treat descriptive detail and rendered sharpness as independent controls. Detailed geometry may remain soft, low-contrast, compressed, flat, rough, or low-legibility. Do not let face, product, garment, or environment detail silently raise local sharpness, scale, polish, or visual priority.

Translate mood words into visible mechanisms. A term such as dramatic, nostalgic, cinematic, clean, or premium cannot replace its supported tone, color, light, sharpness, and texture evidence.

## Prompt additions

State the source fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent. Use source-specific counterweights such as `still visibly compressed`, `not upgraded into a studio portrait`, `not cleaned into a product shot`, or `not normalized into a plausible full scene`.

When the source look materially differs from a clean default, place a compact Aesthetic Signature near the beginning of `PROMPT:`. Keep its strongest look lock affirmative and repeat at most one highest-risk drift constraint near the end; do not scatter the same adjectives through every paragraph.

## Optional negative contribution

Reject beautification, over-polish, relighting, sharpening, style upgrade, social-media glamorization, product-shot cleanup, symmetry correction, plausible-scene normalization, expanded crop, and broad-label defaults that contradict visible evidence.

## Optional settings contribution

- Fidelity ceiling locks:
- Anti-polish and anti-normalization locks:
- Broad-label weakening locks:
