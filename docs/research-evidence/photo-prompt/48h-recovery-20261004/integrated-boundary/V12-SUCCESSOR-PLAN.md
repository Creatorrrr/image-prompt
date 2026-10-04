# Minimal V12 immutable-boundary successor plan

Status: **plan only; no implementation, source installation, baseline edit, validator edit or publication authorized or performed**. The two-alias DATA change remains blocked by the current immutable V11 source pin. The separate integrated 18-input replay and focused tests are still being reviewed; this plan does not claim those stages complete.

## Observed causal basis

Integrated source: `0efc2dfde7de9693799d3c84618705332e59920c`, actual merged PR5. The two experimental arms use the identical photo runtime, tests and frozen V11 four input files, seed 910000 and command recipe.

Actual production generation in both arms produced exactly the same bytes:

- Raw pack SHA256: `6c097471705589a4db45daf5aa164017f2c7b512dcaab880e9e58bb3882f5589`
- Pack ID: `96a0c50349d492f5`
- Every JSON leaf equal; all 64 complete candidate objects and their public order equal
- Frozen scene/core/control/embodiment/composition, negative, privacy and optional-adoption fields equal

The unchanged production validator, SHA256 `9f972a9ab0ca1fa031f772c888009d7c2a5c052c60cbdfe0431cb9a2988c7d4d`, passes default V11 on before and rejects after with `photo metadata successor DATA source bytes drift`. This is an actual invocation with the real nested CLI, not a mock. The initial relocated-interpreter failure occurred before generator execution, remains archived, and was repaired only by pointing the byte-identical copied interpreter to its already-installed Python standard library via temporary PYTHONHOME. No frozen input or source code changed.

Of V11's four pinned source files, only `photo_prompt_visual_profile_index.json` changes:

- Old: `9a279002707290f79ad3b4de646644dfe4146bf4948dd07977e3d16a458482c6`
- Proposed: `eb2b1b5359132de1f0dc62dca074dc71d42d11c17840e35f4cf58c6c879b42f0`

Tags, quality layers and the ordinary semantic-index metadata remain byte-identical. The independent boundary receipt is `boundary-pack-independent-verification.json`; producer evidence is `runs/integrated-0efc2dfde7de-001/boundary/CAUSAL-RESULT.json`.

## Why the existing four-leaf workflow does not apply

The existing V10→V11 transition explicitly requires all four of these leaves to change: `provenance.tags_hash`, `core_retrieval.slot_corpus_sha256`, `core_retrieval.canonical_sha256`, and `pack_id`. Here **none changes**. The index is part of the qualified DATA identity even though this frozen scene's public pack is insensitive to the two alias edits.

Consequently:

- Do not overwrite V11's index hash, pack hash, DATA provenance, predecessor binding or proof
- Do not pretend four fields changed, force a new pack ID, alter the frozen scene, or add a cosmetic output change
- Do not relax the old rule to “zero or four changes” for all versions
- Do not omit the visual-index source pin or make source mismatch merely a warning
- Do not let an unregistered future manifest make itself current

This needs a separately reviewed, explicitly registered **V12 zero-pack-delta transition**, if implementation is later authorized. V10 and V11's exact four-change checks stay intact.

## Minimum implementation scope, subject to separate approval

1. **Finish qualification and freeze exact provenance.** Bind the completed integrated 36-row experiment, ten mutations, genuine index receipts, compatibility results and this boundary proof. Record the actual before runtime SHA, old qualified DATA identity and exact proposal/index hashes. The future DATA commit is not yet available: do not invent it. After an authorized DATA commit exists, bind its verified SHA and the exact parent; do not create a self-referential or guessed commit field.

2. **Append V12 and archive V11 without modifying history.** Add `photo_regression_baseline_v12.json` with predecessor filename/schema and exact V11 manifest SHA256 `b6280e500da723e4e017297246bc4a8d2eed71b8325db1d4a650fd4cbf92fa40`. Add the immediate predecessor raw replay as `photo_regression_baseline_v11_pack.json`, exactly matching V11's pack hash. Retain the same pack bytes/hash/ID for V12; keep frozen inputs, seed, command recipe, preserved-contract hash, candidate count 64, negative and privacy requirements unchanged. Only an output destination may vary under the existing recipe rule. Preserve V1–V11, all historical packs/proofs and universal V1 byte-for-byte.

3. **Add a narrow, immutable transition proof.** Pin both raw packs and their equality, zero changed pack leaves, all 64 candidate objects/order, the exact before/after source hashes, and the actual changed-data scope. The qualification/proof must bind the two exact Korean alias leaves and regenerated visual index, not merely record a successful example. Retain the four current source pins with the new visual-index value. Additionally bind the changed palace profile JSON and permitted two-leaf diff in the V12-specific proof so an index-only digest cannot conceal unrelated DATA edits. This extra proof must be checked against actual bytes, not treated as an informational flag. Do not alter the old V10/V11 four-source-file schema.

4. **Register V12 explicitly with a dedicated zero-delta check.** Add only version 12 to the supported-version set and newest-first dispatch, retaining the existing full historical lineage loop. The version-12 branch must validate source/proof/predecessor bindings and require the current raw pack to equal the archived V11 raw pack, current pack hash to equal both manifests' pinned hash, and canonical pack ID to match. Require zero differences, with no skipped pack fields. Validate the declared visual-index source change and unchanged other pinned source bytes. Existing V10/V11 branches continue requiring exactly their original four changed leaves. A generic configurable “allowed delta” mechanism is unnecessary and would broaden this task.

5. **Maintain the current universal-V2 validator binding only as existing policy requires.** Editing the validator changes its own source SHA. Preserve the old `universal_scene_baseline_v2.json` bytes and prove that only its existing `validator_contract.sha256` descriptive leaf changes. Do not change universal V1, holdouts, oracle constants, case expectations, structural counts or invariants. This is an accompanying hash-maintenance step, not permission to rebaseline semantics.

6. **Document the special V12 contract and its limits.** Keep the existing four-leaf workflow valid for its original transitions. Document this separately authorized zero-pack-delta source-identity transition explicitly. The report must retain the architecture recall cost, optional collateral, contradiction-detection limitation, and missing image/embedding-query evidence. A passing frozen boundary pack does not qualify the changed DATA for every other request.

## Minimum transition and rejection tests

Keep historical expectations strict and test the new branch separately:

- Default dispatch selects V12 only after explicit registration; an unregistered V13 manifest alone cannot advance it
- Historical V1–V11 raw manifests/packs/proofs remain identical to their frozen hashes
- V11 succeeds on its actual qualified before DATA; explicit live V11 against the new after DATA continues to reject the source-pin mismatch
- When existing V11 tests become historical, give them explicit version-11 dispatch and their qualified saved DATA identity; do not let their old positive expectation silently target default V12. Label any historical replay mock and retain actual historical production evidence separately
- V12 succeeds on the exact qualified after source and unchanged frozen pack; verify the full lineage, frozen input bytes/seed/recipe, 64 complete candidates/order, raw hash, canonical ID, preserved contract, negative and privacy requirements
- Reject wrong V11 manifest/archive bytes, DATA commit/parent, source hash, omitted/extra pinned source, proof hash/provenance and an undeclared alias or other DATA edit
- Reject any changed candidate value, candidate ordering, scene/core/control/embodiment/composition field, negative, privacy or adoption field, even when the output checksum or pack ID is recomputed
- Reject a nonzero pack-binding delta in V12; the four-field allowance must not leak from V10/V11 into V12
- Reject malformed/cyclic/skipped predecessor lineage and attempts to register future versions through manifest content
- Preserve the V10/V11 exact-four-change negative controls; zero changed fields must still fail those branches
- Verify the universal-V2 descriptor has exactly the one permitted validator-hash change and that all historical/holdout/oracle anchors remain intact
- Run the new compact architecture helper tests separately from the existing focused integrated suite, then rerun affected boundary/current-oracle tests and feasible repository integration checks against the final authorized code. Preserve all failures and do not claim full-suite green without running it

## Operational cost and stopping rules

This design preserves strict DATA-byte identity. Therefore **each future change to a pinned DATA/index file can require another successor even when this frozen pack is unchanged**. Under the current policy, the recurring cost is: freeze parent/new DATA identity; rebuild/revalidate real indexes; run exact before/after production boundary generation; independently compare full packs/source bytes; archive history; append a manifest/proof; explicitly register the version; update the current validator-source hash descriptor; add/run transition mutation tests; and recheck the final merged head. The current validator runs the generator for each boundary check, so this is more than a cheap checksum update.

This plan intentionally proposes no general validator relaxation, automatic version discovery, mutable current baseline, or exemption for “unrelated” aliases. Reducing that per-update cost would require a separate design and authorization. If any future pack, candidate/order, frozen-input, source scope or unrelated invariant differs from this proof, stop: the zero-delta V12 plan does not apply.

**Current decision needed:** authorization, if desired, for this specifically scoped V12 integration-maintenance implementation after the DATA qualification review. Planning and a causally explained failure are not permission to implement it or publish the two-alias DATA change.
