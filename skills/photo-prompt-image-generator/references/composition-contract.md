# Composition Contract

New H-F2 material v2 uses `photo-validation-context/v1`, not a native candidate
pack. Its source-bound sampled materials are reviewed through the candidate
comparison procedure below and `h_f2_material_decisions`; do not add
`creative_augmentation_brief` or put material IDs into native chosen lists.
The validation context carries the existing core/controls/meaning/embodiment
contracts. Historical native V10 fields described below apply only to native
packs; old frozen records are never rewritten. See [installed H-F2](installed-h-f2.md)
for the per-query creativity windows, limits and recorded sampling seed.

For `adult_appeal.contextual_retrieval`, add the short conditional review and
baseline/alternative comparison inside `adult_appeal_brief` as described in
[contextual appeal](contextual-appeal.md). The general creative sample does not
replace this expression review. Adopted candidates still use the ordinary
interpretation/evidence fields; there is no required adoption count.

Post-core only. This reference must not participate in initial meaning resolution or baseline authoring. Follow `SKILL.md` for user authority, retry-only parent access, and the compact composition view. Full source packs remain the audit input; a view never replaces them.

## Native Candidate Pack V10: Historical Route

The serialized pack contract is `photo-candidate-pack/v10`. The generator retains `v9` as an input selector for that current contract; it does not identify a serialized V9 pack. The full wire name is also accepted; the shorthand `v10` is not a generator selector.

The native candidate-pack path supplies one external `photo-request-envelope/v1`, one `photo-authorial-core/v3`, and the pre-core creative-control snapshot with `--creative-controls-json`. The core binds the snapshot hash. The CLI returns V10 and requires the envelope, core, controls and embodiment review for every generation.

The request envelope is frozen before delegation. It contains the complete byte-exact requester text, its SHA-256, and one or more exact non-overlapping active spans. Multi-topic runs keep the same raw requester text and select only exact arm-local topic and governing global-modifier spans; an agent-authored per-arm paraphrase is invalid. The agent writes an initial core before reading any pack, profile, registry, project reference, fixture, or prior result. A retry may inspect only the parent hashes, preserved frozen fields, effective hard obligations, and relevant defect evidence allowed by `SKILL.md`; previous candidate inventories and optional prose remain unavailable. The core contains that same complete raw text, a context-resolved interpretation, concrete subject/setting/event, two to six visual priorities, a standalone 48–1,280-word English baseline prompt with a default recommended maximum of 720 words, optional request-scoped definitions, true requester exclusions, optional runtime-only labels, optional style evidence, `interpretation_provenance`, mandatory empty `unresolved_ambiguities`, and an `agent_prepack` provenance marker. V10 packs expose `photo-authorial-prompt-budget/v3`: 48 and 1,280 are blocking bounds, 720 is advisory, and required literal evidence expands the advisory ceiling by a 320-word headroom. Scene development, situational clarity, emotional credibility, and hard evidence may justify longer prose within the absolute bound. The prompt-budget contract is required and must be V3; archived artifacts retain their original budgets as evidence. Continue only through newly authored native inputs and current audits.

`photo-intent-lock/v2` makes requesting-user meaning the highest composition priority and permits property anchors on otherwise open dimensions. Such anchors add canonical `target` and `property` paths to the ordinary anchor shape. Changes on a partially locked dimension declare `affected_properties`; preserve both the literal evidence and its meaning. Whole-dimension prescriptions remain fully locked. It requires semantic anchors whose substantive source text is grounded in active requester spans and whose positive evidence is literal in the baseline. Every active span and every locked dimension has anchor coverage, and every locked dimension receives a distinct evidence phrase rather than reusing one generic phrase; `concept`, `subject`, and `event` are always locked, and any other fully prescribed semantic dimension must also be locked. Partially prescribed properties are anchored individually while their remaining choices stay open. Open and locked dimensions are disjoint. A v3 core may have zero or one open dimension; do not invent freedom for a precise request or repair. Every active span additionally has either a real requester definition or typed interpretation provenance. A requester definition's source must equal a complete active span and cannot be inferred from a bare term; bare or externally interpreted terms use `interpretation_provenance`. The generator rejects unresolved ambiguity, unknown or pack-derived fields, ungrounded definitions/exclusions/labels, incomplete span or dimension coverage, and any source bytes that differ from the envelope, then canonicalizes and hash-binds the envelope, request binding, intent lock, and core.

V10 packs include `authorial_composition.authorship_policy` with `contract_version: photo-authorial-authorship-policy/v2`, the source core and intent-lock hashes, and `allowed_dimensions` copied from the frozen open dimensions. Both `minimum_authorial_decisions` and `minimum_preserved_evidence_phrases` are zero: the baseline already carries the main artistic direction, and the final pass need not add detail or preserve incidental staging to meet a quota. The pack's `core_binding_contract` uses `photo-authorial-core-binding/v3` and binds `source_authorship_policy_sha256`. Every semantic anchor, required assertion, selected obligation, and repair relation remains mandatory under its existing audit. Explicit empty lists are valid for the two optional binding lists; supplied evidence is still literal in both prompts, and supplied decisions remain substantive and use distinct open dimensions.

Freezing the core records its independent origin and governing meaning. It does not promote every baseline sentence into a requester instruction. Refine or remove unbound agent-authored staging on open dimensions when that improves the intended impression, subject presence, or coherence. Preserve required evidence exactly and review the new full prompt for physical consistency. Material changes to bound meaning use the existing core rebuild or repair lineage; an aesthetic preference does not authorize erasing a meaningful interaction.

The initial baseline develops the scene's concrete circumstances, connected causes and responses, and meaningful moment before retrieval. Use a compact synopsis in `interpreted_intent` and realize the needed context in the photographic prose. During composition, judge candidates by how they develop that scene's purpose, relationship, consequence, or sense of place, as well as by their complete compatibility contracts. Strengthen context within open scope and record material developments in the existing `authorial_decisions`; neither the synopsis nor newly invented circumstances become requester locks. Read the resulting situation without its source keywords and preserve details that make its significance understandable. This authorial review adds no schema, candidate quota, or machine-verifiable artistic gate.

Semantic retrieval uses the core, not a broad default intent. The positive query combines the exact active requester spans after explicit-exclusion redaction, interpreted meaning, subject, setting, event, priorities, baseline, requester-definition expansion, interpretation resolutions, and optional style evidence. Research URLs do not enter the query. `user_exclusions` are only true requester negatives and never become positive search text. `runtime_forbidden_labels` remain positive retrieval/profile evidence while their literal spellings are prohibited only in the baseline/final/runtime prompt. Mandatory-intent audit uses the lock's positive anchor evidence rather than naively promoting every natural-language token, so a negation or connective cannot be inverted into a positive duty. `provenance.retrieval_query` records the core, envelope, active-scope, and intent-lock hashes plus contributing/redacted fields and recomputable query hash; the composed audit rejects mutation.

V10 separates meaning from exploration:

- `photo-semantic-clarification/v2` is deterministic across creativity and seed. Its required core row projects only frozen anchors and required assertion evidence; requester definitions remain immutable required evidence. The separate `authorial_direction` retains the initial interpretation and visual priorities as context without creating additional locks. Agent-chosen motifs remain replaceable within requester scope. Matched visual-profile meanings use `required`, `eligible`, `context_mismatch`, `requires_existing_adult_context`, or `requires_explicit_mechanism` applicability. Reject a mismatched optional row and continue. A correction to frozen governing meaning requires a rebuilt envelope/core/pack; use clear existing requester intent, and ask only when it is actually unresolved. It does not sample or add a new adult/safety route.
- `photo-creative-augmentation/v1` ranks the same hard-eligible advisory pool for a fixed core and generation seed, partitions it by relative relevance into `near`, `adjacent`, and `lateral`, then samples without replacement. Requested creativity permits near only at levels 0–1, near plus adjacent at level 2, and all three bands at level 3. Hard guards, negative bytes, explicit exclusions, identity/species/no-people, safety, and conflicts are invariant. Every transformed decision names distinct `affected_dimensions`, all of which must be open and subordinate to the intent lock.

`photo-downstream-intent-precedence/v1` applies the same boundary to non-candidate defaults. Each downstream rule declares its affected dimensions and is active only when all are explicitly open. Suppressed rules cannot leave a positive instruction, negative-prompt term, composed evidence duty, or render gate behind. Locked-dimension evidence reuses the matching semantic anchor exactly; other non-open evidence must already be literal in the frozen baseline. The audit recomputes this projection from the core, so removing the metadata cannot bypass it. This is topic-neutral: do not add named-archetype or named-expression exceptions.

`photo-negative-intent-guard/v1` applies a second topic-neutral boundary to both prompt surfaces. Current cores reject instruction-shaped blanket negatives in `baseline_prompt_en`, and composed audit rejects their reintroduction into `prompt_en`. Automatic `negative_en` is restricted to the maintained intent-neutral photographic-defect vocabulary; a semantic term is admitted only when, after removing a literal directive prefix such as `no`, it equals one complete true active-scope requester exclusion. Substring splitting, synonym expansion, and category broadening are forbidden, while identity-preservation controls require explicit identity-reference mode. Generic safety, taste, count, contact, action, relationship, expression, wardrobe, and genre suppressions are not automatic prompt material. Platform/tool policy remains enforced outside the prompt, and a necessary local boundary is written as positive geometry or visible state. The public guard binds the core hash, intent-lock hash, identity mode, exact requester exclusions, emitted terms, and fixed policies with a canonical hash; the composed auditor recomputes the entire object rather than trusting it.

Visual-profile clarification uses one registry-bound hybrid resolver after the core exists. Its generated sidecar contains exact lookup rows and semantic vectors derived from the same authored registry. Boundary-aware exact request hits may project as existing hard visual obligations. Embedding-only hits may project only as optional visual concepts and eligible clarifications; they cannot add prompt evidence or render gates until explicitly selected. The resolver is computed once and shared by all three visual-profile projections. Exact, negated, context-mismatched, and requester-defined meanings cannot be resurrected by similarity. The pack exposes neither vectors, scores, matched terms, match basis, nor rank.

The public V10 pack contains no relevance score, probability, sampler winner, fixed three-route hybrid answer, or candidate prose. Every creative row contains unordered concept terms and a semantic band only. A seed chooses material within the allowed range; array order is non-preferential. Ordinary slot retrieval uses grounded lexical queries; only a recorded embedding query establishes embedding-based visual-profile discovery.

The composed object binds its source, decisions and typed evidence:

- A normal new run supplies `--embodiment-review-json`. Its `embodiment_preflight` policy binds a reviewed baseline without changing requester assertions or retrieval. Supply a complete, separately hashed final `embodiment_review`; see [embodiment-preflight.md](embodiment-preflight.md). Missing or stale reviews and unresolved findings block composition. Missing embodiment policy is rejected.

- `authorial_core_binding` repeats the exact core and intent-lock hashes and preserves every anchor ID and anchor evidence. Under the v2 authorship policy, `preserved_evidence` and `authorial_decisions` may both be empty lists. Extra preserved evidence is an intentional literal commitment; avoid using it for replaceable staging. Record material final refinements, including simplification, as substantive decisions with distinct open dimensions and rationale. Every explicit `user_exclusions` and `runtime_forbidden_labels` phrase remains absent from the final prompt.
- `negative_intent_guard` is pack-owned and has no composer override. `negative_en` remains byte-identical to the pack, but equality alone is insufficient: every emitted item must be an intent-neutral defect, an exact requester-grounded exclusion, or an enabled identity-preservation control, and neither baseline nor final positive prompt may contain a blanket negative directive.
- `semantic_clarification_decisions` gives every clarification one typed decision. Ordinary rows use `applied` or `rejected`: required meanings cannot be rejected, and context-mismatched or adult-context-gated meanings cannot be applied. Core and requester-definition rows are immutable. Only `applied` and `rejected` decisions are accepted. Applied evidence is literal, requester evidence is preserved exactly, and runtime-only labels stay absent.
- `creative_augmentation_brief.decisions` decides every sampled creative row as `transformed` or `rejected`. At most three may be transformed. A transformed ID enters `chosen_candidate_ids` and receives interpretation, transformation, rationale, newly authored literal evidence with at least two content words beyond its source terms, and open-only `affected_dimensions`. Rejecting every creative row is valid.
- If `semantic_assertion_obligations` exists, `semantic_assertion_evidence` contains exactly `source_contract_sha256` plus an `evidence` map keyed by every required non-character assertion ID. Fields and phrases byte-equal the frozen core evidence and every phrase is literal in `prompt_en`; omitting the pack block, assertion, field, or phrase fails closed.
- If `render_repair` exists, `render_repair_evidence` contains exactly its canonical hash plus an evidence map keyed by every lineage repair ID. The interaction and recognition phrases byte-equal the frozen pre-retrieval core, occur literally in `prompt_en`, and are already owned by one required action assertion. The contract is object-agnostic: it preserves actor, object class, interaction state, and required or transitional contact while permitting only declared local repair axes. `relation_origin: parent_preserved` protects an unchanged parent relation; `requester_corrected` freezes an explicit requester correction after the new core is built. Removal, relocation, concealment, or transfer never counts as fidelity repair.
- If `character_response` exists, its specialized composed binding remains authoritative for the one required causal response assertion. The audit also compares its assertion ID, source spans, axes, and frozen evidence directly with the core, so removing or mutating the compiled contract cannot bypass the typed meaning.

## Model-guided candidate review

Read the bound requester spans, definitions/exclusions, locks, baseline, controls and full candidate detail together before adoption. A slot name, rank or eligibility flag is not semantic compatibility.

Apply this review to every considered candidate using the whole request, regardless of topic, language, wording, or whether a named concept was retrieved. Separate three judgments:

- **Meaning:** compare the complete definition, visible components, participants, properties and directed relations with requester meaning and frozen evidence. A shared word or broad impression is insufficient; an unfamiliar expression is not evidence of contradiction.
- **Applicability:** assess the actual prerequisites and joint effects against the final scene, open dimensions and property locks. A prerequisite may be supplied through an authorized open choice or an admitted joint bundle when the declared contract permits it. An unselected candidate, imagined context, or generic atmosphere cannot supply it. Preserve the candidate's full effects, including effects outside its slot.
- **Preference:** realize distinct compatible candidate changes in complete alternative prompts before comparing their contribution with the baseline. Follow the comparison procedure below; the absence of a defect in the baseline is not a preference decision. Keeping the baseline can be preferable after that comparison. A different agent-chosen action is not automatically a requester prohibition; determine ownership from the locks and evidence.

