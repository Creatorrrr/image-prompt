---
id: detail.human-body-form
version: 5
priority: 80
type: detail
tier: 3
facet: detail-risk
facet_values:
  - body-form
  - body-proportion
  - muscle-definition
  - body-tension
  - skin-surface
  - body-region-hierarchy
triggers:
  - visible human body form, proportion, contour, tissue character, muscle definition, skin rendering, or region hierarchy materially carries the image
avoid_when:
  - the body is small, indistinct, fully covered, or merely incidental
dependencies:
  - core.frame-coordinates
  - core.fidelity-discipline
  - subject.human
conflicts: []
provides_anchors:
  - human_body_form_signature
  - muscle_lighting_separation
  - skin_surface_signature
  - body_region_hierarchy
  - persistent_induced_form_split
  - skin_color_contract_handoff
---

# Detail: human body form, proportion, and surface

## When to load

Load only when visible body form is a first-order part of the image's identity or perceptual appeal: source-relative proportion, silhouette, contour rhythm, tissue character, muscular definition, skin surface, or the hierarchy among body regions. Do not load merely because a person is present.

## Analysis

Start with the large-scale form proposition before region detail. State directly what visible quality carries the impression—such as long-lined, compact, broad, narrow, soft, firm, relaxed, tense, delicate, sturdy, or strongly defined—then test it against observable causes. A broad descriptor is a hypothesis, not a substitute for evidence.

Build a visible human-body form signature from source-supported proportion, contour, tissue, tension, and region hierarchy rather than from a body-type label.

Split persistent body-form evidence from induced appearance before selecting prompt controls. Give pose-, perspective-, garment-, light-, occlusion-, or processing-induced shape one causal owner; do not restate it as intrinsic anatomy.

Use only the axes that materially distinguish the source:

- **Proportion:** source-relative spans and transitions among head, shoulders, ribcage/torso, waist, pelvis/hips, arms, legs, hands, and feet where visible. Prefer relationships such as `shoulders only slightly wider than the waist` over inferred measurements.
- **Contour and tissue:** straight or curved outer contours, abrupt or gradual width changes, bony landmarks, soft tissue transitions, firmness, softness, compression, folds, and where contours disappear into clothing, crop, or shadow.
- **Tension and posture:** relaxed suspension, bracing, extension, compression, twist, weight-bearing, or flexion. Distinguish persistent form from a temporary pose effect.
- **Definition:** Separate visible muscle or skeletal definition from contour created by pose, perspective, garment pressure, highlight, self-shadow, and cast shadow.
- **Surface:** Describe skin as a surface system: lightness, hue family, saturation, undertone, tonal variation, finish, texture, and response to light only where visible.
- **Hierarchy:** Assign each visible body region a hierarchy role—primary form, structural connector, supporting mass, edge crop, or low-legibility background evidence.

Analyze transitions between regions, not only isolated sizes. Garment asymmetry and pose asymmetry remain independent; neither may supply the other's missing evidence.

## Perspective and light separation

- Establish camera distance, angle, and foreshortening before treating image-plane width as anatomy.
- Compare near and far counterparts when visible; do not force symmetry through an oblique view.
- Identify the largest bright and dark masses crossing the body, then decide whether they flatten, softly imply, separate, or strongly sculpt form.
- Do not translate smooth lighting into low muscularity, or hard directional shadow into greater muscularity, without contour evidence.
- Keep skin tone separate from exposure and color cast. Record both the underlying visible hue relationship and the illumination that shifts it.
- When skin tone is material, contribute region evidence to the shared Color/Tone Contract instead of independently owning illumination, global cast, or exposure. Keep human-surface evidence source-relative; do not install a preferred skin value, hue, saturation, undertone, or finish.
- Describe source-visible skin color through value, chroma, hue relations, tone zones, and light response. Do not use racial, ethnic, or demographic identity as a shortcut for those observable color controls.

## Evidence contribution

When body form is appearance-led, contribute one compact form proposition and only the decisive proportion, contour/tissue, light-to-form, surface, or hierarchy evidence. The output composer assigns the final clause owner. When body form is secondary, its evidence stays behind the primary face, action, object, or relationship and may require no standalone sentence.

Use a body-type, fitness, or beauty descriptor at most once and only when it reduces ambiguity. Immediately constrain its category prior with visible proportions, tissue transitions, posture, lighting, and crop. Avoid stacking synonyms that would exaggerate leanness, softness, muscularity, curvature, size, or polish.

Do not restate one form direction in the proposition, regional inventory, lighting description, and negative prompt. Merge those observations into one source-relative semantic slot, then delete redundant intensity.

Describe body regions in their source role. A region that acts mainly as a bright plane, dark silhouette boundary, negative-space edge, garment support, or cropped foreground mass should remain that role instead of becoming a separately posed focal subject.

## Diagnostic mode

If the visible appeal is substantially carried by body form or skin rendering, name that plainly first. Then explain which source-supported proportion, contour, tissue, tension, surface, lighting, and hierarchy cues produce the impression, and which pose or placement changes would remain compatible with it.

## Optional negative contribution

Reject only source-likely drift: category-default anatomy, exaggerated or erased definition, changed relative proportions, inflated foreground perspective, rigid symmetry, relighting that invents form, uniform plastic skin, altered undertone, completed cropped anatomy, or secondary regions promoted into the main subject.

## Optional settings contribution

- Body-form invariants:
- Perspective-versus-proportion locks:
- Skin and light-to-form locks:
- Flexible pose or placement dimensions:
