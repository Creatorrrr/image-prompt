# Yandere Photographic Legibility Improvement Plan

Updated: 2026-08-18

## Scope

This plan addresses adult fictional character photography. A face reference controls appearance only; it is not evidence of personality, relationship, pose, or composition. The target outcome is a character-centered, single-frame yandere reading in which obsessive love and barely controlled madness are directly visible, while remaining distinguishable from an ordinary caregiver, generic jealousy, detached surveillance, or a loveless slasher portrait.

## What changed after the initial review

- The runtime data now has an abstract `yandere` character-response profile and a hard `yandere_affection_control_relation` visual profile.
- The visual profile requires one identifiable adult counterpart, visible affection or care, one concrete boundary or access-control action, and an already-visible consequence for the same counterpart.
- A restrained expression contrast—such as a tender asymmetric mouth with overfocused attention and faint lower-lid tension—is supporting evidence rather than the definition.
- Role and horror shortcuts remain insufficient by themselves, but they are not excluded: a syringe, weapon, non-graphic blood, red light, or heart motif may amplify the obsessive-love reading when the character's affection, fixation, and instability are already visible.
- Generic `same_target`, `contrasts`, and `temporal_order` relations now pass through the v6 core and compiled character-response contract.

## 2026-08-18 outward-legibility update

The follow-up source review found no universal yandere face, hairstyle, eye color, costume, palette, or pose. Official character materials and the small research literature instead converge on a target-conditioned pattern: unusually concentrated affection toward one person, exclusivity or abandonment sensitivity, and monitoring or access control. Manga hearts, spiral irises, face shadow, blood, weapons, and red light are conventional genre signs or horror amplifiers, not sufficient archetype evidence. The full ledger and limitations are in `yandere-outward-20260818/source-research.md`.

A separately collected 24-image web convenience corpus reached the same production conclusion while also showing the search medium's bias. High fixed gaze, an affection marker, and a weapon-like threat each appeared in 17/24 inspected images, but only 5/24 showed a strict target-directed action and only 2/24 visibly included the target. After mentally removing blood, weapons, and text, only 7/24 remained clearly yandere-coded, 5/24 were ambiguous, and 12/24 no longer read as yandere. These counts describe this deliberately stratified sample, not population prevalence; the full coding table and source URLs are in `yandere-outward-20260818/visual-corpus.md`.

For photographic generation, the authored `yandere_affection_control_relation` profile now separates the durable relation from a stronger **production legibility gate**. The 2026-08-18 requester correction explicitly supersedes the earlier restrained/nonviolent rendering preference:

1. Keep the required same-target affection, boundary/access action, and visible consequence.
2. Add an affiliative face channel: for example, a soft affectionate mouth, restrained warm smile, subtle natural flush, or softened brow and cheek.
3. Add a distinct target-fixation channel: the eyes, head, and body converge on or keep tracking the same adult counterpart.
4. Add a third, mandatory character-centered channel: feverish devotion and ecstatic or barely controlled instability must be directly visible in the eyes, asymmetric mouth, jaw, grip, or forward posture.
5. Make all three outward channels readable together. Direct camera gaze is appropriate when the camera is explicitly the beloved's point of view.
6. Allow non-graphic blood, a visible weapon, a syringe, red clinical light, and heart imagery as intensity amplifiers. Reject only cases where those devices replace the same-target obsessive-love mechanism.

Requiring these outward channels is a prompt-production choice for first-look and thumbnail readability, not a claim that one eye shape or prop is a universal diagnostic feature. The abstract behavior graph remains free of fixed camera, facial geometry, gaze direction, pose, or prop rules. The direct-madness requirement belongs in the visual-obligation registry, where pixel-facing evidence and render gates can be audited without reducing the archetype to an appearance-only label.

## Research synthesis and limits

- The HAI 2023 prototype supports target-conditioned attention and affect change, but its appearance mapping was not validated as a universal recognition recipe.
- The HAI 2024 scale study supports excessive liking, self-sacrifice, jealousy, and possessiveness as related contributors. Its participants reported only moderate familiarity, the authors warn that the measured pattern may not be unique to yandere, and it did not test photographic cues.
- Bruno's character-element analysis supports a sweet outward surface as one convention inside a larger hierarchy; it does not show that an eye shape alone identifies yandere.
- The 2026 anime/manga expression classifier documents illustrated manic-euphoric conventions, but it used one annotator and does not establish photorealistic or relationship-level validity.

Therefore, the durable photographic mechanism remains relational: affection, control, and consequence must all point to the same adult target. For the requested production style, however, the character's face and posture must also make obsessive love and instability unmistakable at first glance. Blood and weapons are legitimate genre amplifiers, not forbidden content and not standalone proof.

## Remaining defects found and resolved

1. The first relation contract bound target, action, and affect leak but omitted the consequence. The corrected `same_target` vector binds `relationship_target`, `surface_affect`, `primary_action`, and `immediate_consequence`.
2. Relation rows previously accepted arbitrary identifiers and treated member order as meaningful. Validation now permits only declared generic axes and causal roles, requires `relationship_target`, rejects duplicates, and compares `same_target` members as an unordered set.
3. An elliptical retry could preserve the concept in lineage while leaving its visual profile as an unselected optional candidate. A preserved parent hard obligation must now be recreated through hash-bound post-core visual intent from an exact current core field.
4. The authorial baseline had a 24–180 word boundary, but the final composed prompt could exceed it. The v5/v6 composed audit now enforces the same boundary.
5. Research rows linked sweet-surface evidence to unrelated menacing-gaze, reflection-horror, and invisible-mood candidates. Those links and direct yandere routing tags were removed, and source-specific limitations were recorded.

## Composition priority for the next render

Use a tight patient-point-of-view close portrait so the adult nurse dominates the frame. Make obsessive love and instability simultaneous: feverishly adoring target-lock, tear-bright widened eyes, flushed cheeks, and an ecstatic asymmetric smile that looks loving and barely controlled. Let an uncapped syringe or another medical weapon remain clearly visible without touching skin, and permit sparse non-graphic blood flecks on her glove, cheek, or uniform. Keep a minimal adult beloved marker—such as a blurred shoulder or recoiling hand—so her attention and the already-visible consequence point to the same target. The direct facial and bodily performance must remain primary; the blood, tool, and lighting amplify it.

## Acceptance gates

1. Text preflight: all frozen evidence is literal, the hard visual profile survives retries, forbidden labels remain out of runtime text, and `prompt_en` is 24–180 words.
2. Thumbnail review: obsessive love and barely controlled madness are immediately readable on the character, with affection and threat directed toward the same target; the frame does not collapse into “ordinary nurse” or “loveless generic horror.”
3. Native-size review: affiliative face signal, target-locked eye-head-body orientation, ecstatic instability, weapon/tool separation from skin, non-graphic blood treatment, adult identity, and reference-face fidelity are intact.
4. Process report: prompt/audit pass, delivery success, pixel legibility, and user acceptance are reported separately.
5. Promotion: no render is marked representative until the requesting user accepts the yandere reading. A passing contract is preflight evidence, not pixel proof.
