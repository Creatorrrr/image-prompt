# arm-03-solar-flare report

## Outcome

- Package status: **PASS**. Candidate-pack `photo-candidate-pack/v6`, pack ID `722d16d39b510785`, normalized authorial-core SHA-256 `ef79c431df9819a5ae3b94c5b83fc39378068e8a131e30fd7324671a7524d91d`.
- Prompt status: **PASS**. `audit_composed_prompt.py` reported no failures. The 205-word prompt is within the 24–320 hard range and exactly at the evidence-adjusted 205-word advisory ceiling; the remaining warnings only note the default 180-word target and free-description preservation of frozen anchors.
- Runtime-request status: **PASS**. Exact `photo-image-render-request/v2` audit reported no failures, one valid reference, matching negative bytes, and runtime prompt ID `866efce93ffa4883`.
- Render status: **PASS (technical pixels)**. Native `imagegen` was called exactly once, with zero retries. The same saved image passed all 5 common gates and all 5 arm/profile gates. Requesting-user preference is `not_yet_received` and remains separate.

## Hard visual meaning

The request-scoped `solar_flare_active_region_burst` profile is active through `photo-visual-intent/v1`. Its four literal evidence bindings are preserved in the composed prompt and its four strict render gates all passed on the same image.

The advisory `solar_space_weather` CME/coronagraph cluster was rejected. An occulting disk, registered masked solar center, and broad detached radial front would replace the locked localized active-region flare. No CME cluster candidate entered the composed or runtime prompt.

## Pixel review

Common gates:

- `reference_visible_appearance_continuity`: pass — appearance-only continuity in visible face shape, eye aperture/spacing, lower-face shape, hairline, and long dark wavy hair; no identity claim.
- `adult_age_continuity`: pass — visibly adult at native and thumbnail scales.
- `gross_structural_coherence`: pass — subject, limb, glove, control, telescope, display, window, and lunar context form one coherent scene.
- `required_interaction_contact`: pass — a gloved hand visibly operates the telescope-console control.
- `unrequested_text_artifacts`: pass — tiny interface numerals/pseudo-glyphs exist, but the disk, active region, burst, and loops carry the scientific meaning; no caption, sign, or watermark supplies a missing gate.

Profile gates:

- `vo_space_flare_sun_context`: pass.
- `vo_space_flare_active_region`: pass.
- `vo_space_flare_burst`: pass.
- `vo_space_flare_response`: pass.
- `representation_false_color_multiwavelength`: pass.

Failed gates: none. Partial evidence was not used as pass evidence.

## Render artifact

- Workspace image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-space-three-arm-reference-v1/arm-03-solar-flare/render.png`
- SHA-256: `a659a3c859b2ea07f5458f083888118003f16edff620d570b00ec60d527811e7`
- Dimensions: `1536 × 1024`
- Native result source: `/Users/chasoik/.codex/generated_images/01a05c59-3d1e-7360-9d59-b7dd47407cf0/exec-6be7fdde-3f8b-48d4-b2d8-76562cec1d39.png`
- The source result and workspace copy have identical SHA-256 values.

## Key records

- `authorial_core.json`, `authorial_core_hashes.json`
- `visual_intent.json`, `candidate_pack.json`, `candidate_rejection_record.json`
- `composed_prompt.json`, `composed_prompt_audit.json`
- `image_render_request.json`, `image_render_request_audit.json`
- `self_review.json`, `visual_render_review.json`, `visual_render_review_audit.json`
- `imagegen_result.json`, `run_manifest.json`, `run_ledger.ndjson`

## Evidence boundary

Prompt/package audits prove serialized contract compliance. Native and thumbnail review support only the recorded pixel judgments. The generated display is fictional editorial imagery, not evidence of a real solar observation or mission event. The attached portrait was used only as observable appearance guidance for an original adult fictional subject; no identity, same-person, or sensitive-trait inference was made.
