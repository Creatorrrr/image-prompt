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

When `detail.color-tone-fidelity` is selected and the request requires measured color fidelity, source/render comparison, actual generation, or controlled color revision, also read `references/color-reproduction-evaluation.md`. Keep ordinary incidental-color prompt extraction on the shorter module path.

When `detail.light-form-fidelity` is selected and the request requires measured lighting fidelity, source/render comparison, actual generation, or controlled lighting revision, also read `references/lighting-reproduction-evaluation.md`. Keep ordinary incidental lighting on the shorter medium-module path.

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
   8. When color or tonal behavior is material, build the source-relative Color/Tone Contract from `detail.color-tone-fidelity`: set the source-visible/color-managed/user-specified observation scope; separate region value, chroma, and hue from illumination, global cast or palette shift, exposure or tone curve, and processing; keep intrinsic midtone evidence separate from highlight and shadow response; decompose appearance metaphors; record neutral-anchor confidence and cross-layer aggregate effects. For every material intrinsic axis, declare whether it requires a final prompt control or remains diagnostic-only, and link every required axis through one aggregate effect, claim, and axis-specific emitted control.
   9. When illumination, shadow topology, or light-induced form is material, build the source-relative Light/Form Contract from `detail.light-form-fidelity`. Record the visible result before any physical-light hypothesis; separate source geometry, apparent source size, fill, global tonal range, local form contrast, shadow ownership, material response, background spill, and pose dependence. A low-confidence rig hypothesis remains diagnostic or is paired with result-space controls rather than carrying the prompt alone. Link every emitted lighting effect through one claim and one exact final-prompt control.
   10. Add only materially important pose, camera/perspective, focus, lighting, background, medium, texture, artifact, UI, and text evidence.

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
  color_tone_contract: {}  # when material: observation scope, causal effects, then exact post-draft emitted_controls
  light_form_contract: {}  # when material: observed result, confidence-rated cause, spatial effects, then exact emitted_controls
```

4. Build and resolve this internal facet map:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face-detail, body-form, body-proportion, muscle-definition, body-tension, skin-surface, body-region-hierarchy, color-tone, color-fidelity, tone-fidelity, surface-color, global-cast, white-balance, exposure-tone, palette-relationship, lighting-fidelity, light-direction, shadow-topology, light-to-form, material-light-response, background-spill, clothing, hands, text-logo, ui, small-props, cropped-edges, tight-selfie, face-hand-gesture, accessory-torso-budget
  style: []           # stylized-character-maturity or another narrow risk
```

5. Treat selected modules as evidence contributors, not prose entitlements. Merge candidate claims by semantic slot before drafting; one module owns each emitted slot while other modules may strengthen its evidence. For material color and tone, also merge claims by shared perceptual effect across intrinsic surface, illumination, global cast, exposure, processing, and hierarchy even when their semantic-slot names differ. For material lighting, merge effects across source geometry, fill, local form contrast, shadow topology, material response, and background spill. Let the Light/Form Contract own spatial illumination structure and the Color/Tone Contract own displayed color, exposure, and tone response; split or cross-reference rather than duplicate a shared effect. Resolve conflicts and allocate prompt weight using this priority:
   1. Visible-evidence and safety limits.
   2. Primary perceptual proposition, dominant fidelity axis, and invariants.
   3. The mode-leading evidence: topology for relationship-led, causal appearance signature for appearance-led, information hierarchy for information-led, or the named co-primary pair for mixed.
   4. Frame ratio, crop, major zones, boundary sides, visibility, and completion budgets.
   5. Subject, medium, camera, lighting, focus, artifact, background, and color fidelity that supports the proposition.
   6. Flexible pose or placement detail, secondary elements, and generic shorthand.

