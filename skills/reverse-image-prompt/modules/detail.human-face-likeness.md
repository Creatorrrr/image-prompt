---
id: detail.human-face-likeness
version: 3
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

Allocate human detail by visible face scale and legibility.

- **Prominent and legible:** the face is a primary image anchor and individual feature relationships are separable. Use six to ten selective likeness anchors.
- **Readable but secondary:** the face is smaller but several feature groups remain reliable. Use three to six anchors.
- **Small or indistinct:** do not use this module. Preserve head orientation, hair mass, skin-tone massing, and visibility only through `subject.human`.

For a prominent legible face, choose six to ten likeness-bearing visible anchors instead of listing every facial field.

Use the lower end of the anchor range when global softness, haze, compression, low microcontrast, or small face scale limits feature separation. Face-detail anchors preserve geometry; they do not authorize a larger crop, stronger focus, added skin texture, cleaner makeup, brighter catchlights, or sharper hair than the source aesthetic supports.

An anchor must describe a distinctive visible relationship, not a generic adjective. `Narrow lower face with a short rounded chin` is useful; `beautiful detailed face` is not.

## Coarse-to-fine likeness

When `subject.human` selects a broad person-gestalt anchor, treat it as one high-level generation prior rather than as the likeness description itself.

- Place it once before local face geometry; do not repeat the racial, ethnic, regional-appearance, or attractiveness category in later clauses.
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

Preserve expression, gaze, and hair-to-face occlusion as likeness-critical geometry.

Distinguish optical or processing softness from beauty retouching. A globally soft face should remain optically soft rather than becoming a crisp face with smoothed skin.

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

Repeat at most one or two highest-risk anchors in the final constraint block. Do not copy the full passage into negative prompt or settings.

## Optional negative contribution

Reject a generic symmetrical model face, changed face silhouette, wrong eye/brow spacing or tilt, wrong nose/mouth/jaw relationship, changed expression or gaze, cleaned-up asymmetry, hairline/fringe/occlusion drift, invented hidden features, different skin or makeup treatment, and relighting that changes readable facial geometry. Include only the failures supported by the selected anchors.
