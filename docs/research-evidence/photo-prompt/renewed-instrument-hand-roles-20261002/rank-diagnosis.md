# Normalized-core residual rank change

## Finding

The trombone camera_direction swap is a real deterministic retrieval-order change, not public presentation shuffling, seed effects, or hash-bound variety. retrieve_core_slots ranks broad/focal BM25F queries, fuses ranks with RRF k=30, intersects the two lanes, and emits that ordering. The corpus hash binds evidence but does not shuffle the returned candidates.

BM25F statistics are computed over the complete authored slot corpus; allowed_ids restricts candidates for a slot but does not rebuild same-slot-only document frequencies or average field lengths. Two edits in instrument slots can therefore change camera_direction scores.

Before, the broad camera lane starts:
1. first_person_pov_hand_foreground: 118.908388009512
2. overhead_social_snapshot_relation: 118.874388838405
3. pc_px07_component_1: 101.708524259255

After generic correction:
1. overhead_social_snapshot_relation: 118.869270741688
2. first_person_pov_hand_foreground: 118.867858080268
3. pc_px07_component_1: 101.708757145132

The focal lane still ranks pc_px07 first and overhead second. Before, pc_px07 RRF is 0.062561094819 versus overhead 0.0625. After, pc_px07 is unchanged while overhead rises to 0.063508064516 because its broad-lane rank improved. Thus the final public top-two swap has an explicit scoring cause.

## Statistic isolation

Matched-query document-frequency changes include hand 271→272, at 434→435, in 864→865, of 737→738 and with 2193→2194. Small average-field-length changes also occur.

Counterfactuals hold original documents/lexicon fixed:
- Replacing only the document-frequency map with generic's map reproduces the broad top-two reversal
- Replacing only average-field-length statistics does not reverse them
- Updating only hand frequency nearly erases the gap but does not reverse it: first-person 118.874848685461 vs overhead 118.874388838405

The combined document-frequency changes are sufficient. Field-length changes modify scores but are not needed to explain the observed reversal. Full raw scores, matched terms, queries and RRF ranks are in rank-diagnosis-traces.json; statistic counterfactuals are in rank-diagnosis-statistic-ablations.json.

## Smaller semantic alternative

smaller-proposal.json preserves the original keys/valves vocabulary while replacing universal bilateral operation with each hand supporting or operating controls. It was tested in memory with the same corrected trumpet action against all five normalized cores and all returned slots.

Result: the same sole camera_direction swap occurs for trombone, with no other candidate ID/order change. All 17 returned slots retain membership. Full ranked output is in smaller-full-ranked-results.json; full comparison is in smaller-comparison.json.

Recommend the generic proposal. The smaller alternative still describes each hand as supporting or operating keys/valves, which does not cleanly describe the right hand moving a trombone slide. Generic instrument-specific playing/support roles are semantically broader and already remove the concrete error. The smaller version offers no observed rank-stability benefit. Do not tune synonyms merely to force this near-tie ordering back.

## Impact boundary

All ten normalized before/generic retrieval audits pass. Each corrected shared pose remains rank 1. Four scenes preserve all slot candidate orders. Trombone preserves all candidate membership but changes camera_direction ordering as described.

No core field or prompt is altered by retrieval. Every returned slot has selected=null and the binding declares optional candidate adoption. Therefore there is no observed automatic core/adoption change. The new first optional camera candidate describes an overhead social snapshot, which differs from the authored medium three-quarter viewpoint; its promotion is a residual suggestion-ranking risk. The baseline already contained this candidate at rank 2. A downstream composer could choose differently, so downstream composition equivalence is not established. No image rendering or pixel-quality claim is made.
