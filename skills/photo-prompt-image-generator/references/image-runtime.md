# Image Runtime

## Default Tool

When the user asks to create or render an image, use the session's native image generation tool with the audited `prompt_en`. Append the preserved negative prompt as `Avoid: ...` when supported.

Before the tool call, serialize the exact native runtime inputs as `photo-image-render-request/v2` and run `scripts/audit_image_render_request.py`. The request must include `pack_id`, exact `runtime_prompt_en`, exact `runtime_negative_en`, the composed and runtime audit boundary, and every attached reference path, SHA-256, and role. The audited composed prompt must occur contiguously inside the runtime prompt, while the runtime string remains `not_run` until this exact-input audit passes. A negative mismatch, missing reference, hash mismatch, role ambiguity, or inherited composed PASS blocks generation.

For `reference_identity_control`, inspect the concrete local source image first and pass that exact file through the native tool's reference-image mechanism. Do not describe a reference path in text without actually attaching it. Use the audited prompt's identity-preservation sentence, and keep the source portrait unchanged as the comparison control.

After a saved identity-controlled result returns, compare source portrait, current user-preferred baseline when one exists, and new result before promotion. Adult age, same-person identity, eye aperture/shape/spacing, face length, lower-face/jaw width, and absence of de-aging or dollification are hard gates. If any hard gate fails, preserve the result and ledger row as failed evidence, but do not label it representative, better, or moe-qualified. For tsundere, also require one blurred partial outer-eye-plus-temple/profile landmark from the same adult recipient at a named upper edge. Reject promotion when the primary character faces the lens, when head and irises turn together instead of the head turning opposite the landmark and only the irises returning, when a second full recipient face competes, or when softened lower lids and a suppressed starting mouth-corner lift are not both visible. User preference remains a separate terminal judgment after these technical gates.

Record those observations in a `moe-render-review/v1` JSON object keyed by the candidate pack's `moe_response.render_qualification.required_hard_gates`, then run `scripts/audit_moe_render_review.py`. Use only exact `pass` or `fail` statuses and include image-grounded evidence for every hard gate; `partial` is deliberately not promotable. The review must name the exact result path and SHA-256. For pending user review, set `user_judgment.source` to `not_yet_received`. Only a direct requesting-user decision may use `source: requesting_user`, and it needs a concise quote or faithful summary. A nonzero exit preserves the render as failed or pending evidence rather than deleting it.

Do not call the OpenAI Images API merely because the native tool did not expose a local file. Explicit API use requires the user to ask for the API or bundled API script, followed by confirmation that it may incur API cost.

## Saving

Copy a native result into `generated_images/<concept>-<timestamp>/` only when the tool returns a concrete accessible local path or creates a file that can be identified exactly. Do not reconstruct files from UI blobs, app caches, screenshots, browser logs, or inferred names.

If no concrete path exists, finish as preview-only and say no worktree copy or ledger record was created.

## Explicit API Path

After cost confirmation, use:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_images_via_api.py \
  --prompt-json <audited-prompt.json> --concept "<concept>"
```

The script forwards prompt and negative bytes unchanged, saves successful images, and records every `tool: openai_images_api` attempt. It forwards available `pack_id`, chosen candidate IDs, composer, audit status, augmentation brief, and source argv; retry rows link to the immediately preceding attempt. A recorder failure makes the run fail instead of silently leaving an untraceable success.

## Retries and Ledger

For unchanged retries, preserve `prompt_en` and `negative_en` byte-for-byte and keep the same prompt ID. Increment `attempt`; link retries with `retry_of` when available.

Record saved native attempts with `scripts/record_image_run.py` in `runs/image_runs.ndjson`. Include `pack_id`, chosen candidate IDs, `composer: agent`, and audit status when available. When the composed prompt contains `augmentation_brief`, preserve that audited object with `--augmentation-brief-json`; do not reconstruct or summarize its decisions. Do not write a ledger record for a preview-only native result.

For an independent multi-arm qualification, keep one ledger and one `run_manifest.json` inside each arm. Call the recorder with `--arm-id`, `--worktree-id`, the frozen skill SHA-256, source snapshot identity, `--candidate-pack-version v4`, canonical authorial-request SHA-256, every reference SHA-256, the actual image-call count, `--independent-no-cross-arm-inputs`, and `--manifest <path>`. The manifest is `photo-independent-run-manifest/v1`; it records the exact pack/prompt/run IDs, image paths and hashes, tool, source, and the fact that no other arm output was used. Never claim independence from visual diversity alone, and never pass another arm's prompt, pack, message, or image into the current arm.

`assets/run_ledger.schema.json` is the public record contract. Keep its required keys, optional provenance fields, and enums synchronized with `record_image_run.py`; focused tests compare recorder output against that schema.

Report the image tool used and whether a repo-local copy was created.
