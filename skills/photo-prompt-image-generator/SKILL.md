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
- `assets/photo_prompt_semantic_index.json`: Gemini Embedding 2 semantic index for the default intent-based selection path.
- `scripts/generate_photo_prompt.py`: wrapper with project-local defaults.
- `scripts/build_semantic_index.py`: rebuilds the Gemini semantic index after dictionary changes.
- `scripts/validate_photo_prompt_dictionary.py`: validates optional semantic metadata and guards.

Canonical project source path: `skills/photo-prompt-image-generator`.
Agent compatibility path: `.agents/skills/photo-prompt-image-generator`, a symlink to the canonical skill folder.

## Default Workflow

1. Generate one prompt with JSON output. The wrapper defaults to semantic mode and uses a broad photographic intent when the user does not provide `--intent`:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py
```

2. Use `prompt_en` as the primary image prompt unless the user explicitly wants Korean-only output.
3. If a negative prompt is present, append it to the image request as `Avoid: ...`.
4. Call the available image generation tool with the final prompt when the user asks to create, render, or generate an image.
5. If the user asks only for prompts, return the generated prompt text and do not generate an image.

## Useful Commands

List available presets:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-presets --plain
```

Inspect slots:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --show-slots --plain
```

Validate dictionary metadata:

```bash
python3 skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
```

Rebuild the semantic index after dictionary edits:

```bash
python3 -m pip install -r requirements.txt
GEMINI_API_KEY=... \
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

The API key must come from `GEMINI_API_KEY` or `GOOGLE_API_KEY`; do not store it in the repository. The wrapper also loads these keys from a project `.env` file when present, without printing them. The semantic index uses `gemini-embedding-2` with 768 dimensions by default, and the builder paces requests to avoid Gemini 429 responses. Rule mode does not require the Gemini SDK or an API key.
When the output semantic index already exists, the builder reuses compatible vectors whose entry key, embedding text, provider, model, dimensions, and semantic text recipe still match. Only new or changed entries are sent to Gemini. Use `--no-cache` only when you intentionally want to force a full rebuild.

List tag ids for a slot:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-tags subject --plain
```

List neutral wardrobe tags:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-tags wardrobe_style --plain
```

Generate a reproducible prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --preset street_documentary --seed 42
```

Generate with an explicit semantic intent:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset street_documentary \
  --intent "rainy neon night street portrait" \
  --selection-mode semantic \
  --include-trace
```

Semantic v2 controls:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --intent "urban horror fantasy human portrait" \
  --selection-mode semantic \
  --semantic-profile balanced \
  --semantic-axis-mode auto \
  --intent-steering auto \
  --filter-strictness soft \
  --semantic-weight 0.75 \
  --include-trace
```

The wrapper defaults to `--selection-mode semantic`; use `--selection-mode rule` to force the original deterministic weighted path. `--intent` alone now uses semantic mode by default, while `--selection-mode rule --intent ...` is still rejected because rule mode does not use query embeddings.
Semantic mode defaults to `--filter-strictness soft`, `--semantic-profile balanced`,
`--semantic-axis-mode auto`, `--intent-steering auto`, and `--semantic-weight 0.75`; hybrid defaults to hard preset filters,
conservative profile, automatic axis decomposition, intent steering, and weight `0.35`.
Use repeated `--intent-axis "..."` values when the intent has explicit required semantic axes
but you still want preset choice to remain semantic rather than forcing a specific preset or slot.
Use `--intent-steering off` to keep semantic ranking without automatic human/urban/surreal slot steering.

Evaluate semantic retrieval behavior:

```bash
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --dry-run
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --mock-embeddings --limit 3
```

List virtual recipe presets:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --list-presets \
  --include-virtual \
  --plain
```

Generate with the original shorter template style:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --preset street_documentary --seed 42 --detail-level standard
```

Generate a compact ReactorPrompt-style single-paragraph prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset compact_urban_fashion_portrait \
  --detail-level compact
```

