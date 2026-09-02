# Bounded outcome

Technical composition qualification is **PASS for the derived visual contract: 12/12 hard gates passed in one saved image**. Requesting-user judgment has not yet been received, so the result is not representative-eligible and no user-perceived quality claim is made.

## Package

- Generated exactly one `photo-candidate-pack/v6` with creativity `0.5` and seed `902002`.
- Pack ID: `fd8c81da6a916f35`; candidate-pack file SHA-256: `f2ab9e00bdcfd09d8aa2f4ef463a8285029d9be85fbb28f8b8dee47cf1326271`.
- Active hard profiles: `third_grid_focal_anchor_relation`, `look_motion_room_direction_relation`, and `pattern_break_focal_exception`.
- Rejected both unrelated optional visual concepts (`medium_native_glitch`, `kuudere_composed_warmth_relation`) and all six sampled creative candidates. No reference appearance was treated as personality evidence.
- Reference use remained `visible_adult_appearance_reference_only`, bound to `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg` with SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.

## Prompt and preflight

- The final positive prompt is 287 English words and copies all 12 active visual-obligation evidence fields literally.
- `composed_prompt_audit.json`: `status: pass`, no failures. The 180-word recommendation warning is advisory; the prompt remains below the 320-word absolute limit and below the evidence-adjusted 289-word ceiling.
- `runtime_request_audit.json`: `status: pass`, runtime prompt ID `42ef78a2e5d46da0`, exact negative bytes preserved, one reference file verified, and intent-lock SHA-256 `a18f2313249b9dc7e83223d2cdbdc9d0bb8ee17c2c1f98d014e20b7fd135eaac` bound.
- Effective visual contract SHA-256: `196c2edd7bcb3fdd9ed2cb55c7bde6308f7d64b58e42587034becfbebee4d7ba`.

## Generation

- Tool: built-in `image_gen`.
- Image calls: exactly `1`; retries: `0`; fallbacks: `0`; cross-arm inputs: `0`.
- Saved result: `final.png`, 1448 x 1086, SHA-256 `bcbc24527a94cf09f684cdedd4792be9d2c14c1fb2b666fa2d532cf4bd2acc5e`.
- The reference was attached to the single tool call. It was used only for observable adult appearance. No identity, same-person, biometric, protected-trait, health, attractiveness, personality, occupation, ethnicity, nationality, or allegiance assessment was performed.

## Pixels

- Inspected `final-thumbnail.png` at 320-pixel maximum dimension and `final.png` at native resolution.
- Thirds relation: 4/4 pass. The runner's face and raised-flag cluster sits near the upper-left thirds intersection, remains clearly off center, retains broad ferry-pier context, and is established by placement rather than a grid overlay.
- Motion-room relation: 4/4 pass. Profile, stride, bent limbs, flag, and hair define rightward travel; the trailing origin remains visible; roughly two thirds of the frame lies ahead toward the ferry.
- Pattern-break relation: 4/4 pass. Four matching blue pier lamps establish the row, exactly one same-design lamp glows amber, the amber lamp is the strongest thumbnail luminance/color accent, and the row remains coherent. The small ferry beacon is a different object, not a second exception in the lamp row.
- Supplemental fidelity note: the prose asked for five blue lamps, while the image visibly supplies four. This still passes the frozen test case and derived hard gate, both of which require at least four similar baseline forms; the exact prose count did not fully survive rendering.
- `moe_render_review_audit.json`: `technical_qualified: true`, `failed_hard_gates: []`, `schema_failures: []`, qualification status `visual_technical_qualified_user_judgment_pending`.

## User judgment

- Source: `not_yet_received`.
- Representative eligible: `false`.
- The review auditor exits nonzero whenever representative eligibility is absent; here that is solely the pending requesting-user judgment boundary, not a schema or pixel-gate failure.

## Provenance

- Ledger: `image_runs.ndjson` (one row), run ID `06252c6b13025f61`, prompt ID `bd4a9e0542a58bfb`.
- Manifest: `run_manifest.json`, contract `photo-independent-run-manifest/v2`, `image_call_count: 1`, `cross_arm_inputs_used: false`.
- Frozen skill SHA-256: `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`.
- Source reference: `git:215be788525890eecc38114838b457cec584f5bf;working-tree-dirty;composition-semantics-v1`.
