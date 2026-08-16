# Aligned user definition suppressed its exact visual profile

- Recorded: 2026-08-16 11:56 KST
- Status: resolved
- Resolved: 2026-08-16 11:59 KST
- Goal/checkpoint: Visual Profile Hybrid Retrieval Goal / Stage 5 focused regression
- Affected scope: v5 visual-profile exact resolution when an authorial core includes a user-supplied term definition
- Search terms: `visual_profile_user_definition_override_ids`, aligned definition, exact profile suppression, absolute territory
- Related paths: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `tests/test_photo_authorial_core_v5.py`, `GOAL_PLAN.md`
- Related passed reports: `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`
- Resolved by: `docs/passed-reports/2026-08-16-visual-profile-hybrid-retrieval.md`

## Failure

- Conditions or trigger: Generate a v5 pack for an adult fashion request containing the exact project term `절대공역`, while the frozen authorial core also defines that term as true negative space bounded by close upper inner-thigh contours.
- Expected: The user definition, because it agrees with and concretizes the profile meaning, preserves the exact `inner_thigh_negative_space` obligation.
- Observed: The resolver labeled every definition attached to a known exact term as `user_definition_override`, so the hard obligation disappeared even when the definition was semantically aligned.
- Impact on the goal: User intent precedence was implemented too broadly. It protected genuinely different requester meanings but also discarded an explicit, aligned requester explanation, failing the contextual-term regression.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `python3 -m unittest tests.test_photo_visual_profile_retrieval tests.test_photo_prepack_isolation_v5 tests.test_photo_authorial_core_v5 tests.test_photo_visual_obligations tests.test_photo_prompt_contract_v2`
- Result: 96 tests ran in 830.009 seconds; 95 passed and `test_contextual_term_meanings_materialize_without_one_fixed_story` failed because `inner_thigh_negative_space` was absent.

## Cause assessment

- Confirmed cause or current hypothesis: Confirmed by source inspection. `visual_profile_user_definition_override_ids` checks whether the defined term owns an exact profile alias but never checks whether `interpreted_meaning` and `prompt_evidence` agree with that profile's semantic components.
- Confidence: confirmed
- Remaining unknowns: None for the current registry fixtures. New profiles still need both component phrases and literal concept/evidence terms that can establish alignment in rule-mode exact resolution.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Treat every requester definition of a registry-owned exact term as authoritative override | Protects a deliberately unrelated private meaning | Conflates a conflicting redefinition with an aligned explanation that should strengthen the same visual profile |
| Preserve definitions that satisfy the profile component-group matcher | Restored the aligned inner-thigh case and kept the deliberately unrelated definition suppressed | The adult rival definition used two literal profile concept/evidence phrases but did not satisfy a required component-group phrase, so `adult_mesugaki_status_play` was still removed |

## Resolution or next safe step

- Resolution/workaround: Override detection now requires a non-empty supplied meaning that matches neither the profile's data-driven semantic component groups nor its authored concept/evidence terms. Exact term ownership alone no longer implies conflict.
- Verification: Four focused resolver tests and the full contextual-term materialization test passed in 14.537 seconds. The check covers aligned `절대공역`, aligned composite-expression and adult-rival definitions, a deliberately unrelated private definition, adult-context allowance, and negation.
- Next safe step if unresolved: Keep exact activation disabled only for explicitly conflicting meanings; do not infer conflict from the presence of a definition record.

## Reuse guidance

- Avoid: Equating user-provided clarification with user-provided redefinition.
- Prefer: Preserve aligned clarifications, and grant requester precedence only when their supplied meaning is materially different from the registry profile.
- Applicable when: A term registry coexists with frozen authorial-core definitions or provenance records.
- Re-check when: Definition schema, semantic component lexicon, or exact-term precedence changes.
