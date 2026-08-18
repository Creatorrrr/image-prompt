# Yandere Photographic Legibility Improvement Plan

Updated: 2026-08-18

## Scope

This plan addresses adult fictional character photography. A face reference controls appearance only; it is not evidence of personality, relationship, pose, or composition. The target outcome is a nonviolent, single-frame yandere reading that remains distinguishable from an ordinary caregiver, generic jealousy, detached surveillance, and horror styling.

## What changed after the initial review

- The runtime data now has an abstract `yandere` character-response profile and a hard `yandere_affection_control_relation` visual profile.
- The visual profile requires one identifiable adult counterpart, visible affection or care, one concrete boundary or access-control action, and an already-visible consequence for the same counterpart.
- A restrained expression contrast—such as a tender asymmetric mouth with overfocused attention and faint lower-lid tension—is supporting evidence rather than the definition.
- Role and horror shortcuts are explicit confounders: a nurse, syringe, weapon, blood, red light, intense stare, photo wall, or fixed smile cannot prove the archetype.
- Generic `same_target`, `contrasts`, and `temporal_order` relations now pass through the v6 core and compiled character-response contract.

## Research synthesis and limits

- The HAI 2023 prototype supports target-conditioned attention and affect change, but its appearance mapping was not validated as a universal recognition recipe.
- The HAI 2024 scale study supports excessive liking, self-sacrifice, jealousy, and possessiveness as related contributors. Its participants reported only moderate familiarity, the authors warn that the measured pattern may not be unique to yandere, and it did not test photographic cues.
- Bruno's character-element analysis supports a sweet outward surface as one convention inside a larger hierarchy; it does not show that an eye shape alone identifies yandere.
- The 2026 anime/manga expression classifier documents illustrated manic-euphoric conventions, but it used one annotator and does not establish photorealistic or relationship-level validity.

Therefore, the durable photographic mechanism is behavioral: affection, control, and consequence must all point to the same adult target. Facial and gaze cues only increase outward legibility.

## Remaining defects found and resolved

1. The first relation contract bound target, action, and affect leak but omitted the consequence. The corrected `same_target` vector binds `relationship_target`, `surface_affect`, `primary_action`, and `immediate_consequence`.
2. Relation rows previously accepted arbitrary identifiers and treated member order as meaningful. Validation now permits only declared generic axes and causal roles, requires `relationship_target`, rejects duplicates, and compares `same_target` members as an unordered set.
3. An elliptical retry could preserve the concept in lineage while leaving its visual profile as an unselected optional candidate. A preserved parent hard obligation must now be recreated through hash-bound post-core visual intent from an exact current core field.
4. The authorial baseline had a 24–180 word boundary, but the final composed prompt could exceed it. The v5/v6 composed audit now enforces the same boundary.
5. Research rows linked sweet-surface evidence to unrelated menacing-gaze, reflection-horror, and invisible-mood candidates. Those links and direct yandere routing tags were removed, and source-specific limitations were recorded.

## Composition priority for the next render

Use a patient-eye-level medium close-up. Keep the nurse slightly inside the same adult patient's personal space. Make the primary affect channel facial: a soft, slightly asymmetric closed-mouth smile with restrained warmth, sustained patient-directed attention, and faint lower-lid tension. Show one concrete access action and its consequence on the same focal plane—for example, her hand moves the bedside call button away while the taut cable and the gap from the patient's reaching hand remain readable. Keep a capped syringe low, non-contact, and secondary. Avoid cold red-lit menace as the dominant mood.

## Acceptance gates

1. Text preflight: all frozen evidence is literal, the hard visual profile survives retries, forbidden labels remain out of runtime text, and `prompt_en` is 24–180 words.
2. Thumbnail review: tenderness and control both read toward the same target; the frame does not collapse into “ordinary nurse” or “generic horror.”
3. Native-size review: facial asymmetry, gaze focus, hand-object contact, cable/gap consequence, adult identity, and reference-face fidelity are intact.
4. Process report: prompt/audit pass, delivery success, pixel legibility, and user acceptance are reported separately.
5. Promotion: no render is marked representative until the requesting user accepts the yandere reading. A passing contract is preflight evidence, not pixel proof.
