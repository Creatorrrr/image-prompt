# Arm A qualification report

**Final result: FAIL — 6 of 11 required gates pass; 5 fail.** The first image passed 7 of 11. Both actual native calls returned saved images and have canonical ledger rows. Record validity is PASS; pixel qualification is FAIL. User acceptance remains pending.

Two new native image invocations were made, exhausting the authorized limit of two. No paid/API fallback, moderation block, unknown provider result, native save failure or canonical recorder failure occurred. The tool did not return a model identifier; observed model and image-generation seed remain unknown.

The original reference was the sole image attachment in both actual calls. Its role was visible face/hair guidance. No actual identity, age, biography or body similarity is asserted.

**Final native images and hashes**

| Call | Saved original | SHA-256 | Required result | Ledger run / retry parent |
| --- | --- | --- | --- | --- |
| 1 | [attempt-01.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/images/attempt-01.png) | `8e30f82412b060df6b8c9816ecf02fa2b1f28fbb5358306175d28474bc67ff93` | 7/11 PASS, 4/11 FAIL | `55cce97124752552` / `1b243e865d9b8555` |
| 2 | [attempt-02.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/images/attempt-02.png) | `eed55b0bb4fb8dd9165e18b0eaac413cf136c7eb9295425f3962a6b0266b03a9` | 6/11 PASS, 5/11 FAIL | `b0c42fb47d091853` / `55cce97124752552` |

Both native PNGs are 1237 × 1272 pixels. Copies preserve the actual returned local bytes; crops and thumbnails are analysis derivatives only. Actual second invocation ran from 2026-10-10T04:03:49.159Z to 2026-10-10T04:04:11.978Z. Canonical ledger `ts` records reservation timing; its per-operation `attempt: 1` does not change cumulative arm `image_call_count: 2`.

**Exact hard-gate comparison**

| Required gate | First | Final | Observed scales |
| --- | --- | --- | --- |
| `vo_wkr_wk008_selected_relation_1` | FAIL | FAIL | native |
| `vo_wkr_wk080_selected_relation_1` | PASS | FAIL | native |
| `embodiment_body_ownership` | PASS | PASS | native |
| `embodiment_joint_chain_and_reach` | PASS | PASS | native |
| `embodiment_support_and_balance` | PASS | PASS | native |
| `embodiment_contact_and_space` | FAIL | FAIL | native |
| `embodiment_visibility_and_projection` | FAIL | FAIL | native |
| `rr_buckle_joining_contact_object_class_legible` | PASS | PASS | native, thumbnail |
| `rr_buckle_joining_contact_gross_structure_coherent` | PASS | PASS | native |
| `rr_buckle_joining_contact_intended_interaction_matches` | FAIL | FAIL | native, thumbnail |
| `rr_buckle_joining_contact_contact_anatomy_coherent` | PASS | PASS | native |

All eleven existing duties remain intact: two preserved wardrobe owner relations, five embodiment gates, and four generic buckle repair gates. No obligation was removed, demoted or replaced. The official auditor-derived final shape matches the first exact union. Zero optional ordinary, bundle or visual-concept relations were adopted; their complete candidate meanings were reviewed and declined within closed scope.

**Failed-gate native evidence**

**vo_wkr_wk008_selected_relation_1 — FAIL**

The native original and coat-flank crop show the coat front opening around the knit garment, but the waist/flank side panel meets or overlaps the torso and working forearm. No continuous background strip between a torso-side contour and the hanging side-panel contour can be traced. The open front, dark fold/shadow and free lower hem do not substitute for the required torso-side gap; hidden or partial evidence fails.

**vo_wkr_wk080_selected_relation_1 — FAIL**

