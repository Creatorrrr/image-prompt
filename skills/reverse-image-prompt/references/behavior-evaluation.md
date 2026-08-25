# Behavior evaluation for reverse-image-prompt

Read this reference only when evaluating or revising the skill. It is not part of an ordinary prompt-extraction route.

## Evaluation boundary

Structural validation proves that modules, anchors, routes, and generated bundles are consistent. It does not prove that a prompt preserves perceptual salience or that a rendered image resembles the source. Report these layers separately:

1. package and module/lane routing validity
2. lane coverage and disclosed context independence
3. hash-bound finding/atomic-obligation integration, adjudication, and independent-critic validity
4. salience-plan validity
5. prompt-level fidelity
6. rendered-pixel fidelity
7. user judgment

An undelivered render is unscored, not a visual-quality failure. A single stochastic success is evidence for that attempt, not general superiority.

Evaluate `prompt` and `audited` as different execution contracts. A prompt-profile pass does not claim atomic-ledger completeness; an audited pass does not establish acceptable interactive latency.

## Held-out case design

Do not derive the evaluation set from one reported failure. Use raw images or artifacts that were not used to write the current correction and cover materially different subjects, media, and dominant fidelity modes.

Across the evaluation suite, include matched transformation pairs. They are not mandatory extra inputs for each independent single-source pass, and an evaluator must not invent or retrieve a second source outside that pass's scope:

- **Invariant-preserving pair:** the primary appeal or proposition remains stable while a flexible dimension such as minor pose, viewpoint, placement, or incidental capture changes.
- **Aesthetic-changing pair:** object inventory stays substantially similar while a primary form, surface, light-to-form, color, hierarchy, topology, or information invariant changes.

The first pair should retain the primary salience signature without overlocking the flexible change. The second should produce a meaningfully different primary signature instead of collapsing to an object list.

Balance appearance-led cases with relationship-led, information-led, mixed, neutral, photographic, and non-photographic cases. Include both human and non-human subjects when those routes are in scope. The current motivating case may remain one regression sample, but its subject parts, colors, garments, pose, or desired values must not become runtime defaults or expected wording.

Include appearance cases where generic attractiveness stays similar while broad visual reading, local geometry, displayed skin, space, clothing, or pose changes independently. The expected distinction is source-specific priority, never a preferred demographic or beauty preset.

## Independent prompt-profile pass

For a before/after comparison, give each arm only the raw request, source artifact, applicable skill snapshot, and normal runtime tools. Do not reveal the suspected bug, proposed fix, expected answer, prior prompt, or prior render.

For each arm:

1. Resolve `reverse-image-analysis-route/v2` with `analysis_profile=prompt` and run exactly one isolated lane wave.
2. Confirm every lane returns `reverse-image-analysis-lane-report/compact-v1`, details P0/P1, compresses P2, groups P3/non-material topics, and does not create v4/v2 ledgers.
3. Integrate one viewer-priority map and draft from P0 to P2. Check that one lane's inventory cannot acquire weight through length or repetition.
4. Run one independent compact critic. Record `pass`, one `targeted-repair`, or `blocked`; advisories and P2/P3 completeness must not cause reruns.
5. Record route time, lane wall time, integration time, critic time, end-to-end time, report bytes/tokens, lane retry count, full-reroute count, and repair count. Compare medians and tails across identical held-out requests; do not infer latency improvement from one run.
6. Score the standalone prompt without requiring shared wording, a persisted bundle, or an actual render. Keep pixel and user-judgment layers unscored unless separately obtained.

## Independent audited pass

For a before/after comparison, give each arm only the raw request, source artifact, applicable skill snapshot, and normal runtime tools. Do not reveal the suspected bug, proposed fix, expected answer, prior prompt, or prior render.

For each arm:

1. Resolve `reverse-image-analysis-route/v2` with `analysis_profile=audited`, run its lanes under `references/analysis-orchestration.md`, integrate by owner key, and obtain the coverage critic result.
2. Validate `reverse-image-analysis-bundle/v2` with `python tools/analysis_bundle.py ANALYSIS_BUNDLE.json`. Its embedded integrated-plan payload, retained obligation/invariant IDs, and critic review must share one canonical plan SHA-256. Record `delegated`, `sequential-fallback`, or `mixed`; never report fallback as independent evidence.
3. Record the internal salience plan without exposing it to the downstream generator. Every material atomic lane obligation must survive; primary obligations remain primary invariants through `source_obligation_ids`.
4. Draft the standalone prompt. Update generic and specialized ledgers from literal excerpts of that final draft rather than anticipated wording.
5. Validate with `python tools/salience_plan.py PLAN.json --prompt PROMPT.txt`. Omitting `--prompt` validates the structured contract only.
6. For generation or comparison, persist bundle, plan, exact prompt/hash, source/target sizes, binding, reference handling, and attempt log.
7. Freeze only after complete integration and critic `pass`, then compare semantics without requiring shared wording or headings.

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

### Atomic lane obligations

`reverse-image-analysis-lane-report/v2` separates narrative findings from atomic perceptual obligations. A material finding may summarize several cues, but each independently drifting visible result becomes one `atomic_obligation` with an id under the finding namespace, one axis, visible result, source-relative result direction, subject/region ids, relation kind, evidence, confidence, causal origin, attribution status, materiality, role, strength, and confounders. Do not force a physical explanation to obtain a result direction: `confounded` or `uncertain` attribution remains valid while the supported result survives.

Integration disposes every finding and obligation exactly once. A retained or merged obligation reaches a hash-bound invariant through `source_obligation_ids`; a material obligation cannot disappear merely because its parent finding remains. The independent critic reviews every obligation and explicitly flags obligation loss, direction loss, coupling loss, topology collapse, net neutralization, and order drift.

### Spatial/Orientation Coverage schema

When an orientation-bearing subject is material, and always when `subject.human` is routed, add `spatial_orientation_coverage` using `spatial-orientation/v4`. This is a direction-neutral evidence and coverage ledger, not a target-pose template:

```yaml
spatial_orientation_coverage:
  schema_version: spatial-orientation/v4
  subjects:
    - id: "subject-local-id"
      kind: human | non-human | group | component
      visibility: readable | partial | indistinct
      region_id: "known major region id"
      source_evidence: []
  evidence_cues:
    - id: "subject-local-cue-id"
      subject_id: "subject-local-id"
      family: frame-placement | axis-relation | side-visibility | occlusion | depth-order | silhouette | perspective | attention | visibility-limit
      observation: "one source-visible relation or visibility limit"
      source_evidence: []
      confounders: []
  counterfactual_checks:
    - id: "case-local counterfactual id"
      subject_id: "human-subject-local-id"
      scope: whole-orientation | residual-alignment
      tested_change: "replace the source relation with neutral axial alignment"
      verdict: material | not-material | uncertain
      changed_relations: []
      preserved_relations: []
      uncertainty_note: "required only when uncertain"
      neutralized_decision_ids: []
      held_fixed_decision_ids: []
      evidence_cue_ids: []
      source_evidence: []
  decisions:
    - id: "subject-and-dimension-local-id"
      subject_id: "subject-local-id"
      dimension: frame-placement | subject-principal-axis | viewpoint-elevation | viewpoint-azimuth | viewpoint-roll | viewpoint-distance-foreshortening | human-torso-yaw | human-torso-pitch | human-torso-roll | human-head-body-yaw | human-head-body-pitch | human-head-body-roll | human-head-body-lateral-offset | human-shoulder-image-slope | human-shoulder-depth-order | human-attention-direction | cross-component-orientation
      family: frame-placement | principal-axis | viewpoint | part-whole | attention-direction | cross-component
      disposition: invariant | flexible | not-material | not-visible | uncertain
      observation: "source-relative observation or visibility limit"
      causal_origin: pose-deformation | perspective | spatial-relation | layout
      confidence: high | medium | low
      source_evidence: []
      evidence_cue_ids: []
      control_axis_id: "case-local causal control identifier"
      relation_id: "required only for invariant"
      invariant_id: "required only for invariant"
      claim_id: "required only for invariant"
      aggregate_effect_id: "required only for invariant"
      control_id: "required only for invariant"
      non_emission_reason: "required only for non-invariant dispositions"
      counterfactual_preservation_reason: "required for flexible or not-material"
      visibility_limit: "required for not-visible or uncertain"
  coupled_effects:
    - id: "case-local coupled effect id"
      subject_id: "human-subject-local-id"
      member_decision_ids: ["two or more individually non-emitted decision ids"]
      evidence_cue_ids: []
      visible_result: "jointly supported source-visible orientation result"
      result_direction: "source-relative direction"
      result_direction_confidence: high | medium | low
      physical_attribution: resolved | confounded | uncertain
      confounders: []
      causal_origin: pose-deformation | perspective | spatial-relation | layout
      disposition: invariant | not-material | uncertain
      role: primary | supporting
      target_strength: subtle | moderate | strong
      source_evidence: []
      control_axis_id: "distinct aggregate causal control id"
      relation_id: "required only for invariant"
      invariant_id: "required only for invariant"
      claim_id: "required only for invariant"
      aggregate_effect_id: "required only for invariant"
      control_id: "required only for invariant"
      prompt_decomposition: # required only for invariant
        summary_anchor:
          visible_result: "source-relative macro result"
          prompt_excerpt: "literal macro summary inside the coupled control"
          source_evidence: []
        summary_adequacy:
          verdict: sufficient | lossy | uncertain
          at_risk_decision_ids: []
          rationale: "whether the summary preserves every coupled member result"
          source_evidence: []
          uncertainty_note: "required only when uncertain"
        member_actuations:
          - decision_id: "one coupled member decision id"
            visible_result: "that member's source-visible result"
            summary_coverage: complete | partial | lost | not-applicable
            source_evidence: []
            prompt_excerpt: "required literal residual subclause for partial or lost"
            non_emission_reason: "required for complete or not-applicable"
      prompt_order_after_control_ids: []
      prompt_order_before_control_ids: []
      net_effect_audit:
        included_control_ids: []
        verdict: source-consistent | neutralizing | uncertain
        rationale: "net source-relative effect after all spatial controls"
        source_evidence: []
      non_emission_reason: "required only for non-invariant dispositions"
      uncertainty_note: "required only when uncertain"
```

