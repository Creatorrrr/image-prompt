# arm-04 — aeolian dune wind structure

## Outcome

Technical verdict: **PASS**. All 5 target gates and all 5 shared gates pass in the same saved image. User aesthetic preference and user-perceived resemblance remain **pending**.

- Output: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-04/render.png`
- SHA-256: `8b12f6a1897c2481c5cc7b9eaac5d7dcf0297602d56be8b90b8362fa6e996bf9`
- Dimensions: 1672 × 941 PNG
- Tool: built-in `imagegen`, new generation with one appearance reference
- Actual image-tool calls: 1
- Semantic/pixel retries after the call: 0
- Ledger run: `6484acf9b53c4754`
- Prompt/runtime ID: `f0117158903986ac`

## Independently randomized concept

Seed `1735715048` selected a fog-fed coastal barchan field at dawn, a crosswind pulse carrying grains over a connected dune ridge, an adult documentary field traveler with a saffron wind streamer, and an oblique 28 mm environmental frame. The main dune—not the portrait—owns the central and right frame.

The authorial baseline and scene were frozen before project assets or other arm results were read. The first core file was rejected only because `wardrobe` and `props` were unsupported open-dimension enum values. It is preserved as `authorial_core.preflight_rejected.json`; the validated core removes only those two enum names and leaves all semantic and prompt bytes unchanged. This mechanical normalization is documented in `core_schema_fix.json`.

## Candidate-pack and contract evidence

- Validated authorial core: `2e4fa27c4c274670ebac31dc266ad91dcb9168c62cc9e41237c3f85fbbffa810`
- Intent lock: `bbdfb35262b60c7603e576145c947f75e2425df124c614c813e25ca102e8f3e8`
- Final v6 pack: `03c24830e4d656cc`
- Post-core recipe diagnostic maps the assigned keyword to exactly one mixin, `풍성사구 과정`, and to the expected seven canonical slot IDs. Canonical existence and route evidence are in `mixin_activation.json`.
- v6 intentionally withholds selected locked non-open singleton slots from some public pack surfaces. No pack JSON was hand-edited and no invented request concept-lock was used. The final pack uses the exact recipe-derived post-core soft-anchor setup.
- Exactly one hard profile is active: `aeolian_dune_stoss_crest_slipface_transport`.
- Four public recipe candidates were actually chosen: dune-process aesthetic, ripple/stoss/slipface surface, stoss–crest–slipface composition, and near-ground sand drift. Three are transformed only through open dimensions; the weather candidate has its own authorial interpretation.
- Composed audit: PASS, with only advisory prompt-budget and free-description coverage warnings. The 262-word prompt remains below the blocking 320-word limit.
- Runtime audit: PASS. Exact composed prompt, negative bytes, intent-lock hash, and the attached reference path/hash/role are bound.

## Pixel review

| Gate | Scale | Result | Observable evidence |
|---|---|---:|---|
| broad gentle stoss slope | thumbnail | PASS | The illuminated left face is much longer and shallower than the right lee face. |
| continuous dune crest | both | PASS | One uninterrupted diagonal ridge separates the two faces. |
| steep lee slipface | both | PASS | A darker smooth steep face descends directly from that ridge. |
| aligned ripples/transport | native | PASS | Fine parallel ripples and short streaks remain individually legible across the stoss side. |
| non-inference | native | PASS | The reading comes from one connected asymmetric dune body, not dust, flat texture, or a symmetric pile. |
| one saved image | both | PASS | Thumbnail and native inspections resolve to the same render SHA-256. |
| environment primary | thumbnail | PASS | Dune geometry dominates; the person is a smaller left-side scale cue. |
| reference appearance continuity | both | PASS | Visible adult presentation, general facial appearance, long dark softly waved hair, and natural skin continuity survive. |
| reference non-occlusion | both | PASS | The subject overlaps neither the main crest nor the required slope/ripple relations. |
| photographic coherence | native | PASS | Perspective, crosslight, wind direction, anatomy, notebook/fabric contact, materials, and scale read as one capture. |

The visual-obligation review auditor reports `technical_qualified: true`, five required hard gates, no failed gates, and no schema failures. Its process exits nonzero only because representative/user judgment is deliberately pending; it does not negate the technical PASS.

## Reference and independence boundary

The attached portrait was used only for general visible adult appearance guidance. This run makes no biometric identity, same-person, protected-trait, health, attractiveness, personality, nationality, ethnicity, or social-status inference. Source wardrobe and jewelry were not treated as requirements.

No other arm prompt, core, pack, generated image, review, or message was used as an input. `run_manifest.json` records `cross_arm_inputs_used: false` and `image_call_count: 1`.

## Preserved setup failures

Preflight-only failed setup artifacts were retained rather than hidden: a no-mixin pack, a direct forced-set pack that did not preserve the v6 route surface, and two partial soft-anchor routing scaffolds. None was composed or rendered. Their hashes and reasons are listed in `artifact_hashes.json`.

## Primary evidence files

- `candidate_pack.json`
- `composed_prompt.json`
- `composed_audit.json`
- `render_request.json`
- `render_request_audit.json`
- `pixel_review.json`
- `visual_render_review_audit.json`
- `run_manifest.json`
- `image_runs.ndjson`
- `artifact_hashes.json`
