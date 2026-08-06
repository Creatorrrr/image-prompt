# Subculture surface applicability changed an unrelated golden snapshot

- Recorded: 2026-08-07 01:27 KST
- Status: resolved
- Goal/checkpoint: Photo Prompt Subculture Research Expansion / Stage 6
- Affected scope: generic human presets and deterministic rule-mode generation
- Search terms: subculture surface_material applicability, concept_tracksuit_wizard golden drift, RNG pool expansion
- Related paths: `skills/photo-prompt-image-generator/assets/photo_prompt_subculture_extension.json`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `tests/golden/concept_tracksuit_wizard.json`

## Failure

- Conditions or trigger: Run the full unit suite after loading the new subculture extension.
- Expected: Existing rule-mode golden snapshots remain byte-stable because subculture entries are on-demand only.
- Observed: `concept_tracksuit_wizard` selected an extra `surface_material` and a different pre-existing `contact_point`; the full suite ended with one golden mismatch.
- Impact on the goal: Completion criterion 5 and the closed Stage 6 qualification are not met until unrelated automatic pools remain unchanged.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python -m pytest -q`
- Result: `1 failed, 414 passed, 722 subtests passed`; the only failure was `tests/test_golden_snapshots.py::GoldenSnapshotTests::test_concept_generation_snapshots (case='concept_tracksuit_wizard')`.

## Cause assessment

- Confirmed cause or current hypothesis: The extension appended `human` to the global `surface_material.subject_categories` policy without requiring a subculture domain match. This made the optional slot eligible for every human preset, inserted an RNG decision, and shifted later deterministic choices.
- Confidence: confirmed
- Remaining unknowns: Whether restoring the original generic slot eligibility also restores the full snapshot without any fixture change.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Full closed suite | Exposed one unrelated golden drift | The extension widened global human slot applicability |
| Scoped domain override | Restored all existing golden snapshots and kept subculture surface selection available | Applicable fix; no fixture update was needed |

## Resolution or next safe step

- Resolution/workaround: Kept the existing non-human category list and used `allow_domains_override_subject_categories` only for `subculture_practice` presets.
- Verification: The focused golden replay passed all 5 subtests without fixture changes; the subculture tests, validator, and index check passed; the bounded full-suite repair run passed 414 tests and 723 subtests in 871.27 seconds.
- Next safe step if unresolved: Not applicable. The regression test now asserts generic human domains remain blocked while the subculture domain receives the narrow override.

## Reuse guidance

- Avoid: Extending a shared slot's subject categories when a typed domain needs a narrow exception.
- Prefer: `allow_domains_override_subject_categories` plus a scoped domain so unrelated preset eligibility and RNG order remain stable.
- Applicable when: An additive taxonomy pack introduces a slot to a new subject category only inside its own typed domain.
- Re-check when: Slot applicability merge semantics or deterministic optional-slot ordering changes.
