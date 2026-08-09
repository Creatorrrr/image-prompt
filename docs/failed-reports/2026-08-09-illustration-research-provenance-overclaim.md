# Illustration research provenance labels exceeded their evidence cardinality

- Recorded: 2026-08-09 01:31 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 2
- Affected scope: normalized research matrices before repository ingestion
- Search terms: illustration provenance, cross-source synthesis, design inference, source cardinality
- Related paths: `GOAL_PLAN.md`, `docs/failed-reports/2026-08-09-illustration-research-schema-drift.md`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Run one root validator across all six normalized packets and require the canonical provenance enum plus two independent source records for every `cross_source_synthesis` mechanism.
- Expected: `source_supported`, `cross_source_synthesis`, and `design_inference` are the only labels; cross-source claims cite both independent sources rather than the topic matrix plus one source.
- Observed: Six mechanisms use packet-specific enums such as `cross_source_design_synthesis`, `cross_source_limitation_synthesis`, or `source_supported_with_caution`. In addition, multiple world/format/adaptation mechanisms are labeled `cross_source_synthesis` while referencing the matrix and only one independent source.
- Impact on the goal: Counts and source URLs exist, but the current labels can overstate how many independent sources support a runtime mechanism. Stage 2 cannot qualify or feed the typed graph until classification is honest.

## Evidence

- Sanitized artifact: read-only aggregate validation of the six `/tmp/subculture-illustration-research-*.jsonl` packets.
- Aggregate before repair: 72 rows, 24 topics, 192 mechanisms; provenance labels included 58 `source_supported`, 91 `cross_source_synthesis`, 37 `design_inference`, 4 `cross_source_design_synthesis`, 1 `cross_source_limitation_synthesis`, and 1 `source_supported_with_caution`.
- Affected packets: character-world has the noncanonical enums; world-cover, commercial-formats, and adaptation-governance contain cross-source rows with fewer than two independent source IDs.

## Cause assessment

- Confirmed cause: Packet-local validators counted the topic matrix itself as a second evidence record and allowed locally descriptive provenance enums. The global contract requires independent source cardinality and a closed enum.
- Confidence: high.
- Unknowns: Each weak cross-source statement must be reviewed by its owner to decide whether it is directly supported by the single source or is an authored design inference.

## Resolution or next safe step

- Do not add or pad evidence IDs. For each weak row, retag to `source_supported` only when the statement is faithfully supported by the cited source; otherwise use `design_inference`.
- Convert a noncanonical cross-source label to `cross_source_synthesis` only when it already cites both independent sources; convert `source_supported_with_caution` to `source_supported` only if the limitation remains explicit elsewhere.
- Resolve only after a root validator confirms the closed enum, nonempty live references, and two distinct independent source records for every remaining cross-source row across all 192 mechanisms.

## Resolution

- Resolved: 2026-08-09 01:36 KST.
- Packet owners reviewed every weak or noncanonical label without adding evidence. Unsupported authored rules were retagged `design_inference`; directly grounded single-source rules were retagged `source_supported`; only mechanisms already citing both independent topic sources remain `cross_source_synthesis`.
- Final aggregate counts are 63 `source_supported`, 72 `cross_source_synthesis`, and 57 `design_inference`. All 192 entries use the closed enum, carry nonempty live same-topic references, and every cross-source entry includes both independent source records.

## Reuse guidance

- Cross-source cardinality must exclude the topic matrix because it is the synthesis product, not an independent source.
- Preserve caution and limitation in statements/boundaries instead of inventing new provenance enum values.
