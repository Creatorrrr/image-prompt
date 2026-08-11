# Photo prompt skill A/B evaluation

## Conditions

- Skill arm: `photo-prompt-image-generator` candidate pack, agent composition, fail-closed audit, then built-in image generation.
- Baseline arm: general prompt writing only, without reading or using the photo skill, candidate data, or audit scripts; same face reference and built-in image generator.
- One final 1086x1448 image per arm. This is a single-sample product check, not a statistically controlled model evaluation.

## Blind result

The condition reveal occurred only after the scores in `blind-review-before-unblind.md` were fixed.

| Criterion | Weight | Skill | Baseline |
|---|---:|---:|---:|
| Face-reference fidelity | 25 | 23 | 24 |
| Nekomimi / maid / tsundere legibility | 25 | 25 | 21 |
| Photorealism and anatomy | 20 | 18 | 19 |
| Composition and lighting coherence | 15 | 14 | 14 |
| Defect and forbidden-element control | 10 | 9 | 10 |
| Prompt discipline and process evidence | 5 | 4 | 3 |
| Total | 100 | 93 | 91 |

## Interpretation

The skill arm won narrowly because its directed cup handoff, averted pout, and ear response made the tsundere contradiction recoverable at thumbnail size. The baseline produced the cleaner conventional portrait and slightly better face fidelity, but its crossed arms and sideways glance communicated only generic aloofness.

The skill did not provide a broad aesthetic-quality win. Its hand/cup transfer is slightly softer, and the required ear-angle/contact-mark details are subtler in pixels than in the audited prompt. The baseline also used an unrequested ethnicity descriptor inferred from the reference and its first image request was input-moderated by explicit negative-list terms before an affirmative retry succeeded.

Operationally, the skill is expensive. The initial automatic `츤데레 메이드` route produced a legacy `contradiction_in_frame: manual` gate that the fail-closed auditor could never accept. One direct character-preset reroute was required. The final pack passed with exact negative preservation, but retained optional photographic-integration/craft warnings and pushed the prompt to 118 words.

## Verdict

For this sample, the skill improves character-mechanism legibility and auditability, not face fidelity or raw polish. Keep it when the visible relationship behavior matters; simplify the auto-routing/gate path and reduce mandatory evidence density before treating it as an efficient default for ordinary character portraits.
