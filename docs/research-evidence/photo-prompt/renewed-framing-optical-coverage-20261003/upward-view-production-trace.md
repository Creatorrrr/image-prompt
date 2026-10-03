# Case006 upward-direction coverage check — corrected

2026-10-03 UTC. **Existing DATA coverage and production eligibility confirmed; no candidate addition recommended.** This correction supersedes the earlier addendum's 35-candidate count and unsupported historical-runtime explanation. The first probe and superseded report are preserved for auditability.

## Exact cause of 35 versus 28

The first probe used `load_json(photo_prompt_tags.json)` instead of the production `load_runtime_data()`. The former merges candidate rows but does not attach `_quality_layers`; the latter loads quality layers and activates their primary-context requirements through `compatible_with_slot_context`.

Both paths have 49 direction rows and 49 unique direction IDs. This is not deduplication, source change, or historical runtime drift. Using either the saved public core or newly normalized exact input core gives the same result: bare loader 35 eligible; production loader 28 eligible.

The seven extra rows admitted by the incomplete loader are `dashcam_windshield_direction`, `cctv_corner_direction`, `over_shoulder_back_seated`, `long_lens_compressed_direction`, `over_railing_down_direction`, `elevator_corner_camera_direction`, and `from_table_edge_hidden_camera`. Each fails a production quality-layer primary-context requirement for this frozen toy-train scene. Guard source IDs and requirement lists are saved in `coverage-correction-probe.json`.

## Production path and source coverage

Loaded runtime data with `load_runtime_data`; normalized the exact `public-cli-property/inputs/blind_scene_006` request envelope and authorial core against its exact creative controls; called `prepare_candidate_source` with the saved embodiment review and seed 829; and replayed the actual `retrieve_core_slots` function with tracing. No source data or runtime changes were made.

`worms_eye` is in this production source pool and passes the complete pre-ranking eligibility function. Its Korean label is `아래에서 올려다보는 웜즈아이뷰`; its English and emitted concept unit are `worm’s-eye view from below`. This is an upward/from-below camera direction, not merely low physical camera height. It has no human-only restriction and is object-capable for this exact generic toy-train core.

`extreme_low_angle_under_subject` and `extreme_low_hero_angle` also pass production eligibility, although their extreme/hero treatment may be stronger than needed. `low_ground_angle` passes but is not the decisive coverage evidence because its wording alone specifies only ground-level position.

## Where the correct candidate is lost

Production replay reproduces the same four returned direction IDs as the saved public pack: `birds_eye`, `dutch_tilt_dynamic_view`, `strict_top_down_flat_view`, and `mirror_reflection_camera_view` (ordering differs only between internal rank order and public shuffled presentation).

- `extreme_low_angle_under_subject` is broad rank 1
- `extreme_low_hero_angle` is broad rank 2
- `worms_eye` is broad rank 5
- The focal result has only four rows: bird's-eye, Dutch tilt, strict top-down, and mirror
- None of the three upward-facing candidates is in the focal result
- Observed/discovery candidate list is empty
- The code intersects broad and focal IDs before fusion selection, so the upward candidates are removed by that intersection
- `camera_direction` is processed at total=0 with limit=4; total-cap exhaustion is not the cause in this case

The focal query uses the Korean visual priorities/style, including lower-than-shelf camera position, locomotive size, ceiling visibility, `general_photo`, and `independently authored scene study`. The whole-scene query successfully finds the upward candidates; the focal-query/intersection path loses them. This is demonstrated retrieval behavior, not missing DATA and not an applicability block on worm's-eye.

## Artifacts and bounds

`coverage-correction-probe.py`, `.json`, and `.log` contain the four-way loader/core comparison, exact normalized core and controls, production trace, guard-level differences, prepared-source check, and current SHA-256 hashes for runtime source, base tags, quality layers, and every frozen input. The original first probe and superseded report remain unmodified.

No candidate wording correction, new candidate, routing/configuration edit, paid call, image generation, or index write is proposed or performed.
