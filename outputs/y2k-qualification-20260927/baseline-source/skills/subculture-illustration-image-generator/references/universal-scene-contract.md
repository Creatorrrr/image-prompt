# Universal Scene Contract

## Why v3 Has a Semantic Preflight

The default v3 candidate pack adds a topic-independent scene layer for expressions, poses, actions, relations, props, and environmental consequences. The local runtime deliberately does not guess those semantics from arbitrary natural language. Before calling it, the skill agent must derive one literal-bound `subculture-illustration-scene-contract/v2` from the exact original request and pass it through `--scene-contract`.

This step is automatic. Never ask the user to produce the JSON merely because v3 needs it. Ask a follow-up only when a genuinely ambiguous user choice would materially change the requested result.

Do not add a natural-language regex parser, keyword table, or holdout-specific branch. The deterministic boundary is the original UTF-8 request bytes plus canonical scene-contract bytes, exact ordered `prior_exposure_ids`, route, format, creativity, seed, and asset hashes.

`request_contract.prior_exposure_ids` is v3-only. It must be an exact unique ordered list and defaults to `[]`. Populate it only when the workflow was explicitly given a local exposure history; do not infer it from dataset frequency, shared telemetry, or the frozen holdouts. Ordering participates in canonical replay and must not be sorted, deduplicated, or rewritten after pack creation.

## Conservative Derivation Rules

- Copy explicit positive identity, scene, action, relation, prop, and environment facts into literal-bound `fixed` records.
- Mark a slot or event role `closed` only when the request contains an explicit negative phrase for that exact category. A closed record has no value.
- Leave unstated, uncertain, or multiply plausible semantics `open`; use `unknown` in the context profile. Open is eligible for bounded runtime selection, but is not an agent claim about the user.
- Every `request_phrase` must be a normalized literal substring of the original request. The request hash is SHA-256 of the exact UTF-8 request bytes.
- Never derive inner emotion, personality, relationship, intention, culture, nationality, age, gender, diagnosis, ownership, morality, or audience response from face, gaze, proximity, clothing, color, shape, name, genre, or convention.
- Never infer a body channel or capacity from visual stereotypes. Use only an explicit capability statement or an exact frozen embodiment profile whose ID and capacities remain visible in the contract. If profile resolution or capacity is uncertain, use a custom/open representation rather than inventing hands, a face, gaze, or locomotion.
- Preserve explicit user content even when it is unusual or semantically remote. A fixed prop or role consumes the same event, resource, bridge, and salience budgets; creativity cannot delete or excuse it.

`fixed` and `closed` express user constraints. Runtime-selected values for `open` slots remain traceable selections and must never be relabeled as user facts.

## Exact Shape and Closed Order

```json
{
  "schema": "subculture-illustration-scene-contract/v2",
  "request_text_sha256": "64-lowercase-hex",
  "identity_core": {
    "entities": [
      {
        "entity_id": "actor_01",
        "quantity": 1,
        "embodiment_profile_id": "custom_literal_actor",
        "capability_projection_mode": "declared_subset",
        "feature_facts": [
          {"id": "literal_actor", "request_phrases": ["adult mechanical caretaker"]},
          {"id": "literal_manipulators", "request_phrases": ["with two manipulators"]}
        ],
        "capabilities": [
          {
            "id": "manipulator",
            "capacity": 2,
            "state": "available",
            "source": "explicit",
            "source_fact_id": "literal_manipulators"
          }
        ]
      }
    ],
    "scene_facts": [],
    "forbidden_facts": []
  },
  "participant_bindings": [
    {"role_id": "actor", "entity_ids": ["actor_01"], "primary_entity_id": "actor_01"},
    {"role_id": "action", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "target", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "instrument", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "recipient", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "result", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "location", "entity_ids": [], "primary_entity_id": null},
    {"role_id": "phase", "entity_ids": [], "primary_entity_id": null}
  ],
  "slot_states": [
    {
      "slot_id": "expression",
      "state": "fixed",
      "value_ids": ["asymmetric_visible_display"],
      "request_phrases": ["asymmetric visible display"],
      "value_phrase_bindings": [
        {
          "value_id": "asymmetric_visible_display",
          "request_phrases": ["asymmetric visible display"],
          "semantic_anchor_groups": [
            {"alternatives": ["asymmetric"], "required_polarity": "affirmative"},
            {"alternatives": ["visible display"], "required_polarity": "affirmative"}
          ]
        }
      ]
    },
    {"slot_id": "pose", "state": "fixed|closed|open", "value_ids": [], "request_phrases": [], "value_phrase_bindings": []},
    {"slot_id": "action", "state": "fixed|closed|open", "value_ids": [], "request_phrases": [], "value_phrase_bindings": []},
    {"slot_id": "relation", "state": "fixed|closed|open", "value_ids": [], "request_phrases": [], "value_phrase_bindings": []},
    {"slot_id": "prop", "state": "fixed|closed|open", "value_ids": [], "request_phrases": [], "value_phrase_bindings": []},
    {"slot_id": "environment", "state": "fixed|closed|open", "value_ids": [], "request_phrases": [], "value_phrase_bindings": []}
  ],
  "event_roles": [
    {"role_id": "actor", "state": "fixed", "value_id": "actor_01", "request_phrases": ["adult mechanical caretaker"], "semantic_anchor_groups": [{"alternatives": ["mechanical caretaker"], "required_polarity": "affirmative"}]},
    {"role_id": "action", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "target", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "instrument", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "recipient", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "result", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "location", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []},
    {"role_id": "phase", "state": "open", "value_id": null, "request_phrases": [], "semantic_anchor_groups": []}
  ],
  "context_profile": {
    "theme_tags": [],
    "era_technology": "unknown",
    "tone": "unknown",
    "violence": "unknown",
    "social": "unknown",
    "scale": "unknown"
  }
}
```

