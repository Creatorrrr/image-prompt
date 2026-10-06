# Muted-color contrast guidance and immutable V28 boundary

V28 qualifies a source guidance consistency correction. It replaces the ambiguous copied Korean negative example “배경도 함께 선명해짐” with “초점 영역의 채도가 주변만큼 높아져 채도 차이가 사라짐” at exactly three existing leaves for muted-on-vivid. The corrected example describes loss of the intended relative saturation difference.

This is not evidence of an automatic rejection defect or a retrieval, adoption, routing, or image-quality improvement. The target profile and bundle were absent in all three natural before/after pairs. No new images or provider requests were made.

## Scope and provenance

- Previous qualified main: `cb496c1db984f9fe5d632fa764aae4d3f6aedf63`, tree `805043fc6538967e5fef600e042ac7cdf3f81ffe`
- Local DATA input: `873525b100749b68015c1dc0eff5b00cd4fbfa2d`, tree `175a360b3a46eaa6f774fb0ba5518916bce58972`; this local pin is not a remote publication claim
- Three negative text leaves in two color source files; one immutable successor maintenance record and its two reference leaves; one header hash replacement in each index manifest
- All positive source fields, aliases, ownership, activation, components, gates, candidate rows, and the opposite color relation remain exact
- All 10,124 ordinary and 1,921 visual canonical texts and stored vectors remain exact; all 32 active shard bytes, paths, ordering, and references remain exact
- Every original V1–V27 baseline artifact remains unchanged; 47 original baseline/pack files were independently checked against cb496 Git blobs

The frozen V28 pack differs from V27 only at `/0/provenance/tags_hash` and `/0/pack_id`. All 64 candidates, their content and ordering, the authored scene, locks, controls, negative prompt, privacy boundary, and prompt-budget v3 are identical. Each natural pair also changes one bundle's source-dictionary binding, with no change to candidate identities, content, or ordering. [SOURCE-QUALITY-EVIDENCE.json](SOURCE-QUALITY-EVIDENCE.json) records the compact comparisons and their limits.

## Immutable replay and checks

[V28-MUTED-COLOR-PROOF.json](V28-MUTED-COLOR-PROOF.json) seals the exact source deltas, original maintenance record, successor record, source inventory, active shards, evidence, and frozen pack. The validator rejects additional source changes, evidence rehashing, candidate or scene changes, index changes, and missing, altered, or unsafe historical files. The universal descriptor changes only its validator hash.

[V27-PARENT-SOURCE.json](V27-PARENT-SOURCE.json) seals 1,040 original files from cb496. Six snapshot paths reuse 9,271,553 bytes of existing Git blobs; they introduce no new Git blob payload and no large archive. Other historical files are reused in place. The archived V27 validator retains its original strict version range and source pins, including rejection of version 28. Live V27 validation still rejects the new DATA source.

The narrow fixture transition accepts only the four sealed current DATA files and returns authenticated historical bytes. Arbitrary live drift, rollback of current index headers to V27, altered V27/V26 snapshots, missing or rehashed proof/manifest files, historical/proof-path symlinks, and incorrect modes fail closed. A live DATA symlink resolving to identical expected bytes is accepted; this does not permit content drift. Original V27 test assertions remain intact and execute against cb496 source.

[QUALIFICATION.json](QUALIFICATION.json) lists each unique passing test ID by boundary, exact source hashes, actual replay results, guard results, and earlier environment-only attempts. Duplicate reruns are excluded. The broader suite was not rerun; the three previously known failures were neither changed nor counted as passes.

## Reproduce offline

Run from a complete checkout with an existing Python interpreter at `.venv/bin/python`. No dependency installation or credentials are needed. The guard permits only the exact frozen generator subprocess, blocks network and credential access, and installs the same guard in that subprocess. Guard initialization failure terminates the subprocess.

```sh
replay_dir="$PWD/docs/research-evidence/photo-prompt/muted-color-contrast-20261006/offline-replay"
env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$replay_dir" V28_GUARD_LOG=/tmp/muted-color-replay-guard.jsonl \
  python3 -S -B "$replay_dir/run_tests_offline.py" \
  tests.test_photo_muted_color_boundary_history \
  tests.test_photo_color_relations \
  tests.test_photo_appearance_boundary_history \
  tests.test_photo_scene_budget_boundary_history
```

Historical replay creates temporary copies of its authenticated sources and removes those temporary fixtures afterward. It does not change the retained source files or fetch replacements from Git or the network.
