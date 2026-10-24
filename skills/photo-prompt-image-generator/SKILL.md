---
name: photo-prompt-image-generator
description: Write photographic image prompts and generate requested images. Use for photo concepts, creative photo direction, and reference-guided photographic generation.
---

# Photo Prompt Image Generator

Understand the requester, resolve the current creative controls, then make the main artistic decisions before writing the core. Develop a scene with the care of a novelist: concrete circumstances, particular presence, connected causes and responses, and a moment whose significance a viewer can feel. The baseline should already be a compelling, complete photograph with a coherent visual direction informed by those controls. Freeze that independent draft before project-local retrieval. The final authorial pass may preserve, refine, simplify, or substantially reconstruct its replaceable staging at the resolved creativity level, preserving requester meaning.

Canonical skill path: `skills/photo-prompt-image-generator`.

User instructions and existing session authorization take precedence over this skill's procedural defaults, subject to system, developer, and image-tool requirements. Continue work already authorized; do not ask the user to approve the same action or API cost again. Ask only when a required decision or authorization is actually missing.

If a skill instruction causes a pause or a departure from the user's request, name and link this skill, quote the relevant instruction, and explain whether it is a requirement or your interpretation. Treat required bindings and audits as correctness checks; artistic guidance leaves room for judgment. Deliver the requested prompt or image with concise context, keeping internal schemas and checklists in the run artifacts unless requested.

## Non-Negotiable Phase Boundary

For an initial request, before `baseline_prompt_en` and its `photo-authorial-core/v3` hash are frozen, use only:

- the current user conversation, including definitions, exclusions, modifiers, references, and corrections;
- the model's general knowledge and independent visual reasoning;
- this skill's exact `precore/creative_controls.json` and the candidate-free output of `precore/creative_controls.py`, after resolving requester meaning, for the current values, provenance, ranges and artistic meanings;
- this skill's exact `precore/visual_feature_catalog.json`, only in Phase 1 after resolving the request's meaning, for neutral feature selection;
- the neutral `precore/prepare_photo_run.py` entrypoint and its exact shared helpers: `photo_authoring_wire.py`, `photo_authoring_contracts.py`, `photo_camera_authoring.py`, `photo_embodiment_review.py`, `photo_feature_selection.py`, `photo_run_files.py`, `photo_semantic_witnesses.py`, its candidate-free wire guide `photo_semantic_witnesses.md`, and `photo_workflow_shapes.json`; these validate current authored inputs without candidate access;
- one focused clarification question when different plausible meanings would materially change the image; or
- focused public-web research about the term's meaning when it is stable and publicly documentable but unfamiliar or uncertain.

During that pre-core phase, do not open, search, quote, or infer from:

- any candidate pack or earlier generated pack;
- any file under this skill's `assets/`, `references/`, or `scripts/` directories;
- visual-obligation profiles, registries, aliases, slot candidates, semantic indexes, or quality layers;
- tests, fixtures, evaluation cases, snapshots, rendered attempts, or maintenance evidence;
- private routing, another experiment arm, or a previous prompt produced from project-local knowledge.

The `SKILL.md` procedure and the exact named neutral precore files above are the only project-local authoring material available before the core. `scripts/photo_workflow.py status --run RUN` may read neutral file bindings without initializing candidates. Executing or inspecting that resolver is permitted; it reads no candidate data. The catalog contains observation-category names and provenance only, with no visual examples or prescribed realizations. Category names are not request requirements or profile triggers. The control definitions explain configuration, not the meaning of requester keywords. This initial-request rule includes the neutral schemas below; retries have only the explicit exception in the next paragraph. A profile name, alias, or project glossary must never retroactively supply the initial meaning.

A retry has one narrow exception: inspect the named parent request/core/intent-lock hashes, frozen fields and evidence for dimensions the requester preserves, the effective hard obligations governing those dimensions, and the reported defect relevant to the repair. A previously selected opt-in obligation is part of that effective hard contract. Read only those fields from the parent artifacts; candidate inventories, unselected concepts, previous optional prose, other arms, maintenance examples, and the parent's feature-selection record remain unavailable. The current neutral catalog may be read again for a new selection, but previous selected categories are not inherited as hard obligations. This exception carries an existing obligation and never supplies fresh inspiration. Use `scripts/prepare_retry_context.py prepare` (or `scripts/photo_workflow.py retry-prepare`) as the coordinator, and read only `retry_context.json` and `retry_projection_audit.json`. Executing that named extraction and `photo_workflow.py attach-retry` is the precise pre-core retry exception; it does not permit inspecting their source, private diagnostics, proof inputs, or full parent files. Child freeze executes the same coordinator to reverify the parent and closed scope. For a revised-content child, an unrepresentable lineage-v2 scope stays blocked; same-input repeats use the original run instead.

## Managed authoring and execution

Distinguish three failure routes: `same_input` repeats the exact audited inputs in the existing run; `revised_content` creates a newly frozen child within the requester's authorized changes; `recovery_only` repairs evidence, storage or review without another image call. Explicit moderation blocks and observed transient HTTP failures use `same_input` within the existing call budget. Keep all provider safeguards and each blocked result; do not rewrite a prompt to get around a block. Missing/unknown results, save failures and recorder failures require reconciliation first. The full failure table and execution commands are in [image-runtime.md](references/image-runtime.md#failure-routes) and [photo-workflow.md](references/photo-workflow.md#retry-coordinator-and-child-binding). A same-input retry has no child lineage and needs no invented changed dimension. The lineage-v2 restriction above applies only to revised-content children.

Keep new run directories under `generated/photo-runs/<run-id>/` unless the requester specifies another path. Use `precore/prepare_photo_run.py init --run RUN --request request.txt --spans spans.json --mode prompt_only` (or explicit `--whole-request`). Offsets are Unicode string indices; optional span `text` must equal the exact request slice. The tool rejects malformed offsets or mismatched quotes before creating the run and preserves exact UTF-8 bytes. Run `controls --run RUN --context creative_context.json` with any authored overrides. Canonicalize the baseline before writing literal evidence and reviewing it; `canonicalize --baseline draft.txt` only returns the whitespace-normalized text. Write the core, five to ten neutral feature selections, and embodiment review, then `freeze --run RUN --core core.json --selection selection.json --review review.json`. Derived bindings are stamped; supplied stale bindings and missing decisions are rejected. Frozen edits need a new run.

When the request needs an explicit inventory of reference appearance or requester identity, pass the caller-authored `--input-inventory inputs.json` during `init` and follow the neutral frozen witness contract. List every supplied text or reference input with its actual hash, including the request. Text can establish either scope. Missing files or an omitted inventory do not establish that a scope is absent; preserve an unknown state when completeness is unresolved.

After freeze, use `scripts/photo_workflow.py retrieve --run RUN`, `view`, `compose-audit --composed final.json`, and `prepare-render --parameters transport.json --lane api|native`, all with `--run RUN`. Choice lists, literal evidence and review judgments remain authored. Prompt-only delivery uses `deliver`; it does not read keys or invoke images. Read [references/photo-workflow.md](references/photo-workflow.md) only after core freeze for execution, recovery and coordinator input details. New searches use the installed H-only+F2 release by default. Use the managed commands for retrieval, views and audits; individual native entrypoints remain available for already bound native runs.

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

### Resolve the initial creative controls

Create the byte-exact request envelope described below before drafting. Read `precore/creative_controls.json`: it is the single source of saved defaults and level meanings. Write a small `creative_context.json` with request-resolved `subject_category` (`human`, `nonhuman`, or `unspecified`), `no_people`, and `explicit_nonsexual`. These last two booleans describe explicit requester meaning only; do not infer them from an agent preference, platform policy, or a portrait. Use `creative_overrides.json` only for controls actually selected for this request; omit it to use saved values.

```bash
.venv/bin/python skills/photo-prompt-image-generator/precore/creative_controls.py \
  --request-envelope-json request_envelope.json \
  --context-json creative_context.json \
  --output creative_controls.json
```

