# Prompt Compiler

## Compiler goal

Translate the internal brief into direct visual instructions that an image generator can execute. Preserve the authored anchors and causal structure. The final prompt should describe one photograph, not explain the methodology.

Do not include:

- internal scores or candidate rankings
- abstract personality claims without a visual carrier
- a photographer's name as a style shortcut
- generic beauty praise that makes the subject interchangeable
- props that were rejected by the information budget
- contradictory lens, light, action, or gaze instructions

## Positive prompt order

Compile in this order:

1. Medium and photographic intent
2. Necessary place and time
3. Particular subject and social or seasonal context
4. Previous action, current transition, and next likely action
5. Viewer role expressed through distance, height, awareness, and gaze
6. Three individuality anchors
7. Primary SIR cues and meaning core
8. Composition, crop, aspect ratio, and focal length with visible consequences
9. Motivated light, exposure, color, and material texture
10. Controlled question or deliberate omission
11. Realism and preservation constraints

Use concrete nouns and verbs. Prefer one precise paragraph to disconnected tag soup.

## Generator-ready template

    A photorealistic, naturalistic editorial photograph of [particular subject]
    in [necessary place and time]. [Previous action]; at the shutter moment,
    [current transition], while [next action remains visibly possible].
    The camera belongs to [viewer role], positioned [distance and height];
    [subject awareness and gaze behavior]. Preserve [individual anchor 1],
    [anchor 2], and [anchor 3]. The meaning core is [gesture or object relation],
    supported only by [limited place and social cues]. Frame as [aspect and crop]
    with a [focal length] perspective so that [narrative consequence].
    Light comes from [motivated source and direction], with [contrast, exposure,
    and color behavior]. Retain [skin, fabric, paper, room, or use-mark texture].
    Leave unresolved [controlled question]. [Final constraints].

Naturalistic editorial means deliberate framing with real surfaces, not a fashion campaign or polished catalog unless the user explicitly requests one.

## Dynamic negative prompt

Build the negative prompt from actual failure risks in the selected brief. Use only relevant clauses.

Possible categories:

- interchangeability: generic model, flawless symmetry, beauty-advertising expression
- staging: finished pose, direct glamour pose, forced smile, catalog stance
- relationship drift: hidden-camera feeling, detached surveillance, unexplained intimacy, theatrical power angle
- place drift: luxury showroom, generic studio, decorative set dressing, unrelated props
- composition drift: meaningless body-fragment crop, room erased by blur, wide-angle edge distortion, cramped amputated action
- time drift: frozen tableau, no before-or-after action, expression disconnected from gesture
- light drift: unmotivated cinematic backlight, clipped highlights, crushed room detail, fashionable color grade unrelated to place
- surface drift: plastic skin, excessive retouching, spotless unused room, synthetic fabric, artificial depth blur
- rendering defects: extra people, duplicate objects, malformed hands, broken room geometry, illegible text, logos, watermark

Do not negate a requested anchor. If the desired image uses hard sunlight, grain, a tilted frame, or a close crop, remove conflicting negatives.

## Directorial controls

Offer concise controls that can be changed independently:

    emotional_charge: 0-100
    formal_restraint: 0-100
    environment_share: 0-100
    psychological_proximity: 0-100
    motion_residue: 0-100
    controlled_ambiguity: 0-100
    process_texture: 0-100

Add one or two scene-specific controls when useful, such as curtain movement, eye contact, doorway distance, or the visibility of a symbolic object. Explain the visible effect of changing a control; do not merely list numbers.

## Compact mode

Return:

    Final Prompt:
    [one clean English paragraph]

    Negative Prompt:
    [one scene-specific line]

Keep the same brief and quality gate. Compact mode removes explanation, not rigor.

## Revise mode

Diagnose only the problems the user named. Common repairs:

- Replace generic appearance praise with three visible individuality anchors.
- Make the place necessary by attaching it to role, action, memory, or time.
- Define who holds the camera and let that choice alter distance and gaze.
- Convert a completed pose into the instant before, during, or after an action.
- Replace decorative props with one used personal object.
- Choose one meaning core and remove competing details.
- Re-derive lens and light from the theme.
- Preserve one controlled question instead of explaining the whole story.

Return the repaired prompt, negative prompt, and the smallest useful set of directorial controls.

## Render handoff

When the user requests an image, pass the positive prompt and a clearly labeled Avoid clause containing the negative prompt. Do not silently add a new character, brand, text, palette, or story beat at render time. After generation, judge pixels against the brief rather than against prompt fluency.

