"""Preserve both authored parents and rebuild their merged semantic index.

Only exact-key, exact-text vectors from immutable Git snapshots are reused.
No environment file or embedding client is used. Historical shards are kept.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
ASSETS = Path("skills/photo-prompt-image-generator/assets")
MANIFEST = ASSETS / "photo_prompt_semantic_index.json"
TAGS = ASSETS / "photo_prompt_tags.json"
NEW_REQUIRED = {
    "photo_prompt_clothing_structure_extension.json",
    "photo_prompt_textile_surface_extension.json",
    "photo_prompt_accessory_structure_extension.json",
    "photo_prompt_traditional_clothing_detail_extension.json",
}
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as generator
import build_semantic_index as builder


def git_bytes(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stripped_required(value):
    if isinstance(value, dict):
        return {key: stripped_required(item) for key, item in value.items()}
    if isinstance(value, list):
        return [stripped_required(item) for item in value
                if not (isinstance(item, str) and item in NEW_REQUIRED)]
    return value


def snapshot(ref):
    manifest = json.loads(git_bytes(ref, MANIFEST))
    entries = {}
    for shard in manifest["shards"]:
        raw = git_bytes(ref, ASSETS / shard["path"])
        assert sha(raw) == shard["sha256"]
        rows = json.loads(raw)["entries"]
        assert len(rows) == shard["entry_count"]
        assert not entries.keys() & rows.keys()
        entries.update(rows)
    assert len(entries) == manifest["entry_count"]
    assert set(entries) == set(manifest["entry_order"])
    manifest["entries"] = entries
    return manifest


def changed_paths(base, ref):
    return set(subprocess.check_output(
        ["git", "diff", "--name-only", base, ref], cwd=ROOT, text=True
    ).splitlines())


def save(name, payload):
    Path(__file__).with_name(name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", required=True)
    parser.add_argument("--remote", required=True)
    args = parser.parse_args()
    local = subprocess.check_output(["git", "rev-parse", args.local], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(["git", "rev-parse", args.remote], cwd=ROOT, text=True).strip()
    base = subprocess.check_output(["git", "merge-base", local, remote], cwd=ROOT, text=True).strip()
    local_paths, remote_paths = changed_paths(base, local), changed_paths(base, remote)
    shared = local_paths & remote_paths
    assert shared == {str(MANIFEST), str(TAGS)}, sorted(shared)
    proofs = []
    for label, ref, paths in (("local", local, local_paths), ("remote", remote, remote_paths)):
        for path in sorted(paths - shared):
            raw = git_bytes(ref, path)
            assert (ROOT / path).read_bytes() == raw, path
            proofs.append({"path": path, "source_parent": label, "sha256": sha(raw)})
    local_tags = json.loads(git_bytes(local, TAGS))
    remote_tags = json.loads(git_bytes(remote, TAGS))
    base_tags = json.loads(git_bytes(base, TAGS))
    merged_tags = json.loads((ROOT / TAGS).read_text())
    assert stripped_required(local_tags) == base_tags
    assert stripped_required(merged_tags) == remote_tags
    for filename in NEW_REQUIRED:
        assert filename in json.dumps(merged_tags)
    save("source-preservation.json", {
        "local_parent": local, "remote_parent": remote, "merge_base": base,
        "exclusive_changed_paths_exactly_preserved": len(proofs),
        "tags": "exact remote cleaned source plus the four local required extensions",
        "local_validator_and_runtime": "byte-identical to local parent",
        "clothing_source_and_image_evidence": "byte-identical to local parent",
        "cleanup_rows_and_evidence": "byte-identical to remote parent",
        "files": proofs,
    })
    data = generator.load_json(ROOT / TAGS)
    expected = builder.base_payload(data, generator.SEMANTIC_PROVIDER, generator.SEMANTIC_MODEL_ID, 768)
    caches = {"local": snapshot(local), "remote": snapshot(remote)}
    for cache in caches.values():
        assert builder.metadata_matches(cache, expected)
        assert cache["semantic_text_recipe"] == generator.SEMANTIC_TEXT_RECIPE_VERSION
    bm25f = generator.build_semantic_bm25f_payload(data)
    entries, provenance, counts = {}, {}, Counter()
    for key, kind, entry, slot in generator.iter_semantic_entries(data):
        text = generator.semantic_text_for_entry(entry, slot, kind=kind)
        matches = []
        for name, cache in caches.items():
            row = cache["entries"].get(key)
            if row and row["text"] == text:
                vector = row["vector"]
                assert len(vector) == 768 and all(math.isfinite(v) for v in vector)
                matches.append((name, row))
        assert matches, f"Missing exact-text cached vector: {key}"
        if len(matches) == 2:
            assert matches[0][1]["vector"] == matches[1][1]["vector"], key
        name, row = matches[0]
        counts["both" if len(matches) == 2 else name + "_only"] += 1
        entries[key] = {"kind": kind, "slot": slot, "id": entry["id"],
                        "text": text, "vector": row["vector"],
                        "bm25f_document": bm25f["documents"][key]}
        provenance[key] = {"parent": name, "text_sha256": sha(text.encode())}
    payload = dict(expected)
    payload["entries"] = entries
    payload["bm25f"] = {key: value for key, value in bm25f.items() if key != "documents"}
    generator.validate_semantic_index_metadata(payload, data)
    builder.write_sharded_payload(ROOT / MANIFEST, payload, keep_stale_generations=True)
    loaded = generator.load_semantic_index(ROOT / MANIFEST, data)
    assert loaded["entries"] == entries
    report = {
        "local_parent": local, "remote_parent": remote,
        "dictionary_hash": expected["dictionary_hash"],
        "entry_count": len(entries), "exact_cache_matches": dict(counts),
        "cache_misses": 0, "embedding_api_calls": 0,
        "bm25f": "recomputed from merged runtime dictionary",
        "file_backed_loader_validation": "PASS", "historical_shards": "preserved",
        "entry_provenance": provenance,
    }
    save("index-reconciliation.json", report)
    print(json.dumps({key: value for key, value in report.items() if key != "entry_provenance"}))


if __name__ == "__main__":
    main()
