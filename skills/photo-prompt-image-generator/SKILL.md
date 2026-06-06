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
5. After every built-in image generation call, immediately identify the exact newly created file path under `/Users/chasoik/.codex/generated_images` before starting another generation or copying any files. Do not infer the result from a broad mtime search across unrelated worktrees.
6. Copy every successful generated image into this worktree before reporting it. Use `generated_images/<concept>-<timestamp>/` where `<concept>` is a filesystem-safe concept slug and `<timestamp>` is the generation timestamp, and name each file with `prompt_id`, `seed`, and `attempt`, for example `d97311a76c77b29f-seed902-attempt1.png`. Leave the original global generated image file in place.
7. If the user asks for unchanged retries, keep `prompt_en` and `negative_en` byte-for-byte unchanged for each retry. Use `provenance.prompt_id` as the identity for the prompt and retry failed attempts up to the requested budget before reporting remaining failures.
8. Record each image-generation attempt in this worktree's `runs/image_runs.ndjson` with `scripts/record_image_run.py`, including the worktree-local `generated_images/...` path. This is required for retry chains, safety/filter failures, and multi-worktree provenance.
9. If the user asks only for prompts, return the generated prompt text and do not generate an image.

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
Policy-only edits under `semantic_policy` do not require a semantic index rebuild. `dictionary_hash` tracks the tag/preset/slot/facet fields that feed entry embedding text, while `semantic_policy_hash` is provenance for routing, signal lexicons, steering, coverage repair, and runtime axis text. Rebuild the index when entry text inputs or `SEMANTIC_TEXT_RECIPE_VERSION` change; do not rebuild solely because `signal_lexicon`, `slot_signals`, `coverage_repair`, or `axis_embedding_text` changed.

Concept mode defaults:

- `--concept-mode legacy` is the default and keeps behavior-compatible concept recipe expansion.
- `--concept-mode soft` is opt-in. It forwards concept locks and intent axes without forced recipe slot sets, and should not become the default until real-embedding concept benchmarks pass.

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

Generate a concept-faithful princess prompt that treats `공주` as lineage, ceremony, protected confinement, public display, and the threshold into rule rather than a generic Western fairytale figure:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "공주" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

The base `공주` role recipe keeps a readable Korean Joseon court identity: royal hanbok, layered fabric, traditional court hair ornament language, and a royal palace chamber. There is no deterministic multi-bundle `공주` mixin yet, so express deeper princess themes with the base role plus explicit `--set` overrides and repeated `--additional-requirement` text. Keep the hanbok silhouette and East-Asian palace identity dominant; do not convert the concept into a Western ballgown, corset, gem-tiara fantasy, or generic gothic princess.

Choose one dominant princess theme per image instead of stacking all of them:

- 혈통/계승: use a sealed royal decree, ancestral court portrait, genealogical scroll, inherited ornament, or palace record. Pin with `--set prop=sealed_mission_envelope_prop` and explain that the envelope reads as a royal decree or succession document.
- 권력과 무력함: show authority crossed by lattice shadows or bars of light. Pin with `--set composition=centered_symmetry`, `--set action=standing_silence`, and when useful `--set light_shape=venetian_blind_shadows`.
- 보호와 감금: make the beautiful chamber read as a gilded cage through screens, lattice windows, threshold shadows, or a distant guard silhouette. Pin with `--set composition=frame_within_frame` or `--set action=doorframe_shadow_watch`.
- 공개 전시: use ceremonial frontal symmetry, court-record stillness, and fan or sleeve barriers so the viewer reads the subject as a living royal symbol under observation. Pin with `--set action=court_fan_pose` or `--set composition=centered_symmetry`.
- 각성/통치 전환: show a raised chin, hand near the seal or decree, warm light catching the court ornament, or the protected princess stepping into rule. Pin with `--set prop=sealed_mission_envelope_prop`, `--set action=holding_story_prop`, and `--set light_shape=hairline_rim_glow`.

For role + archetype concepts such as `설윤 공주 흡혈귀`, `설윤 공주 팜므파탈`, or `설윤 공주 얀데레`, pass the whole phrase as one `--concept`; `공주` is the role and the other concept is the mixin. Audit with `--explain-concept` to make sure `costume_style=royal_princess_hanbok` and `location=royal_princess_chamber` stay intact unless the user explicitly asks for a different cultural lineage. Keep it dignified and non-graphic: no minors-coding, sexualized framing, visible victims, depicted violence, or Western royalty conversion.

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

After image review, vampire prompts also need a visibility hierarchy. At least one vampire anchor must be attached to the subject or placed immediately beside the lit face, hand, phone, mirror, badge, jewelry, or foreground reflection, so the viewer reads the vampire identity before ordinary role cosplay, fashion, hospital horror, stage costume, or background decoration. For weak or visually competing roles, pin `subject_framing` to an upper-body, waist-up, head-and-shoulders, or face/hand crop rather than relying on full-body costume display or pure silhouette. Reflection anomalies should show the real subject and the failed reflection in the same frame for instant comparison; the wrong reflection should not be a small dark detail in the background. Eastern or historical roles such as `공주` must keep the hanbok and East-Asian court identity dominant, rather than being converted into a Western gothic gown.

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

