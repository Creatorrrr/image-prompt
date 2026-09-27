# Arm A result

One actual v6 pack and one built-in image generation were completed from the unchanged frozen core. No re-draw, render retry, or CLI fallback occurred.

The scene is an adult in Y2K millennium-futurist clothing adjusting a mechanical star projector in an indoor planetarium gallery. Seed: `7278773002676095595`.

## Qualification

The four Y2K appearance gates passed. The complete independent scene test is **not qualified**: 7 gates passed, 0 failed, and 1 is unscored because the right projector sphere extends outside the frame, preventing a complete-equipment visibility pass. Partial is fail; unscored is never promoted to pass. Requesting-user judgment is pending.

| Frozen gate | Status | Direct pixel observation |
| --- | --- | --- |
| a_y2k_materials | pass | The cropped silver jacket has broad metallic specular folds; both sleeves are translucent with lavender/rainbow PVC reflections and the upper-arm skin is visible through the clear panels. |
| a_y2k_silhouette | pass | The fitted jacket ends above the waist; silver cargo trousers sit low on the hips with large flap pockets; both thick-soled platform boots are completely visible. |
| a_y2k_accessories | pass | Narrow purple-tinted curved sunglasses sit above the forehead; a clear pale-lilac belt with grommets and a large polished oval chrome buckle sits across the low-rise waistband. |
| a_y2k_on_subject_cluster | pass | Metallic cropped fabric, translucent rainbow sleeves, low-rise utility trousers, purple narrow glasses, chrome oval belt hardware, and platform footwear coexist on the adult; these remain readable independently of the star machinery. |
| a_reference_visible_appearance | pass | The face is unobscured and visibly has dark brown eyes, a softly tapered facial outline, a straight slender nose, and rounded pale-pink lips. This is an appearance comparison, not an identity judgment. |
| a_physical_actuation | pass | The arm from the subject's right shoulder crosses forward to a grip on the projector side wheel; the left arm extends down to a separate stationary bench edge. Both arm chains and contact points are visible. |
| a_projector_consequence | pass | Two distinct black perforated spherical projection heads are connected by a heavy crossbar and pedestal; the side handwheel is mounted into the same structure. A dense field of projected star points covers the curved dome wall behind it. |
| a_embodied_scene_legibility | unscored | The adult, face, both contacts, belt, and boots are visible with plausible support. However the right spherical projector head extends beyond the top/right boundary, so the frozen requirement that the complete equipment be in frame cannot be assessed as satisfied. This is a crop visibility limit, not a diagnosed bodily defect. |

## Data exposure and adoption

The pack uses the ready dictionary hash. Its compact catalog has 101 rows and 95 distinct candidate IDs. New `y2kr` exposure and adoption are both 0. Eight optional visual profiles were discovered, with no Y2K profile. No bundle was exposed. Wardrobe/style/garment/footwear slots were absent from this slate.

Two existing support candidates were adopted after reading full details: `slot:light_type:calibration_projector_glow` and `slot:focus:deep_focus`. The Y2K prompt evidence came from the independently authored frozen baseline. This image therefore verifies that baseline's visible Y2K cues, but does not establish improvement caused by the reflected data.

## Audit boundaries

Composed audit passed with four candidate-coverage warnings whose frozen intent phrases were retained in prose. Exact runtime audit passed with the original local reference attached. Five embodiment pixel gates passed; the review auditor had no schema failures and returned `technical_qualified: true`, `representative_eligible: false`, with exit 1 because requesting-user judgment remains pending. The independent whole-scene visibility result is kept separately and is not overridden by that technical review.

The native image is 1144 × 1375, saved as `generated_image.png`. The randomization camera record listed a landscape format, but the frozen baseline omitted a format clause; this delivery difference is a supplemental observation and was not added to the frozen gates after rendering.

## Evidence

- `candidate_exposure_adoption.json`: discovery, exposure, adoption, and dimension limits
- `pixel_gate_review.json`: all eight frozen gates and observations
- `embodiment_pixel_review.json` and `pixel_review_audit.json`: schema-bound embodiment review
- `image_runs.ndjson` and `run_manifest.json`: one actual native call, saved bytes, independent provenance
- `evidence_manifest.json`: reference/core/gates/pack/composed/runtime/audit/image SHA-256 values

Original reference SHA-256: `00e6640ccad217559714c4cc93d3d9535ebc3ad03d73318e8bb5e7888ab04f72`. Generated image SHA-256: `ef00197b1e01d800b5ba17932a054d873d1bdb7e0c81872d26d6a2c9532fc1ae`.
