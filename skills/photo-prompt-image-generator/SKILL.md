---
name: photo-prompt-image-generator
description: Generate image-ready photographic prompts and, when requested, images through an isolated intent-first baseline, contextual candidate-pack clarification and creativity-bounded augmentation, an authorial final pass, and fail-closed audit. Use for random, intent-led, preset-based, Korean short-concept, creative, detail-rich, sensual-editorial, fetish-fashion, commercial, audience-outcome, and subculture photo requests.
---

# Photo Prompt Image Generator

Understand the requester first. Write a complete standalone photographic prompt from that understanding. Freeze it. Only then may project-local profiles, registries, candidate data, or composition references enter the workflow.

Canonical skill path: `skills/photo-prompt-image-generator`.

User instructions and existing session authorization take precedence over this skill's procedural defaults, subject to system, developer, and image-tool requirements. Continue work already authorized; do not ask the user to approve the same action or API cost again. Ask only when a required decision or authorization is actually missing.

## Non-Negotiable Phase Boundary

For an initial request, before `baseline_prompt_en` and its `photo-authorial-core/v3` hash are frozen, use only:

- the current user conversation, including definitions, exclusions, modifiers, references, and corrections;
- the model's general knowledge and independent visual reasoning;
- one focused clarification question when different plausible meanings would materially change the image; or
- focused public-web research about the term's meaning when it is stable and publicly documentable but unfamiliar or uncertain.

During that pre-core phase, do not open, search, quote, or infer from:

- any candidate pack or earlier generated pack;
- any file under this skill's `assets/`, `references/`, or `scripts/` directories;
- visual-obligation profiles, registries, aliases, tags, presets, recipes, semantic indexes, or quality layers;
- tests, fixtures, evaluation cases, snapshots, rendered attempts, or maintenance evidence;
- private routing, another experiment arm, or a previous prompt produced from project-local knowledge.

The `SKILL.md` procedure is the only project-local material available before the core. This initial-request rule includes the neutral schemas below; retries have only the explicit exception in the next paragraph. This file intentionally contains no maintained definition for any particular keyword. A profile name, alias, or project glossary must never retroactively supply the initial meaning.

A retry has one narrow exception: inspect the named parent request/core/intent-lock hashes, frozen fields and evidence for dimensions the requester preserves, the effective hard obligations governing those dimensions, and the reported defect relevant to the repair. A previously selected opt-in obligation is part of that effective hard contract. Read only those fields from the parent artifacts; candidate inventories, unselected concepts, previous optional prose, other arms, and maintenance examples remain unavailable. This exception carries an existing obligation and never supplies fresh inspiration. If selective reading is impractical, use a coordinator-created whitelist extract bound to the parent artifact hashes.

## Phase 0 — Resolve Meaning Independently

Read the entire request rather than routing from a token. Preserve user modifiers, negation, reference context, and explicit definitions.

Use this decision order:

1. If the requester supplied a definition, use it. Do not replace it with general knowledge or later project data.
2. If the request has one clear contextual meaning, interpret it with general knowledge and proceed.
3. If a niche term appears to have one stable public meaning but you are not confident, research that meaning using authoritative or primary public sources. Research only the meaning needed to understand the request; do not search for candidate-pack-like visual inspiration.
4. If two or more plausible meanings would materially change subject identity, age, count, pose, body geometry, expression, event, setting, relationship, or exclusions, ask the requester which meaning they intend and wait for the answer.
5. If focused research still leaves a material ambiguity, ask. Do not freeze a guess.

Unspecified creative choices are not unresolved meaning. Decide framing, lighting, or other genuinely open dimensions within the request. A mismatched optional retrieval candidate is rejected later; its presence alone never requires a question.

The requesting user's intended meaning has highest priority. System and image-tool policy still applies. This workflow changes knowledge timing; it does not add a new adult/safety classifier or routing policy.

## Phase 1 — Write and Freeze the Basic Prompt