The same case shows a left strap clip and right-side metal fitting, and the raised shoulder strap forms a readable arch. In the native original and right_strap_endpoint crop, however, its right return passes behind the man's working hand. The visible D-ring below that grip connects the separate carry handle; the arch's continuation into the exterior right fitting is not unambiguously exposed. Fitting count alone does not prove that both endpoints belong to this same supporting shoulder strap. Complete right-end carrier/attachment ownership remains hidden or partial, so this relation fails.

**embodiment_contact_and_space — FAIL**

The woman plausibly grips the black fastener, but the event-critical planned transition of exposed rigid tips entering an open receiving mouth cannot be located unambiguously. Fork-like exterior features are visible, yet they could be latch features of a joined buckle. Holding the object with coherent hands does not prove the required entering contact state; unresolved native contact is fail.

**embodiment_visibility_and_projection — FAIL**

The original frames both soles, the bench and the bag, but the required torso-side coat gap is closed/obscured, the receiving-mouth/tip-entry state of the buckle remains unresolved, and the right return of the supporting strap is hidden behind the working hand/handle area. The complete planned carrying relations cannot all be assessed from this projection; partial visibility fails.

**rr_buckle_joining_contact_intended_interaction_matches — FAIL**

The receiving mouth and rigid tips crossing into it are not unambiguously exposed in native pixels or whole-scene thumbnail. The clearer fork-like features could be the exterior latch portions of an already joined buckle, rather than an entering tongue. The frozen transitional used relation cannot be confirmed from the visible parts; partial/ambiguous evidence fails rather than being promoted to PASS.

The bag failure is a stricter endpoint-ownership finding from an additional unresampled right-end crop. Two visible metal fittings alone do not establish both ends of the same supporting strap. The carry-handle D-ring cannot silently stand in for an unconfirmed shoulder-strap attachment. This applies the existing same-owner relation; it introduces no global route condition. The final image preserves six of the seven previously passing gates in native pixels, while the full seven remained protected in the prompt and closed lineage.

**Whole-scene and reference fidelity**

A reference-guided seated woman handles a buckle while the standing man steadies the same case and raises its strap. Coat/knit/loafers, bag and grips remain consequential, with supported soles and a coherent cooperative practical task. Complete semantics fail because the coat-side gap and buckle entry are unresolved, and the supporting strap's right attachment ownership is not exposed.

A short dark bob, separated fringe and broadly reference-guided visible facial proportions are present. Downward gaze reduces eye comparison; this is guidance, not actual identity, age, biography or body similarity.

The visible gaze, grips, tensioned arch and bench support connect the people to a practical cooperative task. The exact buckle transition is ambiguous. The whole-image impression is quiet concentration, textured clothing and soft natural light. This is compatible with the frozen supporting sensual 1, fetish 0, surreal 0 and creativity 1 direction, as an agent observation; it does not establish user attraction or preference.

**Source, core, controls and reference bindings**

Skill: `4bff09cfe16ef93183c2130d27143045f02da3114410b61e9b3a0369ea4f2455`. Source generation: `f492f8a428edcf489d7fd9b0c2f2525b2dc7ac1c180446cf20f6eb5af7a19870`. Source fingerprint: `614b5e4fb66959c7304e45bfbb1de601f6cbd892dd908812e2e7492f7ecf843b`. The coordinator announced revision 77 / epoch 219; both actual run receipts were independently checked for the exact generation and fingerprint. Retrieval seed: `7194040714219222582` for both. Original reference: `048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c` at `/tmp/codex-remote-attachments/01a1212e-a00b-7170-8446-16480b2873ff/BAA7D121-91EF-4AF5-A73E-C42EEEE77809/1-사진-1.jpg`.

