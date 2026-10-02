# Matte-soft optional candidate collateral

## Finding

A real, unrelated optional candidate changed at the top-eight BM25F cutoff. This is not evidence that retrieval relevance improved. Both the old textile candidate and new seated-body/cushion candidate lack the owner context in this plaster still life.

Exact eligible BM25F ranks and scores:

| Profile | BEFORE rank | BEFORE score | AFTER rank | AFTER score |
|---|---:|---:|---:|---:|
| y2kr_velour | 8 | 128.270476041874 | 10 | 125.301511993474 |
| rb_support_compression | 9 | 127.738935810214 | 8 | 127.778074503079 |

The candidate limit is eight. The selected rank-eight entry's RRF score is 0.014705882353 in each version. In both actual resolver executions, BM25F was evaluated and embeddings were not; the new vector values do not cause this particular swap.

## Actual context and eligibility

The unchanged request is: “Photograph a dry plaster pear on matte paper with large-source soft wrap relation; preserve both dry diffuse surfaces.” The baseline contains a plaster pear, paper, diffuser, tabletop and lighting. There is no human, adult, clothing, textile pile, cushion, or seated action. “Rounded body” refers to the pear. The embodiment review explicitly says no person or animal body action is depicted. The resolver reports `adult_context=false` before and after.

- `y2kr_velour` describes a dense short textile pile, shade changes and diffuse sheen
- `rb_support_compression` describes a seated body on a soft cushion, load-induced depression, and clothing folds
- Both source profiles set `requires_adult_character=false` and `semantic_discovery_requires_component_evidence=false`
- Neither has a component-semantic match to the frozen context
- Both are structurally context-eligible for advisory retrieval; neither is exact-matched or hard-eligible
- BEFORE actual selected hit: velour, `match_basis=bm25f`, `optional_eligible=true`, `hard_eligible=false`
- AFTER actual selected hit: support compression, same advisory/hard status

These are permissive existing advisory boundaries, not proof of scene suitability. Adding a new adult restriction is neither proposed nor needed to repair the source-material defect.

## Why the scores changed

Frozen query fields, both candidate source profiles and both indexed BM25F documents are identical before/after. The reviewed lighting text changes global corpus statistics:
- document frequency for `diffuse`: 7 → 9
- `the`: 1183 → 1184
- `with`: 490 → 491
- average indexed field lengths also change (exact before/after values saved)

The ranker uses these statistics for IDF and length normalization. Velour's matched terms include `diffuse`, `soft` and `changes`; support compression matches `body`, `contact`, `soft`, `relation` and other common terms. The global score shift crosses the advisory cutoff. This explanation is grounded in actual unchanged documents, recorded global statistics and the production ranking formula, not a vector similarity claim.

## Hard-contract and adoption impact

The entire slots object is identical. Slot candidates remain optional and no composed adoption occurred in these runs. The frozen core is identical. The ordered hard-gate IDs are identical; the only hard profile remains `soft_light_shadow_edge_relation`, with the intended reviewed material-response changes. Neither incidental candidate adds any current hard gate or prompt duty.

Risk remains nonzero: the new optional suggestion contains a person/cushion/clothing scene and would be inappropriate to adopt into this fixed still life. The public contract says unselected candidates add no duty, but selecting one promotes its opt-in obligation to hard status. This warrants disclosure as advisory retrieval noise; it must not be described as “no collateral change.” No wording or rankings were tuned to preserve the old unrelated near-cutoff candidate.

## Reproduction and preservation

`probe_collateral.py before` and `probe_collateral.py after` use the genuine frozen source/index snapshots, original immutable inputs, current production source preparation/resolver, and production BM25F ranking. No index/vector fabrication, monkeypatch, provider call or repo mutation. Full actual resolver returns, scores, matched terms, eligible ranks, input context and corpus statistics are in `before-rank-proof.json` and `after-rank-proof.json`. `impact-and-statistics.json` verifies unchanged slots, cores, candidate documents and hard-gate IDs.

Original public comparisons remain untouched. This report is additive and scoped only to the observed matte-soft English collateral swap.
