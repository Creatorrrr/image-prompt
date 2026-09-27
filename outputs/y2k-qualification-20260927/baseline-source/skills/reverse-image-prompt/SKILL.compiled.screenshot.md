---
name: reverse-image-prompt
description: Reverse engineer a standalone English text-to-image prompt from a provided image using visible evidence, routed subject/medium/relationship modules, and an adaptive model-aware output contract. Use for faithful reconstruction, semantic prompt extraction, polished-but-composition-faithful variants, diagnostic image analysis, negative prompts, or generation settings.
---

# Reverse Image Prompt

## Purpose and task scope

Turn one image into a standalone English text-to-image prompt preserving its primary perceptual proposition, composition, visible relationships, form, surface, light, color, medium, crop, and meaningful imperfections. Default to faithful reconstruction.

First distinguish image work from maintenance of this skill. For structure review or revision, inspect the requested files and `references/behavior-evaluation.md`; an image is required only for an image-dependent test. For image work, inspect the exact attached/local source. Ask for a missing source only when the requested result depends on it. Process multiple images independently unless the user asks to combine them. User instructions determine the task scope and take precedence over skill defaults.

## Intent and analysis profile

Infer intent from the request; clarify only when materially different outcomes cannot be resolved from context:

- `faithful` (default): preserve visible composition, relationships, and imperfections.
- `semantic`: extract transferable concept/composition/style, omitting incidental defects.
- `polished-fidelity`: improve only the requested defects while retaining concept and composition.
- `diagnostic`: explain visible evidence, uncertainty, and reproduction limits.

Choose analysis depth separately:

- `prompt` (default for extraction or diagnosis): one routed lane wave, compact-v2 P0/P1 evidence, compressed P2, grouped P3, one critic, at most one targeted repair.
- `audited`: actual generation, source/render or measured fidelity evaluation, or an explicit evidence audit. Use complete atomic obligations and versioned ledgers. Skill structure review alone does not start an image audit.

A human, readable face, complicated scene, or desire for more detail does not itself require `audited`. A compact analysis may escalate for an unresolved P0/P1 conflict that cannot be represented honestly.

## Read only the selected execution contract

Tier 0 always applies: `core.visual-evidence`, `core.frame-coordinates`, `concept.primary-relationship`, `core.fidelity-discipline`, `core.background-color`, `core.pre-emit-gate`, and `core.output-contract` in `modules/`.

When tools are available, read the complete **selected-profile view** of assigned files:

```bash
python3 tools/profile_context.py --analysis-profile prompt --files modules/core.visual-evidence.md modules/core.frame-coordinates.md modules/concept.primary-relationship.md modules/core.fidelity-discipline.md modules/core.background-color.md modules/core.pre-emit-gate.md modules/core.output-contract.md references/analysis-orchestration.md
```

Use `audited` instead when selected. The reader preserves all shared text and excludes only explicit other-profile blocks; it fails if an input is unreadable or a marker is malformed. Do not heuristically skip paragraphs. The returned source/view hashes identify the instructions actually read. Without execution tools, read the files fully and respect the explicit profile boundaries. If sibling files are unavailable, use the smallest matching `SKILL.compiled.*.md` fallback; the all-module bundle is the final fallback and carries both profiles.

Resolve facets through `manifest.json` or `modules/_registry.md`. Every lane reads its lane file plus its complete assigned module views. The integrator reads Tier 0, the selected orchestration/integration views and lane reports; reopen other modules only for a declared conflict or audit.

Conditional references:

- Named downstream generator: `references/model-adapters.md`. It owns supported tool settings and formatting, while core salience and causal order remain authoritative.
- Analysis harness/model binding or execution telemetry: `references/analysis-runtime.md`. Analysis configuration is separate from generator settings and never enters the production prompt.
- Selected color or lighting fidelity with measurement, controlled revision, generation, or source/render comparison: `references/color-reproduction-evaluation.md` or `references/lighting-reproduction-evaluation.md`.
- Measured surface vocabulary or a surface descriptor/label: `references/surface-color-language.md`. Composite/friendly lighting language: `references/lighting-language.md`. Use current-source axes and explicit provenance; never start from a preferred label or demographic proxy.
- Skill evaluation/revision: `references/behavior-evaluation.md`.

