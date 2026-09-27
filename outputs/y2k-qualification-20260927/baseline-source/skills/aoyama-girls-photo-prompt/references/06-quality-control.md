# Quality Control

## 100-point rubric

Score the compiled prompt before delivery:

| Dimension | Points | Full-credit evidence |
|---|---:|---|
| Theme specificity | 12 | WHO, WHERE, HOW, and WHY NOW form one necessary proposition |
| Subject individuality | 12 | Three observable, non-generic anchors |
| SIR construction | 12 | Two axes lead clearly; the third is intentionally present or reserved |
| Relationship and distance | 12 | Viewer role changes viewpoint, awareness, gaze, and crop |
| Temporal transition | 10 | Previous, current, and next action are visually compatible |
| Meaning-led framing | 10 | One core detail governs how far the frame expands |
| Place necessity and information budget | 10 | Place cues carry role, time, action, or memory without decorative clutter |
| Camera and light causality | 8 | Ratio, lens, viewpoint, and light follow the theme |
| Controlled ambiguity | 6 | One supported question remains open |
| Generator clarity and negative prompt | 8 | Instructions are concrete, non-contradictory, and scene-specific |

Target at least 82/100. Also revise when any 12-point category scores below 8 or any 10-point category scores below 7, even if the total passes.

Do not expose a flattering score as proof. The rubric is a preflight decision aid.

## Failure diagnosis and automatic repair

### Generic beauty editorial

Symptoms:

- subject could be replaced without consequence
- attractive, elegant, cinematic, or dreamy carries most of the prompt
- pose and room feel like an advertisement

Repair:

- remove generic praise
- add three observable anchors
- give one object a history of use
- convert the pose to an incomplete action
- lower polish and restore material texture

### Weak person-place relationship

Symptoms:

- any attractive room or street would work
- background is erased by shallow depth of field
- props establish aesthetic rather than life

Repair:

- connect place to routine, role, memory, or present action
- choose two place cues and one personal irregularity
- widen or shorten the lens only enough to make those cues readable
- remove unrelated decoration

### Camera with no owner

Symptoms:

- candid is the only relationship instruction
- eye contact, angle, and distance contradict one another
- intimacy appears without evidence

Repair:

- name the viewer role
- set psychological distance and subject awareness
- alter body orientation and gaze accordingly
- remove dramatic angles unsupported by the relationship

### Frozen pose

Symptoms:

- relaxed pose, natural smile, or looking thoughtful
- no visible trigger or next action

Repair:

- define the previous action and next likely action
- retain a physical residue from the previous moment
- put the shutter between the two states

### Meaningless detail crop

Symptoms:

- the crop only magnifies a body part
- removing the face removes all story
- the detail has no object, action, clothing, or place cue

Repair:

- choose an action-detail junction
- add the smallest adjacent cue that conveys role or time
- widen until meaning is legible, then stop

### Preset camera styling

Symptoms:

- backlight, pastel, 85mm, shallow depth of field, or film grain appears without a thematic reason

Repair:

- restate what information the camera must retain
- derive focal length and ratio from that information
- motivate light from the actual place and time
- remove texture that does not serve the proposition

### Over-explained scene

Symptoms:

- every object has a literal symbolic explanation
- multiple story beats compete
- nothing remains for the viewer to infer

Repair:

- choose one meaning core
- cut redundant cues
- retain one supported question

Run no more than two repair passes. If the brief remains contradictory, surface the conflict instead of inventing a resolution.

## Prompt QA versus pixel QA

Prompt QA checks whether the written request carries the method. Pixel QA checks whether the generated image actually shows it. Keep the two results separate.

After rendering, inspect:

- the correct person and place are present
- the intended viewer distance and awareness are visible
- the current action is genuinely transitional
- the three individuality anchors are recognizable where composition allows
- the primary SIR axes read without explanation
- the meaning core dominates
- the information budget is respected
- lens and aspect function as intended
- light retains important surface and room detail
- hands, objects, text, and room geometry have no obvious generation defects

If a render misses one high-value obligation, make one targeted revision and recheck. Do not rewrite the entire concept or quietly change locked user anchors.

