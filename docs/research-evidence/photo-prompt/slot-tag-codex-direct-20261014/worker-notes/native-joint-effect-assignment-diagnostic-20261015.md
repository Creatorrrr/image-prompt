# Native joint effect assignment diagnostic — read-only, 2026-10-15

Two engine gaps are independently reproduced. Production, tests, accepted source/proofs, catalog, operating index/runtime, CURRENT and Git were not modified. No model, provider, network, embedding inference or image rendering was called. All search vectors in temporary fixture layouts are explicit constants. This is diagnostic evidence, not a native approval or a claim about source/image quality.

## Evidence and source reading

I directly read the full ordinal 9 and 17 BATCH rows: original/source-after, top deltas, complete facts/units/maps/roles/signature/provenance/conditions and rationale. The other 18 rows were inventoried by ordinal/CID/status, not claimed as whole semantic rereads. The two actual source bodies are “a 50mm standard lens” / “50mm 표준 렌즈” and “a 24mm wide-angle lens” / “24mm 광각 렌즈”. Their exact E tuples are camera/lens.focal_length_mm/v1 value strings 50 versus 24 and lens.named_class/v1 standard versus wide_angle, set_value, empty receivers. Both map source-local camera to recording_camera. Individual meaning validity is preserved; no input proof is altered or attached to a fixture/operating corpus.

The reproducer checks these actual rows' meaning SHA, native-contract signature SHA and exact positive quote substrings. It does not rerun research acceptance/verify_batch or claim these checks establish semantic truth. Their source-after/proof SHA and exact E/maps are in the JSON. BATCH raw SHA: `26ad6216c781ae3cf24ea8a71997fcf6f1a098c70ed9b6c19749ee79bc1fef9b`.

Read production paths: photo_semantic_evidence admission, _selected_contract, owner_resolution, _collect_permission_scope, property_scope_allowed, source guard evaluator; audit_composed_prompt audit_native_adoptions and outer fresh audit; audit_image_render_request fresh owner-resolution gate; photo_candidate_realizations eligible_ids; prompt_generator frozen_core_context/prepare/generate_candidate_pack; photo_workflow prepare_render transport shape. Actual line references apply to the pinned hashes below.

## Finding 1: cross-CID assignments are not compared

`photo_semantic_evidence.py:920` creates a fresh assignments dict in each owner_resolution invocation, so its actual-canonical-owner E check ends at one proof/RID. `_collect_permission_scope` at :937 recursively resolves selected dependencies but retains only dimension/actual target/property addresses, including receiver lock addresses. It discards typed value, operation, receiver set and source provenance before merging. `audit_native_adoptions` at :5881 processes each chosen CID separately. Its owner-resolution uniqueness check uses (CID,RID), not an effect-assignment key shared across chosen sources. It does not restore discarded E values.

### Direct full/compact execution

R02 contains 20 manually authored isolated camera cases: independent selected P/B and parent P + required B closure, each with ten variants and full/compact consumers. P/B are fixture CIDs; actual root lens proofs are not reused. Each source validates with c.validate, complete fixture source units and exact signed facts. Every effect quote occurs in its explicit positive source body. The camera graph independently declares camera_A/camera_B disjoint, camera_alias equivalent to camera_A, scene_A/scene_alias equivalent, and exact frozen presence; no part_of equivalence or candidate-driven core enrichment is used.

| Variant | Current admission/permission_scope | Current eligibility |
|---|---|---|
| Same actual camera, 50 vs 24 E | accepts both/whole closure | true |
| Explicit equivalent owner alias, 50 vs 24 E | accepts both/whole closure | true |
| Same target/property/value, conflicting typed value type | accepts | true |
| Same target/property/value/type, conflicting operation | accepts | true |
| Same assignment except differing actual receiver SET | accepts | true |
| Identical assignment | accepts | true |
| Explicit disjoint actual cameras with different values | accepts | true |
| Different properties on same camera | accepts | true |
| Identical receiver SET after explicit receiver alias resolution | accepts | true |
| P old 50, E new 24 (other CID E uses a distinct property) | accepts, no P-vs-E comparison | focal-length mutation correctly rejected by independent frozen property lock |

For the P-old case, the frozen camera prior fact is protected by the exact partial property anchor; it is not an authorization to mutate it. R02's distinct left E property avoids conflating this P exclusion test with a separate competing 50 E. R01 retained the earlier mixed-E version and must not be used to assert isolated P exclusion.

There are 40 full/compact case-view groups, containing 60 admission, 60 permission_scope and 60 eligibility calls (independent cases have two entries). The direct cases also attempted final_native_adoptions with a deliberately minimal diagnostic envelope; those return missing-context / compact-source-validation failures. **Those failures are not evidence that final value-conflict detection exists.** They are preserved verbatim, not counted as meaningful final success/failure controls. Final/runtime evidence comes from the complete frozen public pack below.

