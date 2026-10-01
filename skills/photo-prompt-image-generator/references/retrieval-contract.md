# Retrieval Contract

Bound v6 adult-axis search uses `photo-contextual-appeal/v2`: one lane keeps the
baseline context, while the alternatives lane uses active requester spans,
requester definitions/anchors and the frozen control meanings without copying
agent-selected wardrobe. BM25F and available embeddings rank the compatible
corpus, with soft fusion across whole directions, construction/material and
portrayal/scene relations. Those are expression scopes, not aesthetic membership
classes. No preset list, axis tag or item-specific intensity threshold admits a
candidate. Scope/property locks and requester exclusions still apply.

Up to two short requester-owned event/relationship/action/situation anchors add
relation-focused queries; absent anchors produce no extra queries. Configuration
assignments are not search text. A bounded request-overlap preference helps scene
relevance after rank fusion; it is neither an applicability proof nor a source-ID
boost. Inspect every candidate's conditions before adoption. Role, setting,
relationship and timing effects are admitted only when explicitly open.

The pack records actual keyword/hybrid lanes and semantic coverage. Scores
identify candidates for contextual review; they never establish sensual or
fetish meaning. `contextual_usage` examples, ordinary readings and limits are
composer context only, excluded from positive embedding/keyword fields.
See [contextual appeal](contextual-appeal.md) for how alternatives are used.

Post-core only. Load this reference for retrieval diagnostics or maintenance; ordinary composition starts from the compact pack view and the relevant composition contracts.

## Frozen query and index ownership

The retrieval query combines the exact active requester spans, with true requester exclusions redacted, plus interpreted intent, subject, setting, event, visual priorities, baseline prompt, requester definitions, interpretation resolutions, and optional style evidence. Runtime-forbidden labels remain meaning-retrieval input. Research URLs are provenance only. `--concept-lock` is normally derived; every supplied value must byte-equal the active spans in order.

V6 projects those frozen fields into a versioned BM25F query. Tokenization is NFKC/casefolded and boundary-aware: conservative Korean suffix stripping may recognize an inflected whole term, while an unrelated word containing the same characters cannot activate it.

## Slot-focused candidate lookup

Default `--slot-retrieval-policy stable` preserves the existing field-focused BM25F fusion, global/focused intersection and sampler-selected availability. It repairs frozen-subject category normalization before eligibility and adds private inactive-slot/selection diagnostics. The existing narrow-pool ranking branch remains in use when expansion is solely due to normalization; those additions cannot alone switch it into the broad-search intersection branch. Public retrieval metadata includes policy/experimental markers, so pack bytes and pack IDs may differ from earlier revisions. Candidates newly admitted by normalized eligibility must still pass declared/primary-context guards; this does not globally refilter the legacy pool. Direct adult woman/man noun phrases are recognized only at the subject head, not inside descriptions of statues, photos or nonhuman subjects; explicit no-person constraints still take precedence. A hash-validated pre-core snapshot can also supply its explicit requester-owned context.no_people to the existing slot, bundle and optional adult-inventory guards. In an existing semantic context only people-related fields are updated; domain/scoped routing and other intent-source policies are preserved. This is additive: false or absent context cannot cancel user exclusions, nonhuman category alone creates no ban, and stale/mutated snapshots are rejected. The legacy English no-people parser is not widened by this change. It does not silently turn on the new query weights or wider-union reranker.

`--slot-retrieval-policy evidence-union` explicitly opts into the experimental `photo-slot-query-fusion/v2`: whole-scene and focused BM25F lanes plus the existing whole-scene embedding vector when available. The focused projection starts with slot-relevant frozen core fields and adds source-bound baseline clauses, literal matching-dimension anchors and required typed assertion evidence. Its `photo-slot-meaning/v1` record preserves role, state, relation evidence and declared locked/open ownership; it neither reads the pre-core feature-selection audit nor creates new meaning or locks. Negative/contrast, depicted and carried-object spans are retained diagnostically but excluded from positive evidence. Camera subslots use separate photographic cues while ownership follows the v3 camera/framing dimensions; literal evidence matching is case-insensitive. The English grammatical projection is deliberately partial. Unrecognized prose remains in the whole-scene lane; this is not a general multilingual semantic parser.

Experimental slot queries cap total repeated-token contribution at 1 and damp articles/copulas to 0.15. Negation and relational words (including off, without and under) remain intact. These are explicit query-time options: document tokenization, generated index recipes and other callers' default scores are unchanged.

Search starts with the recorded sampler pool and may expand the same-slot corpus only after request, domain, facet, subject, declared context/primary-context and exclusion guards. Forced, critical and atomic pools stay closed and bypass the experimental reranker. Frozen subject routing supplies category evidence before eligibility checks; a sampler-selected human is not proof of a human request. Normalization-only stable additions must be focused hits and are appended in fused relevance order, never raw catalog order. Each lane is bounded at `max(32, 12 × slot budget)`, capped by eligible corpus size. The bounded union replaces destructive global/focused intersection. Existing catalogue vectors and authored positive relation cues are reused; this stage never calls an embedding API or paid reranker. Private query-vector keys bind provider, model, dimensions and query hash, with at most 64 recent cached vectors; unknown or mismatched spaces do not activate the dense lane.

