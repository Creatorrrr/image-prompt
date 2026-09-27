---
id: style.stylized-character-maturity
version: 4
priority: 60
type: style
tier: 4
facet: style
facet_values:
  - stylized-character-maturity
  - stylized-humanoid
  - cute-doll-like
  - toy-character
  - chibi-risk
triggers:
  - stylized miniature humanoid where face maturity can drift younger or older
avoid_when:
  - not stylized or no human-like character maturity risk
dependencies:
  - core.fidelity-discipline
  - subject.human
conflicts: []
provides_anchors:
  - maturity_anti_collapse
---

# Style: perceived character maturity for stylized miniatures

## When to load

Use only for stylized miniatures, anime figurines, doll-like characters, plush characters, toy-like humanoids, or CG-like inserted figures where apparent character maturity is visually relevant. This is not a real-person age-identification rule.

## Rules

- Do not let cute or doll-like cues automatically collapse an adult-looking stylized subject into a childlike one.
- Treat apparent face maturity as a separate fidelity dimension from body, clothing, safety, attractiveness, or style.
- Do not let `cute`, `doll-like`, `toy-scale`, `large eyes`, `small mouth`, or `youthful` automatically collapse the face into infantile, childlike, chibi, toddler-like, baby-faced, or much younger proportions unless visible.
- Preserve maturity through face/head construction only: face length relative to head height, cheek volume, chin point/softness, eyelid heaviness, eye-to-face scale, mouth size, nose evidence, neck length, shoulder/head relationship, and expression restraint.
- Do not preserve maturity by emphasizing torso, chest, hips, waist, exposed skin, lingerie, cleavage, adult anatomy, glamour pose, or sexualized body traits.
- If large stylized eyes are present without a childlike face, say so: `large anime eyes without chibi proportions`, `small mouth without toddler-like roundness`, `soft cheeks but not baby cheeks`, `compact toy body but not a child body`.
- Use the weakest lock that prevents childlike drift. Avoid repeated maturity language that may age up, glamorize, or product-polish the subject.
- Repeat source crop and head scale after maturity language because maturity wording can cause zoom-out or normalized portrait drift.

## Optional negative contribution

Reject childlike face, baby-faced proportions, chibi head-to-body ratio, toddler cheeks, younger-looking doll, overly juvenile expression, and also reject opposite drift such as adult glamour model face, mature fashion-model styling, somber adult stare, or sexualized adult styling when not present.

## Optional settings contribution

- Face fidelity locks: preserve source-supported stylized face maturity without younger childlike simplification or older glamour upgrading.
- Aesthetic and non-identifying appearance locks: mature-cute/stylized balance if visible.
