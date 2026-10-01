# Cycle 12: fresh explicit reef process unit

Status: a frozen DATA proposal, not source-applied, evaluated, accepted or published.

## Exact scope and separate history

Keep the original 17-row inventory at published baseline `98619e72b07d623e01de65b352cb8188d919901f` (dictionary `04deb75ce13c463ed3890535dd91c15ebc8dcd7397288e9768e2f088e40a41eb`, 10,174 documents). Change only `action:reef_flat_crest_forereef_wave_gradient`: use the exact old corrected English/Korean labels and append `concept_units` containing that unchanged 26-word English sentence. Preserve the other 16 inventory rows, five spatial reef descriptions, ebb/tide alternatives, all aliases/keywords/embedding text/weights/applicability/guards, historical maintenance provenance, parser/schema/caps/scope and logic.

The issue is a conflation of the flat–crest–fore-reef spatial profile with this selected incident-wave process. The proposed scene is supported; outward currents, wave-regime variation and fore-reef attenuation remain valid. No assertion says all conditions follow one direction or all dissipation happens only over the landward flat.

The prior `data-reef-wave-deferred-20261001` branch at `1f7e4915dadb840f84b2f9c427449d5f0a876f05` remains historically deferred. Never check out, merge, edit or revise that trial's disposition. Exact original inventories, results and deferral/correction notices are retained under `historical/`. This fresh representation requires its own explicit acceptance decision.

## Preparation packaging revision

Revision 2 supersedes preparation freeze `29242700dde5758e3a82c3fcf6acb8a66cb75a59f6628e37aa62867780f34c06` before source edits or measurement. The prior freeze/SHA are preserved under `preparation-revisions/`; the explicit reason is `revision-02-reason.json`. Exact original cache-source files are now included under `historical/cache-sources/`, and source inventories use the existing included snapshots. Each is checked against its original byte SHA, every reused original cache record/vector remains exact, and original Git provenance remains recorded. A missing local private deferred ref is permitted; if present, its tip must still match. Published replay does not require private Git objects. Pinned public baseline shards/Git objects remain supported. No source/proposal/query/vector value or acceptance criterion changed.

## Frozen evidence and workload

- Baseline merged data, raw extension and physical index manifest are snapshotted. All 16 baseline shard hashes/order/counts are pinned; the runner reads hash-matching existing shards or the exact pinned baseline Git objects, never a guessed current shard generation
- All 17 original inventory objects are preserved alongside three separate states: current baseline, exact old corrected-label comparator, fresh explicit unit
- Reuse all 14 original reef probes and all 16 prior action probes. Namespaced IDs avoid collisions; original objects, query text hashes, inventory source hashes and commits are preserved. They are inspectable reused diagnostics, not a blind benchmark
- Reuse 30 exact Gemini query vectors and the old comparator document vector. Provenance binds original cache bytes, model, 768 dimensions, exact input and vector hashes; query text is never re-embedded
- The fresh logical workload is 31 texts: one changed document plus 30 probes. Only the fresh 991-byte document (`ea93ec6f75d76cd12e942ba6b4326abd69337466149e254be242d03bbc6841f1`) lacks a cache. Reuse all other 10,173 current document vectors
- Nominal one-call upper bound $0.0016384. Hard cap two attempts / $0.0032768, no automatic retry. The runner refuses any previously attempted input, including uncertain, failed or completed records; the spare budget is not permission for an automatic repeat
- Each attempt is durably logged and fsynced before sending. The only endpoint is Gemini `embedContent`; redirects are rejected. Credentials are read only under `--execute`, from existing environment or ignored project `.env`, and are never printed or saved
- Mandatory STOP/deadline/current-ledger checks, a $10 total tracked budget, and an exclusive execution lock protect the call. Starting tracked upper bound is $1.2075008. Deadline is 2026-10-02 11:46:56 UTC

## Results and acceptance

The runner saves 180 rows: 30 probes × 3 states × dense/lexical. Every row includes the full primary target and secondary reef rank/score, membership, corpus size, and complete available top12. An additional 60-comparison report retains all score/rank/top12 transitions. It regenerates and validates complete full-corpus BM25F, all exact document inputs, 768-dimensional finite nonzero vectors, ordered membership, hashes and the freshly written physical index. Offline replay must reproduce all saved rows and exact physical entries/BM25F.

The copied source/public preflight (SHA `82a4d590615e4ebfe064484ca484d38244896d4aa9746b1e4c36c908320730e5`) proves three controlled actual-production pack/detail/mandatory-overview states. Baseline exports its 18-word label, old correction falls back to four existing keyword units, and the fresh proposal exports the complete corrected sentence as one optional unit. Authored core, original mandatory intents and control candidate remain intact. This is controlled serialization, not natural retrieval, eligibility, adoption, final composed-prompt or rendered-image proof. Typed relations remain empty, and no new hard obligation is introduced.

Acceptance must weigh this concrete full-process output benefit against every collateral exposure. Keeping a positive target at rank1, unchanged top5 membership or passing tests does not suffice. The frozen acceptance rules require an independent explicit tradeoff rationale or fresh deferral/rejection.

Known adverse evidence remains visible: old Korean aquarium dense reef rank4→2; old Korean intertidal secondary dense rank3→2; historical café lexical reef204→17; and current English dune secondary lexical rank4→2 with scores21.607297210918 baseline,37.534987671841 old comparator,38.922125023552 fresh explicit unit. Direction probes q11/q12 still return reef at1 and establish no relational discrimination. Ebb probes q13/q14 are coexistence controls with no low-rank requirement. Fresh dense results are not yet available. Any newly measured score or top12 harm must also be reviewed; no post-freeze wording/probe tuning is permitted.

## Commands after separate review

Run from the repository root using `/bin/bash` with login disabled. Let `E=docs/research-evidence/photo-prompt/reef-wave-explicit-unit-data-cleanup-20261001`.

1. Zero-cost preparation: `PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py"` (dry-run), `PYTHONDONTWRITEBYTECODE=1 python "$E/test_frozen_cycle.py"`, and `PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py"` (plan only)
2. Only after source review/authorization: `PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py" --apply`. This replaces exactly one raw JSON row with verified bytes and does not write the index. Run separately coordinated source/output regression tests
3. Only after paid-execution review/authorization: `PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --execute`. This sends at most one missing exact document request in this normal run, saves cache/attempt evidence, constructs three full-corpus states, writes the fresh proposal index with stale generations retained, and saves results
4. Independent review and offline replay: `PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --replay`. Replay makes no API or file writes and never falls back to network. Accept/reject in a separate new-cycle record after the full result review. This runner does not commit, pull, push, publish or touch the old deferred branch

If interrupted before the request returns, stop and review the durable attempt log before any recovery. A saved cached vector with an incomplete attempt record remains uncertain and is not silently retried. STOP/deadline after embedding preserves paid evidence but prevents an index write.