Relevance reranking combines rank fusion with bounded, length-normalized evidence overlap. The sampler-selected candidate remains a non-preferential member within the existing pack budget, preserving pointer coherence and creative-exploration/scene-contract inputs. Partial grammatical checks demote suspected inactive-source or explicit multi-token-exclusion conflicts without deleting eligible rows; distinct entities, negated emission, off-camera/off-white and external-light shadows must not be conflated. On an explicitly open dimension, an authorial baseline choice cannot itself penalize an alternative: conflict evidence requires requester evidence. Active requester spans are considered on locked dimensions too. Demotion reorders the retrieved union; zero-hit sampler rows remain fallback alternatives, and selected membership is still reserved within budget. These checks are incomplete and do not replace the composer's joint review or existing audit gates.

In the experimental policy, relevance selection stays separate from open-dimension creative exploration and the later public `seed_shuffled_non_preferential` order. Candidate budgets remain unchanged. Public metadata contains source/query hashes and source fields, not scores, ranked IDs or query evidence. Private `slot_retrieval_diagnostics` distinguishes catalogue size, guarded eligibility, bounded-lane union, conflict demotion and final budget loss. Frozen evidence in an inactive slot is diagnosed without activating the slot past its preset/subject guards. A coverage status of `unjudged_catalog_coverage` is intentional: candidate availability and semantic gold coverage require separate evaluation, and inactive/unsupported slots are not ranking failures.

For v6 typed request routing, subject category and exact subject-entry routes read the frozen subject field. An animal-ear modifier in that field is not treated as a standalone animal subject. Authored human role aliases such as witch can supply the human category when the field does not literally say human; a nearby person in the event cannot reclassify an animal subject.
For subject candidates only, an explicit adult human in the frozen core may expose a human role tagged `adult` when that tag describes age alone. Adult-content and suggestive tags retain their existing guards.

Visual-profile retrieval uses one generated index derived from the single authored registry: boundary-aware exact lookup rows, a fielded BM25F derivation, and one embedding vector per profile. Runtime rejects stale registry hashes, BM25F recipes or policies, and semantic text recipes. One private resolution is projected into `visual_obligations`, `visual_concept_candidates`, and `semantic_clarification`. Scores, vectors, matched terms, and rank remain private. This lookup is independent of creativity and seed.

The experimental policy is not a recommended default: frozen development final-pack evaluation found higher primary-slot recall alongside lower camera recall and increased known conflicts. Preserve those findings rather than equating wider candidate recall with improved selection. Callers constructing packs directly may set `data[SLOT_RETRIEVAL_POLICY_DATA_KEY] = "evidence-union"`; otherwise they receive the stable policy. Both paths retain public non-preferential shuffling and existing composition/audit authority.

## Meaning authority

Exact request terms may retain their declared request-scoped hard meaning. A profile found only by BM25F, embedding similarity, or reciprocal-rank fusion is optional and creates no prompt duty or render gate until explicitly selected. A requester definition overrides local profile meaning. Reject a mismatched optional hit and continue with the core; an advisory result never requires a new requester decision by itself.

V6 character-response compilation never calls the legacy raw-text moe router. It copies typed axes and frozen evidence into `photo-character-response/v1`, permits one primary action and one primary affect-leak channel, and exposes advisory candidates only after core freeze.

Character-response meanings, multilingual paraphrases, abstract axis classes, semantic relations, confounders, and optional mechanism-node links live in `photo-character-mechanism-graph/v2`. They are projected into the existing semantic index rather than a second meaning store. BM25F admits a concept profile only when its document outranks every matching confounder declared by that profile, then limits behavior support to its linked nodes. Profile consistency is advisory: neither a match nor `consistent` may revise the core or create hard evidence. The composer may reject every candidate and may not substitute a taxonomy label for frozen evidence or add an unrequested relationship or emotion.

Other required typed meanings use `photo-semantic-assertion-obligations/v1`. The composed audit recomputes the contract from the core, rejects missing or mutated blocks, and requires a byte-identical assertion/evidence map with every phrase literal in `prompt_en`.

## Compact composition view

`scripts/compose_pack_view.py --pack candidate_pack.json` projects an immutable v6 source pack into requirements and a candidate catalog. `--output composer_view.json` saves that view; repeatable `--candidate-id <id>` returns complete candidate details bound to the same source hash.

Read every hard requirement before composing. Catalog order has no preference meaning, and a catalog summary is insufficient authority to adopt a candidate. Read full details for every candidate under consideration before selection, including its applicability, conflicts, affected dimensions, and any opt-in obligation. Rejecting all optional candidates is valid. Keep the original full pack unchanged and pass it to the existing audits; never pass the view as the pack or edit it to remove a duty.

