---
id: core.fidelity-discipline
version: 7
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
  - aesthetic_causal_signature
  - direct_perceptual_appeal
---

# Core: fidelity discipline and anti-normalization

## When to load

Always. Prevent cleaner, more generic, more plausible, or more category-normalized drift.

## Rules

- Cap generated polish to the source. Preserve visible roughness, softness, asymmetry, color cast, retouching level, ordinary capture, and medium imperfections.
- Treat subject attractiveness and image polish as separate controls. A supported attractiveness anchor must not imply cleaner skin, symmetry, makeup, crop, focus, lighting, or editorial finish.
- Preserve illusion, mismatch, mixed-media layering, scale incongruity, low fidelity, or awkward capture above a more plausible scene.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever their default pulls toward common composition, cleaner styling, expanded crop, completion, or beautification. Put visible evidence before shorthand.
- Treat source fidelity ceiling as an affirmative requirement: do not exceed visible sharpness, cleanliness, glamour, lighting balance, readability, symmetry, or plausibility unless requested.
- Avoid `high quality`, `crisp`, `clean`, `luxury`, `cinematic`, or `studio` unless visibly supported without conflicting with crop, light, artifacts, or ordinary capture.

## Aesthetic salience gate

Decide whether changing the visible form, surface, light, color, or hierarchy while retaining the objects would materially change the image's identity or appeal.

In diagnostic mode, name the source-supported perceptual appeal directly before decomposing it into visible mechanisms. Do not attribute unseen motive, identity, or story.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only axes with causal weight. The cues must reinforce one proposition rather than form a comprehensive checklist.

- **High salience:** use three to six mutually supporting causal cues.
- **Neutral:** use one or two ordinary visible cues without a special style block.
- **Ambiguous:** describe observed behavior and avoid named genre, camera, film, or era presets.

Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues.

Treat descriptive detail and rendered sharpness as independent controls. Detailed geometry may remain soft, compressed, flat, rough, or low-legibility; do not let detail raise sharpness, scale, polish, or priority.

Translate evaluative or mood words into visible mechanisms. A broad descriptor cannot replace supported form, surface, tone, color, light, sharpness, and hierarchy. Use it at most once, then describe its causes.

## Prompt additions

State the fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent.

When the source look materially differs from a clean default, place a compact Aesthetic Signature near the beginning of `PROMPT:`. In appearance-led mode, put it before pose minutiae; repeat at most one highest-risk drift constraint near the end.

## Optional negative contribution

Reject only likely beautification, relighting, sharpening, style upgrade, symmetry, scene-normalization, crop, or category-default drift.

## Optional settings contribution

- Fidelity ceiling locks:
- Anti-polish and anti-normalization locks:
- Broad-label weakening locks:
