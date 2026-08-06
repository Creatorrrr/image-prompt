---
name: photo-prompt-image-generator
description: Generate image-ready photographic prompts and, when requested, images from this project's JSON-managed presets, concepts, and quality profiles. Use for random, intent-led, preset-based, or Korean short-concept photo requests.
---

# Photo Prompt Image Generator

Use the project-local generator to produce a compact candidate pack, compose one final English prompt as the agent, audit it, and only then generate an image when the user asked for one.

Canonical skill path: `skills/photo-prompt-image-generator`.

## Read Only What You Need

- Candidate-pack composition, audit, safety, and quality fields: `references/composition-contract.md`
- Intent, concept, preset, slot, and anti-overfitting routing: `references/concept-routing.md`
- Native image generation, explicit API use, saving, retries, and ledger records: `references/image-runtime.md`
- Dictionary edits, validation, semantic index, and evaluation gates: `references/maintenance.md`

Do not load every reference for a simple prompt request.

## Core Resources

- `scripts/generate_photo_prompt.py`: preferred wrapper and concept resolver.
- `scripts/prompt_generator.py`: JSON-driven generation engine.
- `scripts/audit_composed_prompt.py`: fail-closed composed-prompt audit.
- `assets/photo_prompt_tags.json`: presets, slots, weights, facets, and coherence rules.
- `assets/photo_prompt_research_extension.json`: append-only evidence-led operational and scientific presets, slots, facets, and typed-domain overrides loaded alongside the base dictionary.
- `assets/photo_prompt_subculture_extension.json`: separately loaded, on-demand subculture practice presets and shared craft/community taxonomy; keep specialty signals out of unrelated automatic pools.
- `assets/concept_recipes.json`: Korean concepts, identity cores, scene variants, guides, and gates.
- `assets/photo_prompt_quality_layers.json`: domain quality profiles and photographic decision layers.
- `assets/photo_prompt_semantic_index.json`: semantic retrieval manifest; vector shards live under `assets/photo_prompt_semantic_index_shards/` and are materialized transparently.
- `assets/generalization_cases.jsonl`: inspectable public contract and anti-overfitting cases.
- `assets/generalization_holdout_cases.jsonl` and `assets/generalization_domain_holdout_v2.jsonl`: frozen rule-mode holdouts.
- `assets/semantic_retrieval_holdout_v3.jsonl`: frozen preset-free semantic retrieval baseline.
- `assets/semantic_retrieval_holdout_v4.jsonl`: active preset-free retrieval holdout spanning the research extension.
- `assets/research_evidence.jsonl`: abstract source-to-taxonomy evidence ledger; never a raw prompt or image corpus.
- `assets/visual_review_domain_extension_plan.json`: rendered-image review case plan linked to a separate versioned result; the plan itself is never acceptance evidence.

Prefer `.venv/bin/python` when the project virtual environment exists. Rule mode works without an API key. Semantic mode requires the configured Gemini dependency and `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Default Prompt Workflow

1. Generate exactly one candidate pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --emit-candidate-pack --n 1
```

For a short Korean concept:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "제빵사" --emit-candidate-pack --n 1
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

3. Audit before returning the prompt or generating an image:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json --composed composed_prompt.json
```

Fix every failure and rerun. Warnings are a separate quality signal; inspect them rather than treating them as contract failure.

4. If the user asked only for a prompt, return the audited `prompt_en`. If the user asked for an image, follow `references/image-runtime.md`.

## Creative Discovery Workflow

Use the existing creativity lever when the user wants broader exploration rather than a single conservative interpretation:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "도예가" --creativity 0.85 --emit-candidate-pack --n 1
```

- `0..0.25`: conservative neighborhood and low novelty.
- `0.5`: balanced exploration.
- `0.75..1.0`: exploratory neighborhood and high novelty; candidate packs also mark bounded, relevance-preserving contrast candidates from the already exposed eligible pool. Prefer this range only when the user explicitly asks for creative alternatives.
- The lever changes novelty and semantic candidate breadth. It does not relax applicability, conflict, theme, safety, or filter coherence.
- Explicit `--novelty` or `--semantic-profile` values take precedence over the corresponding derived setting.
- Add `--selection-mode rule` for offline, reproducible inspection. Rule mode keeps its deterministic sampler; the creativity value is still carried as an explicit candidate-pack exploration request.
- For a role with `scene_variants`, change `--seed` to explore another atomic scene while keeping `identity_core` stable. Do not mix slots from separate variants.

Keep the default workflow when the user did not ask for broader exploration. Do not silently raise creativity for ordinary prompt or image requests.

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

- Preserve every `mandatory_intent` as visible image content. A candidate label is not proof of coverage.
- Choose only IDs exposed in the pack whose `applicability.status` is `eligible`; never invent or reconstruct a masked candidate.
- Treat `intent_contract` as typed request meaning and `scene_contract` as a hard boundary. An `atomic_scene` group may use only IDs allowed by that one selected variant.
- When `creative_exploration` is present, keep the sampler-selected subject, mandatory intents, and scene contract. Replace at most the stated number of slots, and use only listed contrast IDs that remain conflict-free together.
- Preserve `negative_en` byte-for-byte.
- Respect hard conflicts, concept gates, enforced role-scene policy, and species-family locks.
- `open_slots` expose only slot and bucket names. Invent a compatible detail; do not infer the hidden source choice.
- Use one or two photographic craft decisions, not every available phrase.
- `artistic_final_touch` is profile-specific. Use it only when `enabled` is true; equivalent wording is acceptable and need not be a fixed suffix.
- Keep named-person text out of mandatory visual intent. `--likeness-mode inspired` means an original fictional adult inspired by styling or atmosphere, not exact likeness.
- A request such as `사람 없는`, `인물 없이`, `no people`, or `without people` is a negative-presence constraint; never turn it into a positive human axis.
- Keep compact English prompts at roughly 50–120 words. Optional craft or final-touch text must not push them over budget.

See `references/composition-contract.md` for field-level details.

## Selection Defaults

- The wrapper defaults to semantic selection with a broad photographic intent.
- Use `--selection-mode rule` for reproducible offline generation or tests.
- Use `--intent` for free-form semantic requests and `--concept-lock` for literal meaning that must remain dominant.
- Use `--additional-requirement` only for concrete visible constraints not represented by tags.
- Biodiversity monitoring, agriculture-food systems, and circular-material records are on-demand typed packs: name the domain in semantic intent or select their preset directly; they do not enter unrelated automatic concept pools.
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

# Explain concept routing without generation
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "회사원" --explain-concept

# Local validation
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
```

Do not make hidden LLM calls inside deterministic scripts. Do not edit the tag dictionary unless the user asked to change the skill or its data.
