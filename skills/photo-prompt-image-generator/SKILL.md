---
name: photo-prompt-image-generator
description: Generate image-ready photographic prompts and, when requested, images from this project's JSON-managed presets, concepts, hybrid candidate augmentation, adult fashion-appeal axes, and quality profiles. Use for random, intent-led, preset-based, Korean short-concept, creative or authorial, detail-rich, sensual-editorial, fetish-fashion, commercial audience-outcome, and subculture character-response photo requests.
---

# Photo Prompt Image Generator

Use the project-local generator to produce a compact candidate pack, preserve an agent-authored concept core, selectively enrich it from candidate-sourced routes, compose one final English prompt, audit it, and only then generate an image when the user asked for one.

Canonical skill path: `skills/photo-prompt-image-generator`.

## Read Only What You Need

- Candidate-pack composition, audit, safety, and quality fields: `references/composition-contract.md`
- Candidate-sourced idea routes, selective adoption, and composable adult-appeal axes: `references/hybrid-augmentation-contract.md`
- Viewer-perceived creativity, multi-proposal selection, prompt binding, and authorial grammar: `references/creative-direction-contract.md`
- Viewer needs, affect causes, attachment, reinspection, commercial objectives, and metadata-free review: `references/viewer-experience-contract.md`
- Intent, concept, preset, slot, and anti-overfitting routing: `references/concept-routing.md`
- Native image generation, explicit API use, saving, retries, and ledger records: `references/image-runtime.md`
- Dictionary edits, validation, semantic index, and evaluation gates: `references/maintenance.md`

Do not load every reference for a simple prompt request.

## Core Resources

- `scripts/generate_photo_prompt.py`: preferred wrapper and concept resolver.
- `scripts/prompt_generator.py`: JSON-driven generation engine.
- `scripts/audit_composed_prompt.py`: fail-closed composed-prompt audit.
- `scripts/audit_scene_expression.py`: frozen-baseline and merged-runtime audit for scene counts, functions, operational dominance, and explicit render contracts.
- `assets/photo_prompt_tags.json`: presets, slots, weights, facets, and coherence rules.
- `assets/photo_prompt_research_extension.json`: append-only evidence-led operational and scientific presets, slots, facets, and typed-domain overrides loaded alongside the base dictionary.
- `assets/photo_prompt_subculture_extension.json`: separately loaded, on-demand subculture practice presets and shared craft/community taxonomy; keep specialty signals out of unrelated automatic pools.
- `assets/photo_prompt_worldbuilding_extension.json`: separately loaded, on-demand general world-system presets with atomic scene evidence and scoped routing.
- `assets/photo_prompt_cjk_worldbuilding_extension.json`: separately loaded, source-backed CJK commercial-narrative world systems; keep market terms distinct and lock culture-sensitive scenes to one provenance.
- `assets/photo_prompt_character_moe_extension.json`: separately loaded, on-demand adult character grammar with 24 source-backed routes, eight shared families, typed runtime nodes, compatibility edges, and fail-closed guards.
- `assets/photo_prompt_scene_expression_extension.json`: pilot scene-first data and shared scene-function/provenance vocabulary.
- `assets/photo_prompt_scene_expression_worldbuilding.json` and `assets/photo_prompt_scene_expression_cjk.json`: compact route-specific non-operational scene blueprints; they extend render expression without duplicating research taxonomy slots.
- `assets/photo_prompt_scene_expression_character_moe.json`: three sparse atomic character scenes per route; each selects one primary visual mechanism and at most two compatible support cues.
- `assets/render_scene_expression_baseline_v1.json` and `assets/render_scene_quality_holdout_v1.jsonl`: implementation-before structural baseline and frozen rendered-image acceptance sample.
- `assets/render_scene_quality_visual_review_v1.json`: versioned metadata-free pixel review for the frozen 12-case rendered sample; a plan or prompt audit is not a substitute for this result.
- `assets/semantic_retrieval_holdout_character_moe_v1.jsonl`, `assets/render_character_moe_quality_holdout_v1.jsonl`, and `assets/render_character_moe_quality_visual_review_v1.json`: frozen multilingual retrieval, eight-family render cases, and their metadata-free pixel qualification for the character-mechanism extension.
- `assets/render_viewer_experience_holdout_v1.jsonl` and `assets/render_viewer_experience_visual_review_v1.json`: implementation-before commercial, subculture-attachment, and meaningful-image cases plus their metadata-free local pixel qualification.
- `assets/concept_recipes.json`: Korean concepts, identity cores, scene variants, guides, and gates.
- `assets/photo_prompt_quality_layers.json`: domain quality profiles and photographic decision layers.
- `assets/photo_prompt_semantic_index.json`: semantic retrieval manifest; vector shards live under `assets/photo_prompt_semantic_index_shards/` and are materialized transparently.
- `assets/generalization_cases.jsonl`: inspectable public contract and anti-overfitting cases.
- `assets/generalization_holdout_cases.jsonl` and `assets/generalization_domain_holdout_v2.jsonl`: frozen rule-mode holdouts.
- `assets/semantic_retrieval_holdout_v3.jsonl`: frozen preset-free semantic retrieval baseline.
- `assets/semantic_retrieval_holdout_v4.jsonl`: active preset-free retrieval holdout spanning the research extension.
- `assets/semantic_retrieval_holdout_subculture_v1.jsonl`, `assets/semantic_retrieval_holdout_worldbuilding_v1.jsonl`, and `assets/semantic_retrieval_holdout_cjk_worldbuilding_v1.jsonl`: frozen on-demand specialty-route holdouts; never weaken expectations to fit an index result.
- `assets/research_evidence.jsonl`: abstract source-to-taxonomy evidence ledger; never a raw prompt or image corpus.
- `assets/research_evidence_character_moe/`: hash-ordered character-research shards and manifest; keep this ledger separate instead of enlarging the legacy single file.
- `assets/visual_review_domain_extension_plan.json`: rendered-image review case plan linked to a separate versioned result; the plan itself is never acceptance evidence.