Without project-local prompt data, author a coherent 48–640 word English photographic prompt that can stand alone. Treat 360 words as the default recommended maximum, not a hard cap. Exceed it only when requester meaning or literal hard evidence cannot be represented cleanly within 360 words; never pad toward the limit. It must already specify a concrete subject, setting, visible event or state, and at least two visual priorities. It is not a search query, tag bag, or placeholder.

First create one external `photo-request-envelope/v1` from the actual requester message. `request_text` is the complete, byte-exact user text, never an agent summary. For a single-topic request, the active span may be the whole request. For a multi-topic or multi-arm request, select the exact non-overlapping topic span plus every exact global modifier that governs that arm. Do not invent a cleaner per-arm request. Create and freeze this envelope before delegation so a downstream agent cannot relabel its own interpretation as user text. In delegated work, the coordinator creates the envelope and passes its path plus SHA-256 to the child; a task brief, coordinator safety summary, reviewer note, or subagent message is never requester text and must never be used to create or expand the envelope.

```json
{
  "contract_version": "photo-request-envelope/v1",
  "provenance": "requesting_user",
  "request_id": "<stable run-local request id>",
  "request_text": "A glass lighthouse above a frozen lake",
  "request_sha256": "<SHA-256 of exact UTF-8 request_text bytes>",
  "active_spans": [
    {"span_id": "topic", "start": 0, "end": 38, "text": "A glass lighthouse above a frozen lake"}
  ]
}
```

Freeze it as:

```json
{
  "contract_version": "photo-authorial-core/v3",
  "provenance": "agent_prepack",
  "source_request": "<the complete byte-exact request_text from the envelope>",
  "interpreted_intent": "<contextual meaning and visual purpose>",
  "subject": "<concrete subject>",
  "setting": "<concrete photographic setting>",
  "event": "<one visible action, state, or event>",
  "visual_priorities": ["<priority one>", "<priority two>"],
  "baseline_prompt_en": "<independently authored basic prompt>",
  "user_definitions": [
    {
      "term": "<term defined or clarified by the requester>",
      "source_text": "<exact substring in source_request>",
      "interpreted_meaning": "<the requester's meaning>",
      "prompt_evidence": "<literal component phrase already in baseline_prompt_en>"
    }
  ],
  "interpretation_provenance": [
    {
      "term": "<materially interpreted term>",
      "source_text": "<exact substring in source_request>",
      "basis": "agent_general_knowledge | request_context | public_web_research",
      "resolution": "<context-resolved meaning used to write the baseline>",
      "sources": ["<HTTP(S) URL required only for public_web_research>"]
    }
  ],
  "unresolved_ambiguities": [],
  "user_exclusions": ["<only a visual idea the requester explicitly excluded>"],
  "runtime_forbidden_labels": ["<request-grounded label retained for meaning retrieval but omitted from runtime prose>"],
  "intent_lock": {
    "contract_version": "photo-intent-lock/v1",
    "priority": "requesting_user",
    "semantic_anchors": [
      {
        "anchor_id": "core_concept",
        "source_text": "<text inside one active requester span>",
        "dimension": "concept",
        "prompt_evidence": "<literal positive phrase already in baseline_prompt_en>"
      },
      {
        "anchor_id": "core_subject",
        "source_text": "<text inside one active requester span>",
        "dimension": "subject",
        "prompt_evidence": "<literal subject phrase already in baseline_prompt_en>"
      },
      {
        "anchor_id": "core_event",
        "source_text": "<text inside one active requester span>",
        "dimension": "event",
        "prompt_evidence": "<literal event phrase already in baseline_prompt_en>"
      }
    ],
    "locked_dimensions": ["concept", "subject", "event"],
    "open_dimensions": ["framing", "composition", "lighting", "camera"]
  },
  "semantic_assertions": [],
  "request_lineage": null,
  "style": {
    "domain": "<fitting photographic domain>",
    "family": "<agent-authored style family>",
    "evidence": ["<visible cue one>", "<visible cue two>"]
  },
  "variation_key": "<optional run-local key>"
}
```

Rules:

- `source_request` must byte-equal the envelope's complete `request_text`; the generator derives and hash-binds `request_binding`.
- Every active span needs both semantic-origin coverage (`user_definitions` or `interpretation_provenance`) and at least one intent anchor. Every locked dimension needs an anchor with substantive requester source text and its own distinct literal baseline evidence phrase. `concept`, `subject`, and `event` are always locked; lock any other user-specified dimension as well. Open and locked dimensions are disjoint. V6 permits zero or one open dimension for precise requests or local repairs; write `open_dimensions: []` explicitly when none are open, and never invent freedom to satisfy a creativity quota.
- Use only these v3 dimension names: `concept`, `subject`, `identity`, `count`, `age`, `role`, `species`, `appearance`, `pose`, `body_geometry`, `expression`, `action`, `event`, `setting`, `relationship`, `sexual_tone`, `style`, `reference_use`, `viewer_outcome`, `text`, `format`, `framing`, `composition`, `lighting`, `camera`, `color`, `material`, `timing`, `atmosphere`, `character_response`.
- Put an actual requester definition or answer to a clarification question in `user_definitions`. Its `source_text` must equal a complete active span and cannot be only the term itself. A bare term is an agent interpretation, not proof that the requester supplied a definition.
- Use `interpretation_provenance` for material agent/context/web interpretations, not for requester-owned definitions. Web-based entries require at least one source URL; URLs do not enter the retrieval query.
- `unresolved_ambiguities` is mandatory and must be empty. If it is not empty, ask or research before continuing.
- `user_exclusions` contains only explicit requester negatives. Never use it to hide a requested concept, because exclusions are removed from semantic retrieval.
- Do not translate platform policy, an agent's comfort preference, a coordinator's risk summary, or a profile's conservative default into `user_exclusions`, `baseline_prompt_en`, or runtime negatives. Platform and image-tool enforcement remains active outside prompt semantics.
- If a source-grounded shorthand label should aid interpretation and profile activation but should not be sent to the image runtime, put it in `runtime_forbidden_labels` and express its intended visible components in anchors and the baseline. Runtime-only labels remain in retrieval; only their literal runtime spelling is forbidden.
- `semantic_assertions` is the only normal v6 input for meanings that need a typed downstream contract. A required assertion affects locked dimensions, an advisory assertion affects open dimensions, and an excluded assertion cannot be resurrected by retrieval. Every assertion cites active `source_span_ids`; every required evidence phrase is already literal in `baseline_prompt_en`.
- Treat a named character or relationship archetype whose meaning depends on behavior as a required visible `character_response`, even when the requester calls it a concept or also specifies a costume, role, facial expression, or prop. Lock `character_response` and make the baseline show an unmistakably adult actor, one identifiable relationship target or repeated marker of that same target, one concrete target-directed action, one affect leak, and one already-visible consequence in a single frame. An adjective, intense gaze, smile, role outfit, weapon, medical tool, or other prop alone never satisfies this contract; reference-image appearance never activates personality.
- Every required non-`character_response` assertion is compiled into `photo-semantic-assertion-obligations/v1`. When that block exists, copy its exact frozen evidence into `semantic_assertion_evidence.evidence.<assertion_id>`, bind `source_contract_sha256`, and keep every phrase literal in the final prompt. Retrieval cannot supply or replace any of those hard phrases.
- For a required visible character response, lock `character_response`, add its own semantic anchor, and write one `character_response` assertion with the generic axes `surface_affect`, `underlying_affiliation`, `relationship_target`, `primary_action`, `affect_leak_timing`, `affect_leak_channels`, and `event_phase`. Select exactly one primary leak channel. When the meaning depends on a relation rather than isolated attributes, encode bounded generic `relations` using `same_target`, `contrasts`, and/or `temporal_order`; do not leave the relation to a named label. Every relation member must be a declared generic axis or causal role, and every `same_target` relation must include `relationship_target`. For a named affection-control archetype, bind the affection surface or care, primary action, and immediate consequence to that same target; an affect leak may support this vector but cannot replace the consequence. Bind `actor_phrase`, `baseline_phrase`, `trigger_phrase`, `target_phrase`, `primary_action_phrase`, `affective_leak_phrase`, `visible_response_phrase`, `immediate_consequence_phrase`, and `continuity_phrase` to literal baseline text. Values are authored from the request; never route a named archetype to fixed gaze, face, pose, or story geometry.
- `request_lineage` is `null` for an initial request. On a retry it hash-binds the parent request/core and separates preserved dimensions from the explicitly allowed changes; the two sets are non-empty and disjoint. Inspect only the parent fields allowed by the retry exception above before freezing the retry. If `concept` or `character_response` is preserved and the parent had a hard visual obligation, recreate that same obligation as a hash-bound post-core `photo-visual-intent/v1` sourced from an exact current frozen core field. Do not let an elliptical retry phrase demote a preserved hard obligation into an unselected embedding candidate, and do not carry the obligation when the requester changed or excluded the governing meaning.
- A fidelity complaint about a meaningful interactive prop is not permission to remove, relocate, conceal, or transfer it. On such a retry, use `photo-request-lineage/v2` and one object-agnostic `repair_targets` row. Freeze actor, object, interaction state, expected contact, protected locked dimensions, positive interaction and recognition phrases, and only the local repair axes that may change. Use `relation_origin: parent_preserved` when the parent relation remains intended and `relation_origin: requester_corrected` when the requester explicitly corrects an evasive parent relation. Bind both phrases through one required action assertion in the baseline. Decorative background objects and non-action-bearing ornaments do not need repair targets.
- Every multi-arm run shares the immutable raw requester text but freezes a separate, exact-span-bound envelope and core for each arm before any arm sees project-local data.

