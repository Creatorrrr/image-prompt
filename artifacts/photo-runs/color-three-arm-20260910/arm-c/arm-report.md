# Arm C: ceramic artist color study

Outcome: the saved image visibly satisfies all three independently authored color hypotheses. The selected full data contracts pass 4/4 visual gates plus 5/5 embodiment gates. **All-three new-data adoption fails coverage** because Muted-on-Vivid was absent from the real candidate packs. Its pixel result is supplemental baseline-authored evidence only. User preference remains pending.

## Independent setup

- Random seed: 1986106126; independently authored scene list selected a ceramic artist arranging monumental glaze samples.
- The actual requester envelope was coordinator-frozen and hash-verified. Baseline/core were frozen before assets, references, scripts or packs were read. Reference portrait was viewed before the reference edit.
- Baseline: 247 words; SHA-256 `390748f7856b6c4b58d95067dd992d43190087947c21e122b37f22f46b8f3f64`.
- Canonical core SHA-256: `77c70ad2dd5a711c633eba81dc0e50ddbd52dd6819d47371499898e5e6b2e519`.
- No sibling pack, prompt, image, research or maintenance fixture was read. Only arm-local artifacts were written.

## Actual exposure and composition

The original retrieval is preserved under `retrieval-v1/`. At coordinator request, the index-refresh retrieval is preserved under `retrieval-v2/`. The frozen core and seed were unchanged. Both actual public packs exposed only `visual-concept:cr_color_blocks` and `visual-concept:cr_diagonal_split`; both were read in full and selected with every component and gate. No new color slot or bundle appeared. The public pack ID remained `be22f0d40f8abfff`.

The final composed prompt is 327 words. All ordinary/creative candidates were rejected; no unexposed candidate was injected. Complete selected profile evidence was added in open color/composition/material dimensions while preserving the locked portrait subject, ceramic touch event and reference usage. Composed audit PASS; exact runtime/reference-byte audit PASS.

## Generation and strict pixels

- Tool: `image_gen__imagegen`, one reference edit call, no retries.
- Concrete native PNG was copied byte-for-byte to `generated_images/ceramic-color-20260910/attempt-1.png`; the native original remains intact.
- Review scales: native 1086×1448 and a 320px wide review-only thumbnail.
- Color Blocking: PASS. Large bounded blue/red wall fields and three square slab faces; visible glaze, bevels, shadows and depth at both scales.
- Diagonal Color Split: PASS. Upper-left cobalt and lower-right vermilion share a long rising diagonal boundary legible around the figure.
- Muted-on-Vivid supplemental baseline criterion: PASS. Dusty gray clothing and subdued skin contrast clearly against saturated fields. This is not evidence of adoption of an unexposed profile.
- Embodiment: 5/5 PASS. Both feet and bench supports are shown. The artist’s right fingertips touch the blue slab upper edge; her left hand rests on the table. The red slab locally occludes the left wrist, but the arm/hand support relation remains assessable and coherent.
- Reference appearance supplemental check: similar recognizable face, long dark waves and natural skin rendering. This is visual similarity, not identity authentication.

`strict_render_review.json` contains all 9 exact hard gates and image-grounded observations. `render_review_audit.json` reports `technical_qualified: true`, no schema failures and no failed hard gates; its nonzero exit is due to pending requesting-user judgment, so `representative_eligible` remains false. No generic repair contract was active; no repair retry was performed.

## Evidence

`test-case.json` was frozen before generation. Full request/core/baseline/embodiment records, both packs and composer views, selected full details, composed/runtime audits, exact runtime request, source image hash, native result path, local ledger (`image_runs.ndjson`) and independent v2 run manifest are preserved in this arm.

This one uncontrolled render cannot establish causal improvement over the previous data implementation. It demonstrates selected-contract pixel fidelity for two exposed relations and supplemental baseline fidelity for the third, with incomplete candidate-data coverage kept as a failure.
