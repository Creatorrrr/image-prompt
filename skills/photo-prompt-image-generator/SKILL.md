---
name: photo-prompt-image-generator
description: Generate image-ready photographic prompts and, when requested, images through an isolated intent-first baseline, contextual candidate-pack clarification and creativity-bounded augmentation, an authorial final pass, and fail-closed audit. Use for random, intent-led, preset-based, Korean short-concept, creative, detail-rich, sensual-editorial, fetish-fashion, commercial, audience-outcome, and subculture photo requests.
---

# Photo Prompt Image Generator

Understand the requester first. Write a complete standalone photographic prompt from that understanding. Freeze it. Only then may project-local profiles, registries, candidate data, or composition references enter the workflow.

Canonical skill path: `skills/photo-prompt-image-generator`.

## Non-Negotiable Phase Boundary

Before `baseline_prompt_en` and its `photo-authorial-core/v2` hash are frozen, use only:

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

The `SKILL.md` procedure is the only project-local material available before the core. This file intentionally contains no maintained definition for any particular keyword. A profile name, alias, or project glossary must never retroactively supply the initial meaning.

## Phase 0 — Resolve Meaning Independently

Read the entire request rather than routing from a token. Preserve user modifiers, negation, reference context, and explicit definitions.

Use this decision order:

1. If the requester supplied a definition, use it. Do not replace it with general knowledge or later project data.
2. If the request has one clear contextual meaning, interpret it with general knowledge and proceed.
3. If a niche term appears to have one stable public meaning but you are not confident, research that meaning using authoritative or primary public sources. Research only the meaning needed to understand the request; do not search for candidate-pack-like visual inspiration.
4. If two or more plausible meanings would materially change subject identity, age, count, pose, body geometry, expression, event, setting, relationship, or exclusions, ask the requester which meaning they intend and wait for the answer.
5. If focused research still leaves a material ambiguity, ask. Do not freeze a guess.

The requesting user's intended meaning has highest priority. System and image-tool policy still applies. This workflow changes knowledge timing; it does not add a new adult/safety classifier or routing policy.

## Phase 1 — Write and Freeze the Basic Prompt

Without project-local prompt data, author a coherent 24–180 word English photographic prompt that can stand alone. It must already specify a concrete subject, setting, visible event or state, and at least two visual priorities. It is not a search query, tag bag, or placeholder.

First create one external `photo-request-envelope/v1` from the actual requester message. `request_text` is the complete, byte-exact user text, never an agent summary. For a single-topic request, the active span may be the whole request. For a multi-topic or multi-arm request, select the exact non-overlapping topic span plus every exact global modifier that governs that arm. Do not invent a cleaner per-arm request. Create and freeze this envelope before delegation so a downstream agent cannot relabel its own interpretation as user text.

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
  "contract_version": "photo-authorial-core/v2",
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
- Every active span needs both semantic-origin coverage (`user_definitions` or `interpretation_provenance`) and at least one intent anchor. Every locked dimension needs an anchor with substantive requester source text and its own distinct literal baseline evidence phrase. `concept`, `subject`, and `event` are always locked; lock any other user-specified dimension as well. Open and locked dimensions are disjoint.
- Put an actual requester definition or answer to a clarification question in `user_definitions`. Its `source_text` must equal a complete active span and cannot be only the term itself. A bare term is an agent interpretation, not proof that the requester supplied a definition.
- Use `interpretation_provenance` for material agent/context/web interpretations, not for requester-owned definitions. Web-based entries require at least one source URL; URLs do not enter the retrieval query.
- `unresolved_ambiguities` is mandatory and must be empty. If it is not empty, ask or research before continuing.
- `user_exclusions` contains only explicit requester negatives. Never use it to hide a requested concept, because exclusions are removed from semantic retrieval.
- If a source-grounded shorthand label should aid interpretation and profile activation but should not be sent to the image runtime, put it in `runtime_forbidden_labels` and express its intended visible components in anchors and the baseline. Runtime-only labels remain in retrieval; only their literal runtime spelling is forbidden.
- Every multi-arm run shares the immutable raw requester text but freezes a separate, exact-span-bound envelope and core for each arm before any arm sees project-local data.

Pass the envelope with `--request-envelope-json`, the core with `--authorial-core-json`, and explicitly request candidate-pack v5. The generator canonicalizes both, rejects unsupported or ungrounded fields, and binds their hashes and active spans to retrieval, the public pack, composition, and runtime.

## Phase 2 — Retrieve After the Core Is Frozen

