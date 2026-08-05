---
name: reverse-image-prompt
description: Reverse engineer a standalone English text-to-image prompt from a provided image using visible evidence, routed subject/medium/relationship modules, and an adaptive model-aware output contract. Use for faithful reconstruction, semantic prompt extraction, polished-but-composition-faithful variants, diagnostic image analysis, negative prompts, or generation settings.
---

# Reverse Image Prompt

## Purpose

Turn one provided image into a standalone text-to-image prompt that preserves the visible concept, composition, crop, subject, pose, major-component spatial relationships, aesthetic signature, camera or rendering treatment, lighting, background, color, medium, and meaningful artifacts.

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

3. Analyze silently in this order:
   1. Primary concept, perceptual relationship, and major-component spatial topology.
   2. Frame ratio, crop, subject scale, major zones, boundary sides, and edge interactions.
   3. Global aesthetic salience and the smallest source-specific look signature.
   4. Visible subjects, their image-plane roles, and—only when it materially reduces ambiguity—a compact broad person-gestalt anchor before local human detail.
   5. Pose, contact/support, containment, boundary crossing, occlusion, completion-prone regions, and negative space.
   6. Camera or virtual-camera behavior, perspective, focus, and blur.
   7. Lighting, atmosphere, color, contrast, highlights, and shadows.
   8. Background zones and depth layers.
   9. Medium, texture, artifacts, UI, and text marks.

4. Build and resolve this internal facet map:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face-detail, clothing, hands, text-logo, ui, small-props, cropped-edges, tight-selfie, face-hand-gesture, accessory-torso-budget
  style: []           # stylized-character-maturity or another narrow risk
```

5. Merge selected rules using this priority:
   1. Visible-evidence and safety limits.
   2. Primary concept, perceptual relationship, and any high-salience aesthetic signature.
   3. Frame ratio, crop, major zones, boundary sides, contact/support relations, and visibility budgets.
   4. Occlusion, reflection, screen/frame, replacement, scale, and continuity.
   5. Subject-specific fidelity.
   6. Medium, camera, lighting, focus, and artifact fidelity.
   7. Background, color, and secondary details.
   8. Generic style or aesthetic shorthand.

6. Draft the smallest prompt that carries every concept-critical constraint. If the source look is high-salience, place one compact Aesthetic Signature near the beginning; if it is neutral, use only one or two ordinary look cues. Give each major component or coherent group at least one explicit spatial relation to another component or stable scene zone. Give each major interaction one relation clause when its side, containment, contact, support, or depth order could otherwise flip. Prefer short labeled blocks or compact paragraphs over a field-completion checklist.

7. Apply the pre-emit gate and report prompt-only limits honestly.

## Routing rules

- Always load Tier 0.
- Select at least one subject and one medium; use the generic/unspecified fallbacks only when evidence is unclear.
- Load every visible Tier 1 relationship module, including both photographic and non-photographic medium modules for genuine mixed media.
- Load Tier 3 and Tier 4 modules only for visible, material risks.
- For a prominent or clearly readable human face, add `face-detail`; for a small, blurred, shadowed, or heavily occluded face, keep only scale-appropriate human evidence and do not invent micro-features.
- Treat the spatial topology of major components as Tier 0 evidence. Do not route it away as an optional detail merely because the scene has no special visual effect.
- Treat adaptive aesthetic analysis as Tier 0 evidence, not as a style preset. Do not load extra style modules merely to fill an aesthetic checklist.
- Keep the normal route within 3-8 non-core modules. Refine an over-budget facet map instead of loading every plausible module.
- Treat `ordinary`, `cropped-edges`, and `small-props` as core-handled observations unless another visible risk requires a dedicated module.
- Do not use broad labels such as `cinematic`, `studio`, `luxury`, `beauty shot`, or `high quality` when they would normalize source-specific evidence.

## Output selection

Always write the production prompt in English. Match the response language for diagnostic explanation unless the user asks otherwise.

- Always emit `PROMPT:` for generation requests.
- Emit `NEGATIVE PROMPT:` only when the user requests it or the named downstream generator supports a separate negative prompt.
- Emit `RECOMMENDED SETTINGS:` only when requested, when a target generator is known, or when source dimensions require a model-specific target-size explanation.
- For `diagnostic` mode, use ordinary analysis headings and include a candidate prompt only if useful.
- Essential crop, relationship, occlusion, high-salience aesthetic, and medium constraints must remain in `PROMPT:` even when optional sections are present.

Do not mention the attached/reference image inside the generated prompt.
