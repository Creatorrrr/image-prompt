# Maintenance and Evaluation

## Before Editing Data

Prefer extending existing entries with aliases, keywords, facets, and embedding text before adding slots or near-duplicate presets. Keep weights moderate and use filters plus facets for specificity.

Every preset needs non-empty `required_slots`. Reusable role recipes should separate `identity_core` from at least two `scene_variants`. Quality rules belong in `photo_prompt_quality_layers.json`, not repeated inside prompt templates.

## Validation

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python -m unittest discover -s tests
```

Run focused contract and generalization tests before the full suite. Review golden changes; update snapshots only when output changes are intentional.

## Semantic Checks

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --generalization-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --quality-gate --quality-runs 2
```

Dictionary-hash fields such as presets, slots, labels, aliases, keywords, embedding text, and facets require a semantic-index refresh. Policy-only and quality-layer-only edits do not.

Rebuild only changed embeddings:

```bash
GEMINI_API_KEY=... .venv/bin/python \
  skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

Do not print or commit API keys.

## Promotion Boundary

Local contract, contradiction, and held-out generalization checks do not prove rendered-image quality. Promotion of broad prompt-policy changes should also use the versioned visual-review artifact and fail closed when cases, required fields, or provenance are missing. Image/API generation is not part of ordinary validation unless the user explicitly authorizes it.
