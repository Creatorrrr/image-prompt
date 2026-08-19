# Skill Arm Report

## Outcome

- Arm: `photo-prompt-image-generator` skill arm
- Skill snapshot SHA-256: `fc7d03290477d2b64d6b577fdbbf4a5ce8c5b934e9bb7b2b29b943b1735307a0`
- Source ref: `git:6a91d8f740b169dcf65cf6f19e297455bcd6a89c`
- Candidate packs generated: exactly `1`
- Image-generation calls: exactly `1`
- First-attempt tool status: `success`
- Retry or aesthetic iteration: `none`
- Composed audit: `PASS`, failures `0`
- Exact runtime-input audit: `PASS`, failures `0`
- Pixel qualification: technical `PASS`; complete semantic hard-gate qualification `FAIL`
- User/comparative judgment: pending; no claim that this arm is better or representative

The one delivered image is preserved at:

`/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-ab-20260819/skill_arm/generated_images/skill-arm-first-attempt.png`

- SHA-256: `dbcab60bc4b2510cfef2f4826de8e49f0a5bd1b1f9598475aba9985979962a72`
- Dimensions: `1086 × 1448`
- Format: PNG
- Size: `2,235,492` bytes

## Frozen-input preflight

The initially delegated files were verified before any pack or image call:

- `request_envelope.json`: `02f09b4e9d10e14cd54863c1568c9d1e0a1b95a4404873c74781e30fa5baab75`
- Initial `authorial_core.json`: `5d320b32c814bd920d1790a7c29001a698373cdf67d1938e7e1d5b196cb8d233`

The coordinator then paused the arm because the initial core used mechanically unsupported v6 schema field names. No pack or image call had occurred. The coordinator replaced only the serialization, documented it in `preflight_schema_correction.md`, and re-froze the same semantics, baseline, and evidence. The arm verified the corrected inputs before resuming:

- Current `request_envelope.json`: `02f09b4e9d10e14cd54863c1568c9d1e0a1b95a4404873c74781e30fa5baab75`
- Current `authorial_core.json` file SHA-256: `a8bb55c93f8d3fd3a60e3b52dcf56a1095057fbd3d1d054bd26487540aae7ce3`
- Canonical authorial-core SHA-256: `ff2c6096a1331478c5b7d1ed38b1ecec72fb588b615b9f12d016db66b8158f55`
- Canonical intent-lock SHA-256: `cc54dccfb34e3fc24b69b3c15092a2923bd7471ed88e6ccc1d775d10cc7d4d9d`

Neither frozen JSON file was modified by this arm.

## Exact candidate-pack command

```bash
/Users/chasoik/Projects/image-prompt/.venv/bin/python \
  /Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --request-envelope-json request_envelope.json \
  --authorial-core-json authorial_core.json \
  --candidate-pack-version v6 \
  --creativity 0.5 \
  --emit-candidate-pack \
  --n 1 \
  --output-file candidate_pack.json
```

Result:

- File: `candidate_pack.json`
- SHA-256: `4d83b849b04f69a7cebc368bc9210b1dcbb2df6ea90a2d893097e775e6b11693`
- JSON array length: `1`
- Pack ID: `4fa033c55c2aad41`
- Requested creativity: `0.5`
- Chosen ordinary/creative candidate IDs: `[]`
- Chosen optional visual-concept IDs: `[]`
- All six sampled creative candidates were explicitly rejected because they added no necessary value or could weaken one-frame causal legibility.

## Final prompt

