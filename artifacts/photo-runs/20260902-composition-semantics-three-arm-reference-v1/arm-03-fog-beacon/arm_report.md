# Arm 03 — Fog Beacon Qualification Report

**Bounded outcome: FAIL at strict rendered-pixel qualification.** Package, composed-prompt, and exact runtime-request audits passed; the single authorized image call succeeded. Native and thumbnail review passed 9 of 12 derived hard gates, but the visible rightward walking vector was not established, so all partial motion-room evidence was treated as failure. Requesting-user judgment has not been received.

## Package

- Arm: `arm-03-fog-beacon`
- Candidate pack: `photo-candidate-pack/v6`, pack ID `f457bf67901ba34a`
- Pack generation: creativity `0.5`, seed `902003`, exactly one pack written with `--output-file candidate_pack.json`
- Pack SHA-256: `fbf57e27b3861f4bde27fe5af01f998a0cfc949fa7f225af1bb83124d1d1d0a2`
- Governing core SHA-256: `63b3a6d5f7909a16e67b0ff904b6c0862b641fe42b5afe666dfef9ea419d3275`
- Intent-lock SHA-256: `2c4b15ffeda63d709fe0ee8fe279a012d8e114c50633f2929e28c5c8b8fb34ee`
- Active hard profiles: `subject_field_negative_space_relation`, `asymmetric_counterbalance_relation`, `look_motion_room_direction_relation`
- Optional visual concepts were explicitly left unselected; every semantic-clarification and creative-augmentation candidate received a typed decision.
- Frozen request/core/visual-intent/test-case inputs were not modified. No other arm input was read or used.

## Prompt and Runtime Preflight

- Final positive prompt: 280 English words, within the absolute 24–320-word bound.
- Every required visual-obligation evidence field is present and literal in the prompt.
- The first preserved preflight (`composed_audit.json`) failed seven minimum evidence-word checks. Those phrases were repaired before generation; no image call occurred until the final passing preflight below.
- Composed audit: `status: pass`, no failures; `quality_status: warn` only because required evidence pushes the prompt above the default 180-word concise target.
- Effective visual-contract SHA-256: `397d696d07c47d0642ff0a8ea3c66696908e350890317f58d1e488bc104a53ca`
- Runtime request audit: `status: pass`, `negative_matches_pack: true`, one verified reference.
- Reference role: `visible_adult_appearance_reference_only`.
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.
- The portrait was used only for observable adult appearance. No identity, same-person, biometric, protected-trait, health, attractiveness, personality, occupation, ethnicity, nationality, or allegiance inference was made.

## Generation

- Tool: built-in `image_gen`
- Image calls: exactly `1`
- Retry/fallback: none
- The audited runtime prompt and negative bytes were used, with the reference image attached.
- Saved result: `final.png`, 1537 × 1023 PNG
- Result SHA-256: `3ab26e43402dd544beabab6b57b6efabe38f016f1c70539f9d284e2e0568fef7`
- Arm-local ledger run ID: `3df98cca7d73120c`
- Prompt ID: `1cbdd2f5342acac2`
- Manifest: `photo-independent-run-manifest/v2`, `image_call_count: 1`, `cross_arm_inputs_used: false`

## Rendered Pixels

The image was inspected at a 320 × 213 thumbnail and at native 1537 × 1023 pixels. The exact strict gate set contained 12 gates.

Passed 9 gates:

- The adult figure is a dominant left-of-center mass.
- The small saturated red beacon visibly counterweights the larger figure.
- Pale fog and bridge distance separate the unequal weights.
- Scale and color contrast create an asymmetric equilibrium without random clutter.
- The action origin remains in-frame at lower left.
- A large contiguous low-detail fog field occupies substantial frame area.
- The dark subject contour separates from the pale field.
- The fog field strengthens first-read subject hierarchy.
- Fog retains tonal gradients, softened infrastructure, and damp material detail rather than reading as a blank crop or exposure loss.

Failed 3 gates:

- `vo_composition_room_direction_vector`: the legs and stride are cropped, the torso reads stationary, and the visible eye-line points toward the camera. Bridge leading lines alone do not prove her motion vector.
- `vo_composition_room_greater_ahead`: although large bridge/fog space lies to the right, the missing visible action vector prevents that space from being verified as ahead rather than merely background.
- `vo_composition_room_not_wrong_side`: the open field follows the bridge toward the beacon, but the only clear eye-line is cameraward and no visible action vector connects the subject to the beacon.

Review-contract audit: `schema_failures: []`, `qualification_status: failed_technical_hard_gates`, `technical_qualified: false`, `representative_eligible: false`. Because `partial_is_fail` is active, no partial motion-room observation was promoted to pass.

## User Judgment

- Source: `not_yet_received`
- No requesting-user acceptance, rejection, or preference has been inferred.
- User judgment remains separate from package/preflight success and from the strict pixel failure above.

## Arm-local Artifacts

- `candidate_pack.json`
- `composed_audit.json` (preserved initial failed preflight)
- `composed_prompt.json`
- `composed_prompt_audit.json`
- `runtime_request.json`
- `runtime_request_audit.json`
- `final.png`
- `thumbnail.png`
- `render_review.json`
- `render_review_audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
