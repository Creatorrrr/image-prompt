---
name: photo-prompt-image-generator
description: Generate image-ready photo prompts and images in this project using the bundled prompt_generator.py and photo_prompt_tags.json. Use when the user asks for random photo prompts, preset-based photo prompts, or image generation from this project's prompt tag dictionary.
---

# Photo Prompt Image Generator

## What This Skill Does

Use this project-local skill to generate a structured photo prompt from the bundled tag dictionary, then call image generation when the user asks for an actual image.

Bundled resources:

- `scripts/prompt_generator.py`: original prompt generator CLI.
- `assets/photo_prompt_tags.json`: tag dictionary, presets, coherence rules (slot conflicts), semantic policy.
- `assets/photo_prompt_semantic_index.json`: Gemini Embedding 2 semantic index for the default intent-based selection path.
- `assets/concept_recipes.json`: deterministic short Korean concept recipes. Per-concept knowledge lives here as data: `guide` (definition, dominant axes, anchor guidance, anti-patterns, batch rules) and `review_gates` (machine-checkable and manual audit gates).
- `assets/run_ledger.schema.json`: schema for image-generation attempt records.
- `scripts/generate_photo_prompt.py`: wrapper with project-local defaults and the concept resolver.
- `scripts/audit_composed_prompt.py`: validates an agent-composed prompt against a generated candidate pack.
- `scripts/record_image_run.py`: validates and appends external image-generation attempts to the local run ledger.
- `scripts/generate_images_via_api.py`: direct OpenAI Images API generation for saved prompt JSON (byte-identical forwarding, automatic ledger records).
- `scripts/build_semantic_index.py`: rebuilds the Gemini semantic index after dictionary changes.
- `scripts/validate_photo_prompt_dictionary.py`: validates dictionary metadata, recipes, guides/gates, and SKILL.md literals.
- `scripts/eval_semantic.py`: retrieval/diversity/quality/contradiction evaluation harness.

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

