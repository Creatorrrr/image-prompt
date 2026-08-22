# Source-visible surface color language

Read this reference only when measured surface color must be translated into stable, human-readable language or when a friendly appearance label is being considered. It applies to human and non-human surfaces. It does not define biological color, demographic identity, material reflectance, or a universal color-naming standard.

## Translation boundary

Keep this chain explicit:

```text
profile-aware source-visible measurement
-> causal review of intrinsic color, illumination, cast, exposure, and processing
-> separate value-depth, chroma, and undertone classes
-> optional finish and evenness evidence
-> externally supplied friendly-label candidate with provenance
-> compatibility review
-> literal axis controls first, optional calibrated summary label second
```

The versioned policy in `surface-color-language-policy.json` is an uncalibrated language prototype. Its bins make repeated descriptions consistent; they are not scientific skin categories or preferred targets. Record its policy ID and classification uncertainty. A different validated policy may be supplied when the task has a color-managed or user-specified target.

This skill contains no semantic friendly-label examples or preferred friendly-label list. A candidate may come only from the user's request or an explicitly versioned task vocabulary. If neither exists, stop after axis classification rather than inventing a label.

Use `tools/color_language.py` only after an analyst has selected a comparable midtone or flat group. The tool classifies provided Lab evidence; it never locates skin, objects, food, paint, or fabric and never emits a production prompt.

```bash
python tools/color_language.py OBSERVATION.json \
  --policy references/surface-color-language-policy.json \
  --candidates LABEL-CANDIDATES.json
```

Observation shape (replace every placeholder with current-source evidence before using it as tool input):

```json
{
  "observation_scope": "source-visible",
  "profile_status": "<observed-profile-status>",
  "region_id": "<analyst-selected-region-id>",
  "lab_d65": ["<measured-L-star>", "<measured-a-star>", "<measured-b-star>"],
  "dispersion": {"lightness_range": "<measured-range-or-null>", "chroma_range": "<measured-range-or-null>"},
  "surface_evidence": {
    "finish": {"term": "<observed-finish-term>", "confidence": "<confidence>", "source_evidence": ["<visible evidence>"]},
    "evenness": {"term": "<observed-evenness-term>", "confidence": "<confidence>", "source_evidence": ["<visible evidence>"]}
  }
}
```

`finish` and `evenness` are optional analyst observations. They are never inferred from Lab alone. Valid terms are:

- value depth: `very-light`, `light`, `medium`, `deep`, `uncertain`
- chroma: `very-low`, `low`, `moderate`, `rich`, `uncertain`
- undertone: `rosy`, `peach`, `neutral`, `golden`, `olive`, `mixed`, `uncertain`
- finish: `matte`, `satin`, `luminous`, `dewy`, `uncertain`
- evenness: `even`, `naturally-varied`, `freckled`, `uncertain`

Treat every undertone term as independent of value depth. A composite appearance label is not an exclusive color bin. Its candidate file must preserve external provenance and declare the axis terms it requires. The following is a non-runnable schema shape; placeholders are structural variables, not suggested values:

```json
{
  "candidate_source": {
    "kind": "<user-supplied-or-versioned-vocabulary>",
    "reference": "<request-field-vocabulary-id-or-artifact-reference>"
  },
  "candidates": [
    {
      "phrase": "<externally-supplied-label>",
      "label_scope": "<declared-label-scope>",
      "axis_requirements": {
        "value_depth": ["<allowed-value-depth-class>"],
        "chroma": ["<allowed-chroma-class>"],
        "undertone": ["<allowed-undertone-class>"],
        "finish": ["<allowed-finish-class>"]
      }
    }
  ]
}
```

For `composite-appearance`, the requirements must cover value depth, chroma, undertone, and at least one of finish or evenness. Other scopes require their corresponding axis. A candidate with conflicting axes is rejected; one with unresolved finish, evenness, profile, or boundary evidence remains inconclusive. Do not force one label near a classification boundary.

## Prompt actuation

Write literal value, chroma, and undertone controls before any friendly label. Add finish or evenness only when separately visible. A friendly label may summarize those controls once only when its requirements match and exact generator/version response testing has shown acceptable cross-axis behavior. It never replaces an intrinsic axis-control.

Write a compact sequence in the order value depth, chroma, and undertone, followed only by separately observed finish or evenness. Select every term from current-source classification; do not copy a target combination from this reference.

## Anti-overfitting

- Do not store image-specific Lab values, regions, desired words, or coordinates in the policy.
- Do not map color terms to race, ethnicity, nationality, or identity.
- Do not promote a vocabulary chart, a single render, or one generator version into universal semantics.
- Do not place named friendly-label examples or concrete preferred axis combinations in runtime instructions; keep semantic cases in held-out evaluation only.
- Keep the motivating image as a regression sample only.
