# arm-01r independent qualification report

## Outcome

The assigned `panning_subject_tracking_motion_relation` profile is **not pixel-qualified** in the single allowed render. Package composition and the exact runtime request passed their audits, but the native-pixel review passed 3 of 5 hard gates and failed 2. The saved render remains failed technical evidence and is not promoted.

## Independence and execution counts

- Arm root: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r`
- Native image tool: built-in `image_gen`
- Native image calls: **1**
- Retries: **0**
- Fallbacks: **0**
- Explicit API calls: **0**
- Cross-arm inputs used: **false**
- Ledger rows: **1** (`attempt: 1`, `retry_of: null`)
- Ledger run ID: `9820da409541c9f5`
- Runtime prompt ID: `fb2655112552e2e3`

No sibling arm, prior experiment, or other arm's prompt, pack, image, or message was used as input.

## Prompt and reference summary

The independently frozen concept is a quiet archival mechanism in a circular underground archive. An unmistakably adult woman rides left-to-right with a brass cataloging apparatus on a low rail trolley, feeding a translucent ribbon through a hand-cranked sorter while steadying a numbered glass cylinder containing one pressed fern. A slow lateral pan was specified so her identity-bearing core stays comparatively sharp, the archive streaks laterally, secondary parts retain local motion, and all cues agree on one vector.

The only attached reference was `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`, SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`, with role `appearance_only`. It controlled only facial structure, eye shape and spacing, face length, lower-face and jaw width, hairline, and long dark wavy hair. No identity, same-person, ethnicity, nationality, protected-trait, health, attractiveness, personality, or occupation claim was made.

The assigned panning profile was activated as a mandatory request-scoped visual obligation through `photo-visual-intent/v1`. It therefore was not an optional `chosen_visual_concept_ids` row. The unrelated optional visual candidates for medium-native glitch and kuudere behavior were rejected; `chosen_visual_concept_ids` is `[]`.

## Audit results

### Package and prompt

- Candidate pack: `photo-candidate-pack/v6`, creativity `0.5`, pack ID `122b8269fba3b4a0`.
- Composed-prompt audit: `status: pass`, zero failures, `quality_status: warn`.
- Prompt length: 215 words. This exceeds the 180-word concise target but stays under the 218-word evidence-adjusted ceiling and 320-word absolute maximum.
- The remaining warnings say the four frozen uncovered intents were preserved through literal free description/assertion; none is a failure.

### Runtime

- Exact render-request audit: `status: pass`, zero failures.
- Exact reference count: 1.
- Negative prompt matches the candidate pack byte-for-byte.
- Runtime request binds intent lock `7686c94c39b50342f573e75dc679ee4c5ab504f1a2cbfc79c01eeab501d225c8` and effective visual contract `5235238ec593e6353e10f541a2b1f62094a5ac8f0503e6b051cca7ce20c53e17`.

### Pixel review

- Inspected at 384x288 thumbnail and 1448x1086 native scale.
- Review schema failures: 0.
- Qualification: `failed_technical_hard_gates`.
- Strict result: **3 PASS / 2 FAIL**. Partial, missing, or ambiguous evidence is treated as fail.

| Hard gate | Scale | Verdict | Pixel evidence |
|---|---|---|---|
| `vo_capture_pan_tracked_core_readable` | thumbnail | PASS | The adult subject's face, hairline, torso, hands, and trolley-mounted mechanism remain readable while the archive wall is motion-softened. |
| `vo_capture_pan_parallel_background_streaks` | both | PASS | Shelves and wall lights stretch mainly in parallel horizontal bands along the implied left-to-right trolley travel. |
| `vo_capture_pan_secondary_motion_plausible` | both | **FAIL** | Ribbon, brass gears, trolley wheels, hair, and hands are largely frozen or merely depth-softened; no independently readable directional local or rotational blur survives. |
| `vo_capture_pan_single_motion_vector` | native | **FAIL** | The background supplies a left-to-right streak vector, but missing secondary-part blur leaves no independent local cue corroborating that same vector. |
| `vo_capture_pan_not_shake_zoom_or_speed_lines` | native | PASS | Face and apparatus are comparatively sharp against directional environmental smear; the pattern is not uniform shake or radial zoom, and decorative speed lines are absent. |