6. Draft the smallest prompt that carries every invariant and concept-critical constraint. Let its order follow the dominant fidelity axis. If the source look is high-salience, place one compact Aesthetic Causal Signature near the beginning; if neutral, use only one or two ordinary cues. Translate broad appeal words into form, surface, light, color, hierarchy, or spatial mechanisms. Normally express a semantic slot once and add at most one source-supported drift boundary for a genuinely high-risk failure. For material color or tone, assign every emitted direction to one causal layer and one aggregate effect budget; do not let hierarchy repeat a surface hue unless hue contrast itself is invariant. Give each required intrinsic value, chroma, or hue axis its own literal axis-control; a hierarchy or exposure clause cannot substitute for intrinsic surface value. After drafting, copy the exact final color-changing excerpts into the Color/Tone Contract's `emitted_controls` ledger and reconcile each with one claim, one causal layer, one region, one axis, and its complete aggregate-effect list. For material lighting, copy every exact lighting-changing excerpt into the Light/Form Contract's `emitted_controls`; keep source geometry, fill, local form contrast, shadow topology, material response, and background spill separately owned, and preserve result-space controls when the physical cause is uncertain. Split or replace unowned, cross-axis, and multi-layer compounds. Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Give each major component one relation and each inversion-prone interaction one relation clause, but do not let flexible pose coordinates or secondary details outrank the primary proposition.

7. Apply the pre-emit gate and report prompt-only limits honestly.

## Routing rules

- Always load Tier 0.
- Select at least one subject and one medium; use the generic/unspecified fallbacks only when evidence is unclear.
- Load every visible Tier 1 relationship module, including both photographic and non-photographic medium modules for genuine mixed media.
- Load Tier 3 and Tier 4 modules only for visible, material risks.
- For a prominent or clearly readable human face, add `face-detail`; for a small, blurred, shadowed, or heavily occluded face, keep only scale-appropriate human evidence and do not invent micro-features.
- Add a human body-form risk only when visible proportion, contour/tissue, muscle definition, skin surface, tension, or body-region hierarchy is first-order. Do not route it merely because a person or torso is visible.
- Add `detail.color-tone-fidelity` only when color or tonal behavior is first-order, the user explicitly prioritizes tone fidelity, or confusion among intrinsic color, illumination, cast, exposure, and processing would materially change the image. Do not route it for ordinary incidental color.
- Add `detail.light-form-fidelity` only when lighting, shadow topology, light-induced form, material response, or background spill is first-order; when the user explicitly prioritizes lighting fidelity; or when a source/render comparison identifies lighting as a material residual. Do not route it for ordinary incidental lighting already handled by the selected medium module.
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
- Preserve visible illusion, mismatch, mixed-media layering, scale incongruity, low fidelity, or awkward capture above plausibility.
- Weaken broad portrait, fashion, garment, product, genre, and body-region labels when they pull toward cleaner styling, expanded crop, completion, or beautification. Put evidence before shorthand.
- Treat source fidelity ceiling as an affirmative requirement: do not exceed visible sharpness, cleanliness, glamour, lighting balance, readability, symmetry, or plausibility unless requested.

## Aesthetic salience gate

Decide whether changing visible form, surface, light, color, or hierarchy while retaining objects would change the image's identity or appeal.

In diagnostic mode, name the source-supported perceptual appeal directly before its visible mechanisms; do not infer motive, identity, or story.

Keep appeal language out of the prompt until translated into bounded controls; evaluation is not an invariant.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only causal axes. Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues. Describe ambiguity instead of invoking presets.

Treat descriptive detail and rendered sharpness as independent controls. Detail must not raise sharpness, scale, polish, or priority.

Translate evaluative or mood words into visible mechanisms. Use a broad descriptor at most once; it cannot replace causal evidence.

Treat a broad color descriptor as a hypothesis about one causal layer, not as shorthand for hue, value, chroma, lighting, mood, and processing at once. Replace overload with source-supported axes.

Decompose an appearance metaphor into observable color axes, surface behavior, and illumination before using it as a non-directional summary. A metaphor may summarize resolved evidence once; it must not add a second color, gloss, softness, luminosity, or grading instruction.