## Route and analyze

Inspect visible evidence before domain conclusions. Never infer identity, protected categories, metadata, artists, cameras, lenses, brands, or hidden content from appearance. Keep externally supplied context separate. In final prose describe visible ambiguity (`indistinct`, `partially obscured`, `soft-edged`) rather than repeated epistemic qualifiers.

Build a source-supported facet map:

```yaml
detected_facets:
  subjects: []
  medium: []
  relationships: []
  capture_quality: []
  detail_risks: []
  style: []
```

```bash
python3 tools/route_resolver.py --facets '<JSON>' --analysis-route --analysis-profile prompt
```

Choose subject and medium, all material visible relationships, and only material detail/style risks. Readable/prominent faces route `face-detail`; body-form, color-tone, and lighting fidelity route only when first-order or explicitly prioritized. Ordinary relationships, cropped edges, and small props are core-handled. The normal non-core module maximum is eight. If all excess risks are material, report the coverage limit rather than silently dropping one. The resolved route is authoritative for lane count; currently three to six lanes may activate.

When clean-context delegation is available and permitted, run required lanes as one read-only wave, concurrently up to available capacity. Queued lanes still receive fresh contexts. Each receives the same source bytes/hash, raw request, intent, route/profile/budget, its lane file and assigned module views, and report schema. Do not supply another lane's conclusions, prior prompts/renders, or preferred wording. Workers do not write files, generate, author final prompts, or delegate again.

If isolated delegation is unavailable, freeze each sequential report and mark `sequential-fallback`; do not claim independence. A malformed lane may be retried once; a route gap/source mismatch may reroute the affected work once. Never rerun a successful lane for extra detail. Use a compact report's structured P0/P1 handoff to close an absent causal owner, lane, or required module before integration.

## Integrate, check, and emit

Read the selected view of `references/integration-contract.md`. Preserve the smallest P0/P1 causal cue set, merge useful P2, omit P3. Integrate by owner and visible effect, never by report length or prose concatenation. One supported aggregate descriptor may lead its immediately owned decomposition; it cannot introduce an unowned appearance, pose, crop, light, color, or polish change.

The output contract owns semantic order: source signature and structural identity first, with camera/crop and pose before dependent Light/Form. Generator formatting cannot move background or incidental inventory ahead of those controls. Compile source-relative analysis vocabulary into literal viewer-relative placement, geometry, displayed surface, and lighting targets.

Validate compact reports with `tools/compact_reports.py`. Run one source-aware critic as specified in the orchestration contract and apply at most one targeted repair. Independently check the exact production text with:

```bash
python3 tools/prompt_lint.py PROMPT.txt
```

This narrow text check needs no plan/image and does not prove semantic or visual fidelity. The source-aware critic also evaluates standalone meaning; a same-context reread is not a claim that the critic has forgotten the image. Report unresolved P0/P1 limitations rather than starting another refinement cycle.

For `audited`, persist the validated bundle, reconciled plan, exact production prompt/hash, settings/reference handling, and attempt log before generation. Run `tools/analysis_bundle.py` and `tools/salience_plan.py PLAN.json --prompt PROMPT.txt`. Apply full obligation, spatial-orientation/v6, human-appearance/v3, Color/Tone and Light/Form checks where required; only audited work reconciles every literal control and qualified summary. Freeze after successful validation and critic review. Ordinary prompt-only extraction needs no full ledgers.

Always produce English `PROMPT:` for generation requests. Emit `NEGATIVE PROMPT:` only when requested or separately supported by the generator; emit settings only when requested or needed for a known generator/size handoff. Essential crop, topology, occlusion, medium, hierarchy and fidelity constraints belong in the positive prompt. Diagnostic explanation follows the user's language and names the visible proposition before causal details.