### Neutral assertion wire shape

The following is schema information only; every value and evidence phrase is authored independently before retrieval.

```json
{
  "assertion_id": "<unique alphanumeric, underscore or hyphen ID; at most 64 characters>",
  "dimension": "<one v3 dimension>",
  "polarity": "required | advisory | excluded",
  "source_span_ids": ["<active envelope span ID>"],
  "affected_dimensions": ["<v3 dimension governed by this assertion>"],
  "axes": {"<lowercase_snake_case axis>": "<authored value or list of values>"},
  "evidence": {"<lowercase_snake_case evidence key>": "<literal baseline phrase>"}
}
```

There are at most 16 assertions, 1–16 axes per assertion, at most 8 distinct values per axis, and at most 16 evidence fields. Required assertions have at least one evidence phrase, each with at least two content words. Values are strings or string lists; evidence values are strings. A required `character_response` uses the seven axes and nine evidence keys listed above, exactly one `primary_action`, and a one-item list for `affect_leak_channels`.

Only `character_response` may add `relations`, a list of 1–8 objects with exactly one of these shapes: `{"operator":"same_target","members":["<member>","relationship_target"]}`, `{"operator":"contrasts","left":"<member>","right":"<member>"}`, or `{"operator":"temporal_order","first":"<member>","then":"<member>"}`. Members are `actor`, `baseline`, `surface_affect`, `underlying_affiliation`, `relationship_target`, `target`, `primary_action`, `affect_leak`, `affect_leak_timing`, `trigger`, `visible_response`, `immediate_consequence`, `continuity`, or `event_phase`. Use distinct members and no duplicate relations. Non-character assertions omit `relations`; they may describe their observable relations through authored axes and literal evidence.

### Negative-intent firewall

Write `baseline_prompt_en` as positive visual realization. Do not embed instruction-shaped blanket negatives such as `No X, Y, or Z`, `Do not ...`, `Avoid ...`, `Exclude ...`, or clauses such as `never touching anyone`. These clauses can silently delete the requested relationship, action, emotion, prop, person count, wardrobe, or genre signal. The modern core normalizer rejects them before the core can be frozen.

