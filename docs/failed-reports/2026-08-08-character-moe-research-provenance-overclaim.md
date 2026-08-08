# Character-moe research packets overclaimed provenance and collapsed typed concepts

- Recorded: 2026-08-08 01:42 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Moe and Subculture Character Grammar / Stage 2
- Affected scope: six 24-topic research packets before ledger ingestion and runtime taxonomy implementation
- Search terms: character moe evidence provenance, CJK term overclaim, adult morphology inference, composite candidate IDs
- Related paths: `skills/photo-prompt-image-generator/assets/research_evidence.jsonl`, `skills/photo-prompt-image-generator/assets/character_moe_topic_crosswalk_v1.json`, planned character-mechanism extension

## Failure

- Conditions or trigger: Independently audit the six completed `/tmp/character-moe-research-*.jsonl` packets before appending them to the evidence ledger or converting candidate IDs into runtime data.
- Expected: Each matrix distinguishes source-supported findings from cross-source synthesis and design inference; multilingual term claims are source-traceable; adulthood is explicit metadata/context rather than morphology; runtime atoms keep non-equivalent concepts typed and separate.
- Observed: Four high-severity issues remained: matrix rows visually attributed cross-source synthesis to one source; unsupported Korean `모에` and Chinese `萌` lexical notes and an overstated KOCCA repost source type; two morphology-based adulthood phrases; and composite root IDs combining transformation/genre, nonhuman morphology/personification, SD form/mascot role, companion/familiar/mascot role, or masculine/androgynous/audience affect.
- Impact on the goal: Stage 2 cannot pass, the 72 records must not enter `research_evidence.jsonl` unchanged, and the affected composite IDs must not become runtime atomic candidates.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: independent read-only audit of all 72 rows plus canonical-source and current-asset collision checks; full temporary report at `/tmp/character-moe-research-independent-audit.md` during this run.
- Result: `FAIL pending revision`; critical 0, high 4, medium 6. Mechanical structure passed: 72 rows, 24 topics with 3 rows each, 24 rich matrices, 72 literal URLs, all array minima, 181 safe-syntax candidate IDs, and no positive youth sexualization or candidate-level protected-name leakage.

## Cause assessment

- Confirmed cause or current hypothesis: The research contracts optimized for topic coverage and rich design matrices but did not require claim-level provenance roles or typed separation between research routers and atomic runtime concepts. The adult-default guard was also expressed partly as an appearance heuristic instead of explicit subject metadata and life context.
- Confidence: confirmed
- Remaining unknowns: Whether replacing the duplicate Ego4D and duplicate JSSD records while retaining three independent authoritative URLs per affected topic will require new public research.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Six parallel 4-topic research packets | Produced complete 72-row structural coverage | The schema allowed a single matrix source field to appear to support cross-source synthesis and allowed composite router IDs among candidate IDs |
| Independent pre-ingestion audit | Correctly failed with four high issues | This is the detection step; no revision had yet been applied |
| First bounded revision and independent re-audit | H2, H4 and most H1/H3/schema checks closed; two residual classes remained | One pose policy had an empty evidence list, seven `cross_source_synthesis` entries named only one record, three `source_supported` statements also contained authored realization policy, and two adult-context definitions retained a numeric `18-plus` threshold despite the binding non-numeric adulthood contract |
| Second bounded repair and final independent gate | Passed with critical 0, high 0, medium 0 | Exact provenance classifications/references and the two numeric adult declarations were corrected without adding irrelevant evidence or weakening a criterion |

## Resolution or next safe step

- Resolution/workaround: Normalized all 72 rows to `topic_matrix|independent_source`; added source-specific dimensions, exact synthesis links, mechanism-level provenance, candidate/photo definitions, corrected CJK source authority and routable terms, replaced canonical duplicates, removed morphology/numeric age inference, and split composite research roots from typed runtime atoms. Stored the qualified packet as six ordered evidence shards with a hash/count manifest.
- Verification: Independent final gate passed with critical 0, high 0, medium 0. It verified 72 rows/24 topics, 194 mechanism provenance records, all 53 cross-source syntheses using at least two distinct evidence records and URLs, canonical dedupe against the existing 180-row ledger, explicit non-numeric adult declaration, typed composite boundaries, candidate/photo/support consistency, and citation-only protected names.
- Next safe step if unresolved: Not applicable. Any future row must preserve the same provenance, adult-declaration, dedupe, and typed-router contracts.

## Reuse guidance

- Avoid: Treating a rich matrix's single `source_url` as provenance for every synthesized mechanism or turning a broad research topic name into one runtime atom.
- Prefer: Claim-role labeling, explicit synthesis links, source-specific dimensions, nonvisual market-term provenance, explicit adult context, and typed orthogonal runtime axes.
- Applicable when: Multiple sources and design inferences are compressed into an executable taxonomy or multilingual routing layer.
- Re-check when: The evidence schema, candidate crosswalk, or character-mechanism graph is changed.
