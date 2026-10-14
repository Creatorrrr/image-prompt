# Inverse verifier bounded wire revision 3, 2026-10-14

Authored by `/root/review_05250_06250`, actual model `gpt-6.1-sol`, reasoning effort `high`. Frozen after the final fixture run at 2026-10-14T12:53:39Z. This is a separate historical supplement to the original contract and revision 2; neither earlier note is replaced.

Authorized scope: change only `../verify_inverse_reviews.py` and repository `tests/test_photo_direct_inverse_reviews.py`, plus this new immutable supplement and its byte-hash sidecar. Result schema remains `photo-direct-inverse-review-verification/v1`; selection schema remains `photo-direct-inverse-review-selection/v1`; `contract_revision` is now `bounded-wire-3`.

No actual 139-slot verification was executed, no actual verification output or root result was written, and no raw worker artifact, source record, catalog, production module, pending amendment, operating artifact or Git state was changed by this task. No provider, model or network call occurred. Root's prior actual result and reported failure counts are not measurements from this worker's fixture run.

## Explicit evidence and composition boundary

Read the complete two-candidate memo `authored/native_07250_03250_04250.inverse-footprint-memo.json`, 9,599 bytes, byte SHA256 `9f6a20a50659534c63f29b8cebd9c7ca97fae7f5c3b09082daa9bff657d93013`. Its candidates `cand_7eae6bb97a975fc197e3b84d24093df5` and `cand_2078b471c1dd50b2a67f7854d4b5dd76` have empty root footprints and explicit, actually consumed `content.concept_candidate.affected_dimensions` / `affected_properties` footprints. The memo distinguishes those projections from arbitrary child-closure union and does not claim a semantic judgment failure or native qualification.

Directly compared current production `photo_candidate_realizations.effects` and `photo_semantic_evidence.with_projection` / `effect_set`:

- `skills/photo-prompt-image-generator/scripts/photo_candidate_realizations.py`: 15,468 bytes; SHA256 `d8fe5ba9f9c10f18bead40cac142bb23f77ac97b6a6b584baf345709ee895f41`.
- `skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py`: 61,560 bytes; SHA256 `d7935c7b945bf14b639222f21dd23dc29b21b74994043c011ca8c940318e68d1`.

For a hash-bound canonical source record, expected per-RID effects now start with root dimensions/properties, add only that selected branch's dimensions/properties, and apply the record's explicit concept projection. Optional realization mode retains the independent base RID; one mode retains only the source's branches. Branch properties are appended only when absent, as production does. With an explicit projection, dimension IDs are unioned and exact `(dimension, target, property)` tuples are deduplicated across the root/selected-branch/projection composition. Final dimensions and final properties are sorted; property sorting uses that same three-field tuple, as native `with_projection` does even when no projection exists.

The bounded helper checks the projection's two explicit lists, unique nonempty dimensions, exact three-field nonempty property ownership shape, property-dimension membership and duplicate property tuples. It is an expected-footprint composer for the already input-bound source, not a replacement native corpus schema validator. It does not synthesize projection fields from missing data. Full root effects and intrinsic conditions continue to be compared exactly with source; this change concerns derived per-RID expectations only.

No member candidate, binding closure, role/tag, title, alias or discovery metadata supplies an inferred effect. A property's exact source owner remains its owner. Sibling branches do not acquire each other's effects. Worker `actual_effects_by_realization` is not reordered or repaired: its property list must exactly match the expected native ordering; foreign properties/owners, duplicates and extras still fail. Revision 2's unique dimension-ID set comparison and all existing raw preservation rules remain.

This footprint correction creates no positive semantic evidence. `affected_dimensions`, `affected_properties`, and nested projection property labels remain metadata denied by `positive_path`; an effect being consumed does not turn its property label into a positive fact. Existing canonical branch concept-unit evidence binding remains separate and unchanged.

## Global catalog-wide pair coverage despite a broken summary

After attempting every explicitly selected review, `run` independently builds the expected pair set from **every slot in the validated input catalog** and that slot's saved BM25F / embedding / RRF top-three union, then compares it with accumulated actual `(ordinal, candidate_id)` pairs. The new failure code is `global_top3_pair_coverage`.

This comparison is outside each per-artifact parser's exception boundary. A missing `slot_reviews[*].candidate_ids` can still raise `invalid_worker_contract`, but cannot skip the global pair comparison. The original local pair check and duplicate/overlap checks remain. Invalid/unbound input bytes still stop processing before worker adjudication, as before.

The task's 139-slot catalog is already bound by the root input; no hardcoded alternate catalog or fabricated list was added. Small isolated tests use their own bound three-slot catalog. Selecting only a proper subset of that catalog now retains the true actual counts and also fails global coverage. The reported 21 real checkpoints lacking `candidate_ids` are not patched, defaulted, waived, or claimed to pass. A malformed summary with complete rows still remains an error; a malformed summary plus a missing row additionally fails global coverage. No missing actual row is generated from a summary or prepared packet.

## Fixture verification

The existing 41 tests remain; their revision assertion is updated to v3, and two subset-selection expectations now require the new global coverage failure while preserving actual counts and selected-checkpoint summaries. Six additional tests cover:

1. Manually authored expected property lists for root/selected-branch/projection overlap, canonical tuple sorting, optional/base versus one mode, and sorting without any projection or branch. Expectations are literal fixtures, not output from the helper being tested.
2. An end-to-end three-worker-format fixture with a manually authored per-RID expected footprint, cross-component duplicates, projection application to each actual RID, exact root effects, and unchanged normalized raw row.
3. Rejection of forged sibling/child/projection extras, changed owner, property-order changes and duplicates; a parent's member reference and slot tag supply no footprint.
4. A projection metadata property label still rejected as `metadata_only_primary_fit`, even when the consumed footprint itself is correct; the authored verdict and raw row remain preserved.
5. Missing `candidate_ids` plus a missing actual pair: `invalid_worker_contract` remains, local parsing aborts, and `global_top3_pair_coverage` independently identifies the missing pair.
6. Rejection of missing projection lists, duplicate dimensions/properties, a property outside declared projection dimensions, and an extra property field.

Final counted execution used an empty environment with network denied and bytecode writes disabled:

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  python3 - <<'PY'
import json
import unittest
class CountResult(unittest.TextTestResult):
    subtests = 0
    def addSubTest(self, test, subtest, outcome):
        self.subtests += 1
        super().addSubTest(test, subtest, outcome)
suite = unittest.defaultTestLoader.discover('tests', pattern='test_photo_direct_inverse_reviews.py')
result = unittest.TextTestRunner(verbosity=1, resultclass=CountResult).run(suite)
print(json.dumps({'tests_run': result.testsRun, 'subtests_run': result.subtests,
    'failures': len(result.failures), 'errors': len(result.errors),
    'skipped': len(result.skipped), 'successful': result.wasSuccessful()}, sort_keys=True))
raise SystemExit(not result.wasSuccessful())
PY
```

Actual final result: **47 tests / 74 subtests, 0 failures, 0 errors, 0 skipped**, 1.663 seconds; exit code 0. These are isolated fixture results, not a new actual139 verification or a claim that remaining semantic/grounding failures are resolved.

## Frozen implementation hashes

- `verify_inverse_reviews.py`: 61,320 bytes; byte SHA256 `3b506ecd16e172763e7cb7ad422d86ccbc914f835d45b9a409e161bacb2805c2`.
- `tests/test_photo_direct_inverse_reviews.py`: 60,435 bytes; byte SHA256 `d36a987845e133f1600d166fcbd520550db151353c758ae7589e3776bbfa2ffa`.
- Unchanged historical revision-2 note: 11,345 bytes; byte SHA256 `38812f5f74489dab560b160c9fe3e53d02138de84600e82037e00beba0920590`.

This note's exact bytes are bound by the adjacent `.md.sha256` sidecar. Root owns any later actual-data rerun, new immutable selection/report, registration and Git action. This task stops at the frozen tool/test/supplement handoff.
