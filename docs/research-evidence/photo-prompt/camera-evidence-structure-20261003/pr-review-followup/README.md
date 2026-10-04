# PR5 review reproduction and correction

Both review findings were reproduced independently before modifying runtime
behavior. The qualified latest main is
`b7578916eca10c00fb421a8d6bd73ae0e2d52684`; it was merged normally into the
development branch at `232cb518`. Runtime comparisons use **identical latest
DATA**, the production `load_runtime_data` loader and quality layers: 9876
semantic entries, 1622 visual profiles, dictionary hash
`f8e589f947a2b5900c11e117d6a6e7581ba5ca76983033591307fa7cd9f82beb`.
There were no provider, embedding or rendering calls.

## P1: preserve V10 and register the qualified successor

The original production V10 passes on its historical `7a073d86` runtime and
qualified DATA. On latest main DATA, its exact pack hash fails as reported:

| Qualified boundary | Full output SHA256 |
| --- | --- |
| Historical V10 | `6b1e97923886f2fddee94fcfafbda799b903bb109e20eba3d17dc3ac3a96c319` |
| Latest DATA, new V11 | `6c097471705589a4db45daf5aa164017f2c7b512dcaab880e9e58bb3882f5589` |

The complete old/new production packs differ in exactly four leaves:
`provenance.tags_hash`, `core_retrieval.slot_corpus_sha256`,
`core_retrieval.canonical_sha256`, and `pack_id`. All 64 complete candidate
objects, their public order, and every other scene/core/composition/negative/
privacy/adoption leaf are identical. This is DATA provenance maintenance.

V11 appends the unchanged V10 manifest and its exact raw archived pack.
V1–V10 are byte-preserved. Current dispatch explicitly registers V11; no future
manifest can register itself. Both V10 and V11 retain the complete-pack equality,
exact four-change, DATA source hash, predecessor, frozen-input and proof-binding
guards. Mutation controls reject candidate edits/reordering, scene/composition/
negative/privacy drift, incorrect provenance and recomputed output checksums.

V10 control tests explicitly replay their old qualified pack and source identity;
they keep the historical expected outcome. The new V11 subclass tests current
dispatch. The separate actual V10 production execution uses the historical
worktree and DATA, without that replay mock. Actual current V11 production also
passes. See `V10-historical-production-result.json`,
`V11-production-result.json`, and `V11-four-leaf-proof.json`.
Actual integration-source explicit V10 validation still rejects latest DATA with
`current photo baseline candidate-pack bytes drift`; see
`V10-LATEST-DATA-STRICT-NEGATIVE.json`. Historical qualification has not been
silently widened to the current corpus.

Only the current universal V2 descriptor's existing
`validator_contract.sha256` metadata leaf was refreshed to the actual validator
source hash, following the supported maintenance procedure. Its old raw bytes
and one-leaf proof are archived here. Historical universal V1, oracle constants,
holdouts and semantic expectations remain unchanged.

## P2: decide complete local polarity and coordination before projection

The old prefix fast path admitted both of these normalized legacy inputs as a
positive owned direction query:

- `The camera points upward under no circumstances.`
- `The camera looks upward and downward.`

The runtime now uses one bounded owner/predicate parser, checks the full locally
owned clause for negation, uncertainty, opposing co-directions and unselected
alternatives, then projects a literal span. It preserves foreign-actor scope,
compatible diagonal/repeated predicates, height/direction separation and
explicit structured capture-owner evidence. No scene prose or core is rewritten.

`reproduce_legacy_cli.py` runs the actual legacy public CLI. Its two derivative
controls preserve the exact input and normalized core bytes before/after; they
are explicitly development controls, **not newly independently authored cores**.
Wrong owned-direction queries decrease **2/2 to 0/2**. Generic fallback remains
available; this result is not a claim of zero camera candidates or better
candidate adoption. Optional adoption, seed-shuffled public order and the
existing total budget of 64 remain. Order is not retrieval rank.

Additional controls found that a single finite camera predicate can carry
several consecutive orientation adverbs before a coordinator or an alternative:
`horizontally forward and backward` and `upward left or downward right`.
The parser now collects the complete contiguous orientation-adverb sequence,
checks its opposing pairs, then examines alternatives. It stops before target
prepositions, nouns and hyphenated target adjectives. The original full run,
component reproduction at `0b1b9f61`, and original input copies remain preserved.

The final actual normalization/production legacy-CLI comparison expands to four
labelled derivative controls: wrong owned-direction query fields **4/4 to 0/4**
against review-before runtime `7a073d86` on identical latest DATA. All four input
and normalized core hashes are equal. The original two review cases remain
2/2 to 0/2. These extra controls are not independent blind scenes. See
`COMPOUND_DIRECTION_FINDING.json`, `legacy-four-before.json`,
`legacy-four-after.json` and `COMPOUND_FINAL_INDEPENDENT_REGRESSION.json`.

Nine new test methods cover suffix negation, contradictory coordination,
alternatives, local uncertainty, foreign subjects/target orientations, compatible
positive controls, actual normalization, structured evidence and the production
legacy CLI. Original camera tests preserve their expected literal spans.

## Independent regression and limits