| Binding | First call | Final call |
| --- | --- | --- |
| Core canonical SHA | `cadb86bf75ba15f55d9c4c0c96297a3aa82638a98c1becf0166615cdbd2ac57c` | `68d17617b4595782e6d3825f4889afc6f546268845fd774bc54f079e360df523` |
| Intent lock SHA | `80ccb05d5efe9704af9ed5862477437dcc35f00f069af4e8ae45297b84f1d16d` | `80ccb05d5efe9704af9ed5862477437dcc35f00f069af4e8ae45297b84f1d16d` |
| Pack ID | `c1dbfe8a54aa5921` | `f210632d827d6cf7` |
| Repair contract SHA | `09720628af3fe76992739520d30095bf8a1490a7fd21c158c1fd15c8e8ded142` | `fdad076a3881fd6e3f9390229699c3c412dbbeddd9b1802ac39ccb9f69337454` |
| Positive prompt SHA | `dc90ae8d62ca0ccce2ae4065880d0ebef2b80916deca33bfc7d9113d48c55e48` | `9d4280599a73b08d163015209bb7af58f22d8343b810546c0b8f25dd3fe399e7` |
| Runtime prompt SHA | `a66954295e7bab2dbcd357b05d69e1957ecc944b935a70692b1209a2a2146615` | `46a27d7840b4aa8816fea37f5a00017efc008f308af02c7ad1c58e62bf47dffc` |
| Pack file SHA | `f380daa7010461ac474efe4dfd6947bc505e38e77f5d5bbe752a53cf3631633d` | `6d1b55f5ff72dbc3bf19602df2f7a3d709a21c980c7591052b55ba551e9f2ee3` |
| Receipt file SHA | `bcca684c8a7cb3f80cced4bff16a7ca6f2ed6f1ebadd7d918237b9c9b0eb3e32` | `6a23a74f6d3d1be67679f5fcf1e786e2e27935b5a58f95f5cf291fe4cc0984fc` |
| Controls file SHA | `384205781564c98610ac01d6367872ceed585232e9ef624d37abce53ab244e56` | `803ae2285027cf19346dd86239c32bff63e2eab9c4bca1a934d4635ed1debb11` |
| Composed file SHA | `b04969a095f23e9c3ac31fe9d363ebdb241180053ccf802555bb11aac1f9ad20` | `d348c01e12704ed45f9ea03f92c5f19f53ec91cf21f666b0bedbbcfb8c8c7702` |
| Render request SHA | `02716992ede07dc97da5aecfde411b5224826070c956ececd73ef57e2cf486a4` | `8347806d093200cf76c6c3e5e2963006521510459c1659a17b93689586ff9f12` |
| Native plan SHA | `25d790f76391036775b77f74b23c6388152d1d221c8de48bb552dbab4dc328ed` | `29eb7cde9870ab41d536afdfff863897a7eb7417b7d393a36a05b6068aa0c4c6` |
| Opaque retry proof SHA | `b04dcbf134e6fa6e970fb40046835ef92eee0502368dfc3cc9c9ba51f7f9bcf4` | `5c48991eb5e47d49cfca04dd00eca2ec2bb4eb18331eb6b457a9b78ca8b794ca` |

Public file byte hashes were verified against canonical bindings. Opaque proof hashes are those recorded by the official attach-retry entrypoint; proof contents were not inspected. Exact paths, core input/normalized file hashes, reference roles, source and pack/receipt bindings are in [public_run_artifact_inventory.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/public_run_artifact_inventory.json) and [result_summary.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/result_summary.json).

**Managed lineage and retained preparation failures**

Historical parent `1b243e865d9b8555` → new call 1 `55cce97124752552` → local repair call 2 `b0c42fb47d091853`. Each valid run had official retry attachment before freeze. The final active run is `run_local_pixel_02_original_bound`; its core, selection, review, controls and retrieval seed were reused byte-identically from the independently frozen local repair solely to recover invalid transport state.

The prematurity/obsolete-source/added-binding preflights (`run`, `run_bound`, `run_recovered`) and the invalid two-reference local preparation (`run_local_pixel_02`) remain preserved. None generated an image. An extra own-result reference and edit header were considered only in preparation: the runtime/body guard first rejected the unreviewed header, and the closed-reference guard then rejected the expanded reference set. Attempting to replace composition in that old run also failed because its invalid render artifact remained bound. The fresh run used the original reference only and passed official composition, runtime, authorization, native-plan and native-started checks before call 2.

