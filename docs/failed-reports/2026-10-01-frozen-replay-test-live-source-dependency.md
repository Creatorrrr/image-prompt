# Frozen replay safety test depended on the live source state

- Recorded: 2026-10-02 06:31 KST (2026-10-01 21:31 UTC)
- Status: resolved by isolated test fixture; no runtime change
- Scope: protostar Korean alias evidence helper tests; no runtime defect established
- Related path: `docs/research-evidence/photo-prompt/protostar-korean-alias-data-cleanup-20261001/test_frozen_cycle.py`
- Search terms: replay missing vectors, live raw source, temporary evidence, no API fallback

## Expected and observed

`test_replay_missing_vectors_is_read_only_without_api_fallback` should reach the missing-vector replay guard and prove that no API or evidence write occurs. Preparation passed all 19 tests before source application. Independent review after the exact authorized alias append passed 18 of 19: the test's raw-proposal mock still returned baseline bytes while the evaluator read the now-proposed live source, causing an earlier source-scope error. Its live attempt/cache reads could also make the test state-dependent after measurement.

## Cause and next step

The test fixture was insufficiently isolated. Production source checks failed closed; no paid request was sent. Preserve the original preparation test and freeze, then make a transparent test-only revision using temporary proposed source and evidence files with absent attempt/cache state. Keep the specific missing-vector error and no-network/no-write assertions. Leave all candidate, query, input, cache, budget and acceptance values exact. Recheck the repaired harness independently before paid execution.

## Reuse guidance

A missing-cache safety test must not depend on whether the coordinator has applied the source proposal or completed measurement. Simulate the intended full precondition and absent cache explicitly, and assert the actual guard rather than accepting any earlier failure as success.

## Resolution

The repaired test uses temporary exact proposed-source and baseline-evidence bytes, with absent attempt/cache files. It reaches the specific missing-vector guard and proves no credential access, network/API call, index/evidence write or temporary-byte change. All 19 safety tests pass with the live source already applied, independently reproduced. The original test/freeze is preserved under preparation-revisions/pre-replay-test-isolation; the new freeze is a364c2fce6683fe4115f79a5b9036de5a4d09d167db84bc3a52f360d4eb44816. Source, inputs, queries, caches, runtime, budgets and acceptance criteria are exact. The updated current-regression freeze assertion passed separately, retaining all original experimental-field equalities.
