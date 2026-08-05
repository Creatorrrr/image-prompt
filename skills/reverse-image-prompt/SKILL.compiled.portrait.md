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
