# Arm 2 — heritage/nature operational fantasy

## Outcome

The selected render is a violet-predawn cloud-forest weather observatory scene: an original adult woman storm-keeper, shown full length from a three-quarter rear view with her face naturally visible, threads a luminous liana through a bronze tension ring to recalibrate a living storm compass. The image is the best of two preserved attempts, but it is **not fully pixel-qualified** because three strict semantic hard gates remain failed.

- Seed: `1481082671`
- Concept-selection file SHA-256: `cfae4350ba6f0da756b0bcb20a31ff7f75a6a04691f8abea204bee4be3b922c9`
- Authorial-core file SHA-256: `c2716c41f5f2c5309b8a4df138d44c387bc4e7fcdaa90766a303521568d5ac22`
- Canonical authorial-core SHA-256: `6f7aa246fa16f0673e9a56ecf85711c23c52863b8b9fa83e2162e12c61752980`
- Intent-lock SHA-256: `73049f1b3b33a7ed47e10d372c22f5dee89fc7760b7dc9241297ea33142696bd`
- Candidate pack: v6 `d60b8be07d30c141`, hybrid selection, creativity `0.65`, identity reference-edit mode, inspired likeness mode

The authorial concept and typed v3 core were written before inspecting project candidate-pack implementation. A schema-only normalization changed the intent-lock dimension labels `reference_role` to `appearance` and `body_orientation` to `pose`; it did not change the baseline prompt or meaning. The reference image was not viewed until after prompt and runtime audits, then was viewed before generation as required.

## Candidate/profile evaluation

The first unsteered pack did not surface the held-out target families and instead surfaced two irrelevant visual concepts. It was superseded before composition; the frozen core was unchanged. Post-core evaluation then activated only request-scoped profiles that fit the frozen scene.

| ID | Decision | Reason |
|---|---|---|
| `hogarth_serpentine_line_of_grace` | adopted | The foreground root, turned coat, bronze ring, and luminous liana form a genuine winding depth path. |
| `lateral_waist_hip_contour_transition` | adopted | The full-length rear three-quarter working pose offers a neutral, clothed lateral transition sequence. |
| `hourglass_silhouette_relation` | adopted | Both contours can remain visible as an adult, neutral upper-torso–waist–hip sequence. |
| `posterior_lumbosacral_landmarks` | rejected | The fully closed work coat occludes posterior skin landmarks, so the profile would be forced and untestable. |
| `waist_to_glute_transition` | rejected | Direct posterior body focus would conflict with the operational full-body event. |
| `visual-concept:kuudere_composed_warmth_relation` | rejected | It invents a trusted counterpart and relationship behavior absent from the one-person event. |
| `visual-concept:commercial_appeal_revealing_armor` | rejected | It conflicts with closed expedition clothing and the nonsexual operational scene. |

Chosen ordinary candidate IDs and chosen optional visual-concept IDs are both empty; the three adopted IDs above are request-scoped semantic profiles with strict pixel gates.

## Prompt and audits

- Exact prompt: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260830-body-semantics-independent-3/arm-2-heritage/prompt.txt`
- Exact prompt file SHA-256: `b68688c4362bdc1b027ad16251a35c76567b2af8748eedf771378691c0d3ecdf`
- Composed-prompt audit: **pass**, quality **warn**; 319 words, no failures. Warnings are the advisory concise-word budget and uncovered intents preserved by literal free description.
- Attempt 1 runtime-request audit: **pass**, prompt ID `ae121c077a39691d`, one reference.
- Attempt 2 runtime-request audit: **pass**, prompt ID `f1a16b55eb56ad71`, two references (attempt 1 edit target plus original facial-appearance reference).
- Effective visual-contract SHA-256: `78f529b79f2378491d3095e5ca3cd4bcd4fc650a9dd6041928f43fd3f9ab3c93`

These audits verify prompt/package and reference bytes only; they do not establish pixel quality.

## Render and pixel review

Attempt 1 was preserved at `render_attempt_1.png` (`5e84eea43932575e7eb1ce23b2957e30d6f1c01875bb34f54ba0527901a4f8f6`). It failed the frozen full-length requirement because both feet were cropped, and the belt/coat dominated the body-transition reading. One targeted repair was used.

Attempt 2 is the selected best-available image:

- Image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260830-body-semantics-independent-3/arm-2-heritage/render_attempt_2.png`
- SHA-256: `09c85691f047420937d08a70f84870e71f0a562b6c9c0cc74b995e78736aa2a9`
- Dimensions: `1086x1448`
- Thumbnail/native review: completed at `240x320` and `1086x1448`

Attempt 2 repairs the full-length framing and strongly preserves the frozen scene, original adult subject, closed opaque practical clothing, hand–vine–ring operation, wet botanical material system, rain/fog, and split moss/amber light. Facial appearance is broadly consistent with the reference under a different pose and environmental lighting; this is a non-biometric visual comparison and not an identity, ethnicity, health, or age claim. Requesting-user acceptance remains pending.

All four Hogarth serpentine gates pass. The winding route changes orientation through depth, disappears and reappears through occlusion, and carries coherent wet-material highlights and shadows. The lateral and hourglass sequences are visible, smooth, and neutral, but these strict gates fail:

- `vo_waist_hip_landmark_coherence`: the closed coat prevents direct verification of iliac/trochanteric surface coherence.
- `vo_waist_hip_not_garment_only`: belt and coat tailoring still dominate the apparent relation.
- `vo_hourglass_not_garment_or_ratio_only`: the natural silhouette cannot be separated confidently from belt/coat shaping.

No gross anatomy, mechanism, text, or sexual-content artifact was found. Skin and lighting retain a slightly polished generated-image finish. Because three hard gates fail, this render must not be called fully qualified or representative of complete semantic-profile compliance. No third generation was attempted.

## Preserved evidence

- `candidate_pack.json`, `composed_prompt.json`, `prompt.txt`
- `composed_prompt_audit.json`
- `runtime_request.json`, `runtime_request_audit.json`
- `runtime_request_attempt_2.json`, `runtime_request_attempt_2_audit.json`
- `render_attempt_1.png`, `render_attempt_1_thumb.png`
- `render_attempt_2.png`, `render_attempt_2_thumb.png`
- `repair_decision.json`, `pixel_review.json`
- `provenance.json`, `run_manifest.json`, `image_run_entry.json`

The shared image ledger was not appended. `image_run_entry.json` is the per-arm entry for coordinator merge.
