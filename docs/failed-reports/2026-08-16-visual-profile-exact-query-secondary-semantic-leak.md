# Exact visual-profile query leaked an unrelated secondary semantic candidate

- Recorded: 2026-08-16 11:35 KST
- Status: resolved
- Resolved: 2026-08-16 11:38 KST
- Goal/checkpoint: Visual Profile Hybrid Retrieval Goal / Stage 3 runtime projection
- Affected scope: v5 visual-profile hybrid resolver and optional visual-concept projection
- Search terms: `resolve_visual_profile_hits`, exact precedence, embedding candidate window, unrelated underarm candidate, absolute territory
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`
- Resolved by: `docs/passed-reports/2026-08-16-visual-profile-hybrid-retrieval.md`

## Failure

- Conditions or trigger: Generate a real semantic v5 pack for a frozen adult fallen-angel fashion core whose request explicitly contains the exact project term `절대공역` and whose baseline describes close upper-inner-thigh negative space.
- Expected: `inner_thigh_negative_space` becomes the required exact obligation. Any embedding-only visual profile must still be globally close enough to the best matching profile rather than merely best among the profiles left after exact suppression.
- Observed: The exact profile became required, but `deliberate_underarm_salience` also appeared as an optional visual concept even though the request contained no raised arm or underarm emphasis.
- Impact on the goal: The single resolver works structurally, but its relative semantic window can admit an unrelated secondary profile on exact-term requests, so final relevance criterion 5 is not satisfied.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Local v5 wrapper replay with the committed Gemini visual-profile index, seed 817, and a frozen authorial core. Output was reduced to obligation IDs, optional visual concept IDs, and clarification statuses; no credential, vector, or private runtime text was stored.
- Result: Required obligations: `inner_thigh_negative_space`. Optional visual concepts: `deliberate_underarm_salience`.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed by source inspection. The resolver removes exact-evidence profile IDs before it computes the best semantic score. The `best_score_margin` is therefore anchored to the strongest remaining profile, not to the strongest profile for the query overall.
- Confidence: confirmed
- Remaining unknowns: Whether global-best anchoring alone removes the secondary candidate across all representative exact terms without suppressing a genuinely co-requested second profile.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Global threshold 0.65 plus best-score margin 0.08 | Descriptive paraphrase and unrelated negative controls separated correctly | Exact profiles were omitted before the relative-score reference was calculated, leaving a weaker unrelated profile as the remaining winner |

## Resolution or next safe step

- Resolution/workaround: The resolver now scores every context-applicable profile for the global relevance reference before output eligibility is applied. Exact, negated, and user-definition-owned profiles remain suppressed from the embedding-only output lane, but their scores still anchor the fixed `best_score_margin`.
- Verification: A focused fake-vector regression places an unrelated underarm profile above the absolute threshold but outside the exact profile's global margin; it is rejected. The same real seed-817 wrapper replay now emits only required `inner_thigh_negative_space` and no optional visual concept.
- Next safe step if unresolved: Reopen with the exact query and score ordering; do not widen the fixed margin until a genuinely co-requested second profile supplies direct evidence.

## Reuse guidance

- Avoid: Computing a relative semantic candidate window only after authoritative exact hits have been removed.
- Prefer: Separate ranking reference from output eligibility: exact results can be output-suppressed from the optional lane while still anchoring global semantic relevance.
- Applicable when: Exact and vector retrieval coexist and vector candidates use a best-score-relative window.
- Re-check when: Visual-profile threshold, margin, exact precedence, or multi-profile query behavior changes.
