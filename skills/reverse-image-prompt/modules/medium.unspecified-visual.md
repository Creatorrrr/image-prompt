---
id: medium.unspecified-visual
version: 2
priority: 40
type: medium
tier: 2
facet: medium
facet_values:
  - unspecified
  - unknown-medium
  - medium-fallback
triggers:
  - medium is ambiguous or not worth classifying
avoid_when:
  - photographic, screenshot/UI, or non-photographic rendering medium is visibly clear
dependencies:
  - core.visual-evidence
  - core.fidelity-discipline
conflicts:
  - medium.photographic-capture
  - medium.non-photographic-rendering
  - medium.screenshot-ui
provides_anchors:
  - unspecified_visual_medium
---

# Medium: unspecified visual fallback

## When to load

Load only when no specific medium module clearly applies, or when the medium is visually ambiguous enough that forcing `photographic`, `screenshot`, or `rendered` would be less faithful than staying neutral.

## Rules

- When no specific medium is clear, preserve only visible medium evidence without forcing a photographic or rendered style.
- Name the observable surface qualities instead of inventing a medium: flat/volumetric appearance, edge softness, pixelation, noise, compression, linework, screen glow, paper texture, blur, lighting behavior, or material shading when visible.
- Do not default to `photorealistic`, `photo`, `digital art`, `anime`, `3D render`, `cinematic`, or `studio` unless the source visibly supports that medium.

## Prompt additions

Use neutral wording such as `source-faithful visual medium`, `medium remains ambiguous`, or direct visible texture/capture cues.

## Negative additions

Reject forced photo realism, forced illustration, forced 3D rendering, forced app UI, or a cleaner medium category than the source supports.

## Settings additions

- Medium fallback locks:
