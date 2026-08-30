# Arm 03 result

Technical outcome: **PASS**. The first and only built-in image-generation call produced one saved 916×1717 PNG, and direct `view_image` inspection found all three fixture atomic pose gates present together in that same image. No retry was eligible. Requesting-user preference and facial-resemblance judgment remain pending.

## Frozen concept

One clearly adult woman, age 28, calibrates an amber gyroscopic safety beacon during an emergency drill on a flood-resilient underground maglev platform. She wears a fully opaque graphite technical coverall, gloves, and armored boots. The scene was independently selected for this arm within the future-civic-transit lane.

The target pose terms were recorded as an agent-selected test variation, not requester definitions:

- frontal-plane pelvic obliquity under single-leg support;
- staggered leg depth separation;
- head-shoulder opposition.

The attached image was passed to built-in imagegen as facial-appearance guidance only. Identity control was false. This run makes no biometric, identity-preservation, or same-person claim.

## Candidate qualification

Pack: `photo-candidate-pack/v6`, pack ID `0bcf2e715e23d6e7`.

- `pelvic_obliquity_single_support`: did not surface in the pack; not selectable; retained only through the frozen authorial-core pose anchor.
- `staggered_leg_depth_separation`: did not surface in the pack; not selectable; retained only through the frozen authorial-core pose anchor.
- `head_shoulder_opposition`: surfaced as eligible `slot:body_orientation:head_shoulder_opposition` and was applied/chosen.
- Optional `contrapposto_weight_shift` and `figura_serpentinata_spiral_pose` profile candidates were rejected because their extra counter-tilt/spiral mechanics would confound the isolated three-relation test. No optional visual-profile gate was promoted.

Detailed provenance is in `candidate_surfacing.json`.

## Audit status

- Candidate pack: one emitted v6 pack; SHA-256 `a075d1acd837afa54491a08930e88e8a59afa5341e6ad3031e00fea03667fa26`.
- Composed prompt: PASS, 177 words, zero failures. Quality status WARN only because all seven uncovered candidate-pack intents were preserved literally by authored prose rather than candidate coverage.
- Exact render request: PASS, runtime prompt ID `45d2b00977a2bc3d`, byte-identical negative prompt, one verified appearance-only reference, zero failures.
- Image tool: built-in imagegen; image-call count 1; retry unused.
- Cross-arm inputs used: false.

## Pixel gates

- `pose_arm03_frontal_pelvic_obliquity`: PASS. One image-right boot is clearly planted and loaded, the opposite leg is lifted, and the waistband/hip line has visible left-right height asymmetry while station architecture stays level.
- `pose_arm03_staggered_leg_depth`: PASS. The planted boot occupies the nearer plane, the flexed opposite leg and lifted boot trail behind, and both knees and ankles remain readable.
- `pose_arm03_head_shoulder_opposition`: PASS. Shoulders and arms organize toward the beacon on image-left while the face, nose, and chin turn toward the arriving capsule on image-right through a coherent neck.

Technical verdict: 3/3 atomic gates pass; registry gate count 0; failed gate IDs: none. User preference/resemblance: pending.

## Artifacts and hashes

- `authorial_core.json` — raw file SHA-256 `898a601c9f0fa6a5d3875328a5d58a7bfe2ec751cb04492d6de52746b09e6a21`; generator-canonical core SHA-256 `704525875a10e3c9820435126664d2fcc78b3df4182370cdf6187a34df1c7a72`; intent-lock SHA-256 `8fb75b43e4b4a44855dfeafec734eacf2ab0742f2fb616685c060716248472c4`.
- `candidate_pack.json` — SHA-256 `a075d1acd837afa54491a08930e88e8a59afa5341e6ad3031e00fea03667fa26`.
- `composed_prompt.json` — SHA-256 `9a222bbd317f1763a999ee1f850a86c429de739ebc9b5d61853bc8bc68da5616`.
- `render_request.json` — SHA-256 `b0aafe808e20f37e456218f98e6a6c0ea5c798026643cbd9fa0f4d536c50b2c7`.
- `image-attempt-01.png` — SHA-256 `b3e30fd704f51b224823626df999a6861a4ac64a37da98f5437e6b7f0fdb467a`; 916×1717.
- `pixel_review.json` — SHA-256 `39e69e00e1ae7006085b53c8af231c10b52d33efe759105b22d2d2ecf94460f8`.
- `run_manifest.json` — `photo-independent-run-manifest/v2`; SHA-256 `90078c6ccc132b9134f43f6d4dbfadcec15940ad753861d4aaf0ff4d54bf404b`.
- `image_runs.ndjson` — arm-local ledger run ID `9bd4b42f7f5f48d3`; SHA-256 `463976073c1309348936b80f9d3bb5503baaa847ef374c75a94ccffd7467ff6e`.

All paths are under `artifacts/photo-runs/20260831-pose-semantics-five-arm-v1/arms/arm-03/`.