Add `--overrides-json creative_overrides.json` when applicable. Before writing the baseline, read `authoring_brief` together with the shared `definitions.principle` in the saved snapshot. Each `definition` explains the control's concept and scope; `levels` and `choice_descriptions` explain the selected setting, and `principle` holds shared application rules. For `sensual`, `fetish`, `surreal`, and `creativity`, the brief pairs each actual effective value with its 0–3 range, short meaning and selected level description. For `adult_appeal_emphasis`, it includes the selected value, allowed choices, meaning, selected-choice description, effective result and resolution reason. The resolver both returns this brief and saves it inside the hash-bound `creative_controls.json` snapshot. Copy `canonical_sha256` into the core's `creative_controls_sha256`. Resolve values once; the same frozen snapshot goes to the generator. A changed setting requires rebuilding both. The versioned snapshot embeds its definition and establishes input binding, not independent proof of authoring order. Previous parameter names and the former fractional creativity scale are unsupported.

Use active `sensual`, `fetish`, their emphasis, and `creativity` to shape the whole photograph from the first authorial decision. Sensual concerns human attraction and desire; fetish concerns sexual attraction or arousal focused on elements carrying special erotic significance. Use their full short definitions in the brief; neither is confined to fashion or editorial treatment. The two may share one expressive choice. Their levels describe prominence: zero adds no treatment, one supports subtly, two reads clearly, three leads the image's appeal and direction. Everyday or intimate expression can lead at three; overt expression is available, not mandatory. Preserve explicit content at zero. Realize the chosen scene in the image prompt rather than appending these definitions. Do not introduce covering garments or extra linings as hidden defaults.

Require the literal word `adult` in a subject phrase only when the effective `sensual` intensity is 2 or 3. At `sensual` 0 or 1, omit this boilerplate unless it serves requester meaning; an active `fetish` axis alone does not require the word. Preserve requester-owned age and applicable character-response meaning. When the word is required, bind its literal final-prompt phrase through `adult_appeal_brief.adult_subject_phrase`; otherwise that field may be omitted, and any supplied phrase must remain literal.

Use the saved `creativity` level and resolved `adult_appeal_emphasis` from the first authorial decision. Creativity's default is 1. Its frozen level governs both independent interpretation and later candidate-informed reconstruction: necessary changes at 0, restrained local variation at 1, active reorganization at 2, and whole-photograph reconstruction at 3. This authoring guidance changes no requester lock or source condition, adds no adoption quota, and leaves the existing creativity-dependent retrieval limits unchanged. The emphasis resolution records which active axis leads, or that no emphasis is active. These choices remain agent-owned and do not create requester locks.

Consider reference-use scope, intended viewer experience and use, and any active surreal/trend treatment at this same stage. Use the saved `surreal` meaning and selected level from the first authorial decision. This one integer replaces the former mode, probability and intensity settings; it has no probabilistic activation. The retrieved candidate breadth is not a perceptual measurement or a required detail count. Optional review toggles do not switch off artistic judgment or explicit request meaning. Keep staging register and scene information density in the existing intent explanation when useful, without adding new required sliders. Prompt length, retrieval weights, candidate budgets and surface `artistic_final_touch` remain later/internal concerns.

Settings and agent staging are separate from requester text: do not insert their prose into `source_request`, user definitions, exclusions or requester-owned anchors. Use the baseline and `interpreted_intent` to realize them coherently. No new decision-count or styling checklist is required.

Keep raw request bytes and active spans intact. Explicit `name=value` or `name:value` settings are covered by matching overrides in the bound snapshot, not visual anchors or interpretation-provenance rows. A pure setting span needs no garment/action evidence. If a span mixes settings with visual instructions, source each remaining visual fragment separately; all still require normal coverage. Prefer separate spans for settings and visual requests. An agent-chosen realization of a value remains editable and cannot become a requester lock merely because it expresses that value.

## Phase 1 — Write and Freeze the Basic Prompt

### Primary authorial direction

Apply this authoring procedure to every request handled by this skill, using its complete contextual meaning. Its applicability is independent of particular words, mood labels, language, paraphrase, or the presence of standalone keywords. Scale interpretation and exploration by requester-prescribed meanings, remaining open choices, and the resolved creative controls. Every creativity level retains authorial judgment; the level controls interpretive distance and exploration depth.

Before consulting the neutral catalog or specifying mechanics, decide what makes this particular photograph worth looking at and what the viewer should experience. Interpret subjects, actions, relationships, styles, impressions, and their combinations in context; preserve explicitly requested and semantically necessary properties. Use the request, permitted reference cues, resolved creative controls, and independent visual judgment to choose a coherent whole-image idea. Let that idea shape open choices of form, arrangement, material, environment, photographic treatment and, when relevant, clothing or gesture. Keep optional realizations open instead of treating a familiar visual bundle as the default meaning. A precise request may already supply the direction; preserve it without inventing extra freedom.

When meaningful expressive choices remain open, briefly compare coherent realizations of the same requested meaning using only the permitted pre-core inputs, all at the requested control strengths. If the obvious first realization relies on familiar shorthand, consider a qualitatively different realization. Compare the initial direction by the same relevant criteria as alternatives: subject presence, the force of form, moment or relationship, sensory rhythm, expressive coherence, and required legibility. A cosmetic substitution alone need not constitute a different idea. Familiarity is neither a requirement nor a defect. Choose what serves this photograph, keeping the comparison lightweight without a fixed element menu, a proposal quota, or access to earlier outputs. Let precise static requests retain their intended staging while developing open choices suited to their photographic purpose. Summarize the material direction in `interpreted_intent`; these agent choices create no requester-owned locks.

For a person-centered image, make the portrayal convey the person's distinctive appeal and presence in the requested situation. Expression, bearing, gesture, clothing, light, material, and the relationship with the surroundings can contribute when relevant. Choose camera distance and framing to serve that appeal. Preserve requested reference appearance rather than reshaping facial features to fit a generic ideal. For a non-person subject, apply the same attention to the subject's visual character without inventing a person.

### Develop the scene before drafting

For a request that carries a situation, action, relationship, or feeling, compose a particular scene rather than a brief illustration of its label. Work out the circumstances that brought the subjects here, what they are trying to obtain, protect, refuse, finish, or understand when relevant, what makes that difficult, and why this encounter or state matters now. Connect the relevant preceding condition, the action or choice at the shutter, its already-visible effects, and what remains possible afterward. Scale this development to the actual request and creative controls, preserving the requested action intensity and staging. For non-person subjects, develop applicable circumstances and changes without inventing a human protagonist.

Give the viewer enough context to understand the situation and a concrete reason to care about its outcome. Emotional credibility comes from the subjects' particular circumstances and the fit between action, response, relationship, and surroundings. Connect the subjects' purposes, actions, responses, relationships, and surroundings so their relevance is readable in the photograph. Develop the connections sufficiently instead of reducing them to one generic gesture and a reaction adjective. Interpretive space may remain around motive or outcome while the central situation remains readable. Fictional circumstances are authorial choices; a reference person's actual biography or inner life is not established by their appearance.

Keep a compact scene synopsis in the existing `interpreted_intent`, distinguishing requester meaning from invented circumstances, and put the frame's carrying relationships in `visual_priorities`. These records may explain the scene beyond the shutter; the photographic prompt must realize the useful context through present actions, responses, space, and sensory detail. A concise causal sentence may orient those visible details, but an unseen backstory alone cannot make the photograph understandable. Use connected prose with the specificity and rhythm of a worked scene. This development uses only permitted pre-core inputs and creates no extra schema, detail quota, requester lock, or automatic `character_response` trigger.

For person-centered photography, briefly establish a theme through these questions before choosing camera mechanics:

- **WHO:** What is this particular subject doing or trying to do, what circumstances shape the response, and how do presence, expression, behavior, or presentation reveal that?
- **WHERE:** How does this particular place enable, constrain, or give meaning to the requested action, role, atmosphere, or relationship?
- **HOW:** From what viewer position and psychological distance is the subject seen, and how is the camera acknowledged when relevant?
- **WHY NOW:** What brought the scene to this visible state, what is being decided or changing, and why does that matter to the subjects? Where transition serves the request, connect the preceding condition, the present response, and an emerging next possibility; a requested still pose remains a valid moment.

Consider SIR—symbolicity, individuality, and relationship—as complementary lenses for the frame. Use relevant visible cues for social or situational meaning, particular presence, and the camera-subject relationship, with emphasis suited to the request. These are choices within the authored photograph, not a fixed axis count or a reason to add biography, props, facial differences, or another person. Reference appearance alone establishes no actual personality, memory, preference, or desired self-presentation.

