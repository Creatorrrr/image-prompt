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
- Natural-language adult moe, sexual-tone triage, fixed-reference identity control, causal event phases, nekomimi boundaries, and user-judged image review: `references/moe-response-contract.md`
- Intent, concept, preset, slot, and anti-overfitting routing: `references/concept-routing.md`
- Native image generation, explicit API use, saving, retries, and ledger records: `references/image-runtime.md`
- Dictionary edits, validation, semantic index, and evaluation gates: `references/maintenance.md`

Do not load every reference for a simple prompt request.

## Core Resources

- `scripts/generate_photo_prompt.py`: preferred wrapper and concept resolver.
- `scripts/prompt_generator.py`: JSON-driven generation engine.
- `scripts/audit_composed_prompt.py`: fail-closed composed-prompt audit.
- `scripts/audit_image_render_request.py`: verify the exact runtime prompt, negative bytes, audit boundary, and attached reference hashes before generation.
- `scripts/audit_moe_render_review.py`: validate image-grounded hard-gate evidence and block representative promotion until the requesting user accepts the result as genuinely moe.
- `scripts/audit_scene_expression.py`: frozen-baseline and merged-runtime audit for scene counts, functions, operational dominance, and explicit render contracts.
- `assets/photo_prompt_tags.json`: presets, slots, weights, facets, and coherence rules.
- `assets/photo_prompt_research_extension.json`: operational and scientific presets, slots, facets, and typed-domain overrides loaded alongside the base dictionary.
- `assets/photo_prompt_subculture_extension.json`: selection-gated subculture practice presets and shared craft/community taxonomy.
- `assets/photo_prompt_worldbuilding_extension.json`: selection-gated general world-system presets with atomic scene evidence and scoped routing.
- `assets/photo_prompt_cjk_worldbuilding_extension.json`: selection-gated CJK commercial-narrative world systems with distinct market terms and culture-sensitive scene boundaries.
- `assets/photo_prompt_character_moe_extension.json`: selection-gated adult character behavior routes, shared families, typed runtime nodes, compatibility edges, and fail-closed guards.
- `assets/photo_prompt_scene_expression_extension.json`: pilot scene-first data and shared scene-function/provenance vocabulary.
- `assets/photo_prompt_scene_expression_worldbuilding.json` and `assets/photo_prompt_scene_expression_cjk.json`: compact route-specific non-operational scene blueprints; they extend render expression without duplicating research taxonomy slots.
- `assets/photo_prompt_scene_expression_character_moe.json`: at least four sparse atomic character scenes per route; each selects one primary visual mechanism and at most two compatible support cues. The generic natural-moe route may add bounded `natural_moe_default_only` everyday, expression-led, or pose-led scenes while direct preset selection retains its authored base scenes.
- `assets/concept_recipes.json`: Korean concepts, identity cores, scene variants, guides, and gates.
- `assets/photo_prompt_quality_layers.json`: domain quality profiles and photographic decision layers.
- `assets/photo_prompt_semantic_index.json`: semantic retrieval manifest; vector shards live under `assets/photo_prompt_semantic_index_shards/` and are materialized transparently.

Validation fixtures, research evidence, semantic-index maintenance, and promotion gates are maintenance-only resources. Load their locations and procedures from `references/maintenance.md` only when editing or evaluating the dictionary.

Prefer `.venv/bin/python` when the project virtual environment exists. Rule mode works without an API key. Semantic mode requires the configured Gemini dependency and `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Default Prompt Workflow

For an independent multi-arm run, a broad aesthetic request, or a Japanese-subculture-style request, freeze the agent's own concept before generating a candidate pack. Do this independently inside each arm's worktree, before reading any pack or another arm's output:

```json
{
  "contract_version": "authorial-request/v1",
  "provenance": "agent_prepack",
  "subject": "<concrete adult subject and role>",
  "setting": "<concrete photographic setting>",
  "event": "<one visible unfinished character-revealing event>",
  "style_domain": "japanese_subculture_photo",
  "style_family": "<supported family id>",
  "style_evidence": ["<visible cue one>", "<visible cue two>"],
  "variation_key": "<arm-local key>"
}
```

Pass that object with `--authorial-request-json <path-or-inline-json>`. It is valid only for v4 candidate packs. The generator canonicalizes it, records `canonical_sha256` and `agent_prepack` provenance, and makes it govern the public authorial scene. A pack ID, selected blueprint, candidate ID, or other pack-derived field in this input fails closed. Do not inspect a pack first and then write a concept that rationalizes its private route.

For a Japanese-subculture photo contract, use one concrete fashion/community/venue family and at least two visible clothing, grooming, prop, venue, or participation cues. `Japanese subculture` is a style-domain request, not permission to infer Japanese nationality, ethnicity, or facial features from the reference. The attached portrait remains identity and adult-age evidence only.

1. Generate exactly one candidate pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --hybrid-augmentation --emit-candidate-pack --n 1
```

