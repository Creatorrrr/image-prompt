---
id: detail.human-face-likeness
version: 8
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

- **Prominent and legible:** the face is a primary image anchor and individual feature relationships are separable. Use six to ten selective likeness anchors.
- **Readable but secondary:** the face is smaller but several feature groups remain reliable. Use three to six anchors.
- **Small or indistinct:** do not use this module. Preserve head orientation, hair mass, skin-tone massing, and visibility only through `subject.human`.

For a prominent legible face, choose six to ten likeness-bearing visible anchors instead of listing every facial field.

Use fewer anchors when softness, compression, low contrast, or scale limits separation. Anchors preserve geometry; they do not authorize larger crop, sharper focus, cleaner makeup, extra detail, or a supporting-role downgrade.

An anchor describes a visible relationship, not a generic adjective.

## Coarse-to-fine likeness

When `subject.human` selects a broad person-gestalt anchor, treat it as one high-level generation prior rather than as the likeness description itself.

- Place it once before local face geometry; do not repeat the racial, ethnic, regional-appearance, or attractiveness category in later clauses.
- Preserve user/trusted identity only as external context. Treat source-visible broad appearance as a non-identifying generation approximation, never inferred nationality; keep case labels out of runtime defaults and unrelated holdouts.
- Link `geometry_claim_ids` to separate emitted source-visible form claims with exact generic controls. Neither prose evidence, skin color, nor the prior clause satisfies this link.
- Use the full scale-appropriate geometry budget to correct the category prototype with the source's face silhouette, feature relationships, expression, hair boundary, surface treatment, and visible asymmetry.
- If the broad anchor conflicts with reliable local geometry, revise or omit the broad anchor. Geometry wins.
- Keep attractiveness at the level of overall facial reading; do not let it enlarge the face, idealize proportions, clean the skin, strengthen makeup, sharpen focus, or upgrade lighting.

## Likeness anchor selection

Select only the strongest supported anchors across these groups:

1. **Head and face silhouette:** head width-to-height, forehead height, cheek fullness, cheekbone width, jaw taper or squareness, chin length/shape, visible asymmetry.
2. **Eyes and brows:** eye size relative to the face, spacing, tilt, lid exposure, fold visibility, far-eye reduction in three-quarter/profile view, brow thickness/shape/distance, catchlight pattern, gaze direction.
3. **Midface and nose:** bridge height/width, nose length, frontal or profile projection, tip shape, nostril visibility, relationship to cheek and upper lip.
4. **Mouth, jaw, and expression:** mouth width, lip line/fullness, corners, teeth visibility, closure/parting, chin tension, cheek lift, brow tension, squint, smile asymmetry, neutral or strained expression.
5. **Hair and face boundary:** hairline, part, fringe shape, temple coverage, side masses, curl/wave group, volume, flyaways, shadow color, and exact facial regions hidden by hair.
6. **Skin, makeup, and surface treatment:** tone depth and undertone, matte/reflective balance, visible texture, freckles or marks, under-eye treatment, facial hair, makeup placement and strength, capture smoothing or retouching.
7. **Facial lighting:** which planes receive highlight or shadow, how light changes the readable eye/nose/mouth/jaw geometry, and whether features remain soft, flat, hazy, or contrasty.

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

Create one compact human-likeness passage after composition:

1. optional one-sentence person-gestalt anchor
2. face scale, angle, crop, and visible side
3. the selected likeness anchors in source hierarchy
4. expression and gaze
5. hair silhouette and occlusion
6. skin/makeup/rendering and facial lighting when legible

Treat the passage as one owned face-gestalt effect when its clauses jointly preserve one likeness direction. If separate clauses push the same symmetry, feature scale, projection, polish, or face-type direction, merge or replace them rather than allowing the category anchor and local geometry to amplify one another.

Repeat at most one or two highest-risk anchors in the final constraint block. Do not copy the full passage into negative prompt or settings.

## Optional negative contribution

Reject a generic symmetrical model face, changed face silhouette, wrong eye/brow spacing or tilt, wrong nose/mouth/jaw relationship, changed expression or gaze, cleaned-up asymmetry, hairline/fringe/occlusion drift, invented hidden features, different skin or makeup treatment, and relighting that changes readable facial geometry. Include only the failures supported by the selected anchors.
