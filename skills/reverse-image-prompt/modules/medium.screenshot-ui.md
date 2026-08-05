---
id: medium.screenshot-ui
version: 4
priority: 76
type: medium
tier: 2
facet: medium
facet_values:
  - screenshot-ui
  - screenshot
  - screen-recording
  - app-capture
  - social-video-frame
  - camera-preview-ui
  - ui-overlay
triggers:
  - screenshot
  - screen recording
  - app capture
  - social-video frame
  - camera preview UI
  - visible status bar, control band, comment field, crop marks, UI overlay
avoid_when:
  - pure photo with no UI overlay
dependencies:
  - core.frame-coordinates
  - concept.screen-frame-within-frame
  - detail.text-logo-label
conflicts:
  - medium.unspecified-visual
provides_anchors:
  - screenshot_ui_split
  - absent_ui_controls
---

# Medium: screenshot, app, and social-video UI fidelity

## When to load

Load when the source is or includes a screenshot, screen recording, social-video frame, camera preview, app capture, or any UI overlay.

## Detection cues

- status bar/time/battery icons
- top or bottom app chrome
- comment/input field
- player controls, scrub bars, crop marks, camera preview controls
- reaction buttons, profile icons, side action stack, captions, subtitles, watermarks
- transparent icons floating over image content

## Prompt additions

- Audit the exact UI/content split before emitting.
- Do not invent absent UI controls.
- Treat UI overlays as composition-critical image-plane bands, not decorative afterthoughts.
- Lock exact UI/content split: y-start, height, opacity, corner radius, text size, icon size, edge distance, and whether overlays sit on transparent background or a solid/semitransparent band.
- Distinguish transparent overlay icons from app chrome bands. If top icons float over video/background with no black rectangle, say so and reject a black status/header bar.
- State which controls are present and which common controls are absent, so the generator does not add default social UI.
- Preserve overlay restraint. If the source has only a simple status bar, one bottom field, one crop mark, or one ambiguous control, do not invite a full modern app interface.
- For tiny UI marks, combine with `detail.text-logo-label` and keep low-legibility.
- If a short progress line or edge mark exists, preserve observed length and discontinuity. Do not call it a full progress bar unless visible.

## Optional negative contribution

Reject home indicators, heart/reaction buttons, share buttons, profile avatars, side action stacks, progress bars, captions, subtitles, top app chrome, branded headers, enlarged UI controls, black top bars, full app interface, random UI icons, clean typography, full-width timeline tracks, and scrub knobs unless actually visible.

## Optional settings contribution

- UI/text/label locks when relevant:
- Boundary and visibility-budget locks: UI bands and absent controls.
- Coordinate and anchor locks: overlay y-starts, heights, edge distances, and opacity.
