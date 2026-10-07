# Retrieval Contract

Bound v6 adult-axis search uses `photo-contextual-appeal/v2`: one lane keeps the
baseline context, while the alternatives lane uses active requester spans,
requester definitions/anchors and the frozen control meanings without copying
agent-selected wardrobe. BM25F and available embeddings rank the compatible
corpus, with soft fusion across whole directions, construction/material and
portrayal/scene relations. Those are expression scopes, not aesthetic membership
classes. Scope and context determine candidate eligibility. Scope/property locks and requester exclusions still apply.

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

The retrieval query combines the exact active requester spans, with true requester exclusions redacted, plus interpreted intent, subject, setting, event, visual priorities, baseline prompt, requester definitions, interpretation resolutions, and optional style evidence. Runtime-forbidden labels remain meaning-retrieval input. Research URLs are provenance only.

V6 projects those frozen fields into a versioned BM25F query. Tokenization is NFKC/casefolded and boundary-aware: conservative Korean suffix stripping may recognize an inflected whole term, while an unrelated word containing the same characters cannot activate it.

## Slot-focused candidate lookup

The slot inventory is determined after core freeze. Only a slot with authored ownership dimensions and grounded frozen fields gets a focus query. Search the eligible same-slot corpus with a whole-scene BM25F lane and the focused lane. Reapply subject, domain, facet, primary-context and requester-exclusion guards against the frozen core; another optional candidate cannot establish a prerequisite.

Fuse the two query lanes with reciprocal-rank fusion, preferring their intersection and allowing one focused fallback. Expose at most four candidates for each core slot, two for each support slot, and 64 ordinary slot candidates overall. Source-opted-in options matching frozen semantic assertions or visual priorities receive first access to this cap, followed by the remaining core and support slots. Visual priorities are agent-authored observations; this advisory discovery creates no requester assertion or hard duty. It requires the complete candidate effect to be open and compatible with property locks, and applies requester and typed exclusions before ranking. These are inventory limits, never an active-slot quota or adoption count. Omit a slot without grounded focus or lexical hits. There is no sampled default, fixed scene template, or forced slot selection.

`core_retrieval` binds the core, corpus, ownership, applicability and query hashes. The composed and runtime records must copy `core_retrieval_sha256`. The composition auditor recomputes the full eligible inventory and rejects missing or substituted candidates. Selecting across slots remains a joint authorial decision that preserves the frozen actor, action, target and other directed relations. Rejecting every optional candidate is valid.

For v6 typed request routing, subject category and exact subject-entry routes read the frozen subject field. An animal-ear modifier in that field is not treated as a standalone animal subject. Authored human role aliases such as witch can supply the human category when the field does not literally say human; a nearby person in the event cannot reclassify an animal subject.
For subject candidates only, an explicit adult human in the frozen core may expose a human role tagged `adult` when that tag describes age alone. Adult-content and suggestive tags retain their existing guards.

Visual-profile retrieval uses one generated index derived from the single authored registry: boundary-aware exact lookup rows, a fielded BM25F derivation, and one embedding vector per profile. Runtime rejects stale registry hashes, BM25F recipes or policies, and semantic text recipes. One private resolution is projected into `visual_obligations`, `visual_concept_candidates`, and `semantic_clarification`. Scores, vectors, matched terms, and rank remain private. This lookup is independent of creativity and seed.

## Meaning authority

Exact request terms may retain their declared request-scoped hard meaning. A profile found only by BM25F, embedding similarity, or reciprocal-rank fusion is optional and creates no prompt duty or render gate until explicitly selected. A requester definition overrides local profile meaning. Reject a mismatched optional hit and continue with the core; an advisory result never requires a new requester decision by itself.

V6 character-response compilation never calls the legacy raw-text moe router. It copies typed axes and frozen evidence into `photo-character-response/v1`, permits one primary action and one primary affect-leak channel, and exposes advisory candidates only after core freeze.

Character-response meanings, multilingual paraphrases, abstract axis classes, semantic relations, confounders, and optional mechanism-node links live in `photo-character-mechanism-graph/v2`. They are projected into the existing semantic index rather than a second meaning store. BM25F admits a concept profile only when its document outranks every matching confounder declared by that profile, then limits behavior support to its linked nodes. Profile consistency is advisory: neither a match nor `consistent` may revise the core or create hard evidence. The composer may reject every candidate and may not substitute a taxonomy label for frozen evidence or add an unrequested relationship or emotion.

