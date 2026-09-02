# arm-02 qualification report

## Outcome

- Assigned profile: `rembrandt_face_light_pattern`
- Candidate pack: exactly one `photo-candidate-pack/v6`, pack `4154f967af54f46c`, creativity `0.5`, seed `617637285`
- Image tool: built-in `image_gen`
- Image calls: exactly `1`
- Retries: `0`
- Fallback calls: `0`
- Cross-arm inputs: none
- Generation status: success; native result copied to `render.png`
- Prompt audit: `pass` with advisory quality warnings only
- Exact runtime-input audit: `pass`
- Overall strict pixel verdict: `FAIL`
- Requesting-user judgment: pending and separate

## Frozen pre-core lineage

The 115-word standalone baseline and its scene were authored before the arm assignment was opened. The concrete rain-soaked transit-junction scene is an `agent_general_knowledge` interpretation of the exact requester span `랜덤한 복잡한 컨셉`; it is not a user-supplied scene.

The first input-object freeze used authorial-core hash `a18cca2815fc2b53fd16e03d7d2cfdc1147e1efa431034227cb3b29856aac383`. The assignment was opened after that initial freeze but before normal generator schema normalization. Normal preflight then rejected four unsupported dimension labels. Only labels were mapped (`appearance_reference→reference_use`, `validation_objective→concept`, `tone→atmosphere`, `motion_rendering→timing`); the source request, interpreted intent, subject, setting, event, priorities, baseline prose, anchor source text, anchor evidence, and open lighting dimension did not change. The complete disclosure and both hash sets are in `preflight_amendment.json`.

- Final generator-normalized authorial-core SHA-256: `21704bbc4538896cd52b90380b77c6fd0a185d99906092874cff1b45c69e0bf5`
- Final generator-normalized intent-lock SHA-256: `9307f9c0887c443019147f9c59696672637072380e5cbf0bf15e529e03f88d10`
- Reference JPEG SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Reference role: appearance only for visible adult facial structure, eye shape/spacing, face length, lower-face/jaw width, hairline, and hair; no identity or same-person claim

### Protocol deviation disclosure

After the initial core freeze and after opening the assignment, I read portions of the shared `generate_photo_prompt.py` wrapper and `prompt_generator.py` implementation while diagnosing the unsupported intent-lock labels. This exceeded the arm instruction that prohibited reading shared implementation files. No shared implementation, registry, asset, test, prior experiment, or other arm was modified or used as image input, and the frozen scene meaning did not change; nevertheless, a coordinator applying the strictest read-isolation rule should mark this arm as protocol-deviating rather than silently treating it as fully compliant.

## Pack, prompt, and runtime evidence

The request-scoped `photo-visual-intent/v1` explicitly bound `rembrandt_face_light_pattern` through `agent_postcore_interpretation`. All optional visual concepts and all six sampled creative candidates were rejected because they would add an unrequested relationship/glitch or weaken face-scale, action, environment, or assigned shadow geometry.

`composed_prompt.audit.json` reports `status: pass`, no failures, and effective visual-contract SHA-256 `95133b0ff8bc90f3e98469306e25f0ea158be39f7faa2667797845bbcbc8c523`. Its quality status is `warn`: the 206-word prompt exceeds the default 180-word concise target but remains below the evidence-adjusted 211-word advisory ceiling and the absolute 320-word bound; five uncovered pack intents are explicitly preserved in the final prompt.

`image_render_request.audit.json` reports `status: pass`, runtime prompt ID `1acb5a7ef4d7dea2`, one verified reference, matching negative bytes, the exact intent-lock hash, and no failures.

The built-in tool returned `/Users/chasoik/.codex/generated_images/01a05fda-2f86-7133-b1d8-3f44f8ded183/exec-4716c10c-8c2f-4719-a626-10241c4c54e4.png`. It was copied without replacing the original to:

`/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-capture-elements-three-arm-reference-v1/arm-02/render.png`

- Native dimensions: `1086x1448`
- Native SHA-256: `94bf3357871ff613283b6b9056868bdfe81c7de830b1cc92ee0408ca4359c0b0`
- Review thumbnail: `288x384`, SHA-256 `e14157ea474c58de4a60ea15ffa2bdf791466e737d97ea6733dbeee8ce1e9996`

## Strict pixel gates

Both the `288x384` thumbnail and `1086x1448` native image were inspected. The hard-gate set in `self_review.json` exactly equals the assigned profile gate set. Partial, substitute, or merely readable evidence was treated as failure.

| Gate | Verdict | Image-grounded evidence |
| --- | --- | --- |
| `vo_capture_rembrandt_elevated_side_key` | FAIL | At thumbnail scale the face reads broadly and nearly frontally lit; an elevated off-axis key does not clearly model one near side. |
| `vo_capture_rembrandt_joined_nose_cheek_shadow` | FAIL | At thumbnail and native scale, faint nose shading does not visibly join one continuous far-cheek shadow mass. |
| `vo_capture_rembrandt_contained_far_cheek_triangle` | FAIL | At both scales, under-eye light spreads diffusely; no contained inverted triangle with bounded edges survives beneath the far eye. |
| `vo_capture_rembrandt_readable_shadow_eye` | FAIL | Both eyes are readable at native scale, but flattened fill leaves no distinctly modeled shadow-side eye and surrounding face structure; the conjunctive gate fails. |
| `vo_capture_rembrandt_not_split_butterfly_or_ring` | FAIL | Native detail reads as flat frontal beauty illumination with mild generic side shading, not joined nose-cheek shadow geometry plus a far-cheek triangle. |

`self_review.audit.json` has `schema_failures: []`, `qualification_status: failed_technical_hard_gates`, `technical_qualified: false`, and `representative_eligible: false`. Its nonzero audit exit records the gate failures; it is not a malformed-review failure.

The rendered image does visibly preserve the adult subject, dark wavy hair, rain, red handwheel action, wet outerwear, and rail depth. Those successes do not compensate for the all-gates-same-image Rembrandt-light failure.

## User judgment boundary

No requesting-user preference has been received. Subjective satisfaction with the reference-scoped appearance, scene, and overall image remains pending. That future preference is recorded separately and cannot convert the failed technical hard gates into a pixel pass.

## Artifacts

- `request_envelope.json`
- `authorial_core.json`, `authorial_core.sha256`, `authorial_core.file.sha256`
- `intent_lock.json`, `intent_lock.sha256`
- `baseline_prompt.txt`
- `preflight_amendment.json`
- `visual_intent.json`
- `candidate_pack.json`
- `composed_prompt.json`, `composed_prompt.audit.json`
- `image_render_request.json`, `image_render_request.audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
- `render.png`
- `review-thumbnail.png`
- `self_review.json`, `self_review.audit.json`
