# Inverse verifier bounded wire revision 2, 2026-10-14

This supplement supersedes only the implementation details enumerated below in `inverse-review-verifier-contract-20261014.md`. The original note, original root selection, original failed verification, worker artifacts and production/native code remain unchanged. The original note remains a historical handoff with its original tool/test hashes.

Scope: update `../verify_inverse_reviews.py`, update repository `tests/test_photo_direct_inverse_reviews.py`, add this supplement. No actual-data verification was rerun by this worker; root will select a new explicit immutable manifest and rerun. No source correction, worker judgment rewrite, operating artifact, native qualification, model/network call or Git action occurred.

Current verifier keeps selection schema `photo-direct-inverse-review-selection/v1` and result schema `photo-direct-inverse-review-verification/v1`, with explicit result field `contract_revision: "bounded-wire-2"`. All previous manifest/hash/closure/fit/verdict-preservation/output boundaries continue to apply.

## Immutable evidence inspected

Root supplied the explicit 43-range / 139-slot / 120-artifact selection and original failed result. The selection's bytes SHA was checked before using its artifact paths. No directory scan was used to select workers or infer completion.

- `INVERSE-REVIEW-SELECTION-139-01.json`: 45,295 bytes; SHA256 `7147b51185889c6ce6f412c90030628924ced9ef903f0ad67226792029797c07`.
- `INVERSE-REVIEW-VERIFICATION-139-01.json`: 4,042,870 bytes; SHA256 `4f652c4d3ef7b8e0e7f3c506d96c2b48d5aa92197fea4d246871ebce9182ceb0`.
- Original `worker-notes/inverse-review-verifier-contract-20261014.md`: 19,007 bytes; SHA256 still `aa968bb35fbacaf2ff1bd96af643150ce805b30934dd6d457a60898fafb6e401`.

All original result failure codes were inspected. Its 161 failures comprise 63 `per_rid_effects`, 36 `metadata_only_primary_fit`, 23 `invalid_worker_contract`, 12 `fit_property_prefix`, 9 `fit_dimension_spec`, 6 `binding_read_declaration`, 6 `missing_binding_read_declaration`, 4 `evidence_source_body_pointer`, and 2 `impact_schema`. The 23 parse failures identify 21 missing `baseline_query_sha256` lookups and two missing `immutable_adjudication_path` lookups. The changes below address those evidenced wire gaps. This is not a claim of a newly passing actual result.

## 09250 explicit query hash spelling

The initial checkpoint uses `slot_reviews[*].baseline_query_sha256`; subsequent explicitly selected files such as `authored/inverse_09250_006_008.json` use `query_sha256`. Both are explicit hashes of the same saved query and are now supported through the bounded field reader. If both keys are present they must agree. The authored value must equal the selected query-plan query's exact `text_sha256` in either case. Missing, conflicting or stale hashes still fail. No new query is generated and no key is renamed in preserved raw data.

## 07250 proposed-impact-only schema

The last two explicitly selected impact files (124–134 and 134–139) contain exactly:

```json
{
  "schema": "photo-inverse-proposed141-impact/v1",
  "task_name": "/root/review_07250_08250",
  "slot_start": 124,
  "slot_stop": 134,
  "review": "<original authored impact prose>",
  "new_141_native_runtime_completeness_claim": false
}
```

This exact six-field schema is a separate bounded parser. It requires the selected task/range, nonblank review string, false completeness claim and no unsupported fields. Its file remains descriptor-bound by the root manifest and explicitly associated with the selected adjudication through that selection's `impact` ID. The original object is preserved as `raw_impact`.

These impact objects **do not contain** an adjudication hash or read counts. The verifier does not invent either field or copy calculated counts into them. `impact_validation_contract` explicitly distinguishes:

- proposed-impact-only: binding is selected artifact plus exact task/range; `authored_adjudication_hash_present=false`, `authored_read_counts_present=false`;
- existing checkpoint-scope schema: the separately authored adjudication canonical hash and read counts remain mandatory and checked as before.

The new schema's prose is preserved, not interpreted as a second semantic verdict or machine proof that all proposed definitions are equivalent. Pair coverage, source hashes, closure, conditions/effects, RIDs and fit facts are still independently checked in the selected adjudication. Unknown schemas, incomplete six-field objects, wrong task/range, extra unsupported fields or a true completeness claim fail.

## Derived per-RID dimension order

Examples in the original result show the same dimension IDs in different orders: source root `['action','timing','material']` versus worker derived `['action','material','timing']`, or `['framing','format']` versus `['format','framing']`.

Only `actual_effects_by_realization[*].dimensions` is compared as an unordered set of **exact unique string IDs**. Both compared sides must be lists of strings with no duplicates. Actual RID keys and effect-object keys must agree; missing or additional dimensions, duplicate dimensions, non-string values and foreign RIDs fail. Properties and every other value retain exact canonical comparison, including property owner, dimension, property spelling and property-list order. Root effects and intrinsic conditions remain exact full-source comparisons.

