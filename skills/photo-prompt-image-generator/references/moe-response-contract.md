# Moe Response Contract

Use this contract when the candidate pack contains `moe_response.enabled: true`. It turns an explicit character-moe request into visible photographic evidence. It does not claim that a viewer will actually feel moe; only the requesting user can make that acceptance judgment.

## Operational Meaning

In this skill, moe has two jointly necessary layers. First, the character must pass an aesthetic entry condition: an unmistakably adult original character who reads as both beautiful/pretty and cute/charming, normally an adult `bishoujo` design when presentation is unspecified, an adult `bishonen` design for an explicitly masculine character, or a beautiful/cute adult androgynous equivalent when requested. Second, a small event must make that particular character newly legible. Beauty or cuteness alone is insufficient, but it is not optional. Adult sexual appeal may strengthen the result and is not inherently opposed to moe; it remains a separate supporting axis. Youth, sexual appeal, costumes, animal ears, blush, kindness, or a shy smile never substitute for either required layer.

Build one causal beat:

`adult pretty+cute character-design entry -> behavioral baseline -> visible trigger/target -> unfinished event phase -> involuntary or costly response -> warm affective leak -> immediate consequence -> character-specific second reading`

The frame should let a viewer infer both the character's usual rule and the instant in which something leaks through it. The consequence must already be visible, but the action must not have collapsed into a settled endpoint.

## Element Hierarchy

- Appearance is the entry gate, not decoration. Give the adult character harmonious refined facial features, lively eyes at realistic adult scale, a softly expressive mouth, well-kept hair, and cohesive styling so the first thumbnail read is both pretty and cute. An ordinary generic casting fails even if the later event is strong.
- Situation establishes the character's ordinary rule and puts one small stake at risk. Prefer an exact local event over a generic job, repair, or kindness scenario.
- Action carries the causal change. Show direction, recipient or target, contact state, and what is not yet complete.
- Expression records a timed leak and must not stop at annoyance, sadness, boredom, or embarrassment. Pair any guarded cue with one specific warm countercue visible on the same face: softened eyes, an almost-smile, one pleased or relieved mouth corner, fondness that briefly escapes, or playful embarrassment. Use no more than two negative-affect cues; a pout plus an averted gaze with no positive countercue is not sufficient.
- Pose makes agency and timing readable. Use weight shift, hand interruption, guarded torso, reach/recoil, or one limb lagging behind the intention; avoid a model pose with props.
- Appearance preserves identity and continuity. Role clothing, nekomimi, or another trait explains who acts; it does not replace the event.
- Style and atmosphere support intimacy and observation through distance, light, material continuity, and focal hierarchy. Unless the user asks for readable text, keep the background plain and unlettered: no menu board, chalkboard writing, signage, captions, pseudo-writing, decorative hearts, sparkles, blush circles, or manga reaction marks.

## Primary Mechanisms

- `denial_care_leak`: a guarded or rejecting front is contradicted by a directed protective act.
- `baseline_break_reveal`: a normally controlled character briefly loses composure in response to a small concrete disruption.
- `earnest_effort_recovery`: effort, error, and immediate recovery expose investment without humiliation.
- `nonhuman_reflex_leak`: a body-rooted nonhuman response happens before deliberate facial or hand control. For ears, show an asymmetric directional relation: one trigger-side ear turns toward the visible cause while the other retains its baseline angle.
- `character_specific_reveal`: a private rule, habit, preference, or ritual becomes legible through one interruption and response.

Use exactly one routed primary mechanism and no more than the routed support mechanisms. A support cue cannot become a second competing scene.

## Relationship Registers

- `peer_liking_under_denial`: required for tsundere. Care may prove that the character acts for the recipient, but concealed liking must point toward one blurred partial outer-eye-plus-temple/profile landmark from the same adult recipient at a named upper frame edge. Turn the primary head and nose three-quarter toward the opposite side; only the irises make a small oblique return to the landmark. Pair softened lower lids with one mouth corner that starts to lift and is immediately flattened. Direct frontal eye contact, a second full face, and head and irises turning together are invalid.
- `nurturant_benevolence`: used for explicit mamang, maternal, motherly, or equivalent care requests. Show mature protective warmth through a relaxed brow, patient soft eyes, reassuring mouth, and calm attention. Do not import active denial or a romantic eye-line contradiction.
- `directed_care_without_role_inference`: used for ordinary requested kindness or care when no mamang, maternal, romantic, or hierarchical relationship is named. Show the concrete care event and mild warmth without silently turning a friend or peer into a mother figure.
- `character_specific_reveal`: default for other moe mechanisms. Do not invent romantic or maternal relation semantics when the request does not establish them.