Audit prior-heavy cues as a combined cluster, not only as isolated labels. Ignore subject nouns temporarily; rewrite unsupported quality, lighting, surface, framing, or style defaults from evidence without a universal blacklist.

## Prompt additions

State the fidelity ceiling early when the image is casual, degraded, stylized, awkward, or illusion-dependent.

When the source differs from a clean default, place a compact Aesthetic Signature early; add at most one highest-risk boundary.

## Optional negative contribution

Reject only likely beautification, relighting, sharpening, style upgrade, symmetry, scene-normalization, crop, or category-default drift.


---

# Included module: `core.background-color`

# Core: background, color, and environment zoning

## When to load

Always. Every image has background, color, or negative-space structure.

## Rules

- Analyze background zoning as image-plane layers, edge bands, negative space, dark or bright masses, texture, and low-detail regions; preserve their crop positions.
- Preserve background priority. Keep dim, cropped, blurred, hidden, or secondary elements as low-detail massing.
- Treat background legibility and information density as part of the source aesthetic. Named elements inherit source blur, haze, contrast, and detail limits.
- Preserve color mood, cast, saturation, contrast, shadow/highlight color, and local relationships; do not normalize them toward genre defaults.
- Separate intrinsic surface color from illumination color, global color cast or palette shift, exposure or tone curve, and processing. Consolidate each important surface or region into one owned color instruction; other modules may describe how light shifts it but must not restate the same perceptual direction as additional emphasis.
- Keep global cast consistent with the source-visible behavior of multiple regions rather than inferring it from one salient surface. When a global shift is uncertain, preserve relative region relationships instead of forcing a white balance or palette grade.
- Treat a possible neutral reference as evidence only when its low-chroma appearance survives visible illumination, reflection, exposure, clipping, compression, and processing. Record confidence rather than assuming that white, gray, black, or metal is neutral.
- Keep value, chroma, and hue relationships separate. A hierarchy statement may own relative brightness, saturation, area, or contrast, but must not restate a region's intrinsic hue unless hue contrast itself carries the hierarchy.
- In dark, compressed, or hazy areas, distinguish crushed regions from remaining folds, edges, silhouettes, texture, or hints; neither erase nor brightly recover them.
- Prevent clean-room drift: do not replace messy, partial, compressed, or ordinary zones with a tidy backdrop unless visible.

## Prompt additions

Describe zones by position, mass, contrast, legibility, depth, and color behavior before setting labels.

## Optional negative contribution

Reject source-likely cleanup, recovery, invented legibility, removed clutter, added depth, or priority drift.

## Optional settings contribution

- Background, palette/cast, and low-legibility locks:


---

# Included module: `core.pre-emit-gate`

# Core: pre-emit gate

## When to load

Always. Apply immediately before the final answer.

## Gate

Apply this as a rewrite pass, not a checklist appended to the draft.

### Coverage and ownership

- Confirm that `PROMPT:` contains the primary visual concept.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner.
- Give each primary invariant one affirmative control; keep flexible dimensions supporting. Order by the dominant fidelity axis.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. Plausible cues still fail when their combined pull exaggerates an invariant.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Keep at most one distinct high-risk boundary per slot.
- Check whether a secondary element receives more words than its visible importance supports; compress it when it competes with a primary invariant.
- Rewrite unsupported category defaults from evidence.

### Causal, color, and tone consistency

