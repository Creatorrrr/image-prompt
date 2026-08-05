---
name: reverse-image-prompt
description: Reverse engineer a standalone English text-to-image prompt from a provided image using visible evidence, routed subject/medium/relationship modules, and an adaptive model-aware output contract. Use for faithful reconstruction, semantic prompt extraction, polished-but-composition-faithful variants, diagnostic image analysis, negative prompts, or generation settings.
---

# Reverse Image Prompt

## Purpose

Turn one provided image into a standalone text-to-image prompt that preserves the visible concept, composition, crop, subject, pose, major-component spatial relationships, aesthetic signature, camera or rendering treatment, lighting, background, color, medium, and meaningful artifacts.

Default to **faithful** reconstruction. Preserve awkward, soft, cropped, partial, compressed, or mixed-media evidence instead of silently beautifying or completing it.

## Intent mode

Infer one mode from the request. Ask only when the modes would materially change the result and intent is genuinely unclear.

- `faithful` (default): preserve visible composition, relationships, and imperfections.
- `semantic`: extract the transferable concept, composition, and style without incidental defects.
- `polished-fidelity`: preserve concept and composition while removing only defects the user asks to improve.
- `diagnostic`: explain the evidence, uncertainties, and likely reproduction limits instead of pretending to provide a production-ready prompt.

## Required module loading

Always read the complete Tier 0 core:

- `modules/core.visual-evidence.md`
- `modules/core.frame-coordinates.md`
- `modules/concept.primary-relationship.md`
- `modules/core.fidelity-discipline.md`
- `modules/core.background-color.md`
- `modules/core.pre-emit-gate.md`
- `modules/core.output-contract.md`

Then resolve only the applicable routed modules from `manifest.json` or `modules/_registry.md`. When tools are available, run `tools/route_resolver.py` so unsupported facet values and over-budget routes fail visibly.

Read the full contents of every selected module before drafting. If sibling files cannot be read, use the smallest matching compiled profile; use `SKILL.compiled.all.md` only as the final fallback.

If the target generator is known, read `references/model-adapters.md` and apply only that generator's adapter.

## Workflow

1. Inspect only the provided image.
   - Use the attached image directly or inspect the exact local file.
   - If no image is available, ask for it.
   - Process multiple images independently unless the user clearly requests a combined prompt.

2. Use visible evidence only.
   - Do not identify people, characters, brands, artists, cameras, lenses, film stocks, or private identities from appearance.
   - Keep uncertainty internal during analysis. In the final generation prompt, describe the visible ambiguity itself with terms such as `indistinct`, `partially obscured`, `low-legibility`, or `soft-edged`; avoid weakening commands with repeated `likely` or `appears`.

3. Analyze silently in this order:
   1. Primary concept, perceptual relationship, and major-component spatial topology.
   2. Frame ratio, crop, subject scale, major zones, boundary sides, and edge interactions.
   3. Global aesthetic salience and the smallest source-specific look signature.
   4. Visible subjects, their image-plane roles, and—only when it materially reduces ambiguity—a compact broad person-gestalt anchor before local human detail.
   5. Pose, contact/support, containment, boundary crossing, occlusion, completion-prone regions, and negative space.
   6. Camera or virtual-camera behavior, perspective, focus, and blur.
   7. Lighting, atmosphere, color, contrast, highlights, and shadows.
   8. Background zones and depth layers.
   9. Medium, texture, artifacts, UI, and text marks.

4. Build and resolve this internal facet map:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face-detail, clothing, hands, text-logo, ui, small-props, cropped-edges, tight-selfie, face-hand-gesture, accessory-torso-budget
  style: []           # stylized-character-maturity or another narrow risk
