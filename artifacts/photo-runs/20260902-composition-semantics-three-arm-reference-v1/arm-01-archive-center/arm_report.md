# Bounded outcome: FAIL / revise

The frozen v6 package, composed prompt, exact runtime request, reference bytes, and single built-in image call were valid. The delivered image passed 11 of 12 strict pack-derived visual gates, but `vo_composition_center_anchor_location` failed. Under `partial_is_fail`, this arm is not technically qualified. User judgment has not been received.

## Package

- Arm: `arm-01-archive-center`
- Concept: flooded archive map rescue
- Candidate pack: `photo-candidate-pack/v6`, pack `f62f45eb1f3f4ea2`
- Generator controls: creativity `0.5`, seed `902001`, exactly one pack written through `--output-file`
- Active hard profiles: `centered_primary_anchor_relation`, `frame_within_frame_boundary_relation`, `primary_secondary_figure_ground_hierarchy`
- Optional visual concepts selected: none
- Creative augmentation: all six sampled rows explicitly rejected; no ordinary candidate selected
- Frozen authorial core SHA-256: `038f0de1373809a895083de444eb67eff26c99aef544bd8af2563a6c45023455`
- Frozen intent-lock SHA-256: `09c5b2e1fcbe8dd25900b9441cb1c24a1f67b21d96a2c516f814fca93911a414`
- Reference role: `visible_adult_appearance_reference_only`
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Reference use was limited to observable adult appearance. No identity, same-person, biometric, protected-trait, health, attractiveness, personality, occupation, ethnicity, nationality, or allegiance claim was made.

## Prompt and runtime

- Final positive prompt: 290 English words, within the blocking 24–320 bound
- Every active visual-obligation evidence field is literal in `composed_prompt.json`
- Composed audit: `PASS`; failures `0`; advisory quality status `warn` because the hard-evidence load exceeds the default concise target
- Effective visual-contract SHA-256: `26e1021867ba62530ccf6542e9e872d8da6a1fa95329945de92038832f9e4a45`
- Runtime audit: `PASS`; exact positive prompt, negative bytes, intent-lock binding, reference path/hash/role, and audit boundary all matched
- Runtime prompt ID: `a2a86e999e2f82f7`

## Generation

- Tool: built-in `image_gen`
- Image calls: `1`
- Retries: `0`
- Fallbacks: `0`
- Cross-arm inputs: none
- Saved result: `final.png`, 1023 x 1537 PNG
- Result SHA-256: `a4914d8e2579cba93b7b39dbceffb960f1ce74d7c5de04dd7765a7c81349b91e`
- Ledger run ID: `588ed4b4f4dd85b2`
- Ledger prompt ID: `73c2d6ba47b75707`
- Manifest: `photo-independent-run-manifest/v2`; source `git:215be788525890eecc38114838b457cec584f5bf;working-tree-dirty;composition-semantics-v1`; skill SHA-256 `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`

## Pixels

- Inspection scales: 213 x 320 thumbnail and 1023 x 1537 native pixels
- Strict result: `11 PASS / 1 FAIL`; schema failures `0`
- Failed gate: `vo_composition_center_anchor_location`
- Image-grounded reason: the exact frame center falls on the plain upper apron and torso. The face is clearly above center, while the working hands and rolled-map action are below center, so the intended identity/action anchor does not intersect the true center point.
- Passed: central first-read dominance; supporting margins; centrality beyond symmetry; scene-bound physical opening; three-side enclosure; near-plane depth; non-vignette boundary; primary-first hierarchy; readable subordinate brass catalog plaque; supportive background; hierarchy beyond blur alone.
- Review audit status: `failed_technical_hard_gates`; technical qualification `false`; representative eligibility `false`.

## User judgment

- Source: `not_yet_received`
- Aesthetic/semantic acceptance: pending
- No baseline comparison was available in this arm.

## Artifacts

- `candidate_pack.json`
- `composed_prompt.json`
- `composed_audit.json`
- `runtime_request.json`
- `runtime_audit.json`
- `final.png`
- `thumbnail.png`
- `render_review.json`
- `render_review_audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