- Keep form, surface, light, color, material, and hierarchy causally consistent; do not encode induced effects as intrinsic.
- Audit shared perceptual effects across semantic slots, causal layers, paragraphs, negatives, and settings. Slot names being unique does not make repeated value, chroma, hue, or contrast directions independent.
- For a material color or tone effect, verify one aggregate source-relative target and the evidence for every emitted intrinsic, illumination, global-cast, exposure, processing, or hierarchy contribution. Merge or delete a contribution whose causal layer lacks independent evidence.
- Assign every appearance-changing color or tone phrase to one causal layer; treat free-floating mood or color adjectives as unowned claims and rewrite them from observable axes.
- Split an ambiguous color phrase when one modifier could silently control intrinsic surface, illumination, exposure, or processing at the same time.
- Re-read the exact final `PROMPT:` rather than trusting the analysis plan. Reconcile every exact color-changing excerpt in the final prompt with one emitted claim, one causal layer, and its complete aggregate effect budget. Split, replace, or delete any unowned excerpt, repeated direction, or multi-layer compound.
- For every required intrinsic value, chroma, or hue observation, trace one uninterrupted path from region axis to same-region/same-axis aggregate effect, emitted claim, and intrinsic axis-control. A relative hierarchy, exposure, illumination, or processing clause cannot satisfy missing intrinsic surface value or chroma.
- Give an axis-control one region and one perceptual axis. If one phrase changes several axes, split its literal excerpts or mark it as a justified secondary compound-control; never use a compound-control to satisfy a required intrinsic axis.
- Keep midtone or flat evidence that establishes displayed intrinsic color separate from highlight and shadow evidence that establishes tone response. Mixed tone-zone evidence may remain diagnostic but cannot drive an intrinsic axis-control.
- Treat an appearance metaphor as explanation-only unless it has generator-and-version-specific response evidence. An unverified metaphor cannot be the sole carrier of a material color axis.
- Check global cast against reliable neutral or multi-region evidence; otherwise retain uncertainty.

### Lighting and light-to-form consistency

- For material lighting, verify one source-relative Light/Form target and evidence for every emitted source-geometry, fill, local-form-contrast, shadow-topology, material-response, or background-spill contribution.
- Assign every lighting-changing phrase to one Light/Form owner. Split a phrase that lets apparent source size silently determine fill, local contrast, exposure, material gloss, or background spill.
- Keep global tonal range and local form contrast as separate effects. Do not infer one from the other or let differently named claims amplify the same light-to-form direction.
- Give every material shadow event a source-supported owner or mark it mixed or uncertain. Do not convert contact, occlusion, material absorption, or processing into a directional source without evidence.
- Treat the visible spatial result as authoritative over a physical-light hypothesis. A low-confidence rig may be diagnostic or paired with result-space controls, but cannot carry a primary lighting invariant alone.
- Reconcile every exact lighting-changing excerpt with one emitted claim, one owner, and its complete lighting-effect list. Keep Light/Form spatial effects separate from Color/Tone value, hue, exposure, and tone-curve controls.
- When pose or geometry may vary, preserve the source-supported light-to-form relation while allowing non-invariant highlight coordinates to move.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Remove conflicting numeric anchors; use at most five unless a dense UI or diagram benefits.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Retain scale-appropriate face evidence: selective likeness anchors when readable, only orientation, hair mass, tone, and visibility when small or obscured.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions. Report prompt-only limits honestly for unreliable exact details.

## Length and clarity

- Prefer one concrete statement for a secondary element and add a boundary only for a distinct high-risk failure.
- If the prompt reads as a checklist, rewrite around the proposition, causal cues, and source hierarchy.


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
- **Relationship-led:** crop, major zones, topology, interaction, then appearance.
- **Appearance-led:** causal form, surface, light, color, hierarchy, then flexible pose or inventory.
- **Information-led:** layout, reading order, hierarchy, legibility, then decoration.
- **Mixed:** name co-primary invariants and only cues showing their dependency.
- Finish with supporting subject, capture, background, artifact, and drift controls.

Selected modules contribute evidence candidates, not mandatory prose. Merge them by semantic slot; module count must not determine prompt length.

Assign one clause owner to each emitted semantic slot. State its affirmative target once; add only a distinct high-risk boundary.

