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


---

# Distributed analysis orchestration reference

# Distributed analysis orchestration

Use this contract after facet/module routing and before the salience plan. The existing `modules/*.md` files remain the only domain-analysis source of truth; lane files own separation of responsibility, inputs, outputs, and completion gates.

## 1. Build the route

Resolve modules first, then produce `reverse-image-analysis-route/v1` with `tools/route_resolver.py --analysis-route`. Routing is shallow: it selects analysis lanes but does not make visual conclusions. A non-core module that reaches no lane is a visible route failure.

Use three to five material lanes for an ordinary image; do not create one worker per module. `lane.global-composition` is always required. Other lanes activate from the selected modules.

## 2. Isolate lane analysis

When the host supports delegation and the user permits it, run all required lanes concurrently in separate clean contexts. Each worker is read-only and receives only:

- the exact same source bytes or accessible artifact plus SHA-256;
- the raw user request and resolved intent mode;
- the route fingerprint;
- its complete lane file;
- its route-assigned modules, including required common modules; and
- the `reverse-image-analysis-lane-report/v1` schema below.

Do not pass another lane's report, an expected conclusion, a failure diagnosis, a prior prompt/render, a preferred label, or main-session draft prose. A worker must not edit the skill, author the final prompt, generate an image, or delegate again.

If delegation is unavailable, process the same lanes sequentially into the same report schema. Finish and freeze each report before starting the next; do not feed earlier conclusions forward. Mark `execution.mode=sequential-fallback` and every report `independent_context=false`. This preserves coverage, not independence.

## 3. Lane report schema

Each lane returns one compact JSON object:

```json
{
  "schema_version": "reverse-image-analysis-lane-report/v1",
  "route_fingerprint": "...",
  "lane_id": "lane.subject-appearance",
  "source_artifact": {"sha256": "...", "frame": "1024x1280"},
  "execution": {"mode": "delegated", "independent_context": true},
  "status": "complete",
  "reviewed_modules": [{"id": "subject.human", "version": 15}],
  "topic_dispositions": [
    {"topic": "appearance-drift-risk", "disposition": "analyzed", "finding_ids": ["lane.subject-appearance:f1"], "reason": ""}
  ],
  "findings": [
    {
      "id": "lane.subject-appearance:f1",
      "owner_key": "human-visible-gestalt",
      "scale": "regional",
      "axis": "form",
      "observation": "source-relative observation",
      "source_evidence": ["visible cue"],
      "confidence": "medium",
      "causal_origin": "intrinsic",
      "materiality": "material",
      "proposed_role": "primary",
      "default_drift_risk": "high",
      "confounders": []
    }
  ],
  "control_requirements": [],
  "omission_checks": [],
  "handoffs": [],
  "conflicts": []
}
```

Every required topic is disposed as `analyzed`, `not-material`, `uncertain`, or `blocked`. Findings use source-relative observations, not final prompt excerpts. There is no fixed finding count. Human appearance findings are non-identifying generation approximations; factual identity or nationality requires user/trusted metadata outside image inference.

## 4. Integrate by owner key

The main session combines reports into one `reverse-image-analysis-bundle/v1`; it does not concatenate their prose. Merge by `owner_key`, semantic axis, region/subject, causal owner, direction, and role. Keep one final invariant/control owner per material effect.

Every finding is disposed exactly once as `retained`, `merged`, `diagnostic-only`, `rejected`, or `uncertain`. `rejected` and `uncertain` require reasons. A material primary finding may not be dropped or demoted; it must reach a primary final invariant, or integration remains incomplete. Embed the reconciled plan as `integrated_plan.payload` and record the SHA-256 of its canonical JSON as `integrated_plan.sha256`. Every retained or merged `final_invariant_id` and `final_role` must exist unchanged in that hash-bound plan.

Treat these as material conflicts: opposite directions for one owner key; competing causal owners for one effect; primary-to-supporting demotion; intrinsic-versus-induced attribution disagreement; or a broad label that adds unsupported content. Resolve obvious duplicates and lane ownership mechanically. Send only the unresolved issue and source evidence to a separate clean-context adjudicator. Do not vote; preserve `uncertain` when evidence does not decide.

