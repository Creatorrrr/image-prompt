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

Then resolve only the applicable routed modules from `manifest.json` or `modules/_registry.md`. When tools are available, run `tools/route_resolver.py --analysis-route` so unsupported facets, over-budget module sets, and uncovered analysis lanes fail visibly. Read `references/analysis-orchestration.md` and every selected lane file.

Each lane analyst reads the full contents of its assigned modules before reporting. The main integrator reads Tier 0 plus compact lane reports and only reopens a non-core module for a declared conflict or audit; do not make one context absorb every routed detail module by default. If sibling files cannot be read, use the smallest matching compiled profile; use `SKILL.compiled.all.md` only as the final fallback.

If the target generator is known, read `references/model-adapters.md` and apply only that generator's adapter.

When `detail.color-tone-fidelity` is selected and the request requires measured color fidelity, source/render comparison, actual generation, or controlled color revision, also read `references/color-reproduction-evaluation.md`. Keep ordinary incidental-color prompt extraction on the shorter module path.

When measured surface color must be converted into controlled human-readable classes, an axis-composed surface descriptor, or a friendly appearance label, also read `references/surface-color-language.md`. Use its versioned policy only as source-visible vocabulary translation, never as biological color truth or a demographic proxy. A controlled descriptor deterministically combines current-source axes but does not decide emission. Review friendly-label candidates only when the user or an explicitly versioned task vocabulary supplied them; do not originate candidates from this skill.

When `detail.light-form-fidelity` is selected and the request requires measured lighting fidelity, source/render comparison, actual generation, or controlled lighting revision, also read `references/lighting-reproduction-evaluation.md`. Keep ordinary incidental lighting on the shorter medium-module path.

When source-visible lighting must be translated into a compact human-readable composite or a friendly lighting label is considered, also read `references/lighting-language.md`. Classify the lighting axes before composing a summary. Review friendly-label candidates only when the user or an explicitly versioned task vocabulary supplied them; do not originate named lighting labels from this skill.

When evaluating or revising this skill, also read `references/behavior-evaluation.md`. Do not load that evaluation protocol for an ordinary one-image prompt request.

## Workflow

1. Inspect only the provided image.
   - Use the attached image directly or inspect the exact local file.
   - If no image is available, ask for it.
   - Process multiple images independently unless the user clearly requests a combined prompt.

2. Use visible evidence only.
   - Do not identify people, characters, brands, artists, cameras, lenses, film stocks, or private identities from appearance.
   - Keep uncertainty internal during analysis. In the final generation prompt, describe the visible ambiguity itself with terms such as `indistinct`, `partially obscured`, `low-legibility`, or `soft-edged`; avoid weakening commands with repeated `likely` or `appears`.

3. Build and resolve this preliminary facet map before making domain conclusions:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face-detail, body-form, skin-surface, color-tone, lighting-fidelity, clothing, hands, text-logo, ui, and other visible routed risks
  style: []           # a visible narrow risk only