After visual evaluation, menhera prompts must not collapse into the single `phone + tears + wilted flowers` formula. Each role bundle should choose one dominant visible anchor and a role-appropriate emotional register: maid as teary over-care with a visible one-sided chat, nurse as quiet care-fatigue with the bouquet as the single focal object, police as gaze-avoidant cracks in a too-perfect mirror selfie, miner as bleak isolation with a discordant pastel kawaii detail, casual girlfriend as downcast withdrawal with a read-but-unanswered chat and bedside symbols, princess as serene gilded loneliness with only a subtle cold phone glow, and bunny girl as blank backstage exhaustion through mirror/vanity framing.

Use `--explain-concept` to audit the selected menhera bundle. The expected shape is either standalone `applied_mixins: ["멘헤라"]` with no role, or one applied role plus `applied_mixins: ["멘헤라"]`; role costumes should remain intact, and `combined_forced_slots` should include positive anchors such as `makeup_style=igari_blush`, one dominant phone/mirror/flower/cute-prop anchor, `subject_framing=upper_body_framing`, and mood/color/light choices that support yami-kawaii melancholy. Audit `combined_forced_slots.expression` so role concepts vary across teary, blank, serene, avoidant, and downcast registers instead of always using `emotional_teary_eyes`. Check that no assassin weapon cue or vampire supernatural cue appears unless the user explicitly includes those concepts.

Generate a concept-faithful tsundere prompt that treats the archetype as warmth disguised as coldness whose disguise visibly leaks, rather than a simply angry or insulting person:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "츤데레" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For role + tsundere concepts such as `카리나 메이드 츤데레`, pass the whole phrase as one `--concept` so the resolver preserves the role outfit and adds the `츤데레` mixin:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 츤데레" \
  --selection-mode rule \
  --seed 1202 \
  --include-choices
```

Use the `츤데레` concept mixin for tsundere or "cold on the surface, warm underneath" requests. The single defining gate is a denial-vs-evidence contradiction readable in one frame: a first read of rejection or aloofness, such as an averted face, turned shoulder, crossed arms, guarded side glance, lowered gaze, or brisk distancing gesture, plus a second read of leaked sincerity, such as faint ear-tip or nose-bridge warmth, a wavering peeking glance, fidgeting hands, posture contradiction, or one caring object offered, returned, placed, or held close as a soft barrier. `skeptical_side_eye` is only one optional denial cue, not the default. A purely cold face is just annoyed; a purely sweet face is just shy. Make one caring-evidence object legible in the same crop as the averted face: a lunchbox, wrapped gift, shared umbrella, two coffees, hand-knit scarf, handwritten note, peeled-fruit plate, returned lost item, or small personal token. The caring object exists for the viewer's benefit; it is never hoarded, repeated, pinned to a wall, or used as evidence about the viewer.

Keep the role outfit readable and let the tsundere layer alter expression, gaze direction, posture, blush, framing closeness, light, and one caring prop rather than replacing the costume. This is explicitly not yandere, femme fatale, or menhera: no surveillance, repeated same-person photos, photo wall or shrine, red thread, possessive white-knuckle grip, doorway-stalking menace, birdcage or glass-dome confinement, gaze-reversal power play, seductive pin-up, information-control prop, unread-message waiting, teary depressive collapse, self-harm, medical-risk imagery, weapons, blood, visible victims, minors, or sexualized framing. The eyes should stay alive and embarrassed, never hollow, dead, fixed, or unblinking.

After visual evaluation, tsundere prompts must pass a micro-expression, costume-swap, and frame-budget gate. Blush must remain photographic and restrained: faint warmth at the ear tips, nose bridge, or upper cheeks, cheeks mostly neutral, visible skin texture and pores; avoid heavy Igari blush, red painted circles, airbrushed anime blush, or makeup-level redness unless the user explicitly asks. The denial-vs-evidence contradiction should survive even if the role costume were swapped for plain everyday clothes: the averted face, restrained warmth, hand tension, and one caring object must occupy more visible frame area than the role outfit. Service- or uniform-coded roles such as `메이드`, `간호사`, `경찰`, `바니걸`, and to a lesser extent `광부`, need an explicit anti pin-up / anti body-first guardrail beyond generic "no sexualized framing": no full-body costume display, no side hip pose, no chest-forward or cleavage-emphasis crop, no rim-lit fashion glamour, and no sultry authority pose.

After the next visual review, weak tsundere roles must also pass an active-denial gate. `메이드`, `간호사`, `사복 여친`, and `공주` should not rely on lowered gaze plus a caring object alone, because that collapses into demure service, professional bedside manner, listless melancholy, or graceful courtly shyness. At least one first-read rejection cue must be visible beyond gaze aversion: a huffed or pursed mouth, suppressed pout, raised chin, half-turned shoulder, brisk dismissive hand, chart-tapping scold, small thunk as the object is set down, or an imperious offhand offer. The caring object should become a conflict object, delivered briskly or reluctantly, not shyly cradled or politely presented.

Use `--explain-concept` to audit the selected tsundere bundle. The expected shape is either standalone `applied_mixins: ["츤데레"]` with no role, or one applied role plus `applied_mixins: ["츤데레"]`; `combined_forced_slots` should include `makeup_style=natural_makeup`, a warm or everyday mood, one caring prop, and an expression that can vary across `looking_away_pensive`, `shy_downward_glance`, `playful_smirk`, `calm_intense_gaze`, `skeptical_side_eye`, and `surprised_open_eyes`. Check `selected_bundles[0].subtype` for motif diversity in multi-role batches, and check side-eye budget: a seven-role batch should not rely on `skeptical_side_eye` for more than one role by default. For weak or visually competing roles, pin the contradiction through actual slots such as `expression=playful_smirk|calm_intense_gaze|looking_away_pensive|surprised_open_eyes|skeptical_side_eye`, `prop=coffee_cup_prop|logo_board_prop|transparent_dome_umbrella|picnic_blanket|product_box_prop|paper_coffee_receipt|phoenix_hairpin_prop`, `action=maid_cafe_tray_pose|holding_story_prop|court_fan_pose|standing_backstage`, `composition=medium_close|frame_within_frame|over_the_shoulder_dialogue`, and `subject_framing=head_and_shoulders_crop|upper_body_framing` rather than trusting the bare word `츤데레`. Rotate the caring object so role specificity stays legible: heart-latte or dessert set down brusquely for maid, care chart/checklist/folded note with scolding mouth for nurse, returned umbrella or item for police, spare blanket/glove/warm note for miner, lunchbox or modest wrapped gift for casual girlfriend, hanbok token plus fan/sleeve barrier for princess, saved ticket/note/coat for bunny. Cap coffee/takeaway drink as the primary caring anchor at one role bundle per seven-role batch unless the user explicitly asks for coffee. For `사복 여친`, the recipe forces conservative everyday wardrobe and an offered gift/lunchbox cue to avoid body-display, phone-stalking, or sad breakup drift. For `공주`, preserve hanbok and East-Asian court identity while adding courtly haughtiness, raised chin, and brisk offhand token delivery. For `바니걸`, keep covered backstage or hostess styling in face-and-hands framing and suppress pin-up or stagewear display.

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

Generate a concept-faithful devil prompt that treats the archetype as temptation, contract, accusation, fallen light, shadow-self, and threshold wrongness rather than a generic horned monster:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "악마" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For role + devil concepts such as `카리나 메이드 악마`, pass the whole phrase as one `--concept` so the resolver preserves the role outfit and adds the `악마` mixin:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 악마" \
  --selection-mode rule \
  --seed 606 \
  --include-choices
```