Only now may the generator load dictionaries, the semantic index, candidate material, the visual-profile registry, and its generated registry-hash-bound index.

Generate exactly one pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --request-envelope-json request_envelope.json \
  --authorial-core-json authorial_core.json \
  --candidate-pack-version v5 \
  --creativity 0.5 \
  --emit-candidate-pack --n 1
```

The retrieval query is derived from the exact active requester spans, with true requester exclusions redacted, plus interpreted intent, subject, setting, event, visual priorities, baseline prompt, requester definitions, interpretation resolutions, and optional style evidence. Runtime-forbidden labels stay in retrieval. The pack must not define the baseline after the fact. `--concept-lock` is normally omitted and safely derived; if supplied, every value must byte-equal the active spans in order.

Candidate-pack v5 separates two jobs:

- `semantic_clarification` is deterministic and unaffected by creativity or seed. The v2 core meaning is required and non-revisable inside the pack run; a material correction stops the run and requires requester input plus a rebuilt envelope/core/pack.
- `creative_augmentation` is sampled only after hard applicability, conflict, identity/species/no-people, safety, negative, and requester-exclusion filters. Creativity `0..0.25` permits `near`, `0.25..0.75` permits `near + adjacent`, and `0.75..1` also permits `lateral`; seed selects within the allowed range. Every transformed choice declares `affected_dimensions`, which must all be open and subordinate to the locked meaning.

Every v5 downstream semantic default is also governed by `photo-downstream-intent-precedence/v1`. A default is active only when every dimension it can affect is explicitly listed in `intent_lock.open_dimensions`; a locked or otherwise non-open expression, style, event, relationship, sexual tone, appearance, pose, body geometry, framing, lighting, composition, or text dimension suppresses the corresponding positive instruction, negative-prompt suppression, and render gate. Evidence on a locked dimension must byte-equal its matching semantic-anchor phrase; evidence on another non-open dimension must already be literal in the frozen baseline. In particular, generic warm-affect, cute/beautiful styling, recovery-beat, character-mechanism, background-text, and sensual-support defaults never repair or reinterpret a closed requester meaning. This rule is dimension-based and must not be implemented as named-topic exceptions.

Visual-profile retrieval is a deterministic substep of semantic clarification. One generated index contains boundary-aware exact lookup rows and one embedding vector per profile, all derived from the single authored registry and rejected when its registry hash or text recipe is stale. Exact request terms may retain their existing request-scoped hard meaning. A profile found only by embedding similarity is always an optional `visual_concept_candidate`: it creates no prompt duty or render gate unless the composer explicitly selects it. The same private resolution is projected into `visual_obligations`, `visual_concept_candidates`, and `semantic_clarification`; scores, vectors, matched terms, and rank remain private. This lookup is independent of creativity and seed.

Candidate order is never preference. Every creative candidate remains optional material.

### Optional post-core visual intent

If the requester supplied an exact, non-substitutable visual definition or binding, create `photo-visual-intent/v1` only after the authorial core is frozen:

```json
{
  "contract_version": "photo-visual-intent/v1",
  "provenance": "agent_prepack",
  "obligations": [
    {
      "source": "requesting_user_definition",
      "scope": "request_only",
      "source_text": "<exact normalized requesting-user source>",
      "bindings": {"<required evidence field>": "<literal English prompt phrase>"}
    }
  ]
}
```

Omit `profile_id` when the source text contains one unique direct registry meaning; the generator resolves it through the index's exact lane after the core exists. Embedding similarity never supplies an omitted hard profile ID. Zero or multiple exact matches fail closed. An explicit profile ID remains supported for post-core maintenance or replay. For an agent-owned frozen field, use `agent_postcore_interpretation` and make `source_text` exactly equal that field.

Do not construct visual intent merely because project data offers an attractive interpretation. Direct request semantics and requester definitions govern activation. Strong indirect component similarity may expose an optional visual concept, but cannot silently create a hard duty.

## Phase 3 — Clarify, Enrich, and Add the Authorial Pass

Compose one final English prompt from the core and the pack. The core stays primary; candidate material may clarify, strengthen, contrast, or deepen it.

For every semantic clarification, record exactly one decision:

- Apply a fitting clarification and bind literal prompt evidence.
- Reject a context-mismatched or gated clarification.

Never supersede a v2 core or requester definition. Never silently rewrite the core. If pack data suggests a materially different meaning, stop; do not compose or render until the requester resolves it and a new envelope, core, and pack are built. `superseded_by_revision` exists only for auditing legacy v1 evidence.

For creative candidates, decide each as `transformed` or `rejected`. Rejecting all is valid. Transform at most three, declare `affected_dimensions`, keep them within `intent_lock.open_dimensions`, and add a new relation, cause, material behavior, framing, light, omission, or timing decision instead of copying source terms.

The composed JSON must include the exact pack ID and negative, candidate choices, all clarification decisions, creative decisions, and:

```json
{
  "authorial_core_binding": {
    "source_authorial_core_sha256": "<exact core hash>",
    "source_intent_lock_sha256": "<exact intent-lock hash>",
    "preserved_anchor_ids": ["<every semantic anchor id exactly once>"],
    "preserved_evidence": ["<baseline phrase one>", "<two>", "<three>"],
    "authorial_decisions": [
      {"dimension": "framing", "decision": "<new decision>", "rationale": "<reason>"},
      {"dimension": "lighting", "decision": "<new decision>", "rationale": "<reason>"}
    ]
  },
  "composer": "agent"
}
```

Preserve every anchor's literal evidence plus at least three substantive literal baseline phrases, keep requester exclusions and runtime-only labels absent, and make at least two new authorial decisions only in open dimensions. The final pass should produce one coherent photograph, not a list of adopted keywords. Requester meaning outranks generic character, moe, viewer-response, style, and creative contracts; those contracts may realize the locked intent but cannot replace it.

When hard visual obligations are active, supply every required evidence field as a distinct literal phrase in `prompt_en`, preserve request-scoped bindings byte-for-byte, and keep all declared runtime-forbidden labels absent. Selected optional visual concepts promote their entire opt-in obligation and render gates; unselected concepts add no duty.

## Phase 4 — Audit Before Image Generation

Write the pack and composed object to files, then run:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --candidate-pack candidate_pack.json \
  --composed composed_prompt.json
```

