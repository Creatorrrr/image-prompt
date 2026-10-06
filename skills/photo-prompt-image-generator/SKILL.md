---
name: photo-prompt-image-generator
description: Write photographic image prompts and generate requested images. Use for photo concepts, creative photo direction, and reference-guided photographic generation.
---

# Photo Prompt Image Generator

Understand the requester, resolve the current creative controls, then make the main artistic decisions before writing the core. The baseline should already be a compelling, complete photograph with a coherent visual direction informed by those controls. Freeze that independent draft before project-local retrieval. The final authorial pass refines, simplifies, or preserves it.

Canonical skill path: `skills/photo-prompt-image-generator`.

User instructions and existing session authorization take precedence over this skill's procedural defaults, subject to system, developer, and image-tool requirements. Continue work already authorized; do not ask the user to approve the same action or API cost again. Ask only when a required decision or authorization is actually missing.

If a skill instruction causes a pause or a departure from the user's request, name and link this skill, quote the relevant instruction, and explain whether it is a requirement or your interpretation. Treat required bindings and audits as correctness checks; artistic guidance leaves room for judgment. Deliver the requested prompt or image with concise context, keeping internal schemas and checklists in the run artifacts unless requested.

## Non-Negotiable Phase Boundary

For an initial request, before `baseline_prompt_en` and its `photo-authorial-core/v3` hash are frozen, use only:

- the current user conversation, including definitions, exclusions, modifiers, references, and corrections;
- the model's general knowledge and independent visual reasoning;
- this skill's exact `precore/creative_controls.json` and the candidate-free output of `precore/creative_controls.py`, after resolving requester meaning, for the current values, provenance, ranges and artistic meanings;
- this skill's exact `precore/visual_feature_catalog.json`, only in Phase 1 after resolving the request's meaning, for neutral feature selection;
- one focused clarification question when different plausible meanings would materially change the image; or
- focused public-web research about the term's meaning when it is stable and publicly documentable but unfamiliar or uncertain.

During that pre-core phase, do not open, search, quote, or infer from:

- any candidate pack or earlier generated pack;
- any file under this skill's `assets/`, `references/`, or `scripts/` directories;
- visual-obligation profiles, registries, aliases, slot candidates, semantic indexes, or quality layers;
- tests, fixtures, evaluation cases, snapshots, rendered attempts, or maintenance evidence;
- private routing, another experiment arm, or a previous prompt produced from project-local knowledge.

The `SKILL.md` procedure, the named neutral catalog, and the named creative-control definition/resolver are the only project-local material available before the core. Executing or inspecting that resolver is permitted; it reads no candidate data. The catalog contains observation categories and illustrative examples, not request requirements or profile triggers. The control definitions explain configuration, not the meaning of requester keywords. This initial-request rule includes the neutral schemas below; retries have only the explicit exception in the next paragraph. A profile name, alias, or project glossary must never retroactively supply the initial meaning.

A retry has one narrow exception: inspect the named parent request/core/intent-lock hashes, frozen fields and evidence for dimensions the requester preserves, the effective hard obligations governing those dimensions, and the reported defect relevant to the repair. A previously selected opt-in obligation is part of that effective hard contract. Read only those fields from the parent artifacts; candidate inventories, unselected concepts, previous optional prose, other arms, maintenance examples, and the parent's feature-selection record remain unavailable. The current neutral catalog may be read again for a new selection, but previous selected categories are not inherited as hard obligations. This exception carries an existing obligation and never supplies fresh inspiration. If selective reading is impractical, use a coordinator-created whitelist extract bound to the parent artifact hashes.

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

Use the saved `creativity` level and resolved `adult_appeal_emphasis` from the first authorial decision. Creativity's default is 1; level 3 activates the existing high-creativity composition workflow after the core is frozen. The emphasis resolution records which active axis leads, or that no emphasis is active. These choices remain agent-owned and do not create requester locks.

Consider reference-use scope, intended viewer experience and use, and any active surreal/trend treatment at this same stage. Use the saved `surreal` meaning and selected level from the first authorial decision. This one integer replaces the former mode, probability and intensity settings; it has no probabilistic activation. The retrieved candidate breadth is not a perceptual measurement or a required detail count. Optional review toggles do not switch off artistic judgment or explicit request meaning. Keep staging register (such as candid or directed) and scene information density in the existing intent explanation when useful, without adding new required sliders. Prompt length, retrieval weights, candidate budgets and surface `artistic_final_touch` remain later/internal concerns.

Settings and agent staging are separate from requester text: do not insert their prose into `source_request`, user definitions, exclusions or requester-owned anchors. Use the baseline and `interpreted_intent` to realize them coherently. No new decision-count or styling checklist is required.

Keep raw request bytes and active spans intact. Explicit `name=value` or `name:value` settings are covered by matching overrides in the bound snapshot, not visual anchors or interpretation-provenance rows. A pure setting span needs no garment/action evidence. If a span mixes settings with visual instructions, source each remaining visual fragment separately; all still require normal coverage. Prefer separate spans for settings and visual requests. An agent-chosen realization of a value remains editable and cannot become a requester lock merely because it expresses that value.

## Phase 1 — Write and Freeze the Basic Prompt

### Primary authorial direction

Apply this authoring procedure to every request handled by this skill, using its complete contextual meaning. Its applicability is independent of particular words, mood labels, language, paraphrase, or the presence of standalone keywords. Scale interpretation and exploration by requester-prescribed meanings, remaining open choices, and the resolved creative controls. Every creativity level retains authorial judgment; the level controls interpretive distance and exploration depth.

