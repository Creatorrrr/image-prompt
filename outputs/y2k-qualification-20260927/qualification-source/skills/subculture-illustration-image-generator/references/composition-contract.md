# Candidate-Pack and Composition Contract

## Candidate Pack

The default generator emits one additive `subculture-illustration-candidate-pack/v3` object containing every v2 field plus the universal scene selection:

- `pack_id` and exact `negative_en`;
- `request_contract` with original text, route, and mandatory visible intents;
- v3-only `request_contract.prior_exposure_ids`, an exact unique ordered list that defaults to empty and is preserved as selector input;
- one resolved `format_profile`;
- `visual_grammar` with exactly one primary visual atom and zero to two compatible supports;
- `authorial_contract`, `viewer_contract`, and `guard_contract`;
- every inherited v2 authorial, viewer, format, guard, and composition field without semantic weakening;
- a closed `viewer_contract.second_look_plan_contract` with carrier kinds, risk flags, and format-derived inspection-scale IDs;
- `universal_scene` with the full canonical `scene_contract`, including its eight ordered participant bindings, plus exact identity-core, six-slot, context-profile, and fixed-event-role projections, exactly one connected event, selected universal atoms and bridges, owner-resolved resource claims, authenticated `composition_carriers`, semantic-distance trace, and atom-owned future pixel-evidence obligations;
- `request_contract.scene_contract_schema` and `scene_contract_sha256` bound to the original request;
- `composition_contract.composed_schema = subculture-illustration-composed-prompt/v3` and exact `universal:<instance_id>` / `universal:<bridge_id>` chosen-candidate obligations;
- automatic-pass safety metadata unless explicit evaluation was requested;
- asset hashes and deterministic provenance.

Only `visual_atom` nodes may be selected as prompt candidates. Router, guard, and metric nodes remain metadata.

The explicit legacy runtime can reproduce `subculture-illustration-candidate-pack/v1` and `/v2` for immutable historical qualification. Those paths dispatch before universal assets are loaded, reject a scene contract, and preserve their exact schema, bytes, hashes, negative prompt, pack ID, and composed contract. New composition uses v3. Never rewrite or relabel v1/v2 packs, audits, results, or images as v3 evidence.

## Composed Object

Write one JSON object:

```json
{
  "schema": "subculture-illustration-composed-prompt/v3",
  "pack_id": "exact pack id",
  "prompt_en": "one standalone English image prompt",
  "negative_en": "byte-identical pack negative",
  "chosen_candidate_ids": ["route:...", "format:...", "visual:...", "universal:..."],
  "composer": "agent",
  "visual_evidence": {
    "evidence_type": "literal prompt phrase"
  },
  "authorial_grammar": {},
  "viewer_evidence": {},
  "second_look_plan": {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "exact selected proposal id, or null when creative development is not required",
    "reveal_phrase": "exact viewer and selected-proposal reveal",
    "review_scale_ids": ["pack-declared inspection scale"],
    "primary_carrier": {
      "carrier_kind": "material_boundary",
      "carrier_phrase": "literal prompt phrase",
      "protected_locus_phrase": "literal prompt phrase",
      "consequence_phrase": "literal selected-proposal consequence",
      "risk_flags": []
    },
    "fallback_carrier": {
      "carrier_kind": "environmental_trace",
      "carrier_phrase": "different literal prompt phrase",
      "protected_locus_phrase": "different literal prompt phrase",
      "consequence_phrase": "different literal selected-proposal consequence",
      "risk_flags": []
    }
  },
  "format_evidence": {},
  "universal_scene_evidence": {
    "schema": "illustration-universal-scene-evidence/v1",
    "scene_block_phrase": "one contiguous literal block from prompt_en",
    "identity_core_phrases": [
      {"fact_id": "pack fixed fact id", "phrase": "literal prompt substring"}
    ],
    "fixed_slot_phrases": [
      {"slot_id": "pack fixed slot id", "value_id": "pack fixed value id", "phrase": "literal prompt substring"}
    ],
    "event_role_phrases": [
      {"role_id": "actor", "phrase": "literal prompt substring"}
    ],
    "atom_phrases": [
      {"instance_id": "pack selected instance id", "phrase": "literal prompt substring"}
    ],
    "bridge_phrases": [
      {"bridge_id": "pack selected bridge id", "phrase": "literal prompt substring"}
    ],
    "resource_phrases": [
      {"claim_id": "pack evidence-required claim id", "phrase": "literal prompt substring"}
    ],
    "salience_phrases": {
      "primary_core_event_phrase": "literal prompt substring",
      "secondary_discovery_phrase": null,
      "controlled_rest_phrase": "literal prompt substring",
      "remote_carrier_phrase": null
    },
    "consequence_phrase": "literal prompt substring"
  },
  "reference_boundary": {
    "original_design": true,
    "named_style_references": [],
    "protected_ip_references": []
  }
}
```

