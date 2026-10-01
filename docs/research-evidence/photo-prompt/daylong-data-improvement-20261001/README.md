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

The capture publication was verified on remote main at `8420bdcddf1e6b220f5fd3c5b64ece603c0076d2`; the pull was up to date and all 97 post-pull related tests passed. GitHub reported zero check runs and zero commit-status contexts.

### Material and grain-owner cycle

Frozen evidence: `../material-data-cleanup-20261001/`. Of 32 inspected rows, nine repairs were accepted and 23 retained. Three proposed alias consolidations were restored to exact baseline rows/vectors because their reverse near-misses had no positive-rank benefit. All 13 dense positive rank-one results survived; three dense near-misses moved lower and ten remained equal, with none higher. Korean crochet exact-label coverage improved from no lexical hit to rank one, but English/Korean knitting ambiguity remains and this does not establish general bilingual improvement.

A dedicated background test exposed a stale source binding introduced in the preceding capture owner edits. The current-source contract was repaired with a new versioned maintenance record covering those four capture/material owner corrections; the original and ten historical migration records remain unchanged. This provenance-only repair did not alter runtime semantic text or require another embedding.

Published and remote-verified commit: `749e6c1a19674c1667785bd2a6d1d65539ffbf7d`. All 155 related final tests and 115 post-pull tests passed. GitHub reported zero check runs and zero commit-status contexts. All 38 original one-attempt embeddings are retained, including three unused proposal vectors; the additional conservative bound is $0.0622592, cumulative $0.9699328. These counts are related checks, not a claim that the whole repository suite or rendered-image qualification passed.

### Motion and digital-artifact owner cycle

Frozen evidence: `../motion-artifact-owner-data-cleanup-20261001/`. Forty inspected rows yielded four accepted owner corrections and36 exact keeps after four proposals were restored. All positive target ranks are unchanged. Three dense near-misses improve; two residual relative-rank rises retain exact baseline target vectors/scores and result from source-correct demotions of other wrong candidates. The report explicitly records light trails entering top ten on q04; it does not claim every top-k exposure is unchanged. Independent read-only review reproduced all120 baseline/proposal/accepted result rows and verified the source, derived bundles, index and cached vectors. All164 related final tests passed.

The28 frozen input texts completed over30 attempts, including one interrupted/unknown and one failed attempt followed by separately reviewed recoveries. Both unsuccessful attempts are conservatively counted; no automatic retry or frozen-input change occurred. Additional cost upper bound $0.049152; cumulative tracked upper $1.0190848. Publication receipts and post-pull checks remain separate from these pre-publication results.
