# Shared candidate and lazy search maintenance

The authored source is `assets/photo_candidate_corpus_manifest.json`. Each `cand_<uuid>` has exactly one payload owner. Managed slots are presentation tags. A candidate may have zero or many persistent `bind_<uuid>` relations. New request-local role proposals can present compatible untagged or differently tagged records without modifying source tags. Preserve intrinsic effects, provenance, binding conditions, owner/carrier relations, conditional obligations and bundle requirements.

`photo_candidate_search.json` is the only operating index manifest. It references complete global BM25F statistics, compact source applicability metadata, quantized routing certificates, ordinal/float64 TF posting pages, payload shards and seekable exact float64 vector extents. DF and field-length statistics cover every positive source record. Slot tags never partition the search space or add ranking votes. Each active or explicitly requested slot receives its own candidate-free query, BM25F lane, actual query embedding, exact cosine ranks and RRF before presentation budgets. `keyword_only` is an explicit diagnostic, with no implicit hybrid fallback.

Readers verify declared source/index identities, keep payload/posting/vector bodies lazy, use a 64MiB content cache and at most 64 vector descriptors, and read only required extent bytes. A physical pack may contain many independently checked leaf shards. Source context guards can prune ineligible records; remaining vector areas are skipped only with certified score bounds. Weak bounds cause more exact reads, including bounded full streaming. Query contexts bind slot, language, specification, frozen core, controls, exact text, recipe, model/space and execution/vector hashes.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --env-file .env --publish
```

The build explicitly materializes all vectors offline. It reuses the current verified native layout only when ID, full text hash, text recipe, provider/model/dimensions and vector integrity match. It does not import a legacy index, seed adapter, old query format or ownership tree. Missing/changed text invokes the durable embedding provider; failed or unknown attempts remain inspectable. Source edits during the build block activation. Full source, statistics, payload/vector coverage, extent closure and routing residual bounds verify before the active manifest moves.

The build declares a `source_update` revision and completes it on success. `--publish` then seals an independently copied, fully verified V3 generation. Retrieval never rebuilds or bootstraps a generation; an unpublished or incomplete revision remains blocked. Request acquisition uses sealed filesystem identities and on-read SHA verification. Publication and explicit maintenance perform the complete verification. V8 packs, V3 generations/current pointers and V3 issued receipts are the only operating contracts. Receipt replay uses its stored exact per-slot contexts and never re-embeds a query to manufacture matching ranks.

The full-scan oracle and vector-map materialization are offline build/evaluation tools. They are not retrieval, audit, compose, view or preflight fallbacks. Historical evidence remains archived outside operating manifests. Old pack/query/receipt contracts are rejected; create a new native run instead of rewriting an old result as new success. Cleanup must list and hash exact unreferenced generated members, protect the active manifest closure, authored modules, fixtures and other work, and preserve recoverable history.

Search/index/source integrity does not prove role-specific semantic precision or saved-image quality. Frozen requester meaning and owner/property restrictions retain authority. Unknown effects require review, optional suggestions can all be declined, and required visual meaning must still pass independently.
