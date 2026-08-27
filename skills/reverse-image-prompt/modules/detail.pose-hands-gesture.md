---
id: detail.pose-hands-gesture
version: 7
priority: 78
type: detail
tier: 3
facet: detail-risk
facet_values:
  - hands
  - pose
  - gesture
  - grip
  - contact
  - limb-mechanics
  - negative-space
triggers:
  - sensitive visible pose, hands, grip, limb mechanics, contact gesture
avoid_when:
  - hands/gesture/pose mechanics are not important or not visible
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors: []
---

# Detail: pose, hands, gesture, and contact

## When to load

Load when pose mechanics, hands, fingers, object grip, contact, limb placement, or crop-sensitive body orientation can drift.

## Prompt additions

Describe mechanics rather than generic pose labels:

In `prompt`, select only the macro action and decisive P0/P1 relations from the list below. Group non-material joints, fingers, coordinates, and hidden mechanics; never complete them for checklist coverage. Use exhaustive axis disposal only in `audited`.

- crop, visible parts, negative space, and useful landmarks
- head/chin/gaze/neck; shoulder line, torso twist/lean, action line, and weight distribution
- support plane, torso/center-of-mass side of nearby boundaries, and crossings
- arm/elbow/forearm/wrist; hand/finger/grip/contact; visible leg/knee/foot placement

For side/back, over-shoulder, profile-glimpse, or partly turned human poses, preserve asymmetry separately from category labels. State which side profile, shoulder edge, torso twist, cropped limb, visible side/back/front plane, and hidden planes are present. Avoid summarizing as `back view`, `rear view`, `over shoulder`, or a generic fashion pose if that would square the body to camera, lose the visible face/profile evidence, or complete hidden regions.

Treat pose, hand placement, and occlusion as independent from a person-aesthetic anchor. Keep them protected unless the anchor explicitly intends `pose-occlusion`, cites P0/P1 evidence, and decomposes into this module's control. Emit the material pose result before the appearance passage so aesthetic wording cannot silently frontalize, straighten, or restage it.

For contact gestures, describe the contact as a spatial relationship:

- participating elements, exact regions, size/angle, and visible endpoints
- contact point, compression, overlap, hidden portions, and element extent
- subject zones on either side of the contact boundary
- pinch gap, tension, pressure, load-bearing, stabilization, or passive touch only when visible

Do not infer that a touched element carries body weight. When a structure or edge divides space, keep the torso and center of mass on the source-visible side unless the image clearly shows a crossing, straddling, hanging, or suspended pose.

If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

## Optional negative contribution

Reject mirrored or generic pose, changed head/shoulder/torso/limb/hand relations, malformed grip or fingers, moved contact, wrong boundary side, invented load/crossing/tension, extended parts, or revealed occlusion.

## Optional settings contribution

- Pose fidelity locks:
- Scale/interaction anchor locks:
- Coordinate and anchor locks:
