# Bounded reconciliation of three pre-search failures

This note applies only to the three identified 2026-11-07 magical-girl test
runs, their pinned generation and the specific observed local model package
safety error. It does not broaden the normal H-F2 recovery contract or permit
recovering a partial search with missing material.

The Codex command records for each `retrieve` show exit code 2 and an
untruncated `unsafe local model package` worker traceback. The frozen runtime
calls the query encoder before it opens the search index and calls `index.search`.
The separate arm 3 `resume` record ends with exit code 130 during validation.
The original command observations were independently checked against Codex
`read_thread(includeOutputs=true)`; their local JSON copies are pinned by hash.
These copies are unsigned local evidence, not a cryptographic attestation by
Codex. The conclusion is bounded by the observed executions and retained files;
it does not prove the absence of unrelated external activity.

The offline checker `scripts/photo_h_f2_early_failure_reconcile.py` accepts only
the three pinned run IDs, exact evidence files, native runtime code and original
transaction/preflight hashes. It checks all bound run artifacts, the query and
generation binding, process termination, progress/event consistency, absence of
material and score files, and absence of managed image operations. It holds the
run lock during the check and writes an immutable receipt **outside** the run.
It does not run a search or image provider and does not alter the original run,
journal, preflight or progress history. A changed, missing, unexpected, live or
incomplete item causes refusal. Other runs or failures require their own review.

Example, from the repository root, once the original observations are present:

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_h_f2_early_failure_reconcile.py \
  --root "$PWD" \
  --run "$PWD/generated/magical-girl-tests/arm1/run-v2" \
  --receipt "$PWD/generated/magical-girl-tests/arm1/reconciliation-receipt.json"
```

Use the analogous arm 2 and 3 paths for their own receipts. An existing receipt
is reused only if its bytes exactly equal the currently revalidated snapshot.
The receipt records evidence hashes and an operational closure finding; it is
not a search packet, an H-F2 receipt, native approval, or evidence of image
quality. The original run **remains blocked**: do not remove or edit its journal,
and do not treat `resume` as completed material.

Once that particular original transaction has been explicitly reconciled by this
checker and its receipt revalidated against the still-unchanged evidence, an
operator may manually create a separate, newly frozen run and perform its normal
single retrieval under the installed skill's current workflow. This is allowed
only after closure, not as a way to bypass the unresolved journal. It must use a
new run directory and preserve the original transaction and receipt; the checker
never starts it. A failed revalidation, changed inputs, another failure pattern,
or a resumed/restarted original run removes this basis and requires separate
reconciliation. Ordinary binding, retrieval, composition and image audit gates
continue to apply to the new run. The existing workflow does not consume this
receipt automatically, so this is an explicit operator procedure, not an
enforced cross-run authorization or a general guarantee about other processes.