Every covered subject disposes of frame placement, principal axis, the four viewpoint dimensions, and cross-component orientation. A human additionally disposes of torso yaw/pitch/roll; head-to-body yaw/pitch/roll and lateral offset; shoulder image-plane slope and depth order; and attention direction even when a partial or indistinct view makes one `not-visible` or `uncertain`. The former coarse `human-body-orientation`, `human-head-body-relation`, and `human-shoulder-line` dimensions are legacy-only and cannot establish v4 completeness. `flexible` decision ids also appear in `flexible_dimensions`.

Each evidence cue belongs to one subject and records a generic visible relation plus its confounders; decisions link to those cue ids. Orientation cannot rely only on a frame-placement cue. Cue families contain no preferred body part, direction, angle, garment, or composition. Viewpoint dimensions accept `perspective`; human torso and rotational head/body axes accept `pose-deformation`; lateral head/body offset and shoulder depth order may use a visible `spatial-relation`; attention accepts pose or a visible spatial relation; frame placement and cross-component orientation accept spatial relation or layout; the principal subject axis accepts spatial relation, pose, or layout. These are causal owners, not desired visual values.

Every human has two counterfactuals. `whole-orientation` neutralizes every orientation decision together. `residual-alignment` holds all viewpoint decisions fixed while neutralizing every human pose-geometry decision; this isolates a pose result that a dominant camera angle could otherwise mask. A `material` verdict names changed visible relations and requires an invariant individual or coupled effect inside the tested decision set. `not-material` names preserved relations; `uncertain` records the visibility or confound limit. Neither check prefers asymmetry: a genuinely frontal source can remain valid.

An invariant decision terminates in exactly one generic component relation, invariant, affirmative claim, aggregate effect, and literal prompt control. Its aggregate effect and control carry the same `control_axis_id` and `causal_origin`. A non-invariant decision carries none of those path ids and emits no separate spatial control. `flexible` and `not-material` also record why varying that axis preserves the visible proposition; `not-visible` and `uncertain` record the limiting evidence. When two or more individually non-emitted decisions jointly change the visible result, one invariant `coupled_effect` owns their result direction and full path. Its members remain non-emitted as independent paths, its physical attribution may stay confounded, and its net-effect audit includes every emitted spatial control for the subject. The coupled control is decomposed hierarchically: one source-relative macro summary appears first, then a coverage decision for every member. `complete` and `not-applicable` members add no prose; `partial` and `lost` members require one literal residual subclause inside the same control. A `sufficient` summary has no at-risk members; a `lossy` or `uncertain` summary names exactly the members whose residuals emit. This preserves one owner without allowing a compact label to erase supported relations. Merge duplicate control axes before drafting.

