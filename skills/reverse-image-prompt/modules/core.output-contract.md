---
id: core.output-contract
version: 8
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

Write a standalone English prompt in a skimmable order:

1. Scene, frame shape, medium, fidelity ceiling, primary concept, and any high-salience Aesthetic Signature.
2. Composition, crop, subject scale, major zones, major-component spatial topology, and up to five critical spatial anchors.
3. Subject appearance, pose, gaze, interaction geometry, contact/support, occlusion, and completion boundaries.
4. Camera or rendering behavior, lighting, color, focus, texture, and meaningful artifacts.
5. Compact constraints covering only the highest-risk drift.

Use short labeled blocks or compact paragraphs for complex images. Aim for the smallest prompt that preserves the source hierarchy; a typical prompt should not need every possible camera, anatomy, lighting, and settings field.

Keep essential requirements affirmative. Prefer `only a narrow cropped strip remains visible` over relying on `do not expand the strip` in another section.

Relate every major component or coherent group to another component or stable scene zone. Keep each concept-critical side, containment, contact, and support relation in `PROMPT:` as one compact affirmative sentence. Do not leave it implied only by an action verb, approximate coordinate, or negative prompt.

For a high-salience look, keep one compact Aesthetic Signature in the first or second paragraph before fine face, material, or background inventory. Use three to six source-supported anchors spanning only the dominant tone, color, sharpness, optical/surface, lighting, or hierarchy axes. For a neutral look, use one or two cues without a labeled block. Do not fill every axis or repeat the signature verbatim.

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

For `diagnostic`, explain the evidence and uncertainties in the user's language. A candidate `PROMPT:` may follow, but do not force generation-only sections.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary relationship, crop, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.