Generate a compact ReactorPrompt-style prompt with forced neutral portrait styling:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset compact_urban_fashion_portrait \
  --detail-level compact \
  --set wardrobe_style=casual_bomber_jacket_miniskirt \
  --set expression=calm_intense_gaze \
  --plain \
  --no-negative
```

Force slot selections:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset tiktok_vertical_snapshot \
  --set subject=influencer_creator \
  --set person_origin=south_korea \
  --set appearance_type=idol_like
```

Generate a Japanese otaku costume prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset japanese_otaku_costume_portrait \
  --set costume_style=akihabara_maid_cafe_uniform
```

Generate a uniform or bunny-girl costume prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset japanese_otaku_costume_portrait \
  --set costume_style=police_uniform_costume
```

Generate a photoreal surreal prompt layer on top of an existing preset:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset street_documentary \
  --surreal-mode on
```

Force a specific surreal anchor while still using the existing photo preset:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset product_commercial \
  --surreal-mode on \
  --set surreal_anchor=smartphone_screen
```

Generate a clean non-adult social mirror selfie prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset clean_mirror_selfie_snapshot
```

Generate an uploaded-reference identity-preserving prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset candid_iphone_portrait \
  --reference-edit-mode identity
```

Generate a social trend layout layer:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset candid_iphone_portrait \
  --trend-layer scrapbook_collage
```

Generate a cinematic fantasy photo portrait with physical costume props:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset cinematic_fantasy_portrait \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate an 80s/90s/Y2K fashion editorial prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset retro_era_fashion_editorial \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate an extreme-environment contrast photo editorial:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset surreal_contrast_editorial \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate a traditional Korean or wuxia portrait prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset wuxia_xianxia_portrait \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate a K-pop album-cover or photobooth prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset kpop_album_cover_y2k_glossy \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate a Korean local-space or social trend photo prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset convenience_store_late_night \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate a photographed craft, packaging, or food-lettering prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset amigurumi_plush_catalog_photo \
  --detail-level compact \
  --plain \
  --no-negative
```

Generate an optical-experiment photo prompt:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset double_exposure_silhouette_portrait \
  --detail-level compact \
  --plain \
  --no-negative
