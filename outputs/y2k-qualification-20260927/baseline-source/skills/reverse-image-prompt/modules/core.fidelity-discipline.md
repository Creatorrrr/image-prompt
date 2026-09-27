---
id: core.fidelity-discipline
version: 12
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
  - aggregate_prior_cluster_audit
  - broad_color_descriptor_discipline
  - color_metaphor_decomposition
---

# Core: fidelity discipline and anti-normalization

## When to load

Always. Prevent cleaner, more generic, more plausible, or more category-normalized drift.

## Rules

- Cap generated polish to the source. Preserve visible roughness, softness, asymmetry, color cast, retouching level, ordinary capture, and medium imperfections.
- Treat subject attractiveness and image polish as separate controls. Treat any broader person aesthetic the same way: declare intended and protected dimensions, lead its owned visible controls once, and do not imply unowned skin cleanup, symmetry, makeup, garment exposure, crop, pose, lighting, or editorial finish.
- Preserve visible illusion, mismatch, mixed-media layering, scale incongruity, low fidelity, or awkward capture above plausibility.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels when they pull toward cleaner styling, expanded crop, completion, or beautification. Put evidence before shorthand.
- Treat source fidelity ceiling as an affirmative requirement: do not exceed visible sharpness, cleanliness, glamour, lighting balance, readability, symmetry, or plausibility unless requested.

## Aesthetic salience gate

Decide whether changing visible form, surface, light, color, or hierarchy while retaining objects would change the image's identity or appeal.

In diagnostic mode, name the source-supported perceptual appeal directly before its visible mechanisms; do not infer motive, identity, or story.

An evaluative term is neither automatically valid nor disposable. When an aggregate appeal reading is high-confidence P0/P1 source evidence and its omission causes material drift, retain it once and immediately constrain it with visible controls. Otherwise keep it diagnostic.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only causal axes. Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues. Describe ambiguity instead of invoking presets.

Treat descriptive detail and rendered sharpness as independent controls. Detail must not raise sharpness, scale, polish, or priority.

For a material evaluative or mood term, retain the aggregate once, then immediately unpack visible mechanisms. Neither abstraction nor detail substitutes for the other.

Treat a broad color descriptor as a hypothesis about one causal layer, not as shorthand for hue, value, chroma, lighting, mood, and processing at once. Replace overload with source-supported axes.

Decompose an appearance metaphor into observable color axes, surface behavior, and illumination before using it once as a non-directional summary. Current-source emission requires provenance, high/medium confidence, P0/P1 priority, material-drift omission, compatibility, and immediate owned controls. Calibration remains separate effectiveness evidence; the descriptor adds no second direction.

Audit prior-heavy cues as a combined cluster, not only as isolated labels. Ignore subject nouns temporarily; rewrite unsupported quality, lighting, surface, framing, or style defaults from evidence without a universal blacklist.

## Prompt additions

State the fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent.

When the source differs from a clean default, place a compact Aesthetic Signature early; add at most one highest-risk boundary.

## Optional negative contribution

Reject only likely beautification, relighting, sharpening, style upgrade, symmetry, scene-normalization, crop, or category-default drift.
