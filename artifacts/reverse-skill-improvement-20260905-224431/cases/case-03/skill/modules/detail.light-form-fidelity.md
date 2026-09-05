---
id: detail.light-form-fidelity
version: 11
priority: 79
type: detail
tier: 3
facet: detail-risk
facet_values:
  - lighting-fidelity
  - light-direction
  - shadow-topology
  - light-to-form
  - material-light-response
  - background-spill
triggers:
  - user explicitly prioritizes faithful lighting, shadow, or light-to-form reproduction
  - illumination or shadow topology materially carries the image
  - source/render comparison identifies lighting as a material residual
avoid_when:
  - lighting is incidental and the selected medium module is sufficient
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
  - core.background-color
conflicts: []
provides_anchors:
  - light_form_contract
  - observed_light_result
  - source_geometry_fill_separation
  - global_local_light_contrast
  - shadow_ownership
  - material_light_response
  - pose_light_dependency
  - lighting_color_contract_handoff
  - light_control_ledger
  - render_light_verification
  - apparent_illumination_signature
  - bright_plane_coverage
  - lighting_language_translation
  - lighting_friendly_label_review
  - lighting_label_external_source
---

# Detail: lighting and light-to-form fidelity

## When to load

Load only when illumination, shadow topology, light-induced form, material response, or background spill is an invariant; when the user explicitly requests lighting fidelity; or when a source/render comparison finds a material lighting residual. Do not load merely because an image is lit.

A source/render loss of source-visible value separation between adjacent regions of one surface is a material residual when that separation carries form or hierarchy. Route it here even if the overall lighting looks ordinary; do not compensate by strengthening intrinsic anatomy, object volume, garment fit, or surface color.

## Three-stage Light/Form Contract

In `prompt`, preserve only the P0/P1 visible light result, its named region relation, and any protected local effect. Prefer result-space language when cause is uncertain; do not enumerate every lighting axis or build a final ledger.

In `audited`, measured lighting work, or source/render evaluation: Build a source-relative Light/Form Contract only when illumination materially carries fidelity.

Keep three stages separate:

1. **Observation:** the visible spatial light result.
2. **Actuation:** the smallest literal prompt controls that reproduce that result.
3. **Verification:** what a delivered render actually reproduced.

Treat the observed light-to-form result as evidence and the physical lighting setup as a confidence-rated hypothesis. One image rarely identifies a unique lamp, modifier, fill source, or post-processing path. When the cause is uncertain, preserve the visible result with result-space relations rather than letting an invented rig carry the prompt alone.

## Visible result before rig inference

Record the largest continuous bright and dark masses before small highlights. Map global tonal range, bright-plane coverage, local form contrast, gradient character and extent, edge softness, background spill, and the relative visibility of major planes.

Keep global tonal range separate from local form contrast. A wide scene range or dark frame does not require strong internal modeling; a compressed scene may still contain a hard contact edge.

Build apparent illumination from displayed key level, bright-plane coverage, shadow floor, local form contrast, gradient extent, highlight rolloff, microcontrast, and background spill. Keep bright-plane coverage separate from displayed key level and local form contrast. An ordinary image supports this result-space signature, not physical illuminance or lamp power.

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Describe what the light does to visible form instead of substituting broad mood or quality shorthand.

## Source hypothesis

Separate source geometry, apparent source size, and fill structure. Record source count, direction relative to camera and subject, elevation, apparent angular size, fill or bounce behavior, confidence, and visible evidence only when they matter.

Apparent source size owns shadow-edge softness; it does not automatically own fill level or local contrast. A large off-axis source can remain sculpting, and a small near-axis source can flatten form.

Use `physical-cause` or `physical-plus-result` actuation only with medium- or high-confidence source evidence. With low confidence, use `result-space-only` or keep the hypothesis diagnostic.

## Spatial effects and shadow ownership

For each material region effect, record its role as broad plane, gradient, highlight, shadow, rim, or spill; its source-relative strength; edge character; and evidence. Use semantic region relations rather than fixed coordinates unless exact placement is itself invariant.