## 5. Independent coverage review

After integration, give an independent read-only critic the raw request, exact source/hash, route, compact reports, and integrated plan—without the main reasoning transcript. The critic reports only `route-gap`, `topic-gap`, `merge-loss`, `unsupported-addition`, `ownership-conflict`, `role-strength-drift`, `scope-leakage`, or `unresolved-uncertainty`.

The critic binds its report to the same source SHA-256, route fingerprint, and integrated-plan SHA-256 and lists every reviewed finding and plan-invariant ID. It returns `pass`, `revise-route`, `revise-integration`, or `blocked`; it neither edits the plan nor writes prompt prose. Do not freeze the prompt before an independent critic returns `pass`, including under sequential fallback. A `revise-route` result adds the missing lane and reruns it; `revise-integration` repeats the merge. Persist route, reports, adjudications, critic result, plan, and prompt as distinct evidence when generation or evaluation is requested.

## 6. Validation and evidence boundary

Validate the bundle with `tools/analysis_bundle.py`. The validator proves route/report coverage, source/route/plan hashes, finding-to-plan invariant binding, independence claims, role continuity, conflict adjudication, and critic gating. Validate the embedded plan separately with `tools/salience_plan.py`; the bundle checker does not prove either plan semantics or visual correctness. Package validity, lane coverage, salience-plan validity, prompt fidelity, delivered pixels, and user judgment remain separate evidence layers.


---

# Included analysis lane: `lane.global-composition`

# Analysis lane: global composition

## Role

Own the image-wide proposition, frame, crop, major-region hierarchy, and dominant fidelity mode. Apply the assigned core modules; this file does not redefine their visual rules.

## Input boundary

Read only the raw request, intent mode, exact source artifact and hash, route fingerprint, this lane contract, and the route-assigned modules. Do not receive another lane's findings or a draft prompt.

## Output contract

Return one `reverse-image-analysis-lane-report/v1` object. Record source observations, material findings, uncertainties, omission checks, and handoffs under the owned sections. Propose control requirements, not final prompt prose.

## Completion gate

Dispose every required topic, review every assigned module, retain source uncertainty, and report cross-lane dependencies without resolving them by assumption.


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
- Describe which evidence occupies the frame zones, including any material source-visible axis offset.

## Major-region hierarchy

Map the few largest visually coherent regions as a major-region hierarchy before local detail. Record relative area, role, attention, legibility, and frame contact without fixed percentages.

Preserve region-share hierarchy when flexible pose, viewpoint, or placement changes; exact coordinates may move.

## Spatial language

Before drafting, give each material placement, principal axis, viewpoint, and cross-component dimension a direction-neutral disposition. Placement never proves orientation; require separate axis, side-visibility, occlusion, depth-order, silhouette, or perspective cues. Centered may be oblique and offset may be frontal.

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

Merge synonymous non-color and non-light pulls into one source-relative aggregate effect with one claim and control.

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
- Give each generic effect one claim and exact prompt control; keep specialized ledgers separate.

### Net salience

- Audit semantic salience amplification across exact repeats, synonyms, paraphrases, labels, negatives, and settings; a repeatedly described dimension gains visual priority even when no sentence is duplicated verbatim.
- Compare each slot's aggregate direction and strength with its source target. Plausible cues still fail when combined too strongly.
- Correct an overstrong draft by replacing or deleting the amplifying language, not by appending a negative counterweight. Keep one distinct high-risk boundary per slot.
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
- For every routed human, require explicit person-prior and skin-surface decisions. Emitted priors need visible geometry; emitted controlled descriptors must deterministically wrap separately owned axes. Friendly metaphors remain explanation-only without exact generator/version evidence.
- Check global cast against reliable neutral or multi-region evidence; otherwise retain uncertainty.

### Lighting and light-to-form consistency

- For material lighting, verify one source-relative Light/Form target and evidence for every emitted source-geometry, fill, local-form-contrast, shadow-topology, material-response, or background-spill contribution.
- Assign every lighting-changing phrase to one Light/Form owner. Split multi-owner compounds.
- Keep global tonal range and local form contrast as separate effects. Merge synonymous directions.
- Give every material shadow event a source-supported owner or mark it mixed or uncertain. Do not infer source direction from contact, occlusion, absorption, or processing.
- The visible spatial result outranks a rig hypothesis; a low-confidence cause cannot carry a primary invariant alone.
- Reconcile every exact lighting-changing excerpt with one emitted claim, one owner, and its complete lighting-effect list. Keep spatial Light/Form effects separate from Color/Tone.
- Keep controlled lighting summaries diagnostic. Emit one externally sourced label only with compatible axes, exact generator/version calibration, and literal decomposition.
- When pose or geometry may vary, preserve the source-supported light-to-form relation while allowing non-invariant highlight coordinates to move.

### Spatial and fidelity checks

- Audit coordinate contradictions before emitting. Then audit `spatial-orientation/v2`: placement cannot cover orientation; human subaxes need cue-linked dispositions and a neutral-alignment counterfactual. Invariants need a full relation/control path; non-invariants need a preservation or visibility reason and emit nothing. Delete unsupported axial normalization by net clause meaning, not a word blacklist.
- Relate every major component or coherent group to another component or stable zone. Make inversion-prone side, contact, support, containment, and depth order explicit; distinguish 2D overlap from scene-space contact.
- Preserve the relative area and attention order of major regions. Keep partial or edge-adjacent bodies, garments, objects, reflections, screens, posters, and text blocks incomplete.
- Confirm that detail has not increased subject scale, sharpness, background legibility, retouching, contrast, lighting polish, or a category's default silhouette beyond the source.
- Retain scale-appropriate face evidence: selective likeness anchors when readable, only orientation, hair mass, tone, and visibility when small or obscured.
- Remove unsupported camera, lens, identity, brand, artist, hidden-content, and quality assumptions. Report prompt-only limits honestly; before generation, audit the reconciled plan and final prompt; separate setting and pixel evidence.

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

Give each generic aggregate effect one emitted claim and exact control. Emit only invariant spatial decisions, once per causal control axis; keep every other disposition non-emitted.

Placement controls position, scale, and frame share. Put material human pose before face, hair, and clothing, which inherit rather than replace it.

When color or tone is material, assign each emitted control to one causal layer and one perceptual effect budget. Use source-relative value, chroma, and hue; keep intrinsic surface, illumination, global cast, exposure, processing, and hierarchy consistent.

Keep supported surface, illumination, global response, and processing distinct. Trace every color-changing phrase to the final ledger; a metaphor cannot add direction.

Place one compact color-tone passage early when primary; when supporting, use the smallest relational control. Hierarchy normally owns area, value, chroma, or contrast, not repeated surface hue.

When lighting is material, assign each emitted control to one Light/Form owner and source-relative effect budget. Keep source geometry, apparent size, fill, local contrast, shadow topology, material response, and spill separate; generic adjectives cannot own several.

Lead with the visible result; add physical cause only at supported confidence. Reconcile every exact lighting-changing phrase with one ledger owner and complete effect list. The ledger is internal, not output prose or grounds for repetition. Keep spatial illumination there and displayed color, exposure, and tone response in Color/Tone. Controlled summaries stay diagnostic. An externally sourced friendly label may appear once only after compatible-axis and exact generator/version calibration, immediately before its literal decomposition.

Use compact blocks without a fixed cap; every clause adds a control. Keep essential spatial axes distinct and affirmative.

For a high-salience look, put one supported Aesthetic Signature before inventory; for a neutral look, use one or two cues. Preserve major-region area, role, edge contact, legibility, and attention.

When face likeness is selected, use one scale-appropriate passage; a gestalt anchor cannot replace visible geometry or raise polish. Retain provenance and visible-geometry evidence for any broad human prior.

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
