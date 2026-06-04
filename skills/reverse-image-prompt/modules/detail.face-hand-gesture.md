---
id: detail.face-hand-gesture
version: 1
priority: 75
type: detail
tier: 3
facet: detail-risk
facet_values:
  - face-hand-gesture
  - cheek-hand
  - partial-cheek-hand
  - hand-near-face
  - face-touching-hand
triggers:
  - tight portrait or selfie where a hand touches, supports, frames, or partly occludes the face
avoid_when:
  - no visible hand near the face
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
  - subject.human
  - detail.pose-hands-gesture
conflicts: []
provides_anchors:
  - partial_cheek_hand_budget
---

# Detail: face-hand gesture

## When to load

Load when a close portrait or selfie has a hand touching, supporting, pointing near, framing, hiding, or overlapping the face, especially when the hand is cropped, secondary, or likely to become a full pose or manicure subject.

## Prompt additions

Keep cheek-hand contact as a partial edge-cropped support gesture when that is what the source shows.

- Describe the hand's contact geometry before nail, glove, sleeve, jewelry, or skin detail: which side it enters from, approximate bounding box, finger direction, wrist crop, contact point, overlap, and whether it supports, frames, presses, or merely hovers near the face.
- If the hand is secondary to the face, say so directly. Keep it partial, cropped, low-detail, and source-sized instead of a centered foreground hand.
- Use source-supported wording such as `partial fingertips tucked under the cheek/jaw`, `small fingers at the cheek edge`, `edge-cropped hand near the face`, or `cropped sleeve anchoring the gesture`.
- Preserve the sleeve, glove, hair, face, or crop edge that bounds the hand. Do not let the generator reveal the full wrist, full palm, full arm, or a cleaner hand pose unless visible.
- Keep nail and manicure details brief when they are not the subject; tiny decorations should stay low-legibility and source-sized.

## Negative additions

Reject full hand poses, peace signs, manicure-centered foregrounds, uncropped wrists, recentered hands, enlarged fingers, moved hands that reveal hidden cheek/jaw/neck areas, extra fingers, missing fingers, and hand gestures that no longer contact or frame the face as in the source.

## Settings additions

- Pose fidelity locks: preserve hand-to-face contact geometry, side, crop, and partial visibility.
- Occlusion fidelity locks: keep face, sleeve, glove, hair, and crop boundaries as the hand's limiting anchors.
- Focus and detail locks: hand/nail detail remains no sharper or more dominant than source visibility supports.
