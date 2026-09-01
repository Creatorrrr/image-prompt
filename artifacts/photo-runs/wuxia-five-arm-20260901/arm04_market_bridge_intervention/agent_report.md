# Arm 04 — market bridge intervention

## Outcome

Exactly one built-in `image_gen` call was made with Image 1 attached through `referenced_image_paths` as an `appearance_reference`. The tool generated a new scene rather than editing the portrait. The returned PNG was copied into this arm and preserved even though the strict pixel qualification failed.

- Tool: `built_in_image_gen`
- Image-call count: `1`
- Retry count: `0`
- Saved image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/wuxia-five-arm-20260901/arm04_market_bridge_intervention/render_attempt_01.png`
- Native dimensions: `1536x1024`
- Image SHA-256: `9fd6a8f38ae4cef60f368ecd07bee802d01fc11a35a538c346a5a46ef7ec98b5`
- Ledger run ID: `5b5271d514c44eaf`
- Runtime prompt ID: `e6de26fb1d069c13`

## Frozen-input verification

- Raw `request_envelope.json`: `e50589162562491e876d702cbe9c8ab0e68d08993f2471aede2d3f61b4ad3ae9` — matched the coordinator value.
- Raw `authorial_core.json`: `e49f74075a613616eb593e80894a335ab650b91dfc03dd3c9e8f6b1d94b76642` — matched the coordinator value.
- Candidate pack: v6, pack ID `132dce81495a566c`, canonical core `64f16659d25fbb836b4067b9568735b67e7103f495cebdd0b138474e33f8d05b`, intent lock `5f24680c110ce3b6f39eecd865bf00ea08026d1c3a94d14271a13c188832c03d`.
- Appearance reference: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea` — matched the coordinator value.

## Prompt and runtime audits

- `composed_prompt.json`: blocking audit `pass`, no failures. Quality status is `warn` because the 262-word prompt exceeds the default 180-word concise target, while remaining within the 263-word evidence-adjusted advisory ceiling and the 320-word absolute limit.
- Optional visual concepts selected: none.
- Creative candidates transformed: none; all six sampled candidates were explicitly rejected as unnecessary or harmful to the hard event geometry.
- Effective visual contract: `75dda4aeeded5e68c92fcbf2a22fe9325114b69cefc73526ae1e48ddc10a6d2d`.
- `render_request.json`: exact-input audit `pass`; negative bytes, intent lock, appearance-reference path/hash/role, and runtime/composed boundary all matched.
- Generic `photo-image-render-review/v1`: not applicable because this pack has no `render_repair` contract.

## Strict pixel review

The output was inspected at thumbnail (`384x256`), full native (`1536x1024`), and a native-scale contact crop (`1100x700`). The review contains exactly the five `vo_*` gates. Partial evidence is recorded as failure.

| Gate | Status | Image-grounded result |
| --- | --- | --- |
| `vo_wuxia_xia_three_roles` | fail | Three adults are distinct, but the aggressor is clipped by the left/bottom edges and the courier's extended arm is clipped, so the figures are not all complete. |
| `vo_wuxia_xia_directed_threat` | fail | The aggressor's face, torso, and polearm aim toward the central intervener; the weapon line does not visibly continue toward the courier. |
| `vo_wuxia_xia_interposition` | fail | The intervener is spatially between the adults and blocks a weapon, but the aggressor-to-courier threat line is not explicit; the same-line condition is only partial. |
| `vo_wuxia_xia_consequence` | pass | A sword-and-polearm crossing contact and the courier moving toward the tied boat make a delayed threat and escape opening visible. |
| `vo_wuxia_xia_not_appearance_inference` | pass | Crossed weapons, the planted central blocker, and the courier already moving into the boat establish event consequence beyond costume or face alone. |

`audit_moe_render_review.py` validated the artifact with zero schema failures and returned `qualification_status: failed_technical_hard_gates`, `technical_qualified: false`, and `representative_eligible: false`. Its nonzero exit is the expected result for the three failed gates, not an auditor/schema error.

## Appearance-reference observations and evidence boundary

At native scale, the intervener visibly carries long near-black wavy center-parted hair, a softly oval face, brown eyes, mostly straight brows, and natural lips. The lips are slightly parted, so the requested closed-lip detail did not survive exactly. These are supplemental visible-appearance continuity observations only; they are not biometric identity, ethnicity, personality, attractiveness, or same-person claims.

Prompt and runtime audit passes establish contract/text/reference preflight only. The pixel review establishes this reviewer's scale-specific observations only. Generation success in the ledger does not mean visual qualification. No requesting-user preference or acceptance judgment has been received or claimed.

## Artifacts

- `composed_prompt.json` and `composed_prompt.audit.json`
- `render_request.json` and `render_request.audit.json`
- `render_attempt_01.png`, `render_attempt_01_thumb.png`, and `render_attempt_01_native_contact_crop.png`
- `moe_render_review.json` and `moe_render_review.audit.json`
- `run_manifest.json` (`photo-independent-run-manifest/v2`)
- `run_ledger.ndjson`
