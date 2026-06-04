---
id: detail.tight-selfie-hierarchy
version: 1
priority: 77
type: detail
tier: 3
facet: detail-risk
facet_values:
  - tight-selfie
  - selfie-hierarchy
  - face-hair-hierarchy
  - close-phone-selfie
  - cropped-upper-torso-selfie
triggers:
  - tight human phone selfie where face, hair, crop, and lower-frame completion risk affect fidelity
avoid_when:
  - not a tight human selfie
  - face and hair are not the primary image-plane anchors
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
  - subject.human
  - medium.photographic-capture
conflicts: []
provides_anchors:
  - tight_selfie_hierarchy
---

# Detail: tight selfie hierarchy

## When to load

Load when a close human phone selfie is dominated by the face, hair, headwear, or upper-head crop, and generation is likely to normalize it into a balanced portrait, fashion image, outfit study, or cleaner head-and-shoulders shot.

## Prompt additions

When tight selfie framing makes the face and hair the primary anchors, state that hierarchy before describing clothing, accessories, or broad fashion labels.

- Lead with image-plane priority: face and hair first; hand, accessories, shoulders, and lower-frame clothing second.
- Preserve phone-selfie crop pressure, asymmetry, edge cuts, and high-face or close-face placement before aesthetic labels such as portrait, cosplay, fashion, beauty, editorial, or character reference.
- If the face is phone-smoothed, sun-washed, filtered, doll-like, overexposed, low-contrast, or otherwise capture-treated, state that as a fidelity lock rather than improving it into natural skin or studio beauty lighting.
- If bangs, fringe, hair, hat, hood, veil, or headwear cover the forehead, brows, eyelids, cheek, jaw, or frame edge, describe coverage and occlusion before strand or accessory texture. Reject exposed or completed hidden face regions when the source hides them.
- For wigs, dyed hair, bright hair, or strongly lit hair, separate local hair color from shadow color. Lock highlight masses and shadow masses so the generator does not average the hair into a cleaner single color.
- If a generated comparison drifts into a more natural selfie, centered portrait, or clearer outfit study, strengthen these generic hierarchy and crop locks instead of adding source-only trivia.

## Negative additions

Reject balanced head-and-shoulders portrait drift, fashion-editorial recentering, cleaned-up studio portrait lighting, reduced face/hair dominance, exposed hidden forehead or brows, completed hidden crop edges, and any prompt wording that lets secondary clothing or accessories overtake the face/hair hierarchy.

## Settings additions

- Primary visual concept locks: face and hair remain the first-order anchors; secondary objects stay source-sized.
- Boundary and visibility-budget locks: preserve tight selfie edge cuts, high-face crop, side crops, and incomplete lower-frame regions.
- Coherence/realism ceiling locks: keep the source phone-selfie capture treatment instead of upgrading into a polished portrait.
