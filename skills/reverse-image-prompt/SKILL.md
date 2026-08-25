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

## Analysis profile

- `prompt` (default): keep the routed 3–5 lane architecture, but have each lane return only viewer-material P0/P1 evidence, compressed P2 support, and grouped P3/non-material topics. Use one lane wave, one integration, one independent critic, and at most one targeted repair.
- `audited`: use full atomic obligations and v4/v2 ledgers for actual generation evidence, source/render or measured fidelity evaluation, skill evaluation, or an explicit audit request. Do not choose it merely because the image contains a person, readable face, or complicated scene.

The route and report contracts live in `references/analysis-orchestration.md`. A compact report may request audited escalation only for an unresolved P0/P1 conflict that cannot be represented honestly; detail-seeking alone is not a reason.

## Required module loading

Always read the complete Tier 0 core:

- `modules/core.visual-evidence.md`
- `modules/core.frame-coordinates.md`
- `modules/concept.primary-relationship.md`
- `modules/core.fidelity-discipline.md`
- `modules/core.background-color.md`
- `modules/core.pre-emit-gate.md`
- `modules/core.output-contract.md`

Then resolve only the applicable routed modules from `manifest.json` or `modules/_registry.md`. When tools are available, run `tools/route_resolver.py --analysis-route --analysis-profile prompt` unless `audited` is required, so unsupported facets, over-budget module sets, and uncovered lanes fail visibly. Read `references/analysis-orchestration.md` and every selected lane file.

Each lane analyst reads the full contents of its assigned modules before reporting. The main integrator reads Tier 0 plus compact lane reports and only reopens a non-core module for a declared conflict or audit; do not make one context absorb every routed detail module by default. If sibling files cannot be read, use the smallest matching compiled profile; use `SKILL.compiled.all.md` only as the final fallback.

If the target generator is known, read `references/model-adapters.md` and apply only that generator's adapter.

When `detail.color-tone-fidelity` is selected and the request requires measured color fidelity, source/render comparison, actual generation, or controlled color revision, also read `references/color-reproduction-evaluation.md`. Keep ordinary incidental-color prompt extraction on the shorter module path.

When measured surface color must be converted into controlled human-readable classes, an axis-composed surface descriptor, or a friendly appearance label, also read `references/surface-color-language.md`. Use its versioned policy only as source-visible vocabulary translation, never as biological color truth or a demographic proxy. A controlled descriptor deterministically combines current-source axes but does not decide emission. A candidate may be user-supplied, come from an explicitly versioned task vocabulary, or be a provenance-bound aggregate reading of the current source. Do not install a preferred list or choose a label before observing the image.

When `detail.light-form-fidelity` is selected and the request requires measured lighting fidelity, source/render comparison, actual generation, or controlled lighting revision, also read `references/lighting-reproduction-evaluation.md`. Keep ordinary incidental lighting on the shorter medium-module path.

When source-visible lighting must be translated into a compact human-readable composite or a friendly lighting label is considered, also read `references/lighting-language.md`. Classify the lighting axes and global lighting gestalt independently before composing a summary. A candidate may be user-supplied, versioned-vocabulary, or a provenance-bound aggregate reading of the current source. Do not install a preferred named-lighting list or select a label before observing the image.

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
   - When clean-context delegation is available and permitted, run every required lane concurrently as one read-only wave. Give each the same source bytes/hash, raw request, intent, route fingerprint, analysis profile, lane file, assigned modules, and report schema—never another lane's result, a preferred conclusion, a prior prompt/render, or draft prose. Workers do not write files, author the final prompt, generate, or delegate again.
   - Otherwise complete the same lane contracts sequentially, freezing each report before the next and marking `sequential-fallback`; do not claim independent analysis.
   - In `prompt`, each lane details only P0/P1 findings, compresses P2, groups P3/non-material topics, and avoids exhaustive atomic, orientation, appearance, color, or light ledgers. In `audited`, split material findings into independently drifting atomic obligations and bind retained obligations through `source_obligation_ids`.
   - Integrate by owner key and visible effect, not prose concatenation. Give one independent critic the source, route, reports, priority map, and draft without the main transcript. In `prompt`, it checks blocking P0/P1 loss or salience inversion and may name one targeted repair; P2/P3 completeness is advisory and triggers no rerun. Do not rerun successful lanes for more detail. Only a route gap or source/hash mismatch may rerun an affected lane once.

