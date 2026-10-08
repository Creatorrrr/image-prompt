# Fire semantics main integration, 2026-10-08 KST

`git pull --ff-only origin main` reported Already up to date at `30fc97a84fb3c8a7863adf0b8b60010dce73b444`. The integration branch is `codex/fire-main-merge-20261008`.

The commit combines fetched main with 127 new fire candidates, four additive contexts on retained optical/CME IDs, 131 authored visual profiles and 521 declared native/relation gates. Two managed transport repairs and their four regression tests are included. The frozen capture-owner test retains its original exact assertions and excludes this later additive fire overlay only from the historical inventory; current retained candidate meaning is separately verified.

`AUTHORED-SCOPE.json` lists the exact source scope. All 100 existing main manifest rows remain an exact prefix; fire candidate/profile registrations append at per-kind orders 59 and 41. `MAIN-ASSET-PRESERVATION.json` reports 735 tracked baseline asset files preserved byte-for-byte, excluding the manifest and two intentionally rebuilt index manifests.

The main indexes contain **10,651 semantic entries** and **2,409 profiles**. Canonical builders regenerated BM25F and lookup metadata using complete matching cached text, identity, provider, model and dimensions. Embedding calls are **0**, and network is explicitly forbidden in the offline rebuild wrapper. Gemini / gemini-embedding-2 / 768 is retained. Old shards are retained.

The primary working directory also contains unpublished intellectual-activity registrations and four unrelated profile edits. These are preserved as local work. They are not in this commit. The primary registration orders therefore remain 60/42, and its combined working indexes retain 10,694 semantic entries and 2,452 profiles. `sync_primary.py` preserves the local manifest by source identity, retains untouched dirty bytes and regenerates primary indexes from the resulting authored corpus after fast-forwarding main.

`PRIMARY-BEFORE.json` captures the initial primary HEAD, empty staged index, dirty file hashes and a separate backup of tracked edits. The publication/sync receipts created after the commit are kept under this evidence directory on primary, then published in a follow-up evidence commit. No reset, stash, forced push or unrelated worktree cleanup is part of this operation.

Validation already complete: dictionary metadata PASS, visual index 2,409 profiles/4,982 exact terms PASS, 35 focused fire/candidate/transport/capture tests PASS. The runtime generation is `5baa5a5c1ff4d6cdcd86bbe7c6792883a4e6da2046c8914b078d4396589a6747`. A parallel validation publication raced another pointer observation and reported a pending publication; the sequential final publisher succeeded with the same source generation. Its original warning log is preserved.

The uniform full discovery run completed: **224 modules / 202 passed / 22 failed**; **2,031 discovered cases / 1,947 reported cases**, with 84 cases aborted by class setup. `FULL-REGRESSION-CLASSIFICATION.json` and `.md` preserve exact failures. Historical oracles were not rewritten. The whole suite is not green; preserved-source hashes alone do not prove every failure was pre-existing.

Historical fire research and three image runs are copied byte-for-byte from the original task evidence. Their source generation `c37f392d21d2e87e34206b465cc718e5ce60db2a55ed72e560a4694dc56f417f`, prompts, native images, ledgers, failed inputs and pixel reviews are not reinterpreted against the newer main generation. Main integration performs no new image calls. The original tests had observed fire relationships in all three images, 19 applicable formal gates passing, and supplemental face-light/smoke-path failures. Requesting-user acceptance remains pending. Historical delivery receipts describe their original primary corpus, not the later clean main tree.

After tests finish: review scoped staged diff, commit, refetch main and resolve any new authored-source changes before regenerating derived indexes, fast-forward primary while preserving local overlays, push main normally, and verify primary/tracking/remote SHA equality.