Use the `악마` concept mixin for devil, demon, tempter, fallen-light, adversary, or similar diabolical archetype requests when the user says `악마` explicitly. Treat devil as a set of functions and meanings, not only a body shape. Valid devil modes include visible demon, contract tempter, intimate temptation, adversary/prosecutor, fallen authority, inner shadow, liminal threshold, playful trickster, corruption trace, and social/systemic evil. The mixin should make one mode dominant and let the other details support it. Keep role outfits readable and let the devil layer alter gaze, posture, light behavior, reflection logic, threshold framing, and one near-field bargain, judgement, temptation, contradiction, or system-facing anchor rather than replacing the role with generic dark fantasy costume.

Do not make horned shadows the default solution. Horns, tails, ember eyes, or wall silhouettes are allowed when the selected mode is `visible demon`, `literal anchor`, or `shadow-self`, but they should usually appear as one restrained staged trace, reflection, hairline shape, silhouette, or optional echo. In a seven-role devil batch, literal horned or tailed silhouettes should appear in no more than two roles unless the user explicitly asks for visible demon anatomy. Strong non-horn anchors include a sealed bargain, judgement chart, calling-card accusation, phone temptation interface, decree, corrupted receipt, surveillance/ranking screen, mismatched reflection, delayed mirror expression, broken-halo or fallen-light glow, door/window threshold, ritual candlelight, or an ordinary procedure that feels morally wrong.

