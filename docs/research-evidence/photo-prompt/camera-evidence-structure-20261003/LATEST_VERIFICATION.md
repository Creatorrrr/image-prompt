# Latest frozen-runtime verification, actual-authoring input blocked

Runtime remains byte-identical to 6220d455. DATA main 7e769e3e is integrated
into the development branch. All comparisons here are offline and preserve
original inputs, failed artifacts and expected outcomes.

## Completed full suite

Clean latest-DATA discovery executed **1386/1386 tests across 159 modules** in
2297.406 seconds. There are no missing, unexpected or duplicate execution IDs.
All **159/159 runtime and DATA source snapshots** match the final current files.
The complete summary, per-module results and logs are preserved in
`latest-full-suite-summary.json` and `latest-full-suite-diagnostics.tar.gz`.

There are ten failing subtests and four errors. The ten failing subtests and one
missing source-observation JSON error are the existing missing historical PNG/JSON
failures established by the fresh 1362-test baseline. There are no new assertion
failure IDs. The three additional error methods all call the same unchanged
photo baseline validator and fail with:

`current photo baseline candidate-pack bytes drift`

That validator error was directly reproduced on an untouched main 7e769e3e
worktree. The actual production baseline CLI was then compared on main and the
implementation, with the exact frozen current_boundary inputs, seed 910000 and
identical current DATA. Both output files are byte-identical:

- Actual before and after: `6b1e97923886f2fddee94fcfafbda799b903bb109e20eba3d17dc3ac3a96c319`
- Historical frozen expected: `5776db59f7c06fb0ba590b7365309f044f4aa1f93594e3ad466aa90d8b1539df`

The source change introduces no additional baseline drift in that comparison.
Historical expectations were not rewritten. No complete latest-main baseline suite
was rerun; the direct baseline reproduction and before/after CLI byte comparison
are the specific controls for the three shared-validator errors. Testing is
complete in execution coverage but **not all green**.

The 19 new camera structure methods, 18 existing camera-owner methods and five
upstream nape-scope methods pass. Dictionary metadata validation and visual-profile
index validation pass (1622 profiles, 3837 exact terms).

## Independent and frozen comparisons

On identical latest production DATA (9876 entries/1622 profiles, quality layers
loaded), both archived original and 22-property-corrected twelve-scene arms produce
**24/24 identical before/after pack bytes and scene diagnostics**. Maximum total
candidates remains 64. Budget-bound historical traces concern six cases; the
upward-view focal-intersection loss is not called budget exhaustion. All 24 packs
also pass composition audit with unchanged baseline and zero optional adoptions.
Warnings are retained, and public shuffled order is not treated as retrieval rank.

The fresh independent legacy sixteen-case set remains unchanged at its supplied
SHA-256. Exact positive span match and literal owner-plus-axis coverage are
**0/8 before, 0/8 after**. Negative extraction abstention is **8/8 in both**.
There are zero owned-clause query deliveries; all sixteen result rows match.
The synthetic caller probe admits 15/16, with the existing blanket-negative
preflight rejection unchanged. These probes are explicitly not independently
authored full cores. Development V2 remains development; its 6/6 result is not
promoted into a blind generalization claim.

## Actual independent authoring source cannot yet be evaluated

The independently authored original six-case JSON was transferred through Library
after the delegation body was truncated. Library confirmed authorized version 0,
filename `initial_authoring.json`, size 78046 bytes. The supported current helper
download failed twice, including the one bounded retry pinned to the returned
file identity and the explicit consumer-local destination:

`library file transfer failed: download failed`

No local source file exists. Its expected SHA-256
`2f8daf037ca1d931084eb6f24033ca88bf4af2fa2134c789d9ec519893759242`
has therefore **not** been verified against received body bytes. The underlying
download cause is not supplied by the helper; no permission/authentication cause
is inferred. There were no network permission expansions, guessed transfer URLs,
new credentials or semantic reconstructions. Original stage1 bindings and the
independent source-request axis review are ready; the materializer will preserve
the whole original bytes and unchanged authored fields once an intact accessible
artifact is supplied. `stage2-library-materialization-blocker.json` records the
bounded attempts without signed transfer details.

The current Library skill and its resolved-reference materialization procedure
were used. No Library item was edited or replaced. No actual six-case admission,
query-delivery, exposure, eligibility, adoption or semantic-benefit result is
claimed before the original file is available.

## Merge value and remaining decision

The new legacy parser has demonstrated no independent recall gain on the fresh
set. Compatibility checks and negative extraction controls are useful, but they
do not establish improved scene retrieval or image quality. New-author typed
evidence has developmental tests of source binding and axis separation; format
acceptance alone does not prove semantic ownership or authoring value. The actual
independent before/after must demonstrate correct-owner scoped queries, preserve
unrequested height and explicit negative/positive boundaries, and disclose any
contract rejections, ineligible choices and unchanged exposure. Candidate exposure
must not be called adoption or rendering quality. Existing guards remain intact.

Accordingly **keep PR 5 as draft and unmerged**. An intact original artifact and
the independent actual-authoring value assessment remain the blockers to a merge
recommendation. Parent publication-window coordination is still required. There
are no implementation asset/pre-core changes relative to current main and no
new candidate embedding inputs, paid provider calls or rendering calls.
