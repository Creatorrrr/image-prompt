# Behavior evaluation for reverse-image-prompt

Read this reference only when evaluating or revising the skill. It is not part of an ordinary prompt-extraction route.

## Evaluation boundary

Structural validation proves that modules, anchors, routes, and generated bundles are consistent. It does not prove that a prompt preserves perceptual salience or that a rendered image resembles the source. Report these layers separately:

1. package and routing validity
2. salience-plan validity
3. prompt-level fidelity
4. rendered-pixel fidelity
5. user judgment

An undelivered render is unscored, not a visual-quality failure. A single stochastic success is evidence for that attempt, not general superiority.

## Held-out case design

Do not derive the evaluation set from one reported failure. Use raw images or artifacts that were not used to write the current correction and cover materially different subjects, media, and dominant fidelity modes.

Across the evaluation suite, include matched transformation pairs. They are not mandatory extra inputs for each independent single-source pass, and an evaluator must not invent or retrieve a second source outside that pass's scope:

- **Invariant-preserving pair:** the primary appeal or proposition remains stable while a flexible dimension such as minor pose, viewpoint, placement, or incidental capture changes.
- **Aesthetic-changing pair:** object inventory stays substantially similar while a primary form, surface, light-to-form, color, hierarchy, topology, or information invariant changes.

The first pair should retain the primary salience signature without overlocking the flexible change. The second should produce a meaningfully different primary signature instead of collapsing to an object list.

Balance appearance-led cases with relationship-led, information-led, mixed, neutral, photographic, and non-photographic cases. Include both human and non-human subjects when those routes are in scope. The current motivating case may remain one regression sample, but its subject parts, colors, garments, pose, or desired values must not become runtime defaults or expected wording.

## Independent prompt pass

For a before/after comparison, give each arm only the raw request, source artifact, applicable skill snapshot, and normal runtime tools. Do not reveal the suspected bug, proposed fix, expected answer, prior prompt, or prior render.

For each arm:

1. Record the internal plan in the schema from `SKILL.md` without exposing it to the downstream image generator.
2. Draft the standalone prompt. When color/tone or lighting/light-to-form is material, update each routed contract's `emitted_controls` from literal excerpts of that final draft rather than anticipated wording.
3. Validate the reconciled plan with `python tools/salience_plan.py PLAN.json` when a persisted evaluation artifact is appropriate.
4. Freeze the authored prompt before generation.
5. Compare prompt semantics without requiring shared wording or headings.

For matched image pairs, serialize both plans and run:

```bash
python tools/salience_plan.py BASE.json --compare VARIANT.json --relation invariant-preserving
python tools/salience_plan.py BASE.json --compare VARIANT.json --relation aesthetic-changing
```

The plan checker verifies ownership, source-relative strength, appeal/render separation, flexible-dimension handling, major-region evidence, and unsupported prior clusters. It cannot determine whether the visible evidence was interpreted correctly.

### Persisted evaluation schema

Use source-relative identifiers rather than required wording. The evaluator may add entries when a genuinely layout-dense or mixed case needs them; the schema has no fixed global prompt or invariant count.

```json
{
  "direct_appeal_read": "diagnostic-only explanation",
  "render_contract": {
    "mode": "appearance-led",
    "invariants": [
      {
        "id": "semantic-slot-id",
        "axis": "form",
        "role": "primary",
        "observation": "source-relative visible target",
        "causal_origin": "intrinsic",
        "target_strength": "moderate",
        "source_evidence": ["visible evidence"],
        "clause_owner": "module-or-composer-id"
      }
    ],
    "flexible_dimensions": ["minor-placement"],
    "major_regions": [
      {
        "id": "region-id",
        "role": "dominant",
        "relative_area": "medium",
        "attention": "primary",
        "source_evidence": ["visible evidence"]
      },
      {
        "id": "supporting-region-id",
        "role": "supporting",
        "relative_area": "large",
        "attention": "background",
        "source_evidence": ["comparative visible evidence"]
      }
    ],
    "candidate_claims": [
      {
        "id": "claim-id",
        "semantic_slot": "semantic-slot-id",
        "owner": "module-or-composer-id",
        "role": "primary",
        "polarity": "affirmative",
        "target_strength": "moderate",
        "source_kind": "translated-causal-control",
        "source_evidence": ["visible evidence"],
        "emit": true
      }
    ],
    "prior_clusters": [
      {
        "id": "aggregate-prior-id",
        "claim_ids": ["claim-id"],
        "source_supported": true
      }
    ]
  }
}
```

Valid axes, causes, strengths, roles, and comparison relations are defined by `tools/salience_plan.py`. A negative emitted claim must be a distinct high-risk drift boundary; it cannot serve as a counterweight for an overstrong affirmative cluster.

### Optional Color/Tone Contract schema

When a persisted plan contains a color invariant or the routed `detail.color-tone-fidelity` module, add a source-relative `color_tone_contract`. Values below describe structure, not required wording or desired colors:

```yaml
color_tone_contract:
  importance: primary | supporting
  observation_scope: source-visible | color-managed | user-specified
  global:
    cast_or_palette_shift: "observed, absent, mixed, or uncertain behavior"
    exposure_behavior: "source-relative exposure response"
    contrast_and_tone_curve: "global and local tone behavior"
    processing_shift: "visible grading or processing behavior"
    source_evidence: []
  displayed_tone_response:
    - region_id: "known region id or global"
      axis: displayed-key-level | shadow-floor | highlight-rolloff | microcontrast
      class: "axis-specific controlled class"
      role: primary | supporting
      confidence: high | medium | low
      emission: required | diagnostic-only
      aggregate_effect_id: "required only when emission is required"
      non_emission_reason: "required only when diagnostic-only"
      source_evidence: []
  regions:
    - id: "region id"
      role: dominant | supporting | edge-frame | low-legibility
      intrinsic_axes:
        - axis: value | chroma | hue
          role: primary | supporting
          evidence_scope: highlight | midtone | shadow | flat | mixed
          observation: "source-relative observation"
          confidence: high | medium | low
          emission: required | diagnostic-only
          aggregate_effect_id: "required only when emission is required"
          non_emission_reason: "required only when diagnostic-only"
          source_evidence: []
      tone_zones:
        - zone: highlight | midtone | shadow | flat
          observation: "source-relative response"
          confidence: high | medium | low
          source_evidence: []
      relative_relations: []
      source_evidence: []
  neutral_anchor_status: available | unavailable | uncertain
  uncertainty_note: "required when no reliable neutral anchor is available"
  neutral_anchors:
    - region_id: "known region id"
      confidence: high | medium | low
      source_evidence: []
  surface_color_language:
    policy_id: "versioned policy id"
    policy_status: uncalibrated-language-prototype | model-calibrated
    observation_scope: source-visible | color-managed | user-specified
    profile_status: "observed profile state"
    region_id: "known region id"
    source_evidence: []
    axis_classification:
      value_depth: {term: very-light | light | medium | deep | uncertain, confidence: high | medium | low}
      chroma: {term: very-low | low | moderate | rich | uncertain, confidence: high | medium | low}
      undertone: {term: rosy | peach | neutral | golden | olive | mixed | uncertain, confidence: high | medium | low}
      finish: {term: matte | satin | luminous | dewy | uncertain, confidence: high | medium | low}
      evenness: {term: even | naturally-varied | freckled | uncertain, confidence: high | medium | low}
    friendly_label_review:
      - phrase: "<user-or-vocabulary-supplied-label>"
        candidate_source:
          kind: user-supplied | versioned-vocabulary
          reference: "request field, vocabulary id, or artifact reference"
        label_scope: value-depth | undertone | surface-finish | composite-appearance
        axis_requirements: {}
        matched_axes: []
        conflicting_axes: []
        unresolved_axes: []
        review_status: compatible | conflicting | inconclusive
  claim_ids: []
  aggregate_effects:
    - id: "canonical effect id"
      region_id: "known region id or global"
      axis: value | chroma | hue | contrast | displayed-key-level | shadow-floor | highlight-rolloff | microcontrast
      direction: "canonical source-relative direction"
      role: primary | supporting
      target_strength: subtle | moderate | strong
      claim_ids: []
      source_supported: true
      source_evidence: []
  emitted_controls:
    - id: "control id"
      prompt_excerpt: "literal excerpt copied from the final production prompt"
      claim_id: "one listed emitted claim id"
      causal_layer: intrinsic | illumination | global-cast | exposure | processing | hierarchy
      control_role: axis-control | compound-control
      region_id: "required for axis-control"
      axis: value | chroma | hue | contrast | displayed-key-level | shadow-floor | highlight-rolloff | microcontrast
      compound_justification: "required only for compound-control"
      aggregate_effect_ids: ["every aggregate effect referenced by that claim"]
  appearance_metaphors:
    - phrase: "optional appearance shorthand"
      status: explanation-only | unverified | model-calibrated
      emit: false
      decomposed_control_ids: []
```

