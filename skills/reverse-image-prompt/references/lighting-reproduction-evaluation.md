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
    gradient_character: "long and shallow, short and steep, stepped, mixed, or uncertain"
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
  region_effects:
    - id: "effect observation id"
      region_id: "known major region"
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
  claim_ids: []
  aggregate_effects:
    - id: "canonical light effect"
      region_id: "known major region or global"
      axis: source-geometry | fill | local-form-contrast | shadow-topology | material-response | background-spill
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
      owner: source-geometry | fill | local-form-contrast | shadow-topology | material-response | background-spill
      aggregate_effect_ids: []
```

Candidate claims listed by this contract carry `lighting_effects`, each with an `aggregate_effect_id`, confidence, and source evidence. Every listed claim is emitted, represented exactly once in `emitted_controls`, and references the same complete effect set. A `prompt_excerpt` may be the smallest exact clause inside a compact sentence; it need not be a standalone sentence or visible output section. Two effect IDs may not hide the same region, axis, and direction.

## Cause and result rules

- `physical-cause` requires medium- or high-confidence source evidence and a source-geometry control.
- `physical-plus-result` requires medium- or high-confidence source evidence, a source-geometry control, and at least one result-space control.
- `result-space-only` emits no source-geometry or fill claim; it preserves visible gradients, local contrast, shadows, material response, or spill without inventing a rig.
- `diagnostic-only` emits no source-geometry or fill claim.
- Low-confidence source hypotheses use `result-space-only` or `diagnostic-only`.

Apparent source size owns penumbra or edge softness. Fill owns key/fill separation. Local form contrast owns the amplitude of internal modeling. Keep these effects separate even when one compact sentence carries several clauses.

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

The Light/Form Contract owns spatial distribution and form modeling. The Color/Tone Contract owns displayed value, chroma, hue, illumination color, white balance, exposure, rolloff, black-level compression, and processing response.

When both are present:

- split prompt excerpts whose clauses have different owners;
- do not list one claim in both contracts;
- do not use exposure to satisfy a missing spatial-light effect;
- do not use source geometry to satisfy a missing intrinsic value or hue control;
- review shared contrast language manually because a structural validator cannot infer prose semantics.

## Analyst-selected measurement

Use measurement only when it resolves a real uncertainty or supports source/render comparison. The optional probe never detects subjects, materials, shadows, or light direction. The analyst chooses every region, relation, and profile.

```json
{
  "regions": [
    {
      "name": "major-plane-a",
      "source_bounds": [0.10, 0.20, 0.25, 0.35],
      "comparison_bounds": [0.12, 0.22, 0.27, 0.37]
    },
    {
      "name": "supporting-field",
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

The report may include:

- regional median displayed lightness and IQR
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
- local form contrast
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
- same surface and geometry under different light
- same light under different geometry or pose
- backlight, rim light, mixed light, flash, and ambient-dominant cases
- diffuse, absorbent, glossy, metallic, translucent, and woven responses
- human and non-human subjects
- photographic and non-photographic media

Score prompt validity, delivered pixels, pixel fidelity, and user judgment separately. The motivating case is one regression sample, never a runtime default or proof of general success.
