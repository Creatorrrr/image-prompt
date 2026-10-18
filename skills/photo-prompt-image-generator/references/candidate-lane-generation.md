# Independent candidate search documents (inactive until quality qualification)

`photo_candidate_lane_documents.py` owns the versioned v2 projection. D1 adds
accepted source-only summaries/aliases to the existing sparse fields and keeps
the original D input exactly. D1b additionally appends each complete accepted
English summary to dense D, without aliases. Both use one vector per actual RID.
The old v1 source-review compiler remains unchanged for historical replay.

Sparse additions must be the exact summary/alias in a parent-accepted review,
bound to the same CID/RID/source hash and exact primary source quotes. The native
record, conditions, effects, bindings and meaning authority remain unchanged.
Unreviewed records retain both inputs. Diagnostic, deferred and retain reviews
cannot be promoted through this sidecar. Sparse values have one field owner;
cross-lane token equality is replaced by exact per-lane reconstruction checks.

`photo_candidate_lane_generation.py` copies the complete qualified baseline
source and its original D/fields. It carries the original baseline manifest,
native code manifest, approved review sidecars and exact kernel/projection code.
Its independent content-addressed schema validates these closures, source/RID
coverage, vector execution proofs and complete global F2 DF/length statistics.
F2 weights/normalization, query tokenizer, RRF10, top8 and CID dedup stay fixed.
The old qualified kernel is unchanged. There is no tag partition, prefilter,
reranker or implicit remote provider.

Generation builds go into an explicit `independent-lane-generations` experiment
store and never write CURRENT or `retrieval-runtime.json`. `Generation.index()`
executes the carried kernel's actual one-BM25F/one-cosine search. The new schema
is deliberately not accepted by the installed v1 dispatcher. Deployment needs
a qualified self-contained release and its managed-path validation; a saved
experiment manifest or passing unit tests alone do not activate this path.

Verified split-document contracts/builders remain useful inactive assets after
a quality HOLD. Old issued runs keep their original sealed code and receipts.
