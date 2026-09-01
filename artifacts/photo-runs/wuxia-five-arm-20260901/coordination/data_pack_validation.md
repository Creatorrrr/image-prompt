# Wuxia data and candidate-pack validation

## Implemented data surface

- Research basis: `docs/research-evidence/photo-prompt/wuxia-20260901/source-research.md` plus 10 approved `wuxia_visual_semantics` evidence rows in `docs/research-evidence/photo-prompt/research_evidence.jsonl`.
- Candidate surface: 39 new wuxia/jianghu candidate records distributed across subject, action, location, prop, composition, motion, lighting, mood, world, costume, and wearable slots; four legacy wuxia/xianxia records were narrowed to remove synonym and cosplay leakage.
- Hard visual surface: six all-of profiles in `photo_prompt_visual_obligations.json`. Five were selected by the seeded qualification; `formal_biwu_reciprocal_salute_standoff` remains the held-out sixth profile.
- Current semantic index: dictionary hash `aefe314da4c1fe7e3243a1c555d7ced10e226c3a6bfdd1cc944a60ea7392d0ae`, 7,278 entries, Gemini embedding-2 at 768 dimensions.
- Current visual-profile index: 144 profiles and 894 exact terms.

## Five bound candidate packs

| Arm | Pack | Hard profile | Hard pixel gates |
|---|---|---|---:|
| rooftop herbal cipher | `596e5bf84da40cad` | `wuxia_rooftop_qinggong_traversal` | 5 |
| bamboo stream duel | `d10f0a998fa91d5c` | `wuxia_bamboo_forest_aerial_duel` | 5 |
| snowbound inn | `2e85c8e8b5dec4ca` | `jianghu_inn_identity_standoff` | 5 |
| market-bridge intervention | `132dce81495a566c` | `xia_protective_intervention_event` | 5 |
| desert biaoju | `19c47c76a2417610` | `biaoju_guarded_cargo_departure` | 5 |

Every pack is `photo-candidate-pack/v6`, uses an independently frozen request envelope and authorial core, binds one request-scoped `photo-visual-intent/v1`, and retains optional BM25F/embedding discoveries as rejected-by-default advisory material rather than hard meaning.

## Validation evidence

- `validate_photo_prompt_dictionary.py`: PASS.
- `build_visual_profile_index.py --check`: PASS, 144 profiles / 894 exact terms.
- `eval_semantic.py --check-index`: PASS, 7,278 entries and current dictionary hash.
- `audit_scene_expression.py --current`: PASS, 112/112 routes.
- `tests.test_photo_authorial_core_v6`: PASS, 18 tests.
- `tests.test_photo_visual_profile_retrieval`: PASS, 12 tests.
- `tests.test_photo_traditional_clothing_semantics`: PASS, 8 tests, including exact/hard-negative routing, optional-only paraphrase retrieval, profile connectivity, and research-ID integrity.
- `tests.test_photo_visual_obligations`: PASS, 23 tests, including request-scoped binding, exact effective gate derivation, render-review failure closure, and ledger preservation.

## Evidence boundary

These results prove structured-data, index, routing, and prompt-contract integrity. They do not prove that any generated image contains the requested relations. Each saved render requires its own thumbnail/native pixel review, and requesting-user preference remains a later, separate judgment.

## Post-generation qualification

- Five independent one-shot generations completed with 5/5 composed-prompt audits and 5/5 runtime-request audits passing.
- Coordinator cross-review agrees with every independent subagent review: 20/25 hard pixel gates passed, but only 2/5 scenes passed all five gates and therefore qualified technically.
- Full gate evidence: `cross_pixel_review.md`.
- Machine-readable summary: `qualification_summary.json`.
