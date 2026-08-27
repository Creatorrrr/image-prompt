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

- `prompt` (default): keep the routed 3–5 lane architecture, but have each lane return compact-v2 viewer-material P0/P1 evidence, compressed P2 support, and grouped P3/non-material topics. A coupled macro records whether it is sufficient, lossy, or uncertain and emits only at-risk residual relations. Use one lane wave, one integration, one independent critic, and at most one targeted repair.
- `audited`: use full atomic obligations and versioned ledgers for actual generation evidence, source/render or measured fidelity evaluation, skill evaluation, or an explicit audit request. Do not choose it merely because the image contains a person, readable face, or complicated scene.

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
   - Do not identify people, characters, brands, artists, cameras, lenses, film stocks, or private identities from appearance. Do not infer race, ethnicity, nationality, religion, or another protected identity category from pixels. User-stated or trusted context may be used only as separately sourced intent, never as visual evidence.
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
   - In `prompt`, each lane details only P0/P1 findings, compresses P2, groups P3/non-material topics, and avoids exhaustive atomic, orientation, appearance, color, or light ledgers. A macro finding must declare summary adequacy; `lossy` or `uncertain` retains only independently drifting P0/P1 relations the macro loses. In `audited`, split material findings into independently drifting atomic obligations and bind retained obligations through `source_obligation_ids`.
   - Before integration, close every P0/P1 lane handoff against the selected target lane and required module. An absent causal owner is `route-gap`; use the one-reroute budget to refine the facet map rather than dropping the finding. When tools are available, validate the route-bound compact set with `tools/compact_reports.py`.
   - Integrate by owner key and visible effect, not prose concatenation. Give one independent critic the source, route, reports, priority map, and draft without the main transcript. In `prompt`, it checks blocking P0/P1 loss, hidden macro residuals, dangling handoffs, generic-lighting replacement, pose neutralization, or salience inversion and may name one targeted repair; P2/P3 completeness is advisory and triggers no rerun. Do not rerun successful lanes for more detail. Only a route gap or source/hash mismatch may rerun an affected lane once.

5. Integrate the lane reports with an adaptive hierarchy:
   1. Record the direct, source-supported appeal separately from the render contract. State it plainly in diagnostic mode. When an aggregate appeal term is itself a high-confidence P0/P1 source invariant and omission would materially change the reading, retain it once in the generation prompt as a bounded semantic anchor, immediately followed by its visible causal controls. Otherwise keep it diagnostic or translate it without emission.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Rank cross-lane evidence by viewer effect: `P0 source signature`, `P1 structural identity`, `P2 supporting`, `P3 incidental`. Any source-specific face, skin presentation, space, clothing, pose, topology, light, color, or capture cue may be P0/P1. Record the smallest causal cue set; module count and raw detail do not set prompt weight.
   4. In `prompt`, preserve one macro spatial result, then hold viewpoint and crop fixed and test whether it carries the source-visible placement, facing, depth-order, pose, topology, support/contact, occlusion, and completion relations that jointly create the read. Mark it sufficient, lossy, or uncertain and retain only decisive P0/P1 at-risk residuals; group the rest. Treat alignment-style wording as positive multi-axis actuation rather than a neutral default, and inspect every exact spatial clause for all explicit and implicit axes it controls. In `audited`, build `spatial-orientation/v5`, dispose every required axis, require an isolated per-axis neutralization test before declaring an axis flexible or not-material, run both human counterfactuals, retain coupled-effect summary coverage, and bind every emitted spatial control to a source-consistent prompt-effect audit exactly as specified by the selected modules and evaluation reference.
   5. Map the few largest coherent image regions by relative area, tonal role, edge contact, legibility, and attention. Record only material component relations: region-to-region or region-to-frame reference, relation kind, source-relative observation, evidence, and role. When one invariant spans multiple regions or visible boundary components, preserve the region-to-region boundary topology instead of collapsing it to a category or one broad edge. When partial visibility matters, record the surviving fragments, cropped or hidden counterparts, and completion risk. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze each material human through four independent decisions. First, retain exact race, ethnicity, nationality, or other identity context only when supplied by the user or trusted metadata and P0/P1 for the requested generation; pixels never establish it. Second, decide whether a non-identifying broad person prior is needed to resist model-default drift and immediately correct it with visible geometry. Third, describe displayed skin only as source-visible value/chroma/undertone/finish under the observed capture, with its own priority and region scope. Fourth, when a person-aesthetic or attractiveness reading is itself P0/P1 and omission-sensitive, state one bounded aggregate anchor and immediately decompose only its declared intended dimensions while protecting identity, pose, crop, age presentation, garment coverage, light, color, and polish unless those dimensions are separately source-supported and intentionally owned. In `audited`, create `human-appearance/v3` with provenance, priority, effect budget, claim/control binding, and skin-region handling. Never install a motivating label or surface combination as a default.
   7. Before treating shape, scale, color, surface, or definition as intrinsic, separate effects caused by pose/deformation, perspective, lighting/shadow, material interaction or occlusion, and capture/processing.
   8. When color/tone is material, `prompt` records only the decisive regional axes, displayed result, protected relation, and uncertainty. Build the full Color/Tone Contract only in `audited`, measured color work, or source/render evaluation.
   9. When light/form is material, `prompt` records one macro visible result before any rig hypothesis, then only independently drifting P0/P1 regional relations the macro loses: target/reference region, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, background spill, and pose dependency. This is a source-driven vocabulary, not a checklist. Build the full Light/Form Contract only in `audited`, measured lighting work, or source/render evaluation.
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
    schema_version: spatial-orientation/v5
    subjects: []        # material orientation-bearing subject id, kind, visibility, major-region id, evidence
    evidence_cues: []   # subject-owned visible cue family, observation, evidence, confounders
    counterfactual_checks: [] # per human: whole orientation plus viewpoint-held residual alignment
    decisions: []       # decomposed dimension, disposition, cue ids, owner, emitted path or isolated dimension-neutralization evidence
    coupled_effects: [] # one aggregate control; macro summary first, then only source-visible residual member relations the summary loses
    prompt_effect_audits: [] # exact spatial clause plus every explicit/implicit affected decision; only source-consistent invariant ownership may emit
  human_appearance_decisions: [] # human-appearance/v3: external identity context, broad prior, bounded appearance gestalt, displayed skin, and owned/protected dimensions
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

7. Draft the smallest prompt that carries P0/P1, then only useful P2 support. Put the source-specific signature near the beginning and let order reflect what a viewer notices and would miss first. Use **retain-and-decompose** for material aggregate language: state one evidence-qualified abstract descriptor, then immediately unpack it into owned form, surface, light, color, spatial, hierarchy, or capture controls. Do not use abstraction without controls, and do not assume detailed controls preserve the same global meaning when the omission counterfactual says otherwise. When pose and illumination jointly shape the visible form, order the causal passage as proposition, camera/crop, macro spatial result, at-risk spatial residuals, pose-bound Light/Form relations, surface or garment response, then background/capture; later prose must not normalize an earlier relation. Audit each exact spatial clause as a whole: semantic classes equivalent to centered, frontal, upright, vertical, straight, balanced, or aligned can alter several axes even when only one is named. List those effects as explicit or implicit, and rewrite or remove the clause if any affected axis lacks invariant or coupled ownership. For a human, place material user/trusted identity context once before the appearance passage, keep a broad person prior next to correcting geometry, and let one bounded person-aesthetic anchor lead only its contiguous owned decomposition. State each aggregate once, remove competing normalization instead of adding counter-negatives, and never let incidental inventory or an aesthetic anchor change protected skin, makeup, garment coverage, pose, crop, lighting, or polish. Terms such as `source-relative`, `source-visible`, `source-specific`, `source-supported`, and `current-source` are analysis/provenance vocabulary only. Compile each one into the literal visible target—such as viewer-left placement, a three-quarter head/torso relation, broad highlight coverage, or a named surface value—before it enters `PROMPT:`. In `audited`, additionally reconcile every atomic obligation and exact generic, Color/Tone, and Light/Form control ledger according to the selected modules.

