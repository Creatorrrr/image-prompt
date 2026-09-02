# Arm 01 — Window Reveal Qualification Report

## Result

Technical arm result: **PASS (10/10 hard gates)**. The built-in image generator was called exactly once, returned a concrete local file, and no retry or fallback was used. Requesting-user aesthetic judgment remains pending, so this result is not labeled user-approved or representative.

## Independent concept

- Seed: `13389124217090213127`
- Concept: a curtain-diffused private-bedroom lifestyle-fashion editorial in which an unmistakably adult woman tightens an opaque deep-plum wrap dress; one dominant diagonal lapel edge carries the stable coverage-and-reveal relation.
- Reference role: `appearance_reference` only, limited to visible adult facial proportions, long dark wavy hair, and visible natural skin texture. No identity or same-person claim is made.
- Cross-arm inputs used: `false`

## Generated image

- Native: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-suggestive-editorial-three-arm-v1/arm-01-window-reveal/final.png`
- Native SHA-256: `bee8a97ee78bcff0ef9a56597c428af9f93593785479ba42895aaa278a4fb57f`
- Native size: `1023x1537`
- Thumbnail: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-suggestive-editorial-three-arm-v1/arm-01-window-reveal/thumbnail.png`
- Thumbnail SHA-256: `16163b663cd114c72a442cf973b116c3ebdce52ecda6110b83bf68965e966fbc`
- Tool: `built_in_image_gen`
- Image calls: `1`
- Preview-only: `false`

## Gate review

| Gate | Scale | Status | Pixel evidence |
|---|---|---:|---|
| `vo_everyday_reveal_adult_actor` | both | PASS | One clearly adult woman is the sole visible actor. |
| `vo_everyday_reveal_self_directed_action` | thumbnail | PASS | Both hands manipulate the waist tie while her lowered gaze follows the knot. |
| `vo_everyday_reveal_single_boundary` | both | PASS | The deep-plum outer lapel makes one dominant, continuous opaque diagonal coverage boundary. |
| `vo_everyday_reveal_holistic_context` | thumbnail | PASS | Face, hands, torso, dress, curtain, bed, mirror, slippers, and room depth remain legible together. |
| `vo_everyday_reveal_material_physics` | native | PASS | Weighted cloth, overlapping lapels, crossover shadow, tie tension, and gravity folds explain coverage. |
| `vo_private_window_adult_actor` | both | PASS | The adult remains the portrait's visible acting subject. |
| `vo_private_window_room_context` | thumbnail | PASS | Bed, bedside table/lamp, slippers, mirror, door, window, and depth read as a private bedroom. |
| `vo_private_window_diffused_source` | both | PASS | The visible translucent curtain and window create a left-to-right gradient with soft shadow falloff. |
| `vo_private_window_self_directed_action` | thumbnail | PASS | The standing adult actively tightens her own dress rather than reclining or passively posing. |
| `vo_private_window_material_relation` | native | PASS | Lapel thickness, overlap, contact shadow, tie compression, and gravity-driven panels are visible. |

Partial or missing gate evidence was treated as failure; none of the ten exact gates was partial or missing.

## Audit boundary

- Composed prompt audit: `PASS`; three non-blocking warnings only note that frozen intent anchors were preserved through free prose rather than candidate IDs.
- Exact render-request audit: `PASS`; runtime prompt ID `00252fb0dff2831a`; reference count `1`; negative bytes matched the pack.
- Pixel-review audit: `visual_technical_qualified_user_judgment_pending`; schema failures `0`; failed hard gates `0`.
- User judgment: pending / not yet received.

The first candidate-pack command was rejected before pack creation because the visual-intent source text initially pointed to core `event`/`setting`, while the normalizer permits post-core source binding to `interpreted_intent`, `baseline_prompt_en`, `visual_priorities`, definition meaning, or interpretation resolution. The visual intent was corrected to byte-exact frozen `visual_priorities`; the authorial core and its hash were not changed. This preflight correction consumed no image call.

## Non-gating variance

The image carries the reveal through the V-shaped diagonal lapel and visible collarbone area. The baseline's bare-one-shoulder detail did not survive. That detail is outside the exact `vo_*` profile gate set, so it is recorded as a prompt-level variance rather than a hard-gate failure.

## Lineage

- Pack: `076085a373aae93d` (`photo-candidate-pack/v6`)
- Canonical authorial core SHA-256: `fd078c0649b08a0606befc739acd3ba63543aae38ab9f407a38a1afea83c5b22`
- Intent-lock SHA-256: `90b54256b92c2c5c903adf5b2baae8a9bf1b363a0f9baa72909225ba61a54f26`
- Canonical visual-intent SHA-256: `4466b9f1d47ab18b58dd7cb590f072276f2a2bd2552192dfc3879d408f22c1d2`
- Effective visual contract SHA-256: `3668b7b1535fa114a2337fd7a3277189c987e17150a508cbf20effc91c8bdbe6`
- Ledger run ID: `aaa9782b5e613624`
