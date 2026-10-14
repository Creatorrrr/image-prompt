# Named phrase-field consumer audit (read only)

Task `/root/review_08250_09250`, gpt-6.1-sol/high. No production/test/index,
source, proof, catalog or runtime changes were made for this audit. Bulk stays
at 430/1000; next ordinal is 6680. Structural counts are not semantic reads.

The exact inventory and offline consumer probes are in
`native-08250-phrase-fields-inventory-20261015.json`, raw SHA256
`2b3364c936f31b55d3911433946b37d1c7543f6ddd1d5e236e52571051a01a13`.
Its source is frozen `SOURCE.json.gz`, canonical
`125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b`.
Probes use immutable96c modules in a fresh network-denied process; the file
records actual module paths/hashes. Static code reading also covered current
working consumer functions. No index build, provider invocation, query model,
runtime publication or image execution was performed.

## Exact structural scope

There are 18,250 source CIDs. Exactly 381 have these fields, all visual_option:
381 `/content/phrase_en` and 381 `/content/phrase_ko` strings, 762 occurrences.
All are direct content fields; recursive enumeration found no nested named
phrase fields, selected-RID phrase fields or phrase-bearing conditional CID.
Every phrase-bearing source has actual RID `base`. This is a structural
inventory, not a claim that all 762 strings have been semantically reviewed.

Five visual_bundle parents explicitly reference five such children. Every
parent and child has RID `base`; every member is `adoption: optional`, with an
explicit original location binding whose condition is empty. Their exact
requirements, original binding roles/weights and source hashes are saved in
the inventory. Neither child phrases nor child tags become unconditional
parent meaning merely because the member is listed.

| Parent ordinal | Member pointer suffix | Child CID | Explicit requirement |
| --- | --- | --- | --- |
| 14314 | `/member_candidates/1` | cand_a64123e7e14c514b87eedd8caa170670 | a vintage record shop aisle |
| 14274 | `/member_candidates/0` | cand_59becd611bdd538eadfc163564140e06 | a neon-lit alley on a rainy night |
| 14044 | `/member_candidates/0` | cand_7ccb835c060f5f5c9da725a58e87c148 | a white-cube art gallery hall |
| 14325 | `/member_candidates/0` | cand_4ded9fbd4084540384afe2522c0f8eec | a Korean train platform with yellow tactile paving |
| 14230 | `/member_candidates/0` | cand_9ec1bffe9ad353ffa372bcccc03e9628 | a quiet hanok inner courtyard |

This table is an explicit member-edge scope inspection. It is not a fresh
whole-parent native review or an assertion that these are all possible
transitive references through every other source field.

## Consumer differences

* `photo_semantic_evidence.primary_paths` enumerates the root POSITIVE_FIELDS
  allowlist. These two names are absent, so the automatic required whole-field
  disposition inventory omits them. `meaning_material/meaning_sha256` still
  bind them as complete source content: integrity coverage is not semantic
  disposition coverage.
* `positive_string` accepts exact `/content/phrase_en` and `/content/phrase_ko`
  string pointers, rejects negative/routing labels and foreign selected-RID
  pointers, but does not itself require membership in primary_paths. Thus a
  manually supplied normal fact/unit can already use these named strings;
  automatic complete-unit coverage is the gap. The new semantic_reference
  contract additionally requires both local and canonical pointers in
  primary_paths, so the two omitted names cannot currently act as its anchors.
* `photo_global_index.fields/text` does not read phrase_en/phrase_ko. Visual
  options use en/ko/ja, aliases, definitions, paraphrases, concept units,
  relations, manifestations and keyword/embedding fields. Profile retrieval
  has its own positive_visual_profile_fields allowlist. No phrase field is
  independently inserted into either retrieval recipe.
* `photo_role_proposals.propose` obtains its positive blob from those same
  index fields (or the cached reader positive_blobs). It does not add phrase
  fields. Native role fit is independently determined by the manual proof,
  not by text matching or a phrase occurrence. Record hashes still bind the
  whole original source.
