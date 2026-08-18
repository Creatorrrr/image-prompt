# Two-arm process audit

Status: **partial**. The skill arm has a coherent request-to-image evidence chain with declared warnings. The baseline arm preserves an exactly identical final/runtime prompt pair and one valid PNG, but lacks enough metadata to verify how it was generated.

This is a process-only audit. No rendered pixels, blind/evaluation inputs, prior runs, memory, or repository source were inspected.

| Check | Skill arm | Baseline arm |
|---|---|---|
| Request-envelope binding | Coordinator and arm envelopes are byte-identical (`7fecdbca…`); request text hash `6d06dd87…`; both active spans match their offsets | Coordinator envelope has the same request text/spans (only `request_id` differs), but no arm-local execution binding exists |
| Pre-core freeze | Hash-bound initial core; initial core mtime precedes pack by 46 s; evidence is partial because the freeze marker mtime precedes the core artifact it hashes by 85 s | Not applicable / no metadata |
| Candidate pack | 1 pack, `photo-candidate-pack/v6`, pack `b07ab990718769d3`, requested/provenance creativity `0.5`; semantic mode fell back to rule mode; 6 candidates present, 0 selected | None |
| Composed/runtime audits | Composed: PASS, quality WARN, 0 failures, 6 uncovered-intent warnings. Later standalone runtime audit: PASS, 0 failures, negative match true, 1 reference | None |
| Prompt words | Final/composed: 178 words, SHA-256 `5d534870…`; effective runtime: 199 words and equals composed prompt + `Avoid:` + negative text | Final and runtime: 432 words each; byte-identical, shared SHA-256 `ce2e2fb8…` |
| Image calls / retries | Verified by metadata plus one-row ledger: 1 call, attempt 1, 0 retries, success | Unknown; one PNG cannot establish call or retry count |
| Generated image artifact | Exists; PNG RGB; 1086×1448; 1,896,891 bytes; SHA-256 `d215ca27…`; file, metadata, and manifest agree | Exists; PNG RGB; 1122×1402; 2,029,904 bytes; SHA-256 `91f9d967…`; no metadata cross-check |
| Missing process metadata | None for the requested call/retry/hash checks | Arm envelope/link, runtime request/audit, ledger, first-attempt/retry record, reference hash/role, hash manifest, independence declaration |

## Request and freeze evidence

- `coordinator/request.txt` includes a trailing LF, so its whole-file hash is `b15244da…`; hashing the request content without that LF yields the envelope's `6d06dd87…` exactly.
- Skill coordinator and arm request envelopes are byte-identical. The baseline envelope carries the same request text, active spans, and request hash, with only the arm-specific `request_id` differing.
- `prepack-freeze.json` correctly names the observed request-envelope hash, request-text hash, initial-core hash, initial intent-lock hash, and 153-word baseline prompt. The initial core's source request equals the envelope request.
- A generator schema error (`facial_appearance_reference` was not an accepted lock dimension) led to a recorded structural correction before the pack. The initial and corrected hashes match their files; the baseline prompt and checked semantic fields are unchanged.
- Filesystem ordering is request envelope 17:44:13, freeze marker 17:44:21, initial core 17:45:46, corrected core 17:46:02, correction record 17:46:16, candidate pack 17:46:32 (local time). This supports core-before-pack, but the marker's earlier timestamp means it is not independent proof that the hashed core file already existed at marker time.

## Procedural warnings and partial failures

- Requested semantic selection fell back to rule selection because the generation record says neither Gemini embedding API key was available.
- The composed audit passed, but its quality status is `warn`: six locked intents were not covered by a selected candidate and were instead preserved by free description/assertion. No visual concept candidate was selected.
- The render request's embedded snapshot says runtime audit `not_run`; the standalone audit written later reports PASS, and first-attempt metadata agrees. This is a chronological state transition, not treated as a contradiction.
- The post-render review audit reports `failed_technical_hard_gates`, non-representative status, and four schema failures because it expects legacy `moe_response` fields while the v6 pack contains `photo-character-response/v1`. This audit reports that artifact state only and makes no pixel-quality judgment.
- Baseline provenance is materially incomplete. Its prompt/runtime identity and output file are verifiable, but call count, retry count, reference integrity, exact execution binding, and arm independence are not.

## Limitations

- No pixels were opened or evaluated; recorded render-review claims were not independently checked.
- The referenced face image is outside the permitted directories, so its declared hash/path could only be checked for consistency across skill-arm metadata.
- Filesystem mtimes are mutable ordering evidence, not trusted timestamps or proof of independent authorship.
- Direct file hashes and cross-artifact IDs were checked. Canonical identifiers whose serialization algorithm is not fully specified were checked for internal consistency only.
