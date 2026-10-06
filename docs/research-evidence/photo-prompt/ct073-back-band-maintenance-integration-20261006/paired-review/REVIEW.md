# Latest structural-main paired-result and evidence-reuse review

**PASS for the bounded paired-result/evidence-reuse scope. No substantive discrepancy or correction is requested.** This is not a review or approval of the evolving V25 implementation.

## Verified results

- All 12 new 3b-based packs, six BEFORE and six AFTER, are byte-identical to the corresponding original baa packs. Both old and new COMMANDS pack hashes match actual files.
- All 105 frozen authoring files retain their original byte counts and SHA-256 hashes. The frozen manifest remains `4c1dc1bc6073a2566fae452e198008f8ddd1cf2f7cb53ca7c14e59e1a2fcfae4`.
- All 24 new preflight/generation receipts report successful completion, zero return codes, empty stderr, and no blocked attempt. Commands match their earlier corresponding commands except interpreter/output paths and use the same sealed case inputs.
- BEFORE execution identifies `3b481ca94fdbbeeb453e1d3ec657db0f5baf6a80`. AFTER execution identifies that parent plus the uncommitted 23-file overlay sealed by `43afb3cb42b29fc1462017115e397067ff5d43b54c69a5010a325fd4ab08bfe8`. The receipts do not relabel their execution source as the later DATA commit.
- The exact 23-path overlay matches later commit `dc77d63ce26b9a39037b44e86554b76fe7eacf4c`, parent 3b and tree `9d30471ee0b6717732a711402347b8d1e309bf7e`. All sealed file sizes, SHA-256 values and Git blobs verify.
- Twenty-one reused source/cache paths are exact aaeabe Git blobs. The visual manifest differs from aaeabe by precisely one old-to-normalized registry-hash replacement. Textile is the separate reference correction. No new vector payload is introduced.
- The latest real frozen-boundary generator output is 213,313 bytes, SHA-256 `0b028da1680fd5cdb042b5e6eb711d33484c8c1276220e09b01239163219d037`, identical to the earlier CT073 output. Its command matches official V24's frozen generation command except interpreter/output destination, and all frozen boundary inputs still match official V24's hashes. This receipt proves normal public generation; it is not a completed V25 validator run.

## Consumer qualification

The original **OWNER CONSISTENCY ONLY** outcome remains valid. Direct inspection of current packs confirms:

- All six visual memberships and all primary candidate-collection memberships are preserved
- Positive cases a and b contain no CT073 candidate either before or after: no discovery improvement
- Case c's useful strap v1 offer is byte-identical and eligible at position four
- Case d retains the incompatible v2 offer as eligible despite the explicit no-fastening request; it moves from position six to one
- The ordering policy is `seed_shuffled_non_preferential`. Position movement is not a relevance-ranking improvement
- Case d changes the owner-property metadata and corresponding reject-substitute text; no exclusion/eligibility repair is demonstrated

No adoption, cosine-performance, rendered-pixel, or preference-success claim is supported. New actual executions support reuse of the prior outcome observations, while current source/registry/proof identities must remain separately bound in V25.

## Textile evidence

The recorded one-method BEFORE failure matches the independently recomputed old source/record mismatch (`c0c377…` expected versus `8d2790…` actual). AFTER points to the already-existing main-merge maintenance record whose authored digest is exactly `8d2790…`. The before/after authored textile objects are identical after removing the reference; both maintenance records remain byte-identical. The tested clothing module is unchanged across 3b, dc77 and the working file.

The recorded AFTER run reports all seven clothing methods passing, zero failures/errors/skips, and only deliberate guard self-test events. Those receipts and the precise source cause were reviewed; tests were not rerun.

## Provider and provenance limits

The command environments are sanitized and contain the configured network guard, not API credentials. No blocked-event logs are present. The overlay and generation receipts record zero provider calls and zero embedding attempts; exact previous source/cache blobs substantiate reuse. This reviewer made no network/provider call and read no credential or handoff-execution file.

Original numeric embedding receipts retain their earlier execution provenance and original HTTP-byte limits. Latest execution identity is 3b plus the overlay, later mapped to dc77. Preserved early CT073 V24 work and official upstream V24 are distinct histories; this report does not replace their proofs or validate the evolving V25 code.

## Artifacts and actions

- `packs.json`: direct old/new pack hashes, memberships, CT073 positions and eligibility
- `commands-inputs-source.json`: 105 input checks, 24 command receipts, overlay/commit mapping, frozen-boundary output and cache reuse
- `textile-evidence.json`: direct canonical-digest diagnosis and before/after test receipts
- `audit_commands_and_inputs.py`: reproducible read-only checks

No production edits, tests, refs, commits or publication were performed. The initial prior repository pack paths were unavailable; comparison used the verified original recovery directories `fastening-before-baa-20261006/generation-adapter-v3` and `fastening-after-baa-20261006/generation-adapter-v3`.
