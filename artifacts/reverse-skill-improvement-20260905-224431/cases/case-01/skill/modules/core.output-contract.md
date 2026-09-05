---
id: core.output-contract
version: 25
priority: 98
type: core
tier: 0
facet: core
facet_values:
  - output-contract
  - adaptive-output
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - concept.primary-relationship
  - core.pre-emit-gate
conflicts: []
provides_anchors:
  - output_sections
  - negative_primary_concept
  - recommended_settings_aspect
  - module_evidence_not_prose
  - clause_ownership
  - diagnostic_render_separation
  - color_tone_output_ownership
  - light_form_output_ownership
---

# Core: adaptive output contract

## When to load

Always. Apply after the visual analysis and routed modules.

## PROMPT

Emit only sections required by the selected output mode.

For a generation request, emit:

```text
PROMPT:
...
```

Write a standalone English prompt ordered first by viewer importance, then by the dominant fidelity axis:

- Compile provenance labels into literal targets; never ask for an unavailable artifact. Physical `light source` remains valid.

- Put P0 source-signature controls first, followed by P1 structural identity.
- Merge P2 support into an owned clause or one short later cue; omit P3 unless the user requests it.

- Begin with the perceptual proposition and its material frame shape, medium, and fidelity ceiling; supporting background does not precede P0/P1.
- **Relationship-led:** crop, major zones, topology, interaction, then appearance.
- **Appearance-led:** causal form, surface, light, color, hierarchy, then flexible pose or inventory.
- **Information-led:** layout, reading order, hierarchy, legibility, then decoration.
- **Mixed:** name co-primary invariants and only cues showing their dependency.
- Finish with supporting subject, capture, background, artifact, and drift controls.

Selected modules contribute evidence candidates, not mandatory prose. Merge them by semantic slot; module count and analysis detail must not determine prompt length.

Assign one clause owner to each emitted semantic slot. State its affirmative target once; add only a distinct high-risk boundary.

Emit each generic effect once. A coupled effect uses one control: its macro summary first, then only `partial` or `lost` member residuals.

Placement controls position, scale, and frame share. Order camera/scale, material pose, then contiguous person prior/local geometry and remaining appearance.

When color or tone is material, assign each emitted control to one causal layer and one perceptual effect budget. Use source-relative value, chroma, and hue; keep intrinsic surface, illumination, global cast, exposure, processing, and hierarchy consistent. Require the full ledger only in `audited`.

In `prompt`, place one compact regional color/tone result early only when P0/P1. A source-evidence-qualified surface descriptor may lead its literal axes once without adding a second direction. In `audited`, trace exact controls.

When lighting is material, assign each emitted control to one Light/Form owner and source-relative effect budget. In `prompt`, state the decisive visible result and protected relation; in `audited`, keep source geometry, apparent size, fill, local contrast, shadow topology, material response, and spill separately ledgered. Generic adjectives cannot own several.

Lead with the visible result; add physical cause only at supported confidence. Keep spatial illumination separate from displayed color/tone. A qualified user or current-source descriptor may lead one literal-control block; calibration remains effectiveness evidence.

Use compact blocks without a fixed cap; every clause adds a control. Keep essential spatial axes distinct and affirmative.

For a high-salience look, put one supported source-specific Appearance or Aesthetic Signature before inventory; for a neutral look, use one or two cues. Preserve only material major-region area, role, edge contact, legibility, and attention.

For a material human, keep user/trusted identity context external and use it once only when P0/P1. Then order one scale-appropriate passage as optional broad person prior, correcting geometry, one bounded person-aesthetic or attractiveness anchor with contiguous owned decomposition, displayed skin, hair, expression, garment coverage, and capture. The aggregate cannot replace controls or alter protected pose, crop, identity, age, lighting, or polish dimensions.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

When a negative prompt is supported, reject only likely concept and fidelity drift. Keep it compact; rewrite an overstrong positive instead of countering it with negatives.

## RECOMMENDED SETTINGS

Emit only when requested, when a target generator is known, or when source dimensions require an adapter note:

```text
RECOMMENDED SETTINGS:
- Model:
- Source frame:
- Target size:
- Quality:
- Prompt-only limits:
```

Include only real generator controls. Separate source dimensions from the requested target size, read `references/model-adapters.md`, and keep visual locks in `PROMPT:`.

## Diagnostic mode

For `diagnostic`, state the source-supported proposition, then its visible causal mechanisms. Keep diagnostic appeal language separate from render instructions, distinguish invariants from flexible dimensions, and include a prompt only when useful.

## Final rule

Read `PROMPT:` as if the source image, analysis, conversation, and every optional section disappeared. If any target or the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.