When color or tone is material, assign each emitted control to one causal layer and one perceptual effect budget. Use source-relative value, chroma, and hue; keep intrinsic surface, illumination, global cast, exposure, processing, and hierarchy consistent.

Draft intrinsic surface, illumination, global response, and processing as distinct compact clauses when more than one is supported. Before emission, make every exact color-changing phrase traceable to the final color-control ledger; a metaphor may summarize resolved axes but cannot create another directional control.

Place one compact color-tone passage early when primary; when supporting, use the smallest relational control. Hierarchy normally owns area, value, chroma, or contrast, not repeated surface hue.

When lighting is material, assign each emitted control to one Light/Form owner and one source-relative effect budget. Separate source geometry, apparent source size, fill, local form contrast, shadow topology, material response, and background spill; do not let a generic lighting adjective own several of them at once.

Lead with the visible result and add a physical-light explanation only at its supported confidence. Before emission, make every exact lighting-changing phrase traceable to the final Light/Form control ledger. Treat that ledger as internal bookkeeping over the smallest exact clauses, never as a reason to expose a schema, repeat a control, or lengthen the production prompt. Keep spatial illumination structure in that ledger and displayed color, exposure, and tone response in the Color/Tone ledger.

Use compact blocks for complex images and no fixed word cap; every clause must add a control. Keep essential crop, partial visibility, and interactions affirmative. Relate major components and state inversion-prone topology directly.

For a high-salience look, put one supported Aesthetic Signature before inventory; for a neutral look, use one or two cues. Preserve major-region area, role, edge contact, legibility, and attention.

When face likeness is selected, use one scale-appropriate passage; a gestalt anchor cannot replace visible geometry or raise polish.

## NEGATIVE PROMPT

Emit only when the user requests it or the named generator supports a separate negative-prompt input:

```text
NEGATIVE PROMPT:
...
```

When a negative prompt is supported, reject only likely concept and fidelity drift. Keep it compact; rewrite an overstrong positive instead of countering it with negatives.

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

Include only real generator controls. Separate source dimensions from the requested target size, read `references/model-adapters.md`, and keep visual locks in `PROMPT:`.

## Diagnostic mode

For `diagnostic`, state the source-supported proposition, then its visible causal mechanisms. Keep diagnostic appeal language separate from render instructions, distinguish invariants from flexible dimensions, and include a prompt only when useful.

## Final rule

Read `PROMPT:` as if the source image and every optional section disappeared. If the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.


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

Treat the image's sampled or visually read color as displayed capture output. Without calibrated scene data, it does not establish scene reflectance, material true color, or a person's biological color independently of illumination, white balance, exposure, tone mapping, and profile handling.

Separate photographic white balance or global cast from exposure and tone-curve behavior. A warmer or cooler capture shift must not silently darken, brighten, saturate, or desaturate an intrinsic surface unless the source supports each change.

Map source-visible highlight, midtone, and shadow response separately when tonal reproduction is material. Use comparable midtone or flat patches for displayed intrinsic color and separate highlight or shadow patches for response; never widen an intrinsic target by pooling several illumination zones. Preserve clipping, rolloff, lifted or crushed shadows, and local tone compression without using them as substitutes for intrinsic surface lightness or chroma.

Use reliable neutral anchors or consistent multi-region behavior to support a global white-balance claim. When the evidence is mixed or weak, contribute the observed local shifts and uncertainty to the shared Color/Tone Contract rather than forcing a global cast.

In source/render comparison, compare several target patches with contextual or neutral patches. Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. A common direction across both groups supports a global exposure, cast, or processing explanation; a target-only residual supports a local or intrinsic explanation; mixed directions stay unresolved. Do not declare pixel fidelity without an explicit tolerance policy or user judgment.

