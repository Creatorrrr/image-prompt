# Mechanical native input preparation contract

Author: `/root/review_06250_07250`, `gpt-6.1-sol/high`, 2026-10-14. This separate tool supplements native-reviews contract_02. It does not modify either frozen verifier/adoption tool, their tests or notes, pilot artifacts, source/catalog assets, registry or runtime. No real preparation is executed by this worker.

`R/prepare_native_inputs.py` validates root-authored exact input selections and writes a new immutable `R/native-inputs/prepared/<name>` bundle. Here R abbreviates this research directory. It is bookkeeping for future direct semantic rereview, not a classifier, proof author or approval system. Pure prepare() and CLI --check write nothing. write_inputs() revalidates all exact artifacts before creating a new directory. Existing output names and traversal are rejected. A failed/incomplete write never creates an approval and must be retried with a new name.

Every artifact ref is exactly `{file, file_sha256, sha256}`: explicit existing path within the repository, raw bytes SHA-256 and canonical decoded JSON SHA-256. Compressed full snapshots retain their original raw bytes/path/hash. There is no source/packet/decision directory scan and no locator fallback. All root/worker actor declarations are protocol assertions, not cryptographic authentication.

## Root preparation plan

Schema `photo-codex-native-input-preparation-plan/v1`, with exactly:

```
schema, actor, original_snapshot, current_proposal, order,
catalog_approval, source_approval, original_selection,
assignment, required_revisions, reason
```

Actor is explicitly `/root`. The first six artifact fields point to exact root-selected full original/current corpus snapshots, full order, catalog approval, source proposal approval and original compiled selection. The entire original/current candidate inventories must equal the complete order, with no added/lost CID. Production always requires18,250; CLI exposes no count override. Python fixtures may explicitly use smaller inventories, which yield production_count_gate false.

Assignment has exactly `{task_name, model, reasoning_effort, start, end, ids}`. Root must state the actual task, `gpt-6.1-sol`, `high`, integer half-open ordinal range and exact ordered CID slice. No task suffix, reviewer name, ID or range is invented. Output ordinals are mechanical enumeration of that explicit range. required_revisions is an explicit map limited to assigned CIDs, using contract_02's exact prior artifact/pointer/hash and memo artifact list. Prior values/memos must hash-match. They are copied unchanged; the tool neither resolves pending meaning nor authors a worker revision.

## Explicit final catalog approval, without a fixed role count

Schema `photo-codex-native-input-catalog-approval/v1`, exactly:

```
schema, actor, status, catalog, catalog_count, catalog_ids,
catalog_sha256, review, reason
```

Actor must be `/root`; status must be the explicitly supplied `final_approved`. Provisional or absent final approvals reject preparation. catalog is the exact full approved catalog artifact. catalog_count is an integer equal to its size; catalog_ids is its exact sorted ID roster; catalog_sha256 is its full canonical digest. It must exactly equal current_proposal.slot_catalog. The tool hard-codes neither141 nor142. This differs deliberately from the unchanged frozen native_adoption v2 production141 gate, which root owns separately if the final catalog grows.

review is the entire existing native_reviews catalog-review object: `{before, after, changes, reviewer, whole_catalog_reviewed, provenance}`. Full historical before and exact approved current after catalogs, directly authored exact delta, whole-catalog read assertion and immutable provenance are checked by the frozen verifier. No role/spec is manufactured from source keywords or previous tags. Catalog approval is an input, never produced by this tool.

## Explicit complete source proposal approval

Schema `photo-codex-native-input-source-approval/v1`, exactly:

```
schema, actor, original_source_sha256, current_source_sha256,
changes, binding_changes, policy_change, reason
```

Actor is `/root`; both full snapshot digests must match. For every original-to-current changed CID, changes contains exactly one `{candidate_id, before, after, delta, reason, provenance}`. Before and after are whole exact records. delta uses contract_02's explicit JSON-pointer subtree edits and must reproduce exactly the provided after; overlapping/no-op/guessed edits reject. Original provenance must remain a prefix. All proposal provenance lists are nonempty explicit artifact refs. Unchanged CIDs may not have invented changes. Changes elsewhere in the full snapshot also need complete root proposals even when outside this particular assignment.

Every binding addition/removal/change needs exactly `{binding_id, before, after, reason, provenance}`; before/after are exact whole values or explicit null. All changed binding IDs are covered once. Changed global policies require `{before, after, reason, provenance}` with whole exact values; unchanged policies require explicit null. The preparer validates/copies these proposals; it never changes a condition, binding ID, role, weight or policy on its own.

current_proposal is an already supplied complete full snapshot. The preparer does not build new meanings from historical corrections or recommended_kind. Existing5B corrections can be represented only by root's explicitly selected and approved complete before/after proposals. A historical pending status stays pending in copied history. A proposal approval merely authorizes that input for later review; it does not approve a native meaning. Even a root-provided source proposal may not install/change/remove native role_evidence through this tool. Historical proof fields, if present identically in both source snapshots, are preserved as given. No native proof, mode, owner, typed value, fact, kind, role, blank semantic list, read completion or approval is generated.

## Original compiled selection and archives

Schema `photo-codex-native-input-original-selection/v1`, exactly:

```
schema, actor, original_source_sha256, records, reason
```

Actor is `/root`; records covers exactly the assigned CIDs. Each row has exactly `{locator, packet, reason}`. locator and full historical packet artifact are root-selected explicit inputs. The frozen native_reviews.compiled_review validates the actual declared compiled file, original raw hash, one-based item, canonical row digest, original source/catalog/reference bindings, actual full historical packet and linked immutable authored judgment. Authored paths cannot substitute for compiled paths.

An optional explicit archive retains the declared original file/item/raw/row hashes plus exact artifact/revision/normalization_manifest refs. Actual archived original bytes, required revisions directory/name, REVISION archive_hashes and before-row hash, root normalization registered file/item mapping, original full-source hash and linked immutable artifacts all pass the existing strict resolver. No guess is made from filenames. Packet bookkeeping displays the original declared `file#item=N`; it does not rewrite a proof artifact string. Frozen old pilot source/proof/reviewer suffix/file strings are never converted, normalized or re-signed. Required revision references may intentionally point to immutable legacy artifacts; preserving those does not make their old shape approved.

## Generated bundle and count boundary

Only four new files are written:

- INPUT.json: exact native_reviews input/v1 fields, preserving original/current/order refs, full supplied catalog review, selected original locators/packets and required revision map.
- ASSIGNMENT.json: exact native_reviews assignment/v1 fields copied from root's explicit task/model/effort/range/IDs, binding INPUT's raw/canonical hashes.
- PREPARED-PACKET.json: whole assigned original/current source records, complete current transitive candidate and explicit binding-guard source closure, exact historical compiled rows/statuses and original declared compiled locator strings. No child qualification or effect union is created.
- PREPARATION.json: root plan ref and document refs/hashes, actual historical statuses and prepared_count. actual_read_count and operational_native_qualified_count are always0; native batch/proof/worker read attestation/root acceptance written are false; canonical_applied and semantic_accuracy_certified are false.

prepared_count is the number assigned, even though full snapshots contain18,250 records. Mechanical decoding/hash checks are not a direct semantic read. The tool produces no native BATCH.json, native proof, worker-note/read attestation, latest root acceptance or global progress update. Worker direct reading, individual judgments, required revisions and separate root integration follow later. A synthetic isolated test separately supplies a hand-authored worker review to confirm emitted INPUT/ASSIGNMENT match contract_02; that review is not preparer output.

Root-only future invocation after all exact approval artifacts exist:

```
.venv/bin/python <R>/prepare_native_inputs.py --actor /root \
  --plan <exact-root-plan.json> --plan-file-sha256 <raw-hash> \
  --plan-sha256 <canonical-hash> --output-name <new-name> --check
```

Remove --check only for the separately intended immutable research input write. No operational apply, registration, Git, model, embedding, image, network or publication action is part of either invocation. No real corpus native approval or semantic correction was added by this tooling work.