Every claim listed by the contract carries `perceptual_effects`, each naming one aggregate effect, one causal layer (`intrinsic`, `illumination`, `global-cast`, `exposure`, `processing`, or `hierarchy`), confidence, and evidence. Claims sharing a region, axis, and direction use one canonical effect even when their semantic-slot names differ. Repeating one causal layer is a merge failure. Multiple causal layers are valid only when each layer and their combined pull are independently source-supported.

Every listed color/tone claim is represented exactly once in `emitted_controls`. Its literal final-prompt excerpt must match that claim's sole causal layer and complete aggregate-effect set. Every required intrinsic or displayed-tone axis links to one same-region/same-axis effect and its own axis-control. A compound-control may compress secondary evidence but cannot satisfy a required axis. The structural validator checks ownership and consistency; the reviewer verifies that the excerpt was copied literally and that no omitted phrase elsewhere in the prompt also changes color or tone.

`surface_color_language` is optional unless measured surface color is being translated or an externally supplied friendly label is considered. Classify value depth, chroma, and undertone independently; finish and evenness require separate visual evidence. Every reviewed label records whether it came from the user or an explicitly versioned task vocabulary plus a non-empty reference. The skill must not invent the candidate. A compatible review does not by itself authorize prompt emission. Any emitted friendly label must also be `model-calibrated`, carry calibration evidence, and summarize already-owned literal axis controls.

The schema deliberately contains no preferred hue, skin value, palette, metaphor, adjective blacklist, numeric color, identity proxy, or generator workaround. A hierarchy-layer hue effect additionally requires source evidence that hue contrast itself is invariant.

### Optional Light/Form Contract schema

When a persisted plan contains a primary `light-to-form` invariant or the routed `detail.light-form-fidelity` module, add the source-relative `light_form_contract` defined in `references/lighting-reproduction-evaluation.md`. Keep that schema in the dedicated reference rather than duplicating it here.

The contract records the visible result before a confidence-rated source hypothesis, then region effects, shadow ownership, material response, pose dependence, aggregate effects, and literal final-prompt controls. Candidate claims use `lighting_effects`, not the Color/Tone contract's `perceptual_effects`.

Every listed lighting claim is represented exactly once in `emitted_controls`. A low-confidence physical-light hypothesis cannot carry an emitted source-geometry or fill control; use result-space effects or keep it diagnostic. Global tonal range and local form contrast remain distinct. The same claim or literal excerpt cannot be owned independently by both the Light/Form and Color/Tone contracts.

`lighting_language` and `lighting_labels` are optional. When present, the controlled summary is reconstructed from independently classified source-visible axes and remains explanation-only. Named friendly-label candidates require user or explicitly versioned-vocabulary provenance; compatibility is recalculated from their declared axis requirements. Emission additionally requires exact generator/version calibration and links to already-owned literal controls.

## Prompt-level rubric

Review the standalone prompt with the source visible and score distinct questions:

- Does the first-order proposition survive without the source image?
- Are primary invariants expressed affirmatively at their source-relative strength?
- Are flexible dimensions allowed to vary without becoming primary locks?
- Does each semantic slot have one owner rather than repeated synonymous emphasis?
- Are intrinsic properties separated from pose/deformation, perspective, lighting/shadow, material interaction/occlusion, and processing?
- Are intrinsic surface color, illumination, global cast, and exposure kept distinct?
- When color or tone is material, are value, chroma, hue, tone-zone response, processing, and neutral-anchor confidence represented at source-relative strength?
- Are displayed key level, shadow floor, highlight rolloff, and microcontrast kept distinct rather than collapsed into `light intensity`?
- Does every required intrinsic axis continue through a same-region/same-axis effect and literal intrinsic axis-control, instead of being replaced by hierarchy, exposure, or illumination?
- Does every required displayed-tone axis continue through its own effect and axis-control without substituting for a Light/Form spatial axis?
- Is displayed intrinsic color based on comparable midtone or flat evidence rather than a pooled highlight/midtone/shadow range?
- Is the observation scope limited to what the image/profile evidence supports rather than claiming biological, material, or scene-referred true color?
- Was each appearance metaphor decomposed before use, and does any retained metaphor merely summarize rather than add color, finish, illumination, or polish?
- When friendly surface-color language is used, were value depth, chroma, and undertone classified first, with ambiguous or conflicting labels left non-emitted?
- Does every literal color-changing phrase in the final prompt appear once in the control ledger with one causal layer and a complete effect budget?
- Do differently named claims avoid accumulating the same color or tone direction beyond one supported aggregate target?
- When lighting is material, is the visible result recorded before the physical-light hypothesis, with confidence and evidence for any emitted source geometry?
- Are apparent source size, fill, global tonal range, bright-plane coverage, local form contrast, gradient extent, shadow ownership, material response, and background spill kept causally distinct?
- When compact lighting language is used, were displayed key, shadow floor, edge softness, local form contrast, bright-plane coverage, gradient extent, directionality, and fill classified independently before the summary, with unresolved or conflicting labels left non-emitted?
- Does any emitted friendly lighting label have external provenance, exact generator/version calibration, and immediate literal decomposition without adding a second lighting direction?
- Does every literal lighting-changing phrase appear once in the Light/Form control ledger with one owner and a complete effect set?
- When pose or geometry is flexible, does the prompt preserve the light-to-form relation without overlocking incidental highlight coordinates?
- Do the Light/Form and Color/Tone contracts avoid duplicate claims, excerpts, and contrast directions?
- Does the major-region area and attention hierarchy survive?
- Do combined quality, lighting, surface, framing, and style cues import an unsupported category default?
- Is the fidelity ceiling preserved without polishing, sharpening, completing, or normalizing the source?

Do not award success because required terminology, headings, or anchor phrases appear. Judge the resulting control hierarchy and likely generator behavior.

## Pixel evaluation

Use matched generator, settings, aspect ratio, reference handling, and attempt policy across arms. Keep prompts frozen within each arm. When resources permit, use more than one independent render so stochastic variation is not mistaken for a causal improvement.

Blind the arm mapping and review both thumbnail and native scale. Score at least:

- primary proposition readability
- invariant preservation
- flexible-dimension tolerance
- major-region and attention hierarchy
- form versus induced-light/perspective fidelity
- color and light causality
- surface and material role
- fidelity-ceiling or polish drift
- category-prior drift

For color- or tone-critical cases, additionally score source-relative region value, chroma, hue direction, highlight/midtone/shadow or flat-field response, neutral-anchor drift, global cast, exposure, and processing. Prefer relative region comparisons over exact pixel equality when geometry, stochastic texture, or lighting placement varies. Record embedded-profile status and any assumed display space when measurement is used.

When persisted measurement is warranted, use `color_probe.py --spec` to retain independently selected source/render bounds, semantic group roles, and tone zones. Use `color_fidelity_eval.py` to separate contextual shared movement from target-local residual. Without a justified acceptance policy, record the result as `unscored`; do not promote a structural PASS to a pixel PASS.

