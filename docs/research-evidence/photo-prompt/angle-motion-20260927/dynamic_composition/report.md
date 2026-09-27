# dynamic_composition independent test

엄격 키워드 판정과 전체 고정 장면은 **fail**입니다. 일반 동세·진행 여백·깊이감 4개 관찰 기준은 모두 통과하지만, 생성 전에 고정한 required assertion의 전경 배수 턱 방향과 머리/가방의 결합 동세 근거는 충족하지 않았습니다. 프롬프트와 실제 native 요청 감사는 pass이고 첫 이미지의 저장은 성공했습니다. 사용자 미적 판정은 pending입니다.

- Seed: `13179358549791421548`
- Pack: `86fc1969557e7bec` (v6, semantic, exactly one)
- Run: `d7d1a19f5da1dc78`; positive prompt ID: `adeb2939b13ef902`; exact runtime ID: `b31471476c41e8ed`
- Runtime: native `image_gen.imagegen`, exactly one call, actual `referenced_image_paths` attachment, no fallback/edit/retry
- PNG: 1448 × 1086; SHA-256 `8a0365d80e489f3db0960dcce54bf13c4f892abd3944dff51649dcb726e1779a`
- Core canonical hash: `255446386379127cc73f55b1611173525602689ec827efa1542f7860fe7f8a1b`
- Intent lock hash: `fda02f149b66dc2a1f1029a4934895c66b5e4b803ab65644b3deb5bb39b46ae3`
- Source snapshot: `eaf92164a684128165c15e713dd1a4cbeaa7acab63b65eff45931fbdd3659f99`

The requester supplied no definition of the topic. The diagonal-depth directional-asymmetry interpretation comes from general knowledge. The independent scene draw selected a riverside pedestrian underpass, a bounding push-off past a low drainage threshold, a rolled drawing tube plus rust-red crossbody bag, and late-afternoon side sunlight. These are agent staging, recorded separately from requester text and semantic meaning. The complete immutable requester message remains source_request; the arm uses exact topic/reference/workflow spans. Ten neutral categories were chosen before drafting; pre-core validation passed with no warnings. The original portrait was directly inspected and used only for visible face and hair appearance of an adult fictional character.

| Boundary | Result | Evidence |
| --- | --- | --- |
| Composition audit | pass; quality warn | Zero failures. Five warnings say uncovered pack intents are preserved by literal core prose. |
| Exact native request audit | pass | Unchanged reviewed prompt/negative bytes, intent/embodiment hashes and exact reference SHA are bound. |
| Native delivery and save | success | Concrete returned PNG copied byte-for-byte into this arm. |
| General pre-render test_case topic criteria | 4/4 pass | Two agreeing diagonal vectors, lead room, three depth layers, readable moving actor. |
| Frozen required assertion | 3/5 pass; all-of fail | Foreground ridge vector and combined hair/bag-edge motion fail. Partial is fail. |
| Fixed complex scene | fail | Tube hand and support/lead leg sides reversed; exact face/jacket sun stripe unclear. |
| Embodiment gates | 3/5 pass; all-of fail | support_and_balance and contact_and_space fail; review schema has zero failures. |
| Optional visual gates | none | All visual concepts rejected; approximate retrieval added no hidden hard obligation. |
| User aesthetic judgment | pending | No requesting-user decision received. |

The original 1448×1086 frame and a 512×384 thumbnail were directly viewed. The actor leans toward screen-right, remains left of center and has a clear route ahead. A near ridge, midground actor and receding exit remain readable at both sizes. These broad successes do not replace the frozen phrase requiring pavement seams **and** foreground drainage ridge to flow from lower-left toward the upper-right exit: the foreground ridge instead slopes down-right. Small hair strands trail, but the bag lower edge rests at the hip rather than clearly swinging. The near front-facing body makes the tube hand and rear support read as actor-right, contrary to the frozen actor-left tube/support assignment. The plausible generic stride does not satisfy the specific simultaneous state.

Adopted candidates were `slot:lens:35mm` as a camera transformation, `slot:focus:zone_focus_street` as focus support, and `slot:subject_framing:face_hands_prop_visibility_budget` as a whole-body framing transformation. Their complete constraints were read after the compact view. They helped retain full body, both shoes, entire tube and path. Exposure/adoption reasons are preserved in `candidate_exposure.json`; all sampled creative rows and semantic clarifications have explicit decisions. Optional pose, alternate setting, symmetry, stationary-subject trails, underarm and impossible-world interpretations were rejected because they would alter or distract from the frozen scene.

The active pixel audit is `audit_moe_render_review.py` under embodiment-only `photo-embodiment-preflight/v1`. It returns failed_technical_hard_gates with two failed gates and zero schema failures. The generic repair auditor is inapplicable because this initial core has request_lineage=null and no render_repair contract; this is recorded separately instead of fabricating repair lineage. Ledger delivery status is success and its failure_reason explicitly records failed pixel qualification.

Artifacts: [generated.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/generated.png), [final prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/final_prompt_en.txt), [exact native request](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/render_request.json), [keyword pixels](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/keyword_pixel_results.json), [pixel review](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/pixel_review.json), [pixel audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/pixel_review_audit.json), [manifest v2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/run_manifest.json), [ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/image_runs.ndjson), [core integrity](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/post_render_freeze_integrity.json), [arm summary](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/arm_summary.json).

The first rendered failure remains intact. No other arm or past experiment was read. Main data, indexes, source code and fixtures were not modified. Core, envelope, test_case, pre-core review and feature-selection hashes remain unchanged after generation.
