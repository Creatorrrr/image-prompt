# Arm 03 — Moirai fate-thread life allocation

## Outcome

Decision: **revise**. The image was delivered and inspected at 384×288 thumbnail and 1448×1086 native scale. Four of five authoritative profile gates pass in the same image. `vo_myth_moirai_cut` fails because the shears remain open around one intact filament with no visible severed gap or detached endpoint. Under the predeclared partial-is-fail rule, the arm is not qualified. Requesting-user preference remains pending.

- Image calls: 1
- Retries: 0
- Tool: built-in `image_gen`
- CLI/API fallback: none
- Independent cross-arm inputs: none
- Pack: `photo-candidate-pack/v6`, `c59053b35e2dcb85`
- Render: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/render-attempt-01.png`
- Render SHA-256: `054ec31dbff7a446e317de6aa4ab8bf93056e6139564e04869893160baeb0395`

Prompt/audit PASS is treated only as preflight evidence; it is not pixel PASS.

## Independent concept

Inside a storm-battered tidal observatory, three adult fate-workers allocate one adult lighthouse keeper's finite lifespan. The first spins the origin of one luminous red thread, the second measures an allotted span across a bronze rule, and the third is meant to sever its endpoint so the allotted segment lights a finite amount of amber sand in the keeper's hourglass. The supplied portrait is used only for visible facial and hair appearance guidance for the central measuring woman; no identity or same-person conclusion is made.

## Final prompt

```text
Photorealistic editorial photograph in a storm-battered tidal observatory at blue hour. Moirai visibly spinning measuring and cutting one life thread is expressed through this scene. Three unmistakably adult women stand around a circular stone worktable, performing a three-stage allocation of one human life by a spun, measured, and cut thread. The left woman spins a fresh luminous red thread from a wooden spindle; the central woman draws that same continuous thread taut against a graduated bronze measuring rule; the right woman closes open iron shears through its far end. Simultaneously, three distinct fate figures occupy separate readable work roles around one shared mortal allocation table; the first figure visibly spins or draws the beginning of the thread from a loaded wooden spindle into a bright origin coil; the second figure visibly measures an allotted section of that same thread against a graduated bronze rule with marked endpoints; the third figure visibly cuts the endpoint of that same thread with open iron shears at the marked terminal point; one continuous mortal life thread physically connects the spin measure and cut roles from origin across the rule to the recipient's hourglass token. One adult lighthouse keeper in a wet yellow oilskin holds a clear hourglass below the cut point; the severed measured length falls inside, igniting finite amber sand-light while the unused filament is dark. The central measuring woman carries only the reference image's visible facial appearance and loose, long, center-parted dark hair. Image 1 guides observed realistic-adult facial geometry: eye aperture and spacing, brows, nose, lips, face length, lower-face and jaw width, cheek contours, hairline, and natural asymmetry; the figure is fictional and no identity claim is made. A medium-wide three-quarter tableau keeps every face, six worker hands, tools, complete thread path, recipient, and consequence legible. Cool blue-hour lightning contrasts localized red-thread and amber-hourglass glow on flooded mosaics beneath a brass astrolabe.
```

Preserved `negative_en`:

```text
cartoon style, 3D render look, unrealistic hands, broken facial features, body distortion, over-processed retouching, low resolution, plastic-looking skin
```

## Authoritative profile gates

| Gate | Scale | Result | Pixel evidence |
|---|---|---|---|
| `vo_myth_moirai_three_roles` | thumbnail | PASS | Three separate adult workers are readable as spinner, measurer, and cutter by station and tool. |
| `vo_myth_moirai_spin` | native | PASS | A luminous red filament visibly exits a densely wound spool while the first worker guides the origin. |
| `vo_myth_moirai_measure` | both | PASS | The middle worker holds a graduated bronze rule and the same taut filament lies along the marked length. |
| `vo_myth_moirai_cut` | both | **FAIL** | Open blades surround an intact filament that bends downward; there is no severed gap or detached endpoint. |
| `vo_myth_moirai_continuity` | native | PASS | One red filament can be traced from spool to ruler to shears zone and downward toward the hourglass. |

Supplemental findings:

- Actor PASS; action FAIL; target PASS; consequence PASS. The combined causal chain fails because cutting is not actually visible.
- Reference-visible appearance continuity FAIL under strict scoring: long dark near-center-parted hair, adult facial scale, face length, jaw width, brows, nose, and lips are broadly comparable, but the generated central face looks down with lowered eyelids, so eye aperture/shape/spacing cannot all be compared. This is not an identity assessment.
- Hand visibility FAIL: no obvious extra digits or fused hands, but only five of the six worker hands are clearly exposed; the spinner's second hand is hidden.
- Tool contact FAIL at the cut station; spool/ruler/hourglass contacts are otherwise coherent.
- Text-artifact check PASS: no caption or watermark; ruler/table glyphs are incidental functional/decorative marks with minor pseudo-glyph ambiguity.

## Audit history

- Candidate-pack preflight initially blocked before pack creation because `spin_phrase` had 7 content words versus the required 10. The same component evidence was extended; final v6 pack generation exited 0.
- `audit_composed_prompt.py`: first run FAIL because the active profile required its allowed label plus component definition. After adding the exact allowed label, final run exited 0 with `status=pass`, `failures=[]`. The 311-word prompt and 191-word baseline produce advisory length warnings only; both remain inside the 320-word absolute bound.
- `audit_image_render_request.py`: exit 0, `status=pass`, `runtime_prompt_id=32f58dd760abf993`, negative bytes match, one reference hash matches, intent-lock and effective visual contract are bound.
- `audit_moe_render_review.py`: exit 1 as expected for a failed hard gate, `qualification_status=failed_technical_hard_gates`, `technical_qualified=false`, `schema_failures=[]`, sole failed gate `vo_myth_moirai_cut`.
- `validate_iteration_record.py`: exit 0, `status=ok`, `errors=[]`.
- `record_image_run.py`: exit 0, ledger run `abeb4c8fd89a45d7`, prompt id `dd9b46fde40628d9`.

## Skill use and effect

- `photo-prompt-image-generator` enforced the isolated core-before-pack boundary, v6 intent precedence, post-core hard visual intent, exact negative preservation, native request audit, and strict render gates.
- `imagegen` kept execution on one built-in call with the local reference attached; no CLI/API fallback or retry was used, and the returned original was preserved before a repo-local copy was made.
- `image-prompt-skill-improver` kept source observation, prompt/package checks, generation delivery, rendered pixels, hypotheses, and user judgment as separate evidence layers. One failing sample is retained as `revise`, not turned into a universal skill edit.

## Primary artifacts

- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/request_envelope.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/authorial_core.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/visual_intent.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/candidate_pack.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/composed_prompt.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/composed_prompt_audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/render_request.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/render_request_audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/test_case.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/render-attempt-01.png`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/self_review.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/self_review_audit.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/iteration_record.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/image_run_ledger.ndjson`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/run_manifest.json`
- `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/skill_usage.json`
