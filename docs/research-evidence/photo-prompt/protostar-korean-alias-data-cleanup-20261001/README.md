# Qualified Korean protostar alias DATA experiment

## Frozen hypothesis and scope

Append exactly `원시성 원반 분출계` to
`slot:subject:embedded_protostar_observation_subject.aliases` in
`photo_prompt_space_extension.json`. Preserve `원시별 원반 분출계`, both
existing aliases and every other field, row, bundle, eligibility rule, weight,
runtime and guard. This is one named-concept search-coverage experiment.
No scientific contradiction or final-prompt defect was established.

The complete bounded scout review is frozen: 20 non-action rows spanning five
astronomical clusters across subject, location, prop and aesthetic_trend,
with one append-only proposal and 19 exact keeps. Previously reviewed actions
are excluded. The full source/scout/V6 artifacts are copied intact in `scout/`.
The original proposal/eight independent queries have SHA256
`e2c206fe634b62b6fb3b7a57453a5a7ab312f877faeb2b5d1469677cb3eec91d`.

## Source gate

- KASI's [원시성 terminology](https://astro.kasi.re.kr/kor/post/stellarObjects/71429)
  explicitly equates 원시성 with 원시별
- KASI's [research description, section 8](https://www.kasi.re.kr/kor/publication/post/notice/5575)
  connects protostars with molecular-cloud embedding, bipolar outflows,
  circumstellar envelopes and disks; the copied verification supplement records
  successful direct retrieval after the initial freeze's fetch limitation
- NASA's [Hubble disk observations](https://science.nasa.gov/missions/hubble/hubbles-album-of-planet-forming-disks/)
  support the existing narrow young-source/disk/bipolar-outflow morphology

The full qualified alias is an authored synonym substitution, not an official
quotation. It does not claim all protostars display this specialized morphology.
No bare-name alias is added to the subject or its related cluster.

## Frozen evaluation

Two states × 13 queries × dense/BM25F = 52 rows, all against the full existing
subject corpus. The eight scout probes remain byte-identical. Added controls:

- `protostar`, `원시별`, `원시성`: named discovery controls
- `A welder dressed in protective equipment.` → existing `welder_worker`
- `물이 배어 있는 논흙에서 작업하는 농부` → existing `rice_paddy_farmer`

The two unrelated controls are exact prior positive subject queries, chosen
for their clear meaning, same-slot targets and compatible cached vectors,
without consulting their rank outcomes. Their complete original query inventory
and vector-cache bytes are copied and hash-bound; reuse requires exact model,
768 dimensions and text. No mismatched-slot control is used.

Near-miss primary/secondary protostar exposure is an unwanted-match diagnostic,
not a claim the protostar is the correct answer to those queries. Every result
records primary and secondary protostar rank/score, hit count, no-hit flag, full
top12 and the complete ranking. The comparison includes every changed rank or
score, all top12 transitions and all no-hit cases. There is no automatic acceptance.

Meaningful Korean named lexical gain is required. Dense, positive, near-miss,
bare-name and unrelated collateral costs must be disclosed and independently
judged; unjustified harm rejects promotion. No tuning aliases or probes after
measurement. Bare-name discovery cannot establish universal morphology.

## Complete baseline and actual V6 preservation

Baseline is published commit `9034d6fd856aaa55ea550523424eac5f49b37eca`,
10,174 indexed documents, dictionary
`e6a5e34428733d9bbf4989c38c1bb072975236808407b348ca5d369d598240cb`.
Full raw and merged snapshots are copied. The exact index manifest, generation,
complete entries and entry order are hash-bound. All 16 shard byte hashes were
verified against that published Git commit. Replay may use those published Git
objects if existing shard files are missing; no network, unpublished branch or
private reference is needed. Plan validation checks every text/vector/BM25F record.

`check_v6_preservation.py` rebuilds actual full production V6 packs and verified
detail/overview from the frozen controlled rule fixture and both complete states.
It verifies real subject-bearing compatibility, two existing alternatives,
narrow protostar location compatibility without force, and unchanged generated
soft policy, core and negative guard. The candidate, full pack, detail and
overview are exactly equal. This supplies preservation only, not natural
retrieval, adoption, composed-prompt improvement or image-quality evidence.

## Execution safety and cost

Default evaluator mode is a zero-call plan. `--execute` alone can send frozen
missing inputs after exact raw/merged proposal validation and current STOP,
deadline, ledger, HEAD and once-only guards. Before every request it rechecks
proposal identity and the live ledger; it writes/fsyncs a durable attempt before
sending. Cache writes are atomic and fsynced. Exclusive shared/local locks prevent
concurrent execution. There are no automatic retries or redirects. Any failed,
uncertain or inconsistently persisted attempt blocks further requests.
Only safe exception class, reason type and numeric errno are recorded, never
credentials, response bodies or exception strings.

Expected paid workload: one proposal document plus 11 uncached queries = 12
inputs. Two exact cached query vectors are reused. Each attempt is conservatively
bounded by 8,192 tokens × $0.20/million = $0.0016384; UTF-8 bytes are also capped
at 8,192 as a conservative per-input check. Nominal upper: $0.0196608.
Maximum 13 attempts: $0.0212992, with prior project upper $1.2304384 and maximum
cumulative $1.2517376, inside the $10 project cap. Separate upstream spend is
excluded. Deadline: 2026-10-02T11:46:56Z; STOP: `daylong-progress/STOP` beside
this repository. The live ledger can only make guards more conservative.

The one spare-attempt budget allowance does not authorize or implement recovery.
This new cycle starts with no prior attempts and no manual recovery flag. Any
future one-time manual recovery needs separate approval and independent review,
preserving the failed/uncertain record, exact source/probes and original cap.

## Commands from repository root

Preparation only, no source/runtime/index writes or paid calls:

```sh
E=docs/research-evidence/photo-prompt/protostar-korean-alias-data-cleanup-20261001
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/test_frozen_cycle.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/check_v6_preservation.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py"
```

Separately authorized source apply and measured run (not run in preparation):

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py" --apply
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --execute
```

After successful measurement, read-only zero-API replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --replay
PYTHONDONTWRITEBYTECODE=1 python "$E/check_v6_preservation.py"
```

Current repository tests remain untouched. The coordinator must migrate any
whole-current-state historical assertions before source application while
preserving their historical evidence. Measured acceptance and publication
remain separate decisions.
