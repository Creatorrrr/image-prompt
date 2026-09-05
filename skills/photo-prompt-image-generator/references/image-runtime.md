# Image Runtime

## Default Tool

When the user asks to create or render an image, use the session's native image generation tool with the audited `prompt_en`. Append the preserved negative prompt as `Avoid: ...` when supported.

Follow the current user instructions and existing session authorization before these procedural defaults. An already authorized generation, API fallback, or API cost does not require repeated confirmation. Use the requested attempt count and runtime when they are specified.

Before the tool call, serialize the exact native runtime inputs as `photo-image-render-request/v2` and run `scripts/audit_image_render_request.py`. The request must include `pack_id`, exact `runtime_prompt_en`, exact `runtime_negative_en`, the composed and runtime audit boundary, and every attached reference path, SHA-256, and role. For a normal intent-locked v5/v6 pack, it must also include `source_intent_lock_sha256` copied exactly from `authorial_core.intent_lock.canonical_sha256`. When the pack contains `render_repair`, also copy its exact `canonical_sha256` into `render_repair_contract_sha256`; omission or mutation blocks generation. The audited composed prompt must occur contiguously inside the runtime prompt, while the runtime string remains `not_run` until this exact-input audit passes. When `chosen_visual_concept_ids` is non-empty, also include the auditor-derived `effective_visual_contract_sha256`; this binds the optional selection to the hard contract used after rendering. The inherited composed PASS includes `photo-negative-intent-guard/v1`: do not append a platform-safety summary, recipe suppression, coordinator instruction, or new `Avoid:` item after audit. The runtime auditor scans both the complete positive runtime string and `runtime_negative_en` for the union of core `runtime_forbidden_labels` and active-profile `runtime_expression.runtime_forbidden_labels`; a shorthand label may aid meaning resolution but may not leak through either runtime surface. A negative mismatch, negative-intent-guard failure, runtime-label leak, missing intent-lock or repair-contract binding, missing reference, hash mismatch, visual-contract mismatch, role ambiguity, or missing/failed inherited composed audit blocks generation. An inherited composed PASS is required.

For `reference_identity_control`, inspect the concrete local source image first and pass that exact file through the native tool's reference-image mechanism. Do not describe a reference path in text without actually attaching it. Use the audited prompt's identity-preservation sentence, and keep the source portrait unchanged as the comparison control.

After a saved result returns, derive its gates from the exact pack and audited composed selection. For an identity-controlled result, compare the requested visible reference features against the source and current user-preferred baseline when one exists; a visual comparison does not establish a person's identity. Apply only the active reference-preservation gates. For v6 character response, review the frozen actor-target-action-affect-consequence relations and declared visual obligations; never add a gaze, facial landmark, head direction, pose, or crop merely because of a named archetype. Historical moe packs retain only their recorded active gates, described in `moe-response-legacy.md`. If any hard gate fails, preserve the result and ledger row as failed evidence. User preference remains a separate terminal judgment.

Record those observations in a `moe-render-review/v1` JSON object, then run `scripts/audit_moe_render_review.py` with both `--pack` and the exact audited `--composed` object. The auditor derives the checklist from active typed v6 `character_response.render_gates`, active legacy moe gates, unconditional visual obligations, and only the selected visual-concept opt-in gates. A gate removed by v5 `intent_precedence` must not be recreated during pixel review; review the frozen requester anchor instead. Use only exact `pass` or `fail` statuses and include image-grounded evidence for every hard gate; `partial` is deliberately not promotable. Honor each visual gate's declared `review_scale` and require all components in the same saved image. With a typed character-response or effective strict visual contract, `hard_gates` must exactly equal the derived checklist; put crops, comparisons, and supplemental observations in separate fields or files. The review must name the exact result path and SHA-256. For pending user review, set `user_judgment.source` to `not_yet_received`. Only a direct requesting-user decision may use `source: requesting_user`, and it needs a concise quote or faithful summary. A nonzero exit preserves the render as failed or pending evidence rather than deleting it.

When `render_repair` exists, separately record `photo-image-render-review/v1` and run `scripts/audit_image_render_review.py`. Review the exact generated file at every declared thumbnail/native scale and supply one `pass` or `fail` row for the exact contract gate set: object-class legibility, gross structural coherence, intended interaction match, and contact anatomy when contact is required or transitional. These are major gates for meaningful action-bearing props; minor ornament, decorative engraving, and background accessory variations are non-blocking. The auditor validates the image hash and review record but does not infer pixels or requester preference.

A missing native local path alone does not authorize a new paid API call. Use the OpenAI Images API when the user's request or existing session authorization covers that runtime and cost, including an authorized fallback. Do not require a second confirmation or a special wording of permission already given. If paid API use is outside the authorized scope, prepare the exact audited request first and ask once for the concrete API attempt.

## Saving

Copy a native result into `generated_images/<concept>-<timestamp>/` only when the tool returns a concrete accessible local path or creates a file that can be identified exactly. Do not reconstruct files from UI blobs, app caches, screenshots, browser logs, or inferred names.

If no concrete path exists, finish as preview-only and say no worktree copy or ledger record was created.

## Explicit API Path

When API use is authorized, use:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_images_via_api.py \
  --prompt-json <audited-prompt.json> --concept "<concept>"
```

The script forwards prompt and negative bytes unchanged, saves successful images, and records every `tool: openai_images_api` attempt. It forwards available `pack_id`, chosen candidate IDs, composer, audit status, augmentation brief, and source argv; retry rows link to the immediately preceding attempt. A recorder failure makes the run fail instead of silently leaving an untraceable success.

## Retries and Ledger

For unchanged retries, preserve `prompt_en`, `negative_en`, authorial-core hash, intent-lock hash, semantic-anchor IDs/evidence, and request-envelope binding byte-for-byte, and keep the same prompt ID. Increment `attempt`; link retries with `retry_of` when available.

For a failed visual obligation, identify the smallest failed `vo_*` gate set, preserve all passed identity, mechanism, and intent-anchor evidence, and revise only the necessary open-dimension composition/runtime phrase or declared local edit target. Use the SKILL.md retry whitelist when reading parent artifacts; do not reopen unselected candidate material as inspiration. A retry may improve rendering of a locked meaning but cannot reinterpret, replace, soften, or strengthen it. If repair requires a semantic change, stop that run and rebuild the envelope, core, and pack from an explicit requester correction; ask only if the needed correction is missing. With no allowed change, an authorized unchanged retry keeps the prompt bytes. Do not average components from separate attempts or declare a composite pass from different images. Preserve every attempt and follow the authorized attempt policy; user preference remains pending until received directly.

For a failed `rr_*` gate, preserve the actor, object, interaction state, required contact, all passed gates, and all locked semantic evidence. Make at most one additional attempt and change only the smallest declared local repair axes needed for the failed gate set. Removing, relocating, concealing, transferring, or replacing the object to avoid the interaction is a semantic failure, not a repair. Do not retry solely for a minor decorative difference.

Record saved native attempts with `scripts/record_image_run.py` in `runs/image_runs.ndjson`. Include `pack_id`, chosen candidate IDs, `composer: agent`, and audit status when available. When the pack exposed visual concepts, preserve the exact composed list with `--chosen-visual-concept-ids-json`; when it is non-empty, also preserve `--effective-visual-contract-sha256`. When the composed prompt contains `augmentation_brief`, preserve that audited object with `--augmentation-brief-json`; do not reconstruct or summarize its decisions. Do not write a ledger record for a preview-only native result.

For an independent multi-arm qualification, keep one ledger and one `run_manifest.json` inside each arm. Legacy v2-v4 arms use `photo-independent-run-manifest/v1` with the canonical authorial-request SHA-256. V5/v6 arms use `photo-independent-run-manifest/v2` with the canonical authorial-core and intent-lock SHA-256 values. In either case call the recorder with `--arm-id`, `--worktree-id`, the frozen skill SHA-256, source snapshot identity, candidate-pack version, every reference SHA-256, the actual image-call count, `--independent-no-cross-arm-inputs`, and `--manifest <path>`. When repair is active, also preserve `--render-repair-contract-sha256` and every failed `--failed-repair-gate-id`. The manifest records exact pack/prompt/run IDs, image paths and hashes, tool, source, and the fact that no other arm output was used. Never claim independence from visual diversity alone, and never pass another arm's prompt, pack, message, or image into the current arm.

For a text-only attempt, omit `--reference-sha256`; the independent manifest records `reference_sha256: []`. A blocked attempt still records its actual call and outcome with no delivered image paths. Neither case needs a fabricated reference hash or a second image call to complete the manifest.

`assets/run_ledger.schema.json` is the public record contract. Keep its required keys, optional provenance fields, and enums synchronized with `record_image_run.py`; focused tests compare recorder output against that schema.

Report the image tool used and whether a repo-local copy was created.
