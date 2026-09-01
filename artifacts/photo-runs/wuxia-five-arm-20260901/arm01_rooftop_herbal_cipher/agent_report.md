# Arm 01 — Rooftop Herbal Cipher

## Outcome

- Tool: built-in `image_gen`, generation with one attached appearance reference.
- Image calls: exactly 1; no retry.
- Local image: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/wuxia-five-arm-20260901/arm01_rooftop_herbal_cipher/generated.png`
- Native source retained: `/Users/chasoik/.codex/generated_images/01a05af3-198c-7582-b17c-26b48c993f46/exec-06256a6d-3685-42cb-b9e8-784f89ee157d.png`
- Image dimensions: 1536×1024.
- Image SHA-256: `93a0eb97a1f9eeb4ff68afa12d1abd7ace047325d41ef4bb38c51a5d888e17a8`.
- Thumbnail reviewed at 512×341: `generated_thumbnail.png`.
- Technical visual qualification: 5/5 required hard gates passed.
- User judgment: not yet received. No preference or acceptance claim is made.

## Frozen provenance

- Raw request file SHA-256 verified: `0a029e95ffe58f5817a6b19823239d7d032d3e4d049f059f6e8b1771de365933`.
- Raw authorial-core file SHA-256 verified: `d3ad1141ec635605d82e373b9aac855c2d498890b3cb2fe7db440059da6e10f5`.
- Candidate pack: v6, pack ID `596e5bf84da40cad`.
- Canonical authorial-core SHA-256: `93dca101171d5e2d06c2df4334e04f35aef802314d73f6c92aa1515e057ad6b7`.
- Intent-lock SHA-256: `c7718a3823ab0bfed4507b792a9034731dc6600bc80eeb1bc3058008adbf6c39`.
- Active hard profile: `wuxia_rooftop_qinggong_traversal`.
- Reference portrait SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`.
- Reference role: `appearance_reference`; Image 1 was used to guide visible adult appearance in a newly generated scene, not as an edit target or identity-control source.
- Optional visual concepts and all sampled creative candidates were rejected to preserve route clarity.

## Audit status

- `composed_prompt.json`: `status=pass`, no failures. The 197-word prompt exceeds the 180-word default recommendation but remains below the evidence-adjusted 199-word ceiling; this is an advisory warning only.
- `render_request.json`: `status=pass`; prompt, negative, intent lock, portrait path/hash/role, and composed-audit boundary match.
- `render_review.json`: schema-valid; `technical_qualified=true`, `failed_hard_gates=[]`, `schema_failures=[]`.
- `audit_moe_render_review.py`: qualification status `visual_technical_qualified_user_judgment_pending`; `representative_eligible=false` only because requesting-user judgment is absent. The auditor therefore exits nonzero by design despite technical qualification.
- Generic `audit_image_render_review.py`: not applicable because this pack has no `render_repair` contract.
- Recorder: run ID `1f13e26fbe2e6788`, prompt ID `343db6feaee236fe`; exact runtime prompt and negative match the render request.
- Independent manifest: `photo-independent-run-manifest/v2`, `image_call_count=1`, `cross_arm_inputs_used=false`.

## Five strict visual gates

| Gate | Result | Image-grounded observation |
|---|---|---|
| `vo_wuxia_rooftop_route` | PASS | At thumbnail scale, old tiled roof planes on both sides and the deep alley gap read as one height-changing route. |
| `vo_wuxia_rooftop_takeoff` | PASS | At native scale, the trailing lower-left boot is owned by the left eave tip, with a localized water splash marking push-off. |
| `vo_wuxia_rooftop_trajectory` | PASS | At both scales, the full adult figure is between roofs; hair and robe panels trail left while travel reads rightward. |
| `vo_wuxia_rooftop_destination` | PASS | At both scales, a separate broad right roof lies ahead of the leading boot with an unobstructed landing surface. |
| `vo_wuxia_rooftop_not_flight_or_pose` | PASS | Takeoff splash, eave ownership, intermediate body, coherent cloth lag, gap, and destination jointly read as a human roof-to-roof leap. |

Partial evidence would have been recorded as FAIL; none of the five gates was averaged or inferred across attempts.

## Supplemental appearance observations

- Long near-black wavy hair and a near-center part remain visible.
- A softly oval facial outline remains readable at native scale.
- Dark eyes and straight brows are visible, but exact eye color and fine spacing are not reliably judgeable at this action-subject scale.
- Natural lip shape is visible; exact closed-lip continuity is ambiguous because the face is small and the mouth may be slightly parted.
- These observations concern visible appearance cues only. They do not establish biometric identity, ethnicity, personality, attractiveness, or same-person status.

## Evidence boundary

Prompt and runtime audits establish serialized text, hash, selection, and reference-byte consistency; they do not establish rendered pixels. The recorded pixel review is this agent's inspection of the saved thumbnail and native image, not an automated image measurement and not requesting-user judgment. Technical gate success does not establish user preference. The separate appearance-reference observations do not establish identity. No other arm prompt, image, message, or result was used.

## Artifacts

- `composed_prompt.json`
- `composed_prompt.audit.json`
- `render_request.json`
- `render_request.audit.json`
- `generated.png`
- `generated_thumbnail.png`
- `render_review.json`
- `render_review.audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
