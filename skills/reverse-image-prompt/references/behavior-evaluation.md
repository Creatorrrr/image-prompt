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

Include matched transformation pairs:

- **Invariant-preserving pair:** the primary appeal or proposition remains stable while a flexible dimension such as minor pose, viewpoint, placement, or incidental capture changes.
- **Aesthetic-changing pair:** object inventory stays substantially similar while a primary form, surface, light-to-form, color, hierarchy, topology, or information invariant changes.

The first pair should retain the primary salience signature without overlocking the flexible change. The second should produce a meaningfully different primary signature instead of collapsing to an object list.

Balance appearance-led cases with relationship-led, information-led, mixed, neutral, photographic, and non-photographic cases. Include both human and non-human subjects when those routes are in scope. The current motivating case may remain one regression sample, but its subject parts, colors, garments, pose, or desired values must not become runtime defaults or expected wording.

## Independent prompt pass

For a before/after comparison, give each arm only the raw request, source artifact, applicable skill snapshot, and normal runtime tools. Do not reveal the suspected bug, proposed fix, expected answer, prior prompt, or prior render.

For each arm:

1. Record the internal plan in the schema from `SKILL.md` without exposing it to the downstream image generator.
2. Validate it with `python tools/salience_plan.py PLAN.json` when a persisted evaluation artifact is appropriate.
3. Freeze the authored prompt before generation.
4. Compare prompt semantics without requiring shared wording or headings.

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
  global:
    cast_or_palette_shift: "observed, absent, mixed, or uncertain behavior"
    exposure_behavior: "source-relative exposure response"
    contrast_and_tone_curve: "global and local tone behavior"
    processing_shift: "visible grading or processing behavior"
    source_evidence: []
  regions:
    - id: "region id"
      role: dominant | supporting | edge-frame | low-legibility
      intrinsic_axes:
        - axis: value | chroma | hue
          observation: "source-relative observation"
          confidence: high | medium | low
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
  claim_ids: []
  aggregate_effects:
    - id: "canonical effect id"
      region_id: "known region id or global"
      axis: value | chroma | hue | contrast
      direction: "canonical source-relative direction"
      role: primary | supporting
      target_strength: subtle | moderate | strong
      claim_ids: []
      source_supported: true
      source_evidence: []
```

Every claim listed by the contract carries `perceptual_effects`, each naming one aggregate effect, one causal layer (`intrinsic`, `illumination`, `global-cast`, `exposure`, `processing`, or `hierarchy`), confidence, and evidence. Claims sharing a region, axis, and direction use one canonical effect even when their semantic-slot names differ. Repeating one causal layer is a merge failure. Multiple causal layers are valid only when each layer and their combined pull are independently source-supported.

The schema deliberately contains no preferred hue, skin value, palette, adjective, numeric color, or generator workaround. A hierarchy-layer hue effect additionally requires source evidence that hue contrast itself is invariant.

## Prompt-level rubric

Review the standalone prompt with the source visible and score distinct questions:

- Does the first-order proposition survive without the source image?
- Are primary invariants expressed affirmatively at their source-relative strength?
- Are flexible dimensions allowed to vary without becoming primary locks?
- Does each semantic slot have one owner rather than repeated synonymous emphasis?
- Are intrinsic properties separated from pose/deformation, perspective, lighting/shadow, material interaction/occlusion, and processing?
- Are intrinsic surface color, illumination, global cast, and exposure kept distinct?
- When color or tone is material, are value, chroma, hue, tone-zone response, processing, and neutral-anchor confidence represented at source-relative strength?
- Do differently named claims avoid accumulating the same color or tone direction beyond one supported aggregate target?
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

Include held-out causal pairs spanning materially different subjects and media:

- the same intrinsic surface under different illumination
- different intrinsic surfaces under comparable illumination
- similar hue with changed exposure, chroma, or tone curve
- local colored illumination versus a global cast or palette shift
- low saturation versus simple underexposure
- monochrome, flat-color, mixed-light, photographic, and non-photographic sources
- human and non-human subjects without making either category the runtime default

The motivating image may remain one regression sample, but promotion requires improvement across this causal matrix. Use optional multi-region measurements only as diagnostic evidence; never turn one sample's numeric values or wording into runtime expectations.

Promote a change only when it improves unrelated held-out behavior without material regression in other dominant modes. Keep package PASS, prompt PASS, delivered pixels, pixel fidelity, and user preference as separate claims.

## Anti-overfitting guardrails

- Put source-relative axes and causal distinctions in runtime instructions, not example-specific desired values.
- Do not add a fixed adjective blacklist, fixed global word count, exact source proportions, or generator-specific workaround to solve one case.
- Prefer changing the merge or attribution rule over adding another subject exception.
- Corrections replace or remove amplifying claims; they do not accumulate counter-negatives.
- Treat one case as a regression sample, never as proof that a general rule succeeds or fails everywhere.
