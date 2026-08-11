---
name: subculture-illustration-image-generator
description: Generate and audit original, viewer-readable subculture illustration prompts and images for single illustrations, light-novel or manga covers, anime or game key art, collectible-card splash art, vertical-scroll webtoon sequences, character sheets, merchandise adaptations, and campaign art boards. Use when the requested output is illustration, artwork, key visual, cover art, card art, webtoon, sticker, SD/chibi merchandise, or authorially directed non-photographic subculture imagery.
---

# Subculture Illustration Image Generator

Turn a natural-language idea into a compact typed candidate pack, compose one final English illustration prompt as the agent, audit literal visual evidence and format behavior, and generate an image only when requested.

Canonical skill path: `skills/subculture-illustration-image-generator`.

## Read Only What You Need

- Request, topic, format, creativity, and photo/illustration routing: `references/concept-routing.md`
- Literal-bound identity, fixed/closed/open slots, and the universal one-event layer: `references/universal-scene-contract.md`
- Candidate-pack and composed-prompt shape: `references/composition-contract.md`
- Originality and repeatable authorial decisions: `references/creative-direction-contract.md`
- Viewer need, focal discovery, causal affect, and reinspection: `references/viewer-experience-contract.md`
- Cover, key-art, card, scroll, and adaptation behavior: `references/format-contracts.md`
- Image generation, artifact saving, and pixel review: `references/image-runtime.md`
- Research, graph, format, and test maintenance: `references/maintenance.md`

Do not load all references for a simple prompt request.

## Core Resources

- `scripts/generate_illustration_prompt.py`: deterministic local candidate-pack wrapper.
- `scripts/generate_moe_element_plan.py`: legacy v1 explicit supplement replay; do not use it as the rich product path.
- `scripts/compile_moe_grammar_v2.py`: deterministic compiler from five claim-level dossier shards and the 58-case intent corpus.
- `scripts/generate_moe_candidate_pack.py`: explicit-only v4 wrapper, preference-aware selector, shared-event composer, and replay audit entrypoint.
- `scripts/moe_element_runtime.py`: v1 replay plus v2 dossier/grammar loading, sparse selection, v4 composition, and fail-closed audit.
- `scripts/illustration_runtime.py`: typed research graph, route, format, and sparse-bundle runtime.
- `scripts/universal_scene_runtime.py`: v3 literal-contract validation and topic-independent one-event selection. It is not a natural-language parser.
- `scripts/audit_composed_prompt.py`: fail-closed final-prompt audit.
- `scripts/validate_illustration_assets.py`: research, graph, format, and holdout validator.
- `assets/illustration_mechanism_graph_v1.json`: visual/router/guard nodes and compatible bundles.
- `assets/illustration_format_profiles_v1.json`: six format families and typed variants.
- `assets/illustration_topic_crosswalk_v1.json`: 24 topic routes and local aliases.
- `assets/illustration_universal_scene_candidates_v1.json`: route-independent expression, pose, action, relation, prop, and environment candidates.
- `assets/illustration_universal_compatibility_graph_v1.json`: fixed/closed/open, resource, distance, bridge, and salience policy for the v3 universal layer.
- `assets/illustration_universal_semantic_bindings_v1.json`: reviewed literal, polarity, embodiment, prop, context, and mandatory visual-realization bindings. It is policy data, not a prompt lexicon.
- `assets/image_generation_retry_policy_v1.json`: typed initial-call plus three unchanged-retry contract for every generation phase.
- `assets/illustration_moe_elements_v1.json`: immutable 29-ID/alias baseline used by v1 replay and explicit activation.
- `assets/research_evidence_moe_elements/dossiers_v2/`, `intent_corpus_v2.json`, `illustration_moe_grammar_v2.json`, and `illustration_moe_compatibility_v2.json`: 29 claim-level dossiers, 233 executable variants, paired neutral/preference expectations, and sparse frame/camera/resource policy. They enrich explicitly requested elements; they are not automatic tags or a replacement scene selector.
- `assets/research_evidence_illustration/`: source-traceable research shards; do not copy source prose into prompts.
- `assets/research_evidence_universal_scene/`: independently audited 20-topic evidence for the universal layer; matrices are synthesis, not independent sources.
- `assets/universal_scene_prompt_holdout_v1.jsonl` and `assets/universal_scene_contract_holdout_v1.jsonl`: immutable historical request/scene-contract sources; regression evidence, never templates for deriving a new request.
- `assets/universal_scene_contract_holdout_v2.jsonl`, `assets/universal_scene_current_holdout_v2.jsonl`, and their manifest/crosswalk: reviewed post-contract current oracle with explicit v1 lineage and compiled runtime obligations. It is prompt-only source evidence, not runtime or pixel evidence.
- `assets/prompt_qualification_v3/`: versioned universal-scene prompt qualification when produced; regression evidence and never a scene-contract or prompt template. Its presence alone is not a generalization or pixel-quality claim.
- `assets/prompt_qualification_v2/`: immutable historical 24-case qualification with typed primary/fallback second-look plans. Validate it only through explicit v2 replay; never relabel it as v3.
- `assets/prompt_qualification_v1/`: immutable historical v1 evidence. Validate it only through explicit v1 replay; never rewrite or relabel it as newer evidence.
- `assets/render_case01_v2_preflight/`: generation-free successor for the one exhausted v1 render failure. It freezes the exact v2 pack, prompt, audit, primary/fallback roles, and approval boundary; it is not pixel PASS evidence.
- `assets/render_case01_v2_visual_review.json`: versioned outcome of that successor. Both declared roles are preserved as failures, so it keeps the aggregate product qualification at five of six rather than promoting a prompt-audit PASS.
- `assets/render_case01_v3_preflight/`: authorized structural successor that preserves the v1/v2 failures while replacing their fragile line- and substrate-aligned cues with an isolated moving bell primary and a pattern-free stone-state fallback.
- `assets/render_case01_v3_visual_review.json`: versioned one-attempt pixel PASS. The primary object relation survives native and 320px review, the fallback is correctly not attempted, and the preserved aggregate is six of six.
- `assets/render_illustration_quality_visual_review_v1.json`: versioned native/thumbnail/crop/sequence qualification. Its current `partial` outcome preserves one exhausted failure and must not be described as six-case PASS.

