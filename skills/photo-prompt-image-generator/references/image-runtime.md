# Image Runtime

## Default Tool

When the user asks to create or render an image, use the session's native image generation tool with the audited `prompt_en`. Append the preserved negative prompt as `Avoid: ...` when supported.

Follow the current user instructions and existing session authorization before these procedural defaults. An already authorized generation, API fallback, or API cost does not require repeated confirmation. Use the requested attempt count and runtime when they are specified.

When `embodiment_preflight` is active, also copy its exact `canonical_sha256` into runtime `source_embodiment_preflight_sha256`. Use only the reviewed composed prompt and optional exact `\n\nAvoid: <negative_en>` suffix. New runtime prose requires recomposition and a fresh review. After generation include the applicable `embodiment_*` gates derived from the exact composed review; [embodiment-preflight.md](embodiment-preflight.md) defines their criteria. They join the existing strict checklist even on an initial generation, without fabricating repair lineage.

Before the tool call, serialize the exact native runtime inputs as `photo-image-render-request/v2` and run `scripts/audit_image_render_request.py`. The request must include `core_retrieval_sha256` copied from `core_retrieval.canonical_sha256`, `pack_id`, exact `runtime_prompt_en`, exact `runtime_negative_en`, the composed and runtime audit boundary, and every attached reference path, SHA-256, and role. For a intent-locked v6 pack, it must also include `source_intent_lock_sha256` copied exactly from `authorial_core.intent_lock.canonical_sha256`. When the pack contains `render_repair`, also copy its exact `canonical_sha256` into `render_repair_contract_sha256`; omission or mutation blocks generation. The audited composed prompt must occur contiguously inside the runtime prompt, while the runtime string remains `not_run` until this exact-input audit passes. When `chosen_visual_concept_ids` is non-empty, also include the auditor-derived `effective_visual_contract_sha256`; this binds the optional selection to the hard contract used after rendering. The inherited composed PASS includes `photo-negative-intent-guard/v1`: do not append a platform-safety summary, recipe suppression, coordinator instruction, or new `Avoid:` item after audit. The runtime auditor scans both the complete positive runtime string and `runtime_negative_en` for the union of core `runtime_forbidden_labels` and active-profile `runtime_expression.runtime_forbidden_labels`; a shorthand label may aid meaning resolution but may not leak through either runtime surface. A negative mismatch, negative-intent-guard failure, runtime-label leak, missing intent-lock or repair-contract binding, missing reference, hash mismatch, visual-contract mismatch, or missing/failed inherited composed audit blocks generation. An inherited composed PASS is required. Reference-role meaning is reviewed by the caller; the runtime auditor verifies the supplied files and exact digests.

For `reference_identity_control`, inspect the concrete local source image first and pass that exact file through the native tool's reference-image mechanism. Do not describe a reference path in text without actually attaching it. Use the audited prompt's identity-preservation sentence, and keep the source portrait unchanged as the comparison control.

After a saved result returns, derive its gates from the exact pack and audited composed selection. For an identity-controlled result, compare the requested visible reference features against the source and current user-preferred baseline when one exists; a visual comparison does not establish a person's identity. Apply only the active reference-preservation gates. For v6 character response, review the frozen actor-target-action-affect-consequence relations and declared visual obligations; never add a gaze, facial landmark, head direction, pose, or crop merely because of a named archetype. User preference remains a separate terminal judgment.

Also inspect the complete image against the initial artistic direction. Describe whether its overall impression, subject presence, and hierarchy work together, and whether optional staging feels convincing in this scene. For people, assess appeal through the whole portrayal rather than face size or a required expression. Keep these observations in a supplemental review field or file; they are qualitative judgments, not extra hard gates or requesting-user acceptance. A technically qualified image may still be artistically weak. Use that distinction in any authorized revision or comparison, without starting another generation solely to fill an evaluation record.

Record those observations in a `moe-render-review/v1` JSON object, then run `scripts/audit_moe_render_review.py` with both `--pack` and the exact audited `--composed` object. The auditor derives the checklist from active typed v6 `character_response.render_gates`, unconditional visual obligations, and only the selected visual-concept opt-in gates. Use only exact `pass` or `fail` statuses and include image-grounded evidence for every hard gate; `partial` is deliberately not promotable. Honor each visual gate's declared `review_scale` and require all components in the same saved image. With a typed character-response or effective strict visual contract, `hard_gates` must exactly equal the derived checklist; put crops, comparisons, and supplemental observations in separate fields or files. The review must name the exact result path and SHA-256. For pending user review, set `user_judgment.source` to `not_yet_received`. Only a direct requesting-user decision may use `source: requesting_user`, and it needs a concise quote or faithful summary. A nonzero exit preserves the render as failed or pending evidence rather than deleting it.

