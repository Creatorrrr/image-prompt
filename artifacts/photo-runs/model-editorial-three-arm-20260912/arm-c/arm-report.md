# Arm C — observatory jewelry campaign

Overall result: **FAIL under partial_is_fail**. The image was generated and locally saved, but the new model/editorial data was never exposed in this arm's candidate pack, so this is not evidence that the new data improved or survived image generation. The frozen photographic scene also fails several declared spatial and product requirements.

## Independent randomized design

Agent-owned design seed: `2026091203` using Python `random.Random`. The full choice pools and selections are frozen in `randomization.json`. Selected scene: an observatory instrument room at blue hour; a sculptural silver cuff with oval green cabochon; the adult reference-based subject lifts a lightweight meteorite specimen tray; neutral softbox with black flags. The topic and detailed staging are agent-owned, while `source_request` preserves the coordinator-frozen raw requester message unchanged.

The reference was inspected before core freeze. Visible comparison anchors are soft oval face, dark brown almond-shaped eyes, fine straight nose, full rose-colored lips and long dark center-parted waves. The scene explicitly stages one 28-year-old adult woman. Appearance comparison does not authenticate identity.

Target keywords: product-led jewelry campaign, jewelry hero shot, sculptural silver cuff, model portrait, editorial environmental staging, product contact, controlled specular highlights. The prepack core, embodiment review, test case and hashes were frozen before candidate/registry/reference-script inspection. No other-arm inputs were used. The authoritative source snapshot was verified afterward with zero changed files.

## Data exposure and adoption

Single semantic v6 pack: `c680d861abb9979f`; generator seed `4489987442097853083`, creativity `0.5`.

- New `mep_` slot/profile candidates exposed: **0**.
- Bundles exposed: **0**.
- Optional visual profiles exposed: `deliberate_underarm_salience`, `medium_native_glitch`. Both rejected as mismatches.
- New model/editorial candidates selected: **0**. No profile injection and no second pack.
- Existing candidates selected after full detail read: `slot:lighting:softbox`, `slot:subject_framing:upper_body_framing`.
- All creative augmentation samples rejected; `chosen_visual_concept_ids: []`.

The existing softbox became the literal clause “Shape the silver reflection into a long pale rectangle bounded by a darker edge”; the framing candidate became “Keep a narrow margin below both elbows so the lower frame reveals the full tray support”. No new optional profile was selected, so no new model/editorial all-of obligation or profile pixel gate was activated. Product legibility remained a frozen required typed assertion and was independently reviewed against the prepack test.

## Audit and actual output

Composed audit: **PASS**, with four warnings recording that frozen intent phrases were realized through free description. Exact runtime audit: **PASS**, unchanged negative bytes and actual portrait attachment verified. The native request was read directly from `render_request.json` and forwarded as the exact audited prompt; no extra runtime prose was added.

Exactly one native `image_gen` call; zero retries, zero API calls. Concrete returned output was copied without editing to:

`/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-c/generated.png`

Image SHA-256: `979cedbc11d07134aad5f6cef4fa0a53eff54311770f7287725e45fd87bd0396`.

The arm-local ledger and independent v2 manifest were recorded successfully. Their `status: success` refers to successful image delivery, not pixel qualification. The original returned file remains intact.

## Pixel findings

Reviewed the complete photograph and native 1086 × 1448 image.

| Frozen requirement | Result | Image evidence |
|---|---|---|
| Reference appearance | Pass with comparison limit | Face outline, nose, lips and dark waves strongly resemble the reference. Downcast eyes limit iris/eye-aperture comparison. |
| One adult photographic subject | Pass | One adult-looking woman is visible. |
| Product hero with every construction component | Fail | Silver band, green dome and bezel are crisp; the open-ended gap is not unambiguously exposed. Face and hair dominate the hierarchy. |
| Cuff above tray rim with clear contact | Fail | Skin/metal boundary is clear, but cuff is below the tray rim. |
| Connected plausible hands and all fingertips visible | Fail | Joint chains and two-handed support are plausible; overlapping fingers beneath tray prevent assessment of every fingertip. |
| Tray lifted only a few centimeters | Fail | Tray is raised to lower-chest height, substantially above tabletop. |
| Cuff/eye detail and material color | Pass | Useful sharpness, controlled broad silver highlight and retained green body color. |
| Observatory at blue hour | Pass | Telescope/instruments and blue window are present. |

Exact five-gate embodiment review: body ownership and joint chain pass; support/state, contact/space and visibility/projection fail. The review auditor has **zero schema failures** and reports `failed_technical_hard_gates`; its nonzero exit is the expected failed-evidence result. No generic repair contract exists for this initial attempt, so no repair gate set was fabricated.

The qualitative preflight underexamined the coupled geometry of a palm supporting a shallow tray while the cuff was supposed to sit above its rim. That tension was agent-authored before retrieval. Its missed detection is a preflight limitation; it must not be attributed to the new keyword data or concealed by attractive facial rendering. Bright green jewelry and a polished portrait do not establish the missing construction/contact/product-hierarchy components.

User judgment remains `not_yet_received`. No overall image pass, new-data causal improvement, or user preference claim is made.

## Evidence files

`prepack_freeze.json`, `randomization.json`, `test_case.json`, `authorial_core.json`, `embodiment_review.json`, `candidate_pack.json`, `composer_view.json`, `candidate_details.json`, `adoption.json`, `composed_prompt.json`, `composed_audit.json`, `render_request.json`, `runtime_audit.json`, `native_output.json`, `generated.png`, `render_review.json`, `render_review_audit.json`, `pixel_test_results.json`, `image_runs.ndjson`, `run_manifest.json`, `source_snapshot_verification.json`.
