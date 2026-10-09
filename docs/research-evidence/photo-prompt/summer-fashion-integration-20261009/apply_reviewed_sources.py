"""Apply only reviewed additive sources and fresh derived files to the primary."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

WORKTREE = Path(__file__).resolve().parents[4]
PRIMARY = Path("/Users/chasoik/Projects/image-prompt")
HERE = Path(__file__).resolve().parent
DEST_EVIDENCE = PRIMARY / "docs/research-evidence/photo-prompt/summer-fashion-integration-20261009"
SKILL_REL = Path("skills/photo-prompt-image-generator")
sys.path.insert(0, str(PRIMARY / SKILL_REL / "scripts"))
from photo_runtime_sources import source_update, SnapshotPublisher


def signature(path):
    return dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), mode=path.stat().st_mode & 0o777, bytes=path.stat().st_size)


def main():
    before = json.loads((HERE / "workspace-before.json").read_text())
    scope = json.loads((HERE / "integration-scope.json").read_text())
    source_files = set(scope["new_source_files"])
    derived = {str(SKILL_REL / "assets" / name) for name in (
        "photo_prompt_source_manifest.json", "photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json")}
    concurrent_test = "tests/test_photo_autumn_fashion_semantics.py"
    expected = {}
    for rel, original in before["files"].items():
        p = PRIMARY / rel
        current = signature(p)
        if rel not in derived and rel != concurrent_test and current != original:
            raise RuntimeError("Unreviewed primary drift: " + rel)
        expected[rel] = current
    wa = WORKTREE / SKILL_REL / "assets"
    pa = PRIMARY / SKILL_REL / "assets"
    wm = json.loads((wa / "photo_prompt_source_manifest.json").read_text())
    pm = json.loads((pa / "photo_prompt_source_manifest.json").read_text())
    base_wm = {**wm, "sources": [s for s in wm["sources"] if s["file"] not in source_files]}
    assert base_wm == pm, "Concurrent registration requires a new identity merge and index validation."
    for row in pm["sources"]:
        assert signature(pa / row["file"]) == signature(wa / row["file"]), row["file"]
    for name in source_files:
        if (pa / name).exists():
            assert signature(pa / name) == signature(wa / name), "Owned source collision: " + name
    DEST_EVIDENCE.mkdir(parents=True, exist_ok=True)
    (DEST_EVIDENCE / "primary-application-baseline.json").write_text(json.dumps(expected, indent=2) + "\n")
    copied = []
    with source_update(PRIMARY / SKILL_REL):
        # Preserve the current primary registration objects, then append ours.
        merged = {**pm, "sources": [*pm["sources"], *[s for s in wm["sources"] if s["file"] in source_files]]}
        assert merged == wm
        for file in source_files:
            shutil.copy2(wa / file, pa / file)
            copied.append(str(SKILL_REL / "assets" / file))
        for domain in ["clothing_structure", "coverage", "fit", "ornament", "style", "swimwear", "textile"]:
            name = f"summer-fashion-{domain}-20261009.json"
            rel = Path("docs/research-evidence/photo-prompt/extension-maintenance") / name
            if (PRIMARY / rel).exists():
                assert signature(PRIMARY / rel) == signature(WORKTREE / rel), "Maintenance record collision."
            (PRIMARY / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(WORKTREE / rel, PRIMARY / rel)
            copied.append(str(rel))
        for name in ["photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"]:
            payload = json.loads((wa / name).read_text())
            for shard in payload["shards"]:
                src = wa / shard["path"]
                assert hashlib.sha256(src.read_bytes()).hexdigest() == shard["sha256"]
                target = pa / shard["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    assert target.read_bytes() == src.read_bytes()
                else:
                    shutil.copy2(src, target)
                copied.append(str(SKILL_REL / "assets" / shard["path"]))
            shutil.copy2(wa / name, pa / name)
            copied.append(str(SKILL_REL / "assets" / name))
        (pa / "photo_prompt_source_manifest.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
        copied.append(str(SKILL_REL / "assets/photo_prompt_source_manifest.json"))
        test_rel = Path("tests/test_photo_summer_fashion_semantics.py")
        if (PRIMARY / test_rel).exists():
            assert (PRIMARY / test_rel).read_bytes() == (WORKTREE / test_rel).read_bytes()
        shutil.copy2(WORKTREE / test_rel, PRIMARY / test_rel)
        copied.append(str(test_rel))
    pointer = SnapshotPublisher(PRIMARY / SKILL_REL).publish()
    (DEST_EVIDENCE / "primary-runtime-pointer.json").write_text(json.dumps(pointer, indent=2) + "\n")
    protected = {rel: row for rel, row in expected.items() if rel not in derived}
    drift = [rel for rel, row in protected.items() if signature(PRIMARY / rel) != row]
    receipt = dict(status="pass" if not drift else "fail", protected_files_checked=len(protected),
                   protected_drift=drift, applied_files=copied, current_primary_concurrent_test_preserved=signature(PRIMARY / concurrent_test) == expected[concurrent_test],
                   generation_id=pointer.get("generation_id"), source_fingerprint=pointer.get("source_fingerprint"), revision=pointer.get("revision"))
    (DEST_EVIDENCE / "primary-application-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "applied_files"}, ensure_ascii=False))
    print(json.dumps(pointer, ensure_ascii=False))
    assert not drift


if __name__ == "__main__":
    main()
