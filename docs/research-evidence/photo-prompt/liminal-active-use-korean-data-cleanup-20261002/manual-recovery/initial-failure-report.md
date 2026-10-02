# Frozen liminal embedding approval-review failure and bounded recovery

- Recorded: 2026-10-02 01:49 UTC
- Status: open; no recovery request sent
- Affected scope: cycle 16 liminal Korean active-use correction embedding evidence only
- Search terms: Gemini embedding URLError, automatic approval review rejection, existing project transmission authorization, frozen input, uncertain request, one manual retry
- Related evidence: `docs/research-evidence/photo-prompt/liminal-active-use-korean-data-cleanup-20261002/`
- Related pattern: `2026-10-01-krummholz-embedding-transport-recovery.md`

## Expected and observed behavior

The frozen cycle expected one 641-byte document input followed by 12 new query
inputs, with two additional exact cached query controls reused. The first document
attempt began at 2026-10-02T01:41:43.750838+00:00 and was durably recorded as
`failed_or_uncertain_no_retry`, error class `URLError`, reason type `OSError`.
Its exact text SHA-256 is
`de27c0cfb460b3443c00c93917976460262568d6ef391284c83d40cdcbaf7d8a`.
No vector was cached and no ranking measurements or new physical index resulted.

The execution coordinator received an automatic approval review rejection that
claimed authorization to transmit project-derived text to Google Gemini was
missing. The existing process session subsequently returned `Unknown process
id`; it cannot be resumed. The durable transport error alone does not prove
provider receipt or billing. The failed or uncertain attempt remains charged at
$0.0016384, bringing the tracked project upper bound to $1.2730368.

## Cause, authorization and scope

The confirmed operational blocker is the reported automatic approval review
rejection. The underlying transport outcome and billing remain unknown. The
coordinator supplied existing user-authored authorization allowing the project's
candidate text and test-query use of Google Gemini within the existing $10 budget,
and directed one bounded same-payload official-endpoint retry after review. This
report records that project scope without reproducing private conversation text.
No broader recipient, payload, credential, endpoint or paid-service authority is
being inferred.

Only the original attempt has occurred. There has been no automatic retry,
alternate endpoint, authentication setup, source/query revision or fixture
weakening. All original source, probe, acceptance and cache-provenance evidence
remains frozen under
`603d19882bc0192fc6263800beac14dad69adc666143bf45bc9cf6f561b1b1c1`.

## Proposed bounded next step

Archive the exact original attempt bytes, freeze, evaluator and tests. Prepare a
separate hash-bound recovery helper, leaving those originals untouched. Only an
explicit manual flag may send the same failed document as attempt 2, with a
pointer to immutable attempt 1. The existing 14-attempt cap and $0.0229376 cycle
bound stay unchanged: one failed/uncertain attempt plus 13 successful unique
inputs fits that cap. The expected cumulative project upper bound is $1.294336.
No previously successful/reused input may be retried, no second recovery is
permitted, and any further failure blocks all subsequent paid calls. The normal
execution path continues to reject the failed attempt.

Every request must recheck source and complete dictionary identity, maintenance
records, original freeze and recovery-plan hashes, runtime bindings, HEAD,
STOP/deadline, live budget and durable attempt/cache consistency. Credentials
remain transient and come only from the existing ignored project `.env`. The
endpoint, model, payload and 768 dimensions remain exact. Replay is offline and
never falls back to an API. Independent review precedes owner invocation.

## Reuse guidance

An approval failure does not authorize changing routes or silently replaying a
request. Recover the original authorization context, establish that the prior
process is no longer running, preserve all failed/uncertain records and charge
them. A separately scoped recovery can consume only its exact one-time allowance.
Successful transport would still be separate from retrieval acceptance.
