# Closed camera scope compatibility fix

This is authorized follow-up development after the frozen initial evaluation,
not a new blind result. Initial input bytes, reports, failures and expectations
remain unchanged. The historical zero-open blocker and draft recommendation in
ACTUAL_AUTHORING_RESULT.md describe runtime 6220d455; this note supersedes that
blocker assessment for fix commit 6e3f81ff.

## Minimal behavior change

The public new-author flag now requires a camera review only when camera already
belongs to the normalized core's open or locked dimensions. A closed camera
domain cannot carry an advisory camera assertion under the existing contract;
requiring one previously made valid zero-open/no-op cores impossible to admit.
The fix neither adds a dimension nor infers a requester lock or permission.

Existing requester-axis checks still run before this conditional requirement,
before candidate DATA loads. Any supplied declaration is validated, including
when it would not be required. Partial camera properties still require an open
camera dimension under the unchanged core normalizer. Open-camera cores still
require the review. Whole-camera locked cores use the existing required assertion
and literal anchors; omission fails. Unresolved ambiguities, foreign ownership,
conflicting locks and literal exclusion grounding retain their prior guards.

Four additional test methods cover zero-open and disjoint open scope, fully
locked camera evidence, omitted required declarations, invented advisory review,
explicit-axis checks and unresolved ambiguity. Synthetic scope reductions are
contract controls, not newly independently authored scene interpretations.
The production-loader zero-open control runs both public CLI modes and verifies
complete pack byte equality and unchanged input files. The existing local
negative/ambiguous ownership and axis-exclusion tests remain in the focused run.

## Untouched independent inputs

Post-fix regression replay uses the same six complete initial inputs, seed 829,
production quality layers and identical DATA (9876 entries, 1622 profiles).
Admission remains 5/6; all six input sets remain byte-identical. All five admitted
packs, normalized cores, baselines, axis queries, property locks and feature
records are exactly identical to the initial after arm. The low-horizontal
Korean exclusion fails with the same source-grounding error. No helper repair,
prose padding, expected-outcome change or reclassification as blind success.
See post-fix-authoring-regression.json and its diagnostic archive.

The initial measured benefit remains query isolation 1/9 to 7/9, with open height
borrowing structured direction evidence 1 to 0. Evidence delivery stays 7/9,
eligible camera availability stays 3, and fresh legacy positive recall stays 0/8.
No independent composition, candidate adoption or rendering quality improvement
has been demonstrated.

## Verification and publication boundary

The focused camera/core/isolation run passes 52 tests. Additional related
authorial/embodiment/pre-core contract results are recorded in
post-fix-validation.json. The previous complete run executed all 1386 tests;
it has ten historical failing subtests and four errors, including three shared
immutable-v9 baseline errors reproduced on main. That full run predates this
small CLI fix; it is not presented as a fresh full-suite pass.

Main c8ad4e46 is integrated and adds only evidence relative to the tested DATA
commit 7e769e3e. DATA, indexes and the pre-core boundary are unchanged by this
fix. The independently verified v9 difference has only four hash leaves, with
all 64 candidate objects and public order equal. Immutable successor support
remains a separate recommendation, not a checksum repair implemented here.

The zero-open compatibility blocker is resolved without a new policy decision.
PR 5 remains draft/unmerged for review of its limited measured value and the
separate baseline lineage issue; no direct main push or merge was performed.
