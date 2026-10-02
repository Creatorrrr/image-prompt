# One-time manual recovery of the original document request

The original experimental freeze, source proposal, 14 queries, cache provenance,
acceptance, evaluator and tests remain byte-exact. Exact originals and the raw
failed-attempt journal are preserved in `original/`. The initial failed or
uncertain attempt remains immutable and charged. The matching failed report was
written before this recovery was prepared.

The coordinator supplied existing project authorization for candidate-text and
test-query transmission to Google Gemini within the original $10 budget. This
artifact summarizes that scope; it contains no private conversation transcript.
Independent review is required before the owner invokes the recovery helper.

The separate `evaluate_manual_recovery.py` permits exactly one explicit retry:
original failed document attempt 1, SHA-256
`de27c0cfb460b3443c00c93917976460262568d6ef391284c83d40cdcbaf7d8a`, becomes attempt 2.
It must use the exact original 641-byte text, Gemini embedding model, 768
output dimensions and official endpoint. A retry marker binds attempt 2 to the
canonical digest of unchanged attempt 1. The ordinary execution path refuses
the failure. No successful or reused input may be retried. A failed/uncertain
attempt 2 blocks every subsequent paid request; no further recovery exists.

Thirteen unique inputs remain, including the document. With the charged original
failure, full completion uses exactly 14 attempts and reaches the unchanged
$0.0229376 cycle cap ($1.294336 cumulative project upper bound). The live-ledger
check credits only cycle 16 attempts whose exact cycle identity, count and charge
are verified, preventing double-counting the original failure while preserving
any independent growth in total project spend. Unknown ledger credit fails closed.

The helper rechecks all original frozen artifacts and runtime hashes, the
separate recovery plan and implementation hashes, current source and complete
dictionary, old/new maintenance records, HEAD, STOP, deadline, live ledger and
attempt/cache consistency before every request. Both original execution locks
remain. Credentials are read transiently from the existing ignored `.env` only.
There are no alternate endpoints, redirects, automatic retries or API fallback.

Owner commands from the cycle evidence directory:

- `PYTHONDONTWRITEBYTECODE=1 python test_manual_recovery.py`: synthetic safety tests
- `PYTHONDONTWRITEBYTECODE=1 python evaluate_manual_recovery.py`: zero-call plan, preserving original plan outputs
- `PYTHONDONTWRITEBYTECODE=1 python evaluate_manual_recovery.py --execute --manual-retry-first-document`: consume the one explicit document retry, then only the remaining frozen queries if it succeeds
- `PYTHONDONTWRITEBYTECODE=1 python evaluate_manual_recovery.py --replay`: after completion, exact offline 56-row/index replay; missing vectors fail

Do not invoke the manual flag again after it is consumed. If only subsequent
unattempted inputs remain after a successful recorded recovery, ordinary
`--execute` may continue those inputs under the same cap. If any subsequent
attempt failed or became uncertain, stop. Transport completion does not accept
the data change; the original independent retrieval review still applies.