The strongest devil register is often 90 percent normal and 10 percent morally or perceptually wrong: a normal adult fictional person, role, room, document, phone, mirror, or procedure with one unmistakable bargain, accusation, temptation, reflection anomaly, fallen-light cue, or institutional wrongness. Default handling is safe and non-graphic: no visible blood, gore, wounds, harmed or restrained victims, feeding, attack, torture, punishment scene, graphic body horror, or weapon use. Express danger through consent/bargain, judgement, temptation, stillness, light, reflection, procedure, and social pressure. Do not let reflection, mirror, puddle, or screen-reflection become the default answer: in a seven-role devil batch, use those as the primary devil anchor in no more than two roles by default, and route the other roles toward active anchors such as sealed bargains, tarnished halos, judgement packets, trickster receipts, decrees, procedural accusation, or direct offer gestures. If a generated prompt reads as a bowl, product, package, retail display, ordinary fashion editorial, ordinary cosplay portrait, or generic horror room before it reads as a devil concept, regenerate with a different seed or add stronger `--set prop=sealed_mission_envelope_prop|compact_mirror|single_playing_card_calling_card_prop|logo_board_prop|glowing_lantern_prop|clear_case_smartphone|holographic_screen_prop|paper_coffee_receipt`, `--set composition=reflection|frame_within_frame|puddle_inverted_reflection|over_shoulder_phone_screen|cctv_corner_frame|medium_close|low_angle_hero`, `--set light_shape=screen_rectangle_mask|monitor_rectangle_glow|hairline_rim_glow|cracked_door_sliver_light|long_corridor_shadow|neon_edge_shape`, `--set light_type=phone_screen_glow|phone_screen_face_glow|monitor_glow|neon_sign_light`, or `--set lighting=candlelit_ritual_light|low_key|monitor_glow|neon|underlit_face_horror` constraints.

Use `--explain-concept` to audit the selected devil bundle. The expected shape is either standalone `applied_mixins: ["악마"]` with no role, or one applied role plus `applied_mixins: ["악마"]`; role costumes should remain intact, and `combined_forced_slots` should include a near-field bargain, judgement, temptation, reflection, fallen-light, threshold, or system-facing anchor. For `메이드`, the sealed envelope and hand position should read as a courteous bargain before the maid costume; for `간호사`, the sealed clinical envelope should read as a final triage covenant, soul-ledger packet, or procedural accusation held near the face and hands, with underlit fallen-healer stillness and a tarnished halo rather than a generic logo board; for `경찰`, the calling card and reflective double should carry the adversary/accuser read without coercion; for `광부`, the sealed route permit or descent covenant near the hands, hard-hat headlamp, underlit face, and low-angle threshold posture should make the mine an underworld gate, not survival horror or puddle-reflection horror; for `사복 여친`, the convenience-store receipt or small paper token should read as a corrupted bargain offered directly to the viewer rather than a phone-stalking, haunting, or screen-reflection cue; for `공주`, preserve hanbok and East-Asian court identity while using fallen authority, decree, and tarnished-light cues; for `바니걸`, keep covered backstage framing and make delayed mirror expression or compact-mirror wrongness outrank stagewear display.

Generate a concept-faithful yandere prompt that treats the archetype as love curdled into possessive devotion rather than a slasher or weapon trope:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "얀데레" \
  --selection-mode rule \
  --detail-level compact \
  --plain \
  --no-negative
```

For role + yandere concepts such as `카리나 메이드 얀데레`, pass the whole phrase as one `--concept` so the resolver can preserve the role outfit and add the `얀데레` mixin:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "카리나 메이드 얀데레" \
  --selection-mode rule \
  --seed 902 \
  --include-choices
```

Use the `얀데레` concept mixin for yandere or similar obsessive-devotion archetype requests. The mixin expresses the archetype as affection curdling into possessive devotion and collapsed boundaries, not as one fixed facial expression or one prop formula. Treat yandere as a spectrum of visual subtypes: `surveillance` (records, CCTV, contact sheets, schedule boards), `possession` (red thread, names, keepsakes, white-knuckle grip), `devotion` (caregiving or service turned suffocating), `confinement` (thresholds, locks, birdcage, glass dome), `exclusion` (static erasure of rivals from photos or notes), `shrine` (oversaturated single-target wall or altar), and `collapse` (blank, teary, unfocused, or dead-eyed emotional break). Keep role outfits readable and let the yandere layer alter expression, gaze, framing closeness, posture, light, and symbolic props. Do not collapse the concept into a shallow school-uniform-plus-kitchen-knife-plus-blood cliche, visible victims, gore, self-harm, injury, coercion, sexualized framing, minors, or real-person stalking. The target of obsession should be implied only through objects such as photos, phone screens, dossiers, keepsakes, schedule boards, or shrine-like room evidence, never shown as a harmed, restrained, or controlled person.

