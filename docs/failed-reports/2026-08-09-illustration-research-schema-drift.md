# Illustration research packets used incompatible mechanism shapes

- Recorded: 2026-08-09 01:22 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 2
- Affected scope: six `/tmp/subculture-illustration-research-*.jsonl` packets before repository ingestion
- Search terms: illustration research schema, mechanisms statement definition, provenance mechanism_id
- Related paths: `GOAL_PLAN.md`, `skills/subculture-illustration-image-generator/assets/`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Independently validate the first two completed four-topic research packets against one canonical schema before copying them into the repository.
- Expected: Every matrix exposes one mechanically consumable mechanism representation and a parallel provenance mapping, so the runtime graph can be materialized without packet-specific parsers.
- Observed: Both packets use mechanism objects plus `mechanism_id`, but the foundations packet stores text under `statement` while the authorial-surface packet stores it under `definition`. The original task described 1:1 provenance but did not freeze the exact mechanism object shape tightly enough.
- Impact on the goal: The research content is preserved, but Stage 2 ingestion and any deterministic grammar builder would require silent packet-specific normalization. That would make evidence-to-runtime provenance fragile.

## Evidence

- Sanitized command or artifact: read-only JSON inspection of `/tmp/subculture-illustration-research-foundations.jsonl` and `/tmp/subculture-illustration-research-authorial-surface.jsonl`.
- Result: all eight matrices use provenance keys `mechanism_id`, `provenance`, `evidence_ids`; foundations mechanisms use `{id, statement}` and authorial mechanisms use `{id, definition}`.
- Second cross-packet result after mechanism normalization: authorial-surface still represents `illustration_evidence` as objects and `format_implications` as an object, while the other packets use ID/string lists; character-world and commercial-formats use `compatibility_rules`/`conflict_rules` while the other packets use `compatibility`/`conflicts`. These are the same insufficiently frozen-shape cause, not separate research failures.
- Unrelated state: `.codex_tmp_composed_gothic.json` appeared concurrently but was not created or touched by the architecture or research agents and is excluded from this failure.

## Cause assessment

- Confirmed cause: The delegated schema required counts and 1:1 provenance but did not specify one exact object key for mechanism text.
- Confidence: high.
- Unknowns: Remaining four packets may use either shape until normalized.

## Failed attempts

- The first root validator assumed mechanisms were strings and failed with `KeyError: 'mechanism'`. This was a validator assumption, not source loss, and no repository evidence file was written.

## Resolution or next safe step

- Freeze one schema before ingestion: mechanisms are `{id, statement}`; mechanism provenance is `{mechanism_id, provenance, evidence_ids}`; candidate definitions and roles remain exact maps.
- Freeze the remaining matrix shapes: `illustration_evidence` is a string-ID list with an exact `illustration_evidence_definitions` map; `compatibility`, `conflicts`, `counterexamples`, `boundaries`, `format_implications`, and `viewer_implications` are string lists. Do not retain packet-specific alias keys.
- Ask all six packet owners to normalize only this shape and rerun their existing structural/provenance checks. Do not rewrite research claims or pad evidence.
- Resolve this report only after one root validator confirms the same schema across all 72 rows and the copied shard hashes match their normalized `/tmp` sources.

## Resolution

- Resolved: 2026-08-09 01:36 KST.
- All six packets now use the exact canonical mechanism, provenance, illustration-evidence, candidate-map, compatibility/conflict, and implication shapes described above.
- One aggregate root validator accepted all 72 records across 24 topics with zero errors; all 264 candidate IDs are globally unique and every illustration-evidence ID resolves to a `visual_atom` candidate.
- The six repository shards are byte-identical to their reviewed `/tmp` sources. Their hashes are recorded in `assets/research_evidence_illustration/manifest.json`.

## Reuse guidance

- For independently authored research shards, freeze exact field names and value shapes, not only semantic requirements and minimum counts.
- Validate the first completed packet before the remaining agents finish so schema drift can be corrected without repository migration logic.
