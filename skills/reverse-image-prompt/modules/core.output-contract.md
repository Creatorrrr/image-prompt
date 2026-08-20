---
id: core.output-contract
version: 10
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
- **Relationship-led:** place crop, major zones, topology, interaction geometry, and only critical spatial anchors before local appearance.
- **Appearance-led:** place the compact causal signature and source-specific form, surface, light-to-form, color, and hierarchy before flexible pose or inventory.
- **Information-led:** place layout, reading order, hierarchy, legibility, and container relations before decoration.
- **Mixed:** name the co-primary invariants early and include only cues showing their dependency.
- Finish with remaining subject, capture, background, artifact, and highest-risk drift controls.

Selected modules contribute evidence candidates, not mandatory prose. The output composer merges them by semantic slot before drafting; module count must not determine prompt length.

Assign one clause owner to each emitted semantic slot. Normally state its affirmative target once; a second clause is justified only when it supplies a distinct high-risk boundary rather than repeating the target through synonyms.

Use compact paragraphs or short blocks for complex images. Apply no fixed global word cap; every additional clause must add a new control. Keep essential crop, partial visibility, and interaction requirements affirmative. Relate each major component to another component or stable zone, and state inversion-prone side, containment, contact, or support directly.

For a high-salience look, put one compact Aesthetic Signature before fine inventory and use only source-supported causal axes. For a neutral look, use one or two ordinary cues. Preserve major-region hierarchy by relative area, tonal or material role, edge contact, legibility, and first attention even when flexible pose or placement changes.

When face likeness is selected, use one dedicated, scale-appropriate passage. A broad person-gestalt anchor may lead it but cannot replace visible geometry or raise beauty polish.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

When a negative prompt is supported, reject only likely concept and fidelity drift. Keep it compact and image-specific; do not duplicate the positive prompt or use negatives to counter an overstrong positive cluster. Rewrite the positive wording to source-relative strength first.

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

Include only real controls of the named generator. Separate source dimensions from the requested target size. Omit irrelevant fields, read `references/model-adapters.md` before naming values, and keep visual locks in `PROMPT:`.

## Diagnostic mode

For `diagnostic`, state the source-supported proposition or appeal directly, then explain its visible form, surface, light, color, hierarchy, spatial, and capture mechanisms. Keep diagnostic appeal language separate from render instructions: a candidate prompt receives bounded observable mechanisms, not copied evaluative intensity. Separate invariants from flexible pose or placement; include a candidate prompt only when useful.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.
