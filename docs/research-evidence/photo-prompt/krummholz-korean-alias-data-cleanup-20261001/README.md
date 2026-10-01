# Qualified Korean krummholz alias DATA experiment

## Hypothesis and exact scope

Append exactly `왜성변형수 바람형 패치` to the existing aliases of
`slot:surface_material:treeline_wind_pruned_krummholz_surface` in
`photo_prompt_natural_environment_extension.json`. This is a named-concept
search-coverage proposal, not a scientific correction or final-prompt defect.
Freeze all 11 natural-extension surface-material rows: one append-only proposal,
ten exact keeps. Every other field, alias, eligibility guard, relation, optional
policy, maintenance reference, and accepted reef process unit stays exact.
No bare noun alias is added anywhere in the treeline family.

## Source gate

- National Institute of Ecology, *아고산 침엽수림 쇠퇴 원인과 대책*, NIE IR 16-01,
  PDF page 4 / printed page 5, “산악경관의 수직적 분포”: explicitly pairs
  왜성변형수 with Krummholz. [Official PDF](https://www.nie.re.kr/nie/cmmn/file/fileDown.do?atchFileId=MFILE_0008KundNnNSYYU&fileSn=3)
- 공우석 외, *한반도 주요 산정의 식물종 분포와 기후변화 취약종*, 환경영향평가
  23(2), 2014, pp.119–136, DOI 10.14249/eia.2014.23.2.119, PDF page 16 /
  printed page 134: pairs 왜성변형수 with krummholz and discusses low growth
  adapted to alpine/subalpine conditions. [Original research PDF](https://journal.kci.go.kr/kseia/archive/articlePdf?artiId=ART001871797)
- NPS, “Alpine Vegetation Resource Brief,” Background Information supports the
  existing wind-pruned, ground-hugging, boulder-sheltered specialization.
  [Official source](https://home.nps.gov/articles/000/alpine-vegetation-resource-brief.htm)

The exact source-gated scout proposal and eight unmeasured independent probes
are copied and hash-bound in `scout/`. Its original freeze SHA is
`eaba1d9572a7977a0803f297231ab0703a08512e5e6a301aa78a0e4e83b8332a`.
The copied controlled V6 evidence shows exact candidate, detail, overview and
full-pack equality, optional material-only scope, no relations, and no forced
eligibility. It is a preserved source-gate artifact, not a fresh natural
retrieval/adoption, composed-prompt or rendered-image evaluation.

## Frozen evaluation

Two states (baseline/proposal), 13 queries, two methods (dense/BM25F), 52 rows.
The original eight texts remain exact; add bare-name controls `krummholz`,
`크룸홀츠`, `왜성변형수`, and two exact earlier surface-material controls:

- `a matte concrete surface with subdued highlights` → `matte_concrete_surface`
- `a translucent glass block surface` → `translucent_glass_block`

Control query objects and original vector-cache files are copied intact and
hash-bound. Cache reuse requires exact model, dimension and text. The published
baseline manifest and complete merged/raw snapshots are frozen; baseline shards
are hash-verified from existing runtime files or that published Git object.
No private branch, unpublished ref, or network fetch is required for replay.

Each row includes primary target and secondary krummholz rank/score, hit count,
explicit no-hit status, complete top12 and full ranked list. The collateral
comparison records every changed rank/score entry, all top12 transitions and
all no-hit cases. Nothing auto-accepts the proposal.

Acceptance requires measured Korean named-coverage gain without unjustified
near-miss/collateral loss. Unchanged final output supplies no compensating
semantic repair. Bare-name discovery does not make this specialized surface
universal. No wording/query tuning after measurement.

## Execution safety and budget

Default evaluator execution is a zero-call plan. Only `--execute` can send the
exact frozen missing inputs, after source equality and current ledger/STOP/
deadline checks. It uses a shared exclusive lock, durable fsync-before-send
attempt log, single-request no-retry network path, redirect rejection, per-input
8192-byte conservative token bound, and no secret/error body output. Failed or
uncertain attempts block continuation; completed hashes cannot be resent.

Expected workload: one proposed document plus 11 uncached queries = 12 inputs.
The two unrelated queries use exact cached vectors. The 15-attempt ceiling is
$0.024576; the spare allowance does not authorize automatic retries or extra
inputs. Tracked prior upper bound: $1.2091392; maximum cumulative: $1.2337152,
inside the $10 project ceiling. Deadline: 2026-10-02T11:46:56Z.

## Commands from repository root

Preparation only, no source writes or API calls:

```sh
E=docs/research-evidence/photo-prompt/krummholz-korean-alias-data-cleanup-20261001
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/test_frozen_cycle.py"
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py"
```

Separately authorized apply/evaluate; preparation worker does not run these:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/apply_proposal.py" --apply
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --execute
```

After measurement and independently reviewed acceptance, zero-call replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --replay
```

Current repository tests are intentionally untouched during preparation. The
coordinator owns migration of prior whole-current-snapshot assertions before
source application; historical evidence must remain reproducible.


## Explicit first-document manual recovery

The first document attempt ended with URLError before any vector or query result
was saved. Its immutable record remains charged and copied with the original
freeze/scripts/logs under `recovery-revisions/pre-manual-retry/`. The coordinator
explicitly approved exactly one manual retry of that same document hash. No
inventory, query, source, acceptance criterion, model, dimension or budget cap
changed. Safe future failures add exception/reason type and numeric errno only.

Only this explicit command can consume that recovery, after separate approval:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$E/evaluate_cycle.py" --execute --manual-retry-first-document
```

It permits only attempt2 of the exact failed input. The original failure is
never erased or marked completed. After a successful attempt2, the original 11
unsent queries can proceed once. Any subsequent failure/uncertainty blocks all
further calls, including a repeat of the recovery flag. Thirteen total attempts
are planned including the charged original failure: $0.0212992, cumulative
$1.2304384. The original15-attempt/$0.024576 ceiling is unchanged; no automatic
retry is enabled. See `manual-recovery-rationale.json` for the precise scope.
