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


---

# Distributed analysis orchestration reference

# Distributed analysis orchestration

Use this contract after facet/module routing and before prompt drafting. Domain evidence still comes from the selected `modules/*.md`; lane files define independent ownership and reporting.

## 1. Choose an analysis profile

Resolve `reverse-image-analysis-route/v2` with `tools/route_resolver.py --analysis-route --analysis-profile PROFILE`.

- `prompt` is the default for an ordinary one-image prompt or diagnosis. It preserves separate lane analysts and an independent critic, but collects only viewer-material evidence.
- `audited` is for actual source/render evaluation, measured fidelity work, skill evaluation, or an explicit request for a full evidence ledger. It retains `reverse-image-analysis-lane-report/v2`, `spatial-orientation/v4`, `human-appearance/v2`, and `reverse-image-analysis-bundle/v2`.

Do not enter `audited` merely because a human, readable face, complicated scene, or routed detail module is present. Escalate only when the task requires audited evidence or the compact profile reports one unresolved P0/P1 conflict that cannot be represented honestly.

Both profiles use the same routed set of three to five material lanes for an ordinary image. `lane.global-composition` is always required. A non-core module that reaches no lane is a visible route failure.

## 2. Run one isolated lane wave

When clean-context delegation is available and permitted, run all required lanes concurrently. Each read-only worker receives only:

- the same source artifact and SHA-256;
- raw request and resolved intent;
- route fingerprint, analysis profile, and execution budget;
- its lane file and complete route-assigned modules; and
- the profile's report schema.

Do not pass another lane's result, a preferred conclusion, previous prompt/render, or draft prose. Workers do not write files, generate, author the final prompt, or delegate again.

If delegation is unavailable, freeze each report before starting the next and mark `sequential-fallback`; do not claim independence. Do not rerun a successful lane to seek more detail. A missing or malformed report may be retried once for that lane only; source/hash mismatch or an actual route gap may restart the affected route once.

## 3. Compact prompt report

In `prompt`, each lane returns `reverse-image-analysis-lane-report/compact-v1`:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/compact-v1",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 16}],
  "primary_read": "one sentence naming what this lane says the viewer must retain",
  "material_findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "viewer_priority": "P0",
      "observation": "source-relative visible result",
      "source_evidence": ["decisive visible cue"],
      "confidence": "medium",
      "change_counterfactual": "what visibly becomes a different image if changed",
      "default_drift_risk": "high",
      "control_requirement": "causal requirement, not final prompt prose",
      "aggregate_descriptor_candidate": {
        "phrase": "optional current-source aggregate reading",
        "candidate_source": {
          "kind": "source-visible-approximation",
          "reference": "current source hash or observation id"
        },
        "confidence": "high",
        "viewer_priority": "P0",
        "omission_counterfactual": "material-drift",
        "decomposition_requirements": ["owned visible control requirement"]
      }
    }
  ],
  "supporting_findings": [],
  "grouped_non_material_topics": [
    {"topics": ["intrinsic-induced-confounds"], "reason": "not viewer-material here"}
  ],
  "uncertainties": [],
  "handoffs": [],
  "conflicts": [],
  "escalation": {"required": false, "reason": ""}
}
```

Use the smallest causally sufficient evidence set. Detail P0 and P1; compress P2 into a mergeable supporting cue; group P3 and other non-material required topics with one evidence-based reason. Do not enumerate hidden, unreadable, or non-material axes merely to complete a checklist. Run a counterfactual only when it decides P0/P1 materiality or resolves a high default-drift risk.

`aggregate_descriptor_candidate` is optional and case-bound. Include it only when the phrase itself carries a P0/P1 gestalt not preserved by detail alone; its decomposition requirements remain separately owned. Never fill it from a preferred vocabulary. Split a compact finding only when two visible results can drift independently and both are P0/P1. Otherwise keep the causal result together. Compact reports do not create exhaustive atomic obligations, full color/light ledgers, `spatial-orientation/v4`, or `human-appearance/v2`.

## 4. Viewer-first integration

The main session integrates by owner key and visible effect, never by concatenating lane prose. Before writing the prompt, assign one cross-lane priority:

- `P0 source signature`: changing it makes a viewer read a materially different image. Put its causal controls first.
- `P1 structural identity`: major subject gestalt, face/form/surface, space, clothing silhouette, pose/action, topology, lighting, color, or capture evidence needed to preserve that signature.
- `P2 supporting`: recognizable but safely compressed into an existing clause or one later cue.
- `P3 incidental`: omit unless the user explicitly asks for it.

Priority is counterfactual and source-specific, not category-specific. Face, skin presentation, room geometry, garment silhouette, pose, camera distance, or any other field can outrank the rest. Conversely, a visible field can remain P2/P3 even when a routed module analyzed it.

For a material human, build only the compact appearance signature needed by the image:

- one non-identifying broad visual generation prior only when source evidence supports it and omission creates high model-default drift;
- decisive local face or body geometry;
- displayed skin value/chroma/undertone/finish only where visibly stable and material;
- hair mass or boundary, expression/gaze, and capture treatment only when they carry P0/P1.

A broad prior never states factual nationality or exact ethnicity and never acts as likeness by itself. Keep it immediately adjacent to source-specific geometry, which remains authoritative. `beautiful`, `attractive`, `model-like`, or a similar aggregate appearance reading may be its own P0/P1 finding when high-confidence current-source evidence and a material-drift omission counterfactual support it. Retain the aggregate once before its decomposition; it cannot replace or override broad appearance, geometry, skin presentation, scale, expression, or capture treatment, and it grants no extra polish.

Draft the prompt from P0 to P2. Give each P0/P1 effect one causal owner and one prompt control, merge compatible P2 evidence into those clauses, and omit P3. Specificity follows viewer impact: do not give a long incidental inventory enough repetition to overpower the source signature.

## 5. Compact independent critic and repair budget

Give one independent read-only critic the source/hash, route, compact reports, priority map, and draft prompt without the main reasoning transcript. It checks only blocking visual failures:

- lost or contradicted P0/P1 evidence;
- a generic attractiveness, mood, or style prior replacing source-specific appearance instead of leading an owned decomposition;
- unsupported broad-person inference;
- source-significant face/skin, space, clothing, pose, topology, light, or color drift;
- a P2/P3 detail outranking a P0/P1 control; or
- a route/source mismatch.

The critic returns `pass`, `targeted-repair`, or `blocked`, with exact affected finding/control IDs. Advisories about P2/P3 completeness do not trigger work. Apply at most one local repair to the named controls; do not rerun successful lanes or restart integration. If one repair cannot resolve a P0/P1 uncertainty without guessing, keep the uncertainty visible in diagnostic mode or tell the user the fidelity limit. Do not iterate toward v2, v3, or v4 merely to make the analysis look complete.

When runtime telemetry is available, the orchestrator records route, lane-wall, integration, critic, and repair durations plus report sizes. Lane workers do not spend analysis time estimating their own timing.

## 6. Audited profile

In `audited`, each lane returns `reverse-image-analysis-lane-report/v2`. Every required topic is individually disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`; each material finding is split into independently drifting atomic visible-result obligations. Integrate them into `reverse-image-analysis-bundle/v2`, dispose every finding and obligation once, bind retained obligations through `source_obligation_ids`, and preserve role and causal ownership.

Use `spatial-orientation/v4` and both human orientation counterfactuals only here. Use `human-appearance/v2` and full Color/Tone or Light/Form ledgers only here or when the user explicitly requests those measured contracts. Existing validators remain authoritative:

```bash
python tools/analysis_bundle.py ANALYSIS_BUNDLE.json
python tools/salience_plan.py PLAN.json --prompt PROMPT.txt
```

The audited critic binds to source, route, reports, obligations, and plan hash. It may request one targeted integration repair and one verification pass. Only a route gap or source-artifact mismatch may rerun an affected lane. If the repair budget is exhausted, report `blocked`; never start an open-ended refinement loop.

## 7. Evidence boundary

Route validity, package validity, lane coverage, prompt behavior, delivered pixels, and user judgment are separate evidence layers. A compact prompt can be useful without claiming audited completeness, and an audited bundle can be valid without proving visual fidelity.


