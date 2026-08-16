# Generic adult fashion core leaked an underarm visual profile

- Recorded: 2026-08-16 12:01 KST
- Status: resolved
- Resolved: 2026-08-16 12:07 KST
- Goal/checkpoint: Visual Profile Hybrid Retrieval Goal / Stage 5 actual-index runtime
- Affected scope: v5 embedding-only visual-profile retrieval with the committed 768-dimensional Gemini index
- Search terms: generic adult fashion, deliberate underarm salience, semantic false positive, visual profile query
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`
- Resolved by: `docs/passed-reports/2026-08-16-visual-profile-hybrid-retrieval.md`

## Failure

- Conditions or trigger: Run a real semantic v5 pack with a frozen core for a generic adult woman in a minimal fashion studio, clean tailoring, calm upright pose, broad soft light, and no body-region emphasis.
- Expected: No visual obligation, optional visual concept, or profile clarification is emitted because the request does not imply any maintained visual-profile mechanism.
- Observed: No hard obligation was emitted, but `visual-concept:deliberate_underarm_salience` appeared as an optional candidate and eligible clarification.
- Impact on the goal: Embedding-only discovery is structurally optional but still insufficiently precise on a representative unrelated adult-fashion control, so final relevance criteria 3 and 7 are not satisfied.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Local semantic v5 wrapper replay using the committed visual-profile index, seed 817, and a frozen generic adult-fashion authorial core. Output was reduced to public profile IDs, applicability, and audit result; no credential or vector was stored.
- Result: `visual_obligations=[]`; `optional_concepts=[visual-concept:deliberate_underarm_salience]`; the authorial pack structural audit otherwise returned no failures.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed by real-vector replay. The full frozen-core query scores `deliberate_underarm_salience` at 0.675941, just above the 0.65 global minimum. The descriptive inner-thigh positive scores its intended profile at 0.811146. The threshold was calibrated on a shorter generic-fashion phrase and was too permissive for production's whole-core query recipe.
- Confidence: confirmed
- Remaining unknowns: Whether a 0.70 minimum preserves representative full-core positives for every maintained profile; this is part of the next verification.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Global minimum similarity 0.65 and best-score margin 0.08 calibrated on short positive/control phrases | Separated the initial short generic adult-fashion control from the six profile prototypes | Did not cover a full frozen-core query containing ordinary pose, silhouette, studio, and lighting language |
| Registry-owned minimum 0.70 with unchanged vectors | Removed the generic-fashion leak while preserving the descriptive inner-thigh runtime | Required an all-profile full-core replay before the new global threshold could be accepted |

## Resolution or next safe step

- Resolution/workaround: Raised the registry-owned global optional-retrieval minimum from 0.65 to 0.70 and regenerated the registry-hash-bound index while reusing unchanged vectors. This is a relevance threshold only; it does not add a content, adult, or safety gate.
- Verification: The exact production-style replay now emits only optional `inner_thigh_negative_space` for the descriptive positive and nothing for generic adult fashion. Across six valid exact-free full-core positives, every intended profile ranked first and was emitted; the lowest positive score was 0.770205. Six adjacent full-core controls emitted no profile; their highest score was 0.681438. Both candidate packs also passed the public authorial-pack audit and exposed no visual-profile score, vector, rank, matched term, or match-basis field.
- Next safe step if unresolved: Keep the semantic candidate optional and report the precision limit; do not convert it into a hard duty or add an adult/safety blocker.

## Reuse guidance

- Avoid: Calibrating a visual-profile threshold only on short phrases when production embeds a full frozen authorial core.
- Prefer: Include representative full-core positives and unrelated full-core controls in real-index calibration.
- Applicable when: A semantic resolver embeds interpreted intent, subject, setting, event, priorities, baseline, and definitions together.
- Re-check when: Retrieval-text recipe, profile prototype text, embedding model, or global threshold changes.
