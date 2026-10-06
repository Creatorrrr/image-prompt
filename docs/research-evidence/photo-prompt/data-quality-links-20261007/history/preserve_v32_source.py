"""Preserve exact V32 Git identities without copying the old replay closure again.

This offline authoring helper is not loaded by either production runtime.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PIN = "96e20422316276a4e0b5ed97f44152e4931e7504"
OLD = ROOT / "docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006"
PHOTO = "skills/photo-prompt-image-generator/assets/"
ILLUSTRATION = "skills/subculture-illustration-image-generator/"
SNAPSHOT = HERE / "v32-parent-source-files"
CHANGED = {
    PHOTO + "photo_prompt_visual_obligations.json",
    PHOTO + "photo_prompt_photorealism_elements_extension.json",
    PHOTO + "photo_prompt_realistic_background_extension.json",
    PHOTO + "photo_prompt_semantic_index.json",
    PHOTO + "photo_prompt_visual_profile_index.json",
    ILLUSTRATION + "scripts/validate_illustration_assets.py",
    ILLUSTRATION + "assets/universal_scene_baseline_v2.json",
    "tests/photo_prompt_fixtures.py",
    "tests/test_photo_robe_source_boundary_history.py",
}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def identity(raw, mode, blob):
    actual_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if actual_blob != blob:
        raise AssertionError("Git payload identity drift")
    return dict(mode=mode, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), git_blob=blob)


def main():
    previous = json.loads((OLD / "V31-PARENT-SOURCE.json").read_bytes())
    proof = json.loads((OLD / "V32-ROBE-SOURCE-PROOF.json").read_bytes())
    tree = {}
    for line in subprocess.check_output(["git", "ls-tree", "-r", PIN], cwd=ROOT, text=True).splitlines():
        fields, name = line.split("\t", 1)
        mode, kind, blob = fields.split()
        if kind == "blob":
            tree[name] = mode, blob
    prior = {row["path"]: row for row in previous["members"]}
    paths = set(prior) | CHANGED | {row["source_path"] for row in previous["members"]}
    for field in ("source_files_after", "active_shards_after", "retained_shards_before",
                  "evidence_files", "frozen_inputs"):
        paths.update(proof[field])
    paths.update({(OLD / "V32-ROBE-SOURCE-PROOF.json").relative_to(ROOT).as_posix(),
                  (OLD / "V31-PARENT-SOURCE.json").relative_to(ROOT).as_posix(),
                  proof["maintenance_successor"]["path"],
                  ILLUSTRATION + "assets/photo_regression_baseline_v32.json",
                  ILLUSTRATION + "assets/photo_regression_baseline_v32_pack.json"})
    rows = []
    for name in sorted(paths):
        mode, blob = tree[name]
        old = prior.get(name)
        if (name not in CHANGED and old is not None
                and (old["mode"], old["git_blob"]) == (mode, blob)):
            raw = (ROOT / old["source_path"]).read_bytes()
            source = old["source_path"]
            kind = "reuse_authenticated_v31_backing"
            if hashlib.sha256(raw).hexdigest() != old["sha256"]:
                raise AssertionError(f"Old backing drift: {name}")
        else:
            raw = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=ROOT)
            source = name
            kind = "retained_exact_git_blob"
            if (ROOT / name).read_bytes() != raw:
                source = (SNAPSHOT / name).relative_to(ROOT).as_posix()
                kind = "new_immutable_snapshot_same_git_blob"
        if name in CHANGED:
            source = (SNAPSHOT / name).relative_to(ROOT).as_posix()
            kind = "new_immutable_snapshot_same_git_blob"
        record = identity(raw, mode, blob)
        if kind == "new_immutable_snapshot_same_git_blob":
            target = ROOT / source
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != raw:
                raise AssertionError(f"Refusing to revise preserved source: {name}")
            target.write_bytes(raw)
            target.chmod(int(mode[-3:], 8))
        rows.append(dict(path=name, source_path=source, git_commit=PIN, git_path=name,
                         kind=kind, **record))
    manifest = dict(
        schema="photo-v32-parent-source-manifest/v1", source_pin=PIN,
        source_tree=subprocess.check_output(["git", "rev-parse", PIN + "^{tree}"],
                                            cwd=ROOT, text=True).strip(),
        member_count=len(rows), total_member_bytes=sum(row["bytes"] for row in rows),
        counts={kind: sum(row["kind"] == kind for row in rows)
                for kind in sorted({row["kind"] for row in rows})},
        new_snapshot_bytes=sum(row["bytes"] for row in rows
                               if row["kind"] == "new_immutable_snapshot_same_git_blob"),
        members=rows,
    )
    path = HERE / "V32-PARENT-SOURCE.json"
    raw = encoded(manifest)
    path.write_bytes(raw)
    print(json.dumps({key: value for key, value in manifest.items() if key != "members"}))
    print("manifest_sha256=" + hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
