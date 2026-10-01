# Bounded DATA improvement run

Work window: 2026-10-01 11:46:56 UTC through 2026-10-02 11:46:56 UTC.

Each cycle freezes its source inventory and diagnostic queries, preserves the original authored intent, makes minimal DATA changes, refreshes only changed semantic inputs, verifies positive and near-miss cases, receives an independent read-only review, and runs relevant validation. A publication cycle commits, pulls and reconciles `origin/main`, reruns affected checks, and uses a normal push. No force pushes, blanket filters, or unrelated retrieval changes are part of this run.

The per-cycle directories hold complete frozen rows, baseline data, exact-text vector caches, API-attempt ledgers and reproduction scripts. Current and prior referenced semantic-index shards remain in Git. The previous aggregate-validator errors were resolved upstream before this run; separately reported optional-routing fixture and image-qualification limitations are not treated as passing results.

## Publications

### Initial completed cleanup

- Verified remote main: `dedb6a817742aba25114fa274e19a9deb2990ea2`
- Normal push from `98847a8bcc35f85142fe0eb4322e35eacbe9fdc2`; the fresh pull was already up to date
- 16 DATA corrections preserved; fresh 74-test DATA/retrieval group passed
- Independent review ran 34 focused checks and a synthetic rule-mode baseline-rejection audit
- Dictionary, 10,174-document semantic index and visual-profile index validated
- GitHub returned zero check runs and zero commit-status contexts
- No new API calls for integration/publication

The quiet-home commute near-miss remains disclosed. Within-slot cosine rank changed 8 to 5; BM25F already ranked the candidate first before the cleanup. The live hybrid shortlist can expose it as an optional candidate. A synthetic rule-mode run with all optional candidates rejected passed the composed audit. This does not establish automatic semantic rejection, a semantic-mode end-to-end result, or improved rendered images.

### Texture cycle

Frozen evidence: `../texture-data-cleanup-20261001/`. The immutable inventory covers 44 texture rows with nine proposed minimal corrections and 35 keeps, evaluated with 18 positives and nine diagnostic near-misses. Published and remote-verified commit: `9cc812523ca2ab0dd1301cbff11d3315dde1ac71`. The fresh pull was up to date, and the final post-pull run passed all 89 related tests. Sparse-checkout capture fixtures were restored from their exact baseline bytes with 24 matching hash references. GitHub reported zero check runs and zero commit-status contexts. Both retrieval methods preserved all 18 positive rank-one results; reverse near-misses remain documented. All 36 one-attempt embeddings succeeded, for an additional conservative bound of $0.0589824 and cumulative tracked bound of $0.8290304.

## Cost accounting

The prior tracked cleanup conservative upper bound is $0.770048. The texture cycle is limited to at most 40 one-attempt text-embedding calls, an additional $0.065536 conservative bound. Actual attempted-call bounds are recorded per cycle. These are not measured invoices; unrelated upstream spending was not reconciled with billing. The project authorization remains $10, with exact-text caches reused and automatic retries disabled.

Prices and limits were checked against official documentation on 2026-10-01: https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/embeddings.

### Film/capture ownership cycle

Frozen evidence: `../capture-owner-data-cleanup-20261001/`. The inventory has 54 rows, 16 minimal proposed corrections and 38 keeps. Thirty-two English diagnostic queries were frozen before editing. The maximum 56 one-attempt embeddings have an additional conservative bound of $0.0917504; nominal workload is 48 uncached texts. Valid model/format shorthand, authored optical alternatives, and disposable-camera frontal lighting remain preserved.

The capture cycle accepted 13 corrections after retaining HP5, 400H and compact CCD in their original state. All positive ranks and the five dense/one lexical improvements survive, and all three reverse probes return to baseline. Final accepted-source validation passed 137 related tests. Actual cost history remains 48 one-attempt calls, including three unused proposal document vectors, adding $0.0786432 to the tracked conservative bound ($0.9076736 cumulative).
