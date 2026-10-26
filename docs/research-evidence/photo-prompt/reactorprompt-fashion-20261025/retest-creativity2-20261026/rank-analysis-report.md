# Creativity-2 fashion retrieval diagnosis

**Scope.** Read-only diagnosis of the three scope-corrected retests and the frozen, bounded query replays. The older `pixeltest-20261026-faea2e` run is historical and is not used to explain the latest result. This audit did not inspect new creativity-2 author cores/prompts, modify indexed data/code/configuration, run a managed retrieval/sampler, activate a generation, or call image/paid APIs.

## Finding

There is no evidence of an index-membership or slot-prefilter defect. The eight alias-enriched candidates are in the selected H2 full pool and each has five alias strings in its native search fields and H2 indexed document text. The actual 42 issued queries—42 includes all slot queries plus `__request_topic__` and `__baseline_prompt__`—were searched over all 24,076 CIDs / 24,078 RIDs. The aliases are simply ranked too low for these query texts: all eight are outside rank 96 even when ranked against every actual query; their all-query best ranks range from 368 to 2,212. Therefore the creativity-2 rank-96 window cannot recover any of them without changing query text or retrieval ordering. Changing the sampling seed or sample budget alone cannot recover a candidate outside the window. Their best bound-role ranks span 368 to 9,714.

A second, distinct path explains zero new-cohort prompt contribution. The broader 2,430-candidate cohort entered the rank-32 window 21 times; five distinct records made the actual sample, but all five were rejected at source/scene review. Those are not the eight alias-updated records, which had zero rank-window and sample appearances. Thus alias candidates fail before sampling; the five other sampled records reach selection but fail there.

## Evidence from the actual retest

The saved H2 material files and raw NPZ rankings were verified against their recorded hashes and the pinned full generation. For every target CID, the table gives the best rank among its bound-role queries and the best rank among **all 42** queries. The latter includes cross-role and whole-scene queries; H2 does not prefilter by slot.

| Updated candidate | Bound-role minimum | Best over all actual queries |
|---|---:|---:|
| `cand_026cebb91f745dabb949dbec768dea32` — chunky-sole suede loafers | footwear 368 (C) | footwear 368 (C) |
| `cand_2302d2f7a43055ab81cc122214364021` — white back-button rib-knit top | garment detail 416 (C) | garment detail 416 (C) |
| `cand_628df9d6b064532fbd1dd7411f91a005` — grey wool herringbone maxi coat | surface material 583 (C) | surface material 583 (C) |
| `cand_67e5450849b552f8bd0bfd67ddfd29d3` — white tweed blazer with gold buttons | garment detail 2,101 (C) | motion rendering 1,860 (C) |
| `cand_6df1973e91225acaadfac7be4e132b0b` — white poplin shirt with rolled sleeves | garment detail 7,876 (C) | motion rendering 2,212 (C) |
| `cand_96b9a5c51f925b58a1e8d7780432afd0` — oat-beige cashmere sweater | surface material 1,111 (C) | surface material 1,111 (C) |
| `cand_b96641e3ab0250c58682ab91a2bfd999` — oversized cream-ivory rib-knit pullover | garment detail 9,714 (C) | surface material 1,345 (C) |
| `cand_d791481a79c852eb829d2711b76075e9` — fitted pale-pink rib-knit top | wardrobe style 2,513 (A) | baseline prompt 1,026 (C) |

The scoped retest accounting is 336 sampled material occurrences / 193 unique CIDs. New-cohort exposure was 21 rank-window occurrences, 5 sample occurrences / 5 unique CIDs, 0 retained prompt clauses, and 0 native adoptions. The 8 updated alias candidates had 0 rank-window and 0 sample occurrences. The 5 sampled new-cohort candidates and their actual fused ranks / lane evidence were:

| Case / query | CID | Full fused rank | BM25 score (rank) | Dense cosine (rank) | RRF |
|---|---|---:|---:|---:|---:|
| B / color | `cand_782c9bfd247657318a4078621b0acf4d` | 28 | 3.8993 (10,406) | 0.7260 (13) | 0.043574 |
| B / request topic | `cand_ef2c6f14ae895e1d9208b3a0f974ee23` | 23 | 10.8308 (9) | 0.6993 (3,191) | 0.052944 |
| C / garment state | `cand_b7a7e624ecf05558a9d0389e56f77fd7` | 2 | 13.1807 (632) | 0.8082 (1) | 0.092467 |
| C / surface material | `cand_423e108089215e7e98e6aeaf0d49291c` | 16 | 21.5717 (10) | 0.7086 (105) | 0.058696 |
| C / surface material | `cand_d9b8c6aaf6a35f84a9892905c4d21a87` | 1 | 9.2633 (1,026) | 0.7460 (1) | 0.091874 |