After visual evaluation, yandere prompts must not rely only on the literal word `얀데레`, mood, generic cute/uncanny styling, a pretty cosplay smile, or a photo stack buried in the background. Role outfits and settings easily overpower the archetype: maid can become cute cosplay, nurse can become generic hospital horror, police can become ordinary noir uniform portrait, miner can become survival mine horror, casual girlfriend can become a body-display selfie, princess can become generic gothic melancholy, and bunny-girl can become stage-costume pin-up. Each standalone or role-specific bundle should make the yandere identity visible through a subtype-specific affect and one dominant near-field or environment-scale possession anchor. Do not flatten every role into the same `instant_photo_stack + red thread` formula: rotate expressions such as `mysterious_half_smile`, `cold_unreadable_stare`, `calm_intense_gaze`, `looking_away_pensive`, `emotional_teary_eyes`, `neutral_camera_gaze`, or `skeptical_side_eye`; rotate gaze/framing through direct stare, looking down on the viewer, looking away at the object, dead-eyed stillness, CCTV-like distance, mirror reflection, or extreme-wide room evidence. Assign a role-specific primary cue such as maid same-person shrine wall, nurse chart/clipboard evidence, police surveillance dossier/contact sheet, miner headlamp-lit keepsake shrine, casual girlfriend phone-screen evidence, princess birdcage/glass-dome possession, or bunny backstage compact-mirror shrine. If photos are used, make them visibly repeated photos of the same single off-frame fictional person at different dates, locations, or angles, not playing cards, trading cards, or generic paper rectangles. A few photos are not enough for a room-scale yandere read: a photo wall or shrine needs a single target repeated at overwhelming density, overlapping layers, red-string routes, handwritten dates/times, movement notes, circled details, tape, pushpins, and low-intensity static defacement such as crossed-out rival names or worn edges, while avoiding gore, wounds, or harmed people. Place the anchor beside the lit face, hand, phone, mirror edge, table foreground, badge, headlamp beam, glass case, or room-wide wall so the viewer reads possession before costume display. For weak or visually competing roles such as `경찰`, `광부`, `사복 여친`, and `바니걸`, pin the concept through actual slot choices whenever existing tags allow it: prefer `prop=instant_photo_stack` only when the role's dominant cue is photographic; otherwise prefer `prop=clear_case_smartphone`, `prop=compact_mirror`, `prop=flower_bouquet`, `prop=transparent_dome_umbrella`, `action=holding_story_prop`, `action=checking_phone`, `action=doorframe_shadow_watch`, `composition=medium_close`, `composition=reflection`, `composition=frame_within_frame`, `composition=over_shoulder_phone_screen`, `composition=cctv_corner_frame`, `composition=scrapbook_photo_cutout_layout`, `composition=extreme_wide_environmental`, `subject_framing=head_and_shoulders_crop`, `subject_framing=upper_body_framing`, `subject_framing=close_up_face_crop`, or `subject_framing=detail_crop_hands_accessories`; avoid full-body, pin-up-prone, body-display, stage-display, survival-action, or ordinary selfie posture as the main reading. For `사복 여친`, force conservative everyday wardrobe such as `wardrobe_style=faded_hoodie_sweatpants` and make phone-screen evidence primary. For `바니걸`, keep covered hostess/stage styling in face/hand/mirror framing and prevent unrelated casual wardrobe drift. `얀데레` should generally be used alone or with one role. Do not stack it with `암살자` unless the user explicitly wants that harder hybrid, because assassin weapon cues can reintroduce the blade-and-blood reading the yandere mixin is designed to avoid.

After gpt-image-2 visual review, treat `간호사`, `광부`, and `바니걸` as the highest drift-risk yandere roles. For `간호사`, avoid eyes-closed grief, funeral-like bouquet dominance, and generic hospital horror; make the open watchful gaze and chart/clipboard/bedside note evidence carry caretaking-control, while still excluding syringes, pills, blood, harmed patients, restraints, or medical misuse. For `광부`, avoid lone wilted-bouquet memorial staging and distant mine survival horror; the headlamp should visibly strike a same-person photo stack, keepsake note, or sealed side-niche shrine near the hands. For `경찰`, do not solve weak authority cues with handcuffs, restrained suspects, interrogation-room coercion, weapons, or holsters; use one-way-mirror, CCTV, badge-adjacent contact sheets, dossiers, and evidence-room surveillance density instead. For `바니걸`, do not add glossy full-body stagewear or pin-up display to strengthen the costume; keep ears, bow tie, cuffs, mirror, face, and hands in a close covered backstage composition so the possession cue is read before the costume.

After the next gpt-image-2 review, also treat yandere motif diversity as a first-class quality gate. Role-specific yandere recipes should have multiple seed-selectable subtype variants where the role is weak or visually competing; use `--explain-concept` to check `selected_bundles[0].subtype` and change `--seed` when a batch collapses into one visual grammar. In a seven-role batch, do not let more than two or three roles use a broad photo-wall or `instant_photo_stack + red thread` as the primary anchor. Keep strong shrine/surveillance roles such as maid or police allowed to use dense same-person evidence walls, but route the remaining roles toward chart/phone evidence, route ownership, decree or birdcage confinement, glass-dome preservation, backstage phone logs, doorway watching, mirror doubling, or object fixation. Red thread should usually be secondary unless the selected subtype is explicitly red-thread possession; when a bundle is about phone-screen evidence, chart-like notes, sealed decrees, side niches, glass domes, or birdcage symbolism, avoid adding an extra broad background photo wall.

