#!/usr/bin/env python3
"""Build the Gemini semantic index for the photo prompt dictionary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    SEMANTIC_PROVIDER,
    SEMANTIC_TEXT_RECIPE_VERSION,
    dictionary_hash,
    embed_texts_with_gemini,
    iter_semantic_entries,
    load_json,
    load_semantic_index_payload,
    SEMANTIC_INDEX_SHARDED_FORMAT,
    semantic_dimensions_value,
    semantic_text_for_entry,
)


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} or key in os.environ:
            continue
        value = value.strip().strip("\"'")
        if value:
            os.environ[key] = value


def base_payload(data, provider: str, model: str, dimensions: int) -> dict:
    return {
        "provider": provider,
        "dictionary_hash": dictionary_hash(data),
        "semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
        "embedding_model": model,
        "embedding_dimensions": semantic_dimensions_value(dimensions),
        "entries": {},
    }


def checkpoint_path_for(output: Path, explicit: str | Path | None = None) -> Path:
    if explicit:
        return Path(explicit)
    return output.with_name(output.name + ".partial")


def metadata_matches(payload: dict, expected: dict, require_dictionary_hash: bool = False) -> bool:
    keys = ["provider", "semantic_text_recipe", "embedding_model", "embedding_dimensions"]
    if require_dictionary_hash:
        keys.append("dictionary_hash")
    return all(payload.get(key) == expected.get(key) for key in keys)


def load_payload(path: Path) -> dict | None:
    if not path.exists():
        return None
    return load_semantic_index_payload(path)


def load_reusable_entries(paths: Sequence[Path], expected: dict) -> dict:
    entries: dict = {}
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        payload = load_payload(path)
        if not payload or not metadata_matches(payload, expected, require_dictionary_hash=False):
            continue
        for key, cached in payload.get("entries", {}).items():
            if isinstance(cached, dict):
                entries[key] = cached
    return entries


def load_checkpoint(path: Path, expected: dict, cache_indexes: Sequence[Path] = ()) -> dict:
    payload = dict(expected)
    payload["entries"] = load_reusable_entries([*cache_indexes, path], expected)
    return payload


def write_payload(path: Path, payload: dict, *, compact: bool = False) -> None:
    """Atomically persist JSON, optionally without generated-artifact whitespace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    if compact:
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    else:
        serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def prune_stale_shard_generations(path: Path, keep_generation: str) -> list[str]:
    """Remove prior generated shard directories after a new manifest is durable."""
    shard_parent = path.with_name(f"{path.stem}_shards")
    if not shard_parent.is_dir():
        return []

    removed = []
    for candidate in shard_parent.iterdir():
        if candidate.name == keep_generation or candidate.is_symlink() or not candidate.is_dir():
            continue
        shutil.rmtree(candidate)
        removed.append(candidate.name)
    return sorted(removed)