8. Apply the profile-aware pre-emit gate. Read `PROMPT:` with the image, plan, reports, and conversation hidden. Reject any clause that still asks the generator to match, preserve, or infer an absent source/reference/original instead of stating the target itself. Run one independent compact critic in `prompt`; apply at most one targeted repair and stop. If a P0/P1 conflict remains unresolved without guessing, report the limitation rather than opening another analysis cycle.

9. For actual generation or source/render evaluation, use `audited` and persist the validated bundle, reconciled `plan.json`, exact `prompt.txt` and SHA-256, settings, reference handling, and attempt log. Run `tools/analysis_bundle.py` and `tools/salience_plan.py` before freezing. Ordinary prompt-only extraction needs neither persisted ledgers nor v5 processing.

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

Do not mention or depend on the attached, source, reference, input, provided, or original image inside the generated prompt. `Keep`, `preserve`, `retain`, `remain`, and `stay` are allowed only when the same prompt names the visible state or relation they govern; they may not point outside the prompt.


---

# Distributed analysis orchestration reference

# Distributed analysis orchestration

Use this contract after facet/module routing and before prompt drafting. Domain evidence still comes from the selected `modules/*.md`; lane files define independent ownership and reporting.

## 1. Choose an analysis profile

Resolve `reverse-image-analysis-route/v2` with `tools/route_resolver.py --analysis-route --analysis-profile PROFILE`.

- `prompt` is the default for an ordinary one-image prompt or diagnosis. It preserves separate lane analysts and an independent critic, but collects only viewer-material evidence.
- `audited` is for actual source/render evaluation, measured fidelity work, skill evaluation, or an explicit request for a full evidence ledger. It retains `reverse-image-analysis-lane-report/v2`, `spatial-orientation/v5`, `human-appearance/v3`, and `reverse-image-analysis-bundle/v2`.

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

In `prompt`, each lane returns `reverse-image-analysis-lane-report/compact-v2`:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/compact-v2",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 20}],
  "primary_read": "one sentence naming what this lane says the viewer must retain",
  "material_findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "viewer_priority": "P0",
      "representation": "atomic",
      "observation": "source-relative visible result",
      "source_evidence": ["decisive visible cue"],
      "confidence": "medium",
      "change_counterfactual": "what visibly becomes a different image if changed",
      "default_drift_risk": "high",
      "control_requirement": "causal requirement, not final prompt prose",
      "summary_adequacy": null,
      "aggregate_descriptor_candidate": {
        "phrase": "optional current-source aggregate reading",
        "candidate_source": {
          "kind": "source-visible-approximation",
          "reference": "current source hash or observation id"
        },
        "confidence": "high",
        "viewer_priority": "P0",
        "omission_counterfactual": "material-drift",
        "decomposition_requirements": ["owned visible control requirement"],
        "effect_budget": {
          "intended_dimensions": ["face-form", "hair-boundary"],
          "protected_dimensions": ["identity-context", "pose-occlusion", "capture-treatment"]
        }
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

Set `representation` to `atomic` when the observation is already one independently drifting result. Set it to `macro-summary` when one compact pose, topology, lighting, surface, or capture read compresses several source-visible relations. Every macro summary carries `summary_adequacy.verdict = sufficient | lossy | uncertain`. A sufficient summary has no residuals. A lossy or uncertain summary lists only P0/P1 `at_risk_relations`, each with source-relative subject/region ids, relation kind, visible result, evidence, confidence, control requirement, causal owner lane, and any material dependencies. This is a lightweight loss audit, not an atomic ledger: do not enumerate relations the summary already preserves.

`aggregate_descriptor_candidate` is optional and case-bound. Include it only when the phrase itself carries a P0/P1 gestalt not preserved by detail alone; its decomposition requirements remain separately owned. A human aggregate additionally declares intended and protected dimensions, always protecting identity context. Exact identity context uses a separate provenance-bound integration handoff (`user-supplied` or `trusted-metadata`, external reference, viewer priority, no pixel inference). Never fill either field from a preferred vocabulary. Split a compact finding only when two visible results can drift independently and both are P0/P1. Otherwise keep the causal result together. Compact reports do not create exhaustive atomic obligations, full color/light ledgers, `spatial-orientation/v5`, or `human-appearance/v3`.

After the lane wave, close every structured P0/P1 handoff before integration. A lane-to-lane handoff names its source finding or residual ids, target lane, required routed module, reason, and `route_required: true`. The target lane must be present and the required module must be assigned to it. An absent target or owner is `route-gap`, not an ignorable advisory; use the existing one-reroute budget to refine the facet map, then rerun only the affected route. A provenance note intended only for the integrator sets `route_required: false` and does not invent a lane dependency. When tool execution is available, validate the temporary or persisted set with:

```json
{
  "schema_version": "reverse-image-analysis-compact-set/v2",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "route": {},
  "lane_reports": []
}
```

```bash
python tools/compact_reports.py COMPACT_SET.json
```

The checker validates schema, source/route binding, summary residual shape, module assignment, and handoff closure. It does not validate the visual interpretation.

## 4. Viewer-first integration

The main session integrates by owner key and visible effect, never by concatenating lane prose. Before writing the prompt, assign one cross-lane priority:

- `P0 source signature`: changing it makes a viewer read a materially different image. Put its causal controls first.
- `P1 structural identity`: major subject gestalt, face/form/surface, space, clothing silhouette, pose/action, topology, lighting, color, or capture evidence needed to preserve that signature.
- `P2 supporting`: recognizable but safely compressed into an existing clause or one later cue.
- `P3 incidental`: omit unless the user explicitly asks for it.

Priority is counterfactual and source-specific, not category-specific. Face, skin presentation, room geometry, garment silhouette, pose, camera distance, or any other field can outrank the rest. Conversely, a visible field can remain P2/P3 even when a routed module analyzed it.

For a material human, make four independent, source-prioritized decisions:

- exact identity context only from user/trusted external provenance and only when P0/P1;
- one non-identifying broad person prior only when supported, omission-sensitive, and immediately corrected by decisive geometry;
- displayed skin value/chroma/undertone/finish with its own viewer priority, region, and observation scope;
- one optional person-aesthetic or attractiveness gestalt with intended/protected dimensions and immediate owner-correct decomposition.

Pixels never establish race, ethnicity, nationality, or another protected identity. A broad prior is non-identifying and never acts as likeness by itself; keep it adjacent to authoritative geometry. A person-aesthetic aggregate may emit once when high/medium-confidence P0/P1 evidence and a material-drift omission counterfactual support it. It leads only its declared intended controls and cannot alter protected identity, pose, crop, scale, age presentation, garment coverage, skin/cosmetics, light/color, or capture polish.

Draft the prompt from P0 to P2. Give each P0/P1 effect one causal owner and one prompt control, merge compatible P2 evidence into those clauses, and omit P3. Specificity follows viewer impact: do not give a long incidental inventory enough repetition to overpower the source signature. For a source where pose and illumination jointly determine form, keep this causal order unless the source proposition requires a tighter merge: proposition, camera/crop, macro spatial result, at-risk spatial residuals, pose-bound Light/Form relations, surface or garment response, then background and capture. Later prose must not normalize or symmetrize an earlier source-relative spatial control.

## 5. Compact independent critic and repair budget

Give one independent read-only critic the source/hash, route, compact reports, priority map, and draft prompt without the main reasoning transcript. It checks only blocking visual failures:

- lost or contradicted P0/P1 evidence;
- a generic attractiveness, mood, or style prior replacing source-specific appearance instead of leading an owned decomposition;
- unsupported broad-person inference;
- external identity context inferred from pixels, or appearance wording leaking into a protected dimension;
- source-significant face/skin, space, clothing, pose, topology, light, or color drift;
- a macro summary marked or functioning as sufficient while it hides a decisive source-visible residual relation;
- a P0/P1 handoff whose target lane or required module is absent from the route;
- generic lighting language replacing independently drifting regional Light/Form relations;
- a later clause neutralizing, symmetrizing, or otherwise overriding an earlier pose relation, including alignment-style wording whose implicit affected axes were omitted from the draft's effect audit;
- literal prompt text that leaks internal provenance (`source-relative`, `source-visible`, `source-specific`, `source-supported`, `current-source`) or requires an absent attached/source/reference/input/provided/original image to resolve its target;
- a P2/P3 detail outranking a P0/P1 control; or
- a route/source mismatch.

The critic returns `pass`, `targeted-repair`, or `blocked`, with exact affected finding/control IDs. Advisories about P2/P3 completeness do not trigger work. Apply at most one local repair to the named controls; do not rerun successful lanes or restart integration. If one repair cannot resolve a P0/P1 uncertainty without guessing, keep the uncertainty visible in diagnostic mode or tell the user the fidelity limit. Do not iterate toward v2, v3, or v4 merely to make the analysis look complete.

When runtime telemetry is available, the orchestrator records route, lane-wall, integration, critic, and repair durations plus report sizes. Lane workers do not spend analysis time estimating their own timing.

## 6. Audited profile

In `audited`, each lane returns `reverse-image-analysis-lane-report/v2`. Every required topic is individually disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`; each material finding is split into independently drifting atomic visible-result obligations. Integrate them into `reverse-image-analysis-bundle/v2`, dispose every finding and obligation once, bind retained obligations through `source_obligation_ids`, and preserve role and causal ownership.

Use `spatial-orientation/v5`, isolated per-axis neutralization evidence, exact explicit/implicit spatial prompt-effect audits, and both human orientation counterfactuals only here. The raw-source critic must independently inspect the complete literal spatial clauses for synonymous or implicit axis pulls; declared audit ids alone are not semantic proof. Use `human-appearance/v3` and full Color/Tone or Light/Form ledgers only here or when the user explicitly requests those measured contracts. Existing validators remain authoritative:

```bash
python tools/analysis_bundle.py ANALYSIS_BUNDLE.json
python tools/salience_plan.py PLAN.json --prompt PROMPT.txt
```

The audited critic binds to source, route, reports, obligations, plan hash, and the literal prompt. It reads the prompt once more without the source or analysis context and blocks unresolved external reference language even when every ledger excerpt is present. It may request one targeted integration repair and one verification pass. Only a route gap or source-artifact mismatch may rerun an affected lane. If the repair budget is exhausted, report `blocked`; never start an open-ended refinement loop.

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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`: one primary viewer read, only P0/P1 proposition, frame/crop, and major-region findings, compact P2 support, and grouped P3/non-material topics. Use a change counterfactual only to decide whether a region or crop is identity-bearing. Mark any coupled macro finding with summary adequacy and only at-risk residuals. Propose controls, not prompt prose.

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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. First decide whether orientation or topology is P0/P1. If it is, report one macro visible result, then hold the observed viewpoint and crop fixed and test whether that summary preserves the source-visible component-to-subject, subject-to-frame, facing or gaze, depth-order, support, contact, boundary, occlusion, and completion relations that jointly create the read. This is not a fixed checklist: inspect only relations supported by the current source. Mark the macro `sufficient`, `lossy`, or `uncertain`, and retain only decisive P0/P1 at-risk relations that the macro does not carry. Before handoff, treat each alignment-style phrase as a positive control and enumerate every spatial axis it would explicitly or implicitly actuate; never recommend a clause that normalizes an unsupported axis. Hand off appearance, color, and capture questions through the structured compact handoff.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting spatial results into atomic obligations, and retain confounded result directions.

## Completion gate

Dispose every required topic at the profile's depth. In `prompt`, run at most the counterfactual needed to establish P0/P1 materiality and the lightweight viewpoint-held summary-adequacy check above; a concise macro pose or topology plus only at-risk residual relations is sufficient. In `audited`, require an isolated per-axis neutralization test for each `flexible` or `not-material` decision, whole-orientation and viewpoint-held residual-alignment counterfactuals, full coupled-obligation handling, and an exact explicit/implicit effect audit for every emitted spatial clause. Low-confidence or wholly confounded axes become `uncertain` unless an invariant coupled effect preserves the joint result. Surface, garment, and boundary cues may corroborate but never replace source geometry. Never normalize ambiguous axes or complete hidden structure.


---

# Included analysis lane: `lane.subject-appearance`

# Analysis lane: subject appearance

## Role

Own visible subject form and non-identifying appearance evidence. For humans, separate externally sourced identity context, non-identifying person prior, displayed-skin surface, and appearance gestalt, as well as frame prominence from fidelity salience and intrinsic evidence from induced effects.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred demographic label, another lane's conclusions, or draft prompt prose.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. Report four independently prioritized decisions: exact identity context only from the raw user request or trusted metadata; an optional non-identifying person prior corrected by decisive geometry; displayed-skin axes and region scope; and an optional person-aesthetic gestalt. Mark a coupled macro finding with summary adequacy and only source-supported at-risk residuals. Never propose race, ethnicity, nationality, or another protected identity from source pixels. Hand color/light attribution to its lane through the structured compact handoff.

`beautiful`, `attractive`, `model-like`, or another aggregate appearance reading may be reported as a separate P0/P1 candidate when source evidence and the omission counterfactual support it. Record intended and protected effect dimensions plus the owner needed for each intended decomposition; identity context is always protected. The aggregate cannot replace prior, geometry, skin, scale, expression, garment, pose, light/color, or capture findings. In `audited`, return `reverse-image-analysis-lane-report/v2`, supply `human-appearance/v3`, and split independently drifting results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. A small or secondary subject may still be fidelity-primary. Unsupported identity inference or an aggregate without an effect budget fails. A broad prior may be omitted when local geometry is sufficient and default drift is low; record residual uncertainty instead of repeated omission tests.


---

# Included analysis lane: `lane.color-light-material`

# Analysis lane: color, light, and material

## Role

Own causal separation of intrinsic color, displayed tone, illumination, shadow, and material response. For human skin, own displayed surface evidence only, never identity or biological color. Apply the routed fidelity modules rather than duplicating their rules here.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Receive subject/region identifiers as neutral handoff keys, not appearance conclusions.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. Report only P0/P1 regional color, displayed-tone, light-to-form, or material-response effects. When a compact illumination or form summary represents several relations, test its adequacy and retain the smallest independently drifting at-risk subset among target/reference region, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, background spill, and pose dependency. This list is a causal vocabulary, not a required inventory. Each residual names its source-relative regions and visible result; generic lighting or rig language never substitutes for those relations. For displayed skin, hand off subject/region, P0-P3 viewer priority, observation scope, stable axes, coverage, and confounds; do not supply a demographic label. Prefer stable visible results when physical attribution is uncertain.

In `audited`, return `reverse-image-analysis-lane-report/v2`, keep region/protected scope explicit, and split material intrinsic color, displayed tone, light, shadow, response, and cross-region results into atomic obligations.

## Completion gate

Dispose every required topic at the profile's depth. When pose or deformation changes the visible light-to-form result, record that dependency instead of treating the shading as intrinsic surface. Do not pool mixed regions, convert displayed skin into identity or biological truth, let an appearance anchor change an unowned skin axis, or let a global control erase a protected P0/P1 relation.


---

# Included analysis lane: `lane.medium-aesthetic-capture`

# Analysis lane: medium, aesthetic, and capture

## Role

Own medium/process evidence, capture character, production aesthetic, and meaningful artifacts. Keep portrait-production aesthetics separate from identity and from a person's source-visible appearance gestalt.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive a preferred genre label or a draft prompt.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2` with the fidelity ceiling and only P0/P1 capture or production cues. For humans, report cosmetic visibility, displayed-skin finish, optical softness/bloom, retouching, and polish as separable effects keyed to the shared subject; do not duplicate the subject lane's person-aesthetic aggregate. A broad production aesthetic may become one provenance-bound aggregate candidate only when omission causes material drift; report its literal causal controls separately. If capture evidence makes regional light, shadow, or light-induced form P0/P1 but `detail.light-form-fidelity` is not assigned, emit a route-required structured handoff to `lane.color-light-material` instead of replacing the missing owner with a capture adjective.

In `audited`, return `reverse-image-analysis-lane-report/v2` and decompose a material aesthetic candidate into independently drifting visible obligations.

## Completion gate

Dispose every required topic at the profile's depth. Do not upgrade fidelity, infer an artist/camera, or use genre, quality, mood, or beauty as a substitute for visible controls. Prevent a person-aesthetic handoff from adding makeup, glossy skin, facial sculpture, relighting, or editorial finish outside its declared intended dimensions.


---

# Included analysis lane: `lane.information-layout`

# Analysis lane: information layout

## Role

Own information hierarchy, reading order, text/UI legibility, and nested frame boundaries. Existing routed modules remain the domain source of truth.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and assigned modules. Do not receive other lane conclusions or final wording.

## Output contract

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2` with only P0/P1 container hierarchy, reading order, legibility, or nested-boundary findings; mark a coupled macro finding with summary adequacy and only at-risk residuals, compress supporting structure, and group unreadable or incidental detail. In `audited`, return `reverse-image-analysis-lane-report/v2` with atomic layout obligations. Never transcribe unreadable content or write final prose.

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

- Never refer to the source image in the final prompt.
- Compile `source-*` and `current-source` provenance labels into literal visible targets before emission.
- Describe visible evidence only; do not invent hidden structure or context.
- Do not assert identity, nationality, race, exact ethnicity, religion, personality, measurements, metadata, brands, artists, cameras, lenses, or film stocks from appearance. Exact demographic or nationality context may enter only from a user statement or trusted metadata and remains externally sourced; pixels support non-identifying form, hair, displayed-surface, and aesthetic evidence rather than a protected-category claim.
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

- Record exact source dimensions when available.
- Treat aspect-ratio drift as a major fidelity failure.
- Keep source dimensions separate from target size; do not assume generator support.
- Preserve measured ratio in plain language; add a decimal only to distinguish nearby shapes.
- Do not invent exact dimensions from a viewer preview.
- Put frame shape, crop, and edge interactions first. Lock subject frame share and negative-space share before adding face or object micro-detail.
- Describe which evidence occupies the frame zones, including any material source-visible axis offset.

## Major-region hierarchy

Map the few largest visually coherent regions as a major-region hierarchy before local detail. Record relative area, role, attention, legibility, and frame contact without fixed percentages.

Preserve region-share hierarchy when flexible pose, viewpoint, or placement changes; exact coordinates may move.

## Spatial language

In `prompt`, when orientation is P0/P1, emit one macro result plus decisive residual relations. Placement proves no orientation. Treat alignment semantics as positive controls; enumerate every axis each exact clause affects explicitly or implicitly.

In `audited`, disposition every spatial axis. `flexible` or `not-material` requires isolated neutralization with adjacent relations held; low-confidence or wholly confounded axes become uncertain unless coupled. Run both human counterfactuals, merge joint effects once, and block a spatial clause affecting any unowned axis.

## Relational coordinate frames

- Use frame-relative directions for composition and object- or scene-relative zones for physical relationships. Qualify `left`, `right`, `front`, or `behind` when viewpoint could reverse them.
- Establish a visible shared reference plane when it disambiguates the scene: floor, ground, seat, platform, tabletop, interior volume, or another support region.
- Record which side of a boundary holds the main mass and which parts cross it. Separate 2D overlap from contact, containment, support, and depth order.
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
- Treat subject attractiveness and image polish as separate controls. Treat any broader person aesthetic the same way: declare intended and protected dimensions, lead its owned visible controls once, and do not imply unowned skin cleanup, symmetry, makeup, garment exposure, crop, pose, lighting, or editorial finish.
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
- Reject unresolved provenance labels and missing-artifact comparisons; allow physical `light source` and self-contained state verbs.
- Audit coordinate contradictions before emitting. In `prompt`, a coupled macro declares `sufficient`, `lossy`, or `uncertain`: sufficient emits no residuals; otherwise retain only supported P0/P1 at-risk relations. A missing cross-lane owner or module is `route-gap`. In `audited`, validate the full spatial contract.
- Treat alignment prose as multi-axis control. Record each exact clause's explicit and implicit effects; rewrite it if any affected spatial axis is unowned. Negatives cannot repair the conflict.
- For a material human, verify external identity provenance and output use, displayed-skin scope and priority, and one bounded appearance gestalt. Exact external identity context precedes the gestalt; a broad person prior stays contiguous with correcting geometry.
- Retained human or general aggregate descriptors require provenance, P0/P1 materiality, a material-drift omission check, intended/protected dimensions, and adjacent owned decomposition. Beauty and skin wording cannot act as likeness or demographic evidence.

## Causal ownership

- Audit shared perceptual effects across semantic slots, causal layers, paragraphs, negatives, and settings.
- Keep form, surface, light, color, material, and hierarchy causally consistent; do not encode induced effects as intrinsic.
- Assign every appearance-changing color or tone phrase to one causal layer. A qualified aggregate may lead its axes once; rewrite or remove other free-floating mood or color adjectives.
- Split an ambiguous color phrase when one modifier could silently control intrinsic surface, illumination, exposure, or processing at the same time.
- Give an axis-control one region and one perceptual axis. Split a compound that would silently change several material axes.
- Assign every lighting-changing phrase to one Light/Form owner. Keep the visible result authoritative when physical cause is uncertain.
- Do not let a compact lighting summary replace an at-risk regional or pose-dependent Light/Form relation.
- Keep global tonal range and local form contrast as separate effects.
- Give every material shadow event a source-supported owner or mark it mixed or uncertain.

## Audited-only ledger checks

Apply this section only in `audited`, measured fidelity, or source/render evaluation:

- For a material color or tone effect, verify one aggregate source-relative target and the evidence for every emitted intrinsic, illumination, global-cast, exposure, processing, or hierarchy contribution.
- For every required intrinsic value, chroma, or hue observation, trace one uninterrupted path from region axis to same-region/same-axis aggregate effect, emitted claim, and intrinsic axis-control.
- Reconcile every exact color-changing excerpt in the final prompt with one emitted claim, one causal layer, and its complete aggregate effect budget.
- For material lighting, verify one source-relative Light/Form target and evidence for every emitted source-geometry, fill, local-form-contrast, shadow-topology, material-response, or background-spill contribution.
- Reconcile every exact lighting-changing excerpt with one emitted claim, one owner, and its complete lighting-effect list.
- Before generation, validate human appearance, per-axis neutralization, whole/residual spatial counterfactuals, exact prompt-effect audits, obligation binding, and ledger separation.

## Final checks

- Preserve major-region area and attention order, partial visibility, fidelity ceiling, and scale-appropriate detail.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions.
- When pose and light jointly shape form, keep camera/crop, spatial macro and residuals, then pose-bound Light/Form; later clauses must not neutralize that relation.
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

- Compile provenance labels into literal targets; never ask for an unavailable artifact. Physical `light source` remains valid.

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

For a material human, keep user/trusted identity context external and use it once only when P0/P1. Then order one scale-appropriate passage as optional broad person prior, correcting geometry, one bounded person-aesthetic or attractiveness anchor with contiguous owned decomposition, displayed skin, hair, expression, garment coverage, and capture. The aggregate cannot replace controls or alter protected pose, crop, identity, age, lighting, or polish dimensions.

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

Read `PROMPT:` as if the source image, analysis, conversation, and every optional section disappeared. If any target or the primary proposition, its invariants, crop, required relationship, subject hierarchy, medium, or fidelity ceiling would be lost, revise the prompt itself.


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
- When the secondary layer is cropped or partial, name only one to three source-salient visible fragments, their frame or foreground overlap, and the counterpart parts that stay cropped, hidden, or indistinct. Preserve its source-visible offset and completion budget; do not turn a partial layer into a complete centered subject.
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

In `prompt`, record only P0/P1 entries from this hierarchy before micro-detail; group the rest. In `audited`, dispose every listed axis:

- number of people and primary/secondary roles
- each person's frame share, crop, depth plane, and overlap order
- head position and scale relative to the frame and body
- independently dispose of torso yaw/pitch/roll; head-to-body yaw/pitch/roll and lateral offset; shoulder image-plane slope and depth order; attention direction; and visible action as invariant, flexible, not-material, not-visible, or uncertain
- the visible floor/seat/support region, which side of any nearby boundary contains the person's main mass, and which body parts contact or cross it
- which face, hair, limbs, clothing, or accessories are cropped, hidden, soft, or outside the frame

Allocate detail by legibility; keep distant, blurred, reflected, screen-contained, or background people simple.

In `prompt`, preserve one macro pose result and decisive residuals when pose is P0/P1. Alignment semantics can jointly actuate torso, head/body, shoulder, attention, placement, and viewpoint; inspect every clause's explicit and implicit effects. In `audited`, link decisions to cues/confounders, test each discarded axis in isolation, compare whole with viewpoint-held residual neutralization, cover coupled members, and reject clauses affecting non-invariant or uncertain axes.

Before appearance prose, build a compact appearance signature in `prompt`; create one `human-appearance/v3` decision per spatial human only in `audited`. Distinguish occlusion from crop in either profile.

## Visible appearance

Describe each non-identifying fictional person coarse-to-fine: use one compact broad person-gestalt anchor when it materially reduces ambiguity, then constrain it with visible geometry and source-specific corrections.

For `prompt`, decide four lanes independently: externally sourced identity context, optional non-identifying person prior, displayed-skin surface, and optional appearance gestalt. A field earns detail only when it is P0/P1 or has high model-default drift.

### Broad person-gestalt anchor

- Frame prominence measures image size/attention; fidelity salience measures reconstruction impact. A readable secondary figure may be fidelity-primary.
- Keep exact race, ethnicity, nationality, or other identity context `user-supplied`, `trusted-metadata`, or `absent`. Emit externally sourced context once only when its viewer priority is P0/P1; never derive or corroborate it from pixels, skin, hair, face geometry, or aesthetic reading.
- Set the non-identifying person prior to `emit`, `omit`, or `uncertain`. Record support, default-drift risk, geometry sufficiency, and one omission counterfactual. Omit only when emitted form geometry is sufficient, drift risk is low, and the source reading survives; never force a protected-category guess.
- An emitted person prior carries provenance and matching human/face/body-form controls. Keep them contiguous so visible geometry corrects the anchor; skin and identity context cannot justify it.
- Decide a separate appearance gestalt for attractiveness or another broad person aesthetic. Emit one high/medium-confidence P0/P1 anchor only when omission causes material drift. Declare intended and protected dimensions, then immediately decompose every intended dimension into an owner-correct face, body, hair, expression, displayed-skin, garment, pose, scale, capture, light, or color control. Identity context is always protected; unowned dimensions cannot change.
- Keep the appearance anchor source-relative in analysis but emit only the visible presentation; never emit `source-relative` or a missing-image comparison. It cannot silently idealize, retouch, relight, reveal clothing, change cosmetics, alter pose/crop/scale/age presentation, or upgrade capture; those directions require their own source evidence and ownership.

After the optional anchor, prioritize source-specific corrections:

- Describe broad apparent age presentation or gender presentation only when visually important and sufficiently supported.
- Treat hair first as silhouette and occlusion: hairline, part, fringe, side masses, length, texture group, volume, flyaways, and which facial regions it covers.
- Set displayed skin to `material`, `not-material`, `not-visible`, or `uncertain` with its own P0-P3 priority. When material, name its Color/Tone regions, observation scope, and `exposed`, `through-sheer`, or `mixed` coverage. Describe stable visible value, chroma, undertone, finish, texture, marks, makeup, facial hair, and retouching as captured surface output, never identity or biological color.

Prevent the generated person from drifting into a different visible face type.
Check portrait prompts for aesthetic-upgrade drift.

## Body and silhouette

Describe only visible image-plane structure shaped by pose, crop, clothing, lens perspective, light, shadow, blur, and occlusion. Do not infer hidden anatomy.

- First decide whether visible body form is a primary aesthetic invariant, a structural connector, or secondary support. Do not allocate detail merely because a body region is large in the crop.
- Preserve visible shoulder span, torso length, waist and hip placement, limb thickness, contour rhythm, stance, and clothing-shaped silhouette. Compare them source-relatively in analysis but state actual proportions and relations in final prose. A garment boundary neither proves nor erases pose supported by independent contours or depth cues.
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

Order human controls by cross-lane priority while preserving dependencies: scale/crop and camera; material pose; one P0/P1 external identity context; any broad person prior with correcting geometry; one appearance gestalt with its contiguous owned decomposition; then remaining displayed skin, hair, expression, garment, light/color, and capture controls. In `audited`, coupled pose controls retain the macro summary and only `partial` or `lost` residuals, and every spatial control carries a complete explicit/implicit effect audit against the final literal excerpt. Placement stays positional and appearance inherits pose.

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

When rendered or painted lighting is first-order, contribute the visible shading evidence to `detail.light-form-fidelity`. Treat physical lamp placement as optional and confidence-rated; for stylized media, preserve value grouping, gradient or cel-step structure, shadow ownership, material response, and spill as image-space results.

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

Load for photographic images whose camera, focus, lighting, or processing behavior matters.

## Evidence contribution

Contribute only photographic controls that materially affect an invariant or likely drift. Describe:

- camera distance, height, angle, roll, perspective, and resulting scale or foreshortening
- focus target, depth of field, layer blur, global softness, sharpening, compression, bloom, and haze
- motion blur, shake, ghosting, smear, rolling-shutter, or stable capture
- visible medium impression and its fidelity ceiling. For casual or compressed capture, preserve handheld asymmetry, softness, bloom, clipping, low-legibility, and ordinary framing before genre shorthand.

Map sharpness separately across the primary subject, secondary details, foreground, and background.

Map contrast topology separately at the global scene, major subject masses, local form transitions, and surface/material boundaries.

- Identify the largest bright and dark masses before small accents.
- Separate global range from local contrast; either can be strong while the other is soft.
- State whether shadows flatten, reveal, separate, or sculpt form. Distinguish material responses only when visible.

Decompose photographic appearance into intrinsic subject evidence, pose or deformation, perspective, illumination and shadow, material interaction or occlusion, and capture or processing. Preserve their combined visible result, but do not let one cause rewrite another.

For humans, keep cosmetic visibility, displayed-skin finish, optical softness/bloom, and retouching or editorial polish as separate effects. A person-aesthetic anchor may own capture treatment only when declared in its intended budget and decomposed here; it cannot turn diffused softness into glossy beauty lighting, stronger makeup, sharper facial sculpture, or premium studio finish.

Record important color relationships as intrinsic surface hue, illumination color, global cast, and exposure response. Assign the consolidated hue instruction to one semantic slot; this module should describe the photographic shift rather than repeat another module's color target.

Treat the image's sampled or visually read color as displayed capture output. Without calibrated scene data, it does not establish scene reflectance, material true color, or a person's biological color independently of illumination, white balance, exposure, tone mapping, and profile handling.

Separate photographic white balance or global cast from exposure and tone-curve behavior. A warmer or cooler capture shift must not silently darken, brighten, saturate, or desaturate an intrinsic surface unless the source supports each change.

Map source-visible highlight, midtone, and shadow response separately when tonal reproduction is material. Use comparable midtone or flat patches for displayed intrinsic color and separate highlight or shadow patches for response; do not pool illumination zones or substitute capture response for intrinsic surface axes.

Require neutral anchors or consistent multi-region behavior for global white balance; otherwise report local shifts and uncertainty.

In source/render comparison, compare target and contextual patches. Estimate the shared Lab movement from contextual groups, then subtract it from each target group's movement to expose the target-local residual. Shared movement supports a global cause; target-only movement supports a local cause; mixed results remain unresolved.

Distinguish global softness, diffusion, haze, or compression from depth-of-field blur. Invoke shallow depth only when a sharper focus plane separates from defocused layers; if the subject is also soft, preserve it.

Describe edge sharpness and microcontrast separately. Preserve highlight rolloff, bloom radius, black level, shadow lift, local contrast, and texture suppression only when visible; do not infer a lens or filter.

Describe lighting-to-volume:

- main direction, softness, temperature, fill, back/rim/flash contribution
- highlight placement, shadow falloff, black level, bloom, haze, clipping, and local contrast
- cast, self, and contact shadows only when they affect form, separation, or composition

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Keep global contrast distinct from local form contrast so a dark frame or wide tonal range does not automatically create hard internal definition.

When lighting itself is first-order, contribute capture evidence to `detail.light-form-fidelity` instead of independently owning source geometry, fill, shadow topology, material response, or background spill. Keep exposure, tone curve, white balance, and illumination color in the photographic Color/Tone handoff so the two contracts do not repeat one visible pull.

Do not relight into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes visible structure.

## Optional negative contribution

Reject wrong perspective, focus hierarchy, blur direction, sharpness, shake, grain, flash, cast, tonal response, polished quality beyond the source, and relighting that changes proportions.

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

# Included module: `detail.human-body-form`

# Detail: human body form, proportion, and surface

## When to load

Load only when visible body form is a first-order part of the image's identity or perceptual appeal: source-relative proportion, silhouette, contour rhythm, tissue character, muscular definition, skin surface, or the hierarchy among body regions. Do not load merely because a person is present.

## Analysis

Start with the large-scale form proposition, then test its visible quality against observable causes. A broad descriptor is a hypothesis, not evidence.

In `prompt`, stop after the P0/P1 form proposition and its few decisive proportion, contour, tissue, surface, or hierarchy cues. Compress P2 and do not enumerate the remaining axes. In `audited`, dispose every material axis and retain the full causal handoffs.

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

Inspect torso and shoulder axes from visible relations, then retest with viewpoint fixed. Garment, hair, crop, and foreshortening corroborate or confound but never substitute; weak axes may share one coupled result.

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


---

# Included module: `detail.human-face-likeness`

# Detail: human face likeness

## When to load

Load only when at least one human face is prominent or clearly readable. Do not load merely because a person exists.

## Detail tier

Allocate anchor count by visible face scale and legibility, but assign fidelity role independently. A readable-secondary face may remain a primary invariant when changing its broad reading changes the image.

- **Prominent and legible:** the face is a primary image anchor and individual feature relationships are separable. In `prompt`, use two to five decisive anchors; in `audited`, use six to ten when supported.
- **Readable but secondary:** the face is smaller but several feature groups remain reliable. In `prompt`, use one to three decisive anchors; in `audited`, use three to six.
- **Small or indistinct:** do not use this module. Preserve head orientation, hair mass, skin-tone massing, and visibility only through `subject.human`.

Choose anchors by viewer impact and default-drift risk, never to fill every facial group. A material person-aesthetic or attractiveness reading is one optional gestalt anchor, never local likeness geometry; bind each intended effect to a separate visible control.

Use fewer anchors when softness, compression, low contrast, or scale limits separation. Anchors preserve geometry; they do not authorize larger crop, sharper focus, cleaner makeup, extra detail, or a supporting-role downgrade.

An anchor describes a visible relationship, not a generic adjective.

## Coarse-to-fine likeness

When `subject.human` selects a broad person-gestalt anchor, treat it as one high-level generation prior rather than as the likeness description itself.

- Place it once before local face geometry; do not repeat the broad prior in later clauses.
- Never infer race, ethnicity, nationality, or another protected identity label from a face. Preserve exact user/trusted identity context once as external intent before the appearance passage when it is P0/P1; it is not visual evidence or a generation prior.
- Link `geometry_claim_ids` to exact source-visible form controls. Keep them contiguous after the prior so local geometry corrects it. Prose, skin color, or the prior itself cannot satisfy the link.
- Use the scale-appropriate geometry budget to correct the category prototype with only the source-material face silhouette, feature relationships, expression, hair boundary, surface treatment, and visible asymmetry.
- If the broad anchor conflicts with reliable local geometry, revise or omit the broad anchor. Geometry wins.
- Keep a person-aesthetic or attractiveness anchor at the source-visible overall reading during analysis, then express the actual bounded presentation in the final prompt without the internal phrase `source-visible` or another missing-image comparison. State it once only when P0/P1 and omission-sensitive, followed immediately by controls for every intended dimension. Protect identity, pose, crop, scale, age presentation, cosmetics, garment coverage, light, color, and capture treatment unless separately owned; do not idealize, clean, enlarge, sharpen, or relight by implication.

## Likeness anchor selection

Select only the strongest supported anchors across these groups:

1. **Silhouette:** head proportions, forehead/cheek/jaw/chin relationship, and visible asymmetry.
2. **Eyes and brows:** relative size, spacing, tilt, lid exposure, far-eye compression, brow relation, and gaze.
3. **Midface and nose:** bridge, length, projection, tip, nostril visibility, and cheek/lip relation.
4. **Mouth and expression:** width, line/fullness, closure, corners, teeth, and decisive facial tension.
5. **Hair boundary:** hairline, part/fringe, side masses, volume, texture group, and covered facial regions.
6. **Skin and makeup:** displayed tone/undertone, finish, texture/marks, makeup, facial hair, and capture treatment.
7. **Facial light:** material highlight/shadow planes and their effect on readable geometry.

Preserve expression, gaze, and hair-to-face occlusion as likeness-critical geometry. Keep viewpoint separate from head pose and attention; do not repeat perspective-induced nostril, jaw, neck, eye, or far-side changes as intrinsic geometry.

Infer face orientation from multiple relations—near/far feature exposure, side contour, nose-cheek spacing, compression, and occlusion—not both eyes alone. Record occluders as confounders; if camera/head separation is uncertain, preserve the visible side relation.

Keep optical softness distinct from beauty retouching; do not convert it into crisp, smoothed skin.

Use relational wording: wider than, closer together, higher than, partly hidden by, aligned with, shorter relative to, or more visible on the viewer-left/right. Do not infer unobserved feature geometry.

## Partial, angled, and multiple faces

- For three-quarter or profile views, state near-side/far-side feature visibility and perspective compression instead of describing an imagined frontal face.
- For edge-cropped or occluded faces, list visible and hidden feature groups before fine detail. Do not complete the missing side.
- For a reflected, screen-contained, printed, or background face, keep its detail ceiling tied to that layer.
- For multiple readable faces, allocate the largest anchor budget to the primary face and a smaller distinct set to each secondary face. Never merge anchors between people.
- For stylized faces, preserve the source's shape language, line/render treatment, and feature scale; add the maturity module only when needed.

## Prompt contribution

Create one compact human-likeness passage at the position assigned by viewer priority:

1. optional P0/P1 external identity context, once
2. optional person prior, then face scale, angle, crop, visible side, and correcting geometry
3. optional appearance gestalt and its owned decomposition
4. remaining expression, gaze, hair silhouette, and occlusion
5. displayed skin, makeup, rendering, and facial lighting only when independently material

Treat the passage as one owned face-gestalt effect when its clauses jointly preserve one likeness direction. If separate clauses push the same symmetry, feature scale, projection, polish, or face-type direction, merge or replace them rather than allowing the category anchor and local geometry to amplify one another.

Repeat at most one or two highest-risk anchors in the final constraint block. Do not copy the full passage into negative prompt or settings.

## Optional negative contribution

Reject a generic symmetrical model face, changed face silhouette, wrong eye/brow spacing or tilt, wrong nose/mouth/jaw relationship, changed expression or gaze, cleaned-up asymmetry, hairline/fringe/occlusion drift, invented hidden features, different skin or makeup treatment, and relighting that changes readable facial geometry. Include only the failures supported by the selected anchors.


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

# Included module: `detail.light-form-fidelity`

# Detail: lighting and light-to-form fidelity

## When to load

Load only when illumination, shadow topology, light-induced form, material response, or background spill is an invariant; when the user explicitly requests lighting fidelity; or when a source/render comparison finds a material lighting residual. Do not load merely because an image is lit.

A source/render loss of source-visible value separation between adjacent regions of one surface is a material residual when that separation carries form or hierarchy. Route it here even if the overall lighting looks ordinary; do not compensate by strengthening intrinsic anatomy, object volume, garment fit, or surface color.

## Three-stage Light/Form Contract

In `prompt`, preserve only the P0/P1 visible light result, its named region relation, and any protected local effect. Prefer result-space language when cause is uncertain; do not enumerate every lighting axis or build a final ledger.

In `audited`, measured lighting work, or source/render evaluation: Build a source-relative Light/Form Contract only when illumination materially carries fidelity.

Keep three stages separate:

1. **Observation:** the visible spatial light result.
2. **Actuation:** the smallest literal prompt controls that reproduce that result.
3. **Verification:** what a delivered render actually reproduced.

Treat the observed light-to-form result as evidence and the physical lighting setup as a confidence-rated hypothesis. One image rarely identifies a unique lamp, modifier, fill source, or post-processing path. When the cause is uncertain, preserve the visible result with result-space relations rather than letting an invented rig carry the prompt alone.

## Visible result before rig inference

Record the largest continuous bright and dark masses before small highlights. Map global tonal range, bright-plane coverage, local form contrast, gradient character and extent, edge softness, background spill, and the relative visibility of major planes.

Keep global tonal range separate from local form contrast. A wide scene range or dark frame does not require strong internal modeling; a compressed scene may still contain a hard contact edge.

Build apparent illumination from displayed key level, bright-plane coverage, shadow floor, local form contrast, gradient extent, highlight rolloff, microcontrast, and background spill. Keep bright-plane coverage separate from displayed key level and local form contrast. An ordinary image supports this result-space signature, not physical illuminance or lamp power.

Set light-to-form strength source-relatively as flattening, subtle revelation, moderate separation, or strong sculpture. Describe what the light does to visible form instead of substituting broad mood or quality shorthand.

## Source hypothesis

Separate source geometry, apparent source size, and fill structure. Record source count, direction relative to camera and subject, elevation, apparent angular size, fill or bounce behavior, confidence, and visible evidence only when they matter.

Apparent source size owns shadow-edge softness; it does not automatically own fill level or local contrast. A large off-axis source can remain sculpting, and a small near-axis source can flatten form.

Use `physical-cause` or `physical-plus-result` actuation only with medium- or high-confidence source evidence. With low confidence, use `result-space-only` or keep the hypothesis diagnostic.

## Spatial effects and shadow ownership

For each material region effect, record its role as broad plane, gradient, highlight, shadow, rim, or spill; its source-relative strength; edge character; and evidence. Use semantic region relations rather than fixed coordinates unless exact placement is itself invariant.

When adjacent regions of the same material differ because of light-to-form, record the target `region_id` and distinct `reference_region_id` in both the observed region effect and aggregate actuation, then record the transition as a gradient or shadow event when visible. Let the emitted result-space control preserve that relation; do not turn one motivating region name, direction, value, or threshold into a reusable default.

Assign each material dark region to cast shadow, self-shadow, contact or occlusion, material response, processing, mixed, or uncertain ownership. Do not promote a small contact shadow into a broad directional-light field, and do not encode an illumination-induced contour as intrinsic form.

Keep material response and background spill separate from source intensity. Matte, glossy, metallic, translucent, woven, and absorbent surfaces under one light may have different highlight width, black level, and texture visibility.

Let Light/Form alone own source-visible highlight width or strength, spatial black-level response, and bright-plane coverage. Generic object or material clauses must not repeat or counter that lighting direction.

## Pose and geometry dependence

Record whether each light pattern is pose-bound, pose-robust, mixed, or uncertain. When pose is flexible, preserve relational outcomes such as major-plane balance, gradient depth, or light-to-form class while allowing exact highlight coordinates to move. When pose is locked and the evidence is stable, tighter placement may be justified.

## Color and tone handoff

Let the Light/Form Contract own spatial illumination structure and the Color/Tone Contract own displayed color, exposure, and tone response. More specifically, Light/Form owns bright-plane coverage, gradient extent, and background spill; Color/Tone owns displayed key level, shadow floor, highlight rolloff, and microcontrast. Do not emit the same brightness or contrast pull independently from both contracts.

## Controlled lighting language

When compact human-readable lighting language is useful, read `references/lighting-language.md`. Classify displayed key level, shadow floor, edge softness, local form contrast, bright-plane coverage, gradient extent, directionality, and fill structure independently before composing any summary. This language layer may read evidence owned by both contracts, but it owns no new lighting or tone effect.

The policy may compose one explanation-only axis summary without a preferred preset. A named candidate may come from the user, versioned vocabulary, or a provenance-bound current-source reading after independent observation. Keep conflicts and uncertainty non-emitted.

Literal lighting controls remain authoritative. Emit a current-source label once only with compatibility, high/medium confidence, P0/P1 priority, material-drift omission, and immediate owned decomposition. Model calibration adds exact response evidence. A label never fills a missing axis or justifies a rig.

## Final prompt control ledger

In `audited`: Copy every exact prompt excerpt that changes lighting or light-to-form into the final lighting control ledger. Link it to one claim, owner, and complete effect list. In `prompt`, retain one owner and the decisive visible effect without copying prose into a ledger. In either profile, split cross-owner compounds and replace overstrong positive controls rather than appending counter-negatives.

When measured comparison is warranted, read `references/lighting-reproduction-evaluation.md`. Use only analyst-selected regions and profiles, retain source/profile uncertainty, and never convert diagnostic measurements directly into prompt wording.

## Output and diagnosis

When primary, order one passage by visible topology, fill/local contrast, shadow owner, then material/spill. Put this spatial result before overlapping Color/Tone controls. When supporting, use the smallest relation.

Diagnose source/render differences as source geometry, apparent size, fill, local form contrast, shadow topology, material response, background spill, exposure or processing, or unresolved. Prompt validation never substitutes for rendered-pixel lighting verification.

## Optional negative contribution

Reject only source-likely lighting drift such as an unsupported key/fill split, wrong shadow owner, exaggerated sculpture or flattening, enlarged specular response, or excess background spill. Do not install fixed lighting words, directions, ratios, subject regions, or numeric targets.


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

In `prompt`, first decide whether silhouette, coverage, or material response is P0/P1. Otherwise contribute at most one P2 cue; reserve the inventory for audited or clothing-critical work.

- fit, thickness/weight, opacity, stiffness, tension, folds, sheen, and pattern scale
- legible weave, nap, grain, coating, reflectivity, and edge behavior
- neckline/collar/opening, sleeve/strap, seams/closures/hems, and layer interaction; garment edges never replace owned pose

Before using a garment category label, specify the visible opacity, thickness, weight, weave or knit scale, finish, and construction cues that must override its default prior. Omit dimensions that cannot be seen; the point is to disambiguate the material, not to fill a fabric checklist.

When placement matters, map skin, fabric, shadow-hidden, and cropped regions plus interrupted or softened garment edges; preserve boundary components instead of collapsing them to a category.

Treat close upper-torso edges as measured boundary bands, not fashion labels. Lock neckline/garment-edge width, lowest y-position, visible skin/underlayer area above and below it, sleeve/shoulder fabric area, and bottom crop.

When a person-aesthetic anchor is retained, garment coverage remains an independent dimension. Include it in the anchor's intended effect budget only with P0/P1 source evidence and this module's owned boundary control; otherwise protect it. The anchor cannot imply a deeper opening, fitted bodice, different sleeve, changed opacity, or altered exposure.

Avoid broad fashion or garment labels when their prior would deepen, widen, clarify, center, tighten, reveal, structure, or glamorize beyond the source. Category follows geometry and role.

For edge crops, distinguish a narrow visible band from a completed outfit or body. Describe partial hems, waistbands, pockets, or gaps by bounded height/area and nearby anchors; do not invite centered completion or wider exposure.

For accessories, lock visible silhouette, footprint, crop, density, shadow, and occlusion before detail. Keep secondary or edge-cropped pieces partial and low-legibility; do not upgrade them into crisp, complete, symmetrical ornament.

For tight portraits with secondary clothing, budget visible garment bands, frame range, completeness, interruptions, symmetry, and lower-torso extent before a broad label. Keep compressed or unclear construction unresolved.

Do not let cropped secondary clothing become a clean centered outfit. Lock incomplete geometry before category language and preserve its supporting role.

## Optional negative contribution

Reject wrong neckline, strap, sleeve, seam, hem, fit, opacity, exposure, completed hidden regions, cleaner fashion styling, enlarged accessories, centered outfit completion, clarified low-legibility construction, or expanded lower torso.

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

In `prompt`, select only the macro action and decisive P0/P1 relations from the list below. Group non-material joints, fingers, coordinates, and hidden mechanics; never complete them for checklist coverage. Use exhaustive axis disposal only in `audited`.

- crop, visible parts, negative space, and useful landmarks
- head/chin/gaze/neck; shoulder line, torso twist/lean, action line, and weight distribution
- support plane, torso/center-of-mass side of nearby boundaries, and crossings
- arm/elbow/forearm/wrist; hand/finger/grip/contact; visible leg/knee/foot placement

For side/back, over-shoulder, profile-glimpse, or partly turned human poses, preserve asymmetry separately from category labels. State which side profile, shoulder edge, torso twist, cropped limb, visible side/back/front plane, and hidden planes are present. Avoid summarizing as `back view`, `rear view`, `over shoulder`, or a generic fashion pose if that would square the body to camera, lose the visible face/profile evidence, or complete hidden regions.

Treat pose, hand placement, and occlusion as independent from a person-aesthetic anchor. Keep them protected unless the anchor explicitly intends `pose-occlusion`, cites P0/P1 evidence, and decomposes into this module's control. Emit the material pose result before the appearance passage so aesthetic wording cannot silently frontalize, straighten, or restage it.

For contact gestures, describe the contact as a spatial relationship:

- participating elements, exact regions, size/angle, and visible endpoints
- contact point, compression, overlap, hidden portions, and element extent
- subject zones on either side of the contact boundary
- pinch gap, tension, pressure, load-bearing, stabilization, or passive touch only when visible

Do not infer that a touched element carries body weight. When a structure or edge divides space, keep the torso and center of mass on the source-visible side unless the image clearly shows a crossing, straddling, hanging, or suspended pose.

If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

## Optional negative contribution

Reject mirrored or generic pose, changed head/shoulder/torso/limb/hand relations, malformed grip or fingers, moved contact, wrong boundary side, invented load/crossing/tension, extended parts, or revealed occlusion.

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
