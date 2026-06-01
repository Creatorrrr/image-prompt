---
id: concept.scale-miniature
version: 2
priority: 88
type: concept
tier: 1
facet: relationship
facet_values:
  - scale-miniature
  - miniature-in-real
  - toy-scale
  - figurine
  - small-figure-real-environment
triggers:
  - small physical figure, toy, figurine, plush, miniature, or scale contrast in a real environment
avoid_when:
  - ordinary full-scale subject with no scale contrast
dependencies:
  - concept.primary-relationship
  - core.frame-coordinates
conflicts: []
provides_anchors:
  - miniature_scale
  - endpoint_sensitive
  - polish_amplifying
---

# Concept: stylized miniatures in real environments

## When to load

Use only when visible evidence supports a small stylized physical figure, doll, figurine, plush, toy, collectible, or CG-like miniature placed inside a real photographed environment. Treat miniature-vs-real-world scale as a first-order concept lock, not a style detail.

## Detection cues

- Toy-scale subject near real hands, fingers, household objects, table edges, bedding, screens, or room elements.
- Molded, plush, synthetic, or stylized material visible under real-world lighting.
- Tight crop where the miniature's head/body is large in frame but real-world anchors reveal small scale.
- Casual phone-video compression or low-detail edges around a miniature object.

## Prompt additions

- Lead with measured frame shape, casual capture fidelity, and miniature-vs-real-world scale relationship before attractive character design.
- If a real hand, finger, tool, household object, support surface, or foreground prop interacts with the miniature, lock the contact point, contact area, contact direction, touched endpoint, overlap, untouched regions, and whether anything is lifted or under tension.
- Distinguish passive contact from active manipulation. Avoid `pinch`, `hook`, `pull`, `grip`, `hold`, or `petting` unless visible.
- Contact correction must not widen the shot. Keep tight subject scale, edge cuts, foreground support height, incomplete body visibility, and awkward close-camera framing.
- Describe support geometry before gesture when a hand or prop rests on a cushion edge, blanket fold, table edge, ledge, step, ridge, or raised foreground boundary.
- Preserve the subject as a photographed or captured object when supported: synthetic material, molded surface, seam-like construction, toy scale, real room lighting, mixed-media insertion. Reject life-size human or polished product render drift.
- For low-resolution or casual phone-video captures, put compression softness, focus hierarchy, motion softness, low-detail edges, imperfect room lighting, and casual capture noise near the beginning and in critical locks.
- For small appendages, plush extensions, fuzzy tails, wires, antennae, ornaments, ribbons, straps, cords, tags, or endpoints, lock bounded footprint, path, width budget, endpoint, contact point, and low-detail scale before category nouns.

## Negative additions

Reject life-size human, pure 2D illustration if the source is physical, polished product render, complete seated figure when cropped, full-body product view, zoomed-out scene, added floor, extra environmental breathing room, larger appendages, full loops/ropes/scarves replacing narrow endpoints, high-polish collectible sharpness when source is compressed.

## Settings additions

- Scale/interaction anchor locks: miniature scale relative to hand/object/surface.
- Coherence/realism ceiling locks: captured toy-scale object in real environment; no life-size normalization.
- Focus and depth-of-field locks: phone/compression softness if present.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy Stylized Miniatures in Real Environments

## Stylized Miniatures in Real Environments

Use this section only when visible evidence supports a small stylized physical figure, doll, figurine, plush, toy, collectible, or CG-like miniature placed inside a real photographed environment. Do not apply these rules to ordinary full-size people, ordinary product shots, or pure illustrations unless the source visibly depends on miniature-vs-real-world scale contrast.

When this source type is present, treat the scale relationship as a first-order concept lock rather than a style detail.

