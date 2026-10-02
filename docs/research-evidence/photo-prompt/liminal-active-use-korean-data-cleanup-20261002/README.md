# Liminal active-use Korean data correction, 2026-10-02

This cycle prepares one sourced Korean clause correction for
`slot:action:waiting_in_between_use_space`: `사용 흔적 없이` becomes
`예상된 이용 활동 없이`. English already suspends expected active use. The
original liminal source retains temporal residue; the Korean prohibition on use
traces contradicts that contract. All English, aliases, keywords, embedding text,
units, weights, guards and required context remain exact. The source inventory
contains 22 reviewed rows: this correction and 21 unchanged keeps.

Preparation makes no live source/index changes, paid requests, commits or pushes.
An independent owner reviews and applies the frozen proposal and any necessary
current-regression migration, executes the bounded evaluator, judges collateral,
and publishes only after all required gates pass. No acceptance decision exists
at preparation time.

## Frozen evidence and scope

The scout proposal and 12 independently authored queries retain SHA-256
`cc355a36cc40b957de3a76cb9c976ca835ca18d3bef5bc13f8f5df5ac5f5e03f`.
Two existing action controls reuse the original frozen query and exact vector:
ordinary cafe pickup waiting in English and bus boarding readiness in Korean.
They were selected from query text and source target identity before inspecting
rankings or scores. Complete original query/cache snapshots and exact provenance
are included under `provenance/prior-frozen-controls`.

The published baseline is `0e5cc0d1968d5cfe83d1b63e9cfa198724ea9463`, dictionary
`37737278ea902ccdb29f1c1f9de5a535aa6ae6549ce66cad2710d4d1933b7770`.
Both states retain 10,174 semantic documents. The proposal changes exactly one
semantic document and reuses every other 10,173 vector. The paired experiment
ranks all 963 action rows for 14 queries, 2 methods and 2 states: 56 result rows.
It preserves full rankings, all top-12 results, primary/control and secondary
corrected-candidate rank/score/absence, no-hit cases and exhaustive collateral.
Physical index coverage, text/vector identity, ordering, all shards and complete
regenerated BM25F are validated separately. Missing baseline shard bytes are read
only from the exact published baseline Git objects; no private branches or fetch.

There are 15 logical inputs: 14 query texts and one proposed document. Two query
vectors are reused, leaving 13 nominal inputs ($0.0212992 maximum). The attempt
cap is 14 ($0.0229376), with no automatic or implemented manual retries. The spare
allowance authorizes no retry; a failed/uncertain attempt stops further calls and
requires separate review before any future recovery. Prior tracked cost is
$1.2713984, giving $1.294336 maximum cumulative project cost under the $10 cap.
The fixed deadline is 2026-10-02T11:46:56Z; sibling `daylong-progress/STOP`, the
live ledger and both execution locks are checked. Attempt records are fsynced
before each request; each returned exact vector is atomically cached and fsynced.
Unknown, reused, repeated, failed or uncertain inputs fail closed. Only an
explicit execute reads the existing ignored project `.env`, transiently, without
persisting its credentials or populating the environment. HTTP redirects and
application retries are disabled. No provider fallback exists.

## Maintenance binding, planned before measurement

The old imaginal maintenance record is valid historical provenance: its authored
source SHA binds the original pre-metadata file bytes. It is not a broken current
binding and remains byte-for-byte unchanged. `maintenance-binding-plan.json`
includes that historical snapshot and recipe.

The proposed immutable record is
`extension-maintenance/photo_prompt_imaginal_extension_liminal_use_20261002.json`.
Only its record ID and authored source hash change; the maintenance payload and
all other record fields stay exact. The new authored-source recipe is SHA-256 of
canonical UTF-8 JSON (ensure_ascii=False, sort_keys=True, compact separators) of
the revised source excluding only `maintenance_ref`. The reference digest uses
the same canonical recipe over the complete new record. This new recipe explicitly
binds the current source and does not rewrite historical provenance.

`raw_proposal` replaces only the complete selected Korean string plus the two
predeclared `maintenance_ref` values. Reversing those three substitutions must
recover every original source byte. The new record exists only as an evidence
snapshot until the owner uses the dry-run/default application helper and then
explicitly applies it.

## Actual consumers and honest limits

The real Korean `--list-tags action` CLI changes exactly 1 of 963 display lines;
all other lines are exact. This establishes a source/catalog correction, not
Korean generated-prompt, natural retrieval, adoption or image improvement.

The full production V6 gate uses the genuine source `elderly_commuter`, source
`between_use_transit_interior` and unchanged `waiting_train` companion. Both
actions independently pass ordinary unforced compatibility using subject and
location only. The original generated core, locked concept/subject/event,
negative guard, soft policy and fixture provenance are preserved. The final
target and companion are actually exposed, with full pack, candidate, overview
and hash-verified detail identical at pack `9a9674d57112ec23` in the scout.
This is controlled optional exposure, not natural retrieval or adoption.

Every earlier attempt is retained under `scout`. The singleton control omitted
the target because `singleton_scene_candidate_would_create_fixed_prompt_influence`;
its initial event-lock diagnosis is explicitly superseded. The separate
experiment that tried to open the event was rejected by the normal core validator
and produced no generated pack. Neither failure is acceptance evidence. The final
two-action gate uses the unchanged original valid contract and does not relax a
guard. `check_v6_preservation.py` imports no TestCase or fixture module, performs
no generation/retrieval/network/writes, and checks every actual full surface. It
reports exact difference paths on any mismatch; bindings may never be hidden or
presented as byte equality.

## Commands

Run from this directory, with `PYTHONDONTWRITEBYTECODE=1`:

- `python evaluate_cycle.py`: zero-call plan only; validates full baseline and caches
- `python test_frozen_cycle.py`: focused preparation/safety tests; synthetic transport only
- `python check_v6_preservation.py`: pure read-only actual full V6 replay
- `python check_korean_catalog_consumer.py`: actual CLI catalogs, baseline or proposal live state
- `python apply_proposal.py`: dry run; source and proposed maintenance record unchanged

Only the independently authorized owner runs:

- `python apply_proposal.py --apply`: exact clause/reference plus immutable version record
- `python evaluate_cycle.py --execute`: bounded frozen missing vectors and proposal index
- `python evaluate_cycle.py --replay`: read-only exact result/index reproduction; missing vector fails with no API fallback
- `python check_korean_catalog_consumer.py --require-live-proposal`: final live catalog check

Acceptance requires independent review of both methods and every changed rank,
score, absence/no-hit case and collateral entry. A real Korean source correction
or unchanged V6 English cannot offset unjustified retrieval harm. Source wording,
queries, controls and acceptance are frozen before measurement. Ordinary active
transit and empty domestic waiting remain legitimate scenes, with no new filter.