No other arm file, prompt, image, scene or substantive gate evidence was accessed or used. A coordinator status-only message containing aggregate counts for two other arms arrived after the local core/composition were frozen and played no role in scene or pixel decisions. All actual image calls used the exact original reference only. No shared skill/code/data files were edited by this arm; no commit or push was performed.

**Actual English prompt — first native call (473 words)**

A complex photographic scene in which several visible relationships unfold together, with a reference-guided main subject seated on a bench beside a case-shaped bag while a man steadies its top handle. The woman's visible face and hair are guided by the attached reference: a short dark bob, airy separated fringe, the same visible facial proportions and features. Her quiet concentration and the soft light across her face give the practical shared task an intimate, everyday presence. She wears the long open herringbone coat over a knit garment with loafers. The long outer garment hangs away from the torso with a visible gap beside its side panel. She sits near the front edge of the bench with her torso upright, knees separate, and both feet resting flat on the floor. Her working arms extend forward of her waist; the camera-facing elbow is forward of her flank. At that flank, the knit-covered torso edge and the hanging coat side panel have separate contours, with a continuous strip of softly lit background visible between them at waist level. The side panel drops from the shoulder and hangs freely beside the torso. The case-shaped bag sits on the same bench within easy reach, its broad front turned toward the camera. The same bag's strap supports its body from two visible attachment fittings. The complete shoulder strap forms a single arch from the left attachment fitting across the top to the right attachment fitting; both fittings and the complete intervening strap are exposed. The man stands beside the case and steadies the separate top handle with one hand. His other hand lifts the strap midpoint into a taut arch, taking part of the bag's weight while its lower edge rests on the bench; both hands are clear of the attachment fittings. The woman guides the rigid mating tongue of the black buckle into its housing while holding both parts. The recognizable black buckle has a hollow rectangular housing and a distinct rigid mating tongue. One hand holds the housing around its side edge, leaving the open mouth exposed; the other pinches the base of the tongue, leaving its projecting forks exposed. The fork tips have just entered the mouth while the remaining length of the tongue is visible between her hands. The buckle lies face-on to the camera ahead of her waist, with a lit separation between each hand and the component held by the other. Capture a front three-quarter view from her exposed-flank side, at seated chest height, framing her from the bob through both soles and including the man, the whole case, its strap arch, and the bench. Soft side light reveals the coat gap and the rigid buckle edges. Moderate depth of field keeps the face, hands, buckle, coat flank and bag fittings readable in the same photograph, with restrained photographic texture and natural perspective.

**Actual English prompt — final native call (578 words)**

