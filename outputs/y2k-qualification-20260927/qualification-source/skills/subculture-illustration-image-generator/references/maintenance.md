# Illustration Skill Maintenance

## Keep Research and Runtime Separate

- Store citations, limitations, and provenance in `assets/research_evidence_illustration/`.
- Preserve `illustration_moe_elements_v1.json`, the five `assets/research_evidence_moe_elements/dossiers_v2/` shards, `intent_corpus_v2.json`, `illustration_moe_compatibility_v2.json`, `moe_meaning_contracts_v1.json`, `image_search_evidence_v1.json`, `moe_meaning_contracts_v2.json`, and compiled `illustration_moe_grammar_v2.json`/`v3.json`/`v4.json` as exact historical replay inputs. Build the seventeen-profile successor with `build_moe_visual_additions_v1.py`, then compile the small `illustration_moe_grammar_v5.json` manifest with `compile_moe_grammar_v5.py`. Never hand-edit a generated meaning/grammar asset or scan ordinary concept prose to activate an element.
- A meaning contract must separate `canonical_definition_ko` from runtime realization. Preserve the definition's actual lineage and semantic core, including sensitive adult meaning where material; use `runtime_label_policy` and `runtime_forbidden_labels` only to control emitted labels. Require observable `component_groups`, declare non-equivalents and forbidden inferences, and classify fidelity as exact-componentized, safe analogue, partial evidence, sequence-required, or interaction-required. Label removal is never permission to euphemistically change the concept or evade safety evaluation.
- A visual extension must hash-bind its underlying meaning and image-search evidence. Type every reviewed alias as exact, variant, carrier, related, or ambiguous; related and ambiguous terms never activate. Cover every candidate subtype exactly once across mutually exclusive visual variants. Every variant must retain all meaning component groups and declare all-of/any-of anchors, topology, camera, temporal/interaction needs, negative rendered confounds, and supported output modes. Do not turn a missing source URL into inferred evidence or make a negative-confound phrase a lexical prompt failure. Community-only etymology remains low confidence, tan never implies ethnicity, and an appearance archetype never supplies an unstated relationship plot.
- Store the 20-topic universal-scene corpus and immutable shard hashes in `assets/research_evidence_universal_scene/`. Topic matrices are synthesis records, never independent sources.
- Store only abstract visual/router/guard/metric nodes and evidence IDs in the runtime graph.
- Keep `illustration_universal_scene_candidates_v1.json` route-independent. Research topic IDs are provenance only and cannot participate in selection. Keep fixed/closed/open, resource, distance, bridge, and sparse-exception policy in `illustration_universal_compatibility_graph_v1.json`; never add an all-pairs compatibility matrix.
- Keep reviewed multilingual aliases, directional substitution polarity, embodiment/capability assertions, literal visual-realization profiles, and exact-target English composition carriers in `illustration_universal_semantic_bindings_v1.json`. A realization profile must preserve compatible slot-to-facet authority, nonempty participant ownership, exact quantifier/enforcement semantics, polarized literal groups, and candidate-owned resource/pixel kinds. Composition carriers are keyed by fact/polarity, slot/value, or role/value and must be normalized English; never copy an uncovered non-English request phrase into an English prompt. Compile them with `compile_universal_composition_carriers.py` and do not add a holdout-specific runtime branch.
- Never copy source prose, actual artist names, studio names, protected titles, or franchise designs into prompt candidates.
- Use only `source_supported`, `cross_source_synthesis`, and `design_inference`. Cross-source synthesis requires two independent source records; the topic matrix does not count as a source.

## Validate Before Use

