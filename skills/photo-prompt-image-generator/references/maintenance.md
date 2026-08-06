# Maintenance and Evaluation

## Before Editing Data

Prefer extending existing entries with aliases, keywords, facets, and embedding text before adding slots or near-duplicate presets. Keep weights moderate and use filters plus facets for specificity.

Every preset needs non-empty `required_slots`. Reusable role recipes should separate `identity_core` from at least two `scene_variants`. Quality rules belong in `photo_prompt_quality_layers.json`, not repeated inside prompt templates.

For broad candidate coverage, add coherent subject/action/location/prop/surface clusters rather than isolated nouns. Maintain coverage across non-portrait families including ecology and biodiversity monitoring, technical process and infrastructure, agriculture and food systems, and repair or circular-material flows. Compatibility metadata must make each action reachable from its intended subject tags, while narrow motifs use `requires_primary_any_tags` so a supporting slot cannot accidentally unlock them. The biodiversity, agriculture-food, and circular-material packs are on-demand typed domains: automatic preset discovery requires an explicit routed domain intent, direct preset selection remains available, their tagged entries cannot leak into legacy presets, and semantic slot selection treats the preset filters as a hard record-coherence contract.

Record external taxonomy research as abstract evidence in `assets/research_evidence.jsonl`. Store the official source URL, the dimensions derived from it, affected candidate IDs, and a reuse note. Do not copy raw prompts, source prose, images, or bulk vocabulary dumps into runtime data.

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
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --retrieval-holdout-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --quality-gate --quality-runs 2 --summary-only --report-json artifacts/photo-quality-gate.json
```

The public generalization suite has 60 inspectable cases. The original 24-case holdout and the separate 6-case operational-domain holdout v2 are frozen; do not rewrite their expectations after a failure. The six-case retrieval holdout v3 intentionally omits preset IDs from generator input and verifies real semantic routing with the shared conservative profile and low novelty so sampler variance does not hide ranking defects. Domain-specific integration axes, craft refinements, and strategies use `profile_match`; the validator rejects unknown profile IDs so a typo cannot silently broaden or disable them. Fix a general routing, applicability, schema, or data-coverage defect instead of weakening a failed holdout. The real quality gate also evaluates all 67 golden intents, the rule-mode suites, preset-free retrieval, candidate coverage, diversity, bleed, preset guards, and multi-axis coverage.

Dictionary-hash fields such as presets, slots, labels, aliases, keywords, embedding text, and facets require a semantic-index refresh. Policy-only and quality-layer-only edits do not.

Rebuild only changed embeddings. The final index defaults to 16 stable compact JSON vector shards plus a human-readable manifest while preserving the exact logical entry order exposed to retrieval code:

```bash
GEMINI_API_KEY=... .venv/bin/python \
  skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

Do not print or commit API keys.

## Promotion Boundary

Local contract, contradiction, public generalization, and frozen holdout checks do not prove rendered-image quality. A `photo-domain-visual-review-plan/v1` file only defines pending cases and must never be passed off as acceptance evidence. Promotion of broad prompt-policy changes should also use the versioned `photo-visual-review/v1` artifact and fail closed on invalid enums, declared preset conflict, surviving body emphasis, missing fields, or missing provenance. Domain-specific `review_focus_results` are part of that boundary: every supplied focus needs evidence and a failed focus fails the case. Non-person operational reviews may mark body, role, or mixin fields `not_applicable`, but must include a case-level reason instead of using a meaningless pass. Run the combined boundary with `--acceptance-gate --visual-review <path>`; it requires the real semantic quality gate and a passing review artifact. Image/API generation is not part of ordinary validation unless the user explicitly authorizes it.