---

# Included analysis lane: `lane.global-composition`

# Analysis lane: global composition

## Role

Own the image-wide proposition, frame, crop, major-region hierarchy, and dominant fidelity mode. Apply the assigned core modules; this file does not redefine their visual rules.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and the route-assigned modules. Do not receive another lane's findings or a draft prompt.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`: one primary viewer read, only P0/P1 proposition, frame/crop, and major-region findings, compact P2 support, and grouped P3/non-material topics. Use a change counterfactual only to decide whether a region or crop is identity-bearing. Propose controls, not prompt prose.

In `audited`, return `reverse-image-analysis-lane-report/v2` and split material frame, crop, and region-hierarchy results into independently drifting atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth, review every assigned module, retain source uncertainty, and report cross-lane dependencies without resolving them by assumption. Do not itemize minor scenery merely because it is visible.


---

# Included analysis lane: `lane.spatial-topology`

# Analysis lane: spatial topology

## Role

Own source-visible orientation, component topology, contact, support, occlusion, and completion risk. Use the assigned modules as the sole domain instructions.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive appearance conclusions or prompt wording.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. First decide whether orientation or topology is P0/P1. If it is, report the macro visible result and only the decisive placement, direction, depth, contact, boundary, occlusion, or completion relations needed to preserve it. Group non-material axes; do not enumerate a fixed orientation checklist. Hand off appearance, color, and capture questions.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting spatial results into atomic obligations, and retain confounded result directions.

## Completion gate

Dispose every required topic at the profile's depth. In `prompt`, run at most the counterfactual needed to establish P0/P1 materiality; a concise macro pose or topology plus decisive residual relations is sufficient. In `audited`, require whole-orientation and viewpoint-held residual-alignment counterfactuals and full coupled-obligation handling. Hair, garment, and boundaries may corroborate but never replace subject geometry. Never normalize ambiguous axes or complete hidden structure.


---

# Included analysis lane: `lane.subject-appearance`

# Analysis lane: subject appearance

## Role

Own visible subject form and non-identifying appearance evidence. For humans, separate frame prominence from fidelity salience, identity context from generation approximation, and intrinsic surface evidence from induced effects.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred demographic label, another lane's conclusions, or draft prompt prose.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. Build a source-specific appearance signature from only P0/P1 evidence: optional non-identifying broad visual prior, decisive face/body geometry, material displayed skin axes, hair boundary, expression/gaze, and capture-sensitive appearance. Include a broad prior only when supported and omission has high model-default drift; keep it distinct from factual nationality or exact ethnicity. Hand color/light attribution to its lane.

`beautiful`, `attractive`, `model-like`, or another aggregate appearance reading may be reported as a separate P0/P1 candidate when source evidence and the omission counterfactual support it. It must remain distinct from, and cannot satisfy or replace, the broad prior, geometry, skin, scale, expression, or capture findings. In `audited`, return `reverse-image-analysis-lane-report/v2` and split independently drifting aggregate, prior, geometry, occlusion, and surface results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. A small or secondary subject may still be fidelity-primary. Unsupported identity inference fails. In `prompt`, a supported broad prior may be omitted when local geometry is sufficient and default drift is low; record residual uncertainty instead of performing repeated omission tests.


---

# Included analysis lane: `lane.color-light-material`

# Analysis lane: color, light, and material

## Role

Own causal separation of intrinsic color, displayed tone, illumination, shadow, and material response. Apply the routed fidelity modules rather than duplicating their rules here.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Receive subject/region identifiers as neutral handoff keys, not appearance conclusions.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1`. Report only P0/P1 regional color, displayed-tone, light-to-form, or material-response effects and the minimum protected relation needed to avoid drift. Prefer stable visible results when physical attribution is uncertain; group non-material axes instead of completing full ledgers.

In `audited`, return `reverse-image-analysis-lane-report/v2`, keep region/protected scope explicit, and split material intrinsic color, displayed tone, light, shadow, response, and cross-region results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not pool mixed regions, convert displayed skin color into biological truth, or let a global control erase a protected P0/P1 relation.


---

# Included analysis lane: `lane.medium-aesthetic-capture`

# Analysis lane: medium, aesthetic, and capture

## Role

Own medium/process evidence, capture character, production aesthetic, and meaningful artifacts. Keep regional or cultural portrait aesthetics separate from a person's identity.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred genre label or a draft prompt.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1` with the fidelity ceiling and only the P0/P1 capture or production cues whose change would alter the viewer's read. Compress P2 artifacts and omit P3 inventory. A broad aesthetic or mood reading may become one provenance-bound aggregate candidate when it is high-confidence P0/P1 evidence and omission causes material drift; report its literal causal controls separately so integration can retain-and-decompose it.

