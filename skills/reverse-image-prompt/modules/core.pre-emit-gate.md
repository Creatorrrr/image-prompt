---
id: core.pre-emit-gate
version: 10
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
  - semantic_claim_merge
  - net_salience_audit
  - replacement_correction
---

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

Apply this as a rewrite pass, not a checklist appended to the draft.

### Coverage and ownership

- Confirm that `PROMPT:` contains the primary visual concept, dominant fidelity axis, aesthetic invariants, and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner. Other modules may add evidence but not synonymous output clauses.
- Give every primary invariant one affirmative render control. Keep flexible dimensions supporting unless the source makes their exact state proposition-critical.
- Verify that the first-order proposition leads the prompt: relationship geometry for relationship-led images, form/surface/light/hierarchy for appearance-led images, and layout/legibility for information-led images.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. A set of individually plausible cues fails when their combined pull exaggerates an invariant or promotes a supporting axis.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Normally keep one affirmative clause per slot and only one high-risk drift boundary when it adds a distinct control.
- Preserve source hierarchy. Check whether a secondary element receives more words than its visible importance supports. Compress secondary pose, material, accessory, or micro-detail when it competes with a primary invariant.
- Audit prior-heavy language as a combined cluster. If quality, lighting, surface, framing, and style cues collectively invoke an unsupported category default, rewrite the cluster from evidence instead of blacklisting individual words.

### Causal consistency

- Confirm that form, surface, light-to-form, color, material roles, and hierarchy support one proposition. Do not encode pose, perspective, shadow, material pressure, occlusion, or processing as intrinsic shape or surface without visible evidence.
- Keep intrinsic surface color, illumination color, global cast, and exposure distinct. Remove repeated hue-direction cues owned by another slot.
- Ensure the direct appeal reading was translated into observable controls rather than copied as unbounded evaluative intensity.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer evidence; use at most five unless a layout-dense UI or diagram materially benefits.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- For a prominent readable face, retain a selective scale-appropriate likeness set. For a small, soft, shadowed, or occluded face, remove speculative micro-features and keep only reliable orientation, hair mass, tone, and visibility.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and generic quality assumptions. Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams remain unreliable.

## Length and clarity

- Prefer one measured statement for a secondary element; add a drift constraint only for a distinct high-risk failure.
- Keep constraints concrete and observable; do not repeat locks merely to look exhaustive.
- If the prompt has become a field checklist, rewrite around the dominant proposition, its causal cues, and source hierarchy.
