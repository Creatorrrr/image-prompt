# Arm 01 — robbery forced-property-transfer qualification

## Result

- Pixel qualification: **FAIL** under `partial_is_fail`.
- Image generation: successful, exactly one built-in `image_gen` call, no retry.
- Composed prompt audit: PASS (`quality_status: warn` only for the 210-word advisory budget and optional visual-proposition omission).
- Render request audit: PASS.
- Pixel-review schema audit: valid review with `failed_technical_hard_gates`.
- Failed profile gate: `vo_crime_robbery_transfer`.

The generated still clearly shows a distinct adult offender, a distinct adult courier, a raised crowbar threat, and the courier's initial control of the red case. It does not show the same case moving into offender control: the offender's lower hand points toward or lightly touches the case rather than gripping and pulling it, while the courier continues to hug the case against her torso.

## Random complex concept

Seed `695725796` selected a declared-fictional near-future robbery in a glass desert-observatory tram station during violent sleet, with a rare-map courier, stranded commuters, a red leather case containing a brass astronomical chronometer, a 28 mm environmental frame, sodium-vapor light, and red signal beacons. The supplied portrait guided only the visible adult appearance of the secondary station investigator pressing an alarm.

## Exact gate outcomes

| Gate | Result | Pixel evidence |
|---|---|---|
| `vo_crime_robbery_roles` / `R1_distinct_adults` | PASS | Offender at right and courier at center remain visually distinct at 384×256. |
| `vo_crime_robbery_coercion` / `R2_directed_force_or_threat` | PASS | Raised hooked crowbar and forward reach visibly threaten the courier. |
| `vo_crime_robbery_property_origin` / `R3_initial_holder_control` | PASS | Courier hugs the red case and grips its top handle at native scale. |
| `vo_crime_robbery_transfer` / `R4_same_property_transfer` | FAIL | Offender does not visibly grip or pull the case; transfer direction is absent. |
| `C1_reference_appearance` | PASS | Secondary investigator retains long center-parted dark wavy hair, oval face, dark eyes, and softly arched brows. |
| `C2_supporting_role_secondary` | PASS | Investigator stays at the far-left alarm and does not obscure the robbery. |
| `C3_relation_thumbnail_readability` | FAIL | Actor, target, threat, and case read, but the transfer result does not. |
| `C4_relation_native_detail` | FAIL | Ownership is clear; offender grip and transfer path are not. |
| `C5_clean_delivery` | PASS | No watermark; incidental station signage is integrated and non-disruptive. |

## Artifacts

- `request_envelope.json`, `authorial_core.json`, `visual_intent.json`
- `test_case.json`, `pixel_rubric_precommit.json`
- `candidate_pack.json`, `composed_prompt.json`, `composed_prompt_audit.json`
- `render_request.json`, `render_request_audit.json`
- `render_native.png` (1536×1024), `render_thumbnail.png` (384×256)
- `pixel_review.json`, `pixel_review_audit.json`
- `run_manifest.json`, `run_ledger.ndjson`

Generation success in the ledger records tool execution only; it does not override the failed pixel qualification. User preference remains unscored and pending.
