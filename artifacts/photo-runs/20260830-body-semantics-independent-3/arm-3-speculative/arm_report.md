# Arm 3 — Speculative Science Held-Out Render

## Outcome

The seed-selected concept is **The Selenographic Storm Cabinet**: one clearly adult original woman operates a transparent storm instrument inside a flooded lunar archive while a cyan aurora crosses the room at waist height. The final candidate pack, composed prompt, and both exact runtime requests passed their preflight audits. Two built-in image-generation calls were made: one original render and one permitted targeted repair.

The repair improved the selected semantic details, but the final image is **not strict-pixel-qualified**. Two of nine visual hard gates remain failed: the philtral groove-to-double-arc relation is not reliably readable at thumbnail scale, and the opposite upper-torso contour remains partly occluded by the forearms, preventing a complete bilateral silhouette read. Requesting-user acceptance is still pending.

## Independent Freeze

- Random seed: `3647554984`
- Independent domain: speculative science interior narrative
- Concept file: `concept_selection.json`
- Final pre-pack core file SHA-256: `d765cee62ff3b1e155c012b942f47530d64e990ea1ea10bada22de75adfdcca6`
- Canonical normalized core SHA-256: `b2056c043be929cc120d7f4a89620837d5fd6906ab8fe39452eb8303480158cd`
- Canonical intent-lock SHA-256: `6c02bfae27c1131e957311665859682327e04358ad182f9fba6d79cb159478f2`
- Baseline word count: 174
- Candidate/profile/project data seen before freeze: no
- Cross-arm prompt, pack, message, or image inputs used: no

The first core file hash was superseded only because the v6 normalizer rejected four nonstandard intent-dimension names. The authorial concept and baseline prompt bytes were left unchanged; `core_freeze.json` records that structural correction.

## Candidate Pack and Semantic Decisions

- Final pack: `photo-candidate-pack/v6`
- Pack ID: `76dac2c49dd72185`
- Pack file SHA-256: `2fbae641bc511df21ccffd373450ff87d74f058c1e62fc9bda4c19fad00aeb1f`
- Selection: hybrid, creativity `0.65`, reference-edit mode `identity`, adult-appeal axes explicitly off
- Transformed creative candidate: `slot:lighting:blue_hour`, converted into cyan floor bounce motivated by the frozen aurora
- Naturally surfaced optional visual concepts rejected:
  - `visual-concept:diegetic_reality_invariant_failure`: would introduce a second world-rule mechanism
  - `visual-concept:kuudere_composed_warmth_relation`: requires a relationship counterpart absent from the frozen scene

Adopted new profile IDs:

1. `upper_lip_philtral_contour` — relevant because the frozen face and natural mouth contour are primary review areas.
2. `hourglass_silhouette_relation` — relevant because the frozen head-to-knees view and shaped practical uniform expose an upper-torso/waist/hip relation.

Rejected new family IDs:

- `clavicle_supraclavicular_hollow` — the frozen close collar covers the required region.
- `decolletage_neckline_exposure` — its low-neckline obligation conflicts with the frozen close-collar uniform.
- `lateral_waist_hip_contour_transition` — its side-view outer-thigh topology would duplicate and overconstrain the selected bilateral silhouette test.

## Prompt and Audits

- Exact prompt: `prompt.txt` (179 words)
- Composed object: `composed_prompt.json`
- Prompt ID: `d11857c9c0790bdd`
- Composed audit: PASS, quality WARN only for core intents realized through free literal description rather than candidate IDs; no failures
- Runtime request 1 ID: `370b98159ba1e630`, PASS
- Runtime request 2 ID: `13dd064a734f3e39`, PASS
- Effective visual-contract SHA-256: `622faceda348bb264dff01e9dfeb41aa3c41116b08ba4da5942b07085bee174e`
- Reference path: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Reference role: facial appearance only; no identity, ethnicity, health, age-inference, or biometric claim

## Rendered Attempts

### Attempt 1

- Image: `render-attempt-1.png`
- SHA-256: `87c539cfd41fc45a9e4e2f5135e8e6e8c5be7a408b916213492fe32f2741781a`
- Size: 1254 × 1254 PNG
- Strict failed gates: 5
- Material failures: philtral ridges/arc were too weak; one silhouette side was occluded; the metallic waist band made garment-only interpretation plausible.

### Attempt 2 — selected delivery image

- Image: `render-attempt-2.png`
- SHA-256: `ce0d4b5581298025999d9b36d157d935c9f84a73dea9ae1cf512c21c5abe8edc`
- Size: 1254 × 1254 PNG
- Strict passed gates: 7 of 9
- Strict failed gates:
  - `vo_philtrum_upper_lip_arc`
  - `vo_hourglass_bilateral_silhouette`
- Repair result: native philtral relief became clearer and the belt-like waist band was removed, while the scene, storm interaction, face arrangement, close-collar uniform, and aurora were preserved.

## Pixel Findings

- Facial appearance: moderate visual consistency without an identity claim. Face length, eye spacing, brow line, nose-lip balance, lower-face width, and dark hair framing broadly follow the reference. The rendered eye aperture is slightly rounder and the lower face somewhat narrower.
- Frozen concept: passes at thumbnail and native scales. The flooded archive, transparent storm cabinet, active tuning-ring interaction, waist-height cyan aurora, close-collar black-and-copper uniform, and wet copper-glass material world are all readable.
- Upper-lip/philtral profile: native paired ridges and central depression improved and pass, but the groove-to-double-arc topology is not reliable at thumbnail scale.
- Hourglass silhouette profile: upper-torso/waist/hip sequence, smooth transition, neutral context, and separation from belt cinching pass; a complete bilateral read fails because the near forearms obscure the opposite upper contour.
- Anatomy/contact: both hands maintain plausible cabinet contact; jewelry and concentric control rings are visually dense, but no unambiguous extra digit or fused-hand failure is visible.
- Material quality: water, reflections, smoke glass, oxidized copper, hair, fitted fabric, and storm light remain distinct and coherently lit.
- Text artifact: small pseudo-lettering remains beneath the sleeve emblem despite no requested text.
- Content boundary: fully clothed, clearly adult original fictional subject; nonsexual scene.

## Qualification Boundary

Pack and runtime PASS are preflight evidence only. The selected image remains `failed_strict_visual_hard_gates`, is not representative-eligible, and has not received requesting-user acceptance. The single allowed targeted repair was used; no further render was attempted.