5. Integrate the lane reports with an adaptive hierarchy:
   1. Record the direct, source-supported appeal separately from the render contract. State it plainly in diagnostic mode. When an aggregate appeal term is itself a high-confidence P0/P1 source invariant and omission would materially change the reading, retain it once in the generation prompt as a bounded semantic anchor, immediately followed by its visible causal controls. Otherwise keep it diagnostic or translate it without emission.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Rank cross-lane evidence by viewer effect: `P0 source signature`, `P1 structural identity`, `P2 supporting`, `P3 incidental`. Any source-specific face, skin presentation, space, clothing, pose, topology, light, color, or capture cue may be P0/P1. Record the smallest causal cue set; module count and raw detail do not set prompt weight.
   4. In `prompt`, preserve one macro spatial result plus only decisive P0/P1 placement, viewpoint, pose, topology, and completion relations; group the rest. In `audited`, build `spatial-orientation/v4`, dispose every required axis, run both human counterfactuals, and retain coupled-effect summary coverage exactly as specified by the selected modules and evaluation reference.
   5. Map the few largest coherent image regions by relative area, tonal role, edge contact, legibility, and attention. Record only material component relations: region-to-region or region-to-frame reference, relation kind, source-relative observation, evidence, and role. When one invariant spans multiple regions or visible boundary components, preserve the region-to-region boundary topology instead of collapsing it to a category or one broad edge. When partial visibility matters, record the surviving fragments, cropped or hidden counterparts, and completion risk. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze visible subjects and their image-plane roles. In `prompt`, build only the material human appearance signature: optional non-identifying broad visual and attractiveness priors when default drift is high, decisive local geometry, stable displayed skin axes/finish, hair boundary, expression/gaze, and capture treatment. When attractiveness or another aggregate appearance reading is P0/P1 and source-supported, say it directly once and immediately constrain it with source-specific geometry and treatment. It never replaces those controls or authorizes idealization, retouching, changed crop, makeup, lighting, skin, identity, or factual nationality/ethnicity. In `audited`, additionally create `human-appearance/v2` with full provenance, omission-counterfactual, claim binding, and skin-region handling. Never install a motivating category or surface combination as a default.
   7. Before treating shape, scale, color, surface, or definition as intrinsic, separate effects caused by pose/deformation, perspective, lighting/shadow, material interaction or occlusion, and capture/processing.
   8. When color/tone is material, `prompt` records only the decisive regional axes, displayed result, protected relation, and uncertainty. Build the full Color/Tone Contract only in `audited`, measured color work, or source/render evaluation.
   9. When light/form is material, `prompt` records the decisive visible result before any rig hypothesis and only the protected regional relation. Build the full Light/Form Contract only in `audited`, measured lighting work, or source/render evaluation.
   10. Add only materially important pose, camera/perspective, focus, lighting, background, medium, texture, artifact, UI, and text evidence.

   In `prompt`, a priority map plus compact findings is sufficient. In `audited`, use this sparse internal map and leave irrelevant fields empty rather than completing a checklist:

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
    schema_version: spatial-orientation/v4
    subjects: []        # material orientation-bearing subject id, kind, visibility, major-region id, evidence
    evidence_cues: []   # subject-owned visible cue family, observation, evidence, confounders
    counterfactual_checks: [] # per human: whole orientation plus viewpoint-held residual alignment
    decisions: []       # decomposed dimension, disposition, cue ids, owner, emitted path or bounded non-emission
    coupled_effects: [] # one aggregate control; macro summary first, then only source-visible residual member relations the summary loses
  human_appearance_decisions: [] # human-appearance/v2: frame prominence, fidelity salience, identity context, prior drift/geometry/counterfactual, and skin decision
  candidate_claims: []  # evidence candidates from modules; not automatic prompt sentences
  aggregate_effects: [] # non-color/non-light source-relative effects after cross-slot merge
  emitted_controls: []  # exact final-prompt excerpts for the generic emitted claims
  prior_clusters: []    # broad aesthetic/capture/genre shorthand provenance, source qualification or calibration, and literal decomposition
  color_tone_contract: {}  # when material: observation scope, causal effects, then exact post-draft emitted_controls
  light_form_contract: {}  # when material: observed result, confidence-rated cause, spatial effects, then exact emitted_controls
