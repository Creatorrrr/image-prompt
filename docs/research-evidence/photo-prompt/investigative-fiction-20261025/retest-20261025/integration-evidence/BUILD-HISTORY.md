# Build and processing history

The active, reproducible release recipe is `rebase_code_release.py` using the
explicit current release in `release-base.json`. See `successor.json`,
`post-install-preservation.json`, and `installed-runtime-preflight.json`.

Earlier `build_release.py` / `finish_release.py` attempts are retained as
historical attempts, not instructions to rerun against the rebased base. A
worker imported from the old executable closure was correctly refused after
the one-file coordinator change. A fresh staged worker then correctly refused
a whole `.runtime` directory symlink: the immutable model package was copied
inside the stage and every file hash checked, while only its Python
environment is linked. No freshness, model safety or publisher assertion was
removed. The stale data-only build was interrupted before activation when the
shared release advanced. The final rebase preserves that current source and
all vectors, adds only the reviewed coordinator code, and runs normal complete
publisher, H-F2, installer and recorder checks.

These are build/processing attempts. They are not extra candidate samples or
image calls. Arm B's failed binding attempt remains separately recorded, and
its recovered run retains all 17 authoring/control hashes.
