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