Prefer `.venv/bin/python` when the project virtual environment exists. Rule mode works without an API key. Semantic mode requires the configured Gemini dependency and `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Default Prompt Workflow

1. Generate exactly one candidate pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --hybrid-augmentation --emit-candidate-pack --n 1
```

For a short Korean concept:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "제빵사" --hybrid-augmentation --emit-candidate-pack --n 1
```

2. Compose one JSON object from the pack. Required fields are:

```json
{
  "pack_id": "<exact pack id>",
  "prompt_en": "<agent-composed English prompt>",
  "negative_en": "<exact pack negative or null>",
  "chosen_candidate_ids": ["preset:...", "slot:subject:..."],
  "composer": "agent"
}
```

Add `coverage_assertions` only when useful. Every asserted phrase must occur literally in `prompt_en`, and every key must be an exact `mandatory_intents[].text` value.

When the pack contains `hybrid_augmentation.enabled: true`, `augmentation_brief` is required. Read `references/hybrid-augmentation-contract.md`, consider all three actual-candidate routes, select exactly one or reject all, and record every selected-route detail as accepted, modified, or rejected. Bind only accepted or modified details into `prompt_en` and `chosen_candidate_ids`; never accept candidates merely because the pack exposed them.

For an eligible human candidate pack, `sensual_editorial` defaults to intensity `1` while `fetish_fashion` defaults to `0`, producing `sensual_led` emphasis. Fetish-fashion augmentation is opt-in. Pass `--sensual-editorial-intensity 0` to disable the remaining default.

When the pack contains `creative_direction.enabled: true`, `creative_brief` is also required. Read `references/creative-direction-contract.md`, develop at least four distinct concept moves, critique them, select exactly one, and bind its visual consequences and authorial grammar literally into `prompt_en`.

When the pack contains `viewer_experience.enabled: true`, `viewer_experience` is also required in the composed object. Read `references/viewer-experience-contract.md`, select one primary viewer need and one intended experience, then bind the visible hook and actor/action/target/consequence evidence into `prompt_en`.

3. Audit before returning the prompt or generating an image:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json --composed composed_prompt.json
```

