# Source-only candidate review

Maintain `candidate-authoring/v1` as the versioned full canonical source exported
from the installed snapshot. `photo_candidate_authoring.py verify --source PATH`
checks its complete record/header/binding closure against the original corpus.
Native meanings, conditions, effects, branches and qualifications remain exact.

A `photo-candidate-source-review/v1` JSON has exactly: `schema`, `candidate_id`,
`source_sha256`, `decision`, `rationale`, `realizations`, `slot_tags`, `review`.

- `decision`: enrich, retain, needs_semantic_edit, defer, diagnostic.
- `review`: exactly `{author: "gpt-6-luna", effort: "max", source_only: true,
  native_approval: false}`. The provenance declaration is not a truth proof.
- `realizations`: one actual RID key per source realization, each with exactly
  `summary_en`, `summary_ko`, `anchors`, `facets`, `search_aliases`, `unknowns`.
- `summary_en`: concise natural visible meaning, at most80 words/900 characters.
  `summary_ko`: faithful Korean explanation, at most600 characters. Unknown or
  incorrect source meaning must be deferred rather than invented.
- `anchors`:1–12 exact `{pointer, quote}` positive primary units from this same
  CID/RID. Quote the complete original string. No metadata, other RID or
  evidence-only validation boilerplate may support a new positive claim.
- `facets`: at most12 `{kind, text_en, anchors}` items. Kind is entity, action,
  relation, attribute, context or condition. Express actual subjects, carriers,
  actors, receivers and relations; distinguish visible appearance from an
  unproved physical cause. Missing anatomy, people or prerequisites stay missing.
- `search_aliases`: at most6 `{text, anchors}` faithful synonyms/search cues.
  New settings, moods, sexual implications, events or causal interpretations
  are not synonyms. Do not repeat query-like words to gain ranking weight.
- `unknowns`: at most8 concise unresolved issues, separate from search text.
- `slot_tags`: at most6 `{slot_id, realization_id, rationale, anchors}` reviewed
  discovery-tag proposals from the exact neutral catalog. These do not change
  native bindings or qualify a role, and never filter or vote in search.

Every item needs an actual comparison with the source. Preserve full branch,
owner, membership, required/optional and scope restrictions. Readable summaries
do not authorize native adoption. Mark native contradictions or material meaning
changes `needs_semantic_edit`; keep the original and separate the future review.

The pilot compiler A preserves current D exactly. For selected pilot sources,
B appends existing positively grounded visual manifestations as core meaning.
C appends accepted English summaries and grounded aliases after B. Existing D
meaning, exact lookup cues and their order stay intact. Only additions receive
new field ownership; no string part is assigned twice. Korean summaries and
facets remain review/display metadata. Conditions and native permissions retain
their original source ownership. F2 weights, k1/b, normalization populations,
query texts, one lane each, RRF10 and top8 remain fixed. Every arm recomputes
statistics over the full18,182-document pool, not just96 reviewed candidates.