Use three separate lanes:

- A semantic exclusion is valid only when the requester explicitly supplied it and it is grounded in an active request span. Keep it in `user_exclusions`; after removing a literal directive prefix, a runtime-negative item must equal the complete exclusion. Do not split a combined exclusion or broaden it by substring, synonym, or category inference.
- Automatic `negative_en` is limited to a narrow intent-neutral photographic-defect vocabulary. Generic safety, taste, count, contact, action, relationship, expression, wardrobe, and genre suppressions are removed. Identity-preservation negatives are allowed only when identity-reference preservation is explicitly enabled.
- Platform or image-tool policy is enforced by the platform/tool and by post-render review. It is not serialized as a blanket runtime negative. When a permitted scene needs a local boundary, describe the visible positive state instead: for example, `the capped needle hovers beside an intact sleeve` rather than `no contact, no injection, no gore`.

The pack exposes a hash-bound `photo-negative-intent-guard/v1` containing the emitted negative terms and governing policy. It is recomputed during composed audit. This guard applies to both the positive prompt surface and `negative_en`; copying the pack negative bytes is necessary but no longer sufficient.

Pass the envelope with `--request-envelope-json`, the core with `--authorial-core-json`, and explicitly request candidate-pack v6. The generator canonicalizes both, rejects unsupported or ungrounded fields, and binds their hashes and active spans to retrieval, the public pack, composition, and runtime.

## Phase 2 — Retrieve After the Core Is Frozen

Only now may the generator load dictionaries, the semantic index, candidate material, the visual-profile registry, and its generated registry-hash-bound index.

Generate exactly one pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --request-envelope-json request_envelope.json \
  --authorial-core-json authorial_core.json \
  --candidate-pack-version v6 \
  --creativity 0.5 \
  --emit-candidate-pack --n 1
```

The generator derives retrieval from the active requester spans and frozen core, removes true requester exclusions, and retains runtime-forbidden labels for meaning retrieval. `--concept-lock` is normally omitted; if supplied, every value must byte-equal the active spans in order. The pack must not define the baseline after the fact.

Candidate-pack v6 separates three jobs:

- `semantic_assertions` and the baseline are the governing meaning. The v3 core is required and non-revisable inside the pack run. A material correction requires a rebuilt envelope/core/pack; use an already supplied requester correction without asking again, and ask only when requester meaning remains unresolved.
- `semantic_clarification` and BM25F/embedding retrieval are post-core assistance. Exact request-scoped profile terms may retain their declared hard meaning. BM25F-only, embedding-only, and fused approximate hits are optional and can never create an assertion, required evidence phrase, or render gate.
- `creative_augmentation` is sampled only after hard applicability, conflict, identity/species/no-people, safety, negative, and requester-exclusion filters. Creativity `0..0.25` permits `near`, `0.25..0.75` permits `near + adjacent`, and `0.75..1` also permits `lateral`; seed selects within the allowed range. Every transformed choice declares `affected_dimensions`, which must all be open and subordinate to the locked meaning.

V6 compiles frozen character-response axes and evidence through `photo-character-response/v1`, and other required assertions through `photo-semantic-assertion-obligations/v1`. It never calls the legacy raw-text moe router. The composed audit recomputes these contracts from the core. Retrieval consistency, labels, scores, and array order never create hard evidence or revise a frozen meaning; every creative candidate may be rejected. Consult `references/retrieval-contract.md` only for retrieval diagnostics or implementation details.

Read the compact composition view before loading full optional candidate details:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/compose_pack_view.py \
  --pack candidate_pack.json --output composer_view.json
```

