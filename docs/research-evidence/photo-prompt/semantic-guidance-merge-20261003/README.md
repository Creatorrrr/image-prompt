# Contextual visual semantics and upstream relation fixes: merge evidence

This merge preserves the locally authored contextual/body/garment semantics and
the upstream capture, lighting, composition, instrument-hand-role, and panning
corrections. Runtime selection and skill logic are unchanged by the merge.

## First merge

- Local parent: `0adb5f6e56416e2656dfb4150d0724867530c2bc`.
- Remote parent: `57e29730f0b5c2df336fd1e9dd58374b2025ee03`.
- Common ancestor: `0ed2267b91e73f4b4d1493d095287e7795ebf805`.
- The main registry's 19 local and 14 remote modified profiles have disjoint IDs.
  Structured three-way merging retains complete records from the correct parent.
- All 550 exclusively changed parent files were initially preserved exactly.
  One historical regression test then needed a compatibility adjustment: it now
  asserts the six new instrument label/text values and every untouched field
  before projecting the historical rows. The frozen fixtures, whole-dictionary
  comparison, and 21 historical keep assertions remain intact. The other 549
  exclusively changed parent blobs remain byte-for-byte identical.
- Derived indexes contain 9,700 semantic entries, 1,496 visual profiles, and 3,624
  exact lookup terms. Exact-text parent vectors were reused only when provider,
  model, dimensions, and text agreed; shared vectors were checked for equality.
  BM25F was rebuilt from the merged source. No embedding calls or historical
  shard deletions were needed.
- The initial suite recorded 122 passing tests and 1,095 passing subtests, with
  one failure from the outdated historical label expectation. After the scoped
  test repair, all 11 liminal/instrument regression tests passed. Initial and
  repaired outputs are both retained. The final upstream catch-up is verified
  separately against its final source and indexes.
- Dictionary and visual-index metadata validation passed. `verify_merge.py`
  checks staged parent/source/derived bytes, whitespace, conflict resolution,
  test results, commit parents, staging scope, and unpublished blob sizes.

Concurrent expression-research documents were left unstaged in the worktree.
No image generation or pixel-quality validation was performed for this merge.

`source-preservation.json`, `index-reconciliation.json`,
`test-compatibility.json`, and `final-validation.json` record exact provenance.
`reconcile_merge.py` can write an additional merge's evidence to a separate
directory using `--output`; it never fetches embeddings or prunes old shards.
