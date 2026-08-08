# Creative Direction Pixel Premise Legibility

- Date: 2026-08-08
- Status: resolved
- Scope: `photo-prompt-image-generator` creative-direction frozen render qualification
- Goal: `GOAL_PLAN.md` Viewer-Perceived Creative Direction and Authorial Voice
- Severity: material; two of three first final renders fail fixed pixel focus
- Evidence root: `generated_images/creative-direction-holdout-v1-20260808_163100/`
- Resolved by: `../passed-reports/2026-08-08-viewer-perceived-creative-direction.md`

## Failure

All three creative packs and composed prompts pass the new structural and literal-binding audit. The first built-in image render was then inspected without prompt metadata.

1. `01-potter/final/attempt-01.png` preserves the top-down hand, cup, workshop dust and alignment, but turns the intended empty contact trace into a solid brass circular tool or base. A viewer cannot reliably recover an absent larger vessel; the non-default premise and surprise-to-insight focus fail even though the frame is more intentional than baseline.
2. `02-urban-solitude/final/attempt-01.png` renders a normal dark human reflection in the pavement. The warm domestic image inside the tote is legible, but the selected single reflection law and its first required consequence—a missing traveler reflection—fail.
3. `03-transformation/final/attempt-01.png` is a useful positive control: direct view shows one adult repairing a bicycle lamp while the closed case shows temporally mismatched gloved hands. The repeated hand relation, omission of spectacle, and delayed reflection are metadata-free legible.

## Root Cause Boundary

The audit verifies that declared visual evidence is literal in the prompt; it cannot prove image-model relation following. In the failed frames, familiar photographic priors overrode the chosen rule:

- an outlined circular trace was materialized as a real circular object;
- a person over wet pavement received the default full-body reflection despite explicit absence language.

This is not a candidate taxonomy or safety failure. Adding more operators, presets, adjectives, or anomalies would not address it.

## Bounded Repair

- Potter: state that the circle contains no ring, disk, base, mold, or object; define it as dust displaced from bare tabletop, with surrounding residue completing the missing footprint. Keep cup and hand just offset from the negative-space outline.
- Urban solitude: place the missing reflection in the highest-priority scene description; describe a matte human-shaped blank directly under the traveler, with store and neon reflections visibly continuing around its boundary. Keep the tote's warm domestic reflection as the second consequence.
- Regenerate a pristine same-seed pack/prompt/image once per failed case. Preserve every first attempt. Do not edit the pixels or generate a batch for selection.

## Repair 1 Result

- Potter PASS: removing every physical ring/base interpretation produced a rimless bare-table circle made only by displaced clay dust. The cup hovers off-center above it, so the missing footprint and practiced comparison are recoverable.
- Urban solitude FAIL: the matte person-shaped blank instruction still produced a normal complete reflection. The stronger negative relation also displaced the tote's domestic evidence. This confirms that repeated absence wording is fighting a strong model prior rather than improving the product contract.
- Final repair direction: use the already-developed `functional_recontextualization` proposal instead of stacking more absence language. Give the grocery tote one new function as a portable room threshold; bind a warm apartment doorway inside its translucent side and a narrow dry corridor continuing from its base. This keeps one rule, the same scene, and the same aboutness while using relations the first render partly demonstrated.

## Verification and Lifecycle

- Repair count: Potter 1 of maximum 2 and resolved at the case level; urban solitude 1 of maximum 2 with one final repair remaining.
- Resolution requires both repaired cases to pass every frozen metadata-free focus, not merely prompt audit.
- On resolution, set this report to `resolved` and link the final qualified success report if one is warranted. If the same cause survives two repairs, stop under `GOAL_PLAN.md` rather than weakening the gate.

## Resolution

Potter passed on repair 1 after the physical base was replaced by a rimless displaced-dust footprint. Urban solitude used the final repair budget to select its already-developed functional-recontextualization proposal; a transparent tote now contains a warm room and continues as a dry amber corridor across wet pavement. Transformation passed its first render. The versioned review records 3/3 cases passing every frozen focus, and the full 401-test suite plus dictionary/scene validators passed. This report is therefore resolved without weakening the pixel gate.
