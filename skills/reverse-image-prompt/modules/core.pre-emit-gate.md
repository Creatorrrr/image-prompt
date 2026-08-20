---
id: core.pre-emit-gate
version: 9
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
  - semantic_salience_amplification
---

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

- Confirm that `PROMPT:` contains the primary visual concept, dominant fidelity axis, aesthetic invariants, and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Verify that the first-order proposition leads the prompt: relationship geometry for relationship-led images, form/surface/light/hierarchy for appearance-led images, and layout/legibility for information-led images. Do not overlock dimensions marked flexible.
- Preserve source hierarchy. Check whether a secondary element receives more words than its visible importance supports. Compress secondary pose, material, accessory, or micro-detail when it receives more emphasis than a primary invariant.
- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- State the image's core proposition in one sentence and its causal signature in two to four cues. If that summary is unclear or the cues disagree, rewrite before adding detail.
- Confirm that form, surface, light-to-form, color, material roles, and hierarchy all support the same proposition rather than importing unrelated attractive defaults.
- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer evidence; use at most five unless a layout-dense UI or diagram materially benefits.
- Relate every major component or coherent group to another component or stable zone. For concept-critical interactions, make side, contact, support, containment, and depth order explicit enough to prevent a plausible inversion; distinguish 2D overlap from scene-space contact.
- Keep each primary mass in its source-visible region and every partial or edge-adjacent body, garment, object, reflection, screen, poster, or text block incomplete. Distinguish hair-outline crop from facial-feature crop.
- If the look is high-salience, place its compact Aesthetic Signature before fine detail and keep the cues mutually compatible. For a neutral look, remove the unnecessary signature.
- Confirm that descriptive detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Remove unsupported `shallow depth of field`, beauty lighting, premium bokeh, clean capture, body-type, garment, genre, or other prior-heavy labels unless visible mechanisms constrain their default pull.
- If a human face is prominent and readable, confirm the prompt includes a selective, scale-appropriate likeness set covering the strongest visible face geometry, expression/gaze, hair boundary, and surface/lighting cues. If one broad person-gestalt anchor materially reduces ambiguity, place it before—not instead of—the likeness set; ensure it remains an approximation rather than an identity claim and does not raise beauty polish.
- If a human face is small, soft, shadowed, or heavily occluded, remove speculative micro-features and preserve only reliable head orientation, hair mass, tone, and visibility.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and generic quality assumptions.
- Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams are unlikely to reproduce reliably.

## Length and clarity

- Prefer one measured statement plus one drift constraint for a secondary element.
- Keep constraints concrete and observable; do not repeat locks merely to look exhaustive.
- If the prompt has become a field checklist, rewrite around the dominant proposition, its causal cues, and source hierarchy.
