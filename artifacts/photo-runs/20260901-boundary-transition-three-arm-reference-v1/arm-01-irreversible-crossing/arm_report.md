# Arm 01 — irreversible threshold crossing

Overall result: **FAIL / revise** under `partial_is_fail`.

The v6 candidate pack and both preflight audits passed. The built-in image generator delivered one reference-guided image in the only permitted call. The image clearly shows one adult subject crossing a circular docking collar, but the return tunnel remains visibly open and the orange Earth-horizon glow does not unambiguously prove that reentry has begun. Those two missing causal relations prevent a pixel PASS.

## Frozen test

- Profile: `irreversible_threshold_crossing_consequence`
- Assigned phrase: `visible point-of-no-return crossing`
- Seed: `910165687`
- Random concept: orbital emergency-airlock crossing from a failing habitat into a reentry capsule
- Reference role: visible adult appearance only; no identity, protected-trait, personality, or relationship inference
- Authorial core SHA-256: `bfd37f11ca67a444a2e6d9a966f6525250afc8dc6a73badffdeec0337619777b`
- Intent-lock SHA-256: `cf75362de08ded8faba5b0c4a9dea13345133d24a521f8730314ed038de38c2d`
- Visual-intent SHA-256: `bc855f1864bb3fb401431787b38a1a9b38df98aa74ccd5cd2d1e919b711aa8cb`
- Pack ID: `8d23fad358dcdf73`
- Effective visual contract: `29a5bd4f4af6527434c5c331d35b0b8cb70e0c3246f0c7f7485a2f89bc32ef8e`
- Composed audit: `pass` with advisory word-budget and uncovered-intent warnings only
- Runtime request audit: `pass`
- Image calls: `1`; retries: `0`

## Pixel gates

| Gate | Result | Image-grounded reason |
|---|---|---|
| `vo_boundary_irreversible_subject_continuity` | PASS | One uninterrupted adult body spans the ring. |
| `vo_boundary_irreversible_defined_threshold` | PASS | The circular metal docking collar is concrete and fully readable. |
| `vo_boundary_irreversible_directed_crossing` | PASS | Braced forward hand, advanced torso, and trailing legs give one inward direction. |
| `vo_boundary_irreversible_lost_return` | FAIL | Fire and torn metal are visible, but the aft passage remains open. |
| `vo_boundary_irreversible_committed_result` | FAIL | The orange band can read as sunrise; active reentry plasma is not unambiguous. |
| `C1_reference_appearance` | PASS | Adult impression, long center-parted dark wavy hair, dark eyes, arched brows, and broad face proportions survive. |
| `C2_event_hierarchy` | PASS | Subject and complete threshold remain simultaneously visible. |
| `C3_thumbnail_event_readability` | FAIL | Lost return plus downstream commitment do not read together at 512 px. |
| `C4_native_mechanism_detail` | FAIL | No closed iris, severed joint, or collapsed barrier blocks the exact path. |
| `C5_clean_delivery` | PASS | No watermark or scene-breaking accidental text is visible. |

Official pixel-review audit: `failed_technical_hard_gates`, with zero schema failures. Requesting-user judgment is `not_yet_received`.

## Artifacts

- Native render: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-boundary-transition-three-arm-reference-v1/arm-01-irreversible-crossing/render_native.png`
- Thumbnail: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-boundary-transition-three-arm-reference-v1/arm-01-irreversible-crossing/render_thumbnail.png`
- Prompt and contracts: `authorial_core.json`, `visual_intent.json`, `candidate_pack.json`, `composed_prompt.json`, `render_request.json`
- Audits: `composed_audit.json`, `render_request_audit.json`, `pixel_review_audit.json`
- Records: `test_case.json`, `iteration_record.json`, `run_ledger.ndjson`, `run_manifest.json`

No sibling-arm prompt, pack, message, image, or test result was used, and no runtime source file outside this arm was modified.
