# Supported immutable photo boundary advance

V10 registers the qualified DATA commit 7e769e3e only. Pending CT091 is not
included. This is integration maintenance, separate from the camera query
isolation benefit and independent authoring scores.

## Current registration

`photo_regression_baseline_v10.json` points to the exact V9 manifest bytes.
`photo_regression_baseline_v9_pack.json` is the independently replayed historical
pack, exactly matching V9's pack-byte hash. The validator's explicit supported
version set and newest-first preference add 10; the existing successor loop
still verifies every historical lineage through V10. Explicit V9 validation is
still strict and passes only on its saved V9 pack, not current corrected DATA.

V10 additionally validates pinned current DATA source bytes, independently
recorded old/new DATA provenance and the historical pack hash. It compares the
entire historical and actual current pack after removing exactly these four
leaves, each of which must actually change:

- provenance.tags_hash
- core_retrieval.slot_corpus_sha256
- core_retrieval.canonical_sha256
- pack_id

Everything else must be structurally equal: all 64 complete candidate objects
and their public order, frozen scene/core/control/embodiment/composition fields,
negative prompt, optional adoption and privacy semantics. Existing exact raw
current pack hash, canonical pack ID, input-byte and contract checks remain.
An extra semantic/candidate/order change or recomputed checksum cannot authorize
a metadata-only successor. Full-image quality is outside this proof.

## Later authorized DATA-only changes

1. Qualify the proposed DATA change independently before publishing it. Hold
   unrelated/unqualified changes. Freeze its parent and new DATA commits and
   preserve the existing baseline manifests, archived packs and reports exactly.
2. Run the production CLI with the exact existing frozen request envelope,
   scene core, controls, embodiment review, seed and quality-layer loader on
   both DATA snapshots. Make no input repairs, candidate adoption or provider
   calls. Record full source/DATA hashes and raw output bytes.
3. Compare every JSON leaf and all candidate objects/order independently. A
   metadata-only advance requires precisely the four binding/pack-ID changes
   above, with no scene/core/composition/negative/privacy change. If any other
   delta exists, this workflow does not apply; investigate or obtain a separately
   scoped semantic boundary change rather than broadening the exception.
4. Append a new manifest V(N+1), pointing to V(N)'s exact filename, schema and
   file SHA. Preserve frozen_inputs, preserved_contract_sha256, contract_version,
   public_candidate_count, negative_en and private_fields_absent. Keep the CLI
   recipe unchanged apart from the output filename. Record the qualified DATA
   commits, exact source hashes, comparison evidence and new raw pack hash/ID.
   Archive the immediate predecessor's replay pack without replacing old files.
5. Register the reviewed successor explicitly in the validator's supported set
   and newest-first preference. Add a version-specific transition check against
   its immediate predecessor and pinned proof; V10's V9 comparison remains
   unchanged. The existing lineage loop validates all prior links. Merely adding
   a manifest file never authorizes a version or weakens historical validation.
   Validator edits also require the existing current universal V2 descriptor's
   `validator_contract.sha256` to match the actual source bytes. Archive its
   previous raw file and prove that this one metadata leaf is the only change;
   do not alter historical universal V1, oracle constants, holdouts or expected
   outcomes. This supported maintenance step already exists in the religion/myth
   integration's ILLUSTRATION-VALIDATOR-BINDING-UPDATE.json procedure. Keep sibling
   locations derived from the frozen command and hash source bytes only; never
   import the photo runtime or ingest its semantic DATA into illustration.
6. Test explicit historical-version replay, default current dispatch and complete
   successor lineage. Reject wrong predecessor bytes, DATA commit/source hashes,
   evidence provenance, missing/extra changed fields, candidate edits/reordering,
   scene/composition/negative/privacy drift and recomputed output checksums.
   Re-run affected integration and feasible full tests; preserve missing-asset
   failures and distinguish explicit historical versions from current dispatch.
   Historical generation replay uses that version's qualified runtime and DATA
   snapshot; a current DATA packet must not be silently accepted as an old version.
7. Before publishing, fetch current main and reconcile authorized updates without
   absorbing unqualified DATA. Report the validated head and current main SHA to
   pause the DATA publisher, then perform the ordinary authorized merge/push and
   verify the remote head. A racing main update requires reconciliation and
   relevant revalidation; never overwrite it or force-push.

No automatic version discovery was added: two explicit registration changes are
smaller than a new manifest-discovery mechanism and prevent an unreviewed future
manifest from silently becoming current. A future generalization would need its
own bounded design and tests. Neither this registration nor camera query
separation establishes legacy recall gains or rendered-image quality.
