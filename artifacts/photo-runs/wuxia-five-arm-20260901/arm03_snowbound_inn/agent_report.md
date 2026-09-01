# Arm 03 — snowbound inn qualification report

## Outcome

One built-in `image_gen` call returned a concrete 1536×1024 PNG and the attempt was preserved. The arm is **not technically qualified** because `vo_wuxia_inn_watchful_relation` failed at native scale. Four of the five exact hard gates passed; partial success is failure under the strict contract. No retry was made.

## Frozen inputs and preflight

- Request envelope raw SHA-256: `cf5e60f1b5db7c6fbb4b081bc33f2153eadcbc96a057fa74c1286f8a028c7df6` — verified.
- Authorial core raw SHA-256: `25588d99929ec781976e192dd567a914d3b0162a6c4d781ba71cd478017f7b52` — verified.
- Candidate pack: `photo-candidate-pack/v6`, pack ID `2e85c8e8b5dec4ca`.
- Canonical authorial core SHA-256: `88290220e08f02d5c99f58f6d14e3f5c241d19d5ac247dbc57ddb9cdf9ebd479`.
- Intent-lock SHA-256: `1092cf5b2d68f87b42b407ca1e3655b4196fcc8433fd12da91a7af50975a3110`.
- Active hard profile: `jianghu_inn_identity_standoff`; effective visual contract SHA-256 `99706250d4b0d38544f98257463cb4ddd8699a471e3a627ea7442760f9b91732`.
- Reference SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`; runtime role `appearance_reference` and label `Image 1`.
- Optional visual concepts selected: none; the unrelated aircraft and glitch concepts were rejected. All six sampled creative candidates were also rejected, including bodycon, power-stance, extreme-wide, environmental-portrait, LED-wand, and golden-hour material.
- Composed audit: `status=pass`, zero failures, `quality_status=warn`. The warnings are advisory prompt-budget notices plus four frozen intents that the final prompt preserved through free description.
- Exact render-request audit: `status=pass`, zero failures, runtime prompt ID `6b50ca71fd818a13`, exact negative bytes matched, one reference verified.

## Render

- Tool: built-in `image_gen`.
- Image calls: exactly `1`.
- Native tool result: `/Users/chasoik/.codex/generated_images/01a05af3-a49a-72b3-9e1e-5c19cf778797/exec-c86ba0bd-8469-46be-984c-a22ed1575ca5.png`.
- Preserved arm copy: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/wuxia-five-arm-20260901/arm03_snowbound_inn/render.png`.
- Image SHA-256: `5b42c7a067babca9cf027f6cb7064df54ccb43b85f31ea49a5f2097126a9a5a9`.
- Native dimensions: `1536×1024`, PNG, RGB.
- Thumbnail reviewed: `512×341`, SHA-256 `da181fcd65d8393880464fa61d1099d455b7c6b4eaecd4dbd14b1f764e1a9f15`.

## Exact hard-gate review

| Gate | Status | Image-grounded evidence |
|---|---|---|
| `vo_wuxia_inn_structure` | PASS | The wide thumbnail shows the main wooden table, snow-lit entry threshold, and narrow staircase. |
| `vo_wuxia_inn_faction_zones` | PASS | Lead at the foreground table, traveler on the stair, and server in the right service zone form three separated functional zones at both scales. |
| `vo_wuxia_inn_watchful_relation` | **FAIL** | At native scale, the lead looks toward the server, the stair traveler looks forward/down, and the server looks at the kettle. Their eyelines do not converge on the jade tally, so one mutual identity-testing relation is not visible. |
| `vo_wuxia_inn_preserved_routine` | PASS | The lead's cup, the steaming upright kettle, and several intact service vessels preserve the public inn routine at both scales. |
| `vo_wuxia_inn_not_generic_or_brawl` | PASS | Snowbound waystation architecture, period jianghu clothing, Chinese-character signage, and restrained hands distinguish the scene from a Western saloon, generic fantasy tavern, or open melee. |

The render-review auditor found zero schema failures and returned `qualification_status=failed_technical_hard_gates`, `technical_qualified=false`. Its nonzero exit is the expected fail-closed result for the one failed hard gate. The generic `photo-image-render-review/v1` auditor was not applicable because this pack contains no `render_repair` contract.

## Supplemental appearance observations

The lead reads as an adult. Native inspection shows long near-black wavy hair with a center part, a softly oval face, straight brows, dark warm-looking eyes, and natural lips broadly continuous with the supplied visible appearance cues. The rendered face is smaller, three-quarter turned, and more dimly lit than the frontal reference, so exact eye color and fine facial proportions are less judgeable at thumbnail scale. These are appearance observations only; they are not biometric identity, ethnicity, personality, attractiveness, or same-person claims.

## Provenance and evidence boundary

- Ledger run ID: `88120efcc82f502d`; prompt ID: `c04132c9d3feece8`.
- Independent manifest: `photo-independent-run-manifest/v2`, `cross_arm_inputs_used=false`, image call count `1`.
- Prompt and runtime audits establish frozen text/hash/reference binding only; they do not establish delivered-pixel fidelity.
- The successful tool call establishes returned image bytes only; it does not establish hard-gate success.
- The pixel review records this agent's observation of the saved image at thumbnail and native scales. It does not infer hidden intent or establish user preference.
- Requesting-user judgment has not been received and remains separate.

## Artifact index

- `composed_prompt.json`
- `composed_prompt_audit.json`
- `render_request.json`
- `render_request_audit.json`
- `render.png`
- `render_thumbnail.png`
- `render_review.json`
- `render_review_audit.json`
- `image_runs.ndjson`
- `run_manifest.json`