Other required typed meanings use `photo-semantic-assertion-obligations/v1`. The composed audit recomputes the contract from the core, rejects missing or mutated blocks, and requires a byte-identical assertion/evidence map with every phrase literal in `prompt_en`.

## Interpreting applicability diagnostics

Use this post-core guidance when a consequential rejection needs investigation or the requester asks how data was used. It applies across subjects and wording; it is not a keyword-triggered route or a requirement to inspect implementation for every candidate. Read the relevant saved inputs and full source detail first. Inspect the exact bound implementation only when those records do not explain the predicate; current source may differ from an archived run.

- Separate absent input from a present value that did not match registered classes. Report the latter as unrecognized by that matcher, not absent or semantically opposite. Class matches are also bounded evidence: check negation, contrasting senses and context before treating them as compatibility.
- Separate lack of a positive context match from an explicit different sense or exclusion. Inspect which fields and conditions were evaluated. Do not manufacture a preferred activation phrase, requester definition, age, role or relationship to make a condition pass.
- Separate common input requirements from additional profile requirements. Identify the extra field actually demanded; validity under the common authoring contract does not guarantee conformity to every advisory profile. Missing extra information does not authorize guessing it or treating the request's meaning as invalid.
- Separate a missing relation operator from a present operator with different members or endpoints. Compare participants, ownership, direction, causal stage and literal evidence. A generic starting-state role is not universally equivalent to an affect or result role, and a trigger-to-result edge does not automatically prove a trigger-to-action edge. A role connection needs its own evidence; do not alter signatures just to obtain conformance.
- Separate a valid source meaning from its applicability to this scene and from authorial preference. Record the concrete unmet prerequisite or locked effect when known. A valid but declined option is not evidence of faulty data.

These are explanations, not new serialized statuses or eligibility overrides. Preserve the exact pack, core, assertions and bindings. Advisory recognition failure does not erase a clear requester instruction. Continue with the frozen meaning when the optional hit adds no usable assistance; use the existing rebuild or repair path if required evidence must change. If a binding required gate remains unresolved, report the concrete limitation rather than claim success or waive it. Ask only for genuinely unresolved requester meaning, not because an optional matcher failed.

When explaining the run, distinguish lookup execution, exposed candidates, actual review, selection, final prompt realization, and native-pixel results. Ground each claim in the corresponding records and stable IDs; count duplicate hits once when reporting unique candidates. Preserve uncertainty when a stage was not recorded. Zero selection alone proves neither failed search nor universal incompatibility. Definition correctness, predicate behavior, prompt integrity and image fidelity are separate findings.

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

## Meaning diagnostics

Current clarification uses `photo-semantic-clarification/v2`. The advisory consistency and applicability projections expose `photo-meaning-diagnostics/v1`. Axis checks distinguish absent values, unrecognized expressions, class mismatch, explicit exclusion, negated values and unresolved polarity. Each check retains the original values, authored matching phrase and source assertion, expected/observed classes and whether the check affects eligibility. `missing_axes` means actual absence; `unrecognized_axes`, `class_mismatch_axes` and `unmet_axes` have separate meanings.

Relations use the generic typed signature: `same_target` member order is immaterial, while contrast endpoints and temporal order stay directional. A present operator with different members/endpoints is an unmet structure, not a missing operator. Context checks distinguish an authored exclusion-term match from missing positive lexical proof. Missing positive proof never says the core resolved a different sense. A lexical class match proves neither natural-language relation truth nor pixel realization.

Class matching uses authored exact values or bounded contiguous phrases. Explicit scoped negation and mixed polarity do not automatically pass a positive class. Unknown expression/scope remains unrecognized or unresolved; similarity scores cannot fill missing axes or invent target relations. Only reviewed equivalent expressions belong in the vocabulary. Optional `axis_advisories` retain values and reasons without changing consistency or activating hard obligations. These are data-declared conditions handled by the common engine, never named-concept code branches. Requester definitions and the frozen core retain precedence.

The source-bound composed audit recomputes exposed class and context diagnostics. Composer catalog/details preserve them, but the original pack remains the audit input. Historical v1 clarification artifacts require their sealed implementation; do not rename them to v2.
