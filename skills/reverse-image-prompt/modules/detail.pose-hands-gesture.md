---
id: detail.pose-hands-gesture
version: 5
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

- body crop and visible body parts
- head direction, head tilt, chin angle, gaze, neck visibility
- shoulder line angle, torso orientation, twist, lean, posture, spine/action line
- shoulder/hip height difference, weight distribution
- the support plane under the body, the side of any nearby boundary containing the torso and center of mass, and which parts cross or overlap that boundary
- arm direction, elbow bend, forearm angle, wrist angle
- hand placement, finger visibility, object grip, contact point
- leg placement, knee bend, ankle/foot placement if visible
- negative space and crop boundaries
- approximate pose landmark coordinates when helpful

For side/back, over-shoulder, profile-glimpse, or partly turned human poses, preserve asymmetry separately from category labels. State which side profile, shoulder edge, torso twist, cropped limb, visible side/back/front plane, and hidden planes are present. Avoid summarizing as `back view`, `rear view`, `over shoulder`, or a generic fashion pose if that would square the body to camera, lose the visible face/profile evidence, or complete hidden regions.

For contact gestures, describe the contact as a spatial relationship:

- both participating elements and the exact body/object regions involved
- approximate size and angle of each contacting part
- visible fingers or endpoints
- contact point and compression
- overlap and hidden portions
- where the interacting element begins and ends
- which side or zone contains the subject before and after the contact boundary
- whether there is pinch gap, pulling tension, weight, pressure, load-bearing support, stabilizing contact, or only passive touch

Do not infer that a touched element carries body weight. When a structure or edge divides space, keep the torso and center of mass on the source-visible side unless the image clearly shows a crossing, straddling, hanging, or suspended pose.

If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

## Optional negative contribution

Reject mirrored pose, changed head tilt/gaze/shoulder angle/torso lean, altered arm/elbow/wrist/hand/finger positions, added or removed hands, extra/missing fingers, malformed grip, generic fashion/action pose, contact point moved, wrong side of a boundary, invented body-weight support, unintended crossing or hanging, pinching/pulling/holding invented, longer limbs or props, and occlusion changes that reveal hidden areas.

## Optional settings contribution

- Pose fidelity locks:
- Scale/interaction anchor locks:
- Coordinate and anchor locks:
