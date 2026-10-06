#!/usr/bin/env python3
"""Copy only this task's qualified data after checking the original snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
PRIMARY = OUT.parents[3]
ASSET_PREFIX = Path("skills/photo-prompt-image-generator/assets")
TEST_PATH = Path("tests/test_photo_harry_appearance_semantics.py")


def sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def save(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def replace_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".harry-integration-tmp")
    if temporary.exists():
        raise RuntimeError(f"Refusing to replace an existing temporary file: {temporary}")
    shutil.copy2(source, temporary)
    os.replace(temporary, target)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    start = json.loads((OUT / "START-SNAPSHOT.json").read_text())
    adoption = json.loads((OUT / "ADOPTION-MANIFEST.json").read_text())
    checkout = Path(start["worktree"])
    targets = [ASSET_PREFIX / n for n in adoption["source_files_changed"]]
    index_paths = [ASSET_PREFIX / n for n in start["generated_index_hashes"]]
    conflicts = []
    preservation = []
    concurrent_runtime = []
    for relative, expected in start["source_hashes"].items():
        path = Path(relative)
        primary_hash, checkout_hash = sha(PRIMARY / path), sha(checkout / path)
        if primary_hash != expected:
            if path.is_relative_to(ASSET_PREFIX):
                conflicts.append({"path": relative, "reason": "primary authored data changed after snapshot"})
            elif path not in targets:
                concurrent_runtime.append({"path": relative, "start_sha256": expected,
                                           "current_sha256": primary_hash,
                                           "action": "PRESERVE_CURRENT_PRIMARY_WITHOUT_REPLACEMENT"})
        if path not in targets and checkout_hash != expected:
            conflicts.append({"path": relative, "reason": "unowned checkout source changed"})
        if path not in targets:
            preservation.append({"path": relative, "start_sha256": expected,
                                 "pre_sync_sha256": primary_hash, "current_sha256": primary_hash})
    for path in targets:
        if str(path) not in start["source_hashes"] and (PRIMARY / path).exists():
            conflicts.append({"path": str(path), "reason": "new target already exists in primary"})
    if (PRIMARY / TEST_PATH).exists():
        conflicts.append({"path": str(TEST_PATH), "reason": "new regression test already exists"})
    for path in index_paths:
        if sha(PRIMARY / path) != start["generated_index_hashes"][path.name]:
            conflicts.append({"path": str(path), "reason": "primary index manifest changed after snapshot"})
    shards = []
    for path in index_paths:
        manifest = json.loads((checkout / path).read_text())
        for row in manifest["shards"]:
            relative = ASSET_PREFIX / row["path"]
            if relative.is_absolute() or ".." in relative.parts:
                raise RuntimeError("Invalid manifest shard path")
            expected = row["sha256"]
            if sha(checkout / relative) != expected:
                conflicts.append({"path": str(relative), "reason": "checkout shard hash mismatch"})
            existing = sha(PRIMARY / relative)
            if existing not in (None, expected):
                conflicts.append({"path": str(relative), "reason": "existing primary shard has different bytes"})
            shards.append({"path": str(relative), "sha256": expected, "already_present": existing == expected})
    receipt = {"status": "PREFLIGHT_PASS" if not conflicts else "CONFLICT_STOP",
               "primary": str(PRIMARY), "checkout": str(checkout),
               "source_targets": [str(p) for p in targets], "new_test": str(TEST_PATH),
               "index_manifests": [str(p) for p in index_paths], "declared_active_shards": shards,
               "unrelated_snapshot_sources_preserved": preservation, "conflicts": conflicts,
               "concurrent_runtime_changes_preserved": concurrent_runtime,
               "no_historical_shard_deletion": True, "commit_push_performed": False}
    save(OUT / "PRIMARY-SYNC-PREFLIGHT.json", receipt)
    if conflicts:
        raise RuntimeError(f"Stopped with {len(conflicts)} conflicts; no files copied")
    if not args.apply:
        print(f"Preflight PASS: {len(targets)} authored files, one test, {len(shards)} declared shards, two manifests")
        return
    qualified_paths = [*targets, TEST_PATH, *index_paths]
    qualified = {str(p): sha(checkout / p) for p in qualified_paths}
    # Preserve the previous manifest bytes; all historical shard files remain in place.
    for path in index_paths:
        backup = OUT / "before" / path
        if backup.exists() and sha(backup) != sha(PRIMARY / path):
            raise RuntimeError(f"Backup conflict: {backup}")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PRIMARY / path, backup)
    for row in shards:
        if not row["already_present"]:
            replace_file(checkout / row["path"], PRIMARY / row["path"])
    for path in [*targets, TEST_PATH]:
        replace_file(checkout / path, PRIMARY / path)
    # Publish manifests only after all declared shard bytes are installed.
    for path in index_paths:
        replace_file(checkout / path, PRIMARY / path)
    for relative, expected in qualified.items():
        if sha(PRIMARY / relative) != expected:
            raise RuntimeError(f"Post-copy hash mismatch: {relative}")
    for row in preservation:
        if sha(PRIMARY / row["path"]) != row["pre_sync_sha256"]:
            raise RuntimeError(f"Unrelated source drift during sync: {row['path']}")
    receipt.update(status="APPLIED_HASH_VERIFIED", qualified_checkout_hashes=qualified,
                   changed_paths=[str(p) for p in qualified_paths] + [r["path"] for r in shards if not r["already_present"]])
    save(OUT / "PRIMARY-SYNC.json", receipt)
    print(f"Applied and verified {len(qualified_paths)} source/test/manifest files; preserved {len(preservation)} unrelated sources")


if __name__ == "__main__":
    main()
