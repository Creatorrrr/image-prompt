# Independent installed CT091 integration review

**Verdict: the final uncommitted patch passes this narrow DATA integration review. No unresolved patch-specific blocker was found after the receipt repair. This is not a full-suite, rendered-quality, or general opacity-protection pass.**

Reviewed against `c8ad4e4609f9120a95ee0c10d4ca32805e967a4d`, with no repository edits or provider calls by this reviewer. Evidence: `independent-integration-verification.json`; initial receipt failure is retained separately in `independent-integration-verification-before-receipt-repair.json`.

## Verified actual scope and identity

- Exactly `clt_ct091_v1`, `clt_ct091_v2`, and their two matching `clothing_ct091_*` profiles append `appearance / main_subject / wardrobe.surface.sheer_opacity`. Removing those four additions and restoring the previous reference reconstructs the baseline source objects exactly. Original material-family effects, all other records (including CT098), text, aliases, gates, dimensions, and ownership are unchanged.
- Git has exactly four modified asset files, the new maintenance record, 16 new semantic shards, and the six-method test. No runtime, existing test, PR5, or historical receipt file changes. `git diff --check` passes.
- All 16 new semantic shards are **byte-identical to their corresponding baseline Git blobs**, with verified manifest hashes/counts totaling **9,876 entries**. General metadata differs only in dictionary hash, generation paths, and removal of `created_at` (a nonsemantic serializer difference).
- The **1,622-entry** visual index is object-identical except for its registry hash. General BM25F, visual BM25F/exact lookup, semantic text, and every cached embedding are unchanged. Production index metadata validators pass. Dictionary/registry bindings match `application.json`.
- The final maintenance record uses `photo-extension-maintenance/v1`, supplies the expected source filename/runtime keys, and has equal, independently verified `authored_source_sha256` and reference-stripped source digest. Current reference digest: `4441ed1a5e71f111115ad3526af05b040adabef8a5ffec322c419d280d03be96`. Previous reference and previous receipt remain hash-valid and byte-immutable; its old authored-source digest also matches the baseline source.

## Resolved blocker and completed checks

The first installed run failed the existing clothing integrity test because the new record omitted `authored_source_sha256`. This was a real integration defect, reported immediately. The coordinator repaired only the unpublished receipt/current reference, preserving the failed log and initial record. The unchanged clothing suite then passed **7/7** in `tests/clothing-receipt-recheck.log`; generated dictionary and registry bindings stayed unchanged.

Completed logs establish **72 focused test methods passing across nine modules**, using that seven-method recheck in place of the initial failed run, plus dictionary validation. The new six methods cover exact source/profile additions, canonical/ancestor rejection, disjoint properties and other-owner openness, causal removal of the new effect, CT098 deferral, and current profile text binding. They are structural/source regressions; they do not themselves establish natural retrieval, layer-aware routing, rendered correctness, or broad vocabulary coverage.

I independently compared all **11 installed public objects** with the qualified after archives: whole-object equality, matching pack IDs, unchanged baseline text, and zero stored full-retention audit failures in every case. These are two canonical source-guided product fixtures plus nine admitted fresh requests. I inspected final logs/artifacts rather than rerunning providers or duplicating the public replay.

## Required limits retained

- Alternative valid opacity paths remain uncovered; no aliases were added.
- Same-owner/layer hierarchy can conservatively reject compatible lining-only changes.
- All nine admitted fresh requests have zero natural CT091 exposure under the existing human `surface_material` slot guard, hence **zero measured fresh benefit**. One of ten authored fresh requests remains unadmitted. These are not nine successful blocker cases.
- Matching-profile metadata parity is verified, but no natural matching-profile retrieval benefit is demonstrated.
- The historical v9 exact-byte boundary check remains red pending separate runtime work. Its fingerprints/baseline, the runtime, and PR5 were not changed here. Focused green checks do not supersede that full-regression limitation.
