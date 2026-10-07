# Two recorded environments for the pinned V36 boundary

**Recovery checkpoint only.** These results qualify upstream `4f3d524ed035de8592e4b0c6ad5030b41ffc55af`. Main subsequently moved to `629bf4a88e1f1f524d177d67c09615a7fdb4f89d` at 12:51 UTC on 2026-10-07 with material photo-source changes. That successor is outside this qualification; this checkpoint does not claim latest-main readiness. Its separate integration must be reviewed and qualified after preserving these measured results.

This amendment follows preserved recovery commit `17914d6871e051b0803e68166dc66f86557f3e9d`. It admits two measured current-runtime records while keeping one exact public-pack oracle and the existing source, historical and caller-compatibility checks.

The accepted tuples are **CPython 3.12.14 / Unicode 15.0.0** and **CPython 3.14.3 / Unicode 16.0.0**. Each complete environment/generation/source/algorithm row has an independent canonical seal. Selection uses the actual process environment. Unknown versions, unknown combinations, duplicate or type-confused rows, mixed identity fields, and foreign pointers/receipts/snapshots fail. The original top-level 3.12 reference record remains unchanged. This is not an unrestricted Python-version or platform claim.

| Environment | Generation | Source fingerprint | Algorithm |
| --- | --- | --- | --- |
| 3.12.14 / Unicode 15 | `456ab66e…754ff703` | `64ddd1e4…a8cdd95a` | `3fde7604…6d00ca3a` |
| 3.14.3 / Unicode 16 | `2a2978af…de0d70b` | `5e1b8c83…8d0364ff` | `3309db45…77a6cff` |

Full identities and row seals are in [CONTRACT.json](CONTRACT.json). Both records require pack `f1d5de6f1a273b65`, file SHA-256 `3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075`. Environment-specific runtime identities are not relabeled or interchangeable.

## Measured equivalence and active validation

The separate experiment used the same exact 4f3 source root, all 189 photo files and modes, four frozen inputs, and seed 910000. A fresh local 3.14 publication used the packaged indexes and an independently verified official workspace binary. It did not rerun the unchanged 3.12 experiment or patch any production version check.

The two public packs are byte-identical, with zero changes across all 29 surfaces, 108 candidate occurrences / 100 unique IDs, their order, full meanings, applicability or protections. The public slot count remains 64. Composition, render request and audit-result bytes also match. Full receipt recomputation and ordinary/core/composed/runtime audits passed. Three existing nonblocking composition warnings remain unchanged. [CROSS-RUNTIME-RESULT.json](CROSS-RUNTIME-RESULT.json) and [CROSS-RUNTIME-REVIEW.json](CROSS-RUNTIME-REVIEW.json) preserve the measured result and its independent review. CPython and Unicode changed together; this does not isolate a Unicode effect or prove equivalence for arbitrary inputs or platforms.

The first 3.14 research publication encountered two denied system-entropy reads and remains unqualified. Its store and trace were preserved. Independent review allowed only read-only access to the verified `/dev/urandom` device in the research harness, after which a clean, separate publication and all remaining checks passed. Two publication attempts occurred; one was qualified. No production or network-policy change was made for this retry.

After the acceptance proof and helper were resealed, **all 87 targeted controls passed under each actual interpreter**: 26 existing successor controls, 45 caller/legacy-fixture controls and 16 new environment controls. The actual default public validator then passed independently under both interpreters: 107.695 seconds on 3.12 and 89.731 seconds on 3.14. These timings are execution records, not a performance claim. Both active paths generated a fresh CLI pack and checked its exact private receipt, live source capture and composition/runtime audits. Their qualified immutable runtimes were reused in separate stores; no new index publication was needed for these amended-path checks.

## Preserved contracts and remaining limits

All 156 photo source bindings, current and original shard rules, four frozen inputs, complete pack reconstruction, negatives, controls, safety and other protected surfaces remain intact. No photo production code, DATA, schema, retrieval behavior or anchor limit changes. The public copied-fixture routing and failure-JSON compatibility amendment is preserved. V1–V35 data, original implementations, assertions and historical environment criteria remain unchanged.

The verified Python 3.14.3 interpreter is now available, but the complete original historical fixture set is still unavailable. A metadata-only check found 1,830 required paths and 1,451 unique blobs, with 514 blobs covering 630 paths absent locally. No full original materialization, historical runtime or historical suite was executed. The passing bounded legacy fixture controls are not a full historical replay. [HISTORICAL-AVAILABILITY.json](HISTORICAL-AVAILABILITY.json) records this distinction.

[VALIDATION.json](VALIDATION.json) records both actual amended-path results and targeted tests. Each interpreter must use its own matching prepublished `PHOTO_RUNTIME_STORE`; validation still refuses implicit publisher/fetch/cache-rebuild fallbacks. Unknown environments require their own measured, reviewed qualification rather than a version-check bypass. The new upstream source requires separate integration and qualification before any main publication, in addition to the coordinated exact remote-tip and version-ownership check.

No provider, image or embedding calls and no data-improvement count increment are attributed to this amendment. Private receipts, runtime stores, installed interpreter files and bulky local seals are excluded from the publication packet.
