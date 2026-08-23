---
id: subject.human
version: 13
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
- independently dispose of body orientation, head-to-body relation, shoulder line, attention direction, and visible action as invariant, flexible, not-material, not-visible, or uncertain
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail in proportion to visibility. A primary close face can carry more description; a distant, blurred, reflected, screen-contained, or background person must remain simpler and lower-detail.

Before appearance prose, create one `human_appearance_decisions` record per spatial human. Record face visibility plus separate person-prior and skin-surface dispositions, evidence, confidence, and either emitted links or a non-emission reason. Distinguish obscured features from an actually cropped face.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

### Broad person-gestalt anchor

- Set the person prior to `emit`, `omit`, or `uncertain`. Emit at most one compact anchor for a sufficiently readable primary person when a broad apparent racial, ethnic, or regional appearance category, or calibrated attractiveness type, is supported and likely to stabilize generation. Otherwise record why it emits nothing.
- Treat any image-derived category as a generation-oriented visual approximation, not a factual identity claim. Do not infer nationality or exact ethnicity. Retain user-supplied identity context when requested, but never let it replace visible geometry.
- Record an emitted anchor as a `generation_prior` with provenance and constraining visible geometry. Link `geometry_claim_ids` to separate emitted human or face geometry claims and exact controls. Never reuse a motivating label without current source or user evidence.
- Prefer direct, generator-friendly wording for the fictional subject, then correct the category prior with face silhouette, proportions, feature relationships, skin tone and treatment, hair mass, expression, and lighting. Geometry wins when it conflicts with the broad anchor.
- When attractiveness is salient to the visible gestalt, calibrate its character rather than stacking intensity; for example, `conventionally attractive with a soft, approachable everyday appearance` or `striking and angular rather than polished`. Use one such phrase, not multiple beauty synonyms.
- Keep the attractive impression in the subject's visible facial harmony, expression, and grooming. Preserve asymmetry, ordinary traits, skin treatment, makeup level, capture softness, and crop instead of translating attractiveness into flawless skin, perfect symmetry, larger eyes, heavier makeup, beauty lighting, or a closer portrait.

After the optional gestalt anchor, prioritize the strongest source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Set visible skin to `material`, `not-material`, `not-visible`, or `uncertain`. When material, name its Color/Tone regions, `exposed`, `through-sheer`, or `mixed` coverage, and an `emit`, `omit`, or `uncertain` descriptor decision. Describe only legible tone axes, finish, texture, marks, makeup, facial hair, and retouching.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve source-relative shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette only to the degree visible; a garment boundary does not establish shoulder pose.
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

Place human description after concept and composition: scale/crop, head/body orientation, only emitted person-gestalt anchor, visible-tier face detail, hair occlusion, expression/gaze, pose/contact, clothing silhouette, then texture. Omit non-emitted appearance paths and generic posture that conflicts with recorded relations.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.