```

4. Run the routed analysis lanes before building the salience plan.
   - When clean-context delegation is available and permitted, run every required lane concurrently as a separate read-only worker. Give it the same source bytes/hash, raw request, intent, route fingerprint, lane file, assigned modules, and report schema—never another lane's result, a preferred conclusion, a prior prompt/render, or draft prose. Workers do not write files, author the final prompt, generate, or delegate again.
   - Otherwise complete the same lane contracts sequentially, freezing each report before the next and marking `sequential-fallback`; do not claim independent analysis.
   - The main session integrates reports by owner key and causal effect, not prose concatenation. Preserve each material primary finding as primary. Send only unresolved material conflicts to a clean-context adjudicator and retain uncertainty when evidence cannot decide.
   - Give an independent coverage critic the source, route, compact reports, and integrated plan without the main reasoning transcript. Bind retained findings to invariant IDs in the canonical-SHA-256 plan payload, and bind the critic to that plan hash plus every finding/invariant ID. Do not freeze a prompt until the independent critic passes, including under sequential fallback. Persist and validate one `reverse-image-analysis-bundle/v1` for generation or evaluation work.

5. Integrate the lane reports with an adaptive hierarchy:
   1. Record the direct, source-supported appeal separately from the render contract. State it plainly in diagnostic mode, but do not copy evaluative appeal language into a generation prompt; translate it into visible causal controls first.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Separate a small set of aesthetic or structural invariants from dimensions that may vary without losing the proposition. For each invariant, record its semantic slot, hierarchy role, causal origin, source-relative strength, evidence, and one clause owner. Record the smallest causal cue set rather than every visible field. For non-color and non-light invariants, merge shared pulls into source-relative aggregate effects and reconcile each emitted claim with one exact final-prompt control.
   4. Build a `spatial-orientation/v2` ledger for every material orientation-bearing subject. Dispose independently of placement, principal axis, viewpoint axes/foreshortening, and cross-component orientation; for humans also cover torso yaw/pitch/roll, head-to-body yaw/pitch/roll/lateral offset, shoulder slope/depth order, and attention. Link each decision to subject-owned visible cues and explicit confounders, then run a neutral-axial-alignment counterfactual. Material change requires an invariant decomposed pose axis; `flexible` or `not-material` needs a preservation reason; `not-visible` or `uncertain` needs an evidence limit. Coarse legacy labels and frame placement cannot cover orientation. Keep the ledger direction-neutral, preserve supported result-space relations when the physical split is uncertain, and give each invariant one relation-to-control path under one causal owner.
   5. Map the few largest coherent image regions by relative area, tonal role, edge contact, legibility, and attention. Record only material component relations: region-to-region or region-to-frame reference, relation kind, source-relative observation, evidence, and role. When partial visibility matters, record the surviving fragments, cropped or hidden counterparts, and completion risk. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze visible subjects and their image-plane roles. For every routed human, add one `human-appearance/v2` decision keyed to its spatial subject. Record frame prominence separately from fidelity salience; a small or secondary face may still be fidelity-primary. Keep user/trusted identity context separate from a non-identifying source-visible generation approximation—never infer nationality or factual identity from pixels. Dispose the person prior as `emit`, `omit`, or `uncertain` with candidate support, model-default drift risk, local-geometry sufficiency, linked geometry claims, and an omission counterfactual. A readable fidelity-material person may omit the broad anchor only when emitted geometry is sufficient, default drift risk is low, and neutral omission preserves the source reading; otherwise emit supported approximation or retain uncertainty. For material skin, name the Color/Tone region and visible coverage (`exposed`, `through-sheer`, or `mixed`), then decide whether stable descriptor axes emit. Never install a motivating category or surface combination as a default.
   7. Before treating shape, scale, color, surface, or definition as intrinsic, separate effects caused by pose/deformation, perspective, lighting/shadow, material interaction or occlusion, and capture/processing.
   8. When color or tonal behavior is material, build the source-relative Color/Tone Contract from `detail.color-tone-fidelity`: set observation scope; separate regional value, chroma, and hue from illumination, cast, exposure, and processing; keep intrinsic midtone evidence separate from highlight/shadow response; record neutral confidence and cross-layer effects. Every required intrinsic or displayed-tone axis has one same-region effect, claim, and axis control. A displayed-tone control declares `global`, `region`, or `region-group` scope, affected and protected regions, visible evidence, and a prompt anchor; never apply a coarse shadow floor across mixed bright/dark subregions. For controlled surface language, request value depth, chroma, undertone, and optional separately observed finish. Compose stable axes in canonical order even when another axis remains unresolved; omit—not invent—unresolved axes. Boundary-only candidates stay non-emitted until exact model calibration. Friendly labels remain externally supplied and generator/version calibrated.
   9. When illumination, shadow topology, or light-induced form is material, build the source-relative Light/Form Contract from `detail.light-form-fidelity`. Record the visible result before any physical-light hypothesis; separate source geometry, apparent source size, fill, global tonal range, bright-plane coverage, local form contrast, gradient extent, shadow ownership, material response, background spill, and pose dependence. Treat a material source/render change in regional value separation across one surface as light-to-form evidence even when the lighting is otherwise ordinary; name the compared regions with a distinct `reference_region_id` in both observation and aggregate actuation. A low-confidence rig hypothesis remains diagnostic or is paired with result-space controls rather than carrying the prompt alone. Link every emitted lighting effect through one claim and one exact final-prompt control. When compact lighting language is requested, classify displayed key, shadow floor, edge softness, local form contrast, bright-plane coverage, gradient extent, directionality, and fill independently before composing an explanation-only controlled summary or reviewing an externally supplied friendly label.
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
  component_relations: []  # material region/frame relation, evidence, and optional partial-visibility budget
  spatial_orientation_coverage:  # required for routed humans and other material orientation-bearing subjects
    schema_version: spatial-orientation/v2
    subjects: []        # material orientation-bearing subject id, kind, visibility, major-region id, evidence
    evidence_cues: []   # subject-owned visible cue family, observation, evidence, confounders
    neutralization_checks: [] # one per human: neutral-alignment counterfactual and evidence
    decisions: []       # decomposed dimension, disposition, cue ids, owner, emitted path or bounded non-emission
  human_appearance_decisions: [] # human-appearance/v2: frame prominence, fidelity salience, identity context, prior drift/geometry/counterfactual, and skin decision
  candidate_claims: []  # evidence candidates from modules; not automatic prompt sentences
  aggregate_effects: [] # non-color/non-light source-relative effects after cross-slot merge
  emitted_controls: []  # exact final-prompt excerpts for the generic emitted claims
  prior_clusters: []    # broad aesthetic/capture/genre shorthand provenance, calibration, and literal decomposition
  color_tone_contract: {}  # when material: observation scope, causal effects, then exact post-draft emitted_controls
  light_form_contract: {}  # when material: observed result, confidence-rated cause, spatial effects, then exact emitted_controls
```