Requesting-user judgment remains separate and has not been received (`source: not_yet_received`).

## Key artifacts and hashes

- Frozen core: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/authorial_core.json`
  - file SHA-256: `8d4ca97e6a948d4eaa25f4a6534aeaa28f5c849381559b4974f947a9012dd39c`
  - pre-assignment frozen canonical SHA-256: `07dfda9247ae3dd480369f1ae8abfb227ef9d631030ca9167844d57df34b657f`
  - generator-normalized canonical SHA-256: `67985475374a0b640a990b7697eae2e9b8314f1631b1c29bc49fbe8962e3ca01`
- Frozen intent lock: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/intent_lock.json`
  - file SHA-256: `2729b9b52d7dac0d319f8b92676c4fd316fc29587af353279d979b70789f5e4c`
  - pre-assignment frozen canonical SHA-256: `62efc1e553be7320ec29797a41aaab50ee178c16e63f422ea78dc9d7c9881864`
  - generator-normalized canonical SHA-256: `7686c94c39b50342f573e75dc679ee4c5ab504f1a2cbfc79c01eeab501d225c8`
- Candidate pack: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/candidate_pack.json`
  - file SHA-256: `73e67f04cdbd5db3a27fb7e88a9158b9b84e3b50c9318e8b7b921fcbc3782225`
  - canonical SHA-256: `122b8269fba3b4a060c6844a85a0dd68f1615a23832974ba869943ab5e6fbe96`
- Composed prompt: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/composed_prompt.json`
  - file SHA-256: `81afce3a1b29191f5db3286d669b3673285ecbe3675432c16f62902e76d07d39`
  - prompt UTF-8 SHA-256: `a23eb509b8a56b0ecb73d3267027025a56099508481e3164535b1265952c61d7`
- Runtime request: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/image_render_request.json`
  - file SHA-256: `d16ce2d6cab1b156a0647f22a212bf459f3d7133bb84f957de1a307230689452`
  - runtime prompt UTF-8 SHA-256: `fb2655112552e2e3656def10dbb4706b61775d1ac77da5cfac23073be7cf0aaf`
- Saved native image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/generated_images/quiet-archival-mechanism/arm-01r.png`
  - SHA-256: `91ebf30df80f0a5fda36bd97afe56c2e2c10e697ab171320578fbde382b0863e`
- Pixel review: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/moe_render_review.json`
  - SHA-256: `b7378a3d89f0a34c02880c01ff3e6b31e7fc2bce2d68a83a773e7b5392f7ab50`
- Pixel-review audit: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/moe_render_review_audit.json`
  - SHA-256: `27067cb89de83555d5df8c5a7c9014b889c5a4549f4d83dd4d09125c7da99eb3`
- Arm-local ledger: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/runs/image_runs.ndjson`
  - SHA-256: `e2cb55d88c968465f87dfaa6c8b8c353ca2d96eb597dbf8b81a20e841e7da828`
- Independent manifest: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/run_manifest.json`
  - contract: `photo-independent-run-manifest/v2`
  - SHA-256: `47c737202b7fe66493455fd301be436432549156c21fb908222054e185cd5270`
- Complete artifact hash map: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/artifact_hashes.json`
  - SHA-256: `44cec3996b1b6bb5770dcd79e62d051e6261fb3631253c236dd3c0711dd95253`
- Evidence-layer boundary record: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/evidence_boundaries.json`
  - SHA-256: `7181b31033f079b4684b681f5cff3b5250f0199c3bfd6a0a8542afa54e3e565f`

Post-core binding-only adjustments are recorded in `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-01r/postcore_binding_amendments.json`; neither the frozen core nor the intent lock changed.
