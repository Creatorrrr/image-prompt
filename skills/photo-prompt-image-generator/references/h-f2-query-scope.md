# Bounded lexical scope correction

The installed H-F2 policy retains the exact authored query and its proof-bound
embedding. Each query evaluates one complete BM25F lane and one complete local
cosine lane over the same positive CID/RID pool. A versioned correction can
adjust one lexical RID score before final RRF10 and CID deduplication. It never
filters candidates or grants native adoption.

`photo_h_f2_query_scope.py` records original-text offsets for the structural
`role:` label and explicit comparison adjuncts such as `distinct from`,
`separate from`, `rather than`, and `instead of`. Quoted literals remain literal.
Domain/context priors and epistemic clauses such as `without claiming a
measurement` retain their existing behavior. This is a conservative lexical
witness extractor, not a general negation or natural-language truth parser.

The correction starts from the original fused winner. It considers at most one
RID and keeps the original ranking when its evidence is insufficient:

- A contrast correction needs an actual multiword counterpart witness in that
  winner's D document, a positive compound witness in the proposed replacement,
  strictly stronger positive lexical support, and no same counterpart witness
  in the replacement. Quoted or negated source mentions cannot be witnesses.
- A format-label correction needs the original winner below the semantic lane's
  median, a replacement above it with a stronger cosine, strictly stronger
  positive lexical support, and at least two newly matched positive terms rarer
  than the discarded structural label. Generic owner/subject words alone do
  not establish this evidence.

There are no candidate IDs, slot tags or benchmark files in this decision. The
field weights, document frequencies, document texts, document vectors and query
vectors remain unchanged. The full pool remains available. RRF10 produces the
base order; an explicit inscription can then use the separately witnessed
[carried literal ordering](h-f2-literal-text.md). Recognized lexical scope does not prove complete
role fit, requester compatibility or native eligibility.

Material evidence stores both `bm25_raw` and the final `bm25`, the cosine vector,
full order and a `query_scope` analysis/correction trace. Receipt auditing checks
the original text, verifies affected known-RID field contributions against the
sealed index, replays the bounded decision and reconstructs exact RRF10 plus
any witnessed literal and [event-phase ordering](h-f2-event-phase.md) without another search or embedding. Altered
scope, corrected-score or literal evidence fails.
Older bound runs continue using their original sealed implementation.

Maintenance must compare the identical frozen queries and actual query vectors
against the previous raw order, inspect changed results, and qualify an entire
new code/data generation before selecting it. Installing without activation is
available for deployed-copy validation. Native CURRENT is independent of this
installed release selection and is not updated by installation.
