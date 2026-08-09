# Illustration prompt audit conflated render qualification with prompt evidence

- Recorded: 2026-08-09 02:04 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 3 to 4 boundary
- Affected scope: first implementation of `subculture-illustration-image-generator/scripts/audit_composed_prompt.py`
- Search terms: format evidence, rendered pixel review, prompt audit boundary
- Related paths: `skills/subculture-illustration-image-generator/assets/illustration_format_profiles_v1.json`, `skills/subculture-illustration-image-generator/scripts/audit_composed_prompt.py`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Inspect a real generated candidate pack before composing the 24 frozen prompts.
- Expected: The prompt audit requires only format decisions that can be written literally into a pre-render prompt. Native/thumbnail pixel review remains a later image-qualification gate.
- Observed: `_profile_required_evidence_fields()` treated every format-profile `required_evidence_types` value as a composed `format_evidence` field. The versioned profiles intentionally include `rendered_pixel_review` and `prompt_contract`, so a prompt would have been forced to claim a review that had not happened.
- Impact: A formally passing prompt could imply false post-render evidence and blur the plan's explicit boundary that prompt audit does not prove pixel salience.

## Cause assessment

- Confirmed cause: The audit helper accepted lifecycle evidence categories and typed prompt field names through the same generic accessor.
- Confidence: high.
- Failed artifacts: none. The defect was caught on the first real pack before any of the 24 composed qualifications was accepted.

## Resolution

- Resolved: 2026-08-09 02:04 KST.
- The audit now consumes only `format_profile.required_format_evidence_fields`, whose keys describe literal crop, hierarchy, text-space, sequence, or scale behavior for the selected variant.
- `required_evidence_types` remains in the profile for asset and post-render lifecycle metadata but cannot be asserted as prompt proof.
- A follow-up bypass check also rejects lifecycle/post-render keys injected into composed evidence, completed-render PASS language in `prompt_en`, and packs that expose lifecycle fields as visual or format composition requirements.
- Re-run the audit self-test, the 24 composed prompts, and the later six native/thumbnail/crop reviews as separate gates.

## Reuse guidance

- Never use a generic “required evidence” list across pre-render prompt contracts and post-render qualification. Name the phase-specific field explicitly and keep pixel review outside prompt metadata.
