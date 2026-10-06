# Independent V32 code review

**No unresolved code-review findings remain in the reviewed files.** This is a review of the successor validator, historical recovery fixtures, archived horror harness, proof, and new tests. It does not replace the separate DATA review or establish final aggregate test success, publication, or image-quality improvement.

The review used official V31 commit `6b0338ebe6ad3a9a5ee3c603fc742311ad921054` and local DATA commit `3197ca8ecbff80d2dec110c6c506090c9ab16e62`.

## Findings resolved during review

1. **Missing-proof rollback bypass in historical recovery.** With V32 markers present, deleting its proof and restoring the religion source to exact V31 bytes initially bypassed retained-source checks. The reviewer reproduced acceptance through both `_v24_verified_payload` and `v30_source_path`. Recovery now requires the sealed V32 transition whenever its proof, parent manifest, or baseline marker remains, including dangling symlinks. All three historical resolvers check this before their equality returns. The same independent reproducer now rejects; genuinely older trees without V32 markers retain their original behavior.
2. **Default temporary-directory portability.** The independent three-test invocation failed during setup because hardlinks crossed from the checkout to a separate `/tmp` filesystem. Test sandboxes now use a temporary directory on the checkout filesystem, with unlink-before-mutation preserved. The production historical materializer continues to create independent copied inodes. A subsequent default-`/tmp` run passed the same three tests, with no failures, errors, or skips.
3. **Portable replay arguments.** Two diagnostic argument arrays contained an absolute historical workspace script path. The five cases now use consistent argument-only arrays, with interpreter flags retained separately. All exact seeds and all 20 input byte sizes and SHA-256 identities independently rechecked unchanged.

## Preservation and boundary checks

- All 1,354 archived member Git blob/mode identities independently match the official V31 tree, including the 6,252-byte original water-history test. Existing V1–V31 baseline files remain exact.
- The original V31 horror and V30 water validator function text remains exact. All seven original horror test methods and their assertion sets remain present.
- V32's public dispatcher requires its generated sidecar. Its frozen pack changes exactly four registered binding leaves; candidate objects and ordering remain exact.
- The materializer authenticates source paths, identities, bytes, and modes before staging, verifies again during copying, and publishes the completed tree atomically. It uses no Git/network recovery or hardlinked output.
- The separate original V31 audit uses the original CLI, exact original pack, an isolated original-source store, and independent corpus/full-pack recomputation. Its 15 negative cases address absent or forged receipts, stores, generation sources, loaded code, and candidates, while preserving the original validator and generation timeout.

## Verification scope

The reviewer independently inspected the code/proof, checked original Git identities and assertions, reproduced and rechecked the rollback finding, verified portable input metadata, and recorded the initial default-directory failure. Implementation-run evidence was also inspected: current V32 CLI/receipt, original V31 CLI and its 15-case receipt audit, V30 CLI, and the three final portability/regression tests passed. The initial broader historical aggregate was still running when this review closed; it must be reported separately, under its actual code hashes. Earlier c72 test results are historical only.

Final reviewed SHA-256 identities:

- Validator: `bdf07acfb323fdb35b7d24a821a31672bc6a6ba64618bc8bfc2e3d0e0ff1a99d`
- Recovery fixtures: `ce0bf99f24e13212fdf6826151535e82dc8c7685c0d8ee70e2b37064dee28953`
- Robe boundary tests: `5129000ca52f356639ebd2b2a39ff3060ee20e9df822de026ed20e3b5d3b1d57`
- V32 proof: `edfac81862908b5adb9b69ae69104513c108ec8ac6d2e53e5f71f93ce356c122`
- V31 parent manifest: `16766165b960a59c706482ebfa7406531276fddbc74bc708fc06058f04b8ba56`