The view reduces routine reading without changing retrieval, source-pack identity, composition obligations, or render gates. It is not evidence that a prompt or image passed any audit.

## Post-core visual intent

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

If the requester explicitly makes a perceptual effect focal (for example, asks to focus on it or make it unmistakable), fail closed before rendering when that focal meaning is still uncovered and has neither a required typed assertion nor an active hard visual obligation. A broad label, an embedding hit, or an optional candidate is not coverage. Bind an `agent_postcore_interpretation` visual intent only when one exact frozen core field already decomposes the focal effect into all observable components required by one profile; otherwise rebuild from the clear requester meaning, or ask only if that meaning remains ambiguous. Record this focal-coverage check separately from prompt, runtime, and pixel status.

On a lineage-bound retry, a parent hard obligation is not a new inference when its governing dimensions are explicitly preserved. Rebind it through `agent_postcore_interpretation` to an exact current core field and retain the parent profile ID; record the parent hash in `request_lineage`. Retrieval remains advisory and is never the source of the carried duty.


## Positive retrieval fields and semantic surfaces

Visual-profile text recipe `photo-visual-profile-text/v2` and BM25F policy `photo-visual-profile-bm25f-policy/v2` share one allowlist in `photo_visual_retrieval.py`: positive definition, paraphrases, visual components, and support concept units. Exact aliases remain in the exact/lexical alias lane. Category IDs, component IDs, claim limits, interpretation scope, contrast examples, and orchestration instructions are not positive prototypes. Negation is not removed by a word filter; authored visual meanings may legitimately contain negative-form language. A data editor moves actual limitations into their owning fields and keeps positive fields accurate.

Dictionary text recipe `semantic-text-v5` and lexical policy `photo-semantic-bm25f-policy/v3` also consume authored `concept_units` and directed `relations` alongside the existing public visual-language fields. Relation IDs remain control metadata; subject, relation type, and object retain their direction in both retrieval lanes. Source-data or policy changes require a generated index refresh. Cache reuse is allowed only for byte-identical input text in the same vector space.

## Evaluation scope

Idealized agent-authored slot queries and slot-specific embeddings are separate experiments, not measurements of this automatic projector or production ranker. New pipeline checks must freeze independent inputs before candidate inspection, validate v3 cores, and call the actual pack builder with guards and sampler pools. Lexical-only checks do not establish dense-lane or semantic-judge quality. A small AI-authored holdout supports regression diagnosis, not promotion of evidence-union to default or human relevance claims.

The automatic projector is conservative, not a general English parser. Coordinated explicit negative enumerations retain negative scope, while independent positive clauses after an inactive source can re-enter. Some compound or prefixed sentences can still omit evidence (for example, an inactive lamp after a no-visitors clause or an eye-level camera phrase after an opening lighting adjunct). Such omissions do not grant permission to override a user exclusion or a locked dimension; they remain limitations of the opt-in experiment.

### Experimental structured constraints and independent recall ablation

`--semantic-constraint-policy structured-v1` is opt-in; `off` remains the default.
It extracts a partial, source-bound English meaning footprint from the already
frozen v3 core and the public candidate label. Every recognized constraint carries
its evidence and ownership. No pre-core feature audit, candidate ID, topic ID, or
private catalogue tag supplies the meaning of the request.

The ordinary candidate inventory is filtered before bundle construction, within
the existing exposed budget, for lighting and camera families. Authored bundles
are admitted atomically using the same source-based function in generation and
audit; bundle-only members in the scoped slots receive the same semantic check.
Rejected bundles are removed whole, never partially rewritten or rehashed. Explicitly contradictory candidates are
withheld from selectable inventories (diagnostics still retain their source
evidence); unknown candidates abstain rather than being called safe or replaced by
arbitrary fillers. This can substantially reduce candidate coverage, which must
be reported alongside any conflict improvement. Open creative attributes remain
editable. The core and its requester-owned facts are never rewritten.

The pack carries `semantic_constraint_validation`, and `audit_composed_prompt.py`
checks actual `prompt_en` after composition, including recognized internal
combination conflicts. A recognized contradiction or an
unresolved governing constraint blocks this experimental audit. The composer
must revise only the violating addition and re-audit, retaining locked facts;
the validator does not silently rewrite prose. Chosen candidate IDs alone do not
prove that their final realization is compatible. The repository's normal writer
is still an external authoring agent. No external semantic model is configured
or silently purchased by this flag. The partial recognizer cannot guarantee
arbitrary natural-language consistency or image quality.

`--recall-lane-policy reserve-leaders` is a separate opt-in ablation for
`evidence-union`. It reserves the leading eligible item from each lexical/dense
lane before the same budget cutoff, then fills from the original fused ranking.
It never expands the eligible set or changes a semantic verdict. If capacity is
insufficient, existing lane order breaks ties; existing selected-member placement
can still consume capacity. Compare recall-only separately from constraints and
report catalogue absence, pool miss, rejection, unknown, and final adoption as
different outcomes. Neither flag promotes the experimental retrieval policy.
