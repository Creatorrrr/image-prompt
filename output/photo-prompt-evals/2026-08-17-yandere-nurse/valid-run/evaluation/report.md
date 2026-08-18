# Skill A/B Evaluation — Yandere Nurse

## Outcome

The no-skill baseline wins this one-pair comparison by a small but unanimous blind-review margin.

- Blind reviewer 1: baseline 87, skill 86
- Blind reviewer 2: baseline 89, skill 85
- Mean: baseline 88.0, skill 85.5
- Reviewer preference: baseline 2–0
- Hard-constraint failures: none in either image
- Both arms: one successful built-in image-generation call, no retry or fallback

This is a scoped result for one stochastic pair, not proof of general superiority.

## Mean category scores

| Category | Skill | Baseline | Difference, baseline minus skill |
|---|---:|---:|---:|
| Face-reference fidelity | 18.5/20 | 17.5/20 | -1.0 |
| Yandere concept legibility | 13.0/20 | 15.5/20 | +2.5 |
| Nurse and syringe readability | 15.0/15 | 14.5/15 | -0.5 |
| Character-specific story beat | 6.0/10 | 8.0/10 | +2.0 |
| Photographic/anatomical coherence | 14.0/15 | 13.5/15 | -0.5 |
| Composition/cinematic impact | 9.0/10 | 9.0/10 | 0.0 |
| Constraint compliance | 10.0/10 | 10.0/10 | 0.0 |
| **Total** | **85.5/100** | **88.0/100** | **+2.5** |

## What visibly decided the result

The skill image more closely preserved the reference face, made the capped syringe exceptionally clear, and had slightly cleaner single-hand geometry. Its face-syringe close-up, however, read mainly as a polished clinical portrait. Both blind reviewers found the possessive side of the requested contradiction too subtle.

The baseline image gave up a small amount of exact face matching and syringe geometry but gained a more legible relational instant: forward lean, sustained intimate gaze, hand over the chest, and presented syringe. That visible action cluster made tenderness and implied control coexist more clearly, improving both yandere legibility and story-beat scores.

## Prompt and workflow comparison

- Skill prompt: 149 words.
- Baseline prompt: 421 words.
- The skill prompt was 64.6% shorter while still meeting every hard image constraint.
- Skill pack: `photo-candidate-pack/v6`, pack `7939680264efe4e0`, creativity 0.5, seed 20260817.
- Skill composed audit: PASS with quality WARN and four informational uncovered-intent warnings; runtime-request audit: PASS.
- The skill selected only `preset:beauty_closeup_hand_gaze`, transforming it into a shared face/syringe focal plane. It rejected all unrelated visual concepts, including contained-affect and underarm-salience candidates.
- The baseline had no project audit by design; it used ordinary reasoning only.

The skill therefore demonstrated a real process advantage—compactness, intent/hash provenance, exact runtime binding, and fail-closed preflight—but did not demonstrate a rendered-pixel advantage in this pair. Its one selected augmentation optimized face and prop clarity, while the baseline independently authored the stronger character-specific gesture.

## Practical diagnosis

For behavior-led archetypes such as yandere, the missing quality was not more visual polish. It was a concrete trigger/action/affect-leak/consequence beat. A future clean evaluation should freeze that as a typed `character_response` assertion before retrieval, rather than relying on a concept label plus close-up framing. That would test whether the v6 character-response path improves the exact weakness exposed here without retroactively changing this run.

## Infrastructure-invalid attempt

An earlier setup attempt was excluded before scoring. The shared workspace experiment directory disappeared after both agents had inspected the reference: the baseline's only image call failed because its reference path vanished, while the skill arm made zero image calls. No pixels existed to compare. The valid run above used fresh agents and separate `/tmp` directories with byte-identical frozen request, core, and reference hashes; both produced one image successfully.
