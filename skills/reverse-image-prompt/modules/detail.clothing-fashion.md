---
id: detail.clothing-fashion
version: 5
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
---

# Detail: clothing, fashion, accessories, and coverage maps

## When to load

Load when clothing placement, garment edges, neckline, straps, accessories, exposed/covered bands, fabric tension, or fashion labels affect fidelity.

## Prompt additions

Describe visible garment geometry before broad category labels:

Prefer visible garment geometry over broad fashion-category labels.
Treat visible band-height drift as a composition failure.
Assign each visible garment or accessory a material role: primary subject, silhouette boundary, frame, texture support, or low-legibility mass.

- fit, visible thickness and weight, opacity/transparency, stiffness/looseness
- fabric tension, wrinkles, folds, material sheen, pattern scale
- weave or knit scale, nap, grain, coating, reflectivity, and edge behavior only where legible
- neckline depth/width, collar, shirt opening, sleeve opening, strap position
- seams, waist seam, under-bust seam if visible, buttons, lace, closures, hems
- garment layers and how they interact with body shape, pose, props, hair, hands, shadow, and crop

Before using a garment category label, specify the visible opacity, thickness, weight, weave or knit scale, finish, and construction cues that must override its default prior. Omit dimensions that cannot be seen; the point is to disambiguate the material, not to fill a fabric checklist.

Create a coverage map when clothing placement matters:

- which image regions are skin
- which regions are fabric
- which regions are shadow-hidden
- which regions are cropped away
- which garment edges are interrupted, softened, shadowed, blurred, or blocked

Treat close upper-torso edges as measured boundary bands, not fashion labels. Lock neckline/garment-edge width, lowest y-position, visible skin/underlayer area above and below it, sleeve/shoulder fabric area, and bottom crop.

Avoid broad labels such as `off-shoulder`, `low neckline`, `camisole`, `dress`, `lingerie`, `corset`, `crop top`, or `fashion portrait` if their category prior would deepen, widen, clarify, center, tighten, reveal, structure, or glamorize the garment beyond the source. Category labels follow geometry and material role; they do not define them.

For bottom-edge or side-edge clothing/body crops, distinguish a narrow visible band from a completed outfit or body region. If the source only shows a hem, waistband, partial pocket, side edge, lower garment strip, or crop-boundary gap, describe it as a bounded edge band with height/area and nearby anchors. Avoid wording that invites centered body construction, full pockets, completed legs, or a wider exposed/covered band than the source.

For accessories such as chokers, collars, necklaces, straps, lace trim, bows, patches, pins, bags, or jewelry, describe only visible silhouette, density, low-legibility, shadow, and occlusion. Do not upgrade them into crisp ornate symmetrical fashion accessories unless visible.

For straps, bags, chains, handles, and edge-adjacent accessories, lock footprint and crop before material detail. If the accessory is secondary or partly outside the frame, keep it partial, low-detail, and edge-bound in affirmative prompt language rather than relying only on the negative prompt.

For close portraits or tight human crops where clothing is secondary below the face, create a secondary garment completion budget before using broad fashion labels:

- visible garment bands and approximate frame ranges
- whether collar, neckline, tie, ribbon, scarf, vest, jacket, sleeve, trim, button, patch, strap, or accessory is complete, partial, folded, cropped, occluded, or low-legibility
- which garment parts are interrupted by chin, hair, hand, prop, shadow, blur, or bottom crop
- whether symmetry, openings, knots, edges, seams, and trim should remain compressed or unclear instead of becoming clean outfit construction
- how much lower torso is visible before the prompt would turn a close portrait into a fashion, costume, or uniform study

Do not let secondary formal, uniform-like, costume-like, layered, or accessory-heavy clothing become a clean centered outfit view when the source uses it only as cropped lower-frame or side-frame bands. Use clothing category labels only after locking incomplete garment geometry, and keep the clothing secondary when the face, hand, prop, or crop is the real visual anchor.

## Optional negative contribution

Reject wrong neckline depth/width, strap position, sleeve position, seam placement, hem shift, deeper openings, larger exposed skin bands, tighter/looser fabric, more structured/corseted/lingerie-like garment, more revealing or more modest clothing, completed hidden garment regions, cleaner fashion-editorial styling, and accessory enlargement or sharpening. For secondary clothing in close portraits, reject complete centered outfit views, overly symmetrical collars/necklines, clarified knots/openings/trim/buttons/patches, and lower torso expansion when the source clothing is cropped, compressed, occluded, or low-detail.

## Optional settings contribution

- Clothing-fit, neckline, and seam locks:
- Body-proportion calibration locks:
- Boundary and visibility-budget locks:
