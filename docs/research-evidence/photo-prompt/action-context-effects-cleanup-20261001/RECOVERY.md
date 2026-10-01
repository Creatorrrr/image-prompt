# Recovery

Base commit: `558e5cbfe0e1139f620c1322b943c5624dbb486f`
Working branch: `data-action-context-effects-20261001`
Final dictionary/index hash: `ba7c89b746cca5cfabce69c3204fd830d8f7aacc60d0e473f7b0174cb4e199db`

The patch is incremental to the already-published 37-row cleanup and editing-effects integration in this base. It adds this round's 16-row cleanup, tests, evidence and refreshed semantic index. Do not apply it on top of a different base or overwrite unrelated local changes without review.

The delivery manifest lists the ordered gzip-patch parts, each below 10 MB, the complete compressed and uncompressed patch checksums, and every recovered file hash. Concatenate only the listed parts in order, verify the complete gzip SHA-256, then decompress. In a clean checkout at the base, run `git apply --check` on the patch and then `git apply`. No additional embedding/API call is needed.

The patch includes the final manifest and all 16 referenced shards. Keep them together. Earlier shard generations remain preserved in the base checkout, and are needed by the historical reproduction check. The pre-existing untracked `c464aca9b1547ca9` generation is not part of this patch and was not removed.

Verification after recovery:

1. `python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index`
2. `python -m unittest tests.test_photo_action_context_effects_cleanup -v`
3. `python docs/research-evidence/photo-prompt/action-context-effects-cleanup-20261001/verify_saved_results.py`

The third command recomputes all saved baseline/stage/final diagnostics using existing vectors. It reads neither credentials nor the network. It creates a short-lived manifest alongside the assets so the historical shard paths resolve, then removes that temporary file.

The aggregate dictionary validator retains exactly the same 22 known baseline metadata errors. See the paired logs and report; an aggregate pass is not claimed.

The producer verifies the patch against exact base-file bytes in a separate recovery directory, compares every recovered file hash, and runs the production semantic loader on the recovered data. See the delivery manifest for that result. No `.env`, credentials, clipboard/editor state or unrelated workspace files are included. No push, PR, merge or deployment was performed.
