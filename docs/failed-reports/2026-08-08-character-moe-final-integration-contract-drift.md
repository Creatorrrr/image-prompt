# Character-moe final integration tests conflated visual grammar with topic-intent contracts

- Recorded: 2026-08-08 05:14 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Moe and Subculture Character Grammar / Stage 6
- Affected scope: full unit qualification for character research provenance and candidate-pack schema
- Search terms: character grammar topic intent, evidence topic mapping, candidate pack exact keys
- Related paths: `tests/test_photo_prompt_contract_v2.py`, `tests/test_prompt_generator.py`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`

## Failure

- Conditions or trigger: Run `.venv/bin/python -m unittest discover -s tests` after the focused character grammar, retrieval, scene, and pixel gates had passed.
- Expected: The closed full suite accepts the typed character contract while preserving all existing exact-schema checks.
- Observed: 3/400 tests failed. Two generic research-route assertions required every character preset ID to appear directly in the evidence ledger and required a non-empty generic `topic_intents` list. One legacy exact-key assertion omitted the newly emitted `character_grammar` candidate-pack field.
- Impact on the goal: Stage 6 could not qualify even though the character routes deliberately bind evidence through `character_grammar.topic_id` and keep nonvisual market/taxonomy labels out of photographic prompts.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python -m unittest discover -s tests`
- Result: `Ran 400 tests in 1524.220s`; failures were `test_all_research_routes_have_materialized_scene_expression_contracts`, `test_every_research_route_candidate_pack_selects_one_fail_closed_scene`, and `test_candidate_pack_preserves_unmatched_concept_intents`.

## Cause assessment

- Confirmed cause or current hypothesis: The final test expansion reused the ordinary research/worldbuilding invariant for the separate character contract. Character routes intentionally use a typed research topic plus one primary and at most two support visual atoms; forcing an abstract market/taxonomy phrase into `topic_intents` would violate the nonvisual-label boundary and invalidate already qualified pixel prompts. The exact-key test was simply stale after the additive output field was introduced.
- Confidence: confirmed
- Remaining unknowns: None for this failure signature. A future prompt-visible character taxonomy contract would require a new explicit migration rather than reusing this exception.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Apply generic `preset_id in evidence IDs` and non-empty `topic_intents` to all 112 routes | 3 full-suite failures | Character presets map to evidence by typed topic ID, and their nonvisual label must not become prompt text |
| Add route IDs or synthesize topic phrases into runtime data | Not applied | It would expand or distort the evidence/runtime graph and change the prompt contract solely to satisfy an incorrect generic assertion |

## Resolution or next safe step

- Resolution/workaround: The test now requires each character preset's typed topic ID to exist in the research ledger, requires its generic topic-intent list to remain empty, and still requires a valid sparse character grammar and exact atomic scene. Ordinary research/worldbuilding routes retain their stricter preset-ID and non-empty topic-intent assertions. The exact candidate-pack key set now includes `character_grammar`.
- Verification: All three formerly failing tests passed independently. The closed rerun then completed `Ran 400 tests in 1545.852s` with `OK`; the real acceptance gate also passed without requiring prompt-visible character taxonomy labels.
- Next safe step if unresolved: Inspect only the remaining failing assertion; do not add nonvisual taxonomy labels to generated photographic prompts or weaken sparse grammar validation.

## Reuse guidance

- Avoid: Reusing one route family's mandatory-intent representation as a universal contract when another family has a stronger typed executable representation.
- Prefer: Assert the semantic invariant at the correct layer: ordinary routes use topic intents; character routes use evidence-backed topic IDs plus selected visual atoms and explicit nonvisual-label exclusion.
- Applicable when: A candidate-pack schema supports multiple typed render contracts with different prompt-visible and metadata-only fields.
- Re-check when: Character topic labels become prompt-visible, the grammar bundle shape changes, or the evidence ledger stops binding topic IDs.
