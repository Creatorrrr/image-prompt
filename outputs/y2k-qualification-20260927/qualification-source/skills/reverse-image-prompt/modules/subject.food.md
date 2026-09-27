---
id: subject.food
version: 4
priority: 65
type: subject
tier: 2
facet: subject
facet_values:
  - food
  - drink
  - plating
  - table-setting
triggers:
  - food, drink, plating, table setting
avoid_when:
  - no food/drink subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Subject: food and drink fidelity

## When to load

Load when food, drink, cooking, plating, or table setting is visually important.

## Prompt additions

- Identify food/drink visually and conservatively. Use `appears to be` for ambiguous dishes.
- Lock plating/container geometry: plate/bowl/glass/cup shape, rim, fill level, crop, angle, position, and scale.
- Describe food texture and structure: sauce pooling, crumbs, seeds, char, steam, condensation, bubbles, foam, melted areas, layers, glaze, oil sheen, moisture, burnt/dry/soft/crisp cues.
- Preserve color temperature and appetite level. Do not make food fresher, cleaner, glossier, more symmetrical, more abundant, or more professionally styled unless visible.
- Describe utensils, napkins, hands, table surface, background clutter, and shadows as secondary if secondary.
- For labels/menus/packaging, combine with `detail.text-logo-label`.

## Optional negative contribution

Reject professional food-styling upgrade, extra garnish, extra steam, cleaner plate, fuller portion, changed dish type, added utensils, perfect symmetry, fake glossy sauce, crisp text/menus when not visible, and commercial studio lighting if source is casual.

## Optional settings contribution

- Category-specific locks: dish/container geometry, texture, portion size, table context, lighting, and fidelity ceiling.
