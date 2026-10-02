# Cycle 15 supplemental retrieval review

Status: publication acceptance remains on hold. This diagnostic does not establish that production hybrid retrieval protects the target from the measured lexical loss.

## Reproduction

Run `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/cycle15-hybrid-review/replay.py` from the current workspace. The script reads the immutable cycle 15 baseline/proposal, hash-checks the freeze and production code, independently reruns the exact full-query BM25F ranking, and loads both complete indexes. It blocks network, credential access, embedding API fallback, and the evidence writer. It writes only `result.json` and the redirected log under `/tmp/cycle15-hybrid-review`.

## Exact frozen query

A shopper has put one staple back and paid for fewer essentials. A different sold-out product leaves a separate bare patch on the display; the returned staple itself remains visible in its own spot.

SHA256: `409d4fda2e253764ad43cdf89df4c53d9441d261700f29480585c67cdc2d5fef`

## Verified lexical loss

- Correct reduced-purchase trace: rank 5, score 22.121411454565 -> rank 6, score 22.037665669772
- Unrelated extinguished-flame trace: rank 6, score 22.113405598446 -> rank 5, score 22.113408361609
- Correct-target minus flame score margin: +0.008005856119 -> -0.075742691837
- Correct-target score delta: -0.083745784793
- Flame score delta: +0.000002763163
- Margin delta: -0.083748547956

This is a real unrelated top-five promotion. Unchanged top-twelve membership does not remove it. Both candidates retain identical matched English term sets. The edited target's combined bilingual labels field grows from 34 to 36 tokenizer terms; the flame's field stays 24. The corpus mean labels length changes from 15.716630627088657 to 15.716827206605071. Production BM25F length normalization accounts for field length, so a Korean-only edit can lower an English-query score.

## Production replay boundary

The exact raw query vector is cached with Gemini Embedding 2, 768 dimensions, and verified text/vector hashes. A scan of 32 cache JSON files in the research evidence and daylong workspace finds none of the three default production axis vectors:

1. `A shopper has put one staple back`
2. `product photography, commercial packshot, tactile surface, controlled studio light, object hero image`
3. `the returned staple itself remains visible in its own spot.`

The second text is the production family's canonical expansion, not a reviewer rewrite. A strict call to `make_semantic_context` using the full original query, hybrid mode and default options returns its raw cached vector, then stops at the first missing axis before a shortlist exists. Even the supported nondefault axis-off option requires the uncached canonical product-family text and stops. No missing vector was synthesized, approximated or fetched. No hybrid shortlist is claimed.

The saved V6 scout core is bound to a different shorter grocery request. Its expanded retrieval text is also absent from these caches. It cannot be substituted for a core representing the full coexistence query, and unchanged output from that fixture is not a natural full-query retrieval result.

Production `semantic_weighted_choice` is a metadata/context-weighted semantic sampler; its main weighting formula does not blend raw BM25F scores with cosine. V6 has a separate post-core `candidate_pack_rank_slot_rows` lexical-fusion stage requiring a core, contextual pool, and selected choices. A hand-written dense/BM25 blend would not reproduce either entry point and was not used.

## Embedding task-type caveat

Runtime embedding code supplies `task_type=SEMANTIC_SIMILARITY`; the frozen REST evaluator omits that field. Official Gemini Embedding 2 documentation says task_type is unsupported for this model and task instructions belong in the text: https://ai.google.dev/gemini-api/docs/embeddings#task-types . This is not proof of differing vector semantics. No live SDK/request equivalence test was performed. The definite blockers are unavailable exact axis/core texts and their vectors.

## Consequence for acceptance

The lexical top-five loss remains uncompensated by any demonstrated hybrid protection. Keep the source-consistency benefit separate from unchanged English V6; acceptance needs the parent's actual Korean-output-consumer trace and an explicit root tradeoff decision. Do not claim improved classification: all six frozen near misses still rank first in dense retrieval and some adverse scores increase.

## Subsequent conditional source-compatible lexical bound

`replay_compatible_lexical.py` separately invokes the production `compatible_with_picked` function on all 53 rows, with the real unchanged `pov_food_budget_adult_subject` already picked, `forced=False`, and each frozen complete source state. Exactly the same 12 rows pass in both states. The flame fails its unchanged primary-context guard requiring death_personification, grim_reaper, or mortality; the target passes its food_access_budget_choice_event requirement. No guards were added or changed.

Using the entire unchanged query, production `rank_bm25f` on that compatible pool keeps the target #1 in both states and preserves all 12 positions, including the top five and default 12-result shortlist. Target scores are still 22.121411454565 -> 22.037665669772; corpus filtering does not erase the score decrease.

`replay_quality_overlay.py` repeats this using the real production `load_quality_layers` overlay. It retains the same 12 rows and the same order; no additional exclusions occur. Both scripts prohibit network/API fallback and save complete row-level eligibility audits.

This establishes a conditional source-compatible lexical bound on the flame exposure, not natural selection of the subject, a full hybrid replay, a V6 candidate-pack retrieval run, or adoption. Forced choices and different primary contexts can change eligibility. Raw-corpus rank loss and all unresolved contrasts remain disclosed. Final publication judgment stays with the root's explicit tradeoff review.