Every evidence value that claims a visible result must be a nonempty scalar substring of `prompt_en`. Do not hide evidence in metadata.

`universal_scene_evidence` is additive; do not remove, rename, or weaken any v2 evidence field. Its ID lists must exactly cover the pack's fixed identity facts, every value of every fixed slot, present event roles, selected visual atom instances, selected bridges, and evidence-required resource claims, with no extra IDs. `fixed_slot_phrases` is keyed by the exact `(slot_id, value_id)` pair, so a multi-value fixed slot needs one record per value. Every child phrase must be a literal substring of both `scene_block_phrase` and `prompt_en`. Multiple IDs may share one concrete sentence when that sentence visibly proves each relation.

The pack's `composition_carriers` authenticates the minimum semantic content of those phrases. For each linked identity, fixed-slot, event-role, atom, bridge, and resource record, the phrase must contain at least one normalized English alternative from every `required_lexeme_groups` entry. Where the canonical semantic value supplies two or more substantive anchors, the contract preserves at least two groups; a generic phrase that mentions only one anchor does not pass. Identity carrier polarity is closed to `asserted_presence|asserted_absence|forbidden`. `asserted_absence` is reserved for a literal identity feature that owns an explicit unavailable/zero capability; it is not interchangeable with a forbidden scene fact. A forbidden or asserted-absence fact must be explicitly negated within the same clause as all of its authenticated anchors; `negative_en`, a distant `no`, or an affirmative mention is insufficient.

A literal-realization atom is not generic evidence for its facet. Its parameters bind one reviewed profile, source slot, exact value-to-phrase records, request hash, mechanism class, and resolved participant owners. Its resource claims must resolve from those owner references, while each required pixel kind must belong to that atom's exact candidate or quantified candidate group. Evidence from an unrelated atom, a global same-facet atom, or a same-kind scene pixel item does not satisfy the owner join.

Keep `scene_block_phrase` contiguous, at most 150 English lexical words and at most eight sentences. Use it to replace redundant exposition instead of appending a keyword dump. It must describe exactly one event spine; a prop, expression, gesture, or environmental effect without a causal event role is not valid evidence.

`carrier_kind` is one of `surface_state`, `material_boundary`, `isolated_contour`, `object_relation`, `environmental_trace`, `projected_form`, or `dedicated_panel`. Closed risk flags are `compound_anatomy`, `subscale_symbol_decode`, and `overlapping_multi_limb_projection`. Primary and fallback carrier, locus, and consequence phrases must differ after normalization. The fallback has no risk flags; a risky primary also requires a different fallback kind. Every declared scale becomes a later pixel-review obligation.

## Selection Rules

- Choose the pack's route and format IDs.
- Choose exactly the selected primary runtime ID and the selected support IDs; do not add unexposed siblings.
- Add exactly the selected universal atom and bridge IDs exposed in `composition_contract.required_chosen_candidate_ids`. Router, guard, and metric IDs may appear in pack trace only; they are never chosen visual evidence.
- Keep the primary meaning visually dominant. Supports may clarify action, relation, state, or format, but cannot introduce another premise.
- Preserve every fixed scene-contract fact and honor every closed slot. Bind all open-slot selections to the one selected event, respect capability/resource capacities, and keep the optional remote premise count at zero or one as declared by the pack.
- Preserve user-visible mandatory intents. A synopsis, lore label, market term, or emotion outcome does not cover a visual intent.