Choose the action, expression, interaction, or detail that carries the photograph's meaning, then include the surrounding context needed to read it. Derive distance, crop, lens, and light from that purpose while preserving requested framing and consequential contact. Keep emotional interest and formal restraint distinct: restraint organizes attention and information rather than lowering the resolved creative-control strengths. Leave interpretive space when it serves the request without obscuring required evidence.

These questions are part of this pre-core procedure, using only the permitted inputs. Record material choices in the existing intent and priorities; they introduce no new fields, sliders, candidate count, individuality quota, score threshold, or requester-owned locks. Detailed methodology references remain post-core only.

Use the existing `interpreted_intent` to state the intended experience concisely, distinguishing your artistic choice from requester-specified meaning. Use `visual_priorities` for the few visible relationships that carry it, with a clear focal hierarchy. These planning aids create no additional locks: an authorial motif may be replaced within the request's open scope. Where they serve the request, sensory specificity, emotional tension, or selective ambiguity should come from the scene rather than praise adjectives or unrelated embellishments. Formal staging and clarity can themselves be the intended artistic effect.

Then select the observation categories below and author a coherent 48–1,280 word English photographic prompt that can stand alone. Treat 720 words as the default recommended maximum, not a hard cap or a target. Scene development, situational clarity, emotional credibility, requester meaning, or literal hard evidence may justify exceeding that recommendation; never pad toward the limit. A precise or intentionally sparse photograph may remain short. It must already specify a concrete subject, setting, visible event or state, and two to six distinct visual priorities. Give the scene and its consequential details the space they need, with photographic technique serving their presentation. Write connected photographic prose with an artistic point of view, not a search query, tag bag, or placeholder.

Read the exact neutral catalog named above. Review its category names and choose five to ten distinct categories to develop for this request; count categories already specified by the requester. The catalog supplies no visual examples; its category names do not prescribe the visual choices made for the request. Start with the event, subject, setting, and visible consequence; unless the requester asked for photographic technique, do not let technique categories dominate the selection. A sparse or precise request still gets five meaningful observation axes by counting what it already specifies and making only restrained choices in genuinely open photographic dimensions. More than ten requester-specified axes never lose their instructions merely because only five to ten categories are selected for focused development. Do not count overlapping categories twice for the same visual decision.

Select only features that distinguish the request's meaning, make its event, relationships, or consequential physical or spatial arrangements legible in one frame, or support a visual hierarchy suited to the request's purpose. When relevant, express an abstract situation, affect, or implied prior context through connected actions, directed attention, and visible responses present in that frame. Develop mutually supporting cues that reveal why the action occurs and why the response fits these circumstances. Integrate them into one inhabited scene instead of filling a feature checklist; omit irrelevant prompt detail without closing genuinely open dimensions in `intent_lock`. The five to ten selected categories are not the core's two to six `visual_priorities`: each priority should be one coherent visible proposition, not a concatenation of category names or camera tags. Other selected categories may appear only in the baseline prose. Do not record incidental agent-chosen staging as a requester definition or exclusion, a resolution of a request term in `interpretation_provenance`, or an independent semantic assertion; keep required evidence phrases limited to the visible meaning they prove, excluding incidental detail from open dimensions. A category selection never creates a locked dimension, anchor, assertion, or `photo-visual-intent/v1`, nor does it remove an open dimension; every requester-specified dimension still follows the existing lock rules. A catalog category alone is never a source for `user_definitions`, `interpretation_provenance`, `semantic_assertions`, or `photo-visual-intent/v1`. Showing affect or a visible response this way does not itself activate `character_response`; follow the requester-meaning trigger below.

Count meaningful axes already present in the authored scene; the category count does not justify adding props, expressions, gestures, or technical clauses. Keep the dominant impression clear and let supporting details remain subordinate. Before freezing, remove optional detail that makes the subject demonstrate instructions rather than inhabit the intended moment.

For a requested interaction, state change, or component relationship, distinguish the participants, target or affected property, relevant starting state, action, visible result, and continuity where those roles exist. Connect requester-owned relations to literal evidence in the existing anchors and assertions. Check which roles each phrase actually proves; a general scene description cannot stand in for every endpoint. A static arrangement needs no invented action, history, or additional participant.

Before freezing, read the baseline as if the source keywords and scene synopsis were unavailable. Check what situation a viewer could infer, what makes the subjects' action or response understandable, and which visible connections carry the moment's significance. If the draft only names an emotion or shows an isolated gesture whose reason is missing, develop the authorial circumstances and their visible realization before retrieval. Literal evidence coverage and a longer prompt do not by themselves establish an engaging scene. This is an artistic review within existing intent and priorities, not a new machine-verifiable gate.

Before freezing, plan the visibility of the photograph's consequential relations using only the permitted pre-core inputs. Identify the owners, connecting boundaries and distinguishing state that must read together at the shutter. Account for their projected size, contrast and depth as well as occlusion: extra prose does not give a small detail more pixels. Choose one coherent observable state for an action or fastening, with the acting grip and target contact connected when they carry the meaning. Revise unbound placement, framing or timing when simultaneous details compete for the same view; preserve requested relations and reference scope. Keep incidental authorial mechanics out of requester-owned evidence. Record material reasoning in the existing intent, priorities and applicable review reasons; this adds no schema, fixed crop, detail quota or universal pixel threshold.

Before freezing that draft, review any material bodily action, contact, load-bearing state, or consequentially hidden appendage using only the permitted pre-core inputs. Trace the acting body part to its owner, its connected articulation and target, the supporting surfaces and available space, and what the chosen viewpoint will reveal. Distinguish actor-relative directions from screen directions. Check simultaneous states together; a plausible action label does not establish a plausible way to perform it.

Resolve contradictions and consequentially unspecified geometry in agent-authored staging before freezing. Add only the positive spatial relations needed to make that particular action legible. Preserve the requested interaction, affect, bodily structure, and intentional departures from ordinary realism; do not remove contact, hide the affected part, prescribe universal angles or handedness, or simplify every unusual pose. Do not turn the review into requester-owned exclusions or assertions. Foreshortening, occlusion, clothing, atypical anatomy, and a requested nonhuman structure are reasons to examine the applicable body model, not automatic failures. Ask only when requester meaning remains unresolved, not for routine staging choices.

Keep the full physical explanation in the review record. Include a spatial relation in the photographic prompt when it materially establishes the action or prevents a concrete contradiction. Necessary contact evidence remains explicit. Ordinary support outside the frame can be accounted for in the review; it need not be brought into view merely to demonstrate that review. Choose framing for the photograph's central relationship and subject presence, making only consequential bodily relations assessable.

Freeze a separate `embodiment_review.json` with the corrected baseline. Use single-space whitespace in `baseline_prompt_en` before hashing, matching the core's canonical whitespace form. It is agent-owned review evidence and must not enter semantic retrieval. This neutral wire shape is available pre-core; its explanations and literal phrases come from the current draft, not project examples:

```json
{
  "contract_version": "photo-embodiment-review/v1",
  "provenance": "agent_prepack",
  "prompt_sha256": "<SHA-256 of exact final baseline_prompt_en UTF-8 bytes>",
  "scope": "body_action",
  "summary": "<applicable body model and material physical interaction>",
  "checks": {
    "body_ownership": {"status": "supported", "reason": "<reason>", "prompt_evidence": ["<literal phrase>"]},
    "joint_chain_and_reach": {"status": "supported", "reason": "<reason>", "prompt_evidence": ["<literal phrase>"]},
    "support_and_balance": {"status": "supported", "reason": "<reason>", "prompt_evidence": ["<literal phrase>"]},
    "contact_and_space": {"status": "supported", "reason": "<reason>", "prompt_evidence": ["<literal phrase>"]},
    "visibility_and_projection": {"status": "supported", "reason": "<reason>", "prompt_evidence": ["<literal phrase>"]}
  }
}
```

