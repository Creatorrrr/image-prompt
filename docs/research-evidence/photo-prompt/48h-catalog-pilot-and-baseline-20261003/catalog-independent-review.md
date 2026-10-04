# Independent final review: synthetic pre-core catalog A/B

**Recommendation: DEFER the proposal; KEEP the current production catalog.** The numerical conclusion is correct. The acceptance gates fail, and the release/instruction deviations independently preclude a strict unchanged-confirmatory claim. No source evidence or repository files were edited in this review.

## Verified accounting and provenance

- Eight distinct, designer-created synthetic requests: four development and four held-out, with one animal, plant, adult-human and object case per split; each split has two Korean and two English requests. These are **not eight historical user requests**, and 32 outputs do not create 32 independent test cases.
- All **32 retained outputs** are present in eight author files: 2 arms × 2 author slots × 4 requests × 2 splits. All 32 normalized prompts are distinct. Each appears exactly once in each applicable blinded individual packet and exactly once in its within-request/within-arm pair mapping. Request wording, constraint ledgers and prompt text are preserved; prompt normalization is whitespace-only. Matched forward/reverse output and assignment orders are correct.
- All checked original/v2 design manifests and freeze bindings, proposal hashes, condition hashes, execution assignment/common-packet hashes, pre-release bindings, source-output hashes, blinded-packet hashes and original-rating freezes match. The held-out adjudicator's input hashes also match. Independently recomputing the accounting and scores passed 686 programmatic content/hash/score checks, plus prompt-uniqueness and adjudicator-input checks.
- The currently readable production source SKILL.md, catalog and controls JSON match their original recorded hashes. Across the two four-file condition snapshots, the catalog is the sole byte difference. Both catalogs retain **48 categories and 527 source-example strings**. Added examples change **11 → 17**, exclusively two appends in each of environmental_details, pose and realism_cues. Existing fields, category order, source examples and old added examples are preserved. No post-development condition change is evident in the frozen bytes.
- All prompts satisfy 48–180 words and the category-ID bookkeeping checks. These checks establish artifact integrity, not aesthetic improvement, actual access isolation, or an exhaustive history of all author attempts.

## Recomputed paired results

A = original/m7; B = proposed/p2. Every pair is quality-eligible, so **raw and quality-qualified variety are identical** throughout.

| Case | Variety A | Variety B | B−A | Mean fidelity A | Mean fidelity B |
|---|---:|---:|---:|---:|---:|
| D01 magpie | 0 | 0 | 0 | 3 | 3 |
| D02 basil | 1 | 1 | 0 | 2 | 3 |
| D03 adult mechanic | 3 | 1 | −2 | 3 | 3 |
| D04 kettle | 1 | 1 | 0 | 3 | 3 |
| H01 octopus | 1 | 2 | +1 | 3 | 3 |
| H02 fern | 0 | 0 | 0 | 3 | 2.5 |
| H03 adult passenger | 1 | 0 | −1 | 3 | 3 |
| H04 radio | 1 | 1 | 0 | 3 | 3 |

- Development: eligible-case mean delta **0**; all-four mean **−0.5**; wins/ties/losses **0/3/1**. Overall mean fidelity A/B **2.75/3**.
- Held-out: eligible-case mean delta **+0.5**; all-four mean **0**; wins/ties/losses **1/2/1**. Overall mean fidelity A/B **3/2.875**.
- Every request-arm mean coherence and grounded specificity is **3**. All 32 prompts have zero recorded critical failures. Specificity has no discriminating signal in these ratings.
- Development mean/median words: A **114/114**, B **113.5/114**. Held-out: A **111.75/111.5**, B **110.375/110**. Absolute mean gaps are **0.5** and **1.375** words (about **0.44%** and **1.23%** of A), below both length-confound thresholds. Individual counts in RESULTS.json reconcile exactly; overall range is 106–119 words.

### Strict held-out gates

The eligible mean threshold is met, but three other numerical gates fail:

1. Fern variety is 0 → 0; **both** eligible requests must strictly improve.
2. Adult-control variety is 1 → 0; a control loss is forbidden.
3. Proposed fern prompt P124558/held-p2-2 scores fidelity **2 from both judges**, so only **7/8 B prompts** score 3. The recorded reason is a photographic-medium clarity gap, **not a people/animal-exclusion violation**. It remains pair-eligible and is not a critical failure.

No repeated new critical/physical failure was recorded. Passing that gate cannot offset the failed gates above. Even hypothetically treating the fern's medium wording as fidelity 3 would leave both variety failures intact.

## Adjudication and exact corrections

**No numerical corrections to the reviewed RESULTS.json are required.** All seven observed disagreement items were sent to the third judge, with original ratings retained:

- Development fidelity: P420880 and P761522, each 3/2 → **2**.
- Development variety: B92309 0/1 → **1**; B32183 1/0 → **0**; B34707 2/1 → **1**.
- Held-out fidelity: P820785 3/2 → **3**.
- Held-out variety: B38450 2/1 → **2**.

The summarizer starts from judge 1 instead of explicitly averaging unadjudicated scores. That is a fragile implementation, but **does not change this result**: every unequal numerical item was adjudicated and all remaining scores agree. Future reuse should implement the frozen averaging rule explicitly.

For complete reporting, add explicit raw/qualified variety fields, per-request mean fidelity and grounded specificity, all-four descriptive means, and win/tie/loss counts using the values above. These are omitted reporting fields, not changed scores. Using the more conservative original held-out octopus score of 1 would lower the eligible mean to 0 and all-four mean to −0.25; DEFER is unchanged.

## Procedural qualifications

1. **One-request-at-a-time release was not followed.** PROTOCOL.v2 specifies coordinator sequential release. The frozen assignments expose all four envelope paths and the common packet requests one four-output file. The coordinator confirmed during this review that four-request assignments were delivered together and sequential release cannot be established from tool evidence. Instructions to treat requests independently are not a release barrier. Balanced ordering does not cure this deviation.
2. **Held-out judge handoff wording changed after development.** judge-handoff-note.json discloses an explicit reminder that exclusions need not be repeated as negative clauses when the described scene already satisfies them. The rubric bytes and author packet were unchanged, but judge prompts were not perfectly identical across splits. Development basil fidelity uncertainty must not be presented as a clean treatment effect or directly comparable improvement in judging behavior.
3. Hashes and self-reported freeze times do not prove access isolation, fresh-context independence, no earlier exposure or no selective attempt history. All agents shared a filesystem; the holdout seal was procedural. The score/mapping bridge is independently consistent, but it is not an external audit of execution.
4. A chronology-label error was found and corrected by the coordinator during review: development-summary.json originally labeled its **17:09:56** write time as unblinded_utc. It now uses summary_written_utc, preserves the original value, and records the coordinator-reported first mapped tool result at **17:08:19**, preceding the **17:08:45** held-out pre-release freeze. I verified the corrected metadata; I did not independently inspect that coordinator transcript. This resolves the misleading label but does not turn filesystem timestamps or attestations into independent access-sequence proof. No condition, prompt or rating changed in this correction.
5. Each author context handled four requests, with possible carryover; there are only two output samples per arm/request and two eligible held-out requests. The model/version/backend and sampling seeds were not fully surfaced. Model-based author/judge assessments, purposive synthetic cases and ceiling-heavy ratings further limit generalization. No full-core, retrieval, generated-image, human-preference or pixel-quality evaluation occurred in this experiment.

## Suggested shareable wording

“In a small synthetic text-only pilot, six optional catalog-example additions did not meet the frozen acceptance criteria. Held-out variety improved for the octopus case, tied for the fern and radio, and declined for the adult-passenger control. The two eligible cases averaged +0.5, but the fern strict-gain, adult non-regression and all-proposed-prompts fidelity gates failed. We retained the original catalog. Request-release and cross-split judge-instruction deviations limit this to descriptive pilot evidence; it does not establish a general creativity or rendered-image benefit.”

Reviewed RESULTS.json snapshot SHA256: `c0246f79c8b8864ea1e16efe8c3474f13faf7284b19e55a68b210fddff842b67`.
