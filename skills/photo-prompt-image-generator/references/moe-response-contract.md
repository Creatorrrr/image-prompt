# Moe Response Contract

For the normal v6 workflow, use `character_response` when the candidate pack contains `photo-character-response/v1`. Its semantics were authored and frozen in `photo-authorial-core/v3`; do not run the raw moe router or use any named-archetype mechanism/register below to reinterpret them. The rest of this document beginning with “Requester-First V5 Precedence” applies only to compatibility packs that contain `moe_response.enabled: true`.

## Typed V6 Character Response

Copy the contract's nine `frozen_evidence` phrases into the final prompt exactly: actor, baseline, trigger, target, primary action, affect leak, visible response, immediate consequence, and continuity. Keep the declared semantic axes intact, use one primary action and exactly one primary affect-leak channel, and do not invent a relationship, emotion, gaze geometry, face landmark, pose, or story endpoint. `advisory_retrieval.candidates` are optional unordered support; they may all be rejected and can never replace or harden frozen evidence.

A `concept_profile` candidate comes from contrastive BM25F over one data-authored meaning and its data-authored confounders. Its `semantic_consistency` reports only whether the frozen typed assertion matches the profile's abstract axes and relations. `incomplete` and `conflicting` are diagnostics, not instructions to add missing geometry or rewrite the baseline; `consistent` is not a render gate. `conflicting` and `superseded_by_requester_definition` make the candidate `diagnostic_only`, suppress all linked behavior support, and forbid legacy fallback. Behavior-support candidates may come only from an eligible retained profile's optional runtime-node links, and all retrieval scores, ranks, matched terms, frequencies, and vectors remain private.

The composed object binds this without exposing retrieval scores:

```json
{
  "character_response": {
    "source_contract_sha256": "<character_response.canonical_sha256>",
    "evidence": {
      "actor_phrase": "<exact frozen phrase>",
      "baseline_phrase": "<exact frozen phrase>",
      "trigger_phrase": "<exact frozen phrase>",
      "target_phrase": "<exact frozen phrase>",
      "primary_action_phrase": "<exact frozen phrase>",
      "affective_leak_phrase": "<exact frozen phrase>",
      "visible_response_phrase": "<exact frozen phrase>",
      "immediate_consequence_phrase": "<exact frozen phrase>",
      "continuity_phrase": "<exact frozen phrase>"
    },
    "selected_advisory_candidate_ids": []
  }
}
```

The composed audit requires every evidence value to remain byte-identical to the core and literal in `prompt_en`. A BM25F or embedding hit is never proof that the image expresses the character response. Rendered-pixel review and requester judgment remain separate terminal evidence.

## Requester-First V5 Precedence

When a v5 pack contains `moe_response.intent_precedence`, every semantic default below is conditional. `photo-downstream-intent-precedence/v1` declares each rule's affected dimensions and activates it only when all of them are explicitly listed in `intent_lock.open_dimensions`. A locked or otherwise non-open dimension suppresses the corresponding positive instruction, negative-prompt term, evidence duty, and render gate. Locked evidence must exactly reuse the matching semantic-anchor phrase; evidence on another non-open dimension must already occur in the frozen baseline. The composed audit recomputes these states from the immutable core.

Consequently, a generic warm-affect countercue, pretty/cute styling treatment, recovery beat, character-response mechanism, background-text suppression, or sensual-support default may never repair or reinterpret a closed requester meaning. If expression is closed, do not add softened eyes, a smile, warmth, embarrassment, a negative-affect limit, or a later emotional recovery unless the frozen baseline already contains it. If style, text, appearance, event, relationship, or sexual tone is closed, apply the same rule to that dimension. This is a general dimension boundary, not an exception list for named topics. Explicit request-derived obligations still apply, but only as realizations of the same frozen anchors.

## Operational Meaning

In this skill, moe has two jointly necessary layers. First, the character must pass an aesthetic entry condition: an unmistakably adult original character who reads as both beautiful/pretty and cute/charming, normally an adult `bishoujo` design when presentation is unspecified, an adult `bishonen` design for an explicitly masculine character, or a beautiful/cute adult androgynous equivalent when requested. Second, a small event must make that particular character newly legible. Beauty or cuteness alone is insufficient, but it is not optional. Adult sexual appeal may strengthen the result and is not inherently opposed to moe; it remains a separate supporting axis. Youth, sexual appeal, costumes, animal ears, blush, kindness, or a shy smile never substitute for either required layer.

When the causal-event and affective defaults are active, build one causal beat:

`adult pretty+cute character-design entry -> behavioral baseline -> visible trigger/target -> unfinished event phase -> involuntary or costly response -> warm affective leak -> immediate consequence -> character-specific second reading`

When either default is suppressed, replace its stage with the corresponding frozen requester anchor; do not fill the gap with a new generic beat.

The frame should let a viewer infer both the character's usual rule and the instant in which something leaks through it. The consequence must already be visible, but the action must not have collapsed into a settled endpoint.

## Element Hierarchy

