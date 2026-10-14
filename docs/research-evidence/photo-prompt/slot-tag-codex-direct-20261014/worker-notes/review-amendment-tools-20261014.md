# Sparse worker amendment tooling

Author: `/root/review_amendment_tools`, assigned gpt-6.1-sol / high. This is a tooling note, not a candidate semantic review or worker-source reading attestation. `root_all_worker_sources_read_claimed=false`.

The mechanical reader supports the two existing frozen amendment shapes without changing their JSON, Python, notes or earlier history. The 03250 note has exact sparse CID/ordinal lists, decision/source/catalog/reference and historical compiled-row hashes; its custom `pending_reread_packet.json` contains historical compiled rows, not a full source packet. Tooling preserves that artifact link separately and validates each historical row's linked original full source packet. The 11870 document has `amendments[n].decision`, per-item reread facts and original authored-item hashes, and a separately worker-hashed full packet. `authored_item` reads that original wrapper directly; it does not generate replacement authored documents.

Root creates an explicit normalization manifest with `normalization_author=/root`, `worker_attestation=false`, and `root_all_worker_sources_read_claimed=false`. Every normalized field from the worker is recomputed and checked against immutable originals; the manifest also supplies the exact current compiled row location/hash. In the second format the current compiled original authored tuple must equal the worker's original authored tuple; in the first format its worker-bound previous full compiled-row hash must also match. Original compiler attribution must belong to the same active worker task. Assignment selection is per actual CID ordinal, supports multiple assignments for one task, requires unique active task/model/high binding and rejects transferred/overlapping active assignments. Sparse coverage never claims a contiguous management range.

The compiled amendment keeps schema v2 and `codex_subagent_direct_source_read`. Sparse provenance binds exact reread CID/ordinal/count, worker note, immutable authored document/item/digest, assignment hash, root normalization manifest and actual full source packet. Explicit statuses, including pending, must equal the worker's decision. Existing contiguous management provenance stays unchanged. Existing full frozen/current snapshot and packet checking in `direct_review.verify` remains mandatory.

`apply --actor /root` runs full verification before changes and afterward. It archives exact original compiled document bytes plus before/after rows/hashes in a new `revisions/<manifest-stem>` directory and never overwrites that directory. Failed final verification restores exact original compiled bytes and retains the revision/rollback record. It does not commit, call providers, modify canonical assets, or rewrite worker artifacts. CLI actor declaration encodes the execution contract; it is not an operating-system identity or authentication boundary.

Structured proposal paths additionally allow exactly `/content/authored_components` and `/content/semantics/component_semantics`. Dict values bind the exact canonical before value, nested parents must already exist and be objects, new native candidate references are rejected, and the existing native profile compiler checks schema/projection consistency. Existing realization kind/guard/field restrictions and branch-owned quote checking remain. Structural compilation does not establish semantic correctness.

Validation executed with keys absent (`env -i` preserves PATH only) and OS network denied:

```
/usr/bin/env -i PATH="$PATH" sandbox-exec -p '(version 1) (allow default) (deny network*)' python -m unittest tests.test_photo_direct_review tests.test_photo_direct_review_amendments tests.test_photo_realization_content tests.test_photo_candidate_corpus -q
```

Result: 59 tests passed. New tests use temporary isolated fixture directories only, including actual existing `verify` before/after against a small fixture. They cover both worker formats; exact sparse/noncontiguous coverage and counts; task/model/effort/transfer/overlap; stale notes/documents/current compiled rows/original author tuples; source/catalog/reference/full-packet tampering; pending status; native profile exact old binding, malformed types, metadata override, foreign components and new/unknown references; failed final verification rollback; and preservation/refusal to overwrite historical archives. Existing tests cover cross-branch quote rejection and original realization safeguards.

No actual corpus registration, apply, global verify, CURRENT/progress mutation, canonical/index/runtime edits, provider/network/download calls, delegation or git writes were performed by this tooling worker. Root still must normalize/check/apply the real frozen amendments and assess their semantic/source qualification separately.

Final code SHA-256:

- `direct_review.py`: `06b1f723f07aae5f2536d231dabc1139bc74dd95073642bb9c048d3d734fa583`
- `delegated_amendments.py`: `5a833166c0e2feb6728e13618eabdec93018eca89e437b5e051a2e4328db493c`
- `tests/test_photo_direct_review_amendments.py`: `3ee6cbf37b1bd01e12368fa827d942d5e4b983b1085b9d97ac013e2d7502437a`
