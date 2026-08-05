---
id: subject.vehicle
version: 4
priority: 62
type: subject
tier: 2
facet: subject
facet_values:
  - vehicle
  - car
  - bike
  - aircraft
  - boat
  - train
  - vehicle-interior
triggers:
  - car, bike, aircraft, boat, train, vehicle interior or exterior
avoid_when:
  - no vehicle subject
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors: []
---

# Subject: vehicle fidelity

## When to load

Load when a vehicle exterior, interior, or vehicle detail is visually important.

## Prompt additions

- Describe type conservatively: car, truck, motorcycle, bicycle, train, bus, boat, aircraft, vehicle interior, dashboard, wheel, etc.
- Lock viewpoint: front, rear, side, three-quarter, interior, dashboard, low/high angle, close crop, partial edge view.
- Describe visible geometry: grille, headlights, taillights, windshield, mirrors, wheels, fenders, roofline, doors, handlebars, cockpit, seats, rails, hull, wings, windows, reflections.
- Preserve crop and partial visibility. Do not complete the full vehicle if only a detail or edge is visible.
- Treat badges, license plates, decals, and brand-like marks as visible text/graphic marks, not external brand identification. Combine with `detail.text-logo-label`.
- Preserve environment interaction: road, garage, street, water, track, sky, motion blur, reflections, dirt, damage, shadows.

## Optional negative contribution

Reject wrong vehicle type, complete vehicle from cropped detail, invented badges/logos/license text, showroom upgrade, changed viewpoint, extra wheels/lights, removed dirt/damage/reflection, polished commercial render, wrong motion blur, and changed background context.

## Optional settings contribution

- Category-specific locks: vehicle viewpoint, visible parts, material/reflections, crop, and environment interaction.