Before consulting the neutral catalog or specifying mechanics, decide what makes this particular photograph worth looking at and what the viewer should experience. Interpret subjects, actions, relationships, styles, impressions, and their combinations in context; preserve explicitly requested and semantically necessary properties. Use the request, permitted reference cues, resolved creative controls, and independent visual judgment to choose a coherent whole-image idea. Let that idea shape open choices of form, arrangement, material, environment, photographic treatment and, when relevant, clothing or gesture. Keep optional realizations open instead of treating a familiar visual bundle as the default meaning. A precise request may already supply the direction; preserve it without inventing extra freedom.

When meaningful expressive choices remain open, briefly compare coherent realizations of the same requested meaning using only the permitted pre-core inputs, all at the requested control strengths. If the obvious first realization relies on familiar shorthand, consider a qualitatively different realization. Compare the initial direction by the same relevant criteria as alternatives: subject presence, the force of form, moment or relationship, sensory rhythm, expressive coherence, and required legibility. A cosmetic substitution alone need not constitute a different idea. Familiarity is neither a requirement nor a defect. Choose what serves this photograph, keeping the comparison lightweight without forced novelty, people or narrative, a fixed element menu, a proposal quota, or access to earlier outputs. Summarize the material direction in `interpreted_intent`; these agent choices create no requester-owned locks.

For a person-centered image, make the portrayal convey the person's distinctive appeal and presence in the requested situation. Expression, bearing, gesture, clothing, light, material, and the relationship with the surroundings can contribute when relevant. Choose camera distance and framing to serve that appeal. A distant figure can carry the image. Preserve requested reference appearance rather than reshaping facial features to fit a generic ideal. For a non-person subject, apply the same attention to the subject's visual character without inventing a person.

For person-centered photography, briefly establish a theme through these questions before choosing camera mechanics:

- **WHO:** What observable presence, expression, behavior, or presentation makes this particular subject worth seeing?
- **WHERE:** How does the place contribute to the requested action, role, atmosphere, or relationship?
- **HOW:** From what viewer position and psychological distance is the subject seen, and how is the camera acknowledged when relevant?
- **WHY NOW:** What makes this visible state or moment matter? Where transition serves the request, show a compatible trace of the preceding action or an emerging next action; a requested still pose remains a valid moment.

Consider SIR—symbolicity, individuality, and relationship—as complementary lenses for the frame. Use relevant visible cues for social or situational meaning, particular presence, and the camera-subject relationship, with emphasis suited to the request. These are choices within the authored photograph, not a fixed axis count or a reason to add biography, props, facial differences, or another person. Reference appearance alone establishes no actual personality, memory, preference, or desired self-presentation.

Choose the action, expression, interaction, or detail that carries the photograph's meaning, then include the surrounding context needed to read it. Derive distance, crop, lens, and light from that purpose while preserving requested framing and consequential contact. Keep emotional interest and formal restraint distinct: restraint organizes attention and information rather than lowering the resolved creative-control strengths. Leave interpretive space when it serves the request without obscuring required evidence.

These questions are part of this pre-core procedure, using only the permitted inputs. Record material choices in the existing intent and priorities; they introduce no new fields, sliders, candidate count, individuality quota, score threshold, or requester-owned locks. Detailed methodology references remain post-core only.

Use the existing `interpreted_intent` to state the intended experience concisely, distinguishing your artistic choice from requester-specified meaning. Use `visual_priorities` for the few visible relationships that carry it, with a clear focal hierarchy. These planning aids create no additional locks: an authorial motif may be replaced within the request's open scope. Where they serve the request, sensory specificity, emotional tension, or selective ambiguity should come from the scene rather than praise adjectives or unrelated embellishments. Formal staging and clarity can themselves be the intended artistic effect.

Then select the observation categories below and author a coherent 48–640 word English photographic prompt that can stand alone. Treat 360 words as the default recommended maximum, not a hard cap. Exceed it only when requester meaning or literal hard evidence cannot be represented cleanly within 360 words; never pad toward the limit. It must already specify a concrete subject, setting, visible event or state, and two to six distinct visual priorities. Write it as a photograph with an artistic point of view, not a search query, tag bag, or placeholder.

Read the exact neutral catalog named above. Review its category names and choose five to ten distinct categories to develop for this request; count categories already specified by the requester. The catalog's `source_examples` and `added_examples` are optional examples to consult for relevant categories, not a menu of required values or permission to invent a person, action, era detail, defect, or camera recipe. Translate examples phrased as an absence into visible positive states in the baseline (for example, still reeds or natural edge transitions); do not copy their negated clauses into `baseline_prompt_en`. Start with the event, subject, setting, and visible consequence; unless the requester asked for photographic technique, do not let technique categories dominate the selection. A sparse or precise request still gets five meaningful observation axes by counting what it already specifies and making only restrained choices in genuinely open photographic dimensions. More than ten requester-specified axes never lose their instructions merely because only five to ten categories are selected for focused development. Do not count overlapping categories twice for the same visual decision.

Select only features that distinguish the request's meaning, make its event, relationships, or consequential physical or spatial arrangements legible in one frame, or support a visual hierarchy suited to the request's purpose. When relevant, express an abstract situation, affect, or implied prior context through actions, directed attention, visible responses, material states, or traces present in that frame. Integrate those cues into one scene instead of filling a feature checklist; omit irrelevant prompt detail without closing genuinely open dimensions in `intent_lock`. The five to ten selected categories are not the core's two to six `visual_priorities`: each priority should be one coherent visible proposition, not a concatenation of category names or camera tags. Other selected categories may appear only in the baseline prose. Do not record incidental agent-chosen staging as a requester definition or exclusion, a resolution of a request term in `interpretation_provenance`, or an independent semantic assertion; keep required evidence phrases limited to the visible meaning they prove, excluding incidental detail from open dimensions. A category selection never creates a locked dimension, anchor, assertion, or `photo-visual-intent/v1`, nor does it remove an open dimension; every requester-specified dimension still follows the existing lock rules. A catalog example alone is never a source for `user_definitions`, `interpretation_provenance`, `semantic_assertions`, or `photo-visual-intent/v1`. Showing affect or a visible response this way does not itself activate `character_response`; follow the requester-meaning trigger below.

