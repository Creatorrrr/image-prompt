# Arm 05 — Desert Biaoju Qualification Report

## Outcome

The single built-in image-generation attempt completed and was preserved, but the render is **not technically qualified**. Four of the five exact `vo_*` gates passed; `vo_wuxia_biaoju_route_continuity` failed under the partial-means-fail rule.

## Frozen inputs and composition

- Request-envelope raw SHA-256 verified: `366c0e38852221e52aa00bfa1218b315707e7a85cdef2023623f6da0477fcf26`
- Authorial-core raw SHA-256 verified: `9bf2ca4d89eda3aacad34283a880bd8584e7d5a72f84cd4063c13eeca4c31d0c`
- Candidate pack: v6, pack `19c47c76a2417610`
- Canonical core: `f523eda5b1f5295808aeadf9b748135cc92bb427b275577031336adec42d177f`
- Intent lock: `7d3dc742b0b451d922c8f62b89225fb71418720819d17475aa170bd7160716bf`
- Hard profile: `biaoju_guarded_cargo_departure`
- Optional visual concepts rejected: `medium_native_glitch`, `kuudere_composed_warmth_relation`
- All six sampled creative candidates rejected because they were unnecessary or reduced visibility of the hard convoy relation.

## Audits

- Composed prompt audit: **PASS**, with advisory quality status `warn` for the 261-word evidence-heavy prompt and four already-preserved uncovered-intent notices; blocking failures: 0.
- Exact image-render request audit: **PASS**; runtime prompt ID `98f55ce90a6d0997`; reference count 1; negative bytes match the pack.
- Pixel-review artifact audit: schema failures 0; qualification status `failed_technical_hard_gates`; representative eligible: false.
- Generic `photo-image-render-review/v1`: not applicable because the pack has no `render_repair` contract.

## Generation and saved result

- Tool: built-in `image_gen`
- Image calls: exactly 1; retries: 0
- Reference role: Image 1 as `appearance_reference` only, for visible adult appearance guidance in a newly generated scene
- Saved image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/wuxia-five-arm-20260901/arm05_desert_biaoju/generated_image.png`
- PNG dimensions: 1537 × 1023
- Image SHA-256: `cbee0483139c0b53ffd344b9ae0e30e870528fc013e978554ce3b12c7cb55a76`
- Ledger run ID: `697a31648bf9fc8e`
- Prompt ID: `d1e54309b4e41c40`
- Independent v2 manifest: `run_manifest.json`; `cross_arm_inputs_used: false`

## Strict visual gates

| Gate | Status | Image-grounded result |
|---|---|---|
| `vo_wuxia_biaoju_origin` | pass | At thumbnail scale, the fortified loading-yard gate opens onto the same dusty departure-road space. |
| `vo_wuxia_biaoju_loaded_cargo` | pass | At both scales, one donkey cart visibly carries several sealed crates with taut rope and red seal marks. |
| `vo_wuxia_biaoju_escort_distribution` | pass | At both scales, armed adults occupy forward, rear, gate-threshold, and flank positions around the loaded cart. |
| `vo_wuxia_biaoju_route_continuity` | **fail** | At native scale, the cart points toward the viewer after clearing the gate while the distant road bends away right; no continuous wheel-and-hoof trace visibly bridges the yard threshold to that road. |
| `vo_wuxia_biaoju_not_convoy_or_caravan` | pass | Sealed owned cargo, coordinated armed escorts, pennants, and the escort-office gate distinguish a guarded commercial departure from a merchant-only caravan or generic wagon. |

## Appearance-reference observations and evidence boundary

The rendered captain is visibly adult and shows long near-black hair with a loose center part, a softly oval facial outline, fairly straight brows, and natural closed lips. Warm-brown eye color is not reliably resolvable at this environmental scale. These are supplemental visible-cue continuity observations only; they do not establish biometric identity, ethnicity, personality, attractiveness, or same-person status.

Prompt audit, runtime audit, saved-image bytes, pixel-gate review, and requesting-user judgment are separate evidence layers. User preference or acceptance has not been received and is not claimed.