Distinguish global low acutance, diffusion, haze, compression, or processing softness from depth-of-field blur. Use `shallow depth of field` or premium-looking bokeh only when a visibly sharper focus plane is separated from defocused layers. If the nominal focus subject is also soft, preserve that softness instead of sharpening it while blurring only the background.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, ambient light
- highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, overexposure
- visible cast shadows, self-shadowing, contact shadows only when they affect likeness, separation, occlusion, or composition

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Keep global contrast distinct from local form contrast so a dark frame or wide tonal range does not automatically create hard internal definition.

When lighting itself is first-order, contribute capture evidence to `detail.light-form-fidelity` instead of independently owning source geometry, fill, shadow topology, material response, or background spill. Keep exposure, tone curve, white balance, and illumination color in the photographic Color/Tone handoff so the two contracts do not repeat one visible pull.

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

# Included module: `detail.color-tone-fidelity`

# Detail: color and tone fidelity

## When to load

Load only when color/tone is an invariant, the user requests fidelity, or a causal mix-up could materially change the image. Do not load merely because an image contains color.

## Three-stage Color/Tone Contract

Build a source-relative Color/Tone Contract only when color or tonal behavior materially carries fidelity.

Keep three stages separate:

1. **Observation:** what the source visibly supports.
2. **Actuation:** which literal prompt control carries each material source axis to the named generator.
3. **Verification:** what a delivered render actually reproduced. Prompt validation never substitutes for rendered-pixel verification.

Set scope to `source-visible`, `color-managed` only with trustworthy calibration evidence, or `user-specified` for an explicit external target. Treat sampled pixels as source-visible display color, not proof of biological, material, or scene-referred true color. For human surfaces, use observable evidence rather than demographic identity labels.

For each important region:

- separate value/lightness, chroma/saturation, and hue family/undertone;
- record role, relation to another region, confidence, and uncertainty;
- separate intrinsic surface from illumination, global cast/palette, exposure/tone curve, and processing.

For every intrinsic value, chroma, or hue axis, record `role`, `evidence_scope`, and `emission`. Use `required` only when the axis materially needs a final prompt control. Use `diagnostic-only` with a concrete non-emission reason when an axis is low-confidence, incidental, or already unsupported at prompt precision. Link every required intrinsic axis to exactly one same-region, same-axis aggregate effect.

Assign every material color or tone observation to intrinsic surface, illumination, global cast or palette shift, exposure or tone curve, or processing.

Describe important regions through separate value, chroma, and hue observations plus source-visible relations to other regions. Do not let one broad adjective silently determine all three axes.

Decompose an appearance metaphor into value, chroma, hue, surface, and light response. Mark it `explanation-only`, `unverified`, or `model-calibrated`; only the last may appear once as a summary of already-owned controls, with evidence for the exact generator/version. Treat control effectiveness as generator-and-version-specific evidence.

Map highlight, midtone, shadow, or flat-field behavior only at the granularity the source supports. Do not pool tone zones into an intrinsic target: use comparable midtone or flat patches for displayed intrinsic axes and separate groups for highlight and shadow response. Retain uncertainty for clipping, compression, mixed light, and low legibility.

## Calibration evidence

Treat a possible neutral as a calibration anchor only with visible evidence and an explicit confidence level. Nominal white, gray, black, metallic, or low-chroma regions may still be shifted by light, reflection, exposure, clipping, compression, or grading.

Without a reliable neutral, preserve relative relationships and mark global-cast uncertainty. Translate photographic cast into white-balance/capture language and non-photographic cast into palette/rendering language.

When measurement is justified, use multiple representative patches, robust summaries, profile status, and disclosed display-space assumptions.

Classify auxiliary references as `calibrated-color-target`, `color-managed-reference`, `uncalibrated-vocabulary-chart`, or `photographic-example`. Only the first two establish numeric targets; inconsistent labels remain vocabulary.

Compare multiple target patches with contextual or neutral groups before attributing a color difference to an intrinsic surface or a global cause. Use equal-weight summaries. Shared movement supports global cast/exposure/processing; target-only movement supports a local cause; mixed evidence remains uncertain.

