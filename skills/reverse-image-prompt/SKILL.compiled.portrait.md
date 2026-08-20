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

When evaluating or revising this skill, also read `references/behavior-evaluation.md`. Do not load that evaluation protocol for an ordinary one-image prompt request.

## Workflow

1. Inspect only the provided image.
   - Use the attached image directly or inspect the exact local file.
   - If no image is available, ask for it.
   - Process multiple images independently unless the user clearly requests a combined prompt.

2. Use visible evidence only.
   - Do not identify people, characters, brands, artists, cameras, lenses, film stocks, or private identities from appearance.
   - Keep uncertainty internal during analysis. In the final generation prompt, describe the visible ambiguity itself with terms such as `indistinct`, `partially obscured`, `low-legibility`, or `soft-edged`; avoid weakening commands with repeated `likely` or `appears`.

3. Analyze silently with an adaptive hierarchy:
   1. Record the direct, source-supported appeal separately from the render contract. State it plainly in diagnostic mode, but do not copy evaluative appeal language into a generation prompt; translate it into visible causal controls first.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Separate a small set of aesthetic or structural invariants from dimensions that may vary without losing the proposition. For each invariant, record its semantic slot, hierarchy role, causal origin, source-relative strength, evidence, and one clause owner. Record the smallest causal cue set rather than every visible field.
   4. Lock frame ratio, crop, subject scale, major zones, boundary sides, and edge interactions.
   5. Map the few largest coherent image regions by relative area, tonal role, edge contact, legibility, and attention. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze visible subjects and their image-plane roles. Use a compact broad person-gestalt anchor only when it materially reduces ambiguity; decompose salient human form or appearance into visible causes.
   7. Before treating shape, scale, color, surface, or definition as intrinsic, separate effects caused by pose/deformation, perspective, lighting/shadow, material interaction or occlusion, and capture/processing.
   8. Add only materially important pose, camera/perspective, focus, lighting, background, medium, texture, artifact, UI, and text evidence.

   Use this sparse internal map; leave irrelevant fields empty rather than completing a checklist:

```yaml
direct_appeal_read: ""  # diagnostic explanation only; never copied verbatim into render instructions
render_contract:
  mode: relationship-led | appearance-led | information-led | mixed
  perceptual_proposition: ""
  invariants:
    - id: ""
      axis: form | surface | light-to-form | color | sharpness | hierarchy | topology | information
      role: primary | supporting
      observation: ""
      causal_origin: intrinsic | pose-deformation | perspective | lighting-shadow | material-interaction | processing | spatial-relation | layout
      target_strength: subtle | moderate | strong
      source_evidence: []
      clause_owner: ""
  flexible_dimensions: []
  major_regions: []     # relative area, tonal/material role, edge contact, legibility, attention
  candidate_claims: []  # evidence candidates from modules; not automatic prompt sentences
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

5. Treat selected modules as evidence contributors, not prose entitlements. Merge candidate claims by semantic slot before drafting; one module owns each emitted slot while other modules may strengthen its evidence. Resolve conflicts and allocate prompt weight using this priority:
   1. Visible-evidence and safety limits.
   2. Primary perceptual proposition, dominant fidelity axis, and invariants.
   3. The mode-leading evidence: topology for relationship-led, causal appearance signature for appearance-led, information hierarchy for information-led, or the named co-primary pair for mixed.
   4. Frame ratio, crop, major zones, boundary sides, visibility, and completion budgets.
   5. Subject, medium, camera, lighting, focus, artifact, background, and color fidelity that supports the proposition.
   6. Flexible pose or placement detail, secondary elements, and generic shorthand.

6. Draft the smallest prompt that carries every invariant and concept-critical constraint. Let its order follow the dominant fidelity axis. If the source look is high-salience, place one compact Aesthetic Causal Signature near the beginning; if neutral, use only one or two ordinary cues. Translate broad appeal words into form, surface, light, color, hierarchy, or spatial mechanisms. Normally express a semantic slot once and add at most one source-supported drift boundary for a genuinely high-risk failure. Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Give each major component one relation and each inversion-prone interaction one relation clause, but do not let flexible pose coordinates or secondary details outrank the primary proposition.

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
- Module selection controls what must be checked, not how many words it receives. A routed detail module may contribute no standalone sentence when its evidence is already owned by a primary invariant.
- Keep the normal route within 3-8 non-core modules. Refine an over-budget facet map instead of loading every plausible module.
- Treat `ordinary`, `cropped-edges`, and `small-props` as core-handled observations unless another visible risk requires a dedicated module.
- Do not use broad labels such as `cinematic`, `studio`, `luxury`, `beauty shot`, or `high quality` when they would normalize source-specific evidence.

## Output selection

Always write the production prompt in English. Match the response language for diagnostic explanation unless the user asks otherwise.

- Always emit `PROMPT:` for generation requests.
- Emit `NEGATIVE PROMPT:` only when the user requests it or the named downstream generator supports a separate negative prompt.
- Emit `RECOMMENDED SETTINGS:` only when requested, when a target generator is known, or when source dimensions require a model-specific target-size explanation.
- For `diagnostic` mode, first name the visible core appeal or perceptual proposition directly, then explain the causal form, surface, lighting, color, hierarchy, spatial, and capture evidence. Distinguish invariants from pose or placement differences that would not destroy the aesthetic. Include a candidate prompt only if useful.
- Keep the direct appeal reading in the explanation layer. A production prompt receives only its source-supported causal translation, never unbounded evaluative intensifiers copied from the diagnosis.
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
- Before treating an observed contour, scale, color, surface, or definition as intrinsic, separate effects caused by pose or deformation, perspective, lighting or shadow, material interaction or occlusion, and capture or processing. Preserve the visible result while assigning each prompt control to the most plausible visible cause.

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

## Major-region hierarchy

Map the few largest visually coherent regions as a major-region hierarchy before local detail. For each, record relative area, tonal or material role, first-attention priority, legibility, and contact with the frame edge. Use source-relative roles such as dominant field, supporting mass, edge frame, or low-legibility zone rather than fixed percentages.

Preserve the hierarchy of region shares even when a flexible pose, viewpoint, or placement changes. Exact coordinates may move while the balance among dominant, supporting, and framing regions remains stable.

## Spatial language

Prefer generator-friendly relations such as `left third`, `near the bottom edge`, `occupies roughly half the frame height`, `touches the left edge`, or `leaves a narrow background band`.

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

If settings are requested, report the source frame as metadata and the validated target size separately. Prefer `auto` without a valid deterministic adapter, and disclose ratio-preserving adjustments.


---

# Included module: `concept.primary-relationship`

# Concept: primary perceptual proposition and relationship

## When to load

Always. Apply deeper spatial analysis to relationship-led occlusion, replacement, reflection, frame-within-frame, miniature, mixed-media, or collage images; do not impose it on ordinary images.

## Core rule

State the primary visual concept and perceptual relationship before inventory details.

Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed` before deciding prompt order.

Relationship-led means topology or interaction carries the image; appearance-led means form, surface, light, color, or gestalt survives modest pose variation; information-led means layout, legibility, sequence, or data hierarchy carries it; mixed names two genuinely co-primary axes.

Preserve the side-of-boundary, containment, contact, support, and depth order of concept-critical elements.

## Analysis

Form internally:

1. The visible elements, hierarchy, and primary perceptual proposition: what makes the image itself or compelling, beyond object inventory.
2. Keep the direct appeal reading separate from the render contract: diagnostic language may name the attraction plainly, but generation language must express only its visible causal mechanisms.
3. The dominant fidelity axis and smallest causal cue set.
4. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it.
5. Build an invariant salience ledger. Give each invariant a semantic slot, primary or supporting role, observed target, causal origin, source-relative strength, evidence, and one clause owner.
6. For relationship-led or mixed images, the stable zones and each critical pair's side, containment, contact, support, depth, occlusion, and boundary crossing.
7. One to three likely failures, including a category default replacing source-specific evidence.

Build a sparse relation graph and group elements sharing a relation. Keep ordinary premises ordinary. In appearance-led images, do not let minor coordinates outrank appearance; in information-led images, prioritize layout and legibility.

Distinguish image-plane overlap from scene-space containment, contact, and support. When geometry could invert, record contact, weight support, and the relevant boundary or support plane; use object- or scene-relative zones when screen directions are ambiguous.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record join, overlap, contact, containment, hidden or partial regions, boundary side, support, layer order, scale, and coherence ceiling.

## Prompt contribution

Contribute evidence candidates, not guaranteed prose. The central output contract merges candidates by semantic slot and assigns one clause owner. Write a construction recipe, not a prop list; lead with the dominant axis and spend more words on topology only when it is first-order.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone.

For each concept-critical interaction, write one explicit relation sentence naming both elements, their relevant parts, the side or zone, any contact point, and what provides support when visible.

Normally one to three interaction sentences suffice. Avoid redundant coordinates.

## Optional negative contribution

Reject only likely relationship, completion, normalization, or invariant-demotion drift.


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

## Aesthetic salience gate

Decide whether changing the visible form, surface, light, color, or hierarchy while retaining the objects would materially change the image's identity or appeal.

In diagnostic mode, name the source-supported perceptual appeal directly before decomposing it into visible mechanisms. Do not attribute unseen motive, identity, or story.

Keep that appeal reading out of the production prompt until it has been translated into bounded, observable render controls. An evaluative phrase is not itself an invariant.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only axes with causal weight. Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues. For ambiguous evidence, describe observed behavior rather than invoking a genre, camera, film, or era preset.

Treat descriptive detail and rendered sharpness as independent controls. Detailed geometry may remain soft, compressed, flat, rough, or low-legibility; do not let detail raise sharpness, scale, polish, or priority.

Translate evaluative or mood words into visible mechanisms. A broad descriptor cannot replace supported form, surface, tone, color, light, sharpness, and hierarchy. Use it at most once, then describe its causes.

Audit prior-heavy cues as a combined cluster, not only as isolated labels. Temporarily ignore the subject nouns and ask whether the remaining quality, lighting, surface, framing, and style language strongly invokes a category default unsupported by the source. Rewrite the unsupported cluster from visible evidence; do not turn its individual words into a universal blacklist.

## Prompt additions

State the fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent.

When the source look materially differs from a clean default, place a compact Aesthetic Signature near the beginning of `PROMPT:`. In appearance-led mode, put it before pose minutiae; repeat at most one highest-risk drift constraint near the end.

## Optional negative contribution

Reject only likely beautification, relighting, sharpening, style upgrade, symmetry, scene-normalization, crop, or category-default drift.


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
- Separate intrinsic surface color from illumination color, global color cast, and exposure. Consolidate each important surface or region into one owned color instruction; other modules may describe how light shifts it but must not restate the same hue direction as additional emphasis.
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

Apply this as a rewrite pass, not a checklist appended to the draft.

### Coverage and ownership

- Confirm that `PROMPT:` contains the primary visual concept, dominant fidelity axis, aesthetic invariants, and every non-negotiable relationship, crop, occlusion, boundary, and medium constraint.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner. Other modules may add evidence but not synonymous output clauses.
- Give every primary invariant one affirmative render control. Keep flexible dimensions supporting unless the source makes their exact state proposition-critical.
- Verify that the first-order proposition leads the prompt: relationship geometry for relationship-led images, form/surface/light/hierarchy for appearance-led images, and layout/legibility for information-led images.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. A set of individually plausible cues fails when their combined pull exaggerates an invariant or promotes a supporting axis.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Normally keep one affirmative clause per slot and only one high-risk drift boundary when it adds a distinct control.
- Preserve source hierarchy. Check whether a secondary element receives more words than its visible importance supports. Compress secondary pose, material, accessory, or micro-detail when it competes with a primary invariant.
- Audit prior-heavy language as a combined cluster. If quality, lighting, surface, framing, and style cues collectively invoke an unsupported category default, rewrite the cluster from evidence instead of blacklisting individual words.

### Causal consistency