A complex photographic scene in which several visible relationships unfold together, with a reference-guided main subject seated on a bench beside a case-shaped bag while a man steadies its top handle. The woman's visible face and hair are guided by the attached reference: a short dark bob, airy separated fringe, the same visible facial proportions and features. Her quiet concentration and the soft light across her face give the practical shared task an intimate, everyday presence. She wears the long open herringbone coat over a knit garment with loafers. The long outer garment hangs away from the torso with a visible gap beside its side panel. She sits near the front edge of the bench with her torso upright, knees separate, and both feet resting flat on the floor. Her torso turns slightly toward the case. Both working elbows are raised in front of her lower chest, and her forearms reach forward toward the buckle in free space above the near side of the case. At the camera-facing waist, the knit-covered torso and the hanging coat side panel have separate contours. The coat panel falls outward from the shoulder behind the lifted sleeve; its inner edge hangs a palm-width away from the torso. A bright tapered strip of background runs between the two contours from the lower ribs to the waist, with the lifted forearm clearly above this open strip. The long panel stays connected to the shoulder and drapes freely beside the seated body. The case-shaped bag sits on the same bench within easy reach, its broad front turned toward the camera. The same bag's strap supports its body from two visible attachment fittings. The complete shoulder strap forms a single arch from the left attachment fitting across the top to the right attachment fitting; both fittings and the complete intervening strap are exposed. The man stands beside the case and steadies the separate top handle with one hand. His other hand lifts the strap midpoint into a taut arch, taking part of the bag's weight while its lower edge rests on the bench; both hands are clear of the attachment fittings. The woman guides the rigid mating tongue of the black buckle into its housing while holding both parts. The recognizable black buckle has a hollow rectangular housing and a distinct rigid mating tongue. One hand grips the outside sidewall of the housing, leaving its receiving mouth exposed. The other hand pinches the rear bar of the mating tongue, leaving its two rigid fork prongs and central guide exposed. In the photograph the housing is to the left of the tongue, with the straight prongs pointing left into the open mouth. Only the fork tips have begun entering; most of the rigid prong length remains exposed in a lit channel between the two main components. The open housing mouth and the projecting tongue can be read together around the finger grips. Both hands present the buckle's broad face toward the camera ahead of her torso, above the waist-level coat gap. Capture a front three-quarter view from the visible-flank side, at seated chest height, framing her from the bob through both soles and including the man, the whole case, its strap arch, and the bench. Soft side light distinguishes the open coat gap and the black rigid buckle edges. Moderate depth of field keeps the face, hands, exposed buckle parts, coat flank and bag fittings readable in the same photograph, with restrained photographic texture and natural perspective.

**Exact common guard-approved negative**

3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls

Both actual runtime strings are the corresponding exact positive prompt followed by `

Avoid: ` and this negative. Full strings are preserved in [runtime_prompt_en_attempt_01.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/runtime_prompt_en_attempt_01.txt) and [runtime_prompt_en_attempt_02.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/runtime_prompt_en_attempt_02.txt).

**Canonical validation and preserved errors**

The final official review-audit admitted `record_valid: true`, `technical_qualification: fail`, with user judgments `pending`. The first valid failure review has the same record/pixel separation. The canonical ledger contains exactly two rows; its `status: success` and the manifest status concern returned image recording, not required pixel success.

[image_runs.ndjson](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/image_runs.ndjson), [run_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/run_manifest.json), [review_audit_attempt_02_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/review_audit_attempt_02_diagnostic.json), [qualification_attempt_02.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/qualification_attempt_02.json).

All preserved errors are preflight or auxiliary errors; none is a native image-provider error. Exact official argv, exit codes and stderr remain in their diagnostic files. Metadata helper exceptions and their recovered actual shapes remain recorded as well.

