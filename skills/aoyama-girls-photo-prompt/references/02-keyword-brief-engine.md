# Keyword Brief Engine

## 1. Freeze the authored core

Copy the user's explicit anchors before interpretation. Classify each as:

- person or social role
- place
- viewer relationship
- action or gesture
- object
- visual state or mood
- state change
- time or season
- clothing or appearance
- composition, lens, light, aspect ratio, or medium

An explicit anchor is locked unless the user asks to revise it. An open dimension may be inferred. Keep assumptions minimal and visible.

## 2. Normalize without flattening

Expand synonyms only to clarify a visual obligation. Preserve culturally or emotionally specific wording. Do not translate a concrete noun into an aesthetic category, and do not turn a relationship into a generic candid-camera label.

If the input is only a few words, infer ordinary, lived-in specifics before spectacle. Add no extra character or decorative subplot unless the keyword logically requires one.

## 3. Generate three theme candidates

Each candidate must answer WHO, WHERE, HOW, and WHY NOW in one sentence. Vary meaning, not cosmetic styling.

Score each candidate:

| Criterion | Points |
|---|---:|
| Person and place feel necessary rather than interchangeable | 25 |
| Individuality can become visible anchors | 20 |
| Viewer relationship changes the frame | 20 |
| State A to B creates a transition moment | 15 |
| Theme translates clearly into one image | 10 |
| Scene can remain formally restrained | 10 |

Select the highest-scoring candidate. When scores are close, prefer the candidate that preserves more literal user anchors and requires fewer assumptions.

## 4. Define the state transition

Write:

    state_a: the condition immediately before
    trigger: the small event that changes attention or posture
    state_b: the condition beginning to emerge
    shutter_phase: just_before | in_transition | just_after

Avoid an emotion with no visible carrier. Attach the change to a hand, gaze, posture, object, airflow, sound response, door, machine, light shift, or other photographable event.

## 5. Define the viewer

Choose a relational role rather than a camera label:

    viewer_role:
      type: close friend | colleague | family member | invited visitor | quiet observer
      intimacy: 0.0-1.0
      authority: 0.0-1.0
      subject_awareness: how the camera is acknowledged
      psychological_distance: breath-close | conversational | across-room | remote

The role must affect viewpoint, gaze, body orientation, and framing.

## 6. Select three individuality anchors

Use one anchor from at least two of these categories:

- face or expression
- hand, posture, or habitual gesture
- personal object or evidence of use
- self-styled clothing or hair
- small irregularity in the room or routine

Write anchors as observable details. Replace abstract personality claims with visible evidence.

## 7. Build SIR

    sir:
      symbolicity: social role, season, place, time, or routine
      individuality: three selected anchors
      relationship: viewer role, distance, awareness, or gaze
      primary_axes: the two axes most legible in this frame

Do not force equal emphasis. Decide which two axes lead and which remains supporting context.

## 8. Choose the meaning core

Identify the single gesture, object interaction, expression change, or meaningful detail from which the frame should expand.

For each possible contextual addition, ask:

    meaning_gain > distraction_gain

Add it only when true. Stop when the image already communicates the theme.

## 9. Apply an information budget

Default maximums for one frame:

    environment_budget:
      primary_place: 1
      social_or_seasonal_cues: 2
      personal_irregularity: 1
      decorative_props: 0

These are guidance, not a mechanical quota. A prop should establish place, role, action, time, individuality, or relationship. Remove it when it only makes the scene prettier.

## 10. Emit an internal brief

Before compiling the prompt, form:

    mode:
    locked_user_anchors:
    assumptions:
    theme_sentence:
    who:
    where:
    viewer_role:
    state_a:
    trigger:
    state_b:
    shutter_phase:
    individuality_anchors:
    sir:
    meaning_core:
    previous_action:
    current_action:
    next_action:
    controlled_question:
    environment_budget:
    requested_technical_constraints:

The brief is a reasoning artifact. Present only the user-facing parts required by the output contract.

