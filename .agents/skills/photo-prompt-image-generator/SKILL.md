---
name: photo-prompt-image-generator
description: Generate image-ready photo prompts and images in this project using the bundled prompt_generator.py and photo_prompt_tags.json. Use when the user asks for random photo prompts, preset-based photo prompts, or image generation from this project's prompt tag dictionary.
---

# Photo Prompt Image Generator

## What This Skill Does

Use this project-local skill to generate a structured photo prompt from the bundled tag dictionary, then call image generation when the user asks for an actual image.

Bundled resources:

- `scripts/prompt_generator.py`: original prompt generator CLI.
- `assets/photo_prompt_tags.json`: original tag dictionary.
- `scripts/generate_photo_prompt.py`: wrapper with project-local defaults.

## Default Workflow

1. Generate one prompt with JSON output:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py
```

2. Use `prompt_en` as the primary image prompt unless the user explicitly wants Korean-only output.
3. If a negative prompt is present, append it to the image request as `Avoid: ...`.
4. Call the available image generation tool with the final prompt when the user asks to create, render, or generate an image.
5. If the user asks only for prompts, return the generated prompt text and do not generate an image.

## Useful Commands

List available presets:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-presets --plain
```

Inspect slots:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --show-slots --plain
```

List tag ids for a slot:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-tags subject --plain
```

Generate a reproducible prompt:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --preset street_documentary --seed 42
```

Force slot selections:

```bash
python3 .agents/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset tiktok_vertical_snapshot \
  --set subject=influencer_creator \
  --set person_origin=south_korea \
  --set appearance_type=idol_like
```

## Prompt Handling

- Prefer `prompt_en` for image tools.
- Preserve user-specified subject, location, format, camera, lighting, mood, and aspect instructions by mapping them to `--preset` or `--set` when an exact tag exists.
- If the user's request includes constraints not represented by tags, generate the closest base prompt and append the constraint in plain language.
- Use `--seed` for reproducible variants.
- Do not edit `assets/photo_prompt_tags.json` unless the user explicitly asks to change the tag dictionary.
- Use `--plain` only for human-readable list commands; normal generation should stay JSON.

## Wrapper Defaults

`generate_photo_prompt.py` defaults to:

- bundled `assets/photo_prompt_tags.json`
- `--n 1`
- `--lang both`
- `--json-output`
- `--include-negative`

Pass `--plain` to disable JSON output. Pass `--no-negative` to omit negative prompts.
