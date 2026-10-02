"""Merge authored JSON by identity; rebuild indexes from immutable parent caches."""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ASSETS = Path("skills/photo-prompt-image-generator/assets")
REGISTRY = ASSETS / "photo_prompt_visual_obligations.json"
TAGS = ASSETS / "photo_prompt_tags.json"
SEMANTIC = ASSETS / "photo_prompt_semantic_index.json"
VISUAL = ASSETS / "photo_prompt_visual_profile_index.json"
sys.path.insert(0, str(ROOT / ASSETS.parent / "scripts"))
import prompt_generator as pg
import build_semantic_index as semantic_builder

MISSING = object()

def git_bytes(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)

def git_json(ref, path): return json.loads(git_bytes(ref, path))
def sha(raw): return hashlib.sha256(raw).hexdigest()
def clone(value): return value if value is MISSING else copy.deepcopy(value)
def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def merge_json(base, local, remote, path=""):
    if local == remote: return clone(local)
    if local == base: return clone(remote)
    if remote == base: return clone(local)
    if all(isinstance(v, dict) for v in (base, local, remote)):
        result = {}
        for key in dict.fromkeys([*base, *local, *remote]):
            value = merge_json(base.get(key, MISSING), local.get(key, MISSING), remote.get(key, MISSING), path + "." + key)
            if value is not MISSING: result[key] = value
        return result
    if all(isinstance(v, list) for v in (base, local, remote)):
        if all(all(isinstance(r, dict) and "id" in r for r in v) for v in (base, local, remote)):
            mappings = [{r["id"]: r for r in v} for v in (base, local, remote)]
            assert all(len(m) == len(v) for m, v in zip(mappings, (base, local, remote))), path
            result = []
            for key in dict.fromkeys([*mappings[0], *mappings[1], *mappings[2]]):
                value = merge_json(*(m.get(key, MISSING) for m in mappings), path + f"[id={key}]")
                if value is not MISSING: result.append(value)
            return result
        if local[:len(base)] == remote[:len(base)] == base:
            result = copy.deepcopy(base)
            for value in [*local[len(base):], *remote[len(base):]]:
                if value not in result: result.append(copy.deepcopy(value))
            return result
    raise ValueError("Overlapping authored meaning requires review: " + path)

def semantic_snapshot(ref):
    manifest = git_json(ref, SEMANTIC)
    entries = {}
    for descriptor in manifest["shards"]:
        raw = git_bytes(ref, ASSETS / descriptor["path"])
        assert sha(raw) == descriptor["sha256"]
        rows = json.loads(raw)["entries"]
        assert len(rows) == descriptor["entry_count"] and not entries.keys() & rows.keys()
        entries.update(rows)
    assert set(entries) == set(manifest["entry_order"]) and len(entries) == manifest["entry_count"]
    manifest["entries"] = entries
    return manifest

def changed_paths(base, ref):
    return set(subprocess.check_output(["git", "diff", "--name-only", base, ref], cwd=ROOT, text=True).splitlines())

def choose_vector(key, text, caches, expected, counts, provenance):
    matches = []
    for name, cache in caches.items():
        assert all(cache.get(k) == expected[k] for k in ("provider", "embedding_model", "embedding_dimensions"))
        row = cache["entries"].get(key)
        if isinstance(row, dict) and row.get("text") == text:
            vector = row.get("vector")
            assert isinstance(vector, list) and len(vector) == expected["embedding_dimensions"]
            assert all(isinstance(v, (int, float)) and math.isfinite(v) for v in vector)
            matches.append((name, vector))
    assert matches, "No exact-text compatible parent vector: " + key
    if len(matches) == 2: assert matches[0][1] == matches[1][1], "Parent vector disagreement: " + key
    category = "both" if len(matches) == 2 else matches[0][0] + "_only"
    counts[category] += 1
    provenance[key] = {"parent": matches[0][0], "text_sha256": sha(text.encode())}
    return copy.deepcopy(matches[0][1])

