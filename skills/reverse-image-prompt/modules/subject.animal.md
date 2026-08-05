---
id: subject.animal
version: 4
priority: 65
type: subject
tier: 2
facet: subject
facet_values:
  - animal
  - pet
  - wildlife
  - creature-as-animal
triggers:
  - animal, pet, wildlife, or creature treated visually as an animal
avoid_when:
  - no animal-like subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Subject: animal fidelity

## When to load

Load when an animal, pet, wildlife subject, or animal-like creature is visually important.

## Detection cues

Species or type may be clear, ambiguous, stylized, cropped, or partially hidden. Use broad visual description if exact species/breed is uncertain.

## Prompt additions

Describe only visible animal evidence:

- species/type or broad animal class when clear; otherwise `small animal`, `large animal`, `bird-like`, `dog-like`, `cat-like`, etc.
- head shape, muzzle/beak/snout, ear shape, eye placement, whiskers, horns/antlers, tail, paws/hooves/claws/fins/wings if visible
- fur/feather/scale/skin texture, length, pattern, matting, wetness, sheen, color distribution
- body posture, weight distribution, gait, curled/sitting/standing/flying/swimming mechanics
- gaze, mouth position, tongue/teeth visibility, expression-like cues without assigning human intent
- scale relative to hands, furniture, environment, other animals, or frame
- crop and hidden limbs/tail/wings

For pets, preserve candid capture and ordinary body shape. Do not make the animal cuter, cleaner, fluffier, more symmetrical, more puppy/kitten-like, more studio-lit, or more breed-standard than the source.

## Optional negative contribution

Reject wrong species/breed-like drift, extra limbs/wings/tails, humanized expression, over-cute pet photography, cleaned fur, over-sharp eyes, changed coat pattern, full body when cropped, missing visible tail/ears/paws, and background/scale changes that alter animal size.

## Optional settings contribution

- Category-specific locks: animal type, texture, posture, crop, scale, and visible markings.