6. Treat selected modules as evidence contributors, not prose entitlements. Merge candidate claims by semantic slot before drafting; one module owns each emitted slot while other modules may strengthen its evidence. For spatial decisions, merge repeated ownership by `control_axis_id` across camera, pose, face, body, clothing, composition, and lighting; the same causal axis cannot survive under differently named slots. For form, surface, sharpness, hierarchy, topology, and information, also merge claims that push the same source-relative axis, direction, regions, and relations; one aggregate effect has one emitted owner even when several modules support it. For material color and tone, merge claims by shared perceptual effect across intrinsic surface, illumination, global cast, exposure, processing, and hierarchy even when their semantic-slot names differ. For material lighting, merge effects across source geometry, fill, local form contrast, shadow topology, material response, and background spill. Let the generic, Light/Form, and Color/Tone ledgers have disjoint claims and exact prompt excerpts. Resolve conflicts and allocate prompt weight using this priority:
   1. Visible-evidence and safety limits.
   2. Primary perceptual proposition, dominant fidelity axis, and invariants.
   3. The mode-leading evidence: topology for relationship-led, causal appearance signature for appearance-led, information hierarchy for information-led, or the named co-primary pair for mixed.
   4. Frame ratio, crop, major zones, boundary sides, visibility, and completion budgets.
   5. Subject, medium, camera, lighting, focus, artifact, background, and color fidelity that supports the proposition.
   6. Flexible pose or placement detail, secondary elements, and generic shorthand.

