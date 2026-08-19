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
4. The authorial baseline had a 24–180 hard boundary, and the final composed audit later copied that same fixed cap. The current versioned budget keeps 24–320 as absolute bounds, treats 180 as an advisory target, and expands the advisory ceiling for literal hard evidence rather than forcing semantic compression.
5. Research rows linked sweet-surface evidence to unrelated menacing-gaze, reflection-horror, and invisible-mood candidates. Those links and direct yandere routing tags were removed, and source-specific limitations were recorded.

## Composition priority for the next render

The facial contract now separates five production modes instead of stacking every convention into one face:

1. **Sweet-threat mismatch:** a warm or tender mouth conflicts with overfocused, lower-lid-tense eyes.
2. **Dead-eye devotion:** exact beloved-directed target lock, dim but physically coherent catchlights, flattened low-contrast irises, and a tender mouth.
3. **Ecstatic face cradle:** both palms support the cheeks and jaw while blush and an adoring gaze remain directed to the same beloved.
4. **Manic possessiveness:** wide sclera and small pupils amplify danger but do not prove affection or possession by themselves.
5. **Abandonment fracture:** moist eyes and a tightening mouth visibly react to the same beloved withdrawing.

Select exactly one primary mode per still. Treat pupil scale, iris scale, gaze focus, catchlight state, and iris contrast as independent variables: “dead eyes” are not synonymous with dilated pupils, and a vacant gaze cannot count as beloved-directed target lock. In photorealism, do not demand impossible zero catchlight under a bright source; use dim, scene-coherent catchlights and reduced iris contrast. A broad grin can erase the eye-mouth contradiction, so prefer a small asymmetric tender smile when testing the mismatch or dead-eye modes.

The first three patient-point-of-view render attempts established an important pixel-level failure mode. The adult nurse, capped syringe, far-trolley call button, reaching patient hand, cable, visible gap, and identity all became readable, but the face repeatedly collapsed into a calm beauty portrait: detailed bright irises, strong attractive catchlights, relaxed lids, and a softly tilted head outweighed the authored dead-eye language. Prompt/audit success therefore did not prove facial madness.

The next repair test keeps the successful third scene as an edit target and changes the face only. It selects **sweet-threat mismatch** rather than stacking another dead-eye instruction: a small closed-lip asymmetric tender smile, nearly upright head, slightly elevated upper lids, taut lower lids, almost motionless brow, pale matte low-contrast irises, and one tiny dim scene-coherent catchlight per eye. The same adult patient's reach is the visible trigger; the smile deepens by a fraction while the eyes remain precisely fixed and unchanged. This target-triggered divergence is stronger than a static adjective because the mouth communicates genuine affection while the nonreactive eye system communicates overcontrol.

The repair preserves every previously passing action and identity gate. Large sparkling catchlights, bright detailed beauty irises, a broad friendly smile, relaxed lids, a playful head tilt, or simultaneous movement of both mouth and eyes are recorded as false substitutes for this selected mode. These are request-scoped production controls, not a claim that one facial configuration universally defines the archetype.

## 2026-08-19 face-only forward-test result

Two bounded native edits tested the repaired data against the successful third scene. Attempt 1 preserved identity, the capped syringe, the pinned call button, the reaching patient hand, cable, gap, framing, and background, but its bright detailed irises, prominent beauty catchlights, relaxed lids, friendly mouth, and head tilt still read as a gentle beauty portrait. Attempt 2 changed only the eye region. It successfully produced paler matte irises, lower internal iris contrast, and smaller dimmer catchlights while preserving every scene invariant.

Attempt 2 still failed the first-look madness gate. This isolates a reusable lesson: **eye micro-texture is not enough**. The selected facial mode needs meso-scale mechanics—slightly elevated upper lids, taut lower lids, an almost motionless brow, a near-upright head, and a visibly unfinished one-corner mouth change—to survive together. If the lids, head angle, and mouth remain socially friendly, pale irises merely create a soft fantasy-eye beauty effect.

The test also exposes a still-image observability boundary. “The mouth changed while the eyes did not” is a temporal claim that one photograph cannot prove by itself. Future composition data therefore freezes an observable unfinished state: the same target's reaching or withdrawing movement remains visible, one mouth corner is caught partway through a fractional deepening, and the eyes remain fixed. This is an optional production translation of the relationship event, not a new universal definition or a standalone archetype gate.

## Acceptance gates

1. Text preflight: all frozen evidence is literal, the hard visual profile survives retries, forbidden labels remain out of runtime text, and `prompt_en` stays within the absolute 24–320 word bounds; exceeding the default 180-word target is reported as an advisory warning.
2. Thumbnail review: obsessive love and barely controlled madness are immediately readable on the character, with affection and threat directed toward the same target; the frame does not collapse into “ordinary nurse” or “loveless generic horror.”
3. Native-size review: affiliative face signal, target-locked eye-head-body orientation, ecstatic instability, weapon/tool separation from skin, non-graphic blood treatment, adult identity, and reference-face fidelity are intact.
4. Process report: prompt/audit pass, delivery success, pixel legibility, and user acceptance are reported separately.
5. Promotion: no render is marked representative until the requesting user accepts the yandere reading. A passing contract is preflight evidence, not pixel proof.
