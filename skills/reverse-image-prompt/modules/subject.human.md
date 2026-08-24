---
id: subject.human
version: 15
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
- independently dispose of torso yaw/pitch/roll; head-to-body yaw/pitch/roll and lateral offset; shoulder image-plane slope and depth order; attention direction; and visible action as invariant, flexible, not-material, not-visible, or uncertain
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail by legibility; keep distant, blurred, reflected, screen-contained, or background people simple.

Link each pose decision to subject-owned cues and confounders. Under neutral axial alignment, material changed relations require an invariant decomposed axis; `flexible` or `not-material` needs a preservation reason, while `not-visible` or `uncertain` names the evidence limit.

Before appearance prose, create one `human-appearance/v2` decision per spatial human. Record face visibility, frame prominence, fidelity salience, appearance invariant IDs, identity context, person-prior risk/geometry/counterfactual, and skin handling. Distinguish occlusion from crop.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

### Broad person-gestalt anchor

- Frame prominence measures image size/attention; fidelity salience measures whether changing this person's reading changes reconstruction. A readable secondary figure may be fidelity-primary.
- Keep factual identity context `user-supplied`, `trusted-metadata`, or `absent`. Image-derived broad appearance is only a non-identifying, source-visible generation approximation; never infer nationality or exact ethnicity.
- Set the person prior to `emit`, `omit`, or `uncertain`. Record candidate support, model-default drift risk, local-geometry sufficiency, geometry claim IDs, and an omission counterfactual.
- For readable fidelity-material appearance, omit only when separate emitted form geometry is sufficient, default drift risk is low, and omission preserves the source reading. Unsupported high-risk cases remain uncertain rather than forcing a demographic guess.
- An emitted `generation_prior` carries provenance and exactly matching separate human/face/body-form controls. Geometry wins over the compact anchor; skin color alone cannot justify it.
- If attractiveness materially carries the visible gestalt, use one source-relative generation approximation and preserve asymmetry, grooming, skin treatment, makeup, capture softness, crop, and scale. Do not turn it into flawless symmetry, retouching, beauty lighting, or a closer portrait.

After the optional anchor, prioritize source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Set visible skin to `material`, `not-material`, `not-visible`, or `uncertain`. When material, name its Color/Tone regions and `exposed`, `through-sheer`, or `mixed` coverage. A descriptor may combine stable current-source axes while omitting unresolved ones; describe only legible tone, finish, texture, marks, makeup, facial hair, and retouching.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve source-relative shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette only to the degree visible. A garment boundary neither proves nor erases pose supported by independent contours or depth cues.
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

After concept and composition, order human controls as scale/crop, camera, material head/torso/shoulder relation, fidelity-primary gestalt, face, hair, gaze, contact, clothing, texture. Frame prominence cannot demote fidelity salience. Placement stays positional; appearance inherits pose. Omit non-emitted paths and conflicting generic posture.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.
