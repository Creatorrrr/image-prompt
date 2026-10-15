# Root-only publication handoff

The worker did not publish, acquire the operating runtime, modify operating source/catalog/assets, stage or commit. Root owns those actions after reviewing the frozen code and final tests.

`OPERATING-SOURCE-IMMUTABILITY-v1.json` compares all764 source/config/asset members in frozen50fd92's manifest against the current workspace: every byte hash matches. Code is intentionally excluded from that inventory. `OPERATING-COUNTS-v1.json` merges every manifest module without overwriting same-kind shards:18250 candidates,12089 bindings,139 slots,13 policies, native proof0, permission-envelope0. Catalog canonical4723660c37d3f665f883a81f0e8d35b8c690307406d18d63ade654527d5bec9c; whole operating corpus125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b. These are mechanical integrity/count checks, not a claim to reread all semantics.

Use a fresh Python process after the final reviewed edits/commit. `photo_runtime_sources.LOADED_CODE` is captured at import, so an old long-lived process must not relabel edited files as its loaded implementation.

The existing standard local publisher is:

```sh
sandbox-exec -p '(version 1)(allow default)(deny network*)' /usr/bin/env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 .venv/bin/python skills/photo-prompt-image-generator/scripts/publish_photo_runtime_snapshot.py
```

This invokes `SnapshotPublisher(source_root, runtime_store).publish()`, which fully checks the current corpus/layout, copies source and every scripts/precore Python file into an immutable generation, verifies code/environment/source binding and atomically updates the local pointer. Both new helpers are included automatically by `code_inventory`; do not omit ignored/untracked helper files from Git or the reviewed code allowlist. No embedding generation or source/index rebuild is requested. If publication reports a stale layout or pending maintenance revision, inspect that exact failure rather than forcing an adapter/rebuild or adding `--complete-update` blindly.

Then in another fresh network-denied Python process, place `skills/photo-prompt-image-generator/scripts` on sys.path and use the existing API:

```python
from photo_runtime_sources import RuntimeSnapshotProvider
provider = RuntimeSnapshotProvider()       # local_current, existing standard store
snapshot = provider.acquire()
print(snapshot.generation_id)
print(snapshot.manifest['source_fingerprint'])
print(snapshot.manifest['algorithm_sha256'])
print(snapshot.manifest['search_layout'])
print(snapshot.cache_status)
```

Check the generation's `source.code` includes exact current hashes for `photo_native_permission.py`, `photo_permission_comparison.py`, native, prompt, audit and runtime_sources; also verify all code/policy closure members and current source fingerprint. Record actual loaded module paths/hashes and acquired generation identity. Verify source/assets139/native0 and unchanged vector/source fingerprints independently; reading/reusing existing18180 vector records is separate from inference0. Keep model-import/provider-entrypoint guards as in the supplied offline regression runner if desired. Do not use remote sync or download.

This publishes updated Python behavior with the original operating139/native0 corpus. It does not select149V6, apply the unselected1299 execution-contract proposal, install a research proof or qualify actual hands-exchange source semantics. Root must separately select the source opt-in and prepare fresh exact input before any such application.
