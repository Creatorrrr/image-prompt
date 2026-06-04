---
id: detail.accessory-torso-budget
version: 1
priority: 76
type: detail
tier: 3
facet: detail-risk
facet_values:
  - accessory-torso-budget
  - measured-accessories
  - secondary-accessories
  - cropped-torso
  - lower-garment-band
  - cropped-garment-band
triggers:
  - tight human crop where accessories, neckline, upper torso, or lower garment bands are visible but secondary
avoid_when:
  - accessories and cropped torso/clothing are absent or central enough to be the main subject
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
  - subject.human
  - detail.clothing-fashion
conflicts: []
provides_anchors:
  - accessory_torso_budget
---

# Detail: accessory and torso budgets

## When to load

Load when a tight human crop includes headpieces, bows, clips, chokers, necklaces, straps, lace, ruffles, garment trim, cropped shoulders, or upper-torso clothing that must remain secondary to the primary face, hand, prop, or crop concept.

## Prompt additions

Treat accessories and cropped torso regions as measured support budgets, not as invitations to complete a costume, outfit, glamour pose, or body-centered portrait.

- Define each accessory footprint once: approximate frame location, scale relative to face/head, crop, occlusion, contrast, and legibility. Then keep it secondary unless it visibly dominates.
- Avoid multiplying accessory adjectives after footprint is established. Extra detail on lace, jewelry, bows, nails, plaid, straps, or trim can enlarge or sharpen them.
- For close portraits, prioritize face scale, eye line, chin line, hair edges, and crop boundaries over costume labels and accessory material.
- For upper torso that is visible but secondary, prefer `cropped skin plane`, `covered torso plane`, `interrupted neckline`, `hair-overlapped torso edge`, `secondary shoulder edge`, `lower-frame garment band`, or `cropped garment edge band` when supported by the source.
- Lock lower garment, collar, neckline, ruffle, strap, or trim bands by y-start, height, width, interruption, and crop. If the source shows only a bottom or side band, keep it as a band and do not complete it into a bodice, dress, uniform, corset, or full outfit view.
- Preserve side-specific asymmetry for shoulders, straps, hair occlusion, accessory position, and edge cuts instead of normalizing into a symmetrical fashion portrait.

## Negative additions

Reject accessory enlargement, crisp ornate accessory upgrading, centered outfit views, complete costume construction, lower torso expansion, clarified hidden neckline, widened or deepened garment openings, cleaner symmetrical straps/collars, and clothing/body regions promoted beyond their visible source budget.

## Settings additions

- Clothing-fit, neckline, and seam locks: describe incomplete bands, cropped trims, interrupted necklines, and occluding hair/hand/props before category labels.
- Boundary and visibility-budget locks: accessories and torso regions remain source-sized, cropped, interrupted, and secondary.
- Body-proportion calibration locks: visible torso information remains limited to source-visible image-plane regions without hidden anatomy inference.