The optional probe accepts analyst-selected normalized regions and never chooses semantic targets:

```bash
python tools/color_probe.py SOURCE --compare RENDER --spec SAMPLING.json
python tools/color_fidelity_eval.py COMPARISON.json --policy POLICY.json
```

Use measurements as diagnostic evidence, never as automatic prompt wording or proof of intrinsic color. Keep exact values out unless the generator supports them and evidence justifies the precision.

Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. Without an explicit tolerance policy, report the decomposition as unscored.

## Cross-layer effect budget

Merge color and tone claims by their shared perceptual effect across causal layers, not only by semantic-slot name.

Give each material effect a source-relative identifier covering region, axis, direction, and aggregate strength. Multiple causal layers pushing one region/axis require independent evidence and one aggregate target.

- Merge unsupported repetition into one owned control.
- Preserve multi-layer color only when every layer and the aggregate result are supported.
- Let hierarchy own relative area, value, chroma, or contrast; let it own hue only when hue contrast is invariant.
- Treat free-floating color or mood words as unowned until assigned to one causal layer.

## Final prompt control ledger

Copy every exact prompt excerpt that changes color/tone into `emitted_controls`. Give an `axis-control` one claim, causal layer, region, axis, and complete effect list. A required intrinsic axis is complete only when it has its own intrinsic axis-control; hierarchy, exposure, or illumination cannot substitute. A justified secondary `compound-control` cannot satisfy a required axis. Cover each claim exactly once and split ambiguous compounds.

When a draft over-pulls an axis, replace or remove its positive control rather than appending an opposing negative.

## Output and diagnosis

When color is primary, emit one compact causal signature before flexible inventory: dominant-region axes, supported global/light shift, and tone response without repeated direction.

When supporting, emit only the smallest relational cue. Diagnose differences as intrinsic, illumination, global cast, exposure/tone curve, processing, or unresolved; keep profile/measurement uncertainty separate from visual judgment.

For render comparisons, report prompt validity, pixel availability, evaluation status, global component, target-local residual, and user judgment separately. An identical-prompt retry is not a color correction. Revise one dominant residual axis at a time only with permission, then freeze a new version.

## Optional negative contribution

Reject only source-likely drift in relative value, chroma, hue direction, global cast, exposure response, tone-zone behavior, or unsupported uniform grading. Do not install fixed color-word blacklists or example-specific desired values.


---

# Included module: `detail.light-form-fidelity`

# Detail: lighting and light-to-form fidelity

## When to load

Load only when illumination, shadow topology, light-induced form, material response, or background spill is an invariant; when the user explicitly requests lighting fidelity; or when a source/render comparison finds a material lighting residual. Do not load merely because an image is lit.

## Three-stage Light/Form Contract

Build a source-relative Light/Form Contract only when illumination materially carries fidelity.

Keep three stages separate:

1. **Observation:** the visible spatial light result.
2. **Actuation:** the smallest literal prompt controls that reproduce that result.
3. **Verification:** what a delivered render actually reproduced.

Treat the observed light-to-form result as evidence and the physical lighting setup as a confidence-rated hypothesis. One image rarely identifies a unique lamp, modifier, fill source, or post-processing path. When the cause is uncertain, preserve the visible result with result-space relations rather than letting an invented rig carry the prompt alone.

## Visible result before rig inference

Record the largest continuous bright and dark masses before small highlights. Map global tonal range, local form contrast, gradient character, edge softness, and the relative visibility of major planes.

Keep global tonal range separate from local form contrast. A wide scene range or dark frame does not require strong internal modeling; a compressed scene may still contain a hard contact edge.

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Describe what the light does to visible form instead of substituting broad mood or quality shorthand.

## Source hypothesis

Separate source geometry, apparent source size, and fill structure. Record source count, direction relative to camera and subject, elevation, apparent angular size, fill or bounce behavior, confidence, and visible evidence only when they matter.

