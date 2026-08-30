# arm-04 qualification result

Overall result: **FAIL**. The bounded run completed with two built-in image calls. The final saved image passes the perched-support and relaxed-wrist atomic gates but fails `pose_arm04_crossed_ankles` because the lower calves cross while the visible ankle joints remain side by side.

## Frozen intent and provenance

- Request envelope: `../../coordinator/request_envelopes/arm-04.json`
  - file SHA-256: `4d457d73b8831c05540127bca65ce2bb844a6dddc9e36dbafd31e69450dde6fd`
  - request-text SHA-256: `c63f586dc12b8e08e292bca34f6fd9f4a6251e38f3b9aca645ce96060bd9277c`
- Reference portrait: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`
  - SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
  - role: facial appearance only
  - identity control: `false`
  - same-person/biometric claim: none
- Authorial core: `authorial_core.json`
  - baseline words: 173
  - file SHA-256: `e3ce598ae91c8242ab5d3c59ff7cdac8bad54863bd0b923a48cf8cb8f320a0e0`
  - canonical v3 SHA-256: `1d59689644210a3239fa65f00b4020f232910e7bafb59ccb0e841ee57bcf9463`
  - intent-lock SHA-256: `b7737e30c6d5857f1ccec3032f020e538ac7ad5cbdb7d47d62ac6e109675e20b`
  - `source_request` byte-matches the coordinator envelope.
- Pre-pack schema note: the first frozen file used four unsupported dimension labels. Before any pack was emitted, only those labels were mapped to supported equivalents (`appearance_reference -> reference_use`, `pose_geometry -> pose`, `output_medium -> format`, `color_palette -> color`). `baseline_prompt_en`, scene, event, pose meaning, and anchor evidence did not change. See `core_schema_normalization.json`.
- Skill SHA-256: `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`
- Source snapshot base commit: `ae84f15022d07211d583ca917952bc8dc9cff11b`

## Candidate pack and composition

- Exactly one successful v6 pack was emitted: `candidate_pack.json`
  - file SHA-256: `0e96d7b9d52558a71df42e8a63c37ca01cd34cdc0e36de5c6e296d364cedca0a`
  - pack ID: `f383e0d9d4910d53`
  - pack contract: `photo-candidate-pack/v6`
- Assigned-candidate surfacing: **0/3**.
  - `perched_edge_sit_grounded_support`: not surfaced; not selectable; not applied or rejected as a pack candidate.
  - `crossed_ankles_narrow_base`: not surfaced; not selectable; not applied or rejected as a pack candidate.
  - `relaxed_wrist_offset_line`: not surfaced; not selectable; not applied or rejected as a pack candidate.
- The three agent-selected test meanings were nevertheless preserved from the already-frozen core anchor and expressed literally in the final prompt. They are not requester definitions. Full evidence is in `assigned_candidate_decisions.json`.
- Pack decisions:
  - applied: required `clarification:authorial-core:interpreted-intent`;
  - rejected: unrelated hands-free drink and uncanny-mismatch visual-profile clarifications;
  - rejected: all six sampled creative-augmentation candidates;
  - selected ordinary candidate IDs: `[]`;
  - selected optional visual concepts: `[]`.
- Composed prompt: `composed_prompt.json`
  - words: 180
  - file SHA-256: `7b3088fad982f40ec4e734f8fe68c18a095eced48ecd68b284229cd3e454314b`
  - audit: **PASS**, no blocking failures; quality status `warn` only because six pack intents were uncovered by candidates but preserved literally by free description.

## Runtime audits and image calls

- Attempt 1 render request: `render_request.json`
  - file SHA-256: `3178f936cd20ef77ea0f1f4a2ed666c22568c4c25ace50a62a687cf8cf5cbb7d`
  - runtime audit: **PASS**
  - runtime prompt ID: `217cc857f90ae9cf`
- Attempt 2 repair request: `render_request_attempt_02.json`
  - file SHA-256: `02e09eba643a3094fc89886597a7431001678bc71267b2b3daa86b4e6cd107aa`
  - runtime audit: **PASS**
  - runtime prompt ID: `884ab81b7dcf8058`
  - repair scope: lower-leg/foot staging only; passed support/wrist geometry and all locked semantics preserved.
- Image tool: built-in imagegen only.
- Total image calls: **2**. No further retry is permitted or attempted.
- Attempt 1 image: `images/attempt-01.png`
  - SHA-256: `c31443df52f74ebc37bf57010d22092201a62b307995c3475b8bd2030487706e`
  - dimensions: 887 x 1774
  - pixel result: failed `pose_arm04_crossed_ankles`; triggered the one allowed local retry.
- Final attempt 2 image: `images/attempt-02.png`
  - SHA-256: `8ff512be2dbf35a07bff01492f74cf705df6178c6491aa7828cc943cf0eea808`
  - dimensions: 972 x 1619

## Final native-pixel review

`pixel_review.json` evaluates all fixture atomic gates on the same final saved image at original detail. Its file SHA-256 is `ee8e32dfd068432c7814257381d17c51894e7b54e97b79cee1bc54b7e8f839ca`.

- PASS `pose_arm04_perched_support`: pelvis bears on the wooden front edge; palm and planted shoes give a readable support path.
- FAIL `pose_arm04_crossed_ankles`: shoes are separate and planted, but ankle openings are side by side and the crossing occurs at the lower calves. This is the fixture's rejected substitute, `crossed calves with uncrossed ankles`.
- PASS `pose_arm04_relaxed_wrist`: the supporting wrist has a soft offset with intact forearm-to-hand continuity and no extreme kink.

Exact failed gate set: `["pose_arm04_crossed_ankles"]`.

User preference and facial resemblance remain `pending_requesting_user_judgment`. Technical pixel review is not a same-person, biometric, or user-acceptance conclusion.

## Manifest and ledger

- Independent v2 manifest: `run_manifest.json`
  - file SHA-256: `c38426d5c5455a245b09d6151cc44e88fc4f1e16dbb5f64d8d6bb41004fb9682`
  - contract: `photo-independent-run-manifest/v2`
  - `cross_arm_inputs_used: false`
  - `image_call_count: 2`
  - ledger run ID: `1fc40f392325a84c`
  - prompt ID: `b78fecf7397e23f5`
- Repo-local ledger row appended to `runs/image_runs.ndjson` for run ID `1fc40f392325a84c`.
