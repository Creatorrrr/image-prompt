# DATA cleanup integration with current main

This directory records the integration of the completed 37-row DATA cleanup
with the independently updated upstream `main`. It supplements, rather than
rewrites, the historical cleanup reports and their evaluation limitations.

## Source history and preservation

- Original cleanup base: `769f005f01fd54e302e0399e44ac1b2b20122c69`
- Fetched and fast-forward-pulled upstream main: `0087e876bc4bc4a086c01977e77ba54e5499d6f2`
- Cumulative cleanup checkpoint: `0e5a98b549a497b576f64edad4f446d594174b28`
- The merge retains both parents and uses no force push or history rewrite
- All 35 changed raw tag rows and two changed extension rows are exactly
  preserved from the cleanup checkpoint
- Upstream's four independent source-row changes, editing-effects extension,
  runtime changes, visual registry/index, and research artifacts are retained
- The generated semantic-index manifest was the only merge conflict; its
  replacement was derived from both verified caches

`source-preservation.json` contains row hashes and the source-composition checks.

## Reconciled semantic index

The actual integrated runtime compiles upstream property-scope metadata into
candidate bundles, so its dictionary hash is
`f0d9e292e189135c064ab271b254163d73b2c9977595f18e1e03460aa6eec0c9`.

- 9,887 documents: 9,145 slot documents, 705 presets and 37 other document kinds
- 9,717 entries match both caches, 37 match only the cleanup cache, and 133 match
  only upstream's cache
- Every selected vector matches its exact generated text, key, provider, model
  and dimensions; shared matching vectors are identical
- BM25F is recomputed from the integrated dictionary and validated by the
  production file-backed semantic-index loader
- Zero missing cache entries, zero embedding calls, and zero additional API cost
- Previous shard generations are preserved

`reconcile_cached_index.py` reproduces the index from the two immutable Git
snapshots. It never reads the project environment file or invokes an embedding
client. `index-reconciliation.json` records cache provenance for every document.

## Existing upstream aggregate-validator failure

The aggregate dictionary validator fails with 22 identical errors both on the
upstream-only source and on this integrated tree. Compare
`upstream-aggregate-dictionary.log` with
`aggregate-dictionary-baseline-errors.log` byte-for-byte.

The unchanged aggregate validator requires each visual profile's
`concept_candidate` object to contain only `concept_terms`. Upstream's 22 new
editing-effects profiles also intentionally contain `core_assertion_discovery`,
`affected_dimensions`, and `affected_properties`. The upstream runtime accepts
and validates these fields for bounded assertion discovery and property-lock
protection. Removing them would damage the independently developed feature.

This DATA merge therefore preserves upstream behavior and reports that existing
validator/schema mismatch. It does not suppress those errors, broaden the
validator, remove discovery metadata, or claim an aggregate-validation pass.

## Verification scope

The focused cleanup suite passes all 102 tests on the integrated tree
(242.612 seconds). The additional upstream-integration suite is recorded in
the adjacent log. A sparse-checkout maintenance-fixture read error was repaired
by restoring the exact tracked blob, and its isolated recheck passes. There are 169 unique passing test cases across the runs: 102 cleanup cases,
66 additional cases on the first run, and the repaired fixture case on recheck.
Final counts and outcomes are recorded in `validation.json`.
This is not a full-repository test, generated-image, or pixel-quality claim.
Earlier frozen retrieval measurements retain the limitations stated in their
original reports; this integration makes no new retrieval-quality claim.
