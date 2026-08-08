# Research-backed character grammar and rendered-image qualification

- Recorded: 2026-08-08 05:16 KST
- Status: current
- Qualification: resolved-material-failure
- Goal/problem signature: Turn 24 moe and subculture-character research topics into source-traceable, composable adult character mechanisms that produce observable action, relationship, expression, state, and prop evidence instead of costume-only portraits.
- Search terms: character moe grammar, sparse visual atoms, nonvisual market labels, multilingual scoped route, atomic character scene, pixel action legibility
- Affected scope: `skills/photo-prompt-image-generator` character research shards, typed graph, scoped routing, atomic scene selection, candidate-pack/audit contracts, semantic index, retrieval holdouts, and rendered-image qualification
- Excluded scope: push, PR, deployment, protected-character recreation, universal CJK lexical equivalence, youth sexualization, automatic promotion of optional soft concept readiness, and exhaustive image-model quality
- Related paths: `skills/photo-prompt-image-generator/assets/research_evidence_character_moe/`, `skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_scene_expression_character_moe.json`, `skills/photo-prompt-image-generator/assets/render_character_moe_quality_visual_review_v1.json`
- Related failed reports: `docs/failed-reports/2026-08-08-character-moe-research-provenance-overclaim.md`, `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`, `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`, `docs/failed-reports/2026-08-08-character-moe-final-integration-contract-drift.md`

## Reproduction context

- Repository/ref: `/Users/chasoik/Projects/image-prompt`, local `main`
- Baseline: clean `main@b8fe45e`, five commits ahead of `origin/main`; implementation was qualified before publication, and a later user request authorized its local commit while push remained out of scope
- Runtime: Python 3.14.3, repository `.venv`, Gemini `gemini-embedding-2`, 768 dimensions, semantic text recipe `semantic-text-v2`
- Final dictionary/index: `930f5f4359ed51f5784cc0b75923f2702495590c48811dd359c776660d07d6d2`, 6,513 entries, 16 JSON shards
- External boundary: Public source research and the user-approved sanitized taxonomy/retrieval text were used. One external cache-first embedding build created the new vectors; later source-only repairs used cache-only rematerialization. The final acceptance gate used real embeddings. Only the frozen eight-case local image sample was rendered.

## Successful approach

- Freeze first: Bind 24 topics to eight families, 96 KO/EN/JA/ZH retrieval cases, generic negative controls, and eight image families before runtime implementation.
- Separate evidence roles: Keep each source's supported dimensions, cross-source synthesis, and design inference explicit. Store six immutable JSONL shards rather than growing the legacy evidence ledger.
- Keep taxonomy nonvisual: Model market terms, audience familiarity, adulthood declarations, identity/orientation boundaries, and stereotype guards as router/guard metadata. Select only visual atoms into a scene.
- Use a sparse executable grammar: Choose one primary visual atom and at most two compatible support atoms with fixed priority `observable action > relationship stake > expression or gaze > morphology or state > costume`.
- Render atomic events: Give every route three distinct action/location/prop scenes, no static portraits, one diegetic provenance, explicit adult metadata, and deterministic scene-function selection.
- Qualify pixels separately: Pass candidate and prompt audits first, then inspect the actual pixels. Preserve failed attempts, permit only one cause-specific edit or one repaired pristine rerender, and never equate prompt PASS with image PASS.

## Material repair history

1. The first independent research audit found provenance overclaim, unsupported lexical equivalence, morphology-based adulthood inference, and conflated composite concepts. Source-specific provenance, typed atoms, and explicit-adult metadata resolved Critical/High/Medium to zero.
2. Initial scoped aliases routed only 11/96 frozen multilingual requests. Replacing paraphrases with unique short literal spans from the frozen requests produced 96/96 without broad words or whole-sentence overfit.
3. Pixel qualification exposed a wrong hair target, weak transformed/ordinary identity separation, and an inferred or reversed care handoff. Bounded scene repairs and pristine rerenders fixed the visible actions while retaining the unsuccessful images.
4. The first closed full suite ended 397/400 because generic research-route assertions were applied to the separate typed character contract and one exact-key test omitted the new field. Character routes now require evidence-backed `character_grammar.topic_id`, valid sparse visual atoms, and empty generic topic intents; ordinary routes retain their stricter topic-intent contract. The repaired suite passes 400/400.

