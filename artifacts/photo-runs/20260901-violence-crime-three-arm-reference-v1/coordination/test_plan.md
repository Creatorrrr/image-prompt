# Independent three-arm render test

The coordinator froze the source snapshot, random assignment, and rubrics before any arm received another arm's prompt, candidate pack, or image.

Common rules:

- Each arm authors one random complex fictional concept around only its assigned hard profile.
- Complexity must add at least four independent scene dimensions such as era, occupation, weather, location, camera, crowd behavior, architecture, wardrobe, or documentary mode.
- The added complexity must not replace or soften the assigned four-part relation.
- The supplied portrait is a reference for visible adult appearance only and is used for an adult witness, investigator, responder, negotiator, or other non-accused supporting role. It is not evidence about the real person and must not be used as a minor.
- Each arm freezes its authorial core and pixel rubric before candidate-pack retrieval.
- Each arm produces a v6 candidate pack, composed prompt, prompt audit, render request, render-request audit, one built-in image generation call, run ledger, native image, thumbnail, and independent pixel review.
- No arm may inspect or reuse a sibling arm's prompt, candidate pack, test case, image, review, or messages.
- One native image generation only; no semantic repair or aesthetic retry. A tool block is recorded as blocked, not converted into a quality score.
- `partial_is_fail`: every assigned hard gate and every common reference/technical gate must pass. Prompt PASS is not pixel PASS, and user preference remains unscored.

Assigned hard rubrics:

## Arm 01 — `robbery_forced_property_transfer`

1. Adult offender and specific adult property holder remain clearly distinct.
2. Force or a credible directed threat compels the taking.
3. The targeted property visibly begins under the victim's control.
4. The same property visibly moves toward the offender's possession or control.

## Arm 02 — `deliberate_arson_causality`

1. An adult fire-setter and one selected property target remain visible.
2. A coherent ignition-source path reaches one target point.
3. Fresh burning visibly originates at the same deliberate ignition point.
4. New flame, smoke, or scorching expands outward from that point.

## Arm 03 — `declared_minor_targeted_crime_relation`

1. The authorial core explicitly declares the victim under eighteen; age is not inferred from appearance alone.
2. An identifiable adult offender specifically targets that declared minor.
3. One named concrete nonsexual crime is visibly underway rather than implied by mood.
4. A same-event consequence, escape, or protective intervention trace is visible.
5. The supplied adult portrait may guide only an adult supporting role and must not be mapped to the declared minor or offender.

Common pixel gates:

1. The reference-guided adult supporting role visibly preserves long center-parted dark wavy hair, oval facial geometry, dark eyes, and softly arched brows without claiming identity.
2. Reference-guided adult appearance remains secondary to, and does not obscure, the assigned criminal-event relation.
3. Actor, target, mechanism, and result remain readable at thumbnail scale.
4. Contact, ownership, origin, boundary, or status details required by the profile remain readable at native scale.
5. No extra watermark or unintended text is required for a pass; if exact text is used as evidence, its legibility is scored explicitly.
