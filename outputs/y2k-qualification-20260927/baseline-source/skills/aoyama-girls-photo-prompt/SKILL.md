---
name: aoyama-girls-photo-prompt
description: "Turn short Korean or English keywords into detailed, generator-ready photographic prompts built around theme, subject individuality, symbolicity, relational distance, meaningful framing, and transitional action. Use for a single image, a 6-10 image series, a meaning-led detail image, or revision of a generic portrait prompt; render only when the user requests an image."
---

# Aoyama Girls Photo Prompt

Convert sparse keywords into a photographic proposition, not a longer adjective list. The finished image should answer: who is being seen, where, from whose emotional position, and why this moment matters.

Treat the user's wording as the authored core. Preserve explicit people, places, relationships, actions, objects, mood, crop, lens, and aspect ratio. Fill only open dimensions, label consequential assumptions, and never replace a concrete request with a house style.

## Select a mode

- single: one independent image. This is the default.
- series: a coherent 6, 8, or 10 image sequence.
- parts: one meaning-led detail or partial-frame image.
- revise: diagnose and rewrite an existing prompt.
- compact: one generator-ready English paragraph plus a negative prompt.

Do not ask for a mode when the request makes it clear. If details are sparse, make restrained assumptions and proceed unless two choices would produce materially different work.

## Load only the needed references

Always read:

- [01-methodology.md](references/01-methodology.md) for the governing photographic philosophy.
- [02-keyword-brief-engine.md](references/02-keyword-brief-engine.md) for keyword interpretation and theme selection.

Then route by mode:

- single or compact: read [03-composition-camera-light.md](references/03-composition-camera-light.md), [04-prompt-compiler.md](references/04-prompt-compiler.md), and [06-quality-control.md](references/06-quality-control.md).
- parts: read the same three files, applying the parts rules in the composition reference.
- series: additionally read [05-series-and-selection.md](references/05-series-and-selection.md).
- revise: read the methodology, composition, compiler, and quality-control references; preserve the source prompt's authored core while repairing only the stated problem.

Use [keyword-to-prompt-examples.md](examples/keyword-to-prompt-examples.md) only when an example materially helps resolve ambiguity. Acceptance behavior is recorded in [acceptance-cases.md](tests/acceptance-cases.md).

## Core workflow

1. Normalize the keywords without polishing away literal anchors.
2. Separate locked facts from open dimensions and inferred assumptions.
3. Extract person, place, viewer relationship, action, object, mood, temporal state, and technical requests.
4. Propose three theme sentences and score them for necessity, individuality, relationship, transition, visual clarity, and restraint.
5. Select a state A to state B transition. Prefer just-before, mid-action, or just-after moments over a finished pose.
6. Define the viewer's role and translate physical camera distance into psychological distance.
7. Choose three memorable individuality anchors. Discover them additively; do not define the subject through generic perfection.
8. Build SIR: Symbolicity, Individuality, and Relationship. Make at least two axes legible in one image and all three across a series.
9. Select one meaning core: a gesture, object interaction, expression change, or detail that compresses the theme.
10. Expand the frame only while each added cue contributes more meaning than distraction.
11. Apply a place-and-prop information budget. Prefer use marks and lived relationships over decoration.
12. Derive focal length, aspect ratio, viewpoint, depth of field, light, exposure, and texture from the theme.
13. Compile a clean English final prompt and a scene-specific negative prompt. Do not use a photographer's name as a style token.
14. Score the draft with the 100-point rubric and revise weak dimensions before delivery.
15. If the user requested image generation, render the audited prompt, inspect the returned pixels against the brief, and report the saved workspace path.

## Output contract

For single and parts modes, return:

1. Interpreted theme
2. Assumptions, only when used
3. Viewer role and psychological distance
4. SIR visual anchors
5. Composition, lens, aspect-ratio, and light rationale
6. Final Prompt in English
7. Negative Prompt for this scene
8. Directorial Controls for iteration

For compact mode, return only the Final Prompt and Negative Prompt unless the user asks for rationale.

For series mode, follow the series reference and include the series thesis, continuity lock, frame plan, per-frame delta, shared negative prompt, and final sequence.

For revise mode, identify the small number of causes of the stated failure, then return the repaired prompt and controls. Avoid rewriting unrelated choices.

## Rendering boundary

Writing and auditing a prompt is preflight evidence. It is not a generated-image result.

When rendering is requested:

- Use the final positive and negative prompt without changing their meaning.
- Keep the requested single/series count exact.
- Save selected project-bound outputs under the workspace without overwriting an existing file.
- Inspect subject, relationship, action phase, meaningful anchors, room or place necessity, composition, and obvious image defects.
- Report any mismatch plainly; do not claim pixel fidelity from a prompt-only check.
