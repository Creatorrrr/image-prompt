# 24-hour DATA improvement review

Measurement checkpoint: 2026-10-02 10:45 UTC. The authorized work window ends at 2026-10-02 11:46:56 UTC (20:46:56 Korea time). C20 and C21 are independently deferred. The final 44-row source-only audits are complete; final integration checks continue through the cutoff.

## Published results

Fourteen new DATA cycles have published 49 accepted row changes. The initial 16-row delivery is separate, making 65 accepted rows across the initial delivery and this loop. An additional audit/report correction made no source changes. Rejected trials are excluded. The measured code/data baseline is [a207029](https://github.com/Creatorrrr/image-prompt/commit/a207029edc5abcc8c29179cbe1d3a138cf522b31), integrated by the user-requested fast-forward pull. Subsequent documentation commits do not change that measured baseline.

| Cycle | Change area | Accepted rows | Commit |
| --- | --- | ---: | --- |
| 1 | texture capture artifacts and material aliases | 9 | [9cc8125](https://github.com/Creatorrrr/image-prompt/commit/9cc812523ca2ab0dd1301cbff11d3315dde1ac71) |
| 2 | film/capture identities and optical effect ownership | 13 | [8420bdc](https://github.com/Creatorrrr/image-prompt/commit/8420bdcddf1e6b220f5fd3c5b64ece603c0076d2) |
| 3 | material surfaces and image-plane texture owners | 9 | [749e6c1](https://github.com/Creatorrrr/image-prompt/commit/749e6c1a19674c1667785bd2a6d1d65539ffbf7d) |
| 4 | motion and digital-artifact component owners | 4 | [d49725c](https://github.com/Creatorrrr/image-prompt/commit/d49725ccd3c811f9c1a2944f85a66118545fc2bd) |
| 5 | tonal-region and bounded lighting owners | 5 | [b2bdb46](https://github.com/Creatorrrr/image-prompt/commit/b2bdb46d5fde01713f2b41d5b482c0f938be2790) |
| 6 | Korean occupational labels | 1 | [e0444f0](https://github.com/Creatorrrr/image-prompt/commit/e0444f0fd07bb4913dacffcf16772e7440bc0a06) |
| 7 | photorealism image-layer owners | 1 | [e70ad91](https://github.com/Creatorrrr/image-prompt/commit/e70ad9109ba0a16f3f9236ad1c83106d60128581) |
| 10 | preserve a fictional non-sacred record contrast as an explicit source unit | 1 | [8e497ff](https://github.com/Creatorrrr/image-prompt/commit/8e497ffd49e8a37dcd3ca435b547135fa218be22) |
| 11 | preserve three narrative role and variant distinctions as complete optional units | 1 | [98619e7](https://github.com/Creatorrrr/image-prompt/commit/98619e72b07d623e01de65b352cb8188d919901f) |
| 12 | fresh explicit reef process unit, keeping original trial deferred | 1 | [3033a27](https://github.com/Creatorrrr/image-prompt/commit/3033a27234d3f702e3e98e4986922b8c1a0328b5) |
| 13 | official Korean krummholz name as one qualified alias | 1 | [9034d6f](https://github.com/Creatorrrr/image-prompt/commit/9034d6fd856aaa55ea550523424eac5f49b37eca) |
| 14 | Official Korean protostar name as one qualified subject alias | 1 | [e793d35](https://github.com/Creatorrrr/image-prompt/commit/e793d350eed966745dcb5c5d35ebbfd924cb6bff) |
| 15 | Korean returned-item shelf-state consistency | 1 | [0e5cc0d](https://github.com/Creatorrrr/image-prompt/commit/0e5cc0d1968d5cfe83d1b63e9cfa198724ea9463) |
| 16 | Liminal Korean active-use versus traces-of-use consistency | 1 | [f1d40d9](https://github.com/Creatorrrr/image-prompt/commit/f1d40d95a3e1aea89d3dbdfd2348c8ee0106c640) |

Initial delivery: [dedb6a8](https://github.com/Creatorrrr/image-prompt/commit/dedb6a817742aba25114fa274e19a9deb2990ea2). Historical final-surface audit and corrected claims: [5d5fe18](https://github.com/Creatorrrr/image-prompt/commit/5d5fe18c3960210b5c8adce7da0af7a71743ef17).

## Integration and validation

The current upstream architecture removed presets and their retired interfaces while retaining slot arrays from 42 source assets: 112 slots and 9,432 entries with identical row values and order. The new semantic index contains 9,468 documents. The dictionary hash is 23fd879001f019f0b5dd1ce2461e097014a4f530fe8d400e3c97f689fd011a46. All accepted DATA source rows survive the integration.

Locally verified 79 distinct focused current-architecture tests: 55 original passes, 3 passes after materializing current tracked illustration assets omitted by sparse checkout, and 21 additional current-boundary/authorship tests. Source/index membership, complete BM25F derivation, shard metadata and source-array preservation also passed. This is not a claim of a complete repository suite pass. Upstream's own 1131-test report is separate. Historical fixture failures from retired interfaces are not relabeled as current failures.

Current ordinary candidate retrieval uses frozen-core slot-only BM25F, eligibility and reciprocal-rank fusion. Dense query rankings from prior cycles and their old public-pack evidence remain historical evidence for those publication states; they do not establish current natural retrieval or rendered-image gains. The C20/C21 gate exercised 32 current candidate inventories and actual four-input packs with zero paid document refreshes. The cores were independently authored without candidate data from frozen synthetic engineering requests; the C21 requests were source-guided probes, not blind tests. Both proposed changes failed to demonstrate meaningful current public-consumer benefit and remain unpublished.

## Rejected or deferred trials

- C8: corrected reef labels did not preserve the physical relation on the old final surface. This exact trial remains deferred. A later separately frozen explicit-unit proposal C12 was accepted; the original result was not rewritten.
- C17 titanium alias: Korean intended recall improved, but wrong-material probes gained target exposure, including new rank 1 errors. Rejected and restored; complete local trial and a verified Library recovery bundle remain available.
- C18 rescue wording: original multilingual authored intent specifies craftspeople. A rescue preset did not justify overwriting it. Deferred before API calls.
- C19 falconer translation: the falconer candidate incorrectly ranked first for ordinary-pedestrian-with-glove queries in dense retrieval and Korean lexical retrieval. Rejected and restored; full trial and Library recovery bundle retained.
- C20 rabbit/hare label: all 16 current-core cases retain the same ordinary candidate membership and raw order. The target’s public meaning is unchanged. Presentation shuffling and four optional-augmentation substitutions add no demonstrated benefit, so the faithful translation is deferred with zero API calls. Four representative unchanged-baseline rejection audits pass; no rendered benefit is claimed.
- C21 Fresnel alias: all 16 public inventories and orders are unchanged; semantic candidate content is preserved, while admission/source bindings differ. One generic-lantern Korean case moves the existing target from raw rank 2 to 1, exchanging places with its generic sibling; no new exposure or public benefit results. Museum queries retain a pre-existing false lighthouse overlap at raw rank 2. Input/retrieval checks pass throughout; studio/workbench full composition audits pass, but keeper/museum synthetic composition records lack required adult postcomposition review fields, so those two full audits remain failures. Zero API calls.
- Other rejected subsets within published cycles remain in their original measured evidence. Accepted changes do not imply every near-miss score improved; tradeoffs and scope limitations are recorded per cycle.

## Remaining source-only leads

A 24-row instrument audit, disjoint from the recorded prior review inventories, produced 21 justified keeps and three deferrals. The shared wind pose assigns key or valve operation to both hands, while the authored trumpet action/profile assigns the left hand to support and the right hand to valve operation, consistent with [Yamaha’s guide](https://www.yamaha.com/en/musical_instrument_guide/trumpet/play/). This source-owner conflict remains unedited pending current-consumer qualification. Two shared material rows have ambiguous component lists and are not established defects. No retrieval, adoption or image benefit was measured by that source audit.

A further 20-row celestial/process audit retained all 20 rows without a qualified source repair. The rows were disjoint from recorded explicit review inventories. One broad historical evidence-link association remains an unvalidated documentation-scope ambiguity, not a physical contradiction. Historical comparisons are limited to the available shallow checkout; the audit did not measure current candidate exposure or image output.

## Spend and limits

Tracked conservative project Gemini upper: $1.3451264 against the authorized $10 cap. This includes $0.770048 recorded before the loop and $0.5750784 added during it. This deliberately includes uncertain/failed attempts and is not provider billing. Separate upstream/account spend is unknown and excluded. No C20/C21 paid calls have occurred. No automatic retry was used for uncertain API or publication outcomes.

No rendered-image quality gain is claimed. The loop's edits preserve runtime/schema/guards; the current architecture change came from upstream and was integrated as requested. A 09:50 UTC read-only check confirmed origin/main still at a207029, with zero GitHub check runs and zero commit-status contexts; the returned pending state is not CI green. Final publication and latest remote/check status will be reverified before closing the window.

## Evidence

The [current-core evidence archive](../research-evidence/photo-prompt/daylong-current-core-review-20261002/current-core-c20-c21-evidence.tar.gz) contains the exact 128 runtime input files, 32 full case records, fixed representative packs/views/audits, proposal snapshots, criteria and artifact hashes. Its SHA-256 is a7810bfdfd2219479df4dafc35a9bd8f6d81185578d8f856c126ecd710c98680. The accompanying [scope and replay limitations](../research-evidence/photo-prompt/daylong-current-core-review-20261002/README.md) distinguish the detached helper comparison from a refreshed proposed-index CLI run.

The [instrument inventory and decisions](../research-evidence/photo-prompt/daylong-current-core-review-20261002/instrument-source-inventory-and-decisions.json) record all 24 reviewed source rows and the remaining qualification limits.

The [integration record](../research-evidence/photo-prompt/daylong-current-core-review-20261002/slot-and-index-preservation.json) binds the preserved source arrays and current index. Focused test logs retain the original sparse-checkout errors and the successful [three-test rerun](../research-evidence/photo-prompt/daylong-current-core-review-20261002/illustration-boundary-rerun.log), alongside the [21 additional boundary/authorship passes](../research-evidence/photo-prompt/daylong-current-core-review-20261002/current-boundary-and-authorship.log).

The [celestial inventory and decisions](../research-evidence/photo-prompt/daylong-current-core-review-20261002/celestial-source-inventory-and-decisions.json) preserve the 20 keeps and the bounded provenance caveat.
