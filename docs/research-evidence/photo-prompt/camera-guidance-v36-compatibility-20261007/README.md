# V36 caller compatibility amendment

This amendment follows preserved checkpoint `ab666a0bee0fe2e45cd07c23b215cfcb0767e0eb`. It repairs two public-entry compatibility issues while preserving that checkpoint's measured source, pack and environment results.

The canonical asset-root check now applies when dispatching V36. Explicit V36 still rejects a wrong root before loading its helper. Canonical current assets retain current and historical dispatch. Copied legacy fixture roots reach the unchanged original validator body, including when their original file glob also copies the V36 descriptor.

Expected successor assertion, runtime and value failures now become `ValidationFailure`, retaining the original exception as their cause. The existing CLI handler therefore returns its normal failure JSON and exit code instead of an uncaught traceback. A missing historical environment remains a failure, never a pass or skip.

All **71 targeted tests passed** after resealing: the 26 existing successor controls and 45 compatibility tests. The new harness inherits the original V6 and V10–V13 positive and negative test methods and the affected default lineage controls without rewriting their assertions. It executes the actual amended validator with their original fixture mocks. Four exact original 8c Git blobs, totaling 492,146 bytes, supply only the missing fixture observations, original tar and provenance file in a temporary projection. Blob identities, modes, sizes and hashes are checked offline. No synthetic pack, replacement historical archive or interpreter fallback is used. Public routing and actual `main()`/`parse_args()` error-JSON controls are included.

The resealed active default validator also passed a new guarded CLI, exact receipt and composition/runtime qualification in **104.562 seconds** on CPython 3.12.14 / Unicode 15. The pack remains `f1d5de6f1a273b65`, SHA-256 `3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075`.

All 156 photo source bindings, active indexes, frozen inputs and pack bytes are unchanged. The new source root was independently captured and matched the existing generation `456ab66e03ca8c8196458ca9fbdf81c9d5ec082feaf2980f00cdfbd4754ff703`. Reusing its immutable runtime data is justified by that equality; the amended default path still generated and checked a fresh request. The earlier same-runtime doc-only comparison and complete 42-leaf historical-to-current delta remain unchanged evidence.

The proof adds this caller contract and its regression-test hash. Its source/DATA/pack/delta/environment bindings are retained. The helper changes only its proof seal; the V36 descriptor changes only its proof link; the universal descriptor changes only its validator hash. Original V1–V35 data, implementations, criteria and test assertions remain unchanged. Prior qualification records continue to describe the preserved checkpoint; its original proof is available at the parent commit.

**Main remains held.** The current exact Python/Unicode guard is unchanged, and native Python 3.14 pack equivalence is still unproven. The actual historical V35 probe under 3.12 produced public `ValidationFailure` with `HistoricalReplayUnavailable` as its preserved cause, retaining the original 3.14.3 / Unicode 16 requirement. This caller fix does not establish full historical replay or cross-environment compatibility.

[CONTRACT.json](CONTRACT.json) describes the bounded amendment, [VALIDATION.json](VALIDATION.json) records its checks and limits, and [TESTS.txt](TESTS.txt) preserves the full targeted test output. Reproduce the focused tests with `python -B -m unittest -v tests.test_photo_camera_guidance_v36 tests.test_photo_camera_guidance_v36_compatibility` from a checkout containing the authenticated original Git objects.

No provider/image calls, production retrieval changes, DATA/schema changes, anchor-limit changes or data-improvement count increment are included. Private receipts, runtime stores and temporary fixture copies are excluded from the publication packet.