In `audited`, return `reverse-image-analysis-lane-report/v2` and decompose a material aesthetic candidate into independently drifting visible obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not upgrade fidelity, infer an artist/camera, or use a genre, quality, mood, or beauty label as a substitute for visible controls. Do not erase a material aggregate reading merely because the controls have been decomposed.


---

# Included analysis lane: `lane.information-layout`

# Analysis lane: information layout

## Role

Own information hierarchy, reading order, text/UI legibility, and nested frame boundaries. Existing routed modules remain the domain source of truth.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive other lane conclusions or final wording.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v1` with only P0/P1 container hierarchy, reading order, legibility, or nested-boundary findings; compress supporting structure and group unreadable or incidental detail. In `audited`, return `reverse-image-analysis-lane-report/v2` with atomic layout obligations. Never transcribe unreadable content or write final prose.

## Completion gate

Dispose every required topic at the profile's depth. Preserve low legibility and distinguish the source image frame from screens, documents, or embedded panels.


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
- Before treating an observed contour, scale, color, surface, or definition as intrinsic, separate effects caused by pose or deformation, perspective, lighting or shadow, material interaction or occlusion, and capture or processing.
- In the default `prompt` profile, keep only P0/P1 viewer-material results, compress P2 support, and group P3 or non-material evidence instead of enumerating it.
- In `audited`, preserve independently drifting material results as atomic obligations; uncertain attribution never erases a supported direction.

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
- Describe which evidence occupies the frame zones, including any material source-visible axis offset.

## Major-region hierarchy

Map the few largest visually coherent regions as a major-region hierarchy before local detail. Record relative area, role, attention, legibility, and frame contact without fixed percentages.

Preserve region-share hierarchy when flexible pose, viewpoint, or placement changes; exact coordinates may move.

## Spatial language

In `prompt`, first decide whether spatial orientation is P0/P1. If so, preserve one macro visible result plus only decisive placement, viewpoint, pose, and cross-component relations; group non-material axes. Placement proves no orientation. Centered may be oblique and offset may be frontal.

In `audited`, disposition every material placement, principal axis, viewpoint, cross-component orientation, and human pose axis. For humans test whole orientation, then residual pose with viewpoint fixed; merge jointly material weak axes once.

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
2. Record the direct appeal reading separately before deciding actuation. In generation, retain it once only as high-confidence P0/P1 source evidence whose omission causes material drift; immediately follow with visible mechanisms. Otherwise emit only the mechanisms.
3. The dominant fidelity axis and smallest causal cue set.
4. Rank visible effects by a viewer counterfactual: `P0` changes the source signature, `P1` changes structural identity, `P2` supports the read, and `P3` is incidental. Face, skin presentation, space, clothing, pose, topology, light, color, or capture may occupy any level; category and module count do not set priority.
5. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it. In `prompt`, retain only the smallest P0/P1 causal set and merge P2 support. In `audited`, build the full ledger. Build an invariant salience ledger. Bind retained atomic obligations.
6. For relationship-led or mixed images, the stable zones and each critical pair's side, containment, contact, support, depth, occlusion, and boundary crossing.
7. One to three likely failures, including a category default replacing source-specific evidence.

Merge synonymous non-color and non-light pulls into one source-relative aggregate effect with one claim and control.

Build a sparse relation graph and group elements sharing a relation. Keep ordinary premises ordinary. In appearance-led images, do not let minor coordinates or generic attractiveness outrank source-specific appearance; in information-led images, prioritize layout and legibility.

Distinguish image-plane overlap from scene-space containment, contact, and support. When geometry could invert, record contact, weight support, and the relevant boundary or support plane; use object- or scene-relative zones when screen directions are ambiguous.

For special relationships, use this compact Concept Spec:

- Name each concept-critical element, its image-plane role, and its relationship.
- Record join, overlap, contact, containment, hidden or partial regions, boundary side, support, layer order, scale, and coherence ceiling.

## Prompt contribution

Contribute evidence candidates, not guaranteed prose. The central output contract merges candidates by semantic slot and assigns one clause owner. Write a construction recipe, not a prop list; lead with P0, then P1, and spend words only in proportion to viewer impact.

Give each major component or coherent group at least one explicit spatial relation to another major component or stable reference zone. Multi-region form/topology retains its material region-to-region boundary.

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

An evaluative term is neither automatically valid nor disposable. When an aggregate appeal reading is high-confidence P0/P1 source evidence and its omission causes material drift, retain it once and immediately constrain it with visible controls. Otherwise keep it diagnostic.

Build a sparse Aesthetic Causal Signature from only the form, surface, light-to-form, color, sharpness, and hierarchy axes that materially create the image's perceptual proposition.

- **Form:** silhouette, proportion, contour rhythm, tension, softness, or rigidity.
- **Surface:** texture, finish, translucency, sheen, grain, or processing.
- **Light-to-form:** flattening, soft revelation, separation, or hard sculpture.
- **Color/tone:** palette, cast, saturation, range, and local contrast.
- **Hierarchy:** dominant shapes, material roles, subject/environment balance, and first attention.

Select only causal axes. Use three to six mutually supporting look anchors only when the source aesthetic is high-salience; otherwise use one or two ordinary cues. Describe ambiguity instead of invoking presets.

Treat descriptive detail and rendered sharpness as independent controls. Detail must not raise sharpness, scale, polish, or priority.

For a material evaluative or mood term, retain the aggregate once, then immediately unpack visible mechanisms. Neither abstraction nor detail substitutes for the other.

Treat a broad color descriptor as a hypothesis about one causal layer, not as shorthand for hue, value, chroma, lighting, mood, and processing at once. Replace overload with source-supported axes.

Decompose an appearance metaphor into observable color axes, surface behavior, and illumination before using it once as a non-directional summary. Current-source emission requires provenance, high/medium confidence, P0/P1 priority, material-drift omission, compatibility, and immediate owned controls. Calibration remains separate effectiveness evidence; the descriptor adds no second direction.

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

Always. Apply immediately before the final answer as a rewrite pass, not an appended checklist.

## Viewer-first gate

- Confirm that `PROMPT:` contains the primary visual concept and that every P0/P1 effect has one early causal control.
- Merge candidate claims by semantic slot before writing prose; each emitted slot has one clause owner.
- Merge P2 into an owned control or one short supporting clause; delete P3 unless requested.
- Check whether a secondary element receives more words than its visible importance supports; compress it when it competes with P0/P1.
- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. Generic beauty, style, quality, or demographic-looking shorthand cannot replace source-specific appearance, geometry, skin presentation, space, clothing, pose, light, or color.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight.
- Audit coordinate contradictions before emitting. In `prompt`, preserve only the P0/P1 macro spatial result and decisive relations; in `audited`, validate the full spatial contract.
- For a material human, keep any non-identifying broad prior contiguous with correcting local geometry. Beauty and skin wording cannot act as likeness by themselves.
- Retained aggregate descriptors require provenance, P0/P1 materiality, and adjacent owned decomposition. Remove free-floating labels, not qualified anchors whose controls are detailed.

## Causal ownership

- Audit shared perceptual effects across semantic slots, causal layers, paragraphs, negatives, and settings.
- Keep form, surface, light, color, material, and hierarchy causally consistent; do not encode induced effects as intrinsic.
- Assign every appearance-changing color or tone phrase to one causal layer. A qualified aggregate may lead its axes once; rewrite or remove other free-floating mood or color adjectives.
- Split an ambiguous color phrase when one modifier could silently control intrinsic surface, illumination, exposure, or processing at the same time.
- Give an axis-control one region and one perceptual axis. Split a compound that would silently change several material axes.
- Assign every lighting-changing phrase to one Light/Form owner. Keep the visible result authoritative when physical cause is uncertain.
- Keep global tonal range and local form contrast as separate effects.
- Give every material shadow event a source-supported owner or mark it mixed or uncertain.

## Audited-only ledger checks

Apply this section only in `audited`, measured fidelity, or source/render evaluation:

- For a material color or tone effect, verify one aggregate source-relative target and the evidence for every emitted intrinsic, illumination, global-cast, exposure, processing, or hierarchy contribution.
- For every required intrinsic value, chroma, or hue observation, trace one uninterrupted path from region axis to same-region/same-axis aggregate effect, emitted claim, and intrinsic axis-control.
- Reconcile every exact color-changing excerpt in the final prompt with one emitted claim, one causal layer, and its complete aggregate effect budget.
- For material lighting, verify one source-relative Light/Form target and evidence for every emitted source-geometry, fill, local-form-contrast, shadow-topology, material-response, or background-spill contribution.
- Reconcile every exact lighting-changing excerpt with one emitted claim, one owner, and its complete lighting-effect list.
- Validate routed human appearance decisions, spatial counterfactuals, obligation binding, and specialized-ledger separation with the audited tools before generation evidence is frozen.

## Final checks

- Preserve major-region area and attention order, partial visibility, fidelity ceiling, and scale-appropriate detail.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions.
- Confirm that later face, hair, garment, background, color, or lighting language does not neutralize an earlier P0/P1 relation.
- Report prompt-only limits honestly. Package validity, prompt quality, pixels, and user judgment remain separate.
- If the prompt reads as a checklist, rewrite around the proposition and its smallest causal cue set.


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

Write a standalone English prompt ordered first by viewer importance, then by the dominant fidelity axis:

- Put P0 source-signature controls first, followed by P1 structural identity.
- Merge P2 support into an owned clause or one short later cue; omit P3 unless the user requests it.

- Begin with frame shape, medium, fidelity ceiling, and the perceptual proposition.
- **Relationship-led:** crop, major zones, topology, interaction, then appearance.
- **Appearance-led:** causal form, surface, light, color, hierarchy, then flexible pose or inventory.
- **Information-led:** layout, reading order, hierarchy, legibility, then decoration.
- **Mixed:** name co-primary invariants and only cues showing their dependency.
- Finish with supporting subject, capture, background, artifact, and drift controls.

Selected modules contribute evidence candidates, not mandatory prose. Merge them by semantic slot; module count and analysis detail must not determine prompt length.

Assign one clause owner to each emitted semantic slot. State its affirmative target once; add only a distinct high-risk boundary.

Emit each generic effect once. A coupled effect uses one control: its macro summary first, then only `partial` or `lost` member residuals.

Placement controls position, scale, and frame share. Order camera/scale, material pose, then contiguous person prior/local geometry and remaining appearance.

When color or tone is material, assign each emitted control to one causal layer and one perceptual effect budget. Use source-relative value, chroma, and hue; keep intrinsic surface, illumination, global cast, exposure, processing, and hierarchy consistent. Require the full ledger only in `audited`.

In `prompt`, place one compact regional color/tone result early only when P0/P1. A source-evidence-qualified surface descriptor may lead its literal axes once without adding a second direction. In `audited`, trace exact controls.

When lighting is material, assign each emitted control to one Light/Form owner and source-relative effect budget. In `prompt`, state the decisive visible result and protected relation; in `audited`, keep source geometry, apparent size, fill, local contrast, shadow topology, material response, and spill separately ledgered. Generic adjectives cannot own several.

Lead with the visible result; add physical cause only at supported confidence. Keep spatial illumination separate from displayed color/tone. A qualified user or current-source descriptor may lead one literal-control block; calibration remains effectiveness evidence.

Use compact blocks without a fixed cap; every clause adds a control. Keep essential spatial axes distinct and affirmative.

For a high-salience look, put one supported source-specific Appearance or Aesthetic Signature before inventory; for a neutral look, use one or two cues. Preserve only material major-region area, role, edge contact, legibility, and attention.

When face likeness is selected, order one scale-appropriate passage as optional broad visual or attractiveness prior, correcting geometry, material skin, hair, expression, and capture. An attractiveness anchor may carry the overall reading once but cannot replace geometry or raise polish. Retain provenance and geometry evidence.

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

# Included module: `detail.color-tone-fidelity`

# Detail: color and tone fidelity

## When to load

Load only when color/tone is an invariant, the user requests fidelity, or a causal mix-up could materially change the image. Do not load merely because an image contains color.

## Three-stage Color/Tone Contract

In `prompt`, state only the P0/P1 displayed result: named region or region group, source-relative value/chroma/hue or tone-response direction, protected relation, and uncertainty. Do not build a full axis, actuation, or verification ledger; merge P2 color into an owned clause and omit P3.

In `audited`, measured color work, or source/render evaluation: Build a source-relative Color/Tone Contract only when color or tonal behavior materially carries fidelity.

Keep three stages separate:

1. **Observation:** what the source visibly supports.
2. **Actuation:** which literal prompt control carries each material source axis to the named generator.
3. **Verification:** what a delivered render actually reproduced. Prompt validation never substitutes for rendered-pixel verification.

Set scope to `source-visible`, `color-managed` only with trustworthy calibration evidence, or `user-specified` for an explicit external target. Treat sampled pixels as source-visible display color, not proof of biological, material, or scene-referred true color. For human surfaces, use observable evidence rather than demographic identity labels.

For each important region:

- separate value/lightness, chroma/saturation, and hue family/undertone;
- record role, relation to another region, confidence, and uncertainty;
- separate intrinsic surface from illumination, global cast/palette, exposure/tone curve, and processing.

In the full contract: For every intrinsic value, chroma, or hue axis, record `role`, `evidence_scope`, and `emission`. Use `required` only when the axis materially needs a final prompt control. Use `diagnostic-only` with a concrete non-emission reason when an axis is low-confidence, incidental, or already unsupported at prompt precision. Link every required intrinsic axis to exactly one same-region, same-axis aggregate effect.

Assign every material color or tone observation to intrinsic surface, illumination, global cast or palette shift, exposure or tone curve, or processing.

Describe important regions through separate value, chroma, and hue observations plus source-visible relations to other regions. Do not let one broad adjective silently determine all three axes.

Decompose an appearance metaphor into value, chroma, hue, surface, and light response. Status is `explanation-only`, `unverified`, `source-evidence-qualified`, or `model-calibrated`. Source qualification requires current-source provenance, high/medium confidence, P0/P1 priority, `material-drift` omission, compatibility, and immediate literal decomposition. Model calibration adds exact response evidence. Treat calibration as control-effectiveness evidence, not description permission.

When measured surface color needs natural language, read `references/surface-color-language.md`. Classify value depth, chroma, undertone, and optional separately observed finish independently. Compose stable axes in canonical order, omitting unresolved axes without invention. A boundary-only result stays diagnostic until exact model calibration. The descriptor is not a friendly label and may emit only as one wrapper containing the exact included axis-control excerpts.

Friendly labels remain separate from axis composition. Review user, versioned-vocabulary, or provenance-bound current-source candidates. Current-source emission requires qualification and immediate decomposition; calibration independently establishes response reliability. Never map axes to demographic identity.

Map highlight, midtone, shadow, or flat-field behavior only at the granularity the source supports. Do not pool tone zones into an intrinsic target: use comparable midtone or flat patches for displayed intrinsic axes and separate groups for highlight and shadow response. Retain uncertainty for clipping, compression, mixed light, and low legibility.

Record displayed key level, shadow floor, highlight rolloff, and microcontrast as separate tone-response axes. Give every Color/Tone region a non-trivial prompt anchor. Each required control declares global, region, or declared region-group scope, affected/protected regions, evidence, and reuses the declared exact anchor in its prompt excerpt. Split mixed bright/dark coarse regions before applying one shadow floor. Light/Form separately owns bright-plane coverage and spatial gradients.

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
python tools/color_language.py OBSERVATION.json --policy references/surface-color-language-policy.json --compose-for "<analyst-supplied-surface>" --candidates LABELS.json
```

