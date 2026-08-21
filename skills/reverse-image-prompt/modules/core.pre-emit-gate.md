---
id: core.pre-emit-gate
version: 11
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
  - cross_slot_perceptual_effect_audit
  - color_tone_causal_consistency
  - unowned_appearance_claim_audit
---

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

Apply this as a rewrite pass, not a checklist appended to the draft.

### Coverage and ownership

- Confirm that `PROMPT:` contains the primary visual concept, dominant fidelity axis, aesthetic invariants, and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner.
- Give every primary invariant one affirmative render control; keep flexible dimensions supporting. Lead with topology for relationship-led, appearance for appearance-led, and layout/legibility for information-led images.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. Plausible cues still fail when their combined pull exaggerates an invariant.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Keep at most one distinct high-risk boundary per slot.
- Preserve source hierarchy. Check whether a secondary element receives more words than its visible importance supports; compress it when it competes with a primary invariant.
- Audit prior-heavy quality, lighting, surface, framing, and style language as one cluster; rewrite unsupported category defaults from evidence.

### Causal, color, and tone consistency

- Keep form, surface, light-to-form, color, material roles, and hierarchy causally consistent. Do not encode induced effects as intrinsic, and translate direct appeal into observable controls.
- Audit shared perceptual effects across semantic slots, causal layers, paragraphs, negatives, and settings. Slot names being unique does not make repeated value, chroma, hue, or contrast directions independent.
- For a material color or tone effect, verify one aggregate source-relative target and the evidence for every emitted intrinsic, illumination, global-cast, exposure, processing, or hierarchy contribution. Merge or delete a contribution whose causal layer lacks independent evidence.
- Assign every appearance-changing color or tone phrase to one causal layer; treat free-floating mood or color adjectives as unowned claims and rewrite them from observable axes.
- Check global cast against reliable neutral or multi-region evidence; otherwise retain uncertainty and relative relations. Keep hierarchy to area, value, chroma, or contrast unless hue contrast itself is invariant.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Remove conflicting numeric anchors; use at most five unless a dense UI or diagram benefits.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Retain scale-appropriate face evidence: selective likeness anchors when readable, only orientation, hair mass, tone, and visibility when small or obscured.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions. Report prompt-only limits honestly for unreliable exact details.

## Length and clarity

- Prefer one concrete statement for a secondary element and add a boundary only for a distinct high-risk failure.
- If the prompt reads as a checklist, rewrite around the proposition, causal cues, and source hierarchy.
