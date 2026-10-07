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

```bash
python skills/photo-prompt-image-generator/scripts/photo_workflow.py retrieve --run RUN
python skills/photo-prompt-image-generator/scripts/photo_workflow.py view --run RUN
python skills/photo-prompt-image-generator/scripts/photo_workflow.py compose-audit --run RUN --composed final.json
python skills/photo-prompt-image-generator/scripts/photo_workflow.py prepare-render --run RUN --parameters transport.json --lane api
```

Retrieve optionally accepts `--seed`, `--runtime-store`, `--visual-intent`, and
the existing remote source policy flags. The first transaction preserves its
seed and policy. A complete staging pair may be verified and admitted on resume;
an incomplete or failed pair requires reconciliation. It cannot silently publish
a new seed/pack. Only one public pack and its exact private receipt are admitted.
The receipt fixes the immutable generation for all subsequent audits.

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
python skills/photo-prompt-image-generator/scripts/photo_workflow.py render-api --run RUN --ledger runs/image_runs.ndjson --dry-run
python skills/photo-prompt-image-generator/scripts/photo_workflow.py render-api --run RUN --ledger runs/image_runs.ndjson --attempts 2
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
  --run PARENT_RUN --attempt exact-ledger-row.json --ledger runs/image_runs.ndjson \
  --current-envelope child-envelope.json --decision repair-decision.json --output RETRY_DIR
python skills/photo-prompt-image-generator/scripts/photo_workflow.py attach-retry \
  --run CHILD_RUN --proof RETRY_DIR/retry_proof.json
```

For an older v6 parent without workflow state, add `--parent-manifest FILE`.
The manifest uses `photo-retry-parent-artifacts/v1`, `runtime_store`, and
`artifacts`. Required roles are `request_envelope_input`, `authorial_core_input`,
`creative_controls`, `pack`, `runtime_receipt`, `composed`, and `render_request`;
applicable `generic_review`/`visual_review` and optional historical selection or
catalog records may be supplied. Each role is an exact path, or an object with
`path` and optional `sha256`. The coordinator computes omitted hashes and uses
the parent's immutable worker to normalize original authored inputs, then
compares them with the actual pack. Imported state and normalized files stay
private. Use an ordinary parent run directory for the shared retry operation,
not the immutable generation directory.

The coordinator verifies the actual ledger row, input bytes, image/error,
reviews, receipt and source generation. It derives effective hard obligations
from actual opt-in selection. The compatible generation worker runs existing
auditors; new source is never inserted into an old generation. Unsupported
historical versions, missing snapshots, environments or projection structures
stop with a code instead of using current DATA.

The child writer reads only `retry_context.json` and
`retry_projection_audit.json`. Proof and `private/` diagnostics are coordinator
inputs, not inspiration. Output is a closed allowlist, with source role/pointer/
SHA provenance for values. Candidate inventories, unselected IDs/scores, previous
feature selections, optional baseline prose and raw errors never enter it.
Unknown nested obligations stop explicitly when their complete meaning cannot
be projected safely. Relations retain both endpoints and required evidence.

Create the child using its actual current user request and a new neutral catalog
selection. The author rebinds child span IDs and evidence in its new baseline;
the tool stamps parent IDs/hashes only. Both nonempty, disjoint v2 dimension
sets are required for executable lineage. Local-only scopes that cannot fit v2
still have a closed projection, with
`scope_not_representable_in_lineage_v2`; they cannot execute by opening an extra
dimension. Child freeze and subsequent operations rederive the parent proof and
check preserved locks, assertions, interaction endpoints, effective obligations
and local axes. Existing control values in the context are preserved too.