The saved decisions reject these for distinct, source-grounded reasons: an unrequested scarf competing with the chosen palette; an unsupported adult-specific bra; a walking coat conflicting with the still-wait scene and carrying an adult condition; wet clothing not established by a wet platform; and a dark sweater that weakens the selected coat/top contrast. Those are selection outcomes, not missed sampling. No relaxation of source conditions or forced inclusion is indicated.

## Why the alias text and actual role queries diverged

The H2 generation does index aliases (`aliases` field weight 4), but the actual role query strings are mostly generic task descriptions. For example, C garment detail says the current coat/top/trousers are “replaceable examples”; C material makes the baseline wool/knit and rain-dark platform “optional”; A detail asks for any visible construction/local-form detail; B material searches clothing **or** environmental surfaces. The target aliases instead encode compact, specific propositions such as a back-button rib-knit top, a white tweed blazer with gold buttons, or a maxi grey wool coat with herringbone weave. They consequently have little lexical overlap with a generic duty or with a different baseline garment, even though all aliases exist in the indexed text. Cross-role results do not fix this: the best any-role rank for some candidates is still 1,026–2,212.

This diagnosis is supported by the ranking implementation, not inferred from absent `bm25` fields. Each H2 result stores BM25 score/rank, cosine/rank, and RRF. The sealed code uses BM25F field weights, local cosine, and reciprocal-rank fusion; it evaluates the full RID pool, deduplicates to CID order, then applies witnessed order/projection and sampling. Alias weight is 4; RRF uses `k=10`. Actual sampled rows above show the separate lanes. In the 42 saved queries the query-scope witnesses show no correction, literal, focus, or phase ordering/filter that could explain these eight candidates being removed before scoring.

The sealed query constructor forms slot text as `Photographic role: <role_focus>` plus `Scene context: <scene_context>` and also issues the two full-scene queries. The sampler is downstream: creativity 1 uses rank window 32 and sample limit 8; creativity 2 uses rank window 96 and sample limit 12. Its algorithm keeps rank-1 as anchor and uniformly samples the remaining budget from the rest of the window. The source file and saved receipts show no CID/topic quota or seed-based target preference.

## Bounded counterfactual and fixed query checks

A nine-query, three-per-arm diagnostic was frozen before its search, using only the prior cases’ own baseline garments/materials and scene facts. The comparison reuses the exact old query vectors and locally encodes only the nine rewritten queries with the same local EmbeddingGemma2 binding; both sides use the same sealed e8d4 full pool and unchanged H2 scoring. It is exploratory, not a quality benchmark, and query drafting was not blind to the earlier alias inspection.

For the nine original query texts, no target is in top 96. For the nine baseline-grounded rewrites, only `cand_628df9d6b064532fbd1dd7411f91a005` enters top 96: rank 66 in its own C surface-material query and rank 92 in C garment-detail (cross-role). No target reaches top 8 or top 32. This is evidence that concrete role-local garment anchors can materially change retrieval rank, but it is not evidence that a candidate will be sampled, selected, adopted, or improve pixels. The C fit rewrite also shifted top-8 away from trouser-fit sources toward transit/action sources, so the change is not uniformly beneficial.

The old C surface-material query is also an exact replay of the saved actual query, not a re-encoded substitute: its text SHA is `92967eb1c2da9dec72b8fed6c39808b3094e0642b273b627513e5484c61960d3`, and its cached local vector SHA is `5b583bd6c52fa6b79212106caaf73aa98bbbf94a8f8d66fa3fb410043dec2155`. Reading the actual saved NPZ full order and score arrays confirms that the herringbone-coat CID `cand_628df9d6b064532fbd1dd7411f91a005` is rank 583 in both artifacts, with identical BM25 and cosine values. The rank-489 entry is a different CID, `cand_2302d2f7a43055ab81cc122214364021` (the white rib-knit top); its best rank across all actual queries is 416 in C garment detail. These different CIDs/rank scopes explain the apparent discrepancy.

Separate fixed retrieval checks provide a useful sanity check, not proof of broad success:

- The frozen natural46 suite has 3 successor top-8 appearances across 2 target IDs; 43/46 top-8 orders equal the selected a55 baseline, and every saved baseline replay matches.
- In the 16-query general/control suite, five target IDs appear in positive-query top 8; four control top-8 orders remain identical. Two query-level target appearances are new relative to the old-alias baseline: `cand_b96641e3ab0250c58682ab91a2bfd999` is rank 8 for “Show a roomy pullover with a knitted surface” (BM25 12.7566/rank 13; cosine 0.7731/rank 14; RRF 0.085145), and `cand_6df1973e91225acaadfac7be4e132b0b` is rank 5 for the Korean rolled-sleeve shirt query (BM25 25.0465/rank 4; cosine 0.7583/rank 34; RRF 0.094156). These confirm that the revised aliases can affect targeted natural-query retrieval; they do not change the three retest’s zero prompt contribution or establish quality.

## Minimal next change and validation

The minimal general change is query authoring, not a ranking or sampler exception: after the concept is frozen, phrase each searched visual role around the actual garment/form/material and the visual property that role should show, grounded in that arm’s existing baseline. Keep scene context concise. Keep optionality, requester constraints, source guards, and agent workflow instructions in their existing fields; do not make them positive visual search text or imply the baseline garments are locked. Do not copy a whole baseline into every query. The process-only guidance update in the skill already points this way; this audit does not edit it.

Candidate authorship should remain source-faithful. Compact common garment/material terms and natural EN/KO variants can improve ordinary queries where supported, but aliasing should not imply that a specific item belongs in a different chosen scene. When the retrieved source introduces a conflict, preserve the skip. Do not raise the window/sample size as a substitute for relevant rank, force a CID/cohort, reroll a seed to shop for exposure, or bypass source/selection guards.

For a fair next retrieval-only check, preserve this finite suite and add an arm-local set of concise role queries before looking at their results; use the same pinned full-pool scorer and report top-8/32/96, the selected sample, and every candidate decision separately. Include non-fashion controls and compare source relevance across all roles, not only changed aliases. Only claim prompt contribution when a source-backed new clause is actually present in the final prompt; assess pixels separately. The nine-query diagnostic here is a feasibility signal, not a release or image test.

## Reproduction pins and evidence

- Installed H2: `e8d4f9039129c78559622bbe9fc1779a96a9f68c266ae90312b72ab9af82806f`; native: `7c878e032ac2f2ac1c3e3e468e1be591ba22946d63f52fb58de908dd61767d1f`; code: `9fae54abf63e20b5cd9e542fead3f6ac03572297d27821830066b794174cc8e6`. The diagnostic loaded the full generation and verified the local query encoder binding; paid API calls 0, image calls 0.
- Three actual material files (case A/B/C) were hash-checked in place by the diagnostic; their recorded canonical hashes are `af665e40709c9ecf3783dcf08d038a79e04520a41d78cee742578b9ab6ef689c`, `9a952551697544266fc9cb0e602445985b2c36ae9e799a7b478a168c5cbf7690`, and `f0eb81f11c70bd355958e1cf681ea08e20e30e4967af32554b35709d3387ac32`.
- Retest receipts: `generated/photo-runs/reactorprompt-fashion-retest-20261026/FINAL.json` SHA `33173d7397a38c73e90437cdfecce1ab178807e652b745454103b7b75c3d5594`; `MATERIAL-USE-AUDIT.json` SHA `66068c427e706a36035e81e3dbede34d011f61717b72c4d640d2028ee0cf3a0f`; `SAMPLING-COVERAGE.json` SHA `d831a38d318bbec8e81f115459117616bad9da018dae2ac571a5fc14a97e5a78`.
- Counterfactual suite SHA `41d3ece7aa3f5b78184c371f36c33f7860c535de7d4b91b4043bc873652aee1c`; full-rank diagnostic SHA `5457167e2389ef103a2ae3e2849e0555d4b04b6d60c4e1701b14c8502931a5f7`.
- The natural46 and general/control receipts are `generated/trend-scout/raw/reactorprompt-fashion-remediation-20261026/runtime/bounded-query-verification.json` SHA `18dd2733d89ca8e82a0f87e38413b251f907b4e14bcccde0aaf92af36bbd4c8c` and `general-control-query-replay.json` SHA `e518e2352a88872865764c6097fc65db7e3a11a11051a336f63b52157778178e`.
- Owning sealed source files: `generated/trend-scout/raw/reactorprompt-fashion-remediation-20261026/runtime/stage/07dc8e671afaed7f6ef1a74966107c7dff2a143087eaeb3df4bd774098fa4e1d/successor-skill/scripts/photo_h_f2_queries.py:41-60`, `photo_h_f2_generation.py:14-16`, `photo_h_f2_search.py:10-25,28-45,64-99`, `photo_h_f2_sampling.py:5-43`, and `photo_h_f2_workflow.py:34-61`.
