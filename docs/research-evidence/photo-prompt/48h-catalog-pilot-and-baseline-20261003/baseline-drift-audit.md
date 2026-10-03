# Frozen photo v9 byte-drift diagnosis

## Result

**Introduced by `7e769e3e`, not present at `8a0fb5b8` / `6fb87682`.** The failure is a current-corpus fingerprint/identity change in the immutable v9 candidate pack. For this frozen still-life request, every selected candidate and scene contract is unchanged.

- Prior snapshot: SHA-256 `5776db59f7c06fb0ba590b7365309f044f4aa1f93594e3ad466aa90d8b1539df`, pack `efdad53981af8456`. This is byte-identical to the original saved v9 pack and its baseline.
- Nape snapshot, production, and repeated production: SHA-256 `6b1e97923886f2fddee94fcfafbda799b903bb109e20eba3d17dc3ac3a96c319`, pack `5e136f4f8f1db0ad`. All three outputs are byte-identical, 202,126 bytes.
- All runs use the current `.venv/bin/python`, v9 seed **910000**, and the exact four v9 frozen input files. Only the output destination changes for production; snapshot runs also select their existing absolute script path while keeping the same working directory, interpreter, and frozen input arguments. Command receipts and output hashes are in `replay-results.json`.

## Exact output drift

There are exactly four changed JSON leaves (full old/new values in `pack-leaf-diff.json`):

1. `/0/provenance/tags_hash`: `28e52ed2...` → `8ae1cb27...`
2. `/0/core_retrieval/slot_corpus_sha256`: `e25eb3c6...` → `b1132251...`
3. `/0/core_retrieval/canonical_sha256`: `b6b43915...` → `aa68d0a2...`
4. `/0/pack_id`: `efdad53981af8456` → `5e136f4f8f1db0ad`

No candidate was added, removed, reordered, reranked, or altered in this fixture: the complete `slots` object and all other candidate surfaces are identical. Public count remains 64; contract remains `photo-candidate-pack/v6`. Authorial core, creative controls, authorial composition, negative prompt, and other scene/policy surfaces are identical. The baseline's preserved-contract digest remains `4dd926370d017e22d41e0a1c05f49d9b00ec42b37c050eaa246a8fd2697c9c19`. Public provenance is identical except `tags_hash`; private-field omission and non-exposure declarations remain intact. Both old and new pack IDs independently satisfy canonical hashing.

## Why

`prompt_generator.py:10435` hashes the complete compiled dictionary, including slots. `prompt_generator.py:11538` binds the complete slot-corpus hash into `core_retrieval`, then hashes that binding. The final pack identity includes these fields. Expanding H15/H16 `affected_properties` therefore changes fingerprint fields even for this no-people teacup fixture where none of the admitted candidates changes. This is consistent with the fingerprint contract; it does **not** make the exact-byte v9 assertion pass.

The validator checks scene preservation and private provenance before the full-pack byte assertion (`validate_illustration_assets.py:6509`). Thus the reported error is accurately the byte assertion, not an observed scene/candidate failure. Later count/contract/pack-ID checks do not run after the exception; this audit independently checked them rather than assuming they passed.

## Source qualification

- Existing before snapshot: **127/127 files** match Git blobs at both prior commits, with no missing runtime scripts/precore Python modules.
- Photo runtime Python and all four input files are unchanged from `8a0fb5b8` through `7e769e3e`.
- Existing after snapshot: **143 files** checked against `7e769e3e`. Two raw-byte differences are explicitly qualified: its semantic index is structurally identical JSON with different serialization; the extension differs only in `maintenance_ref`. The runtime modules match, and independent production replays match the snapshot output exactly.
- Original v9 saved pack is `docs/research-evidence/photo-prompt/subculture-appearance-integration-20261003/boundary-preservation/current-photo-pack.json`; its SHA equals the immutable v9 baseline.

See `source-verification.json`, `SUMMARY.json`, and scripts for independently repeatable details. No full source copies were made. Provider keys were blanked for replay, which exercised local candidate generation only. There were no provider/image calls or repository, baseline, validator, or index edits. Git working tree remained clean.

## Safe next step and limits

Preserve v1-v9 and the original v9 pack exactly. Keep the full-suite result marked failed until a separately authorized boundary/runtime follow-up implements the project's successor-observation workflow (for example v10 with explicit current-version routing and history tests), and reruns the affected checks/full suite. Do not overwrite v9, suppress corpus fingerprints, weaken the validator, or report green based on candidate invariance alone. That runtime change is outside this DATA diagnosis.

This conclusion is limited to this exact v9 request and the compared revisions. It does not claim no changes for all requests: nape-locked fixtures deliberately changed eligibility. No pixel or image-quality claim is made.
