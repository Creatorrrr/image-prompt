# Lighting reproduction evaluation

Read this reference only when `detail.light-form-fidelity` is selected and the request requires measured source/render comparison, actual generation, controlled lighting revision, or skill evaluation. Ordinary prompt extraction should use the shorter module path.

## Evidence boundary

A single image directly supports an image-space lighting result, not a unique physical rig. Several combinations of source position, source size, bounce, fill, exposure, local adjustment, material response, and tone mapping can produce similar pixels.

Keep these levels separate:

1. visible spatial result
2. confidence-rated physical or rendered-light hypothesis
3. literal prompt actuation
4. delivered-pixel verification
5. user judgment

Do not claim exact lamp geometry, ratios, scene-referred luminance, or material reflectance without corresponding calibration evidence.

## Optional Light/Form Contract schema

Use source-relative identifiers and omit optional region, shadow, or material entries that are not visible. Values below define structure, not preferred lighting. For a prompt-only case, keep the internal contract to material invariants and the smallest literal prompt clauses; the schema must not dictate the prompt's headings, sentence count, or length.

```yaml
light_form_contract:
  importance: primary | supporting
  observation_scope: source-visible | user-specified
  observed_result:
    global_tonal_range: "source-relative scene range"
    local_form_contrast: flattening | subtle | moderate | strong
    bright_plane_coverage: narrow | balanced | broad | mixed | uncertain
    gradient_character: "long and shallow, short and steep, stepped, mixed, or uncertain"
    gradient_extent: short | medium | long | mixed | uncertain
    background_spill_relation: suppressed | low | moderate | high | mixed | uncertain
    largest_bright_masses: []
    largest_dark_masses: []
    source_evidence: []
  source_hypothesis:
    model_type: physical-light | rendered-shading | mixed | uncertain
    source_count: one-dominant | multiple | mixed | uncertain
    camera_axis_offset: near-axis | slight | moderate | strong | uncertain
    elevation: below | level | slight-above | high | uncertain
    front_side_back_relation: "source-relative relation or uncertainty"
    apparent_angular_size: small | medium | large | uncertain
    fill_structure: high | moderate | low | mixed | uncertain
    confidence: high | medium | low
    actuation: physical-cause | physical-plus-result | result-space-only | diagnostic-only
    source_evidence: []
  regions:  # optional source-derived Light/Form subregions inside major regions
    - id: "light-region-id"
      parent_region_id: "known major region"
      prompt_anchor: "non-trivial exact prompt phrase"
      role: major-plane | shadow-zone | transition | material-mass | context | spill-field
      source_evidence: []
  region_effects:
    - id: "effect observation id"
      region_id: "known major region or declared Light/Form subregion"
      reference_region_id: "optional distinct known major or Light/Form region for a comparative spatial effect"
      role: broad-plane | gradient | highlight | shadow | rim | spill
      value_relation: "source-relative relation"
      gradient_strength: subtle | moderate | strong
      edge_character: "source-visible edge behavior"
      source_evidence: []
  shadow_events:
    - id: "shadow id"
      region_id: "known major region"
      owner: cast | self | contact-occlusion | material-response | processing | mixed | uncertain
      footprint: "source-relative footprint"
      edge_character: "source-visible edge behavior"
      confidence: high | medium | low
      source_evidence: []
  material_responses:
    - region_id: "known major region"
      response: diffuse | absorbent | glossy | metallic | translucent | woven | mixed
      highlight_width: "source-relative width or absence"
      highlight_strength: "source-relative strength or absence"
      black_level_behavior: "source-relative response"
      source_evidence: []
  pose_light_dependency:
    geometry_dependency: pose-bound | pose-robust | mixed | uncertain
    preserved_result: "light-to-form relation that must survive"
    flexible_effects: []
    source_evidence: []
  lighting_language:  # optional; diagnostic translation, not a new effect owner
    policy_id: "versioned lighting-language policy"
    policy_status: uncalibrated-language-prototype | model-calibrated
    observation_scope: source-visible
    region_id: "known major region or global"
    source_evidence: []
    axis_classification:
      displayed_key_level: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      shadow_floor: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      edge_softness: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      local_form_contrast: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      bright_plane_coverage: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      gradient_extent: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      directionality: {term: "policy term", confidence: high | medium | low, source_evidence: []}
      fill_structure: {term: "policy term", confidence: high | medium | low, source_evidence: []}
    controlled_summary:
      phrase: null
      status: explanation-only | inconclusive
      emit: false
      decomposed_axes: []
      unresolved_axes: []
    friendly_label_review: []
  lighting_labels:  # optional provenance-bound shorthand after compatibility review
    - phrase: "candidate label"
      status: explanation-only | unverified | source-evidence-qualified | model-calibrated
      emit: false
      source_evidence: []
      confidence: high | medium | low
      viewer_priority: P0 | P1 | P2 | P3
      omission_counterfactual: preserved | material-drift | uncertain
      generator_id: "required only for model-calibrated status"
      generator_version: "required only for model-calibrated status"
      conditioning_route: "required only for model-calibrated status"
      calibration_evidence: []
      decomposed_control_ids: []
  claim_ids: []
  aggregate_effects:
    - id: "canonical light effect"
      region_id: "known major region, declared Light/Form subregion, or global"
      reference_region_id: "optional distinct known major or Light/Form region matching a comparative observation"
      axis: source-geometry | fill | bright-plane-coverage | local-form-contrast | gradient-extent | shadow-topology | material-response | background-spill
      direction: "canonical source-relative direction"
      role: primary | supporting
      target_strength: subtle | moderate | strong
      claim_ids: []
      source_supported: true
      source_evidence: []
  emitted_controls:
    - id: "control id"
      prompt_excerpt: "literal excerpt copied from the final production prompt"
      claim_id: "one listed emitted lighting claim"
      owner: source-geometry | fill | bright-plane-coverage | local-form-contrast | gradient-extent | shadow-topology | material-response | background-spill
      aggregate_effect_ids: []
```

