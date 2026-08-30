# Arm-02 Result

Final technical verdict: **PASS**. The second and final saved image passes all four fixture registry gates and both fixture atomic pixel gates on the same native-resolution image. Requesting-user preference and facial-reference resemblance remain **pending**.

## Independent concept

One clearly adult female heritage dancer lights the final brass lamp during a rain-soaked reenactment inside a 13th-century Kakatiya temple mandapa. She is fully and opaquely clothed. The independently frozen pose interpretation combines an inclined-head/opposing-torso-and-hip/flexed-knee tribhanga chain, an axially elongated torso with relaxed lowered shoulders, and a plantar-flexed trailing lower-limb line. The attached portrait is used only for facial-appearance guidance.

## Authorial and pack provenance

- Request envelope file SHA-256: `a4858812981dfc2ce702756fc4b23079a1d318ec468296abbde16cb272ffa21b`
- Authorial-core file SHA-256: `3cceb36891f1490472c76ebbf07b850e729744b36933e88124787e32cdca51db`
- Normalized authorial-core SHA-256: `d256aefaf97f3027ebb83d27e246db508c86e1d3026637a84bc8f6601cf30f4a`
- Intent-lock SHA-256: `3b4a196bc331e7be3ae7c3d7beb203072683da71a51dc0a31e908402e9c18ad4`
- One successful v6 pack: `3142162c2f822e07`; file SHA-256 `523cfe06160cd197bef40d75b55612742dca2180368fac331c474f1ad20eff11`
- Composed prompt file SHA-256: `c2f88b6031597f779f103fbc2254c40951ef727f93708c152d338fc0e51d9972`
- Composed audit: `status=pass`, `quality_status=warn`, blocking failures `0`. The four warnings only report that core anchors absent from sampled candidates were preserved by literal final prose.
- Initial schema preflight required one name-only correction from unsupported lock dimension `appearance_reference` to allowed `reference_use`; the scene, baseline, pose interpretation, anchors, and requester bytes did not change. Both initial and corrected freeze hashes are retained in `authorial_core.freeze.json`.

## Candidate/profile decisions

- Assigned profile `tribhanga_three_bend_pose`: surfaced in `visual_concept_candidates` and `semantic_clarification`; **applied** by selecting `visual-concept:tribhanga_three_bend_pose`.
- Effective visual-contract SHA-256: `53928249bfe5c55d4f9c030c8424a5e8d9b0fff11481c7dc6ac551f4d59e4a59`.
- Assigned candidate IDs `tribhanga_three_bend_full_body`, `axial_elongation_relaxed_shoulders`, and `lower_limb_plantarflexed_line`: did **not** surface as candidate IDs. No adoption is claimed; their geometry remains independently authored in the frozen core/final prompt.
- Unrelated `medium_native_glitch`: surfaced and rejected.
- Creative `balanced_exposure`: transformed into motivated rain-reflected fill. Walking, head-shoulder opposition, low-ground angle, knee-up crop, and generic contrapposto candidates were rejected.

The complete decision record is `candidate_surface_report.json`.

## Runtime and reference boundary

- Tool: built-in `imagegen`; use case `historical-scene`; CLI/API fallback not used.
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.
- Reference role: `facial_appearance_only`.
- Identity control: `false`; same-person claim: `false`; biometric verification claim: `false`.
- Attempt-1 runtime audit: PASS; runtime prompt ID `8beb4bd99ff0d9db`.
- Attempt-2 runtime audit: PASS; runtime prompt ID `3a5e7d362b646ea9`.
- Image calls consumed: `2` of maximum `2`.

## Pixel evidence

Attempt 1 saved as `image-attempt-01.png` (`1024x1536`, SHA-256 `45262642c75ae555ac4edeaadb6769fdb4975a3834e6507c1fd4c1a90ce05e2e`). Its opaque central pleats concealed the flexed-knee hinge, so these gates failed and triggered the single allowed targeted retry:

- `vo_tribhanga_bent_knee_return`
- `vo_tribhanga_full_body_three_bend_read`

Final attempt 2 saved as `image-attempt-02.png` (`934x1683`, SHA-256 `5d95c7e2d67702ad3945b2b79ebf58d1601890b6d60e4f8cb871b5ac1372a4b9`). Native-pixel review passes:

- `vo_tribhanga_inclined_head`
- `vo_tribhanga_opposing_middle_bend`
- `vo_tribhanga_bent_knee_return`
- `vo_tribhanga_full_body_three_bend_read`
- `pose_arm02_axial_elongation`
- `pose_arm02_plantarflexed_line`

Final failed gates: **none**. `pixel_review.json` contains concrete same-image visible evidence for every fixture gate and every reject-substitute check; prompt presence was not used as pixel proof.

## Manifest and ledger

- Independent manifest: `run_manifest.json`, contract `photo-independent-run-manifest/v2`, SHA-256 `164ed734c77a2a82dabfb3aa5dff9157f5bb092e67ad4587246318e32b07040b`.
- `cross_arm_inputs_used: false`.
- Repo-local ledger: `runs/image_runs.ndjson`.
- Attempt-1 ledger run ID: `3f6e1911ce85dbf7`.
- Attempt-2/final ledger run ID: `0ff40c4299a9d0a4`, linked by `retry_of` to attempt 1.

## Remaining user boundary

Technical pixel qualification does not establish subjective preference or resemblance. Both remain `pending_requesting_user_judgment`; no same-person or biometric conclusion is made.