When `render_repair` exists, separately record `photo-image-render-review/v1` and run `scripts/audit_image_render_review.py`. Review the exact generated file at every declared thumbnail/native scale and supply one `pass` or `fail` row for the exact contract gate set: object-class legibility, gross structural coherence, intended interaction match, and contact anatomy when contact is required or transitional. These are major gates for meaningful action-bearing props; minor ornament, decorative engraving, and background accessory variations are non-blocking. The auditor validates the image hash and review record but does not infer pixels or requester preference.

A missing native local path alone does not authorize a new paid API call. Use the OpenAI Images API when the user's request or existing session authorization covers that runtime and cost, including an authorized fallback. Do not require a second confirmation or a special wording of permission already given. If paid API use is outside the authorized scope, prepare the exact audited request first and ask once for the concrete API attempt.

## Saving

Copy a native result into `generated_images/<concept>-<timestamp>/` only when the tool returns a concrete accessible local path or creates a file that can be identified exactly. Do not reconstruct files from UI blobs, app caches, screenshots, browser logs, or inferred names.

If no concrete path exists, finish as preview-only and say no worktree copy or ledger record was created.

## Explicit API Path

When API use is authorized, supply the original pack, its exact private runtime receipt, the composed object and the concrete `photo-image-render-request/v2`:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_images_via_api.py \
  --pack /absolute/path/pack.json \
  --runtime-receipt /absolute/path/pack.json.runtime-receipt.json \
  --composed /absolute/path/composed.json \
  --render-request /absolute/path/render-request.json \
  --concept "<concept>" --dry-run
```

`--dry-run` saves a preflight report and performs no key lookup, provider invocation or attempt ledger write. Omit it only for the authorized actual attempt. Use `--runtime-store` when the receipt's generation is stored outside the default runtime store. The adapter requires a positive `--attempts`; its current defaults remain two attempts, `gpt-image-2` and `1024x1536`. Existing authorization and the run's actual attempt policy govern those choices.

The adapter resolves the pinned receipt and freshly runs both composed and runtime audits. Self-declared PASS is not proof. Quality warnings remain visible in the report without becoming hard failures. It saves `photo-api-render-preflight/v1` with exact input bytes, generation, audit results and immutable execution parameters before reading the key or invoking the API. Preparation failures are reported separately with call count zero and never become attempt rows. There is no `--prompt-json`, folder scan or skip-audit execution path. Multiple-object input lists fail rather than silently selecting the first object.

This adapter is text-only. Nonempty references, active reference-edit modes, attached-image parameters and unsupported runtime additions fail before invocation. Use an already authorized reference-capable tool for those requests; never clear the references or copy their paths into prose to force this adapter to run. For this API lane only, the runtime string must equal the composed prompt plus its optional exact `\n\nAvoid: <negative_en>` suffix. The shared native runtime auditor retains its continuous-containment contract. The adapter sends the audited runtime string without whitespace normalization, recombination or rewriting.

Every actual attempt binds the same sidecar file/hash, runtime text hash, pack, selected IDs, composer, core/intent/repair hashes and requested model/size. `observed_image_model` is null unless a model is actually supplied by the response; the requested model is not a substitute. Observed request IDs are separate metadata. The recorder independently verifies sidecar inputs and audits before appending. Successful API rows also retain saved image hashes. Historical rows are preserved without fabricated new provenance.

Failed API attempts also save a `photo-image-attempt-evidence/v1` file beside the output. It retains the complete HTTP response bytes as base64, the observed request ID header, and separately parsed error fields. `failure_reason` is only a short display message. Invalid UTF-8 affects that display, not the retained bytes; a failed body read is explicitly `unavailable`. Only explicit `moderation_blocked` or `content_policy_violation` codes classify a safety block. A generic `safety` word, HTTP 400, or a malformed response stays `error`. Evidence or recorder failures stop the run before another API call.

Returned bytes are first saved in a unique recovery file before the image writer runs. If the API returns image bytes but their local save fails, record the failure with `invocation_outcome: returned` and stop. A local persistence failure does not trigger another image generation. Explicit moderation blocks stop unchanged retries. Only observed transient HTTP errors (429 or 500/502/503/504) may retry within the authorized bound; an unobserved provider result is marked unknown in error evidence and stops automatic retries.

## Native Error Capture

Use the actual shared `scripts/capture_image_tool_error.js` function for native failures. It is a pure function expression with no imports or image calls, so the native V8 code-mode can evaluate the same file that offline Node tests exercise. Set `photo_runtime_workdir` to the current arm's absolute checkout directory and load its helper before invoking the image tool; do not rewrite a catch that only reads `error.name` and `error.message`.

```javascript
const source = await tools.exec_command({
  cmd: "cat skills/photo-prompt-image-generator/scripts/capture_image_tool_error.js",
  workdir: load("photo_runtime_workdir"), login: false, max_output_tokens: 10000
});
if (source.exit_code !== 0) throw new Error("Native capture helper unavailable");
store("photo_error_capture_source", source.output);
```

With the exact audited inputs already loaded, the invocation cell can use this template. `photo_native_args`, `photo_composed`, `photo_attempt`, and the unique absolute `photo_error_evidence_path` are caller-prepared values from the current arm. The catch surrounds only the tool invocation; saving or displaying a successful result happens afterward.

```javascript
const capture = eval(load("photo_error_capture_source"));
const args = load("photo_native_args");
const composed = load("photo_composed");
const attempt = load("photo_attempt");
const started_at = new Date().toISOString();
let result;
try {
  result = await tools.image_gen__imagegen(args);
} catch (thrown) {
  const evidence = capture(thrown, {
    tool: "image_gen.imagegen", generation_environment: "codex_native", attempt,
    started_at, ended_at: new Date().toISOString(),
    prompt_en: composed.prompt_en, negative_en: composed.negative_en ?? null,
    runtime_prompt_en: args.prompt
  });
  // Retain the serializable value even if the following file write fails.
  store("photo_attempt_error_evidence", evidence);
  const quote = value => "'" + value.replaceAll("'", "'\\''") + "'";
  const saved = await tools.exec_command({
    cmd: "python3 skills/photo-prompt-image-generator/scripts/image_attempt_evidence.py --write-json " +
      quote(load("photo_error_evidence_path")) + " <<'PHOTO_NATIVE_ERROR_JSON'\n" +
      JSON.stringify(evidence) + "\nPHOTO_NATIVE_ERROR_JSON",
    workdir: load("photo_runtime_workdir"), login: false, max_output_tokens: 1000
  });
  if (saved.exit_code !== 0) throw new Error("Error evidence save failed; do not retry the image call");
  store("photo_attempt_error_file", JSON.parse(saved.output));
  text({attempt, status: evidence.outcome.status,
    request_id: evidence.outcome.request_id, fidelity: evidence.raw_error.fidelity});
}
// Handle the concrete successful result using the saving/review rules above.
```

Keep normal image-tool timeout/yield handling around this cell. For an error returned as a value rather than thrown, capture the actual error object with `invocation_outcome: "returned"`. Do not interpret a missing image path alone as a moderation error. Strings are retained exactly. Other values use a tagged, JSON-serializable snapshot of own properties; Error message/stack/cause, null, undefined, BigInt, symbols, nonfinite numbers and cyclic references are represented. Getters are never evaluated. Accessors, enumeration failures and depth/property limits are declared in `raw_error.limitations` and `fidelity`; `typed_capture` is a representation, not an exact reconstruction of object prototypes or internal slots.

The evidence writer uses lossless JSON escapes, including lone UTF-16 surrogates. Such a surrogate is replaced only in the display message and that display limitation is declared; the raw string stays exact.

After saving, pass the actual file to `record_image_run.py` with `--attempt-evidence-json <file>` and the writer's `--attempt-evidence-sha256 <digest>`. Use the evidence's `outcome.status` and display message, the same tool name, attempt, exact prompt and negative. The recorder verifies the file hash when supplied and always binds its computed SHA-256, checks those fields and the complete runtime prompt, then copies environment, capture fidelity and structured error details to the ledger and independent manifest. Missing/mismatched evidence fails before any ledger append. Evidence files must be unique per actual attempt; the shared writer refuses replacement. Neither the helper nor a logger failure authorizes another image call.

## Retries and Ledger

For unchanged retries, preserve `prompt_en`, `negative_en`, authorial-core hash, intent-lock hash, semantic-anchor IDs/evidence, and request-envelope binding byte-for-byte, and keep the same prompt ID. Increment `attempt`; link retries with `retry_of` when available.

For a failed visual obligation, identify the smallest failed `vo_*` gate set, preserve all passed identity, mechanism, and intent-anchor evidence, and revise only the necessary open-dimension composition/runtime phrase or declared local edit target. Use the SKILL.md retry whitelist when reading parent artifacts; do not reopen unselected candidate material as inspiration. A retry may improve rendering of a locked meaning but cannot reinterpret, replace, soften, or strengthen it. If repair requires a semantic change, stop that run and rebuild the envelope, core, and pack from an explicit requester correction; ask only if the needed correction is missing. With no allowed change, an authorized unchanged retry keeps the prompt bytes. Do not average components from separate attempts or declare a composite pass from different images. Preserve every attempt and follow the authorized attempt policy; user preference remains pending until received directly.

For a failed `rr_*` gate, preserve the actor, object, interaction state, required contact, all passed gates, and all locked semantic evidence. Make at most one additional attempt and change only the smallest declared local repair axes needed for the failed gate set. Removing, relocating, concealing, transferring, or replacing the object to avoid the interaction is a semantic failure, not a repair. Do not retry solely for a minor decorative difference.

Record saved native attempts with `scripts/record_image_run.py` in `runs/image_runs.ndjson`. Include `pack_id`, chosen candidate IDs, `composer: agent`, and audit status when available. When the pack exposed visual concepts, preserve the exact composed list with `--chosen-visual-concept-ids-json`; when it is non-empty, also preserve `--effective-visual-contract-sha256`. When the composed prompt contains `augmentation_brief`, preserve that audited object with `--augmentation-brief-json`; do not reconstruct or summarize its decisions. Do not write a ledger record for a preview-only native result.

For an independent multi-arm qualification, keep one ledger and one `run_manifest.json` inside each arm. V6 arms use `photo-independent-run-manifest/v2` with the canonical authorial-core and intent-lock SHA-256 values. Call the recorder with `--arm-id`, `--worktree-id`, the frozen skill SHA-256, source snapshot identity, candidate-pack version, every reference SHA-256, the actual image-call count, `--independent-no-cross-arm-inputs`, and `--manifest <path>`. When repair is active, also preserve `--render-repair-contract-sha256` and every failed `--failed-repair-gate-id`. The manifest records exact pack/prompt/run IDs, image paths and hashes, tool, source, and the fact that no other arm output was used. Never claim independence from visual diversity alone, and never pass another arm's prompt, pack, message, or image into the current arm.

Managed native arms can pass `--arm-id`, `--worktree-id`, `--skill-sha256`, `--source-ref`, `--independent-no-cross-arm-inputs` and `--manifest` directly to `photo_workflow.py native-result`. It forwards these declarations to the ordinary recorder while deriving the V6 pack/core/intent, references, selected IDs and native-plan bindings from the audited run. Pass the actual cumulative arm call count with `--image-call-count` when it exceeds the default of one, and repeat `--failed-repair-gate-id` when applicable. This path records an already observed result; it adds no image invocation or independent proof of the declaration.

For a text-only attempt, omit `--reference-sha256`; the independent manifest records `reference_sha256: []`. A blocked attempt still records its actual call and outcome with no delivered image paths. Neither case needs a fabricated reference hash or a second image call to complete the manifest.

Count actual tool invocations, keeping preparation/audit failures and unknown interruption outcomes separate. `image_call_count` is cumulative within an arm; do not sum successive cumulative values. Preserve failed outcomes and immediate `retry_of` links. A user-supplied successful image from ChatGPT or another surface has separate `origin: user_supplied` provenance, user-reported prompt/reference bindings and observed file hashes. It is not a new native retry or a revision of earlier failed outcomes. Record an unobserved external model, timestamp or attempt count as unknown; the prompt-authoring model is not an image-model identifier.

`assets/run_ledger.schema.json` is the public record contract. Keep its required keys, optional provenance fields, and enums synchronized with `record_image_run.py`; focused tests compare recorder output against that schema.

Report the image tool used and whether a repo-local copy was created.

## Managed execution

After core freeze, [photo-workflow.md](photo-workflow.md) describes the managed `--run` path. It reuses the same P0 API adapter and fresh audits. Record already-existing authorization with `authorize`; the record is not independent permission. `render-api --dry-run` needs no authorization or key. Native execution uses an audited plan, a durable start marker, the tool-environment bridge, and the actual observed result. No concrete native file means `preview_only`, without a paid fallback or a fabricated ledger image. An uncertain invocation stops automatic reexecution.