The prompt must stand alone after the image, analysis, conversation, and optional sections disappear. `Keep`, `preserve`, `retain`, `remain`, and `stay` may govern a fully named visible state; they cannot refer outside the prompt. Keep package validity, prompt fidelity, delivered pixels, pixel fidelity, and user judgment separate.


---

# Distributed analysis orchestration reference

# Distributed analysis orchestration

Use this contract after facet/module routing and before prompt drafting. Domain evidence still comes from the selected `modules/*.md`; lane files define independent ownership and reporting.

## 1. Choose an analysis profile

Resolve `reverse-image-analysis-route/v2` with `tools/route_resolver.py --analysis-route --analysis-profile PROFILE`.

- `prompt` is the default for an ordinary one-image prompt or diagnosis. It preserves separate lane analysts and an independent critic, but collects only viewer-material evidence.
- `audited` is for actual source/render evaluation, measured fidelity work, skill evaluation, or an explicit request for a full evidence ledger. It retains `reverse-image-analysis-lane-report/v2`, `spatial-orientation/v6`, `human-appearance/v3`, and `reverse-image-analysis-bundle/v2`.

Do not enter `audited` merely because a human, readable face, complicated scene, or routed detail module is present. Escalate only when the task requires audited evidence or the compact profile reports one unresolved P0/P1 conflict that cannot be represented honestly.

Both profiles use the same source-routed lane set (currently three to six lanes). `lane.global-composition` is always required. A non-core module that reaches no lane is a visible route failure.

## 2. Run one isolated lane wave

When clean-context delegation is available and permitted, run all required lanes concurrently. Respect available worker capacity: lanes in the same logical wave may queue, but each starts with a fresh context. Queueing is not a retry or another analysis wave; never reuse a previous lane's transcript. Each read-only worker receives only:

- the same source artifact and SHA-256;
- raw request and resolved intent;
- route fingerprint, analysis profile, and execution budget;
- its lane file and complete route-assigned modules; and
- the profile's report schema.

Do not pass another lane's result, a preferred conclusion, previous prompt/render, or draft prose. Workers do not write files, generate, author the final prompt, or delegate again.

If delegation is unavailable, freeze each report before starting the next and mark `sequential-fallback`; do not claim independence. Do not rerun a successful lane to seek more detail. A missing or malformed report may be retried once for that lane only; source/hash mismatch or an actual route gap may restart the affected route once.

<!-- profile:prompt -->
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
        "scope": "human-appearance",
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

`aggregate_descriptor_candidate` is optional and case-bound. New candidates name `scope: general | human-appearance`. When scope is absent in an older report, assignment of `subject.human` requires the human effect budget; an explicit general candidate in a mixed lane remains a general claim, and the critic checks whether that scope is truthful. Validate any supplied budget even for general candidates. Include it only when the phrase itself carries a P0/P1 gestalt not preserved by detail alone; its decomposition requirements remain separately owned. A human aggregate additionally declares intended and protected dimensions, always protecting identity context. Exact identity context uses a separate provenance-bound integration handoff (`user-supplied` or `trusted-metadata`, external reference, viewer priority, no pixel inference). Never fill either field from a preferred vocabulary. Split a compact finding only when two visible results can drift independently and both are P0/P1. Otherwise keep the causal result together. Compact reports do not create exhaustive atomic obligations, full color/light ledgers, `spatial-orientation/v6`, or `human-appearance/v3`.

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

<!-- /profile -->

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

<!-- profile:audited -->
## 6. Audited profile

