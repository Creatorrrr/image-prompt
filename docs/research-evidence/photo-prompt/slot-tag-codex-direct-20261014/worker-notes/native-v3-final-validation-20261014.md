# Native v3 implementation and final validation handoff — 2026-10-14

Production implementation is frozen for root integration. No canonical source, catalog, bindings, registration, index manifest, R/CURRENT, runtime publication, Git mutation, network, Gemini or model/embedding inference was performed by this worker. Temporary synthetic search/layout/runtime fixtures used by unit suites are isolated from production.

## Before and after

V2 required every displayed role fact property to be an actual mutation and used role facts as its carrier inventory. This could invent an age mutation from an adult declaration and omit pre-existing carrier obligations for effects outside displayed roles. Historical broad owner/category/keyword allowances cannot prove the existence of a face, hair, nails, prop identity or frozen focus.

V3 separates a manually reviewed whole per-actual-RID fact inventory into effect/prerequisite/preservation/context, binds actual complete local effect sets independently of roles, and retains every selected dependency's obligations. Canonical mutations still need effect-mode coverage; mode relabeling cannot hide a locked change. No automated semantic conversion or carrier/default-empty-array generation was introduced. Test fixture serialization helpers calculate only fixture hashes/path/reference sets around explicitly authored facts, and must never be repurposed to qualify the corpus.

Source owner maps use owner-bindings/v2: explicit source target → stable common core_role → independently authored request actual owner. Existing owner facts are exact typed values with active requester spans, frozen baseline evidence and either whole locks or the limited exact-owner/property-anchor exception. Equivalence, part containment and explicit disjointness remain distinct. Unknown overlap with protected properties denies; different spellings or a human/object category do not create anatomy or aliases.

Full source qualification, sealed compact guard admission, source/materialized/lazy consumers and final composed audit now share the actual scope. Parent own/joint effects remain independent of explicitly selected optional children; child alternatives never become a sibling union. Temporary explicitly named old presentation conditions remain ANDed and fully hash-bound; no binding-only native identity fallback exists. Their final phase6/8 removal requires manual condition migration, as described in the supplement.

Absent proof remains explicitly unqualified only to preserve existing discovery recall. Present old/null/empty/false proof is invalid. The final composed audit requires full native v3 source/admission/actual CID-RID dependency scope for ordinary chosen cues, visual concepts and transformed augmentations. Search eligibility does not authorize native adoption. Root's canonical source stage still has zero qualified records; these tests do not change that count.

## Authored fixture changes and proof boundary

Primitive fixtures explicitly model existing adulthood plus wardrobe mutation; existing face plus lighting; frozen focus preservation; context without mutation; exact existing wig hair without invented nails; object with a separately declared depiction face; same-owner protected properties; distinct grounded secondary actors; and different facts/effects on actual OR RIDs. These are new synthetic sources, not automatic translations of prior review judgements.

Compound fixtures preserve actual old-style positive member concept_units/relations separately from child bodies and intrinsic/role guards; bind manually reviewed fact modes to actual child CID/RIDs; reject missing new mutation footprints; require selected-only literal render evidence; and explicitly distinguish required and optional members, candidate identity from presentation roles, parent joint effects from selected child effects, conditional child actual RIDs, complete binding-only reference closure, source/reference/proof tampering and source-unit coverage. Full/compact and materialized/lazy public contracts agree. A real candidate-free freeze → synthetic layout/search → native pack → selected primitive full composed audit passes. A candidate-only optional bundle also passes that complete path with its child unselected; selecting its ungrounded face child fails final adoption.

The multiowner fixture independently appends two named people with declared faces/hands/jackets/mugs to a blanket request and baseline, preserving eleven owner nodes and more than sixteen assertions through actual freeze, independent audit and replay. The partial-lock fixture independently changes the synthetic request from blanket to white linen robe, updates its authored subject feature, adds only a white wardrobe.color anchor while keeping appearance open, and proves round neckline permission and color-change rejection on all three consumers. Missing anchor/wrong owner/broader fact/advisory/part-only support fail; exact neutral-role/equivalence succeeds. These fixture-only before/after changes make no claim about canonical sources or rendered pixels.

## Final validation

The exact offline command below completed successfully: **196 test executions, 166 unique test IDs, 358 subtests, 0 failures, 0 errors**, 19.487 seconds. Some older suites import another TestCase, so imported cases execute more than once; the unique count is provided explicitly. Environment `env -i` removed provider keys, and sandbox-exec denied network*. No provider or inference invocation was part of these tests. AST parsing passed for the worker production/test paths and path-scoped git diff --check passed. The superseding primitive JSON fixture also validates against the final code.

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYTEST'
import unittest
names='''test_photo_semantic_evidence test_photo_native_fact_wire test_photo_native_compound_evidence test_photo_native_adoption test_photo_candidate_corpus test_photo_candidate_realizations test_photo_realization_content test_photo_slot_semantics test_photo_slot_workflow test_photo_native_runtime_freshness test_photo_workflow_precore test_photo_global_retrieval test_photo_search_layout test_photo_slot_queries test_photo_slot_retrieval test_photo_global_retrieval_audit test_photo_native_wardrobe_owners'''.split()
class Counted(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.identities=set();self.subtests=0
    def startTest(self,test):self.identities.add(test.id());super().startTest(test)
    def addSubTest(self,test,subtest,err):self.subtests+=1;super().addSubTest(test,subtest,err)
result=unittest.TextTestRunner(verbosity=1,resultclass=Counted).run(unittest.defaultTestLoader.loadTestsFromNames(['tests.'+name for name in names]))
print('FINAL_COUNTS executions=%d unique_test_ids=%d subtests=%d failures=%d errors=%d'%(result.testsRun,len(result.identities),result.subtests,len(result.failures),len(result.errors)))
raise SystemExit(not result.wasSuccessful())
PYTEST
```

## Changed/new worker files

- `skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py`
- `skills/photo-prompt-image-generator/precore/photo_authoring_wire.py`
- `skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py`
- `skills/photo-prompt-image-generator/scripts/photo_candidate_corpus.py`
- `skills/photo-prompt-image-generator/scripts/photo_candidate_realizations.py`
- `skills/photo-prompt-image-generator/scripts/photo_slot_semantics.py`
- `skills/photo-prompt-image-generator/scripts/photo_role_proposals.py`
- `skills/photo-prompt-image-generator/scripts/photo_search_layout.py`
- `skills/photo-prompt-image-generator/scripts/photo_search_reader.py`
- `skills/photo-prompt-image-generator/scripts/photo_shared_views.py`
- `skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py`
- `skills/photo-prompt-image-generator/scripts/photo_contracts.py`
- `skills/photo-prompt-image-generator/scripts/prompt_generator.py`
- `skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py`
- `tests/test_photo_semantic_evidence.py`
- `tests/test_photo_slot_semantics.py`
- `tests/test_photo_native_fact_wire.py`
- `tests/test_photo_native_compound_evidence.py`
- `tests/test_photo_native_adoption.py`

Worker notes/examples (historical guides preserved):

- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-fact-mode-design-20261014.md`
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-v3-authoring-guide-20261014.md`
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-v3-primitive-fixture-20261014.json`
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-v3-authoring-guide-20261014_v2.md`
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-v3-primitive-fixture-20261014_v2.json`
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-v3-compound-and-partial-lock-contract-20261014.md`

- This validation note and `native-v3-handoff-hashes-20261014.json`.

`photo_candidate_realizations.py` retains the separately authored relationship-mechanism explicit-projection extension from root's projection worker; this worker subsequently added only the native member-selection/condition integration. Its `tests/test_photo_realization_content.py` is a tested integration dependency, not edited here. Root owns SKILL.md, precore/photo_semantic_witnesses.md and references/photo-workflow.md; their current native authoring guidance was reviewed and matches the implementation.

## Remaining root gates

Root must independently review/tests this frozen patch, verify actual original native review artifacts/provenance and manual source/spec/dependency judgements, apply approved source corrections separately, rebuild metadata/guards with exact same-space vector reuse, verify source/index/guard closure, publish and perform actual acquire, and commit reviewed paths. This worker did none of those production actions. Full corpus qualification, condition migration/old-binding-path removal and final absent-search-only accommodation removal remain later completion gates. No fixture/mechanical result establishes corpus semantic truth, artistic quality, image pixels or completion of the full migration.
