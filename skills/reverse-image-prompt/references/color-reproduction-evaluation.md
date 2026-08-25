# Color reproduction and control-effectiveness evaluation

Read this reference only when routed color/tone fidelity requires measured source evidence, source/render comparison, actual generation, or controlled color revision. Ordinary incidental-color prompt extraction does not need it.

## Evidence boundary

Keep three artifacts distinct:

1. **Observation contract:** source-visible or color-managed evidence from the input.
2. **Actuation contract:** literal generator controls intended to carry that evidence.
3. **Verification report:** measured delivered pixels and an optional acceptance policy.

A correct observation and structurally valid prompt do not prove that the downstream model obeyed the control. A render that was blocked or never returned is unscored. Measurements describe displayed image color, not biological, material, demographic, or scene-referred truth.

## Reference classification

Classify any auxiliary swatch, chart, named palette, or example before using it:

- `calibrated-color-target`: measured values and a defined observation condition are available.
- `color-managed-reference`: a trustworthy embedded profile or explicit managed space supports display-color comparison.
- `uncalibrated-vocabulary-chart`: names or swatches are present without calibration evidence.
- `photographic-example`: subject color is mixed with lighting, exposure, optics, makeup, material finish, and processing.

Only calibrated or color-managed references may establish numeric targets. Vocabulary charts may suggest language but cannot define one true color. If two references use one label for materially different swatches, downgrade the label to vocabulary. Never turn a human color label into a racial, ethnic, national, or demographic proxy.

## Sampling design

The analyst chooses semantic regions. Tools must not auto-detect skin, products, food, paint, clothing, or other target classes.

Use several small, internally coherent patches when the image permits. Avoid boundaries, specular highlights, deep occlusion, clipped pixels, compression blocks, and mixed materials unless one of those effects is itself the target.

Separate groups by both semantic role and tone zone:

- target midtone or flat groups estimate displayed intrinsic value, chroma, and hue
- target highlight groups estimate highlight response and clipping or rolloff
- target shadow groups estimate shadow response, compression, and cast
- contextual or neutral-like groups estimate shared exposure, cast, and processing movement

Do not mix highlight, midtone, and shadow patches in a group used to drive an intrinsic axis. A `mixed` evidence scope is diagnostic-only.

When source and render geometry differ, choose source and render bounds independently while retaining matching region names, semantic roles, and tone zones. Coordinate equality is not semantic correspondence.

### Sampling specification

`color_probe.py --spec` accepts JSON of this form:

```json
{
  "regions": [
    {
      "name": "target-midtone-a",
      "source_bounds": [0.1, 0.1, 0.2, 0.2],
      "comparison_bounds": [0.2, 0.1, 0.3, 0.2],
      "semantic_role": "target",
      "tone_zone": "midtone",
      "purpose": "intrinsic-displayed-color"
    },
    {
      "name": "target-midtone-b",
      "source_bounds": [0.3, 0.1, 0.4, 0.2],
      "comparison_bounds": [0.4, 0.1, 0.5, 0.2],
      "semantic_role": "target",
      "tone_zone": "midtone",
      "purpose": "intrinsic-displayed-color"
    },
    {
      "name": "context-a",
      "source_bounds": [0.7, 0.1, 0.8, 0.2],
      "comparison_bounds": [0.65, 0.1, 0.75, 0.2],
      "semantic_role": "context",
      "tone_zone": "flat",
      "purpose": "global-cast-and-exposure"
    },
    {
      "name": "context-b",
      "source_bounds": [0.7, 0.3, 0.8, 0.4],
      "comparison_bounds": [0.65, 0.3, 0.75, 0.4],
      "semantic_role": "context",
      "tone_zone": "flat",
      "purpose": "global-cast-and-exposure"
    }
  ],
  "groups": [
    {
      "name": "target-midtone",
      "region_names": ["target-midtone-a", "target-midtone-b"],
      "semantic_role": "target",
      "tone_zone": "midtone",
      "purpose": "intrinsic-displayed-color"
    },
    {
      "name": "context",
      "region_names": ["context-a", "context-b"],
      "semantic_role": "context",
      "tone_zone": "flat",
      "purpose": "global-cast-and-exposure"
    }
  ]
}
```

Bounds are normalized. `comparison_bounds` may be omitted when the same bounds remain valid.

## Measurement interpretation

Use CIELAB axes separately:

- `L*` for displayed value or lightness
- `a*` and `b*` for opponent-color movement
- `C*` for chroma magnitude
- circular hue difference only when chroma supports a stable hue reading
- CIEDE2000 as a summary distance, never as a replacement for axis diagnosis

Prefer equal weighting of region medians so a large patch does not overpower smaller semantic peers. Keep the source group dispersion with its center; a center without dispersion overstates precision.

An embedded profile converted successfully to sRGB supports a color-managed relative comparison. Missing or failed profiles support only an assumed-display-space relative comparison. Neither establishes scene reflectance or intrinsic biological color.

## Source-visible surface language

When measured color must become stable human-readable language, read `surface-color-language.md` and preserve this order:

```text
profile-aware measurement
-> causal review
-> value-depth, chroma, and undertone classification
-> separately observed finish and evenness
-> optional deterministic axis composition for an analyst-named surface
-> optional user, versioned-vocabulary, or provenance-bound current-source label review
```

The controlled terms are source-visible axes, not identity categories. Undertone remains independent of value depth. A controlled descriptor is a deterministic wrapper around the current literal axes, not a demographic or friendly label; mixed, uncertain, or low-confidence included evidence yields no phrase. The plan, not the classifier, decides emission and must link every substring to an owned control. A friendly label is never sufficient by itself: a current-source candidate may be retained once only with compatible axes, high/medium confidence, P0/P1 priority, a `material-drift` omission counterfactual, and immediate literal decomposition. Exact generator/version response evidence separately determines actuation reliability.

When persisted, place the classifier result under `surface_color_language` with `policy_id`, `policy_status`, `observation_scope`, `profile_status`, `region_id`, source evidence, and all five axis classifications. An optional `controlled_descriptor` retains reconstructed fields plus evidence, emission decision, and axis-control IDs. Friendly-label reviews retain provenance, requirements, matched/conflicting/unresolved axes, and status. Do not store image-specific target values, composed phrases, or preferred labels in the policy file.

## Displayed tone-response axes

When apparent illumination is material, keep four Color/Tone-owned axes separate:

- `displayed-key-level`: `very-low`, `low`, `middle`, `high`, `very-high`, or `uncertain`
- `shadow-floor`: `crushed`, `deep`, `open`, `lifted`, `mixed`, or `uncertain`
- `highlight-rolloff`: `clipped`, `abrupt-unclipped`, `gradual-unclipped`, `compressed`, `mixed`, or `uncertain`
- `microcontrast`: `suppressed`, `natural`, `emphasized`, `mixed`, or `uncertain`

These are displayed results, not a claim about physical lamp power. Record them under `displayed_tone_response` as region-and-axis entries with `class`, `role`, `confidence`, `emission`, source evidence, and either an aggregate effect ID or a diagnostic non-emission reason. Give every Color/Tone region a non-trivial exact prompt anchor. Add `tone_scope`: `global`, one Color/Tone `region`, or a declared `region-group`, plus affected/protected region IDs and evidence; regional scopes reuse the declared anchor. A required axis follows the same effect/claim/axis-control chain as a required intrinsic axis, and its literal excerpt retains that anchor as a token-bounded span. Split a coarse region when it mixes materially bright and dark subregions. Light/Form separately owns bright-plane coverage and gradient extent.

## Global and target-local decomposition

For matching groups, compute each render-minus-source Lab movement. Let `G` be the component-wise median movement across contextual groups. For a target group with movement `T`, compute the target-local residual `R = T - G`.

- large `G` with small `R`: principally global exposure, cast, or processing
- small `G` with large `R`: principally target-local or intrinsic rendering drift
- large `G` and large `R`: mixed
- weak, inconsistent, or uncalibrated evidence: inconclusive

For local chroma and hue, subtract `G` in Lab first, then recompute the corrected target's chroma and hue relative to its source. Do not subtract hue angles directly.

## Acceptance policy

`color_fidelity_eval.py` reports decomposition without a policy, but returns `unscored`. A policy may set any subset of these positive tolerances:

```yaml
target:
  max_abs_delta_l: <positive task-specific tolerance>
  max_abs_delta_c: <positive task-specific tolerance>
  max_abs_hue_degrees: <positive task-specific tolerance>
  max_delta_e2000: <positive task-specific tolerance>
context:
  max_abs_delta_l: <positive task-specific tolerance>
  max_opponent_shift: <positive task-specific tolerance>
```

Omit unused keys. Choose tolerances from source-region dispersion, profile uncertainty, repeated-render variance, task importance, and any user-specified requirement. If no justified policy exists, do not invent a PASS.

## Actuation contract

For each material intrinsic axis, link:

```text
region intrinsic axis
-> same-region and same-axis aggregate effect
-> emitted claim
-> literal intrinsic axis-control
```

An axis-control owns one region, one axis, and one causal layer. Split literal prompt excerpts when a sentence contains several clauses. A hierarchy or exposure relationship cannot replace a missing intrinsic surface-value control. A justified compound-control may compress secondary multi-axis evidence, but it cannot satisfy a required intrinsic axis.

For each required displayed-tone axis, use the same chain but restrict causal ownership: displayed key and shadow floor may be illumination, exposure, or processing; highlight rolloff may be exposure or processing; microcontrast may be illumination or processing. Its scope cannot include protected regions, and a global claim needs global evidence. One generic `stronger lighting` clause cannot satisfy several axes or any Light/Form spatial axis.

Appearance metaphors are `explanation-only` or `unverified` by default. A `source-evidence-qualified` metaphor may emit once when it is a provenance-bound current-source P0/P1 invariant, omission causes material drift, compatibility passes, and already-owned axes immediately unpack it. A `model-calibrated` metaphor additionally records exact generator-and-version evidence that the phrase reinforces those axes without unacceptable cross-axis leakage.

An emitted controlled descriptor follows a different rule: its full phrase must be exactly reconstructible from current classified axes, and its `axis_control_ids` must point to literal same-region value, chroma, and hue controls. Optional finish points to a separately owned generic surface control. The wrapper appears once and contains those excerpts; it is not an additional color direction or proof that the generator obeyed them.

Exact RGB, hex, Lab, or color-temperature values remain evaluation evidence unless the named generator documents numeric color control and the task supports that precision.

## Generator response calibration

Natural-language color controls, including deterministic axis compositions, are model actuators rather than universal color definitions. Maintain response evidence by exact model and version only when enough independent evaluation exists.

For each tested descriptor, record:

- intended axis and source-relative direction
- observed median Lab movement
- repeated-render variance
- movement in unintended axes
- human and non-human context coverage
- photographic and non-photographic coverage when applicable
- model identifier, version, settings, and reference handling

Use matched prompts that change one control at a time. Do not promote the closest single render; compare distributions. Do not install a fixed preferred color, demographic mapping, adjective blacklist, or one-case workaround.

## Reference-conditioned generation

When the named generator and user request permit visual conditioning, prefer the strongest supported route:

1. direct source-image edit or reference conditioning
2. analyst-selected highlight, midtone, shadow, and context palette reference
3. generator-version-calibrated text controls
4. uncalibrated generator-agnostic text

Keep the production prompt standalone: do not mention an absent reference inside its text. Pass a reference through the tool input. Respect a text-only request.

## Retry and revision

An identical-prompt retry samples the same control distribution. Preserve exact bytes and hash when the user requests frozen retries, measure each delivered render, and stop at the user's cap. Do not claim that retries corrected a systematic axis error.

When prompt revision is allowed, change only the largest policy-normalized residual axis, create a new prompt version and hash, and re-evaluate. If no policy exists, report the measured residuals and ask or infer only within the user's stated scope; do not silently optimize several axes at once.

## Reporting

Report these outcomes separately:

1. package and route validity
2. salience-plan and axis-coverage validity
3. prompt freeze/integrity
4. delivered-render availability
5. color evaluation: pass, fail, or unscored
6. drift classification and dominant residual axis
7. user judgment

The motivating image may be a regression sample, but promotion requires unrelated human and non-human, photographic and non-photographic, profile-present and profile-missing cases.
