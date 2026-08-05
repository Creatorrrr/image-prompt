---
id: core.pre-emit-gate
version: 8
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

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

- Confirm that `PROMPT:` contains the primary visual concept and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Preserve source hierarchy: dominant concept first, primary subject and interaction next, secondary elements last.
- Check whether a secondary element receives more words than its visible importance supports. Compress it when it does.
- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer visible spatial evidence.
- Use at most five numeric anchors unless the source is a layout-dense UI or diagram and numeric bands materially help.
- Confirm that every major component or coherent group has at least one explicit spatial relation to another component or stable scene zone; no major element should remain a free-floating inventory item.
- For every concept-critical interaction, confirm that the relevant side or zone, any contact parts, support role, containment, and depth order are explicit enough to prevent a plausible spatial inversion.
- Distinguish image-plane overlap from scene-space contact or support. A bare interaction verb is insufficient when the subject could be placed on the wrong side of a boundary while still satisfying the verb.
- Confirm that each primary subject's main mass remains in the source-visible region and that only visibly crossing or overlapping parts cross a barrier, opening, frame, edge, or support surface.
- Confirm every partial or edge-adjacent region remains partial; do not let wording imply a completed body, garment, object, reflection, screen, poster, or text block.
- Distinguish head/hair cropping from actual facial-feature cropping.
- If the source look is high-salience, confirm that its compact Aesthetic Signature appears before fine subject detail and that its anchors agree rather than mixing incompatible clean, hazy, sharp, flat, cinematic, casual, or studio defaults.
- Confirm that descriptive detail has not increased subject scale, local sharpness, background legibility, retouching, microcontrast, or lighting polish beyond the source.
- Remove `shallow depth of field`, beauty lighting, premium bokeh, clean digital capture, or other category defaults unless their visible mechanisms are actually supported.
- If a human face is prominent and readable, confirm the prompt includes a selective, scale-appropriate likeness set covering the strongest visible face geometry, expression/gaze, hair boundary, and surface/lighting cues. If one broad person-gestalt anchor materially reduces ambiguity, place it before—not instead of—the likeness set; ensure it remains an approximation rather than an identity claim and does not raise beauty polish.
- If a human face is small, soft, shadowed, or heavily occluded, remove speculative micro-features and preserve only reliable head orientation, hair mass, tone, and visibility.
- Remove repeated constraints that appear unchanged in the prompt, negative prompt, and settings.
- Remove unsupported camera, lens, identity, brand, artist, or hidden-content assumptions.
- Remove generic quality words that would raise polish above the selected intent mode.
- Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams are unlikely to reproduce reliably.

## Length and clarity

- Prefer one measured statement plus one drift constraint for a secondary element.
- Keep constraints concrete and observable.
- Do not repeat important locks merely to make the output look exhaustive.
- If the prompt has become a checklist of every possible visual field, rewrite around the image's actual hierarchy.