- Confirm that form, surface, light-to-form, color, material roles, and hierarchy support one proposition. Do not encode pose, perspective, shadow, material pressure, occlusion, or processing as intrinsic shape or surface without visible evidence.
- Keep intrinsic surface color, illumination color, global cast, and exposure distinct. Remove repeated hue-direction cues owned by another slot.
- Ensure the direct appeal reading was translated into observable controls rather than copied as unbounded evaluative intensity.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Remove a numeric anchor when it conflicts with clearer evidence; use at most five unless a layout-dense UI or diagram materially benefits.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- For a prominent readable face, retain a selective scale-appropriate likeness set. For a small, soft, shadowed, or occluded face, remove speculative micro-features and keep only reliable orientation, hair mass, tone, and visibility.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and generic quality assumptions. Report prompt-only limits honestly when exact text, identity, pose, hands, UI placement, tiny marks, or complex seams remain unreliable.

## Length and clarity

- Prefer one measured statement for a secondary element; add a drift constraint only for a distinct high-risk failure.
- Keep constraints concrete and observable; do not repeat locks merely to look exhaustive.
- If the prompt has become a field checklist, rewrite around the dominant proposition, its causal cues, and source hierarchy.


---

# Included module: `core.output-contract`

# Core: adaptive output contract

## When to load

Always. Apply after the visual analysis and routed modules.

## PROMPT

Emit only sections required by the selected output mode.

For a generation request, emit:

```text
PROMPT:
...
```

Write a standalone English prompt ordered by the dominant fidelity axis:

- Begin with frame shape, medium, fidelity ceiling, and the perceptual proposition.
- **Relationship-led:** place crop, major zones, topology, interaction geometry, and only critical spatial anchors before local appearance.
- **Appearance-led:** place the compact causal signature and source-specific form, surface, light-to-form, color, and hierarchy before flexible pose or inventory.
- **Information-led:** place layout, reading order, hierarchy, legibility, and container relations before decoration.
- **Mixed:** name the co-primary invariants early and include only cues showing their dependency.
- Finish with remaining subject, capture, background, artifact, and highest-risk drift controls.

Selected modules contribute evidence candidates, not mandatory prose. The output composer merges them by semantic slot before drafting; module count must not determine prompt length.

Assign one clause owner to each emitted semantic slot. Normally state its affirmative target once; a second clause is justified only when it supplies a distinct high-risk boundary rather than repeating the target through synonyms.

Use compact paragraphs or short blocks for complex images. Apply no fixed global word cap; every additional clause must add a new control. Keep essential crop, partial visibility, and interaction requirements affirmative. Relate each major component to another component or stable zone, and state inversion-prone side, containment, contact, or support directly.

For a high-salience look, put one compact Aesthetic Signature before fine inventory and use only source-supported causal axes. For a neutral look, use one or two ordinary cues. Preserve major-region hierarchy by relative area, tonal or material role, edge contact, legibility, and first attention even when flexible pose or placement changes.

When face likeness is selected, use one dedicated, scale-appropriate passage. A broad person-gestalt anchor may lead it but cannot replace visible geometry or raise beauty polish.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

When a negative prompt is supported, reject only likely concept and fidelity drift. Keep it compact and image-specific; do not duplicate the positive prompt or use negatives to counter an overstrong positive cluster. Rewrite the positive wording to source-relative strength first.

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

Include only real controls of the named generator. Separate source dimensions from the requested target size. Omit irrelevant fields, read `references/model-adapters.md` before naming values, and keep visual locks in `PROMPT:`.

## Diagnostic mode