Run:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py
.venv/bin/python -m unittest tests.test_subculture_illustration_moe_elements
.venv/bin/python skills/subculture-illustration-image-generator/scripts/build_moe_meaning_contracts_v2.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v4.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/build_moe_visual_additions_v1.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_moe_grammar_v5.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/compile_universal_composition_carriers.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v4.py --check
.venv/bin/python skills/subculture-illustration-image-generator/scripts/qualify_moe_grammar_v5.py --check
```

For a moe-only change, the focused unittest plus deterministic historical v4 checks, v5 addition/manifest comparisons, and v5 bounded qualification are the required product checks. Do not expand it into universal 24x417 or hidden generalization qualification unless the universal assets/runtime changed. The focused suite must preserve the historical neutral/preference/multi-element cases, then cover all 45 current canonical selections, all typed aliases, related/ambiguous rejection, variant-lineage isolation, sensitive-label omission, meaning/visual contract mutations, literal visual requirements, output capability, and retry/photo hash stability.

The validator must cover both research corpora, typed node roles, compatibility, route/format coverage, the typed image-generation retry policy, the current source-only universal oracle and full canonical embedded scene contracts with ordered participant bindings, exact unique ordered prior-exposure inputs, exact identity/slot/context/fixed-role projections, authenticated fact/slot/role/atom/bridge/resource composition carriers, asserted-presence/asserted-absence/forbidden identity polarity, complete fixed-slot composition evidence, literal-realization selection/eligibility quantifiers and owner-joined claims/pixels, canonical universal-scene selector replay, frozen universal render expectations, any versioned v3 prompt qualification included in the release, protected-name boundaries, and explicit byte-preserving replay of immutable v1/v2 prompt and render evidence. It is not a pixel evaluator.

Read top-level `status` as validator execution/integrity only. Read `product_qualification_status` for the actual aggregate qualification; it remains `partial` while any required render case lacks a qualified final image.

## Preserve the Photo Boundary

The illustration skill must not import photo generator modules, load photo tags or quality layers, or regenerate the photo semantic index. Re-run the frozen photo baseline after changes. Only the photo skill's descriptive sibling-routing text may change in this goal.

## Change Discipline

- Freeze new natural-language and render expectations before adding routes.
- Freeze the exact original request and separately reviewed literal-bound scene contract before implementing a v3 behavior. Fixed values need literal positive spans, closed slots need literal negative spans, and ambiguity must remain open or unknown.
- Preserve three-way oracle lineage: immutable v1 request source, immutable v1 scene-contract source, and reviewed v2 contract/current-oracle/crosswalk artifacts. Every v2 row names its exact v1 source record and revision reason. The oracle compiler may read only those source artifacts; it must not read production candidates, runtime selections, packs, audits, qualification outputs, images, or run ledgers.
- Never replace the skill-agent semantic preflight with request-specific regexes, keyword guessing, holdout branches, or a claim that the local runtime understands arbitrary natural language.
- Keep audit authority outside pack self-assertions: recompute the exact request-text and canonical embedded-contract hashes, validate embedded participant bindings and the unique ordered prior-exposure list, cross-check identity/slot/context/fixed-role projections, reload local universal assets, match their bytes to the pack hashes, and replay the selector from every canonical input before re-evaluating selected guards, owner-resolved resources, candidate-owned pixels, weapon boundaries, and fixed/closed slots. Include mutation tests that remove or substitute an atom, break a realization owner join or quantifier, recompute every stored hash and `pack_id`, and still fail exact scene replay.
- Validate `composition_carriers` as selector-authenticated data: exact six-section coverage, exact identifiers and semantic values, unique normalized lexeme groups, at least two substantive anchors where available, and closed identity polarity. Mutation tests must fail when a group is removed or weakened, an asserted fact is relabeled forbidden, or a forbidden-fact evidence phrase lacks same-clause scoped negation.
- Prefer a shared mechanism family and typed compatibility over flat presets.
- Keep one primary plus at most two supports.
- Apply that primary/support budget globally across all explicitly selected moe elements. Never allocate a separate three-node bundle per element or append independent element clauses after a completed prompt.
- Bind each selected moe element to the exact local canonical and visual meaning-contract bytes and hashes before variant selection. Make every required component group and selected variant constraint literal in the composed prompt even when an element receives only one global support node. Reload and compare the local v5 manifest, v4 base, and addition bytes during audit; recomputing an embedded contract hash or pack ID must not authorize a changed definition, fidelity class, runtime-label policy, visual lineage, or medium capability.
- Keep one universal event spine, invariant candidate-count and hard-gate budgets across creativity, and at most one optional remote premise. Catalog growth must not change canonical selection order or create quadratic pair data.
- Add a node only when it produces observable evidence that an existing node cannot express.
- Record material research, routing, audit, or pixel failures before retrying. Do not lower a gate to accept a failed image.
- Add a new qualification version when a pack or composed contract changes. Never mutate a historical pack, composed prompt, audit, result, image, or its recorded hash to make it satisfy a newer contract.
- Default new work to v3. Explicit v1/v2 dispatch must occur before universal loading or scene-contract validation and must reject the new input so historical bytes cannot drift.

## Generalization Qualification Boundary

- Freeze production runtime, audit, assets, current source-only oracle, thresholds, and source hashes before revealing the hidden fixture. Production code must never read hidden prose, fixture metadata, case tokens, or reports.
- Qualify semantic families rather than proposal or candidate IDs. A family signature is derived from slot, prop concept, event frame, and resource footprint; record identities, bridge IDs, and pixel IDs do not define novelty.
- Exercise every hidden contract at the canonical near/middle/far creativity points across the frozen seed set. Require target-band eligibility and diversity, exact replay, creativity-invariant hard gates/resources/cardinality, bounded optional remoteness, clean audits, mandatory mutation rejection, and byte-identical legacy replay.
- A source-only oracle pass, static inventory pass, prompt audit, or helper-module test is not hidden generalization qualification. Do not claim qualification until the separately frozen runner has executed the complete matrix and produced a schema-valid redacted report; even that report does not prove pixel quality, population preference, originality, commercial response, or legal clearance.