Relationship semantics outrank compatible presentation or species reflexes. A mamang nekomimi request therefore keeps `quiet_care_trace` and `nurturant_benevolence` as its primary mechanism/register while `nonhuman_reflex_leak` remains optional support; cat ears must never erase the requested maternal reading. Tsundere remains the deliberate exception because its care and peer liking are one coupled contradiction.

## Required Composed Shape

`moe_response_contract/v10` retains the hard compactness boundary: the complete English `prompt_en` must contain 50–120 words. The budget covers the final positive prompt, not `negative_en` or metadata. Reuse the same concise clause as literal evidence for compatible moe, viewer, identity, and augmentation fields; do not concatenate a separate explanatory sentence for every schema field. Version 10 keeps the v9 concealment and identity gates, then makes the affection endpoint visible and directionally testable. For tsundere, a hand, wound, or carried object occupies a lower task anchor while one blurred partial outer eye plus temple/profile sliver from the same adult recipient occupies a named upper frame edge. The primary head and nose turn three-quarter toward the opposite side; only the irises return obliquely to the landmark. Softened lower lids and one mouth corner that begins to lift must both be immediately suppressed. Looking only at the task, direct frontal eye contact, a centered or selfie-like viewer gaze, generic side-eye, an imagined off-frame eye line, a second full face, head and irises turning together, or benevolent maternal warmth no longer stands in for concealed tsundere affection. Explicit mamang or maternal requests instead route to `nurturant_benevolence`, where relaxed brows, patient soft eyes, a reassuring mouth, and calm protective attention are desirable rather than a failure. Identity-controlled v10 retains eye aperture, face length, lower-face/jaw width, adult-age continuity, and no dollification as hard render-promotion gates.

```json
{
  "moe_response": {
    "aesthetic_baseline": "adult_bishoujo | adult_bishonen | adult_beautiful_cute_character",
    "mechanism": "one routed primary mechanism",
    "relationship_register": "peer_liking_under_denial | nurturant_benevolence | directed_care_without_role_inference | character_specific_reveal",
    "baseline": "the character's ordinary rule",
    "event_phase": "an unfinished transition",
    "trigger": "the visible cause",
    "target": "the visible person or object affected",
    "visible_response": "face, gaze, hand, posture, or reflex evidence",
    "immediate_consequence": "a visible state change already underway",
    "continuity": "adult role and identity anchors that remain stable",
    "support_mechanisms": [],
    "prompt_evidence": {
      "actor_phrase": "literal prompt substring",
      "aesthetic_baseline_phrase": "literal adult plus pretty and cute design substring with at least two concrete face/hair/style details",
      "active_denial_phrase": "required for denial_care_leak: literal visible mouth, chin, shoulder, or helping-hand protest",
      "care_action_anchor_phrase": "required for denial_care_leak: recipient hand, wound, or carried object visibly low in-frame",
      "relationship_gaze_anchor_phrase": "required for denial_care_leak: one blurred partial outer eye plus temple/profile sliver from the same adult recipient at a named upper frame edge",
      "concealed_affection_phrase": "required for denial_care_leak: named three-quarter head and nose turn toward the side opposite the landmark, only the irises returning obliquely, softened lower lids, and one starting mouth-corner lift immediately suppressed",
      "benevolent_affect_phrase": "required for nurturant_benevolence: relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention in one literal expression phrase",
      "affective_leak_phrase": "literal warm or pleased facial micro-response that counters guarded or negative affect",
      "background_control_phrase": "literal plain or unlettered background instruction without text or symbolic shorthand",
      "baseline_phrase": "literal prompt substring",
      "event_phase_phrase": "literal prompt substring",
      "trigger_phrase": "literal prompt substring",
      "target_phrase": "literal prompt substring",
      "visible_response_phrase": "literal prompt substring",
      "immediate_consequence_phrase": "literal prompt substring",
      "continuity_phrase": "literal prompt substring",
      "focal_plane_phrase": "literal prompt substring",
      "reference_identity_phrase": "conditional literal substring preserving eye aperture/shape/spacing, face length, lower-face/jaw width, other facial anchors, and adult age with explicit no-enlarging/no-rounding/no-shortening/no-narrowing clauses"
    }
  }
}
```