In `audited`, each lane returns `reverse-image-analysis-lane-report/v2`. Every required topic is individually disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`; each material finding is split into independently drifting atomic visible-result obligations. Integrate them into `reverse-image-analysis-bundle/v2`, dispose every finding and obligation once, bind retained obligations through `source_obligation_ids`, and preserve role and causal ownership.

Use `spatial-orientation/v6`, isolated per-axis neutralization evidence, exact explicit/implicit spatial prompt-effect audits, and both human orientation counterfactuals only here. Keep frame and cross-component relation types distinct; a high-degeneracy direction also requires the closed subject/frame, reference/frame, and inter-region placement check. The raw-source critic must independently inspect the complete literal spatial clauses for synonymous or implicit axis pulls; declared audit ids alone are not semantic proof. Use `human-appearance/v3` and full Color/Tone or Light/Form ledgers only here or when the user explicitly requests those measured contracts. After ledger reconciliation, the authored prompt contains no semantic prose outside exact owned controls and qualified summaries. Existing validators remain authoritative:

```bash
python tools/analysis_bundle.py ANALYSIS_BUNDLE.json
python tools/salience_plan.py PLAN.json --prompt PROMPT.txt
```

The audited critic binds to source, route, reports, obligations, plan hash, and the literal prompt. It checks the prompt for unresolved external reference language or unowned semantic residue even when every expected ledger excerpt is present. Run the source-free text checker separately; do not describe a source-aware critic's reread as physically isolated. It may request one targeted integration repair and one verification pass. Only a route gap or source-artifact mismatch may rerun an affected lane. If the repair budget is exhausted, report `blocked`; never start an open-ended refinement loop.

<!-- /profile -->

## 7. Evidence boundary

Route validity, package validity, lane coverage, prompt behavior, delivered pixels, and user judgment are separate evidence layers. A compact prompt can be useful without claiming audited completeness, and an audited bundle can be valid without proving visual fidelity.


---

# Integration and prompt actuation

Read after the lane wave. Use the selected profile view through `tools/profile_context.py`; the shared rules retain visible meaning, while the audited block defines the persisted plan. The core output contract owns order; generator adapters may format controls but cannot reorder their salience or causal dependencies.

5. Integrate the lane reports with an adaptive hierarchy:
   1. Record the direct, source-supported appeal separately from the render contract. State it plainly in diagnostic mode. When an aggregate appeal term is itself a high-confidence P0/P1 source invariant and omission would materially change the reading, retain it once in the generation prompt as a bounded semantic anchor, immediately followed by its visible causal controls. Otherwise keep it diagnostic or translate it without emission.
   2. Classify the dominant fidelity axis as `relationship-led`, `appearance-led`, `information-led`, or `mixed`.
   3. Rank cross-lane evidence by viewer effect: `P0 source signature`, `P1 structural identity`, `P2 supporting`, `P3 incidental`. Any source-specific face, skin presentation, space, clothing, pose, topology, light, color, or capture cue may be P0/P1. Record the smallest causal cue set; module count and raw detail do not set prompt weight.
   4. In `prompt`, preserve one macro spatial result, then hold viewpoint and crop fixed and test whether it carries the source-visible placement, facing, depth-order, pose, topology, support/contact, occlusion, and completion relations that jointly create the read. Mark it sufficient, lossy, or uncertain and retain only decisive P0/P1 at-risk residuals; group the rest. Treat alignment-style wording as positive multi-axis actuation rather than a neutral default, and inspect every exact spatial clause for all explicit and implicit axes it controls. Keep subject-to-frame placement separate from component-to-component orientation. When the latter is material, record not only direction but any independently material proximity, overlap, or surviving-visibility relation; direction alone may remain literally true after an extreme displacement.
<!-- profile:audited -->
In `audited`, build `spatial-orientation/v6`, dispose every required axis, require an isolated per-axis neutralization test before declaring an axis flexible or not-material, run both human counterfactuals, retain coupled-effect summary coverage, and bind every emitted spatial control to a source-consistent prompt-effect audit exactly as specified by the selected modules and evaluation reference.
<!-- /profile -->

   5. Map the few largest coherent image regions by relative area, tonal role, edge contact, legibility, and attention. Record only material component relations: region-to-region or region-to-frame reference, relation kind, source-relative observation, evidence, and role. A frame-placement relation must terminate at the frame; a cross-component relation must terminate at another named region. If a cross-component direction can be satisfied while materially changing distance, overlap, or visibility, close the placement triangle with separate subject-to-frame, reference-to-frame, and inter-region relations, then test a direction-held displacement counterfactual. When one invariant spans multiple regions or visible boundary components, preserve the region-to-region boundary topology instead of collapsing it to a category or one broad edge. When partial visibility matters, record the surviving fragments, cropped or hidden counterparts, and completion risk. For relationship-led or mixed images, map major-component topology, contact/support, containment, boundary crossing, occlusion, and negative space. For appearance-led images, map form, surface, light-to-form, color, material roles, and subject/environment hierarchy first. For information-led images, map layout, reading order, legibility, and container hierarchy first.
   6. Analyze each material human through four independent decisions. First, retain exact race, ethnicity, nationality, or other identity context only when supplied by the user or trusted metadata and P0/P1 for the requested generation; pixels never establish it. Second, decide whether a non-identifying broad person prior is needed to resist model-default drift and immediately correct it with visible geometry. Third, describe displayed skin only as source-visible value/chroma/undertone/finish under the observed capture, with its own priority and region scope. Fourth, when a person-aesthetic or attractiveness reading is itself P0/P1 and omission-sensitive, state one bounded aggregate anchor and immediately decompose only its declared intended dimensions while protecting identity, pose, crop, age presentation, garment coverage, light, color, and polish unless those dimensions are separately source-supported and intentionally owned.
<!-- profile:audited -->
In `audited`, create `human-appearance/v3` with provenance, priority, effect budget, claim/control binding, and skin-region handling.
<!-- /profile -->
 Never install a motivating label or surface combination as a default.
   7. Before treating shape, scale, color, surface, or definition as intrinsic, separate effects caused by pose/deformation, perspective, lighting/shadow, material interaction or occlusion, and capture/processing.
   8. When color/tone is material, `prompt` records only the decisive regional axes, displayed result, protected relation, and uncertainty. Build the full Color/Tone Contract only in `audited`, measured color work, or source/render evaluation. If the draft names displayed key level, shadow floor, highlight rolloff, microcontrast, surface value, chroma, hue, cast, exposure, or processing, route that phrase to an owned Color/Tone control or remove it; a Light/Form or generic clause cannot donate tone ownership.
   9. When light/form is material, `prompt` records one macro visible result before any rig hypothesis, then only independently drifting P0/P1 regional relations the macro loses: target/reference region, bright-plane coverage, local form contrast, gradient extent, shadow topology, material response, background spill, and pose dependency. Split a coarse major region into named Light/Form subregions when one surface contains materially different main plane, shadow zone, transition, or material mass. Give each emitted regional relation exact prompt anchors for both sides. This is a source-driven vocabulary, not a checklist. Build the full Light/Form Contract only in `audited`, measured lighting work, or source/render evaluation.
   10. Add only materially important pose, camera/perspective, focus, lighting, background, medium, texture, artifact, UI, and text evidence.

<!-- profile:audited -->
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
  placement_closures: [] # only when direction can stay true after material proximity, overlap, or visibility drift
  spatial_orientation_coverage:  # required for routed humans and other material orientation-bearing subjects
    schema_version: spatial-orientation/v6
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

<!-- /profile -->

6. Treat selected modules as evidence contributors, not prose entitlements. Merge by owner key, visible effect, direction, region/subject, and causal owner. In `prompt`, retain P0/P1 once, fold P2 into an owned control, and omit P3; only audited work needs complete atomic-obligation and exact-ledger reconciliation. Resolve conflicts and allocate prompt weight in this order:
   1. Visible-evidence and safety limits.
   2. P0 source signature and perceptual proposition.
   3. P1 source-specific appearance, topology, space, information hierarchy, crop, pose, light, color, or capture controls.
   4. P2 support that can be expressed without competing with P0/P1.
   5. Omit P3, flexible inventory, and generic shorthand unless requested.

7. Draft the smallest prompt that carries P0/P1, then only useful P2 support. Put the source-specific signature near the beginning and let order reflect what a viewer notices and would miss first. Use **retain-and-decompose** for material aggregate language: state one evidence-qualified abstract descriptor, then immediately unpack it into owned form, surface, light, color, spatial, hierarchy, or capture controls. Do not use abstraction without controls, and do not assume detailed controls preserve the same global meaning when the omission counterfactual says otherwise. When pose and illumination jointly shape the visible form, order the causal passage as proposition, camera/crop, macro spatial result, at-risk spatial residuals, pose-bound Light/Form relations, surface or garment response, then background/capture; later prose must not normalize an earlier relation. Audit each exact spatial clause as a whole: semantic classes equivalent to centered, frontal, upright, vertical, straight, balanced, or aligned can alter several axes even when only one is named. List those effects as explicit or implicit, and rewrite or remove the clause if any affected axis lacks invariant or coupled ownership. For a human, place material user/trusted identity context once before the appearance passage, keep a broad person prior next to correcting geometry, and let one bounded person-aesthetic anchor lead only its contiguous owned decomposition. State each aggregate once, remove competing normalization instead of adding counter-negatives, and never let incidental inventory or an aesthetic anchor change protected skin, makeup, garment coverage, pose, crop, lighting, or polish. Terms such as `source-relative`, `source-visible`, `source-specific`, `source-supported`, and `current-source` are analysis/provenance vocabulary only. Compile each one into the literal visible target—such as viewer-left placement, a three-quarter head/torso relation, broad highlight coverage, or a named surface value—before it enters `PROMPT:`.
<!-- profile:audited -->
In `audited`, additionally reconcile every atomic obligation and exact generic, Color/Tone, and Light/Form control ledger according to the selected modules. The authored `PROMPT:`, `NEGATIVE PROMPT:`, and settings text may contain only exact owned controls or qualified summaries plus structural labels and punctuation; do not add free semantic bridge prose after ledger reconciliation.
<!-- /profile -->


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

In `prompt`, return `reverse-image-analysis-lane-report/compact-v2`. First decide whether orientation or topology is P0/P1. If so, report one macro, then hold viewpoint and crop while testing its source-visible component, frame, facing/gaze, depth, support/contact, boundary, occlusion, and completion relations. Inspect only current-source evidence. Mark the macro `sufficient`, `lossy`, or `uncertain`; retain only decisive P0/P1 residuals. Distinguish region-to-frame position from inter-region direction. Separately disposition material proximity, overlap, and surviving visibility; if direction survives extreme displacement, hand off both frame relations, the inter-region relation, and a direction-held counterfactual. Treat alignment phrases as positive controls over every explicit or implicit axis. Hand off appearance, color, and capture questions structurally.

In `audited`, return `reverse-image-analysis-lane-report/v2`, split independently drifting results into atomic obligations, retain confounded directions, and close every high-degeneracy cross-component placement.

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

<!-- profile:audited -->
- In `audited`, preserve independently drifting material results as atomic obligations; uncertain attribution never erases a supported direction.
<!-- /profile -->


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

In `prompt`, emit one P0/P1 macro plus decisive residuals. Placement proves no orientation. Treat alignment wording as positive control and enumerate every affected axis.

<!-- profile:audited -->
In `audited`, disposition every axis. `flexible` or `not-material` needs isolated neutralization; uncertain evidence stays uncertain unless coupled. Run both human counterfactuals, merge joint effects once, and block unowned spatial pulls.
<!-- /profile -->

## Relational coordinate frames

- Frame placement references the frame. Cross-component placement references another region and separates direction, proximity, overlap, and surviving visibility.
- If direction survives material displacement, close subject-to-frame, reference-to-frame, and inter-region relations, then test residual drift with direction held.
- Use frame-relative directions for composition and scene-relative zones for physical relations. Qualify viewpoint-dependent sides.
- Establish a visible support plane only when it disambiguates the scene.
- Separate 2D overlap from contact, containment, support, and depth order.
- Prefer stable natural language; coordinates lock frame position, not physical topology.

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
5. Separate aesthetic invariants from flexible dimensions before drafting. An invariant would materially weaken or change the proposition if altered; a flexible dimension may vary without losing it. In `prompt`, retain only the smallest P0/P1 causal set and merge P2 support.
<!-- profile:audited -->
In `audited` only, build the full ledger: Build an invariant salience ledger. Bind retained atomic obligations.
<!-- /profile -->

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
- Audit coordinate contradictions. In `prompt`, a coupled macro is `sufficient`, `lossy`, or `uncertain`; only supported P0/P1 at-risk residuals survive. A missing owner or module is `route-gap`. In `audited`, validate the full spatial contract.
- Treat alignment prose as multi-axis control. Record each exact clause's explicit and implicit effects; rewrite it if any affected spatial axis is unowned. Negatives cannot repair the conflict.
- Frame placement uses a frame reference; cross-component placement uses a region. If direction survives material displacement, require both frame relations plus the inter-region relation and protect proximity, overlap, or visibility.
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

<!-- profile:audited -->
## Audited-only ledger checks

Apply this section only in `audited`, measured fidelity, or source/render evaluation:

- For color/tone, verify each aggregate source-relative target and causal contribution. Trace every required intrinsic axis through same-region/same-axis effect, claim, and axis-control; reconcile each exact excerpt with its layer and full effect budget.
- For Light/Form, verify each target and emitted causal contribution, then reconcile every exact excerpt with one owner and complete effect list.
- Before generation, validate appearance, spatial counterfactuals, exact effect audits, obligation binding, and ledger separation. Mask every owned control or qualified summary in the complete prompt; after structural labels and punctuation, reject semantic residue. Expected excerpts alone do not prove ownership.

<!-- /profile -->

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

- Begin with the perceptual proposition and its material frame shape, medium, and fidelity ceiling; supporting background does not precede P0/P1.
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


<!-- profile:audited -->
In the full contract: For every intrinsic value, chroma, or hue axis, record `role`, `evidence_scope`, and `emission`. Use `required` only when the axis materially needs a final prompt control. Use `diagnostic-only` with a concrete non-emission reason when an axis is low-confidence, incidental, or already unsupported at prompt precision. Link every required intrinsic axis to exactly one same-region, same-axis aggregate effect.
<!-- /profile -->


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

<!-- profile:audited -->
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

<!-- /profile -->

## Cross-layer effect budget

Merge color and tone claims by their shared perceptual effect across causal layers, not only by semantic-slot name.

Give each material effect a source-relative identifier covering region, axis, direction, and aggregate strength. Multiple causal layers pushing one region/axis require independent evidence and one aggregate target.

- Merge unsupported repetition into one owned control.
- Preserve multi-layer color only when every layer and the aggregate result are supported.
- Let hierarchy own relative area, value, chroma, or contrast; let it own hue only when hue contrast is invariant.
- Treat free-floating color or mood words as unowned until assigned to one causal layer.

## Final prompt control ledger


<!-- profile:audited -->
In `audited`, copy every color/tone excerpt into `emitted_controls` with one claim, layer, region, axis, and effect list. Overlapping value/tone controls list `protected_light_effect_ids` and follow the primary light result. A required intrinsic axis needs its own intrinsic axis-control; compounds cannot satisfy it. After reconciliation, remove any final-prompt phrase about displayed key, shadow floor, highlight rolloff, microcontrast, surface value/chroma/hue, cast, exposure, or processing that is absent from the Color/Tone ledger; it cannot survive as generic bridge prose or borrow ownership from Light/Form.
<!-- /profile -->
 In `prompt`, ownership and protected relations are sufficient without duplicating the excerpt in a ledger.

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

- Keep the core output contract's P0/P1 and causal dependency order. Use skimmable blocks within that order; scene/background leads only when it carries the source signature.
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
