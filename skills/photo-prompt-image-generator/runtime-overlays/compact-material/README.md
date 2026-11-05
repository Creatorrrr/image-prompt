# Compact H-F2 material view overlay

This overlay stages the compact result view and decision binding against the
exact installed parent recorded in `BASE.json`. It preserves that parent's
candidate snapshot, indexes and vectors. It does not rebuild or publish them.
The parent release must be separately available in the runtime store.

Stage both listed members with `stage_photo_h_f2_code.py`, qualify the resulting
release, and install it using the procedure in `references/installed-h-f2.md`.
The tracked `retrieval-runtime.json` may select a different release; committing
this overlay does not install or activate it. Existing runs remain bound to their
original releases.