Each explanation is concrete; each applicable check cites one to four literal phrases of at least three words. Use `not_applicable` with a reason and empty evidence for an irrelevant check. An intentional departure uses `requester_intended` plus `requester_source_text` copied exactly from an active requester span; it is not permission to erase that departure. `needs_revision` and `unresolved` block the reviewed version until addressed. For a scene without a material bodily mechanism, use `scope: not_applicable`, explain why, and set `checks: {}`. Do not fabricate a bodily action to fill the record. `supported` means the agent found a plausible realization, not that a solver or rendered image verified it. Review timing is declared provenance, not independently proven by the hash.

First create one external `photo-request-envelope/v1` from the actual requester message. `request_text` is the complete, byte-exact user text, never an agent summary. Active spans select the scene requirements and every governing visual or creative-control modifier. A single-topic request may use the whole request when it contains only those instructions. Keep output-delivery instructions in `request_text` and follow them as workflow requirements, but leave them outside visual active spans; they need no image evidence. For a multi-topic or multi-arm request, select the exact non-overlapping topic span plus every exact global modifier that governs that arm. Do not invent a cleaner per-arm request. Create and freeze this envelope before delegation so a downstream agent cannot relabel its own interpretation as user text. In delegated work, the coordinator creates the envelope and passes its path plus SHA-256 to the child; a task brief, coordinator safety summary, reviewer note, or subagent message is never requester text and must never be used to create or expand the envelope.

```json
{
  "contract_version": "photo-request-envelope/v1",
  "provenance": "requesting_user",
  "request_id": "<stable run-local request id>",
  "request_text": "<complete byte-exact requesting-user text>",
  "request_sha256": "<SHA-256 of exact UTF-8 request_text bytes>",
  "active_spans": [
    {"span_id": "<span ID>", "start": "<Unicode start index>", "end": "<exclusive Unicode end index>", "text": "<exact active substring>"}
  ]
}
```

Freeze it as:

```json
{
  "contract_version": "photo-authorial-core/v3",
  "provenance": "agent_prepack",
  "source_request": "<the complete byte-exact request_text from the envelope>",
  "creative_controls_sha256": "<canonical_sha256 from the frozen pre-core controls>",
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
    "contract_version": "photo-intent-lock/v2",
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
- Every active span needs both semantic-origin coverage (`user_definitions` or `interpretation_provenance`) and at least one intent anchor. Every fully locked dimension needs an anchor with substantive requester source text and its own distinct literal baseline evidence phrase. `concept`, `subject`, and `event` are always locked. Fully specified dimensions remain locked; for a partially specified dimension, use the property anchors below and leave its other choices open. Open and fully locked dimensions are disjoint. Current intent locks permit zero or one open dimension for precise requests or local repairs; write `open_dimensions: []` explicitly when none are open, and never invent freedom to satisfy a creativity quota.
- For a new core, review requester-owned camera direction and height separately. When camera is partially specified, leave `camera` open and record each prescribed axis in its own property anchor with `dimension: camera`, `target: camera`, and `property: viewpoint.direction` or `property: viewpoint.height`, bound to its literal English baseline evidence. Use separate anchors when both axes are prescribed; combined property paths do not provide equivalent overlap protection. An independently justified whole-camera lock keeps `camera` locked and uses whole-dimension camera anchors. A concept anchor alone does not supply camera ownership. Pass `--require-camera-evidence direction` and/or `--require-camera-evidence height` for those prescribed axes when generating the pack. The check runs before candidate DATA loads. Do not lock an unprescribed authorial camera choice merely to satisfy the check. Older frozen cores may use a conservative literal camera-clause query projection; this never creates missing locks or authorizes adoption on a locked viewpoint.
- `intent_lock.semantic_anchors` accepts 1–16 rows in total. Preserve every requester-owned constraint; if it cannot be represented faithfully within that limit, report the contract limitation instead of dropping constraints or broadening locks to fit.
- When `camera` is an existing open or locked dimension, every newly authored core also records one camera assertion in the existing neutral assertion shape. When camera is absent from both lists, omit that assertion: the dimension remains closed, including in zero-open/no-op cores. Never add camera freedom or a whole-camera lock to fill a review row. Explicit requester-axis checks above still apply, and any supplied declaration is always validated. Its axes are exactly `camera_axis_review: camera_axis_review_v1`, `capture_owner: camera` when an axis is requested (otherwise `unprescribed`), and separate `direction_requirement`/`height_requirement` values `requested`, `open`, or `excluded`. Use advisory polarity while camera is partially open; existing property anchors retain the requested hard duties. Use required polarity only for an independently justified whole-camera lock. For requested axes, evidence contains exactly `owner_phrase` naming the capture camera and `direction_phrase` and/or `height_phrase`; select literal baseline subphrases, at most 16 words for the owner and 24 for each axis. Each axis phrase must occur in its existing camera-target viewpoint anchor for partially specified camera, or in its whole-dimension camera anchor for an independently justified whole-camera lock. With no requested axes, evidence is empty; do not add camera prose to an unspecified scene. An excluded axis needs requester-grounded `user_exclusions` and receives no positive axis evidence. Cite the active requester span IDs normally. Pass `--new-author-camera-evidence` with the public generator. Review actual capture ownership, lens attachment and local negation yourself: these source/type/literal checks cannot prove your interpretation is correct. An older frozen core is replayed without this new-author flag and is never rewritten merely to obtain an assertion.
- Use only these v3 dimension names: `concept`, `subject`, `identity`, `count`, `age`, `role`, `species`, `appearance`, `pose`, `body_geometry`, `expression`, `action`, `event`, `setting`, `relationship`, `sexual_tone`, `style`, `reference_use`, `viewer_outcome`, `text`, `format`, `framing`, `composition`, `lighting`, `camera`, `color`, `material`, `timing`, `atmosphere`, `character_response`.
- Record requester-grounded existing owners, common role addresses and exact frozen facts through the neutral [frozen witness contract](precore/photo_semantic_witnesses.md). Author them before retrieval, with active spans and literal baseline evidence. A role address or human category does not establish anatomy, age or permission to change a locked property. Preserve actual owner equivalence, owned parts and separate actors; missing evidence remains missing after retrieval. The old `carrier_target`/`existing_carriers` shorthand does not qualify native v4 candidates.
- Put an actual requester definition or answer to a clarification question in `user_definitions`. Its `source_text` must equal a complete active span and cannot be only the term itself. A bare term is an agent interpretation, not proof that the requester supplied a definition.
- Use `interpretation_provenance` for material agent/context/web interpretations, not for requester-owned definitions. Web-based entries require at least one source URL; URLs do not enter the retrieval query.
- `unresolved_ambiguities` is mandatory and must be empty. If it is not empty, ask or research before continuing.
- `user_exclusions` contains only explicit requester negatives. Never use it to hide a requested concept, because exclusions are removed from semantic retrieval.
- Do not translate platform policy, an agent's comfort preference, a coordinator's risk summary, or a profile's conservative default into `user_exclusions`, `baseline_prompt_en`, or runtime negatives. Platform and image-tool enforcement remains active outside prompt semantics.
- If a source-grounded shorthand label should aid interpretation and profile activation but should not be sent to the image runtime, put it in `runtime_forbidden_labels` and express its intended visible components in anchors and the baseline. Runtime-only labels remain in retrieval; only their literal runtime spelling is forbidden.
- `semantic_assertions` is the typed input for downstream meaning. Required assertions affect locked dimensions; an exact native frozen fact may instead be protected by its existing requester property anchor on a partially open dimension. Advisory assertions affect open dimensions, and retrieval cannot resurrect exclusions. Every assertion cites active `source_span_ids`; every required evidence phrase is already literal in `baseline_prompt_en`.
- Hand off the resolved primary subject category through an optional required `subject` assertion with `axes.subject_category` set to one of `human`, `animal`, `object`, `food`, `plant`, `environment`, `sign`, or `unknown`. Bind it to the requester span and literal subject evidence before retrieval. Use the category of the actual primary subject rather than a category inferred from what it depicts; do not insert technical category aliases into the request or baseline. This type constrains retrieval and adds no detail obligation. Missing or `unknown` categories preserve conservative slot guards; the coarse creative-context value `nonhuman` does not establish `object`.
- Lock the requester-owned meaning at the narrowest sufficient level, preserving every explicit requirement and semantically necessary relation. The always-locked `concept`, `subject`, and `event` protect that meaning; they do not make every invented circumstance in their descriptive core fields mandatory. Keep replaceable staging outside anchors, required assertion evidence, definitions and term-resolution claims. A mood or relationship does not by itself require the particular stance, hand arrangement, smile, garment, or camera distance you chose to express it. Write the minimal coherent action-and-result phrase that proves the requested meaning, placing incidental styling or geometry outside that phrase. The same authorial choice must not be declared optional in the feature-selection record and included intact in mandatory evidence; do not relabel it as request-derived merely to avoid that check. Freezing the complete baseline preserves its independent provenance and comparison text, not a duty to retain its authorial staging. Creativity never opens an actually locked dimension or removes required literal evidence. Correct overbroad ownership before freeze; an already frozen binding changes only through the existing rebuild or scoped retry path.
- Treat a named character or relationship archetype whose meaning depends on behavior as a required visible `character_response`, even when the requester calls it a concept or also specifies a costume, role, facial expression, or prop. Lock `character_response` and make the baseline show a clearly identifiable actor, one identifiable relationship target or repeated marker of that same target, one concrete target-directed action, one affect leak, and one already-visible consequence in a single frame. This behavioral requirement does not prescribe age; preserve requester-owned age. An isolated label, appearance cue, or object alone never satisfies this contract; reference-image appearance never activates personality.
- Every required non-`character_response` assertion is compiled into `photo-semantic-assertion-obligations/v1`. When that block exists, copy its exact frozen evidence into `semantic_assertion_evidence.evidence.<assertion_id>`, bind `source_contract_sha256`, and keep every phrase literal in the final prompt. Retrieval cannot supply or replace any of those hard phrases.
- For a required visible character response, lock `character_response`, add its own semantic anchor, and write one `character_response` assertion with the generic axes `surface_affect`, `underlying_affiliation`, `relationship_target`, `primary_action`, `affect_leak_timing`, `affect_leak_channels`, and `event_phase`. Select exactly one primary leak channel. When the meaning depends on a relation rather than isolated attributes, encode bounded generic `relations` using `same_target`, `contrasts`, and/or `temporal_order`; do not leave the relation to a named label. Every relation member must be a declared generic axis or causal role, and every `same_target` relation must include `relationship_target`. For a named affection-control archetype, bind the affection surface or care, primary action, and immediate consequence to that same target; an affect leak may support this vector but cannot replace the consequence. Bind `actor_phrase`, `baseline_phrase`, `trigger_phrase`, `target_phrase`, `primary_action_phrase`, `affective_leak_phrase`, `visible_response_phrase`, `immediate_consequence_phrase`, and `continuity_phrase` to literal baseline text. Values are authored from the request; never route a named archetype to fixed gaze, face, pose, or story geometry.
- Make behavioral evidence sufficient and economical. Compatible evidence fields may share a clause when it actually proves both relations. Do not invent a second gesture or force a reassuring expression merely to fill a field; preserve ambiguity that belongs to the requested feeling while making the governing action and relationship legible.
- `request_lineage` is `null` for an initial request and stays unchanged for a same-input repeat of that run. On a revised-content child it hash-binds the parent request/core and separates preserved dimensions from the explicitly allowed changes; the two sets are non-empty and disjoint. Inspect only the parent fields allowed by the retry exception above before freezing the retry. If `concept` or `character_response` is preserved and the parent had a hard visual obligation, recreate that same obligation as a hash-bound post-core `photo-visual-intent/v1` sourced from an exact current frozen core field. Do not let an elliptical retry phrase demote a preserved hard obligation into an unselected embedding candidate, and do not carry the obligation when the requester changed or excluded the governing meaning.
- A fidelity complaint about a meaningful interactive prop is not permission to remove, relocate, conceal, or transfer it. On such a retry, use `photo-request-lineage/v2` and one object-agnostic `repair_targets` row. Freeze actor, object, interaction state, expected contact, protected locked dimensions, positive interaction and recognition phrases, and only the local repair axes that may change. Use `relation_origin: parent_preserved` when the parent relation remains intended and `relation_origin: requester_corrected` when the requester explicitly corrects an evasive parent relation. Bind both phrases through one required action assertion in the baseline. Decorative background objects and non-action-bearing ornaments do not need repair targets.
- Every multi-arm run shares the immutable raw requester text but freezes a separate, exact-span-bound envelope and core for each arm before any arm sees project-local data.

For a partial prescription, `photo-intent-lock/v2` permits a semantic anchor on an open dimension with additional `target` and `property` paths. Bind only the actual requester-prescribed properties; unrelated properties remain open. Use stable lowercase paths for the actual object and property; preserve their meaning across composition. Property anchors may share one economical evidence phrase. Keep complete reference-outfit preservation or a fully specified appearance as a whole-dimension lock. These anchors do not change the existing rules for required typed semantic assertions.

Preserve every property anchor's literal evidence and its meaning. Any authored or candidate change on a partially locked dimension needs `affected_properties` rows containing `dimension`, `target`, and `property`. Broad/unknown candidate effects cannot establish compatibility with a partial lock; reject the candidate or author an independent compatible detail. Changing a parent property includes its children. Do not evade a lock through an alias, another carrier or contradictory added prose. Declarations and literal evidence are mechanically checked; actual semantic consistency remains the agent's responsibility.

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

There are at most 64 assertions in total, 1–16 axes per assertion, at most 8 distinct values per axis, and at most 16 evidence fields. Required assertions have at least one evidence phrase, each with at least two content words. Values are strings or string lists; evidence values are strings. A required `character_response` uses the seven axes and nine evidence keys listed above, exactly one `primary_action`, and a one-item list for `affect_leak_channels`.

Only `character_response` may add `relations`, a list of 1–8 objects with exactly one of these shapes: `{"operator":"same_target","members":["<member>","relationship_target"]}`, `{"operator":"contrasts","left":"<member>","right":"<member>"}`, or `{"operator":"temporal_order","first":"<member>","then":"<member>"}`. Members are `actor`, `baseline`, `surface_affect`, `underlying_affiliation`, `relationship_target`, `target`, `primary_action`, `affect_leak`, `affect_leak_timing`, `trigger`, `visible_response`, `immediate_consequence`, `continuity`, or `event_phase`. Use distinct members and no duplicate relations. Non-character assertions omit `relations`; they may describe their observable relations through authored axes and literal evidence.

### Negative-intent firewall

Write `baseline_prompt_en` as positive visual realization. Do not embed instruction-shaped blanket negatives such as `No X, Y, or Z`, `Do not ...`, `Avoid ...`, `Exclude ...`. These clauses can silently delete the requested relationship, action, emotion, prop, person count, wardrobe, or genre signal. The modern core normalizer rejects them before the core can be frozen.

Use three separate lanes:

- A semantic exclusion is valid only when the requester explicitly supplied it and it is grounded in an active request span. Keep it in `user_exclusions`; after removing a literal directive prefix, a runtime-negative item must equal the complete exclusion. Do not split a combined exclusion or broaden it by substring, synonym, or category inference.
- Automatic `negative_en` is limited to a narrow intent-neutral photographic-defect vocabulary. Generic safety, taste, count, contact, action, relationship, expression, wardrobe, and genre suppressions are removed. Identity-preservation negatives are allowed only when identity-reference preservation is explicitly enabled.
- Platform or image-tool policy is enforced by the platform/tool and by post-render review. It is not serialized as a blanket runtime negative. When a permitted scene needs a local boundary, describe its actual visible state and required relation positively.

The pack exposes a hash-bound `photo-negative-intent-guard/v1` containing the emitted negative terms and governing policy. It is recomputed during composed audit. This guard applies to both the positive prompt surface and `negative_en`; copying the pack negative bytes is necessary but no longer sufficient.

### Record the pre-core feature selection

Keep one `precore_feature_selection.json` beside the envelope and core for each request arm. Choose the categories before drafting, then finish this record using the final, canonically spaced `baseline_prompt_en` and frozen envelope. Each selected category needs a distinct reason and a literal baseline phrase showing how it was used. `basis` is `explicit_request` for an exact requester span, `request_derived` for a visible realization derived from a cited active span, or `agent_visual_choice` for a decision within an open dimension. For `explicit_request`, fill `source_span_ids` and `source_text` with an exact substring of an active span, and set `derivation` to `null`. For `request_derived`, fill `source_span_ids` and `derivation`, and set `source_text` to `null`. For `agent_visual_choice`, set `source_span_ids` to `[]` and both `source_text` and `derivation` to `null`. These labels describe the recorded realization, not the category's permanent authority.

```json
{
  "contract_version": "photo-precore-feature-selection/v1",
  "request_id": "<envelope request_id>",
  "active_span_ids": ["<this arm's active envelope span ID>"],
  "catalog_path": "skills/photo-prompt-image-generator/precore/visual_feature_catalog.json",
  "catalog_schema_version": "photo-precore-feature-catalog/v2",
  "catalog_sha256": "<SHA-256 of exact catalog file bytes>",
  "request_sha256": "<envelope request_sha256>",
  "baseline_prompt_sha256": "<SHA-256 of final canonical baseline_prompt_en UTF-8 bytes>",
  "selected": [
    {
      "category_id": "<selected category ID>",
      "basis": "explicit_request",
      "source_span_ids": ["topic"],
      "source_text": "<exact requester substring inside topic>",
      "derivation": null,
      "reason": "<why this category matters to the image>",
      "baseline_evidence": "<literal phrase in canonical baseline_prompt_en>"
    }
  ]
}
```

The row template specifies fields, not a default category or a complete five-to-ten selection. The selection record is audit evidence only: do not put it in the core, retrieval query, candidate pack, semantic assertion, or runtime prompt. Copy the exact catalog bytes beside the run artifacts for later historical review; never use a prior run's copy to write a new core. After freezing the core, and **before** any candidate or profile access, validate the record:

```bash
cp skills/photo-prompt-image-generator/precore/visual_feature_catalog.json visual_feature_catalog.snapshot.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_precore_feature_selection.py \
  --catalog skills/photo-prompt-image-generator/precore/visual_feature_catalog.json \
  --request-envelope request_envelope.json \
  --authorial-core authorial_core.json \
  --embodiment-review embodiment_review.json \
  --selection precore_feature_selection.json
