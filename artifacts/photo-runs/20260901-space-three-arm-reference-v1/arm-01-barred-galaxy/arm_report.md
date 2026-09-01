# arm-01-barred-galaxy report

## Outcome

- Package: **PASS** — `photo-candidate-pack/v6`, pack `138b16f55bb142a8`, request-scoped `barred_spiral_galaxy_structure` hard binding active.
- Prompt: **PASS** — 180-word composed prompt, zero blocking failures; quality status remains `warn` only because the generator labels the five preserved intent anchors as candidate-uncovered despite literal prompt coverage.
- Runtime request: **PASS** — exact `photo-image-render-request/v2` audit, one reference file and byte-exact negative binding.
- Render: **PASS** — native imagegen called exactly once, saved PNG reviewed at native and thumbnail scales, all common and profile gates passed in the same saved image.
- User preference: **not_yet_received** — kept separate from technical qualification.

## Independence and provenance

- Arm: `arm-01-barred-galaxy`
- Random seed: `2253228305`
- Variation key: `orbital_observatory_control_room`
- Authorial core canonical SHA-256: `1c896a12e14d38061e3b09773dda64c9a042b5f2a554295e9f93f3cadcd39438`
- Intent-lock canonical SHA-256: `2f8c0233cd27ecce6cabb4cfded4ffa81653781cf11812032e8c3d1ca94ba9fd`
- Visual-intent canonical SHA-256: `c4610be51b7e34cbcf32a7b1fa0d6fd4b447ebf0a98a7cf861b0785e447e8398`
- Effective visual contract SHA-256: `f42bb5526451f93048c5604a1b81e1ea6655624e27658f17b50fad088d46ac32`
- Cross-arm inputs used: `false`
- Image calls: `1`; retries: `0`
- Conflicting `galaxy_structure_observation` interacting-galaxy cluster: explicitly rejected because its two bodies, tidal bridge, and tails would replace the locked single barred-spiral morphology.

## Saved render

- Path: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-space-three-arm-reference-v1/arm-01-barred-galaxy/render.png`
- SHA-256: `76c930ce5dc6eb067dd590feef898167dd707e57586dbe27a34e66dd30587a84`
- Dimensions: `1536 x 1024`
- Native tool source path: `/Users/chasoik/.codex/generated_images/01a05c58-85e1-71c0-acf2-3f2495e8f025/exec-8229346f-e117-475b-b4d1-c19f2c34cbfe.png`

## Pixel gates

| Gate | Status | Evidence summary |
|---|---|---|
| `reference_visible_appearance_continuity` | pass | Visible face-shape, eye-aperture/spacing, lower-face, hairline, and long dark wavy hair cues continue; no identity claim. |
| `adult_age_continuity` | pass | Subject remains visibly adult without doll-like reshaping. |
| `gross_structural_coherence` | pass | Body, hand, control, console, display, and spatial relations are coherent. |
| `required_interaction_contact` | pass | Fingers and thumb visibly grip the physical telescope-control knob. |
| `unrequested_text_artifacts` | pass | Galaxy meaning is carried by morphology pixels, not side alert copy or tiny console glyphs. |
| `vo_space_barred_bulge` | pass | One central luminous bulge anchors the disk. |
| `vo_space_barred_bar` | pass | An elongated stellar bar crosses the bulge. |
| `vo_space_barred_arm_attachment` | pass | Two dominant arms begin at opposite bar ends. |
| `vo_space_barred_shared_disk` | pass | Bulge, bar, and arms form one coherent disk. |
| `representation_false_color_multiwavelength` | pass | Blue, pink, and warm analytical mapping reads as a false-color scientific display. |

Failed gates: none. Partial results were not promoted.

## Key artifacts

- `authorial_core.json` / `authorial_core.sha256`
- `visual_intent.json`
- `candidate_pack.json`
- `candidate_rejections.json`
- `composed_prompt.json` / `composed_prompt.audit.json`
- `image_render_request.json` / `image_render_request.audit.json`
- `render.png` and review derivatives
- `self_review.json` / `self_review.audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
- `imagegen_result.json`

Prompt and runtime audit PASS establish input integrity only. The pixel decision above comes from direct inspection of the saved render, while requesting-user preference remains pending.
