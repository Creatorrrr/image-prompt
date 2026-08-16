# Embedding-positive transformation was blocked by a lexical context guard

- Recorded: 2026-08-16 12:05 KST
- Status: resolved
- Resolved: 2026-08-16 12:07 KST
- Goal/checkpoint: Visual Profile Hybrid Retrieval Goal / Stage 5 all-profile actual-index calibration
- Affected scope: semantic-only `embodied_corruption_transition` resolution with authorial-core context disambiguation
- Search terms: context disambiguation, embedding positive, embodied transition, exact lexical guard
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`
- Resolved by: `docs/passed-reports/2026-08-16-visual-profile-hybrid-retrieval.md`

## Failure

- Conditions or trigger: Resolve an exact-term-free full authorial core describing an adult character with a former bright identity and a dark present state simultaneously visible across an unfinished on-body transition boundary.
- Expected: The actual embedding score makes `embodied_corruption_transition` an optional semantic candidate; no exact hard obligation is created.
- Observed: The intended profile ranked first at 0.775264, above the 0.70 minimum, but no optional candidate was emitted because `activation.context_disambiguation.any_terms` did not literally match the core's equivalent wording.
- Impact on the goal: A post-vector lexical positive gate prevents semantically related wording from being retrieved, contradicting the intended embedding-based paraphrase discovery path.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Local batch-size-one Gemini replay over six exact-free full-core positives and six adjacent full-core controls, using the committed registry-bound index. Stored output was limited to profile IDs and similarity scores.
- Result: Intended transformation profile top score 0.775264; optional profile list empty. Four other valid positives emitted their intended profiles, and all six controls emitted none. One proposed drink case was determined to describe a different physical support mechanism and is not counted as a valid profile failure.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed by resolver inspection. `visual_profile_context_applicability` applies the exact positive `context_disambiguation.any_terms` requirement to both exact and embedding lanes. The embedding lane therefore requires vector relevance and a redundant literal positive phrase, while exact excludes and negative context phrases already protect adjacent meanings.
- Confidence: confirmed
- Remaining unknowns: None for the current registry and focused boundary cases.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| One shared positive lexical context requirement after both exact and embedding matching | Keeps ambiguous exact `corruption` senses narrow | Rejects valid semantic paraphrases even when the dedicated profile vector is the top result well above threshold |

## Resolution or next safe step

- Resolution/workaround: Exclusions and negative context terms remain shared by both lanes. Ambiguous exact activation still requires literal positive context, while an above-threshold embedding score now supplies the positive context proof for embedding-only optional discovery.
- Verification: A focused fake-vector test proves an exact-free paraphrase becomes optional while an exact ambiguous term with `no character transformation` remains a non-eligible context mismatch. The real transformation full core now emits only optional `embodied_corruption_transition` at 0.775264; all six valid exact-free positives emit their intended top profile and all six adjacent controls emit none.
- Next safe step if unresolved: Keep the profile absent rather than weakening exact ambiguity handling; do not add topic-specific aliases or a new adult/safety gate.

## Reuse guidance

- Avoid: Applying an exact positive phrase gate after a semantic vector has already established the same positive sense.
- Prefer: Share negative exclusions across lanes while using lane-appropriate positive proof: boundary-aware terms for exact and vector relevance for semantic discovery.
- Applicable when: A hybrid resolver combines ambiguous exact aliases with embedding-only paraphrase retrieval.
- Re-check when: Context-disambiguation schema, vector thresholds, or exact/semantic precedence changes.
