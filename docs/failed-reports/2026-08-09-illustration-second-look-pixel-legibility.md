# Illustration second-look cue remained ambiguous after the bounded repair

- Recorded: 2026-08-09 02:40 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 5 render qualification
- Affected scope: single-frame narrative realization of `recurring_motif_visual_metaphor`
- Search terms: second look, shadow silhouette, renderability, repair exhausted
- Related paths: `skills/subculture-illustration-image-generator/references/creative-direction-contract.md`, `skills/subculture-illustration-image-generator/references/image-runtime.md`, `generated_images/subculture-illustration-6-format-validation-20260809_022415/01-single-narrative`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Render the frozen adult night-mender case once, then use the one allowed targeted edit to clarify a subordinate counter shadow as two hands clasping before the real handoff.
- Expected: The first read remains the real coat handoff, while a separate second-look cue clearly changes the reading without text.
- Observed: The initial shadow was an ordinary arm/hand cast shadow. The edit preserved every frozen primary requirement but still looked like one elongated arm ending in clustered fingers rather than two clasped human hands.
- Impact on the goal: Five of six format cases qualify, but the six-case pixel completion criterion remains unmet. Prompt audit PASS did not establish rendered second-look salience.

## Evidence

- Initial image SHA-256: `35cc697742084d5bd6cc1b119b5c5dd828e84512b28426b3bed142070946a0ea`.
- Bounded edit SHA-256: `fcefebe9e913a5899f5463d616248178761a2305d2b6a7425162facb9b91aac4`.
- Result record: `generated_images/subculture-illustration-6-format-validation-20260809_022415/01-single-narrative/result.json` reports `final_fail_repair_exhausted`; `final.png` is intentionally absent.

## Cause assessment

- Confirmed cause: The selected realization made a compound two-person anatomy silhouette the sole secondary cue but did not reserve a sufficiently simple, separated receiving plane. The targeted edit repeated the same fragile realization instead of switching to a simpler consequence that preserved the changed rule.
- Confidence: confirmed for this render pair; model-wide frequency is unknown.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Initial generation | Primary frozen focus passed; second-look failed | Ordinary cast-shadow prior dominated the requested anticipatory relation. |
| One targeted edit | Primary focus remained stable; second-look still failed | The requested two-hand shadow collapsed into one arm and clustered digits. |

## Resolution or next safe step

- Resolved: 2026-08-09 12:21 KST.
- Resolution/workaround: The historical v1 failure pair and both failed v2 roles remain preserved. A separately authorized v3 qualification replaced the line-like primary with an isolated object relation: fixed vertical chain, displaced bell body, separately displaced clapper, taut causal thread, untouched handoff gap, and black negative space. Its safe surface-state fallback remained declared but was not invoked because the primary passed.
- Verification: The v2 primary became a thin threshold trace instead of a broad pale seam. Its sole fallback became a regular woven rug center instead of a visible terminating wet/dry boundary. Neither role can be promoted to PASS.
- Final verification: the v3 pristine image passed metadata-free native and 320px review, all frozen focus/thumbnail/forbidden checks, local hash verification, and the post-fix 437-test full suite. The aggregate product qualification is now 6/6.

## Successor preflight (2026-08-09 04:15 KST)

- The default pack and composed contracts are now v2. All 24 frozen prompt cases were regenerated with typed primary/fallback second-look plans and pass the current audit; immutable v1 records remain independently replayable.
- `skills/subculture-illustration-image-generator/assets/render_case01_v2_preflight/` freezes the successor case-01 pack `db15b9138a402405`, exact prompt SHA-256 `e0af5c7c9e239b1361b501631454d3e44c32253ced62ae2f2c436ccdece4351e`, clean audit, and canonical plan SHA-256 `b1482fef3ddc0c22c1009cfde79a02329559656df5f5bfe8abcb29f099279325`.
- The primary is a broad seam crossing a clear brass material boundary; the fallback is a broad dry state change on an unoccupied receiving mat. Neither depends on compound anatomy, projected hands, or subscale symbol decoding.
- The preflight validator reproduces the exact pack, audit and hashes, verifies all six historical v1 artifacts when local-image verification is enabled, forbids a generated PNG in the preflight directory, and reports `ready_awaiting_user_approval`.
- This section records the pre-generation state. The separately required authority was later received; the outcome below supersedes only the waiting state, not the immutable preflight bytes.