State material reasons in existing supported decision fields or concise run notes. Distinguish actual meaning conflict, unmet prerequisites or scope, unresolved recognition, and compatible options that were not preferred. Do not add new decision enums or interpretation rows for rejected ordinary candidates. If an eligibility explanation appears inconsistent with the evidence, consult the [retrieval diagnostic guidance](retrieval-contract.md#interpreting-applicability-diagnostics); keep the source pack and gates intact.

Use the resulting judgment with these reasoning outcomes and existing fields, not new schema values:

- **Adopt the complete meaning:** use existing selection/interpretation fields and satisfy all concept, relation, component, conditional and opt-in evidence. New prose is allowed; check joint effects with other selections.
- **Use independently justified generic attributes:** decline the contractual candidate and record a material refinement in `authorial_decisions` within open scope. Do not retain its distinctive compound meaning, omit its prerequisites, or relabel it as authorial to evade its contract.
- **Decline:** leave the optional candidate unselected, using an existing rejected decision where required. Record its actual conflict, prerequisite gap, redundancy, or comparative disadvantage. No replacement or extra final detail is owed; retaining the baseline is valid after the comparison procedure below.

For example, a daylight-only scene may use an independently justified gentle transition from its existing window light without adopting a softbox candidate or adding that apparatus. Required meanings remain binding; uncertain optional additions can be withheld without inventing new exclusions or claiming that mechanical audit guarantees semantic or image quality.

### Candidate-informed alternatives and comparison

Apply this procedure after retrieval and before choosing a new composed prompt. Keep the frozen baseline intact as a comparison option; freezing its independent origin does not make it the preferred final answer. Keep the same requester meaning, resolved controls, reference scope, prompt budget, and hard obligations across the options. Do not turn replaceable baseline staging into an extra requester constraint to avoid considering a candidate.

#### Creativity and reconstruction

Read the selected creativity definition from the bound `creative_controls` snapshot. It governs how actively candidate material may reshape the photograph as well as the requested interpretive freedom. Apply these directions within the existing open dimensions and property locks:

| creativity | Candidate-informed authoring and comparison |
|---|---|
| 0 | Realize the request directly. Compare compatible changes by whether they are needed for faithful meaning, legibility or consistency; retain only those needed changes. Novelty or an unused source is not a reason to expand the scene. |
| 1 | Explore restrained local additions, replacements and subtractions close to the requested direction. Prefer a change when its concrete expressive benefit justifies its whole-image tradeoffs. |
| 2 | Actively develop alternatives that reorganize connected open choices around compatible material. Compare changes to the authorial direction as well as local improvements; the existing arrangement need not remain the organizing center. |
| 3 | Actively develop whole-photograph reconstructions from requester requirements and compatible material. Treat the independent baseline as one possible realization; substantially replace its agent-authored staging when the new direction serves the requested freedom. Do not restrict exploration to fixing defects or adding to the existing scene. |

The preserved core meaning consists of every requester requirement, definition, exclusion, reference-use duty and effective hard obligation, not the smallest surviving amount of baseline prose. Do not promote an invented circumstance or preferred motif to a requirement merely because it supplies the baseline's story or hierarchy. Conversely, this guidance never demotes an existing frozen anchor, assertion, owner requirement or adopted contract. If correcting overbroad ownership would change a frozen binding, use the existing rebuild or scoped retry path; do not edit the core or required evidence in place.

Review all returned sources and perform the concrete-alternative comparison below at every level. These reconstruction directions change exploration and qualitative preference criteria without altering decision-coverage duties or source prerequisites, adding proposal/adoption counts or a rewrite-percentage quota, or changing the existing creativity-dependent sampling policy. At 2–3, assess the expressive value of reinterpretation itself as part of fidelity to the requested controls. Distance from the initial staging, removal of an optional motif, or the need to write a different scene is not by itself a comparative disadvantage. Coherence and legibility apply to the proposed new scene, not to keeping the old arrangement intact. Novelty alone does not establish a better photograph, and a precise request never gains invented freedom.

Baseline selection remains valid. At 0, candidate-specific findings may show that no change is needed. At 1, compare the actual local benefits and costs. At 2–3, first explore the viable reorganizations or reconstructions and explain their concrete tradeoffs; baseline completeness or familiarity alone does not justify rejecting them. If scope or prerequisites prevent such alternatives, state that evidence rather than manufacturing a change or claiming that broad reconstruction occurred.

#### Compare and record the complete options

Read every distinct returned H-F2 CID/RID and its complete source conditions and effects, paging the material view as needed. A duplicate source with the same hash may be reviewed once, with its originating queries linked to that review. Continue the existing review and decision coverage for considered native candidates, clarifications, and creative samples; their contracts and decision enums do not change.

Separate actual meaning conflict, unmet prerequisites or locked effects, and a contribution already fully realized in the baseline from artistic preference. Ground a conflict in the exact source requirement and relevant requester anchor, property, or missing prerequisite. Ground redundancy in the candidate's actual visible meaning and literal baseline evidence; shared terminology alone is not redundancy. Do not invent a contradictory alternative merely to reject it. If no distinct compatible change is available, record these candidate-specific findings and retain the baseline without manufacturing an alternative.

For a candidate that can make a distinct, compatible change within open scope, write its concrete realization in a complete standalone English alternative before choosing between that realization and the baseline. Compatible candidates may share an alternative when their complete effects form a coherent photograph; keep materially different realizations separate. Consider replacement, subtraction, and reorganization as well as additions. A candidate label, a list of possible changes, or an assertion that the baseline is already sufficient is not an alternative. This requires no fixed proposal count and no candidate adoption. A source already completely realized in the baseline needs no artificial extra change.

Compare each viable alternative and the baseline as complete photographs using the same applicable criteria: requester fidelity and required legibility, subject presence, situational clarity, purpose and connected causes and responses, emotional credibility, whole-image direction, visual hierarchy, and the resolved control strengths including level-matched reinterpretation. First check that the proposed realization can preserve the existing locks, literal evidence, full candidate conditions, and physical consistency. Then assess its benefits and tradeoffs without giving either the initial wording or novelty an automatic preference. Keep the comparison qualitative; do not add a scoring threshold or detail quota. Select the final prompt only after this comparison. If the final selection combines or materially revises compared options, update its complete text and comparative assessment before the existing audits.

Save `composition-comparison.md` beside the composed object as current-run authoring evidence. Record:

- The exact baseline path and hash, the frozen creativity level and its effect on the comparison, the requester-owned invariants versus replaceable authorial choices, and each alternative's ID and complete prompt text. Identify candidate CID/RID/source hashes and the actual open dimensions and properties changed by each alternative.
- Concrete strengths and tradeoffs of the baseline and each alternative on the same criteria, the chosen option, and why it serves the request better. When the baseline wins, identify what the candidate-informed alternatives would change and why those changes are less useful; a generic claim of completeness is insufficient.
- Each candidate's source meaning, the option in which it was realized or the evidenced reason no distinct compatible realization was possible, and its final use or non-use. Cite the actual source detail and relevant baseline, alternative, or final phrase. Distinguish incompatibility, unmet scope or prerequisites, genuine redundancy, and a compatible option that was not preferred. Shared findings may be referenced, but do not replace different candidates' reasons with a slot-wide rejection sentence.

For every returned H-F2 query/CID/RID occurrence, keep the existing exact `h_f2_material_decisions` fields. Put its candidate-specific finding, comparison reference, and final effect or reason for non-use in `rationale`; add no unsupported fields or new `use` values. `inspiration_only` describes an independently justified contribution actually retained in the final prompt, with its literal final evidence identified. A candidate explored only in an unchosen alternative is `skip`. These values never establish native whole-source adoption; all existing native selection, prerequisite, owner, and complete-source requirements remain binding. Use the ordinary native interpretation and creative-decision fields where their contracts apply. Final material refinements still belong in `authorial_decisions` and applicable scope declarations.

Before `compose-audit`, check that the returned material occurrences have decisions, that every preference-based rejection points to a concrete level-matched comparison, and that the chosen complete text matches `prompt_en`. This is an authored review requirement, not a new wire schema or a claim that the mechanical auditor can judge artistic superiority or reconstruction strength. Keep the comparison document outside the frozen core, retrieval queries, and runtime prompt. Apply the expanded authoring guidance to new compositions; archived snapshots retain their embedded control definitions and original validation contract and are not rewritten or required to acquire new prose. Preserve the existing hashes, evidence, negative policy, candidate limits, and audit commands; refresh the required final embodiment review when the chosen prompt changes. An unchosen alternative does not create an adopted obligation or authorize rendering. Rendering any option still requires the user's existing image-generation scope.

### Explicit existing-owner selection

An `owner_selection_requirements` descriptor identifies a manually reviewed
source target that can apply to a compatible existing owner. Read its full source
and choose the actual entity from the independently frozen owner graph. Required
`subject/entity.presence` uses type `entity.presence/v1`, value `present`; each
specific material, anatomy or other prerequisite still needs its own exact
frozen fact. Presence and a property lock never grant permission to change that
property. A descriptor may include optional children; those children contribute
no duty until explicitly selected.

For actually adopted selector nodes, add this composed field before audit:

```json
{"owner_selections": {
  "schema": "photo-request-owner-selections/v1",
  "core_sha256": "<frozen core canonical_sha256>",
  "owner_graph_sha256": "<canonical frozen witness graph SHA256>",
  "entries": [{
    "candidate_id": "<source CID>",
    "realization_id": "<selected actual RID>",
    "meaning_sha256": "<descriptor meaning_sha256>",
    "qualification_sha256": "<descriptor full-proof qualification_sha256>",
    "bindings": [{"target": "<source target>", "owner_id": "<actual frozen owner ID>"}]
  }]
}}
```

The graph hash is
`photo_candidate_corpus.digest(photo_semantic_evidence.frozen_witnesses(core)['graph'])`.
Entries must exactly cover the actually selected selector-node closure, with
1–64 entries and 1–32 unique target bindings per entry. Use the full-proof hash
from the descriptor. Keep fixed-role bindings unchanged and omit unused optional
children. All selected effects and receivers resolve through this same mapping;
explicit owner equivalence identifies one actual entity, while `part_of` retains
distinct part ownership. For the union of all chosen candidates and their
actually selected child realizations, assignments on the same actual owner,
dimension and property must agree in typed value, operation and actual receiver
set. This includes repeated assignments within a source and shared children.
Prerequisite old values remain distinct from selected new effects. Keep
conflicting choices separate or use a source-authored explicit aggregate value;
do not silently merge them. An owner choice never grants permission to change
a frozen property.

Keep the original public pack unchanged. A passing audit emits its own
`native_owner_resolution`, bound to the exact pack, composed text, source
qualifications, core and owner graph. Do not supply that receipt as composed
input. After a successful `compose-audit`, a different owner mapping requires a
new run; a failed audit can be corrected. The workflow binds the receipt to the
render request and independently recomputes it before execution.

### Conditions on the selected source owners

Some sources require a relationship between their actual selected owners. For
example, two existing hands can belong to the same existing holder while
remaining distinct parts. Read and satisfy those conditions as well as each
owner's precise prerequisites. A selected owner, an owner name or a matching
material does not establish a part relation, distinctness or another owner's
identity. Only independently frozen facts and explicit graph relations can do so.

The authored source may express this with `photo-native-source-guards/v2`.
Each endpoint is exactly `{kind: "source_target", candidate_id: "<CID>",
target: "<source-local target>"}`. The actual selected realization and its
audited owner mapping resolve that address. Rules support `part_of` or
`disjoint`, an exact typed frozen value, an exact frozen entity relationship,
and complete established-scope preservation. Explicit equivalent owner IDs
refer to the same entity; part ownership remains distinct. The older v1 guard
format retains its literal fixed-role meaning.

Source and branch conditions can address themselves and required direct
children. A member-pointer condition can address its parent and that selected
child; the child's presentation condition addresses the child and its required
direct children. Optional unselected children supply no owners or conditions.
Keep the declared source conditions intact. Do not author internal condition
frames or amend the public pack, binding, frozen graph or core to make a cue fit.
The final audit reconstructs the selected closure and condition provenance.

An unresolved owner or child realization can remain available for review during
discovery. Adoption and permission checks require its complete actual mapping
and every applicable condition to pass. A resolved relationship failure cannot
be treated as an unresolved choice. Preservation checks include the whole
selected effect and receiver scope, including selected children, and still
require the final literal preservation evidence.

### Authorial binding shape

The example below retains a complete baseline without additional refinements under the v2 policy. Add a decision only for a material final refinement.

The composed JSON must include the exact pack ID and negative, candidate choices, all clarification decisions, creative decisions, and:

```json
{
  "authorial_core_binding": {
    "source_authorial_core_sha256": "<exact core hash>",
    "source_intent_lock_sha256": "<exact intent-lock hash>",
    "preserved_anchor_ids": ["<every semantic anchor id exactly once>"],
    "preserved_evidence": [],
    "authorial_decisions": []
  },
  "composer": "agent"
}
```


## Candidate Pack V10

The generator returns a one-pack JSON array. Generate and audit one pack at a time. The default pack carries `contract_version: photo-candidate-pack/v10`; `pack_id` is the first 16 hexadecimal characters of SHA-256 over canonical JSON with `pack_id` replaced by `null`.

V10 makes the agent the final author rather than a phrase assembler. Candidate labels, long candidate terms, photographic suggestion phrases, craft prompt fragments, and render-blueprint prose are not exposed as reusable final wording. Candidate surfaces contain unordered `concept_terms` and no sampler-selected flag, probability, weight, score, slot-level selected answer, or candidate-ID `covered_by` answer key. Candidate and route order is seed-shuffled and non-preferential: use individual technical, identity, or material terms selectively, but invent their relationship, causality, timing, and final prose. `authorial_composition.variation_lens` is a seed-varying abstract lens, not a mandatory phrase or scene.

`photo-visual-intent/v1` is a separate post-core, pre-pack input for non-substitutable visual meaning. Use it only after the baseline hash exists and only when the request explicitly defines exact pose geometry, physical support, simultaneous expression components, body-region salience, an embodied state transition, or a behavioral archetype. A row may omit `profile_id`; the generator then resolves exactly one direct registry profile from its exact source text, failing closed on zero or multiple matches. An explicit ID remains supported for post-core maintenance and replay. A V10 pack hashes that input into `photo-visual-obligations/v1`; it never converts these hard duties into optional candidate IDs. Related objects, generic styling, reference appearance, or excluded homonyms cannot hard-activate a profile. Strong indirect component combinations and weaker nearby cues instead create unordered, non-ranked `photo-visual-concepts/v1` candidates with no matched terms, score, or routing reason. The composed object must include `chosen_visual_concept_ids` when such candidates exist, even if empty. Selecting one promotes its immutable opt-in obligation to the effective hard contract; not selecting it adds no prompt or review duty. A requester definition has precedence and remains local to that request. If an activation label is unsuitable for the runtime prompt, use `coverage_assertions` to bind its exact mandatory-intent key to one safe component phrase; definition-only runtime profiles still require every other component independently.

`japanese-subculture-photo/v1` selects one concrete family from the existing scoped subculture taxonomy and requires at least two literal visible cues. A style label alone fails, as does converting the style request into Japanese nationality, ethnicity, or facial morphology. Strong-theme candidates named by its guard stay absent unless the original request explicitly names them. Prompt audit proves literal binding only; pixel survival is reviewed separately.


V10 keeps only reproducibility, user-input, reference-control, and safety provenance. It withholds expanded argv, private ranking and retrieval internals. Its public `quality_profile` carries only request-critical subject kind; photographic integration categories and craft dimensions are unordered optional pools with no selected axis, strategy, refinement, score, or matched-facet answer key.

Sampler-built atomic scene groups are also private routing in V10. Their public projection is an `optional_inspiration_group` containing only non-ranked `allowed_candidate_ids`; the group name, selected entry, semantic entry-ID lists, scene-tag winner, and required-adoption rule are absent. Every group and every member may be rejected.


The audit rejects a changed pack, a list containing zero or multiple packs, a missing composed field, a non-agent composer, an empty required candidate selection, a changed negative prompt, failed concept gates, and a non-pass safety record. Optional candidates may all be rejected.

Candidate caps are four candidates for core slots, two for support slots, and 64 ordinary slot candidates overall. Every ordinary candidate comes from guarded core-derived retrieval, with `applicability.source: frozen_core_slot_contract`. The pack carries no preselected candidate or required slot count.

A resolved render blueprint remains private source material in V10. The public pack exposes only abstract scene functions, relationship stakes, genre anchors, visual-evidence types, and diegetic provenance. It never exposes the source subject/action/location/prop prose, blueprint ID, hash, or sibling inventory. The composer supplies a new `authored_scene` with a governing premise, artistic rationale, four newly written prompt-bound atoms, and at least two distinct interpretive choices.

The frozen `creativity=3` value may add `creative_exploration`. Its contrast rows never add, remove, or reorder candidates: each `candidate_id` is an already exposed `frozen_core_slot_contract` option that clears conflicts and exceeds the declared feature-distance floor. V10 removes the prior `replaces_candidate_id` and relevance-rank answer key; use no more than `composition_guidance.use_at_most` mutually compatible options by artistic judgment. The field is absent below the activation floor.

The same level adds `creative_direction`, an agent-level creation and selection contract with no topic examples or new candidates. It requires an ordinary-baseline critique, at least four proposals using distinct concept operators, exactly one selection, one rule change, at least two visible consequences, a staged reveal path, and a concrete authorial grammar. Its evidence fields must be literal in `prompt_en`; signatures from unselected proposals are forbidden. See `creative-direction-contract.md`. The field is absent below the activation floor, so ordinary composed prompts retain their existing contract.

All advisory V10 candidates are optional, including optional scene-group, visual-proposition, photographic-integration, and photographic-craft candidates. Hard identity, species-family, enforced role-scene, and safety constraints remain required when declared. For every chosen non-augmentation ID, `candidate_interpretations` contains exactly one row with an artistic interpretation, a transformation description, and literal newly authored prompt evidence. The evidence has at least four content words and introduces at least two content words beyond the source concept terms. An empty `chosen_candidate_ids` list is valid only when the authored request and hard contracts need no candidate.

A frozen `viewer_experience` control adds the separate topic-neutral `photo-viewer-experience/v1` composition contract. High creative-direction runs include it automatically. The contract it requires one viewing context, audience-literacy scope, primary viewer need, scalar intended experience, visible first-glance hook, actor/action/target/consequence, attachment and reinspection conditions, and one commercial objective. Only declared visible evidence is literal in `prompt_en`; the intended response remains a hypothesis. See `viewer-experience-contract.md`. Ordinary requests without an explicit audience, affect, attachment, commercial, subculture-response, or creative goal retain the previous pack shape.

## Required Composition Behavior

- When `contract_version` is `photo-candidate-pack/v10`, validate `request_binding`, `authorial_core`, `intent_lock`, complete active-span/locked-dimension coverage, interpretation provenance and empty unresolved list, recomputed retrieval provenance, `intent_preservation`, `authorial_core_binding`, every semantic-clarification decision, and every creative-augmentation decision. Also validate its typed assertion contracts and authorship policy when present. Candidate choice never outranks the frozen core. A material meaning change requires a rebuilt run; rejecting an optional mismatch does not.
- Use every `mandatory_intents[].text` as literal or faithfully translated visible content.
- `mandatory_intents` contains required positive user meaning. Read `intent_contract` for the complete typed request: `user_requirement` and `additional_requirement` are required, `role_requirement` and `soft_guidance` are advisory, and `negative_requirement` is excluded.
- `audit_terms` and candidate labels are discovery aids, not proof of user-intent coverage.
- `coverage_assertions` may map an exact mandatory-intent key to one or more phrases. Every phrase must occur literally in `prompt_en`.
- Choose IDs only from `slots`, proposition candidates, or the adult-appeal candidate inventory included in the pack.
- Choose only candidates with `applicability.status: eligible`.
- Do not choose both sides of a hard conflict.
- Preserve `negative_en` exactly, including `null`.
- Set `composer` to `agent`.
- When `viewer_experience.enabled` is true, add the composed `viewer_experience` object and obey its conditional evidence rules.
- When `visual_concept_candidates.enabled` is true, add `chosen_visual_concept_ids`, even when empty. For every selected ID, treat `opt_in_contract.obligation` exactly like an active hard obligation: supply its semantic evidence fields, obey its `runtime_expression.default_mode`, and include its gates in the derived effective checklist. The pack remains immutable; audits derive the effective contract from pack plus composed selection instead of trusting a review's self-reported gate list.
- When V10 `creative_augmentation.enabled` is true, add `creative_augmentation_brief`, decide every sampled ID, choose only transformed IDs, and keep the maximum of three. Every transformed row declares distinct `affected_dimensions` contained in `intent_lock.open_dimensions`; rejected IDs stay absent and source-term-only evidence fails.
- When V10 `semantic_clarification.enabled` is true, add exactly one decision per clarification, apply every required meaning, reject inapplicable senses, and bind component evidence without runtime-only labels. A change to governing meaning requires a new frozen core.
- For each ordinary V10 `chosen_candidate_ids` entry, add one `candidate_interpretations` row. Do not add rows for rejected candidates or for transformed augmentation details already documented in `augmentation_brief`.
- For a chosen candidate with `context_prerequisites.contract_version: photo-candidate-context/v2`, add `context_review.requirement_evidence` to that interpretation or its transformed augmentation decision. Each witness names the supplied `requirement_id`, one declared `fact`, `state`, literal final `prompt_evidence`, a semantic `reason`, `origin`, and actual `affected_dimensions` and `affected_properties`. An `any_of_all` condition needs every fact in at least one declared alternative; an unrelated candidate's tags do not supply a fact. A `retained` witness occurs in baseline and final prose and adds no effects. An `authored` witness stays within open dimensions and property locks. Missing or unsupported evidence blocks that optional adoption; rejecting the candidate requires no context witness. Source hashes and literal bindings validate the record, while the composer judges the evidence's meaning.

## Meaning and Coherence

`intent_contract` and `coverage.intent_constraints` describe typed source, polarity, subject category, domain and negative-presence constraints. Excluded and advisory rows never become positive mandatory prose. Required typed assertions and request-scoped visual obligations preserve their independent authority.

Every composed object must bind `global_retrieval.canonical_sha256` as `global_retrieval_sha256`, in addition to `pack_id` and the frozen intent-lock binding. Audits recompute the ordinary candidate inventory from its authored source. Candidate adoption is optional, including for a singleton inventory. Retain the independently written baseline when the comparison procedure supports that choice, whether optional material is incompatible, unrealizable within scope, or valid but less useful.

## Moe Response and Event Timing

For V10 `character_response`, compose the frozen actor, baseline, trigger, relationship target, primary action, affect leak, visible response, immediate consequence, and continuity as one coherent frame. Preserve the declared event phase and same-target, contrast, or temporal relations. Framing and lighting may make them legible only when those dimensions are open. A named archetype never adds a fixed gaze, facial landmark, pose, object placement, or camera direction. See `moe-response-contract.md` for the typed binding.

When a hard visual obligation has several components, all must coexist in the same saved image. Evidence split across retries or hidden in metadata is insufficient. Preserve the audited negative bytes and requester-controlled sexual tone; generic defaults never change a closed dimension.

## Quality Layers

The frozen `creative_controls` record guides initial and final authorship. Keep its intended experience, creativity, reference scope and active surreal/trend direction coherent; do not append the same treatment again. An adult-axis `realization: baseline` may retain already-authored literal evidence without an extra styling detail. See `hybrid-augmentation-contract.md` for versioned scope and property declarations.

V10 publishes `quality_profile.profile_id: authorial` and only request-critical subject-kind facets; internal profile and facet winners remain private.

Use `photographic_integration.category_candidates` as a non-ranked pool and artistically select any fitting categories; use one visible `visual_proposition`, then at most one or two optional `photographic_craft.dimension_candidates`. These pools have no preferred selection. These are quality signals, so the audit reports omissions as warnings.

`artistic_final_touch` is disabled for most profiles. When enabled, use the sentence or equivalent terms; it does not have to be the exact final suffix. It is surface craft, not evidence of a distinct authorial point of view, and the creative-direction audit rejects using its fixed sentence as authorial grammar evidence. Never add the documentary imperfection formula to product, food, architecture, nature, or polished editorial prompts by default.

## Safety

Default safety uses the pack's ordinary report mode and adds no approval wait. Run `--safety-evaluation` only when the user explicitly asks for a safety review. It changes only the report mode and lists the frozen eligibility constraints; it does not grant extra authority and does not replace platform or image-tool policy. Safety evaluation and platform enforcement must not manufacture prompt semantics: unless the requester explicitly excluded an element, do not convert a safety transform into `No ...`, `never ...`, or an automatic `negative_en` term. Prefer a narrowly positive visible state when one is needed, and leave non-prompt enforcement to the tool and pixel-review boundary.

Adult-appeal axes are composition inputs, not safety transforms. Saved adult-axis defaults and ordinal definitions live in `precore/creative_controls.json`; V10 emits those defaults only across explicitly open dimensions. Explicit controls may override or disable either axis while remaining bound by the frozen requester core. Permit `sensual` and `fetish` simultaneously, retaining subject originality, visible agency, and combined styling-pose-framing-camera review whenever active. Require a literal `adult` subject phrase only at effective `sensual` intensity 2 or 3; at 0 or 1, `adult_subject_phrase` may be omitted regardless of `fetish` intensity. Preserve requester-owned age and applicable character-response meaning. A project audit failure must be fixed before generation; a project pass never overrides platform enforcement.
## Optional Candidate Semantic Units and Bundles

V10 packs must declare `candidate_semantic_surface_version: photo-candidate-semantic-surface/v1`. Their unordered `concept_units` preserve short internal relationships; `concept_terms` carries the same units for the ordinary authorship audit. Interpret these units in a newly authored scene. Source words, member IDs, and associated profile IDs are not a selection answer or a final-prompt template.

When selecting a candidate that declares `relations`, add `relation_evidence` to its `candidate_interpretations` row, mapping every relation ID to a literal phrase in the final prompt. A transformed creative-augmentation decision carries the same mapping in that decision instead. Preserve each relation's direction, subject, and object.

`candidate_bundles.candidates` are optional complete realizations. Read the full detail view before adopting one. Select its `bundle:*` ID and provide ordinary artistic interpretation/transformation evidence plus `component_evidence` for every component ID and `relation_evidence` for every relation ID. Each component group requires at least one of its authored alternatives; all groups must remain represented in the same coherent realization. An unselected bundle adds no obligation. Its `associated_profile_ids` remain advisory and never automatically activate visual profiles.

Some bundles satisfy member prerequisites only through joint adoption. Their nested members do not become standalone choices unless those candidates are independently present and eligible in the ordinary pack. The generator and auditor recompute joint admission from the frozen core and the same skill source snapshot; unsupported external context, unknown dimension ownership, locked dimensions, conflicts, or modified source contracts fail closed. Bundle selection requires prompt-level evidence; it is not a new claim of successful pixels or user acceptance. Earlier serialized v9/v9 surfaces retain their original reading contracts.


Every pack requires current authorship V2, binding V3, budget V2, semantic-surface V1 and embodiment preflight V1 markers. Missing or historical policy markers fail validation. The current composer view is V2 and always binds the original full pack hash.
