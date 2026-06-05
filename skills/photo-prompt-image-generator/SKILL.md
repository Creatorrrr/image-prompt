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
- `assets/concept_recipes.json`: deterministic short Korean concept to generator-argv recipes.
- `assets/run_ledger.schema.json`: schema for image-generation attempt records.
- `scripts/generate_photo_prompt.py`: wrapper with project-local defaults.
- `scripts/record_image_run.py`: validates and appends external image-generation attempts to the local run ledger.
- `scripts/build_semantic_index.py`: rebuilds the Gemini semantic index after dictionary changes.
- `scripts/validate_photo_prompt_dictionary.py`: validates optional semantic metadata and guards.

Canonical project source path: `skills/photo-prompt-image-generator`.
Agent compatibility path: `.agents/skills/photo-prompt-image-generator`, a symlink to the canonical skill folder.

## Default Workflow

0. For semantic-mode generation, prefer the project virtualenv when it exists:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py
```

If `.venv` is missing, `google-genai` cannot be imported, or generation prints `semantic default fell back to rule mode`, self-heal the local environment before continuing:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python - <<'PY'
from google import genai
print("google-genai ok")
PY
```

Then rerun the original prompt command with `.venv/bin/python`. Do this directly without asking the user unless the install fails, the network is unavailable, or `GEMINI_API_KEY`/`GOOGLE_API_KEY` is missing from both the environment and the project `.env`.

1. Generate one prompt with JSON output. The wrapper defaults to semantic mode and uses a broad photographic intent when the user does not provide `--intent`:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py
```

2. Use `prompt_en` as the primary image prompt unless the user explicitly wants Korean-only output.
3. If a negative prompt is present, append it to the image request as `Avoid: ...`.
4. Call the available image generation tool with the final prompt when the user asks to create, render, or generate an image.
5. If the user asks for unchanged retries, keep `prompt_en` and `negative_en` byte-for-byte unchanged for each retry. Use `provenance.prompt_id` as the identity for the prompt and retry failed attempts up to the requested budget before reporting remaining failures.
6. Record each image-generation attempt with `scripts/record_image_run.py` when provenance matters, especially for safety/filter failures and retry chains.
7. If the user asks only for prompts, return the generated prompt text and do not generate an image.

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

The API key must come from `GEMINI_API_KEY` or `GOOGLE_API_KEY`; do not store it in the repository. The wrapper and semantic index builder also load these keys from a project `.env` file when present, without printing them. The semantic index uses `gemini-embedding-2` with 768 dimensions by default, and the builder paces requests to avoid Gemini 429 responses. Rule mode does not require the Gemini SDK or an API key.
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

Generate concept-faithful variants where the original idea must stay visually dominant:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --intent "cozy homebody guy in a small lived-in bedroom at night, gaming desk, snacks, blanket" \
  --concept-lock "방구석 집돌이 컨셉, 작은 방, 모니터 빛, 게임패드, 간식, 담요" \
  --intent-axis "homebody guy in small bedroom" \
  --intent-axis "gaming desk snacks blanket" \
  --n 3
```

Use `--concept-lock` when the user provides a compact scene concept and wants diversity without drifting away from it. The locked concept is rendered near the front of the prompt, while generated subject, action, lighting, camera, texture, and format slots become supporting detail. Repeat `--concept-lock` for multiple non-negotiable scene anchors.

Expand a short Korean concept through the recipe resolver before generation:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "유나 바니걸" \
  --explain-concept
