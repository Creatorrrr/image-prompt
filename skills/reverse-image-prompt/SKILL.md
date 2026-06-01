---
name: reverse-image-prompt
description: Reverse engineer a faithful standalone English text-to-image prompt from a provided or attached image using a compact core plus routed subject, medium, relationship, and detail-risk modules. Use when the user asks to analyze a reference image, extract or reconstruct an image-generation prompt, create a GPT Image 2 prompt, write a negative prompt, or produce recommended generation settings from visible image evidence.
---

# Reverse Image Prompt

## Purpose

Create a text-only image generation prompt from one provided image. The prompt must stand alone without the original image attached and should maximize reproducibility of the source image's visible composition, subject appearance, pose, crop, camera treatment, lighting, background, color, medium, and artifacts.

Preserve the source image, not a corrected, beautified, safer-looking, more modest, more sexualized, more cinematic, more polished, more generic, or more socially normalized version of it.

This skill is modular. Use this root `SKILL.md` as the mandatory router, then load the relevant `modules/*.md` files after detecting visual facets. Do not treat the image as belonging to exactly one category; combine subject, medium, relationship, capture-quality, and detail-risk facets.

## Required Module Loading

Always apply and read the complete Tier 0 core:

- `modules/core.visual-evidence.md`
- `modules/core.frame-coordinates.md`
- `modules/concept.primary-relationship.md`
- `modules/core.fidelity-discipline.md`
- `modules/core.background-color.md`
- `modules/core.pre-emit-gate.md`
- `modules/core.output-contract.md`

`concept.primary-relationship` is intentionally still named as a concept module for compatibility, but it is Tier 0 and functionally core.

If sibling files are available, you MUST read the exact contents of every selected module file before drafting `PROMPT:`, `NEGATIVE PROMPT:`, or `RECOMMENDED SETTINGS:`. Do not rely on this router summary as a substitute for module contents. If module files cannot be read in the runtime, use `SKILL.compiled.all.md`; profile bundles are optimization aids, not the safest fallback.

## Workflow

1. Inspect only the provided image.
   - If the image is attached in the conversation, visually analyze it directly.
   - If the user provides a local path, use local image inspection when available.
   - If no image is available, ask the user to attach or provide the image.
   - If multiple images are provided and the user asks for one prompt, ask which image to use or process each image independently if the request clearly allows multiple outputs.

2. Do not use external identity or metadata assumptions.
   - Do not identify or name real people, celebrities, copyrighted characters, brands, artists, exact cameras, exact lenses, exact film stocks, or exact private identities.
   - Use only visible evidence.
   - If a detail is ambiguous, write `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, `ambiguous`, `low-confidence`, or `indistinct`.

3. Silently analyze in this order:
   1. Primary visual concept, perceived intent, and perceptual relationships.
   2. Composition, actual source frame ratio, orientation, crop, subject scale, frame placement, spatial layout, and normalized coordinates.
   3. Visible subjects and their image-plane roles.
   4. Pose mechanics, gesture, limb or object placement, negative space, occlusion, completion-prone regions, and crop boundaries.
   5. Camera distance, height, angle, lens impression, perspective distortion, focus, blur, camera shake, and optical behavior.
   6. Lighting direction, atmosphere, color grading, contrast, highlights, shadows, flash behavior, and lighting-to-volume effects.
   7. Background zones, palette, color massing, depth layers, and environmental details.
   8. Medium, texture, grain, noise, compression, imperfections, rendering artifacts, UI overlays, and text marks.

4. Build an internal facet map, resolve modules from `manifest.json` / `modules/_registry.md`, read those module files, then merge their rules using the conflict priority below. Do not print the facet map unless the user asks for diagnostics.

5. Output only the required sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

6. Report prompt-only limits honestly when exact crop, pose, facial appearance, background fragments, UI/text placement, or small low-legibility details are unlikely to be reproduced from text alone.

## Facet Router

`manifest.json` and `modules/_registry.md` are generated from module frontmatter and are the canonical registry. The router uses these tiers:

- Tier 0: always-on core.
- Tier 1: concept and relationship modules. If the relationship is visible, load every applicable concept module, even when several apply.
- Tier 2: subject and medium modules.
- Tier 3: detail-risk modules.
- Tier 4: narrow style modules.

Use this internal facet shape:

```yaml
detected_facets:
  subjects: []        # human, animal, product, food, architecture, landscape, vehicle, document/data, generic-object/none
  medium: []          # photographic, screenshot-ui, non-photographic, unspecified
  relationships: []   # ordinary, occlusion, replacement, reflection, screen-frame-within-frame, scale-miniature, mixed-media
  capture_quality: [] # low-quality, compressed, underexposed, motion-blurred, flash, casual-phone
  detail_risks: []    # face, body-silhouette, clothing, hands, text-logo, UI, small props, cropped edges
  style: []           # stylized-character-maturity or other narrow style risks
```

Routing rules:

- Always load all Tier 0 modules.
- Always evaluate the relationship facet. Load all detected Tier 1 concept modules; concept-critical relationships outrank subject labels.
- Select at least one medium. If the medium is unclear, load `medium.unspecified-visual`, not `medium.photographic-capture`.
- Select at least one subject decision. If no subject module fits, load `subject.generic-object` to preserve an ordinary object/scene/none decision without inventing a category.
- Apply dependencies from the manifest after initial selection. Examples: `medium.screenshot-ui` pulls `concept.screen-frame-within-frame` and `detail.text-logo-label`; `subject.document-data-diagram` pulls `detail.text-logo-label`.
- Human images with visible hands, clothing geometry, or body-silhouette drift risk should add the corresponding detail-risk modules; do not rely on `subject.human` alone.
- Usually select 3-8 modules beyond the core, but do not omit a concept-critical relationship module to stay under budget.

## Conflict Priority

Resolve conflicts in this order:

1. Safety, visible-evidence limits, and no external identity assumptions.
2. Primary visual concept and perceptual relationship.
3. Actual source frame ratio, crop, normalized coordinates, boundary artifacts, and visibility budgets.
4. Occlusion, reflection, screen/frame, replacement, scale, seam, continuity, and completion logic.
5. Subject-specific fidelity: face, body silhouette, product geometry, animal anatomy, food texture, architecture, landscape, vehicle form, diagram layout.
6. Medium and capture fidelity: camera, focus, lighting, UI overlay, rendering style, compression, noise.
7. Background, palette, color massing, and secondary object budgets.
8. Aesthetic shorthand and generator convenience terms.

Broad labels such as `portrait`, `beauty shot`, `product shot`, `landscape`, `fashion`, `anime`, `cinematic`, `studio`, `luxury`, or `high quality` are allowed only after source-specific crop, relationship, medium, and visibility constraints are established. If a broad label conflicts with coordinates, crop boundaries, occlusion, completion logic, background/color evidence, or source fidelity, weaken or omit the label.

## Output Requirements

Final output must be in English and must include only:

```text
PROMPT:
...

NEGATIVE PROMPT:
...

RECOMMENDED SETTINGS:
...
```

The `PROMPT:` body must carry all non-negotiable constraints in affirmative language. Do not rely on `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:` for essential crop, occlusion, boundary, identity-limitation, face, clothing, object, UI, background/color, or medium constraints.