This emits `photo-candidate-pack/v4`. It exposes candidates as unordered inspiration terms in a seed-shuffled, non-preferential order, gives the agent a seed-varying abstract authorial lens, and withholds reusable render-blueprint prose. It does not expose a sampler-selected candidate, scene entry, probability, weight, score, slot-level answer, intent-coverage candidate answer key, singleton routing preset, sampled motif, private preset ID, or expanded generator argv. Sampler-derived scene groups, quality axes, and craft winners are projected as optional unordered pools instead. Use `--candidate-pack-version v3` or `v2` only to replay a legacy consumer or historical contract, and always pass a non-empty `--legacy-replay-reason`; normal composition must use the authorial v4 projection.

`--explain-scene-routing` is an opt-in private diagnostic. It exposes blueprint IDs and cue scores under `private_scene_routing`, marks the result `diagnostic_only`, and must never be used as the composition pack. Ordinary v4 output keeps that routing private.

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
  "chosen_candidate_ids": ["slot:lighting:..."],
  "candidate_interpretations": [
    {
      "candidate_id": "slot:lighting:...",
      "artistic_interpretation": "<why this cue serves the authored premise>",
      "transformation": "<how its context, relation, or material behavior changed>",
      "prompt_evidence": "<new literal phrase bound into prompt_en>"
    }
  ],
  "composer": "agent"
}
```

Add `coverage_assertions` only when useful. Every asserted phrase must occur literally in `prompt_en`, and every key must be an exact `mandatory_intents[].text` value.

When the v4 pack contains `hybrid_augmentation.enabled: true`, `augmentation_brief` is required. Read `references/hybrid-augmentation-contract.md`, consider all three actual-candidate routes, select exactly one or reject all, and record every selected-route detail as `transformed` or `rejected`. Candidate `concept_terms` are unordered inspiration only. For each transformed detail, invent the relationship and prompt prose, record the artistic interpretation and transformation dimensions, and bind the newly authored evidence into `prompt_en` and `chosen_candidate_ids`. Joining or lightly inflecting the exposed terms is not authorship and fails audit. v3/v2 replay packs retain their legacy states.

When `authorial_composition.authored_scene_required` is true, add `authored_scene` with `governing_premise`, `artistic_rationale`, newly written `atoms` for subject/action/location/prop, and at least two distinct `interpretive_choices` containing dimension, decision, and reason. If the pack has `authorial_request`, also set `authored_scene.source_authorial_request_sha256` to its exact `canonical_sha256` and preserve the request's subject, setting, event, style family, and style evidence. That pre-pack request governs the scene; private blueprint abstractions cannot replace it. Without a pre-pack request, use only the abstract scene functions, stakes, genre anchors, evidence types, and authorial lens as constraints. The source blueprint sentence, ID, hash, and sibling inventory are intentionally unavailable; do not try to reconstruct them.

When `japanese_subculture_photo.requested` is true, bind at least `minimum_visible_cues` of its `visible_cues[].prompt_phrase` literally into `prompt_en`. A family label alone fails. Keep the family original, fictional, and unbranded, and do not turn a style-domain label into nationality, ethnicity, or facial morphology.

When `authorial_open_slots` is present, the generator intentionally withheld a singleton subject/action/location/prop candidate that would otherwise anchor every prompt. Add `authored_slots.<slot>` with newly written `prompt_evidence` and an `artistic_rationale`. Bind the evidence literally. If the slot declares a `scene_family`, include that value in `constraint_acknowledgments` and author a compatible location; the family name itself is not prompt text.

Every advisory v4 candidate is optional, and optional scene or augmentation groups may be rejected in full. `chosen_candidate_ids` may be empty only when no hard identity, species-family, role-scene, or safety contract requires an ID. For each chosen candidate not already transformed through `augmentation_brief`, add exactly one `candidate_interpretations` row with `candidate_id`, `artistic_interpretation`, `transformation`, and newly authored literal `prompt_evidence`. The evidence needs at least four content words and at least two words not supplied by that candidate's unordered concepts. Copying, concatenating, or lightly inflecting the candidate terms fails audit even when the resulting phrase is grammatical.

For an eligible human candidate pack, including a plain adult-moe request, `sensual_editorial` normally defaults to intensity `1` while `fetish_fashion` defaults to `0`, producing `sensual_led` emphasis. Only explicit nonsexual moe wording suppresses both configured defaults to `0`; explicit adult sensual intent may strengthen the axis. Sexual appeal is a supporting axis, never a substitute for the pretty-and-cute adult character gate or character-specific event. Fetish-fashion augmentation remains opt-in. Pass `--sensual-editorial-intensity 0` to disable the remaining default on ordinary human paths.

When the pack contains `creative_direction.enabled: true`, `creative_brief` is also required. Read `references/creative-direction-contract.md`, develop at least four distinct concept moves, critique them, select exactly one, and bind its visual consequences and authorial grammar literally into `prompt_en`.

When the pack contains `viewer_experience.enabled: true`, `viewer_experience` is also required in the composed object. Read `references/viewer-experience-contract.md`, select one primary viewer need and one intended experience, then bind the visible hook and actor/action/target/consequence evidence into `prompt_en`.

When the pack contains `moe_response.enabled: true`, `moe_response` is also required. Read `references/moe-response-contract.md`. Preserve the routed adult aesthetic baseline: explicit feminine -> adult bishoujo, explicit masculine -> adult bishonen, explicit androgynous/nonbinary -> beautiful-and-cute adult equivalent, and unspecified -> adult bishoujo. Also preserve the routed `relationship_register`: tsundere uses `peer_liking_under_denial`, explicitly mamang/maternal care uses `nurturant_benevolence`, ordinary requested care uses `directed_care_without_role_inference`, and other mechanisms remain `character_specific_reveal`. A relationship request outranks a compatible species reflex: for example, mamang nekomimi uses `quiet_care_trace` as primary and keeps `nonhuman_reflex_leak` as support. Bind a literal phrase that establishes adulthood, both pretty/beautiful and cute/charming first-read qualities, and at least two concrete face/hair/style details. Separately bind one warm or pleased facial micro-response in `affective_leak_phrase`; guardedness, annoyance, sadness, or embarrassment may frame the event but cannot be the only facial read. For `denial_care_leak`, also bind a distinct `active_denial_phrase` with a visible mouth, chin, shoulder, or helping-hand protest—guardedness, a label, or averted gaze alone does not qualify. Bind `care_action_anchor_phrase` to the recipient's visible hand, wound, or carried object at a named lower screen position. Separately bind `relationship_gaze_anchor_phrase` to one small blurred outer eye plus temple/profile sliver from the same adult recipient at a named upper frame edge. A wholly off-frame eye line is unverifiable and a second full face competes with the primary subject. Then bind `concealed_affection_phrase` as explicit geometry: name a three-quarter head turn toward the side opposite that landmark, keep the nose axis off the lens, let only the irises make a small oblique return to the landmark, soften the lower lids, and start one mouth corner lifting before it is suppressed. Direct frontal eye contact, a centered face, selfie-like viewer gaze, head and irises turning together, generic side-eye, task-only gaze, or maternal benevolence does not establish tsundere liking. For `nurturant_benevolence`, instead preserve a relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention without importing active denial. Bind `background_control_phrase` to a plain/unlettered surface or text-free bokeh unless the user requested readable text. Then preserve the routed primary mechanism and bind the behavioral baseline, unfinished event phase, trigger, target, visible response, immediate consequence, continuity, and focal-plane evidence literally into `prompt_en`. Keep the complete English `prompt_en` within the pack's 50–120-word budget by reusing short substrings across moe, viewer, identity, and augmentation evidence rather than repeating explanations. Give the unfinished event a concrete physical separation from its endpoint; for a nekomimi ear reflex, keep each ear no taller than the visible human ear, show one trigger-side ear turning toward the in-frame cause, and give the other ear a clearly different baseline angle. A generic-looking person fails the entry gate; an attractive or sexual pose without the causal event also fails. When `reference_identity_control.enabled` is true, use the uploaded portrait as the sole identity reference, preserve eye aperture/shape/spacing, face length, lower-face and jaw width, and the other listed facial and adult-age anchors, and bind explicit no-enlarging/no-rounding/no-shortening/no-narrowing language in `reference_identity_phrase`. Change only the allowed expression/pose/outfit/light/setting fields. A rendered identity failure must be preserved as failed evidence and cannot be promoted as the representative candidate, even if it looks prettier or cuter.

3. Audit before returning the prompt or generating an image:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json --composed composed_prompt.json
```