Fix every failure. Do not generate an image from an unaudited prompt.

If image generation was requested, read `references/image-runtime.md`, copy `source_intent_lock_sha256` into the exact runtime request, audit it with `scripts/audit_image_render_request.py`, generate, preserve the output and ledger record, and apply any request-specific pixel review contract. Prompt/audit success is preflight evidence, not proof that rendered pixels satisfy the request.

## Post-Core Reference Routing

All references below are post-core only. Load only what the frozen request and returned pack require:

- Candidate composition, audit, hard obligations, and quality fields: `references/composition-contract.md`
- Candidate idea routes and composable adult-appeal axes: `references/hybrid-augmentation-contract.md`
- High-creativity proposals and authorial selection: `references/creative-direction-contract.md`
- Viewer response or commercial communication outcomes: `references/viewer-experience-contract.md`
- Natural-language character-response, identity, and pixel-review contracts: `references/moe-response-contract.md`
- Intent, concept, preset, and slot routing behavior: `references/concept-routing.md`
- Image generation, saving, retries, and ledger records: `references/image-runtime.md`
- Dictionary/profile edits, validation, semantic index, and evaluation: `references/maintenance.md`

Do not load every reference for a normal prompt request. Maintenance fixtures and research evidence are never runtime composition sources.

## Compatibility and Diagnostics

- V5 plus `photo-request-envelope/v1`, `photo-authorial-core/v2`, and `photo-intent-lock/v1` is the normal workflow. V1 core packs remain audit-only legacy evidence and cannot be generated through the normal v5 CLI.
- V4 remains available only for an explicit compatibility consumer. Its older `authorial-request/v1` and hybrid-augmentation behavior are unchanged.
- V3/V2 are historical replay surfaces and require `--legacy-replay-reason`.
- `--explain-scene-routing` is private diagnostic output and must never be used as a composition pack.
- Public packs withhold scores, probabilities, private preset IDs, sampler answer keys, reusable render-blueprint prose, and expanded argv.

## Validation for Skill Maintenance

After changing this skill or its contracts, run focused tests first, then the related suite:

```bash
.venv/bin/python -m unittest tests.test_photo_prepack_isolation_v5 -v
.venv/bin/python -m unittest tests.test_photo_authorial_core_v5 -v
.venv/bin/python -m unittest tests.test_photo_visual_obligations -v
.venv/bin/python -m unittest tests.test_photo_visual_profile_retrieval -v
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current
.venv/bin/python -m unittest discover -s tests
```

Review intentional golden changes. Do not weaken frozen holdouts after a failure. Dictionary fields that affect semantic text require an index refresh; policy-only documentation does not. Image/API generation is not ordinary validation unless the requester explicitly asks for it.
