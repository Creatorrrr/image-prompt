# Illustration Image Runtime

Use the built-in image-generation tool after the candidate pack and composed prompt pass the illustration audit. Do not use the photo API wrapper or photo ledger for this sibling skill.

## Generation

1. Save pristine `candidate_pack.json`, `composed_prompt.json`, and `audit.json` in a dedicated output directory.
2. Generate exactly one initial image from `prompt_en`. Preserve exact `negative_en` in local metadata even when the native tool has no separate negative field.
3. Save the native image without re-encoding when possible. Record dimensions, SHA-256, tool, prompt, negative, chosen IDs, pack ID, and attempt count in `result.json`.
4. Inspect the image without reading prompt metadata first.

Before the tool call, verify the audited `second_look_plan`: primary and fallback phrases are literal, their loci and consequences are distinct, and every `review_scale_id` comes from the format profile. Treat the initial generation as `attempted_role=primary_carrier`. Tiny glyphs, compound hand anatomy, and overlapping multi-limb projections require their declared risk flags and a risk-free fallback.

A saved preflight is still generation-free evidence. Keep `approval_required_before_generation=true`, `authorization_recorded_for_generation=false`, and all image-action flags false until the separately required authority is actually received; do not infer approval from prompt-audit PASS.

## Pixel Review

Review native resolution and the format-required views:

- every format: native plus a 320px thumbnail;
- responsive key art: square, wide, and vertical center-safe crops;
- cover/card: trim or frame-safe crop;
- vertical sequence: mobile-width top-to-bottom order;
- adaptation board: smallest declared representation.

Require the event, first and second look, primary atom, authorial rule, and format behavior to remain visible. Hash the UTF-8 JSON of `second_look_plan` using sorted keys and compact separators into `second_look_pixel_review.plan_sha256`, record the attempted role, and judge that carrier at every declared review scale with concrete pixel evidence. Qualification requires at least one declared role to pass all of its declared scales.

Do not infer a state change from palette contrast alone. If a proposed dry/wet, clean/dirty, hot/cold, worn/intact, or similar boundary coincides with a rug border, tile edge, fabric weave, panel division, or printed decoration, record it as ambiguous unless visible process evidence terminates at or crosses the boundary. Likewise, a narrow line cannot substitute for a declared broad carrier.

For an object-relation carrier, confirm the declared parts and relation separately at every review scale. A fixed support plus a displaced body, an independently displaced part, a causal connector, and an untouched action gap is stronger than a single tilt or motion mark. Do not credit decorative posture or motion lines alone as the claimed event.

## Bounded Repair

Preserve every failure. If the primary carrier fails, identify the product cause and switch the one allowed targeted edit or pristine rerender to `attempted_role=fallback_carrier`; do not spend it asking the same fragile carrier to become clearer. Never generate a batch and select the most favorable result. Historical v1 result files and PNGs remain immutable rather than being retroactively relabeled.

An audit pass is preflight only. A pixel pass is local product qualification, not proof of historical novelty or real audience behavior.
