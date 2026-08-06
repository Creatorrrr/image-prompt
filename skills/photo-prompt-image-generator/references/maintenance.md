# Maintenance and Evaluation

## Before Editing Data

Prefer extending existing entries with aliases, keywords, facets, and embedding text before adding slots or near-duplicate presets. Keep weights moderate and use filters plus facets for specificity.

Every preset needs non-empty `required_slots`. Reusable role recipes should separate `identity_core` from at least two `scene_variants`. Quality rules belong in `photo_prompt_quality_layers.json`, not repeated inside prompt templates.

For broad candidate coverage, add coherent subject/action/location/prop/surface clusters rather than isolated nouns. Maintain coverage across at least three non-portrait families: ecology and wildlife, technical process and infrastructure, and food systems and community process. Compatibility metadata must make each action reachable from its intended subject tags, while narrow motifs use `requires_primary_any_tags` so a supporting slot cannot accidentally unlock them.

Treat explicit entry `facets` as the authority. Typed operational domains limit implicit tag-to-facet inference to semantically owning slots; for example, a `street` token in a focus entry must not become the scene's `place_type`. Legacy domains retain their historical inference until they are deliberately facet-migrated and their golden outputs reviewed. Use specific taxonomy such as `field_survey` when a generic legacy tag such as `field` would activate an unrelated applicability guard.

Put repeated theme boundaries in quality-layer `applicability_guards`. Use `match_any_tags` for curated taxonomy and `match_any_terms` only for a stable shared marker carried by a legacy family; both require a matching primary subject/location/genre context. Keep generic metadata words such as `role` and `subject` in `intent_routing.literal_subject_stop_terms` so they cannot infer unrelated secondary subjects from entry IDs.

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
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --holdout-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --domain-holdout-v2-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --quality-gate --quality-runs 2
```

The public generalization suite has 54 inspectable cases. The original 24-case holdout and the separate 6-case operational-domain holdout v2 are frozen; do not rewrite their expectations after a failure. Fix a general routing, applicability, schema, or data-coverage defect instead. The real quality gate also evaluates all 67 golden intents, all three rule-mode suites, candidate coverage, diversity, bleed, preset guards, and multi-axis coverage.

Dictionary-hash fields such as presets, slots, labels, aliases, keywords, embedding text, and facets require a semantic-index refresh. Policy-only and quality-layer-only edits do not.

Rebuild only changed embeddings:

```bash
GEMINI_API_KEY=... .venv/bin/python \
  skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

Do not print or commit API keys.

## Promotion Boundary

Local contract, contradiction, public generalization, and frozen holdout checks do not prove rendered-image quality. A `photo-domain-visual-review-plan/v1` file only defines pending cases and must never be passed off as acceptance evidence. Promotion of broad prompt-policy changes should also use the versioned `photo-visual-review/v1` artifact and fail closed on invalid enums, declared preset conflict, surviving body emphasis, missing fields, or missing provenance. Run the combined boundary with `--acceptance-gate --visual-review <path>`; it requires the real semantic quality gate and a passing review artifact. Image/API generation is not part of ordinary validation unless the user explicitly authorizes it.
