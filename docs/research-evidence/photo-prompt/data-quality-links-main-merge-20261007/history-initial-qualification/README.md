# V34 merged scope boundary

The canonical V33 remains the upstream palette qualification at
`c4c0e4ed25981fc46c09de6e138247b5788ea43c`. The local V33 at
`d9dc3df7012f395c48d536ee9df80df060cd24f9` is a separate original qualification.
V34 succeeds the canonical upstream V33 and applies only the three local scope
restrictions. Neither original V33 is renamed or regenerated in place.

`SOURCE-V32.json`, `SOURCE-UPSTREAM-V33.json`, and `SOURCE-LOCAL-V33.json` bind each
original path to its original commit, tree, Git blob, SHA-256, byte length and
file mode. Unchanged payloads reuse authenticated retained files; the sixteen
new snapshots cover paths whose current content would otherwise replace an
original source. Materialization authenticates every member before publication
and rechecks each member during the atomic copy. No Git or network is needed to
run a replay. The source-preservation authoring script uses read-only local Git
objects only.

The original test modules run unchanged in their own materialized source trees:

| Live entry point | Original source | Original assertions |
| --- | --- | --- |
| `tests.test_photo_robe_source_boundary_history` | V32 at `96e20422316276a4e0b5ed97f44152e4931e7504` | 28 |
| `tests.test_photo_palette_boundary_history` | upstream V33 at `c4c0e4ed25981fc46c09de6e138247b5788ea43c` | 9 |
| `tests.test_photo_data_scope_boundary_history` | local V33 at `d9dc3df7012f395c48d536ee9df80df060cd24f9` | 16 |

The live modules route execution to those original files. Their assertions and
expected hashes are not revised. `tests.test_photo_data_scope_v34_boundary_history`
adds sixteen current and mutation tests. An explicit baseline request for V32 or
V33 executes the original V32 or canonical upstream V33 validator in a separate
process. A missing or mismatched retained payload fails closed.

V32 requires CPython 3.12.14 and Unicode 15.0.0. Both V33 originals require
CPython 3.14.3 and Unicode 16.0.0. Runtime selection probes the real child
interpreter and requires exact equality. `PHOTO_V32_PYTHON` selects the V32
interpreter; `PHOTO_HISTORY_PYTHON` selects a V33 replay interpreter. An explicit
mismatched choice fails without fallback. The selected path, probed version,
source commit and manifest digest are recorded alongside the original test log.
Nested original V32 checks inside V33 tests select their own historical runtime.
The original receipts and pack hashes remain fixed, so the original validators
also enforce the qualified algorithm and source-generation bindings.

`V34-DATA-SCOPE-PROOF.json` binds the actual current pack and receipt. The upstream
palette candidate/profile files and source registration are exact bytes. The
only authored changes are six added leaves across three existing records; the
pack delta is four source-binding leaves and motion `candidate_count` 34 to 33.
Candidate objects, order, fixed scene inputs and all 64 public candidate objects
are preserved. The illustration universal descriptor changes only its validator
digest. `INDEX-VECTOR-REUSE-PROOF.json` independently compares all 12,639 texts and
vectors with the upstream original. That equality is separate from the parent's
offline rebuild/API-call evidence.

The old `data-quality-links-20261007/history` evidence and upstream palette proof,
helper and baseline files are immutable. `IMMUTABLE-ORIGINALS-CHECK.json` records
the read-only Git-object comparison. The earlier missing-backup and runtime
mismatch failures remain in their original local evidence. During V34 authoring,
an initial current validation identified the universal descriptor as a live
historical backing; the final source manifests archive that original descriptor
and the other live routing files. That authoring failure did not revise any
original expectation.

This boundary proves authored scope, original replay and runtime reproducibility.
It adds no image generation, embedding request, native-pixel quality or user
acceptance claim. Upstream native PASS/FAIL outcomes and existing unrelated
regression failures remain separate evidence.
