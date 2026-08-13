# Atomic scene alternatives leaked outside the selected role scene

- Recorded: 2026-08-12 20:18 KST
- Status: resolved
- Goal/checkpoint: affected photo generalization regression after natural moe routing changes
- Affected scope: `photo-prompt-image-generator` rule-mode candidate-pack projection
- Search terms: `atomic_scene_candidate_leak`, `candidate_pool_trace`, `soft_anchor_atomic_pool_for_slot`, `office_scene_variant_seed_b`
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `tests/fixtures/photo_prompt/generalization_cases.jsonl`
- Related passed reports: none

## Failure

- Conditions or trigger: Run the frozen seventh generalization case, concept `회사원`, in rule mode after the expanded dictionary changed deterministic preset sampling.
- Expected: If the role scene is `glass_office_task`, every exposed location alternative stays inside `glass_office` or `corporate_high_floor_office`.
- Observed: The selected location was valid, but the public candidate pack also exposed `cozy_apartment` and `campus_cafe`; `evaluate_atomic_scene_contract` returned `atomic_scene_candidate_leak:location`.
- Impact on the goal: A composer could replace a preserved user role scene with an unrelated location even though the selected prompt itself looked correct.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --generalization-check --limit 7`.
- Result: `office_scene_variant_seed_b` was the only failed case; its scene contract allowed two office locations but exposed three candidates including two outside the atomic pool.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed. `candidate_pack_build_slots` has a score-trace path and a rule-mode choice fallback. The latter rebuilt public candidates from the eligible trace or preset filter without intersecting them with the active atomic soft-anchor pool.
- Confidence: confirmed
- Remaining unknowns: None for the candidate-pack contract; rendered quality remains outside this structural regression.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Restrict only the score-trace branch | Still failed | Rule mode used the separate choice fallback branch |
| Apply the same atomic intersection and selected-member recovery to both branches | Passed | Public alternatives and selected value stayed inside the active atomic scene |

## Resolution or next safe step

- Resolution/workaround: Intersect exposed eligible IDs with `soft_anchor_atomic_pool_for_slot` in both projection branches. If a late trace has no surviving member, recover only the selected atomic member plus declared atomic IDs; never fall back to unrelated preset candidates.
- Verification: The seven-case forward slice changed from 1 failure to 0, and the full 79-case generalization plus 24-case holdout and 6-case domain holdout test passed.

## Reuse guidance

- Avoid: Treating a valid selected slot as proof that candidate alternatives obey the same atomic contract.
- Prefer: Audit the entire exposed candidate set against the selected scene's allowed IDs and make every candidate-pack projection path enforce the same pool.
- Applicable when: A generator separates sampling traces from public candidate-pack construction or has multiple projection paths for semantic and rule modes.
- Re-check when: Adding a new late repair stage, trace writer, or candidate-pack fallback.