No disposition or dimension implies a preferred value. Centered and offset, frontal and oblique, aligned and opposed, and either mirrored direction all remain valid source-relative outcomes. Keep placement controls positional. Put a material human pose relation after camera/scale and before local face, hair, and clothing inventory; validate the literal prompt order and source-consistent net effect. Hair and garment evidence may corroborate but never substitute for pose. Do not put case-specific coordinates, directions, body parts, garments, exact angles, or adjective exclusions into runtime expectations.

For form, surface, sharpness, hierarchy, topology, and information, every emitted claim carries `salience_effects`. The top-level `aggregate_effects` merges claims by the same axis, source-relative direction, regions, and relations; one aggregate effect has one emitted generic claim. The top-level `emitted_controls` then represents each generic emitted claim exactly once with a literal excerpt from the authored prompt. Generic, Color/Tone, and Light/Form contracts may not own the same claim or exact excerpt. The checker compares declared strings and ownership; a reviewer still audits synonymous prose because the tool does not infer semantics.

An emitted broad human category or attractiveness anchor may add a `generation_prior` object to its owning claim. It records `scope`, a `candidate_source` with `kind` (`user-supplied`, `source-visible-approximation`, or `model-calibrated`) and a non-empty reference, `non_identifying: true`, `visible_geometry_evidence`, and non-empty `geometry_claim_ids`. Each ID references a separate emitted affirmative form claim owned by `subject.human`, `detail.human-face-likeness`, or `detail.human-body-form`, kept in the generic ledger, and represented by exactly one prompt control. The runtime skill contains no named preferred category, and neither diagnostic evidence, a skin/surface claim, nor the prior clause itself can replace local face or body geometry.

Broad aesthetic, capture, mood, or genre shorthand uses `prior-cluster/v2`, not an unowned adjective. Record `scope`, `disposition`, source provenance/evidence, calibration status, a summary control only for emission, and decomposed claim/control IDs. A source-visible unverified summary may emit when confidence is high/medium, viewer priority is P0/P1, its omission counterfactual is `material-drift`, and the summary immediately leads its owned decomposition. User-supplied wording remains explicit user intent. Model calibration separately records exact generator/version response evidence. Human appearance remains in the dedicated decision/generation-prior path.

### Human Appearance Decisions schema

Whenever `subject.human` is routed, add exactly one record for every human in `spatial_orientation_coverage.subjects`:

```yaml
human_appearance_decisions:
  - id: "case-local decision id"
    schema_version: human-appearance/v2
    subject_id: "matching human spatial subject id"
    face_visibility: readable | partial | indistinct | not-visible | uncertain
    frame_prominence: primary | secondary | background
    fidelity_salience: primary | supporting | not-material | uncertain
    appearance_invariant_ids: []
    source_evidence: []
    identity_context:
      disposition: user-supplied | trusted-metadata | absent
      source_reference: "required for user-supplied or trusted metadata"
      claim_id: "optional user-context claim"
    person_prior:
      disposition: emit | omit | uncertain
      confidence: high | medium | low
      candidate_support: supported | unsupported | uncertain
      default_drift_risk: low | medium | high | uncertain
      local_geometry_sufficiency: sufficient | insufficient | uncertain
      geometry_claim_ids: []
      source_evidence: []
      claim_id: "required only for emit"
      non_emission_reason: "required for omit or uncertain"
      omission_counterfactual:
        verdict: preserved | material-drift | uncertain
        source_evidence: []
      residual_risk: "required while uncertain"
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

This is a processing-completeness contract, not an instruction to emit a category or color. Frame prominence does not set fidelity salience. Factual identity/nationality can enter only as user-supplied or trusted metadata with an external source reference; pixels can support only a non-identifying generation approximation. For a readable fidelity-material person, `omit` requires sufficient emitted form geometry, low default-drift risk, and a preserved omission counterfactual. Otherwise emit a supported prior or keep uncertainty with residual risk. Skin color cannot substitute for form geometry. Material skin names matching Color/Tone regions and coverage; an emitted descriptor targets one and may contain only stable included axes.

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
      tone_scope:
        kind: global | region | region-group
        affected_region_ids: []
        protected_region_ids: []
        prompt_anchor: "exact region phrase retained by the control"
        source_evidence: []
  regions:
    - id: "region id"
      prompt_anchor: "non-trivial exact region phrase"
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
  region_groups:
    - id: "group id"
      member_region_ids: ["two or more color region ids"]
      prompt_anchor: "analyst-supplied group phrase"
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
      status: complete | partial | bounded | inconclusive
      surface_term: "analyst-supplied visible region phrase"
      phrase: "deterministic phrase reconstructed from the included current-source axes"
      requested_axes: [value_depth, chroma, undertone]
      included_axes: [value_depth, chroma, undertone]
      axis_excerpts: {}
      bounded_axes: {}
      unresolved_axes: []
      composition_source: axis-composed
      emit: false
      axis_control_ids: {}
      source_evidence: []
      non_emission_reason: "required when not emitted"
    friendly_label_review:
      - phrase: "<provenance-bound-candidate-label>"
        candidate_source:
          kind: user-supplied | source-visible-approximation | versioned-vocabulary
          reference: "request field, current-source observation, vocabulary id, or artifact reference"
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
      protected_light_effect_ids: ["required primary Light/Form effects when this value/tone control overlaps them"]
  appearance_metaphors:
    - phrase: "optional appearance shorthand"
      status: explanation-only | unverified | source-evidence-qualified | model-calibrated
      emit: false
      source_evidence: []
      confidence: high | medium | low
      viewer_priority: P0 | P1 | P2 | P3
      omission_counterfactual: preserved | material-drift | uncertain
      decomposed_control_ids: []
```

Every Color/Tone region declares a non-trivial exact `prompt_anchor`. A regional or `region-group` tone response must reuse its declared anchor, and the emitted excerpt must retain that phrase as a complete token-bounded span; it cannot use a trivial substring or silently substitute a broader phrase.

Every claim listed by the contract carries `perceptual_effects`, each naming one aggregate effect, one causal layer (`intrinsic`, `illumination`, `global-cast`, `exposure`, `processing`, or `hierarchy`), confidence, and evidence. Claims sharing a region, axis, and direction use one canonical effect even when their semantic-slot names differ. Repeating one causal layer is a merge failure. Multiple causal layers are valid only when each layer and their combined pull are independently source-supported.

Every listed color/tone claim is represented exactly once in `emitted_controls`. Its literal excerpt matches the claim's causal layer and complete effect set. Every required intrinsic or displayed-tone axis links to one same-region/same-axis effect and axis-control. Displayed tone additionally retains a declared global/region/group prompt anchor and cannot include protected regions; split a coarse mixed-tone region first. A compound-control cannot satisfy a required axis.

`surface_color_language` is optional unless measured surface color is translated, a descriptor is composed, or a friendly label is considered. Classify value depth, chroma, undertone, and optional finish independently. `complete` contains every requested stable axis; `partial` contains only stable axes and omits bounded/unresolved ones; boundary-only `bounded` and empty `inconclusive` remain non-emitted. On emission, control IDs cover exactly included axes and the wrapper appears once.

Friendly labels remain a distinct path. Every reviewed label records user, current-source, or explicitly versioned-vocabulary provenance plus a reference. A compatible review alone does not authorize emission. A `source-evidence-qualified` label additionally requires high/medium confidence, P0/P1 priority, a `material-drift` omission counterfactual, and immediate already-owned literal controls. A `model-calibrated` label instead carries exact generator/version response evidence. Both summarize rather than replace their decomposition.

The schema deliberately contains no preferred hue, skin value, palette, metaphor, adjective blacklist, numeric color, identity proxy, or generator workaround. A hierarchy-layer hue effect additionally requires source evidence that hue contrast itself is invariant.

### Optional Light/Form Contract schema