Fix every failure and rerun. Warnings are a separate quality signal; inspect them rather than treating them as contract failure.

4. If the user asked only for a prompt, return the audited `prompt_en`. If the user asked for an image, follow `references/image-runtime.md`.

## Creative Discovery Workflow

Automatically use the creative-direction path when the user explicitly asks for a creative, original, ingenious, inventive, surprising, or authorially distinctive result—including Korean requests using `창의적`, `독창적`, `기발한`, `참신한`, `작가적`, or `작가의 터치`. Do not ask for a second creativity instruction. Set `--creativity` to at least `0.85`:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "도예가" --creativity 0.85 --hybrid-augmentation --emit-candidate-pack --n 1
```

- `0..0.25`: conservative neighborhood and low novelty.
- `0.5`: balanced exploration.
- `0.75..1.0`: exploratory neighborhood and high novelty; candidate packs expose both bounded slot contrasts and a binding `creative_direction` concept-development contract. Prefer this range only when the user explicitly asks for a creative result.
- The lever changes novelty and semantic candidate breadth. It does not relax applicability, conflict, theme, safety, or filter coherence.
- Explicit `--novelty` or `--semantic-profile` values take precedence over the corresponding derived setting.
- Add `--selection-mode rule` for offline, reproducible inspection. Rule mode keeps its deterministic sampler; the creativity value is still carried as an explicit candidate-pack exploration request.
- `creative_exploration` widens eligible slot choices; it is not proof of creativity. `creative_direction` requires an ordinary baseline, at least four different concept moves, exactly one selected premise, a visible consequence chain, a viewer reveal path, and authorial frame/time/omission/material decisions.
- Do not simulate creativity by adding more surreal objects, stylistic adjectives, or unrelated anomalies. Prefer one changed rule whose consequences the viewer can discover.
- For a role with `scene_variants`, change `--seed` to explore another atomic scene while keeping `identity_core` stable. Do not mix slots from separate variants.
- For a direct research-backed preset, `--scene-function <value>` selects a supported scene function without turning that control into visible user intent. It requires `--preset` and fails closed when the route has no compatible scene.

High creative-direction runs include `viewer_experience` automatically. Keep the default workflow when the user did not ask for broader exploration. Do not silently raise creativity for ordinary prompt or image requests.

## Adult Fashion-Appeal Workflow

Eligible human candidate packs use a low-intensity adult fashion default: `sensual_editorial=1`, `fetish_fashion=0`, and `sensual_led`. Fetish-fashion augmentation is opt-in. This is a configured composition policy, not an inference from a face, body, clothing, demographic, market term, or presumed popularity. Increase, reduce, rebalance, or disable it from explicit user intent. Both axes may still be activated together explicitly:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "현대적이고 신화적인 성인 타천사" \
  --hybrid-augmentation \
  --sensual-editorial-intensity 2 \
  --fetish-fashion-intensity 2 \
  --adult-appeal-emphasis balanced \
  --emit-candidate-pack --n 1
```

- Use intensity `0..3` independently for each axis. The defaults are `1` for `sensual_editorial` and `0` for `fetish_fashion`; both zero means off.
- Apply the configured default only when the resolved subject category is human. Block it for explicit no-people and non-human requests.
- Intensity `1` keeps the fetish-fashion inventory to the lower tier; higher intensities widen the eligible material and garment pool.
- Let `sensual_editorial` supply gaze, pose, light, framing, or silhouette decisions.
- Let `fetish_fashion` supply material, garment layering, accessory, or footwear decisions.
- Accept at least one candidate from every active axis; keep the total augmentation budget at two to five details.
- State an explicitly adult original subject and visible self-directed agency in the prompt. Keep styling subordinate to the concept core.
- Audit garment, pose, body framing, and camera together. Fix every hard combination failure before generation; inspect warnings intentionally.