## Evidence and eight completion criteria

| Criterion | Direct evidence | Result |
|---|---|---|
| 1. All 24 topics have bounded source evidence | 72 rows = 24 matrices + 48 independent sources, 72 unique URLs, 194 mechanisms, 53 cross-source syntheses with at least two records and URLs; independent research audit Critical/High/Medium 0 | pass |
| 2. The additive character graph is executable and original | 8 families; 184 nodes = 141 visual, 33 router, 10 guard; 23 policies, 24 compatibility edges, 14 guards; evidence candidate IDs equal runtime node IDs | pass |
| 3. Every route has an atomic event grammar | 24 exact routes, 72 scenes, three per route, at least two functions per route, 72 unique action/location/prop tuples, zero static portraits | pass |
| 4. Culture, IP, adult, and safety boundaries remain separate | Market terms stay nonvisual; each scene has one visual provenance; adult/non-inference/no-youth-sexualization/IP/person/stereotype policies pass; direct packs keep automatic safety PASS | pass |
| 5. New multilingual retrieval works without broad leakage | Frozen KO/EN/JA/ZH cases are 24 each and 96/96 real-semantic PASS across all 24 routes; generic negatives remain outside the typed domain | pass |
| 6. Existing routing and sampler contracts do not regress | Existing retrieval is 264/264: v4 22, subculture 70, worldbuilding 72, CJK 100; generalization 79/79, holdout 24/24, domain v2 6/6, contradiction 2,001/2,001 | pass |
| 7. The frozen rendered sample is visibly qualified | 8/8 final PNGs, 32/32 focus results, eight distinct events, no studio-costume convergence; saved image hashes match; failed pre-fix transformation/adult-inclusive results remain preserved | pass |
| 8. Closed technical qualification passes | Dictionary and index checks PASS; 6,513-entry/16-shard checksum, count, ID set and logical order pass; candidate 6/6; full unit 400/400; real acceptance `passed=true`; final `git diff --check` pass; independent final audit Critical/High/Medium 0 | pass |

## Rendered sample and retained limitations

- Qualified files: `generated_images/character-moe-8-family-validation-20260808_030639/`. Transformation and adult-inclusive use the `-revision` directories; their pre-fix directories remain evidence, not passing finals.
- Trait-gap and relationship cases each used one concrete pixel edit. The other qualified images used one initial render; hair, transformation, and adult-inclusive source repairs used a new pristine pack rather than selecting among uncontrolled variants.
- The creepy-cute creature's third bracing appendage is intentionally anomalous and slightly less anatomically explicit than its two grounded feet. The transformation worker's handheld device is phone-like, while the separate plain pager carries the work-role clue. A single hair-state still demonstrates wet/release traces but cannot prove across-frame temporal identity.
- `soft_promotion_ready=false` remains an optional legacy concept-benchmark signal. It was not made a hard requirement; all hard legacy, golden, routing, grammar, and visual gates pass.

## Verification commands

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --generalization-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --holdout-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --domain-holdout-v2-check
.venv/bin/python -m unittest discover -s tests
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py \
  --acceptance-gate --quality-runs 2 \
  --visual-review skills/photo-prompt-image-generator/assets/render_character_moe_quality_visual_review_v1.json \
  --summary-only
git diff --check
```

The four domain-specific real retrieval files were also run independently: character-moe 96, subculture 70, worldbuilding 72, and CJK worldbuilding 100.

## Reuse guidance

- Prefer: Freeze natural requests and pixel criteria before implementation, route through typed evidence topics, keep market labels metadata-only, and give the renderer one sparse observable event.
- Avoid: Treating archetype names as visual atoms, forcing nonvisual taxonomy into prompt text, inferring personality or adulthood from morphology, increasing evidence density, or fixing pixels by weakening the rubric.
- Re-check when: Evidence provenance, scoped-alias normalization, graph node roles, scene resolver, candidate-pack schema, semantic model/recipe, image model, or the frozen pixel rubric changes.
