# Yandere nurse photo-prompt skill A/B evaluation

## Outcome

The skill arm won prompt semantics and was the only arm to deliver an image, but its rendered image failed the defining behavior gate. The baseline made one generation call and was blocked at the output stage under the `sexual` moderation category, so this trial has no valid paired pixel-quality winner.

## Controlled setup

- Two fresh subagent contexts with no cross-arm prompt, image, or artifact access.
- Same face-only reference image and same built-in image-generation tool.
- Exactly one image call per arm; no retry, fallback, or edit.
- Request/core and 100-point rubric frozen before generation.
- Three blind prompt reviewers and three blind pixel reviewers.

## Delivery and process

| Arm | Target skill | Prompt preflight | Runtime preflight | Calls | Delivery |
|---|---|---|---|---:|---|
| Skill | yes | PASS, 0 failures | PASS, 0 failures | 1 | image delivered |
| Baseline | no | not applicable | not applicable | 1 | output moderation block: `sexual` |

The skill arm used pack `f0ab0cae8b2c0945` and produced a 1122×1402 image with SHA-256 `22984e0b471a380933818c5a16a72985f8c25e822166dff534ee5550d3c7db8d`. Two pre-emission corrections were mechanical schema normalizations; the baseline prompt and nine frozen character-response evidence phrases did not change.

## Blind prompt review

| Prompt source | Reviewer scores /50 | Mean | Reviewer wins |
|---|---|---:|---:|
| Skill | 48, 48, 46 | **47.3** | **3/3** |
| Baseline | 35, 31, 35 | **33.7** | 0/3 |

Consensus: the skill prompt names one adult beloved target, a concrete target-directed action, an outward/underlying affect contrast, an already-visible consequence, and same-frame continuity. The baseline prompt communicates genre through a stare, rose, locket, and syringe, but provides no identifiable relationship target, action toward that target, or visible consequence.

The skill prompt is 267 words versus 286 for baseline. It is semantically stronger but still over-engineered and physically dense.

## Blind pixel review of the delivered image

The three blind scores were **75, 77, and 77**, for a mean of **76.3/100**. All three reviewers issued a strict concept failure.

| Category | Mean |
|---|---:|
| Reference-face fidelity | 16.7/20 |
| Adult nurse and syringe | 18.3/20 |
| Obsessive-romance behavior | 16.7/30 |
| Photo/anatomy/prop coherence | 16.3/20 |
| Composition/integration | 8.3/10 |

Visible strengths: strong reference resemblance, unmistakable adult nurse role, legible capped syringe, coherent patient-POV composition, and polished clinical photography.

Visible failure: both nurse hands are occupied by the syringe and chart. She does not visibly move the call button; the button's separation from the patient's hand does not prove a consequence; the chart grip is not clearly white-knuckled. At thumbnail scale the image reads mainly as an attractive or ominous nurse holding a syringe and chart, not a concrete obsessive-romance incident.

## Skill assessment

- Prompt-semantic performance: strong improvement in this trial.
- Delivery: skill 1/1, baseline 0/1, but one stochastic moderation block is not causal proof.
- Rendered concept fidelity: not qualified. Audit PASS proved textual binding only.
- Execution cost: materially higher for the skill because envelope/core/pack/composed/runtime contracts and audits were required.

The most important improvement is a physical-action feasibility check before rendering. The prompt should allocate one hand to the capped syringe and the other to visibly dragging the call button away, removing the chart entirely; the affect leak should use a facial or gaze micro-signal that does not require a third hand. Abstract clauses such as “his choice has narrowed” should be replaced by visible contact geometry.

## Conclusion

For this one-shot pair, the skill clearly improved the written prompt and delivered the only usable image, so it showed real value. It did not yet demonstrate superior final concept pixels: the one delivered render failed the very relationship behavior the skill was designed to preserve, while the baseline produced no pixels to compare.