For lighting-critical comparisons, read `references/lighting-reproduction-evaluation.md`. Use `light_probe.py` only with analyst-selected regions, relations, and profiles to compare regional lightness, local gradient amplitude, transition width, material response, and background spill. The probe cannot identify semantics, infer a rig, or declare fidelity.

When comparing a source and render, include multiple analyst-selected patches from the target surface and at least one contextual or neutral group where the image permits it. Check whether drift is shared across groups before labeling it intrinsic or global; do not infer semantics from coordinates or patch names.

Include held-out causal pairs spanning materially different subjects and media:

- the same intrinsic surface under different illumination
- different intrinsic surfaces under comparable illumination
- similar hue with changed exposure, chroma, or tone curve
- the same local form contrast at different displayed key levels
- the same displayed key level with different bright-plane coverage or shadow floor
- local colored illumination versus a global cast or palette shift
- low saturation versus simple underexposure
- monochrome, flat-color, mixed-light, photographic, and non-photographic sources
- human and non-human subjects without making either category the runtime default
- the same displayed target relation under different global exposure or cast
- a color/finish metaphor versus an axis-equivalent description across human and non-human surfaces
- the same undertone class across different value-depth classes, including olive without treating it as a depth category
- boundary and missing-profile cases where no friendly label should be forced
- embedded-profile, missing-profile, and failed-profile cases
- local target drift versus a shared target-and-context drift
- large near-axis versus large off-axis illumination
- small near-axis versus small off-axis illumination
- high global tonal range with low local form contrast, and the inverse
- the same light with changed geometry or pose
- cast, self, contact-occlusion, material-response, and processing-owned darkness
- diffuse, absorbent, glossy, metallic, translucent, and woven material response
- identical core lighting axes with unrelated subjects and media, so a controlled summary remains stable without becoming a preferred preset
- one-axis lighting changes that keep the other axes fixed, especially edge softness versus local form contrast and displayed key versus bright-plane coverage
- compatible, conflicting, inconclusive, missing-candidate, and stale-generator-calibration label cases

The motivating image may remain one regression sample, but promotion requires improvement across this causal matrix. Use optional multi-region measurements only as diagnostic evidence; never turn one sample's numeric values or wording into runtime expectations.

For generator control-effectiveness evaluation, change one axis-control at a time and record the exact model/version, settings, reference handling, repeated-render median movement, variance, and unintended-axis leakage. Include both human and non-human surfaces. A response table is stale when the model version or relevant conditioning route changes.

Promote a change only when it improves unrelated held-out behavior without material regression in other dominant modes. Keep package PASS, prompt PASS, delivered pixels, pixel fidelity, and user preference as separate claims.

## Anti-overfitting guardrails

- Put source-relative axes and causal distinctions in runtime instructions, not example-specific desired values.
- Do not add a fixed adjective blacklist, fixed global word count, exact source proportions, or generator-specific workaround to solve one case.
- Do not install a preferred human color, demographic-to-color mapping, fixed image-specific metaphor dictionary, or subject-specific measurement region. A versioned source-visible axis vocabulary is allowed only when it records uncertainty and does not select a preferred label.
- Do not place named friendly-label examples or concrete preferred axis combinations in runtime instructions. Keep semantic label cases in held-out tests, and require runtime candidates to carry user or versioned-vocabulary provenance.
- Do not install a preferred source direction, fill level, light-to-form strength, shadow owner, material response, or subject-specific lighting coordinate.
- Do not install named friendly lighting-label examples, preferred composite-light combinations, or one generator's response as universal semantics. Runtime candidates require external provenance; generator calibration expires with the relevant model/version or conditioning route.
- Prefer changing the merge or attribution rule over adding another subject exception.
- Corrections replace or remove amplifying claims; they do not accumulate counter-negatives.
- Treat one case as a regression sample, never as proof that a general rule succeeds or fails everywhere.