```

If the explanation looks right, rerun without `--explain-concept`. The wrapper expands `--concept` into deterministic generator args such as `--concept-lock`, `--preset`, `--set`, `--intent-axis`, `--additional-requirement`, and `--likeness-mode`.

Generate a concept-faithful vampire prompt that avoids blood-and-fang cliches:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "흡혈귀" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For existence/archetype concepts such as `흡혈귀`, use the vampire concept mixin rather than a standalone role override when another role is present. The resolver should preserve the role outfit and readable job/costume identity, then add vampire facets through deterministic bundles: daylight refusal, mirror or reflection unease, moonlit pallor, bat-like shadows, withered-life cues, coffin-like geometry, antique portraits, or centuries-old stillness. This avoids the old failure mode where every result collapsed into black lace, candles, antique mirrors, and a generic gothic studio. Keep it non-graphic: no visible blood, exposed fangs, bite wounds, visible victims, gore, feeding scene, or graphic violence.

After visual evaluation, vampire prompts must not rely only on absence metaphors such as "missing reflection" or "avoids daylight". Each role-specific vampire bundle should include at least two positive, visible identity anchors that can survive in a single still image: an open mirror or phone screen visibly showing an absent/mismatched reflection, a black umbrella or curtain barrier at a daylight threshold, bat-wing-shaped shadows, moon-pale skin, a tiny crimson eye catchlight, ruby jewelry, withered flowers, coffin-like geometry, antique portraits, or a small cup of dark red wine. Generic gothic fashion, ordinary moody lifestyle portraiture, or plain mine horror is not enough. For weak or visually competing roles such as `경찰`, `사복 여친`, and `바니걸`, pin the vampire anchor through actual slot choices such as `prop`, `action`, `location`, or `composition` whenever existing tags allow it, rather than leaving the cue only in free prose. Keep the role outfit readable but place the vampire anchor near the face, hand, mirror/phone screen, foreground reflection, or central reflection rather than burying it in background atmosphere. Also suppress unrelated playful props and ordinary selfie/nightclub readings that would overpower the vampire identity.

For role + vampire concepts such as `카리나 메이드 흡혈귀`, pass the whole phrase as one `--concept` so the resolver can apply the role and the `흡혈귀` mixin together:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 흡혈귀" \
  --selection-mode rule \
  --seed 701 \
  --include-choices
```

Use `--explain-concept` to audit the selected vampire bundle. The expected shape is one applied role plus `applied_mixins: ["흡혈귀"]`; the selected bundle should vary location, lighting, action, mood, or composition while keeping `costume_style` from the role unless the concept is standalone `흡혈귀`. When a role has a dedicated vampire bundle, the resolver prefers that role-specific bundle over low-weight shared fallback bundles so a seed does not accidentally drop role-specific anchors such as the miner's impossible puddle reflection, the police foreground reflection cue, the casual mirror-selfie/phone-reflection/daylight-barrier cue, or the bunny-girl compact-mirror/bat-shadow cue. Audit weak-role bundles to make sure `combined_forced_slots` does not leave distracting props such as plush dolls or mascot toys available when they would weaken the vampire reading.

Generate a concept-faithful femme fatale prompt that treats the archetype as gaze, power, and danger rather than a generic sexy villain:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "팜므파탈" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For role + femme fatale concepts such as `카리나 메이드 팜므파탈`, pass the whole phrase as one `--concept` so the resolver can preserve the role outfit and add the `팜므파탈` mixin:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 팜므파탈" \
  --selection-mode rule \
  --seed 812 \
  --include-choices