7. Draft the smallest prompt that carries every invariant and concept-critical constraint. Let its order follow the dominant fidelity axis. If the source look is high-salience, place one compact Aesthetic Causal Signature near the beginning; if neutral, use only one or two ordinary cues. Translate broad appeal words into form, surface, light, color, hierarchy, or spatial mechanisms. A broad aesthetic/capture/genre shorthand may emit only through a provenance-bearing prior cluster that points to its already-owned causal controls; uncalibrated shorthand stays diagnostic. Normally express a semantic slot once and add at most one source-supported drift boundary for a genuinely high-risk failure. Emit only spatial/orientation decisions marked `invariant`, once per `control_axis_id`; do not leak controls from non-invariant decisions. Placement controls only position and frame share. Put material human pose after camera/scale and before face, hair, and clothing; later appearance inherits rather than replaces it. Emit a person prior or skin descriptor only from its explicit human-appearance decision. After drafting, copy each exact non-color/non-light control into the generic `emitted_controls` ledger and reconcile it with one emitted claim and its complete aggregate-effect set. Reconcile every material placement or orientation clause with the source-relative component and pose relations; remove unsupported axial normalization instead of adding a negative counterweight. For material color or tone, assign every emitted direction to one causal layer and one aggregate effect budget; do not let hierarchy repeat a surface hue unless hue contrast itself is invariant. Give each required intrinsic value, chroma, hue, or displayed-tone axis its own literal axis-control. An emitted axis-composed descriptor is one wrapper containing only its exact stable owned excerpts; optional finish uses a separately owned generic surface control. Write literal axes before any externally supplied friendly label, retained at most once as a compatible model-calibrated summary. After drafting, copy exact color-changing excerpts into the Color/Tone ledger and reconcile each with one claim, causal layer, region, axis, scope, and complete effect list. For material lighting, copy every exact lighting-changing excerpt into the Light/Form Contract's `emitted_controls`; keep source geometry, fill, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, and background spill separately owned, and preserve result-space controls when the physical cause is uncertain. Literal lighting controls remain authoritative. Retain an externally sourced friendly lighting label at most once and only when it is compatible, generator/version calibrated, and immediately unpacked by its already-owned literal controls; never emit the explanation-only controlled summary as an extra control. Split or replace unowned, cross-axis, and multi-layer compounds. Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Give each major component one relation and each inversion-prone interaction one relation clause, but do not let flexible pose coordinates or secondary details outrank the primary proposition.

8. Apply the pre-emit gate and report prompt-only limits honestly.

9. For actual generation or source/render evaluation, persist the validated analysis bundle, reconciled `plan.json`, exact `prompt.txt` and SHA-256, a settings record with source frame, target size, size-binding status, and reference handling, plus an attempt log. Run `python tools/analysis_bundle.py ANALYSIS_BUNDLE.json` and `python tools/salience_plan.py PLAN.json --prompt PROMPT.txt` immediately before freezing the prompt. Use `tools/size_adapter.py` for a supported target and delivered-frame evidence; `auto`, unsupported, or unbound size remains unscored for composition-frame delivery. Ordinary prompt-only extraction does not require persisted artifacts.

## Routing rules

- Always load Tier 0.
- Select at least one subject and one medium; use the generic/unspecified fallbacks only when evidence is unclear.
- Load every visible Tier 1 relationship module, including both photographic and non-photographic medium modules for genuine mixed media.
- Load Tier 3 and Tier 4 modules only for visible, material risks.
- For a prominent or clearly readable human face, add `face-detail`; for a small, blurred, shadowed, or heavily occluded face, keep only scale-appropriate human evidence and do not invent micro-features.
- Add a human body-form risk only when visible proportion, contour/tissue, muscle definition, skin surface, tension, or body-region hierarchy is first-order. Do not route it merely because a person or torso is visible.
- Add `detail.color-tone-fidelity` only when color or tonal behavior is first-order, the user explicitly prioritizes tone fidelity, or confusion among intrinsic color, illumination, cast, exposure, and processing would materially change the image. Do not route it for ordinary incidental color.
- Add `detail.light-form-fidelity` only when lighting, shadow topology, light-induced form, material response, or background spill is first-order; when the user explicitly prioritizes lighting fidelity; or when a source/render comparison identifies lighting as a material residual, including lost regional value separation across the same material. Do not route it for ordinary incidental lighting already handled by the selected medium module.
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
