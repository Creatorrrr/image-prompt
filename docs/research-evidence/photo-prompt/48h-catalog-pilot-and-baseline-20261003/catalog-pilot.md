# Neutral pre-core catalog experiment: retain the existing catalog

Decision: **DEFER the six proposed additions; KEEP production unchanged.** This is a small synthetic text-only pilot, not proof of general creativity or rendered-image improvement. Request-release and judge-handoff deviations further limit inference; this negative result does not establish general catalog harm. No DATA cycle is counted and no provider calls were made.

## Intervention and design

The proposal appends six optional nonhuman surface/support examples across three existing categories. Both conditions retain 48 categories and 527 source examples; authored added examples change 11→17. The other supplied skill/controls files are byte-identical. There are eight distinct synthetic requests, four development and four held-out, with animal, plant, adult-human and object cases in each split. Two independently assigned author contexts per condition each produce four prompts, giving 32 retained initial paragraphs. This does not create 32 independent test cases.

Original and pre-output-amended v 2 criteria are both archived. The v 2 primary comparison is the two eligible living-nonhuman held-out requests; both must strictly improve, while human/object controls must not regress. Passing would justify only a larger preregistered pilot, not a repository patch. Four new author contexts were used for held-out requests. No intervention or author-package changes followed development. Outputs were frozen, whitespace-normalized, anonymized and scored by two fresh judges in individual-first/pair-second phases, followed by fresh adjudication of every numerical disagreement. Full mappings and hashes are retained for reproducibility.

## Results

Quality-qualified pair variety on a 0–3 scale; every pair is eligible, so raw scores are identical:

| Request | Original | Proposed | Difference |
|---|---:|---:|---:|
| Development magpie |0|0|0|
| Development basil |1|1|0|
| Development adult mechanic |3|1|−2|
| Development kettle |1|1|0|
| Held-out octopus |1|2|+1|
| Held-out fern |0|0|0|
| Held-out adult passenger |1|0|−1|
| Held-out radio |1|1|0|

The held-out eligible mean difference is+0.5, but the fern strict-gain and adult non-regression gates fail. One proposed fern paragraph receives fidelity 2 from both judges for underexplicit photographic medium, so the all-proposed-fidelity 3 gate also fails. This is not an exclusion violation or critical failure. All 32 prompts have no recorded critical failure, coherence 3 and specificity 3; the ceiling-heavy ratings provide little discrimination on those metrics.

Development all-four mean difference is−0.5, with 0 wins/3 ties/1 loss. Held-out all-four mean is 0, with 1 win/2 ties/1 loss. Mean fidelity original/proposed is 2.75/3 in development and 3/2.875 held-out. Mean words original/proposed are 114/113.5 and 111.75/110.375, below the frozen length-confound thresholds. Using the more conservative original octopus judge score would lower the eligible difference to 0, leaving DEFER unchanged.

## Important procedural limitations

- The protocol requested one-request-at-a-time release, but each author received all four envelope paths together. Independent-treatment instructions and matched forward/reverse orders are not a release barrier. Carryover remains possible.
- Held-out judge handoffs added a reminder that satisfied exclusions need not be repeated as negative clauses, after development exclusion uncertainty was observed. Rubric bytes stayed unchanged, but judge wording was not identical across splits. This is an additional procedural limitation; no clean cross-split fidelity-treatment claim is made.
- Shared filesystem and procedural seals do not prove access isolation. Hashes establish artifact consistency, not a complete independent history of every model attempt. Exact backend/model version, temperature and model sampling seed were unavailable.
- A summary write timestamp was initially mislabeled as unblinding time and corrected with the original value preserved. The reported mapped-output tool result preceded held-out release, but filesystem timestamps alone cannot establish that sequence.
- Only two eligible held-out cases and two samples per condition/request were tested. No complete core, retrieval, image generation, pixel evaluation or human preference study occurred.

These numerical failures and procedural deviations independently support retaining the existing production catalog. Do not treat a single octopus gain as general improvement. No examples, thresholds, prompts or scores were tuned after held-out outcomes.

## Evidence

`RESULTS.json` includes all case metrics and decision limits. `RESULTS.reviewed-snapshot.json` preserves the snapshot checked by the independent final reviewer. `independent-final-review.md` independently reconciles 32 outputs, mappings, original and adjudicated scores, and 686 content/hash/score checks. Frozen design, condition snapshots, assignments, first outputs, opaque judging packets, ratings, mappings and scripts are included in the evidence archive. Paths recorded inside scripts reflect the evaluation workspace and may need relocation before replay. No secrets are included.