* `photo_candidate_corpus.entry` deep-copies source content, so base entries
  preserve both names. `photo_search_layout.guard_record` does not remove them;
  payload shards retain the whole exact record. `photo_native_pack.finalize`
  places the whole source in candidate_pool[CID].authored_record, so named
  source phrases can be exposed to the human/agent composer even though they
  are absent from retrieval text and automatic unit coverage.
* `photo_candidate_realizations.project_content` derives phrase_en/phrase_ko
  from the actual selected projection's en/ko. It overwrites old common phrase
  values when a realization_content projection exists. An offline synthetic
  shape probe confirms this; it is not a corpus/source approval. Actual381
  sources have no such projection, so their original phrase fields survive.
* Runtime `prompt_generator.localize` reads en/ko/id, and native candidate labels
  use it. A repository Python search found no photo-runtime getter that reads
  phrase_en/phrase_ko directly into a rendered sentence; their only explicit
  production spelling is the selected-projection write. Therefore this audit
  does **not** claim a legacy phrase template currently renders them directly.
  Final photographic prose is authored, then audited and transported as
  composed.prompt_en/runtime_prompt_en. API preflight compares those exact
  authored strings rather than recomposing candidate phrases.

## Three whole-source examples directly read

The inventory saves the complete original records, own bindings, exact source
strings, primary_paths, index fields/text, base entries, localized labels and
unqualified role proposals for all three examples. They remain unqualified.

* Ordinal6673, cand_ac39d8f9844c5239a4e7f3937233fd91: en names a lush summer
  orchard; phrase_en adds `deep inside`, and phrase_ko adds the same inner
  location. This is actual location meaning, not arbitrary metadata. It was
  already included in the bulk425 checkpoint as a manually identified extra
  positive field, without altering that frozen checkpoint.
* Ordinal5151, cand_026d3eebda735d5694be80bf4a721013: en/embedding say
  `unlabeled containers`; phrase_ko says `라벨이 읽히지 않는` (labels not readable).
  A reviewer must distinguish absence of labels from readability restriction;
  the short Korean phrase does not independently entail complete label
  absence. This example is a consumer-scope read, not a new semantic ruling.
* Ordinal2667, cand_022b574a012054e4b42424a06662bdb2: en names a blue-lit data
  center; phrase_en is `inside a blue-lit data center`. Its inner-place wording
  remains in base content while localize and retrieval labels use en/ko.

## Minimum proposal, not implementation authorization

For complete manual source disposition, add **only** `phrase_en` and
`phrase_ko` to the existing root POSITIVE_FIELDS allowlist. Preserve
positive_string's negative/foreign-RID rules and the semantic_reference
same-CID/same-RID/direct-primary constraints. Do not allow unknown_extra or
promote aliases, keywords, tags, provenance or other metadata into native
positive evidence. No CID-specific branch is needed. All newly required
phrase clauses must then receive a direct manual meaning/owner/mode review;
path coverage alone cannot approve any of381 CIDs or reuse an old signature.

Search inclusion is a **separate** decision: optional future exact named-field
projection into index labels/text would change retrieval material, index
recipe/fingerprints and possibly embeddings. It is not necessary to repair
manual whole-source evidence coverage, and this audit does not recommend a
silent search recipe expansion or vector reuse.

No projection-schema expansion is needed for the observed381 base-only
records. A future conditional record carrying distinct phrase-only meaning
needs explicit reviewed selected-source semantics. The current selected en/ko
derivation must not import another RID or make unselected common alternatives
mandatory; adding the two coverage fields must not bypass those boundaries.

Suggested focused regressions for a later authorized patch: exact named-field
coverage and positive_string acceptance; missing phrase unit rejection;
same-RID direct semantic and semantic_reference anchors; aliases/tags/unknown
extra/foreign RID rejection; unchanged en/ko localize and selected phrase
derivation; base entry and full authored-record transport; optional child
dependency scope; native signature invalidation on changed phrase; full and
compact admission/lock behavior. Search recipe tests should explicitly prove
it unchanged unless a separate search change is approved. No such tests or
production patch were added by this read-only investigation.