1. Generate one candidate pack with JSON output. The wrapper defaults to semantic mode and uses a broad photographic intent when the user does not provide `--intent`:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --emit-candidate-pack
```

For multi-concept batches, repeated retries, or subagent runs that should avoid converging on the same anchors, create one shared temporary ledger and pass it to every candidate-pack call:

```bash
LEDGER="$(mktemp -t photo-prompt-anchor-ledger.XXXXXX.json)"
python3 skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --concept "닝닝 경찰 수인" --emit-candidate-pack --anchor-diversity-ledger "$LEDGER" > candidate_pack.json
```

2. Compose the final prompt as the agent, using the candidate pack as source material:
   - Every item in `mandatory_intents` is required. Reflect it as a visible image anchor.
   - If an intent has no useful preset/tag candidate, preserve it with direct free description and add `coverage_assertions` that map the original intent text to the English phrase used in `prompt_en`.
   - Choose candidate ids from `presets[].id` and `slots.*.candidates[].id`; do not choose both sides of a hard conflict listed in `conflicts`.
   - Respect `role_scene_policy`: when enabled, choose a role-compatible location and do not use forbidden generic scene locks such as highland/pasture defaults unless the user explicitly requested that place.
   - Respect `species_family`: when enabled, species marker, texture, and anatomical connection must come from the same locked family unless the user explicitly asked for a hybrid.
   - Use `diversity_state` as a warning surface. If the pack says a candidate is repeated or penalized, prefer an equivalent non-repeated candidate when it still preserves the concept.
   - Treat `concept_axes.required` as the non-negotiable meaning layer. Cover each axis visibly through the scene, object behavior, expression, framing, or `coverage_assertions`; do not satisfy an axis only by naming the concept.
   - A `coverage_assertions` value must describe a visual phenomenon, not readable text. Signs, receipts, labels, screens, captions, or legible contract wording do not satisfy a concept axis; rewrite them as object behavior, light behavior, reflection, gesture, material change, or symbolic marks.
   - For subtle or supernatural concepts, mark one required concept's assertion as the primary visual anchor, for example `{"서큐버스": "primary visual anchor: wrong reflection in the vanity mirror"}`. The primary anchor must be foreground or clearly in focus; generic markers such as horns, tails, wings, or fangs cannot be the primary anchor.
   - Treat `motif_budget` and `motif_pools` as interchangeable reference material, not a template. When `discouraged_now` names a motif, avoid it unless the user explicitly requested that exact motif.
   - Treat `preset_reference` as provenance for what was consulted, not as the final scene. `used_sections` are reference scaffolding; `dropped_sections` and `masked_buckets` are deliberate creative openings.
   - Fill every `open_slots` bucket freely within the user request, safety floor, and identity axes. Do not reconstruct the masked `candidate_id`, `masked_entry_id`, or listed terms from the preset/bundle unless the user explicitly asked for that exact object or scene.
   - Preserve `negative_en` from the pack unless the user explicitly requests a different negative prompt.
   - Output composed JSON with `pack_id`, `prompt_en`, `negative_en`, `chosen_candidate_ids`, `composer: "agent"`, and optional `coverage_assertions`.
3. Audit the composed prompt before image generation:

```bash
python3 skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py --pack candidate_pack.json --composed composed_prompt.json
```

If the audit fails, rewrite the composed prompt or change the chosen candidate ids and rerun the audit. Do not generate an image from a failed audit.
4. Use the audited `prompt_en` as the primary image prompt unless the user explicitly wants Korean-only output.
5. If a negative prompt is present, append it to the image request as `Avoid: ...`.
6. Generate the image when the user asks to create, render, or generate one. Tool priority is strict:
   - **First, always use the session's built-in/native image generation tool** (e.g. Codex `image_gen`) with the final prompt. If you used the built-in tool, you must then perform the worktree save and ledger steps yourself.
   - **Only fall back to the bundled direct-API script below if you have actually verified that no built-in image tool is exposed in this session, or a built-in call failed with an environment error** (tool-not-available, sandbox/DNS network failure). Do not pick the API path merely because it is more convenient or automates the bookkeeping; convenience is not a fallback trigger.
   - The fallback script forwards the prompt byte-identical and performs the worktree save plus ledger records (`tool: openai_images_api`) automatically:

```bash
python3 skills/photo-prompt-image-generator/scripts/generate_images_via_api.py --prompt-json <generator-output.json> --concept "<컨셉>"
```
   - In either path, report which tool generated the images; the ledger `tool` field must reflect it (`image_gen` vs `openai_images_api`).
7. After every built-in image generation call, immediately identify the exact newly created file path under `/Users/chasoik/.codex/generated_images` before starting another generation or copying any files. Do not infer the result from a broad mtime search across unrelated worktrees.
8. Copy every successful generated image into this worktree before reporting it. Use `generated_images/<concept>-<timestamp>/` where `<concept>` is a filesystem-safe concept slug and `<timestamp>` is the generation timestamp, and name each file with `prompt_id`, `seed`, and `attempt`, for example `d97311a76c77b29f-seed902-attempt1.png`. Leave the original global generated image file in place.
9. If the user asks for unchanged retries, keep `prompt_en` and `negative_en` byte-for-byte unchanged for each retry. Use the composed prompt's `prompt_id` or the recorder-computed id as the identity for the prompt and retry failed attempts up to the requested budget before reporting remaining failures.
10. Record each image-generation attempt in this worktree's `runs/image_runs.ndjson` with `scripts/record_image_run.py`, including the worktree-local `generated_images/...` path and, when available, `pack_id`, `chosen_candidate_ids`, `composer`, and `audit_status`. This is required for retry chains, safety/filter failures, and multi-worktree provenance.
   - For `safety_block` or `error` outcomes, include a categorized token in `--failure-reason` when it is knowable, such as `role_fetish_costume`, `body_exposure`, `text_anchor`, `tool_error`, or `policy_unknown`. For successful images whose concept read is weak, record the `concept_salience` verdict in the batch evaluation artifact or final report next to the ledger `run_id`.
11. If the user asks only for prompts, return the audited composed prompt text and do not generate an image.

## Useful Commands

```bash
# Discovery
python3 .../generate_photo_prompt.py --list-presets --plain          # 441+ presets (add --include-virtual for recipe presets)
python3 .../generate_photo_prompt.py --show-slots --plain            # 74+ slots
python3 .../generate_photo_prompt.py --list-tags <slot> --plain      # ids for one slot
python3 .../generate_photo_prompt.py --concept "카리나 메이드 흡혈귀" --emit-candidate-pack > candidate_pack.json
python3 .../audit_composed_prompt.py --pack candidate_pack.json --composed composed_prompt.json

