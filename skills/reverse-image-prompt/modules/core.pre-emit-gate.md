---
id: core.pre-emit-gate
version: 20
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
  - causal_color_phrase_scope
  - final_color_control_ledger
  - intrinsic_axis_emission_coverage
  - axis_control_separability
  - light_form_causal_consistency
  - unowned_lighting_claim_audit
  - global_local_contrast_separation
  - shadow_owner_coverage
  - final_light_control_ledger
---

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

Apply this as a rewrite pass, not a checklist appended to the draft.

### Coverage and ownership

- Confirm that `PROMPT:` contains the primary visual concept.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner.
- Give each primary invariant one affirmative control; keep flexible dimensions supporting. Order by the dominant fidelity axis.
- Give each generic effect one claim and exact prompt control; keep specialized ledgers separate.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. Plausible cues still fail when combined too strongly.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Keep one distinct high-risk boundary per slot.
- Check whether a secondary element receives more words than its visible importance supports; compress it when it competes with a primary invariant.
- Rewrite unsupported category defaults from evidence.

### Causal, color, and tone consistency

- Keep form, surface, light, color, material, and hierarchy causally consistent; do not encode induced effects as intrinsic.
- Audit shared perceptual effects across semantic slots, causal layers, paragraphs, negatives, and settings. Slot names being unique does not make repeated value, chroma, hue, or contrast directions independent.
- For a material color or tone effect, verify one aggregate source-relative target and the evidence for every emitted intrinsic, illumination, global-cast, exposure, processing, or hierarchy contribution. Merge or delete a contribution whose causal layer lacks independent evidence.
- Assign every appearance-changing color or tone phrase to one causal layer; treat free-floating mood or color adjectives as unowned claims and rewrite them from observable axes.
- Split an ambiguous color phrase when one modifier could silently control intrinsic surface, illumination, exposure, or processing at the same time.
- Re-read the exact final `PROMPT:` rather than trusting the analysis plan. Reconcile every exact color-changing excerpt in the final prompt with one emitted claim, one causal layer, and its complete aggregate effect budget. Split, replace, or delete any unowned excerpt, repeated direction, or multi-layer compound.
- For every required intrinsic value, chroma, or hue observation, trace one uninterrupted path from region axis to same-region/same-axis aggregate effect, emitted claim, and intrinsic axis-control. A relative hierarchy, exposure, illumination, or processing clause cannot satisfy missing intrinsic surface value or chroma.
- Give an axis-control one region and one perceptual axis. If one phrase changes several axes, split its literal excerpts or mark it as a justified secondary compound-control; never use a compound-control to satisfy a required intrinsic axis.
- Keep midtone or flat evidence that establishes displayed intrinsic color separate from highlight and shadow evidence that establishes tone response. Mixed tone-zone evidence may remain diagnostic but cannot drive an intrinsic axis-control.
- For every routed human, require explicit person-prior and skin-surface decisions. Emitted priors need visible geometry; emitted controlled descriptors must deterministically wrap separately owned axes. Friendly metaphors remain explanation-only without exact generator/version evidence.
- Check global cast against reliable neutral or multi-region evidence; otherwise retain uncertainty.

### Lighting and light-to-form consistency

- For material lighting, verify one source-relative Light/Form target and evidence for every emitted source-geometry, fill, local-form-contrast, shadow-topology, material-response, or background-spill contribution.
- Assign every lighting-changing phrase to one Light/Form owner. Split multi-owner compounds.
- Keep global tonal range and local form contrast as separate effects. Merge synonymous directions.
- Give every material shadow event a source-supported owner or mark it mixed or uncertain. Do not infer source direction from contact, occlusion, absorption, or processing.
- The visible spatial result outranks a rig hypothesis; a low-confidence cause cannot carry a primary invariant alone.
- Reconcile every exact lighting-changing excerpt with one emitted claim, one owner, and its complete lighting-effect list. Keep spatial Light/Form effects separate from Color/Tone.
- Keep controlled lighting summaries diagnostic. Emit one externally sourced label only with compatible axes, exact generator/version calibration, and literal decomposition.
- When pose or geometry may vary, preserve the source-supported light-to-form relation while allowing non-invariant highlight coordinates to move.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Then audit `spatial-orientation/v2`: placement cannot cover orientation; human subaxes need cue-linked dispositions and a neutral-alignment counterfactual. Invariants need a full relation/control path; non-invariants need a preservation or visibility reason and emit nothing. Delete unsupported axial normalization by net clause meaning, not a word blacklist.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Retain scale-appropriate face evidence: selective likeness anchors when readable, only orientation, hair mass, tone, and visibility when small or obscured.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions. Report prompt-only limits honestly; before generation, audit the reconciled plan and final prompt; separate setting and pixel evidence.

## Length and clarity

- Prefer one concrete statement for a secondary element and add a boundary only for a distinct high-risk failure.
- If the prompt reads as a checklist, rewrite around the proposition, causal cues, and source hierarchy.