## Prompt Priorities

Write in this order unless the format contract requires a sequence:

1. original subject, fixed identity anchors, and decisive one-event spine;
2. actor, directed action, target, phase, and consequence;
3. selected universal atom roles, typed causal bridges, contact/resource evidence, and controlled visual rest;
4. first-glance hierarchy and second-look reveal;
5. primary second-look carrier, its distinct safe fallback, and the selected visible consequences they realize;
6. primary authorial visual atom and sparse supports;
7. authorial omission, edge/mark, and repeated motif/material rule;
8. format-specific crop, panel, safe-area, or scale behavior;
9. text/logo/IP and other visible exclusions.

Avoid camera-brand, lens, and photoreal capture formulas unless the user explicitly requests a hybrid medium. Illustration rendering language must remain dominant.

## Audit Boundary

The v3 audit verifies integrity, the full embedded canonical scene contract and its ordered participant bindings, exact unique ordered prior exposures, exact identity/slot/context/fixed-role projections, authenticated composition-carrier coverage and polarity, fixed/closed preservation, complete fixed-slot literal evidence, literal-realization quantifiers and owner joins, one-event connectivity, candidate eligibility, resource capacity, distance and bridge rules, sparse compatibility, literal universal/authorial evidence, format behavior, reference boundaries, and second-look plan binding. It recomputes the exact request-text SHA and canonical contract SHA before evaluating any projection. It rejects inner-state, personality, culture, age, intent, relationship, or capability claims that were not explicit in the request or validated by the frozen embodiment contract.

Canonical hash and `pack_id` verification detects accidental content drift but does not establish eligibility. The audit cross-binds the full scene contract to its request and every projection, independently reloads the local universal assets, requires byte hashes to match `asset_hashes`, and replays the selector from the embedded contract, ordered `prior_exposure_ids`, request/topic/format/creativity/seed, and those assets. It exact-compares the entire replayed `universal_scene` before re-evaluating selected guards, resources, weapon policy, and fixed/closed-slot constraints. Partially mutating a contract or projection, removing or substituting an atom, and recomputing stored hashes and the pack ID therefore cannot authorize an otherwise invalid selection.

An audit pass is planning evidence only. It cannot prove that an action, contact, support, state boundary, bridge, consequence, or carrier rendered legibly; that the image is historically original; or that viewers will respond or buy as intended. Those image claims require pixel inspection at every declared native and reduced scale.

## Research-Backed Moe Candidate-Pack v4

The historical `subculture-illustration-moe-element-plan/v1` remains available only for byte-stable replay. New work uses the additive `subculture-illustration-candidate-pack/v4` wrapper described in `moe-element-contract.md`: build and preserve the ordinary v1-v3 base pack, explicitly select one to three reviewed element IDs or complete aliases, interpret preference cues inside those elements, and expose the resulting real candidate and atom IDs in `composition_contract.required_chosen_candidate_ids`.

V4 applies the same sparse composition invariant globally, not once per element: exactly one selected moe node owns the governing event and no more than two nodes are supports. With one element, its evidence atoms may be the two supports; with two elements, the second element is a support and only one additional evidence atom remains; with three elements, the second and third elements are the two supports. The first explicit element owns the primary unless a higher-level request contract supplies a different reviewed order.

The composer must recompose the base scene, governing candidate, supports, and one compatibility bridge into a single event hierarchy. A period-separated label or clause dump appended after a finished prompt is invalid. Preserve the selected atom phrases in the auditable composition evidence, but use them as causal action, relation, wardrobe, pose, expression, prop, or consequence instructions. The wrapper cannot override the scene contract, selected universal event, negative prompt, safety metadata, or format prohibitions. If frame/camera requirements have no valid intersection, fail closed rather than claiming a still image proves time, relation, or optical interaction.
