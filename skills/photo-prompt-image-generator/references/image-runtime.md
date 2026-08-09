# Image Runtime

## Default Tool

When the user asks to create or render an image, use the session's native image generation tool with the audited `prompt_en`. Append the preserved negative prompt as `Avoid: ...` when supported.

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

The script forwards prompt and negative bytes unchanged, saves successful images, and records `tool: openai_images_api` attempts.

## Retries and Ledger

For unchanged retries, preserve `prompt_en` and `negative_en` byte-for-byte and keep the same prompt ID. Increment `attempt`; link retries with `retry_of` when available.

Record saved native attempts with `scripts/record_image_run.py` in `runs/image_runs.ndjson`. Include `pack_id`, chosen candidate IDs, `composer: agent`, and audit status when available. When the composed prompt contains `augmentation_brief`, preserve that audited object with `--augmentation-brief-json`; do not reconstruct or summarize its decisions. Do not write a ledger record for a preview-only native result.

Report the image tool used and whether a repo-local copy was created.
