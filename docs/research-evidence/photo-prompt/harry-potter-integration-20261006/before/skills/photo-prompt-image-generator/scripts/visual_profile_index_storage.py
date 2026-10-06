"""Deterministic, integrity-checked storage for visual-profile index entries.

Storage never changes the logical payload or its insertion order. Legacy JSON
remains readable for historical fixtures and incremental cache migration.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FORMAT = "visual-profile-sharded-json-v1"
STORAGE_KEYS = {"storage", "entry_count", "entry_order", "shards"}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key in visual profile index: {key}")
        result[key] = value
    return result


def _decode(raw):
    return json.loads(raw, object_pairs_hook=_unique_object)


def _bytes(payload):
    return (json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _bucket(key, count):
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest(), 16) % count


def load_visual_profile_index_payload(path):
    """Materialize either a legacy index or a verified sharded manifest."""
    path = Path(path)
    payload = _decode(path.read_bytes())
    if not isinstance(payload, dict):
        raise ValueError("visual profile index must be an object")
    if "storage" not in payload:
        if not isinstance(payload.get("entries"), dict):
            raise ValueError("legacy visual profile index must contain entries")
        return payload
    storage = payload["storage"]
    if not isinstance(storage, dict) or storage.get("format") != FORMAT or storage.get("hash_algorithm") != "sha256":
        raise ValueError("Unsupported visual profile index storage")
    count = storage.get("shard_count")
    if type(count) is not int or count < 1:
        raise ValueError("Invalid visual profile shard count")
    order, rows = payload.get("entry_order"), payload.get("shards")
    if (not isinstance(order, list) or any(not isinstance(key, str) for key in order)
            or len(order) != len(set(order))):
        raise ValueError("Invalid or duplicate visual profile entry_order")
    if type(payload.get("entry_count")) is not int or payload["entry_count"] != len(order):
        raise ValueError("Visual profile manifest entry count mismatch")
    if "entries" in payload or not isinstance(rows, list) or len(rows) != count:
        raise ValueError("Invalid visual profile shard descriptors")
    entries, seen_paths = {}, set()
    root = path.parent.resolve()
    for index, row in enumerate(rows):
        sid = f"{index:0{max(3, len(str(count - 1)))}d}"
        if not isinstance(row, dict) or row.get("id") != sid:
            raise ValueError("Invalid or duplicate visual profile shard id")
        relative = row.get("path")
        digest = row.get("sha256")
        if not isinstance(relative, str) or not relative or not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("Invalid visual profile shard path/checksum")
        shard_path = (root / relative).resolve()
        if root not in shard_path.parents or shard_path in seen_paths:
            raise ValueError("Visual profile shard path escapes directory or is duplicated")
        seen_paths.add(shard_path)
        raw = shard_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"Visual profile shard checksum mismatch: {relative}")
        shard = _decode(raw)
        if not isinstance(shard, dict) or shard.get("schema_version") != 1 or shard.get("shard_id") != sid:
            raise ValueError("Invalid visual profile shard identity")
        part = shard.get("entries")
        if not isinstance(part, dict) or type(row.get("entry_count")) is not int or row["entry_count"] != len(part):
            raise ValueError("Visual profile shard entry count mismatch")
        if set(entries) & set(part):
            raise ValueError("Duplicate visual profile entry across shards")
        if any(_bucket(key, count) != index for key in part):
            raise ValueError("Visual profile entry in wrong hash shard")
        entries.update(part)
    if set(entries) != set(order):
        raise ValueError("Visual profile manifest does not match shard entries")
    result = {key: value for key, value in payload.items() if key not in STORAGE_KEYS}
    result["entries"] = {key: entries[key] for key in order}
    return result


def _write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == raw:
        return
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def write_sharded_visual_profile_index(path, payload, shard_count=16):
    """Write immutable content-addressed shards, then atomically switch manifest.

    Unreferenced old shards are retained: readers of the previous manifest remain
    valid during publication. They can be removed explicitly after readers finish.
    """
    path = Path(path)
    if type(shard_count) is not int or shard_count < 1:
        raise ValueError("shard_count must be a positive integer")
    entries = payload.get("entries")
    if not isinstance(entries, dict) or any(not isinstance(key, str) for key in entries):
        raise ValueError("visual profile entries must be a string-keyed object")
    buckets = [{} for _ in range(shard_count)]
    for key, entry in entries.items():
        buckets[_bucket(key, shard_count)][key] = entry
    rows = []
    for index, part in enumerate(buckets):
        sid = f"{index:0{max(3, len(str(shard_count - 1)))}d}"
        raw = _bytes({"schema_version": 1, "shard_id": sid, "entries": part})
        digest = hashlib.sha256(raw).hexdigest()
        relative = f"{path.stem}_shards/shard-{sid}-{digest}.json"
        _write(path.parent / relative, raw)
        rows.append({"id": sid, "path": relative, "entry_count": len(part), "sha256": digest})
    manifest = {key: value for key, value in payload.items() if key != "entries" and key not in STORAGE_KEYS}
    manifest.update(storage={"format": FORMAT, "hash_algorithm": "sha256", "shard_count": shard_count},
                    entry_count=len(entries), entry_order=list(entries), shards=rows)
    _write(path, _bytes(manifest))
    return manifest
