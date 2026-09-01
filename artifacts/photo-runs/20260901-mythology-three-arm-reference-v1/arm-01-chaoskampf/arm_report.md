# arm-01 — `chaoskampf_cosmogonic_ordering`

## Outcome

- Final decision: `revise`
- Technical qualification: `false`
- Prompt/composition audit: `pass`
- Exact runtime-input audit: `pass`
- Pixel review: `fail`
- User preference: `pending`
- Built-in image calls: `1`
- Retries: `0`
- CLI/API fallback: `0`
- Independent no-cross-arm inputs: `true`

The render strongly preserves the champion, primordial serpent, two-handed spear combat, lightning, and epic flooded setting. It does not strictly preserve the same-adversary defeat transition, the exact defeat-caused ordered-world consequence, the requested jaw-pinning geometry, or the reference-visible face geometry. Partial evidence was counted as failure.

## Independently frozen concept

Before opening project candidate/profile data, the arm froze a 170-word `photo-authorial-core/v3`: one adult woman storm-bearer pins one colossal abyssal sea serpent to a basalt meridian stone with a bronze axis-spear; at that same impact the defeated flood must become exactly four straight rivers and concentric stone terraces. The source portrait is used only for visible face and hair appearance continuity.

## Final prompt

> Photorealistic: cosmogonic combat visibly producing ordered realms, a battle that visibly turns primordial disorder into a measured world. At a flooded salt quarry, one adult woman storm-bearer wears four-river bronze regalia; one tradition-bound champion remains distinct from the adversary and leads the ordering side as the adult woman storm-bearer. Opposing her, one primordial sea storm serpent or chaos adversary is visually distinct and tradition-bound, embodied as a single colossal rain-dark serpent resisting at the strike point. She drives a bronze axis-spear down across the armored jaw of one colossal abyssal sea serpent onto a basalt meridian stone. Weapon force counterforce and contact geometry make the central combat readable as both of her hands drive the spear against the serpent's jaw. Lightning links spear, contact, and coil. The adversary visibly passes from active resistance into a defeated or partitioned state because the spear pins its jaw and its resisting coil is splitting at the same impact. New boundaries world matter stable realms or sovereign placement visibly result from that defeat as four straight rivers and concentric terraces emerge from the pinned flood. Her clearly visible face and long center-parted dark wavy hair follow only the supplied portrait's visible facial and hair appearance. Image 1 solely guides appearance continuity; preserve eye aperture and spacing, face length, jaw width, brows, nose, lips, cheekbones, asymmetry, and hairline. Low 35mm framing keeps face, hands, contact, coil, rivers, and terraces legible together. Deep focus, cobalt backlight, bronze return, wet salt, scales, spray: documentary texture.

Preserved negative:

> cartoon style, 3D render look, illustration look, distorted fingers, low resolution, excessive HDR, unrealistic hands, body distortion

## Strict gate results

| Gate | Result | Pixel evidence |
|---|---|---|
| `vo_myth_chaoskampf_champion` | PASS | The bronze-clad adult storm champion dominates the 213×320 thumbnail and remains distinct from the serpent. |
| `vo_myth_chaoskampf_adversary` | PASS | One massive rain-black sea-serpent head and connected coils remain the clear primordial target at thumbnail and native scales. |
| `vo_myth_chaoskampf_combat` | PASS | Both hands grip one shaft; the lower blade contacts the serpent's upper head; lightning follows the shaft into the contact point. |
| `vo_myth_chaoskampf_defeat` | FAIL | The main head and coils remain active; a distant raised coil fragments, but the link from that breakup to the same spear impact is ambiguous. |
| `vo_myth_chaoskampf_order` | FAIL | More than four irregular waterways and horizontal terraces can read as pre-existing terrain; defeat-caused new cosmic order is not unmistakable. |

Supplemental failures:

- Core action: the blade contacts the upper head rather than visibly pinning the armored jaw to the meridian stone.
- Core consequence: the image does not show exactly four straight rivers and newly formed concentric terraces.
- Reference-visible appearance continuity: hair silhouette passes, but the rendered eyes are larger/rounder, the face is shorter, and the lower face/jaw is narrower. This is an appearance comparison only, not a same-person or identity judgment.
- Contact/anatomy/text: human hands are grossly coherent and no accidental text appears; requested jaw alignment and one-body partition causality fail.

## Evidence and hashes

- Source reference: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`
  - SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- Saved result: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-01-chaoskampf/render-attempt-01.png`
  - Native size: `1024×1535`
  - SHA-256: `f881178191337c11a6d0711e883411b069f93797b4bc6edc38bd9786123277bb`
- Pack: `521ae094353daf7a`
- Prompt ID: `ce4d9aec6cde8c8e`
- Runtime prompt ID: `e8e92865a8d65515`
- Effective visual contract: `8fefbb5377399267e95292a16a1bfc520b15197000993310be5093dc73567d94`

## Skill use and influence

- `photo-prompt-image-generator`: enforced the pre-core isolation boundary, exact envelope binding, four locked dimensions, at least two open authorial dimensions, v6 reference-edit identity mode, hard visual intent, literal evidence, unchanged negative bytes, and exact runtime request audit.
- `imagegen`: enforced the built-in-only path, exact one-call policy, concrete local output discovery, non-destructive project copy, and no CLI/API fallback.
- `image-prompt-skill-improver`: separated package, prompt, generation, pixel, and user evidence; required thumbnail/native review, falsifiable hypotheses, an iteration record, and the bounded `revise` decision rather than treating audit PASS as pixel PASS.

## Audit commands and results

- `generate_photo_prompt.py ... --candidate-pack-version v6 --reference-edit-mode identity --creativity 0.5`: PASS after a structure-only correction from unsupported open-dimension names (`palette`, `surface_detail`) to allowed names (`color`, `material`); baseline prompt bytes and meaning were unchanged.
- `audit_composed_prompt.py --pack candidate_pack.json --composed composed_prompt.json`: PASS, 248 words, no failures; only expected advisory warnings for exceeding the default 180-word concise target and for free-described frozen intents.
- `audit_image_render_request.py ... --request render_request.json`: PASS; negative bytes, intent-lock hash, reference hash, and exact runtime prompt all match.
- `audit_moe_render_review.py --pack ... --composed ... --review self_review.json`: schema PASS but exit 1 by design, `failed_technical_hard_gates`; exact failed gates are defeat and order.
- `validate_iteration_record.py iteration_record.json`: PASS, `{"status":"ok","errors":[]}`.
- `record_image_run.py ... --image-call-count 1 --independent-no-cross-arm-inputs`: PASS; ledger run `e515d63f7941b6b9` and v2 manifest created.

## Boundary

Prompt and runtime audits establish preflight integrity only. The delivered pixels establish a strict technical failure for this attempt. No requesting-user preference judgment has been received, and no skill-level general improvement is promoted from this single motivating sample.