Candidate claims listed by this contract carry `lighting_effects`, each with an `aggregate_effect_id`, confidence, and source evidence. Every listed claim is emitted, represented exactly once in `emitted_controls`, and references the same complete effect set. A `prompt_excerpt` may be the smallest exact clause inside a compact sentence; it need not be a standalone sentence or visible output section. Two effect IDs may not hide the same region, axis, and direction.

When adjacent regions belong to the same visible surface, a material source/render change in their value separation is evidence for a spatial Light/Form residual, not automatically for intrinsic form or surface color. If one coarse major region contains both sides of that material relation, declare only the necessary Light/Form subregions—such as major plane, shadow zone, transition, or material mass—under their parent major region. Each subregion carries source evidence and a non-trivial exact prompt anchor. Record the compared regions as `region_id` and a distinct known `reference_region_id`; the same ordered pair must appear in an aggregate actuation rather than remaining diagnostic-only, and every emitted control for that comparison must retain both exact anchors. Omit the optional reference for genuinely one-region effects. Then assign any visible transition to gradient extent, local form contrast, shadow topology, or material response. Use `result-space-only` when the image does not identify a reliable physical cause.

`lighting_language` is optional unless source-visible lighting is being translated into a compact composite or a friendly label is considered. Use `references/lighting-language.md` and its versioned policy. Classify every axis independently, preserve evidence and uncertainty, and keep its deterministic `controlled_summary` explanation-only. Every named review records user, versioned-vocabulary, or current-source provenance. Compatibility alone does not authorize emission: a `source-evidence-qualified` entry must also have high/medium confidence, P0/P1 priority, a `material-drift` omission counterfactual, and immediately adjacent already-owned literal controls. A `model-calibrated` entry instead carries exact generator/version response evidence.

## Cause and result rules

- `physical-cause` requires medium- or high-confidence source evidence and a source-geometry control.
- `physical-plus-result` requires medium- or high-confidence source evidence, a source-geometry control, and at least one result-space control.
- `result-space-only` emits no source-geometry or fill claim; it preserves visible gradients, local contrast, shadows, material response, or spill without inventing a rig.
- `diagnostic-only` emits no source-geometry or fill claim.
- Low-confidence source hypotheses use `result-space-only` or `diagnostic-only`.

Apparent source size owns penumbra or edge softness. Fill owns key/fill separation. Local form contrast owns the amplitude of internal modeling. Keep these effects separate even when one compact sentence carries several clauses.

## Apparent illumination signature

Do not reduce the visible result to physical `light intensity`. Build an apparent-illumination signature from independently observed axes:

- Color/Tone owns displayed key level, shadow floor, highlight rolloff, and microcontrast.
- Light/Form owns bright-plane coverage, local form contrast, gradient extent, and background spill.

Displayed key level says how high the major relevant tones sit. Bright-plane coverage says how much of the relevant form occupies its broad bright side. Local form contrast says how far adjacent bright and dark form regions separate. Gradient extent says how much surface distance the main transition consumes. Thus a higher-key image may retain the same local contrast, and broad bright coverage may coexist with a deep shadow floor. Preserve these distinctions in analysis, aggregate effects, and prompt controls.

## Shadow attribution

Record a shadow event only when it affects an invariant or likely drift.

- `cast`: one surface or object blocks illumination onto another.
- `self`: a turning surface shades itself.
- `contact-occlusion`: narrow darkness at touching, overlapping, or recessed boundaries.
- `material-response`: absorption or reflection behavior reads as darkness without a distinct shadow event.
- `processing`: local contrast, black-level, vignette, dodge/burn, or tone mapping materially creates the dark region.
- `mixed` or `uncertain`: evidence does not support one owner.

Do not infer source direction from one ambiguous dark patch. Prefer corroborating highlight placement, repeated gradients, cast-shadow displacement, or consistent multi-region behavior.

## Color/Tone ownership boundary

The Light/Form Contract owns bright-plane coverage, local form contrast, gradient extent, spatial distribution, and background spill. The Color/Tone Contract owns displayed value, chroma, hue, illumination color, white balance, displayed key level, shadow floor, highlight rolloff, microcontrast, exposure, and processing response.

