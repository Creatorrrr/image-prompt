# Pinned baseline regression: complete coverage, non-green result

Source pin: `7e769e3e4a0da7068723830bb0c5c5c2dfd784c8`.

All 158 discovered test modules executed, running 1,367 test methods. 152 modules exited successfully and six did not. There are 10 failed assertion entries (including subtests), four error entries and no skipped tests. **This is not a green full suite.** Counts of failed subtests are not counts of distinct test methods.

## Non-green modules

- Korean emotional semantics: three subtests require the same frozen JPEG in a local user Downloads directory, absent in this environment
- Makeup reference balance: a historical source-observation JSON and five frozen core artifacts are absent
- Poverty semantics: three historical result artifacts are absent
- Rare-photo semantics: three historical reference/result artifacts are absent
- Illustration contract v1: one aggregate-validation error due to current frozen photo candidate-pack byte drift
- Illustration universal scene v3: two errors at the same photo candidate-pack byte check

The photo baseline validator passes its frozen-input, scene/composition-preservation and public-provenance checks before failing the whole-pack byte comparison. The cause of the byte drift is being separately audited; it must not be assumed to be an environment-only failure or dismissed as harmless. No existing baseline has been rewritten to turn the check green.

## Execution provenance

The first qualified session completed 74 modules before an executor transport disconnect. Its next-module log remained empty and progress stayed stale beyond the configured 600-second module timeout. That partial run and log were preserved, a STOP marker was installed, and all 84 unfinished modules were executed in a separate resumed session at the identical clean source pin. The interrupted module passed on resume. The final resumed runner confirmed unchanged HEAD and a clean tree.

An earlier, separate harness attempt omitted the repository import path; it was stopped and preserved. Those harness import errors are not included in the qualified 158-module result. No test was silently excluded, no missing artifact was fabricated, and no provider credential was deliberately supplied. The run is sequential per session but is not described as one uninterrupted process.

This pinned run is baseline evidence only. It does not validate later DATA patches or remote runtime changes. Exact method IDs, failures, errors, per-module durations, source hashes, scripts and logs are retained in the evidence archive.
