"""Optional, content-addressed slot BM25F derivations. No network clients."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

SCHEMA = "photo-core-slot-bm25f-cache/v1"


def canonical_bytes(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_digest(value) -> str:
    return digest(canonical_bytes(value))


def decode(raw: bytes):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid JSON constant: {value}")))


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def cache_key(slot_hash: str, algorithm_hash: str) -> str:
    return json_digest({"cache_schema": SCHEMA, "slot_corpus_sha256": slot_hash,
                        "bm25f_algorithm_sha256": algorithm_hash})


class CoreSlotIndexStore:
    def __init__(self, root: Path):
        self.root = Path(root)

    def create(self, corpus_json: str, algorithm_hash: str, builder, *, proposed=None) -> dict:
        expected = builder(corpus_json)
        if proposed is not None and proposed != expected:
            raise ValueError("slot cache differs from full source-derived BM25F statistics")
        raw = canonical_bytes(expected)
        if decode(raw) != expected:
            raise ValueError("slot cache serialization changed its derivation")
        payload_hash = digest(raw)
        relative = f"core-slot-index-data/{payload_hash}.json"
        target = self.root / relative
        if not target.exists() or target.read_bytes() != raw:
            atomic_write(target, raw)
        slot_hash = digest(corpus_json.encode("utf-8"))
        return {"schema": SCHEMA, "slot_corpus_sha256": slot_hash,
                "bm25f_algorithm_sha256": algorithm_hash,
                "slot_cache_key": cache_key(slot_hash, algorithm_hash),
                "document_count": len(expected["documents"]),
                "document_ids_sha256": json_digest(sorted(expected["documents"])),
                "payload": {"path": relative, "sha256": payload_hash, "bytes": len(raw)}}

    def load(self, metadata: dict, corpus_json: str, algorithm_hash: str, builder) -> tuple[dict, str]:
        """Metadata comes from the pinned generation, never from a cache file."""
        try:
            slot_hash = digest(corpus_json.encode("utf-8"))
            if (metadata["schema"] != SCHEMA or metadata["slot_corpus_sha256"] != slot_hash
                    or metadata["bm25f_algorithm_sha256"] != algorithm_hash
                    or metadata["slot_cache_key"] != cache_key(slot_hash, algorithm_hash)):
                raise ValueError("stale slot cache binding")
            payload = metadata["payload"]
            expected_path = f"core-slot-index-data/{payload['sha256']}.json"
            if payload["path"] != expected_path or len(payload["sha256"]) != 64:
                raise ValueError("invalid slot cache path")
            target = self.root / expected_path
            if target.is_symlink():
                raise ValueError("slot cache must be a regular runtime-owned file")
            raw = target.read_bytes()
            if digest(raw) != payload["sha256"] or len(raw) != payload["bytes"]:
                raise ValueError("slot cache checksum mismatch")
            index = decode(raw)
            if (len(index["documents"]) != metadata["document_count"]
                    or json_digest(sorted(index["documents"])) != metadata["document_ids_sha256"]):
                raise ValueError("slot cache document inventory mismatch")
            return index, "hit"
        except (OSError, ValueError, KeyError, TypeError):
            # A required source/index failure never reaches this function.
            return builder(corpus_json), "fallback"
