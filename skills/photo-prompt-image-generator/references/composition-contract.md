# Composition Contract

## Candidate Pack v2

`--emit-candidate-pack` returns a JSON array. Generate and audit one pack at a time. Each generated pack carries `contract_version: photo-candidate-pack/v2`; `pack_id` is the first 16 hexadecimal characters of SHA-256 over canonical JSON with `pack_id` replaced by `null`.

The audit rejects a changed pack, a list containing zero or multiple packs, a missing composed field, a non-agent composer, an empty candidate selection, a changed negative prompt, failed concept gates, and a non-pass safety record.

Candidate caps are four presets, four candidates for core slots, two for support slots, and 64 slot candidates in total. Every sampled selection is reserved before alternatives so truncation cannot silently remove it. Rule mode exposes small filtered alternative pools instead of a one-choice answer key.

## Required Composition Behavior

- Use every `mandatory_intents[].text` as literal or faithfully translated visible content.
- `audit_terms` and candidate labels are discovery aids, not proof of user-intent coverage.
- `coverage_assertions` may map an exact mandatory-intent key to one or more phrases. Every phrase must occur literally in `prompt_en`.
- Choose IDs only from `presets`, `slots`, or proposition candidates included in the pack.
- Do not choose both sides of a hard conflict.
- Preserve `negative_en` exactly, including `null`.
- Set `composer` to `agent`.

## Masking and Generalization

Semantic dropout removes masked slot candidates, selected IDs, labels, terms, and preset values from the public pack. `open_slots` contains only the slot name, bucket, status, and reason. Fill the opening from the user request and remaining contract; never reconstruct the hidden exemplar.

If a composed ID names an open slot, the audit fails. Masked details are also removed from conflicts and mandatory-intent coverage metadata.

## Meaning and Coherence

- `concept_axes.required`: show each meaning axis through behavior, placement, expression, material, light, or framing.
- `role_scene_policy`: when `enforce` is true, select an allowed location ID; omission is a failure.
- `species_family`: select every required family slot from the allowed family. Missing IDs and mismatches both fail.
- `motif_budget.discouraged_now`: avoid repeated motifs unless the user explicitly requested one.
- `concept_gates`: every result must be `pass`; the wrapper blocks failed gates before pack generation.

## Quality Layers

`quality_profile.profile_id` is one of `general`, `documentary`, `portrait_editorial`, `product`, `food`, `architecture`, or `nature`.

Use `photographic_integration` to bind subject and setting with believable light, contact, material, or optical depth. Use one visible `visual_proposition`, then at most one or two `photographic_craft` decisions. These are quality signals, so the audit reports omissions as warnings.

`artistic_final_touch` is disabled for most profiles. When enabled, use the sentence or equivalent terms; it does not have to be the exact final suffix. Never add the documentary imperfection formula to product, food, architecture, nature, or polished editorial prompts by default.

## Safety

Default safety is automatic pass with no approval wait. `--safety-evaluation` changes only the report mode and lists evaluated recipe transforms; it does not grant extra authority and does not replace platform or image-tool policy.
