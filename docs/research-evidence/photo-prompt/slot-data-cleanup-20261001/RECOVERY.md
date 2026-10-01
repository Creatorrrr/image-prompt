# Recovery

Base commit: `769f005f01fd54e302e0399e44ac1b2b20122c69`
Local working branch: `improve/next-slot-data-20261001`
No push, pull request, merge to main, or deployment was performed.

Two recovery artifacts are produced outside the repository:

1. `slot-data-cleanup-20261001.patch.gz`: complete patch for the base commit, including generated index shards, tests and evidence
2. `slot-data-cleanup-20261001-files.tar.gz`: final copies of the changed/new files with repository-relative paths

Use a clean checkout at the base commit. Decompress the patch, run `git apply --check`, then apply it. Keep the semantic index manifest and all of its referenced shards together. The file archive is an alternate recovery source, not a command to overwrite unrelated work.

The adjacent recovery manifest records SHA-256 values for every included file and both artifacts. No `.env`, credentials, session state, raw auth logs, or unrelated workspace files are included.

Final validation uses the project's dictionary validator and these unittest modules:

- tests.test_photo_next_slot_data_cleanup
- tests.test_photo_slot_data_cleanup
- tests.test_photo_slot_rank_regressions
- tests.test_photo_slot_pipeline_regressions
- tests.test_photo_bm25f_retrieval
- tests.test_photo_loading
- tests.test_photo_lighting_visual_semantics
- tests.test_photo_portrait_composition_semantics

The report and JSON evidence distinguish full-slot lexical/dense retrieval from final candidate-pack and image quality. Query vectors are included to avoid repeat API requests; they contain only the authorized project evaluation text and returned embedding values.