## Workflow

1. Decide that the requested output is illustration rather than photography. Route photographic output to `$photo-prompt-image-generator`.
2. Before calling the wrapper, automatically derive one `subculture-illustration-scene-contract/v2` from the original request. The user does not need to request or write it. Bind explicit positive facts as `fixed`, bind only literal negative constraints as `closed`, and leave every ambiguity `open` or `unknown`. Partition each fixed slot value into its own phrase binding and typed polarity anchors; bind all eight participant roles to declared identity entities without inventing an owner. Choose `catalog_exact` only for a full exact catalog capability projection and otherwise use a validated declared subset. Do not infer emotion, personality, relationship, intent, culture, age, gender, diagnosis, ownership, or body capability. See `references/universal-scene-contract.md`.
3. Run the wrapper with the original request, the derived scene-contract JSON, explicit format when known, and a stable seed when reproducibility matters. The default is v3. Use explicit `--contract-version v1` or `v2` only to replay immutable historical evidence; those paths reject a scene contract and never load universal assets.
3a. When the user explicitly requests one of the 29 researched moe elements, first build the ordinary v1-v3 pack, then pass that unchanged pack plus one to three exact IDs or complete reviewed aliases to `generate_moe_candidate_pack.py`. Use the original request as preference text. The selector interprets research-backed subtype, viewpoint, intensity, material, pose, camera, and format cues only inside those explicitly selected elements; it never scans prose to activate a sibling element. The v4 wrapper must expose exactly one governing moe primary and at most two total support nodes, preserve the base safety and negative prompt byte-for-byte, and recompose all selected nodes into the base scene's single event. Do not use the legacy v1 supplement's append block for new work. Run `audit_moe_candidate_pack` after composition.
4. Inspect the compact pack. The existing authorial layer still exposes exactly one primary visual atom and at most two compatible supports. The additive `universal_scene` embeds the full canonical scene contract, including all participant bindings, plus exact identity, slot, context, and fixed-role projections, exactly one connected event, at most one optional remote premise, causal bridges, owner-resolved resource claims, authenticated `composition_carriers`, and atom-owned future pixel obligations. Literal visual-realization groups matched by fixed semantics are reserved before ordinary catalog proposals and must preserve their profile, value binding, participant owner, quantifier, and candidate-owned evidence. V3 also preserves `request_contract.prior_exposure_ids` as an exact unique ordered list; use an empty list unless the workflow was explicitly given local prior-exposure IDs.
5. Compose one English prompt as `composer: agent`. Preserve the user's visible subject and event; bind only observable evidence. Write the v3 object with the existing v2 fields, `second_look_plan`, and additive `universal_scene_evidence`, including exact literal coverage for every value in every fixed slot. Each linked evidence phrase must express at least one alternative from every authenticated lexeme group for its fact, slot, role, atom, bridge, or resource. A forbidden identity fact needs an explicit negator scoped to its anchors in the same clause.
6. Run the composed-prompt audit. Fix the prompt or composition object until structural and literal gates pass. This audit validates planning evidence, not rendered pixels.
7. Give the second look a named primary carrier, a different protected locus and consequence for a safe fallback carrier, and the exact inspection scales where it must remain legible. Declare compound anatomy, subscale-symbol, and overlapping multi-limb projection risks honestly. A risky primary is allowed only with a different, risk-free fallback.
8. If an image was requested, make one primary generation call. When no concrete image is returned because of an error, timeout, empty or inaccessible result, or any refusal including safety or policy refusal, retry the same phase up to three additional times with prompt, negative prompt, pack, seed, and generation parameters unchanged. Stop on the first concrete image or after four total calls.
9. Preserve and inspect the first concrete image at the universal and second-look declared scales plus the format-required views. Use at most one cause-specific repair when a required relation fails; the repair must switch to the declared fallback instead of asking the failed fragile carrier to become more emphatic. Apply the same unchanged retry budget to a fallback generation call that returns no image.

Candidate-pack example:

```bash
.venv/bin/python skills/subculture-illustration-image-generator/scripts/generate_illustration_prompt.py \
  --concept "기억을 실로 봉합하는 성인 야간 수선사의 작가적 일러스트" \
  --scene-contract /tmp/illustration-scene-contract.json \
  --format single_illustration \
  --creativity 0.85 \
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

- Use balanced creativity `0.5` by default when the user gives an ordinary illustration brief.
- At `0.5`, the universal layer targets the middle distance band. It keeps the same hard gates and fixed candidate-count budgets as every other creativity level.
- Every default pack still requires concrete focal, omission, edge/mark, and repeated material or motif decisions, a causal first-to-second-look reveal, and two distinct visible consequences bound to the primary and fallback carriers. At `0.5`, it does not require four alternative proposals or one selected changed rule.
- Keep the stored creativity value at the ordinary default `0.5` unless the user explicitly supplies a numeric creativity/distance preference. Creative, original, ingenious, surprising, or authorially distinctive wording—including `창의적`, `독창적`, `기발한`, `참신한`, `작가적`, and `작가의 터치`—activates the high-development authorial contract without silently rewriting that number. The authorial contract may select a compatible novelty-2 moe candidate or far-development proposal, but it does not force remoteness, weaken a gate, or increase the candidate budget.
- Treat intended viewer emotion, attachment, memory, or commercial action as a hypothesis. Prompt evidence must be a visible actor, directed action, target, consequence, and focal discovery—not a response claim.

## Non-Negotiable Boundaries

- Never use a living artist, studio, franchise, or protected character name as a style or visual candidate. Translate only general mechanisms into an original design system.
- Never claim that one color, geometric shape, facial morphology, or CJK convention universally determines emotion, personality, nationality, gender, or audience response.
- Keep one primary visual mechanism and at most two support cues. More symbols, effects, detail, or anomalies are not a repair for weak meaning.
- Build exactly one connected event spine. Every selected expression, pose, action, relation, prop, environment cue, and remote premise must serve that event; allow at most one optional remote premise and never a second independent vignette.
- Require a causal bridge and literal prompt evidence for every selected universal atom. Middle and far selections have stronger typed bridge obligations, and every declared contact, state change, consequence, or bridge remains a future pixel-review obligation until an image is inspected.
- Use `composition_carriers` only as a semantic preflight against empty or generic evidence prose. Their authenticated lexeme matches prove that the intended scene meaning is literally stated, not that the generator rendered the fact, relation, polarity, or consequence in pixels.
- Treat stored hashes and `pack_id` as content integrity, never policy authority. The audit must recompute the request-text and canonical scene-contract hashes, validate embedded participant bindings, and require every identity/slot/context/fixed-role projection to equal the embedded contract. It reloads the local universal assets named by the exact pack hashes and canonically replays selection from the embedded contract, ordered prior exposures, request/topic/format/creativity/seed, and those assets. It exact-compares the replayed `universal_scene`, including literal-realization profiles, owner-joined resource claims, and candidate-owned pixel obligations, before re-evaluating guards, resource capacities, weapon boundaries, and fixed/closed-slot policy. Recomputing stored hashes and `pack_id` after a partial contract mutation, atom removal, or atom substitution cannot make an invalid scene valid.
- Do not implement or simulate scene-contract derivation with request-specific regexes or keyword branches. The skill agent performs a conservative semantic preflight; the deterministic runtime only validates and consumes its literal-bound JSON.
- Do not replace cover, crop, card, vertical-scroll, or adaptation behavior with an aspect-ratio suffix.
- Do not infer age from face, body, clothing, hair, or makeup. Require an explicit adult declaration when sexualization, romance, sensual styling, or body-focused presentation is requested; never sexualize youth.
- Default safety metadata passes automatically. Perform a separate safety evaluation only when the user explicitly requests it; platform safety still applies.
- Retrying a safety or policy refusal never authorizes prompt rewriting, euphemistic substitution, model downgrade, or policy evasion. A higher-priority platform instruction to stop overrides the remaining retry budget.
- An audit pass proves prompt binding, not rendered salience, originality across history, audience emotion, virality, or sales. Inspect actual pixels for image claims.
- Moe-element activation is explicit-only. A culture label is routing metadata; the selected v2 candidate must describe observable construction, action, relation, camera, or format evidence. Preference cues choose only among candidates of the explicitly selected element. The v4 wrapper never changes ordinary safety metadata, refusal/retry behavior, negative prompt, or universal-scene eligibility, and v1-v3 replay remains untouched.
