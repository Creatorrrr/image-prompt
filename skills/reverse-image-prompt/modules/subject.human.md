---
id: subject.human
version: 19
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

In `prompt`, record only P0/P1 entries from this hierarchy before micro-detail; group the rest. In `audited`, dispose every listed axis:

- number of people and primary/secondary roles
- each person's frame share, crop, depth plane, and overlap order
- head position and scale relative to the frame and body
- independently dispose of torso yaw/pitch/roll; head-to-body yaw/pitch/roll and lateral offset; shoulder image-plane slope and depth order; attention direction; and visible action as invariant, flexible, not-material, not-visible, or uncertain
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail by legibility; keep distant, blurred, reflected, screen-contained, or background people simple.

In `prompt`, preserve one macro pose result and only decisive residual relations when pose is P0/P1. In `audited`, link every pose decision to cues/confounders, compare whole with viewpoint-held residual neutralization, and apply coupled-member summary coverage.

Before appearance prose, build a compact appearance signature in `prompt`; create one `human-appearance/v2` decision per spatial human only in `audited`. Distinguish occlusion from crop in either profile.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

For `prompt`, select only source-material fields from broad visual prior, local face/body geometry, displayed skin axes and finish, hair boundary, expression/gaze, and capture treatment. A field earns detail only when changing it would alter P0/P1 or when model-default drift is high.

### Broad person-gestalt anchor

- Frame prominence measures image size/attention; fidelity salience measures whether changing this person's reading changes reconstruction. A readable secondary figure may be fidelity-primary.
- Keep factual identity context `user-supplied`, `trusted-metadata`, or `absent`. Image-derived broad appearance is only a non-identifying, source-visible generation approximation; never infer nationality or exact ethnicity.
- Set the person prior to `emit`, `omit`, or `uncertain`. In `prompt`, record candidate support, default-drift risk, geometry sufficiency, and one omission counterfactual only when that decision is P0/P1. In `audited`, also record the full claim bindings.
- For readable fidelity-material appearance, omit only when separate emitted form geometry is sufficient, default drift risk is low, and omission preserves the source reading. Unsupported high-risk cases remain uncertain rather than forcing a demographic guess.
- An emitted `generation_prior` carries provenance and matching human/face/body-form controls. Keep them contiguous so geometry corrects the anchor; skin color cannot justify it.
- If attractiveness materially carries the gestalt, use an optional `generation_prior` with scope `attractiveness`. Retain it once with P0/P1 source evidence and material-drift omission, then constrain it with geometry, asymmetry, grooming, skin/makeup, capture, crop, and scale. It cannot authorize retouching, idealization, relighting, or a closer portrait.

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

Order human controls by cross-lane viewer priority, while preserving dependencies: scale/crop and camera before a material pose result; any broad prior immediately before correcting local geometry; then material skin/surface, hair, expression, and capture. In `audited`, coupled pose controls retain the macro summary and only `partial` or `lost` residuals. Placement stays positional and appearance inherits pose.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.
