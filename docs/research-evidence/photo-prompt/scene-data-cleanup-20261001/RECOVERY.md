# Recovery

Base commit: `769f005f01fd54e302e0399e44ac1b2b20122c69`
Working branch: `improve/next-slot-data-20261001`
Final dictionary/index hash: `c5bbaf8c6fdace817c1c35f2a90ba9531ff18201d8932e64017401ba0c55ab8d`

The final recovery is cumulative: it includes the preceding 23 unpublished row edits and the additional 14 scene edits, for 37 distinct changed rows. It is intended for a clean checkout at the base commit. Do not apply the cumulative patch on top of the earlier 23-edit patch without checking the working tree first.

Deliverables:

1. `scene-data-cleanup-20261001.patch.gz`: cumulative patch, including current generated semantic-index shards, tests and evidence
2. `scene-data-cleanup-20261001-files.tar.gz`: exact final copies of all changed/new files, with repository-relative paths
3. Recovery manifest: SHA-256 values for every included file, both artifacts and their ordered under-10 MB parts
4. Korean report: scope, before/after retrieval, validation, limitations and conservative cost ceiling

Keep the semantic-index manifest and all 16 referenced shards together. The archive includes the final generation only. The earlier 23-edit recovery archive remains a separate preserved baseline and supplies its original valid index if historical comparison is needed. Existing older generated shard directories can remain on disk; the final manifest does not refer to them.

Concatenate split parts in their listed order before decompressing. Verify the recovered artifact SHA-256 against the manifest. Decompress the patch, run `git apply --check`, then apply it to the base checkout. The producer separately applies the patch in a clean validation directory and verifies every resulting file hash; the file archive is also verified byte-for-byte. The archive is an alternate recovery route, not permission to overwrite unrelated local work.

No `.env`, credentials, editor state, clipboard content, raw authentication responses or unrelated workspace files are included. Applying the saved final index needs no API call. No commit, push, PR, merge or deployment was performed.

Validation completed:

- Existing incremental baseline: 86 tests passed
- Final combined relevant suites: 102 tests passed
- Aggregate dictionary metadata validator: passed
- Production semantic-index loader and BM25F derivation: passed, 9,754 entries
- Independent vector/cache/API-ledger audit: 9,740 unchanged vectors, 14 new vectors, exactly 56 completed unique attempts and no retries
- Independently recomputed all 42 ranks/scores/top-five results in baseline, stage 1, stage 2 and final: no mismatches

The 42 queries were frozen before edits, but are candidate-derived rather than an independent holdout. The 10 probes contain valid alternatives and overlap cases; rank changes are not categorical compatibility decisions. The review-added `blue hour` diagnostic is recorded separately. No rendered-image-quality or full-repository-test claim is made.
