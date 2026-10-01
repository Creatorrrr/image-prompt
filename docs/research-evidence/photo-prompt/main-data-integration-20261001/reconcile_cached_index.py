"""Reconcile this merge's semantic index from exact-text cached vectors only.

No environment file is loaded and no embedding client is called. Both Git
snapshots are immutable, and every output document must match a compatible
cached text and a finite 768-dimensional vector. Run from the repository root.
"""
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as generator
import build_semantic_index as builder

LOCAL = "0e5a98b549a497b576f64edad4f446d594174b28"
UPSTREAM = "0087e876bc4bc4a086c01977e77ba54e5499d6f2"
ASSETS = Path("skills/photo-prompt-image-generator/assets")
MANIFEST = ASSETS / "photo_prompt_semantic_index.json"
EXPECTED_HASH = "f0d9e292e189135c064ab271b254163d73b2c9977595f18e1e03460aa6eec0c9"


def git_bytes(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)


def read_snapshot(ref):
    manifest = json.loads(git_bytes(ref, MANIFEST))
    entries = {}
    for shard in manifest["shards"]:
        raw = git_bytes(ref, ASSETS / shard["path"])
        assert hashlib.sha256(raw).hexdigest() == shard["sha256"]
        rows = json.loads(raw)["entries"]
        assert len(rows) == shard["entry_count"]
        assert not entries.keys() & rows.keys()
        entries.update(rows)
    assert set(entries) == set(manifest["entry_order"])
    assert len(entries) == manifest["entry_count"]
    manifest["entries"] = entries
    return manifest


def main():
    data = generator.load_json(ROOT / ASSETS / "photo_prompt_tags.json")
    assert generator.dictionary_hash(data) == EXPECTED_HASH
    local, upstream = read_snapshot(LOCAL), read_snapshot(UPSTREAM)
    expected = builder.base_payload(data, generator.SEMANTIC_PROVIDER,
                                    generator.SEMANTIC_MODEL_ID, 768)
    for snapshot in [local, upstream]:
        assert builder.metadata_matches(snapshot, expected)
        assert snapshot["semantic_text_recipe"] == generator.SEMANTIC_TEXT_RECIPE_VERSION
    bm25f = generator.build_semantic_bm25f_payload(data)
    entries, provenance, counts = {}, {}, Counter()
    for key, kind, entry, slot in generator.iter_semantic_entries(data):
        text = generator.semantic_text_for_entry(entry, slot, kind=kind)
        candidates = []
        for name, snapshot in [("local", local), ("upstream", upstream)]:
            row = snapshot["entries"].get(key)
            if row and row["text"] == text:
                vector = row.get("vector", [])
                assert len(vector) == 768 and all(math.isfinite(v) for v in vector)
                candidates.append((name, row))
        assert candidates, f"No exact-text compatible cached vector: {key}"
        selected_name, selected = candidates[0]
        category = "both" if len(candidates) == 2 else selected_name + "_only"
        counts[category] += 1
        if len(candidates) == 2:
            assert candidates[0][1]["vector"] == candidates[1][1]["vector"], key
        entries[key] = {
            "kind": kind, "slot": slot, "id": entry["id"], "text": text,
            "vector": copy.deepcopy(selected["vector"]),
            "bm25f_document": bm25f["documents"][key],
        }
        provenance[key] = {"source": selected_name, "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
    assert len(entries) == 9887
    assert counts == {"both": 9717, "local_only": 37, "upstream_only": 133}
    payload = dict(expected)
    payload["entries"] = entries
    payload["bm25f"] = {key: value for key, value in bm25f.items() if key != "documents"}
    generator.validate_semantic_index_metadata(payload, data)
    builder.write_sharded_payload(ROOT / MANIFEST, payload, keep_stale_generations=True)
    reloaded = generator.load_semantic_index(ROOT / MANIFEST, data)
    assert reloaded["entries"] == entries
    report = {
        "upstream_commit": UPSTREAM, "cleanup_commit": LOCAL,
        "dictionary_hash": EXPECTED_HASH, "documents": len(entries),
        "exact_text_cache_matches": dict(counts), "cache_misses": 0,
        "api_calls": 0, "additional_cost_usd": 0,
        "bm25f": "recomputed from merged dictionary",
        "loader_validation": "passed", "stale_generations": "preserved",
        "entry_kinds": dict(Counter(row["kind"] for row in entries.values())),
        "entry_provenance": provenance,
    }
    (Path(__file__).parent / "index-reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "entry_provenance"}, indent=2))


if __name__ == "__main__":
    main()
