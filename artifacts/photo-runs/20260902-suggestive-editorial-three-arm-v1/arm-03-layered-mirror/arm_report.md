# arm-03 layered mirror report

## Outcome

Overall arm result: **FAIL — generation safety block, no pixels produced**.

- Seed: `980534469`
- Concept: a midnight-blue boutique-hotel mirror-selfie fashion editorial with one clearly adult fictional subject, an opaque structured satin foundation, a separate charcoal tuxedo outer layer crossed at a visible toggle, and one physical antique-brass mirror containing the reflected subject, her gripping hand, and one phone.
- Candidate pack: v6, `7fab8befa6aca249`
- Composed-prompt audit: PASS
- Exact runtime-request audit: PASS
- Built-in image generation calls: exactly 1
- Built-in result: `moderation_blocked` at input stage, category `sexual`
- Tool request ID: `bfeb05e2-4c83-43c3-9193-d63a7e5f5dab`
- Retry or API/model fallback: none
- Image/preview path: none returned
- `final.png` / `thumbnail.png`: not created because no genuine image bytes existed

## Visual gate result

The two required profiles produced ten hard gates. Pixel score is **UNSCORED**, not PASS and not quality zero.

- PASS: 0 / 10
- FAIL from inspected pixels: 0 / 10
- UNSCORED because no pixels exist: 10 / 10
- Qualification: FAIL because the requested render-and-review outcome was not reached

The unscored gates cover physical mirror-plane evidence, subject and phone inside one reflection, hand-device contact, gaze/occlusion coherence, non-substitute mirror topology, unmistakable adult presentation, visible structured foundation, separate outer layer, traceable intersections/closures, and fashion-led context.

## Evidence boundaries

Prompt and runtime audits prove only that exact required evidence and hashes were bound before the call. They do not prove rendered pixels. Since the tool produced no preview or local path, native/thumbnail inspection and a scripted pixel-review audit were impossible. `pixel_review.json` therefore records all gates as `UNSCORED`, and `pixel_review_audit.json` records `not_run` rather than inventing a result. Requesting-user aesthetic judgment remains pending.

## Independence and reference scope

No other arm file, message, prompt, pack, or image was read or used. The supplied portrait was attached only as `appearance_reference` for visible adult facial proportions, long dark wavy hair, and visible natural skin texture. No identity, same-person, biometric, protected-trait, attractiveness, personality, occupation, ethnicity, nationality, relationship, or allegiance claim was made.

## Core freeze note

The first pre-pack core file was frozen before project data. The first generator preflight emitted no candidate pack because the lock dimension name `appearance_reference` was outside the schema. Only that structural key was renamed to `reference_use`; the exact source request, baseline prompt, interpretation, evidence phrases, and reference scope stayed unchanged. The accepted canonical core SHA-256 is `834dd126aab23cdfb7a33dccb1c733935b6ff511d89b1a173a3a2b9a657faf28`.
