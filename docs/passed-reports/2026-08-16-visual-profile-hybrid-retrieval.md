# Single-source hybrid visual-profile retrieval preserved exact intent and found paraphrases

- Recorded: 2026-08-16 12:38 KST
- Status: active
- Qualification: resolved-material-failure
- Goal/problem signature: One authored visual-profile registry must drive deterministic exact activation and embedding-only paraphrase discovery after the authorial core is frozen, without turning semantic resemblance into a hard duty or strengthening adult/safety blocking.
- Search terms: visual profile registry v3, registry-bound index, exact plus embedding resolver, optional semantic concept, user definition precedence
- Affected scope: `photo-prompt-image-generator` visual-profile registry, generated index, v5 resolver/projections, validators, audits, tests, and maintenance contracts
- Excluded scope: pre-core meaning interpretation, image generation, pixel-quality acceptance, general semantic-index redesign, and unrelated subculture-illustration baseline repair
- Related paths: `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`, `skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json`, `skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`, `tests/test_photo_visual_profile_retrieval.py`, `GOAL_PLAN.md`
- Related failed reports: `docs/failed-reports/2026-08-16-visual-profile-exact-query-secondary-semantic-leak.md`, `docs/failed-reports/2026-08-16-visual-profile-aligned-user-definition-suppression.md`, `docs/failed-reports/2026-08-16-generic-adult-fashion-visual-profile-leak.md`, `docs/failed-reports/2026-08-16-embedding-positive-blocked-by-lexical-context-guard.md`

## Reproduction context

- Repository/ref or artifact: `/Users/chasoik/Projects/image-prompt` dirty working tree based on `8350aca`; only goal-related photo-prompt paths and reports were changed.
- Commit: Not committed.
- Runtime and dependency versions: Python 3.14.3; Gemini `gemini-embedding-2`; 768-dimensional generated visual-profile vectors.
- External conditions or assumptions: Actual semantic replays used the project's already configured Gemini credential without printing or storing it. Rule-mode exact resolution remains offline. Request meaning and the standalone baseline are frozen before either registry or index is available.

## Successful approach

- Prerequisites: One human-edited registry with exact terms, project aliases, positive semantic material, contrast material, obligations, evidence rules, and render gates; a generated sidecar bound to its canonical SHA-256 and text recipe.
- Sequence: Freeze the independent authorial core; load the registry-bound sidecar; resolve boundary-aware exact evidence and the post-core query vector once; apply exact, negation, requester-definition, context, and adult applicability precedence; project that private typed resolution into obligations, optional concepts, and clarification.
- Decisive choices: Exact hits alone may preserve hard behavior. Embedding-only hits are always optional. Exact profiles still anchor the global semantic score window. An aligned requester explanation preserves its profile, while a materially unrelated definition overrides it. Negative context applies to both lanes; positive literal context is required only for ambiguous exact activation because the embedding score supplies semantic-lane positive proof. The global optional-retrieval minimum is 0.70.
- Avoided approaches and why: No second manually maintained glossary; no embedding-only hard activation; no query-specific blacklist; no creativity-dependent meaning lookup; no pre-core registry access; no new or stronger adult/safety blocker.

## Evidence and completion criteria

| Criterion | Direct evidence | Result |
|---|---|---|
| Single authored source and reproducible sidecar | Builder and validator accept 6 profiles and 27 exact terms; a changed registry hash is rejected; index model, dimensions, text, lookup, and vector cardinality are checked | pass |
| Exact versus paraphrase behavior | Exact `절대공역` replay emits only required `inner_thigh_negative_space`; the descriptive thigh-space replay emits no hard obligation and one optional profile clarification/candidate | pass |
| Real-index relevance | Six valid exact-free full-core positives each ranked and emitted their intended profile; lowest positive score 0.770205. Six adjacent full-core controls emitted no profile; highest control score 0.681438 | pass |
| User and context precedence | Focused tests cover aligned and unrelated definitions, negation, exact context mismatch, and an embedding-only transformation paraphrase; exact hits cannot be resurrected as secondary semantic output | pass |
| Optionality and privacy | Unselected semantic candidates create no obligation or gate; public visual-profile blocks expose no score, vector, rank, matched term, or match basis; candidate-pack audits pass | pass |
| Adult/safety boundary | No blocker was added or strengthened. `여성`, `女性`, `woman`, `women`, and `lady` widen existing adult-context recognition; five existing adult-appeal/render boundary tests plus the allowing-context regression pass | pass |
| Affected regression and integrity | 31 core/prepack/visual tests and 5 adult/contract tests pass; dictionary valid; scene expression 112/112; semantic index 6,513 entries valid; compile, index check, and diff check pass | pass |

## Reuse guidance

- Prefer: One authored registry plus a hash-bound generated index; a single typed resolver; lane-specific positive proof with shared negatives; global ranking reference separate from output eligibility.
- Minimum verification when reused: Fake-vector exact/semantic/negation/definition/context tests, at least one real full-core positive and unrelated control per profile, public-field privacy audit, index-hash check, and affected adult/contract regressions.
- Applicable when: A maintained visual concept has a deterministic shorthand as well as natural descriptive paraphrases and optional composition duties.
- Do not apply when: The meaning must be decided before the core is frozen, the user has not resolved a material ambiguity, or rendered pixels rather than retrieval/prompt contracts are the acceptance target.
- Re-check or invalidate when: Registry semantics, model, dimensions, query recipe, threshold, exact aliases, context-disambiguation fields, or public projection contracts change.