# Validation and evaluation (no image generation required)
python3 .../validate_photo_prompt_dictionary.py                      # dictionary + recipes + guides/gates + SKILL.md literals
python3 .../eval_semantic.py --check-index                           # stale-index detection
python3 .../eval_semantic.py --contradiction-check                   # rule-mode sweep against declared slot conflicts
python3 .../eval_semantic.py --mock-embeddings --limit 3             # CI structure checks
python3 .../eval_semantic.py --diversity-check                       # free-slot diversity + beastkin role-scene matrix gate
python3 .../eval_semantic.py --quality-gate --quality-runs 2         # real-embedding quality gate (API key required)

# Rebuild the semantic index after dictionary edits (only changed entries are re-embedded)
GEMINI_API_KEY=... python3 .../build_semantic_index.py --progress
```

The API key must come from `GEMINI_API_KEY` or `GOOGLE_API_KEY`; do not store it in the repository. The wrapper and index builder also load these keys from a project `.env` file when present, without printing them. Rule mode does not require the Gemini SDK or an API key.

Rebuild policy: `dictionary_hash` tracks tag/preset/slot/facet fields that feed entry embedding text — rebuild the index when those change (including entry `facets`). Policy-only edits under `semantic_policy` and rule edits under `coherence_rules` do not require a rebuild. Golden snapshot tests (`tests/test_golden_snapshots.py`) pin rule-mode outputs; regenerate them with `UPDATE_GOLDEN=1` only for intentional changes and review the fixture diff.

## Generation Modes and Diversity Controls

```bash
# Reproducible rule-mode generation
python3 .../generate_photo_prompt.py --preset street_documentary --seed 42 --selection-mode rule

# Semantic generation with an explicit intent
python3 .../generate_photo_prompt.py --intent "rainy neon night street portrait" --selection-mode semantic --include-trace

# Concept-faithful variants that must not drift from a compact scene concept
python3 .../generate_photo_prompt.py \
  --intent "cozy homebody guy in a small lived-in bedroom at night" \
  --concept-lock "방구석 집돌이 컨셉, 작은 방, 모니터 빛, 게임패드" \
  --intent-axis "homebody guy in small bedroom" --n 3
