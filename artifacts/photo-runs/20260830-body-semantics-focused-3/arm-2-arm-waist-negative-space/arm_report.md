# Arm 2 — Arm–Waist Body-Bounded Negative Space

## Outcome

- Selected concept: **Meridian Dispute at the Abandoned Observatory**
- Selection: Python `random.Random(999609921).randrange(8)` → zero-based index `4`
- Candidate pack: `photo-candidate-pack/v6`, pack ID `42ac3b8c1c72c009`, creativity `0.65`
- Active hard profile: `body_bounded_negative_space`
- Built-in image calls: `2` (`attempt 1` generation, `attempt 2` targeted edit repair)
- Final saved image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260830-body-semantics-focused-3/arm-2-arm-waist-negative-space/attempt-2.png`
- Final image SHA-256: `7d802eb04e50eb7cc33c477ba55efcf527cd5a7d7aae68ef154d9bc4c91082f8`
- Overall technical verdict: **FAIL**
- Requesting-user appearance/acceptance judgment: **pending**

## Final pixel gates

| Gate | Scale | Verdict | Pixel observation |
|---|---|---|---|
| `vo_body_negative_space_real_boundaries` | native | FAIL | A long dark coat flap/strip makes the apparent inner edge; the second edge is not an unmistakable anatomical outer-waist contour. |
| `vo_body_negative_space_continuous_background` | both | FAIL | Pale wall is visible, but the cord and coat strip traverse the intended opening, preventing the requested uncluttered, unbroken wall patch. |
| `vo_body_negative_space_shape_legible` | thumbnail | PASS | A large triangular pale wedge remains legible at `170×256`. |
| `vo_body_negative_space_region_specific` | both | FAIL | The wedge reads as a coat-created side opening rather than a clean arm–waist interval, matching the rejected garment-cutout substitute. |

The test rule requires all four gates in one saved image. Passing only the thumbnail-shape gate is therefore a technical failure.

## Attempt history

1. `attempt-1.png` — SHA-256 `8a255f205f970352832291f074da338fe5d9dc0fa7932d86b69839fc3ad9353b`. Continuous wall and thumbnail shape passed, but the wedge could be read as a coat opening rather than real arm/waist boundaries.
2. `attempt-2.png` — targeted only at framing, composition, and camera alignment while preserving the core, face-reference role, event, pose, wardrobe, and passed gates. It enlarged the wedge but retained a garment strip and cord across the region. The two-call limit is exhausted.

Named audit mapping was regenerated directly from each request:

- `runtime_request_attempt_1.json` → `runtime_request_audit_attempt_1.json`: runtime prompt ID `39270ebce2f413b0`, `1` reference, audit SHA-256 `2462749231f3cc4bd0aa1082b76841d96817dddfc7ab6cbf1a89f9a18c99a069`.
- `runtime_request_attempt_2.json` → `runtime_request_audit_attempt_2.json`: runtime prompt ID `c7abac62c84b2462`, `2` references, audit SHA-256 `376fb31d433fa4c89bac83a614dc1ebd6d1dc40b29afdd263b7a610eaef971b3`.
- Recorder linkage: attempt 1 run ID `38c0d12fc7657152`; final attempt 2 entry `db359e18b06d7597` has `retry_of: 38c0d12fc7657152`. The v2 manifest schema does not expose `retry_of`, so it remains linked through the schema-supported ledger entry and provenance.
- Parent-merge ledger: `image_run_attempts.ndjson` contains the two schema-valid recorder rows in attempt order; SHA-256 `ec8f065ec0819769c4588e99a9ac210f66eaaaa8a9e59d2520c8e76787464e83`. Each row records only that attempt's saved output, and the second row is byte-for-byte identical to `image_run_entry.json`.

## Exact bindings and hashes

- Request envelope file: `2dd3c09d52a130f80d3e2829d9d2f5056fd7e65a5dd1831fe4f91857d25b7f0c`
- Exact request text: `2215db543ae95360539cbb06595c00c75e813b4cc2afe61abc506260d3e4a9c5`
- Canonical envelope: `8be1e20eadf7873f4a2cf92343b163fb1168ad331874ce259f9fd4246f5e51af`
- Final authorial-core file: `a784a3121422bbf6da1f49199cdff6a80c1a22176fee7a27622fa724b62bdfb7`
- Generator-normalized authorial core: `ee392217aeb1eec8c606d5d6e22605b8d94a97549ed3dc90182468ada57eabc8`
- Generator-normalized intent lock: `83f1707b32589aa783949a1f4d7b833e5ab8a910fa83fed2bf3294ebe8475945`
- Visual intent: `a48fa555211169659d9aa12b1adc0f15cf26fd455b18c3514dc81b81d176159b`
- Candidate-pack file: `86d140f3899fae65dd19d3b087cd1dc353e0d4f9cbfc797d139d7dc86f1eb221`
- Candidate-pack object canonical: `933ea124c941b189c9c8426e0638f8295bfdae2e8df551fe92908f3b6bb01890`
- Effective hard visual contract: `bd0845bca0c76a145f77ce4e2110d8912e33806d507b513cc5f1a0bb4ff2b1e6`
- Exact composed positive prompt text: `6af010444a5f583d810d640e0d2a8f811fccad740903beebd9a7c4fe12348699`
- Exact negative text: `3568104dafac50bd31d3d66edc4887da6be47005a0c5bf1ef1b9c3d85f399705`
- Attempt 1 runtime prompt: `39270ebce2f413b01e6d40c171f97138d7d312d65b0553f376fb2fa2c5bf3395`
- Attempt 2 runtime prompt: `c7abac62c84b2462fcdeb666c9a46cfda347566888dafa2cf3b746a0e17568b8`
- Final `image_run_entry.json` file: `2a581280cf2a60a6d490dad63551e16d7397eeee14ae3e3a5817478617ca0215`
- Arm-local `image_run_attempts.ndjson` file: `ec8f065ec0819769c4588e99a9ac210f66eaaaa8a9e59d2520c8e76787464e83`
- Final `run_manifest.json` file: `d7bd88d1957503036a1f5da3fa73a69aa39d2e53f11fea6018cc71cbe3399e72`
- Face reference: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`, SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`, role `facial_appearance_only`

Both composed and per-attempt runtime audits passed. The composed prompt is 190 words, within the 191-word evidence-adjusted advisory ceiling and the 320-word hard ceiling; the remaining default 180-word warning is non-blocking. Prompt/audit success is preflight only and did not override the failed pixel gates.

## Isolation and limitations

- No other arm directory or output was read or used.
- No shared source, test, profile, index, or `runs/image_runs.ndjson` file was modified.
- The initial pre-profile core and hashes were frozen before project semantic access. The first pack validation then rejected the metadata dimension `reference_appearance`; a schema-only correction renamed it to supported `reference_use` and pointed its anchor at an already-literal baseline phrase. Baseline, subject, setting, event, and visual priorities were unchanged. Initial and final hashes plus the validator error are retained in `core_hashes.json` and `provenance.json`.
- Face-reference review is limited to visible appearance guidance. This report makes no identity, ethnicity, or biometric determination.
- The pack contains no `moe_response` contract, so the moe-only render-review auditor is not applicable. Pixel qualification is recorded from direct `view_image` inspection at required thumbnail and native scales.

## Artifacts

`concept_selection.json`, `authorial_core.json`, `core_hashes.json`, `visual_intent.json`, `candidate_pack.json`, `composed_prompt.json`, `prompt.txt`, `negative.txt`, `composed_audit.json`, both runtime requests and audits, both native images and thumbnails, attempt reviews, `pixel_review.json`, `provenance.json`, `image_run_entry.json`, and `run_manifest.json` are all contained in this arm directory.
