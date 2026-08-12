# Photo API image path dropped audited ledger provenance

- Recorded: 2026-08-12 10:47 KST
- Status: resolved
- Goal/checkpoint: Photo Prompt Residual Runtime Boundary and Legacy Cleanup / Stage 1
- Affected scope: explicit OpenAI Images API helper, retry linkage, and `runs/image_runs.ndjson` provenance
- Search terms: generate_images_via_api, record_image_run, pack_id, chosen_candidate_ids, augmentation_brief, retry_of
- Related paths: `skills/photo-prompt-image-generator/scripts/generate_images_via_api.py`, `skills/photo-prompt-image-generator/scripts/record_image_run.py`, `skills/photo-prompt-image-generator/references/image-runtime.md`, `skills/photo-prompt-image-generator/assets/run_ledger.schema.json`
- Related passed report: `docs/passed-reports/2026-08-12-photo-runtime-boundary-and-api-ledger.md`

## Failure

- Conditions or trigger: Execute `generate_for_file` with a sanitized audited composed JSON containing pack ID, chosen candidate IDs, composer, audit status, augmentation brief, and two unchanged attempts while replacing the network call and recorder with local fakes.
- Expected: Every ledger call preserves exact prompt and negative bytes plus the audited composition provenance; attempt two links to attempt one's run ID through `retry_of`.
- Observed: Both recorder invocations omit `--pack-id`, `--chosen-candidate-ids-json`, `--composer`, `--audit-status`, `--augmentation-brief-json`, and `--retry-of`. The helper discards recorder stdout, so it cannot obtain the prior run ID for a retry.
- Impact on the goal: The documented explicit API path produces images but cannot prove which audited candidate pack or augmentation decisions created them, and unchanged retries are not linked as promised.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: Network-free import probe with a temporary prompt file, synthetic image bytes, and an in-memory recorder argument capture. No credential, endpoint call, user prompt, or real image was used.
- Result: Two recorder calls were captured; all six expected provenance/retry flags were absent from both. Existing `record_image_run.py` already accepts every missing field, isolating the gap to the API helper.

## Cause assessment

- Confirmed cause or current hypothesis: `generate_images_via_api.py` reads only prompt/negative and nested generation provenance, constructs a reduced recorder argv, and treats the recorder as a fire-and-forget subprocess with no returned run ID.
- Confidence: confirmed
- Remaining unknowns: Whether any external wrapper parses the helper's current human-readable stdout; the CLI arguments and final exit code will be preserved.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Existing direct recorder tests | Recorder correctly stores provenance and retry links | They bypass the API helper and therefore cannot detect its reduced argv |
| Network-free API helper probe | Reproduced all missing fields without external mutation | Detection only; no repair had been applied |

## Resolution or next safe step

- Resolution/workaround: The helper now computes a valid prompt ID when absent, forwards pack ID, chosen candidate IDs, composer, audit status, augmentation brief, and source argv, parses the recorder's returned run ID, and supplies it as `retry_of` on the next unchanged attempt. It also preserves `negative_en: null` versus an empty string, supports output paths outside the repository, and fails the run if ledger recording fails.
- Verification: A network-free helper test makes attempt one fail and attempt two return synthetic bytes. Both API calls receive the exact same prompt plus negative text; both recorder calls preserve the audited fields; attempt two links to attempt one's run ID; the successful absolute output path exists with exact bytes. Recorder output keys and enums are also checked against `assets/run_ledger.schema.json`. The affected photo suite passed 319 tests plus 597 subtests.
- Next safe step if unresolved: None for the in-repository helper. An external wrapper that parses the human-readable progress lines was not available for compatibility testing; the CLI options and final exit-code contract remain unchanged.

## Reuse guidance

- Avoid: Testing the recorder and assuming every caller forwards the same contract, or making ledger failure non-fatal after a real image was saved.
- Prefer: End-to-end caller-to-recorder argument tests with fake network bytes and exact prompt/negative assertions.
- Applicable when: Adding an image-generation helper or retry loop that claims audited provenance.
- Re-check when: The composed prompt schema, recorder CLI, retry behavior, or API helper output changes.
