# Genuine-index identical-query replay

Normal production `load_visual_profile_index` validation passed for both genuine 1,496-entry indexes. BEFORE loaded source/index at 99ebda65 before source application; AFTER loaded refreshed source/index. Every one of the 115 saved query texts, source rows, adult_context values and query_fields was identical between runs. No query embeddings, provider calls, source edits, or synthetic vectors were used in this replay.

## Target results

All 115 target eligibility/status/reason/match-basis projections are unchanged. The three amended positive texts were already BM25F optional and exact required BEFORE the source patch; they retain those outcomes AFTER. Original positive texts remain self-excluded before and after. All 84 guard-lane controls remain target noneligible. There is no demonstrated fixed-query routing gain.

The real improvement is source generation: previously generated original positive descriptions reject themselves; the newly stored replacements yield positive descriptions accepted by existing consumers. That different-text source-derived before/after comparison must not be presented as improvement to the same user query. Original user-authored negated-confound wording remains an unresolved runtime limitation.

## Full hits, order, and scores

Complete hit results differ for all 115 queries because BM25F scores changed. Hit ID membership/order is identical for 111 queries and changes for four boubou controls:

- Query index 75, semantic full positive + `single caftan body`: final two hits swap, y2kr_long_short_layer / bust_prominence_relation → bust_prominence_relation / y2kr_long_short_layer
- Query index 76, same exact-label control: same final-two swap
- Query index 89, missing coordinated_inner_layer: rank-8 pc_pc27_owner_relation is replaced by y2kr_chainmail
- Query index 90, replacement leaf alone: rank-7/8 y2kr_sheer_top / y2kr_cropped_denim_jacket swap

These are genuine collateral lexical-ranking differences, not byte-identical retrieval parity. The boubou target stays absent or noneligible in all four cases. No claim about the visual quality of the alternate tail candidates is made.

For amended positive semantic queries, target rank remains 1 with the same fusion score (0.016393442623). BM25F scores change:
- Ghost: 485.5241605907 → 623.521506865641
- Boubou: 457.546738911857 → 505.210953495646
- Repair: 1183.989999405259 → 1189.775142355803

Higher lexical scores alone are not routing gains or evidence of improved image quality. Complete resolver objects also contain expected changed registry hashes.

## Evidence

- `genuine-index-before-full-resolver.json`: all full BEFORE returns and capture manifest
- `genuine-index-after-full-resolver.json`: all full AFTER returns and validated-index manifest
- `genuine-index-identical-query-comparison.json`: 115 per-query target/hit-order comparisons
- `genuine-index-complete-hit-deltas.json`: every changed hit's exact before/after object, scores and ranks, with frozen query index/text
- `genuine-index-frozen-query-baseline.json`: original control freeze

Earlier lexical-only and proposal diagnostics are preserved separately and have not been relabeled as genuine-index experiments.