```

6. Treat selected modules as evidence contributors, not prose entitlements. Merge by owner key, visible effect, direction, region/subject, and causal owner. In `prompt`, retain P0/P1 once, fold P2 into an owned control, and omit P3; only audited work needs complete atomic-obligation and exact-ledger reconciliation. Resolve conflicts and allocate prompt weight in this order:
   1. Visible-evidence and safety limits.
   2. P0 source signature and perceptual proposition.
   3. P1 source-specific appearance, topology, space, information hierarchy, crop, pose, light, color, or capture controls.
   4. P2 support that can be expressed without competing with P0/P1.
   5. Omit P3, flexible inventory, and generic shorthand unless requested.

7. Draft the smallest prompt that carries P0/P1, then only useful P2 support. Put the source-specific signature near the beginning and let order reflect what a viewer notices and would miss first. Use **retain-and-decompose** for material aggregate language: state one evidence-qualified abstract descriptor, then immediately unpack it into owned form, surface, light, color, spatial, hierarchy, or capture controls. Do not use abstraction without controls, and do not assume detailed controls preserve the same global meaning when the omission counterfactual says otherwise. Keep a material human broad or attractiveness prior adjacent to correcting local geometry; it cannot substitute for a different broad appearance, skin presentation, face geometry, scale, expression, space, clothing, or pose. State each aggregate once, remove competing normalization instead of adding counter-negatives, and never let a detailed incidental inventory outweigh the proposition. In `audited`, additionally reconcile every atomic obligation and exact generic, Color/Tone, and Light/Form control ledger according to the selected modules.

8. Apply the profile-aware pre-emit gate. Run one independent compact critic in `prompt`; apply at most one targeted repair and stop. If a P0/P1 conflict remains unresolved without guessing, report the limitation rather than opening another analysis cycle.

9. For actual generation or source/render evaluation, use `audited` and persist the validated bundle, reconciled `plan.json`, exact `prompt.txt` and SHA-256, settings, reference handling, and attempt log. Run `tools/analysis_bundle.py` and `tools/salience_plan.py` before freezing. Ordinary prompt-only extraction needs neither persisted ledgers nor v4 processing.

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
- Do not use a broad label merely because it is familiar or desirable. Retain one when the current source independently supports it as P0/P1, omission causes material drift, provenance is explicit, and adjacent literal controls prevent normalization; otherwise omit it.

## Output selection

Always write the production prompt in English. Match the response language for diagnostic explanation unless the user asks otherwise.

- Always emit `PROMPT:` for generation requests.
- Emit `NEGATIVE PROMPT:` only when the user requests it or the named downstream generator supports a separate negative prompt.
- Emit `RECOMMENDED SETTINGS:` only when requested, when a target generator is known, or when source dimensions require a model-specific target-size explanation.
- For `diagnostic` mode, first name the visible core appeal or perceptual proposition directly, then explain the causal form, surface, lighting, color, hierarchy, spatial, and capture evidence. Distinguish invariants from pose or placement differences that would not destroy the aesthetic. Include a candidate prompt only if useful.
- Keep unsupported, unbounded, or merely preferred appeal language in the explanation layer. A source-visible P0/P1 aggregate descriptor may enter the production prompt once through the retain-and-decompose path; its adjacent controls, source fidelity ceiling, and anti-polish boundaries remain authoritative.
- Essential crop, relationship, occlusion, high-salience aesthetic, and medium constraints must remain in `PROMPT:` even when optional sections are present.

Do not mention the attached/reference image inside the generated prompt.
