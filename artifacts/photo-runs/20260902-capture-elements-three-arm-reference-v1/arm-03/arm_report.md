# Arm 03 report

## Outcome

- Assigned profile: `highlight_rolloff_tone_response`
- Frozen independent scene: wind-driven coastal salvage with one adult woman hauling a rope-connected brass ship's bell and blue glass floats from a flooded skiff.
- Native image call count: **1**
- Retries: **0**
- Fallbacks: **0**
- Cross-arm inputs: **none**
- Candidate packs emitted: **1** (`photo-candidate-pack/v6`, seed `1970607820`, creativity `0.5`, pack ID `b8dd7975e1eec422`)
- Optional creative candidates selected: **0**
- Optional visual-concept candidates selected: **0**
- Native render: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/render.png`
- Native render SHA-256: `069d9475763b7b2f1d3bfab0966928e13cb464b3abd884c6a034b77aafea437c`
- Native dimensions: `1023x1537`

## Phase-boundary record

The initial pre-core scene, 146-word baseline, and intent were created before opening the assignment. The assignment was opened before the first generator preflight exposed unsupported custom dimension labels. The exact schema-only mapping, original pre-core hash, rejected preflights, assignment timing boundary, and final normalizer hashes are preserved in `preflight_amendment.json`. No scene, event, subject, baseline prompt, interpretation, or variation meaning changed after the assignment was opened.

- Original recorded pre-core hash: `3b583eec7f13b7d6a3cf22dac43967b251e6cf17902c1e70eaf3b9d320d5670a`
- Final normal-generator canonical core hash: `527b4075420a1763f82b1559c7ad1fc42a8c187e5cfb28a80088f3b71b28cc1b`
- Final intent-lock hash: `494579d3b931ceae300ffb321b4e63da4ca44b3f058d6d111bd33408119a866c`

The first three candidate-pack commands failed before emitting any pack: unsupported core-dimension vocabulary, undersized visual-intent evidence, and an unsupported governing source field. The fourth command emitted the run's sole candidate pack. These are preflight failures, not image-generation calls.

## Audit status

- Composed prompt audit: **PASS** (`quality_status: warn` only because the 271-word prompt exceeds the default 180-word concise target; it remains below the evidence-adjusted 275-word advisory ceiling and the 320-word absolute limit).
- Runtime request audit: **PASS**, runtime prompt ID `ecae4f6f8ae3d936`, exact pack negative preserved, one reference attached, role `appearance_only`.
- Render review audit: **PASS for technical qualification**; `visual_technical_qualified_user_judgment_pending`.
- Representative eligibility: **false**, solely because requesting-user judgment has not yet been received.

## Hard-gate verdicts

All verdicts use the same saved image. `partial`, missing, uninspectable, and substitute evidence were treated as failure conditions.

1. `vo_capture_rolloff_clear_near_white_anchor` — **PASS**. At thumbnail scale, the sunlit cloud opening beside the beacon is an immediate near-white diffuse anchor, reinforced by bell and foam speculars.
2. `vo_capture_rolloff_gradual_bright_steps` — **PASS**. At thumbnail and native scales, the cloud opening and bell reflection show several distinguishable luminance steps into white.
3. `vo_capture_rolloff_small_confined_clip_core` — **PASS**. Native analysis found 210 exact-white pixels of 1,572,351 (`0.0134%`); the largest four-connected exact-white component was 14 pixels.
4. `vo_capture_rolloff_texture_hue_midtones_survive` — **PASS**. Bronze patina, blue glass, orange sail, cloud structure, foam detail, black clothing folds, and cliff separation survive around the highlights.
5. `vo_capture_rolloff_not_flat_glow_or_hdr` — **PASS**. Native detail retains deep-tone separation and natural bright-edge transitions without local HDR outlines, gray highlight substitution, or generalized glow.

Overall pixel verdict: **PASS for the exact assigned five-gate technical contract**.

## Judgment boundary

The supplied JPEG was used only as an appearance reference for visible adult facial structure, eye shape and spacing, face length, lower-face and jaw width, hairline, and hair. This arm makes no identity or same-person claim. Requesting-user acceptance of the generated appearance and visual result remains pending and is not replaced by the technical pixel pass.

## Exact artifacts

- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/authorial_core.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/authorial_core.sha256`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/intent_lock.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/baseline_prompt_en.txt`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/preflight_amendment.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/visual_intent.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/candidate_pack.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/composed_prompt.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/composed_prompt.audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/image_render_request.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/image_render_request.audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/render_request_corrections.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/image_runs.ndjson`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/render.png`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/render-thumb.png`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/review-highlight-sky.png`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/review-highlight-bell.png`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/self_review.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/self_review.audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/self_review_corrections.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/run_manifest.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-03/arm_report.md`
