---
name: reverse-image-prompt
description: Reverse engineer a standalone English text-to-image prompt from a provided image using visible evidence, routed subject/medium/relationship modules, and an adaptive model-aware output contract. Use for faithful reconstruction, semantic prompt extraction, polished-but-composition-faithful variants, diagnostic image analysis, negative prompts, or generation settings.
---

# Reverse Image Prompt

## Purpose

Turn one provided image into a standalone text-to-image prompt that preserves its primary perceptual proposition: the visible concept or appeal that makes the image itself rather than merely a collection of matching objects. Preserve the source-specific composition, form, surface, light, hierarchy, crop, subject, pose, major-component relationships, color, medium, and meaningful artifacts that causally create that proposition.

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

3. Analyze silently with an adaptive hierarchy:
   1. State the primary perceptual proposition and, in diagnostic mode, the source-supported appeal directly rather than euphemistically.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Separate two to four aesthetic or structural invariants from dimensions that may vary without losing the proposition. Record the smallest causal cue set rather than every visible field.
   4. Lock frame ratio, crop, subject scale, major zones, boundary sides, and edge interactions.
   5. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze visible subjects and their image-plane roles. Use a compact broad person-gestalt anchor only when it materially reduces ambiguity; decompose salient human form or appearance into visible causes.
   7. Add only materially important pose, camera/perspective, focus, lighting, background, medium, texture, artifact, UI, and text evidence.

   Use this sparse internal map; leave irrelevant fields empty rather than completing a checklist:

```yaml
dominant_fidelity:
  mode: relationship-led | appearance-led | information-led | mixed
  perceptual_proposition: ""
  invariants: []
  flexible_dimensions: []
  causal_cues: []       # only material form, surface, light, color, hierarchy, topology, or information cues
```

4. Build and resolve this internal facet map:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face-detail, body-form, body-proportion, muscle-definition, body-tension, skin-surface, body-region-hierarchy, clothing, hands, text-logo, ui, small-props, cropped-edges, tight-selfie, face-hand-gesture, accessory-torso-budget
  style: []           # stylized-character-maturity or another narrow risk
```

5. Merge selected rules using this priority:
   1. Visible-evidence and safety limits.
   2. Primary perceptual proposition, dominant fidelity axis, and invariants.
   3. The mode-leading evidence: topology for relationship-led, causal appearance signature for appearance-led, information hierarchy for information-led, or the named co-primary pair for mixed.
   4. Frame ratio, crop, major zones, boundary sides, visibility, and completion budgets.
   5. Subject, medium, camera, lighting, focus, artifact, background, and color fidelity that supports the proposition.
   6. Flexible pose or placement detail, secondary elements, and generic shorthand.

6. Draft the smallest prompt that carries every invariant and concept-critical constraint. Let its order follow the dominant fidelity axis. If the source look is high-salience, place one compact Aesthetic Causal Signature near the beginning; if neutral, use only one or two ordinary cues. Translate broad appeal words into form, surface, light, color, hierarchy, or spatial mechanisms. Give each major component one relation and each inversion-prone interaction one relation clause, but do not let flexible pose coordinates or secondary details outrank the primary proposition.

7. Apply the pre-emit gate and report prompt-only limits honestly.

## Routing rules

- Always load Tier 0.
- Select at least one subject and one medium; use the generic/unspecified fallbacks only when evidence is unclear.
- Load every visible Tier 1 relationship module, including both photographic and non-photographic medium modules for genuine mixed media.
- Load Tier 3 and Tier 4 modules only for visible, material risks.
- For a prominent or clearly readable human face, add `face-detail`; for a small, blurred, shadowed, or heavily occluded face, keep only scale-appropriate human evidence and do not invent micro-features.
- Add a human body-form risk only when visible proportion, contour/tissue, muscle definition, skin surface, tension, or body-region hierarchy is first-order. Do not route it merely because a person or torso is visible.
- Treat the spatial topology of major components as Tier 0 evidence, but let the dominant fidelity axis determine its prompt weight. Do not force ordinary topology to outrank appearance or information invariants.
- Treat adaptive aesthetic analysis as Tier 0 evidence, not as a style preset. Do not load extra style modules merely to fill an aesthetic checklist.
- Keep the normal route within 3-8 non-core modules. Refine an over-budget facet map instead of loading every plausible module.
- Treat `ordinary`, `cropped-edges`, and `small-props` as core-handled observations unless another visible risk requires a dedicated module.
- Do not use broad labels such as `cinematic`, `studio`, `luxury`, `beauty shot`, or `high quality` when they would normalize source-specific evidence.

## Output selection

Always write the production prompt in English. Match the response language for diagnostic explanation unless the user asks otherwise.

- Always emit `PROMPT:` for generation requests.
- Emit `NEGATIVE PROMPT:` only when the user requests it or the named downstream generator supports a separate negative prompt.
- Emit `RECOMMENDED SETTINGS:` only when requested, when a target generator is known, or when source dimensions require a model-specific target-size explanation.
- For `diagnostic` mode, first name the visible core appeal or perceptual proposition directly, then explain the causal form, surface, lighting, color, hierarchy, spatial, and capture evidence. Distinguish invariants from pose or placement differences that would not destroy the aesthetic. Include a candidate prompt only if useful.
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

# Concept: primary perceptual proposition and relationship

## When to load

Always. Apply spatial analysis more deeply to occlusion, replacement, reflection, frame-within-frame, miniature scale, mixed media, collage, and other relationship-led images. Do not assume every image is relationship-led.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed` before deciding prompt order.

