# Source-visible surface color language

Read this reference only when measured surface color must be translated into stable, human-readable language or when a friendly appearance label is being considered. It applies to human and non-human surfaces. It does not define biological color, demographic identity, material reflectance, or a universal color-naming standard.

## Translation boundary

Keep this chain explicit:

```text
profile-aware source-visible measurement
-> causal review of intrinsic color, illumination, cast, exposure, and processing
-> separate value-depth, chroma, and undertone classes
-> optional finish and evenness evidence
-> analyst-authored friendly-label candidate
-> compatibility review
-> literal axis controls first, optional calibrated summary label second
```

The versioned policy in `surface-color-language-policy.json` is an uncalibrated language prototype. Its bins make repeated descriptions consistent; they are not scientific skin categories or preferred targets. Record its policy ID and classification uncertainty. A different validated policy may be supplied when the task has a color-managed or user-specified target.

Use `tools/color_language.py` only after an analyst has selected a comparable midtone or flat group. The tool classifies provided Lab evidence; it never locates skin, objects, food, paint, or fabric and never emits a production prompt.

```bash
python tools/color_language.py OBSERVATION.json \
  --policy references/surface-color-language-policy.json \
  --candidates LABEL-CANDIDATES.json
```

Minimum observation:

```json
{
  "observation_scope": "source-visible",
  "profile_status": "missing-profile-assumed-srgb",
  "region_id": "analyst-selected-surface",
  "lab_d65": [70.0, 8.0, 12.0],
  "dispersion": {"lightness_range": 5.0, "chroma_range": 4.0},
  "surface_evidence": {
    "finish": {"term": "satin", "confidence": "medium", "source_evidence": ["broad soft reflection without a sharp highlight"]},
    "evenness": {"term": "even", "confidence": "medium", "source_evidence": ["small midtone variation across selected patches"]}
  }
}
```

`finish` and `evenness` are optional analyst observations. They are never inferred from Lab alone. Valid terms are:

- value depth: `very-light`, `light`, `medium`, `deep`, `uncertain`
- chroma: `very-low`, `low`, `moderate`, `rich`, `uncertain`
- undertone: `rosy`, `peach`, `neutral`, `golden`, `olive`, `mixed`, `uncertain`
- finish: `matte`, `satin`, `luminous`, `dewy`, `uncertain`
- evenness: `even`, `naturally-varied`, `freckled`, `uncertain`

Treat `olive` as an undertone, independent of value depth. Treat labels such as `milky` or `porcelain-like` as composite appearance candidates, not exclusive color bins. Their candidate file must state which axis terms they require:

```json
{
  "candidates": [
    {
      "phrase": "candidate appearance label",
      "label_scope": "composite-appearance",
      "axis_requirements": {
        "value_depth": ["very-light"],
        "chroma": ["very-low", "low"],
        "undertone": ["neutral", "rosy", "peach"],
        "finish": ["matte", "satin"],
        "evenness": ["even"]
      }
    }
  ]
}
```

The example describes structure, not a preferred label or target. A candidate with conflicting axes is rejected; one with unresolved finish, evenness, profile, or boundary evidence remains inconclusive. Do not force one label near a classification boundary.

## Prompt actuation

Write literal value, chroma, and undertone controls before any friendly label. Add finish or evenness only when separately visible. A friendly label may summarize those controls once only when its requirements match and exact generator/version response testing has shown acceptable cross-axis behavior. It never replaces an intrinsic axis-control.

For example, prefer the compositional form `very light, low-chroma, neutral-to-peach surface color with a soft satin finish` over a label alone. The particular terms must come from the current source, not this example.

## Anti-overfitting

- Do not store image-specific Lab values, regions, desired words, or coordinates in the policy.
- Do not map color terms to race, ethnicity, nationality, or identity.
- Do not promote a vocabulary chart, a single render, or one generator version into universal semantics.
- Keep the motivating image as a regression sample only.
