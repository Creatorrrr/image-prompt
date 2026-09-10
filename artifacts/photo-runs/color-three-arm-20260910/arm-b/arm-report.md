# Arm B — planetarium projectionist

**Promoted hard-gate result: FAIL (4 visual gates failed, 5 embodiment gates passed). Full-scene result: FAIL. New-data adoption coverage: 2/3.** One reference-based native image was generated and preserved; no retries were made. User preference remains pending.

## Frozen independent setup

Seed `1361614120` selected an overnight planetarium projectionist aligning a brass star projector from five independently authored scene options. The attached portrait was viewed and its hash verified. The 223-word baseline and v3 authorial core were frozen before candidate, profile, reference-contract or script access. Only this arm’s artifacts were used; no sibling output or previous run supplied the scene or prompt.

Envelope file SHA256: `c032fea62b9862ae51ae925c915fcbcc709b71b4862951f5420aecad010357b0`.
Baseline SHA256: `e31fe1f4b51ec9eb0872df8a40150ba37f413b52f6aa4f8ad2cabd5bda95d7f9`.
Canonical core SHA256: `2d29fa8af94e899a6c19c70fc7fa090268b55f73a612f72a16ca3f68732a6bf8`.
Intent-lock SHA256: `ace6802e200a51898ed2d4b6995820b863cdd1c03b0f18b6094a05ff55bc441f`.

## Actual candidate exposure

Both real semantic v6 retrieval attempts are retained in `retrieval-v1` and `retrieval-v2`. The second followed the coordinator’s new-data prerequisite/index refresh, keeping the baseline and core unchanged. Both produced the same public pack `1785200558ae16a5`.

There were **zero newly added color slot candidates and zero bundles** in either pack. The optional visual profile surface exposed exactly `cr_cross_color_light` and `cr_colored_rim`. Both complete contracts were read and selected, promoting four color gates. **Background Color Wash was not exposed or adopted**; its emerald dome realization comes solely from the independently authored baseline. Therefore the image cannot qualify adoption of all three newly added data relations.

## Prompt and runtime verification

The 311-word composed prompt preserves all anchors and baseline text. It adds exact evidence for the two exposed profile contracts and two open-dimension decisions: eye-level 50mm camera and a triangular eyes/calibration-plate/hand composition. All sampled creative candidates were explicitly rejected. Composed audit PASS and exact runtime/reference audit PASS; composed warnings only describe preserved free-authored intent lacking candidate coverage. The supplied reference file was attached through `referenced_image_paths`.

The native tool `image_gen__imagegen` completed one call. Its concrete returned file was copied into `generated_images/planetarium-attempt-1/image.png`; original retained. `image_runs.ndjson` and `run_manifest.json` record run `c897bd44fcaa3b7a` and actual call count 1. Ledger success means generation succeeded, not scene fidelity. There is no repair lineage, so the separate repair-only audit does not apply.

## Pixel results

The saved 1086×1448 image and a 288×384 review thumbnail were inspected.

| Check | Result | Image evidence |
|---|---|---|
| Selected cross-color profile, both gates | **Fail** | Final prompt scopes receiving light to the same face/black blouse, nose and blouse folds. Cyan face partition and amber blouse footprint are absent or unclear; sleeve/hair success does not satisfy those owners. |
| Selected colored-rim profile, both gates | **Fail** | Magenta hair contour is clear, but the declared far shoulder lacks an assessable distinct magenta rim. Hair-only realization is partial and fails both full-scope gates. |
| Five embodiment gates | Pass | Connected arms, reachable knob grip, left hand console support, coherent torso and assessable contacts survive. |
| Strict frozen cross-color scene | **Fail** | The face is largely neutral/warm, with no clear cyan cheek or cyan/amber central transition; blouse amber is weak. Sleeve/hair success cannot replace the baseline’s same-face-and-blouse relation. |
| Strict frozen magenta hair-and-shoulder rim | **Fail** | The hair contour is magenta, but the shoulder is primarily cyan; both specified receiving regions do not clearly share the magenta rim. |
| Emerald background wash | Pass, supplemental only | A broad emerald curved dome sits visibly behind the subject; this was not data-adopted. |
| Reference appearance | Pass | Similar facial configuration and long dark wavy hair survive the changed viewing angle; this is appearance comparison, not identity verification. |
| Focus-knob event | Pass | Right fingers grip the brass knob, left hand rests on console, and gaze follows the raised constellation plate. |

The revised exact gate audit reports **4 failed visual gates and 5 passed embodiment gates**, `technical_qualified: false`, and `failed_technical_hard_gates`, with zero schema failures. The CLI exits nonzero because technical gates fail. All four color gates explicitly require judging declared owners and scope; the initial review incorrectly treated partial sleeve/hair success as a generic profile pass and moved the missing owners into supplemental checks. That interpretation is withdrawn. The initial review, audit and report remain in `initial-review-v1/`; the current review enforces the unchanged final prompt scope. `partial_is_fail` applies within each promoted gate, and supplemental observations do not override those failures.

There is no old-data control image and no causal improvement claim. The result demonstrates two exposed optional contracts can be composed and submitted to rendering, but their declared owner-specific pixel relations fail. It does not demonstrate complete target fidelity, all-three data adoption, or user acceptance. The image SHA256 remains `b5e213aff5745227fe8e6c33c1863b4c75677428936a0ad315f0304a56f46d38`; no image calls were added during review correction. Generation ledger/manifest status remains success for the completed tool call; the supported schemas have no general visual-review status fields. `run-review-state.json` binds their unchanged hashes to the corrected review and failed gate IDs.