```

If validation fails, correct the record or rebuild the affected pre-core artifacts before opening candidate data. An `agent_visual_choice` phrase included intact in a mandatory anchor, definition, or required assertion is an ownership conflict: narrow the mandatory evidence or correct its provenance from the actual request, rather than relabeling the choice to pass. Inspect `warnings` even when the command succeeds: revise repeated reasons or evidence, and review any delivery-and-technique majority against the request before proceeding. The group-majority warning is a review cue, not an automatic rejection of a justified composition choice. Any baseline change also invalidates the embodiment-review hash, core, derived intent-lock binding, and selection hash. Live runs use the current example-free V2 catalog. Use `--historical-catalog` only to verify an archived record against its exact saved snapshot; legacy V1 catalogs remain valid only for historical verification. Managed revalidation of an already frozen run uses its hash-bound snapshot without rewriting its records. It confirms structure and literal binding; it cannot prove that selection preceded drafting or that the resulting image is good.

Freeze the envelope and authorial core through the managed precore entrypoint before retrieval. Their exact normalized hashes and active spans bind the material plan, core validation context, composition and runtime.

## Phase 2 — Retrieve After the Core Is Frozen

Only after freeze, prepare the neutral slot material and directly author what each slot should express. Read [installed H-only+F2](references/installed-h-f2.md) for the row shape and execution. Do not load candidates before writing and sealing the expression plan.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py prepare-slot-intents --run RUN
# Write authored-intents.json with the overall intent and one reviewed row per requested slot.
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_photo_slot_intents.py --run RUN --authored authored-intents.json --output slot-plan.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py seal-slot-intents --run RUN --plan slot-plan.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py retrieve --run RUN
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py view --run RUN
```

The ordinary `retrieve` command selects the installed, sealed H-only+F2 release without a policy, generation or store flag. It preserves the independent search for every slot row marked `search` and adds two independent whole-scene searches: the active requester topic and the frozen `baseline_prompt_en`. Each query searches the entire existing positive common pool through one BM25F lane and one local embedding/cosine lane using identical text. The topic query uses only this arm's frozen active request spans, removing creative-control assignments and applying the existing explicit-exclusion firewall; delivery text and inactive arms are outside its scope. The baseline query uses the complete frozen baseline through the same positive-text firewall. Slot tags, context eligibility and native admission do not prefilter material search. F2 preserves meaning and original lookup cues with global field statistics; RRF10 combines the two lanes per actual realization, then deduplicates by candidate and returns a separate creativity-bounded sample for every query. There is no reranker, Gemini fallback or automatic data rebuild. `not_applicable` and `unresolved` slot rows perform no slot search; the two whole-scene searches still run.

Write role focus and scene context from the intended photograph and the slot's expressive purpose, including the relevant target, action, relation and conditions. Do not copy the full baseline into every query. Candidate-free role definitions help delimit the purpose; they do not create facts or permissions. The plan binds the exact frozen core, controls and neutral catalog. A missing plan requests authoring; it never substitutes an automatically generated query.

The installed release owns its code, canonical candidate snapshot, F2 index and verified document vectors. It reads no research checkout or experiment output at runtime. `retrieval-runtime.json` selects that installed release; the existing native `CURRENT` stays unchanged. Missing or altered release files block execution rather than fall back to an older search. Existing bound native runs retain their original receipt path. See the installed reference for maintenance and data freshness.

The material view exposes complete source meaning, conditions and effects, separately from the core validation context. `query_scopes` distinguishes slot results from `__request_topic__` and `__baseline_prompt__`; review the whole-scene results alongside slot results against the frozen photograph. These search IDs are not new slots or adoption permissions. Use `view --candidate-id CID` for full source detail or `view --material-page N` for further pages of at most64 unique sources. Paging, repeat retrieve, resume and composition verification reuse issued evidence and perform no extra search. Every query keeps its own creativity-bounded sample; the reading page budget does not discard another query's results.

Review the candidate's whole meaning against the frozen requester intent before using it. `native_approval: false` means the result grants no whole-source adoption authority. For new compositions, review every distinct returned material source and record each returned query/CID/RID occurrence in `h_f2_material_decisions` with its exact source hash, `use: inspiration_only|skip`, and a candidate-specific rationale under the [comparison and decision procedure](references/composition-contract.md#candidate-informed-alternatives-and-comparison). Repeated sources may share one detailed review referenced by their query-specific rows. Compatible authorial ideas must still respect complete source constraints and requester locks; a distinctive whole cue cannot evade its native adoption contract by being renamed inspiration. Do not insert H-F2 result IDs into native chosen lists. Selecting no material is valid after the comparison or an evidenced finding that no distinct compatible alternative is available.

New H-F2 runs compile a core validation context directly, preserving mandatory meanings, profile duties, negative policy and final composition auditing without creating a native candidate pack or running a separate creative-augmentation sampler. Each query retains the first eligible CID-deduplicated source after source-scope projection and draws the remaining material uniformly without replacement from the same creativity-bounded rank window: 0 uses 8/4, 1 uses 32/8, 2 uses 96/12, and 3 uses 256/16 (window/total sample limit, including the one rank anchor). The anchor is generic: never inspect candidate identity, recency or topic to promote a source. The seed, anchor and diversity evidence are saved and replayable; resume never resamples. A user-authorized sampling-policy repair requires a new sealed generation and a new run preserving the exact previously frozen meaning; retain all pre-fix evidence. Historical runs retain their original format and sealed implementation. Keep the exact bindings and compose through `photo_workflow.py compose-audit`. Material discovery never supplies a hard assertion, required owner, prerequisite or render permission. All source conditions, complete adopted contracts and frozen requester evidence remain binding. Read [composition-contract.md](references/composition-contract.md) for those duties.

### Optional post-core visual intent

For an exact, non-substitutable requester definition or a preserved parent hard obligation, read `references/retrieval-contract.md` and construct `photo-visual-intent/v1` only after the core is frozen. Its evidence must already belong to the requester definition or one exact frozen core field. Exact resolution may bind a hard profile; approximate retrieval remains optional. Do not construct visual intent merely because a candidate offers an attractive interpretation.

Before rendering, when the requester explicitly makes a perceptual effect focal, cover that meaning with a required typed assertion or an active hard visual obligation. A broad label, an embedding hit, or an optional candidate is not coverage. If the focal meaning is still uncovered, rebuild from the clear requester meaning; ask only if that meaning is still ambiguous. Record this focal-coverage check separately from prompt, runtime, and pixel status.

