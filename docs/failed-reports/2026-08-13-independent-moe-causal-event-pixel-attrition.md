# Independent moe causal events were not reliably legible in rendered pixels

- Recorded: 2026-08-13 KST
- Status: open
- Goal/checkpoint: Independent Japanese-subculture moe generation, Stage 6 pixel review
- Affected scope: `photo-prompt-image-generator` behavior-led moe composition and image-runtime realization
- Search terms: independent five arm, causal event legibility, primary mechanism legibility, Decora, retro arcade, exact negative
- Related paths: `skills/photo-prompt-image-generator/SKILL.md`, `skills/photo-prompt-image-generator/references/composition-contract.md`, `skills/photo-prompt-image-generator/references/image-runtime.md`, `GOAL_PLAN.md`

## Failure

- Conditions or trigger: Five isolated agents independently authored an `authorial-request/v1`, materialized one v4 candidate pack, passed composed-prompt and exact runtime-request audits, and made one identity-preserving built-in image edit each from the same adult reference. No image was retried.
- Expected: Each prompt's concrete baseline-breaking event and emotional leak should be readable in the native pixels while preserving the chosen Japanese-subculture family cues.
- Observed: All five images preserved adult identity and rendered at least two requested family cues. Only arm 4 made the causal event readable; arms 1, 2, 3, and 5 reduced the requested interrupted action to a calm task, posed smile, or ambiguous hand interaction. Arm 4 still failed full qualification because generated heart-shaped charms violated the exact negative prompt.
- Impact: The skill repair proves that plant convergence, pre-pack provenance, and style evidence were fixed, but it does not prove reliable pixel-level behavior-led moe. Zero of five images qualify as representative, and requesting-user genuine-moe judgment remains pending.

## Evidence

- Durable artifacts: `generated_images/japanese-subculture-moe-five-reference-v2-20260813/`
- Review summary: `generated_images/japanese-subculture-moe-five-reference-v2-20260813/evaluation/review_summary.md`
- Source: base `795691ed4f843e161f79e16a983849e6e9d187ec`, skill tree SHA-256 `b356e6b5f9f3491bd30959e67e075223de89338f278a88a190ef2090fc5b29d7`.
- Aggregate: images 5/5, adult identity 5/5, two or more visible style cues 5/5, plant scenes 0/5, readable causal events 1/5, fully qualified 0/5.

## Cause assessment

- Confirmed: Prompt and runtime audits are structural preflight checks and cannot guarantee pixel realization. The output model often preserved the broad venue, fashion, props, and face while weakening the small object-state transition and its causal emotional response.
- Hypothesis: The 120-word identity/style/negative constraint load competes with a multi-part micro-event. Events depending on tiny contact geometry, simultaneous hand states, and a subtle before/after expression are especially vulnerable.
- Confidence: High for the observed failure boundary; medium for the causal hypothesis until a separately authorized render comparison is run.

## Attempts and boundary

| Attempt | Result | Boundary |
|---|---|---|
| Five independent pre-pack concepts with one render each | Five distinct prompts and images; no plant scene | Independence and prompt diversity did not guarantee pixel event legibility |
| Explicit same-focal-plane event evidence | Style/identity remained strong; four events stayed ambiguous | Text preflight passed but native pixels failed the causal gate |
| Fail-closed review with no retry | Preserved unbiased evidence | The fixed budget forbids rerolling toward a favorable result |

## Next safe step

- Do not retry these five images or promote arm 4 as a clean success.
- In a new, separately authorized goal, test a smaller runtime event contract that prioritizes one large, unmistakable state transition and one facial leak, then compare it against the current dense identity/style prompt under a frozen character and a declared image budget.
- Keep style evidence and causal-event qualification separate. Continue treating the requesting user's direct moe judgment as distinct from technical gates.
