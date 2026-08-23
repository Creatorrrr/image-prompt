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
2. Draft the standalone prompt. Update the generic `emitted_controls` and, when color/tone or lighting/light-to-form is material, each routed contract's specialized `emitted_controls` from literal excerpts of that final draft rather than anticipated wording.
3. Validate the reconciled plan with `python tools/salience_plan.py PLAN.json --prompt PROMPT.txt`. Omitting `--prompt` validates the structured contract only.
4. For actual generation or source/render comparison, persist the plan, exact prompt and SHA-256, source and target sizes, size-binding status, reference handling, and attempt log. A prompt-only extraction may remain ephemeral.
5. Freeze the authored prompt and settings before generation.
6. Compare prompt semantics without requiring shared wording or headings.

Immediately before an actual generation call, the plan-plus-prompt audit is mandatory. The settings record names whether the requested size was `explicitly-applied`, `auto`, `unsupported`, or `unbound`; when a render is delivered, add its dimensions and the continuous source-to-delivery and target-to-delivery ratio errors. Do not compensate for an unavailable size control by increasing framing adjectives in the prompt.

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
    "component_relations": [
      {
        "id": "region-to-frame-relation",
        "kind": "frame-zone",
        "subject_region_id": "region-id",
        "frame_reference": "source-relative frame zone",
        "observation": "the dominant region keeps its source-visible frame relation",
        "role": "supporting",
        "source_evidence": ["visible frame and region boundary"]
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
        "emit": true,
        "salience_effects": [
          {
            "aggregate_effect_id": "source-relative-form-effect",
            "source_evidence": ["visible evidence"]
          }
        ]
      }
    ],
    "aggregate_effects": [
      {
        "id": "source-relative-form-effect",
        "axis": "form",
        "direction": "source-relative-form-direction",
        "role": "primary",
        "target_strength": "moderate",
        "claim_ids": ["claim-id"],
        "region_ids": ["region-id"],
        "relation_ids": ["region-to-frame-relation"],
        "source_supported": true,
        "source_evidence": ["visible evidence"]
      }
    ],
    "emitted_controls": [
      {
        "id": "generic-control-id",
        "prompt_excerpt": "literal source-relative form control",
        "claim_id": "claim-id",
        "owner": "module-or-composer-id",
        "aggregate_effect_ids": ["source-relative-form-effect"]
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

`component_relations` is sparse. Record a relation only when a region-to-region or region-to-frame relation materially affects an invariant or likely drift. Valid relations carry one source region, exactly one frame or region reference, a source-relative observation, evidence, and a role. Partial visibility additionally records the surviving fragments, cropped or hidden counterparts, and a completion risk. Every recorded relation terminates in a generic aggregate effect rather than remaining an unused diagnostic field.

### Spatial/Orientation Coverage schema

When an orientation-bearing subject is material, and always when `subject.human` is routed, add `spatial_orientation_coverage`. This is a coverage ledger, not a target-pose template:

```yaml
spatial_orientation_coverage:
  subjects:
    - id: "subject-local-id"
      kind: human | non-human | group | component
      visibility: readable | partial | indistinct
      region_id: "known major region id"
      source_evidence: []
  decisions:
    - id: "subject-and-dimension-local-id"
      subject_id: "subject-local-id"
      dimension: frame-placement | subject-principal-axis | viewpoint-elevation | viewpoint-azimuth | viewpoint-roll | viewpoint-distance-foreshortening | human-body-orientation | human-head-body-relation | human-shoulder-line | human-attention-direction | cross-component-orientation
      family: frame-placement | principal-axis | viewpoint | part-whole | attention-direction | cross-component
      disposition: invariant | flexible | not-material | not-visible | uncertain
      observation: "source-relative observation or visibility limit"
      causal_origin: pose-deformation | perspective | spatial-relation | layout
      confidence: high | medium | low
      source_evidence: []
      control_axis_id: "case-local causal control identifier"
      relation_id: "required only for invariant"
      invariant_id: "required only for invariant"
      claim_id: "required only for invariant"
      aggregate_effect_id: "required only for invariant"
      control_id: "required only for invariant"
      non_emission_reason: "required only for non-invariant dispositions"
```

Every covered subject disposes of frame placement, principal axis, the four viewpoint dimensions, and cross-component orientation. A human also disposes of body orientation, head-to-body relation, shoulder line, and attention direction even when a partial or indistinct view makes one `not-visible` or `uncertain`. `flexible` decision ids also appear in `flexible_dimensions`.

Viewpoint dimensions accept `perspective`; human body, head/body, and shoulder dimensions accept `pose-deformation`; attention accepts pose or a visible spatial relation; frame placement and cross-component orientation accept spatial relation or layout; the principal subject axis accepts spatial relation, pose, or layout. These are causal owners, not desired visual values.

An invariant decision terminates in exactly one generic component relation, invariant, affirmative claim, aggregate effect, and literal prompt control. Its aggregate effect and control carry the same `control_axis_id` and `causal_origin`. A non-invariant decision carries none of those path ids and emits no spatial control. Merge duplicate control axes before drafting, including duplicates split between camera and head pitch, frame placement and body orientation, garment boundaries and shoulder pose, or perspective-owned appearance and intrinsic form.

No disposition or dimension implies a preferred value. Centered and offset, frontal and oblique, aligned and opposed, and either mirrored direction all remain valid source-relative outcomes. Do not put case-specific coordinates, directions, body parts, garments, or adjective exclusions into runtime expectations.

For form, surface, sharpness, hierarchy, topology, and information, every emitted claim carries `salience_effects`. The top-level `aggregate_effects` merges claims by the same axis, source-relative direction, regions, and relations; one aggregate effect has one emitted generic claim. The top-level `emitted_controls` then represents each generic emitted claim exactly once with a literal excerpt from the authored prompt. Generic, Color/Tone, and Light/Form contracts may not own the same claim or exact excerpt. The checker compares declared strings and ownership; a reviewer still audits synonymous prose because the tool does not infer semantics.

An emitted broad human category or attractiveness anchor may add a `generation_prior` object to its owning claim. It records `scope`, a `candidate_source` with `kind` (`user-supplied`, `source-visible-approximation`, or `model-calibrated`) and a non-empty reference, `non_identifying: true`, `visible_geometry_evidence`, and non-empty `geometry_claim_ids`. Each ID references a separate emitted affirmative claim owned by `subject.human` or `detail.human-face-likeness`, kept in the generic ledger, and represented by exactly one prompt control. The runtime skill contains no named preferred category, and neither diagnostic evidence nor the prior clause itself can replace local face geometry.

### Human Appearance Decisions schema

Whenever `subject.human` is routed, add exactly one record for every human in `spatial_orientation_coverage.subjects`:

```yaml
human_appearance_decisions:
  - id: "case-local decision id"
    subject_id: "matching human spatial subject id"
    face_visibility: readable | partial | indistinct | not-visible | uncertain
    source_evidence: []
    person_prior:
      disposition: emit | omit | uncertain
      confidence: high | medium | low
      source_evidence: []
      claim_id: "required only for emit"
      non_emission_reason: "required for omit or uncertain"
    skin_surface:
      disposition: material | not-material | not-visible | uncertain
      confidence: high | medium | low
      source_evidence: []
      region_ids: []
      coverage: exposed | through-sheer | mixed
      descriptor_disposition: emit | omit | uncertain
      descriptor_non_emission_reason: "required unless descriptor emits"
      non_emission_reason: "required when skin is not material"
```

This is a processing-completeness contract, not an instruction to emit a category or color. A person prior may emit only for a readable or partially readable face, must own one `person-gestalt` generation prior, and remains constrained by its separate geometry controls. Material skin names one or more matching Color/Tone regions and a visible coverage state. An emitted skin descriptor targets one of those regions and requires an emitted `controlled_descriptor`; every other path records why it emits nothing. No disposition selects a race, ethnicity, nationality, value depth, undertone, or finish.

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
    controlled_descriptor:
      status: ready | inconclusive
      surface_term: "analyst-supplied visible region phrase"
      phrase: "deterministic phrase reconstructed from the included current-source axes"
      included_axes: [value_depth, chroma, undertone]
      axis_excerpts: {}
      unresolved_axes: []
      composition_source: axis-composed
      emit: false
      axis_control_ids: {}
      source_evidence: []
      non_emission_reason: "required when not emitted"
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

`surface_color_language` is optional unless measured surface color is translated, a controlled descriptor is composed, or an externally supplied friendly label is considered. Classify value depth, chroma, and undertone independently; finish and evenness require separate visual evidence. A controlled descriptor is reconstructed from the current classification and an analyst-supplied surface term. It fails closed on unresolved included axes and never selects its own emission. When emitted, each axis excerpt maps to the same-region literal axis-control; optional finish maps to a generic surface control; the full wrapper appears exactly once.

Friendly labels remain a distinct path. Every reviewed label records user or explicitly versioned-vocabulary provenance plus a reference. A compatible review does not authorize emission. An emitted friendly label must also be `model-calibrated`, carry calibration evidence, and summarize already-owned literal controls.

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
- Does each generic emitted claim terminate in one literal control, and have synonymous cross-slot pulls been merged into one source-relative aggregate effect?
- Does each orientation-bearing subject have a complete disposition ledger, with human head/body, shoulder, and attention decisions present even when they are non-emitted?
- Does each invariant spatial decision reach one relation/effect/claim/control path under one causal control axis, while every non-invariant decision remains non-emitted?
- Are placement, principal axis, viewpoint, part-whole pose, attention, and cross-component orientation kept distinct without selecting a preferred direction?
- Do material frame bias, principal-axis offset, edge contact, and partial-layer completion budgets remain source-relative rather than defaulting to centered completion?
- Does every material placement and orientation clause agree with the recorded component, head/body, shoulder, gaze, and frame relations rather than importing a neutral alignment?
- If a broad human generation prior is emitted, is its provenance recorded, non-identifying, and linked through `geometry_claim_ids` to separately actuated visible face geometry instead of acting as the likeness description?
- Does every routed human have one explicit person-prior and skin-surface decision, including reasons for non-emitted paths?
- If skin is material, are visibility/coverage and matching Color/Tone regions recorded instead of inferred from demographic identity?
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
- If an axis-composed descriptor is emitted, is it exactly reconstructible from current-source axes and does it contain each owned axis excerpt once without introducing a preferred combination?
- Does every literal color-changing phrase in the final prompt appear once in the control ledger with one causal layer and a complete effect budget?
- Do differently named claims avoid accumulating the same color or tone direction beyond one supported aggregate target?
- When lighting is material, is the visible result recorded before the physical-light hypothesis, with confidence and evidence for any emitted source geometry?
- When one material carries distinct regional light-to-form values, is their spatial relation owned by Light/Form rather than repeated as intrinsic anatomy, volume, fit, or surface color?
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

Run `tools/size_adapter.py` for the source frame and record the requested target, binding status, and delivered dimensions. Only an explicitly applied target that is delivered at the exact target size passes the frame-setting layer. A mismatched explicitly applied delivery fails it; `auto`, unsupported, unbound, or not-yet-delivered cases remain unscored while retaining continuous ratio errors when pixels exist. A settings-layer pass does not prove pixel composition, but source/render composition fidelity cannot be reported as PASS while frame delivery is unscored.

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
- axis-composed descriptors whose phrases change with held-out value, chroma, and undertone evidence rather than converging on one motivating combination
- reliable versus mixed, uncertain, low-confidence, and missing-finish classifications, with no descriptor phrase on an unresolved included axis
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
- centered versus source-offset principal axes with otherwise similar inventory
- centered frontal, source-offset oblique, opposite-offset, and mirrored orientation cases, all without a direction default
- readable versus partial or indistinct humans where non-visible pose dimensions remain non-emitted
- camera-elevation changes with head pitch held fixed, and head-pitch changes with camera elevation held fixed
- garment asymmetry with unchanged shoulder pose, and shoulder-pose asymmetry with unchanged garment construction
- aligned versus offset cross-component axes for both human and non-human scenes
- complete versus partial secondary layers with otherwise similar medium contrast
- an externally supplied broad person cue versus no supplied cue, while local geometry remains authoritative in both arms
- material, not-material, not-visible, and uncertain skin decisions across unrelated human compositions and coverage states
- the same non-human material with regional light-to-form separation versus spatially uniform illumination
- one-axis lighting changes that keep the other axes fixed, especially edge softness versus local form contrast and displayed key versus bright-plane coverage
- compatible, conflicting, inconclusive, missing-candidate, and stale-generator-calibration label cases

The motivating image may remain one regression sample, but promotion requires improvement across this causal matrix. Use optional multi-region measurements only as diagnostic evidence; never turn one sample's numeric values or wording into runtime expectations.

For generator control-effectiveness evaluation, change one axis-control at a time and record the exact model/version, settings, reference handling, repeated-render median movement, variance, and unintended-axis leakage. Include both human and non-human surfaces. A response table is stale when the model version or relevant conditioning route changes.

Promote a change only when it improves unrelated held-out behavior without material regression in other dominant modes. Keep package PASS, prompt PASS, delivered pixels, pixel fidelity, and user preference as separate claims.

## Anti-overfitting guardrails

- Put source-relative axes and causal distinctions in runtime instructions, not example-specific desired values.
- Do not add a fixed adjective blacklist, fixed global word count, exact source proportions, or generator-specific workaround to solve one case.
- Do not install a preferred human color, demographic-to-color mapping, fixed image-specific metaphor dictionary, composed target phrase, or subject-specific measurement region. A versioned source-visible axis vocabulary and deterministic grammar are allowed only when they record uncertainty and select no preferred label or axis combination.
- Do not place named friendly-label examples or concrete preferred axis combinations in runtime instructions. Keep semantic label cases in held-out tests, and require runtime candidates to carry user or versioned-vocabulary provenance.
- Do not install a preferred source direction, fill level, light-to-form strength, shadow owner, material response, or subject-specific lighting coordinate.
- Do not install a preferred face category, centered or off-center placement, completion budget, named body region, or regional value relationship. Store motivating labels and coordinates only in regression evidence; runtime rules remain source-relative.
- Do not install named friendly lighting-label examples, preferred composite-light combinations, or one generator's response as universal semantics. Runtime candidates require external provenance; generator calibration expires with the relevant model/version or conditioning route.
- Prefer changing the merge or attribution rule over adding another subject exception.
- Corrections replace or remove amplifying claims; they do not accumulate counter-negatives.
- Treat one case as a regression sample, never as proof that a general rule succeeds or fails everywhere.