- Appearance is the entry gate, not decoration. Give the adult character harmonious refined facial features, lively eyes at realistic adult scale, a softly expressive mouth, well-kept hair, and cohesive styling so the first thumbnail read is both pretty and cute. An ordinary generic casting fails even if the later event is strong.
- Situation establishes the character's ordinary rule and puts one small stake at risk. Prefer an exact local event over a generic job, repair, or kindness scenario.
- Action carries the causal change. Show direction, recipient or target, contact state, and what is not yet complete.
- When `affective_balance_default` is active, expression records a timed leak and must not stop at annoyance, sadness, boredom, or embarrassment. Pair any guarded cue with one specific warm countercue visible on the same face and use no more than two negative-affect cues. When it is suppressed, neither the countercue nor the negative-affect cap applies; expression comes only from the frozen baseline and requester anchors.
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
      "aesthetic_baseline_phrase": "conditional: literal adult plus pretty and cute design substring when the aesthetic-style default is active",
      "active_denial_phrase": "required for denial_care_leak: literal visible mouth, chin, shoulder, or helping-hand protest",
      "care_action_anchor_phrase": "required for denial_care_leak: recipient hand, wound, or carried object visibly low in-frame",
      "relationship_gaze_anchor_phrase": "required for denial_care_leak: one blurred partial outer eye plus temple/profile sliver from the same adult recipient at a named upper frame edge",
      "concealed_affection_phrase": "required for denial_care_leak: named three-quarter head and nose turn toward the side opposite the landmark, only the irises returning obliquely, softened lower lids, and one starting mouth-corner lift immediately suppressed",
      "benevolent_affect_phrase": "required for nurturant_benevolence: relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention in one literal expression phrase",
      "affective_leak_phrase": "conditional: literal warm or pleased facial micro-response only when affective_balance_default is active",
      "background_control_phrase": "conditional: literal plain or unlettered background instruction only when the text default is active",
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

Bind exactly the fields listed by `prompt_binding.required_evidence_fields`; the list is authoritative. When the aesthetic-style default is active, bind the routed aesthetic baseline literally before the event description. Preserve explicit routed relationship semantics without inventing a new relation. Request-derived `denial_care_leak`, `nurturant_benevolence`, and ordinary-care fields retain their typed evidence requirements, but any locked-dimension phrase must exactly reuse its matching requester anchor. Bind `affective_leak_phrase` only when present in the required list, and bind `background_control_phrase` only when present. When the generic causal mechanism is suppressed, the frozen authorial-core event replaces the behavioral-baseline/trigger/target/recovery schema; do not invent those fields. Keep any required face/gaze, hand/posture, and target evidence in one close or medium focal plane. If all required evidence does not fit within 120 words, remove optional augmentation; never alter the requester meaning or expand the budget.

## Aesthetic Routing

- Explicit feminine presentation routes to `adult_bishoujo`.
- Explicit masculine presentation routes to `adult_bishonen`.
- Explicit androgynous, nonbinary, or gender-neutral presentation routes to `adult_beautiful_cute_character` without forcing femininity or masculinity.
- Gender-unspecified explicit moe routes default to `adult_bishoujo` only on legacy packs or when the v5 style dimension is explicitly open; otherwise the frozen requester subject/style remains unchanged.

These are adult character-design categories, not literal age labels. Say `adult woman`, `adult man`, or `adult character`, preferably `mid-twenties or older`, rather than `girl`, `boy`, or a school-age term. “Bishoujo-inspired” and “bishonen-inspired” describe the polished beauty/cuteness read, while the prompt retains realistic adult eye scale and adult morphology.

## Fixed-Identity Evaluation

Use `--reference-edit-mode identity` when a supplied fictional adult portrait should hold casting constant across prompt tests. The resulting candidate pack exposes `reference_identity_control` and requires `reference_identity_phrase` in the composed prompt.

Treat the portrait as the sole identity source. Preserve facial geometry, eye aperture/shape/spacing, eyebrows, nose, lips, face length, lower-face and jaw width, cheekbones, skin tone and natural asymmetry, hairline, and adult age. State the anti-reshape boundary literally: no enlarging or rounding the eyes, shortening the face, narrowing the jaw, substituting or averaging another face, structural beautification, dollification, or de-aging. Change only the requested micro-expression, pose, outfit, lighting, and setting. This means the adult pretty-and-cute gate must be achieved through the preserved person's expression, grooming, styling, pose, and light rather than a different “prettier” face.

At pixel review, compare the source portrait, the current user-preferred baseline when one exists, and the new result before evaluating the moe direction. Adult age, same-person identity, eye aperture/shape/spacing, face length, lower-face/jaw width, and no de-aging or dollification are hard gates. A failure is retained as evidence but cannot be promoted as the representative candidate, even when it appears prettier or cuter. Identity preservation is a control condition, not proof of moe; the user still decides whether the qualified expression and scene are more moe.

## Adult Sexual-Tone Axis