## Viewer Experience Workflow

Use `--viewer-experience` without raising creativity when the user explicitly asks about audience response, emotion, empathy, immersion, attachment, revisiting, sharing, purchase behavior, a commercial communication objective, or a subculture character relationship. Korean triggers include `독자`, `관객`, `감동`, `공감`, `몰입`, `애착`, `다시 보고 싶은`, `기억에 남는`, `광고`, and an explicit relation-centered `귀여움`; interpret meaning, not keyword presence.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "성인 조사원과 비인간 동료의 관계" \
  --viewer-experience --emit-candidate-pack --n 1
```

- Select exactly one `primary_viewer_need`, one scalar `intended_experience`, and one `commercial_objective`; do not stack affects to simulate depth.
- Treat the block as a response hypothesis, not proof of human emotion, purchase, or long-term attachment.
- Bind visible causes: first-glance hook plus actor, action, target, and consequence. Do not bind “the viewer feels” outcome claims.
- `care`, `relatedness`, and `identity` need a non-`none` attachment channel and directed visible relation evidence.
- `comprehend`, `remember`, and `act` need literal product or subject legibility. A product-detail image may put immediate clarity ahead of a second-reading device.
- Noncommercial creative-direction work needs one causal reinspection reward. Keep it tied to the same premise rather than adding an Easter egg.
- Judge generated pixels without prompt metadata at both thumbnail and native size. LLM inspection is local product evidence, not a population study.

## Safety Contract

Safety metadata is deliberately simple:

```json
{
  "mode": "automatic",
  "evaluation_requested": false,
  "status": "pass",
  "requires_user_approval": false,
  "items": []
}
```

Normal generation automatically passes this project-level safety contract. Do not pause for safety-transform approval and do not ask the user to approve recipe guards, negative floors, or render directives.

Run the optional recipe safety evaluation only when the user explicitly asks for a safety review or evaluation:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "<concept>" --emit-candidate-pack --safety-evaluation
```

There is no separate approval flag or policy mode. This project-level automatic pass never overrides system policy or the image tool's own safety enforcement. If the platform or image tool blocks a request, report that block honestly.

## Composition Rules