The view binds the unchanged source pack and presents requirements plus a candidate catalog. Use repeatable `--candidate-id <id>` to read full details for candidates under consideration. Review every mandatory requirement, retrieve a selected candidate's complete constraints before using it, and keep the original pack as the audit input. The view is a reading aid, not a replacement or mutable pack. Modern v6 semantic surfaces preserve short `concept_units` and directed `relations`; keep each unit intact when interpreting its meaning. Selecting a relational candidate requires literal `relation_evidence`, and selecting an optional bundle also requires `component_evidence` for every component. Read the complete selection contract in the detail view and `references/composition-contract.md`. Bundle members form one joint choice; their associated profile IDs never acquire automatic hard authority.

### Optional post-core visual intent

For an exact, non-substitutable requester definition or a preserved parent hard obligation, read `references/retrieval-contract.md` and construct `photo-visual-intent/v1` only after the core is frozen. Its evidence must already belong to the requester definition or one exact frozen core field. Exact resolution may bind a hard profile; approximate retrieval remains optional. Do not construct visual intent merely because a candidate offers an attractive interpretation.

Before rendering, an explicitly focal perceptual meaning needs a required typed assertion or an active hard visual obligation. A broad label, optional candidate, or embedding hit does not provide coverage. If coverage is missing, rebuild from the clear requester meaning; ask only if that meaning is still ambiguous. Record focal coverage separately from prompt, runtime, and pixel status.

## Phase 3 — Clarify, Enrich, and Add the Authorial Pass

Read `references/composition-contract.md` for the composed shape and active conditional fields. Compose one final English prompt from the core and the pack; optional candidates may clarify or deepen it only within permitted dimensions.

For every semantic clarification, record exactly one decision:

- Apply a fitting clarification and bind literal prompt evidence.
- Reject a context-mismatched or gated clarification.

Never supersede a v2/v3 core or requester definition. Reject optional candidates that suggest a different meaning and continue with the frozen core. If an actual requester ambiguity or a conflict in required evidence prevents faithful composition, stop that run and resolve it before rebuilding the envelope, core, and pack. A clear requester correction already authorizes that rebuild. `superseded_by_revision` exists only for auditing legacy v1 evidence.

For creative candidates, decide each as `transformed` or `rejected`. Rejecting all is valid. Transform at most three, declare `affected_dimensions`, keep them within `intent_lock.open_dimensions`, and add a new relation, cause, material behavior, framing, light, omission, or timing decision instead of copying source terms.

Bind the exact pack ID, negative, core hash, intent-lock hash, anchor IDs, preserved evidence, candidate choices, all clarification decisions, and creative decisions in the composed object. Set `composer` to `agent`.

Preserve every anchor's literal evidence plus at least three substantive literal baseline phrases, and keep requester exclusions and runtime-only labels absent. New v6 packs expose `authorial_composition.authorship_policy` (`photo-authorial-authorship-policy/v1`): make at least `min(2, len(open_dimensions))` substantive decisions on distinct open dimensions. With zero open dimensions, use an empty `authorial_decisions` list and preserve the requested realization. With one, make one decision. Do not add freedom or alter locked evidence to meet this count. Serialized packs without the policy retain their recorded legacy minimum of two.

Keep `prompt_en` within 48–640 English words and aim for at most 360. The evidence-adjusted advisory ceiling is the larger of 360 or hard-evidence words plus 160, capped at 640; exceeding either advisory ceiling produces a warning. Remove optional material before dropping requester meaning or literal evidence. Compatible evidence may share a natural clause. The final result must read as one coherent photograph. Requester meaning outranks generic character, moe, viewer, style, and creative defaults. Preserve only the guard-approved pack `negative_en`, and keep blanket negative directives out of the positive prompt. Recorded legacy prompt budgets remain authoritative during replay.

When hard visual obligations are active, supply every required evidence field as an identifiable literal phrase in `prompt_en`, preserve request-scoped bindings byte-for-byte, and keep all declared runtime-forbidden labels absent. Compatible evidence phrases may overlap inside one natural clause; do not duplicate prose solely to satisfy the budget ledger. Selected optional visual concepts promote their entire opt-in obligation and render gates; unselected concepts add no duty.

