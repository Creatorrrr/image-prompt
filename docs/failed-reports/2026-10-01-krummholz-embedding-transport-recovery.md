# Frozen krummholz embedding transport failure and bounded recovery

- Recorded: 2026-10-02 05:48 KST (2026-10-01 20:48 UTC)
- Status: resolved by the specifically reviewed one-time manual recovery; original transport cause and billing remain unknown
- Affected scope: cycle 13 Korean krummholz alias embedding evidence only
- Search terms: Gemini embedding URLError, frozen input, uncertain request, no automatic retry, exact-text cache
- Related evidence: `docs/research-evidence/photo-prompt/krummholz-korean-alias-data-cleanup-20261001/`

## Failure and evidence

The frozen 12-input evaluation expected one 768-dimensional document vector followed by 11 new query vectors. The first 618-byte document input, SHA-256 `7559ea2349bd286fdb5b6f52bfe2a499444df76ddb471c9278dc122e5eeacec2`, stopped with `URLError` at 2026-10-01T20:48:49.676999Z. The process terminated with exit 1. `api-attempts.json` retains the original failed-or-uncertain record; no new vector cache or ranking results were produced. No later input was sent, and the physical index stayed on the published cycle 12 baseline.

The error category alone cannot establish whether the provider received or billed the request. Credential-free connectivity checks immediately afterward reached the official Gemini endpoint (root HTTP 404) and GitHub (HTTP 200). Those checks establish current reachability only, not the cause or billing outcome of the earlier request. No credentials, request headers or response bodies were logged.

## Cause and attempts

The transport cause is unknown. One automatic application attempt occurred; no automatic retry occurred. The failed/uncertain attempt is conservatively charged at the same $0.0016384 upper bound as a completed attempt. The tracked project upper bound therefore became $1.2107776 before recovery. It is not an account invoice.

## Next safe step

Preserve the original frozen plan, scripts and attempt record. A separately reviewed recovery revision may permit exactly one explicit manual retry of this same document input, tied to the failed record, within the unchanged 15-attempt cycle cap. Preserve all 13 queries, source delta and acceptance criteria. Do not restart a live operation, discard an attempt, retry any further uncertain failure, or let replay call the API. Count all attempts from the original cycle budget baseline, without dropping or double-charging the failed attempt. If the bounded retry fails, pause paid evaluation and continue independent offline work.

## Reuse guidance

A transient transport error is not evidence of a successful request or a safe implicit rerun. Check terminal process status, durable attempt journals and partial caches before any manual recovery. Keep exactly matched vectors when available, and keep explicit recovery decisions separate from measured retrieval acceptance.

## Recovery result

The explicit manual document retry succeeded, followed by all 11 remaining new query inputs. Thirteen attempts were charged, including the unchanged failed/uncertain record; 12 unique new vectors completed. The complete 52-row paired matrix and 10,174-document physical index were produced successfully. Total cycle upper bound: $0.0212992; cumulative tracked upper bound: $1.2304384. The transport recovery does not itself accept the data change; independent retrieval tradeoff review remains required. See the hash-bound `manual-recovery-rationale.json`, `manual-recovery-validation.json`, `api-attempts.json`, and `api-workload.json` in the cycle evidence.