def main(local, remote):
    base = subprocess.check_output(["git", "merge-base", local, remote], cwd=ROOT, text=True).strip()
    paths = {"local": changed_paths(base, local), "remote": changed_paths(base, remote)}
    shared = paths["local"] & paths["remote"]
    allowed_shared = {str(p) for p in (REGISTRY, TAGS, SEMANTIC, VISUAL)}
    assert shared <= allowed_shared, sorted(shared - allowed_shared)
    exclusive = []
    concurrent_documents = []
    for name, ref in (("local", local), ("remote", remote)):
        for path in sorted(paths[name] - shared):
            raw = git_bytes(ref, path)
            working = (ROOT / path).read_bytes()
            if working != raw:
                # Another active task is editing research documents. Preserve
                # its worktree bytes while checking the parent's staged blob.
                assert path.startswith("docs/"), "Concurrent runtime source change: " + path
                staged = subprocess.check_output(["git", "show", f":{path}"], cwd=ROOT)
                assert staged == raw, "Exclusive staged parent source changed: " + path
                concurrent_documents.append({"path": path, "staged_parent_sha256": sha(raw),
                                             "observed_working_sha256": sha(working)})
            exclusive.append({"path": path, "parent": name, "sha256": sha(raw)})
    registry_parents = {name: git_json(ref, REGISTRY) for name, ref in (("base", base), ("local", local), ("remote", remote))}
    merged = merge_json(registry_parents["base"], registry_parents["local"], registry_parents["remote"])
    expected_tags = merge_json(git_json(base, TAGS), git_json(local, TAGS), git_json(remote, TAGS))
    assert json.loads((ROOT / TAGS).read_text()) == expected_tags
    by = {name: {r["id"]: r for r in value["profiles"]} for name, value in registry_parents.items()}
    modifications = {name: [pid for pid, row in value.items() if row != by["base"].get(pid)] for name, value in by.items() if name != "base"}
    assert not set(modifications["local"]) & set(modifications["remote"])
    (ROOT / REGISTRY).write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
    save("source-preservation.json", {"local_parent": local, "remote_parent": remote, "merge_base": base,
        "exclusive_parent_blobs_exactly_preserved": len(exclusive), "exclusive_files": exclusive,
        "concurrent_working_documents_left_unstaged": concurrent_documents,
        "shared_authored_files": [str(p) for p in (REGISTRY, TAGS) if str(p) in shared],
        "shared_parent_paths": sorted(shared), "main_registry_profiles": len(merged["profiles"]),
        "local_modified_profile_ids": modifications["local"], "remote_modified_profile_ids": modifications["remote"],
        "overlapping_modified_profile_ids": [], "merged_raw_registry_sha256": sha((ROOT / REGISTRY).read_bytes()),
        "merged_raw_tags_sha256": sha((ROOT / TAGS).read_bytes())})

    data = pg.load_json(ROOT / TAGS)
    registry = pg.load_visual_obligation_registry(ROOT / REGISTRY)
    expected = semantic_builder.base_payload(data, pg.SEMANTIC_PROVIDER, pg.SEMANTIC_MODEL_ID, pg.DEFAULT_SEMANTIC_DIMENSIONS)
    caches = {"local": semantic_snapshot(local), "remote": semantic_snapshot(remote)}
    visual_caches = {"local": git_json(local, VISUAL), "remote": git_json(remote, VISUAL)}
    semantic_counts, visual_counts = Counter(), Counter()
    semantic_provenance, visual_provenance = {}, {}
    bm25f = pg.build_semantic_bm25f_payload(data)
    entries = {}
    for key, kind, row, slot in pg.iter_semantic_entries(data):
        text = pg.semantic_text_for_entry(row, slot, kind=kind)
        vector = choose_vector(key, text, caches, expected, semantic_counts, semantic_provenance)
        entries[key] = {"kind": kind, "slot": slot, "id": row["id"], "text": text,
                        "vector": vector, "bm25f_document": bm25f["documents"][key]}
    vectors = {}
    for profile in registry["profiles"]:
        pid = profile["id"]
        vectors[pid] = choose_vector(pid, pg.visual_profile_semantic_text(profile), visual_caches,
                                    expected, visual_counts, visual_provenance)
    semantic = {**expected, "entries": entries,
                "bm25f": {key: value for key, value in bm25f.items() if key != "documents"}}
    pg.validate_semantic_index_metadata(semantic, data)
    visual = pg.build_visual_profile_index_payload(registry, vectors=vectors,
        provider=expected["provider"], model=expected["embedding_model"], dimensions=expected["embedding_dimensions"])
    manifest = semantic_builder.write_sharded_payload(ROOT / SEMANTIC, semantic, keep_stale_generations=True)
    (ROOT / VISUAL).write_text(json.dumps(visual, ensure_ascii=False, indent=2) + "\n")
    actual_semantic = pg.load_semantic_index_payload(ROOT / SEMANTIC)
    pg.validate_semantic_index_metadata(actual_semantic, data)
    pg.load_visual_profile_index(ROOT / VISUAL, registry)
    assert actual_semantic["entries"] == entries
    report = {"local_parent": local, "remote_parent": remote, "dictionary_hash": expected["dictionary_hash"],
        "registry_sha256": visual["registry_sha256"], "semantic_entries": len(entries),
        "visual_profiles": len(vectors), "exact_terms": len(visual["exact_lookup"]),
        "semantic_exact_text_cache": dict(semantic_counts), "visual_exact_text_cache": dict(visual_counts),
        "cache_misses": 0, "embedding_api_calls": 0, "historical_shards_deleted": 0,
        "bm25f": "recomputed from merged authored data", "file_backed_validation": "PASS",
        "semantic_shards": [str(ASSETS / row["path"]) for row in manifest["shards"]],
        "semantic_entry_provenance": semantic_provenance, "visual_entry_provenance": visual_provenance}
    save("index-reconciliation.json", report)
    print(json.dumps({k: v for k, v in report.items() if not k.endswith("provenance") and k != "semantic_shards"}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", required=True)
    parser.add_argument("--remote", required=True)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    OUT = args.output.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    main(args.local, args.remote)