```

- The wrapper defaults to `--selection-mode semantic`; `--selection-mode rule` forces the deterministic weighted path. `--intent` is rejected in rule mode.
- Semantic defaults: `--filter-strictness soft`, `--semantic-profile balanced`, `--semantic-axis-mode auto`, `--intent-steering auto`, `--semantic-weight 0.75`. Hybrid defaults to hard filters, conservative profile, weight `0.35`.
- `--creativity 0..1` is the single diversity lever: 0 maps to conservative/low-novelty, 0.5 to balanced/medium, 1 to exploratory/high (continuous interpolation of profile windows, sampling temperature, and batch-diversity pressure). Explicit `--novelty` or `--semantic-profile` always wins over the lever. Coherence controls (`--semantic-weight`, `--filter-strictness`) are intentionally separate: they trade off correctness, not creativity.
- Declared cross-slot contradiction rules live in `photo_prompt_tags.json` under `coherence_rules.slot_conflicts` (hard = candidate filtered, soft = weight penalty) and `coherence_rules.slot_context_rules`. Add new contradictions there, not in Python; verify with `--contradiction-check`.
- Use repeated `--intent-axis "..."` for explicit required semantic axes; `--intent-steering off` keeps ranking without slot steering.
- Use `--seed` for reproducible variants; `--n` plus a stable `--concept-lock` for a spectrum around one concept.

## Concept Workflow

Short Korean concepts (`--concept "카리나 메이드 흡혈귀"`) resolve through `concept_recipes.json`: one optional role + zero or more mixins + seed-selected bundles. Always pass the whole phrase as one `--concept` so the resolver keeps the role anchor and layers mixins on top.

```bash
# 1. Audit the resolution before generating
python3 .../generate_photo_prompt.py --concept "카리나 메이드 흡혈귀" --seed 701 --explain-concept

