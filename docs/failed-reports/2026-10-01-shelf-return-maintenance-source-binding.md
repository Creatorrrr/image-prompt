# Shelf-return source maintenance binding

- Status: resolved for maintenance source binding; independent baseline image-artifact limit retained
- Observed UTC: 2026-10-01T23:20:40Z
- Scope: photo_prompt_poverty_extension.json Korean returned-item state correction
- Expected: unchanged external maintenance contract hashes current authored source
- Observed: existing test_maintenance_record_is_external_hash_bound_and_source_bound rejected old c5b20d… digest versus corrected-source 27067e… digest
- Reproduction: run the unchanged test against the measured ko-only proposal
- Cause: high confidence. The ko edit changes the authored source while the original maintenance_ref still points at its historical record
- Failed attempts: one existing contract test; no paid request and no publication
- Next safe step: preserve original record; clone a versioned record changing only record_id and authored_source_sha256; bind current source to it. Preserve original experiment freeze and measurements, amend only raw metadata replay
- Reuse: authored-source maintenance hashes must be renewed after source edits. Do not overwrite historical records or relax existing binding fixtures
- Evidence: ../research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001/maintenance-binding-revision.json

- Focused resolution: the unchanged original maintenance test passed (1 test, 1.099s). The preparation byte-reversal test initially omitted the two new metadata values; its assertion now reverses all three exact approved replacements, preserving full-byte equality. Intermediate freeze9874c3…/test/decision are archived; no source or measured evidence changed.

- Final-suite environment limits: unchanged poverty pixel fixture references three generated PNGs absent from both checkout and baseline Git tree; baseline source/merged snapshot reproduces the exact three missing-image subtest failures. No placeholder, skip or relaxed assertion. The first command also used a nonexistent BM25F test module; corrected to tests.test_photo_bm25f_retrieval.

- Resolution: unchanged maintenance test passes in final20-test completion run;19preparation tests and48-row full-index replay pass. Final validation and exact baseline artifact limit are documented in the evidence directory. No source, guard or ranking tuning.