Positive prompt (`172` words under the skill auditor's ASCII-word rule):

> Create a cinematic fantasy editorial photograph of an unmistakably adult woman, an ancient Northern Sea Ice Palace grandmaster restored to a youthful adult form. Her face follows the attached portrait only: pale luminous skin, a softly tapered oval face, large cool-gray eyes, straight delicate brows, a slim nose, full pale-rose lips, a tiny beauty mark beside the nose, and long ash-blonde hair with airy bangs. In a frozen moonlit palace corridor after a blizzard, she keeps an aloof, composed expression while fastening a frost-silk wrist guard around the same adult disciple's injured hand. At the instant she tightens the silver knot, her cool-gray eyes soften toward that disciple. The disciple's tense fingers visibly relax as the wrist guard seals the cracked glove with a thin crystalline sheen. Matching snow-crane emblems on the disciple's sleeve and the wrist guard establish continuity. Show glacial jade robes, restrained silver embroidery, translucent ice architecture, drifting snow, realistic skin texture, and quiet blue-white light. Prioritize facial likeness and the readable contrast between distant authority and protective care.

Negative prompt (`17` words):

> distorted fingers, fake-looking background, excessive HDR, cartoon style, over-processed retouching, unrealistic hands, broken facial features, illustration look

Exact composed object: `composed_prompt.json` (`33b747e8f91e9522b3c907dbaa766e9c1d434c7bbf77959516514c2f0b35c517`). The plain positive prompt is also preserved in `final_prompt.txt`.

## Audits and procedural commands

The SKILL.md example uses the obsolete option name `--candidate-pack`. That exact documented command was tried once and exited before auditing with `the following arguments are required: --pack`; it did not change the prompt or any generation input:

```bash
/Users/chasoik/Projects/image-prompt/.venv/bin/python \
  /Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --candidate-pack candidate_pack.json \
  --composed composed_prompt.json
```

The current CLI's actual option was then used:

```bash
/Users/chasoik/Projects/image-prompt/.venv/bin/python \
  /Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json \
  --composed composed_prompt.json
```

Result: `status: pass`, `failures: []`, `quality_status: warn`. The five warnings are non-blocking `uncovered_intent` trace rows; every warned core phrase occurs literally in the final prompt. Exact result: `composed_audit.json`.

Runtime request command:

```bash
/Users/chasoik/Projects/image-prompt/.venv/bin/python \
  /Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_image_render_request.py \
  --pack candidate_pack.json \
  --composed composed_prompt.json \
  --request runtime_request.json \
  --output runtime_audit.json
```

Result:

- `status: pass`
- `runtime_prompt_id: 5d6e95191e13bab0`
- `source_intent_lock_sha256: cc54dccfb34e3fc24b69b3c15092a2923bd7471ed88e6ccc1d775d10cc7d4d9d`
- Negative bytes match pack: `true`
- Reference count: `1`
- Failures: `[]`

The exact runtime prompt is the positive prompt followed contiguously by:

`Avoid: distorted fingers, fake-looking background, excessive HDR, cartoon style, over-processed retouching, unrealistic hands, broken facial features, illustration look`

Runtime prompt word count: `190`. Exact request and result are preserved as `runtime_request.json` and `runtime_audit.json`.

## First-attempt image call

Native tool: `image_gen.imagegen`

Exact tool parameters:

```json
{
  "prompt": "<runtime_request.json runtime_prompt_en, byte-identical>",
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/4FBED371-F292-4BB7-8800-B33B91190D45.jpeg"
  ]
}
```

Reference facts:

- Role: `face_appearance_reference_only`
- SHA-256: `a8aa61ee7f1452e8b155dc557e55aa7bb662e6755617f779e78ffbae6d769022`
- Dimensions: `1086 × 1448`
- Format: JPEG

The tool returned one accessible local PNG on the first call. It was copied into this arm while leaving the original tool output intact. No retry, correction render, or aesthetic iteration was performed.

## Pixel self-review

Prompt and runtime audits are preflight evidence only. The delivered pixels were inspected separately at thumbnail and native size; full findings are in `pixel_review.json`.

Strongly realized:

- Facial appearance follows the attachment well: pale luminous complexion, tapered oval face, cool-gray eyes, delicate nose and lips, nose-side beauty mark, and ash-blonde airy bangs.
- The subject reads as an adult woman, and the blue-white frozen architecture, silver-blue robes, snow, and crane embroidery make the Northern Sea ice-palace concept legible.
- The medium portrait keeps face, hands, recipient, and care action in one hierarchy.
- Her composed surface, practical wrist-guard fastening, softened gaze toward the recipient, and the recipient's open hand make the restrained-care archetype readable in one frame.
- No obvious extra hand, large text, or major background artifact appears.

Not fully realized:

- `character_response_trigger` fails: the centered hand is clear, but its specific injury is not unambiguous.
- `character_response_immediate_consequence` fails: the crystalline sheen is visible, but a cracked glove actively sealing is not clearly distinguishable.
- `character_response_continuity` fails: crane embroidery is present, but matching snow-crane emblems on both the disciple's sleeve and wrist guard are not unmistakable.

Therefore the first attempt is a successful delivery and a technically coherent image, but it is not a complete semantic hard-gate pass and is not promoted as representative. Single-frame archetype legibility is locally judged `PASS`; user preference, genuine concept success, and comparison against the other arm remain pending.

## Ledger and manifest status

One accurate standard ledger row was created with the current recorder's supported fields:

- Ledger: `runs/image_runs.ndjson`
- Run ID: `d15764e4ccf254df`
- Prompt ID: `cf94e9461e7f473d`
- Pack ID: `4fa033c55c2aad41`
- Image call count: `1`
- `cross_arm_inputs_used: false`

No independent-run manifest was fabricated. The current `record_image_run.py` accepts only candidate-pack versions `v2`, `v3`, or `v4`, and its manifest requires the v4-era `authorial_request_sha256`; this arm used v6 plus a canonical `photo-authorial-core/v3`. The accurate v6 generator argv, pack, hashes, runtime request, output, and ledger row are preserved instead.

## Isolation statement

This arm did not inspect or use `/baseline_arm`, `/blind_eval`, memory, prior experiment outputs, or another arm's prompt, pack, message, or image. It changed no repository source code. All created artifacts are confined to this arm directory.