A one-CID control has two distinct source-local camera targets that both resolve to camera_A, with 50 vs24. Full and compact admission reject it, and permission_scope raises `conflicting actual-owner effect assignment`. Thus the existing within-CID checker operates correctly; the missing boundary is joint selected sources.

### Complete public pack → composition → runtime request

The independent fixture uses the existing frozen_owner_run authoring/freezing path with independently declared secondary leather coat and background leather bench. The source helper's cracked texture fixture is directly read. The B variant is manually changed only from cracked to smooth in its positive effect clause, effect quote and typed value; presence/leather P, origin/selector, operation, receivers and whole scope stay explicit. Native fixture source-unit hashes/signature are freshly serialized with seal; these are artificial fixture signatures, not human-source approval provenance. Existing helper correction metadata bound to original 1272 is isolated fixture provenance; it does not alter or approve actual 1272.

A temporary SearchReader/LazyRuntimeData layout is built with constant vectors; the immutable public pack is generated by the actual engine. Composer input explicitly selects P and B onto the same coat_surface and spells both cracked and smooth surface assignments. It carries exact owner_selections; no auditor output is supplied as input. The full audit_composed_prompt returns **status=pass, failures=[]** and emits a resolution receipt. The pack's canonical bytes remain unchanged.

Using the exact workflow prepare_render transport shape (schema v2, pack/core lock/retrieval/embodiment pins, exact prompt plus Avoid suffix, negative, references=[], explicit audit_boundary, composed/resolution hashes), `audit_image_render_request` then returns **status=pass, failures=[]**. Its fresh owner-resolution branch reexecutes the whole composed audit against the same bound lazy fixture source. This is actual runtime-request audit acceptance of an unresolved semantic conflict; it is not a provider call or operating runtime acquisition.

The authoritative R02 JSON stores the entire actual pack, composed input, emitted audit/receipt, exact request and render audit. This proves the specific independent-CID same-owner texture conflict through those consumers. It does not claim every alias/type/operation/receiver variant was exercised through a complete public pack/runtime request; those are directly verified at admission/permission/eligibility only. The actual 50/24 root proofs were never modified or adopted in this diagnostic.

## Finding 2: required qualified child crashes lazy discovery before pack completion

A second manually authored fixture adds `member_candidates: [{candidate_id:B, adoption:required, requirements:{}}]` to parent P and a matching complete required dependency declaration pinned to child meaning/proof/RID. Child is still the independently valid smooth texture fixture. Source c.validate succeeds. No optional member defaults or source conditions are copied/deleted.

During actual public-pack generation:

1. photo_global_retrieval.eligible uses `reader.meta['guards']`.
2. photo_candidate_realizations.eligible_ids :208 calls `native.compact(data['candidates'][child_id], data)` on an already compact qualified child.
3. photo_semantic_evidence.compact :572 only reads content.role_evidence; that field was deliberately removed from the compact guard, so it returns None.
4. eligible_ids :210 passes None to dependency_choices; _dependency_guards :760 indexes proof['dependencies'] and raises **TypeError: 'NoneType' object is not subscriptable**.

R02 stores the exact complete exception trace. Required-child public-pack final/runtime audits are **not reached**; no success claim applies to them. Direct full/compact parent+required-child admission and permission collection above are separately exercised and do reach the cross-CID gap.

This does not contradict root's separate reported operating build/acquire scope: existing139 catalog/18250 source/18180 reused vectors with canonical native-qualified0. I did not acquire or independently verify that operating generation and do not call it fully qualified compound lazy-search coverage.

## Minimal future correction proposal — not implemented/authorized here

1. Add a shared nonrecursive selected-effect-assignment collector in photo_semantic_evidence. Read only actual E facts from the exact selected CID/RID/dependency closure; preserve every provenance row. Resolve using the same core/graph/proof/mapping pins and existing introduced-origin rules. Key by (dimension, actual canonical target, property); compare exact typed value, operation and canonical actual receiver SET. Equivalence only uses explicit graph equivalence; part_of remains distinct. Receivers remain lock endpoints, not independent value assignments.
2. Apply this comparison to a selected parent's own/required/actually chosen optional closure before admission/permission succeeds, and to the union of all independently chosen final-adoption roots. Deduplicate a shared child by exact CID/RID/proof identity without discarding contradictory alternate selection contexts. Identical assignments can coexist with their provenance. P/context/preservation are excluded from this E-only value comparison; existing locks and final preservation remain independently strict. No property aliases, merge operators, synonyms, automatic winners or typed-value coercions.
3. Keep discovery search_only where mappings/RIDs remain unresolved. Do not mutate/reissue immutable packs or treat search results as adopted effects. Final audit must compute and compare the whole actual selected union before emitting resolution. Existing runtime fresh audit then consumes the same rejection; outer receipt/API schemas need no unrelated change.
4. For the lazy child, use the already sealed/validated compact proof via proof_of on a compact child, or full-source compact projection only for an actual full source. Avoid passing None and avoid treating arbitrary unvalidated dictionaries as sealed guards. Minimal likely production location is the qualified-child projection in photo_candidate_realizations.eligible_ids; shared helper expansion only if other exact observed paths need it.
5. Required regression: same/alias conflicting values, type, operation, receiver SET; identical/alias receiver SET; disjoint owners; distinct properties; P old/E new; parent/required and explicitly selected optional child, unselected optional nonobligation, reused shared child, branch RID and unused selections; same-CID checker unchanged; part_of not equivalence; introduced synthetic origin boundaries; receiver locks and scope-preservation nonrecursion. Repeat full/compact/direct lazy/public pack/final/runtime consumers and inject changed source/proof/graph/selection after audit. Add a positive qualified required-child lazy-discovery fixture with matching child closure, plus corrupt/absent guard negatives. Actual source corrections/approval and operating publish/acquire stay separate root work.

## Commands and execution accounting

All three diagnostic process attempts used env-i with only HOME, PATH and PYTHONDONTWRITEBYTECODE plus sandbox-exec deny network*. First attempt aborted with the required-child TypeError before creating output. R01 then captured that error but deliberately incomplete transport failed unrelated request checks. R02 uses exact transport and preserves R01 rather than rewriting it. R02 is the authoritative completion result. These are diagnostic executions, not a unittest suite: **0 unittest/subtest pass counts are claimed**. R02 covers 20 direct scenario definitions / 40 view groups +2 within-CID rejection controls +2 public-pack attempts (one complete audit/runtime acceptance, one crash). No cases skipped silently.

```sh
env -i HOME="$HOME" PATH="/opt/homebrew/bin:/usr/bin:/bin" PYTHONDONTWRITEBYTECODE=1 /usr/bin/sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/authored/native_joint_effect_assignment_repro_20261015.py --output docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-effect-assignment-diagnostic-20261015-r02.json
```

The output argument is create-once; use a new explicitly chosen research path for independent replay. Frozen code and BATCH before/after hashes are identical and embedded in R02. The current research script is final revision; the original R01 was produced by an earlier development revision, retained as execution history, not falsely labelled a byte-identical replay of this final script.

## Frozen artifacts

- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/authored/native_joint_effect_assignment_repro_20261015.py` — 17768 bytes, raw SHA256 `394604d353244ce3cf06cb84e26eb6cebeb84595d2532d88fedbcaf14d4d0168`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-effect-assignment-diagnostic-20261015.json` — 874538 bytes, raw SHA256 `019e9ef2911ddfe59a366c8d97d9352b874c2ff95679b303fa0bcc13bc27bae6`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/worker-notes/native-joint-effect-assignment-diagnostic-20261015-r02.json` — 893605 bytes, raw SHA256 `6a8258b04709a4867b823c7645305ad84ea6da8be2aedb9538f673c03e451f47`.

Production/test/input pins before=after:

- `skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py` — `e85f8a92c262a1a2b8f24f15255a33332bcd287dff9702b8fadc69d0fa8cfa58`.
- `skills/photo-prompt-image-generator/scripts/photo_candidate_corpus.py` — `b00b200643fe672ba4fc84e162333d937b0ee83ddb0ab431b1a67169cda52da4`.
- `skills/photo-prompt-image-generator/scripts/photo_shared_views.py` — `561823b22b7bfc9ccdc5a8a6b4f778d471d37b1deb8eddbd0d56e7cff2168733`.
- `skills/photo-prompt-image-generator/scripts/photo_candidate_realizations.py` — `c6e4388a1c13cdb7f53df8a81c98a9fd75e665efcd648cc90126e7053698657a`.
- `skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py` — `0a2a1fa6cec5d0e79a0a8d272eb81dc7853bc0c96ac87ce853c540feeb064215`.
- `skills/photo-prompt-image-generator/scripts/photo_search_layout.py` — `f7760546dd1374e90af57e0f5d286ed7bb1c7be45960ad1524454c79d869c69f`.
- `skills/photo-prompt-image-generator/scripts/prompt_generator.py` — `cfbdc7d66f0d065fedc111d8bac9a47b13a7c891e59c95261ed4f170b1f9671a`.
- `skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py` — `9f797eb72b98f624c8e891a00b9aaa02f8d54d9d42574bb78ced79ec3b161cb6`.
- `skills/photo-prompt-image-generator/scripts/audit_image_render_request.py` — `b52d70becb9dbdeade3d0aeda72dfe7610a1303ba259837eae7c89c17999d154`.
- `tests/test_photo_native_source_guards_v2.py` — `2748f9110b239ed9e59ac544ec235268a940e159a168cb68a683a0a4b4faa7fd`.
- `docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/root-00000-00020-01/BATCH-WIRE-02.json` — `26ad6216c781ae3cf24ea8a71997fcf6f1a098c70ed9b6c19749ee79bc1fef9b`.
