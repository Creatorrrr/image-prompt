# HAREM independent render arm

## Outcome

- Overall technical verdict: **PASS** (`visual_technical_qualified_user_judgment_pending`).
- Candidate-pack/composed preflight: **PASS** with no blocking failure. The 185-word prompt is five words above the default 180-word concise target but below its 186-word evidence-adjusted ceiling; the remaining warnings only note anchor prose that was intentionally written by the agent.
- Exact runtime-input audit: **PASS**, one attached `adult_appearance_reference`, exact reference hash verified, and pack negative bytes preserved.
- Generation: **one** independent `native_imagegen` call; a concrete 1024 x 1536 PNG was saved locally.
- Pixel qualification: **5/5 hard gates PASS** at their declared thumbnail/native scales; no partial status was used.
- User aesthetic judgment: **pending**. `representative_eligible` is therefore false even though `technical_qualified` is true. The render-review command returns nonzero at this terminal user-judgment boundary, not because of a schema or pixel-gate failure.
- Reference boundary: the attached portrait was used only for visible adult appearance cues. This arm makes no identity, same-person, biometric, protected-trait, or preference claim.

## Frozen inputs

| Artifact | SHA-256 |
|---|---|
| `request_envelope.json` | `d621318af6d10e85332f08a3c180749ef531a6bfa65891eed37de80d632cbcbf` |
| `authorial_core.json` raw file | `8a5b1442a4dad31ed49956e2ea59336fdd1ea9184ee741bb8a61f4acfee3cac0` |
| normalized authorial core | `f62f42352d5b067eb693540be0c25a2cb9436bd1ac7461cfd70aeb4936a0bd07` |
| intent lock | `7a9535a11d5fe349e4ff8b3fd026882e8bcf4e6a79f76b69a4f7430783b93602` |
| repaired/frozen `visual_intent.json` raw file | `f68beeeb800c28d9f4733e31776bf0434db1bd869de802e03b5fe12e274db846` |
| normalized visual intent | `4a026c07e8e2d9bfa1802fc2986b4e2838909c36fa9cbc480b9e627ca7aff964` |
| adult appearance reference | `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea` |

## Candidate-pack use

- v6 pack: `d44ca1d684af808b`; file SHA-256 `2ba130c4b221369744a03a43f48b716a020d91d80d0069b645c956fa054c1b1e`.
- Required visual profile: `gathered_ankle_voluminous_trouser`.
- Transformed optional candidates:
  - `slot:shot_scale:full_length_body_shot` -> open `framing` dimension.
  - `slot:light_shape:diffused_ambient` -> open `lighting` dimension.
- Optional `kuudere` and `medium_native_glitch` visual concepts were explicitly rejected and contributed no prompt or review duty.

## Pixel gates

| Gate | Scale | Result | Pixel-grounded observation |
|---|---|---|---|
| `vo_summer_harem_gathered_waist` | thumbnail | PASS | One dense gathered waistband releases a large olive fabric mass into two legs. |
| `vo_summer_harem_roomy_seat_crotch` | both | PASS | A deep loose central drape and roomy upper seat/crotch remain clearly below the waistband. |
| `vo_summer_harem_hip_thigh_volume` | both | PASS | Both hips and thighs keep pronounced mass and multiple loose folds. |
| `vo_summer_harem_two_gathered_cuffs` | native | PASS | Both narrow elastic-gathered cuffs are separately visible above the clear sandals. |
| `vo_summer_harem_not_wide_balloon_jogger` | native | PASS | Two-leg bifurcation, dropped crotch volume, longitudinal fold convergence, and visibly ruched paired cuffs exclude the declared straight-wide, smooth-balloon, low-volume-jogger, uncuffed, and skirt-like substitutes. |

## Artifacts

- Final image: `generated.png`, SHA-256 `5b3ed5999ff7dcb0d71020fe840c51e4a5e7bdd0c1a7fb97c6eaf7c7df6eb7db`.
- Thumbnail inspection: `thumbnail.png` (256 x 384).
- Native garment crop: `native_lower_body.png`.
- Prompt artifacts: `candidate_pack.json`, `composed_prompt.json`, `final_prompt.txt`, `composed_audit.json`.
- Runtime artifacts: `runtime_request.json`, `runtime_audit.json`.
- Pixel artifacts: `pixel_review.json`, `pixel_review_audit.json`.
- Independence provenance: `run_manifest.json`, `image_runs.ndjson`; one image call and `cross_arm_inputs_used: false`.
