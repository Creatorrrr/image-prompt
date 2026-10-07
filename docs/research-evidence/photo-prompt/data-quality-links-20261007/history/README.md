# V33 DATA scope successor and unchanged V32 history

The V33 boundary covers three authored applicability corrections found while testing independent prompts. The cello profile now requires both seated support and active bowing and excludes bow inspection. The casual human crop and shared hair/clothing wind candidates now declare `kind` and `for_any` as `human`. Their strings, definitions, relations, declared links, candidate ordering, and earlier qualification outcomes remain unchanged.

This is an explicit successor because V32 binds the complete authored inventory, generated index identities, and current candidate pack bytes. Reusing V32 against the newer sources would misrepresent historical evidence. No V1–V32 baseline, pack, proof, fixture expectation, or source snapshot was revised.

`photo_regression_baseline_v33.json` records six added DATA leaves and five candidate-pack leaf changes. Four pack changes are retrieval or provenance bindings. The fifth is the actual motion candidate total, `34 → 33`, after making the wind candidate human-only. Every public candidate object and its order, the 64-candidate public boundary, frozen core, controls, review, composition, and negative string stay exact.

`V32-PARENT-SOURCE.json` authenticates the original V32 source at commit `96e20422316276a4e0b5ed97f44152e4931e7504`, tree `ae809d09bc01042c15b77271764036871d28949d`. The 1,377 members total 2,609,717,339 bytes. Only nine changed backing files require new physical snapshots, totaling 12,620,835 bytes. The rest reuse exact authenticated historical sources or retained Git identities. Eight previous backup files are explicit replay dependencies in addition to their original destination files.

The current fixture helper fixes the complete manifest and V33 proof SHA-256 values in code, checks regular paths and ancestors, and authenticates byte count, SHA-256, Git blob identity, and file mode. A current V33 source must match its reviewed after hash before the helper returns an archived V32 identity; arbitrary drift or a rollback cannot activate historical recovery. Missing or changed proof, manifest, archive, identity, mode, or unsafe path fails closed. Materialization validates before writing and stages an atomic destination. It uses no Git or network fallback.

The original `test_photo_robe_source_boundary_history.py` is preserved by its exact Git blob, hash, and mode inside the manifest. Its live entry point only restores the original source, publishes an isolated original runtime snapshot before the existing request budget, and executes the unchanged 28-test module. V32 validation similarly dispatches to its exact original validator in a separate process. V33 tests live in the new `test_photo_data_scope_boundary_history.py`.

V32 originally ran on CPython 3.12.14 with Unicode 15.0.0; V33 runs on the project's current CPython 3.14.3 environment. Python and Unicode are part of the original generation fingerprint. An explicit `PHOTO_HISTORY_PYTHON` executable path must match exactly and cannot silently fall back. Otherwise the dispatcher probes the current interpreter, bundled local Python, and version-specific local executable. It accepts only exact equality to the sealed original environment and clearly fails if none matches. `V32-PYTHON-ENVIRONMENT.json` records the actual selected child executable, required and observed versions, and unchanged original proof identity. It does not spoof environment fields or revise expected hashes.

`INDEX-VECTOR-REUSE-PROOF.json` records an independent comparison of all 10,396 semantic and 2,193 visual-profile entry identities. Provider, model, dimensions, recipe, exact text, and vector remain equal to V32. This comparison establishes vector reuse, while the separate parent-owned rebuild log records API-call behavior.

The first V32 test replay lacked those eight backup dependencies and failed during setup. `V32-ORIGINAL-TESTS.initial.log` preserves that attempt. Dependency closure was completed from the same original Git tree. A second replay passed 27 assertions and failed the real receipt assertion because it used Python 3.14.3. `V32-ORIGINAL-TESTS.environment-mismatch.log` preserves that attempt. The dispatcher was corrected to select the original compatible local runtime; no original assertion was changed. Current test and replay logs are separate evidence files.

The final original V32 module passes all 28 unchanged tests (`V32-ORIGINAL-TESTS.log`, 136.401 seconds). Its live dispatcher passes (`V32-DISPATCHER-TEST.log`, 164.985 seconds). The V33 module passes its 14 tests present in that run, and a separate run verifies the additional explicit-override rejection together with both existing interpreter-selection gates. The requested-version V32 CLI path also passes (`V32-DISPATCH-CLI-TEST.log`, 59.892 seconds). These runs cover all 16 distinct tests currently in the V33 module. `QUALIFICATION-RESULTS.json` records the final evidence. `OWNED-CHANGES.json` records before/after file hashes and the independent check that 132 frozen baseline, pack, input, and V32 evidence files stay unchanged against the original source pin.

All results here concern source, retrieval, prompt preflight, history integrity, and runtime receipt binding. They do not qualify native image pixels or user acceptance and do not relabel any earlier image failure.

Offline verification uses the project's existing Python environment:

```sh
.venv/bin/python -m unittest tests.test_photo_data_scope_boundary_history tests.test_photo_robe_source_boundary_history -v
```

The offline authoring helpers `preserve_v32_source.py` and `build_v33_boundary.py` reproduce the source mapping and successor evidence. Runtime and historical replay use the authenticated artifacts; they never execute these authoring helpers or query Git to recover missing inputs.
