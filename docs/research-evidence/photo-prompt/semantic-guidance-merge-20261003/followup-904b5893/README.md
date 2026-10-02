# Latest upstream catch-up

The first merge's local contextual/body/garment improvements and upstream
capture, lighting, composition, panning, and instrument-hand-role corrections
are retained. This follow-up also incorporates upstream commit
`904b5893c94e2d59d646e977c8400e270635a568`, which repairs positive component
bundles that could reject themselves through their exclusion guards.

- Local merge parent: `f9fb4c2902cbcb603f07923b207a867c297b48e8`.
- Latest upstream parent: `904b5893c94e2d59d646e977c8400e270635a568`.
- The 19 locally modified main-registry profiles and 6 newly modified upstream
  main-registry profiles have disjoint IDs. The poverty-extension repair is
  retained byte-for-byte from upstream. All 527 exclusively changed parent
  blobs are preserved, including the first merge's bounded historical-test
  compatibility repair and its immutable initial/repaired test evidence.
- `integrated-parent-proof.json` checks the entire main registry and raw tag
  dictionary against a direct three-way merge of the original local parent
  `0adb5f6e56416e2656dfb4150d0724867530c2bc`, latest upstream, and original
  common ancestor `0ed2267b91e73f4b4d1493d095287e7795ebf805`. Both match exactly.
- Runtime scripts and `SKILL.md` files are unchanged from the original local
  parent. Advisory retrieval and context-specific hard activation retain their
  existing behavior.
- The final indexes contain 9,700 semantic entries, 1,496 visual profiles, and
  3,624 exact terms. All 9,700 semantic vectors were reused; 7 visual vectors
  came exclusively from the latest upstream cache, 101 exclusively from the
  local cache, and 1,388 were identical in both. Cache misses, embedding calls,
  and historical shard deletions are zero. BM25F reflects the merged source.
- Dictionary and visual-index metadata validation passed. Final test and
  staged-byte verification evidence is retained in `merged-tests.log`,
  `merged-tests.xml`, and `final-validation.json`.
- The final focused suite passed all 127 tests and 1,144 subtests in 379.96
  seconds. It covers contextual activation, profile retrieval, clothing/body
  semantics, portrait exposure, character concepts, BM25F, semantic metadata,
  historical liminal preservation, instrument hands, lighting/composition,
  capture boundaries, panning directions, and the additional positive-bundle
  self-exclusion repairs.

Concurrent expression-research work remains unstaged and is excluded from the
merge. Image generation, pixel validation, and a full repository test run are
outside this focused merge verification.
