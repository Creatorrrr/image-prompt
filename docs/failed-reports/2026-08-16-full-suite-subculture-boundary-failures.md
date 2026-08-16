# Full suite exposed subculture-illustration boundary failures outside the changed paths

- Recorded: 2026-08-16 12:34 KST
- Status: open
- Goal/checkpoint: Visual Profile Hybrid Retrieval Goal / Stage 5 full repository regression
- Affected scope: full `tests/` discovery; reported failures are confined to subculture-illustration contract and universal-scene modules
- Search terms: full unittest discover, subculture illustration, photo baseline argv, universal scene shared state
- Related paths: `tests/test_subculture_illustration_contract_v1.py`, `tests/test_subculture_illustration_photo_boundary.py`, `tests/test_subculture_illustration_universal_scene_v3.py`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`

## Failure

- Conditions or trigger: Run `.venv/bin/python -m unittest discover -s tests` after all focused and affected photo-prompt validations pass.
- Expected: The repository-wide suite completes without failures.
- Observed: 584 tests ran in 1448.630 seconds; 11 failures and 5 errors occurred, all in three subculture-illustration test modules. Three errors report missing legacy photo `provenance.argv`; the remaining errors/failures concern universal-scene closed slots, bridge counts, semantic carrier groups, and word budgets.
- Impact on the goal: The visual-profile implementation's focused criteria pass, but the plan's repository-wide suite criterion is not yet satisfied or cleanly attributable to an unrelated baseline.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python -m unittest discover -s tests`
- Result: `FAILED (failures=11, errors=5)`. `git status --short` shows no modified or untracked subculture-illustration source, asset, fixture, or test path; all current changes are under photo-prompt, its tests, goal plan, and failure reports.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed as pre-existing Git HEAD baseline failures outside this goal. The same universal-scene failures reproduce from a temporary clean `HEAD` archive. With the project `.venv` linked into that archive, the four frozen-photo checks also reproduce the identical missing-`provenance.argv` error; `HEAD` already projects `argv` into `omitted_private_fields`.
- Confidence: confirmed
- Remaining unknowns: The correct repair contract for those subculture fixtures and universal-scene expectations. That decision is outside the visual-profile retrieval goal.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Full repository discovery after focused photo validation | Confirmed 568 passing tests and localized all 16 issues to three subculture modules | The combined run does not distinguish independent baseline failures from test-order contamination or cross-skill photo provenance compatibility |
| Isolated rerun in the current worktree | Reproduced all 5 errors immediately and the same universal-scene failure methods | Proved they were not full-discovery-only, but not yet whether dirty photo changes caused them |
| Temporary clean `HEAD` archive, then rerun with the project `.venv` linked | Reproduced the same 11 failure subcases and 5 errors, including the identical missing-`argv` contract | Confirms a pre-existing repository baseline issue rather than a regression from this goal; repairing it would expand into another skill |

## Resolution or next safe step

- Resolution/workaround: Scoped attribution is complete; no unrelated subculture files were changed. The visual-profile goal uses its passing affected-photo suite, while repository-wide discovery remains non-green until a separately authorized subculture repair reconciles the frozen provenance and universal-scene contracts.
- Verification: Current worktree full discovery: 584 total, 11 failures, 5 errors. Clean `HEAD` selected-method replay: the same 11 failure subcases and 5 errors. Focused visual-profile/core/obligation tests and adult-appeal regressions remain green.
- Next safe step if unresolved: Open a separate subculture-illustration maintenance goal; do not restore private `argv` or rewrite universal-scene expectations from this visual-profile task.

## Reuse guidance

- Avoid: Treating unrelated full-suite failures as evidence that the changed visual-profile resolver is broken, or rewriting distant fixtures without attribution.
- Prefer: Localize by module, reproduce independently, and compare against clean baseline behavior before expanding scope.
- Applicable when: A broad monorepo-style test discovery covers multiple independent skills with shared Python module names or cross-skill frozen baselines.
- Re-check when: Public photo provenance, universal-scene assets, or test import isolation changes.
