---
id: subject.human
version: 9
priority: 82
type: subject
tier: 2
facet: subject
facet_values:
  - human
  - person
  - portrait
  - face
  - body
  - human-like
triggers:
  - visible person
  - visible human face, hair, skin, body silhouette, or portrait/body crop
avoid_when:
  - no human subject or human-like figure
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors:
  - face_fidelity
  - aesthetic_upgrade
  - symmetric_large_body_lock
  - symmetric_moderate_body_lock
  - face_exposure_budget
  - broad_person_gestalt_anchor
---

# Subject: human fidelity

## When to load

Load whenever a real or fictional person is visibly present. Add `detail.human-face-likeness` only when facial features are prominent or clearly readable.

## Human hierarchy

Record these before micro-detail:

- number of people and primary/secondary roles
- each person's frame share, crop, depth plane, and overlap order
- head position and scale relative to the frame and body
- body orientation, head turn, gaze direction, shoulder line, and visible action
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail in proportion to visibility. A primary close face can carry more description; a distant, blurred, reflected, screen-contained, or background person must remain simpler and lower-detail.

Define a face visibility budget before choosing a broad person-gestalt anchor or local face detail. Record which feature groups are fully visible, partly hidden, shadowed, soft, occluded, or actually cut by the frame. If only hair or the outer head mass is cropped, do not imply that eyes, nose, mouth, cheek, or chin are sliced.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

### Broad person-gestalt anchor

- Use at most one compact anchor for a primary, sufficiently readable person when a broad apparent racial, ethnic, or regional appearance category, or a calibrated attractiveness type, is visually supported and likely to stabilize generation. Omit it for small, blurred, heavily occluded, or genuinely ambiguous people.
- Treat any image-derived category as a generation-oriented visual approximation, not a factual identity claim. Do not infer nationality or exact ethnicity. Retain user-supplied identity context when requested, but never let it replace visible geometry.
- Prefer direct, generator-friendly wording for the fictional subject, then correct the category prior with face silhouette, proportions, feature relationships, skin tone and treatment, hair mass, expression, and lighting. Geometry wins when it conflicts with the broad anchor.
- When attractiveness is salient to the visible gestalt, calibrate its character rather than stacking intensity; for example, `conventionally attractive with a soft, approachable everyday appearance` or `striking and angular rather than polished`. Use one such phrase, not multiple beauty synonyms.
- Keep the attractive impression in the subject's visible facial harmony, expression, and grooming. Preserve asymmetry, ordinary traits, skin treatment, makeup level, capture softness, and crop instead of translating attractiveness into flawless skin, perfect symmetry, larger eyes, heavier makeup, beauty lighting, or a closer portrait.

After the optional gestalt anchor, prioritize the strongest source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Treat skin and makeup as rendering evidence: tone depth, undertone, matte or reflective finish, visible texture, freckles or marks, under-eye treatment, facial hair, cosmetic strength, and retouching level only when legible.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve source-relative shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette only to the degree visible.
- Separate anatomical proportion from near-camera enlargement, foreshortening, pose compression, garment pressure, and light/shadow shaping. Do not convert a bright edge or dark groove into unsupported anatomy.
- Keep the torso, pelvis, and center of mass in the source-visible spatial zone; do not let a contact pose silently relocate the person across a barrier, edge, opening, or support surface.
- Preserve a clearly visible large-scale body silhouette without exaggeration or reduction.
- Keep a moderate or obscured body silhouette secondary rather than promoting it.
- If age is unclear or the person is not clearly adult, use neutral, non-sexual silhouette and clothing language.
- Keep secondary or cropped body regions subordinate to a dominant face, action, prop, or relationship.
- Lock the person's frame share and environmental context before facial detail. Do not let a detailed face passage enlarge the subject or convert an environmental portrait into a close beauty portrait.

## Module handoff

- Add `detail.human-face-likeness` for a prominent or clearly readable face.
- Add `detail.human-body-form` when visible proportion, contour, tissue character, muscle definition, skin surface, or body-region hierarchy is a first-order part of the image's identity or appeal.
- Add `detail.pose-hands-gesture` when hand shape, grip, contact, limb mechanics, or pose landmarks matter.
- Add `detail.clothing-fashion` when garment boundaries, fit, seams, straps, or coverage affect the visible silhouette.
- Add `detail.tight-selfie-hierarchy` for a close phone selfie whose face/hair hierarchy and edge crop are first-order.
- Add `style.stylized-character-maturity` only for a stylized human-like subject with maturity drift risk.

## Prompt contribution

Place human description after the primary concept and composition. Preserve this order: subject scale and crop, head/body orientation, optional one-sentence person-gestalt anchor, face detail at the visible tier, hair-to-face occlusion, expression/gaze, pose/contact, clothing silhouette, then secondary texture.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.