Count meaningful axes already present in the authored scene; the category count does not justify adding props, expressions, gestures, or technical clauses. Keep the dominant impression clear and let supporting details remain subordinate. Before freezing, remove optional detail that makes the subject demonstrate instructions rather than inhabit the intended moment.

For a requested interaction, state change, or component relationship, distinguish the participants, target or affected property, relevant starting state, action, visible result, and continuity where those roles exist. Connect requester-owned relations to literal evidence in the existing anchors and assertions. Check which roles each phrase actually proves; a general scene description cannot stand in for every endpoint. A static arrangement needs no invented action, history, or additional participant.

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
- Every active span needs both semantic-origin coverage (`user_definitions` or `interpretation_provenance`) and at least one intent anchor. Every fully locked dimension needs an anchor with substantive requester source text and its own distinct literal baseline evidence phrase. `concept`, `subject`, and `event` are always locked. Fully specified dimensions remain locked; for a partially specified dimension, use the property anchors below and leave its other choices open. Open and fully locked dimensions are disjoint. V6 permits zero or one open dimension for precise requests or local repairs; write `open_dimensions: []` explicitly when none are open, and never invent freedom to satisfy a creativity quota.
- For a new core, review requester-owned camera direction and height separately. Record each prescribed axis in a `camera` property anchor (`viewpoint.direction`, `viewpoint.height`, or a combined path) with its literal English baseline evidence; a concept anchor alone does not supply camera ownership. Pass `--require-camera-evidence direction` and/or `--require-camera-evidence height` for those prescribed axes when generating the pack. The check runs before candidate DATA loads. Do not lock an unprescribed authorial camera choice merely to satisfy the check. Older frozen cores may use a conservative literal camera-clause query projection; this never creates missing locks or authorizes adoption on a locked viewpoint.
- When `camera` is an existing open or locked dimension, every newly authored core also records one camera assertion in the existing neutral assertion shape. When camera is absent from both lists, omit that assertion: the dimension remains closed, including in zero-open/no-op cores. Never add camera freedom or a whole-camera lock to fill a review row. Explicit requester-axis checks above still apply, and any supplied declaration is always validated. Its axes are exactly `camera_axis_review: camera_axis_review_v1`, `capture_owner: camera` when an axis is requested (otherwise `unprescribed`), and separate `direction_requirement`/`height_requirement` values `requested`, `open`, or `excluded`. Use advisory polarity while camera is partially open; existing property anchors retain the requested hard duties. Use required polarity only for an independently justified whole-camera lock. For requested axes, evidence contains exactly `owner_phrase` naming the capture camera and `direction_phrase` and/or `height_phrase`; select literal baseline subphrases, at most 16 words for the owner and 24 for each axis. Each axis phrase must occur in its existing camera-target viewpoint anchor. With no requested axes, evidence is empty; do not add camera prose to an unspecified scene. An excluded axis needs requester-grounded `user_exclusions` and receives no positive axis evidence. Cite the active requester span IDs normally. Pass `--new-author-camera-evidence` with the public generator. Review actual capture ownership, lens attachment and local negation yourself: these source/type/literal checks cannot prove your interpretation is correct. An older frozen core is replayed without this new-author flag and is never rewritten merely to obtain an assertion.
- Use only these v3 dimension names: `concept`, `subject`, `identity`, `count`, `age`, `role`, `species`, `appearance`, `pose`, `body_geometry`, `expression`, `action`, `event`, `setting`, `relationship`, `sexual_tone`, `style`, `reference_use`, `viewer_outcome`, `text`, `format`, `framing`, `composition`, `lighting`, `camera`, `color`, `material`, `timing`, `atmosphere`, `character_response`.
- Put an actual requester definition or answer to a clarification question in `user_definitions`. Its `source_text` must equal a complete active span and cannot be only the term itself. A bare term is an agent interpretation, not proof that the requester supplied a definition.
- Use `interpretation_provenance` for material agent/context/web interpretations, not for requester-owned definitions. Web-based entries require at least one source URL; URLs do not enter the retrieval query.
- `unresolved_ambiguities` is mandatory and must be empty. If it is not empty, ask or research before continuing.
- `user_exclusions` contains only explicit requester negatives. Never use it to hide a requested concept, because exclusions are removed from semantic retrieval.
- Do not translate platform policy, an agent's comfort preference, a coordinator's risk summary, or a profile's conservative default into `user_exclusions`, `baseline_prompt_en`, or runtime negatives. Platform and image-tool enforcement remains active outside prompt semantics.
- If a source-grounded shorthand label should aid interpretation and profile activation but should not be sent to the image runtime, put it in `runtime_forbidden_labels` and express its intended visible components in anchors and the baseline. Runtime-only labels remain in retrieval; only their literal runtime spelling is forbidden.
- `semantic_assertions` is the only normal v6 input for meanings that need a typed downstream contract. A required assertion affects locked dimensions, an advisory assertion affects open dimensions, and an excluded assertion cannot be resurrected by retrieval. Every assertion cites active `source_span_ids`; every required evidence phrase is already literal in `baseline_prompt_en`.
- Hand off the resolved primary subject category through an optional required `subject` assertion with `axes.subject_category` set to one of `human`, `animal`, `object`, `food`, `plant`, `environment`, `sign`, or `unknown`. Bind it to the requester span and literal subject evidence before retrieval. Use the actual primary subject, including an object depicting a person or animal; do not insert technical category aliases into the request or baseline. This type constrains retrieval and adds no detail obligation. Missing or `unknown` categories preserve conservative slot guards; the coarse creative-context value `nonhuman` does not establish `object`.
- Lock the requester-owned meaning at the narrowest sufficient level. A mood or relationship does not by itself require the particular stance, hand arrangement, smile, garment, or camera distance you chose to express it. Write the minimal coherent action-and-result phrase that proves the requested meaning, placing incidental styling or geometry outside that phrase. The same authorial choice must not be declared optional in the feature-selection record and included intact in mandatory evidence. Freezing the baseline preserves its provenance; unbound staging on open dimensions remains editable in final composition.
- Treat a named character or relationship archetype whose meaning depends on behavior as a required visible `character_response`, even when the requester calls it a concept or also specifies a costume, role, facial expression, or prop. Lock `character_response` and make the baseline show a clearly identifiable actor, one identifiable relationship target or repeated marker of that same target, one concrete target-directed action, one affect leak, and one already-visible consequence in a single frame. This behavioral requirement does not prescribe age; preserve requester-owned age. An adjective, intense gaze, smile, role outfit, weapon, medical tool, or other prop alone never satisfies this contract; reference-image appearance never activates personality.
- Every required non-`character_response` assertion is compiled into `photo-semantic-assertion-obligations/v1`. When that block exists, copy its exact frozen evidence into `semantic_assertion_evidence.evidence.<assertion_id>`, bind `source_contract_sha256`, and keep every phrase literal in the final prompt. Retrieval cannot supply or replace any of those hard phrases.
- For a required visible character response, lock `character_response`, add its own semantic anchor, and write one `character_response` assertion with the generic axes `surface_affect`, `underlying_affiliation`, `relationship_target`, `primary_action`, `affect_leak_timing`, `affect_leak_channels`, and `event_phase`. Select exactly one primary leak channel. When the meaning depends on a relation rather than isolated attributes, encode bounded generic `relations` using `same_target`, `contrasts`, and/or `temporal_order`; do not leave the relation to a named label. Every relation member must be a declared generic axis or causal role, and every `same_target` relation must include `relationship_target`. For a named affection-control archetype, bind the affection surface or care, primary action, and immediate consequence to that same target; an affect leak may support this vector but cannot replace the consequence. Bind `actor_phrase`, `baseline_phrase`, `trigger_phrase`, `target_phrase`, `primary_action_phrase`, `affective_leak_phrase`, `visible_response_phrase`, `immediate_consequence_phrase`, and `continuity_phrase` to literal baseline text. Values are authored from the request; never route a named archetype to fixed gaze, face, pose, or story geometry.
- Make behavioral evidence sufficient and economical. Compatible evidence fields may share a clause when it actually proves both relations. Do not invent a second gesture or force a reassuring expression merely to fill a field; preserve ambiguity that belongs to the requested feeling while making the governing action and relationship legible.
- `request_lineage` is `null` for an initial request. On a retry it hash-binds the parent request/core and separates preserved dimensions from the explicitly allowed changes; the two sets are non-empty and disjoint. Inspect only the parent fields allowed by the retry exception above before freezing the retry. If `concept` or `character_response` is preserved and the parent had a hard visual obligation, recreate that same obligation as a hash-bound post-core `photo-visual-intent/v1` sourced from an exact current frozen core field. Do not let an elliptical retry phrase demote a preserved hard obligation into an unselected embedding candidate, and do not carry the obligation when the requester changed or excluded the governing meaning.
- A fidelity complaint about a meaningful interactive prop is not permission to remove, relocate, conceal, or transfer it. On such a retry, use `photo-request-lineage/v2` and one object-agnostic `repair_targets` row. Freeze actor, object, interaction state, expected contact, protected locked dimensions, positive interaction and recognition phrases, and only the local repair axes that may change. Use `relation_origin: parent_preserved` when the parent relation remains intended and `relation_origin: requester_corrected` when the requester explicitly corrects an evasive parent relation. Bind both phrases through one required action assertion in the baseline. Decorative background objects and non-action-bearing ornaments do not need repair targets.
- Every multi-arm run shares the immutable raw requester text but freezes a separate, exact-span-bound envelope and core for each arm before any arm sees project-local data.

