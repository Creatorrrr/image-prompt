# Series and Selection

## Choose the series length

Use 6, 8, or 10 frames. Default to 8 when the user asks for a series without a count.

- 6 frames: compressed proposition with little redundancy.
- 8 frames: balanced arc with place, self-presentation, relationship, detail, habit, distance, and open ending.
- 10 frames: additional transition or counterpoint frames justified by the thesis.

Do not treat a series as repeated variants of one hero image.

## Series thesis

Write one sentence that names:

- the particular subject
- the necessary place or route
- the viewer relationship
- the state transition across the sequence
- the question the ending keeps open

Every frame must advance, complicate, or recontextualize the thesis.

## Continuity lock

Freeze before writing frames:

    subject_identity:
    recurring_individuality_anchors:
    core_clothing_and_hair:
    place_geography:
    recurring_objects:
    viewer_role:
    base_camera_language:
    light_and_time_progression:
    color_and_texture_behavior:
    exclusions:

A frame may vary focal length, crop, angle, and distance only when the change has a narrative role. Keep identity, object state, room geography, and time progression coherent.

## Default eight-frame arc

1. The door of the place: establish the threshold, routine, or social environment before intimacy.
2. Chosen self-presentation: show how the subject would willingly present themself.
3. Social role begins to move: an object, clothing cue, or routine enters action.
4. Relationship becomes visible: gaze, distance, or response reveals who holds the camera.
5. Symbolic detail: one part or object compresses role, time, and action.
6. Personal habit: a repeated gesture or use mark makes the subject non-interchangeable.
7. Return to distance: the environment reframes the earlier intimacy.
8. Open ending: a next action is possible but not completed.

For 6 or 10 frames, combine or expand roles without losing the arc.

## Frame record

For each frame, specify:

    frame_number:
    narrative_role:
    primary_sir_axis:
    secondary_sir_axis:
    psychological_distance:
    aspect_ratio:
    focal_length:
    previous_action:
    current_transition:
    next_action:
    meaning_core:
    environment_cues:
    shot_delta:

Shot Delta must identify exactly what changes from the previous frame and why. Examples: distance increases to restore uncertainty; the face disappears so the object carries meaning; the room becomes legible after an intimate frame; direct awareness briefly appears.

## Prompt strategy

Create:

- one shared continuity block
- one shared negative prompt
- one concise per-frame prompt containing only the role and shot delta

Repeat identity-critical and geography-critical anchors as needed. Do not let repetition turn all frames into the same crop.

## Selection

Select by narrative role rather than by standalone attractiveness. Ask:

- Does the opening establish a real place and threshold?
- Is at least one frame close to the subject's chosen self-presentation?
- Does one frame reveal the viewer relationship?
- Does one detail frame compress meaning rather than merely crop?
- Does a habitual gesture or personal trace recur?
- Does the sequence vary distance and information density?
- Does the last image stay open without feeling arbitrary?

Reject beautiful frames that duplicate a stronger role or break continuity.

## Sequence

Arrange for changing knowledge, not a mechanical wide-medium-close pattern. A useful rhythm is:

place -> self-presentation -> role in motion -> relationship -> symbolic detail -> habit -> restored distance -> unresolved next action.

The viewer should know more by the end while still having one meaningful question.

