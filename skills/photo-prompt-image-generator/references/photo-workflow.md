# Managed photographic workflow

Read this reference after the independent core is frozen. Before that point, use
only the named neutral precore entrypoint, shapes and current authored inputs in
SKILL.md. The tools calculate bindings and connect artifacts; the author resolves
meaning, writes the photograph, chooses candidates, and reviews actual pixels.

## Frozen inputs and retrieval

`precore/prepare_photo_run.py` provides `init`, `controls`, `canonicalize`, and
`freeze`. Every command except `canonicalize` uses `--run RUN`. Init requires
`--request FILE`, an explicit `--spans FILE` or `--whole-request`, and
`--mode prompt_only|image`. A spans file is an array of objects with exactly
`span_id`, `start`, and `end`; indices refer to Unicode characters. Raw request
bytes preserve CRLF. Controls requires an authored `--context FILE`; optional
`--overrides FILE` and `--seed INTEGER` use the existing resolver.

Freeze accepts the existing raw v3 core plus authored `--selection FILE` and
`--review FILE`. Baseline whitespace must already be canonical before evidence
and body review are finalized. Omit derived SHA fields to have the tool stamp
them; a supplied conflicting digest is rejected. The selection may contain only
`selected` on input; every category, basis, reason and literal evidence remains
authored. An explicit zero-choice composed selection is similarly required.
Camera direction/height requirements come from the author's separate ownership
declaration; the workflow never infers a capture camera from a depicted device.

New runs use the installed H-only+F2 default. Follow [installed-h-f2.md](installed-h-f2.md) to author and seal the per-slot expression plan, then use:

```bash
python skills/photo-prompt-image-generator/scripts/photo_workflow.py retrieve --run RUN
python skills/photo-prompt-image-generator/scripts/photo_workflow.py view --run RUN
python skills/photo-prompt-image-generator/scripts/photo_workflow.py compose-audit --run RUN --composed final.json
python skills/photo-prompt-image-generator/scripts/photo_workflow.py prepare-render --run RUN --parameters transport.json --lane api
```

No policy/generation/store options are required. The installed release is independent of CURRENT and the research checkout. Missing files fail closed. New material retrieval accepts only local hybrid H-F2; keyword-only, precap, remote source and nonzero seed overrides are rejected. Repeated retrieve and resume reuse exact issued material evidence. The receipt pins the immutable generation for later views and audits. An incomplete material transaction requires reconciliation; it is never retried as a fresh search automatically.

H-F2 materials and the native guard pack remain separate. Native whole-source adoption requires its original contract; creative material decisions grant no native authority. Existing bound native runs continue through their original local implementation.

Discovery and adoption have separate contracts. Before selecting a cue, read its
complete source, actual realization and whole native v4 facts, prerequisites,
preservation duties, owner bindings and effects. Every selected candidate,
including a transformed choice, must pass whole-cue admission against the frozen
core and its property locks. An unqualified source may remain discoverable during
the corpus migration; it cannot be adopted as a qualified cue. A score or role
tag cannot supply a missing frozen owner, anatomy, age or property fact.

For an adopted source with `owner_selection_requirements`, author the composed
`owner_selections` described in
[composition-contract.md](composition-contract.md#explicit-existing-owner-selection).
Choose only compatible actual owners already declared before retrieval. Keep
the single public pack and frozen core unchanged; optional unselected children
need no mapping. A successful composition audit stores a source/core/graph and
composed-bound owner-resolution receipt. A changed owner mapping after that pass
requires a new run, while a failed audit can be corrected normally. Render
preparation copies the audited receipt and composed hashes; transport parameters
cannot supply or override them, and runtime recomputes the same resolution.

Source-local relationship conditions resolve through the same exact selected
CID, realization and owner mapping. Satisfy the independently frozen part,
distinctness, typed-value and preservation obligations described in
[composition-contract.md](composition-contract.md#conditions-on-the-selected-source-owners).
Missing choices remain review-only until resolved; an actual failed relationship
is ineligible. The final audit reconstructs member and presentation conditions
from the selected source closure, then runtime checks them again.

Intrinsic, selected-branch, explicit presentation and selected dependency
conditions remain cumulative. Conditional reference or identity preservation
uses the exact caller input inventory and frozen scope inventory: known absent
is inapplicable, known present preserves every scoped frozen item, and missing,
incomplete or unknown information needs review. Equal proposed values still
count as mutations when checking property locks. Supply literal final-prompt
`scope_preservation_evidence` for every protected actual owner and typed value.

Use exact candidate IDs and presented realization IDs. For compound choices,
provide `dependency_selections` by child CID and actual RID when selecting an
optional child or choosing among child alternatives. The parent's own effects
remain in force. Unselected optional members add no adoption, conditions or
effects; required members remain required. A source binding is a presentation
relationship, not child identity. Do not choose an arbitrary replacement binding
when the requested role changes or a source needs correction.

For an actually selected member with positive source requirements, provide its
literal `member_requirement_evidence[parentCID][childCID]` as
`{concept_units: {index: literal}, relations: {relationID: literal}}`. Keep the
source-defined requirement separate from the child's body. Its manually reviewed
native binding must match a fact on the actual selected child RID; a new mutation
outside that child's declared effects needs source correction and rereview.
Unselected optional edges require no member render evidence.

For a conditional visual profile, read `native_profile_choices` and explicitly
choose an actual eligible RID. Preserve its exact `selected_profile_contract`
and provide `selected_profile_evidence` by the selected obligation's required
fields in the candidate interpretation or transformed decision. Required
profiles need an explicit choice; optional unselected profiles add no duties.
The audit compiles render gates from that chosen projection and checks its
source, meaning, body and obligation hashes. A common registry profile, a
different branch or the first listed alternative cannot supply this contract.

Compose accepts the existing authored composed schema. It stamps pack/core/lock
and review SHA bindings; it does not create interpretations, decisions, reasons
or evidence. It preserves quality warnings separately from blocking failures.
Use a new run to revise composition/transport after any invocation reservation.
Earlier immutable revision files remain available.

Transport parameters require an explicit `references` array, including `[]`.
They may additionally contain `referenced_image_paths`,
`num_last_images_to_include`, `transparent_background`, `runtime_prompt_en`, and
`runtime_negative_en`. The default runtime string is the exact composed text and
optional `\n\nAvoid: ` suffix. The existing runtime auditor checks references and
bindings. The API lane also applies the P0 text-only transport restrictions and
accepts optional `--model`/`--size`. References are never removed to fit that lane.

`deliver --run RUN` freshly audits the prompt-only result. `status --run RUN`
reads neutral file bindings and operation summaries without parsing candidate
payloads. Any mismatched artifact is stale, even if a stored audit says pass.

## Authorized execution and recovery

`authorize --run RUN --scope scope.json` records existing human authorization:
an object with exactly `lanes` (`api` and/or `native`), `invocation_limit` (positive
integer), and `authorization_source` (the actual session instruction). This
record cannot create permission. Reuse existing authorization; do not ask again.
Prompt-only runs reject actual rendering. Prepare and audit before requesting
any missing authorization for a concrete execution.

```bash
python skills/photo-prompt-image-generator/scripts/photo_workflow.py render-api --run RUN --ledger generated/photo-runs/image_runs.ndjson --dry-run
python skills/photo-prompt-image-generator/scripts/photo_workflow.py render-api --run RUN --ledger generated/photo-runs/image_runs.ndjson --attempts 2
```

Dry-run reads no API key, invokes no provider, and appends no attempt row. Actual
API execution reuses the P0 adapter's four original inputs and real audits. An
operation and each actual attempt's timestamp/run identity are durable before
calling. Transient calls consume the same budget. The generic repair cap of one
additional invocation overrides the API default of two attempts. Cross-child
reservations beside the ledger and recorded retry descendants also consume the parent's budget;
unknown reservations stay conservative until reconciled.

`operations/OPERATION.json` is a structured execution journal, including exact
recorder arguments and returned-byte recovery paths. Identical operation/row
replay is idempotent; different content with the same identity conflicts. Ledger
append uses a file lock and atomic replacement while preserving historical bytes.
`resume --run RUN` may reconnect a saved record without an image call. It never
rerenders an uncertain invocation or treats a dead PID as proof no call happened.
Use actual returned bytes or provider/native observations for reconciliation.
No external exactly-once guarantee is claimed.

Policy block, unknown provider outcome, local save failure, and recorder failure
remain distinct and stop automatic rerendering. A returned image is saved as
recovery bytes before ordinary image persistence. Frozen bytes and past failed
reviews are not rewritten into successful results.

## Native tool environment

`native-plan --run RUN` creates an audited exact payload and operation.
`photo_native_bridge.py source` emits `runPhotoNative`, a small JavaScript
function to execute in the Codex tools environment with `tools`, `python`,
`workflowScript`, `run`, `ledger`, and an `observe(result)` callback. It calls
`native-started`, then `tools.image_gen__imagegen` once using the returned payload.
The observer reports only a concrete local path actually returned by the tool,
or `{outcome: "preview_only"}` when no such file is available. Do not infer a
path from a UI blob, cache, naming convention, or unrelated file.

The bridge sends tool errors to the shared capture/recorder path. Native ledger rows bind the exact saved plan and four original inputs; the recorder reaudits them before appending, including any audited runtime addition. Actual local
results go through `native-result --run RUN --ledger FILE --result FILE`; the
observation has `operation_id`, `outcome` (`returned`, `preview_only`, `rejected`,
or `unknown`), and only applicable `image_path` or
`evidence_path`/`evidence_sha256`. Preview-only produces no fabricated image row,
and never causes an extra API call. Conversation-only reference attachment is
not reconstructible by this standalone bridge; attach the exact local reference
and audit it instead. Existing manual native execution remains available.

## Pixel review

`review-shape --run RUN --image ACTUAL_FILE` derives applicable gates, exact image
SHA, and required observation scales. It leaves reviewer, statuses, evidence and
user judgments unfilled. Shapes separate instructions from review wire objects.
Author the applicable reviews, then run `review-audit --run RUN` with
`--generic-review FILE` and/or `--visual-review FILE`. Both existing auditors run
against the exact generation. The workflow also checks declared visual scales.
A valid failure record is admitted with technical qualification `fail`; malformed
records are rejected. Pixel truth and artistic quality remain the reviewer's
observations, and user acceptance remains actual requester feedback.

## Retry coordinator and child binding

Use the neutral `photo_workflow_shapes.json` repair-decision fields. The author
supplies current source spans, actual preserved/changed dimensions and properties,
generic local axes, relevant failed gates, an explicit failure class, and the
already authorized additional invocation limit. `obligation_dimensions` declares
the governing preserved dimensions of every actually effective visual obligation;
code validates closure but cannot independently understand that declaration.
Mechanical error routes require corresponding observed provider evidence.

```bash
python skills/photo-prompt-image-generator/scripts/prepare_retry_context.py prepare \
  --run PARENT_RUN --attempt exact-ledger-row.json --ledger generated/photo-runs/image_runs.ndjson \
  --current-envelope child-envelope.json --decision repair-decision.json --output RETRY_DIR
python skills/photo-prompt-image-generator/scripts/photo_workflow.py attach-retry \
  --run CHILD_RUN --proof RETRY_DIR/retry_proof.json
```

Retries require a current `photo-workflow-run/v2` parent, its native v10 pack and issued runtime receipt v3. Archived runs retain their evidence; create and audit a fresh native run before retrying. No parent-manifest import or historical worker is supported.