The six slot IDs, eight participant bindings, and eight event-role IDs must appear exactly once in the order above. Participant `entity_ids` are sorted and unique, `primary_entity_id` is null exactly when the list is empty, and the actor binding is never empty. A nonempty binding is allowed only for the same fixed event role; a closed role cannot bind a participant.

State invariants:

- `fixed`: nonempty normalized value plus at least one literal phrase and 1..4 typed semantic-anchor groups per value or role;
- `closed`: empty value plus at least one literal negative phrase;
- `open`: empty/null value and no phrase;
- a fixed slot's `value_phrase_bindings` follows `value_ids` exactly, partitions `request_phrases` in exact order, and cannot reuse a phrase or normalized anchor across values; closed/open slots have no value binding;
- every semantic-anchor alternative is a literal substring of that record's own phrase, and the complete group must co-occur with its declared `affirmative` or `negated` polarity in one phrase; another value, role, clause, or global request span cannot lend authority;
- identity feature, scene, and forbidden facts: unique IDs and at least one literal phrase;
- `catalog_exact`: a known embodiment profile's full ordered capability projection with exact capacities and profile provenance;
- `declared_subset`: only individually valid explicit or exact-profile-derived declarations are exposed; it never fills an omitted capacity. Custom profiles must use this mode and may authorize positive capacity only through a reviewed literal-bound explicit feature fact;
- positive/available capacity is nonzero, unavailable capacity is zero, and profile-derived capacity must name the exact frozen profile and catalog value.

V1 scene contracts remain immutable historical source evidence. The current v2 oracle is a reviewed post-contract migration: every v2 row records its v1 source file, record index, raw-record hash, and request hash, plus its explicit revision reason. It may incorporate reviewed semantic corrections, but it is authored without candidate packs, runtime selections, audits, qualification outputs, generated images, or run ledgers. Never rewrite the v1 file, describe v2 as pre-implementation evidence, or use either holdout as a template for a new request.

## Literal Visual Realization

A fixed literal is not satisfied merely because its prose survives in the embedded contract. Data-owned `literal_visual_realization_profiles` connect reviewed literal authority to an observable candidate group. Every active profile uses this exact shape:

```json
{
  "id": "unique profile id",
  "source_slot_id": "expression|pose|action|relation|prop|environment",
  "mechanism_class_id": "closed reviewed mechanism id",
  "realized_facet": "slot-compatible visual facet",
  "candidate_group": ["sorted unique visual candidate id"],
  "participant_roles": [
    {"role_id": "actor|action|target|instrument|recipient|result|location|phase", "entity_quantifier": "primary|all"}
  ],
  "quantifier": "any|all",
  "enforcement": "selected|eligible",
  "literal_scope": "fixed_value_bindings|slot_phrases|request_text",
  "required_literal_groups": [
    {"alternatives": ["literal anchor"], "required_polarity": "affirmative|negated"}
  ],
  "owned_pixel_kinds": ["candidate-owned pixel kind"],
  "owned_resource_kinds": ["candidate-owned resource kind"],
  "selection_rank": 0
}
```

