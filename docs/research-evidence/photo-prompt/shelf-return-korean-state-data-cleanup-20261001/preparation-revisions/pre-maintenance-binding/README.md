# Shelf-return Korean source-state DATA correction

## Frozen source finding

Replace only `ko` on `slot:aftermath_trace:pov_reduced_purchase_set_trace` in
`photo_prompt_poverty_extension.json`:

- Before: 되돌린 한 품목의 진열 공백과 결제된 더 작은 필수 식품 묶음이 함께 남는 결과
- Proposed: 되돌린 한 품목이 놓인 원래 진열 위치와 결제된 더 작은 필수 식품 묶음이 함께 남는 결과

The original authored Korean says the returned item leaves a display gap. Its
unchanged English unit, matched return action and source-to-result composition
instead put that same item back in its original display position, alongside the
smaller completed purchase. The correction names the occupied original position.
It does not require a fully stocked shelf; unrelated shelf vacancies may coexist.

The exact 12-row source inventory contains one correction and eleven exact keeps.
All other labels, aliases, keywords, positive embedding text, complete English
units, relationships, adult context, reduced completed purchase, resource/actor
continuity, bindings, eligibility, weights, scopes and guards remain unchanged.
No runtime or schema change is proposed. Source-chain snapshots and exact scout
artifacts are included. Official evidence supports abstract resource dimensions
and representation limits; authored project sources provide the staged physical
continuity. This is Korean source consistency repair, not a V6 semantic-loss fix.

## Acceptance frozen before measurement

1. Eliminate the exact sourced Korean owner/state contradiction without broadening
   meaning or changing any other field
2. Run honest paired lexical and dense diagnostics over the full existing
   aftermath_trace corpus for both states. Preserve all target absence/no-hit
   cases, primary and secondary corrected-candidate ranks/scores, complete top12,
   complete rankings, top12 transitions and every changed rank/score
3. Retain intended positive and unrelated-gap coexistence behavior. Disclose and
   independently judge any target disappearance, no-hit introduction, top12 exit,
   rank/score loss or changed ordering. No automatic pass or invented numerical
   success threshold is allowed
4. Reject unjustified near-miss or unrelated-control/collateral regression. The
   completed-purchase/wrong-source-position pair must be reviewed separately from
   unfinished removal and different-actor restocking. Different shopping scenes
   are legitimate requests, not new exclusion rules
5. Full English V6 preservation cannot compensate for harmful retrieval. There
   is no required named-alias lexical gain, because the defect is state consistency
6. Do not tune source text, probes, controls or acceptance criteria after measurement

## Queries and cache discipline

Twelve queries × two states × dense/BM25F = 48 rows:

- Exact eight independently authored scout probes: EN/KO positive, unrelated-gap
  coexistence, unfinished item removal and different-actor restocking
- Two independently authored reviewer probes: a smaller purchase is completed,
  but the omitted package remains beside the till and its source position is empty
- Two meaningful existing aftermath_trace controls: untouched cooled drink and
  luggage beside a waiting position

No bare-name probes are appropriate for a state correction. No prior frozen
same-slot query controls with compatible cached vectors were found; fresh controls
were authored before measurement instead of borrowing mismatched-slot probes.
All exact model/dimension/text-compatible vectors are reused. Cache availability
was checked without inspecting retrieval ranks or scores. No exact vector for
any of the 13 proposed inputs exists in the inspected prior cycle caches.

The corrected candidate is a desired recovery target for intended/coexistence
queries and an unwanted-exposure diagnostic for the six near misses. On unrelated
controls the existing control is primary and the corrected candidate is secondary.
All query objects and input bytes are immutable and hash-bound.

## Published baseline and portable replay

Published verified baseline: `e793d350eed966745dcb5c5d35ebbfd924cb6bff`.
Dictionary: `aac0b2ab210f09dd32eb1fcc319acc87f979020ac38349350e712f04dddf3bf9`.
There are 10,174 complete indexed documents. Raw and merged baseline snapshots,
the index manifest, full entry-order/entries digests and source provenance are
included. Every shard is verified against the published Git object. If an existing
shard is unavailable, replay can read that exact published object without network
access, unpublished branch dependencies or private evidence paths.

`check_v6_preservation.check()` is read-only. It replays production pack construction
from the exact saved source fixture, without importing TestCase or rerunning rule
generation. Both states must reproduce the full expected scout pack, candidate,
hash-verified detail and overview, pack `946d69ecd0b85dc6`. The genuine human/adult
source subject is present and compatibility is unforced for the changed row and
all twelve reviewed rows. Generated core, provenance, soft policy and negative
guards remain unchanged. This proves preservation only, not natural retrieval,
adoption, composed English improvement or image quality.

## Execution and budget

Preparation modifies only this evidence directory. It does not apply the proposal,
write an index/current test, call a paid API, commit or push.

The default evaluator is a zero-call plan. Separately authorized `--execute`
requires exact applied raw/merged source and baseline HEAD. It takes exclusive
shared/local locks, rechecks live STOP/deadline/project ledger, records and fsyncs
every attempt before send, and atomically persists its exact vector. No redirects
or automatic retries. Any failed, uncertain or inconsistently persisted attempt
blocks continuation. Diagnostics contain only safe exception class/reason type
and numeric errno; no credentials, response body or exception message.

Frozen model: gemini-embedding-2, 768 dimensions. Each input is capped at 8,192
UTF-8 bytes as a conservative token-bound check, and each attempt is bounded by
8,192 tokens × $0.20/million = $0.0016384. One new document plus twelve query inputs
means 13 pending inputs, nominal upper $0.0212992. Fourteen-attempt budget ceiling:
$0.0229376. Previous tracked project upper: $1.2500992; maximum cumulative:
$1.2730368, within the $10 project cap. Unrelated account use is excluded.
Deadline: 2026-10-02T11:46:56Z. STOP: `daylong-progress/STOP` beside the repository.
The live ledger may only tighten the budget/deadline.

One spare budget allowance authorizes no retry. This version prohibits duplicate
inputs and contains no manual-recovery mode. Any later recovery requires separate
review and authorization, preserving failed/uncertain attempts and the original cap.

## Commands from repository root

Preparation and checks:

```sh
E=docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/test_frozen_cycle.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/check_v6_preservation.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py"
```

Only after separate approval, regression migration and pre-call review:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py" --apply
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --execute
```

After measurement, `evaluate_cycle.py --replay` performs zero API calls and no
writes. It refuses absent vectors without API fallback and verifies the saved
48-row evidence plus complete physical index. Existing repository tests are
unchanged; the coordinator owns current regression and historical migration work.
