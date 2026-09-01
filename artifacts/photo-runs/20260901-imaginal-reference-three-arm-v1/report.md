# Imaginal reference three-arm render qualification

## Outcome

Three independently generated images completed one built-in `image_gen` call each with zero retries and no cross-arm inputs. All composed-prompt and runtime audits passed. The selected target profiles qualified in 2/3 images and 13/15 target gates passed, but strict full-case qualification is 0/3 because each frozen complex case retained at least one failed target, scene, or locked-core gate. Overall decision: `revise`. Requesting-user aesthetic judgment remains pending.

The portrait was used only for visible long dark wavy hairstyle and dark blouse styling. The run makes no biometric identity, same-person, protected-trait, health, attractiveness, or personality claim.

## Randomization

The run shuffled nine newly added imaginal profiles and twelve unrelated scene concepts from SHA-256 seed `f5e0d46048b3bf82ab6f6459440e4288d5b1ec69a67d95579b935d2207d30c4d`. The selected arms were:

1. `phantasmagoria projection` in an abandoned aquarium ticket hall.
2. `matter-of-fact magical realism` in an after-hours railway lost-property office.
3. `face pareidolia` in a coastal weather observatory.

Six profiles remain untested in this run: ambiguous figure-ground, oneiric dream logic, continuous metamorphosis, liminal transition-use gap, impossible object, and mirror reflection mismatch.

## Results

| Arm | Target keyword pixels | Scene / frozen-core gate | Reference style | Full case |
|---|---:|---|---|---|
| A — phantasmagoria | 5/5 PASS | FAIL: camera faces projection, not route map | PASS | `revise` |
| B — magical realism | 5/5 PASS | FAIL in root cross-review: floor aperture is detached from parcel cast shadow | PASS | `revise` |
| C — face pareidolia | 3/5 PASS | Scene PASS; target material continuity and unadded-component gates fail | PASS | `revise` |

### Arm A

The lantern/projector and operator, bounded light cone, tiled receiving wall, four-stage jellyfish sequence, and separated depth layers are all visible in the same image. The target keyword therefore qualifies technically. The supplemental route-map recording event fails because the tripod camera points toward the projection wall while the map is behind the filmmaker.

- Image: `arms/arm-a/result.png`
- Exact prompt: `arms/arm-a/composed_prompt.json`
- Pixel evidence: `arms/arm-a/pixel_review.json`

### Arm B

The ordinary office, single impossible railway region, calm practical response, continued logging-and-shelving routine, and floor occlusion/residue all remain legible. The broad magical-realism profile therefore qualifies technically. The frozen core was more specific: the railway platform had to open inside the parcel's connected cast shadow. The image instead shows a detached floor aperture or shadow-pool, so the complete case remains `revise`.

- Image: `arms/arm-b/result.png`
- Exact prompt: `arms/arm-b/composed_prompt.json`
- Pixel evidence: `arms/arm-b/pixel_review.json`

### Arm C

The storm glass remains a recognizable nonface instrument and a face-like eye/mouth relation is immediately visible. The two reads coexist, but the crisp ringed eyes and smooth dark smile interrupt the crystal-liquid material and look deliberately inserted. `material_continuity` and `unadded_components` fail; partial evidence is not promotable.

- Image: `arms/arm-c/result.png`
- Exact prompt: `arms/arm-c/composed_prompt.json`
- Pixel evidence: `arms/arm-c/pixel_review.json`

## Verification layers

- Package: focused imaginal tests 9/9 PASS; generated index check PASS at 189 profiles and 1,090 exact terms.
- Prompt: composed audits 3/3 PASS, with advisory word-budget warnings only.
- Runtime: exact render-request audits 3/3 PASS.
- Delivery: saved PNGs 3/3; one image call and zero retries per arm.
- Independence: `photo-independent-run-manifest/v2` for all arms, `cross_arm_inputs_used=false`, one ledger row per arm.
- Pixels: 13/15 target gates, 2/3 target profiles, 0/3 full frozen cases.
- User: direct aesthetic acceptance not yet received.

## Bounded next step

No skill, registry, index, or test source was changed. A future authorized render-only follow-up should change one local actuation per failed case: make the map occupy Arm A's camera optical path; attach Arm B's anomaly boundary to the parcel's cast-shadow origin; and replace Arm C's symbolic eyes and smile with irregular substrate-owned bubbles and sediment. These are hypotheses for retest, not claims that the current contracts are universally improved.
