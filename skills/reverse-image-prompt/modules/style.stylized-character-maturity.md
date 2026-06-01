---
id: style.stylized-character-maturity
version: 2
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

- Treat apparent face maturity as a separate fidelity dimension from body, clothing, safety, attractiveness, or style.
- Do not let `cute`, `doll-like`, `toy-scale`, `large eyes`, `small mouth`, or `youthful` automatically collapse the face into infantile, childlike, chibi, toddler-like, baby-faced, or much younger proportions unless visible.
- Preserve maturity through face/head construction only: face length relative to head height, cheek volume, chin point/softness, eyelid heaviness, eye-to-face scale, mouth size, nose evidence, neck length, shoulder/head relationship, and expression restraint.
- Do not preserve maturity by emphasizing torso, chest, hips, waist, exposed skin, lingerie, cleavage, adult anatomy, glamour pose, or sexualized body traits.
- If large stylized eyes are present without a childlike face, say so: `large anime eyes without chibi proportions`, `small mouth without toddler-like roundness`, `soft cheeks but not baby cheeks`, `compact toy body but not a child body`.
- Use the weakest lock that prevents childlike drift. Avoid repeated maturity language that may age up, glamorize, or product-polish the subject.
- Repeat source crop and head scale after maturity language because maturity wording can cause zoom-out or normalized portrait drift.

## Negative additions

Reject childlike face, baby-faced proportions, chibi head-to-body ratio, toddler cheeks, younger-looking doll, overly juvenile expression, and also reject opposite drift such as adult glamour model face, mature fashion-model styling, somber adult stare, or sexualized adult styling when not present.

## Settings additions

- Face fidelity locks: preserve source-supported stylized face maturity without younger childlike simplification or older glamour upgrading.
- Aesthetic and non-identifying appearance locks: mature-cute/stylized balance if visible.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy Perceived Character Maturity for Stylized Miniatures

## Perceived Character Maturity for Stylized Miniatures

Use this section only for stylized miniatures, anime figurines, doll-like characters, plush characters, toy-like humanoids, or CG-like inserted figures where apparent character maturity is visually relevant. This is not a real-person age-identification rule. Do not infer exact age, identity, or hidden anatomy.

Treat apparent face maturity as a separate fidelity dimension from body, clothing, safety, attractiveness, or style. Do not let `cute`, `doll-like`, `toy-scale`, `large eyes`, `small mouth`, or `youthful` automatically collapse the face into an infantile, childlike, chibi, toddler-like, baby-faced, or much younger reading unless the source visibly has those proportions.

- Describe perceived character maturity using neutral visual construction cues, not real-person identity claims. Prefer source-supported phrases such as `mature-cute stylized figure face`, `stylized young-adult anime-figure facial balance`, `not chibi`, `not baby-faced`, `less infantile cheek volume`, `defined but soft chin`, `longer face-to-head balance`, and `restrained expression` when the source supports that reading.
- Preserve maturity through face and head construction only: face length relative to head height, cheek volume, chin point or softness, eyelid heaviness, eye-to-face scale, mouth size, nose evidence, neck length, shoulder/head relationship, and expression restraint.
- Do not preserve maturity by emphasizing torso, chest, hips, waist, exposed skin, lingerie, cleavage, adult anatomy, glamour pose, or sexualized body traits. If the subject is a clothed miniature, keep the torso and outfit as cropped, softened, source-visible garment geometry.
- If the source shows large stylized eyes but not a childlike face, state that distinction directly: `large anime eyes without chibi proportions`, `small parted mouth without toddler-like roundness`, `soft cheeks but not baby cheeks`, and `compact toy body but not a child body`.
- Audit prompt language for younger-looking drift before final output. Replace or qualify broad terms that bias younger, such as `young girl`, `little girl`, `childlike`, `baby doll`, `child`, `teen`, `youthful` by itself, `adorable child`, `innocent child`, `tiny child`, `kawaii girl`, `chibi`, or `cute girl`, unless those are visibly required by the source. When `doll-like` or `cute` is necessary, pair it with source-specific non-child face construction cues.
- In `NEGATIVE PROMPT:`, include image-specific exclusions for apparent-maturity drift when relevant: `childlike face`, `baby-faced proportions`, `chibi head-to-body ratio`, `toddler cheeks`, `younger-looking doll`, `overly juvenile expression`, or `rounder infantile face`. Also include the opposite drift, such as `adult glamour model face`, `mature fashion-model styling`, `somber adult stare`, or `sexualized adult styling`, when those are not present.
- In `RECOMMENDED SETTINGS:`, add a face or aesthetic lock that preserves apparent character maturity and rejects both younger childlike simplification and older glamour/adult-model upgrading when this axis matters to likeness.
- Balance maturity locks against overcorrection. Preserving a more mature stylized face must not shrink the source's large eyes, make eyelids overly sleepy, over-lengthen the face, sharpen the chin into a fashion-model jaw, darken the expression into a somber stare, beautify the subject, or widen the crop to reveal more body.
- If the source face is mature-cute, use the weakest lock that prevents childlike drift. One concise sentence about face construction plus direct negative exclusions is usually better than repeated maturity language that may age up, glamorize, or product-polish the subject.
- Repeat source crop and head scale after maturity language when the source is crop-sensitive. Maturity wording often causes generators to zoom out or normalize into a complete portrait; counter this by restating that the head remains source-sized, the lower body or hidden regions remain incomplete, and foreground occluders or support surfaces remain in their source positions.
- Treat apparent-maturity drift as a major comparison failure in iterative work. If a generated result looks substantially younger, older, more childlike, or more glamour-adult than the source, the next skill revision should address the specific face/head cue that failed instead of only adjusting crop, pose, lighting, or accessories.
