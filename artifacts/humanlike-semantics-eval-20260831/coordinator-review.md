# Humanlike visual-semantics five-arm evaluation

Date: 2026-08-31  
Baseline revision: `9e7cbbb418c268ce4c4e0cdd7d3c08b7bd2c318f`  
Reference image SHA-256: `e3e010b75a48da02f914d7e8202690b3353450a78832daaefea0bbbc234aa5b3`

The supplied portrait was used only as facial-appearance inspiration. This evaluation makes no biometric match, identity, or same-person claim.

## Evaluation contract

- Five independent subagents used five distinct frozen authorial cores and arm-local candidate packs.
- Each arm called the built-in image generator exactly once and recorded `cross_arm_inputs_used=false`.
- Prompt audit and the exact runtime-request audit had to pass before generation.
- Pixels were inspected at native resolution and thumbnail scale.
- Every profile owned five hard gates. A partial or ambiguous gate counted as fail; prompt wording alone was not pixel evidence.
- Requesting-user judgment remains pending and is separate from technical qualification.

## Results

| Arm | Random complex concept | Profile / pack | Prompt + runtime | Pixel gates | Technical result | Image |
|---|---|---|---|---:|---|---|
| Clone | Flooded botanical genetics archive at blue hour | `biological_human_clone_provenance` / `2f2952ee9d73dba6` | PASS / PASS | 3/5 | FAIL: source-to-copy direction and ordinary-twin substitute remain ambiguous | [generated_clone.png](clone/generated_clone.png) |
| Chimera | Storm-lit mobile genomics clinic in an alpine seed vault | `human_cellular_chimera_lineage` / `2621d1aa9044ee83` | PASS / PASS | 5/5 | PASS | [generated.png](chimera/generated.png) |
| Anthrobot | Midnight orbital wet lab with a live microscopy experiment | `anthrobot_microscopic_ciliated_biobot` / `0a02eb4ec139298e` | PASS / PASS | 5/5 | PASS | [anthrobot-render.png](anthrobot/anthrobot-render.png) |
| Human digital twin | Coastal storm-surge command room | `human_digital_twin_bidirectional_sync` / `c88c11cc31c8ee56` | PASS / PASS | 5/5 | PASS | [generated.png](digital-twin/generated.png) |
| Biohybrid robot | Moonlit tidal greenhouse | `biohybrid_robot_living_synthetic_integration` / `8acac34a9fc365ed` | PASS / PASS | 4/5 | FAIL: tissue–electrode contact, force path, and contraction-driven fin deformation are not unambiguous | [biohybrid-tidal-greenhouse.png](biohybrid/biohybrid-tidal-greenhouse.png) |

Aggregate: 5/5 prompt audits passed, 5/5 runtime audits passed, 22/25 pixel gates passed, and 3/5 arms achieved technical pixel qualification.

## Coordinator pixel cross-check

- Clone: the continuous scene, two organic adults, `LINEAGE VERIFICATION`, paired DNA displays, 99.86% genomic match, and bioreactor records are visible. The panel does not make an original-to-clone direction readable at thumbnail scale, so related test subjects or twins remain a plausible substitute.
- Chimera: the physical adult has ordinary coherent anatomy, while separate green and magenta lineage networks are integrated across the same projected organs in an explicit genomics workflow. No fantasy animal-part patchwork is present.
- Anthrobot: a physical microfluidic chamber, microscope, magnified monitor, 100 µm scale, irregular living spheroids, dense surface cilia, and dotted motility paths are all visible. The experimental subjects are neither humanoid nor metallic.
- Human digital twin: a solid physical referent and a corresponding translucent model are distinct. A blue live biosensor stream travels outward, while a separate orange predictive return path updates evacuation routing on the physical decision surface.
- Biohybrid robot: living pink tissue, a transparent synthetic shell, ribs, connectors, and an independent manta-shaped robot body are visible. Co-location is strong, but a functional force-transmission interface is not visually proven.

## Implementation and evidence

- Visual profiles: `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`
- Exact-tag collision correction: `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`
- Derived indexes: `photo_prompt_visual_profile_index.json` and `photo_prompt_semantic_index.json`
- Routing cases: `tests/fixtures/photo_prompt/visual_obligation_routing_v1.jsonl`
- Five-arm pixel cases: `tests/fixtures/photo_prompt/humanlike_semantics_five_arm_cases_v1.jsonl`
- Behavior tests: `tests/test_photo_humanlike_semantics.py`
- Source abstractions and observability boundaries: `docs/research-evidence/photo-prompt/humanlike-entities-20260831/source-research.md`

Arm-local prompts, request audits, native images, thumbnails, pixel reviews, manifests, and append-only ledgers are preserved in each arm directory.

## Verification

- `tests.test_photo_humanlike_semantics`: 4 tests PASS.
- `tests.test_photo_visual_obligations`: 23 tests PASS.
- `tests.test_photo_visual_profile_retrieval`: 12 tests PASS.
- `tests.test_photo_bm25f_retrieval`: 5 tests PASS.
- `tests.test_photo_authorial_core_v5`: 9 tests PASS.
- `tests.test_photo_authorial_core_v6`: 18 tests PASS.
- `tests.test_photo_prepack_isolation_v5`: 6 tests PASS.
- Visual-profile index check: 97 profiles and 568 exact terms, PASS.
- Dictionary metadata, scene-expression audit, iteration-record schema, and `git diff --check`: PASS.
- Full discovery: 782 tests in 2790.140 seconds, ending with 10 failures and 3 errors. Every failing name reproduced on a clean archive of the starting revision: seven stale golden snapshot cases, one pre-existing research `reuse_note` contract failure, one pre-existing fixed semantic-row-count failure, and one pre-existing frozen photo-baseline failure plus its three dependent validator errors. No new full-suite failing name was introduced by this change.