For a partial prescription, `photo-intent-lock/v2` permits a semantic anchor on an open dimension with additional `target` and `property` paths. For example, a requester-specified white garment may have `dimension: appearance`, `target: main_subject`, `property: wardrobe.color`, and literal evidence proving that color. A separate `wardrobe.garment_type` anchor can preserve the garment type while leaving `wardrobe.neckline` open. Use stable lowercase paths for the actual object and property; preserve their meaning across composition. Property anchors may share one economical evidence phrase. Keep complete reference-outfit preservation or a fully specified appearance as a whole-dimension lock. These anchors do not change the existing rules for required typed semantic assertions.

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

There are at most 16 assertions, 1–16 axes per assertion, at most 8 distinct values per axis, and at most 16 evidence fields. Required assertions have at least one evidence phrase, each with at least two content words. Values are strings or string lists; evidence values are strings. A required `character_response` uses the seven axes and nine evidence keys listed above, exactly one `primary_action`, and a one-item list for `affect_leak_channels`.

Only `character_response` may add `relations`, a list of 1–8 objects with exactly one of these shapes: `{"operator":"same_target","members":["<member>","relationship_target"]}`, `{"operator":"contrasts","left":"<member>","right":"<member>"}`, or `{"operator":"temporal_order","first":"<member>","then":"<member>"}`. Members are `actor`, `baseline`, `surface_affect`, `underlying_affiliation`, `relationship_target`, `target`, `primary_action`, `affect_leak`, `affect_leak_timing`, `trigger`, `visible_response`, `immediate_consequence`, `continuity`, or `event_phase`. Use distinct members and no duplicate relations. Non-character assertions omit `relations`; they may describe their observable relations through authored axes and literal evidence.

