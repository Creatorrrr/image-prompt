# Relationship mechanism selected-text projection

Tooling worker: `/root/review_amendment_tools`, assigned gpt-6.1-sol / high. This note is not a corpus approval or registration. No root source-reading attribution is asserted.

## Actual frozen source read

Read the complete frozen candidate at `ORDER[12165]`: `cand_faa4fd72b79d567ca6423eafa8058be0`, source record canonical SHA-256 `5d09d69583bd5d8b7255b409706e307070e42dc9cb67698e8602fa033886a8ec`. Its complete reference closure is empty. The full source is:

```
record_kind: relationship_mechanism
conditions: {}
effects: {dimensions: [], properties: []}
content.definition: Subtle practical makeup or motivated reflected color appears on the cheeks while other social-action evidence remains visible.
content.family_ids: [affect_expression_gaze]
content.priority_dimension: observable_action
content.role: visual_atom
content.topic_ids: [expression_manga_symbol_translation]
provenance.source: character_mechanism_node:practical_blush_color_cue
provenance.sha256: 491064af49b3e4a94b5a352eae92992f34d21ceff8bf424ccbff557a29cd2b22
```

The source offers practical makeup OR motivated reflected color, with a shared cheek carrier and the shared requirement that other social-action evidence remain visible. It does not select a cosmetic hue, a reflected-light source, exact emotion, a facial movement, or an actual social act. The new tests use this text only as an isolated structural fixture. They do not supply actual effects, qualify native ownership, change its kind, amend its frozen decision, or approve that record.

## Consumer and source-field audit

Read the relevant complete functions in `photo_candidate_corpus.entry`, `photo_global_index.fields/text/documents`, `photo_search_layout.guard_record`, `prompt_generator.candidate_pack_entry_blob`, `photo_candidate_realizations.selected_view`, and native pack/proposal projection consumers. Entry starts from the complete content, so allowing the mechanism kind alone would leave its unselected original definition in the selected entry. Overriding only en/ko would not solve that leak. Native pack consumers also use selected en/definition as fallback and can read `concept_candidate.concept_terms`.

A mechanical key inventory of the frozen SOURCE found 135 relationship_mechanism records. Every one has exactly `definition`, `family_ids`, `priority_dimension`, `role`, and `topic_ids`; none has another positive prose field such as topic definitions, manifestations, components, labels, aliases or semantic prose. This key inventory is not a claim of a complete semantic read of all 135 definitions. No additional actual positive-field leakage example was found in this frozen kind.

## Contract and behavior

The existing visual_option projection contract remains exactly `{en, ko, embedding_text, concept_units, relations}`. `photo-relationship-realization-content/v1` is an explicit per-kind extension with exactly those five fields plus required nonempty string `definition`. No version/identity/metadata/guard keys are accepted inside a branch body. Every actual declared RID, including optional base, needs exactly one full selected body; foreign, missing and duplicate RIDs fail. Mechanism effect contract/branch guards are structurally validated without rewriting them.

The mechanism source may keep canonical discovery aliases, keywords, terms, paraphrases and concept_terms. Existing explicit projection behavior clears these discovery-only lists in the selected render view, while leaving canonical search text unchanged. Selected phrase_en/phrase_ko are derived from selected en/ko. Complete definition/en/ko/embedding/concept/relation body comes from the explicit branch. Negative/research metadata such as semantics.claim_limits remains unchanged.

Source fields without selected counterparts fail visibly if nonempty: `ja`, `label_en`, `label_ko`, `definitions_by_topic`, `manifestations`, `components`, `member_candidates`, `embedding_texts`, `concept_candidate`, and known positive nested `semantics` fields (`definition`, `semantic_caption`, `visual_components`, `support_cues`, `component_semantics`). This is an explicit bounded supported contract, not a generic stripping of source text. Such sources need a separately designed projection contract before use. Source metadata is not flattened into selected meaning.

Canonical full positive index text preserves the original OR and its single search identity/document. A selected entry or selected presented view has only the selected definition/body in positive text surfaces. The original authored_record remains available as immutable provenance in presented views. Parsing/compilation cannot itself establish whether an author's selected text is semantically correct.

## Offline validation

Keys were absent (`env -i` preserves PATH only) and OS networking denied:

```
/usr/bin/env -i PATH="$PATH" sandbox-exec -p '(version 1) (allow default) (deny network*)' python -m unittest tests.test_photo_realization_content tests.test_photo_candidate_corpus -q
```

Final result: 28 tests passed, including 14 selected-text tests. New meaningful cases cover both makeup/reflected-color directions, complete selected definition without original OR leakage, selected_view integration, unchanged kind/identity/guards/effects/provenance/source, exact per-kind shape, malformed/foreign fields and RIDs, unprojected positive-field rejection, source discovery/render distinction, optional base, lazy/full selected equivalence, and sibling-definition quote rejection.

The broader command also included `tests.test_photo_candidate_realizations`. Before the final selected_view case was added it passed 47 tests. The subsequent 48-test run failed three existing tests: `test_optional_playback_requires_an_existing_positive_witness`, `test_public_bundle_exposes_two_complete_choices_with_one_member_each`, and `test_unselected_branch_does_not_close_selected_open_scope`. Only the new selected_view test changed between those runs in this worker's files; concurrently owned native qualification/precore code was changing. The failures were reported to root, and no guards or unowned fixtures were weakened. They remain a broader integration check for root/native worker.

No canonical/SOURCE/authored/global/index/runtime data, R/direct_review.py, R/delegated_amendments.py, git state, provider/network/download/model state or other worker-owned source was modified. No actual candidate proposal/registration/application occurred.

Final changed code SHA-256:

- `skills/photo-prompt-image-generator/scripts/photo_candidate_realizations.py`: `ab77a4e5d262af30ef1a432ff1898c74eecbce7c95485cf923aeb94b386f94fb`
- `tests/test_photo_realization_content.py`: `5a5e7459258680ea2ffcbdb396527583fb6c44a4036930c906925e641a4e4ee3`
