# Arm 1 — Urban surreal rendering report

## Outcome

This arm produced and preserved two native `image_gen` attempts for **The Rain Atlas Exchange**. The candidate-package and both exact runtime-request audits passed. The frozen urban-surreal narrative, adult fully clothed subject, facial-appearance reference use, materials, and two-handed translucent-plan action survived rendering. The newly tested body/composition semantics did **not** achieve a strict pixel pass: counter-tilt stayed partly hidden by the plan, the arm–waist background void did not become a clean recognizable triangle, and the two-curve S-route remained a C-like window arc plus separate plan curve.

The final saved output is `rain-atlas-exchange-attempt-2.png` with SHA-256 `e1349d7c0576ae68f2ecc8732b2c1bf472c11b1a27a52eee6f8ff17ef92331eb`.

## Independent authorial freeze

- Seed: `3947272135`
- Concept: a woman steadies a translucent rain atlas inside a wet flood-control atrium while detached window bays crest overhead as an impossible architectural wave.
- Raw frozen core file SHA-256: `268347a54b3adb2a81e07a99206c36196219e9a30213f0fa67a64a64f69fea63`
- Generator-normalized canonical core SHA-256: `618a4b897143ac3f6c7a5420ff9d1c1f7ce105a448de6a12dd279ccf6683dda6`
- Intent-lock SHA-256: `edcabe55653a8e4789f51ac5d0755b0b6b9bf81f6d70943f1efed2fe2e29a5c5`
- The first raw core hash `4af875a80d7bbb38704be23892310dbd21abf9f492ff0b39167a63d438b10d47` was superseded before candidate emission because two metadata dimension names were outside the typed schema. The baseline prompt and concept were unchanged; `prepack_schema_validation.json` records the failure and schema-only mapping.

No sibling-arm file, prompt, pack, message, or image was used.

## Candidate pack and composition

- Pack: `bcb6f8c4fa6bb417`
- Pack SHA-256: `a307ddfe176d607f552f44b4d3782eb8eccf64ccf74ea0558304c75a4546c918`
- Mode: v6, hybrid semantic selection, hybrid augmentation requested, creativity `0.65`, identity reference-edit mode.
- Adopted IDs:
  - `slot:body_pose:contrapposto_full_body`
  - `slot:composition:negative_space`
- `contrapposto_weight_shift` itself did not surface as a visual profile, but its slot candidate did and was transformed into a loaded left support leg, relaxed right curb leg, and intended counter-tilt.
- `body_bounded_negative_space` did not surface as a profile. The eligible generic negative-space candidate was transformed into an arm–waist background-triangle proxy; this was never claimed as a promoted profile contract.
- `hogarth_waving_line_of_beauty` did not surface. Its two-curve idea fit the frozen wave/plan/coat relation and was tried only as an open composition decision, not as a selected profile ID or hard gate.
- The surfaced `medium_native_glitch` and `kuudere_composed_warmth_relation` visual concepts were rejected as context mismatches.

## Prompt and preflight

- Exact composed prompt: `prompt.txt` (178 words)
- Composed audit: `status=pass`, `quality_status=warn`; warnings are the four mandatory anchors preserved by free literal description rather than candidate coverage.
- Runtime attempt 1 audit: PASS, runtime prompt ID `f7c2d6a9e2aacbb1`.
- Runtime attempt 2 audit: PASS, runtime prompt ID `f947bed2851e2f0e`.
- Effective selected visual-contract SHA-256: `null`, because no optional visual-profile candidate was promoted.

## Pixel review

Both attempts were inspected at 213×320 thumbnail and 1023×1537 native scale.

- Facial appearance: visually consistent overall with the provided reference's hair framing, face length, eye spacing, nose/lip placement, and adult presentation; the generated eyes are somewhat rounder and the lower face somewhat narrower. This is not an identity or biometric claim.
- Frozen concept: PASS. The wet civic atrium, full-body woman, plan, window wave, teal/amber light, and fully clothed nonsexual editorial treatment are clear.
- Contrapposto counter-tilt: FAIL. The support/free-leg arrangement reads, but the plan hides the hip line and the opposed hip/shoulder tilt is not unambiguous at thumbnail scale.
- Arm–waist body-bounded negative space: FAIL. The map and coat fill the intended opening, so no clean continuous-background triangle survives.
- Hogarth waving-line probe: FAIL. The windows create one strong C-like curl, while the plan curve remains separate rather than forming one dominant S-route.
- Anatomy/material/text: PASS. Hands, legs, boots, wet surfaces, raincoat, translucent plan, and surreal window structure are coherent; no prominent malformed readable text or watermark appears.

Attempt 2 preserved the successful face, scene, wardrobe, and material qualities but did not materially repair the three semantic failures. The single permitted repair was consumed; no further image call was made. Full details are in `pixel_review.json`. Requesting-user aesthetic judgment remains pending.

## Provenance

- Tool: native built-in `image_gen`
- Image calls: 2
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Source commit: `e27e2dd816506ba148a9b775458897d5f6334273`
- Photo-prompt skill SHA-256: `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`
- Arm-local ledger: `image_runs.ndjson`
- Coordinator merge entry: `image_run_entry.json`
- Independent manifest: `run_manifest.json`