When a persisted plan contains a primary `light-to-form` invariant or the routed `detail.light-form-fidelity` module, add the source-relative `light_form_contract` defined in `references/lighting-reproduction-evaluation.md`. Keep that schema in the dedicated reference rather than duplicating it here.

The contract records the visible result before a confidence-rated source hypothesis, then region effects, shadow ownership, material response, pose dependence, aggregate effects, and literal final-prompt controls. Candidate claims use `lighting_effects`, not the Color/Tone contract's `perceptual_effects`.

Every listed lighting claim is represented exactly once in `emitted_controls`. A low-confidence physical-light hypothesis cannot carry an emitted source-geometry or fill control; use result-space effects or keep it diagnostic. Global tonal range and local form contrast remain distinct. The same claim or literal excerpt cannot be owned independently by both the Light/Form and Color/Tone contracts.

`lighting_language` and `lighting_labels` are optional. When present, the controlled summary is reconstructed from independently classified source-visible axes and remains explanation-only. Named candidates require user, current-source, or explicitly versioned-vocabulary provenance; compatibility is recalculated from their declared axis requirements. Source-evidence-qualified emission additionally requires high/medium confidence, P0/P1 priority, a `material-drift` omission counterfactual, and immediate links to already-owned literal controls. Model-calibrated emission additionally carries exact generator/version response evidence.

## Prompt-level rubric

### Prompt profile

- Does each required lane run once in an isolated context and return the compact schema?
- Does every P0/P1 finding name a visible change counterfactual and causal control requirement?
- Are P2 findings compressed and P3/non-material topics grouped rather than exhaustively analyzed?
- Does the integrated order reflect what a viewer would notice and miss first, independent of lane report length?
- Can face, displayed skin, space, clothing, pose, topology, light, color, or capture become P0/P1 when the source makes it identity-bearing?
- For a material human, does the compact appearance signature retain the source-supported broad visual prior when needed, authoritative local geometry, stable displayed-skin axes, and only material hair/expression/capture cues?
- Is a broad person prior non-identifying and immediately corrected by local geometry, with generic attractiveness unable to replace or override it?
- Does each P0/P1 effect appear once, while incidental inventory and generic quality/style language remain subordinate?
- Is there exactly one compact critic pass, no rerun for advisories, and at most one targeted repair or one affected-lane reroute for a true route/source failure?
- Are runtime and report-size metrics recorded separately from prompt, pixel, and user-judgment evidence?

### Audited profile

Review the standalone prompt with the source visible and score distinct questions:

- Does the first-order proposition survive without the source image?
- Are primary invariants expressed affirmatively at their source-relative strength?
- Are flexible dimensions allowed to vary without becoming primary locks?
- Does each semantic slot have one owner rather than repeated synonymous emphasis?
- Did every routed lane review its assigned modules and dispose every required topic against identical source bytes/hash?
- Are delegated lane reports genuinely clean-context, while sequential fallback is disclosed as non-independent?
- Does integration dispose every finding and atomic obligation once, bind every retained obligation through `source_obligation_ids`, preserve result direction and role, adjudicate conflicts, and pass an independent coverage critic before prompt freeze?
- Does each generic emitted claim terminate in one literal control, and have synonymous cross-slot pulls been merged into one source-relative aggregate effect?
- Does each orientation-bearing subject use `spatial-orientation/v4`, with human torso, head/body, shoulder, and attention subaxes present even when they are non-emitted?
- Does every spatial decision link to subject-owned structured cues, with frame-placement evidence excluded as the sole basis for orientation?
- Does each human have both whole-orientation and viewpoint-held residual-alignment counterfactuals, naming what changes, remains preserved, or is uncertain without preferring asymmetry?
- When individually weak cues jointly matter, does one coupled effect preserve their visible result direction while its member decisions remain non-emitted as separate paths and physical attribution may remain confounded?
- Does every invariant coupled effect state a source-relative macro summary first, assess that summary against every coupled member exactly once, and retain a literal residual subclause for each `partial` or `lost` member inside the same control?
- Does a `sufficient` summary avoid unnecessary residual detail, while a `lossy` or `uncertain` summary names exactly the at-risk members without inventing unsupported physical attribution?
- Does every material coupled effect pass a source-consistent net-effect audit and appear after camera/scale but before non-spatial face, hair, body-form, and clothing controls?
- Does each invariant spatial decision reach one relation/effect/claim/control path under one causal control axis, while every non-invariant decision remains non-emitted?
- Are placement, principal axis, viewpoint, part-whole pose, attention, and cross-component orientation kept distinct without selecting a preferred direction?
- Do material frame bias, principal-axis offset, edge contact, and partial-layer completion budgets remain source-relative rather than defaulting to centered completion?
- Does every material placement and orientation clause agree with the recorded component, head/body, shoulder, gaze, and frame relations rather than importing a neutral alignment?
- Is frame placement wording limited to position and frame share, with a material pose relation stated before face, hair, and garment inventory?
- Do hair and garment clauses preserve the recorded side visibility and depth relation instead of supplying pose evidence or restoring bilateral symmetry?
- If a broad human generation prior is emitted, is its provenance recorded, non-identifying, and kept contiguous with separately actuated visible geometry that immediately corrects it instead of letting the prior act as the likeness description?
- Does every routed human separate frame prominence, fidelity salience, user/trusted identity context, generation approximation, person-prior drift risk, geometry sufficiency, omission counterfactual, and skin handling?
- For readable fidelity-material appearance, does omission have sufficient emitted form geometry, low default-drift risk, and a preserved counterfactual—or remain explicitly uncertain?
- If skin is material, are visibility/coverage and matching Color/Tone regions recorded instead of inferred from demographic identity?
- Are intrinsic properties separated from pose/deformation, perspective, lighting/shadow, material interaction/occlusion, and processing?
- Are intrinsic surface color, illumination, global cast, and exposure kept distinct?
- When color or tone is material, are value, chroma, hue, tone-zone response, processing, and neutral-anchor confidence represented at source-relative strength?
- Are displayed key level, shadow floor, highlight rolloff, and microcontrast kept distinct rather than collapsed into `light intensity`?
- Does every required intrinsic axis continue through a same-region/same-axis effect and literal intrinsic axis-control, instead of being replaced by hierarchy, exposure, or illumination?
- Does every required displayed-tone axis continue through its own effect and axis-control, retain a region-scope anchor, and protect unaffected regions without substituting for Light/Form?
- Is displayed intrinsic color based on comparable midtone or flat evidence rather than a pooled highlight/midtone/shadow range?
- Is the observation scope limited to what the image/profile evidence supports rather than claiming biological, material, or scene-referred true color?
- Was each material appearance metaphor retained once and immediately decomposed, with unsupported or non-material metaphors omitted and no added color, finish, illumination, or polish direction?
- When friendly surface-color language is used, were value depth, chroma, and undertone classified first, with ambiguous or conflicting labels left non-emitted?
- If an axis-composed descriptor is emitted, is it reconstructible from current-source axes, limited to stable included axes, and free of invented bounded/unresolved terms?
- Does every literal color-changing phrase in the final prompt appear once in the control ledger with one causal layer and a complete effect budget?
- Do differently named claims avoid accumulating the same color or tone direction beyond one supported aggregate target?
- When lighting is material, is the visible result recorded before the physical-light hypothesis, with confidence and evidence for any emitted source geometry?
- When one material carries distinct regional light-to-form values, is their spatial relation owned by Light/Form rather than repeated as intrinsic anatomy, volume, fit, or surface color?
- Are apparent source size, fill, global tonal range, bright-plane coverage, local form contrast, gradient extent, shadow ownership, material response, and background spill kept causally distinct?
- When compact lighting language is used, were displayed key, shadow floor, edge softness, local form contrast, bright-plane coverage, gradient extent, directionality, and fill classified independently before the summary, with unresolved or conflicting labels left non-emitted?
- Does any emitted friendly lighting label have explicit provenance plus either source-evidence qualification or exact generator/version calibration, and immediate literal decomposition without adding a second lighting direction?
- Does every literal lighting-changing phrase appear once in the Light/Form control ledger with one owner and a complete effect set?
- When pose or geometry is flexible, does the prompt preserve the light-to-form relation without overlocking incidental highlight coordinates?
- Do the Light/Form and Color/Tone contracts avoid duplicate claims, excerpts, and contrast directions; and does every overlapping value/tone control name protected primary light effects and follow their visible-result control?
- Does every multi-region form/topology invariant retain a region-to-region relation for its material boundary rather than collapsing to one category or broad edge?
- Does the major-region area and attention hierarchy survive?
- Do combined quality, lighting, surface, framing, and style cues import an unsupported category default?
- Does every broad aesthetic/capture/mood/genre shorthand carry provenance, P0/P1 materiality, a material-drift omission check, and immediate literal decomposition, with generator calibration reported separately when available?
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
- complete, partial, boundary-only, inconclusive, and missing-finish classifications, with stable axes surviving and unresolved axes absent from descriptor prose
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
- centered-frontal versus centered-oblique, and off-center-frontal versus centered-oblique, so frame placement cannot stand in for pose
- source-side-A oblique, source-side-B mirrored oblique, and source-frontal orientation cases, all without a direction default
- readable versus partial or indistinct humans where non-visible pose dimensions remain non-emitted
- camera-elevation changes with head pitch held fixed, and head-pitch changes with camera elevation held fixed
- whole-orientation neutralization versus viewpoint-held residual alignment, including a strong viewpoint with subtle but jointly material pose cues
- head/body yaw, pitch, roll, and lateral-offset changes with the adjacent axes held fixed
- individually weak torso, head/body, shoulder, silhouette, and depth cues whose coupled result is material, versus the same cues whose joint result remains neutral
- coupled effects whose macro summary fully preserves every member result versus coupled effects where otherwise similar summaries lose one or more source-visible member relations
- lossy and uncertain coupled summaries across mirrored, frontal, oblique, human, and non-human cases, with only the at-risk member relations retained as residual subclauses
- garment asymmetry with unchanged shoulder pose, and shoulder-pose asymmetry with unchanged garment construction
- asymmetric hair or object occlusion with unchanged face plane, and face-plane change with comparable occlusion
- aligned versus offset cross-component axes for both human and non-human scenes
- complete versus partial secondary layers with otherwise similar medium contrast
- one-boundary versus multi-boundary objects, garments, UI containers, and architecture, including reordered, merged, and missing boundary components
- a broad person prior adjacent to its linked geometry versus the same controls separated or reversed in prompt order
- a provenance-bound broad person or attractiveness cue versus no aggregate cue, while local geometry remains authoritative in both arms
- readable-secondary/fidelity-primary people with low versus high default-drift risk, sufficient versus insufficient geometry, and preserved versus material-drift omission counterfactuals
- the same broad person reading under different lighting, different broad readings with similar skin axes, and the same person under different portrait-production aesthetics
- material, not-material, not-visible, and uncertain skin decisions across unrelated human compositions and coverage states
- scoped displayed-tone controls for one region, declared region groups, and global response with protected bright/dark regions
- spatially uniform dark/light surfaces versus the same displayed value with a primary regional Light/Form separation, including reversed prompt order
- ordinary generic, portrait, product, document/UI, and non-photographic routes with lane coverage, merge-loss, conflict, critic, and sequential-fallback fixtures
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
- Do not place named friendly-label examples or concrete preferred axis combinations in runtime instructions. Keep semantic label cases in held-out tests, and require runtime candidates to carry user, source-visible-approximation, or versioned-vocabulary provenance.
- Do not install a preferred source direction, fill level, light-to-form strength, shadow owner, material response, or subject-specific lighting coordinate.
- Do not install a preferred face category, centered or off-center placement, completion budget, named body region, or regional value relationship. Store motivating labels and coordinates only in regression evidence; runtime rules remain source-relative.
- Do not install a preferred frontal or oblique pose, left/right direction, exact angle, cue count, named anatomy cue, garment, or hair arrangement. Runtime pose fields describe generic degrees of freedom and evidence families; motivating literals remain fixtures.
- Do not install named friendly lighting-label examples, preferred composite-light combinations, or one generator's response as universal semantics. Runtime candidates require explicit provenance; current-source qualification is case-bound, and generator calibration expires with the relevant model/version or conditioning route.
- Prefer changing the merge or attribution rule over adding another subject exception.
- Corrections replace or remove amplifying claims; they do not accumulate counter-negatives.
- Treat one case as a regression sample, never as proof that a general rule succeeds or fails everywhere.
