# Maintenance and Evaluation

## Before Editing Data

Prefer extending existing entries with aliases, keywords, facets, and embedding text before adding slots or near-duplicate presets. Keep weights moderate and use filters plus facets for specificity.

Every preset needs non-empty `required_slots`. Reusable role recipes should separate `identity_core` from at least two `scene_variants`. Quality rules belong in `photo_prompt_quality_layers.json`, not repeated inside prompt templates.

Hybrid augmentation route definitions, adoption budgets, adult-appeal defaults and eligibility, carrier mappings, and cross-combination risk groups also belong in `photo_prompt_quality_layers.json`. Keep route slots backed by real dictionary slots and adult candidates backed by the declared `inventory_preset_id` filters. Add an axis candidate through that data contract; do not hard-code prompt prose in the generator. Preserve `sensual_editorial` and `fetish_fashion` as independent axes rather than a mutually exclusive mode enum; keep their configured defaults synchronized with the CLI constants.

For broad candidate coverage, add coherent subject/action/location/prop/surface clusters rather than isolated nouns. Maintain coverage across non-portrait families including ecology, technical systems, access and learning, sports mechanics, heritage, agriculture and food systems, lifecycle evidence, disasters, place change, natural processes, and reusable visual structure. Compatibility metadata must make each action reachable from its intended subject tags, while narrow motifs use `requires_primary_any_tags` so a supporting slot cannot accidentally unlock them. Evidence-led typed packs are on-demand domains: automatic preset discovery requires an explicit routed domain intent, direct preset selection remains available, their tagged entries cannot leak into legacy presets, and semantic slot selection treats the preset filters as a hard record-coherence contract. Research-extension presets also use `auto_optional_policy: authored_filters_only`, so global narrative or motion options cannot enter unless the preset explicitly filters that slot.

CJK commercial-narrative worldbuilding lives in the separate `cjk_narrative_world` domain. Keep platform category, market-term, trope, subtype, industry-term, and living-practice distinctions in research evidence and typed routing rules, not as `term_level`, `market_origin`, or `cultural_provenance` fields on runtime candidates. A compound route may share institutional logic, but its manifestation scenes must be atomic: VRMMO/card/probability, kaiju/mecha, territory/dungeon, and magical-transformation/idol/virtual variants cannot cross-select scene slots. Culture-sensitive spirit and afterlife scenes use original abstract visual mechanisms and never collect or reproduce living ritual instructions, sacred text, or restricted knowledge.

Adult character-mechanism research uses the private `character_moe_grammar` routing domain and the neutral v3 public profile `character_scene_grammar`. Keep its graph outside the ordinary sampler slots: runtime anchors may be routers or guards, while each atomic scene selects exactly one primary `visual_atom` and at most two support atoms from one compatible topic edge. Apply the fixed priority `observable_action > relationship_stake > expression_or_gaze > morphology_or_state > costume`. Do not store market-origin or audience-familiarity classifications on runtime scenes; explicit-adult, identity, orientation, and personality guards cannot select ethnicity, national costume, face/body proportions, or a protected character design. Every route needs at least three atomic scenes and two functions, with no static-portrait majority.

`authorship_basis`, `audience_scope`, `audience_familiarity`, `character_family`, `character_topic`, `content_basis`, `cultural_provenance`, `market_origin`, and `term_level` are retired runtime metadata keys; the dictionary validator rejects their reintroduction. Keep `safety_tier` as the only control-only facet because the hard guard consumes it. Preset-family routing IDs remain internal rather than candidate evidence. Likewise, keep adult-eligibility tags, structural character-scene tags, nonvisual graph tags, router nodes, policy IDs, compatibility-edge IDs, and guard IDs out of public candidate tags. Ownership or legal-status phrases such as `rights-cleared` and `copyrighted` are not photographic evidence; describe the actual original fictional design or visible making process instead.

Research extensions may declare `preset_render_contract_defaults` to derive compact scene blueprints from their existing filtered subject/action/location/prop entries. Put only route-specific new events in the scene-expression shard files; do not duplicate the research taxonomy's original slot entries. Resolved blueprint atoms remain outside the ordinary sampler candidates so dictionary provenance and candidate-cap semantics stay exact. Narrative-world routes need at least four resolved blueprints, three scene functions, and no operational majority. Evidence and specialty routes need at least two functions or an explicit evidence-documentary exception. Every authored blueprint needs four concrete image fields, a non-empty function set, a boolean operational classification, and exactly one diegetic visual provenance. Declare `subject_kind` or `subject_tags` explicitly for any blueprint intended to satisfy a no-people request; an undeclared subject is not presumed non-human. Research-market classification is never a substitute for visual provenance and must not be copied into the blueprint.