Apparent source size owns shadow-edge softness; it does not automatically own fill level or local contrast. A large off-axis source can remain sculpting, and a small near-axis source can flatten form.

Use `physical-cause` or `physical-plus-result` actuation only with medium- or high-confidence source evidence. With low confidence, use `result-space-only` or keep the hypothesis diagnostic.

## Spatial effects and shadow ownership

For each material region effect, record its role as broad plane, gradient, highlight, shadow, rim, or spill; its source-relative strength; edge character; and evidence. Use semantic region relations rather than fixed coordinates unless exact placement is itself invariant.

Assign each material dark region to cast shadow, self-shadow, contact or occlusion, material response, processing, mixed, or uncertain ownership. Do not promote a small contact shadow into a broad directional-light field, and do not encode an illumination-induced contour as intrinsic form.

Keep material response and background spill separate from source intensity. Matte, glossy, metallic, translucent, woven, and absorbent surfaces under one light may have different highlight width, black level, and texture visibility.

## Pose and geometry dependence

Record whether each light pattern is pose-bound, pose-robust, mixed, or uncertain. When pose is flexible, preserve relational outcomes such as major-plane balance, gradient depth, or light-to-form class while allowing exact highlight coordinates to move. When pose is locked and the evidence is stable, tighter placement may be justified.

## Color and tone handoff

Let the Light/Form Contract own spatial illumination structure and the Color/Tone Contract own displayed color, exposure, and tone response. Illumination color, white balance, intrinsic value or hue, highlight rolloff, and tone-curve compression remain in the shared color/tone path; do not emit the same brightness or contrast pull independently from both contracts.

## Final prompt control ledger

Copy every exact prompt excerpt that changes lighting or light-to-form into the final lighting control ledger. Link it to one emitted claim, one owner among source geometry, fill, local form contrast, shadow topology, material response, or background spill, and its complete effect list. The ledger is an internal trace, not an output template: copy the smallest exact clause that carries the control, omit non-material observations, and do not add headings, repetitions, or prose merely to make the ledger look complete. Split cross-owner compounds and replace overstrong positive controls rather than appending counter-negatives.

When measured comparison is warranted, read `references/lighting-reproduction-evaluation.md`. Use only analyst-selected regions and profiles, retain source/profile uncertainty, and never convert diagnostic measurements directly into prompt wording.

## Output and diagnosis

When lighting is primary, emit one compact causal passage ordered by visible effect: source-supported topology when reliable, fill and local form contrast, decisive shadow ownership, then material or background response. When supporting, use only the smallest relational control.

Diagnose source/render differences as source geometry, apparent size, fill, local form contrast, shadow topology, material response, background spill, exposure or processing, or unresolved. Prompt validation never substitutes for rendered-pixel lighting verification.

## Optional negative contribution

Reject only source-likely lighting drift such as an unsupported key/fill split, wrong shadow owner, exaggerated sculpture or flattening, enlarged specular response, or excess background spill. Do not install fixed lighting words, directions, ratios, subject regions, or numeric targets.


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
- For material color fidelity, keep intrinsic value, chroma, and hue in separate short controls. Treat broad color/finish metaphors as unverified unless response evidence matches the exact model version.

### Visual color conditioning

- When the active image tool accepts referenced images and the request permits reference-conditioned generation, pass the source or an analyst-built color reference through the tool input; keep the standalone production prompt free of references to an absent image.
- When the user asks for text-only generation, do not silently add reference conditioning.
- Do not assume that natural-language color terms map to stable Lab movement across model versions. Use a version-matched response evaluation when available, otherwise report the control as uncalibrated and rely on delivered-pixel evaluation.

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
- Use image, palette, or edit conditioning only when the downstream tool exposes that capability and the request permits it. Keep tool-level reference handling separate from the standalone prompt text.
- Treat any descriptor-response table as model-and-version-specific evaluation evidence, not as a universal color dictionary.