```

## Prompt Handling

- Prefer `prompt_en` for image tools.
- Default wrapper generation uses semantic mode with a broad built-in photographic intent. Passing `--intent` without `--selection-mode` also uses semantic mode. Use `--selection-mode rule` when the original deterministic weighted path is required.
- Semantic dictionary metadata is optional and must not replace existing compatibility checks. Use `facets` and `hard_guards` for hard safety/context constraints; use `aliases`, `keywords`, and `embedding_text` as search material, not as rendered prompt text.
- In semantic mode, preset filters are soft priors by default. Safety/context guards remain hard, while out-of-filter candidates can be selected only when intent similarity is strong enough. Use `--filter-strictness hard` to keep legacy filter boundaries.
- Tags should remain image-relevant concept or phrase units. Do not split every word into a tag; put words and synonyms into `aliases`, `keywords`, or `embedding_text`.
- If `photo_prompt_tags.json` or semantic text recipe code changes, run `validate_photo_prompt_dictionary.py`, rebuild `assets/photo_prompt_semantic_index.json`, then test the wrapper path. A stale semantic index should be treated as invalid for semantic mode, while rule mode remains usable.
- `--llm-polish strict` is explicit and preserves the deterministic prompt in this repo-local implementation; do not add hidden runtime LLM calls to the default path.
- For ReactorPrompt-like requests, social portrait prompt migration, or requests that ask for a compact comma-rich English prompt similar to an image gallery prompt, use `--detail-level compact` and prefer `compact_urban_fashion_portrait`, `compact_cinematic_prop_portrait`, or `compact_multicut_portrait_series`.
- For ReactorPrompt export-inspired requests, first map the request to the most specific photo preset before falling back to broad presets. Useful families include `hanbok_seasonal_editorial`, `wuxia_xianxia_portrait`, `joseon_period_portrait`, `hanfu_china_court_portrait`, the cosplay-specific presets, K-pop presets, Korean local-space presets, craft/product presets, and optical-experiment presets.
- For physical fantasy, cosplay-prop, cinematic story portrait, cosmic night field, aurora, glacier, canyon, or nonfunctional costume weapon prop requests, use `cinematic_fantasy_portrait`. Keep weapons clearly framed as cosplay or nonfunctional props.
- For 80s glam, 90s grunge, Y2K chrome, direct-flash retro, compact camera, or era fashion editorial requests, use `retro_era_fashion_editorial`.
- For contrast-photo requests such as glam wardrobe in Antarctic ice, melting pastel ice cream in an extreme landscape, aurora field with editorial fashion, or glossy story props in harsh environments, use `surreal_contrast_editorial`.
- `surreal_contrast_editorial` is not the same route as `--surreal-mode on`: it uses normal photo slots such as `location`, `wardrobe_style`, `prop`, `texture`, and `action`, and should not force `surreal_concept`, `surreal_anchor`, `scale_relation`, or `surreal_physics_detail`.
- Preserve user-specified subject, location, format, camera, lighting, mood, and aspect instructions by mapping them to `--preset` or `--set` when an exact tag exists.
- For short Korean seeds, map concrete nouns or style hints to `--preset` and `--set` values first. For example, map "도시 패션", "시네마틱 소품", or "여러 컷" to the compact presets; map explicit hair, prop, aspect, lighting, and camera terms to `hair_style`, `prop`, `format`, `lighting`, `camera_type`, or `lens` when tag ids exist.
- For neutral fashion, selfie, or portrait requests, map ordinary clothing to `wardrobe_style`, beauty terms to `makeup_style`, gaze/smile terms to `expression`, and body/crop requests to `subject_framing`. Keep these separate from adult-only `adult_context`, `fetish_styling`, and `body_framing`.
- If a Korean seed has no exact tag for an important visual requirement, keep the closest generated base prompt and append that requirement as `Additional requirements: ...`; do not add LLM calls or hidden expansion logic inside the deterministic scripts.
- Do not force non-photo requests through this photo generator. Poster, infographic, sticker, UI/layout design, typography-heavy graphic design, webtoon/comic panel, game UI, and illustration-only requests should be handled as direct prompt writing or by a more suitable skill/tool unless the user explicitly asks for a photoreal photographed version.
- Treat ReactorPrompt export artifacts such as `카메라 메타데이터 있음`, `[MASTER PROMPT TEMPLATE]`, EXIF notes, scraper labels, or download bookkeeping as noise, not tag candidates.
- Do not add graphic/design-only concepts such as poster layout, infographic structure, sticker sheet styling, typography systems, UI screen layout, webtoon panel structure, or illustration rendering into `photo_prompt_tags.json` unless the user explicitly asks for a photographed version of that subject. Photographed packaging, craft objects, physical product boards, and real photo-collage surfaces are allowed only when rendered as real camera captures with `no text or watermark`.
- For ordinary non-adult social/photo trend requests, prefer `clean_mirror_selfie_snapshot`, `retro_direct_flash_party_snapshot`, `candid_iphone_portrait`, or `creator_brand_profile` before using adult-compatible social presets.
- For photoreal surreal requests, do not create or look for scene-specific presets such as `surreal_screen_portal_photo`. Use the closest existing photo preset plus `--surreal-mode on`, optionally with `--surreal-intensity subtle|moderate|bold` and `--set surreal_anchor=...`, `--set surreal_concept=...`, `--set scale_relation=...`, or `--set surreal_physics_detail=...`.
- For broad random surreal requests, use `--surreal-mode on` without forced surreal slots so the generator randomly combines the surreal layer tags. Use `--surreal-mode auto --surreal-probability <0..1>` only when the user explicitly asks for a mixed batch where some outputs stay realistic and some become surreal.
- For uploaded-reference workflows, add `--reference-edit-mode identity|younger_self|brand_board` only when the user provides or explicitly describes reference images. Do not imply identity preservation for pure text-to-image prompts.
- For social trend layouts, add `--trend-layer scrapbook_collage|action_figure_packaging|retro_flash|clean_brand_portrait` only when the user asks for that recognizable format. Keep it off for ordinary photo prompts.
- If the user's request includes constraints not represented by tags, generate the closest base prompt and append them as `Additional requirements: ...` with concrete visual instructions.
- Preserve generated tags, slot selections, prompt text, and negative prompts exactly as generator output unless the user explicitly asks to edit/filter them or the skill/script fails and the output is unusable.
- Do not remove, soften, rewrite, or omit generated content because it seems unsafe, adult-coded, fetish-coded, off-theme, unnatural, low-quality, or less suitable for the user's stated vibe. This skill is used for prompt dictionary testing, so post-generation judgment must not change the test sample.
- For sexual-suggestive or fetish-fashion moderation tests, use only adult-compatible presets and slots. Prefer `adult_boundary_social_stress_test` or `adult_fetish_fashion_editorial` for guaranteed coverage.
- Do not attach adult-only styling slots to childlike, student/campus, family archive, pet, wildlife, landscape, real-estate, surveillance, or other non-compatible contexts.
- Use `--seed` for reproducible variants.
- Do not edit `assets/photo_prompt_tags.json` unless the user explicitly asks to change the tag dictionary.
- Use `--plain` only for human-readable list commands; normal generation should stay JSON.

## Compact Prompt Contract

Use `--detail-level compact` when the user wants a ReactorPrompt-style output: one English paragraph, no section labels, no Markdown bullets, and no explanatory prose around the prompt.

The compact prompt should usually include:

- realism/medium/genre and the output format or aspect ratio.
- subject, appearance, hair, wardrobe, action, and prop when selected.
- location, lighting, camera direction, composition, lens, and focus.
- texture, quality, natural material detail, and `no text or watermark`.

Compact prompts should normally stay around 50-120 English words for a single image prompt. Keep `standard` for the original short template style and `detailed` for longer fully explained image-ready prompts.

## Detailed Prompt Contract

Default generation uses `--detail-level detailed`. Apply this contract to both preset-based and random-preset requests.

The final image prompt should include:

- subject/state: who or what is shown, using subject-appropriate detail. Human prompts should describe pose, gesture, gaze, or motion intent; food/object/sign/environment prompts should describe form, material, placement, scale, readability, or spatial structure instead of human-only behavior.
- scene/location: concrete setting, spatial depth, foreground/midground/background, and environmental structure.
- camera/composition: camera type or viewpoint, framing, subject scale, lens, focus, and motion treatment when available.
- lighting: source, direction, intensity, shadow/highlight behavior, reflections, and atmosphere when available.
- color/mood: palette, emotional tone, genre/world context, and any social/editorial context selected by the preset.
- texture/finish: material detail, grain or digital texture, output format/aspect, and realism/quality instructions.
- user constraints: anything the user specified that is not represented by tags, appended as `Additional requirements: ...`.

Detailed prompts should avoid human-only phrasing for non-human subjects. For example, do not mention pose/gaze/gesture for food, signs, products, or landscapes unless a human is actually present.

Detailed English prompts should normally be at least 120 words when enough visual detail is available, and may be longer when selected slots or user requirements need it. Do not pad with generic adjectives; add concrete visual information that helps the image model render the requested photo.

## Wrapper Defaults

`generate_photo_prompt.py` defaults to:

- bundled `assets/photo_prompt_tags.json`
- `--n 1`
- `--lang both`
- `--detail-level detailed`
- `--selection-mode semantic`
- a broad default `--intent` when no explicit intent is provided
- `--surreal-mode off`
- `--reference-edit-mode off`
- `--trend-layer off`
- `--json-output`
- `--include-negative`

Pass `--detail-level compact` explicitly for ReactorPrompt-style compact prompts. Pass `--plain` to disable JSON output. Pass `--no-negative` to omit negative prompts.