## Phase 3 — Clarify and Refine the Authored Photograph

Read `references/composition-contract.md` for the composed shape and active conditional fields. Develop the independently authored photograph from Phase 1 at the frozen creativity level, following [creativity and reconstruction](references/composition-contract.md#creativity-and-reconstruction). Before selecting the final prompt, follow [candidate-informed alternatives and comparison](references/composition-contract.md#candidate-informed-alternatives-and-comparison): write concrete, complete alternatives for distinct compatible candidate changes, then compare those alternatives and the baseline on equal terms. Use the same relevant artistic criteria from Phase 1, including situational clarity, connected causes and responses, emotional credibility, whole-image direction, visual hierarchy, and the requested degree of reinterpretation. Candidate or profile term matches provide semantic assistance and never determine whether this common authoring procedure applies. The final pass may retain, clarify, remove, or replace agent-authored detail on open dimensions; at high creativity it actively explores a new whole-image realization rather than limiting candidates to additions or repairs. Appearing in the first draft gives an authorial motif no protection. Preserve requester-owned meaning and complete adopted contracts. Make artistic refinements during composition before the bounded semantic self-review below; absence of a semantic contradiction alone does not settle the artistic choice. Selecting the baseline remains valid after the level-matched comparison; an unchosen alternative creates no candidate-adoption or final-detail quota.

Before choosing, read the exact active requester text, definitions/exclusions, ownership of whole-dimension and property locks, the baseline, and each considered candidate's full source detail. Use the compact view for navigation, not as permission inferred from a slot name, rank, or summary. Judge what the candidate would actually add across the whole frame, including implicit people, apparatus, relationships, and effects outside its named slot. Follow the model-guided candidate review in `references/composition-contract.md`: adopt the complete compatible meaning, use only independently justified generic attributes as an authorial choice, or decline. These are reasoning outcomes, not new wire-format decision values. Required meanings and atomic/conditional candidate contracts remain binding; do not relabel a distinctive candidate realization as authorial to evade them.

If an adopted source requires an explicitly selected existing owner, choose the actual compatible entity already grounded in the frozen core and record `owner_selections` in the composed object as described in [composition-contract.md](references/composition-contract.md#explicit-existing-owner-selection). Satisfy every material, anatomy and other prerequisite on that entity. Keep the public pack and core unchanged. A missing compatible owner leaves that optional candidate unselected; a role label, a sole available object or an owner name does not supply the choice or its prerequisites.

Also satisfy the source's conditions between the actual selected owners, including part ownership, distinctness and exact frozen relationships. Read [conditions on the selected source owners](references/composition-contract.md#conditions-on-the-selected-source-owners); review-only unresolved choices require resolution before adoption, and an actual failed relationship makes that candidate ineligible.

Consider how a candidate could realize the requester meaning at the selected creativity level, from a necessary clarification to a substantially different arrangement of open choices. Examine cause, purpose, relationship, response, consequence and sense of place in the proposed complete photograph. Compatible implications may deepen the current moment or support a different authorial realization; connect the selected circumstances coherently rather than requiring every candidate to justify itself as an addition to the old scene. Independently authored refinements may also strengthen the scene within open scope. Review the resulting situation as a whole; a candidate's relevance, exposure, or successful audit does not prove that the viewer will understand it or care about its outcome. Record material scene developments, replacements or subtractions and their reasons in the existing `authorial_decisions`. An optional story detail remains authorial even when it is important to the photograph; preserve the narrow requester-owned evidence and complete adopted contracts.

Apply that semantic and applicability review across all subjects, languages, paraphrases, compound descriptions, and requests without standalone labels. Its scope follows the request's meaning and the candidate's complete effects, independent of a keyword list or profile match. Distinguish meaning compatibility, realizable prerequisites and allowed changes, then artistic preference. Record candidate-specific source meaning, concrete prompt effects or conflicts, and the comparative reason in existing decision fields and the run's `composition-comparison.md`; a compatible but less useful option is not semantically invalid. A blanket statement that the baseline is sufficient, or the count of rejected candidates, does not replace that review.

When the requester asks for the photographic methodology, or a scene would benefit from clearer causal or emotional context, relationship, moment, individuality, or meaning-led framing, read the relevant sections of this skill's internal [photographic-methodology.md](references/photographic-methodology.md). It contains the integrated scene development, theme, SIR, psychological-distance, framing, camera, and review guidance. Apply useful refinements within the existing open dimensions and property locks, recording material changes in the existing `authorial_decisions`; retain the baseline when the candidate comparison supports that choice. This skill owns the methodology, final prompt, pack-approved negative, audit, and render.

When `adult_appeal.dimension_scope` is present, read the adult-axis section of `references/hybrid-augmentation-contract.md`. Those two axes may use their declared unlocked dimensions even if omitted from `open_dimensions`; preserve every locked meaning and record the dimensions actually changed in `adult_appeal_brief`. This scoped exception does not open dimensions for unrelated creative additions or revise the core.

When `adult_appeal.contextual_retrieval` is present, use [contextual appeal](references/contextual-appeal.md). Its expression shortlist is visible independently of the general creative sample. Interpret these candidates in the current scene and compare viable alternatives with the baseline at the same strengths; retain either on artistic grounds. Record a concise review in the existing adult brief. Candidate adoption remains optional, and the final prompt contains only the selected direction.

Both axes can use compatible choices throughout the scene while preserving property anchors. Role, setting, relationship and timing changes require those dimensions to be explicitly open. If an axis is already expressed in the baseline, use `realization: baseline`, retain literal baseline evidence, and set `affected_dimensions: []`; no new detail is required. For a refinement, use `realization: refined` and declare actual changes, including `affected_properties` on partially locked dimensions. Assess whether the intended direction is readable in context; a generic material word or valid intensity number alone does not establish that. Explain a constrained realization in the existing artistic interpretation instead of claiming visual success.

Reconsider the whole frame before polishing clauses. Read the final scene without the source keywords or candidate labels and judge whether the situation, its connected responses, and a reason to care remain legible. Compare each viable realization by the requested meaning, subject appeal and whole-image effect; losing an agent-chosen motif can be a worthwhile trade when the alternative establishes a stronger relationship. If a chosen pose, distance, expression, or prop arrangement weakens the intended experience, revise the unbound staging while preserving every requester-owned anchor and effective hard obligation. Preserve context that gives the action its significance; simplification should remove distraction rather than the links that make the moment understandable. Record material refinements in the existing `authorial_decisions`, including scene development, subtraction or simplification. Do not change the frozen core in place or silently rewrite required evidence. If a needed change would alter a frozen anchor or assertion, rebuild through the existing request/core path; use clear existing user intent without another approval request.

After considering the complete adopted contracts, check whether their evidence can coexist in the chosen photograph. Trace each required owner, endpoint and state in one planned view at its required review scale; distinguish a local visible connection from a complete route or endpoint count. Develop feasible unbound staging before polishing the wording. Decline an optional addition before adoption when it defeats the scene or cannot be made legible within scope. A preserved or already adopted hard duty remains complete: do not remove a component, demote a review, hide an endpoint or replace a difficult mechanism with its general impression. Use the existing rebuild or scoped retry path when necessary. Keep this planning in current authorial decisions and review reasons rather than adding a parallel qualification checklist.

When `embodiment_preflight` is present, read `references/embodiment-preflight.md`. Recheck the entire final prompt, including new camera, framing, clothing, and contact clauses; preserve the baseline review and bind a fresh `agent_postcomposition` review in `embodiment_review`. A changed prompt invalidates the previous review hash. Fix composition conflicts through unbound staging on open dimensions. Use the existing rebuild or repair lineage when required frozen evidence must change. General defect negatives cannot substitute for a coherent positive realization.

For every semantic clarification, record exactly one decision:

- Apply a fitting clarification and bind literal prompt evidence.
- Reject a context-mismatched or gated clarification.

Never supersede a v3 core or requester definition. Reject optional candidates that suggest a different meaning and continue with the frozen core. If an actual requester ambiguity or a conflict in required evidence prevents faithful composition, stop that run and resolve it before rebuilding the envelope, core, and pack. A clear requester correction already authorizes that rebuild.

For creative candidates, decide each as `transformed` or `rejected`. Rejecting all is valid. Transform at most three, declare `affected_dimensions`, keep them within `intent_lock.open_dimensions` or the adult-axis scope above for a scoped adult candidate, and add a new relation, cause, material behavior, framing, light, omission, or timing decision instead of copying source terms.

Bind the exact pack ID, negative, core hash, intent-lock hash, anchor IDs, preserved evidence, candidate choices, all clarification decisions, and creative decisions in the composed object. Set `composer` to `agent`.

Preserve every anchor's literal evidence and all required assertion/profile evidence, and keep requester exclusions and runtime-only labels absent. Core validation contexts and native V10 packs expose `photo-authorial-authorship-policy/v2`: no additional baseline-phrase quota or final-decision quota is imposed. Use `preserved_evidence: []` unless extra literal preservation is intentionally needed, and `authorial_decisions: []` when no material refinement is needed. Any recorded decision must be substantive and use a distinct open dimension; any extra preserved phrase must occur in both prompts. Never add detail to fill a quota in a new run.

Keep `prompt_en` within 48–1,280 English words, with 720 as the default recommended maximum. The evidence-adjusted advisory ceiling is the larger of 720 or hard-evidence words plus 320, capped at 1,280; exceeding either advisory ceiling produces a warning. Scene development, situational clarity, and emotional credibility may justify a longer prompt within the absolute bound. Review redundancy rather than automatically cutting context: remove unrelated decoration, repeated explanation, or excess technique before the details that make the scene readable, and preserve requester meaning, literal evidence, and adopted contracts. Compatible evidence may share a natural clause. Length is capacity, not a detail quota or proof of quality. The final result must read as one coherent photograph. Requester meaning outranks generic character, moe, viewer, style, and creative defaults. Preserve only the guard-approved pack `negative_en`, and keep blanket negative directives out of the positive prompt.

When hard visual obligations are active, supply every required evidence field as an identifiable literal phrase in `prompt_en`, preserve request-scoped bindings byte-for-byte, and keep all declared runtime-forbidden labels absent. Compatible evidence phrases may overlap inside one natural clause; do not duplicate prose solely to satisfy the budget ledger. Selected optional visual concepts promote their entire opt-in obligation and render gates; unselected concepts add no duty.

When `render_repair` exists, add `render_repair_evidence` with its exact `source_contract_sha256` and one byte-identical evidence map per repair ID. Keep both the frozen interaction phrase and object-recognition phrase literal in `prompt_en`. This is positive realization of the requested relation, never a negative list or an instruction to move the object away from the actor.

### One bounded semantic self-review

Compare the complete final prompt with the active requester meaning, locks, exclusions and adopted candidate contracts once. Repair only a concrete, evidenced contradiction within open scope; otherwise retain the draft. Refresh any affected bindings and run the existing audits; an unresolved required contradiction uses the existing rebuild/clarification path, not repeated review loops or a claim of semantic certainty.

## Phase 4 — Audit Before Image Generation

Write the pack and composed object to files, then run:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py compose-audit \
  --run RUN --composed composed_prompt.json
```

Fix every composition-audit failure before generation. This is an audit repair, not authorization for another image call after a provider or execution failure. `negative_intent_guard_contract`, `negative_intent_guard_terms`, `negative_intent_guard_baseline`, and `negative_intent_guard_prompt` are blocking failures: they mean either the pack carries an ungrounded semantic suppression or positive prompt prose is trying to delete meaning with a blanket negative directive. Do not generate an image from an unaudited prompt.

`embodiment_preflight` failures block missing, stale, unsupported, or unresolved review records. The validator checks records and literal actuation; the agent must actually inspect spatial consistency. It does not detect arbitrary anatomical contradictions from prose. Every generated pack requires the baseline-review flag above; a non-body scene uses an explicit `not_applicable` review.

For an installed H-F2 run, keep using managed `prepare-render`, `native-plan`, `render-api` and review commands so the same sealed release performs its audits; do not pass its pack to a different standalone source implementation.

If image generation was requested, read `references/image-runtime.md`, copy `source_intent_lock_sha256` into the exact runtime request, and when present also copy `render_repair_contract_sha256`. Audit it with `scripts/audit_image_render_request.py`, generate, preserve the output and ledger record, then record and audit the exact generic repair hard-gate set with `scripts/audit_image_render_review.py`. Prompt/audit success is preflight evidence, not proof that rendered pixels satisfy the request. Use managed `review-shape --run RUN --image ACTUAL_FILE --baseline-available yes|no`; pending requester judgments are never acceptance. Author each gate's `observability` as `visible`, `partial`, or `unobservable` from the actual image. A multi-component gate requires every component and connection to be visible together; partial evidence cannot pass the full gate.

Review the saved image as a whole as well as checking hard gates. Assess whether its main impression, subject presence, and visual hierarchy realize the initial artistic direction, and whether its staging serves the requested genre and feeling. Also read the visible scene without its keyword explanation: assess whether actions, responses, and setting connect into an understandable situation, and what visible circumstances could make the viewer care. Distinguish what the pixels support from the richer story imagined during authoring. Note image-grounded strengths and weaknesses as supplemental observations, not new universal gates or user acceptance. A person's appeal is assessed in context at the chosen scale, not by face size. If comparisons are available, judge overall preference separately from instruction fidelity. Further generation follows the user's authorized scope; maintenance tests alone cannot establish an artistic improvement.

For control calibration, first describe the image's impression without consulting the intensity labels, then compare it with the frozen intended direction. Report technical binding, perceived expression and user preference separately. Do not promote a prompt phrase or metadata PASS into proof of artistic strength.

## Post-Core Reference Routing

All references below are post-core only. Load only what the frozen request and returned pack require:

- Candidate composition, audit, hard obligations, and quality fields: `references/composition-contract.md`
- Requested photographic-methodology review, or person-centered relationship, moment, individuality, and meaning-led framing: [photographic-methodology.md](references/photographic-methodology.md)
- Retrieval internals, indexes, and diagnostic boundaries: `references/retrieval-contract.md`
- Skill-owned local embedding installation and rollback: `references/local-embeddings.md`
- Candidate idea routes and composable adult-appeal axes: `references/hybrid-augmentation-contract.md`
- High-creativity proposals and authorial selection: `references/creative-direction-contract.md`
- Viewer response or commercial communication outcomes: `references/viewer-experience-contract.md`
- Natural-language character-response, identity, and pixel-review contracts: `references/moe-response-contract.md`
- Intent, concept, and slot retrieval behavior: `references/concept-routing.md`
- Image generation, saving, retries, and ledger records: `references/image-runtime.md`
- Body-action review binding and conditional pixel gates: `references/embodiment-preflight.md`
- Dictionary/profile edits, validation, semantic index, and evaluation: `references/maintenance.md`

Do not load every reference for a normal prompt request. Maintenance fixtures and research evidence are never runtime composition sources.

## Supported Contracts and Diagnostics

- New H-F2 runs use material V2 and validation context V1, with request envelope V1, core V3, intent lock V2, creative controls V4 and embodiment preflight V1. Bound historical native V10 runs retain their original path.
- Removed pack/core versions and missing current policy markers fail validation. Historical artifacts and their sealed execution paths retain their original contracts; new validation contexts and legacy native candidate packs are distinct types.
- Public packs withhold scores, probabilities, private ranking evidence and expanded argv.
- Current meaning clarification is V2. Source-grounded diagnostics distinguish absence, unrecognized expression, actual exclusion and relation structure; they never revise the frozen core or create hard obligations.
- The API adapter requires the original pack, exact runtime receipt, composed object and render request, and freshly audits both stages. Its text-only lane rejects unsupported references before invocation; dry-run performs no key lookup or image call. See `references/image-runtime.md` after the core is frozen.

## Validation for Skill Maintenance

For maintenance, use the change-scoped validation in `references/maintenance.md`. Start with the affected invariants and related contracts; use the full suite when the change's reach or unresolved regression risk warrants it. Preserve historical artifacts and frozen holdout meaning. Dictionary fields that affect semantic text require an index refresh; policy-only documentation does not. Image/API generation is not ordinary validation unless the requester explicitly asks for it. Contract tests establish integrity, not artistic quality.
