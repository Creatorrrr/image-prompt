# Retrieval Contract

Post-core only. Load this reference for retrieval diagnostics or maintenance; ordinary composition starts from the compact pack view and the relevant composition contracts.

## Frozen query and index ownership

The retrieval query combines the exact active requester spans, with true requester exclusions redacted, plus interpreted intent, subject, setting, event, visual priorities, baseline prompt, requester definitions, interpretation resolutions, and optional style evidence. Runtime-forbidden labels remain meaning-retrieval input. Research URLs are provenance only. `--concept-lock` is normally derived; every supplied value must byte-equal the active spans in order.

V6 projects those frozen fields into a versioned BM25F query. Tokenization is NFKC/casefolded and boundary-aware: conservative Korean suffix stripping may recognize an inflected whole term, while an unrelated word containing the same characters cannot activate it.

Visual-profile retrieval uses one generated index derived from the single authored registry: boundary-aware exact lookup rows, a fielded BM25F derivation, and one embedding vector per profile. Runtime rejects stale registry hashes, BM25F recipes or policies, and semantic text recipes. One private resolution is projected into `visual_obligations`, `visual_concept_candidates`, and `semantic_clarification`. Scores, vectors, matched terms, and rank remain private. This lookup is independent of creativity and seed.

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