- Preserve every `mandatory_intent` as visible image content. This list contains required positive user meaning only; advisory role/soft guidance and excluded constraints remain typed in `intent_contract`. A candidate label is not proof of coverage.
- Choose only IDs exposed in the pack whose `applicability.status` is `eligible`; never invent or reconstruct a masked candidate.
- Treat `intent_contract` as typed request meaning and `scene_contract` as a hard boundary. A selected render blueprint contributes four mandatory literal scene atoms—subject, action, location, and prop—outside the ordinary sampler candidate pool.
- Copy all four `selected_render_blueprint` labels into the composed prompt. Do not select an ordinary subject/action/location/prop candidate for the same controlled slots, and never reconstruct a sibling from `available_blueprint_ids`.
- Respect `evidence_budget`: the selected physical prop normally consumes one clue, so add at most one other configured world-evidence slot when `maximum_chosen` is 2.
- When `creative_exploration` is present, keep the sampler-selected subject, mandatory intents, and scene contract. Replace at most the stated number of slots, and use only listed contrast IDs that remain conflict-free together.
- When `hybrid_augmentation` is present, keep the agent-authored concept core, consider all three candidate routes, select one or reject all, and record every selected-route candidate decision. Accepted and modified candidates require literal prompt evidence and provenance; rejected candidates must remain absent.
- When adult-appeal axes are active, preserve their independent intensities and blend emphasis. Require one accepted detail per active axis, explicit adult-original-subject evidence, visible agency, and the cross-check of styling with pose, framing, and camera.
- When `creative_direction` is present, follow `references/creative-direction-contract.md`. Select one proposal only; never blend rejected signatures into the final prompt. The concept move may reinterpret relationships inside the selected scene but may not replace mandatory subjects, atomic scene labels, character grammar, safety, or negative bytes.
- When `viewer_experience` is present, follow `references/viewer-experience-contract.md`. Keep one viewer need and intended experience, make affect causal through visible action, and preserve commercial clarity or typed character evidence. Genre labels, youth morphology, faces, and style adjectives alone are not attachment evidence.
- Preserve `negative_en` byte-for-byte.
- Respect hard conflicts, concept gates, enforced role-scene policy, and species-family locks.
- When `character_grammar.enabled` is true, preserve its primary runtime mechanism and use no more than its two support cues. Treat router IDs, policy IDs, market terms, and audience familiarity as nonvisual guidance; the selected atomic scene is the visible realization.
- Character routes require an explicitly adult original subject. Do not infer adulthood, identity, orientation, or personality from face/body proportions, hair, clothing, disability, ethnicity, or market origin.
- `open_slots` expose only slot and bucket names. Invent a compatible detail; do not infer the hidden source choice.
- Use one or two photographic craft decisions, not every available phrase.
- `artistic_final_touch` is profile-specific surface craft. Use it only when `enabled` is true; equivalent wording is acceptable and need not be a fixed suffix. It never satisfies `creative_direction` authorial grammar by itself.
- Keep named-person text out of mandatory visual intent. `--likeness-mode inspired` means an original fictional adult inspired by styling or atmosphere, not exact likeness.
- A request such as `사람 없는`, `인물 없이`, `no people`, or `without people` is a negative-presence constraint. Keep it in `intent_contract.constraints`, exclude its absence phrase from positive `mandatory_intents`, and never turn it into a positive human axis.
- Keep compact English prompts at roughly 50–120 words. Optional craft or final-touch text must not push them over budget.

See `references/composition-contract.md` for field-level details.

## Selection Defaults

- Route illustration, key visual, cover, card art, vertical webtoon, sticker, SD/chibi merchandise, and campaign-art requests to `$subculture-illustration-image-generator`; do not add camera/lens/photoreal defaults first.
- The wrapper defaults to semantic selection with a broad photographic intent.
- Use `--selection-mode rule` for reproducible offline generation or tests.
- Use `--intent` for free-form semantic requests and `--concept-lock` for literal meaning that must remain dominant.
- Use `--additional-requirement` only for concrete visible constraints not represented by tags.
- Biodiversity monitoring, agriculture-food systems, and circular-material records are on-demand typed packs: name the domain in semantic intent or select their preset directly; they do not enter unrelated automatic concept pools.
- Character-moe grammar is also on demand. Route it only from a specific character mechanism or an exact scoped alias; an ordinary cute portrait, animal photograph, real cultural record, or generic streamer request must remain on its existing route.
- Rule mode gives a uniquely strong explicit request-term match deterministic priority while retaining the other sampler-eligible alternatives in the candidate pack.
- K-pop/K-beauty/idol and fantasy candidates receive an implicit-theme penalty unless the request names that theme.
- Concept recipes may define `identity_core` plus weighted `scene_variants`; keep the identity stable while rotating one atomic scene instead of mixing slots from separate exemplars.

See `references/concept-routing.md` before adding a new preset, concept, or slot.

## Useful Commands

```bash
# Discovery
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-presets --plain
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --show-slots --plain
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --list-tags subject --plain

# Reproducible prompt
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset street_documentary --selection-mode rule --seed 42 --emit-candidate-pack

# Reproducible non-default scene function for a research-backed direct preset
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset natural_process_trace_documentary --scene-function revelation \
  --selection-mode rule --seed 42 --emit-candidate-pack

# Explain concept routing without generation
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "회사원" --explain-concept

# Local validation
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
```

Do not make hidden LLM calls inside deterministic scripts. Do not edit the tag dictionary unless the user asked to change the skill or its data.