- Lead with the measured frame shape, casual capture fidelity, and miniature-vs-real-world scale relationship before describing attractive character design.
- If a real hand, finger, tool, household object, support surface, or foreground prop interacts with the miniature, lock the interaction as a small image-plane relationship: contact point, contact area, contact direction, touched endpoint, overlap, what remains untouched, and whether anything is lifted or under tension.
- Distinguish passive contact from active manipulation. If the source shows a hand resting on a support surface and only one fingertip lightly touching an appendage or prop, describe the support surface, relaxed finger spread, fingertip-pad contact, lack of pinch gap, lack of lifted object, and absence of pulling tension. Avoid `pinch`, `hook`, `pull`, `grip`, `hold`, or `petting` unless those mechanics are visibly present.
- Contact or gesture correction must not widen the shot. If the source is a tight crop, keep the same tight subject scale, edge cuts, foreground support height, incomplete body visibility, and awkward close-camera framing while describing the contact.
- For tight miniature interaction frames, audit for zoom-out and completion drift before final output. If the source shows a large head or upper body, partial lower body, and a foreground support or hand crop, state that the body remains incomplete and the camera stays close. Reject a complete seated figure, full-body product view, added floor, lowered foreground boundary, smaller face-to-frame ratio, or extra environmental breathing room unless visible in the source.
- When a foreground hand or prop rests on a raised support such as a cushion edge, blanket fold, table edge, ledge, step, ridge, or other high foreground boundary, describe that support geometry before the gesture. Lock the boundary y-position, thickness, seam or ridge direction, and whether the hand or prop lies over, behind, or below it.
- Foreground-support locks must preserve the main subject's face angle and scale. If the source has a large close-cropped head, partial torso, off-center gaze, or interrupted over-shoulder view, repeat those pose and scale locks after the support description so the scene does not recenter into a smaller frontal product composition.
- Preserve the subject as a photographed or captured object when visible evidence supports it. Mention synthetic material, molded surfaces, seam-like construction, toy scale, real room lighting, or mixed-media insertion only when visible; reject conversion into a life-size human, pure 2D illustration, or polished product render.
- Avoid broad medium labels that can upgrade the scene into a clean fantasy render. Prefer source-supported terms such as `small stylized figure`, `physical miniature`, `toy-scale subject`, `captured miniature`, `mixed-media phone capture`, or `video-compressed captured object`; avoid `AR-like`, `seamless CG`, `3D character`, `product photo`, or `detailed collectible` unless the source visibly depends on that reading.
- For low-resolution or casual phone-video captures of miniatures, put the fidelity ceiling near the beginning of `PROMPT:` and again in critical locks: compression softness, focus hierarchy, motion softness, low-detail edges, imperfect room lighting, and casual capture noise outrank collectible-product sharpness.
- When a background screen, poster, reflection, framed image, display, or secondary media layer contains anime, cartoon, human, object, or scenic imagery, keep it as a cropped, blurred, low-legibility background layer unless it is the actual subject. Do not describe enough internal content to make it a clean second subject.
- For small appendages, plush extensions, fuzzy tails, wires, antennae, ornaments, ribbons, straps, cords, tags, or similar endpoint-sensitive elements, lock their bounded footprint and endpoint. State whether the element is narrow, partial, soft-edged, secondary, touched only at the tip, cropped, or low-detail so the generator does not enlarge it into a blanket, scarf, rope, prop, full loop, or central object.
- If an appendage or plush extension is only a partial tapering endpoint, describe its visible path, width budget, endpoint, and contact point before using a category noun such as `tail`, `wire`, `strap`, `ribbon`, or `cord`. Avoid unqualified phrases such as `fluffy tail` or `long ribbon` when they could become a large standalone object.
- In the final prompt body, every mention of an endpoint-sensitive appendage should include scale language in the same sentence when the source shows only a narrow or partial element. If the element has a larger root but a narrow endpoint, separate root and endpoint so the generator does not enlarge the contact area.
- If the source includes a top-edge ornament, wire, clipped prop, partial fixture, or other border-adjacent detail, describe its incomplete arc or shape, crop pressure, thinness, and low-detail edge behavior before naming the motif.
- Before emitting, audit for polish-amplifying phrases in low-fidelity miniature interaction frames. Remove or qualify `highly polished`, `perfect`, `pristine`, `clean render`, `product photo`, `detailed collectible`, `glossy commercial`, and similar descriptors unless the source is actually polished. If synthetic material must be described, pair it with the source fidelity ceiling, such as `molded surface softened by phone-video compression`.
