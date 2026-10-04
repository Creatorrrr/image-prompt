# Independent v9 boundary verification and minimal successor recommendation

The pre-nape 8a0fb5b production CLI replay of the exact frozen current_boundary
inputs and seed 910000 reproduces immutable v9 bytes exactly:
`5776db59f7c06fb0ba590b7365309f044f4aa1f93594e3ad466aa90d8b1539df`.
Current DATA main 7e769e3e and the frozen camera implementation produce identical
bytes with SHA-256
`6b1e97923886f2fddee94fcfafbda799b903bb109e20eba3d17dc3ac3a96c319`.
The recursive independent comparison finds exactly four changed leaves:

1. provenance.tags_hash
2. core_retrieval.slot_corpus_sha256
3. core_retrieval.canonical_sha256
4. pack_id

All 64 complete candidate objects and their public order are identical. With no
other leaf differences, scene, composition, negatives and privacy fields are also
identical. The independent result and exact before/after leaf values are preserved
in independent-v9-boundary-verification.json. This corroborates the DATA worker's
diagnosis rather than treating the three validator errors as camera regressions.
No provider calls, baseline expectation edits or rendering claims are involved.

## Minimal justified support

Preserve photo_regression_baseline_v9.json byte-for-byte and every historical
predecessor. Add a new immutable photo_regression_baseline_v10.json with:

- schema photo_regression_baseline/v10 and explicit current status;
- historical_baseline pointing to v9's filename, schema and exact file SHA;
- the actual deterministic current pack SHA and computed pack_id;
- unchanged frozen_inputs, preserved_contract_sha256, contract_version,
  public_candidate_count (64), negative_en and private_fields_absent;
- an explicit metadata-only nape-scope change description and source DATA commit
  7e769e3e, the pre-nape source snapshot and four-leaf comparison evidence;
- the same offline CLI recipe and seed, with only its output filename advanced.

The existing validator already checks successive history, hashes, frozen scene
and public-boundary fields in a successor loop. The two minimal recognition
changes are to include 10 in the default preference tuple currently (9,8,7) and
the allowed version set currently {6,7,8,9}. The existing successor loop naturally
verifies v8, v9 and v10's chain. Preserve its exact current pack-byte and canonical
pack-ID checks; do not strip hashes or silently accept checksum drift. Pin and
verify the new version's source DATA provenance, and retain the independent
four-leaf/candidate-equality control. Reject any additional candidate/scene/order/
negative/privacy delta under this metadata-only transition claim.

Targeted validation should prove the pre-nape v9 replay still matches, v10 matches
the pinned corrected DATA, predecessor/file hashes are enforced, and the same
three integration methods reach their original downstream assertions. Negative
controls should reject changed predecessor bytes, wrong source provenance and
any extra semantic/candidate/order leaf. Historical partial pixel qualification
and missing artifacts must remain reported; this maintenance does not turn them
into rendered-quality passes. A later DATA revision needs a separately reviewed
successor rather than editing v10 or treating all future hash drift as harmless.

This is a recommendation, not an implemented validator or manifest change. The
runtime freeze and original expected outcomes remain intact. It is separate from
PR 5's demonstrated axis-query isolation, unchanged eligible availability, zero
fresh legacy recall gain, and new-mode zero-open compatibility gap. Resolving this
DATA lineage issue does not establish camera rendering quality or remove that
new-mode publication blocker.
