# Worldbuilding scoped route lost to a generic semantic preset

- Recorded: 2026-08-07 11:15 KST
- Status: resolved
- Goal/checkpoint: 18-topic worldbuilding taxonomy, Stage 4 real semantic retrieval qualification
- Affected scope: explicit `worldbuilding_system` scoped-route selection in semantic mode
- Search terms: worldbuilding_system, scoped_routes, civic_solarpunk_institutional_world, urban_heat_air_quality_record
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/semantic_retrieval_holdout_worldbuilding_v1.jsonl`, `tests/test_photo_prompt_contract_v2.py`
- Related passed reports: `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`, `docs/passed-reports/2026-08-07-deep-worldbuilding-taxonomy-scoped-routing.md`

## Failure

- Conditions or trigger: Run all 72 frozen Korean/English worldbuilding retrieval cases against the regenerated real Gemini semantic index.
- Expected: Every explicit worldbuilding route phrase selects its single frozen route preset.
- Observed: 71/72 passed. `world_solarpunk_ko_02` resolved the correct `worldbuilding_system` domain and scoped route, but semantic weighting selected the generic `urban_heat_air_quality_record` preset instead of `civic_solarpunk_institutional_world`.
- Impact on the goal: Completion criterion 5 remained open because explicit on-demand routing was not deterministic against a nearby generic climate preset.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --retrieval-holdout-check --retrieval-holdout-cases skills/photo-prompt-image-generator/assets/semantic_retrieval_holdout_worldbuilding_v1.jsonl`
- Result: Exit 12, 72 cases, 1 failure, `selected_preset_not_allowed` for `world_solarpunk_ko_02`.

## Cause assessment

- Confirmed cause or current hypothesis: `preset_matches_automatic_intent_scope` rejected non-matching scoped worldbuilding presets but continued admitting generic unscoped presets after an exact scoped route had matched. Embedding similarity and weighted sampling could therefore override the explicit route signal.
- Confidence: confirmed
- Remaining unknowns: The pre-existing retrieval holdout remains part of the closed final regression sequence.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Preserve exact domain and scoped-route aliases in taxonomy/routing data | Structural route resolution was 72/72, but real semantic retrieval was 71/72 | Exact route detection alone did not remove generic presets from the semantic candidate set |
| Treat a user-authored exact scoped route as stronger than embedding similarity | The previously failing intent directly selected `civic_solarpunk_institutional_world`; focused worldbuilding and legacy subculture contract tests passed; full worldbuilding retrieval passed 72/72 | Worked; no second root-cause repair was needed |

## Resolution or next safe step

- Resolution/workaround: When a user-authored intent resolves an explicit subculture or worldbuilding scoped route, automatic preset eligibility is restricted to the matched route set. Direct preset selection and generic intents without a scoped-route match are unchanged.
- Verification: Direct real-index replay of the failing intent passed; two focused unit contracts passed; the unchanged 72-case bilingual real-index holdout passed with zero failures.

## Reuse guidance

- Avoid: Letting generic semantic presets compete after an exact typed-route alias has already resolved.
- Prefer: Domain quarantine plus exact scoped-route precedence, with generic negative controls.
- Applicable when: A specific on-demand taxonomy route overlaps semantically with a broad legacy domain.
- Re-check when: Adding a new intent-scoped domain, changing scoped aliases, or changing automatic preset eligibility.