Bind the routed aesthetic baseline literally before the event description. The phrase must establish explicit adulthood, both pretty/beautiful and cute/charming first-read qualities, and at least two concrete character-design details such as face, eyes, mouth, hair, or cohesive styling. Preserve the routed `relationship_register`; warmth is not interchangeable across archetypes. For `denial_care_leak`, bind `active_denial_phrase` separately with a visible mouth, chin, shoulder, or helping-hand protest; guardedness, `tsundere`, side-eye, or an averted gaze alone does not qualify. Bind `care_action_anchor_phrase` to the recipient's visible hand, wound, or carried object at a named lower screen position. Bind `relationship_gaze_anchor_phrase` separately to one blurred partial outer eye plus temple/profile sliver from the same adult recipient at a named upper frame edge. Then bind `concealed_affection_phrase` as one continuous geometry: a named three-quarter head turn points the nose toward the side opposite the landmark; only the irises or pupils make a small oblique return to it; the lower lids soften; one mouth corner starts to lift and is suppressed. All visual facts are required. Direct frontal eye contact is too overt; looking only at the hand or object reads as care; a second full face competes; head and irises turning together reads as a generic side-look; generic warmth, maternal benevolence, or a generic side-eye does not prove peer liking. For an explicit mamang or maternal request, route to `nurturant_benevolence` and bind `benevolent_affect_phrase` with all four concrete cues: relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention. Do not import active denial or romantic gaze leakage. Ordinary care requests instead use `directed_care_without_role_inference`, so friendliness alone never invents motherhood. Bind `affective_leak_phrase` separately again, then bind `background_control_phrase` as a plain wall, unlettered material surface, or text-free bokeh unless the request explicitly needs readable text. Keep face/gaze, hand/posture, and trigger/target in one close or medium focal plane. Name an unfinished event and one concrete physical separation. If all required evidence does not fit within 120 words, simplify the event or remove optional augmentation; do not expand the budget.

## Aesthetic Routing

- Explicit feminine presentation routes to `adult_bishoujo`.
- Explicit masculine presentation routes to `adult_bishonen`.
- Explicit androgynous, nonbinary, or gender-neutral presentation routes to `adult_beautiful_cute_character` without forcing femininity or masculinity.
- Gender-unspecified explicit moe routes default to `adult_bishoujo`; this default is local to moe and must never affect ordinary non-moe photographs.

These are adult character-design categories, not literal age labels. Say `adult woman`, `adult man`, or `adult character`, preferably `mid-twenties or older`, rather than `girl`, `boy`, or a school-age term. “Bishoujo-inspired” and “bishonen-inspired” describe the polished beauty/cuteness read, while the prompt retains realistic adult eye scale and adult morphology.

## Fixed-Identity Evaluation

Use `--reference-edit-mode identity` when a supplied fictional adult portrait should hold casting constant across prompt tests. The resulting candidate pack exposes `reference_identity_control` and requires `reference_identity_phrase` in the composed prompt.

Treat the portrait as the sole identity source. Preserve facial geometry, eye aperture/shape/spacing, eyebrows, nose, lips, face length, lower-face and jaw width, cheekbones, skin tone and natural asymmetry, hairline, and adult age. State the anti-reshape boundary literally: no enlarging or rounding the eyes, shortening the face, narrowing the jaw, substituting or averaging another face, structural beautification, dollification, or de-aging. Change only the requested micro-expression, pose, outfit, lighting, and setting. This means the adult pretty-and-cute gate must be achieved through the preserved person's expression, grooming, styling, pose, and light rather than a different “prettier” face.

At pixel review, compare the source portrait, the current user-preferred baseline when one exists, and the new result before evaluating the moe direction. Adult age, same-person identity, eye aperture/shape/spacing, face length, lower-face/jaw width, and no de-aging or dollification are hard gates. A failure is retained as evidence but cannot be promoted as the representative candidate, even when it appears prettier or cuter. Identity preservation is a control condition, not proof of moe; the user still decides whether the qualified expression and scene are more moe.

## Adult Sexual-Tone Axis

Adult age and sexual tone are independent. Explicit nonsexual wording routes to `sexual_tone: nonsexual`, disables the configured sensual-editorial and fetish-fashion defaults, and keeps the subject explicitly adult. A plain adult-moe request routes to `sexual_tone: sensual_optional`: it may retain the eligible-human low-intensity sensual-editorial default as a subordinate cue while fetish fashion stays off. Explicit adult sensual wording routes to `sexual_tone: sensual` and may strengthen that cue under visible agency. Do not infer a stronger sexual tone from gender, body, clothing, role, or market convention.

Never use childlike proportions, baby-face direction, oversized eyes, school-age coding, or age ambiguity as moe evidence. Nonsexual does not mean sterile: closeness, warmth, embarrassment, reciprocity, or tactile care can remain. `sensual_optional` does not mean body-first: gaze, posture, silhouette, fabric, or lighting may add adult appeal only after the pretty-and-cute face and character-specific response remain dominant.

