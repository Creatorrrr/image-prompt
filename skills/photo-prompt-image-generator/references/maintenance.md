# Native shared candidate maintenance

The authored source is `assets/photo_candidate_corpus_manifest.json`. It declares candidate modules, one slot catalog, binding modules and a policy module. Each global `cand_<uuid>` has exactly one owner. A role is a `bind_<uuid>` referencing that candidate and a managed slot tag. Candidates may have zero or many bindings. Add a record once; add bindings for useful presentations. Do not copy a candidate into another role. Keep its ID when editing text or changing tags. A change of meaning, owner or indispensable precondition that cannot be shared needs a distinct candidate.

Declare intrinsic visual effects, properties and provenance on the candidate. Declare role conditions, effects and weight on its binding. Moving a tag must preserve the role's subject/context guards. Unknown effects remain unresolved; they do not create permission to change a requester-owned property. Profile components, directed relations, conditional obligations and bundle-specific member requirements are complete authored contracts. Diagnostic/router/guard records are preserved separately from positive optional search.

`photo_candidate_index.json` and its referenced `photo_candidate_index_shards/` are generated from the entire positive shared corpus. Source identity, full text, text recipe, provider, model and dimensions must match before reusing a vector. Role counts never increase search documents or votes. The default query path is global BM25F plus exact cosine and RRF. `keyword_only` is an explicit diagnostic; it cannot claim embedding execution. Private query results bind exact text, core, controls, recipe, vector space, raw execution trace and vector hash.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --env-file .env
```

Use `photo_runtime_sources.source_update` during a coordinated edit/build, complete the revision and publish only validated source/index pairs with `SnapshotPublisher`. New runtime generations, receipts and workflow runs use the native contracts exclusively. Source changes without a completed index/publication remain blocked. Audit reads the original request receipt and recorded exact vectors; it never re-embeds a query to manufacture a matching rank.

Migration ledgers and archived requests are evidence, outside the operating manifest/import/build. They are not lookup tables. Past frozen results retain their original hashes; regenerate a new native run when that request is needed. New edits must not rewrite an earlier result as a new success.

Native tests cover shared/untagged discovery, role guard preservation, budgets, source/index integrity, recorded-query replay, semantic ownership and old-input rejection. Natural query ranking remains imperfect: explicit requester obligations come from the independently frozen core, and optional search results may all be declined. Search/index/transport checks do not establish image or native-pixel quality.
