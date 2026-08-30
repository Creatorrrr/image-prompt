# Arm-05 Qualification Result

Outcome: **render completed; pixel qualification failed**. The built-in image tool succeeded twice, but the final saved image did not realize the required elbow-torso background opening. Prompt and runtime preflight success are recorded separately from rendered-pixel failure.

## Frozen source and candidate pack

- Request envelope: `coordinator/request_envelopes/arm-05.json`, SHA-256 `67069932b5eeff7a8e4ba442b59a256e7299f14cfa9f54e4ac1af37868fb934c`.
- Authorial core: `authorial_core.json`, file SHA-256 `01269cbd81d18f3b47921f652f26f714ec489cc0deb6e2c02513a246a5aea3b2`; pack-canonical core SHA-256 `702f6dd3a6fe54f221aca9663c68ac66c327c9f20639762be9309610f1c71110`; intent-lock SHA-256 `4bae2f2dcf8d28d1890da5ceafe0de34224c139b71292033d225836e257aa33f`.
- Exactly one v6 candidate pack was produced: `candidate_pack.json`, SHA-256 `a1b37ea45a9e3f278a408de72a09469581b5239f555355e8140923682bad1589`, `pack_id: 04cf124135c1a79d`.
- Assigned profile `body_bounded_negative_space` surfaced both as a semantic clarification and as optional `visual-concept:body_bounded_negative_space`; it was applied and promoted to a hard visual obligation.
- Assigned candidate IDs `propped_elbow_recline_support`, `single_arc_c_curve_pose`, and `bent_elbow_torso_negative_space` did not surface in the pack and were not falsely selected. Their agent-selected test meanings were already frozen independently and remain literal in the final prompt. Full decisions are in `qualification_decisions.json`.
- Context-mismatched `inner_thigh_negative_space` and all six sampled creative candidates were rejected.

Two early generator invocations produced no pack: one stopped at core-schema validation, and one stopped on the coordinator-confirmed transient shared-index mutation. The 161-word baseline meaning was preserved; only unsupported extra lock-dimension labels were removed before the successful canonical pack run. Shared registry/index data was never edited by this arm.

## Prompt and runtime audit

- Final composed prompt: 179 words, `composed_prompt.json`, SHA-256 `99bc0dacd4c7f56411069f2bc4b6f4fcdacf7a23a9cfee1e1c6cf15426f639c5`.
- Composed audit: **PASS**, zero blocking failures. `quality_status: warn` contains only three expected uncovered-intent notices whose exact phrases remain literal. Audit record SHA-256: `1f374adf7bf3e471dab7631496641a84a010399461f81ea65f77b8033e637ffb`.
- Effective visual contract SHA-256: `ca0f23edd22c2cbb1bdc95114536abba184c29882fb34d9d2329f02466601103`.
- Attempt-1 runtime audit: **PASS**, `runtime_prompt_id: 12ae928952ad0fa7`, one reference.
- Attempt-2 runtime audit: **PASS**, `runtime_prompt_id: 82b8be5bf8a76935`, edit target plus facial-appearance reference.
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`; role `facial_appearance_only`; identity control `false`; no biometric or same-person claim.

## Image and pixel evidence

- Tool: built-in `imagegen` only.
- Image-call count: **2**. The second call was the one permitted geometry retry; no further call is allowed.
- Attempt 1: `image-attempt-01.png`, 1448×1086, SHA-256 `2f8ffa8368b8107551f81d69254b3caab8d40ec963c304f5ec756e6f33335ed9`.
- Final attempt 2: `image-attempt-02.png`, 1448×1086, SHA-256 `d88a962c80c44e5ea1d11b568716590fa216685c528073c16b1521b565f522dc`.
- Final `pixel_review.json`: SHA-256 `1ab46db85d75f3e2fc92f660ec53c4ff7101b82805213e44af58e2b16371ae33`; fixture registry/atomic gate IDs were checked for exact set equality.

Passed final gates:

- `vo_body_negative_space_region_specific`
- `pose_arm05_elbow_load_path`
- `pose_arm05_single_c_arc`

Failed final gates:

- `vo_body_negative_space_real_boundaries`
- `vo_body_negative_space_continuous_background`
- `vo_body_negative_space_shape_legible`
- `pose_arm05_elbow_torso_void`

The supporting elbow is genuinely planted and load-bearing, and the body follows a single same-side arc. However, blue sleeve fabric and hair fill the elbow-torso region, so no continuous background patch or readable enclosed void exists. Prompt presence was not counted as pixel proof. Overall verdict is therefore **FAIL** under the fixture rule requiring all registry and atomic gates to pass.

User preference and facial resemblance both remain `pending_requesting_user_judgment`.

## Independent provenance

- Manifest: `run_manifest.json`, `photo-independent-run-manifest/v2`, SHA-256 `6e6943ae95cd3d7cb34c38093e4522aecd9175cddcbf4d3d6a6f844c79da7b86`.
- `cross_arm_inputs_used: false`.
- Repo-local ledger: `runs/image_runs.ndjson`; attempt run IDs `087a810580227f0c` and `54f5f67779d0bd2d`.
- Source snapshot: `coordinator/source_snapshot.json`, SHA-256 `8bfc9d8b24bc3593d18468701a9ae47312aa9f95e20cac5ad62bd38e58f0d1f6`.
- Frozen skill SHA-256: `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`.
