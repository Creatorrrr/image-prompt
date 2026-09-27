"""Read-only comparison with the checked-out base, including retained old shards."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = Path("skills/photo-prompt-image-generator/assets")
BASE = "766c327d23d721bfc4bc459e4d596a4563fa7264"


def read(path, old=False):
    raw = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT) if old else (ROOT / path).read_bytes()
    return json.loads(raw), raw


def semantic_entries(old=False):
    manifest, _ = read(ASSETS / "photo_prompt_semantic_index.json", old)
    if "entries" in manifest:
        return manifest["entries"]
    entries = {}
    for shard in manifest["shards"]:
        path = ASSETS / shard["path"]
        payload, raw = read(path, old)
        assert hashlib.sha256(raw).hexdigest() == shard["sha256"], path
        if old:
            assert (ROOT / path).read_bytes() == raw, f"Historical shard modified: {path}"
        entries.update(payload["entries"])
    assert len(entries) == manifest["entry_count"]
    return entries


def main():
    report = {"base_revision": BASE, "scope": "Unchanged base text/vectors and old generation preservation; no rendered-quality evidence."}
    for kind in ("semantic", "visual"):
        if kind == "semantic":
            old, new = semantic_entries(True), semantic_entries()
        else:
            old = read(ASSETS / "photo_prompt_visual_profile_index.json", True)[0]["entries"]
            new = read(ASSETS / "photo_prompt_visual_profile_index.json")[0]["entries"]
        removed = sorted(old.keys() - new.keys())
        same_vector = sum(new.get(key, {}).get("vector") == row["vector"] for key, row in old.items())
        same_text = sum(new.get(key, {}).get("text") == row["text"] for key, row in old.items())
        report.update({f"{kind}_old": len(old), f"{kind}_new": len(new),
                       f"{kind}_added": len(new.keys() - old.keys()), f"{kind}_removed": removed,
                       f"{kind}_old_vectors_unchanged": same_vector, f"{kind}_old_texts_unchanged": same_text})
        assert not removed
        assert same_vector == same_text == len(old)
    report["base_semantic_generation_preserved"] = True
    (HERE / "embedding-reuse.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
