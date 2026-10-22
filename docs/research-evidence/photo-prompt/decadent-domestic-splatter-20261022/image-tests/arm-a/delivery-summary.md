# Arm A delivery summary

Final image outcome: **BLOCKED_NO_PIXELS**. The sole built-in image generation call returned HTTP 400 `moderation_blocked` at output moderation, with categories `sexual` and `violence`; request ID `6103c2a4-dbee-45b5-8455-5815c633853b`. No image file returned. No retry, provider switch or regeneration occurred. The block is not a pixel FAIL; all planned pixel observations remain `UNOBSERVABLE_NOT_PASS`.

The independent core, 3-slot plan, composed prompt and native runtime input audits passed. Supported `deliver` also passed its composed-prompt audit, leaving phase `prompt_delivered` and the actual operation `provider_blocked`. This delivers the prompt record only and does not establish image success or user acceptance.

Managed retrieval returned 32 query occurrences / 31 unique complete sources, all reviewed. One newly added DDS source was exposed (`cand_96fd33adb0d15ce0834258545e6d3512`); none was retained or natively adopted. Thirteen complete alternatives were compared and the independent baseline was retained. Environment-detail retrieval returned zero after the sealed query’s nonpositive-scope projection; no re-query or resampling was performed.

The initial ledger write failed with `attempt evidence tool mismatch`. That original failure and raw capture remain unchanged. An explicit separate protocol projection maps only `image_gen.imagegen` to sealed family `image_gen`, and `codex_native` to sealed environment `native_imagegen`. The entire raw error, outcome, request, actual timestamps and attempt remain identical. The parent coordinator recorded that same blocked attempt successfully as ledger run `6a3e12f95ad954cf`. Original recording error is history; current recording status is `attempt_recorded`.

Artifacts:

- Final prompt: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/final-prompt.txt`
- Original raw capture: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/native-attempt-error.json`; SHA-256 `9ba53b9cd96006e55b5bb4bfa53c0c0d222fa787b65eb5aa9486e3b56b0d8a15`
- Explicit projection/recovery receipt: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/native-protocol-recovery-receipt.json`
- Recovery verification: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/protocol-recovery-verification.json`; SHA-256 `386ff78de1ed9011229a6865acb7d005f04a2389169788475da107426ce4544a`
- Ledger: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/image_runs.ndjson`; SHA-256 `a3a338faed5a92f78864956920890d49ce6a4429875e9ff3bc8342b05c737d5d`
- Independent manifest: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/run_manifest.json`; SHA-256 `dc8570fe8ebc142f40eb350c7e7d5d50387bdde9277ec3cf617f3b210494c3f7`
- Material review/comparison: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/candidate-source-review.json` and `/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/composition-comparison.md`
- Pixel observation: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-a/pixel-review-blocked.json`
- Current blocked status: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-a/blocked-status.json`

All 14 frozen authoring artifact hashes and the pre-generation testcase hash were rechecked unchanged. The original evidence, source code, core and criteria were not edited during recording recovery. Actual image calls: 1; blocks: 1; returned images: 0; new image calls for recovery: 0. Requester acceptance remains pending.