Use measurements as diagnostic evidence, never as proof of intrinsic color. The language tool can return reviewable axes, a deterministic descriptor candidate, and label compatibility; the plan still decides emission and supplies semantic region ownership. Keep exact values out unless the generator supports them and evidence justifies the precision.

Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. Without an explicit tolerance policy, report the decomposition as unscored.

## Cross-layer effect budget

Merge color and tone claims by their shared perceptual effect across causal layers, not only by semantic-slot name.

Give each material effect a source-relative identifier covering region, axis, direction, and aggregate strength. Multiple causal layers pushing one region/axis require independent evidence and one aggregate target.

- Merge unsupported repetition into one owned control.
- Preserve multi-layer color only when every layer and the aggregate result are supported.
- Let hierarchy own relative area, value, chroma, or contrast; let it own hue only when hue contrast is invariant.
- Treat free-floating color or mood words as unowned until assigned to one causal layer.

## Final prompt control ledger

In `audited`, copy every color/tone excerpt into `emitted_controls` with one claim, layer, region, axis, and effect list. Overlapping value/tone controls list `protected_light_effect_ids` and follow the primary light result. A required intrinsic axis needs its own intrinsic axis-control; compounds cannot satisfy it. In `prompt`, ownership and protected relations are sufficient without duplicating the excerpt in a ledger.

