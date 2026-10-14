# Native review and adoption preview contract, correction 02

Author: `/root/review_06250_07250`, `gpt-6.1-sol`, reasoning effort `high`, 2026-10-14. This supplements the immutable first native-reviews contract and note. Their recorded hashes describe that earlier tool version. No frozen pilot, direct-review decision, source amendment, root registration, catalog, source asset, runtime or Git history is rewritten by this work.

`native_reviews.py` is read-only. Valid shape preserves an explicitly authored `approved`, `diagnostic_reviewed` or `pending` status; it never creates semantic approval. A separate exact root batch-acceptance artifact is required by latest selection. The acceptance must retain the worker's exact row/status. All reports retain operational native-qualified count zero and semantic certification false. Actor/task declarations are collaboration protocol assertions, not cryptographic authentication.

The first contract still specifies complete input snapshots, assignment/task/model/high bindings, original full source packets, exact original compiled and immutable authored provenance, explicit before/after source delta, full v3 meaning/catalog/spec/native-contract proof, complete source/reference read attestations, and prepared versus actual-read counts. A pending or legacy pilot artifact has no automatic upgrade. A root-required revision binds the exact prior immutable judgment pointer/hash and memo artifacts; the assigned worker must explicitly author the matching revision, and root must separately accept that new row. The tool contains no ordinal-11 or other pilot exception.

## Exact historical compiled locator

A locator retains its originally declared actual compiled file, one-based item, raw original file SHA-256 and canonical row SHA-256:

```
{file, file_sha256, item, row_sha256}
```

The native proof's original_review.artifact must be that actual declared `file#item=N` string. Authored item paths, `file#N` and inferred alternate paths are rejected. Existing frozen proof strings are never converted or re-signed.

If a subsequent sparse amendment changed the live compiled file, root may explicitly add:

```
archive: {
  artifact: {file, file_sha256, sha256},
  revision: {file, file_sha256, sha256},
  normalization_manifest: {file, file_sha256, sha256}
}
```

The artifact is the actual original compiled bytes under `R/revisions/<normalization-manifest-stem>/<original-basename>`. Revision must be that directory's exact `REVISION.json`; the explicit root normalization manifest must be under R/worker-notes. Raw archived bytes must match the original declared file hash, the archive artifact binding and revision archive_hashes. The revision must bind the exact root normalization manifest. Its before row/hash must equal the actual archived file item; the root manifest must map the same original registered file/item/before-row hash. Root authority flags, original full-source hash, linked immutable authored/note artifacts, previous authored locator and after-change mapping are also checked. An archive path is never discovered by scanning, basename search or authored-file substitution. The declared historical file/item and proof provenance remain unchanged.

## Latest contribution reuse

The root latest manifest binds the final full original/current snapshots and full order, plus exact assignment/batch/note/acceptance artifact references. Every final CID must have exactly one accepted latest row, with pending zero. Production has exactly 18,250 IDs; CLI exposes no fixture-size override.

A batch's historical whole current snapshot hash remains its actual input history. It need not equal a later final snapshot when only unrelated CIDs changed. Reuse instead requires:

- The batch original snapshot is the final manifest's exact frozen original snapshot.
- Its entire catalog and global policies fingerprints equal the final current catalog/policies.
- Every assigned row's entire source_after equals its final current CID value.
- Its complete final required/reference CID closure has identical full source records, apart from separately inserted role_evidence proofs.
- Every referenced guard binding is the exact final full binding definition; transitive CIDs reached through bindings are included.
- Every dependency proof equals that CID's separately accepted latest proof.
- All accepted proofs validate again together against the final current full corpus/catalog.

Therefore an unrelated CID correction is reusable only when that CID itself also has its own exact accepted latest judgment. A changed own body, reference body, guard binding, policy, spec/catalog, or child proof rejects stale reuse. Historical input hashes and read counts are not replaced with final hashes, and no worker is described as reading unrelated changes.

## Adoption v2 manual document

`native_adoption.py` production CLI accepts only `photo-codex-native-adoption-manual/v2` and an explicit latest manifest. It re-runs verify_latest before building and again when writing through write_preview_v2. Historical-v1 production build/write are disabled; small old fixtures remain supported for regression tests only.

The complete v2 document has exactly:

```
schema, actor, latest_manifest_sha256, original_source_sha256,
current_source_sha256, catalog_sha256, member_contract,
records, source_approvals, reference_approvals, binding_approvals,
policy_approval, member_guard_migrations
```

Actor is `/root`; member_contract is `candidate-id-presentation-role/v1`. Hashes bind the final root manifest and exact original/current source/catalog. Production additionally requires the fully reviewed 141-role current catalog. Every contributing input's catalog review preserves full historical before and full reviewed current after catalogs, exact explicit delta, whole-catalog review and immutable provenance artifacts. There is no historical139 role-set equality constraint.

`records[CID]` is exactly `{review_sha256, proof_sha256, bindings}`. The binding keys exactly equal that accepted native proof's role keys. Each binding is a fully and directly authored `{id, candidate_id, slot_id, role, semantic_role, conditions, weight}` object, including retained values. IDs are never generated; conditions are never copied from intrinsic meaning or replaced by default empty objects. Conditions/weights/roles/IDs and additions/deletions all require exact policy inputs. Current role specs, source/RIDs, facts, modes, owners, whole effects and dependency qualifications are validated by the frozen native v3 validator.

Every changed original-to-current CID needs a source_approvals row `{candidate_id, review_sha256, before, after, delta, reason}` exactly matching its accepted full source judgment. Every added, removed or changed typed CID/binding reference leaf additionally needs `{candidate_id, review_sha256, pointer, before_exists, before, after_exists, after, reason}`. No replacement is calculated or performed from those approvals. Every original-to-final or current-to-final binding addition/removal/change needs `{candidate_id, review_sha256, before, current_before, after, reason}`. Both full original and full current input values are bound, including when the final value equals original history but would undo a current edit. A binding ID cannot be moved to another CID; use explicit deletion plus separately named new identity if independently reviewed. Non-identical global policies require an exact full `{before, after, reason}` policy_approval; unchanged policies require explicit null.

Unknown or unconsumed subject_applicability fields are rejected, including inside actual branch conditions. The current guard consumer recognizes list fields subject_categories, deny_subject_categories, allow_domains and deny_domains, plus boolean allow_domains_override_subject_categories and require_domain_match. Source condition top-level keys still obey the existing canonical condition contract. This tool does not translate unsupported source policies. Such a source needs explicit review/correction or a separately integrated consumer contract.

## Former member guard migration boundary

Final preview members require explicit CID and no binding_id. An explicitly authored presentation_role must name the current catalog; an absent presentation_role stays absent. No old role is chosen automatically, and no (CID, role) binding lookup is assumed. Positive requirements remain semantic/render obligations under the frozen native requirement_bindings contract. The existing validator enforces exact parent requirement source hash, positive pointer/quote, actual child RID/fact semantics, full child proof digest, required versus explicit_optional selection and whole parent effects. Runtime selected-edge literal requirement evidence belongs to final composition, not this research preview.

Every original member containing binding_id needs an explicit member_guard_migrations row with exactly:

```
candidate_id, review_sha256, before_pointer, before_member, before_binding,
after_pointer, after_member, classification, condition_targets, reason
```

The entire old member and actual full old binding must match the original source; parent review hash must match the latest accepted row. after_pointer explicitly addresses the actual final member; after_member is its exact full value without binding_id and with the same CID. A removed member instead requires both after fields null and actual absence of that CID edge. A former binding-only source edge may gain an explicitly authored/reviewed CID only when it matches the exact before binding's CID; this validation does not create or infer the new member.

Classification is explicitly authored as transferred_to_source_conditions, already_enforced_intrinsic, or reviewed_nonessential. The first two require nonempty condition_targets; the last requires an explicitly empty list and an individual rationale. A target is exactly `{candidate_id, review_sha256, before, after, reason}`, binding full original/final canonical conditions to that target's separately accepted review. Transfer requires an actual condition change; already intrinsic requires exact unchanged conditions. All changes also require the separate whole source/reference approvals above. The code does not decide which condition is essential, equivalent, redundant, or nonessential. Root and worker explicitly own those judgments. There is no new unconsumed member-guard schema, blanket intrinsic copy, silent condition deletion or arbitrary binding retarget.

The resulting preview ledger explicitly says full_runtime_consumer_integration_verified false, native_changes_applied false, runtime_activated false, index_rebuilt false, stage06_complete false, semantic_accuracy_certified false, operational_native_qualified_count zero. The remaining old runtime membership/materialization/admission branches and search-only absent-proof accommodation require root's later consumer integration and full migration gates. This preview never performs those actions.

## Immutable output and invocation

build_preview_v2 is a pure in-memory operation. write_preview_v2 reopens and verifies the full accepted input set and writes only a new R/native-previews/<new-name> directory. It refuses an existing directory or traversal name. Its six input/result documents preserve original corpus, before-native current corpus, next corpus, change ledger, exact root latest manifest and exact manual qualification. PREVIEW-COMPLETE hashes the documents and explicitly says applied false. No existing preview is overwritten.

Root-only future invocation, after the complete real manifest/manual files exist:

```
.venv/bin/python R/native_adoption.py --actor /root \
  --latest-manifest <exact-root-latest-manifest.json> \
  --manual-qualification <exact-root-v2-manual.json> --output-name <new-research-name>
```

`R` is documentation shorthand for this research directory, not a literal CLI path. This worker executed only isolated synthetic fixture previews under temporary directories. It did not run this command against real pilot or corpus artifacts. Fixture and hash validity do not prove semantic truth, artistic quality or pixels.
