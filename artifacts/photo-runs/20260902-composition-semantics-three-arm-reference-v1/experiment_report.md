# Composition semantics three-arm qualification

## Outcome

The data and prompt layers passed, but the rendered-pixel layer requires revision. With `partial_is_fail`, one of three independent arms passed all hard gates. Across the three images, 32 of 36 gates passed; user aesthetic judgment remains unscored.

| Arm | Random complex concept | Exercised profiles | Prompt/runtime | Pixels |
|---|---|---|---|---|
| arm-01 | flooded archive map rescue | centered primary anchor; frame within frame; primary-secondary hierarchy | PASS | FAIL, 11/12 |
| arm-02 | rain-dark ferry pier signal run | thirds anchor; look/motion room; pattern-break exception | PASS | PASS, 12/12 |
| arm-03 | fog observatory beacon crossing | negative space; asymmetric counterbalance; look/motion room | PASS | FAIL, 9/12 |

Arm 01 missed `vo_composition_center_anchor_location`: the exact frame center lands on the plain upper apron/torso rather than the face, hands, or map action. Arm 03 missed three direction gates: the lower-body motion cue is cropped and the gaze turns toward camera, so the right-side field cannot be proven to be ahead of a visible subject vector.

## Implemented data

Twelve composition relations were added to both the candidate dictionary and visual-obligation registry:

1. `third_grid_focal_anchor_relation`
2. `centered_primary_anchor_relation`
3. `axial_bilateral_symmetry_relation`
4. `asymmetric_counterbalance_relation`
5. `leading_line_target_continuity`
6. `look_motion_room_direction_relation`
7. `subject_field_negative_space_relation`
8. `frame_within_frame_boundary_relation`
9. `three_plane_depth_chain`
10. `pattern_break_focal_exception`
11. `primary_secondary_figure_ground_hierarchy`
12. `peak_action_event_phase`

Each visual profile contains four observable component groups, literal prompt-evidence requirements, four pixel gates, and explicit reject substitutes. The candidate layer also declares conflicts for center versus thirds placement, symmetry versus asymmetric counterbalance, and negative space versus frame-filling crops.

The rebuilt registries contain 312 visual profiles, 1,616 exact lookup terms, and 7,986 semantic-index entries across 16 shards. Eight unique new profiles were exercised in pixels; the other four have package and retrieval evidence only and are not image-qualified by this run.

## Research boundary

The implementation treats composition as a testable organization of locations, contours, groups, directions, and figure-ground relations. It does not encode a style label as proof of the relation. This follows the distinction between perceptual grouping and simple naming in the [Gestalt review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/), directional compatibility findings in [Palmer, Gardner, and Wickens](https://palmerlab.berkeley.edu/pdf/PalmerGardner%26Wickens-1.pdf), implied-motion evidence in [Kourtzi and Kanwisher](https://pubmed.ncbi.nlm.nih.gov/10769305/), and saliency limits discussed by [Itti and Koch](https://pubmed.ncbi.nlm.nih.gov/11256080/). Rule-of-thirds evidence is intentionally bounded: one empirical study reports only a weak relation to aesthetic ratings, so this work tests placement rather than claiming universal beauty ([Amirshahi et al.](https://doi.org/10.1163/22134913-00002024)).

## Independence and reference scope

The random seed was `16495771412272955302`, with one draw from each predeclared stratum and no redraw after selection. Each arm received its own frozen request envelope, authorial core, intent lock, and visual intent; used no cross-arm artifact; and made exactly one successful built-in image generation call with no retry or fallback.

The supplied portrait was used solely for observable adult-appearance cues. The review does not make identity, same-person, biometric, protected-trait, or other nonvisual inferences.

## Evidence layers

- Package: PASS. Dictionary/index validators and dedicated exact, false-substitute, and embedding-only tests passed.
- Prompt: PASS. All three v6 packs, composed prompts, and runtime requests passed their audits.
- Generation: PASS. Three independent one-call generations produced preserved files and hashes.
- Pixels: FAIL at the experiment level. Only arm 02 passed all gates.
- User judgment: UNSCORED. No requesting-user acceptance has yet been recorded.

The broad visual-obligation test suite still reports six failures around the pre-existing exact term `nurse`; the same failures reproduce against the baseline HEAD and are outside this composition change. Scene-expression (112/112), contradiction (2,106/2,106), public generalization (79/79), frozen rule holdout (24/24), and semantic retrieval holdout (22/22) passed.

## Artifacts

- Randomization and frozen inputs: `coordination/randomization.json`, `coordination/frozen_inputs.json`
- Root pixel review: `coordination/root_pixel_review.json`
- Improvement record: `iteration_record.json`
- Per-arm pack, composed prompt, runtime audit, image, pixel review, ledger, manifest, and report: `arm-01-archive-center/`, `arm-02-harbor-signal/`, `arm-03-fog-beacon/`

Decision: `revise` for render fidelity. The next bounded improvement should make exact-center targets coordinate-explicit and require a visible pose/gaze vector before allocating look/motion room; no such second-generation retry is included in this one-call experiment.