- `relationship-led`: topology or interaction carries the image.
- `appearance-led`: form, surface, light, color, or visible gestalt carries it despite modest pose variation.
- `information-led`: layout, legibility, sequence, or data hierarchy carries it.
- `mixed`: two named axes are genuinely co-primary.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. The visible elements, hierarchy, and primary perceptual proposition: what makes the image itself or compelling, beyond object inventory.
2. The dominant fidelity axis and smallest causal cue set.
3. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it.
4. For relationship-led or mixed images, the stable zones and each critical pair's side, containment, contact, support, depth, occlusion, and boundary crossing.
5. One to three likely failures, including a category default replacing source-specific evidence.

Build a sparse relation graph, grouping repeated elements that share a relation. For ordinary images, keep an ordinary premise. In appearance-led images, preserve spatial facts without letting minor pose coordinates outrank form, surface, light, color, or hierarchy. In information-led images, prioritize layout and legibility.

Distinguish image-plane overlap from scene-space containment, contact, and support. A bare verb such as `holding`, `leaning`, or `sitting` is insufficient when the geometry could plausibly invert. Record contact, visible weight support, and relation to the boundary or support plane. Use object- or scene-relative zones when screen directions are ambiguous.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record join, overlap, contact, containment, hidden or partial regions, boundary side, support, layer order, scale, and coherence ceiling.

## Prompt contribution

Write a construction recipe, not a prop list. Lead with the dominant axis and invariants; spend more words on topology only when it is first-order.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Normally one to three interaction sentences suffice. Avoid redundant coordinates.

## Optional negative contribution

When supported, reject only likely drift: broken seams, wrong boundary side, inverted containment or support, wrong layer order, completed hidden regions, normalized appearance, or a primary invariant demoted to generic detail.


---

# Included module: `core.fidelity-discipline`

# Core: fidelity discipline and anti-normalization

## When to load

Always. Prevent cleaner, more generic, more plausible, or more category-normalized drift.

## Rules

- Cap generated polish to the source. Preserve visible roughness, softness, asymmetry, color cast, retouching level, ordinary capture, and medium imperfections.
- Treat subject attractiveness and image polish as separate controls. A supported attractiveness anchor must not imply cleaner skin, symmetry, makeup, crop, focus, lighting, or editorial finish.
- Preserve illusion, mismatch, mixed-media layering, scale incongruity, low fidelity, or awkward capture above a more plausible scene.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever their default pulls toward common composition, cleaner styling, expanded crop, completion, or beautification. Put visible evidence before shorthand.
- Treat source fidelity ceiling as an affirmative requirement: do not exceed visible sharpness, cleanliness, glamour, lighting balance, readability, symmetry, or plausibility unless requested.
- Avoid `high quality`, `crisp`, `clean`, `luxury`, `cinematic`, or `studio` unless visibly supported without conflicting with crop, light, artifacts, or ordinary capture.

## Aesthetic salience gate

Decide whether changing the visible form, surface, light, color, or hierarchy while retaining the objects would materially change the image's identity or appeal.

In diagnostic mode, name the source-supported perceptual appeal directly before decomposing it into visible mechanisms. Do not attribute unseen motive, identity, or story.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only axes with causal weight. The cues must reinforce one proposition rather than form a comprehensive checklist.

- **High salience:** use three to six mutually supporting causal cues.
- **Neutral:** use one or two ordinary visible cues without a special style block.
- **Ambiguous:** describe observed behavior and avoid named genre, camera, film, or era presets.

Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues.

Treat descriptive detail and rendered sharpness as independent controls. Detailed geometry may remain soft, compressed, flat, rough, or low-legibility; do not let detail raise sharpness, scale, polish, or priority.

Translate evaluative or mood words into visible mechanisms. A broad descriptor cannot replace supported form, surface, tone, color, light, sharpness, and hierarchy. Use it at most once, then describe its causes.

## Prompt additions

State the fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent.

