# Source-visible lighting language

Read this reference only when source-visible lighting must be translated into a compact human-readable summary or when a friendly lighting label is being considered. It applies to human and non-human subjects and photographic and non-photographic media. It does not identify a physical rig, lamp power, exposure value, or universal lighting style.

## Translation boundary

Keep this chain explicit:

```text
visible spatial-light evidence
-> causal review of displayed tone, source geometry, fill, form contrast, gradient, shadow, material, and processing
-> separate source-relative lighting-axis classes
-> explanation-only controlled composite summary
-> optional user, versioned-vocabulary, or current-source aggregate candidate with provenance
-> compatibility review
-> optional qualified label once, immediately followed by literal axis controls
-> delivered-pixel verification
```

The versioned policy in `lighting-language-policy.json` is an uncalibrated language prototype. Its terms make repeated descriptions consistent; they are not physical-light measurements, preferred targets, or a closed style taxonomy.

The policy contains no friendly lighting labels or preferred axis combinations. A friendly-label candidate may come from the user's request, an explicitly versioned task vocabulary, or a provenance-bound aggregate reading formed from the current source after independent axis observation. Do not select from a hidden preferred list or force a label when the global reading is not material.

## Axis classification

Classify every policy axis independently. In particular, edge softness does not determine local form contrast, displayed key does not determine shadow floor, and bright-plane coverage does not determine gradient extent. Use `mixed` or `uncertain` rather than forcing a family.

Use `tools/lighting_language.py` only after an analyst has identified the visible result and supplied evidence for each resolved axis. The tool does not inspect images or infer a rig.

```bash
python tools/lighting_language.py OBSERVATION.json \
  --policy references/lighting-language-policy.json \
  --candidates LABEL-CANDIDATES.json
```

Observation shape; placeholders are structural variables, not suggested values:

```json
{
  "observation_scope": "<policy-supported-scope>",
  "region_id": "<known-major-region-or-global>",
  "source_evidence": ["<visible-evidence>"],
  "axis_classification": {
    "displayed_key_level": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "shadow_floor": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "edge_softness": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "local_form_contrast": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "bright_plane_coverage": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "gradient_extent": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "directionality": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]},
    "fill_structure": {"term": "<policy-term>", "confidence": "<confidence>", "source_evidence": ["<evidence>"]}
  }
}
```

The tool may compose one `controlled_summary` from literal tokens for sufficiently confident core axes. That summary is always `explanation-only`, never a friendly-label candidate, physical-rig claim, or production prompt control. When a core axis is uncertain, the summary remains inconclusive rather than completing a familiar archetype.

## Friendly-label compatibility

Candidate shape; the skill never supplies the placeholder values:

```json
{
  "candidate_source": {
    "kind": "<user-supplied-source-visible-approximation-or-versioned-vocabulary>",
    "reference": "<request-field-vocabulary-id-or-artifact-reference>"
  },
  "candidates": [
    {
      "phrase": "<provenance-bound-candidate-label>",
      "label_scope": "<declared-label-scope>",
      "axis_requirements": {
        "<axis>": ["<allowed-policy-term>"]
      }
    }
  ]
}
```

A composite-lighting candidate must declare requirements for displayed key level, edge softness, and local form contrast. Narrower scopes declare their corresponding axis. Additional axes may be required by the source or external vocabulary. A conflicting candidate is rejected; low-confidence, mixed, or uncertain required evidence keeps it inconclusive.

## Prompt actuation

In diagnostic explanation, present a controlled summary or compatible friendly label before its decomposed axes when that improves readability. In a production prompt, a qualified aggregate label may also lead once when its omission would materially change the source reading; literal region, direction, coverage, contrast, gradient, shadow, and displayed-tone controls must immediately follow and remain authoritative.

A current-source friendly label may appear once when provenance is `source-visible-approximation`, compatibility passes, confidence is high or medium, viewer priority is P0/P1, omission would cause `material-drift`, and the following literal clauses immediately unpack every required axis. A model-calibrated label additionally records exact generator/version testing for unintended movement in exposure, color, material response, background, polish, or composition. Calibration is response evidence, not the sole permission to state a visible lighting gestalt.

Do not let a label satisfy source geometry, fill, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, background spill, displayed key, shadow floor, highlight rolloff, or microcontrast by itself.

## Anti-overfitting

- Do not store image-specific directions, regions, numeric targets, preferred words, or preferred axis combinations in the policy.
- Do not install named lighting examples or mood/style presets in runtime instructions.
- Do not infer a physical setup from label compatibility.
- Do not promote one render or one generator version into universal semantics.
- Evaluate labels across unrelated subjects, materials, media, key levels, edge classes, and local-contrast classes.
- Keep the motivating image as a regression sample only.
