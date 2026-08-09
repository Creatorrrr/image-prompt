---
name: subculture-illustration-image-generator
description: Generate and audit original, viewer-readable subculture illustration prompts and images for single illustrations, light-novel or manga covers, anime or game key art, collectible-card splash art, vertical-scroll webtoon sequences, character sheets, merchandise adaptations, and campaign art boards. Use when the requested output is illustration, artwork, key visual, cover art, card art, webtoon, sticker, SD/chibi merchandise, or authorially directed non-photographic subculture imagery.
---

# Subculture Illustration Image Generator

Turn a natural-language idea into a compact typed candidate pack, compose one final English illustration prompt as the agent, audit literal visual evidence and format behavior, and generate an image only when requested.

Canonical skill path: `skills/subculture-illustration-image-generator`.

## Read Only What You Need

- Request, topic, format, creativity, and photo/illustration routing: `references/concept-routing.md`
- Candidate-pack and composed-prompt shape: `references/composition-contract.md`
- Originality and repeatable authorial decisions: `references/creative-direction-contract.md`
- Viewer need, focal discovery, causal affect, and reinspection: `references/viewer-experience-contract.md`
- Cover, key-art, card, scroll, and adaptation behavior: `references/format-contracts.md`
- Image generation, artifact saving, and pixel review: `references/image-runtime.md`
- Research, graph, format, and test maintenance: `references/maintenance.md`

Do not load all references for a simple prompt request.

## Core Resources

- `scripts/generate_illustration_prompt.py`: deterministic local candidate-pack wrapper.
- `scripts/illustration_runtime.py`: typed research graph, route, format, and sparse-bundle runtime.
- `scripts/audit_composed_prompt.py`: fail-closed final-prompt audit.
- `scripts/validate_illustration_assets.py`: research, graph, format, and holdout validator.
- `assets/illustration_mechanism_graph_v1.json`: visual/router/guard nodes and compatible bundles.
- `assets/illustration_format_profiles_v1.json`: six format families and typed variants.
- `assets/illustration_topic_crosswalk_v1.json`: 24 topic routes and local aliases.
- `assets/research_evidence_illustration/`: source-traceable research shards; do not copy source prose into prompts.
- `assets/prompt_qualification_v2/`: current 24-case prompt qualification with typed primary/fallback second-look plans; regression evidence, not reusable prompt templates.
- `assets/prompt_qualification_v1/`: immutable historical v1 evidence. Validate it only through the explicit legacy contract; never rewrite or relabel it as v2.
- `assets/render_case01_v2_preflight/`: generation-free successor for the one exhausted v1 render failure. It freezes the exact v2 pack, prompt, audit, primary/fallback roles, and approval boundary; it is not pixel PASS evidence.
- `assets/render_case01_v2_visual_review.json`: versioned outcome of that successor. Both declared roles are preserved as failures, so it keeps the aggregate product qualification at five of six rather than promoting a prompt-audit PASS.
- `assets/render_case01_v3_preflight/`: authorized structural successor that preserves the v1/v2 failures while replacing their fragile line- and substrate-aligned cues with an isolated moving bell primary and a pattern-free stone-state fallback.
- `assets/render_case01_v3_visual_review.json`: versioned one-attempt pixel PASS. The primary object relation survives native and 320px review, the fallback is correctly not attempted, and the preserved aggregate is six of six.
- `assets/render_illustration_quality_visual_review_v1.json`: versioned native/thumbnail/crop/sequence qualification. Its current `partial` outcome preserves one exhausted failure and must not be described as six-case PASS.

## Workflow

1. Decide that the requested output is illustration rather than photography. Route photographic output to `$photo-prompt-image-generator`.
2. Run the wrapper with the original request, explicit format when known, and a stable seed when reproducibility matters.
3. Inspect the compact pack. It exposes exactly one primary visual atom, at most two compatible support atoms, a format contract, authorial and viewer requirements, guards, and an exact negative prompt.
4. Compose one English prompt as `composer: agent`. Preserve the user's visible subject and event; bind only observable evidence.
5. Compose the v2 object with a `second_look_plan`, then run the composed-prompt audit. Fix the prompt or composition object until both structural and literal gates pass.
6. Give the second look a named primary carrier, a different protected locus and consequence for a safe fallback carrier, and the exact inspection scales where it must remain legible. Declare compound anatomy, subscale-symbol, and overlapping multi-limb projection risks honestly. A risky primary is allowed only with a different, risk-free fallback.
7. If an image was requested, generate exactly one initial image against the primary plan, preserve it, and inspect the declared scales plus the format-required views. Use at most one cause-specific repair when a required relation fails; the repair must switch to the declared fallback instead of asking the failed fragile carrier to become more emphatic.

Candidate-pack example:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/generate_illustration_prompt.py \
  --concept "기억을 실로 봉합하는 성인 야간 수선사의 작가적 일러스트" \
  --format single_illustration \
  --seed 910001 \
  --emit-candidate-pack \
  --output-file /tmp/illustration-pack.json
```

Audit example:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/audit_composed_prompt.py \
  --pack /tmp/illustration-pack.json \
  --composed /tmp/illustration-composed.json
```

## Creative and Viewer Defaults

- Use creativity `0.85` by default, including when the user gives only an ordinary illustration brief. Do not require the user to request creativity or authorial touch separately.
- Every default pack requires concrete focal, omission, edge/mark, and repeated material or motif decisions plus four distinct proposals, one selected changed rule, a causal first-to-second-look reveal, and two distinct visible consequences bound to the primary and fallback carriers.
- Lower creativity below `0.75` only when the user explicitly asks for a restrained, literal, or utilitarian treatment. Explicit `창의적`, `독창적`, `기발한`, `작가적`, or equivalent intent always keeps high creative development enabled.
- Treat intended viewer emotion, attachment, memory, or commercial action as a hypothesis. Prompt evidence must be a visible actor, directed action, target, consequence, and focal discovery—not a response claim.

## Non-Negotiable Boundaries

- Never use a living artist, studio, franchise, or protected character name as a style or visual candidate. Translate only general mechanisms into an original design system.
- Never claim that one color, geometric shape, facial morphology, or CJK convention universally determines emotion, personality, nationality, gender, or audience response.
- Keep one primary visual mechanism and at most two support cues. More symbols, effects, detail, or anomalies are not a repair for weak meaning.
- Do not replace cover, crop, card, vertical-scroll, or adaptation behavior with an aspect-ratio suffix.
- Do not infer age from face, body, clothing, hair, or makeup. Require an explicit adult declaration when sexualization, romance, sensual styling, or body-focused presentation is requested; never sexualize youth.
- Default safety metadata passes automatically. Perform a separate safety evaluation only when the user explicitly requests it; platform safety still applies.
- An audit pass proves prompt binding, not rendered salience, originality across history, audience emotion, virality, or sales. Inspect actual pixels for image claims.
