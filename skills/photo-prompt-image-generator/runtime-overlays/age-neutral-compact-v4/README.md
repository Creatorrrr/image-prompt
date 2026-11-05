# Age-neutral compact display

This overlay contains the code used by the installed H-F2 generation recorded
in `BASE.json`. It keeps native owner and gate references intact and projects
reviewed identifiers to neutral display names. Positive source meaning,
conditions, and native decision bindings remain source-bound. The additional
inventory is tied to exact source hashes; a mismatch fails closed.

The overlay is not an index or an installed runtime. The selected generation,
its candidate snapshot, vectors, search index, and model files live in the
local runtime store and must be made available separately. Committing the
overlay or `retrieval-runtime.json` does not upload or install those files.
Existing runs continue to use the generation bound to their receipt.