```

Use the `팜므파탈` concept mixin for femme fatale or similar dangerous-intelligent-woman archetype requests. The mixin expresses the archetype through gaze reversal, power, and noir/symbolist visual grammar: cold unreadable stare, low-angle dominance framed around face and stance, chiaroscuro or low-key light, venetian-blind shadows, reflection/doubling, threshold framing, wilted-flower or poison omen, calling cards, gloves, mirrors, hairpins, or perfume bottles. Keep role outfits readable and let the femme fatale layer alter posture, gaze, light, framing, and symbolic props. Do not collapse the concept into lingerie, cleavage-centric framing, pin-up posing, come-hither/bedroom-eyes expression, parted-lips invitation, submissive availability, explicit content, visible victims, or depicted violence. The lethal quality is atmospheric and symbolic: agency, intelligence, control, danger, and the viewer becoming the observed one.

After visual evaluation, femme fatale prompts must not rely only on mood, beauty, or negated pin-up wording. Each role-specific bundle should make intellectual danger visible through at least one information-control anchor near the face, hand, table edge, foreground, mirror, or phone screen: a sealed file, guest book, ledger, calling card, phone message, key, decree, withheld result, or similar sign that she already controls the situation. For weak or visually competing roles such as `경찰`, `사복 여친`, and `바니걸`, pin the power reversal through actual slot choices whenever existing tags allow it: prefer `subject_framing` values such as `upper_body_framing`, `head_and_shoulders_crop`, `waist_up_framing`, or `detail_crop_hands_accessories`; prefer face-and-hands compositions such as `medium_close`, `reflection`, or `frame_within_frame`; avoid combining `looking_down_at_low_camera` with `low_angle` for service, uniform, or stage-costume roles because it can collapse into full-body display. Keep gaze, gloves, cards, phones, envelopes, mirrors, and documents near the face or hand so the viewer reads strategy and leverage before costume display.

Treat femme fatale as two legitimate visual registers, not only one cold-broker template: `cold information-control authority` and `magnetic lure-as-weapon`, where the invitation itself is the trap. Both must show agency, intelligence, and danger; neither should become passive availability. Assign `사복 여친` to an intimacy-trap register where a phone-screen or private-space clue proves she already knows the viewer's secret, and assign `바니걸` to a lure-as-weapon register where covered stage styling, warm rim light, and a poison/invitation omen pull the mark in while she remains in control.

Service- or fetish-coded roles such as `메이드`, `간호사`, and `바니걸` need explicit power-reversal cues: treat the outfit as a cover identity, disguise, institutional authority, or room-operator role, and make the viewer the mark, suspect, patient, or observed party. Tool/action-coded roles such as `광부` need leverage and control cues rather than survival-action posing; use withheld knowledge, route ownership, sealed envelopes, face-height gaze, low-key noir light, and distance from pin-up body angles.

Use `--explain-concept` to audit the selected femme fatale bundle. The expected shape is either standalone `applied_mixins: ["팜므파탈"]` with no role, or one applied role plus `applied_mixins: ["팜므파탈"]`; role costumes should remain intact, `subject_framing` should stay in a face/upper-body/hand-detail family for role concepts, and there should be no assassin weapon cue unless the user also explicitly includes `암살자`. For `경찰`, `사복 여친`, and `바니걸`, check that `combined_forced_slots` does not leave a full-body or pin-up-prone posture as the main reading; the bundle should show the viewer as suspect, mark, or observed party through a visible information-control anchor.

Generate a concept-faithful menhera prompt that treats the concept as yami-kawaii / jirai-kei emotional atmosphere rather than a diagnosis, self-harm scene, or stigmatizing caricature:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "멘헤라" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For role + menhera concepts such as `카리나 메이드 멘헤라`, pass the whole phrase as one `--concept` so the resolver preserves the role outfit and adds the `멘헤라` mixin:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 멘헤라" \
  --selection-mode rule \
  --seed 902 \
  --include-choices
```

Use the `멘헤라` concept mixin for menhera, yami-kawaii, jirai-kei, or similar cute-but-fragile emotional-subculture requests. The mixin expresses the concept through safe visible anchors: phone glow with an unread-message feeling, emotional teary or blank distant gaze, Igari-style tired eye makeup, wilted bouquet, cracked or fragmented mirror, loosened ribbon, small protective cute props, cluttered pastel bedroom, hospital waiting-room light, cool digicam grain, and soft pastel or cold fluorescent color. It must not render menhera as a clinical diagnosis, mental-illness label, self-harm result, or "crazy girlfriend" caricature. Keep the subject as an adult original fictional person treated with dignity; express fragility through atmosphere, light, props, and contained posture rather than crisis acting.

Service- or fetish-coded roles such as `메이드`, `간호사`, and `바니걸` need stronger guardrails. Keep the role outfit readable, but make the menhera layer alter expression, palette, phone/mirror/flower props, and room mood rather than turning the role into submissive availability, medical-risk imagery, or stage-costume display. For `간호사`, the bundle should read as care-fatigue and waiting in an empty hospital waiting room; no syringes, IV lines, medication, pills, bandaged wrists, patient distress, blood, self-harm, or medical misuse imagery. For `바니걸`, keep a fully covered adult stage costume, upper-body framing, vanity/mirror context, and backstage exhaustion; no pin-up pose, cleavage-centered framing, come-hither expression, nudity, fetish staging, or self-harm cue. For `사복 여친`, center adult everyday styling, unread-message waiting, and phone glow; no youthful-minor coding, sexualized vulnerability, or crisis framing.

Use `--explain-concept` to audit the selected menhera bundle. The expected shape is either standalone `applied_mixins: ["멘헤라"]` with no role, or one applied role plus `applied_mixins: ["멘헤라"]`; role costumes should remain intact, and `combined_forced_slots` should include positive anchors such as `expression=emotional_teary_eyes`, `makeup_style=igari_blush`, phone/mirror/flower props, `subject_framing=upper_body_framing`, and mood/color/light choices that support yami-kawaii melancholy. Check that no assassin weapon cue or vampire supernatural cue appears unless the user explicitly includes those concepts.

