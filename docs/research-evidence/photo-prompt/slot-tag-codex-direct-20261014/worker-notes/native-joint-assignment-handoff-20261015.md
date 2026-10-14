# Joint E assignment + lazy child correction — frozen handoff

Production editing began only after root's explicit guard-v2 commit-complete message (32c500c4b). The four before-file copies and MANIFEST remain exact; a read-only git-show check confirmed all four before SHAs equal that authorized commit. Production changes are limited to three files plus one new test file. prompt_generator.py is unchanged. No existing test, product guide, canonical/source/catalog/proof/index/runtime/CURRENT/registry or Git was modified by this task. Old diagnostic artifacts remain byte-identical.

## Result

- The common pure selected E ledger compares (dimension, actual canonical target, property) against exact typed-value bytes, operation and canonical actual receiver SET across all selected own/child effects. Existing same-source-local and within-CID actual-owner checks remain strict. Explicit equivalence alone defines same entity; part_of is not collapsed. Source literal values/order are preserved. No aliases, value coercion, partial merge or automatic winner are introduced.
- Whole admission and permission collection use that ledger on actual selected closure. The collector never calls admission or guard evaluation, so preservation guards can still inspect permission scope without recursion. Search-only unresolved selectors remain discoverable; final remains strict.
- Final native adoption audits the union of successfully admitted independent chosen roots before emitting a resolution. Reused children require the same exact CID/RID/proof/owner/active-child closure; they are not silently skipped before checking all assignments. Only E participates; P old versus E new does not produce a value conflict, while unchanged frozen property locks still reject unauthorized mutation.
- Qualified required children already projected as compact layout guards now reuse their proof rather than calling compact on compact and receiving None. Actual full sources still use the validated compact projection. Changed compact seals fail closed in tests.
- Top v4 proof, map v2/v3, immutable public pack and outer receipt/API schemas are unchanged.

## Final test evidence

**181 executions / 181 unique / 431 subtests, failures 0 / errors 0 / skips 0**, nine modules, 14.813 seconds including suite loading (runner-reported test time14.512s). The new test file has14 methods;167 methods are existing tests. Every tested code/test hash stayed identical during the final suite. git diff --check passed for changed paths. A previous focused revision had179/179/429 PASS before two additional necessary controls; it remains separately recorded and is not added to the final unique count.

The14 new methods exercise independent and required-child conflicts in value/type/operation/receiver SET, identical values, selected-owner aliases, receiver alias and reversed receiver order, explicit disjoint owners, distinct properties, part_of not equivalence, fixed recording_camera v2 maps with manual50/24 counterparts, selected vs unselected optional child, actual branch, repeated shared child and changed guard, guard-only owners and sibling injection, unresolved search-only/final strictness, P old/E new and immutable locks, and real lazy→public pack→whole compose→fresh runtime request boundaries. Existing nine-module coverage also reexecutes original source guard scopes/receivers/introduction/scope preservation and whole core wire/realization projection paths.

The separately serialized consumer-proof JSON contains two full fixture public packs, four exact composed inputs, four exact transport requests and their actual audit reports. Both independent chosen and required-child cases reject same-owner cracked/smooth assignment at compose and runtime request; both accept the explicit separate bench owner at compose and runtime request. Successful receipts bind the same composed/core/graph/owner mapping hashes. Packs remain byte-identical across audit. Rebinding after audit with the old request is rejected; unused extra mapping entries fail final native adoption. This invokes fresh request audit only, not a provider or image render.

## Initial failures and fixture corrections

The pre-production RED log preserves9 methods with3 failures/29 errors: missing new ledger API, actual cross-CID acceptance and the lazy-child TypeError, together with fixture problems. It is not a count of32 independent product defects. Post-change r01 had3 failures/9 errors: new alias owners were incorrectly declared surface while the existing fixture owners were entity; a public permission assertion expected an overly specific error despite a valid source-guard rejection; and the new bare bundle omitted its positive parent component. Those new fixture declarations/assertions were corrected directly; production guarantees were not weakened. The component now has a literal parent texture unit plus an explicit duplicate same-assignment E fact, with receiver effects spelled out when present. R02's9 methods passed. Extending actual-RID coverage initially exposed mechanically unrenamed prerequisite fact IDs in the new branch fixture; the references were explicitly renamed within each RID. R04's12 methods passed. A manual fixed-role camera50/24 control and a part_of identity control brought the file to14 methods; the final suite uses that final byte hash. No actual source/proof was converted or corrected.

## Commands

Every test process used this isolated prefix (only HOME/PATH/PYTHONDONTWRITEBYTECODE; no provider keys), plus deny-network sandbox:

```sh
env -i HOME="$HOME" PATH="/opt/homebrew/bin:/usr/bin:/bin" PYTHONDONTWRITEBYTECODE=1 /usr/bin/sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 -m unittest -v tests.test_photo_native_joint_assignments
```

For the actual final result, the same prefix invoked `python3 -` with an inline unittest runner. It loaded the following exact modules, counted test IDs/startTest and addSubTest, recorded before/after file SHA, and wrote focused-final JSON/log. Reproduce the same test selection with:

```sh
env -i HOME="$HOME" PATH="/opt/homebrew/bin:/usr/bin:/bin" PYTHONDONTWRITEBYTECODE=1 /usr/bin/sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 -m unittest -v tests.test_photo_semantic_evidence tests.test_photo_native_compound_evidence tests.test_photo_native_owner_selection tests.test_photo_native_source_guards_v2 tests.test_photo_native_v4_guards tests.test_photo_candidate_realizations tests.test_photo_native_joint_assignments tests.test_photo_native_fact_wire tests.test_photo_realization_content
```

Actual counter hooks were `startTest: ids.append(test.id())` and `addSubTest: subtests += 1`, delegated to unittest.TextTestResult, with unique=len(set(ids)). Execution count is TextTestResult.testsRun; no duplicated runs are represented as additional unique tests.

The additional consumer-proof capture invoked the exact new test helper `pair(required=False/True)`→existing `owner_pack`→`JointPublicPackTests.composed/request`→actual audit_composed_prompt and audit_image_render_request inside bound_native_source. It asserted same-owner=false and bench-owner=true at both boundaries, and identical public pack bytes, then serialized full actual inputs/reports. Four actual fresh-runtime audits were captured separately from unittest metrics. Code hashes before/after equal the final suite's recorded hashes.

## Boundaries / remaining root work

All fixtures are manually authored isolated declarations; constant synthetic vectors exercise integrity and transport, with inference/provider/network calls0. Actual root7 accepted proofs, actual1278/1296 proposals and all canonical records are unchanged. No operating qualified-count update, actual source approval, full corpus semantic truth, operating rebuild/publication/acquire, provider execution or image pixels are claimed. Root performs independent broader regression and actual metadata guard rebuild/publication/acquire/commit. The task is now frozen.

## Exact changed-file SHA256

- `skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py` — 96345 bytes, `28385c8c7659a661659b0b737b58ca6d4220a50f5c5c70c0874cfafbc44fbe5b`.
- `skills/photo-prompt-image-generator/scripts/photo_candidate_realizations.py` — 16454 bytes, `749f00eb2f6e5c219e06bcf88b90912c2bf24f7a72eb180a70a4d93d04e0dd5c`.
- `skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py` — 279151 bytes, `7c3c843ce97c9e02fc215a3247eb624349d61beddc62d7659dcc5914649c8d59`.
- `tests/test_photo_native_joint_assignments.py` — 24033 bytes, `7a9b1e7c55c1b22ae87d1365db94e2f08e6eef50ef3cfdee0430ec0224eb4743`.

Authorized but unchanged: `skills/photo-prompt-image-generator/scripts/prompt_generator.py` — `cfbdc7d66f0d065fedc111d8bac9a47b13a7c891e59c95261ed4f170b1f9671a`.

## Evidence hashes

- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-before-20261015/MANIFEST.json` — `f6e7c4fc12bbcdd5ede662cedd90b5df7bf3ae94692319d9d33ccc24b78ea76c`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-plan-20261015.md` — `28c6603fd3cf843111dcb2c16434f592924e08e048d61ae9f15a2c4596847252`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-before-20261015.log` — `031e9d73cc44d241bbd9509e42640e406ad71e9b3aa9873764373bfce65754b4`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-after-r01-20261015.log` — `f92fd4f979774d6c9d59b7d95609724fc4ae7c12d737fc73c82c10762c752e2b`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-after-r02-20261015.log` — `6d341e3af1a1b531e93000f451f2a58799f0ae57e72d0cfffa412373724a7edd`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-after-r03-20261015.log` — `3e676a3f97e30e320abdf0f9cf19d13f274347ed991890c4ef51f7fbef2807f4`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-after-r04-20261015.log` — `c27f3dd7ea51e2a29e99bf3b75c26254906cfee1b4a24455f14660f1a3ac530f`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-tests-after-r05-20261015.log` — `746200c9b07e8212d17d0c3757767530bed173442f4eed17f487a513168aea94`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-focused-r01-20261015.json` — `8fd6f1279bcf73263a899a633612ef7723c8087692d5df8481574345116c6f5f`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-focused-r01-20261015.log` — `2795709fd0d237d96e62e59d637dbac362f71487b0c658215104e67be7e1fc67`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-focused-final-20261015.json` — `3c8cda2b25a65c00d9b06517c3096b753d3e5456e180f46fbb67a74859da071f`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-focused-final-20261015.log` — `1aee0a34b662db871eefd53e4dd16a2925e6bf3ee0947016d25bdfca1f7d32a3`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-assignment-consumer-proof-20261015.json` — `98c49f02a41953bce0916199be96fdc088a0e055144777da3b6988a5c8588353`.
- `native-joint-assignment-handoff-20261015.json` — `be6b1383c0998b1e33b5eb17fab26ca5f5cf4c709ed32ec4502257897363bb62`.