## Successor qualification outcome (2026-08-09 11:13 KST)

- Result: `final_fail_repair_exhausted_v2`; aggregate product qualification remains 5/6 and `partial`. No `final.png` was created.
- Initial `primary_carrier`: built-in image generation once. Native PNG SHA-256 `5ff90d9ad61c6772d5147dc3f0f4a6f6553401291b116b76c80540cf758cc4e1` at 1149×1369. All frozen first-read, authorial, thumbnail and forbidden checks pass, but the threshold cue is a thin red-white edge trace rather than the declared broad pale material seam.
- Sole `fallback_carrier` repair: targeted edit once. Native PNG SHA-256 `3d58ae585c7e6e9269b56e03f3767f11cd4deeef854a571c3c3092df8ced0b29` at 1149×1368. The lighter mat center follows regular nested woven borders and lacks a visible terminating moisture front, so blind review reads it as rug coloration rather than a dry-state consequence.
- Both metadata-free blind observations, exact prompts, native paths, derived views, hashes and role-by-scale failures are preserved in `generated_images/subculture-illustration-case01-v2-qualification-20260809_105207/01-single-narrative/result.json` and linked by `skills/subculture-illustration-image-generator/assets/render_case01_v2_visual_review.json`.
- The authorized 421-test rerun was conditional on pixel PASS. Since neither role qualified, that condition was not met and the suite was not executed.
- Stop condition reached: this is the second materially redesigned attempt family for the same second-look pixel-legibility gap. No additional image generation, edit, variant selection or criterion relaxation is permitted in the current goal.

## Structural successor qualification outcome (2026-08-09 12:21 KST)

- New authorization covered one materially different pristine generation and, only if its primary failed, one fallback edit. The new preflight retained candidate pack `db15b9138a402405` while changing the prompt SHA-256 to `4efc3a3cc6874b9befcdddf8e5a6893cc8ec0b6c5d85b12867a92c0cbef578ea` and the plan SHA-256 to `b2e69c250153c8e4f3821f6826cc7e001861db5a38816d4914e8ac09e6ddbb76`.
- The built-in generator was invoked exactly once. Native `initial.png` and byte-identical `final.png` are 1024×1536 with SHA-256 `95b9b3c311af85de3092c30b0e4272929e307decfc3e68434917b1d7eba1b796`.
- Independent review froze observations before reading metadata. At native and 213×320, the pending coat handoff reads first; the isolated bell's vertical chain, tilted body, separate displaced clapper, motion marks, taut red cuff-to-clapper line, and untouched gap recover the early motion on second look.
- The primary `object_relation` passed both declared scales. The `surface_state` fallback was not attempted, so the one-image/zero-repair budget is preserved rather than spent unnecessarily.
- Versioned evidence: `skills/subculture-illustration-image-generator/assets/render_case01_v3_preflight/`, `skills/subculture-illustration-image-generator/assets/render_case01_v3_visual_review.json`, and `generated_images/subculture-illustration-case01-v3-qualification-20260809_114514/01-single-narrative/result.json`.
- Regression: `python3 -m unittest discover -s tests` completed 437 tests in 1483.337 seconds with zero failures and zero errors. Focused illustration/photo boundary tests then passed 33/33 after recording the suite result.

## Reuse guidance

- Avoid: compound hand anatomy, tiny glyphs, or multi-limb shadows as the sole subordinate reveal at thumbnail scale.
- Prefer: one separated contour, state change, or material discontinuity on a named clear surface, with the first-read event unchanged.
- Applicable when: high-creativity prompts require a first-to-second-look path or an early anomaly support atom.
- Re-check when: the selected realization changes, the target format changes, or a new image model is qualified.