When a draft over-pulls an axis, replace or remove its positive control rather than appending an opposing negative.

## Output and diagnosis

When color is primary, emit one compact causal signature before flexible inventory: dominant-region axes, supported global/light shift, and tone response without repeated direction.

When supporting, emit only the smallest relational cue. Diagnose differences as intrinsic, illumination, global cast, exposure/tone curve, processing, or unresolved; keep profile/measurement uncertainty separate from visual judgment.

For render comparisons, report prompt validity, pixel availability, evaluation status, global component, target-local residual, and user judgment separately. An identical-prompt retry is not a color correction. Revise one dominant residual axis at a time only with permission, then freeze a new version.

## Optional negative contribution

Reject only source-likely drift in relative value, chroma, hue direction, global cast, exposure response, tone-zone behavior, or unsupported uniform grading. Do not install fixed color-word blacklists or example-specific desired values.


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
- For material color fidelity, keep intrinsic value, chroma, and hue in separate short controls. A current-source aggregate color/finish descriptor may lead them once through source-evidence qualification; treat its generator effectiveness as unverified unless response evidence matches the exact model version.

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

For actual generation or source/render evaluation, also record how the size reached the tool. Use one of `explicitly-applied`, `auto`, `unsupported`, or `unbound`. After delivery, add the actual frame:

```bash
python3 tools/size_adapter.py WIDTH HEIGHT \
  --binding-status explicitly-applied \
  --delivered-width OUTPUT_WIDTH --delivered-height OUTPUT_HEIGHT
```

Only an explicitly applied target delivered at that exact size passes the frame-setting layer. An explicit mismatch fails; `auto`, unsupported, unbound, or missing delivered dimensions remain unscored, with continuous ratio errors reported when available. This setting evidence does not replace rendered-pixel composition review. Do not try to repair an unavailable size control by repeating aspect-ratio or framing adjectives in the prompt.

## Other generators

- Emit `NEGATIVE PROMPT:` only when the downstream tool exposes a separate negative-prompt input or the user explicitly requests a reusable negative list.
- Use natural-language zones by default. Emit numeric coordinates only if the tool has a compatible layout/control surface or the concept depends on a small number of boundaries.
- Do not name sampler, scheduler, guidance, seed, steps, or control inputs unless the named tool actually supports them.
- Use image, palette, or edit conditioning only when the downstream tool exposes that capability and the request permits it. Keep tool-level reference handling separate from the standalone prompt text.
- Treat any descriptor-response table as model-and-version-specific evaluation evidence, not as a universal color dictionary.