```

5. Merge selected rules using this priority:
   1. Visible-evidence and safety limits.
   2. Primary concept, perceptual relationship, and any high-salience aesthetic signature.
   3. Frame ratio, crop, major zones, boundary sides, contact/support relations, and visibility budgets.
   4. Occlusion, reflection, screen/frame, replacement, scale, and continuity.
   5. Subject-specific fidelity.
   6. Medium, camera, lighting, focus, and artifact fidelity.
   7. Background, color, and secondary details.
   8. Generic style or aesthetic shorthand.

6. Draft the smallest prompt that carries every concept-critical constraint. If the source look is high-salience, place one compact Aesthetic Signature near the beginning; if it is neutral, use only one or two ordinary look cues. Give each major component or coherent group at least one explicit spatial relation to another component or stable scene zone. Give each major interaction one relation clause when its side, containment, contact, support, or depth order could otherwise flip. Prefer short labeled blocks or compact paragraphs over a field-completion checklist.

7. Apply the pre-emit gate and report prompt-only limits honestly.

## Routing rules

- Always load Tier 0.
- Select at least one subject and one medium; use the generic/unspecified fallbacks only when evidence is unclear.
- Load every visible Tier 1 relationship module, including both photographic and non-photographic medium modules for genuine mixed media.
- Load Tier 3 and Tier 4 modules only for visible, material risks.
- For a prominent or clearly readable human face, add `face-detail`; for a small, blurred, shadowed, or heavily occluded face, keep only scale-appropriate human evidence and do not invent micro-features.
- Treat the spatial topology of major components as Tier 0 evidence. Do not route it away as an optional detail merely because the scene has no special visual effect.
- Treat adaptive aesthetic analysis as Tier 0 evidence, not as a style preset. Do not load extra style modules merely to fill an aesthetic checklist.
- Keep the normal route within 3-8 non-core modules. Refine an over-budget facet map instead of loading every plausible module.
- Treat `ordinary`, `cropped-edges`, and `small-props` as core-handled observations unless another visible risk requires a dedicated module.
- Do not use broad labels such as `cinematic`, `studio`, `luxury`, `beauty shot`, or `high quality` when they would normalize source-specific evidence.

## Output selection

Always write the production prompt in English. Match the response language for diagnostic explanation unless the user asks otherwise.

- Always emit `PROMPT:` for generation requests.
- Emit `NEGATIVE PROMPT:` only when the user requests it or the named downstream generator supports a separate negative prompt.
- Emit `RECOMMENDED SETTINGS:` only when requested, when a target generator is known, or when source dimensions require a model-specific target-size explanation.
- For `diagnostic` mode, use ordinary analysis headings and include a candidate prompt only if useful.
- Essential crop, relationship, occlusion, high-salience aesthetic, and medium constraints must remain in `PROMPT:` even when optional sections are present.

Do not mention the attached/reference image inside the generated prompt.


---

# Compiled module bundle

The following module files were appended for runtimes that cannot read sibling files dynamically.



---

# Included module: `core.visual-evidence`

# Core: visual evidence

## When to load

Always.

## Rules

- Never refer to the source image in the final prompt. The prompt must remain usable after the image is removed.
- Describe visible evidence only; do not invent hidden structure or context.
- Do not assert identity, nationality, exact ethnicity, religion, personality, measurements, metadata, brands, artists, cameras, lenses, or film stocks from appearance. When `subject.human` permits one broad racial, ethnic, regional-appearance, or attractiveness category as a generation-oriented visual prior, treat it as a non-identifying approximation rather than a factual identity claim.
- Distinguish absence from uncertainty. Use `absent` only when the frame supports it; otherwise use visual descriptions such as `hidden`, `cropped out`, `indistinct`, `shadow-obscured`, or `low-legibility`.
- Keep epistemic qualifiers in analysis. In the final prompt, describe the visible ambiguity rather than repeatedly saying `appears`, `likely`, or `possibly`.
- In `faithful` mode, preserve visible softness, compression, blur, exposure problems, asymmetry, awkward crop, partial elements, and edge artifacts.
- In `semantic` mode, retain concept-defining imperfections but omit incidental capture defects.
- In `polished-fidelity` mode, improve only the dimensions requested by the user; do not silently alter crop, pose, relationships, identity-relevant appearance, or geometry.
- Give partial elements a visibility budget: what remains visible, how large it is, where it touches the frame, and whether it stays secondary or low-detail.
- Do not complete hidden anatomy, objects, clothing, text, reflections, or background fragments.

## Prompt contribution

Put the fidelity ceiling near the beginning only when it materially defines the image. State partial or incomplete evidence affirmatively: `only a narrow cropped strip remains visible`, `the lower half stays outside the frame`, or `the text remains small and indistinct`.

## Optional negative contribution

Reject only likely evidence drift: invented hidden content, completed crops, cleaner relighting, upgraded sharpness, or aesthetic normalization.


---

# Included module: `core.frame-coordinates`

# Core: frame, crop, and spatial anchors

## When to load

Always.

## Source frame

- Inspect the exact file dimensions when available and record them internally as source metadata.
- Treat aspect-ratio drift as a major fidelity failure.
- Separate source dimensions from the requested target size. Never assume the source pixel dimensions are accepted by the target generator.
- Preserve the measured ratio in plain language such as `narrow portrait`, `wide landscape`, or `source-specific portrait ratio`; add a decimal ratio only when it helps distinguish nearby shapes.
- Do not invent exact dimensions from a viewer preview.
- Put frame shape, crop, subject scale, and edge interactions before small object detail.
- Lock subject frame share and negative-space share before adding face or object micro-detail.
- Describe which evidence occupies the top, middle, bottom, left, center, and right zones when those bands control the composition.

## Spatial language

Prefer generator-friendly spatial relationships:

- `centered`, `left third`, `upper-right`, `near the bottom edge`
- `occupies roughly half the frame height`
- `touches the left edge`, `cropped above the knees`
- `overlaps the lower half of the face`
- `leaves a narrow band of background on the right`

## Relational coordinate frames

- Use frame-relative directions for composition and object- or scene-relative zones for physical relationships.
- Do not let `left`, `right`, `front`, or `behind` stand alone when viewpoint changes could reverse the intended side of a barrier, opening, surface, or container.
- Establish a visible shared reference plane when it disambiguates the scene: floor, ground, seat, platform, tabletop, interior volume, or another support region.
- Record which side of a boundary contains the subject's main mass and which parts, if any, cross, overlap, or remain on the other side.
- Separate apparent 2D overlap from 3D contact, containment, weight support, and depth ordering.
- Prefer a stable natural-language relation over extra coordinates. Coordinates lock placement in the frame but cannot by themselves establish physical topology.

Use normalized coordinates only for concept-critical anchors.

- Use no more than five numeric anchors in a normal prompt.
- Reserve them for seams, screen corners, occluder boundaries, UI bands, reflection joins, replacement zones, or unusual scale relationships that natural language cannot lock clearly.
- Use approximate ranges rather than false precision.
- Do not repeat the same coordinate in prose, negative prompt, and settings.
- When coordinates and natural-language placement disagree, keep the visible relationship and revise or remove the numeric estimate.

## Crop and completion

- Separate hair/head-outline cropping from facial-feature cropping.
- Name which important features remain fully inside the frame and which regions are hidden, occluded, or outside it.
- Preserve unusual headroom, edge bias, negative space, or full-frame scale.
- Prevent a salient face, hand, product, or text mark from being enlarged when that would erase source-visible context.

## Target-size handoff

If settings are requested:

- Report `Source frame` as metadata.
- Report `Target size` separately and validate it against the named generator.
- Prefer `auto` when no valid deterministic adapter is available.
- Explain any small ratio-preserving adjustment instead of presenting it as the original size.


---

# Included module: `concept.primary-relationship`

# Concept: primary visual relationship

## When to load

Always. Apply more deeply to occlusion, replacement, reflection, frame-within-frame, miniature scale, mixed media, collage, or other relationship-led images.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

An object-complete prompt can still fail when the overlap, alignment, scale, seam, replacement, foreground/background ordering, side of a boundary, or support relationship is wrong.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. Literal visible elements.
2. The relationship viewers are meant to perceive.
3. The stable reference zones: visible floor/ground/support plane, interior or exterior region, near or far side, foreground or background layer, and any frame, barrier, opening, or container boundary.
4. For each concept-critical pair, the participating parts, relative side or containment, contact point, support or load-bearing role, depth order, occlusion, and whether either element crosses the boundary.
5. The cues that create it: alignment, contour continuation, overlap, shared line, crop boundary, contact, scale match, reflection, replacement, frame, or medium contrast.
6. The one to three most likely failure modes.

Build a sparse relation graph rather than an inventory: connect each major component or coherent repeated group to at least one other major component or stable reference zone. Group crowds, repeated objects, or background clusters when they share the same relation. Do not enumerate every possible pair.

For ordinary images, state an ordinary premise and do not invent a special effect.

Distinguish image-plane overlap from scene-space containment, contact, and support.

Contact alone is underspecified. `Holding`, `leaning`, `resting`, `sitting`, `standing against`, or similar interaction verbs must not replace the visible geometry when a plausible spatial inversion would change the scene. Record which part touches which surface or edge, which element carries visible weight, and where the remainder of the subject sits relative to the boundary or support plane.

Use object- or scene-relative zones when screen left/right would be ambiguous. Prefer a visible shared reference such as the same side as the floor or platform, within an enclosure, outside an opening, or on the near/far side of a structure. Name a semantic side only when the image actually supports it.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record the join, seam, overlap, contact, or containment geometry.
- Record what stays hidden, partial, or absent.
- Record the required boundary side, support relation, layer order, scale relationship, and coherence ceiling.

## Prompt contribution

Write a construction recipe, not a prop list. Explain what each element contributes and the minimum geometry required for the effect to read correctly. Spend more words on the relationship than on secondary textures or labels.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Keep this selective: normally one to three interaction sentences are enough. Do not enumerate every pair of objects, and do not add coordinates when the topological relationship is already clear in natural language.

## Optional negative contribution

When a negative prompt is supported, reject only likely concept and fidelity drift: broken seams, wrong boundary side, inverted containment or support, implausible boundary crossing, wrong layer order, duplicated counterparts, completed hidden regions, normalized medium contrast, or a concept-critical element demoted to a generic prop.


---

# Included module: `core.fidelity-discipline`

# Core: fidelity discipline and anti-normalization

## When to load

Always. This module keeps every routed path from becoming cleaner, more generic, more attractive, more plausible, or more category-normalized than the source.

## Rules

- Cap generated polish to the source. If the source is casual, degraded, compressed, dim, soft, awkwardly framed, low-resolution, underexposed, socially edited, or non-editorial, prevent cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished drift.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal or product ideal. Keep roughness, awkwardness, asymmetry, styling, social-media look, visible mood, surface sheen, color cast, retouching level, and medium imperfections when present.
- Treat subject attractiveness and image polish as separate controls. A supported attractiveness anchor may describe the visible person gestalt, but it must not imply stronger symmetry, skin cleanup, makeup, styling, crop, focus, lighting, or editorial finish than the source.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or awkward capture, preserve that relationship above realism and plausibility.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever the label would pull the generator toward a common composition, cleaner styling, expanded crop, completed object, or more attractive category default. Put visible geometry, crop, relationship, medium, and fidelity constraints before shorthand labels.
- Treat source fidelity ceiling as an affirmative requirement: the output should not exceed the visible source in sharpness, cleanliness, glamour, lighting balance, polish, readability, symmetry, or plausibility unless the user explicitly asks for improvement.
- Do not use absolute enhancement terms such as `high quality`, `sharp`, `crisp`, `clean`, `pristine`, `luxury`, `cinematic`, or `studio` unless the source visibly supports them and they do not conflict with crop, lighting, artifacts, or ordinary capture.

## Aesthetic salience gate

Decide whether changing the global look while preserving the objects would materially change the image.

- **High-salience look:** select three to six mutually supporting anchors from tone curve and microcontrast; palette, cast, and saturation; sharpness distribution; diffusion, bloom, haze, grain, compression, or surface treatment; lighting character; and subject/environment hierarchy.
- **Neutral look:** use one or two ordinary visible cues. Do not create a special style block.
- **Ambiguous look:** describe only observed behavior and avoid named genre, camera, film, or era presets.

Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues.

Treat descriptive detail and rendered sharpness as independent controls. Detailed geometry may remain soft, low-contrast, compressed, flat, rough, or low-legibility. Do not let face, product, garment, or environment detail silently raise local sharpness, scale, polish, or visual priority.

Translate mood words into visible mechanisms. A term such as dramatic, nostalgic, cinematic, clean, or premium cannot replace its supported tone, color, light, sharpness, and texture evidence.

## Prompt additions

State the source fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent. Use source-specific counterweights such as `still visibly compressed`, `not upgraded into a studio portrait`, `not cleaned into a product shot`, or `not normalized into a plausible full scene`.

When the source look materially differs from a clean default, place a compact Aesthetic Signature near the beginning of `PROMPT:`. Keep its strongest look lock affirmative and repeat at most one highest-risk drift constraint near the end; do not scatter the same adjectives through every paragraph.

## Optional negative contribution

Reject beautification, over-polish, relighting, sharpening, style upgrade, social-media glamorization, product-shot cleanup, symmetry correction, plausible-scene normalization, expanded crop, and broad-label defaults that contradict visible evidence.

## Optional settings contribution

- Fidelity ceiling locks:
- Anti-polish and anti-normalization locks:
- Broad-label weakening locks:


---

# Included module: `core.background-color`

# Core: background, color, and environment zoning

## When to load

Always. Every image has a background, color structure, or negative-space field that can drift if ignored.

## Rules

- Analyze background zoning as image-plane structure: foreground, midground, background, edge bands, negative space, depth layers, occluded zones, dark masses, bright windows, flat fields, texture bands, and ambiguous low-detail regions.
- Preserve the source background's visual priority. If background elements are dim, cropped, blurred, low-legibility, partly hidden, or secondary, keep them as low-detail background massing rather than turning them into clean readable objects.
- Treat background legibility and information density as part of the source aesthetic. A named or distinctive background element must inherit the source-visible blur, haze, contrast, and detail ceiling rather than becoming a crisp landmark.
- Preserve color mood, palette, color cast, saturation, contrast, shadow color, highlight color, and local color relationships. Do not neutralize a visible cast or push the image toward a postcard, clean-room, catalog, cinematic, or studio palette unless that is visibly present.
- For underexposed, low-contrast, compressed, or hazy backgrounds, distinguish fully crushed regions from regions that still show folds, edges, silhouettes, texture, or environmental hints. Preserve remaining detail without turning dark areas into featureless black or brightly recovered scenery.
- Prevent clean-room drift for products, portraits, screenshots, documents, and ordinary scenes. Do not replace messy, partial, compressed, cropped, or ordinary background zones with a smooth backdrop, empty studio, clean wall, perfect sky, luxury interior, or tidy product surface unless visibly present.
- Treat background zoning as part of crop and coordinate fidelity. Edge bands, side strips, awkward headroom, bottom UI bands, floor/wall seams, horizon placement, poster edges, and environmental slivers must remain in their visible positions when they matter.

## Prompt additions

Describe background zones by position, mass, contrast, legibility, depth, and color behavior before using broad setting labels.

## Optional negative contribution

Reject postcard scenery, clean-room backdrop, studio sweep, tidy catalog surface, brightened recovered background, readable invented signage, removed clutter, added depth, and background elements becoming cleaner or more central than visible.

## Optional settings contribution

- Background zoning locks:
- Palette/color-cast locks:
- Low-legibility background massing locks:


---

# Included module: `core.pre-emit-gate`

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

- Confirm that `PROMPT:` contains the primary visual concept and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Preserve source hierarchy: dominant concept first, primary subject and interaction next, secondary elements last.
- Check whether a secondary element receives more words than its visible importance supports. Compress it when it does.
- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer visible spatial evidence.
- Use at most five numeric anchors unless the source is a layout-dense UI or diagram and numeric bands materially help.
- Confirm that every major component or coherent group has at least one explicit spatial relation to another component or stable scene zone; no major element should remain a free-floating inventory item.
- For every concept-critical interaction, confirm that the relevant side or zone, any contact parts, support role, containment, and depth order are explicit enough to prevent a plausible spatial inversion.
- Distinguish image-plane overlap from scene-space contact or support. A bare interaction verb is insufficient when the subject could be placed on the wrong side of a boundary while still satisfying the verb.
- Confirm that each primary subject's main mass remains in the source-visible region and that only visibly crossing or overlapping parts cross a barrier, opening, frame, edge, or support surface.
- Confirm every partial or edge-adjacent region remains partial; do not let wording imply a completed body, garment, object, reflection, screen, poster, or text block.
- Distinguish head/hair cropping from actual facial-feature cropping.
- If the source look is high-salience, confirm that its compact Aesthetic Signature appears before fine subject detail and that its anchors agree rather than mixing incompatible clean, hazy, sharp, flat, cinematic, casual, or studio defaults.
- Confirm that descriptive detail has not increased subject scale, local sharpness, background legibility, retouching, microcontrast, or lighting polish beyond the source.
- Remove `shallow depth of field`, beauty lighting, premium bokeh, clean digital capture, or other category defaults unless their visible mechanisms are actually supported.
- If a human face is prominent and readable, confirm the prompt includes a selective, scale-appropriate likeness set covering the strongest visible face geometry, expression/gaze, hair boundary, and surface/lighting cues. If one broad person-gestalt anchor materially reduces ambiguity, place it before—not instead of—the likeness set; ensure it remains an approximation rather than an identity claim and does not raise beauty polish.
- If a human face is small, soft, shadowed, or heavily occluded, remove speculative micro-features and preserve only reliable head orientation, hair mass, tone, and visibility.
- Remove repeated constraints that appear unchanged in the prompt, negative prompt, and settings.
- Remove unsupported camera, lens, identity, brand, artist, or hidden-content assumptions.
- Remove generic quality words that would raise polish above the selected intent mode.
- Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams are unlikely to reproduce reliably.

## Length and clarity

- Prefer one measured statement plus one drift constraint for a secondary element.
- Keep constraints concrete and observable.
- Do not repeat important locks merely to make the output look exhaustive.
- If the prompt has become a checklist of every possible visual field, rewrite around the image's actual hierarchy.


---

# Included module: `core.output-contract`

# Core: adaptive output contract

## When to load

Always. Apply after the visual analysis and routed modules.

## PROMPT

Emit only sections required by the selected output mode.

For a generation request, always emit:

```text
PROMPT:
...
```

Write a standalone English prompt in a skimmable order:

1. Scene, frame shape, medium, fidelity ceiling, primary concept, and any high-salience Aesthetic Signature.
2. Composition, crop, subject scale, major zones, major-component spatial topology, and up to five critical spatial anchors.
3. Subject appearance, pose, gaze, interaction geometry, contact/support, occlusion, and completion boundaries.
4. Camera or rendering behavior, lighting, color, focus, texture, and meaningful artifacts.
5. Compact constraints covering only the highest-risk drift.

Use short labeled blocks or compact paragraphs for complex images. Aim for the smallest prompt that preserves the source hierarchy; a typical prompt should not need every possible camera, anatomy, lighting, and settings field.

Keep essential requirements affirmative. Prefer `only a narrow cropped strip remains visible` over relying on `do not expand the strip` in another section.

Relate every major component or coherent group to another component or stable scene zone. Keep each concept-critical side, containment, contact, and support relation in `PROMPT:` as one compact affirmative sentence. Do not leave it implied only by an action verb, approximate coordinate, or negative prompt.

For a high-salience look, keep one compact Aesthetic Signature in the first or second paragraph before fine face, material, or background inventory. Use three to six source-supported anchors spanning only the dominant tone, color, sharpness, optical/surface, lighting, or hierarchy axes. For a neutral look, use one or two cues without a labeled block. Do not fill every axis or repeat the signature verbatim.

When `detail.human-face-likeness` is selected, keep one dedicated likeness passage. If `subject.human` selects a broad person-gestalt anchor, place that one compact anchor at the start of the passage, then immediately constrain it with scale-appropriate visible anchors. Never use demographic, beauty, or character shorthand as the whole likeness description.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

Use one compact, image-specific list. Do not duplicate the entire prompt. Include only likely failure modes that are difficult to express affirmatively.

When a negative prompt is supported, reject only likely concept and fidelity drift.

## RECOMMENDED SETTINGS

Emit only when requested, when a target generator is known, or when source dimensions require an adapter note:

```text
RECOMMENDED SETTINGS:
- Model:
- Source frame:
- Target size:
- Quality:
- Prompt-only limits:
```

- Include only fields that map to real controls of the target generator.
- Separate source dimensions from the requested target size.
- Omit irrelevant fields instead of filling them with prose.
- Read `references/model-adapters.md` before naming model-specific values.
- Keep visual locks in `PROMPT:`, not in settings.

## Diagnostic mode

For `diagnostic`, explain the evidence and uncertainties in the user's language. A candidate `PROMPT:` may follow, but do not force generation-only sections.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary relationship, crop, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.


---

# Included module: `concept.occlusion-replacement`

# Concept: occlusion and replacement surfaces

## When to load

Load when an object, hand, phone, screen, sign, book, card, foreground prop, shadow, hair, crop edge, or frame boundary hides a concept-critical area or substitutes for part of another subject.

## Detection cues

- Opaque rectangle or prop crossing a face, torso, product, label, or background.
- Only a sliver of a counterpart feature remains visible.
- A phone/screen/card/frame supplies content that visually replaces hidden features.
- The image would become a different scene if the occluder moved, shrank, rotated, or became transparent.

## Prompt additions

- Describe the occluder before attractiveness, product clarity, garment labels, or scene completion.
- Lock the occluder's image-plane footprint, approximate corners, rotation, border thickness if visible, and overlap boundary.
- State which real-layer features remain visible outside the occluder and which features are hidden by it.
- If a surface replaces hidden content, state what the replacement surface carries and how it lines up with the hidden area.
- State hidden features as absent in the real layer when supported by visible evidence. Do not let them reappear around the edges.
- Use an overlap polygon when needed: containing surface corners, edge crossing the subject, lower/inner edge hiding features, and maximum reveal outside the polygon.
- Preserve awkwardness. If a prettier or more plausible image requires moving the occluder away, keep the occluder and accept the awkward crop.

## Optional negative contribution

Reject moved, smaller, higher, lower, transparent, recentered, or cleaned-up occluders; hidden face/body/product/text features reappearing; full counterpart completion; conventional portrait/product clarity replacing the blocked view; seam mismatch; duplicate features on both sides of the occluder.

## Optional settings contribution

- Occlusion fidelity locks: occluder footprint, corners, rotation, edge crossings, hidden-feature budget.
- Completion/seam continuity locks: which hidden/counterpart features remain absent.
- Boundary and visibility-budget locks: slivers remain slivers; cropped areas stay cropped.


---

# Included module: `concept.reflection-mirror`

# Concept: reflection and mirror fidelity

## When to load

Load when reflection is a meaningful part of the image: mirror selfie, reflective product, water reflection, window reflection, glass overlay, glossy metal highlight, or reflected background layer.

## Detection cues

- Duplicated but softened or distorted subject/object.
- Visible mirror/window/glass edge or reflective plane.
- Reversed orientation, offset, transparency, blur, color shift, glare, or partial occlusion.
- Reflection contains only fragments, not a complete second scene.

## Prompt additions

- Name the reflecting surface as a visual role: mirror plane, glass overlay, water reflection, glossy material, metallic highlight, or secondary reflected layer.
- Lock the reflection plane coordinates, crop, angle, opacity, blur, distortion, color shift, and brightness relative to the real layer.
- State whether reflection content is reversed, offset, partial, cropped, shadowed, or low-legibility.
- Keep reflected faces, objects, text, and background fragments as fragments unless the source clearly shows a complete reflected object.
- If reflection and real subject align, preserve shared lines, eye lines, edges, contact points, and scale match.

## Optional negative contribution

Reject a complete duplicate subject when only a fragment exists; wrong mirror side; reflection becoming a separate physical object; removing glass glare; making reflection too sharp, bright, centered, complete, or readable; inventing missing reflected features; eliminating the reflective surface.

## Optional settings contribution

- Perceptual relationship locks: real layer and reflection layer remain distinct but aligned.
- Completion/seam continuity locks: reflected fragments stay cropped/blurred/partial.
- Lighting-to-volume fidelity locks: preserve glare, highlight streaks, reflection brightness, and surface sheen only as visible.


---

# Included module: `concept.screen-frame-within-frame`

# Concept: screen, poster, and frame-within-frame

## When to load

Load when a visible screen, poster, print, photograph, frame, UI preview, window, or picture plane contains important content, or when that plane completes/replaces another visible subject.

## Detection cues

- Rectangular plane with its own content and edges.
- Secondary face/object/scene inside a screen, poster, reflection, or frame.
- Contained content differs in medium, scale, sharpness, brightness, or perspective from the surrounding scene.
- The contained layer is partial or low-legibility.

## Prompt additions

- Separate canvas orientation from object orientation. For each major rectangle, state its long edge, short edge, corner order, and image-plane rotation.
- Lock the container's corner coordinates, border thickness, rotation, perspective skew, crop, and image-plane area.
- Describe contained content as contained content, not as an in-world object unless it visibly is one.
- State visible fragments inside the container and absent counterpart fragments.
- Preserve medium contrast: screen glow, print flatness, poster grain, frame border, glass glare, UI preview softness, or low-resolution contained image.
- If the screen/frame replaces hidden subject features, combine with `concept.occlusion-replacement` and state replacement logic explicitly.

## Optional negative contribution

Reject turning screen/poster content into a real physical subject; full second scene; complete body/object when only a fragment is visible; wrong rectangle rotation; flattening a diagonal screen upright; removing borders; adding full app chrome or clean product-screen UI when absent.

## Optional settings contribution

- Perceptual relationship locks: contained layer remains within the frame/screen/poster.
- Coordinate and anchor locks: container corners, border, rotation, and content crop.
- Coherence/realism ceiling locks: preserve mixed layer or screen-contained reading.


---

# Included module: `concept.scale-miniature`

# Concept: stylized miniatures in real environments

## When to load

Use only when visible evidence supports a small stylized physical figure, doll, figurine, plush, toy, collectible, or CG-like miniature placed inside a real photographed environment. Treat miniature-vs-real-world scale as a first-order concept lock, not a style detail.

## Detection cues

- Toy-scale subject near real hands, fingers, household objects, table edges, bedding, screens, or room elements.
- Molded, plush, synthetic, or stylized material visible under real-world lighting.
- Tight crop where the miniature's head/body is large in frame but real-world anchors reveal small scale.
- Casual phone-video compression or low-detail edges around a miniature object.

## Prompt additions

- Treat the scale relationship as a first-order concept lock.
- Treat a cropped or obscured appendage as endpoint-sensitive.
- Audit for polish-amplifying phrases.
- Lead with measured frame shape, casual capture fidelity, and miniature-vs-real-world scale relationship before attractive character design.
- If a real hand, finger, tool, household object, support surface, or foreground prop interacts with the miniature, lock the contact point, contact area, contact direction, touched endpoint, overlap, untouched regions, and whether anything is lifted or under tension.
- Distinguish passive contact from active manipulation. Avoid `pinch`, `hook`, `pull`, `grip`, `hold`, or `petting` unless visible.
- Contact correction must not widen the shot. Keep tight subject scale, edge cuts, foreground support height, incomplete body visibility, and awkward close-camera framing.
- Describe support geometry before gesture when a hand or prop rests on a cushion edge, blanket fold, table edge, ledge, step, ridge, or raised foreground boundary.
- Preserve the subject as a photographed or captured object when supported: synthetic material, molded surface, seam-like construction, toy scale, real room lighting, mixed-media insertion. Reject life-size human or polished product render drift.
- For low-resolution or casual phone-video captures, put compression softness, focus hierarchy, motion softness, low-detail edges, imperfect room lighting, and casual capture noise near the beginning and in critical locks.
- For small appendages, plush extensions, fuzzy tails, wires, antennae, ornaments, ribbons, straps, cords, tags, or endpoints, lock bounded footprint, path, width budget, endpoint, contact point, and low-detail scale before category nouns.

## Optional negative contribution

Reject life-size human, pure 2D illustration if the source is physical, polished product render, complete seated figure when cropped, full-body product view, zoomed-out scene, added floor, extra environmental breathing room, larger appendages, full loops/ropes/scarves replacing narrow endpoints, high-polish collectible sharpness when source is compressed.

## Optional settings contribution

- Scale/interaction anchor locks: miniature scale relative to hand/object/surface.
- Coherence/realism ceiling locks: captured toy-scale object in real environment; no life-size normalization.
- Focus and depth-of-field locks: phone/compression softness if present.


---

# Included module: `concept.mixed-media-illusion`

# Concept: mixed media, flat overlays, and illusion fidelity

## When to load

Load when the image combines different media or realism levels, such as a flat sticker on a photo, cel-shaded graphic over a real subject, printed insert, collage panel, stylized overlay, or composited element whose contrast is visually important.

## Detection cues

- Hard simplified contours, outline style, color blocks, or limited shading against a photographic subject.
- Inserted element has different resolution, lighting, perspective, grain, or material behavior.
- The source depends on the mismatch rather than seamless realism.

## Prompt additions

- Describe the element's visual role first: flat graphic overlay, sticker, decal, printed mark, cel-shaded insert, collage fragment, or stylized overlay.
- Lock simplified contour, outline weight, shape count, color-block treatment, limited shading, flatness, and exact overlap with the real subject.
- If related stems, labels, marks, leaves, symbols, or secondary shapes share the same graphic treatment, treat them as part of the same overlay family.
- Preserve the coherence ceiling: do not make the mixed-media element physically plausible, seamlessly 3D, or material-matched unless the source is visibly that way.

## Optional negative contribution

Reject conversion into realistic physical props, botanical objects, jewelry, polished 3D accessories, clean product graphics, seamless CG, or fully integrated realistic objects when the source depends on medium contrast.

## Optional settings contribution

- Coherence/realism ceiling locks: preserve medium mismatch and source-level implausibility.
- Style/rendering target: specify each medium layer separately when needed.


---

# Included module: `subject.human`

# Subject: human fidelity

## When to load

Load whenever a real or fictional person is visibly present. Add `detail.human-face-likeness` only when facial features are prominent or clearly readable.

## Human hierarchy

Record these before micro-detail:

- number of people and primary/secondary roles
- each person's frame share, crop, depth plane, and overlap order
- head position and scale relative to the frame and body
- body orientation, head turn, gaze direction, shoulder line, and visible action
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail in proportion to visibility. A primary close face can carry more description; a distant, blurred, reflected, screen-contained, or background person must remain simpler and lower-detail.

Define a face visibility budget before choosing a broad person-gestalt anchor or local face detail. Record which feature groups are fully visible, partly hidden, shadowed, soft, occluded, or actually cut by the frame. If only hair or the outer head mass is cropped, do not imply that eyes, nose, mouth, cheek, or chin are sliced.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

### Broad person-gestalt anchor

- Use at most one compact anchor for a primary, sufficiently readable person when a broad apparent racial, ethnic, or regional appearance category, or a calibrated attractiveness type, is visually supported and likely to stabilize generation. Omit it for small, blurred, heavily occluded, or genuinely ambiguous people.
- Treat any image-derived category as a generation-oriented visual approximation, not a factual identity claim. Do not infer nationality or exact ethnicity. Retain user-supplied identity context when requested, but never let it replace visible geometry.
- Prefer direct, generator-friendly wording for the fictional subject, then correct the category prior with face silhouette, proportions, feature relationships, skin tone and treatment, hair mass, expression, and lighting. Geometry wins when it conflicts with the broad anchor.
- When attractiveness is salient to the visible gestalt, calibrate its character rather than stacking intensity; for example, `conventionally attractive with a soft, approachable everyday appearance` or `striking and angular rather than polished`. Use one such phrase, not multiple beauty synonyms.
- Keep the attractive impression in the subject's visible facial harmony, expression, and grooming. Preserve asymmetry, ordinary traits, skin treatment, makeup level, capture softness, and crop instead of translating attractiveness into flawless skin, perfect symmetry, larger eyes, heavier makeup, beauty lighting, or a closer portrait.

After the optional gestalt anchor, prioritize the strongest source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Treat skin and makeup as rendering evidence: tone depth, undertone, matte or reflective finish, visible texture, freckles or marks, under-eye treatment, facial hair, cosmetic strength, and retouching level only when legible.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- Preserve shoulder span, torso length, waist and hip placement, limb thickness, stance, and clothing-shaped silhouette only to the degree visible.
- Keep the torso, pelvis, and center of mass in the source-visible spatial zone; do not let a contact pose silently relocate the person across a barrier, edge, opening, or support surface.
- Separate near-camera enlargement from anatomical size.
- Preserve a clearly visible large-scale body silhouette without exaggeration or reduction.
- Keep a moderate or obscured body silhouette secondary rather than promoting it.
- If age is unclear or the person is not clearly adult, use neutral, non-sexual silhouette and clothing language.
- Keep secondary or cropped body regions subordinate to a dominant face, action, prop, or relationship.
- Lock the person's frame share and environmental context before facial detail. Do not let a detailed face passage enlarge the subject or convert an environmental portrait into a close beauty portrait.

## Module handoff

- Add `detail.human-face-likeness` for a prominent or clearly readable face.
- Add `detail.pose-hands-gesture` when hand shape, grip, contact, limb mechanics, or pose landmarks matter.
- Add `detail.clothing-fashion` when garment boundaries, fit, seams, straps, or coverage affect the visible silhouette.
- Add `detail.tight-selfie-hierarchy` for a close phone selfie whose face/hair hierarchy and edge crop are first-order.
- Add `style.stylized-character-maturity` only for a stylized human-like subject with maturity drift risk.

## Prompt contribution

Place human description after the primary concept and composition. Preserve this order: subject scale and crop, head/body orientation, optional one-sentence person-gestalt anchor, face detail at the visible tier, hair-to-face occlusion, expression/gaze, pose/contact, clothing silhouette, then secondary texture.

For multiple people, describe each person separately by frame role and do not blend their face, hair, clothing, pose, or lighting anchors.

## Optional negative contribution

Reject unsupported identity claims or broad-anchor prototype drift, generic model-face drift, beauty retouching, changed apparent age presentation, different face silhouette, altered feature spacing, changed expression or gaze, hairline and hair-mass drift, invented hidden anatomy, mirrored pose, completed cropped regions, and lighting changes that alter visible facial or body structure. Keep exclusions proportional to what is readable.


---

# Included module: `medium.screenshot-ui`

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


---

# Included module: `medium.non-photographic-rendering`

# Medium: non-photographic rendering fidelity

## When to load

Load for illustration, painting, 3D rendering, anime/cel shading, vector art, sketches, concept art, pixel art, game-engine images, diagrams with stylized rendering, or mixed media with clear non-photographic layers.

## Prompt additions

Adapt fidelity rules to the visible medium:

- virtual camera, perspective, crop, depth layering, and composition
- stylized proportions and shape language
- edge quality: hard vector edges, soft painterly edges, sketch lines, inked contours, anti-aliasing, pixel edges
- linework: thickness, taper, pressure, wobble, clean/rough quality, hatch density
- brush texture, paint thickness, canvas/paper grain, wash, dry-brush, impasto, airbrush, marker, watercolor bleed
- value structure, shadow style, cel-shading steps, gradients, ambient occlusion, rim lines, highlights
- 3D material treatment: plastic, clay, metal, skin shader, subsurface, roughness, specular, depth of field, render noise, game-engine lighting
- composition and crop over style shorthand; do not use a famous artist or copyrighted character name

If the image mixes photographic and non-photographic layers, combine with `concept.mixed-media-illusion`.

## Optional negative contribution

Reject wrong medium: photo realism when source is illustration, cartoon/anime when source is realistic, 3D render when source is painting, vector clean-up when source is hand-drawn, painterly blur when source is crisp cel-shaded, excessive detail, famous-artist style drift, and polishing rough linework or texture.

## Optional settings contribution

- Style/rendering target:
- Film/camera/sensor or medium artifact locks:
- Coherence/realism ceiling locks when mixed media is present.


---

# Included module: `medium.photographic-capture`

# Medium: photographic capture, camera, focus, lighting

## When to load

Load for photographs, phone captures, snapshots, camera previews, scanned photos, and photorealistic images whose camera/focus/lighting behavior should be preserved.

## Prompt additions

Describe photographic capture:

- camera distance, height, angle, roll/rotation, lens impression, perspective distortion
- subject-to-camera relationship and how perspective affects face/body/object/background proportions
- close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, telephoto compression, low-angle elongation, high-angle compression only when visible
- focus target, focus accuracy, depth of field, bokeh, foreground/background blur, low-resolution softness, sharpening, compression, noise reduction, bloom, haze
- motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable capture
- camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look
- For casual phone, screenshot, social-video, or compressed outdoor captures, state the capture imperfection ceiling before beauty, fashion, scenic, studio, or product shorthand. Preserve handheld asymmetry, preview/compression softness, flattened distant layers, bloom, haze, clipped highlights, low-legibility marks, and ordinary non-editorial framing when visible.

Map sharpness separately across the primary subject, secondary details, foreground, and background.

Distinguish global low acutance, diffusion, haze, compression, or processing softness from depth-of-field blur. Use `shallow depth of field` or premium-looking bokeh only when a visibly sharper focus plane is separated from defocused layers. If the nominal focus subject is also soft, preserve that softness instead of sharpening it while blurring only the background.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Do not relight into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes visible structure.

## Optional negative contribution

Reject wrong camera distance/height/angle/lens perspective, wrong focus target/depth of field, background too sharp, soft photo becoming overly sharp, sharp photo becoming blurry, added/removed camera shake, wrong blur direction, wrong grain/sharpening/flash/color cast/dynamic range/highlight rolloff, polished studio quality when source is casual, and relighting that changes apparent proportions.

## Optional settings contribution

- Camera/film/rendering target:
- Lighting/rendering target:
- Lighting-to-volume fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:


---

# Included module: `subject.animal`

# Subject: animal fidelity

## When to load

Load when an animal, pet, wildlife subject, or animal-like creature is visually important.

## Detection cues

Species or type may be clear, ambiguous, stylized, cropped, or partially hidden. Use broad visual description if exact species/breed is uncertain.

## Prompt additions

Describe only visible animal evidence:

- species/type or broad animal class when clear; otherwise `small animal`, `large animal`, `bird-like`, `dog-like`, `cat-like`, etc.
- head shape, muzzle/beak/snout, ear shape, eye placement, whiskers, horns/antlers, tail, paws/hooves/claws/fins/wings if visible
- fur/feather/scale/skin texture, length, pattern, matting, wetness, sheen, color distribution
- body posture, weight distribution, gait, curled/sitting/standing/flying/swimming mechanics
- gaze, mouth position, tongue/teeth visibility, expression-like cues without assigning human intent
- scale relative to hands, furniture, environment, other animals, or frame
- crop and hidden limbs/tail/wings

For pets, preserve candid capture and ordinary body shape. Do not make the animal cuter, cleaner, fluffier, more symmetrical, more puppy/kitten-like, more studio-lit, or more breed-standard than the source.

## Optional negative contribution

Reject wrong species/breed-like drift, extra limbs/wings/tails, humanized expression, over-cute pet photography, cleaned fur, over-sharp eyes, changed coat pattern, full body when cropped, missing visible tail/ears/paws, and background/scale changes that alter animal size.

## Optional settings contribution

- Category-specific locks: animal type, texture, posture, crop, scale, and visible markings.


---

# Included module: `subject.food`

# Subject: food and drink fidelity

## When to load

Load when food, drink, cooking, plating, or table setting is visually important.

## Prompt additions

- Identify food/drink visually and conservatively. Use `appears to be` for ambiguous dishes.
- Lock plating/container geometry: plate/bowl/glass/cup shape, rim, fill level, crop, angle, position, and scale.
- Describe food texture and structure: sauce pooling, crumbs, seeds, char, steam, condensation, bubbles, foam, melted areas, layers, glaze, oil sheen, moisture, burnt/dry/soft/crisp cues.
- Preserve color temperature and appetite level. Do not make food fresher, cleaner, glossier, more symmetrical, more abundant, or more professionally styled unless visible.
- Describe utensils, napkins, hands, table surface, background clutter, and shadows as secondary if secondary.
- For labels/menus/packaging, combine with `detail.text-logo-label`.

## Optional negative contribution

Reject professional food-styling upgrade, extra garnish, extra steam, cleaner plate, fuller portion, changed dish type, added utensils, perfect symmetry, fake glossy sauce, crisp text/menus when not visible, and commercial studio lighting if source is casual.

## Optional settings contribution

- Category-specific locks: dish/container geometry, texture, portion size, table context, lighting, and fidelity ceiling.


---

# Included module: `subject.product`

# Subject: product and object fidelity

## When to load

Load when a product, package, tool, container, collectible, appliance, object arrangement, or foreground prop is a main subject or important anchor.

## Prompt additions

- State whether the object is the hero subject, co-dominant, secondary anchor, or incidental prop.
- Lock bounding box, rotation, perspective skew, top/bottom/side edges, visible face planes, crop, scale relative to hands/body/table/frame, and overlap.
- Describe geometry before brand/category: rectangular box, cylinder, soft pouch, transparent bottle, curved device, rigid package, folded fabric object, glossy prop, etc.
- Describe materials and surface behavior: matte/glossy, transparent, translucent, metallic, plastic, paper, cardboard, fabric, ceramic, glass, liquid, worn, scratched, wrinkled, compressed, low-res.
- For labels or packaging text, combine with `detail.text-logo-label`. Treat text as low-legibility graphic marks unless exact text is central and clearly readable.
- If decorative small details exist, keep them subordinate to object size. Do not let detail count turn a prop into a product hero.
- Preserve ordinary, candid, cluttered, awkward, cropped, or low-quality product evidence. Do not turn it into clean commercial product photography unless visible.

## Optional negative contribution

Reject product-shot normalization, centered clean hero object, enlarged secondary prop, invented brand labels, crisp unreadable marks, more premium materials, different package shape, wrong rotation/perspective, completed cropped object, duplicated products, removed hand/object overlap, and studio lighting when source is casual.

## Optional settings contribution

- Category-specific locks: product/object geometry, material, scale, crop, and label legibility.
- Coordinate and anchor locks: object bounding box and edge placement.


---

# Included module: `subject.architecture-interior`

# Subject: architecture, street structure, and interiors

## When to load

Load when buildings, interiors, rooms, corridors, streetscapes, furniture layout, or structural perspective are important.

## Prompt additions

- Describe space by zones: foreground, midground, background, left, right, top, bottom.
- Lock horizon, vanishing direction, wall/floor/ceiling planes, doorway/window positions, vertical lines, arches, stairs, railings, columns, furniture seams, countertops, table edges, shelves, and floor/wall transitions.
- Treat a salient edge, barrier, wall, opening, counter, platform, seat, or ledge as a spatial boundary or support surface when it organizes an interaction. State which visible region it separates, which side contains each major subject, and whether contact is load-bearing, stabilizing, or merely overlapping in the image.
- State camera height, tilt, roll, and perspective distortion. Preserve vertical convergence or skew when visible.
- Describe materials: concrete, brick, tile, wood, plaster, glass, metal, fabric, stone, painted surface, worn/clean/reflective/matte.
- Preserve clutter, partial objects, edge cuts, occlusion, and imperfect room lighting. Do not turn an ordinary room or street into a clean architectural visualization.
- For signs/posters/labels, combine with `detail.text-logo-label`.

## Optional negative contribution

Reject straightened perspective if source is tilted, clean interior render, added windows/doors/furniture, removed clutter, wrong room type, sharper background than source, postcard-like architecture, perfect symmetry, extra people, and completed cropped structural elements.

## Optional settings contribution

- Category-specific locks: structural planes, perspective, material, room/street zoning, and architectural crop.


---

# Included module: `subject.document-data-diagram`

# Subject: documents, data, diagrams, maps, and layouts

## When to load

Load when the source contains a document, poster, graph, chart, table, map, technical diagram, scientific/medical visualization, infographic, or layout where geometry and text/data placement matter.

## Prompt additions

- Decide whether the document/data/diagram is the main subject, secondary layer, screen-contained content, or background fragment.
- Lock page/screen/poster aspect, rotation, perspective, margins, grid, panels, title area, axes, legends, callouts, arrows, tables, rows/columns, icons, blocks, labels, and whitespace.
- Preserve exact readable text only when clear and central. For small or ambiguous text, describe it as low-legibility marks with approximate placement, length, density, and contrast.
- For charts, describe chart type, axis placement, line/bar/point density, legend position, color grouping only if visible, and whether values are readable.
- For maps, describe land/water blocks, roads/paths, boundary lines, labels, markers, north/legend if visible, and scale of detail.
- For technical/scientific diagrams, preserve visual structure: nodes, arrows, layers, anatomy/parts only as visible, schematic vs realistic rendering, annotation density.
- Do not invent data, legible numbers, axis labels, or precise scientific meaning that is not visible.

## Optional negative contribution

Reject crisp invented text, random letters, fake labels, altered chart type, invented data values, extra legends, completed tables, wrong panel layout, centered clean poster redesign, infographic beautification, and document flattening when source has perspective/crop.

## Optional settings contribution

- UI/text/label locks when relevant: legibility ceiling, layout, grid, panels, axes, labels, and data mark density.
- Category-specific locks: document/diagram layout and perspective.


---

# Included module: `subject.landscape-nature`

# Subject: landscape and natural environment

## When to load

Load when the image is primarily or substantially about an outdoor natural environment.

## Prompt additions

- Lock horizon height, terrain bands, sky area, waterline, mountain/forest/building silhouettes, foreground texture, midground layers, and background haze.
- Describe weather and atmosphere only as visible: clouds, fog, rain, snow, mist, dust, smoke, humidity, harsh sun, overcast light, sunset/sunrise color, night darkness.
- Describe natural textures: foliage density, grass length, rock surfaces, sand, mud, water ripple, wave foam, snow crust, cloud edge softness.
- Preserve low-legibility distant features as massing, not detailed postcard scenery.
- State absent object classes when generators might add them: no people, no boats, no buildings, no birds, no signs, if absent and relevant.
- Preserve ordinary or degraded capture. Do not beautify into a travel-poster, HDR landscape, dramatic cinematic sky, or saturated postcard unless source is visibly that way.

## Optional negative contribution

Reject altered horizon, added sun/moon/rainbows, extra people/animals/boats/buildings, over-detailed distant objects, HDR postcard lighting, wrong weather/time of day, sharpened haze, changed terrain band proportions, and cleaned-up composition.

## Optional settings contribution

- Category-specific locks: horizon, terrain layers, atmosphere, weather, natural textures, and fidelity ceiling.


---

# Included module: `subject.vehicle`

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


---

# Included module: `subject.generic-object`

# Subject: generic object or ordinary scene fallback

## When to load

Load when no specific subject module fits, but the router still needs a subject decision for an ordinary object, partial prop, abstract surface, empty scene, or visually simple arrangement.

## Rules

- When no specific subject module fits, preserve the main visible object or ordinary scene as a generic object/scene without inventing a category.
- Describe image-plane role, position, scale, crop, material, color, occlusion, edge contact, and visibility level before naming a broad object category.
- If the subject is absent, abstract, mostly background, or only a partial edge element, say so and avoid promoting it into a central object.
- Do not add a person, product, animal, vehicle, document, architecture, landscape, food, or brand category just to make the prompt sound complete.

## Prompt additions

Use direct visible descriptions such as `ordinary partial object`, `simple cropped surface`, `abstract/ambiguous foreground shape`, or `mostly empty scene` when that is more faithful than a category label.

## Optional negative contribution

Reject invented categories, added subjects, object completion, product-shot conversion, and subject centralization that is not visible.

## Optional settings contribution

- Generic subject fallback locks:


---

# Included module: `medium.unspecified-visual`

# Medium: unspecified visual fallback

## When to load

Load only when no specific medium module clearly applies, or when the medium is visually ambiguous enough that forcing `photographic`, `screenshot`, or `rendered` would be less faithful than staying neutral.

## Rules

- When no specific medium is clear, preserve only visible medium evidence without forcing a photographic or rendered style.
- Name the observable surface qualities instead of inventing a medium: flat/volumetric appearance, edge softness, pixelation, noise, compression, linework, screen glow, paper texture, blur, lighting behavior, or material shading when visible.
- Do not default to `photorealistic`, `photo`, `digital art`, `anime`, `3D render`, `cinematic`, or `studio` unless the source visibly supports that medium.

## Prompt additions

Use neutral wording such as `source-faithful visual medium`, `medium remains ambiguous`, or direct visible texture/capture cues.

## Optional negative contribution

Reject forced photo realism, forced illustration, forced 3D rendering, forced app UI, or a cleaner medium category than the source supports.

## Optional settings contribution

- Medium fallback locks:


---

# Included module: `detail.human-face-likeness`

# Detail: human face likeness

## When to load

Load only when at least one human face is prominent or clearly readable. Do not load merely because a person exists.

## Detail tier

Allocate human detail by visible face scale and legibility.

- **Prominent and legible:** the face is a primary image anchor and individual feature relationships are separable. Use six to ten selective likeness anchors.
- **Readable but secondary:** the face is smaller but several feature groups remain reliable. Use three to six anchors.
- **Small or indistinct:** do not use this module. Preserve head orientation, hair mass, skin-tone massing, and visibility only through `subject.human`.

For a prominent legible face, choose six to ten likeness-bearing visible anchors instead of listing every facial field.

Use the lower end of the anchor range when global softness, haze, compression, low microcontrast, or small face scale limits feature separation. Face-detail anchors preserve geometry; they do not authorize a larger crop, stronger focus, added skin texture, cleaner makeup, brighter catchlights, or sharper hair than the source aesthetic supports.

An anchor must describe a distinctive visible relationship, not a generic adjective. `Narrow lower face with a short rounded chin` is useful; `beautiful detailed face` is not.

## Coarse-to-fine likeness

When `subject.human` selects a broad person-gestalt anchor, treat it as one high-level generation prior rather than as the likeness description itself.

- Place it once before local face geometry; do not repeat the racial, ethnic, regional-appearance, or attractiveness category in later clauses.
- Use the full scale-appropriate geometry budget to correct the category prototype with the source's face silhouette, feature relationships, expression, hair boundary, surface treatment, and visible asymmetry.
- If the broad anchor conflicts with reliable local geometry, revise or omit the broad anchor. Geometry wins.
- Keep attractiveness at the level of overall facial reading; do not let it enlarge the face, idealize proportions, clean the skin, strengthen makeup, sharpen focus, or upgrade lighting.

## Likeness anchor selection

Select only the strongest supported anchors across these groups:

1. **Head and face silhouette:** head width-to-height, forehead height, cheek fullness, cheekbone width, jaw taper or squareness, chin length/shape, visible asymmetry.
2. **Eyes and brows:** eye size relative to the face, spacing, tilt, lid exposure, fold visibility, far-eye reduction in three-quarter/profile view, brow thickness/shape/distance, catchlight pattern, gaze direction.
3. **Midface and nose:** bridge height/width, nose length, frontal or profile projection, tip shape, nostril visibility, relationship to cheek and upper lip.
4. **Mouth, jaw, and expression:** mouth width, lip line/fullness, corners, teeth visibility, closure/parting, chin tension, cheek lift, brow tension, squint, smile asymmetry, neutral or strained expression.
5. **Hair and face boundary:** hairline, part, fringe shape, temple coverage, side masses, curl/wave group, volume, flyaways, shadow color, and exact facial regions hidden by hair.
6. **Skin, makeup, and surface treatment:** tone depth and undertone, matte/reflective balance, visible texture, freckles or marks, under-eye treatment, facial hair, makeup placement and strength, capture smoothing or retouching.
7. **Facial lighting:** which planes receive highlight or shadow, how light changes the readable eye/nose/mouth/jaw geometry, and whether features remain soft, flat, hazy, or contrasty.

Preserve expression, gaze, and hair-to-face occlusion as likeness-critical geometry.

Distinguish optical or processing softness from beauty retouching. A globally soft face should remain optically soft rather than becoming a crisp face with smoothed skin.

Use relational wording: wider than, closer together, higher than, partly hidden by, aligned with, shorter relative to, or more visible on the viewer-left/right. Do not infer unobserved feature geometry.

## Partial, angled, and multiple faces

- For three-quarter or profile views, state near-side/far-side feature visibility and perspective compression instead of describing an imagined frontal face.
- For edge-cropped or occluded faces, list visible and hidden feature groups before fine detail. Do not complete the missing side.
- For a reflected, screen-contained, printed, or background face, keep its detail ceiling tied to that layer.
- For multiple readable faces, allocate the largest anchor budget to the primary face and a smaller distinct set to each secondary face. Never merge anchors between people.
- For stylized faces, preserve the source's shape language, line/render treatment, and feature scale; add the maturity module only when needed.

## Prompt contribution

Create one compact human-likeness passage after composition:

1. optional one-sentence person-gestalt anchor
2. face scale, angle, crop, and visible side
3. the selected likeness anchors in source hierarchy
4. expression and gaze
5. hair silhouette and occlusion
6. skin/makeup/rendering and facial lighting when legible

Repeat at most one or two highest-risk anchors in the final constraint block. Do not copy the full passage into negative prompt or settings.

## Optional negative contribution

Reject a generic symmetrical model face, changed face silhouette, wrong eye/brow spacing or tilt, wrong nose/mouth/jaw relationship, changed expression or gaze, cleaned-up asymmetry, hairline/fringe/occlusion drift, invented hidden features, different skin or makeup treatment, and relighting that changes readable facial geometry. Include only the failures supported by the selected anchors.


---

# Included module: `detail.clothing-fashion`

# Detail: clothing, fashion, accessories, and coverage maps

## When to load

Load when clothing placement, garment edges, neckline, straps, accessories, exposed/covered bands, fabric tension, or fashion labels affect fidelity.

## Prompt additions

Describe visible garment geometry before broad category labels:

Prefer visible garment geometry over broad fashion-category labels.
Treat visible band-height drift as a composition failure.

- fit, fabric type/thickness, opacity/transparency, stiffness/looseness
- fabric tension, wrinkles, folds, material sheen, pattern scale
- neckline depth/width, collar, shirt opening, sleeve opening, strap position
- seams, waist seam, under-bust seam if visible, buttons, lace, closures, hems
- garment layers and how they interact with body shape, pose, props, hair, hands, shadow, and crop

Create a coverage map when clothing placement matters:

- which image regions are skin
- which regions are fabric
- which regions are shadow-hidden
- which regions are cropped away
- which garment edges are interrupted, softened, shadowed, blurred, or blocked

Treat close upper-torso edges as measured boundary bands, not fashion labels. Lock neckline/garment-edge width, lowest y-position, visible skin/underlayer area above and below it, sleeve/shoulder fabric area, and bottom crop.

Avoid broad labels such as `off-shoulder`, `low neckline`, `camisole`, `dress`, `lingerie`, `corset`, `crop top`, or `fashion portrait` if they would deepen, widen, clarify, center, tighten, reveal, or glamorize the garment beyond the source.

For bottom-edge or side-edge clothing/body crops, distinguish a narrow visible band from a completed outfit or body region. If the source only shows a hem, waistband, partial pocket, side edge, lower garment strip, or crop-boundary gap, describe it as a bounded edge band with height/area and nearby anchors. Avoid wording that invites centered body construction, full pockets, completed legs, or a wider exposed/covered band than the source.

For accessories such as chokers, collars, necklaces, straps, lace trim, bows, patches, pins, bags, or jewelry, describe only visible silhouette, density, low-legibility, shadow, and occlusion. Do not upgrade them into crisp ornate symmetrical fashion accessories unless visible.

For straps, bags, chains, handles, and edge-adjacent accessories, lock footprint and crop before material detail. If the accessory is secondary or partly outside the frame, keep it partial, low-detail, and edge-bound in affirmative prompt language rather than relying only on the negative prompt.

For close portraits or tight human crops where clothing is secondary below the face, create a secondary garment completion budget before using broad fashion labels:

- visible garment bands and approximate frame ranges
- whether collar, neckline, tie, ribbon, scarf, vest, jacket, sleeve, trim, button, patch, strap, or accessory is complete, partial, folded, cropped, occluded, or low-legibility
- which garment parts are interrupted by chin, hair, hand, prop, shadow, blur, or bottom crop
- whether symmetry, openings, knots, edges, seams, and trim should remain compressed or unclear instead of becoming clean outfit construction
- how much lower torso is visible before the prompt would turn a close portrait into a fashion, costume, or uniform study

Do not let secondary formal, uniform-like, costume-like, layered, or accessory-heavy clothing become a clean centered outfit view when the source uses it only as cropped lower-frame or side-frame bands. Use clothing category labels only after locking incomplete garment geometry, and keep the clothing secondary when the face, hand, prop, or crop is the real visual anchor.

## Optional negative contribution

Reject wrong neckline depth/width, strap position, sleeve position, seam placement, hem shift, deeper openings, larger exposed skin bands, tighter/looser fabric, more structured/corseted/lingerie-like garment, more revealing or more modest clothing, completed hidden garment regions, cleaner fashion-editorial styling, and accessory enlargement or sharpening. For secondary clothing in close portraits, reject complete centered outfit views, overly symmetrical collars/necklines, clarified knots/openings/trim/buttons/patches, and lower torso expansion when the source clothing is cropped, compressed, occluded, or low-detail.

## Optional settings contribution

- Clothing-fit, neckline, and seam locks:
- Body-proportion calibration locks:
- Boundary and visibility-budget locks:


---

# Included module: `detail.pose-hands-gesture`

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


---

# Included module: `detail.tight-selfie-hierarchy`

# Detail: tight selfie hierarchy

## When to load

Load when a close human phone selfie is dominated by the face, hair, headwear, or upper-head crop, and generation is likely to normalize it into a balanced portrait, fashion image, outfit study, or cleaner head-and-shoulders shot.

## Prompt additions

When tight selfie framing makes the face and hair the primary anchors, state that hierarchy before describing clothing, accessories, or broad fashion labels.

- Lead with image-plane priority: face and hair first; hand, accessories, shoulders, and lower-frame clothing second.
- Preserve phone-selfie crop pressure, asymmetry, edge cuts, and high-face or close-face placement before aesthetic labels such as portrait, cosplay, fashion, beauty, editorial, or character reference.
- If the face is phone-smoothed, sun-washed, filtered, doll-like, overexposed, low-contrast, or otherwise capture-treated, state that as a fidelity lock rather than improving it into natural skin or studio beauty lighting.
- If bangs, fringe, hair, hat, hood, veil, or headwear cover the forehead, brows, eyelids, cheek, jaw, or frame edge, describe coverage and occlusion before strand or accessory texture. Reject exposed or completed hidden face regions when the source hides them.
- For wigs, dyed hair, bright hair, or strongly lit hair, separate local hair color from shadow color. Lock highlight masses and shadow masses so the generator does not average the hair into a cleaner single color.
- If a generated comparison drifts into a more natural selfie, centered portrait, or clearer outfit study, strengthen these generic hierarchy and crop locks instead of adding source-only trivia.

## Optional negative contribution

Reject balanced head-and-shoulders portrait drift, fashion-editorial recentering, cleaned-up studio portrait lighting, reduced face/hair dominance, exposed hidden forehead or brows, completed hidden crop edges, and any prompt wording that lets secondary clothing or accessories overtake the face/hair hierarchy.

## Optional settings contribution

- Primary visual concept locks: face and hair remain the first-order anchors; secondary objects stay source-sized.
- Boundary and visibility-budget locks: preserve tight selfie edge cuts, high-face crop, side crops, and incomplete lower-frame regions.
- Coherence/realism ceiling locks: keep the source phone-selfie capture treatment instead of upgrading into a polished portrait.


---

# Included module: `detail.accessory-torso-budget`

# Detail: accessory and torso budgets

## When to load

Load when a tight human crop includes headpieces, bows, clips, chokers, necklaces, straps, lace, ruffles, garment trim, cropped shoulders, or upper-torso clothing that must remain secondary to the primary face, hand, prop, or crop concept.

## Prompt additions

Treat accessories and cropped torso regions as measured support budgets, not as invitations to complete a costume, outfit, glamour pose, or body-centered portrait.

- Define each accessory footprint once: approximate frame location, scale relative to face/head, crop, occlusion, contrast, and legibility. Then keep it secondary unless it visibly dominates.
- Avoid multiplying accessory adjectives after footprint is established. Extra detail on lace, jewelry, bows, nails, plaid, straps, or trim can enlarge or sharpen them.
- For close portraits, prioritize face scale, eye line, chin line, hair edges, and crop boundaries over costume labels and accessory material.
- For upper torso that is visible but secondary, prefer `cropped skin plane`, `covered torso plane`, `interrupted neckline`, `hair-overlapped torso edge`, `secondary shoulder edge`, `lower-frame garment band`, or `cropped garment edge band` when supported by the source.
- Lock lower garment, collar, neckline, ruffle, strap, or trim bands by y-start, height, width, interruption, and crop. If the source shows only a bottom or side band, keep it as a band and do not complete it into a bodice, dress, uniform, corset, or full outfit view.
- Preserve side-specific asymmetry for shoulders, straps, hair occlusion, accessory position, and edge cuts instead of normalizing into a symmetrical fashion portrait.

## Optional negative contribution

Reject accessory enlargement, crisp ornate accessory upgrading, centered outfit views, complete costume construction, lower torso expansion, clarified hidden neckline, widened or deepened garment openings, cleaner symmetrical straps/collars, and clothing/body regions promoted beyond their visible source budget.

## Optional settings contribution

- Clothing-fit, neckline, and seam locks: describe incomplete bands, cropped trims, interrupted necklines, and occluding hair/hand/props before category labels.
- Boundary and visibility-budget locks: accessories and torso regions remain source-sized, cropped, interrupted, and secondary.
- Body-proportion calibration locks: visible torso information remains limited to source-visible image-plane regions without hidden anatomy inference.


---

# Included module: `detail.face-hand-gesture`

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

## Optional negative contribution

Reject full hand poses, peace signs, manicure-centered foregrounds, uncropped wrists, recentered hands, enlarged fingers, moved hands that reveal hidden cheek/jaw/neck areas, extra fingers, missing fingers, and hand gestures that no longer contact or frame the face as in the source.

## Optional settings contribution

- Pose fidelity locks: preserve hand-to-face contact geometry, side, crop, and partial visibility.
- Occlusion fidelity locks: keep face, sleeve, glove, hair, and crop boundaries as the hand's limiting anchors.
- Focus and detail locks: hand/nail detail remains no sharper or more dominant than source visibility supports.


---

# Included module: `detail.low-quality-artifacts`

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


---

# Included module: `detail.text-logo-label`

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


---

# Included module: `style.stylized-character-maturity`

# Style: perceived character maturity for stylized miniatures

## When to load

Use only for stylized miniatures, anime figurines, doll-like characters, plush characters, toy-like humanoids, or CG-like inserted figures where apparent character maturity is visually relevant. This is not a real-person age-identification rule.

## Rules

- Do not let cute or doll-like cues automatically collapse an adult-looking stylized subject into a childlike one.
- Treat apparent face maturity as a separate fidelity dimension from body, clothing, safety, attractiveness, or style.
- Do not let `cute`, `doll-like`, `toy-scale`, `large eyes`, `small mouth`, or `youthful` automatically collapse the face into infantile, childlike, chibi, toddler-like, baby-faced, or much younger proportions unless visible.
- Preserve maturity through face/head construction only: face length relative to head height, cheek volume, chin point/softness, eyelid heaviness, eye-to-face scale, mouth size, nose evidence, neck length, shoulder/head relationship, and expression restraint.
- Do not preserve maturity by emphasizing torso, chest, hips, waist, exposed skin, lingerie, cleavage, adult anatomy, glamour pose, or sexualized body traits.
- If large stylized eyes are present without a childlike face, say so: `large anime eyes without chibi proportions`, `small mouth without toddler-like roundness`, `soft cheeks but not baby cheeks`, `compact toy body but not a child body`.
- Use the weakest lock that prevents childlike drift. Avoid repeated maturity language that may age up, glamorize, or product-polish the subject.
- Repeat source crop and head scale after maturity language because maturity wording can cause zoom-out or normalized portrait drift.

## Optional negative contribution

Reject childlike face, baby-faced proportions, chibi head-to-body ratio, toddler cheeks, younger-looking doll, overly juvenile expression, and also reject opposite drift such as adult glamour model face, mature fashion-model styling, somber adult stare, or sexualized adult styling when not present.

## Optional settings contribution

- Face fidelity locks: preserve source-supported stylized face maturity without younger childlike simplification or older glamour upgrading.
- Aesthetic and non-identifying appearance locks: mature-cute/stylized balance if visible.


---

# Optional model adapter reference

Apply only the section for the named downstream generator.

# Model adapters

Read only the adapter for the named downstream generator. If no generator is named, keep settings generator-agnostic and do not invent unsupported controls.

## GPT Image 2

Official references:

- https://developers.openai.com/api/docs/guides/image-generation#customize-image-output
- https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals

### Prompt

- Use a skimmable order: scene/background, subject, key details, constraints.
- Use short labeled segments or line breaks for complex prompts.
- Describe framing, viewpoint, placement, interaction, medium, lighting, and only the quality cues that matter.
- Treat detailed camera specifications as high-level visual cues, not exact physical simulation.
- Put essential exclusions and invariants in the main prompt. The official Image API output controls do not document a separate negative-prompt field.

### Settings

Use only documented controls that are relevant:

- `model: gpt-image-2`
- `size: auto` or a valid custom size
- `quality: low | medium | high | auto`
- `output_format: png | jpeg | webp`
- `output_compression: 0-100` for JPEG or WebP
- `background: auto | opaque`

Do not request a transparent background for GPT Image 2.

### Custom-size constraints

A custom size is valid only when:

- both edges are multiples of 16 pixels
- the maximum edge is at most 3840 pixels
- long-edge to short-edge ratio is at most 3:1
- total pixels are between 655,360 and 8,294,400 inclusive

Keep `Source frame` and `Target size` separate. When source dimensions are invalid, run:

```bash
python3 tools/size_adapter.py WIDTH HEIGHT
```

Use its target size or choose `auto`. State that the target is a ratio-preserving adapter size, not the source file dimensions.

## Other generators

- Emit `NEGATIVE PROMPT:` only when the downstream tool exposes a separate negative-prompt input or the user explicitly requests a reusable negative list.
- Use natural-language zones by default. Emit numeric coordinates only if the tool has a compatible layout/control surface or the concept depends on a small number of boundaries.
- Do not name sampler, scheduler, guidance, seed, steps, or control inputs unless the named tool actually supports them.