Comparison operates on copies. Worker raw rows and source expectations retain their original dimension order and all original properties. This is a mechanical ordering allowance, not a semantic synonym mapper or mutation-footprint exemption.

## Canonical branch positive concept units

The explicitly selected 11870 065–068 file has a fit source anchor and positive slot evidence for `cand_aceaa5a1d9465f5a9e9ded075cefeac0` at:

```text
/effects/realizations/branches/0/concept_units/1
"Signal dropout appears only in the already declared recorded playback image."
```

The complete frozen source places that exact string in branch ID `visible_recorded_playback`, mode `optional`; the actual RID list is `base` plus `visible_recorded_playback`. The original authored role-scope prose explicitly limits the fit to that branch. The verifier previously classified every `/effects/...` pointer as non-body, which was too broad for this canonical positive-unit surface.

Revision 2 adds only this exact pointer shape:

```text
/effects/realizations/branches/<canonical unsigned list index>/concept_units/<canonical unsigned list index>
```

A pointer-only check cannot authorize it. The checker must resolve the original source record, a `one` or `optional` realization object, the actual branch at that index, a unique nonblank branch ID other than `base`, a nonblank concept-unit string, and inclusion of that branch ID in the row's exact source-validated actual RID list. The ordinary exact quote, CID and full source-hash checks remain mandatory. An explicitly authored evidence `realization_id`, when present, must equal the resolved branch ID; null, a foreign RID or another branch's RID cannot fall back to a derived value.

Each normalized row now retains `branch_positive_evidence_bindings`, including full source SHA, CID, exact pointer, source branch index, concept-unit index, surface name `canonical_branch_concept_unit`, and exact actual `realization_id`. Repeated source-anchor/positive-fact uses of the same binding are deduplicated. Identical sentences in two branches remain separately bound to their respective actual RIDs. This does not make a branch fact a common/base fact and does not certify native qualification.

No other effects surface becomes positive evidence: root/branch `effects.properties`, `dimensions`, branch IDs, conditions, context terms, evidence/discovery terms and other metadata remain rejected. Noncanonical/absent indices, stale hashes, missing/foreign RID bindings and wrong literal quotes fail. Existing `/content/...` checks and negative/routing/review metadata deny rules remain unchanged.

One original `metadata_only_primary_fit` failure is the above branch-positive pointer itself. The original count of 36 therefore consists of this evidenced wire misclassification plus 35 other metadata-surface failures. Supporting the explicitly authorized branch surface can remove that single misclassification; it does not waive the remaining routing/alias/evidence-term cases. Actual revised failure counts are intentionally left to root's new immutable run.

## Unchanged substantive failures

No convenience relaxation was made for:

- discovery/alias/evidence-term-only primary fit facts;
- required binding-read declaration/hash omissions;
- manually authored properties outside a selected spec's prefixes;
- manually authored dimensions outside the spec;
- missing/duplicate top3-union pairs, stale source/closure/guard hashes, changed source conditions/effects, invalid owner literals, or verdict spellings.

The original 12 binding errors are two codes on six source rows, not 12 independent source records. Existing tests still require these errors. Metadata anchor failure is not a machine claim that the authored semantic judgment is false; the worker/root must manually reread and supply suitable positive grounding or an explicit authorized source correction. No automatic tag/native authoring is performed.

## Isolated fixture changes and validation

The existing 33 tests remain and pass. Eight additional tests cover the evidenced query spelling, exact six-field proposed-impact schema, unchanged raw data, unique dimension-set comparison and adversarial differences, exact branch-unit source/RID binding, and rejection of effects metadata. Optional fixture-only source branches now have explicitly authored concept units, conditions, context and evidence terms when requested by a test; the default existing fixture remains unchanged. This supplies a real positive source unit and real counterexamples rather than inferring positivity from candidate keywords.

Executed with network denied and an empty environment (keys removed):

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p test_photo_direct_inverse_reviews.py -q
```

A counted final run using `unittest.TextTestResult.addSubTest` produced **41 tests / 60 subtests, 0 failures, 0 errors**, 1.506 seconds. It exercised only isolated fixtures. No original actual-data manifest was rerun, and no new actual verification JSON was written.

Current frozen implementation:

- `verify_inverse_reviews.py`: 58,615 bytes; byte SHA256 `4d71093d4f0d451bd69d5f6cddffdc105f80c2decdecd79d91488691e3cfa11a`.
- `tests/test_photo_direct_inverse_reviews.py`: 49,317 bytes; byte SHA256 `ca61181a3b22e649872feb72535567d0113ecffe04f2c1c67b0a73d1176b7627`.

Root next step: independently review this revision, create a new explicit immutable selection with the revised tool/test/supplement bindings, and rerun into a new explicit immutable verification JSON. The original failed report and selection remain historical evidence. Production conditional-reference/profile projection gaps remain outside this revision and await separate root authorization.