When a major region mixes material lighting topology, declare only the needed source-derived Light/Form subregions: major plane, shadow zone, transition, material mass, context, or spill. Each needs an exact prompt anchor and visible evidence; never install a fixed part, direction, or coordinate.

When adjacent regions of the same material differ because of light-to-form, record the target `region_id` and distinct `reference_region_id` in both the observed region effect and aggregate actuation, then record the transition as a gradient or shadow event when visible. Let the emitted result-space control preserve that relation and contain the exact anchors for every declared Light/Form subregion it compares; do not turn one motivating region name, direction, value, or threshold into a reusable default.

Assign each material dark region to cast shadow, self-shadow, contact or occlusion, material response, processing, mixed, or uncertain ownership. Do not promote a small contact shadow into a broad directional-light field, and do not encode an illumination-induced contour as intrinsic form.

Keep material response and background spill separate from source intensity. Matte, glossy, metallic, translucent, woven, and absorbent surfaces under one light may have different highlight width, black level, and texture visibility.

Let Light/Form alone own source-visible highlight width or strength, spatial black-level response, and bright-plane coverage. Generic object or material clauses must not repeat or counter that lighting direction.

## Pose and geometry dependence

Record whether each light pattern is pose-bound, pose-robust, mixed, or uncertain. When pose is flexible, preserve relational outcomes such as major-plane balance, gradient depth, or light-to-form class while allowing exact highlight coordinates to move. When pose is locked and the evidence is stable, tighter placement may be justified.

## Color and tone handoff

Let the Light/Form Contract own spatial illumination structure and the Color/Tone Contract own displayed color, exposure, and tone response. More specifically, Light/Form owns bright-plane coverage, gradient extent, and background spill; Color/Tone owns displayed key level, shadow floor, highlight rolloff, and microcontrast. Do not emit the same brightness or contrast pull independently from both contracts.

## Controlled lighting language

When compact human-readable lighting language is useful, read `references/lighting-language.md`. Classify displayed key level, shadow floor, edge softness, local form contrast, bright-plane coverage, gradient extent, directionality, and fill structure independently before composing any summary. This language layer may read evidence owned by both contracts, but it owns no new lighting or tone effect.

The policy may compose one explanation-only axis summary without a preferred preset. A named candidate may come from the user, versioned vocabulary, or a provenance-bound current-source reading after independent observation. Keep conflicts and uncertainty non-emitted.

Literal lighting controls remain authoritative. Emit a current-source label once only with compatibility, high/medium confidence, P0/P1 priority, material-drift omission, and immediate owned decomposition. Model calibration adds exact response evidence. A label never fills a missing axis or justifies a rig.

## Final prompt control ledger


<!-- profile:audited -->
In `audited`: Copy every exact lighting excerpt into the ledger with one claim, owner, complete effects, and declared regional anchors. Final composition adds no lighting, shadow, gradient, or material-response prose.
<!-- /profile -->
 In `prompt`, retain one owner and decisive visible effect without a ledger. In either profile, split cross-owner compounds and replace overstrong controls rather than appending counter-negatives.

When measured comparison is warranted, read `references/lighting-reproduction-evaluation.md`. Use only analyst-selected regions and profiles, retain source/profile uncertainty, and never convert diagnostic measurements directly into prompt wording.

## Output and diagnosis

When primary, order one passage by visible topology, fill/local contrast, shadow owner, then material/spill. Put this spatial result before overlapping Color/Tone controls. When supporting, use the smallest relation.

Diagnose source/render differences as source geometry, apparent size, fill, local form contrast, shadow topology, material response, background spill, exposure or processing, or unresolved. Prompt validation never substitutes for rendered-pixel lighting verification.

## Optional negative contribution

Reject only source-likely lighting drift such as an unsupported key/fill split, wrong shadow owner, exaggerated sculpture or flattening, enlarged specular response, or excess background spill. Do not install fixed lighting words, directions, ratios, subject regions, or numeric targets.
