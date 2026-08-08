# Composition Contract

## Candidate Pack v2

`--emit-candidate-pack` returns a JSON array. Generate and audit one pack at a time. Each generated pack carries `contract_version: photo-candidate-pack/v2`; `pack_id` is the first 16 hexadecimal characters of SHA-256 over canonical JSON with `pack_id` replaced by `null`.

The audit rejects a changed pack, a list containing zero or multiple packs, a missing composed field, a non-agent composer, an empty candidate selection, a changed negative prompt, failed concept gates, and a non-pass safety record.

Candidate caps are four presets, four candidates for core slots, two for support slots, and 64 slot candidates in total. Every sampled selection is reserved before alternatives so truncation cannot silently remove it. Ordinary slot alternatives come from the exact pool recorded after sampler applicability, no-people, compatibility, and hard-conflict filtering, with `applicability.source: sampler_eligible_pool`.

A resolved render blueprint is not a candidate. It lives in `render_contract.selected_scene` and a `scene_contract` group whose source is `selected_render_blueprint`, outside the ordinary `slots` pool. Its subject, action, location, and prop labels are mandatory literal render atoms. The composer copies all four labels into the prompt and does not choose ordinary candidate IDs for those controlled core slots. This preserves exact sampler provenance while preventing cross-scene mixing.

An explicit `--creativity` value from `0.75` through `1.0` may add `creative_exploration`. Its contrast rows never add, remove, or reorder candidates: each `candidate_id` is an already exposed `sampler_eligible_pool` alternative that replaces the selected candidate in the same slot, clears conflicts with selected candidates in other slots, and exceeds the declared feature-distance floor. Keep the selected subject, mandatory intents, and atomic scene; use no more than `composition_guidance.replace_at_most` mutually compatible contrasts. The field is absent below the activation floor, preserving the ordinary pack shape.

The same explicit range adds `creative_direction`, an agent-level creation and selection contract with no topic examples or new candidates. It requires an ordinary-baseline critique, at least four proposals using distinct concept operators, exactly one selection, one rule change, at least two visible consequences, a staged reveal path, and a concrete authorial grammar. Its evidence fields must be literal in `prompt_en`; signatures from unselected proposals are forbidden. See `creative-direction-contract.md`. The field is absent below the activation floor, so ordinary composed prompts retain their existing contract.

## Required Composition Behavior

- Use every `mandatory_intents[].text` as literal or faithfully translated visible content.
- `audit_terms` and candidate labels are discovery aids, not proof of user-intent coverage.
- `coverage_assertions` may map an exact mandatory-intent key to one or more phrases. Every phrase must occur literally in `prompt_en`.
- Choose IDs only from `presets`, `slots`, or proposition candidates included in the pack.
- Choose only candidates with `applicability.status: eligible`.
- Do not choose both sides of a hard conflict.
- Preserve `negative_en` exactly, including `null`.
- Set `composer` to `agent`.

## Masking and Generalization

Semantic dropout removes masked slot candidates, selected IDs, labels, terms, and preset values from the public pack. `open_slots` contains only the slot name, bucket, status, and reason. Fill the opening from the user request and remaining contract; never reconstruct the hidden exemplar.

If a composed ID names an open slot, the audit fails. Masked details are also removed from conflicts and mandatory-intent coverage metadata.

## Meaning and Coherence

- `intent_contract` and `coverage.intent_constraints`: typed subject categories, domains, negative-presence constraints, and their matching evidence. They are routing constraints, not prose suggestions.
- `scene_contract`: every `atomic_scene` group is fail-closed. Candidate-backed groups constrain IDs to a selected variant. A `selected_render_blueprint` group instead requires all four literal labels and rejects ordinary candidate IDs for its controlled core slots.
- `render_contract.selected_scene`: one selected scene function set, one diegetic visual provenance, relationship stakes, and genre anchors. `market_origin` is not visual provenance and must not be rendered as a national costume shortcut.
- `--scene-function` is an optional control for direct research-backed presets. It requires `--preset`, does not add a mandatory intent, and fails closed for an unknown or unavailable function. A no-people request first removes every blueprint that is not explicitly declared non-human; an empty or human-only remainder is an error rather than a silent human render.
- `evidence_budget`: count chosen slot names, not candidate count. A materialized scene prop may be the first physical clue; when the range is 1–2, choose no more than one additional listed clue slot.
- `concept_axes.required`: show each meaning axis through behavior, placement, expression, material, light, or framing.
- `role_scene_policy`: when `enforce` is true, select an allowed location ID; omission is a failure.
- `species_family`: select every required family slot from the allowed family. Missing IDs and mismatches both fail.
- `motif_budget.discouraged_now`: avoid repeated motifs unless the user explicitly requested one.
- `concept_gates`: every result must be `pass`; the wrapper blocks failed gates before pack generation.

## Quality Layers

`quality_profile.profile_id` is one of `general`, `documentary`, `portrait_editorial`, `product`, `food`, `architecture`, `nature`, `science_inspection`, `mobility_logistics`, `climate_adaptation`, `biodiversity_monitoring`, `agriculture_food_systems`, or `circular_materials`.

Use `photographic_integration` to bind subject and setting with believable light, contact, material, or optical depth. Use one visible `visual_proposition`, then at most one or two `photographic_craft` decisions. These are quality signals, so the audit reports omissions as warnings.

`artistic_final_touch` is disabled for most profiles. When enabled, use the sentence or equivalent terms; it does not have to be the exact final suffix. It is surface craft, not evidence of a distinct authorial point of view, and the creative-direction audit rejects using its fixed sentence as authorial grammar evidence. Never add the documentary imperfection formula to product, food, architecture, nature, or polished editorial prompts by default.

## Safety

Default safety is the small automatic-pass object documented in `SKILL.md`, with no approval wait. Run `--safety-evaluation` only when the user explicitly asks for a safety review. It changes only the report mode and lists evaluated recipe transforms; it does not grant extra authority and does not replace platform or image-tool policy.