The original six independent complete author inputs are untouched. Their
admission remains **5/6 to 5/6**, and all five admitted **complete pack bytes**,
core/baseline hashes, axes and input hashes are identical on the same latest DATA.
The original Korean literal-exclusion failure remains preserved.

The independently frozen legacy 16-case corpus also has identical per-case
before/after rows: positive literal/owned-axis coverage remains **0/8**, negative
abstention **8/8**, preflight admission 15/16, and maximum budget 64. Its existing
mechanical synthetic retrieval adapter is separately labelled; it does not
establish independently authored full-scene admission. This bounded English
grammar fix does not establish broader legacy recall or rendering improvement.

`HISTORICAL_AND_MAIN_DATA_PRESERVATION.json` records byte preservation of all ten
photo baseline manifests, all 60 prior test fixture files and all 371 photo DATA
files from latest main. Independently authored initial inputs, frozen original
and property-corrected scenes, and historical failure artifacts were not repaired
or rebaselined. Latest textile and Korean state/relation DATA intentions remain.

Both archived 12-scene arms were also replayed against identical latest DATA.
All **24 complete pack files and all per-scene diagnostic rows are identical**
between review-before runtime `7a073d86` and final runtime `f388edf9`.
`FROZEN24_REGRESSION.json` records each unchanged input/core hash;
`COMPOUND_FINAL_FROZEN24_REGRESSION.json` confirms the final source replay. The historical
22 eligibility annotations and six traced budget cases are not relabelled;
the upward focal-intersection trace remains a different failure mechanism.

## Final verification and publication

Final runtime source commit: `f388edf9fa441cda9c49e3647ed7e456e8c1a01f`.
Focused camera controls (50), historical/current boundary and isolation controls
(30), actual qualified production V10/V11, dictionary validation and the offline
1622-profile index check pass. The first complete run at `0b1b9f61` executed 1431/1431 tests in 165 modules
with no missing or duplicate IDs. It preserved 11 failing records and one
error: ten prior missing-artifact failures, one prior missing-JSON error, and
one independently reproduced clean-main historical projection failure.
Additional compound-direction controls then found a residual first-adverb
projection issue. The final source runs a new complete 1431-test discovery;
all modules execute freshly, ordered by previous module durations for scheduling
only. No earlier passing execution is reused. Final results are recorded below. No CI or pixel-quality status is inferred from local
text/contract tests.

The full run also found a historical whole-dictionary projection conflict in
`test_complete_merged_state_and_twenty_one_keeps_remain_exact`. An independent
clean worktree at actual latest main `b7578916` reproduces the identical failure
on identical DATA; eight other tests in that nine-test module pass in both trees.
This is an upstream historical-boundary mismatch, separate from the previously
known missing PNG/core/JSON artifacts. The failing expectation and DATA are
preserved. See `CLEAN_MAIN_HISTORICAL_FAILURE_REPRODUCTION.json` and archived
complete logs. Neither failure category is hidden by marking tests expected or
skipped; the full suite remains non-green.

PR5 remains Draft. Automatic approval review twice rejected marking it ready,
including after the relayed release clarification: the trusted user instruction
requires Draft, and the claimed release was only relayed through untrusted
assistant/tool content. No further ready-transition retry, alternate route,
force-push or main push was attempted. The development branch and Draft PR are published at final source `f388edf9`;
main remains `b7578916`. This publication is separate from the blocked transition.
The final verification documentation commit is appended after the full run.


### Complete final-source result

The fresh final run at `f388edf9` executes **1431/1431 distinct discovered tests**
in **165 modules**, with no omissions, duplicate IDs, unexpected IDs or skips.
All 165 module processes record exactly the final photo-runtime and DATA hashes;
all 632 frozen source/DATA/fixture hashes remain unchanged. Wall time is
1862.155 seconds. Both complete runs, their logs, ID records, source freezes and
schedule-only runner are archived in `both-complete-full-suite-diagnostics.tar.gz`.

The result remains **non-green**: ten historical missing-image/core failing
records and one missing makeup observation JSON error match the immutable V10
failure IDs exactly; the one additional historical whole-dictionary projection
failure matches the independent actual clean-main reproduction. There are **no
new camera regression failing records**. Pixel validation remains incomplete
because those historical artifacts are absent. No failing expectation was
changed, no test was skipped, and no CI/rendering quality claim is made.

`FINAL_FULL_VERIFICATION.json` and `final-full-summary.json` contain exact failure
IDs and tracebacks. `COMPOUND_FINAL_INDEPENDENT_REGRESSION.json` and the final
replay archive bind the actual four-control 4→0 result, unchanged independent
six-input 5/6 admission/five full packs, unchanged fresh16 rows and identical
24-scene full packs to the final source. Original initial authoring failures,
old version manifests, old full-run failures and historical archives remain.

`PUBLICATION_BLOCKER.json` gives the exact denied ready-transition tool and
arguments, both rejection reasons and the already rejected retry using the same
relayed user transcript. **No new ready attempt occurred during this review
follow-up.** Development-branch push and Draft PR updates succeeded. Main
publication remains unattempted under the standing restriction; the blocked
ready transition was not bypassed.