Fix every failure and rerun. Warnings are a separate quality signal; inspect them rather than treating them as contract failure.

4. If the user asked only for a prompt, return the audited `prompt_en`. If the user asked for an image, follow `references/image-runtime.md`.

Before invoking an image tool, freeze the concrete runtime request and audit it separately from composition:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_image_render_request.py \
  --pack candidate_pack.json --composed composed_prompt.json --request render_request.json
```

The exact audited `prompt_en` must occur in `runtime_prompt_en`, `runtime_negative_en` must equal the pack's `negative_en` byte-for-byte, and every attached reference path/hash/role must validate. Do not generate on failure, and never let the longer runtime string inherit the composed prompt's PASS.

After an eligible moe image is saved, record its pixel review and run the separate promotion audit:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_moe_render_review.py \
  --pack candidate_pack.json --review render_review.json --output render_review.audit.json
```

Every `required_hard_gates` entry from the pack must be exactly `pass` with concise image-grounded evidence; `partial`, missing, or failed gates block promotion. A technically qualified image remains pending until `user_judgment.source` is `requesting_user` with a faithful decision summary and the user accepts genuine moe plus baseline improvement when a baseline exists. The auditor validates recorded review evidence and file hashes; it does not inspect pixels, authenticate the speaker, or establish genuine user preference by itself. Populate requesting-user fields only from the actual conversation.

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
- For a direct taxonomy preset, `--scene-function <value>` selects a supported scene function without turning that control into visible user intent. It requires `--preset` and fails closed when the route has no compatible scene.

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

