---
id: detail.human-face-likeness
version: 13
priority: 80
type: detail
tier: 3
facet: detail-risk
facet_values:
  - face
  - face-detail
  - face-likeness
  - prominent-face
  - readable-face
  - portrait-likeness
triggers:
  - prominent or clearly readable human face
  - portrait where facial likeness materially affects reconstruction
avoid_when:
  - face is tiny, heavily blurred, deeply shadowed, or too occluded for reliable feature evidence
dependencies:
  - subject.human
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors:
  - human_detail_hierarchy
  - face_anchor_budget
  - expression_gaze_hair_geometry
---

# Detail: human face likeness

## When to load

Load only when at least one human face is prominent or clearly readable. Do not load merely because a person exists.

## Detail tier

Allocate anchor count by visible face scale and legibility, but assign fidelity role independently. A readable-secondary face may remain a primary invariant when changing its broad reading changes the image.

- **Prominent and legible:** the face is a primary image anchor and individual feature relationships are separable. In `prompt`, use two to five decisive anchors; in `audited`, use six to ten when supported.
- **Readable but secondary:** the face is smaller but several feature groups remain reliable. In `prompt`, use one to three decisive anchors; in `audited`, use three to six.
- **Small or indistinct:** do not use this module. Preserve head orientation, hair mass, skin-tone massing, and visibility only through `subject.human`.

Choose anchors by viewer impact and default-drift risk, never to fill every facial group. A material person-aesthetic or attractiveness reading is one optional gestalt anchor, never local likeness geometry; bind each intended effect to a separate visible control.

Use fewer anchors when softness, compression, low contrast, or scale limits separation. Anchors preserve geometry; they do not authorize larger crop, sharper focus, cleaner makeup, extra detail, or a supporting-role downgrade.

An anchor describes a visible relationship, not a generic adjective.

## Coarse-to-fine likeness

When `subject.human` selects a broad person-gestalt anchor, treat it as one high-level generation prior rather than as the likeness description itself.

- Place it once before local face geometry; do not repeat the broad prior in later clauses.
- Never infer race, ethnicity, nationality, or another protected identity label from a face. Preserve exact user/trusted identity context once as external intent before the appearance passage when it is P0/P1; it is not visual evidence or a generation prior.
- Link `geometry_claim_ids` to exact source-visible form controls. Keep them contiguous after the prior so local geometry corrects it. Prose, skin color, or the prior itself cannot satisfy the link.
- Use the scale-appropriate geometry budget to correct the category prototype with only the source-material face silhouette, feature relationships, expression, hair boundary, surface treatment, and visible asymmetry.
- If the broad anchor conflicts with reliable local geometry, revise or omit the broad anchor. Geometry wins.
- Keep a person-aesthetic or attractiveness anchor at the source-visible overall reading during analysis, then express the actual bounded presentation in the final prompt without the internal phrase `source-visible` or another missing-image comparison. State it once only when P0/P1 and omission-sensitive, followed immediately by controls for every intended dimension. Protect identity, pose, crop, scale, age presentation, cosmetics, garment coverage, light, color, and capture treatment unless separately owned; do not idealize, clean, enlarge, sharpen, or relight by implication.

## Likeness anchor selection

Select only the strongest supported anchors across these groups:

1. **Silhouette:** head proportions, forehead/cheek/jaw/chin relationship, and visible asymmetry.
2. **Eyes and brows:** relative size, spacing, tilt, lid exposure, far-eye compression, brow relation, and gaze.
3. **Midface and nose:** bridge, length, projection, tip, nostril visibility, and cheek/lip relation.
4. **Mouth and expression:** width, line/fullness, closure, corners, teeth, and decisive facial tension.
5. **Hair boundary:** hairline, part/fringe, side masses, volume, texture group, and covered facial regions.
6. **Skin and makeup:** displayed tone/undertone, finish, texture/marks, makeup, facial hair, and capture treatment.
7. **Facial light:** material highlight/shadow planes and their effect on readable geometry.

Preserve expression, gaze, and hair-to-face occlusion as likeness-critical geometry. Keep viewpoint separate from head pose and attention; do not repeat perspective-induced nostril, jaw, neck, eye, or far-side changes as intrinsic geometry.

Infer face orientation from multiple relations—near/far feature exposure, side contour, nose-cheek spacing, compression, and occlusion—not both eyes alone. Record occluders as confounders; if camera/head separation is uncertain, preserve the visible side relation.

Keep optical softness distinct from beauty retouching; do not convert it into crisp, smoothed skin.

Use relational wording: wider than, closer together, higher than, partly hidden by, aligned with, shorter relative to, or more visible on the viewer-left/right. Do not infer unobserved feature geometry.

## Partial, angled, and multiple faces

- For three-quarter or profile views, state near-side/far-side feature visibility and perspective compression instead of describing an imagined frontal face.
- For edge-cropped or occluded faces, list visible and hidden feature groups before fine detail. Do not complete the missing side.
- For a reflected, screen-contained, printed, or background face, keep its detail ceiling tied to that layer.
- For multiple readable faces, allocate the largest anchor budget to the primary face and a smaller distinct set to each secondary face. Never merge anchors between people.
- For stylized faces, preserve the source's shape language, line/render treatment, and feature scale; add the maturity module only when needed.

## Prompt contribution

Create one compact human-likeness passage at the position assigned by viewer priority:

1. optional P0/P1 external identity context, once
2. optional person prior, then face scale, angle, crop, visible side, and correcting geometry
3. optional appearance gestalt and its owned decomposition
4. remaining expression, gaze, hair silhouette, and occlusion
5. displayed skin, makeup, rendering, and facial lighting only when independently material

Treat the passage as one owned face-gestalt effect when its clauses jointly preserve one likeness direction. If separate clauses push the same symmetry, feature scale, projection, polish, or face-type direction, merge or replace them rather than allowing the category anchor and local geometry to amplify one another.

Repeat at most one or two highest-risk anchors in the final constraint block. Do not copy the full passage into negative prompt or settings.

## Optional negative contribution

Reject a generic symmetrical model face, changed face silhouette, wrong eye/brow spacing or tilt, wrong nose/mouth/jaw relationship, changed expression or gaze, cleaned-up asymmetry, hairline/fringe/occlusion drift, invented hidden features, different skin or makeup treatment, and relighting that changes readable facial geometry. Include only the failures supported by the selected anchors.