### Negative-intent firewall

Write `baseline_prompt_en` as positive visual realization. Do not embed instruction-shaped blanket negatives such as `No X, Y, or Z`, `Do not ...`, `Avoid ...`, `Exclude ...`, or clauses such as `never touching anyone`. These clauses can silently delete the requested relationship, action, emotion, prop, person count, wardrobe, or genre signal. The modern core normalizer rejects them before the core can be frozen.

Use three separate lanes:

- A semantic exclusion is valid only when the requester explicitly supplied it and it is grounded in an active request span. Keep it in `user_exclusions`; after removing a literal directive prefix, a runtime-negative item must equal the complete exclusion. Do not split a combined exclusion or broaden it by substring, synonym, or category inference.
- Automatic `negative_en` is limited to a narrow intent-neutral photographic-defect vocabulary. Generic safety, taste, count, contact, action, relationship, expression, wardrobe, and genre suppressions are removed. Identity-preservation negatives are allowed only when identity-reference preservation is explicitly enabled.
- Platform or image-tool policy is enforced by the platform/tool and by post-render review. It is not serialized as a blanket runtime negative. When a permitted scene needs a local boundary, describe the visible positive state instead: for example, `the capped needle hovers beside an intact sleeve` rather than `no contact, no injection, no gore`.

The pack exposes a hash-bound `photo-negative-intent-guard/v1` containing the emitted negative terms and governing policy. It is recomputed during composed audit. This guard applies to both the positive prompt surface and `negative_en`; copying the pack negative bytes is necessary but no longer sufficient.

### Record the pre-core feature selection

Keep one `precore_feature_selection.json` beside the envelope and core for each request arm. Choose the categories before drafting, then finish this record using the final, canonically spaced `baseline_prompt_en` and frozen envelope. Each selected category needs a distinct reason and a literal baseline phrase showing how it was used. `basis` is `explicit_request` for an exact requester span, `request_derived` for a visible realization derived from a cited active span, or `agent_visual_choice` for a decision within an open dimension. For `explicit_request`, fill `source_span_ids` and `source_text` with an exact substring of an active span, and set `derivation` to `null`. For `request_derived`, fill `source_span_ids` and `derivation`, and set `source_text` to `null`. For `agent_visual_choice`, set `source_span_ids` to `[]` and both `source_text` and `derivation` to `null`. These labels describe the recorded realization, not the category's permanent authority.

```json
{
  "contract_version": "photo-precore-feature-selection/v1",
  "request_id": "<envelope request_id>",
  "active_span_ids": ["<this arm's active envelope span ID>"],
  "catalog_path": "skills/photo-prompt-image-generator/precore/visual_feature_catalog.json",
  "catalog_schema_version": "photo-precore-feature-catalog/v1",
  "catalog_sha256": "<SHA-256 of exact catalog file bytes>",
  "request_sha256": "<envelope request_sha256>",
  "baseline_prompt_sha256": "<SHA-256 of final canonical baseline_prompt_en UTF-8 bytes>",
  "selected": [
    {
      "category_id": "feature.situation",
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

The sample row shows shape, not a default category or a complete five-to-ten selection. The selection record is audit evidence only: do not put it in the core, retrieval query, candidate pack, semantic assertion, or runtime prompt. Copy the exact catalog bytes beside the run artifacts for later historical review; never use a prior run's copy to write a new core. After freezing the core, and **before** any candidate or profile access, validate the record:

```bash
cp skills/photo-prompt-image-generator/precore/visual_feature_catalog.json visual_feature_catalog.snapshot.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_precore_feature_selection.py \
  --catalog skills/photo-prompt-image-generator/precore/visual_feature_catalog.json \
  --request-envelope request_envelope.json \
  --authorial-core authorial_core.json \
  --embodiment-review embodiment_review.json \
  --selection precore_feature_selection.json
```

If validation fails, correct the record or rebuild the affected pre-core artifacts before opening candidate data. An `agent_visual_choice` phrase included intact in a mandatory anchor, definition, or required assertion is an ownership conflict: narrow the mandatory evidence or correct its provenance from the actual request, rather than relabeling the choice to pass. Inspect `warnings` even when the command succeeds: revise repeated reasons or evidence, and review any delivery-and-technique majority against the request before proceeding. The group-majority warning is a review cue, not an automatic rejection of a justified composition choice. Any baseline change also invalidates the embodiment-review hash, core, derived intent-lock binding, and selection hash. The validator checks the supplied catalog against the current permitted file in live runs; use `--historical-catalog` only to verify an archived record against its saved snapshot after the run. It confirms structure and literal binding; it cannot prove that selection preceded drafting or that the resulting image is good.

Pass the envelope with `--request-envelope-json`, the core with `--authorial-core-json`, to the generator; it always returns candidate-pack v6. The generator canonicalizes both, rejects unsupported or ungrounded fields, and binds their hashes and active spans to retrieval, the public pack, composition, and runtime.

## Phase 2 — Retrieve After the Core Is Frozen

Only now may the generator load dictionaries, the semantic index, candidate material, the visual-profile registry, and its generated registry-hash-bound index.

Generate exactly one pack:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py \
  --request-envelope-json request_envelope.json \
  --authorial-core-json authorial_core.json \
  --creative-controls-json creative_controls.json \
  --embodiment-review-json embodiment_review.json \
  --output-file candidate_pack.json
```

The generator derives retrieval from the active requester spans and frozen core, removes true requester exclusions, and retains runtime-forbidden labels for meaning retrieval. The pack must not define the baseline after the fact.

The generator takes initial artistic controls from the supplied snapshot. Conflicting later CLI controls are rejected; update the pre-core inputs and rebuild instead of silently changing the creative direction after freezing. Every generated pack requires this binding.

Bound v6 runs retrieve adult-axis possibilities from the compatible corpus, using separate baseline-coherence and request-led alternatives queries. Eligibility follows the frozen scope and context. The returned mode states whether keyword or hybrid search actually ran; a hit proposes material for contextual interpretation, never proves an aesthetic category. Internal search lanes still produce one external pack.

Basic-prompt authoring does not receive a slot list or candidate data. The frozen core determines which slot queries are grounded. After freeze, each such slot searches its eligible authored corpus with the whole-scene query and a core-derived focus query, then fuses supported hits into one bounded pack. Explicit frozen observations also receive focused lexical discovery from source-declared, property-compatible candidates and take priority within the shared candidate cap. This priority changes exposure only; it never creates an adoption duty. Eligibility uses requester exclusions, subject/domain constraints, facets and primary-context guards from the frozen core. An ungrounded slot or a slot without a lexical hit is omitted; there is no automatic detail-slot quota or required adoption. All optional candidates may be rejected, leaving the independently written baseline intact.

The pack records `photo-core-retrieval/v1` in `core_retrieval`, binding the frozen core, slot corpus, ownership and applicability hashes, whole-scene query and active-slot focus hashes. Copy its exact `canonical_sha256` into `core_retrieval_sha256` in both the composed prompt and runtime request. Audits recompute the inventory from the source corpus; an added, omitted or substituted candidate fails.

Candidate-pack v6 separates three jobs:

- Requester-owned anchors, definitions and required `semantic_assertions` govern meaning. The frozen baseline records the initial realization; its unbound authorial choices remain editable. The v3 core itself is non-revisable inside the pack run. Correcting a frozen requirement needs a rebuilt envelope/core/pack; use clear existing requester intent without asking again, and ask only when that meaning remains unresolved.
- `semantic_clarification` and BM25F/embedding retrieval are post-core assistance. Exact request-scoped profile terms may retain their declared hard meaning. BM25F-only, embedding-only, and fused approximate hits are optional and can never create an assertion, required evidence phrase, or render gate.
- `creative_augmentation` is sampled only after hard applicability, conflict, identity/species/no-people, safety, negative, and requester-exclusion filters. Creativity levels `0–1` permit `near`, level `2` permits `near + adjacent`, and level `3` also permits `lateral`; seed selects within the allowed range. Every transformed choice declares `affected_dimensions` within its applicable dimension boundary and remains subordinate to the locked meaning; Phase 3 describes the scoped adult-axis exception.

V6 compiles frozen character-response axes and evidence through `photo-character-response/v1`, and other required assertions through `photo-semantic-assertion-obligations/v1`. Character meaning comes only from the frozen typed assertion. The composed audit recomputes these contracts from the core. Semantic clarification projects the actual frozen duties and keeps `authorial_direction` as separate context; it does not promote the entire `interpreted_intent` or `visual_priorities` into requirements. Retrieval consistency, labels, scores, and array order never create hard evidence or revise a frozen meaning; every creative candidate may be rejected. Consult `references/retrieval-contract.md` only for retrieval diagnostics or implementation details.