Generate a concept-faithful angel prompt that treats the archetype as messenger, threshold, immaterial light, awe, guardianship, and trace rather than a generic halo-and-wings costume:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset double_exposure_silhouette_portrait \
  --concept-lock "천사, 전령, 문지방의 빛, 흔적으로만 암시되는 비물질적 존재" \
  --additional-requirement "a presence implied by traces rather than shown directly: a single feather on the floor, a wing-shaped shadow on the wall, and light spilling through a doorway threshold" \
  --additional-requirement "immaterial luminosity with no clear source, strong backlight and god rays, faint overexposed glow, awe and reverent quiet" \
  --detail-level compact \
  --plain \
  --no-negative
```

There is no deterministic `천사` concept mixin yet, so do not rely on `--concept "천사"` as if it were equivalent to `흡혈귀` or `팜므파탈`. Build angel concepts manually from the closest photo preset plus `--concept-lock`, repeated `--intent-axis` values, explicit `--set` overrides when useful, and repeated `--additional-requirement` text. Use `double_exposure_silhouette_portrait` for absence, traces, silhouettes, and immateriality; use `cinematic_fantasy_portrait` only when the user actually wants physical wings, robes, or fantasy-prop staging; use `surreal_contrast_editorial` or `--surreal-mode on` when the angelic reading should come from impossible light, scale, or atmospheric distortion. Treat `angel_halo_wings_tail_set` as a costume/cosplay prop, not as the default meaning of angel.

Angel prompts must include at least two positive visible anchors that can survive in a single still image. Useful anchors include sourceless inner glow, strong backlight or god rays, a door/window/dawn threshold, a raised hand or sealed message that reads as heraldic arrival, low-angle awe or overwhelming scale, a single feather on the floor, light through a window, a wing-shaped shadow, suspended dust, or a room still reacting to a presence. Do not rely only on abstract words like "holy" or "divine", and do not collapse the concept into pretty white wings, a simple ring halo, soft glamour, or idol-costume styling. If the user combines a role with angel, such as `카리나 메이드 천사`, keep the role outfit readable through the base preset or `--concept-lock`, then add angel anchors near the face, hand, threshold, foreground trace, or background light rather than replacing the role with a generic angel costume. Keep judgment or severity atmospheric and symbolic: no blood, visible victims, depicted violence, graphic punishment, or weapon-use scene unless the user explicitly asks for a separate safe weapon-prop concept.

For concepts that combine a role with `암살자`, the recipe resolver uses deterministic scene bundles. Keep the role outfit as a cover identity and let the assassin layer read through hiding in plain sight, off-frame gaze, concealed props, implied targets, reflection surveillance, cover-identity cracks, exit-route checks, crowd blending, and unsettling clues that break a pretty job or lifestyle editorial. The resolver automatically adds a role-specific subtle weapon cue as text, without replacing the bundle's `prop` or `action` scene slots. Do not turn these into graphic violence, visible victims, operational instructions, or drawn/aimed weapons.

When the user asks for a weapon to be subtly visible in an `암살자` concept, keep the recipe intact and add explicit `--set` overrides plus an additional requirement instead of changing recipe pools. Use existing 39df660 tags only:

- 메이드/간호사/사복 여친/바니걸: `--set prop=sheathed_utility_knife_prop --set action=concealed_holster_adjust_pose`
- 경찰: `--set prop=real_holstered_service_pistol --set action=concealed_holster_adjust_pose`
- 광부: `--set prop=nonfunctional_pickaxe_prop --set action=weapon_low_ready_stance`
- 공주: `--set prop=phoenix_hairpin_prop --set action=standing_silence`

Also add a role-specific `--additional-requirement` rather than only a generic weapon phrase:

- 메이드: `a slim sheathed utility blade sits partially visible beneath the apron tie; never drawn, aimed, used, bloody, or shown with a victim`
- 간호사: `a slim sheathed utility blade rides partially visible at the hip under the uniform or jacket; never drawn, aimed, used, bloody, or shown with a victim`
- 경찰: `a duty holster grip is partially visible at the belt as a quiet cover-identity tell; never drawn, aimed, used, bloody, or shown with a victim`
- 광부: `a nonfunctional pickaxe tool head is subtly visible in-context as work equipment held low or shouldered; never drawn, aimed, used, bloody, or shown with a victim`
- 사복 여친: `a compact sheathed blade peeks at the waistband or hoodie edge; never drawn, aimed, used, bloody, or shown with a victim`
- 공주: `a phoenix hairpin catches a subtle metallic glint as the only weapon cue, with no firearm or modern weapon; never drawn, aimed, used, bloody, or shown with a victim`
- 바니걸: `a slim sheathed blade is just visible along the garment seam or edge; never drawn, aimed, used, bloody, or shown with a victim`

Add unrepresented concrete requirements without manual prompt editing:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset cinematic_fantasy_portrait \
  --concept-lock "지젤 광부" \
  --additional-requirement "coal miner workwear" \
  --additional-requirement "mining helmet with headlamp" \
  --likeness-mode inspired
```

Record an image attempt after using the external image tool:

```bash
python3 skills/photo-prompt-image-generator/scripts/record_image_run.py \
  --ts "2026-06-03T10:00:00+09:00" \
  --concept "유나 바니걸" \
  --prompt-en "$PROMPT_EN" \
  --prompt-id "$PROMPT_ID" \
  --attempt 1 \
  --status safety_block \
  --failure-reason "safety filter" \
  --tool image_gen
```

The recorder recomputes `prompt_id` from `--prompt-en`; if it differs from `--prompt-id`, it exits without writing. On retries, pass the same prompt text and increment `--attempt`; use `--retry-of` with the previous `run_id` when available.

Evaluate semantic retrieval behavior:

```bash
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --dry-run
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --mock-embeddings --limit 3
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --diversity-check --limit 1
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
- For vampire or similar supernatural archetype requests, use the `흡혈귀` concept mixin or the closest gothic/horror preset plus `--concept-lock`; express the creature through atmosphere, body language, daylight refusal, mirror/reflection unease, moonlit pallor, withered-life cues, bat-like shadows, coffin-like geometry, antique portraits, ruby/crimson accents, dark red wine as a prop beverage, and room effects, not through gore, victims, feeding, exposed fangs, or visible blood. Do not force a generic gothic dress or candle studio over a more specific role outfit, and do not let the output collapse into generic gothic fashion, ordinary moody lifestyle photography, or plain horror without a clear vampire anchor.
- For femme fatale or similar dangerous-intelligent-woman archetype requests, use the `팜므파탈` concept mixin or the closest noir/editorial preset plus `--concept-lock`; express the archetype through gaze reversal, authority, controlled stillness, noir/symbolist light, reflection/doubling, threshold framing, quiet omen props, visible information-control anchors, and when role-appropriate magnetic lure-as-weapon where the invitation itself is the trap. The concept is about agency, intelligence, danger, and the viewer being observed or deliberately drawn in under her control, not sexual availability. Do not rewrite it into lingerie, cleavage-centered framing, pin-up posing, bedroom eyes, come-hither gestures, explicit content, visible victims, or depicted violence. For service/fetish-coded or action-coded roles, add stronger power-reversal anchors so the role reads as a disguise, authority position, room-operator identity, or leverage holder rather than cosplay display; in semantic mode, add explicit `--intent-axis` or `--set subject_framing=...` constraints rather than trusting free-text `no pin-up` wording alone.
- For menhera, yami-kawaii, jirai-kei, or similar cute-but-fragile emotional-subculture requests, use the `멘헤라` concept mixin or the closest candid phone/social portrait preset plus `--concept-lock`; express the concept through phone glow, unread-message waiting, teary or blank distant gaze, Igari-style tired eye makeup, wilted flowers, cracked mirrors, loosened ribbons, protective cute props, cluttered pastel bedrooms, hospital waiting-room light, cool digicam grain, and soft pastel or cold fluorescent palettes. Treat it as a subculture mood about attachment and quiet burnout, not a diagnosis, self-harm scene, crisis spectacle, or stigmatizing "crazy girlfriend" caricature. Do not render wounds, scars, blood, bandaged wrists, medication, pills, syringes, IV lines, overdose, suicidal staging, minors, nudity, sexualized vulnerability, fetish staging, or pin-up framing. For `간호사`, `사복 여친`, and `바니걸`, audit `--explain-concept` and actual `prompt_en` because medical-risk imagery, youthful-minor coding, and stage-costume display are the highest-risk drift modes.
- For angel, guardian-angel, messenger-angel, or similar divine messenger archetype requests, do not treat `angel_halo_wings_tail_set` as the default or the whole concept. There is no deterministic `천사` concept mixin yet, so compose the idea manually with the closest preset plus `--concept-lock`, repeated `--intent-axis`, and concrete `--additional-requirement` anchors. Express angels through messenger/herald function, threshold or liminal arrival, immaterial light, awe or "be not afraid" distance, guardianship, mercy-and-judgment ambiguity, and traces of a presence rather than only white wings and a halo. Include at least two visible anchors such as sourceless inner glow, god rays, a doorway/window/dawn threshold, a raised hand or sealed message, low-angle scale, a single feather, a wing-shaped shadow, suspended dust, or a room reacting to a presence. Keep judgment atmospheric and non-graphic.
- For 80s glam, 90s grunge, Y2K chrome, direct-flash retro, compact camera, or era fashion editorial requests, use `retro_era_fashion_editorial`.
- For contrast-photo requests such as glam wardrobe in Antarctic ice, melting pastel ice cream in an extreme landscape, aurora field with editorial fashion, or glossy story props in harsh environments, use `surreal_contrast_editorial`.
- `surreal_contrast_editorial` is not the same route as `--surreal-mode on`: it uses normal photo slots such as `location`, `wardrobe_style`, `prop`, `texture`, and `action`, and should not force `surreal_concept`, `surreal_anchor`, `scale_relation`, or `surreal_physics_detail`.
- Preserve user-specified subject, location, format, camera, lighting, mood, and aspect instructions by mapping them to `--preset` or `--set` when an exact tag exists.
- For short Korean seeds, pass the original seed through `--concept-lock` first, then map concrete nouns or style hints to `--preset` and `--set` values. For example, map "도시 패션", "시네마틱 소품", or "여러 컷" to the compact presets; map explicit hair, prop, aspect, lighting, and camera terms to `hair_style`, `prop`, `format`, `lighting`, `camera_type`, or `lens` when tag ids exist.
- When the user asks for a spectrum of variants around one concept, use `--concept-lock` plus `--n`, `--seed`, and optional repeated `--intent-axis` values. Keep the locked concept stable and let only supporting slots vary.
- For neutral fashion, selfie, or portrait requests, map ordinary clothing to `wardrobe_style`, beauty terms to `makeup_style`, gaze/smile terms to `expression`, and body/crop requests to `subject_framing`. Keep these separate from adult-only `adult_context`, `fetish_styling`, and `body_framing`.
- If a Korean seed has no exact tag for an important visual requirement, keep it in `--concept-lock` first; append `Additional requirements: ...` only for concrete details still not represented by tags. Do not add LLM calls or hidden expansion logic inside the deterministic scripts.
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

- concept lock: when `--concept-lock` is provided, render the original user concept near the beginning and treat all generated slot detail as support rather than replacement.
- subject/state: who or what is shown, using subject-appropriate detail. Human prompts should describe pose, gesture, gaze, or motion intent; food/object/sign/environment prompts should describe form, material, placement, scale, readability, or spatial structure instead of human-only behavior.
- scene/location: concrete setting, spatial depth, foreground/midground/background, and environmental structure.
- camera/composition: camera type or viewpoint, framing, subject scale, lens, focus, and motion treatment when available.
- lighting: source, direction, intensity, shadow/highlight behavior, reflections, and atmosphere when available.
- color/mood: palette, emotional tone, genre/world context, and any social/editorial context selected by the preset.
- texture/finish: material detail, grain or digital texture, output format/aspect, and realism/quality instructions.
- user constraints: anything the user specified that is not represented by tags, passed through repeated `--additional-requirement` so it renders as `Additional requirements: ...` before `provenance.prompt_id` is computed.
- likeness handling: when a concept names a public figure or idol, prefer `--likeness-mode inspired` so the rendered prompt asks for an original adult fictional person inspired by the style/vibe, not an exact likeness.

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

Each JSON result includes a `provenance` block with `prompt_id`, `negative_id`, `generator_version`, `seed`, `batch_index`, `preset_id`, `selection_mode`, `concept_lock`, `additional_requirements`, `likeness_mode`, and the final forwarded `argv`.

Pass `--detail-level compact` explicitly for ReactorPrompt-style compact prompts. Pass `--plain` to disable JSON output. Pass `--no-negative` to omit negative prompts. Pass `--concept "짧은 한국어 컨셉"` to use the local recipe resolver, and `--explain-concept` to inspect the resolved args without generating.
