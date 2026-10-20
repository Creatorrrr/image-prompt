# Analysis plan contract

Use this schema for source-bound audited analysis and `tools/salience_plan.py` validation. It describes the live analysis plan, atomic obligations, ownership, and optional color/light contracts. Saved evaluations and test results are not required.

## Persisted analysis plan schema

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
      },
      {
        "id": "region-to-region-direction",
        "kind": "cross-component-orientation",
        "subject_region_id": "region-id",
        "reference_region_id": "supporting-region-id",
        "placement_axes": ["direction", "proximity"],
        "degenerate_satisfaction_risk": "high",
        "degeneracy_rationale": "direction survives a material separation change",
        "placement_closure_id": "closed-placement-id",
        "observation": "source-relative inter-region placement",
        "role": "primary",
        "source_evidence": ["visible relation between both regions"]
      },
      {
        "id": "supporting-region-to-frame-relation",
        "kind": "frame-zone",
        "subject_region_id": "supporting-region-id",
        "frame_reference": "source-relative frame zone",
        "observation": "the supporting region keeps its source-visible frame relation",
        "role": "supporting",
        "source_evidence": ["visible supporting-region frame boundary"]
      }
    ],
    "placement_closures": [
      {
        "id": "closed-placement-id",
        "subject_region_id": "region-id",
        "reference_region_id": "supporting-region-id",
        "subject_frame_relation_id": "region-to-frame-relation",
        "reference_frame_relation_id": "supporting-region-to-frame-relation",
        "inter_region_relation_ids": ["region-to-region-direction"],
        "protected_axes": ["frame-position", "direction", "proximity"],
        "degenerate_satisfaction_check": {
          "tested_change": "change separation while holding direction fixed",
          "held_fixed_axes": ["direction"],
          "changed_axes": ["proximity"],
          "verdict": "material-drift",
          "source_evidence": ["direction-held comparison"]
        }
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
        "region_ids": ["region-id", "supporting-region-id"],
        "relation_ids": ["region-to-frame-relation", "region-to-region-direction", "supporting-region-to-frame-relation"],
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

`component_relations` is sparse. Record a relation only when a region-to-region or region-to-frame relation materially affects an invariant or likely drift. Valid relations carry one source region, exactly one frame or region reference, a source-relative observation, evidence, and a role. A `frame-placement` decision uses a frame relation; `cross-component-orientation` uses a named reference region and records its material placement axes. If direction alone can remain true after an extreme displacement, mark its degeneracy risk and reference one `placement_closure`: both regions bind separately to the frame, the inter-region relation protects direction plus proximity, overlap, or visibility budget, and a direction-held counterfactual must classify the residual change as material, preserved, or uncertain. Partial visibility additionally records the surviving fragments, cropped or hidden counterparts, and a completion risk. Every recorded relation terminates in a generic aggregate effect rather than remaining an unused diagnostic field.

### Atomic lane obligations

`reverse-image-analysis-lane-report/v2` separates narrative findings from atomic perceptual obligations. A material finding may summarize several cues, but each independently drifting visible result becomes one `atomic_obligation` with an id under the finding namespace, one axis, visible result, source-relative result direction, subject/region ids, relation kind, evidence, confidence, causal origin, attribution status, materiality, role, strength, and confounders. Do not force a physical explanation to obtain a result direction: `confounded` or `uncertain` attribution remains valid while the supported result survives.

Integration disposes every finding and obligation exactly once. A retained or merged obligation reaches a hash-bound invariant through `source_obligation_ids`; a material obligation cannot disappear merely because its parent finding remains. The independent critic reviews every obligation and explicitly flags obligation loss, direction loss, coupling loss, topology collapse, net neutralization, and order drift.

### Spatial/Orientation Coverage schema

When an orientation-bearing subject is material, and always when `subject.human` is routed, add `spatial_orientation_coverage` using `spatial-orientation/v6`. This is a direction-neutral evidence, non-emission, placement-closure, and prompt-actuation ledger, not a target-pose template:

```yaml
spatial_orientation_coverage:
  schema_version: spatial-orientation/v6
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
      neutralization_test: # required for flexible or not-material
        test_scope: single-dimension-with-adjacent-spatial-relations-held
        tested_change: "neutralize only this dimension"
        verdict: preserved | material-drift | uncertain
        preserved_relations: []
        changed_relations: []
        held_fixed_decision_ids: []
        evidence_cue_ids: []
        confidence: high | medium | low
        source_evidence: []
        uncertainty_note: "required only when uncertain"
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
  prompt_effect_audits:
    - id: "case-local prompt-effect audit id"
      control_id: "one emitted spatial control id"
      subject_id: "matching spatial subject id"
      effect_scope: explicit-and-implicit-spatial-effects
      prompt_excerpt: "exact complete emitted spatial control"
      explicit_decision_ids: []
      implicit_decision_ids: []
      verdict: source-consistent | neutralizing | uncertain
      rationale: "why every semantic spatial effect is source-owned"
      source_evidence: []
```

Every covered subject disposes of frame placement, principal axis, the four viewpoint dimensions, and cross-component orientation. A human additionally disposes of torso yaw/pitch/roll; head-to-body yaw/pitch/roll and lateral offset; shoulder image-plane slope and depth order; and attention direction even when a partial or indistinct view makes one `not-visible` or `uncertain`. The former coarse `human-body-orientation`, `human-head-body-relation`, and `human-shoulder-line` dimensions are legacy-only and cannot establish v5 completeness. `flexible` decision ids also appear in `flexible_dimensions`.

Each evidence cue belongs to one subject and records a generic visible relation plus its confounders; decisions link to those cue ids. Orientation cannot rely only on a frame-placement cue. Cue families contain no preferred body part, direction, angle, garment, or composition. Viewpoint dimensions accept `perspective`; human torso and rotational head/body axes accept `pose-deformation`; lateral head/body offset and shoulder depth order may use a visible `spatial-relation`; attention accepts pose or a visible spatial relation; frame placement and cross-component orientation accept spatial relation or layout; the principal subject axis accepts spatial relation, pose, or layout. These are causal owners, not desired visual values.

Every human has two counterfactuals. `whole-orientation` neutralizes every orientation decision together. `residual-alignment` holds all viewpoint decisions fixed while neutralizing every human pose-geometry decision; this isolates a pose result that a dominant camera angle could otherwise mask. A `material` verdict names changed visible relations and requires an invariant individual or coupled effect inside the tested decision set. `not-material` names preserved relations; `uncertain` records the visibility or confound limit. Neither check prefers asymmetry: a genuinely frontal source can remain valid.

An invariant decision terminates in exactly one generic component relation, invariant, affirmative claim, aggregate effect, and literal prompt control. Its aggregate effect and control carry the same `control_axis_id` and `causal_origin`. A non-invariant decision carries none of those path ids and emits no separate spatial control. Each `flexible` or `not-material` decision must pass a structured single-dimension neutralization test with adjacent spatial decisions held fixed; a free-form claim that variation is minor does not establish preservation. A `preserved` verdict names surviving relations, uses decision-owned cues, and has high or medium confidence. Low-confidence or wholly confounded evidence becomes `uncertain` unless one invariant coupled effect preserves the joint result. `not-visible` and `uncertain` record the limiting evidence. When two or more individually non-emitted decisions jointly change the visible result, one invariant `coupled_effect` owns their result direction and full path. Its members remain non-emitted as independent paths, its physical attribution may stay confounded, and its net-effect audit includes every emitted spatial control for the subject. The coupled control is decomposed hierarchically: one source-relative macro summary appears first, then a coverage decision for every member. `complete` and `not-applicable` members add no prose; `partial` and `lost` members require one literal residual subclause inside the same control. A `sufficient` summary has no at-risk members; a `lossy` or `uncertain` summary names exactly the members whose residuals emit. This preserves one owner without allowing a compact label to erase supported relations. Merge duplicate control axes before drafting.

Every emitted spatial control has exactly one `prompt_effect_audit` over its exact complete excerpt. The audit separates directly named decision effects from implicit semantic pulls and must include the individual owner or every coupled member. Treat alignment semantics—centered, frontal, upright, vertical, straight, balanced, aligned, and source-specific equivalents—as positive multi-axis actuations, not harmless defaults or a forbidden-word list. A clause may emit only when every affected decision has individual invariant ownership or belongs to an invariant coupled effect and the audit verdict is `source-consistent`. Rewrite or delete a neutralizing or uncertain clause; do not append a negative counterweight. The validator checks declared ids and literal ownership, while the independent raw-source critic is responsible for finding omitted synonymous or implicit effects.

No disposition or dimension implies a preferred value. Centered and offset, frontal and oblique, aligned and opposed, and either mirrored direction all remain valid source-relative outcomes when supported and owned. Keep placement controls positional. Put a material human pose relation after camera/scale and before local face, hair, and clothing inventory; validate the literal prompt order, complete prompt-effect audit, and source-consistent net effect. Hair and garment evidence may corroborate but never substitute for pose. Do not put case-specific coordinates, directions, body parts, garments, exact angles, or adjective exclusions into runtime expectations.

Direction is not a complete placement contract when proximity, overlap, or surviving visibility carries the source read. A relation such as above/below or viewer-left/viewer-right can be satisfied at arbitrary distance. The closed placement check therefore protects both frame positions plus the independently material inter-region axes without turning any motivating coordinate into a default.

For form, surface, sharpness, hierarchy, topology, and information, every emitted claim carries `salience_effects`. The top-level `aggregate_effects` merges claims by the same axis, source-relative direction, regions, and relations; one aggregate effect has one emitted generic claim. The top-level `emitted_controls` then represents each generic emitted claim exactly once with a literal excerpt from the authored prompt. Generic, Color/Tone, and Light/Form contracts may not own the same claim or exact excerpt. For an authored audited prompt, mask every owned excerpt and qualified emitted summary; after removing only structural labels and punctuation, any remaining semantic text is an ownership failure. A reviewer still audits whether an owned phrase has undeclared synonymous or implicit effects because the tool does not infer its full meaning.

An emitted human generation prior has scope `person-gestalt`, `attractiveness`, or `person-aesthetic`, a provenance-bound candidate source, and `non_identifying: true`. `person-gestalt` and `attractiveness` retain visible geometry evidence and separately actuated `geometry_claim_ids`; `attractiveness` and `person-aesthetic` also bind `decomposed_control_ids`. A person-aesthetic prior uses visible appearance evidence. Each decomposition control declares one valid `appearance_dimension` and an owner authorized for it. Exact race, ethnicity, nationality, or other protected identity context is never a generation prior and never comes from pixels.

Broad aesthetic, capture, mood, or genre shorthand uses `prior-cluster/v2`, not an unowned adjective. Record `scope`, `disposition`, source provenance/evidence, calibration status, a summary control only for emission, and decomposed claim/control IDs. A source-visible unverified summary may emit when confidence is high/medium, viewer priority is P0/P1, its omission counterfactual is `material-drift`, and the summary immediately leads its owned decomposition. User-supplied wording remains explicit user intent. Model calibration separately records exact generator/version response evidence. Human appearance remains in the dedicated decision/generation-prior path.

### Human Appearance Decisions schema

Whenever `subject.human` is routed, add exactly one record for every human in `spatial_orientation_coverage.subjects`:

```yaml
human_appearance_decisions:
  - id: "case-local decision id"
    schema_version: human-appearance/v3
    subject_id: "matching human spatial subject id"
    face_visibility: readable | partial | indistinct | not-visible | uncertain
    frame_prominence: primary | secondary | background
    fidelity_salience: primary | supporting | not-material | uncertain
    appearance_invariant_ids: []
    source_evidence: []
    identity_context:
      disposition: user-supplied | trusted-metadata | absent
      context_use: creative-target | user-asserted-context | trusted-factual-context | none
      prompt_disposition: emit | diagnostic-only | omit
      viewer_priority: P0 | P1 | P2 | P3 | not-material | uncertain
      source_reference: "required for externally supplied context"
      claim_id: "required only for emitted external context"
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
    appearance_gestalt:
      scope: attractiveness | person-aesthetic
      disposition: emit | omit | uncertain
      confidence: high | medium | low
      candidate_support: supported | unsupported | uncertain
      viewer_priority: P0 | P1 | P2 | P3 | not-material | uncertain
      default_drift_risk: low | medium | high | uncertain
      source_evidence: []
      claim_id: "required only for emit"
      decomposition_control_ids: []
      effect_budget:
        intended_dimensions: []
        protected_dimensions: [identity-context]
        source_evidence: []
      omission_counterfactual:
        verdict: preserved | material-drift | uncertain
        source_evidence: []
      non_emission_reason: "required unless emitted"
      residual_risk: "required while uncertain"
    skin_surface:
      disposition: material | not-material | not-visible | uncertain
      viewer_priority: P0 | P1 | P2 | P3 | not-material | uncertain
      observation_scope: source-visible | color-managed | user-specified
      semantic_use: displayed-surface
      confidence: high | medium | low
      source_evidence: []
      region_ids: []
      coverage: exposed | through-sheer | mixed
      descriptor_disposition: emit | omit | uncertain
      descriptor_non_emission_reason: "required unless descriptor emits"
      non_emission_reason: "required when skin is not material"
```

This is a processing-completeness contract, not an instruction to emit identity, aesthetic, or skin wording. Frame prominence does not set fidelity salience. Exact identity context enters only from user/trusted external provenance, emits only at P0/P1, and remains separate from pixel evidence and generation priors. For a readable fidelity-material person, omitting a broad prior requires sufficient geometry, low drift risk, and a preserved counterfactual. A qualified P0/P1 appearance gestalt emits once, declares intended/protected dimensions, and immediately leads every intended owner-correct control; identity context is always protected. Displayed skin has independent priority and scope, names matching Color/Tone regions when material, and never substitutes for geometry or demographic identity.

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
