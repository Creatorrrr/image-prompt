# Installed H-only+F2 search

The normal managed workflow uses this installed release for new runs. Its
18,180 positive CIDs and18,182 actual realization documents come from the
existing complete candidate pool. The70 diagnostic candidates remain source
records, outside positive material retrieval. Test requests do not restrict the
candidate population. Slot tags never partition or prefilter this search.

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
reused. No second query, reranker, Gemini or remote fallback is available.

F2 keeps original lookup cues and meaning fields, with frozen weights, global
document frequencies and nonempty normalization on its designated fields. The
two complete ranks combine by RRF10 on the same CID/RID, followed by CID dedup
and top8. No relevance threshold or native eligibility pruning removes material
before retrieval. Payloads remain lazy; exact full-pool cosine can read all
vector extents. This is a recall-oriented material search, not a claim that
every result fits or that every useful candidate is recovered.

Use `view --candidate-id CID` for full source detail and
`view --material-page N` for reading pages of at most64 unique sources. This
page cap does not truncate the stored per-slot top8. Repeat retrieve, view,
resume, compose-audit and deliver reuse issued scores and add zero searches.

Material decisions are optional authored rows in `h_f2_material_decisions`:
`{slot, candidate_id, realization_id, source_sha256, use, rationale}`. `use` is
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
