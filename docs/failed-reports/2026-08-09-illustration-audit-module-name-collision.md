# Illustration audit was shadowed by the photo audit in the full test process

- Recorded: 2026-08-09 03:24 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 6 full regression
- Affected scope: illustration audit import boundary and full-suite order independence
- Search terms: audit_composed_prompt module collision, sys.modules, focused pass full suite fail
- Related paths: `skills/subculture-illustration-image-generator/scripts/audit_composed_prompt.py`, `skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py`, `tests/test_subculture_illustration_contract_v1.py`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Run the full `unittest discover` process after `test_photo_prompt_contract_v2` has imported the photo skill's top-level module named `audit_composed_prompt`.
- Expected: The sibling illustration skill always invokes its own typed illustration auditor, independent of test discovery order or another skill's module cache.
- Observed: The illustration test inserted its script directory into `sys.path` and then imported the already-cached generic module name. Python reused the photo auditor from `sys.modules`. Illustration `route:`, `format:`, and `visual:` IDs were then reported as unknown; the result omitted the illustration-only `integrity_errors` field.
- Impact on the goal: Focused tests passed in isolation, but the one reserved full suite failed with 6 failures and 12 errors. The sibling runtime was not process-isolated despite its data/runtime separation.

## Evidence

- Full suite: `Ran 421 tests in 1611.021s`, `FAILED (failures=6, errors=12)`.
- Failure signature: valid illustration pack `4288defd58ebe333` returned `chosen_candidate_ids: unknown candidate id` for `format:ensemble_key_art`, `route:ensemble_relationship_staging`, and three `visual:` IDs; mutation assertions raised `KeyError: integrity_errors`.
- Scope boundary: all preceding legacy tests passed, and the same 17 illustration/photo-boundary tests had passed in focused execution before the full run.

## Cause assessment

- Confirmed cause: both skills expose a top-level file named `audit_composed_prompt.py`; `sys.path` precedence cannot replace an object already cached under the same `sys.modules` key.
- Confidence: confirmed from the returned photo-audit schema and candidate-ID vocabulary.

## Resolution or next safe step

- Resolved: 2026-08-09 03:23 KST.
- Resolution: moved the unchanged audit core to the unique import name `illustration_audit.py`; retained `audit_composed_prompt.py` as the documented compatibility CLI; changed the validator and contract tests to import only the unique core. The prompt-qualification audit hash remains byte-identical because the core content did not change.
- Verification: deliberately preloaded one photo-audit contract and then ran the illustration contract and photo-boundary modules in the same interpreter. All 19 tests passed, including the new assertion that the bound audit file is exactly the sibling `illustration_audit.py`. After separate authorization and pixel qualification, the current full suite ran 437 tests in 1483.337 seconds with zero failures and zero errors. The wrapper and core compile successfully, closing the earlier full-process uncertainty.

## Reuse guidance

- Avoid: relying on `sys.path.insert` to distinguish same-named top-level modules in a shared Python process.
- Prefer: skill-specific module names or real package-qualified imports; CLI filenames may remain generic only as wrappers.
- Applicable when: multiple skills are tested or embedded in one interpreter.
- Re-check when: adding another sibling skill with generic script module names.
