---
id: subject.human
version: 22
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

In `prompt`, preserve one macro pose result and decisive residuals when pose is P0/P1. Alignment semantics can jointly actuate torso, head/body, shoulder, attention, placement, and viewpoint; inspect every clause's explicit and implicit effects. In `audited`, link decisions to cues/confounders, test each discarded axis in isolation, compare whole with viewpoint-held residual neutralization, cover coupled members, and reject clauses affecting non-invariant or uncertain axes.

Before appearance prose, build a compact appearance signature in `prompt`; create one `human-appearance/v3` decision per spatial human only in `audited`. Distinguish occlusion from crop in either profile.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

For `prompt`, decide four lanes independently: externally sourced identity context, optional non-identifying person prior, displayed-skin surface, and optional appearance gestalt. A field earns detail only when it is P0/P1 or has high model-default drift.

### Broad person-gestalt anchor

- Frame prominence measures image size/attention; fidelity salience measures reconstruction impact. A readable secondary figure may be fidelity-primary.
- Keep exact race, ethnicity, nationality, or other identity context `user-supplied`, `trusted-metadata`, or `absent`. Emit externally sourced context once only when its viewer priority is P0/P1; never derive or corroborate it from pixels, skin, hair, face geometry, or aesthetic reading.
- Set the non-identifying person prior to `emit`, `omit`, or `uncertain`. Record support, default-drift risk, geometry sufficiency, and one omission counterfactual. Omit only when emitted form geometry is sufficient, drift risk is low, and the source reading survives; never force a protected-category guess.
- An emitted person prior carries provenance and matching human/face/body-form controls. Keep them contiguous so visible geometry corrects the anchor; skin and identity context cannot justify it.
- Decide a separate appearance gestalt for attractiveness or another broad person aesthetic. Emit one high/medium-confidence P0/P1 anchor only when omission causes material drift. Declare intended and protected dimensions, then immediately decompose every intended dimension into an owner-correct face, body, hair, expression, displayed-skin, garment, pose, scale, capture, light, or color control. Identity context is always protected; unowned dimensions cannot change.
- Keep the appearance anchor source-relative in analysis but emit only the visible presentation; never emit `source-relative` or a missing-image comparison. It cannot silently idealize, retouch, relight, reveal clothing, change cosmetics, alter pose/crop/scale/age presentation, or upgrade capture; those directions require their own source evidence and ownership.

After the optional anchor, prioritize source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Set displayed skin to `material`, `not-material`, `not-visible`, or `uncertain` with its own P0-P3 priority. When material, name its Color/Tone regions, observation scope, and `exposed`, `through-sheer`, or `mixed` coverage. Describe stable visible value, chroma, undertone, finish, texture, marks, makeup, facial hair, and retouching as captured surface output, never identity or biological color.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve visible shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette. Compare them source-relatively in analysis but state actual proportions and relations in final prose. A garment boundary neither proves nor erases pose supported by independent contours or depth cues.
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

Order human controls by cross-lane priority while preserving dependencies: scale/crop and camera; material pose; one P0/P1 external identity context; any broad person prior with correcting geometry; one appearance gestalt with its contiguous owned decomposition; then remaining displayed skin, hair, expression, garment, light/color, and capture controls. In `audited`, coupled pose controls retain the macro summary and only `partial` or `lost` residuals, and every spatial control carries a complete explicit/implicit effect audit against the final literal excerpt. Placement stays positional and appearance inherits pose.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.
