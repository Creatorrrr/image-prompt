# Clothing semantics and DATA cleanup merge

This merge retains both parents: local `a1e08cc0c4de109bd38f463cc9cd0211cf21b418`
and remote `558e5cbfe0e1139f620c1322b943c5624dbb486f`. Their common base is
`0087e876bc4bc4a086c01977e77ba54e5499d6f2`.

The local parent contributes 287 clothing candidates and visual profiles,
294 visual gates, 30 optional combinations, four paired source extensions,
the scoped candidate-validator repair, and three original image experiments.
The remote parent contributes the completed cleanup of 37 source rows and its
regressions and evidence. Every exclusively changed parent file remains
byte-identical, including the research and image records.

The shared tag dictionary contains the exact remote cleaned source plus the
four local required clothing extensions. Neither parent's source intent was
replaced with the other parent's version. `source-preservation.json` records
the file hashes and structured dictionary checks.

Only the generated semantic-index manifest conflicted. It was rebuilt from
the combined runtime dictionary using exact-key, exact-text compatible vectors
from both immutable parent caches:

- 10,174 entries: 9,850 found in both caches, 287 only in the local cache, and
  37 only in the remote cache
- Provider, model, 768-dimensional vector shape and text recipe verified
- Shared matching vectors verified identical; zero cache misses
- BM25F recomputed from the merged runtime data
- Zero embedding API calls; historical shard generations preserved
- Dictionary hash `3d06f6624ea62e8db289089624bfd3fe52a7506cbaf3ad11c62644461f6c5cc3`

`reconcile_parents.py` reproduces the source checks and regenerated index.
It does not read an environment file or invoke an embedding client.

The merged tree passes all 42 tests in the clothing-terminology, next-slot
cleanup, scene cleanup and lighting-semantics modules. Dictionary metadata,
semantic index and visual index checks also pass. The unchanged visual registry
contains 1,385 profiles and 3,305 exact terms. `validation.json` and the adjacent
logs record the checks.

This is a focused merge verification. The previously recorded broader fixture
mismatches remain historical limitations, and no new image or pixel evaluation
was run. The original three clothing images retain their frozen pre-merge
dictionary and prompt bindings; their pixel evidence is not relabeled as an
evaluation of the merged retrieval dictionary.