For `diagnostic`, state the source-supported proposition or appeal directly, then explain its visible form, surface, light, color, hierarchy, spatial, and capture mechanisms. Keep diagnostic appeal language separate from render instructions: a candidate prompt receives bounded observable mechanisms, not copied evaluative intensity. Separate invariants from flexible pose or placement; include a candidate prompt only when useful.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.


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

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve source-relative shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette only to the degree visible.
- Separate anatomical proportion from near-camera enlargement, foreshortening, pose compression, garment pressure, and light/shadow shaping. Do not convert a bright edge or dark groove into unsupported anatomy.
- Keep the torso, pelvis, and center of mass in the source-visible spatial zone; do not let a contact pose silently relocate the person across a barrier, edge, opening, or support surface.
- Preserve a clearly visible large-scale body silhouette without exaggeration or reduction.
- Keep a moderate or obscured body silhouette secondary rather than promoting it.
- If age is unclear or the person is not clearly adult, use neutral, non-sexual silhouette and clothing language.
- Keep secondary or cropped body regions subordinate to a dominant face, action, prop, or relationship.
- Lock the person's frame share and environmental context before facial detail. Do not let a detailed face passage enlarge the subject or convert an environmental portrait into a close beauty portrait.

## Module handoff

- Add `detail.human-face-likeness` for a prominent or clearly readable face.
- Add `detail.human-body-form` when visible proportion, contour, tissue character, muscle definition, skin surface, or body-region hierarchy is a first-order part of the image's identity or appeal.
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

## Evidence contribution

Contribute only photographic controls that materially affect an invariant or likely drift. Describe:

- camera distance, height, angle, roll/rotation, lens impression, perspective distortion
- subject-to-camera relationship and how perspective affects face/body/object/background proportions
- close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, telephoto compression, low-angle elongation, high-angle compression only when visible
- focus target, focus accuracy, depth of field, bokeh, foreground/background blur, low-resolution softness, sharpening, compression, noise reduction, bloom, haze
- motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable capture
- camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look
- For casual phone, screenshot, social-video, or compressed outdoor captures, state the capture imperfection ceiling before beauty, fashion, scenic, studio, or product shorthand. Preserve handheld asymmetry, preview/compression softness, flattened distant layers, bloom, haze, clipped highlights, low-legibility marks, and ordinary non-editorial framing when visible.

Map sharpness separately across the primary subject, secondary details, foreground, and background.

Map contrast topology separately at the global scene, major subject masses, local form transitions, and surface/material boundaries.

- Identify the largest continuous bright shapes and darkest framing masses before listing small highlights or shadows.
- Separate overall tonal range from local subject contrast. A low-contrast scene can still have one crisp boundary; a high-contrast scene can retain soft internal form.
- State whether shadows flatten volume, softly imply it, separate overlapping planes, or hard-sculpt contours. Do not let `dramatic lighting` stand in for that behavior.
- Distinguish diffuse, matte, translucent, oily, glossy, metallic, woven, and absorbent responses only when visible; different surfaces under one light need not share highlight width or black level.

Decompose photographic appearance into intrinsic subject evidence, pose or deformation, perspective, illumination and shadow, material interaction or occlusion, and capture or processing. Preserve their combined visible result, but do not let one cause rewrite another.

Record important color relationships as intrinsic surface hue, illumination color, global cast, and exposure response. Assign the consolidated hue instruction to one semantic slot; this module should describe the photographic shift rather than repeat another module's color target.

Distinguish global low acutance, diffusion, haze, compression, or processing softness from depth-of-field blur. Use `shallow depth of field` or premium-looking bokeh only when a visibly sharper focus plane is separated from defocused layers. If the nominal focus subject is also soft, preserve that softness instead of sharpening it while blurring only the background.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Keep global contrast distinct from local form contrast so a dark frame or wide tonal range does not automatically create hard internal definition.

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

# Included module: `detail.human-body-form`

# Detail: human body form, proportion, and surface

## When to load

Load only when visible body form is a first-order part of the image's identity or perceptual appeal: source-relative proportion, silhouette, contour rhythm, tissue character, muscular definition, skin surface, or the hierarchy among body regions. Do not load merely because a person is present.

## Analysis

Start with the large-scale form proposition before region detail. State directly what visible quality carries the impression—such as long-lined, compact, broad, narrow, soft, firm, relaxed, tense, delicate, sturdy, or strongly defined—then test it against observable causes. A broad descriptor is a hypothesis, not a substitute for evidence.

Build a visible human-body form signature from source-supported proportion, contour, tissue, tension, and region hierarchy rather than from a body-type label.

