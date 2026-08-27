---
id: detail.clothing-fashion
version: 9
priority: 78
type: detail
tier: 3
facet: detail-risk
facet_values:
  - clothing
  - fashion
  - body-silhouette
  - neckline
  - straps
  - garment-geometry
  - band-height
  - accessories
triggers:
  - important clothing silhouette, neckline, straps, exposed/covered bands, accessories
avoid_when:
  - clothing is absent or visually unimportant
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors:
  - band_height_drift
  - garment_geometry
  - material_role
  - category_prior_disambiguation
  - detail_role_ceiling
---

# Detail: clothing, fashion, accessories, and coverage maps

## When to load

Load when clothing placement, garment edges, neckline, straps, accessories, exposed/covered bands, fabric tension, or fashion labels affect fidelity.

## Evidence contribution

Describe visible garment geometry before broad category labels:

Prefer visible garment geometry over broad fashion-category labels.
Treat visible band-height drift as a composition failure.
Assign each visible garment or accessory a material role: primary subject, silhouette boundary, frame, texture support, or low-legibility mass.

Route selection does not entitle clothing to prompt space. Cap material and construction detail to the garment's hierarchy role; a framing or supporting garment must not receive more semantic emphasis, sharpness, or completion than the primary invariant.

In `prompt`, first decide whether silhouette, coverage, or material response is P0/P1. Otherwise contribute at most one P2 cue; reserve the inventory for audited or clothing-critical work.

- fit, thickness/weight, opacity, stiffness, tension, folds, sheen, and pattern scale
- legible weave, nap, grain, coating, reflectivity, and edge behavior
- neckline/collar/opening, sleeve/strap, seams/closures/hems, and layer interaction; garment edges never replace owned pose

Before using a garment category label, specify the visible opacity, thickness, weight, weave or knit scale, finish, and construction cues that must override its default prior. Omit dimensions that cannot be seen; the point is to disambiguate the material, not to fill a fabric checklist.

When placement matters, map skin, fabric, shadow-hidden, and cropped regions plus interrupted or softened garment edges; preserve boundary components instead of collapsing them to a category.

Treat close upper-torso edges as measured boundary bands, not fashion labels. Lock neckline/garment-edge width, lowest y-position, visible skin/underlayer area above and below it, sleeve/shoulder fabric area, and bottom crop.

When a person-aesthetic anchor is retained, garment coverage remains an independent dimension. Include it in the anchor's intended effect budget only with P0/P1 source evidence and this module's owned boundary control; otherwise protect it. The anchor cannot imply a deeper opening, fitted bodice, different sleeve, changed opacity, or altered exposure.

Avoid broad fashion or garment labels when their prior would deepen, widen, clarify, center, tighten, reveal, structure, or glamorize beyond the source. Category follows geometry and role.

For edge crops, distinguish a narrow visible band from a completed outfit or body. Describe partial hems, waistbands, pockets, or gaps by bounded height/area and nearby anchors; do not invite centered completion or wider exposure.

For accessories, lock visible silhouette, footprint, crop, density, shadow, and occlusion before detail. Keep secondary or edge-cropped pieces partial and low-legibility; do not upgrade them into crisp, complete, symmetrical ornament.

For tight portraits with secondary clothing, budget visible garment bands, frame range, completeness, interruptions, symmetry, and lower-torso extent before a broad label. Keep compressed or unclear construction unresolved.

Do not let cropped secondary clothing become a clean centered outfit. Lock incomplete geometry before category language and preserve its supporting role.

## Optional negative contribution

Reject wrong neckline, strap, sleeve, seam, hem, fit, opacity, exposure, completed hidden regions, cleaner fashion styling, enlarged accessories, centered outfit completion, clarified low-legibility construction, or expanded lower torso.

## Optional settings contribution

- Clothing-fit, neckline, and seam locks:
- Body-proportion calibration locks:
- Boundary and visibility-budget locks:
