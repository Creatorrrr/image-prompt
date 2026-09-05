---
id: detail.low-quality-artifacts
version: 4
priority: 70
type: detail
tier: 3
facet: detail-risk
facet_values:
  - low-quality
  - compressed
  - underexposed
  - motion-blurred
  - noise
  - haze
  - soft-focus
  - artifact
  - low-resolution
triggers:
  - low-res, compression, blur, noise, underexposure, artifacts, casual capture
avoid_when:
  - clean high-detail source without degradation
dependencies:
  - core.visual-evidence
  - core.fidelity-discipline
conflicts: []
provides_anchors: []
---

# Detail: low-quality, compression, blur, and artifact fidelity

## When to load

Load when degraded capture quality is visually important or when a generator is likely to over-polish the image.

## Detection cues

- compression blocks, social-media softness, small image upscaling, smeared edges
- low-light noise, chroma noise, crushed shadows, clipped highlights
- motion blur, camera shake, rolling-shutter smear
- haze, bloom, low contrast, sharpening halos, noise reduction plasticity
- low-legibility text or background due to resolution

## Prompt additions

- Put fidelity ceiling near the beginning of `PROMPT:` when degradation controls the look.
- State relative focus hierarchy: what is least soft, what is heavily blurred, what remains indistinct.
- Calibrate underexposure. Distinguish fully crushed black regions from dark low-contrast regions that still show folds, edges, face planes, object silhouettes, or background detail.
- Preserve haze, softness, noise, compression, and low-detail edges. Do not request `crisp`, `pristine`, `sharp`, `clean`, or `high quality` unless the source is actually clean.
- Mention artifact distribution: edges, shadows, flat color areas, UI bands, background, skin/hair, text, motion direction.
- For phone-video, screenshots, social-media captures, or compressed casual sources, promote visible imperfections into positive prompt constraints before any aesthetic or material polish. Name low-resolution edge softness, compression smearing, motion-soft groups, flattened background massing, haze, bloom, clipped highlights, low-legibility marks, and sensor/app artifacts when visible.
- Treat distant or secondary background elements in degraded captures as massing and artifact planes before category labels. Lock them as blurred, low-legibility, compressed, partially cropped, or secondary unless the source clearly makes them the subject.

## Optional negative contribution

Reject over-sharpening, clean studio quality, HDR upgrade, noise removal, plastic smoothing, brightening shadows into invented detail, erasing compression, perfect focus, clean text, detailed background, polished render, and making the image more cinematic or commercial than the source.

## Optional settings contribution

- Quality/Fidelity: degraded/soft/compressed/noisy/hazy/underexposed as visible.
- Focus and depth-of-field locks: relative focus hierarchy.
- Film/camera/sensor or medium artifact locks: artifact types and distribution.