The source slot and realized facet must satisfy the closed compatibility table. Candidate IDs, participant role IDs, owned kinds, and selection rank are unique where the runtime requires uniqueness. Every active profile has nonempty participant roles and nonempty reviewed polarized literal groups; a data row cannot use an empty group as blanket authority for every fixed value in a slot.

Matched `selected` groups are reserved before the ordinary catalog proposal solver: `any` materializes exactly one eligible alternative and `all` materializes the complete group. Matched `eligible` groups prove the whole required eligibility condition without forcing selection. Ambiguous candidate ownership, wrong slot-to-facet projection, missing participants, incomplete eligibility, resource overflow, or per-facet/scene budget overflow fails closed; the runtime never truncates the requirement or overwrites one profile with another.

Every selected realization atom carries the exact profile ID, mechanism class, source slot, request hash, value-to-phrase bindings, and resolved `{role_id, entity_id}` owner references. Its resource claims are resolved against those owners, and its pixel obligations remain owned by that exact atom/candidate. A scene-global atom or another same-kind pixel item cannot satisfy an owner-joined realization obligation.

Context literal profiles are a separate, creativity-invariant overlay. They may add only their reviewed bounded bridge carriers; they cannot borrow the zero-distance core anchor, introduce an arbitrary content atom, or bypass the universal selection and resource budgets.

## One-Event Universal Selection

The v3 runtime locks identity and all fixed/closed slots, then selects exactly one connected event spine. It may fill open facets only when each selection is compatible with the same event and declared capabilities.

Fixed budgets do not vary with creativity:

- exactly one event root, primary action, and phase;
- one pose/support solution;
- zero or one gesture, relation topology, optional prop, and primary environment role;
- zero or one optional remote or high-load premise;
- no orphan atom, second event, or decorative prop with no event role;
- a claimed result requires one visible state or consequence trace;
- resource claims cannot exceed entity or scene capacity in the selected phase.

Every selected noncore atom must have a typed edge to the event. A prop needs an actor-to-prop-to-target, recipient, result, or environment relation rather than decorative presence.

## Creativity, Distance, and Bridges

Semantic distance is a typed seven-axis ordinal vector, not an embedding similarity or a quality score.

- `0.00 <= creativity < 0.25`: near target, no optional remote premise;
- `0.25 <= creativity < 0.75`: middle target, no optional remote premise;
- `0.75 <= creativity <= 1.00`: far eligible, at most one optional remote premise.

Use `0.5` for an ordinary brief. Pass `0.85` when the user explicitly requests creativity, originality, ingenuity, surprise, or an authorial treatment. Creativity changes target-band preference only. It must not change fixed/closed facts, hard-gate outcomes, candidate-count budgets, platform boundaries, or resource capacities.

Bridge obligations:

- near: at least one direct typed event edge;
- middle: at least two distinct bridge types covering entry/relevance and state/result;
- far: entry (`affordance`, `motivation`, or `identity_contrast`), mediation (`mechanics` or `ownership`), and exit (`state_change` or `consequence`), plus a separately visible core identity anchor.

A far selection is optional, not a creativity score. If identity, bridge, resource, salience, or pixel-evidence requirements cannot be met, select the closest coherent lower band and record `fallback_reason`. Never force novelty by weakening a gate or adding another event.

## Composition and Pixel Boundary

The pack's `universal_scene` is a pre-render plan. It must embed the full canonical `scene_contract` object, including all eight ordered participant bindings, not merely its hash or selected projections. Alongside it, the pack preserves exact working projections of `identity_core`, `slot_states`, `context_profile`, and every fixed event role so the solver and composer can consume compact typed views without losing the original contract authority. Participant ownership is projected only through validated role bindings and literal-realization owner references; it is never inferred from prose or candidate defaults.

Audit recomputes `scene_contract.request_text_sha256` from the exact UTF-8 `request_contract.request_text`, recomputes the canonical JSON SHA-256 of the embedded contract, and requires it to equal both `request_contract.scene_contract_sha256` and `selection_trace.scene_contract_sha256`. It validates the embedded participant bindings and requires the identity core, all slot states, context profile, and fixed event-role projections to equal their embedded-contract sources exactly. It never reconstructs any of them from prompt prose.