When both are present:

- split prompt excerpts whose clauses have different owners;
- do not list one claim in both contracts;
- do not use exposure to satisfy a missing spatial-light effect;
- do not use source geometry to satisfy a missing intrinsic value or hue control;
- every overlapping Color/Tone value, displayed-key, shadow-floor, contrast, or microcontrast control lists the primary spatial light effects it protects;
- place the primary visible Light/Form result before those overlapping tone controls, then review shared contrast language manually because structural validation cannot infer all prose semantics.

After the ledgers are reconciled, no additional lighting or tone prose may be added as a bridge during final composition. Every semantic span in the authored audited prompt must be an exact owned control or a qualified emitted summary; otherwise route it to the correct contract or remove it.

## Analyst-selected measurement

Use measurement only when it resolves a real uncertainty or supports source/render comparison. The optional probe never detects subjects, materials, shadows, or light direction. The analyst chooses every region, relation, and profile.

```json
{
  "metrics_policy": {
    "bright_plateau_delta_l": 5.0,
    "near_clip_l": 98.0
  },
  "regions": [
    {
      "name": "major-plane-a",
      "role": "major-plane",
      "source_bounds": [0.10, 0.20, 0.25, 0.35],
      "comparison_bounds": [0.12, 0.22, 0.27, 0.37]
    },
    {
      "name": "supporting-field",
      "role": "background",
      "source_bounds": [0.70, 0.15, 0.90, 0.35],
      "comparison_bounds": [0.68, 0.16, 0.88, 0.36]
    }
  ],
  "relations": [
    {
      "name": "plane-to-field",
      "left_region": "major-plane-a",
      "right_region": "supporting-field"
    }
  ],
  "profiles": [
    {
      "name": "form-gradient",
      "source_line": [0.20, 0.50, 0.70, 0.50],
      "comparison_line": [0.22, 0.52, 0.72, 0.52],
      "samples": 64,
      "width_px": 3
    }
  ]
}
```

Run:

```bash
python tools/light_probe.py SOURCE --compare RENDER --spec SAMPLING.json
```

The task-specific `metrics_policy` makes threshold-dependent measurements explicit; its illustrated values are not runtime defaults. Region roles may be `major-plane`, `shadow`, `highlight`, `context`, `background`, `material`, or `diagnostic`.

The report may include:

- regional median displayed lightness, shadow-floor p10, high-side p90, robust p90-p10 range, and within-region IQR
- local-neighbor median and p90 lightness differences as scale-dependent microcontrast diagnostics
- optional bright-plateau coverage and near-clip fractions under the declared task policy
- analyst-named regional lightness relations
- profile p10/p50/p90, robust range, net change, and total variation
- monotonicity and a 10–90% transition width only when the profile is sufficiently monotonic
- source/render deltas for the same analyst-named metrics
- profile status and display-space assumptions

Treat these as diagnostic, display-relative measurements. Different geometry, pose, crop, material, texture, or sampling placement can change them. Do not derive prompt text automatically or declare PASS without a justified tolerance policy.

## Controlled revision

When revision is allowed, change only the largest source-supported lighting residual while keeping unrelated controls frozen. Distinguish at least:

- source geometry
- apparent source size or edge softness
- fill structure
- displayed key level and shadow floor, owned by Color/Tone
- bright-plane coverage
- local form contrast
- gradient extent
- highlight rolloff and microcontrast, owned by Color/Tone
- shadow topology
- material response
- background spill
- Color/Tone exposure or processing residual

Create a new prompt version and hash after any edit. Identical-prompt retries sample the same control distribution; they do not correct a systematic lighting error.

## Evaluation matrix

This matrix is for building and promoting a skill-level evaluation suite, not for completing every individual reverse-prompt request. A valid single-source task must remain single-source unless the user supplies or requests comparison material. Across the suite, include held-out causal pairs rather than deriving behavior from one motivating image:

- large near-axis versus large off-axis source
- small near-axis versus small off-axis source
- high global range with low local form contrast
- low global range with a sharp contact shadow
- the same local robust range shifted to a different displayed key level
- similar displayed key level with broad versus narrow bright-plane coverage
- similar bright-plane coverage with different shadow floors
- same surface and geometry under different light
- the same surface with regional light-to-form separation versus spatially uniform illumination
- same light under different geometry or pose
- backlight, rim light, mixed light, flash, and ambient-dominant cases
- diffuse, absorbent, glossy, metallic, translucent, and woven responses
- human and non-human subjects
- photographic and non-photographic media
- the same displayed key with different edge softness or local form contrast
- the same edge softness with flattening versus strong local modeling
- compatible, conflicting, unresolved, and missing user, current-source, and versioned-vocabulary label candidates
- label-present versus axis-equivalent literal-only prompts on the exact target generator/version

Score prompt validity, delivered pixels, pixel fidelity, and user judgment separately. The motivating case is one regression sample, never a runtime default or proof of general success.
