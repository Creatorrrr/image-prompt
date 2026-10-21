# Installed H-only+F2 search

The maintained weak-slot source contains 18,368 positive candidate records and
70 diagnostic records. The installed config separately selects the immutable
release and its exact CID/RID population for new managed runs. Source edits alone
do not switch the installed release. Slot tags never partition or prefilter the
whole positive search pool.

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
local cosine lane, RRF10/CID dedup and its own top8. Results are not pooled into
or allowed to displace a slot's top8. `query_scopes` identifies `slot`,
`request_topic` and `baseline_prompt`; the two reserved IDs appear alongside
slot IDs in `materials`. Read and review these complete sources with the same
requester-lock and native-adoption boundaries as slot material.

Frozen source, controls, plan and projection provenance bind the new queries.
Missing active request scope or an empty positive query stops retrieval rather
than searching another arm or substituting an invented query.

F2 keeps original lookup cues and meaning fields, with frozen weights, global
document frequencies and nonempty normalization on its designated fields. The
two complete ranks combine by RRF10 on the same CID/RID, followed by CID dedup
and top8. No relevance threshold or native eligibility pruning removes material
before retrieval. Payloads remain lazy; exact full-pool cosine can read all
vector extents. This is a recall-oriented material search, not a claim that
every result fits or that every useful candidate is recovered.

Use `view --candidate-id CID` for full source detail and
`view --material-page N` for reading pages of at most64 unique sources. This
page cap does not truncate any stored top8. Repeat retrieve, view,
resume, compose-audit and deliver reuse issued scores and add zero searches.

Material decisions are optional authored rows in `h_f2_material_decisions`:
`{slot, candidate_id, realization_id, source_sha256, use, rationale}`. For
whole-scene material, `slot` retains its originating reserved search ID
(`__request_topic__` or `__baseline_prompt__`). `use` is
`skip` or `inspiration_only`. Read complete source conditions and effects;
preserve requester locks. The native guard pack carries hard duties and
performs zero slot searches. Do not put material IDs into native chosen lists
or treat `native_approval: false` as a whole-source adoption permission.

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
paths naming existing sealed `scripts/*.py` or `precore/*.py` members. An optional
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
returns zero with a reason; no extra search or ordinary top8 padding is used.
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
