# Arm 02 — deliberate arson causality

Outcome: **FAIL under `partial_is_fail`**, despite all four assigned arson-profile gates passing. The reference-guided investigator is spatially separate and does not hide the event, but her foreground scale makes her the dominant visual subject rather than a secondary supporting role.

## Frozen test case

- Seed: `695725796`
- Declared-fictional concept: early-1990s evidence photograph at a shuttered riverfront botanical greenhouse during freezing rain
- Independent complexity dimensions: era, location, weather, documentary mode, architecture, camera
- Reference scope: visible adult appearance for the fictional adult fire investigator only
- Native image calls: exactly `1`; retry: none

The core, visual intent, test case, and rubric were hash-frozen before candidate-pack generation in `prepack_freeze.json`.

## Preflight evidence

- Candidate pack: v6, `pack_id=02b7f27adc3bbd0a`
- Active hard profile: `deliberate_arson_causality`
- Optional visual concepts selected: none
- Composed prompt audit: PASS; 208 words, advisory concision warning only
- Runtime request audit: PASS; exact prompt, negative bytes, intent-lock hash, reference path, reference hash, and role all bound
- Image tool: built-in `image_gen`
- Tool outcome: SUCCESS
- Native render: `render-native.png`, 1536×1024, SHA-256 `fdd1e76bd46e2c97a8d67eab9e9a0e48559c2bc6c132feda6a3e9ed394a8d75f`
- Thumbnail: `render-thumbnail.png`, 512×341, SHA-256 `34c8b003d081b7d1ac1569a4a8bfc6ff9d3eeae2dbdf811842ee4ad1f830afde`

## Pixel gates

| Gate | Scale | Result | Evidence |
|---|---|---:|---|
| `arson_actor_target` → `vo_crime_arson_setter_target` | thumbnail | PASS | Crouching adult fire-setter and one blue greenhouse service door are distinct. |
| `arson_ignition_path` → `vo_crime_arson_ignition_path` | native | PASS | One pale linear path continuously joins the actor's hand to the door-base fire. |
| `arson_same_point_origin` → `vo_crime_arson_origin` | native | PASS | Fresh flame begins where that path meets the selected door. |
| `arson_outward_expansion` → `vo_crime_arson_growth` | native | PASS | Flame and a dark scorch plume expand outward/upward from the same point. |
| `reference_adult_supporting_appearance` | native | PASS | Long center-parted dark wavy hair, oval face, dark eyes, and softly arched brows are visible. |
| `reference_role_separation` | thumbnail | **FAIL** | The investigator is separate but visually dominates the frame because of her large foreground face and torso. Partial secondary hierarchy fails. |
| `thumbnail_relation_readability` | thumbnail | PASS | Actor, door, diagonal ignition path, and bright fire point remain readable together. |
| `native_origin_boundary` | native | PASS | Fuse, contact point, orange origin, and scorch boundary remain distinct. |

Profile-only result: **4/4 PASS**. Full arm result: **7/8 PASS → FAIL**. User preference is pending and is not included in the technical score.

## Artifacts

- `request_envelope.json`, `authorial_core.json`, `visual_intent.json`, `test_case.json`, `pixel_rubric_precommit.json`, `prepack_freeze.json`
- `candidate_pack.json`, `composed_prompt.json`, `composed_prompt_audit.json`
- `render_request.json`, `render_request_audit.json`
- `render-native.png`, `render-thumbnail.png`
- `pixel_review.json`, `pixel_review_audit.json`
- `run_manifest.json`, `image_runs.ndjson`

The ledger contains one successful tool attempt; the separate pixel review records the strict technical failure. No sibling-arm prompt, pack, message, image, or review was used.
