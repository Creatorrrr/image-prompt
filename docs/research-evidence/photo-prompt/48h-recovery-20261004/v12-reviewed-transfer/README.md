# Reviewed V12 source: branch-only transfer

Exact source `62b0ba99960fb580c0f1bc07a17b0e3041a08fc2` was independently approved within the scope and limits in the manifest. Its immediate prerequisite is the already published DATA commit `cd52f366f0b27ca16a20edef2b64cfea8de07c3a`. This bundle preserves the original commit identity and includes the DATA plus successor through that ancestry. It does not contain keys, authentication configuration or generated images.

The same source bytes had an earlier provisional durability backup; the original provisional artifact remains unchanged. This copy is accompanied by the later completed qualification and independent-review receipts. Approval is for these exact source bytes, not further edits or a claim that every repository test passes.

## Verify and import

After checking bundle SHA256 against TRANSFER-MANIFEST.json, use an existing authorized repository with the prerequisite. Do not change main or credentials.

```
git cat-file -e cd52f366f0b27ca16a20edef2b64cfea8de07c3a^{commit}
git bundle verify /absolute/path/v12-maintenance-reviewed-62b0ba99.bundle
git bundle list-heads /absolute/path/v12-maintenance-reviewed-62b0ba99.bundle
git fetch /absolute/path/v12-maintenance-reviewed-62b0ba99.bundle refs/heads/data/v12-architecture-zero-delta-20261004:refs/heads/data/v12-architecture-reviewed-20261004
git rev-list --parents -n 1 data/v12-architecture-reviewed-20261004
git rev-parse data/v12-architecture-reviewed-20261004^{tree}
```

Require the manifest commit, sole prerequisite parent and tree. Stop if the destination branch already has a different head; do not overwrite or force. If explicitly instructed to publish this work branch, use only:

```
git push origin refs/heads/data/v12-architecture-reviewed-20261004:refs/heads/data/v12-architecture-reviewed-20261004
git ls-remote origin refs/heads/data/v12-architecture-reviewed-20261004
```

This procedure creates no PR and performs no main merge/push. DATA and V12 must remain together for any separately authorized final integration. The DATA-only parent alone fails the old V11 source pin.

## Qualification limits

All 1447 discovered test IDs have aggregate coverage, but the single discovery attempt was interrupted and six methods still fail identically on unchanged integrated main. Focused transition checks and actual V12 replay pass; explicit live V11 remains strict. Synthetic-fixture guard errors and the history-object skip are preserved alongside their separate successful reruns. The two-alias fix repairs five source-guided wrong-hard cases, with six valid-old Korean render gates lost and four unrelated unselected optional displacements. It does not prove natural-query recall or rendered-image quality.
