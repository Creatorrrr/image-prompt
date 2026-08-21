---
id: core.output-contract
version: 11
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

Write a standalone English prompt ordered by the dominant fidelity axis:

- Begin with frame shape, medium, fidelity ceiling, and the perceptual proposition.
- **Relationship-led:** crop, major zones, topology, interaction, then appearance.
- **Appearance-led:** causal form, surface, light, color, hierarchy, then flexible pose or inventory.
- **Information-led:** layout, reading order, hierarchy, legibility, then decoration.
- **Mixed:** name co-primary invariants and only cues showing their dependency.
- Finish with supporting subject, capture, background, artifact, and drift controls.

Selected modules contribute evidence candidates, not mandatory prose. Merge them by semantic slot; module count must not determine prompt length.

Assign one clause owner to each emitted semantic slot. State its affirmative target once; add only a distinct high-risk boundary.

When color or tone is material, assign each emitted control to one causal layer and one perceptual effect budget. Use source-relative value, chroma, and hue; keep intrinsic surface, illumination, global cast, exposure, processing, and hierarchy consistent.

Place one compact color-tone passage early when primary; when supporting, use the smallest relational control. Hierarchy normally owns area, value, chroma, or contrast, not repeated surface hue.

Use compact blocks for complex images and no fixed word cap; every clause must add a control. Keep essential crop, partial visibility, and interactions affirmative. Relate major components and state inversion-prone topology directly.

For a high-salience look, put one supported Aesthetic Signature before inventory; for a neutral look, use one or two cues. Preserve major-region area, role, edge contact, legibility, and attention.

When face likeness is selected, use one scale-appropriate passage; a gestalt anchor cannot replace visible geometry or raise polish.

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

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.