Interpret post-core applicability against the whole request and frozen evidence. An unmatched expression, missing field, unsupported prerequisite, or different relation signature does not by itself prove a different meaning. Before explaining a questionable rejection, use the [diagnostic guidance](references/retrieval-contract.md#interpreting-applicability-diagnostics) to identify what was actually checked. Preserve the returned status and all required bindings; semantic judgment cannot bypass a gate, revise the frozen core, or invent evidence. Clear requester meaning remains authoritative when local data does not recognize it.

Read the compact composition view before loading full optional candidate details:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/compose_pack_view.py \
  --pack candidate_pack.json --output composer_view.json
```

The view binds the unchanged source pack and presents requirements plus a candidate catalog. Use repeatable `--candidate-id <id>` to read full details for candidates under consideration. Review every mandatory requirement, retrieve a selected candidate's complete constraints before using it, and keep the original pack as the audit input. The view is a reading aid, not a replacement or mutable pack. Modern v6 semantic surfaces preserve short `concept_units` and directed `relations`; keep each unit intact when interpreting its meaning. Selecting a relational candidate requires literal `relation_evidence`, and selecting an optional bundle also requires `component_evidence` for every component. Read the complete selection contract in the detail view and `references/composition-contract.md`. Bundle members form one joint choice; their associated profile IDs never acquire automatic hard authority.

### Optional post-core visual intent

For an exact, non-substitutable requester definition or a preserved parent hard obligation, read `references/retrieval-contract.md` and construct `photo-visual-intent/v1` only after the core is frozen. Its evidence must already belong to the requester definition or one exact frozen core field. Exact resolution may bind a hard profile; approximate retrieval remains optional. Do not construct visual intent merely because a candidate offers an attractive interpretation.

Before rendering, when the requester explicitly makes a perceptual effect focal, cover that meaning with a required typed assertion or an active hard visual obligation. A broad label, an embedding hit, or an optional candidate is not coverage. If the focal meaning is still uncovered, rebuild from the clear requester meaning; ask only if that meaning is still ambiguous. Record this focal-coverage check separately from prompt, runtime, and pixel status.

## Phase 3 — Clarify and Refine the Authored Photograph

Read `references/composition-contract.md` for the composed shape and active conditional fields. Refine the independently authored photograph from Phase 1. Judge optional candidates and the baseline by the same relevant artistic criteria from Phase 1 and their contribution to the whole-image direction and visual hierarchy; selecting none is valid. Candidate or profile term matches provide semantic assistance and never determine whether this common authoring procedure applies. The final pass may retain, clarify, remove, or replace agent-authored detail on open dimensions. Reconsider a familiar motif when another compatible realization better serves this photograph; appearing in the first draft gives it no protection. Preserve requester-owned meaning and complete adopted contracts. Make artistic refinements during composition before the bounded semantic self-review below; absence of a semantic contradiction alone does not settle the artistic choice. Retain the baseline when it remains the best realization, without requiring a new visual idea or detail count.

Before choosing, read the exact active requester text, definitions/exclusions, ownership of whole-dimension and property locks, the baseline, and each considered candidate's full source detail. Use the compact view for navigation, not as permission inferred from a slot name, rank, or summary. Judge what the candidate would actually add across the whole frame, including implicit people, apparatus, relationships, and effects outside its named slot. Follow the model-guided candidate review in `references/composition-contract.md`: adopt the complete compatible meaning, use only independently justified generic attributes as an authorial choice, or decline. These are reasoning outcomes, not new wire-format decision values. Required meanings and atomic/conditional candidate contracts remain binding; do not relabel a distinctive candidate realization as authorial to evade them.

Apply that semantic and applicability review across all subjects, languages, paraphrases, compound descriptions, and requests without standalone labels. Its scope follows the request's meaning and the candidate's complete effects, independent of a keyword list or profile match. Distinguish meaning compatibility, realizable prerequisites and allowed changes, then artistic preference. Use existing decision fields or concise run notes for material reasons; a compatible but less useful option is not semantically invalid, and zero adoption does not explain why candidates were declined.

When the requester asks for the photographic methodology, or a person-centered frame would benefit from clearer relationship, moment, individuality, or meaning-led framing, read the relevant sections of this skill's internal [photographic-methodology.md](references/photographic-methodology.md). It contains the integrated theme, SIR, psychological-distance, framing, camera, and review guidance. Apply useful refinements within the existing open dimensions and property locks, recording material changes in the existing `authorial_decisions`; preserve the baseline when it already works. This skill owns the methodology, final prompt, pack-approved negative, audit, and render.

When `adult_appeal.dimension_scope` is present, read the adult-axis section of `references/hybrid-augmentation-contract.md`. Those two axes may use their declared unlocked dimensions even if omitted from `open_dimensions`; preserve every locked meaning and record the dimensions actually changed in `adult_appeal_brief`. This scoped exception does not open dimensions for unrelated creative additions or revise the core.

When `adult_appeal.contextual_retrieval` is present, use [contextual appeal](references/contextual-appeal.md). Its expression shortlist is visible independently of the general creative sample. Interpret these candidates in the current scene and compare viable alternatives with the baseline at the same strengths; retain either on artistic grounds. Record a concise review in the existing adult brief. Candidate adoption remains optional, and the final prompt contains only the selected direction.

Both axes can use compatible choices throughout the scene while preserving property anchors. Role, setting, relationship and timing changes require those dimensions to be explicitly open. If an axis is already expressed in the baseline, use `realization: baseline`, retain literal baseline evidence, and set `affected_dimensions: []`; no new detail is required. For a refinement, use `realization: refined` and declare actual changes, including `affected_properties` on partially locked dimensions. Assess whether the intended direction is readable in context; a generic material word or valid intensity number alone does not establish that. Explain a constrained realization in the existing artistic interpretation instead of claiming visual success.

Reconsider the whole frame before polishing clauses. Compare each viable realization by the requested meaning, subject appeal and whole-image effect; losing an agent-chosen motif can be a worthwhile trade when the alternative establishes a stronger relationship. If a chosen pose, distance, expression, or prop arrangement weakens the intended experience, revise the unbound staging while preserving every requester-owned anchor and effective hard obligation. Record material refinements in the existing `authorial_decisions`, including subtraction or simplification. Do not change the frozen core in place or silently rewrite required evidence. If a needed change would alter a frozen anchor or assertion, rebuild through the existing request/core path; use clear existing user intent without another approval request.

When `embodiment_preflight` is present, read `references/embodiment-preflight.md`. Recheck the entire final prompt, including new camera, framing, clothing, and contact clauses; preserve the baseline review and bind a fresh `agent_postcomposition` review in `embodiment_review`. A changed prompt invalidates the previous review hash. Fix composition conflicts through unbound staging on open dimensions. Use the existing rebuild or repair lineage when required frozen evidence must change. General defect negatives cannot substitute for a coherent positive realization.

For every semantic clarification, record exactly one decision:

- Apply a fitting clarification and bind literal prompt evidence.
- Reject a context-mismatched or gated clarification.

Never supersede a v3 core or requester definition. Reject optional candidates that suggest a different meaning and continue with the frozen core. If an actual requester ambiguity or a conflict in required evidence prevents faithful composition, stop that run and resolve it before rebuilding the envelope, core, and pack. A clear requester correction already authorizes that rebuild.

For creative candidates, decide each as `transformed` or `rejected`. Rejecting all is valid. Transform at most three, declare `affected_dimensions`, keep them within `intent_lock.open_dimensions` or the adult-axis scope above for a scoped adult candidate, and add a new relation, cause, material behavior, framing, light, omission, or timing decision instead of copying source terms.

Bind the exact pack ID, negative, core hash, intent-lock hash, anchor IDs, preserved evidence, candidate choices, all clarification decisions, and creative decisions in the composed object. Set `composer` to `agent`.

Preserve every anchor's literal evidence and all required assertion/profile evidence, and keep requester exclusions and runtime-only labels absent. New v6 packs expose `photo-authorial-authorship-policy/v2`: no additional baseline-phrase quota or final-decision quota is imposed. Use `preserved_evidence: []` unless extra literal preservation is intentionally needed, and `authorial_decisions: []` when no material refinement is needed. Any recorded decision must be substantive and use a distinct open dimension; any extra preserved phrase must occur in both prompts. Never add detail to fill a quota in a new run.

Keep `prompt_en` within 48–640 English words and aim for at most 360. The evidence-adjusted advisory ceiling is the larger of 360 or hard-evidence words plus 160, capped at 640; exceeding either advisory ceiling produces a warning. Remove optional material before dropping requester meaning or literal evidence. Compatible evidence may share a natural clause. The final result must read as one coherent photograph. Requester meaning outranks generic character, moe, viewer, style, and creative defaults. Preserve only the guard-approved pack `negative_en`, and keep blanket negative directives out of the positive prompt.

When hard visual obligations are active, supply every required evidence field as an identifiable literal phrase in `prompt_en`, preserve request-scoped bindings byte-for-byte, and keep all declared runtime-forbidden labels absent. Compatible evidence phrases may overlap inside one natural clause; do not duplicate prose solely to satisfy the budget ledger. Selected optional visual concepts promote their entire opt-in obligation and render gates; unselected concepts add no duty.

When `render_repair` exists, add `render_repair_evidence` with its exact `source_contract_sha256` and one byte-identical evidence map per repair ID. Keep both the frozen interaction phrase and object-recognition phrase literal in `prompt_en`. This is positive realization of the requested relation, never a negative list or an instruction to move the object away from the actor.

### One bounded semantic self-review

Compare the complete final prompt with the active requester meaning, locks, exclusions and adopted candidate contracts once. Repair only a concrete, evidenced contradiction within open scope; otherwise retain the draft. Refresh any affected bindings and run the existing audits; an unresolved required contradiction uses the existing rebuild/clarification path, not repeated review loops or a claim of semantic certainty.

## Phase 4 — Audit Before Image Generation

Write the pack and composed object to files, then run:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py \
  --pack candidate_pack.json \
  --composed composed_prompt.json
```

Fix every failure. `negative_intent_guard_contract`, `negative_intent_guard_terms`, `negative_intent_guard_baseline`, and `negative_intent_guard_prompt` are blocking failures: they mean either the pack carries an ungrounded semantic suppression or positive prompt prose is trying to delete meaning with a blanket negative directive. Do not generate an image from an unaudited prompt.

`embodiment_preflight` failures block missing, stale, unsupported, or unresolved review records. The validator checks records and literal actuation; the agent must actually inspect spatial consistency. It does not detect arbitrary anatomical contradictions from prose. Every generated pack requires the baseline-review flag above; a non-body scene uses an explicit `not_applicable` review.

If image generation was requested, read `references/image-runtime.md`, copy `source_intent_lock_sha256` into the exact runtime request, and when present also copy `render_repair_contract_sha256`. Audit it with `scripts/audit_image_render_request.py`, generate, preserve the output and ledger record, then record and audit the exact generic repair hard-gate set with `scripts/audit_image_render_review.py`. Prompt/audit success is preflight evidence, not proof that rendered pixels satisfy the request.

Review the saved image as a whole as well as checking hard gates. Assess whether its main impression, subject presence, and visual hierarchy realize the initial artistic direction, and whether its staging serves the requested genre and feeling. Note image-grounded strengths and weaknesses as supplemental observations, not new universal gates or user acceptance. A person's appeal is assessed in context at the chosen scale, not by face size. If comparisons are available, judge overall preference separately from instruction fidelity. Further generation follows the user's authorized scope; maintenance tests alone cannot establish an artistic improvement.

For control calibration, first describe the image's impression without consulting the intensity labels, then compare it with the frozen intended direction. Report technical binding, perceived expression and user preference separately. Do not promote a prompt phrase or metadata PASS into proof of artistic strength.

## Post-Core Reference Routing

All references below are post-core only. Load only what the frozen request and returned pack require:

- Candidate composition, audit, hard obligations, and quality fields: `references/composition-contract.md`
- Requested photographic-methodology review, or person-centered relationship, moment, individuality, and meaning-led framing: [photographic-methodology.md](references/photographic-methodology.md)
- Retrieval internals, indexes, and diagnostic boundaries: `references/retrieval-contract.md`
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

- The supported workflow is V6, request envelope V1, core V3, intent lock V2, creative controls V4 and embodiment preflight V1.
- Removed pack/core versions and missing current policy markers fail validation. Historical artifacts remain evidence and can be inspected with their historical implementation.
- Public packs withhold scores, probabilities, private ranking evidence and expanded argv.

## Validation for Skill Maintenance

For maintenance, use the change-scoped validation in `references/maintenance.md`. Start with the affected invariants and related contracts; use the full suite when the change's reach or unresolved regression risk warrants it. Preserve historical artifacts and frozen holdout meaning. Dictionary fields that affect semantic text require an index refresh; policy-only documentation does not. Image/API generation is not ordinary validation unless the requester explicitly asks for it. Contract tests establish integrity, not artistic quality.