- Use intensity `0..3` independently for each axis. The ordinary eligible-human defaults are `1` for `sensual_editorial` and `0` for `fetish_fashion`; an explicit nonsexual moe route suppresses both to zero. Both zero means off.
- Apply the configured default only when the resolved subject category is human. Block it for explicit no-people and non-human requests.
- Intensity `1` keeps the fetish-fashion inventory to the lower tier; higher intensities widen the eligible material and garment pool.
- Let `sensual_editorial` supply gaze, pose, light, framing, or silhouette decisions.
- Let `fetish_fashion` supply material, garment layering, accessory, or footwear decisions.
- Accept at least one candidate from every active axis; keep the total augmentation budget at two to five details.
- State an explicitly adult original subject and visible self-directed agency in the prompt. Keep styling subordinate to the concept core.
- Audit garment, pose, body framing, and camera together. Fix every hard combination failure before generation; inspect warnings intentionally.

## Viewer Experience Workflow

Use `--viewer-experience` without raising creativity when the user explicitly asks about audience response, emotion, empathy, immersion, attachment, revisiting, sharing, purchase behavior, a commercial communication objective, or a subculture character relationship. Korean triggers include `독자`, `관객`, `감동`, `공감`, `몰입`, `애착`, `다시 보고 싶은`, `기억에 남는`, `광고`, and an explicit relation-centered `귀여움`; interpret meaning, not keyword presence. A routed explicit moe request attaches this viewer contract automatically because moe is a requested response hypothesis.

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
- Treat `intent_contract` as typed request meaning. In v4, `optional_inspiration_group` scene candidates are rejectable and reveal no sampler winner; a private selected blueprint contributes only abstract functions, stakes, genre anchors, evidence types, and provenance, while the agent authors the concrete subject, action, location, and prop. v3/v2 retain fail-closed selected atomic entries and literal atoms only for replay.
- When `authorial_request` is present, treat its canonical hash and `agent_prepack` provenance as the governing concept source. Preserve subject, setting, event, style family, and at least two style-evidence phrases in the authored scene and final prompt; never backfill it from pack candidates.
- When `japanese_subculture_photo` is present, preserve its typed family and literal visible-cue floor. Do not infer nationality, ethnicity, or facial traits, and do not reintroduce candidates listed by its unrequested strong-theme guard.
- When v4 requests `authored_scene`, write all four atoms yourself and bind them literally. Make at least two explicit interpretive choices; do not reconstruct a source scene from private data.
- When v4 exposes `authorial_open_slots`, fill each opening through artistic judgment rather than recreating the removed singleton. Preserve listed hard constraints and bind every authored phrase literally.
- Treat every v4 candidate, photographic category, craft dimension, visual proposition, and motif family as rejectable inspiration. For every ordinary chosen ID, record one `candidate_interpretations` decision and create prompt evidence that materially transforms the source concepts. Do not infer a preferred choice from array order, routing metadata, or profile data; v4 intentionally withholds those answers.
- Respect `evidence_budget`: the selected physical prop normally consumes one clue, so add at most one other configured world-evidence slot when `maximum_chosen` is 2.
- When `creative_exploration` is present, keep the sampler-selected subject, mandatory intents, and scene contract. Replace at most the stated number of slots, and use only listed contrast IDs that remain conflict-free together.
- When v4 `hybrid_augmentation` is present, keep the agent-authored concept core, consider all three candidate routes, select one or reject all, and record every selected-route candidate decision. Only artistically transformed candidates enter the prompt; they require newly authored relational evidence and provenance. Rejected candidates remain absent. v3/v2 follow their embedded legacy adoption contract.
- When adult-appeal axes are active, preserve their independent intensities and blend emphasis. In v4, author a scene-specific interpretation and literal evidence per active axis; adopting an inventory candidate is optional. Always require explicit adult-original-subject evidence, visible agency, and the cross-check of styling with pose, framing, and camera.
- When `creative_direction` is present, follow `references/creative-direction-contract.md`. Select one proposal only; never blend rejected signatures into the final prompt. The concept move may reinterpret relationships inside the selected scene but may not replace mandatory subjects, the authorial scene boundary (or legacy atomic labels), character grammar, safety, or negative bytes.
- When `viewer_experience` is present, follow `references/viewer-experience-contract.md`. Keep one viewer need and intended experience, make affect causal through visible action, and preserve commercial clarity or typed character evidence. Genre labels, youth morphology, faces, and style adjectives alone are not attachment evidence.
- When `moe_response` is present, follow `references/moe-response-contract.md`. First preserve the routed adult bishoujo/bishonen/androgynous aesthetic baseline and make the character read as both pretty and cute through concrete facial, eye, mouth, hair, or cohesive-style evidence. Preserve the routed relationship register rather than letting all warmth collapse into generic care. Add one specific warm affective leak and keep negative-affect cues to at most two. For `denial_care_leak`, keep the care-action target low in-frame, place one blurred outer-eye-plus-temple/profile sliver from the same adult recipient at a named upper frame edge, turn the primary head and nose three-quarter toward the opposite side, and return only the irises to that visible landmark while softened lower lids and a starting mouth-corner lift are suppressed. An imagined off-frame eye line, second full face, direct frontal eye contact, or head and irises turning together cannot stand in for concealed liking. For explicit mamang/maternal care, bind a concrete benevolent expression—relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention—without adding tsundere denial; ordinary friendly care must not silently become mamang. Use a plain unlettered background unless text is requested. Then keep one primary mechanism, show an unfinished event phase with a concrete gap/contact/offset state, and place the face or gaze, responding hand/posture, and trigger or target in one focal plane. A nekomimi ear reflex must remain at human-ear scale, be asymmetric, and aim toward the visible trigger. The immediate consequence must be visible without completing the whole action. Neither the aesthetic layer nor the causal layer can substitute for the other. For identity-controlled renders, reject promotion if eye aperture/shape/spacing, face length, lower-face/jaw width, or adult age visibly drift.
- Preserve `negative_en` byte-for-byte.
- Respect hard conflicts, concept gates, enforced role-scene policy, and species-family locks. A manual gate may pass prompt preflight only with literal `manual_gate_evidence` and `review_stage: pixel_review_required`; inspect the generated pixels before treating it as satisfied.
- When `character_grammar.enabled` is true, preserve the one node marked `primary` and use no more than its two support nodes. v4 exposes selected visual mechanisms, evidence types, generic composition constraints, and an abstract authorial scene contract; the agent invents the visible realization. Router anchors and policy/guard records remain private, while market/audience research classifications are not stored in runtime scene data.
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
- Character-moe grammar is also on demand. Route natural KO/JA/EN requests that explicitly ask for moe, gap moe, or a named character-specific mechanism when adult character context is present. Keep ordinary cute portraits, discussions of the word, negated requests, animal photographs, real cultural records, and generic streamer requests on their existing routes.
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

# Reproducible non-default scene function for a direct taxonomy preset
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --preset natural_process_trace_documentary --scene-function revelation \
  --selection-mode rule --seed 42 --emit-candidate-pack

# Explain concept routing without generation
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept "회사원" --explain-concept

# Private selector diagnosis only; never compose from this diagnostic pack
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --concept-lock "adult woman watering a houseplant" --selection-mode rule --seed 42 \
  --emit-candidate-pack --explain-scene-routing

# Local validation
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --contradiction-check
```

Do not make hidden LLM calls inside deterministic scripts. Do not edit the tag dictionary unless the user asked to change the skill or its data.