Split persistent body-form evidence from induced appearance before selecting prompt controls. Persistent evidence comes from repeated contour and proportion relationships; induced evidence may come from pose, compression, perspective, garment pressure, highlight, self-shadow, cast shadow, occlusion, or processing. Preserve the visible combination without promoting an induced effect into an intrinsic body invariant.

Use only the axes that materially distinguish the source:

- **Proportion:** source-relative spans and transitions among head, shoulders, ribcage/torso, waist, pelvis/hips, arms, legs, hands, and feet where visible. Prefer relationships such as `shoulders only slightly wider than the waist` over inferred measurements.
- **Contour and tissue:** straight or curved outer contours, abrupt or gradual width changes, bony landmarks, soft tissue transitions, firmness, softness, compression, folds, and where contours disappear into clothing, crop, or shadow.
- **Tension and posture:** relaxed suspension, bracing, extension, compression, twist, weight-bearing, or flexion. Distinguish persistent form from a temporary pose effect.
- **Definition:** Separate visible muscle or skeletal definition from contour created by pose, perspective, garment pressure, highlight, self-shadow, and cast shadow.
- **Surface:** Describe skin as a surface system: lightness, hue family, saturation, undertone, tonal variation, finish, texture, and response to light only where visible.
- **Hierarchy:** Assign each visible body region a hierarchy role—primary form, structural connector, supporting mass, edge crop, or low-legibility background evidence.

Analyze the transitions between regions, not only isolated sizes. A waist, shoulder, joint, torso, or limb reads through its relation to adjacent forms, garment boundaries, negative space, and the direction of light.

## Perspective and light separation

- Establish camera distance, angle, and foreshortening before treating image-plane width as anatomy.
- Compare near and far counterparts when visible; do not force symmetry through an oblique view.
- Identify the largest bright and dark masses crossing the body, then decide whether they flatten, softly imply, separate, or strongly sculpt form.
- Do not translate smooth lighting into low muscularity, or hard directional shadow into greater muscularity, without contour evidence.
- Keep skin tone separate from exposure and color cast. Record both the underlying visible hue relationship and the illumination that shifts it.

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

## Evidence contribution

Describe visible garment geometry before broad category labels:

Prefer visible garment geometry over broad fashion-category labels.
Treat visible band-height drift as a composition failure.
Assign each visible garment or accessory a material role: primary subject, silhouette boundary, frame, texture support, or low-legibility mass.

Route selection does not entitle clothing to prompt space. Cap material and construction detail to the garment's hierarchy role; a framing or supporting garment must not receive more semantic emphasis, sharpness, or completion than the primary invariant.

- fit, visible thickness and weight, opacity/transparency, stiffness/looseness
- fabric tension, wrinkles, folds, material sheen, pattern scale
- weave or knit scale, nap, grain, coating, reflectivity, and edge behavior only where legible
- neckline depth/width, collar, shirt opening, sleeve opening, strap position
- seams, waist seam, under-bust seam if visible, buttons, lace, closures, hems
- garment layers and how they interact with body shape, pose, props, hair, hands, shadow, and crop

Before using a garment category label, specify the visible opacity, thickness, weight, weave or knit scale, finish, and construction cues that must override its default prior. Omit dimensions that cannot be seen; the point is to disambiguate the material, not to fill a fabric checklist.

Create a coverage map when clothing placement matters:

- which image regions are skin
- which regions are fabric
- which regions are shadow-hidden
- which regions are cropped away
- which garment edges are interrupted, softened, shadowed, blurred, or blocked

Treat close upper-torso edges as measured boundary bands, not fashion labels. Lock neckline/garment-edge width, lowest y-position, visible skin/underlayer area above and below it, sleeve/shoulder fabric area, and bottom crop.

Avoid broad labels such as `off-shoulder`, `low neckline`, `camisole`, `dress`, `lingerie`, `corset`, `crop top`, or `fashion portrait` if their category prior would deepen, widen, clarify, center, tighten, reveal, structure, or glamorize the garment beyond the source. Category labels follow geometry and material role; they do not define them.

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