Keep external taxonomy research outside the distributable skill under `docs/research-evidence/photo-prompt/`. The legacy ledger is `research_evidence.jsonl`; large additive domains may use a manifest plus immutable JSONL shards, as `character_moe/` does. Validate manifest order, row count, and SHA-256 without concatenating the legacy ledger. Store official source URLs, derived dimensions, affected candidate IDs, and reuse notes only in that evidence area. Do not copy source titles, URLs, research-process labels, raw prompts, source prose, images, or bulk vocabulary dumps into runtime data, semantic text, candidate relevance text, mandatory intent, or final prompts.

Treat `tests/fixtures/photo_prompt/semantic_retrieval_contract_character_moe_v1.jsonl` as a literal multilingual routing contract, not an independent holdout: its short spans are intentionally shared with production aliases. Keep independent generalization claims limited to cases frozen without implementation-derived phrases.

Treat explicit entry `facets` as the authority. Typed operational domains limit implicit tag-to-facet inference to semantically owning slots; for example, a `street` token in a focus entry must not become the scene's `place_type`. Legacy domains retain their historical inference until they are deliberately facet-migrated and their golden outputs reviewed. Use specific taxonomy such as `field_survey` when a generic legacy tag such as `field` would activate an unrelated applicability guard.

Put repeated theme boundaries in quality-layer `applicability_guards`. Use `match_any_tags` for curated taxonomy and `match_any_terms` only for a stable shared marker carried by a legacy family; both require a matching primary subject/location/genre context. Keep generic metadata words such as `role` and `subject` in `intent_routing.literal_subject_stop_terms` so they cannot infer unrelated secondary subjects from entry IDs.

## Validation

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python -m unittest tests.test_photo_prompt_contract_v2.PhotoPromptContractV2Tests.test_hybrid_augmentation_exposes_real_candidate_routes_and_audits_selective_adoption
.venv/bin/python -m unittest tests.test_photo_prompt_contract_v2.PhotoPromptContractV2Tests.test_adult_appeal_defaults_to_sensual_only_for_eligible_humans
.venv/bin/python -m unittest tests.test_photo_prompt_contract_v2.PhotoPromptContractV2Tests.test_sensual_editorial_and_fetish_fashion_axes_combine_and_risky_camera_pair_fails
.venv/bin/python -m unittest discover -s tests
```

Run focused contract and generalization tests before the full suite. Review golden changes; update snapshots only when output changes are intentional. Evaluation cases, holdouts, baselines, plans, and visual-review fixtures live under `tests/fixtures/photo_prompt/`; they are not runtime skill assets.

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

The public generalization suite has 79 inspectable cases. The original 24-case holdout, the separate 6-case operational-domain holdout v2, and the six-case retrieval baseline v3 are frozen; do not rewrite their expectations after a failure. Retrieval holdout v4 keeps the v3 cases and adds preset-free cases for the research extension. It verifies real semantic routing with the shared conservative profile and low novelty so sampler variance does not hide ranking defects. Domain-specific integration axes, craft refinements, and strategies use `profile_match`; the validator rejects unknown profile IDs so a typo cannot silently broaden or disable them. Fix a general routing, applicability, schema, or data-coverage defect instead of weakening a failed holdout. The real quality gate also evaluates all 67 golden intents, the rule-mode suites, preset-free retrieval, candidate coverage, diversity, bleed, preset guards, and multi-axis coverage.

Dictionary-hash fields such as presets, slots, labels, aliases, keywords, embedding text, and facets require a semantic-index refresh. Policy-only and quality-layer-only edits do not.

Rebuild only changed embeddings. The final index defaults to 16 stable compact JSON vector shards plus a human-readable manifest while preserving the exact logical entry order exposed to retrieval code:

```bash
GEMINI_API_KEY=... .venv/bin/python \
  skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

Do not print or commit API keys.

## Promotion Boundary

Local contract, scene-expression, contradiction, public generalization, and frozen holdout checks do not prove rendered-image quality. `render_scene_quality_holdout_v1.jsonl` freezes the cross-extension image cases but is not acceptance evidence until each case has a saved rendered result and pixel review. A `photo-domain-visual-review-plan/v1` file likewise defines pending cases and must never be passed off as acceptance evidence. Promotion of broad prompt-policy changes should also use the versioned `photo-visual-review/v1` artifact and fail closed on invalid enums, declared preset conflict, surviving body emphasis, missing fields, or missing provenance. Domain-specific `review_focus_results` are part of that boundary: every supplied focus needs evidence and a failed focus fails the case. Non-person operational reviews may mark body, role, or mixin fields `not_applicable`, but must include a case-level reason instead of using a meaningless pass. Run the combined boundary with `--acceptance-gate --visual-review <path>`; it requires the real semantic quality gate and a passing review artifact. Image/API generation is not part of ordinary validation unless the user explicitly authorizes it.
