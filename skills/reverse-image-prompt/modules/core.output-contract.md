---
id: core.output-contract
version: 9
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
---

# Core: adaptive output contract

## When to load

Always. Apply after the visual analysis and routed modules.

## PROMPT

Emit only sections required by the selected output mode.

For a generation request, always emit:

```text
PROMPT:
...
```

Write a standalone English prompt whose order follows the dominant fidelity axis:

- Start every mode with the frame shape, medium, fidelity ceiling, and one-sentence primary perceptual proposition.
- **Relationship-led:** establish composition, crop, major zones, topology, interaction geometry, and up to five critical spatial anchors before local appearance.
- **Appearance-led:** establish the compact Aesthetic Causal Signature and source-specific subject form, surface, light-to-form, color, and hierarchy before secondary pose coordinates or inventory.
- **Information-led:** establish layout, reading order, information hierarchy, legibility, and container relationships before decorative styling.
- **Mixed:** name the two co-primary invariants early and interleave only the cues needed to show how they depend on each other.
- Finish with remaining subject detail, camera/rendering behavior, background, meaningful artifacts, and only the highest-risk drift constraints.

Use short labeled blocks or compact paragraphs for complex images. Aim for the smallest prompt that preserves the source hierarchy; a typical prompt should not need every possible camera, anatomy, lighting, and settings field.

Keep essential requirements affirmative. Prefer `only a narrow cropped strip remains visible` over relying on `do not expand the strip` in another section.

Relate every major component or coherent group to another component or stable scene zone. Keep each concept-critical side, containment, contact, and support relation in `PROMPT:` as one compact affirmative sentence. Do not leave it implied only by an action verb, approximate coordinate, or negative prompt.

For a high-salience look, keep one compact Aesthetic Signature in the first or second paragraph before fine face, material, or background inventory. Use three to six source-supported causal cues spanning only material form, surface, light-to-form, tone/color, sharpness, or hierarchy axes. For a neutral look, use one or two cues without a labeled block. Do not fill every axis or repeat the signature through synonyms.

When `detail.human-face-likeness` is selected, keep one dedicated likeness passage. If `subject.human` selects a broad person-gestalt anchor, place that one compact anchor at the start of the passage, then immediately constrain it with scale-appropriate visible anchors. Never use demographic, beauty, or character shorthand as the whole likeness description.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

Use one compact, image-specific list. Do not duplicate the entire prompt. Include only likely failure modes that are difficult to express affirmatively.

When a negative prompt is supported, reject only likely concept and fidelity drift.

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

- Include only fields that map to real controls of the target generator.
- Separate source dimensions from the requested target size.
- Omit irrelevant fields instead of filling them with prose.
- Read `references/model-adapters.md` before naming model-specific values.
- Keep visual locks in `PROMPT:`, not in settings.

## Diagnostic mode

For `diagnostic`, first state the source-supported perceptual proposition or appeal directly in the user's language, then explain the form, surface, light, color, hierarchy, spatial, and capture mechanisms that create it. Separate invariants from pose or placement details that may vary. A candidate `PROMPT:` may follow, but do not force generation-only sections.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.
