# Exact two-file DATA thin-bundle transfer

This Git bundle contains commit `cd52f366f0b27ca16a20edef2b64cfea8de07c3a`, whose sole parent/prerequisite is integrated PR5 main `0efc2dfde7de9693799d3c84618705332e59920c`. Its two changed files are the reviewed Korean palace aliases and the genuinely cached rebuilt visual index. It contains no generated images, credentials, authentication configuration, runtime implementation or V12 successor. The bundle uses the existing parent objects as delta bases, so the 32,334,024-byte resulting index does not need to be retransmitted in full.

The exact file and bundle hashes are in TRANSFER-MANIFEST.json. Preserve this DATA commit identity for the V12 provenance proof. Do not recreate it with a different commit SHA.

## Verify before any branch publication

Use an already authorized repository checkout with the prerequisite present. Reading/fetching the existing main is sufficient; do not alter main. Verify the downloaded bundle SHA-256, then run:

```
git cat-file -e 0efc2dfde7de9693799d3c84618705332e59920c^{commit}
git bundle verify /absolute/path/architecture-data-cd52f366.bundle
git bundle list-heads /absolute/path/architecture-data-cd52f366.bundle
```

The bundle must name only the single included branch ref from the manifest. If the target remote branch already exists with any different head, stop; do not overwrite or force-push.

Import under a separate local DATA branch:

```
git fetch /absolute/path/architecture-data-cd52f366.bundle refs/heads/data/v12-architecture-zero-delta-20261004:refs/heads/data/v12-architecture-data-20261004
git rev-list --parents -n 1 data/v12-architecture-data-20261004
git diff --name-only 0efc2dfde7de9693799d3c84618705332e59920c data/v12-architecture-data-20261004
```

Require the exact commit and sole parent above, and exactly the two manifest paths. Use `git show COMMIT:PATH | sha256sum` to verify both resulting full file hashes and `git rev-parse COMMIT:PATH` to verify each Git blob ID. No source reconstruction or provider call is needed.

Only if separately instructed to publish this work branch, use the ordinary non-force refspec and verify it:

```
git push origin refs/heads/data/v12-architecture-data-20261004:refs/heads/data/v12-architecture-data-20261004
git ls-remote origin refs/heads/data/v12-architecture-data-20261004
```

No command here merges, pushes or changes main. This DATA-only commit intentionally does not resolve the existing V11 source-pin rejection. It must not be promoted to main alone: the reviewed immutable V12 successor and the DATA must pass their joint final checks first. The separate V12 implementation remains under local development and independent review.