## Nekomimi Is Not Full Beastkin

Natural `네코미미`, `猫耳`, and `cat-eared` requests route to a human adult with compact living cat ears. Require organic roots in the hairline and, when relevant, a visible ear reflex. Each ear must be no taller than the visible human ear from base to tip. Do not leave both ears symmetrically upright: place the trigger in-frame, turn only the nearer or trigger-side ear toward it, and explicitly put the other ear tip at a clearly different baseline angle. Keep ordinary human forearms, hands, nails, face, and proportions. Do not add furry limbs, paw hands, long claws, a muzzle, full-body fur, oversized ears, or a tail unless the user asks for fuller beastkin anatomy.

`수인`, `獣人`, and explicit beastkin or kemonomimi requests may use the broader species-family contract. Do not silently upgrade nekomimi into that body plan.

## Failure Patterns

Reject or repair these outcomes:

- generic casting: an ordinary adult with no clearly pretty-and-cute bishoujo/bishonen/equivalent character-design read;
- aesthetic-only: an attractive adult in a costume or with ears, but no character-revealing event;
- endpoint collapse: a cup already handed over, a mistake already fixed, or an arrangement already restored;
- generic kindness: a helpful act with no baseline contradiction, cost, leak, or character-specific rule;
- label substitution: `cute`, `moe`, blush, ears, hearts, or a smile used as the evidence;
- affective collapse: a pout, scowl, averted gaze, sadness, or boredom dominates the face without one specific warm or pleased countercue;
- collapsed relationship vector: the character looks only at the hand, wound, object, or care task, so generic or maternal nurturance is mislabeled as tsundere liking;
- unverifiable affection vector: the recipient exists only as an off-frame eye line, a second full face competes with the primary subject, or the head and irises turn together instead of opposing each other around a visible partial recipient landmark;
- overexposed affection vector: the face and nose point at the lens with direct frontal eye contact, so liking reads as an open viewer-facing gaze instead of an involuntary oblique leak;
- identity beautification drift: eye aperture grows or rounds, the face shortens, the lower face or jaw narrows, or adult morphology becomes doll-like even though the result looks prettier;
- background shorthand: decorative hearts, sparkles, menu lettering, signage, or pseudo-writing competes with the face and causal event;
- body-first substitution: sensual pose, cleavage emphasis, or fetish clothing becomes the main evidence while the pretty-and-cute face or character-specific response weakens;
- overpacked causality: several independent actions, reactions, and props competing in one still frame;
- role replacement: the mechanism changes a maid, guard, barista, or other requested role into a generic model;
- nonhuman overreach: nekomimi becomes a furry-limbed or clawed beastkin without explicit instruction.

## Review Boundary

The composed-prompt audit is fail-closed preflight. A manual concept gate with literal evidence may pass preflight only as `pixel_review_required`; it is never automatic proof that organic ear roots, a contradiction, or event timing survived rendering.

Review generated pixels twice:

1. At thumbnail size, verify adult/role identity, pretty-and-cute facial entry, one warm affective leak, focal hierarchy, trigger, response, and consequence are recoverable without reading metadata. For tsundere, require the small blurred partial recipient landmark and reject direct frontal eye contact or a same-direction side-look: the three-quarter head turn must oppose the landmark while only the irises return, and softened lower lids plus the suppressed starting mouth-corner lift must survive. Reject a face whose dominant read is merely annoyed, sad, bored, blank, openly affectionate, or viewer-facing.
2. At native size, verify identity hard gates first—eye aperture/shape/spacing, face length, lower-face/jaw width, and adult-age continuity—then hands, contact state, event phase, species anatomy and ear scale, the requested sexual tone, a text-free background when text was not requested, and the absence of unrequested visual shorthand. Any identity hard-gate failure blocks representative promotion.

Record technical and causal qualification separately from user preference. An agent may say the scene is readable or that a specific defect remains; it must not declare the image moe or better on the user's behalf.

For a saved candidate, use the pack's `render_qualification.required_hard_gates` as the complete review checklist and validate it with `scripts/audit_moe_render_review.py`. Every gate needs an exact `pass` or `fail` plus image-grounded evidence; a partial observation blocks representative promotion. Technical success alone yields `pending_requesting_user_judgment`. Representative eligibility additionally requires a direct requesting-user acceptance of genuine moe and, when a comparison baseline exists, improvement over that baseline. The review source and faithful decision summary are required as explicit provenance, but the JSON auditor cannot authenticate the speaker; populate those fields only from the actual conversation.