Adult age and sexual tone are independent. Explicit nonsexual wording routes to `sexual_tone: nonsexual`, disables configured sensual-editorial and fetish-fashion defaults, and keeps the subject explicitly adult. A legacy plain adult-moe request may use `sexual_tone: sensual_optional`. V5 may retain that skill default only when sexual tone, style, composition, expression, pose, body geometry, framing, and lighting are all explicitly open; otherwise it is suppressed. Explicit adult sensual wording remains requester-controlled under the frozen core and visible agency. Do not infer a stronger sexual tone from gender, body, clothing, role, or market convention.

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
- affective collapse: when `affective_balance_default` is active, a guarded or negative face lacks its required warm countercue; when it is suppressed, judge only fidelity to the frozen expression anchors;
- collapsed relationship vector: the character looks only at the hand, wound, object, or care task, so generic or maternal nurturance is mislabeled as tsundere liking;
- unverifiable affection vector: the recipient exists only as an off-frame eye line, a second full face competes with the primary subject, or the head and irises turn together instead of opposing each other around a visible partial recipient landmark;
- overexposed affection vector: the face and nose point at the lens with direct frontal eye contact, so liking reads as an open viewer-facing gaze instead of an involuntary oblique leak;
- identity beautification drift: eye aperture grows or rounds, the face shortens, the lower face or jaw narrows, or adult morphology becomes doll-like even though the result looks prettier;
- background shorthand: decorative hearts, sparkles, menu lettering, signage, or pseudo-writing competes with the face and causal event;
- body-first substitution: sensual pose, cleavage emphasis, or fetish clothing becomes the main evidence while the pretty-and-cute face or character-specific response weakens;
- overpacked causality: several independent actions, reactions, and props competing in one still frame;
- role replacement: the mechanism changes a maid, guard, barista, or other requested role into a generic model;
- nonhuman overreach: nekomimi becomes a furry-limbed or clawed beastkin without explicit instruction.

## Request-Scoped Visual Obligations

`photo-visual-obligations/v1` complements this contract when the request's meaning has an exact visual topology or all-of mechanism. Direct terms, profile-local glossary aliases, and frozen `photo-visual-intent/v1` definitions create hard obligations. `photo-visual-concepts/v1` handles indirect component combinations and weak nearby cues without over-activating them: it exposes an optional non-ranked candidate, and only a composed `chosen_visual_concept_ids` selection promotes its immutable opt-in obligation. Neither contract adds a new moe theory or activates from ordinary related objects, excluded homonyms, reference appearance, or inferred personality. Effective profiles translate the request into distinct literal composition evidence, rejected substitutes, runtime-expression policy, and `vo_*` pixel gates. Those gates join the pack-plus-composed derived render checklist; they cannot be kept in an unaudited side list or self-selected by the review record.

Treat composite expressions, object support, pose geometry, body-region salience, corruption transitions, and status-play archetypes as conjunctions. For example, a stable load needs contact, compression, center-of-mass, and hands-clear evidence at once; an embodied transformation needs former state, current state, an on-body boundary, a present choice, and a suppressed relational remnant at once. Passing different components in different attempts is still a failed candidate. The ordinary adult identity, pretty-and-cute entry, causal event, sexual-tone, background, and user-judgment boundaries remain unchanged.

Mamang remains routed by `nurturant_benevolence`, not by a new topic profile: relaxed brow, patient soft eyes, reassuring mouth, calm protective attention, and the visible care consequence already form the reusable mechanism. Add a new visual-obligation profile only when an additional non-substitutable visual topology is actually requested.

## Review Boundary

The composed-prompt audit is fail-closed preflight. A manual concept gate with literal evidence may pass preflight only as `pixel_review_required`; it is never automatic proof that organic ear roots, a contradiction, or event timing survived rendering.

Review generated pixels twice:

1. At thumbnail size, verify the candidate pack's exact required gates without reading metadata. Pretty-and-cute entry, warm affective leak, trigger/recovery causality, or plain background are gates only when `intent_precedence` leaves their rules active or an exact request-derived obligation requires them. A suppressed generic gate must not be reintroduced during review; judge locked expression and event dimensions against their frozen anchors.
2. At native size, verify identity hard gates first—eye aperture/shape/spacing, face length, lower-face/jaw width, and adult-age continuity—then hands, contact state, event phase, species anatomy and ear scale, the requested sexual tone, a text-free background when text was not requested, and the absence of unrequested visual shorthand. Any identity hard-gate failure blocks representative promotion.

Record technical and causal qualification separately from user preference. An agent may say the scene is readable or that a specific defect remains; it must not declare the image moe or better on the user's behalf.

For a saved candidate, derive the complete review checklist from the pack plus the exact audited composed selection and validate it with `scripts/audit_moe_render_review.py --pack ... --composed ... --review ...`. Every gate needs an exact `pass` or `fail` plus image-grounded evidence; a partial observation blocks representative promotion. Technical success alone yields `pending_requesting_user_judgment`. Representative eligibility additionally requires a direct requesting-user acceptance of genuine moe and, when a comparison baseline exists, improvement over that baseline. The review source and faithful decision summary are required as explicit provenance, but the JSON auditor cannot authenticate the speaker; populate those fields only from the actual conversation.
