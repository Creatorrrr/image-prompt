# Moe-element supplement did not enrich candidate selection or user-taste interpretation

- Recorded: 2026-08-11 17:54 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Moe Grammar and Candidate-Pack Integration / baseline correction
- Affected scope: `GOAL_PLAN.md`, moe research/element assets, standalone moe planner, subculture illustration candidate-pack and composer integration
- Search terms: moe element supplement, fixed prompt clause, pseudo candidate id, candidate-pack underintegration, preference axes
- Related paths: `skills/subculture-illustration-image-generator/assets/illustration_moe_elements_v1.json`, `skills/subculture-illustration-image-generator/assets/research_evidence_moe_elements/research_v1.json`, `skills/subculture-illustration-image-generator/scripts/moe_element_runtime.py`, `tests/test_subculture_illustration_moe_elements.py`
- Related passed reports: `docs/passed-reports/2026-08-11-moe-element-explicit-supplement.md`

## Failure

- Conditions or trigger: Review the completed supplement against the user's original outcome: research every element and use that research to improve intent understanding, candidate richness, creativity, and reader-taste alignment.
- Expected: Research produces typed variants and preference-aware candidates that participate in the ordinary candidate pack, ranking, composition, and prompt evidence.
- Observed: The implementation preserves 34 origin URLs and 29 element records but gives each element one fixed `prompt_clause_en`. The runtime concatenates those clauses into a separate plan, exposes supplement-local `moe:<element-id>` labels rather than real candidate records, and never changes the existing candidate pack, selection graph, composer, creativity, or preference behavior. Tests replay the generated clause and verify literal containment.
- Impact on the goal: Inventory and provenance work are reusable, but the requested product behavior is absent. The previous goal cannot remain complete.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: current repository inspection at `main@c10becc`; `jq` field inventory, runtime source review, test method review, and `git diff --numstat` for existing candidate-pack assets/runtime.
- Result: 29 elements, 29 fixed prompt clauses, zero `variants`, `research_questions`, `candidates`, `pairing_rules`, or `preference_axes`; no diff in `illustration_runtime.py` or existing mechanism/candidate assets.

## Cause assessment

- Confirmed cause or current hypothesis: A request to reduce excessive validation was interpreted as authority to reduce the product scope. The plan optimized for keeping v1~v3 byte-stable and proving a standalone supplement rather than adding an additive new candidate-pack version.
- Confidence: confirmed
- Remaining unknowns: The exact minimum useful candidate count varies by element; the replacement grammar must be driven by researched semantic subtypes rather than an arbitrary quota.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Explicit-only supplemental plan with one prompt clause per element | 29/29 literal plan tests passed | It proves inclusion, not understanding, candidate richness, preference alignment, or composition |
| Six representative combinations | Concatenated clauses passed | The clauses were not jointly ranked or fused into one scene and did not exercise the ordinary candidate pack |
| Mark the bounded supplement as a passed product integration | Reported active success | Its own excluded scope states candidate-pack schema changes and rendered quality were not included |

## Resolution or next safe step

- Resolution/workaround: Preserved the v1 inventory/replay and added five claim-level dossier shards covering all 29 elements, a deterministic 233-candidate grammar compiler, paired neutral/preference intent corpus, sparse compatibility graph, additive candidate-pack v4 wrapper, preference-axis selector, global one-primary/two-support bundle, shared-event composer, and replay audit.
- Verification: 29/29 neutral requests select their canonical researched candidate; 29/29 paired preference requests select the expected different subtype/key; 6/6 multi-element requests preserve the declared primary and global support cap; 12/12 stored prompt-evidence comparisons pass. Creative cues preserve stored creativity `0.5` while targeting novelty 2. Safety, negative prompt, retry, and photo baseline bytes remain unchanged.
- Next safe step if unresolved: Not applicable to this failure. Pixel quality and blind audience preference remain separate optional work, not missing evidence for the resolved pack/composer defect.

## Reuse guidance

- Avoid: Treating a deterministic literal supplement as candidate-pack integration or prompt-quality evidence.
- Prefer: Research questions -> claim-level provenance -> typed subtypes/appeal mechanisms -> sparse candidate bundles -> actual pack/composer selection.
- Applicable when: A research taxonomy is intended to improve generated content rather than merely document or append terminology.
- Re-check when: Every requested concept has a selected candidate in the real pack and user preference changes are observable in composed prompts.

## Supersession

- Supersedes: `docs/passed-reports/2026-08-11-moe-element-explicit-supplement.md` as evidence of the original user outcome; its inventory/provenance evidence remains reusable.
- Reason: The previous report qualified a narrower supplement prototype while the product-level candidate selection and taste interpretation remained absent.

## Resolution evidence

- Resolved: 2026-08-11 18:50 KST
- Passed report: `docs/passed-reports/2026-08-11-research-backed-moe-grammar-v2.md`
- Key artifacts: `illustration_moe_grammar_v2.json` (29 dossiers, 233 candidates), `intent_corpus_v2.json` (29 neutral + 29 preference + 6 combinations + 12 comparisons), and `qualification_v2.json` (12/12 planning/prompt-evidence PASS).