| Preserved artifact | SHA-256 | Meaning |
| --- | --- | --- |
| [preflight_error_history.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/preflight_error_history.json) | `498d547cb0edaf47c4a50004f7c62ff8f2525a0a41c5b8fdd7f5b82f2c73066e` | initial request-span and controls-path preparation errors |
| [attach_retry_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/attach_retry_diagnostic.json) | `2c5179524420aa6c1073cd53c7f7ff72c1efce2005c6ccd841317c3c7f8a6702` | premature frozen preflight run could not attach retry |
| [corrected_view_error.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/corrected_view_error.json) | `b9a1ad0b75c667535c748e7f563cd50b3de2a1608d064506bdbbe8d16fecd602` | new child-only visual bindings changed inherited effective obligation |
| [postreturn_inspection_errors.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/postreturn_inspection_errors.json) | `8794433859d9535ad744ad156ea6ff18b5641ad4396e6bc002dd2bffa7c99008` | post-return PIL import and not-yet-created inspection copy errors; recovered without new image call |
| [supplemental_local_errors.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/supplemental_local_errors.json) | `5487b20659c9c2ab3073ddbc851ab425ec9db0a81d7f3065c352bf9a52de8e1a` | neutral catalog path and own pack list-wrapper inspection errors |
| [review_audit_attempt_01_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/review_audit_attempt_01_diagnostic.json) | `312874ff01ae0f92b9db55065a7e212bc4fbe8022e01911780120291b121b68f` | invalid initial unreceived-user judgment enum wire |
| [visual_review_attempt_01_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/visual_review_attempt_01_diagnostic.json) | `cd39261fb969136595b001264b25e7890ee151c75fffe413d4361c8248dc645f` | exact schema failures for null judgment values |
| [retry_prepare_local_pixel_02_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/retry_prepare_local_pixel_02_diagnostic.json) | `26d88412161e402250241a8e826a3c57b6fd285c69d84a874009f4e423ecd212` | decision source text did not fit active request evidence |
| [local_input_writer_syntax_error.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/local_input_writer_syntax_error.json) | `46e4875172bfe38bb40118101af6105d2b08fdff0d9be764a387957f1977e4d6` | local input-writer apostrophe syntax error before writes |
| [deferred_view_inspection_error.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/deferred_view_inspection_error.json) | `653b8024e7e20727b979ecf14053fdaf6ed98add5576ab3c43e8dbbdbe0cbb59` | deferred candidate ID wrapper was treated as row objects |
| [prepare_render_local_pixel_02_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/prepare_render_local_pixel_02_diagnostic.json) | `8eea73f2dc7af07111dac190f27b214b9846e0afc49128df2d71cb21e231c8dc` | runtime body review rejected extra edit-direction prefix; exit zero with nested runtime fail |
| [native_plan_local_pixel_02_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/native_plan_local_pixel_02_diagnostic.json) | `2942949762232c6bfecb3ffb398ff7640ffd8e331fc574fb6c3b693b085be549` | official native plan rejected failed runtime preparation before any reservation or image call |
| [native_plan_local_pixel_02_final_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/native_plan_local_pixel_02_final_diagnostic.json) | `f0334a5f6fcacfc808235378995cb8727cec3e9d09c410395e79a48cda61f1a6` | Official native plan rejected expanded reference set before reservation; exact preserved set remains original reference only. |
| [compose_audit_local_pixel_02_original_reference_diagnostic.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/compose_audit_local_pixel_02_original_reference_diagnostic.json) | `2f80bd5765811b8f6f3ab0bcc91d6830fb06a985b31fefbf0c55783de3a94212` | Original-only composition could not replace a workflow already holding the invalid two-reference render artifact; fresh managed recovery retains exact closed obligations. |
| [controls_status_interpretation_local_pixel_02_original_bound.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/controls_status_interpretation_local_pixel_02_original_bound.json) | `0a2a4f1cd4ccd0b72772b689d6fe57dca803f6ef3fb48d7cb457731778815ab9` | Conservative wrapper incorrectly expected a controls hash in compact response; unchanged saved controls verified and workflow continued with no image call. |
| [recovery_pack_wrapper_error.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/recovery_pack_wrapper_error.json) | `ef5fc5f59b7b09588441501fea67119be74d9eb745665a206e98ef02543e4ac5` | two own metadata-shape inspection errors after successful official retrieval; recovered with actual shape |
| [recovery_pack_wrapper_errors_exact_tracebacks.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/recovery_pack_wrapper_errors_exact_tracebacks.json) | `fa7772764e2feccc345d72293814709bd2b26183a43f43afa002ce5b54f8923b` | Exact returned helper metadata inspection tracebacks, supplemental to the preserved recovery error descriptions |
| [ledger_metadata_key_error.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010/arms/a/ledger_metadata_key_error.json) | `0646e36bb7225c084f5d02a5f62751224c872330fd0f36c2da76bd44095fc9d5` | Canonical native rows store image hashes in image_hashes array, not a scalar image_sha256. |

The native call budget is exhausted. The final required-condition result remains FAIL, and user acceptance remains pending.
