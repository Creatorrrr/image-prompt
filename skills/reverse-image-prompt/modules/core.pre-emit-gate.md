---
id: core.pre-emit-gate
version: 2
priority: 100
type: core
tier: 0
facet: core
facet_values:
  - pre-emit-gate
  - final-output-gate
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - concept.primary-relationship
conflicts: []
provides_anchors:
  - coordinate_contradictions
  - secondary_detail_budget
  - output_gate
  - prompt_only_limits
---

# Core: pre-emit fidelity gate

## When to load

Always. Apply this gate immediately before writing the final answer.

## Rules

- Confirm that `PROMPT:` contains the primary visual concept, the relationship/effect reading when present, the source aspect ratio, crop, normalized coordinate locks, boundary locks, occlusion/completion logic, medium fidelity, and all required source-fidelity constraints.
- For coordinate-heavy prompts, audit internal contradictions before emitting. If face center, head mass, eye line, shoulder span, prop box, hand box, text mark, watermark, label, or background seam coordinates disagree with descriptive phrases such as `centered`, `slightly right`, `lower-left`, `near the face`, `below the cheek`, `wide`, `small`, `dominant`, or `secondary`, revise so the coordinates and plain-language placement describe the same image-plane layout.
- For every secondary object, background element, UI mark, text mark, cropped garment/body region, prop, strap, reflection, or partial edge band, check whether it receives more words than its visible importance supports. If it does, shrink the wording and explicitly keep it secondary, partial, low-detail, or edge-adjacent.
- Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. Lock each such region as partial or cropped in `PROMPT:` and reject completing, recentering, expanding, or clarifying it in `NEGATIVE PROMPT:`.
- Check for concept omission: if all objects are listed but the intended relationship, occlusion, reflection, screen/frame, scale contrast, mixed-media effect, or ordinary premise is missing, rewrite before emitting.
- Report prompt-only limits honestly when exact crop, pose, facial appearance, background fragments, UI/text placement, or small low-legibility details are unlikely to be reproduced from text alone.
- Assume downstream image generation may use only the `PROMPT:` body. Any non-negotiable crop, camera, boundary, appearance, garment, occlusion, and medium-fidelity constraints must appear inside `PROMPT:` in affirmative visual language, not only in `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:`.

## Prompt additions

Repeat the most important crop, coordinate, occlusion, completion, and concept locks near the beginning and again in critical fidelity locks.

## Negative additions

Reject concept omission, coordinate contradiction, common-crop normalization, expanded secondary details, completed partial regions, and upgraded clarity.

## Settings additions

- Final output gate locks:
- Prompt-only reproduction limits:
- Secondary-detail budget locks:
