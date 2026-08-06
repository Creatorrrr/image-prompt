# Gemini semantic index batch response cardinality mismatch

- Recorded: 2026-08-07 00:04 KST
- Status: resolved
- Goal/checkpoint: Photo Prompt Subculture Research Expansion / Stage 4
- Affected scope: semantic index regeneration only
- Search terms: Gemini embedding batch cardinality, build_semantic_index batch-size
- Related paths: `skills/photo-prompt-image-generator/scripts/build_semantic_index.py`, `skills/photo-prompt-image-generator/scripts/prompt_generator.py`

## Failure

- Conditions or trigger: Rebuild the semantic index with the approved sanitized taxonomy text and `--batch-size 16` while reusing compatible cached vectors.
- Expected: Gemini returns one 768-dimensional vector for each of the 16 input texts.
- Observed: Gemini returned one embedding for 16 input texts and the builder failed closed before writing the final manifest or shards.
- Impact on the goal: Stage 4 is delayed; source taxonomy, prior index, and frozen expectations are unchanged.

## Evidence

- Sanitized command, test, log, trace, artifact, or access-controlled reference: `.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 16 --request-interval 0.8 --progress`
- Result: exit 1 with `Gemini returned 1 embeddings for 16 input texts.` No credential or vector value was logged.

## Cause assessment

- Confirmed cause or current hypothesis: The active Gemini SDK/model call path accepts the list but returns a single embedding, so this repository's cardinality check correctly rejects multi-input batching.
- Confidence: confirmed
- Remaining unknowns: Whether a future SDK/model revision will support multi-input batching through this call shape.

## Attempts

| Attempt | Result | Why it did not work |
|---|---|---|
| Batch size 16 | Failed before final write | Response cardinality was 1 instead of 16 |
| Batch size 1 | Completed 5,697 entries | Verified single-input response cardinality; cached unchanged vectors were reused |

## Resolution or next safe step

- Resolution/workaround: Rebuilt with the builder's default verified single-input contract, `--batch-size 1`, while retaining cache/checkpoint behavior.
- Verification: The final write completed with 5,697 entries; `--check-index` passed; all 16 manifest hashes, shard entry counts, and logical entry order matched. Retrieval quality remains a separate Stage 4 gate.
- Next safe step if unresolved: Not applicable; keep batch size 1 until a focused integration test proves multi-input response parity.

## Reuse guidance

- Avoid: Increasing `--batch-size` for this SDK/model call without a cardinality probe.
- Prefer: `--batch-size 1` until a focused integration test proves multi-input response parity.
- Applicable when: Rebuilding `gemini-embedding-2` semantic indexes through `embed_content`.
- Re-check when: The Gemini SDK or embedding model integration changes.