Compose a contiguous literal `scene_block_phrase` and bind the selected facts, every fixed slot value, event roles, atoms, bridges, evidence-required resources, salience, and consequence in `universal_scene_evidence`. A fixed slot uses one `{slot_id, value_id, phrase}` record per value, and the records must exactly cover the pack with no additions or omissions. See `composition-contract.md`.

### Authenticated Composition Carriers

`universal_scene.composition_carriers` is an additive semantic preflight with schema `illustration-universal-composition-carriers/v1`. It exactly covers the canonical scene records in six sections:

```json
{
  "schema": "illustration-universal-composition-carriers/v1",
  "identity_core": [
    {"fact_id": "fact_id", "polarity": "asserted_presence|asserted_absence|forbidden", "required_lexeme_groups": [["anchor"], ["second anchor"]]}
  ],
  "fixed_slots": [
    {"slot_id": "slot_id", "value_id": "value_id", "required_lexeme_groups": [["anchor"]]}
  ],
  "event_roles": [
    {"role_id": "role_id", "value_id": "value_id", "required_lexeme_groups": [["anchor"]]}
  ],
  "atoms": [
    {"instance_id": "instance_id", "candidate_id": "candidate_id", "required_lexeme_groups": [["anchor"]]}
  ],
  "bridges": [
    {"bridge_id": "bridge_id", "bridge_type": "bridge_type", "required_lexeme_groups": [["anchor"]]}
  ],
  "resources": [
    {"claim_id": "claim_id", "resource_kind": "resource_kind", "required_lexeme_groups": [["anchor"]]}
  ]
}
```

Each lexeme group is a nonempty set of normalized English alternatives. A valid linked composed-evidence phrase must contain at least one alternative from every group. Derive up to two distinct substantive anchors from the canonical semantic value when available; do not weaken a multi-anchor carrier to one generic word such as `visible`, `scene`, `detail`, or `object`. Carrier identifiers, values, polarities, groups, and order are selector-authenticated pack data; the composer cannot invent, delete, substitute, or relax them.

Ordinary identity features and scene facts use `asserted_presence`. A feature that owns a literal explicit unavailable/zero capability uses `asserted_absence`; every `forbidden_fact` uses `forbidden`. Absence and forbidden phrases must include an explicit negator scoped to all authenticated anchors in the same clause. Merely mentioning the concept, placing `no` in another clause, or relying on `negative_en` does not prove the scoped exclusion.

Composition-carrier validation is semantic preflight, not pixel proof. Every bridge and declared contact, support, path, state boundary, residue, display, or consequence still creates an inspection obligation at the pack-declared scales. Literal prompt and lexeme-group binding proves that the plan is stated; it does not prove the relation or polarity rendered, survived thumbnail reduction, or affected a viewer. Only inspection of the generated pixels can satisfy that obligation.

The current universal-scene delivery is qualified at the public 24-case planning boundary: deterministic selection, exact source-compiled obligations, composition evidence, audit replay, and legacy/photo regression. It has not executed a hidden 1,152-run generalization matrix or the six-case image holdout. Do not describe the delivery as hidden-unseen qualification or rendered-pixel proof unless those separate workflows are completed later.

Pack content, stored hashes, and `pack_id` are not trusted as a self-authorizing policy record. V3 audit reloads the local universal candidate, compatibility, and research-manifest assets, requires their hashes to match the pack, then canonically replays the selector with the embedded scene contract, exact ordered prior exposures, request, topic, format, creativity, seed, and those assets. The replayed `universal_scene` must exactly equal the packed scene before selected candidates, guard outcomes, resource capacities, weapon boundaries, and fixed/closed-slot policy are accepted. A caller cannot partially mutate the embedded contract or a projection, remove or substitute an atom, recompute the request/contract hashes and `pack_id`, and bypass the replay, cross-projection, or substantive gates.

## Legacy Boundary

V3 is the default. Explicit v1 and v2 calls are immutable historical replay paths:

- dispatch before universal assets are loaded or a scene contract is validated;
- reject `--scene-contract`;
- preserve their schema, pack bytes, negative prompt, pack ID, asset hashes, and qualification artifacts;
- never relabel v1/v2 prompt or render evidence as v3 evidence.
