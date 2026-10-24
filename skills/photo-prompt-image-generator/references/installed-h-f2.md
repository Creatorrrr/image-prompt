# Installed H-only+F2 search

New runs use H-F2 material v2 and a core-derived `photo-validation-context/v1`.
No empty native candidate pack or separate `creative_augmentation` stage is
created. Validation compiles frozen meaning, controls, source obligations,
negative policy and embodiment checks directly. Historical material v1/native
V10 runs keep their original sealed implementation and records.

## Creativity and one-pass sampling

Each query still ranks the whole positive corpus once with BM25F and local
cosine. Apply the existing phase/literal/primary-source scope projection first,
then take a CID-deduplicated rank window. Retain its first eligible source and
draw the remaining positions uniformly without replacement. The rank anchor
counts toward the same total sample limit; it never depends on source identity,
recency or topic. Creativity never relaxes requester locks or source conditions.

| creativity | rank window per query | sample limit per query |
| --- | ---: | ---: |
| 0 | 8 | 4 |
| 1 | 32 | 8 |
| 2 | 96 | 12 |
| 3 | 256 | 16 |

A new run records a fresh 128-bit `sampling_seed` before searching. Query ID and
query hash derive independent random streams from that seed. Save the policy,
window IDs/hash and sampled IDs; receipt audits replay the exact sample without
search or model calls. Resume/view reuse issued evidence and never resample.
When fewer compatible sources exist, return only those sources without padding.
Current goals store `candidates`; historical goals retain `top8`. Every returned
query/CID/RID occurrence still needs its source-bound material decision. Compare
candidate-informed alternatives with the frozen baseline; adoption is optional.
Use the bound creativity level for [candidate-informed reconstruction](composition-contract.md#creativity-and-reconstruction), from necessary changes at 0 to active whole-photograph alternatives at 3. This authoring guidance does not change the sampling windows, return limits, source conditions or receipt replay above, and does not reactivate the historical creative-augmentation sampler.
`pack`/`pack_id` remain transport names for historical CLI compatibility, but the
new artifact is a validation context with no native candidate inventory or
creative-guide payload. Image records identify this format as `h-f2-v2`.


The normal managed workflow uses the sealed release selected by
`retrieval-runtime.json` for new runs. Its manifest declares the current positive
CID and realization-document counts; diagnostics remain source records outside
positive material retrieval. Test requests do not restrict the candidate
population. Slot tags never partition or prefilter this search.

The [biopunk and body-horror data extension](biopunk-body-horror-semantics.md)
adds 141 complete visual options and 21 diagnostic/context records, with 162
semantic cards, 259 keyword routes and 202 optional role bindings. The scoped
source/index commit leaves the installed-runtime pointer unchanged; see the
[validation boundary](biopunk-body-horror-validation-20261021.md).

The [liminal, dreamcore and weirdcore data extension](liminal-dreamcore-visual-semantics.md)
adds 133 complete bilingual visual options, 72 diagnostic/context records and
250 optional role bindings across 200 researched term cards and five bounded
alternatives. These are authored sources with `native_approval: false`.
The scoped source/index publication preserves the installed-runtime pointer.

The [metafiction, existential-horror and LitRPG extension](metafiction-existential-litrpg-semantics.md)
adds 64 optional visual sources, 10 contextual diagnostics and 130 keyword
routes. It separates visible relations, narrative proxies and an explicit
three-panel sequence. Its source graphs and 549 review gates are metadata,
without native qualification or automatic genre activation.

After independent core freeze, run `photo_workflow.py prepare-slot-intents
--run RUN`. Add repeatable `--slot SLOT` only to choose a smaller explicit
authoring scope; otherwise the neutral catalog and frozen open dimensions
determine the slots to review. Author every requested row before seeing any
candidates. All later commands must retain the same scope.

Write `authored-intents.json` as `{ "overall_intent": "...", "slots": { ... } }`.
Each slot row has exactly these fields; text represents the current photograph,
not candidate terms, IDs, metadata or past query examples:

```json
{
  "status": "search",
  "reason": "<why this role is useful>",
  "expressive_goal": "<what the image should express through this slot>",
  "observable_targets": ["<visible target or action>"],
  "owner_relations": ["<relevant actors, carriers and directed relationships>"],
  "required_constraints": ["<actual constraints to retain>"],
  "preserved_choices": ["<existing choices that should remain>"],
  "open_scope": ["<what may be developed>"],
  "unknowns": [],
  "role_focus": "<directly authored search intent for this role>",
  "scene_context": "<only the scene context needed to interpret the intent>",
  "language": "en",
  "grounds": [{
    "source_pointer": "/subject",
    "start": 0,
    "end": 0,
    "quote": "<exact nonempty substring; use its real Unicode end offset>",
    "source_sha256": "<SHA256 of the complete addressed core string>"
  }],
  "review": {"author": "Codex", "rationale": "<actual semantic review>"}
}
```

Use actual Unicode character offsets and a literal quote from a semantic frozen
core field. `grounds` certifies provenance, not truth. Author `not_applicable`
with a reason for an irrelevant role, or `unresolved` with explicit unknowns
when necessary; both have empty `role_focus`/`scene_context` and perform zero
searches. Do not fabricate applicability to fill the slot list. Up to149 rows
are supported; the plan validator checks the exact requested coverage.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_photo_slot_intents.py --run RUN --authored authored-intents.json --output slot-plan.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py seal-slot-intents --run RUN --plan slot-plan.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py retrieve --run RUN
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_workflow.py view --run RUN
```

The builder adds structural bindings and validates the authored rows. It writes
no expression goals, interpretations or query prose. Both lanes receive one
identical text: `Photographic role: {role_focus}` followed, when nonempty, by
`Scene context: {scene_context}` on a new line. There is one global F2 BM25F
evaluation and one full local cosine evaluation per searched slot. A fresh text
uses one proof-bound local query embedding; an exact existing proof may be
reused. These slot query texts and bindings remain unchanged by the additional
whole-scene searches below. No reranker, Gemini or remote fallback is available.

Every new retrieval also issues two independent queries after core freeze:

- `__request_topic__`: this arm's active requester spans, using the existing
  positive-text projection to remove creative-control assignments and explicit
  exclusions. Inactive arms and delivery text outside active spans are omitted.
- `__baseline_prompt__`: the complete frozen `baseline_prompt_en`, through the
  same explicit-exclusion firewall.

Neither query is derived from a slot or from `overall_intent`. Both run even
when there are no searched slots. Each receives one BM25F lane and one full
local cosine lane, RRF10/CID dedup and its own creativity-bounded sample. Results are not pooled into
or allowed to displace a slot's sample. `query_scopes` identifies `slot`,
`request_topic` and `baseline_prompt`; the two reserved IDs appear alongside
slot IDs in `materials`. Read and review these complete sources with the same
requester-lock and native-adoption boundaries as slot material.

Frozen source, controls, plan and projection provenance bind the new queries.
Missing active request scope or an empty positive query stops retrieval rather
than searching another arm or substituting an invented query.

F2 keeps original lookup cues and meaning fields, with frozen weights, global
document frequencies and nonempty normalization on its designated fields. The
two complete ranks combine by RRF10 on the same CID/RID, followed by CID dedup. New runs then apply the sampling policy above. No relevance threshold or native eligibility pruning removes material
before retrieval. Payloads remain lazy; exact full-pool cosine can read all
vector extents. This is a recall-oriented material search, not a claim that
every result fits or that every useful candidate is recovered.

Use `view --candidate-id CID` for full source detail and
`view --material-page N` for reading pages of at most64 unique sources. This
page cap does not truncate any stored candidate list. Repeat retrieve, view,
resume, compose-audit and deliver reuse issued scores and add zero searches.

Material decisions keep the existing authored rows in `h_f2_material_decisions`:
`{slot, candidate_id, realization_id, source_sha256, use, rationale}`. For
whole-scene material, `slot` retains its originating reserved search ID
(`__request_topic__` or `__baseline_prompt__`). `use` is
`skip` or `inspiration_only`. Read complete source conditions and effects;
preserve requester locks. The core validation context carries hard duties and performs no candidate searches. Do not put material IDs into native chosen lists
or treat `native_approval: false` as a whole-source adoption permission.

For new compositions, follow [candidate-informed alternatives and comparison](composition-contract.md#candidate-informed-alternatives-and-comparison). Review every distinct returned source across the material pages and record each returned query/CID/RID occurrence. Repeated sources may refer to one candidate-specific review. Put the concrete source finding, alternative comparison reference, and retained final effect or reason for non-use in `rationale`; a slot-wide sufficiency statement is not a candidate-specific review. Compare concrete compatible alternatives with the baseline before selecting the final prompt. Final use of every candidate remains optional. The material decision fields, requester locks and audit commands are unchanged; archived decision lists retain their original validation contract.

## Installation and freshness

`retrieval-runtime.json` selects the sealed H-F2 release under
`photo-shared-runtime/h-f2-installed`. Code, candidate bodies, postings and
document vectors are copied into that operating store. The installed skill's
existing local embedding installation supplies the exact model and Python
runtime; native validation has its own checked model files. Runtime does not
read a research checkout, benchmark judgments or build caches. Code and data
seals are verified; missing/altered files stop execution. The installer and
normal workflow never write native CURRENT.

Maintenance can install another already qualified release with:

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/install_photo_h_f2_runtime.py --source-store QUALIFIED_STORE --generation-id QUALIFIED_ID
```

Installation verifies all members, runs the deployed H-F2/native validators,
then atomically selects the release in the installed config. It does not build
or approve a new dataset. Candidate edits in the working source or a CURRENT
change do not silently update this pinned release. Prepare and qualify a new
whole-pool generation, then install it explicitly. Existing H-F2 runs keep their
issued release; already bound older native runs keep their native receipt path.
An incomplete search transaction requires reconciliation, not automatic retry.

For a code-only query/workflow update, first run
`scripts/stage_photo_h_f2_code.py --destination STAGING_STORE`. This copies the
currently installed sealed data and replaces only the two maintained query and
workflow modules, rebinds code/algorithm manifests, and leaves the previous
release and CURRENT intact. Run focused query tests and real retrieval/receipt
checks before selecting it as the default. The installer accepts `--no-activate`
to copy and validate a release, including its local runtime, without changing
`retrieval-runtime.json`; test it with explicit generation/store options, then
run the installer without that flag to select it. This path does not publish
dirty working candidate data or rebuild document vectors.

A phase/context update must stage the complete maintained H-F2 module closure,
including `photo_h_f2_event_phase.py` and `photo_h_f2_aftermath_scope.py`, and bind
the new code inventory. The two-module helper above applies to updates confined
to query/workflow modules; it does not publish edits to that wider closure.

For a reviewed wider code-only fix, the helper also accepts repeated `--member`
paths naming existing or new `scripts/*.py` or `precore/*.py` members. An optional
`--overlay-root` supplies exactly those reviewed files. Use an overlay built by
applying only the intended patch to the installed source when the working file
also contains unrelated edits. The stager verifies the complete expected code
inventory, keeps all source/index/vector bytes, and copies the overlay into the
immutable generation; runtime has no overlay dependency. Omitted `--member`
retains the original two-module default. Validate the exact new closure before
installing it.

The installed query policy includes a [bounded lexical scope correction](h-f2-query-scope.md). It preserves the exact query and embedding, retains original lane evidence, and corrects at most one lexical RID before final RRF10 when explicit source witnesses and conservative agreement checks pass. Saved-score replay verifies the correction without extra searches.

Explicit inscription literals can then use [carried literal ordering](h-f2-literal-text.md). Same-carrier, source-witnessed character preservation or an exact fixed literal precedes unproven contextual similarity; an explicitly different fixed literal follows it. RRF10 scores remain unchanged and ordering within each group is stable. Without a positive same-carrier source contract, the original order remains. This advisory step neither rewrites a source word nor grants native adoption.

Carrier-specific declaration-preserving sources cover entrance-door glass, fabric banners and wooden crates. Their exact text stays supplied by the independent scene. Short names remain labels; complete physical relation prose belongs to the explicit definition field. See the [authored source review](carried-inscription-source-review.md).

Affirmative physical aftermath can use [source-witnessed phase and context
contracts](h-f2-event-phase.md) after the full-pool score lanes. Version7
supports bounded English/Korean phase expressions without requiring an explicit
negative comparison. It verifies complete selected-primary assertions, recognizes
plain traces left behind, and keeps ongoing transformation distinct from a
completed initiating event.

Generic requests retain only witnessed physical aftermath without additional
authored context. Specific scene/owner requests require source-scene evidence.
Required, optional, negative and quoted context are separate: spell residue,
vanitas support, former luxury decline, a quiet event setting and a failed recipe
retain their complete source meaning. Unsupported owners do not borrow unrelated
or generic timing sources. If no compatible source exists, a supported request
returns zero with a reason; no extra search or ordinary-source padding is used.
Other intents retain ordinary retrieval. All scored sources and scores remain
in the common pool and saved full order.

Packs/views expose query scene/context, accepted context witnesses, withheld
context witnesses and the exact returned count. Saved-score audits reconstruct
all of them from original query text and verified primary sources, including
withheld records. Native conditions/effects and authoring guards remain separate.
This is a bounded advisory contract, not universal semantic or native approval.
See the frozen 212+96 maintenance report for exact quality and evidence limits.


Version7 also recognizes existing ordinary extinguished-wick material in Korean
primary fields and supports the declared dog/floor, bread/cutting-board and
opened-parcel/table aftermath families. Their complete source review is in
[aftermath-gap-source-review.md](aftermath-gap-source-review.md). Neutral material
can be returned without supernatural or symbolic context. Additional authored
event histories require matching declared owners and support surfaces. Data
additions are separately embedded and reindexed; the installed release remains
pinned until its full query and installed-copy qualification passes.


The 2026-10-21 weak-slot expansion preserves the prior installed source closure and adds 91 complete discovery candidates. The qualified primary-source compatibility projection is documented in [primary scope](h-f2-primary-scope.md). Existing 308 plus new 504 queries are preserved as 812 actual full-pool searches; exact adoption still requires the independent native source/owner/guard/permission workflow.

The 2026-10-22 dark-fantasy/grimdark addition registers 68 complete optional
visual realizations, four diagnostic/context records, 136 optional bindings
and 247 keyword routes while preserving the previous source records. See
[dark-fantasy visual semantics](dark-fantasy-grimdark-semantics.md) for complete
meaning, post-core use and pixel-evidence limits. Registration grants no native
approval.

The [2026-10-22 genre-fusion extension](genre-fusion-visual-semantics.md) adds
84 complete optional realizations and 12 diagnostic/context records for Dying
Earth, New Weird, Cozy Fantasy and Cosmic Horror. Its 96 cards and 150 keyword
routes preserve explicit owners, claim limits and separate still-image proof
from narrative interpretation. The selected `retrieval-runtime.json` generation
remains the authority; data registration, retrieval and image outcomes are
recorded separately in the research integration report.

The [2026-10-22 decadent domestic and splatter extension](decadent-domestic-splatter-semantics.md)
adds 86 complete bilingual visual options and 22 context-only diagnostics,
with 172 optional bindings, 189 keyword routes and 252 directed-relation review
gates. Material appearance, access relationships, anatomical results, models
and narrative claims retain separate meanings. New sources have no native
approval; discovery exposure, complete-source compatibility and saved pixels
are evaluated separately. The active installed generation remains selected by
`retrieval-runtime.json`.

The [military-fiction data extension](military-fiction-semantics.md) preserves
393 advisory term routes and contributes complete optional visual material for
barracks, uniforms, equipment, maintenance, ceremonial contact and represented
images. The selected installed config remains the runtime authority; source
registration alone does not change search. See the topic integration evidence
for the scoped successor, qualification and independent three-arm image tests.

