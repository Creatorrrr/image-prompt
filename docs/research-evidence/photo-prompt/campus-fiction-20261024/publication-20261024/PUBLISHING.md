# Campus semantics and requester query publication

Source commit: `0c740c75d9ea4433a20fca91bcaebe023215713c`.

The publication branch was created from `origin/main` at `f41dd84089acce7d87f864630760c428ab3898a7`. After the source commit, `git pull --no-rebase origin main` completed with “Already up to date”. All preexisting candidate and binding modules remain byte-identical to that main version; the campus modules are appended to its manifest. Unrelated working-tree policy edits and machine-specific installed-runtime configuration are preserved outside this publication.

The merged authored source contains 21,987 candidates and 16,811 bindings. The search index was rebuilt from that source with the pinned embedding space, reusing only recipe/text/model-compatible vectors. No provider call was needed. Full index verification and independent dictionary validation passed. The 32 original research snapshot files retain their recorded checksums.

The 72 focused publication tests passed using the publication producer, auditor and neutral modules with deployed H-F2 v4 expression/query support. Main’s legacy v2 query lane remains unchanged. See FOCUSED-TESTS.json and VALIDATION-NOTES.md for the runtime boundary.

The three independent reference-image retests and their original artifacts are retained. New campus sources contributed to two actual prompts; strict full-scene new-source pixel qualification remains 0/3. Partial results, technical checks and user acceptance remain separate in ../query-core-retest-20261024/RESULTS.md.

The derived-index commit will be merged explicitly into an integration branch based on origin/main, then pushed to main without force. Final local, tracking and live-remote SHA receipts and cleanup verification are recorded in this directory after publication.