When `render_repair` exists, add `render_repair_evidence` with its exact `source_contract_sha256` and one byte-identical evidence map per repair ID. Keep both the frozen interaction phrase and object-recognition phrase literal in `prompt_en`. This is positive realization of the requested relation, never a negative list or an instruction to move the object away from the actor.

## Phase 4 — Audit Before Image Generation

Write the pack and composed object to files, then run:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json \
  --composed composed_prompt.json
```

Fix every failure. `negative_intent_guard_contract`, `negative_intent_guard_terms`, `negative_intent_guard_baseline`, and `negative_intent_guard_prompt` are blocking failures: they mean either the pack carries an ungrounded semantic suppression or positive prompt prose is trying to delete meaning with a blanket negative directive. Do not generate an image from an unaudited prompt.

If image generation was requested, read `references/image-runtime.md`, copy `source_intent_lock_sha256` into the exact runtime request, and when present also copy `render_repair_contract_sha256`. Audit it with `scripts/audit_image_render_request.py`, generate, preserve the output and ledger record, then record and audit the exact generic repair hard-gate set with `scripts/audit_image_render_review.py`. Prompt/audit success is preflight evidence, not proof that rendered pixels satisfy the request.

## Post-Core Reference Routing

All references below are post-core only. Load only what the frozen request and returned pack require:

- Candidate composition, audit, hard obligations, and quality fields: `references/composition-contract.md`
- Retrieval internals, indexes, and diagnostic boundaries: `references/retrieval-contract.md`
- Candidate idea routes and composable adult-appeal axes: `references/hybrid-augmentation-contract.md`
- High-creativity proposals and authorial selection: `references/creative-direction-contract.md`
- Viewer response or commercial communication outcomes: `references/viewer-experience-contract.md`
- Natural-language character-response, identity, and pixel-review contracts: `references/moe-response-contract.md`
- Intent, concept, preset, and slot routing behavior: `references/concept-routing.md`
- Image generation, saving, retries, and ledger records: `references/image-runtime.md`
- Dictionary/profile edits, validation, semantic index, and evaluation: `references/maintenance.md`

Do not load every reference for a normal prompt request. Maintenance fixtures and research evidence are never runtime composition sources.

## Compatibility and Diagnostics

- V6 plus `photo-request-envelope/v1`, `photo-authorial-core/v3`, `photo-intent-lock/v1`, and typed `semantic_assertions` is the normal workflow.
- V5 plus `photo-authorial-core/v2` remains a compatibility workflow for replaying the prior raw-text character router and downstream-default contract. V1 core packs remain audit-only legacy evidence.
- V4 remains available only for an explicit compatibility consumer. Its older `authorial-request/v1` and hybrid-augmentation behavior are unchanged.
- V3/V2 are historical replay surfaces and require `--legacy-replay-reason`.
- `--explain-scene-routing` is private diagnostic output and must never be used as a composition pack.
- Public packs withhold scores, probabilities, private preset IDs, sampler answer keys, reusable render-blueprint prose, and expanded argv.

## Validation for Skill Maintenance

After changing this skill or its contracts, run focused tests first, then the related suite:

```bash
.venv/bin/python -m unittest tests.test_photo_prepack_isolation_v5 -v
.venv/bin/python -m unittest tests.test_photo_authorial_core_v5 -v
.venv/bin/python -m unittest tests.test_photo_authorial_core_v6 -v
.venv/bin/python -m unittest tests.test_photo_bm25f_retrieval -v
.venv/bin/python -m unittest tests.test_photo_character_response_concepts -v
.venv/bin/python -m unittest tests.test_photo_visual_obligations -v
.venv/bin/python -m unittest tests.test_photo_visual_profile_retrieval -v
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python -m unittest discover -s tests
```

Review intentional golden changes. Do not weaken frozen holdouts after a failure. Dictionary fields that affect semantic text require an index refresh; policy-only documentation does not. Image/API generation is not ordinary validation unless the requester explicitly asks for it.