When the source look materially differs from a clean default, place a compact Aesthetic Signature near the beginning of `PROMPT:`. In appearance-led mode, put it before pose minutiae; repeat at most one highest-risk drift constraint near the end.

## Optional negative contribution

Reject only likely beautification, relighting, sharpening, style upgrade, symmetry, scene-normalization, crop, or category-default drift.

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

- Confirm that `PROMPT:` contains the primary visual concept, dominant fidelity axis, aesthetic invariants, and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Verify that the first-order proposition leads the prompt: relationship geometry for relationship-led images, form/surface/light/hierarchy for appearance-led images, and layout/legibility for information-led images. Do not overlock dimensions marked flexible.
- Preserve source hierarchy. Check whether a secondary element receives more words than its visible importance supports. Compress secondary pose, material, accessory, or micro-detail when it receives more emphasis than a primary invariant.
- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- State the image's core proposition in one sentence and its causal signature in two to four cues. If that summary is unclear or the cues disagree, rewrite before adding detail.
- Confirm that form, surface, light-to-form, color, material roles, and hierarchy all support the same proposition rather than importing unrelated attractive defaults.
- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer evidence; use at most five unless a layout-dense UI or diagram materially benefits.
- Relate every major component or coherent group to another component or stable zone. For concept-critical interactions, make side, contact, support, containment, and depth order explicit enough to prevent a plausible inversion; distinguish 2D overlap from scene-space contact.
- Keep each primary mass in its source-visible region and every partial or edge-adjacent body, garment, object, reflection, screen, poster, or text block incomplete. Distinguish hair-outline crop from facial-feature crop.
- If the look is high-salience, place its compact Aesthetic Signature before fine detail and keep the cues mutually compatible. For a neutral look, remove the unnecessary signature.
- Confirm that descriptive detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Remove unsupported `shallow depth of field`, beauty lighting, premium bokeh, clean capture, body-type, garment, genre, or other prior-heavy labels unless visible mechanisms constrain their default pull.
- If a human face is prominent and readable, confirm the prompt includes a selective, scale-appropriate likeness set covering the strongest visible face geometry, expression/gaze, hair boundary, and surface/lighting cues. If one broad person-gestalt anchor materially reduces ambiguity, place it before—not instead of—the likeness set; ensure it remains an approximation rather than an identity claim and does not raise beauty polish.
- If a human face is small, soft, shadowed, or heavily occluded, remove speculative micro-features and preserve only reliable head orientation, hair mass, tone, and visibility.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and generic quality assumptions.
- Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams are unlikely to reproduce reliably.

## Length and clarity

- Prefer one measured statement plus one drift constraint for a secondary element.
- Keep constraints concrete and observable; do not repeat locks merely to look exhaustive.
- If the prompt has become a field checklist, rewrite around the dominant proposition, its causal cues, and source hierarchy.


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

Write a standalone English prompt whose order follows the dominant fidelity axis:

- Start every mode with the frame shape, medium, fidelity ceiling, and one-sentence primary perceptual proposition.
- **Relationship-led:** establish composition, crop, major zones, topology, interaction geometry, and up to five critical spatial anchors before local appearance.
- **Appearance-led:** establish the compact Aesthetic Causal Signature and source-specific subject form, surface, light-to-form, color, and hierarchy before secondary pose coordinates or inventory.
- **Information-led:** establish layout, reading order, information hierarchy, legibility, and container relationships before decorative styling.
- **Mixed:** name the two co-primary invariants early and interleave only the cues needed to show how they depend on each other.
- Finish with remaining subject detail, camera/rendering behavior, background, meaningful artifacts, and only the highest-risk drift constraints.

Use short labeled blocks or compact paragraphs for complex images. Aim for the smallest prompt that preserves the source hierarchy; a typical prompt should not need every possible camera, anatomy, lighting, and settings field.

Keep essential requirements affirmative. Prefer `only a narrow cropped strip remains visible` over relying on `do not expand the strip` in another section.

Relate every major component or coherent group to another component or stable scene zone. Keep each concept-critical side, containment, contact, and support relation in `PROMPT:` as one compact affirmative sentence. Do not leave it implied only by an action verb, approximate coordinate, or negative prompt.

For a high-salience look, keep one compact Aesthetic Signature in the first or second paragraph before fine face, material, or background inventory. Use three to six source-supported causal cues spanning only material form, surface, light-to-form, tone/color, sharpness, or hierarchy axes. For a neutral look, use one or two cues without a labeled block. Do not fill every axis or repeat the signature through synonyms.

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

For `diagnostic`, first state the source-supported perceptual proposition or appeal directly in the user's language, then explain the form, surface, light, color, hierarchy, spatial, and capture mechanisms that create it. Separate invariants from pose or placement details that may vary. A candidate `PROMPT:` may follow, but do not force generation-only sections.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.


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