# 2. Generate a candidate pack when the explanation looks right
python3 .../generate_photo_prompt.py --concept "카리나 메이드 흡혈귀" --seed 701 --emit-candidate-pack > candidate_pack.json
```

`--explain-concept` output is the single audit surface per concept:

- `gate_results`: auto-evaluated machine gates (`pass`/`fail`) plus `manual` gates. Machine gates check the resolution shape (`applied_mixins`, role costume preservation, required forced slots). If a machine gate fails, change `--seed`, fix the concept phrase, or pin slots with `--set`; do not generate from a failing resolution.
- `guide`: per-concept definition, dominant axes, anchor guidance, anti-patterns, and batch rules migrated from this document. Read it instead of guessing what a concept means.
- `manual` gates: apply them when reviewing generated images (costume-swap test, dual-read test, anchor visibility, batch motif quotas). The generic costume-swap test: if the role outfit were replaced with plain clothes, the concept's anchors must still carry the reading. The dual-read and anchor-visibility tests include a blind-read pass: from the image alone, at least one primary anchor must make the non-obvious concept identifiable without reading the prompt text. Generic markers such as horns, tails, wings, or fangs do not count toward this primary anchor.
- `selected_bundles[0].subtype`: check motif diversity in multi-role batches; change seeds for roles that converge on one visual grammar.
- `combined_forced_slots`: legacy mode applies these as forced slots; verify the expected anchors are pinned through slots, not only prose.

Concept-mode defaults:

- `--concept-mode legacy` is the global default and keeps behavior-compatible forced-slot expansion.
- `--emit-candidate-pack` promotes unresolved `--concept` requests to `--concept-mode soft` unless the user explicitly supplies `--concept-mode`. This keeps role/mixin anchors as candidate material instead of collapsing them into one forced preset/slot path.
- `--concept-mode soft` forwards pool-based soft anchors instead of forced values. Recipes may opt in per concept via `concept_mode_default: "soft"` once they pass `eval_semantic.py --quality-gate --quality-require-soft`; an explicit `--concept-mode` always wins.
- `anchor_pool` entries accept in-pool weights (`{"id": "...", "w": 3}`) so soft mode samples related variety while keeping identity anchors dominant.
- `soft_anchor_defaults.anchor_expansion` (opt-in, default off) widens soft anchor pools with same-slot embedding neighbors at reduced weight; expanded members remain subject to all hard guards and slot conflicts.
- Role + body-trait concepts should keep the role scene first. For example, role recipes may define `role_scene_policy.allowed_locations`; mixins like `수인` provide body evidence and species-family support without owning the location/preset unless the role has no scene pool.
- Species variants lock `species_marker`, `texture`, and `anatomical_connection` to one family per prompt. Use a shared `--anchor-diversity-ledger` across independent calls when a batch should rotate species families and anchor details.

Concept-data conventions when editing `concept_recipes.json`:

- Roles read through workplace, costume, action, and prop anchors; mixins are visible-anchor recipes (face/hand/prop/location evidence), not vibe words. Bundles must preserve the role anchor when overriding a slot; unrelated roles fall back to the base mixin.
- Persona registers (`청순`, `걸크러시`, `몽환`, `터프`, ...) steer expression, posture, wardrobe, and light without replacing the role. Relationship-grammar slots (`relational_action`, `prop_direction`, `partner_role`, `partner_framing`, `gaze_target`, `proxemics`, ...) are first-class controls for relational concepts; visible multi-subject support is opt-in through `partner_role`/`partner_framing` values.
- Succubus-style dream-demon mixins must not collapse to horns/tail/wings, readable text, or fetish framing. Preserve the role outfit as professional/in-role identity and make the concept visible through at least two scene anchors, at least one of them primary/foreground. Prefer contract-by-symbol (wax seal, drawn sigil, offered hand), invitation/threshold (doorway or beckoning gesture into a space), wrong reflection (mirror/window disagreeing with the pose or showing an impossible silhouette), life-drain trace (wilting flowers, guttering candle, frost or pallor on nearby objects, never on a victim body), gaze bargain (direct contractual eye contact or a token passed between hands), or light behaving against its source near the face or hands. Render the seduction register as atmosphere and symbol, never as exposure, contact, or a sleeping/drained partner.
- New per-concept guidance goes into the recipe's `guide`/`review_gates` fields (validated by `validate_photo_prompt_dictionary.py`), not into this document. Per-concept sensitive-role lists, approved primary-anchor catalogs, and no-text-anchor gates should live in the recipe review gates when they can be machine-checked.

### Making Concept Cues Survive to the Rendered Image

A composed prompt that passes `audit_composed_prompt.py` is not yet a readable image. The audit checks textual coverage and conflicts; it does not prove that the concept will be visible after rendering. Apply these cross-concept rules at composition time and again when reviewing generated images:

- **No readable-text anchors.** A concept axis is never satisfied by readable text, lettering, signage, receipts, labels, screen text, or contract wording. Keep `no text or watermark` unless the user explicitly asks for legible text as the subject. If the concept needs a pact, warning, message, or invitation, express it as a wax seal, symbolic marks, object placement, gaze, reflection, or light behavior instead.
- **Salience floor.** At least one required concept anchor must be primary: foreground or clearly in focus, close to the face/hands/central prop, and capable of defining the concept on its own. Ambient cues such as faint haze, distant silhouettes, or minor color grading are secondary and cannot satisfy the salience floor by themselves.
- **Generic-marker credit.** For body-trait and dream-demon archetypes, off-the-shelf markers such as horns, tails, wings, fangs, slit pupils, halos, or clip-on costume parts count as zero toward the primary anchor floor unless the user explicitly requested that exact marker. They may appear as supporting details, but if the concept depends on them, treat it as template collapse and recompose.
- **Scene-poor role reinforcement.** Roles with weak visual grammar, such as casual girlfriend, office worker, miner, or study/student-adjacent scenes, need stronger environmental anchoring than rich costume roles. Push the concept into environment, object behavior, reflection, light behavior, and gaze instead of relying on a single handheld prop or text cue.
- **Blind-read review.** After generation, evaluate whether the image communicates the role and the non-obvious concept without looking at the prompt. If the role is clear but the concept is only inferable from prompt text, mark the image as partial/fail in the evaluation even when generation succeeded.

Safety floor for all concepts (recipes carry concept-specific rules in `safety_requirements`/`concept_safety`):

- Subjects are original adult fictional people; use `--likeness-mode inspired` when a public figure or idol is named. `학생` always means adult-only school-uniform styling, covered and non-minor-coded.
- Uniform/service roles read as professional identity, not fetish framing. Keep role outfits covered and readable.
- Run a role-fetish pre-check before generation whenever a uniform, service role, bunny/costume role, nurse role, maid role, or other commonly sexualized costume is combined with a dream/seduction archetype. Preserve the requested concept, but move the supernatural or seductive meaning onto scene/light/reflection/contract symbols rather than body display, costume exposure, or body-first framing. This is concept redistribution, not silent prompt softening. If a block still occurs, record the block honestly instead of rewriting and retrying without telling the user.
- Non-graphic always: no gore, wounds, blood, victims, self-harm, medical misuse, coercion, or sexualized vulnerability. Folk/religious/divine imagery stays respectful; horror stays atmospheric. Weapon cues only when explicitly requested, always sheathed/inert/static.
- Dream/seduction archetypes such as `서큐버스` stay symbolic and adult-only: no explicit sex, nudity, sleeping-victim harm, drained bodies, coercive contact, bedroom-victim staging, or role-fetish replacement.
- Glitch/tech concepts keep faces, eyes, hands, and text clean; body-trait archetypes (수인, 용인, 리빙돌, ...) use body-rooted, non-graphic evidence, never detachable-costume shortcuts.

## Preset Routing

- Map the request to the most specific preset family first; fall back to broad portrait presets last. Families cover: compact/ReactorPrompt styles (`compact_urban_fashion_portrait`, `compact_cinematic_prop_portrait`), K-traditional and period (`hanbok_seasonal_editorial`, `joseon_period_portrait`, `wuxia_xianxia_portrait`), cosplay-specific, K-pop, Korean local spaces, craft/product, optical experiments, manual trades, sports action, underwater, forensics, 7080 retro, live music, architecture, maritime labor, subculture, family documentary, night-sky, relationship/daily-realism, beastkin/perspective, and psychological/symbolic concept families.
- For era fashion use `retro_era_fashion_editorial`; for extreme-environment contrast editorials use `surreal_contrast_editorial` (normal photo slots — do not force `surreal_*` slots).
- For photoreal surreal requests use the closest photo preset plus `--surreal-mode on` (optionally `--surreal-intensity`, `--set surreal_anchor=...`); `--surreal-mode auto --surreal-probability <p>` only for explicitly mixed batches.
- For physical fantasy/cosplay-prop/cinematic story portraits use `cinematic_fantasy_portrait`; keep weapons framed as nonfunctional cosplay props.
- For ordinary non-adult social trends prefer `clean_mirror_selfie_snapshot`, `retro_direct_flash_party_snapshot`, `candid_iphone_portrait`, or `creator_brand_profile`. Use `--reference-edit-mode` only with actual reference images; `--trend-layer` only when the user asks for that format.
- For sexual-suggestive or fetish-fashion moderation tests, use only adult-compatible presets (`adult_boundary_social_stress_test`, `adult_fetish_fashion_editorial`); never attach adult-only styling slots to childlike, student, family, pet, wildlife, or other incompatible contexts.

## Prompt Handling

- Prefer `prompt_en` for image tools.
- Preserve user-specified subject, location, format, camera, lighting, mood, and aspect instructions by mapping them to `--preset` or `--set` when an exact tag exists; keep unrepresented constraints in `--concept-lock` first, then `--additional-requirement` for concrete leftover details. Do not add hidden LLM calls to the deterministic scripts.
- Map neutral fashion/selfie terms to `wardrobe_style`/`makeup_style`/`expression`/`subject_framing`, separate from adult-only slots.
- Do not force non-photo requests (posters, infographics, stickers, UI, typography, webtoon, illustration) through this generator, and do not add design-only concepts to the dictionary. Treat ReactorPrompt export artifacts (EXIF notes, scraper labels) as noise.
- Preserve candidate-pack ids, chosen slot selections, `negative_en`, and audited `prompt_en` exactly after composition unless the user explicitly asks to edit them or the output is unusable. Do not silently soften or rewrite an audited prompt before image generation; if it is off-theme, regenerate or revise the composed prompt and rerun `audit_composed_prompt.py`.
- Do not edit `assets/photo_prompt_tags.json` unless the user explicitly asks to change the tag dictionary. Use `--plain` only for human-readable list commands.
- In semantic mode, preset filters are soft priors; safety/context guards stay hard. `--filter-strictness hard` restores legacy filter boundaries. Tags stay image-relevant concept units; synonyms belong in `aliases`/`keywords`/`embedding_text`.

## Output Contracts

Candidate pack (`--emit-candidate-pack`): JSON array of pack objects. Each pack has `pack_id`, `mandatory_intents`, `uncovered_intents`, `presets`, `slots`, `concept_axes`, `motif_budget`, `preset_reference`, `masked_buckets`, `open_slots`, `template_echo_risk`, `role_scene_policy`, `species_family`, `diversity_state`, `coverage`, `conflicts`, `safety_floor`, `negative_en`, and `provenance`. Preset candidates expose exact ids as `preset:<preset_id>`; slot candidates expose exact ids as `slot:<slot>:<entry_id>`. Default caps are preset top 5, core slot top 5, support slot top 3, and 120 total slot candidates. The pack is not a final prompt. Masked/open sections are intentionally absent from the final scene plan until the composing agent invents fresh details.

Composed prompt JSON: `pack_id`, `prompt_en`, `negative_en`, `chosen_candidate_ids`, `composer`, and optional `coverage_assertions`. `coverage_assertions` maps an original mandatory intent text to the English visual phrase used in `prompt_en`, for example `{"드래곤": "dragon horns and a scaled tail"}`.

Compact (`--detail-level compact`, ReactorPrompt-style): one English paragraph, no section labels, ~50-120 words, covering medium/genre/format, subject/appearance/action/prop, location, lighting, camera/composition/lens/focus, texture/quality, and `no text or watermark`.

Detailed (default `--detail-level detailed`): include concept lock near the beginning when provided; subject/state with subject-appropriate detail (no human-only phrasing for food/objects/landscapes); concrete scene depth; camera/composition; lighting behavior; color/mood; texture/finish; user constraints as `Additional requirements: ...` (rendered before `prompt_id` is computed); `--likeness-mode inspired` for named public figures. Normally 120+ words of concrete visual information, no generic padding.

`standard` keeps the original short template style.

## Wrapper Defaults

`generate_photo_prompt.py` defaults to: bundled tags, `--n 1`, `--lang both`, `--detail-level detailed`, `--selection-mode semantic` with a broad default intent, `--surreal-mode off`, `--reference-edit-mode off`, `--trend-layer off`, `--json-output`, `--include-negative`.

Default generation now emits a candidate pack when `--emit-candidate-pack` is supplied. The legacy final-prompt JSON path remains available by omitting that flag, but user-facing prompt work should use candidate pack + agent composition + audit.

Each legacy final-prompt JSON result includes a `provenance` block with `prompt_id`, `negative_id`, `generator_version`, `seed`, `batch_index`, `preset_id`, `selection_mode`, `creativity`, `concept_lock`, `additional_requirements`, `likeness_mode`, and the final forwarded `argv`.

Record an image attempt after using the external image tool:

```bash
python3 .../record_image_run.py --ts "2026-06-03T10:00:00+09:00" --concept "유나 바니걸" \
  --prompt-en "$PROMPT_EN" --prompt-id "$PROMPT_ID" --attempt 1 --status safety_block \
  --failure-reason "safety filter" --tool image_gen --pack-id "$PACK_ID" \
  --chosen-candidate-ids-json '["preset:clean_mirror_selfie_snapshot"]' \
  --composer agent --audit-status pass
```

The recorder recomputes `prompt_id` from `--prompt-en`; if it differs from `--prompt-id`, it exits without writing. On retries, pass the same prompt text and increment `--attempt`; use `--retry-of` with the previous `run_id` when available.