def write_sharded_payload(
    path: Path,
    payload: dict,
    shard_count: int = 16,
    *,
    keep_stale_generations: bool = False,
) -> dict:
    """Persist vectors in stable hash shards and return the written manifest."""
    count = int(shard_count)
    if count < 1:
        raise ValueError("shard_count must be at least 1")
    entries = payload.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("semantic index payload must contain an entries object")

    buckets: list[dict] = [{} for _ in range(count)]
    for key, value in entries.items():
        bucket = int(hashlib.sha256(str(key).encode("utf-8")).hexdigest(), 16) % count
        buckets[bucket][key] = value

    generation = str(payload.get("dictionary_hash") or "unversioned")[:16]
    shard_root = path.with_name(f"{path.stem}_shards") / generation
    width = max(3, len(str(count - 1)))
    shard_rows = []
    for index, shard_entries in enumerate(buckets):
        shard_id = f"{index:0{width}d}"
        shard_path = shard_root / f"shard-{shard_id}.json"
        shard_payload = {
            "schema_version": 1,
            "shard_id": shard_id,
            "entries": shard_entries,
        }
        write_payload(shard_path, shard_payload, compact=True)
        raw = shard_path.read_bytes()
        shard_rows.append(
            {
                "id": shard_id,
                "path": str(shard_path.relative_to(path.parent)),
                "entry_count": len(shard_entries),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )

    manifest = {key: value for key, value in payload.items() if key != "entries"}
    manifest.update(
        {
            "storage": {
                "format": SEMANTIC_INDEX_SHARDED_FORMAT,
                "hash_algorithm": "sha256",
                "shard_count": count,
            },
            "entry_count": len(entries),
            "entry_order": list(entries),
            "shards": shard_rows,
        }
    )
    write_payload(path, manifest)
    if not keep_stale_generations:
        prune_stale_shard_generations(path, generation)
    return manifest


def build_resumable_index_payload(
    data,
    output: Path,
    checkpoint: Path,
    provider: str,
    model: str,
    dimensions: int,
    batch_size: int,
    request_interval: float,
    retry_attempts: int,
    retry_initial_delay: float,
    cache_indexes: Sequence[Path] = (),
    progress_callback=None,
) -> dict:
    if provider != SEMANTIC_PROVIDER:
        raise ValueError(f"Unsupported semantic provider '{provider}'. Only '{SEMANTIC_PROVIDER}' is supported.")
    dims = semantic_dimensions_value(dimensions)
    batch = max(1, int(batch_size))
    rows = iter_semantic_entries(data)
    expected = base_payload(data, provider, model, dims)
    payload = load_checkpoint(checkpoint, expected, cache_indexes=cache_indexes)
    entries = payload.setdefault("entries", {})

    pending = []
    for key, kind, entry, slot in rows:
        text = semantic_text_for_entry(entry, slot)
        cached = entries.get(key)
        if (
            cached
            and cached.get("text") == text
            and isinstance(cached.get("vector"), list)
            and len(cached["vector"]) == dims
        ):
            continue
        pending.append((key, kind, entry, slot, text))

    completed = len(rows) - len(pending)
    if progress_callback and completed:
        progress_callback(completed, len(rows))

    for start in range(0, len(pending), batch):
        chunk = pending[start : start + batch]
        vectors = embed_texts_with_gemini(
            [row[4] for row in chunk],
            model=model,
            dimensions=dims,
            retry_attempts=retry_attempts,
            retry_initial_delay=retry_initial_delay,
        )
        if len(vectors) != len(chunk):
            raise RuntimeError(f"Gemini returned {len(vectors)} embeddings for {len(chunk)} input texts.")
        for (key, kind, entry, slot, text), vector in zip(chunk, vectors):
            entries[key] = {
                "kind": kind,
                "slot": slot,
                "id": entry.get("id"),
                "text": text,
                "vector": vector,
            }
        completed += len(chunk)
        write_payload(checkpoint, payload)
        if progress_callback:
            progress_callback(completed, len(rows))
        if request_interval > 0 and completed < len(rows):
            import time

            time.sleep(request_interval)

    ordered_entries = {}
    for key, _kind, _entry, _slot in rows:
        if key not in entries:
            raise RuntimeError(f"Missing semantic vector for {key}.")
        ordered_entries[key] = entries[key]
    payload["entries"] = ordered_entries
    return payload


def main() -> int:
    load_project_env()
    parser = argparse.ArgumentParser(description="Build a Gemini embedding semantic index JSON.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    parser.add_argument("--output", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_semantic_index.json")
    parser.add_argument("--provider", choices=[SEMANTIC_PROVIDER], default=SEMANTIC_PROVIDER)
    parser.add_argument("--model", default=SEMANTIC_MODEL_ID)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_SEMANTIC_DIMENSIONS)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--request-interval", type=float, default=0.8, help="Seconds to sleep between Gemini requests.")
    parser.add_argument("--retry-attempts", type=int, default=4, help="Retry count for Gemini 429 RESOURCE_EXHAUSTED responses.")
    parser.add_argument("--retry-initial-delay", type=float, default=15.0, help="Initial retry sleep in seconds for Gemini 429 responses.")
    parser.add_argument("--checkpoint", default=None, help="Partial index path used for resumable builds. Defaults to OUTPUT.partial.")
    parser.add_argument("--keep-checkpoint", action="store_true", help="Keep the partial checkpoint after a successful final write.")
    parser.add_argument("--shard-count", type=int, default=16, help="Stable hash-shard count for the final index (default: 16).")
    parser.add_argument("--monolithic", action="store_true", help="Write a legacy single-file index instead of the default sharded format.")
    parser.add_argument(
        "--keep-stale-generations",
        action="store_true",
        help="Keep older shard generations after the new manifest is written.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Do not reuse compatible vectors from an existing output index.")
    parser.add_argument("--progress", action="store_true", help="Print embedding progress without vector values.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned index metadata without calling the Gemini API or writing output.")
    args = parser.parse_args()

    data = load_json(args.tags)
    entry_count = len(iter_semantic_entries(data))

    if args.dry_run:
        print(
            json.dumps(
                {
                    "provider": args.provider,
                    "semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
                    "embedding_model": args.model,
                    "embedding_dimensions": args.dimensions,
                    "entries": entry_count,
                    "storage_format": "monolithic" if args.monolithic else SEMANTIC_INDEX_SHARDED_FORMAT,
                    "shard_count": 0 if args.monolithic else args.shard_count,
                    "output": str(args.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        def progress(done: int, total: int) -> None:
            if done == total or done % 50 == 0:
                print(f"Embedded {done}/{total} entries", flush=True)

        out = Path(args.output)
        checkpoint = checkpoint_path_for(out, args.checkpoint)
        cache_indexes = [] if args.no_cache else [out]
        payload = build_resumable_index_payload(
            data,
            output=out,
            checkpoint=checkpoint,
            dimensions=args.dimensions,
            provider=args.provider,
            model=args.model,
            batch_size=args.batch_size,
            request_interval=args.request_interval,
            retry_attempts=args.retry_attempts,
            retry_initial_delay=args.retry_initial_delay,
            cache_indexes=cache_indexes,
            progress_callback=progress if args.progress else None,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    payload["created_at"] = datetime.now(timezone.utc).isoformat()

    out = Path(args.output)
    if args.monolithic:
        write_payload(out, payload)
        storage_description = "monolithic JSON"
    else:
        write_sharded_payload(
            out,
            payload,
            shard_count=args.shard_count,
            keep_stale_generations=args.keep_stale_generations,
        )
        storage_description = f"{args.shard_count} JSON shards"
    checkpoint = checkpoint_path_for(out, args.checkpoint)
    if checkpoint.exists() and not args.keep_checkpoint:
        checkpoint.unlink()
    print(
        f"Wrote {len(payload['entries'])} Gemini semantic entries "
        f"({payload['embedding_model']}, {payload['embedding_dimensions']}d; {storage_description}) to {out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
