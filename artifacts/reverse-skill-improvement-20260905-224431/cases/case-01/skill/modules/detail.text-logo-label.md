---
id: detail.text-logo-label
version: 4
priority: 70
type: detail
tier: 3
facet: detail-risk
facet_values:
  - text-logo
  - text
  - logo
  - label
  - watermark
  - caption
  - ui-text
  - small-letters
triggers:
  - text, logo-like mark, label, watermark, caption, UI text, small letters
avoid_when:
  - no visible text or symbolic mark
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - low_legibility_text
---

# Detail: text, logos, labels, watermarks, and tiny marks

## When to load

Load when text, label marks, logo-like marks, signs, watermarks, UI text, chart labels, document text, or small graphic marks are visible.

## Prompt additions

- Preserve location, size, contrast, and readability level before exact transcription.
- Preserve location, size, contrast, orientation, perspective, opacity, softness, and readability level over exact transcription unless exact readable text is central.
- If text is small, partial, distorted, reflected, low-confidence, compressed, or secondary, describe it as low-legibility marks, faint letters, short word-like fragments, label blocks, or abstract marks.
- If incidental text is clearly readable despite being small, preserve exact visible characters and low-legibility rendering together. Do not let exact text become clean hero typography.
- For watermarks, product labels, package labels, background signs, reflected marks, engraved marks, and decorative monograms, distinguish text-plane role from exact content.
- Do not identify brands externally. Treat brand-like marks as visible graphic/text evidence unless the user explicitly asks for brand recognition and policy allows it.
- For UI text, combine with `medium.screenshot-ui` and preserve small size, opacity, and placement.
- For charts/documents, combine with `subject.document-data-diagram` and preserve layout before text content.
- For tiny ambiguous UI marks, cropped controls, small badges, or low-confidence symbols, preserve position, size, opacity, edge distance, and ambiguity over exact icon identity. If the internal mark is unclear, call it an abstract or low-legibility mark rather than a named icon, logo, app control, or readable symbol.

## Optional negative contribution

Reject random letters, invented words, crisp typography, enlarged text, prominent logo creation, readable brand marks, substituted times/numbers/labels, full captions, clean subtitles, extra watermarks, and exact text over-prioritized at the expense of placement and softness.

## Optional settings contribution

- UI/text/label locks when relevant: exact or low-legibility text, mark coordinates, size, contrast, and readability ceiling.
- Boundary and visibility-budget locks: small marks stay small and secondary.