After the following gpt-image-2 review, apply a stricter weak-role yandere gate: the dominant yandere read should survive a costume swap. If `costume_style` or `wardrobe_style` were replaced with plain everyday clothes, the remaining `prop`, `action`, `composition`, `location`, and near-field evidence should still read as possessive devotion, surveillance, confinement, or emotional collapse. This is mandatory for `간호사`, `광부`, and `바니걸`, because the generated images can otherwise collapse into a hospital selfie, mine mood portrait, or pretty backstage cosplay. Do not leave the real yandere cue only in `additional` prose for these roles; pin it through slots and place it next to the lit face, hands, doorway, bed threshold, headlamp beam, vanity mirror, route marker, or board.

When dedicated non-photo props are absent from `photo_prompt_tags.json`, repurpose existing props explicitly and say what they must read as: use `logo_board_prop` for clinical charts, care-record boards, reservation logs, booking boards, or route boards; use `sealed_mission_envelope_prop` for sealed decrees, claim papers, route permits, access documents, or possession records; use `holographic_screen_prop` for CCTV monitors or screen walls; use `transparent_dome_umbrella` for glass-dome keepsakes; and use `clear_umbrella` or `paper_umbrella_prop` only as threshold/barrier symbols. In seven-role yandere batches, cap `instant_photo_stack` to two roles and avoid letting `clear_case_smartphone` become the dominant anchor for more than three roles; at least two weak or institutional roles should use non-photo/non-phone board, document, monitor, dome, or barrier anchors. Strengthen intensity through charts, records, booking logs, sealed documents, route control, monitors, thresholds, and object ownership rather than through weapons, blood, or harmed people.

Yandere weapon or blood cues are allowed only as fictional visual symbolism when the user explicitly asks for that harder register, and they must stay static, non-instructional, and non-graphic. The default yandere recipe remains bloodless and victimless. If the user explicitly asks for a weapon, prefer inert or sheathed props, a clean object held still or lying on a table, a closed drawer silhouette, or an absence cue such as an empty knife slot; do not depict aiming, swinging, use, injury, visible victims, restraints, gore, or aftermath bodies. If the user explicitly asks for blood, keep it to tiny symbolic stains, red liquid, red smears on paper, red thread, or theatrical color accents rather than gore or wounds. Use `암살자` only when the user wants operational assassin imagery; use yandere symbolic-threat wording when the request is about obsessive romance horror rather than action.

Use `--explain-concept` to audit the selected yandere bundle. The expected shape is either standalone `applied_mixins: ["얀데레"]` with no role, or one applied role plus `applied_mixins: ["얀데레"]`; role costumes should remain intact, the selected bundle should keep face/upper-body/hand/mirror framing, and there should be no weapon cue unless the user also explicitly includes `암살자`. Check `combined_forced_slots.expression`, `prop`, `action`, `composition`, and `subject_framing`: role batches should vary gaze/affect instead of repeating one stare, and weak roles should pin the dominant possession anchor through slots rather than free prose only. For `사복 여친`, check that the generated requirements keep the subject an original adult fictional character and not a real-person stalking scenario. For `간호사`, check that a chart/records board and watchful care-control outrank grief, medical-horror cues, bouquet props, and phone-selfie staging. For `광부`, check that route ownership, sealed access documents, blocked tunnel framing, or side-niche control outrank mine atmosphere and survival action. For `바니걸`, check that booking-board or reservation-log possession outranks glossy stagewear, mirror glam, or pin-up display, and that no unrelated `wardrobe_style` override turns the image into casual fashion without the only-audience obsession.

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

Run the real semantic quality gate before treating semantic-policy or concept-mode changes as quality-improving evidence:

```bash
python3 skills/photo-prompt-image-generator/scripts/eval_semantic.py --quality-gate --quality-runs 2
```

`--quality-gate` requires real Gemini embeddings and a valid semantic index; it intentionally rejects `--mock-embeddings`. The gate reports legacy concept-mode pass/fail separately from soft concept-mode promotion readiness. Add `--quality-require-soft` only when a change is intended to promote `--concept-mode soft`. Rule mode still rejects `--intent`; with `--concept-lock`, it may use semantic-policy lexicons only as deterministic weighted-rule bias, not as semantic retrieval.

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
- For princess or `공주` requests, use the existing `공주` role recipe rather than a bare fairytale concept lock. Preserve Korean Joseon court identity through `royal_princess_hanbok`, `royal_princess_chamber`, traditional court ornament language, lineage, ceremonial posture, and palace restraint. To express deeper princess themes, choose one dominant axis at a time: lineage/succession, power-yet-powerlessness, protected confinement, public ceremonial display, or awakening into rule. Pin the axis with explicit slots such as `prop=sealed_mission_envelope_prop`, `composition=centered_symmetry|frame_within_frame`, `action=standing_silence|court_fan_pose|holding_story_prop|doorframe_shadow_watch`, and `light_shape=venetian_blind_shadows|hairline_rim_glow` plus concrete `--additional-requirement` text. Do not let `공주` collapse into a Western ballgown, corset, gem-tiara fantasy, generic gothic princess, damsel-in-distress pose, sexualized framing, minors-coding, or decorative cosplay.
- For vampire or similar supernatural archetype requests, use the `흡혈귀` concept mixin or the closest gothic/horror preset plus `--concept-lock`; express the creature through atmosphere, body language, daylight refusal, mirror/reflection unease, moonlit pallor, withered-life cues, bat-like shadows, coffin-like geometry, antique portraits, ruby/crimson accents, dark red wine as a prop beverage, and room effects, not through gore, victims, feeding, exposed fangs, or visible blood. Do not force a generic gothic dress or candle studio over a more specific role outfit, and do not let the output collapse into generic gothic fashion, ordinary moody lifestyle photography, plain hospital horror, ordinary police cosplay, nightclub/stage-costume display, or mine horror without a clear vampire anchor. The strongest vampire cue should be close to the subject's lit face, hand, phone, mirror, badge, jewelry, or foreground reflection, with role-specific `subject_framing` where needed; historical Korean roles must preserve hanbok/East-Asian court identity instead of becoming Western gothic royalty.
- For devil, demon, tempter, fallen-light, adversary, or similar diabolical archetype requests where the user says `악마`, use the `악마` concept mixin rather than a bare semantic concept lock. Express the concept through temptation/contract, accusation, fallen light, shadow-self, liminal thresholds, underlighting, occult noir, mismatched reflections, and one near-field visible anchor such as a sealed bargain, calling-card accusation, judgement packet, compact mirror, corrupted receipt, phone temptation interface, lantern/headlamp cue, or broken-halo glow. Keep any role outfit readable and make the devil cue appear beside the lit face, hand, phone, mirror, badge, envelope, chart, lantern, or foreground reflection. Do not let `악마` collapse into product/commercial still life, ordinary dark fashion, generic gothic cosplay, distant ritual mood, gore, visible victims, attack, punishment, or weapon-use scenes. For weak roles, prefer active anchors over reflection by adding explicit `--set prop=sealed_mission_envelope_prop|single_playing_card_calling_card_prop|logo_board_prop|compact_mirror|clear_case_smartphone|glowing_lantern_prop|paper_coffee_receipt`, `--set composition=frame_within_frame|medium_close|low_angle_hero|reflection|puddle_inverted_reflection`, `--set light_shape=hairline_rim_glow|neon_edge_shape|screen_rectangle_mask`, or `--set lighting=underlit_face_horror|candlelit_ritual_light|neon` constraints instead of trusting the word alone. In multi-role batches, cap reflection, mirror, puddle, or screen-reflection as the primary devil anchor at two roles by default.
- For femme fatale or similar dangerous-intelligent-woman archetype requests, use the `팜므파탈` concept mixin or the closest noir/editorial preset plus `--concept-lock`; express the archetype through gaze reversal, authority, controlled stillness, noir/symbolist light, reflection/doubling, threshold framing, quiet omen props, visible information-control anchors, and when role-appropriate magnetic lure-as-weapon where the invitation itself is the trap. The concept is about agency, intelligence, danger, and the viewer being observed or deliberately drawn in under her control, not sexual availability. Do not rewrite it into lingerie, cleavage-centered framing, pin-up posing, bedroom eyes, come-hither gestures, explicit content, visible victims, or depicted violence. For service/fetish-coded or action-coded roles, add stronger power-reversal anchors so the role reads as a disguise, authority position, room-operator identity, or leverage holder rather than cosplay display; in semantic mode, add explicit `--intent-axis` or `--set subject_framing=...` constraints rather than trusting free-text `no pin-up` wording alone.
- For menhera, yami-kawaii, jirai-kei, or similar cute-but-fragile emotional-subculture requests, use the `멘헤라` concept mixin or the closest candid phone/social portrait preset plus `--concept-lock`; express the concept through phone glow, unread-message waiting, teary or blank distant gaze, Igari-style tired eye makeup, wilted flowers, cracked mirrors, loosened ribbons, protective cute props, cluttered pastel bedrooms, hospital waiting-room light, cool digicam grain, and soft pastel or cold fluorescent palettes. Treat it as a subculture mood about attachment and quiet burnout, not a diagnosis, self-harm scene, crisis spectacle, or stigmatizing "crazy girlfriend" caricature. Do not render wounds, scars, blood, bandaged wrists, medication, pills, syringes, IV lines, overdose, suicidal staging, minors, nudity, sexualized vulnerability, fetish staging, or pin-up framing. For `간호사`, `사복 여친`, and `바니걸`, audit `--explain-concept` and actual `prompt_en` because medical-risk imagery, youthful-minor coding, and stage-costume display are the highest-risk drift modes. The most common quality failure is different: weak role bundles such as `경찰`, `광부`, `사복 여친`, and sometimes `공주` can read as pretty cosplay or ordinary tired phone use unless the anxiety anchor is pinned through actual `expression`, `prop`, `composition`, or `light_type` slots plus concrete `Additional requirements`.
- For tsundere or similar cold-on-the-surface, warm-underneath requests, use the `츤데레` concept mixin or the closest candid/intimate portrait preset plus `--concept-lock`; express the archetype through one visible denial-vs-evidence contradiction: a defensive first read (averted face, turned shoulder, crossed arms, guarded side glance, lowered gaze, object-as-soft-barrier, huffed/pursed mouth, suppressed pout, raised chin, chart-tapping scold, brisk dismissive hand) plus a leaked second read (faint ear-tip or nose-bridge warmth, wavering peeking glance, fidgeting hands, posture contradiction, or a caring object such as a lunchbox, gift, shared umbrella, two coffees, knit scarf, note, returned item, or personal token) beside the same face. Side-eye is optional, not the default; blush should be subtle and photographic, with cheeks mostly neutral and skin texture intact, not heavy Igari/anime redness. It is warm and comedic-romantic, with alive embarrassed eyes, not yandere obsession, femme-fatale power, or menhera depressive waiting. Never use surveillance, repeated photos, red thread, weapons, gore, victims, sexualized framing, or minors. For weak roles, pin the contradiction through `expression`, `makeup_style=natural_makeup`, `prop`, `action`, `composition`, and `subject_framing` slots rather than the bare word `츤데레`, keep the caring object in the same crop as the active rejection cue, and apply the micro-expression/costume-swap/frame-budget gate: face plus hands plus caring object must read before costume body, with no full-body costume display, side hip pose, chest-forward crop, rim-lit fashion glamour, or sultry authority pose. In multi-role batches, avoid side-eye and coffee convergence by keeping `skeptical_side_eye` to one role by default and coffee/takeaway drink as the primary caring anchor for no more than one role unless explicitly requested, moving weaker roles to role-specific chart, umbrella, blanket, modest wrapped gift/lunchbox, note, ticket, coat, or hanbok token anchors. Also block the newest observed drift modes: demure service smile, professional bedside manner, listless/sad girlfriend framing, and fragile courtly shyness.
- For yandere or similar obsessive-devotion archetype requests, use the `얀데레` concept mixin or the closest intimate/uncanny portrait preset plus `--concept-lock`; express the archetype as fictional possessive devotion and collapsed boundaries across multiple subtypes, including surveillance, possession, devotion, confinement, exclusion, shrine, and emotional collapse. Do not reduce it to `instant_photo_stack + red thread + mysterious_half_smile`: rotate expression and gaze through hollow half-smile, cold unreadable stare, direct blank stare, looking-away fixation, teary collapse, high-angle control, CCTV distance, mirror doubling, and room-wide evidence. The concept is not a real psychiatric diagnosis, not a default slasher scene, and not real-person stalking. Do not rewrite it into school-uniform-plus-knife-and-blood imagery, gore, visible victims, coercion, self-harm, sexualized framing, minors, or a harmed/restrained person. After image review, weak roles must use deterministic anchors rather than trusting prose: attach one dominant role-specific possession cue to the lit face, hand, phone, mirror edge, table foreground, badge, headlamp beam, glass case, board, sealed document, threshold, or oversaturated wall, and use close crops or environment-wide evidence intentionally. For photo walls, require single-target repetition at overwhelming density with overlapping photos, red-string routes, handwritten dates/times, movement notes, circled details, tape, pins, and low-intensity static defacement; a few photos read as ordinary photography. For `간호사`, make chart/records-board evidence and open watchful care-control outrank eyes-closed grief, funeral flowers, phone selfies, or medical-horror props; for `경찰`, use CCTV/one-way-mirror/dossier density instead of handcuffs, restraints, suspects, weapons, or coercive interrogation; for `사복 여친`, avoid `mirror_selfie` body-display drift by forcing conservative everyday wardrobe and phone-screen possession cues; for `바니걸`, keep covered hostess/stage styling in face/hand/board/mirror framing and make single-name booking or reservation logs outrank glossy stagewear; for `광부`, keep sealed route documents, side-niche markers, or same-person keepsake evidence close to the hand or headlamp so the mine does not dominate. Weapon or blood cues are symbolic only when explicitly requested: keep them static, clean/sheathed/low-intensity, non-instructional, non-graphic, and never paired with a visible victim, injury, coercion, or depicted use. Add explicit `--intent-axis` or `--set prop=instant_photo_stack|clear_case_smartphone|compact_mirror|logo_board_prop|sealed_mission_envelope_prop|transparent_dome_umbrella` / `--set subject_framing=...` / `--set composition=...` constraints rather than trusting the word `얀데레` alone.
- For multi-role yandere batches, audit motif diversity before rendering. If `--explain-concept` shows that too many roles selected `instant_photo_stack`, broad photo-wall language, red-thread possession, or phone-screen possession, change seeds for drift-risk roles or prefer variants whose primary cue is a chart/records board, side niche, sealed route/decree/access document, birdcage/glass-dome symbol, compact mirror, CCTV monitor, or backstage reservation board. A strong photo wall is still correct for shrine/surveillance subtypes, but it should not be the default solution for every role. For weak roles, apply the costume-swap test: the yandere read must survive even if the role outfit is replaced by plain clothes.
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
