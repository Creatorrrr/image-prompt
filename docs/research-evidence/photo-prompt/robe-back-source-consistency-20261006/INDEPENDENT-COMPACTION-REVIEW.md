# Independent review addendum: compact V32 provenance

**No unresolved findings remain in the final compact-provenance change.** This addendum reviews the change from frozen local commit `2447796539462a8d19386fca5a48a00d0c56d818`; it supplements the earlier V32 code review rather than relabeling its hashes or test results.

## Preservation and verification

- The 1,767-byte summary independently matches the preserved 4,245,895-byte table: all 12,589 ordered records, both changed records, corpus counts, exact original-byte SHA-256, and canonical ordered-table SHA-256. The full original table remains preserved locally and can be reconstructed using committed source evidence.
- The final offline checker reconstructs original/current canonical text, supported index payloads, vector coordinates, ordering, and complete unchanged entries. It reproduces both original-table digests without provider, network, runtime-store, or Git operations. Its temporary source views use same-filesystem hardlinks without writing their contents; the historical materializer continues to create independent copies.
- The reviewer independently confirmed that the photo DATA, indexes, runtime, and candidate pack are unchanged from the frozen local commit. Validator, recovery fixtures, and V32 baseline differ only by one proof-hash replacement each; the universal descriptor differs only by the validator hash. Proof changes are limited to the compact-summary digest and the new checker digest.
- Independent negative probes corrupting the summary, reviewed index proof, and current-source binding map all reject at fixed digest pins before importing the local generator. Final full reconstruction passes. The implementation's three final affected boundary, descriptor, and current-CLI tests also pass on the final hashes.

## Review findings resolved

The initial checker relied on mutable evidence maps as standalone trust anchors. It now pins the compact summary, reviewed index proof, original parent manifest, and canonical current source/shard map before importing local generator modules. This avoids circular checker/proof hashing while authenticating the complete source set.

One intermediate checker run rejected legitimate derived metadata. Independent comparison found only ordinary `bm25f_document` and visual `text_sha256` changes beyond the reviewed text/vector pair. The final checker permits only those corpus-specific derived fields, rebuilds/validates BM25F against canonical source, explicitly checks both visual text digests, and requires all remaining fields to be exact. The failed intermediate run remains recorded; it was not a DATA defect or a successful qualification.

The earlier V32 aggregate later completed with 45 of 46 test methods passing and four failed rollback subcases in one method. Those failures were covered by the already-reviewed guard correction; the affected final-helper rerun passed 20 of 20. This compaction does not claim a new full-suite run: validation here is the exact mechanical-change audit, independent negative probes, full provenance reconstruction, and three affected tests.

## Final reviewed SHA-256 identities

- Compact summary: `ddb901fd18d5bab666a4aa8426371fbbfd91bbb260d3626adebc0a33b47e7504`
- Reproducer: `44fb66cbf1504cf344b1b4a38b1d22f9faa554a2eca3af330584735b7b14ee02`
- V32 proof: `5142254443a263dae0d6f90c11fa8d97184f68b3b7cd31c441cd94a00f6b3c8b`
- Validator: `63914fc5e0c75a2b6fe5e5ee1a1072ce5264b442bb6235484cccecd006f4998d`
- Recovery fixtures: `1096a7b528684e3b608e6cb9ed24c05906dd6f99e67918875e02390b0dd77734`

This review establishes no additional provider attestation, source research, retrieval benefit, image-quality gain, or publication status. The earlier source-quality limitations remain applicable.
