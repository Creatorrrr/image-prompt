#!/usr/bin/env python3
"""Build the Gemini semantic index for the photo prompt dictionary."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from core_slot_index_storage import atomic_write, canonical_bytes, decode
from photo_runtime_sources import file_lock

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    SEMANTIC_BM25F_POLICY_VERSION,
    SEMANTIC_PROVIDER,
    SEMANTIC_TEXT_RECIPE_VERSION,
    dictionary_hash,
    build_semantic_bm25f_payload,
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
    """Check vector-space compatibility before exact text-level cache reuse.

    A semantic text recipe version can change because new document kinds or
    fields were added while older entries retain byte-identical input text.
    ``build_resumable_index_payload`` compares every cached entry's exact text
    before reuse, so provider/model/dimensions are the only global vector-space
    constraints required here.
    """

    keys = ["provider", "embedding_model", "embedding_dimensions"]
    if require_dictionary_hash:
        keys.append("dictionary_hash")
    return all(payload.get(key) == expected.get(key) for key in keys)


def load_payload(path: Path) -> dict | None:
    """Load a completed sharded index for vector reuse."""
    return load_semantic_index_payload(path) if path.exists() else None


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
    """Read the private resumable payload separately from completed indexes."""
    payload = dict(expected)
    entries = load_reusable_entries(cache_indexes, expected)
    if path.exists():
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(checkpoint, dict) or not isinstance(checkpoint.get("entries"), dict):
            raise ValueError("invalid semantic build checkpoint")
        if metadata_matches(checkpoint, expected):
            entries.update({key: row for key, row in checkpoint["entries"].items() if isinstance(row, dict)})
    payload["entries"] = entries
    return payload


def write_payload(path: Path, payload: dict, *, compact: bool = False,
                  record_embedding_attempts: bool = False) -> None:
    """Atomically persist JSON, optionally without generated-artifact whitespace."""
    if record_embedding_attempts:
        serialized = json.dumps(payload, ensure_ascii=False,
            separators=(",", ":")) if compact else json.dumps(payload, ensure_ascii=False, indent=2)
        atomic_write(path, serialized.encode("utf-8"))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    if compact:
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    else:
        serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(path)


def recorded_file_exists(path: Path) -> bool:
    """An existing broken link or special file is damaged evidence, never absence."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    if not stat.S_ISREG(mode):
        raise RuntimeError("Recorded embedding evidence must be a regular file; no resend or overwrite")
    return True


def sync_attempt_directory(directory: Path) -> None:
    """Persist mkdir entries, including any newly created checkpoint ancestors."""
    directory = directory.resolve()
    for parent in (directory, *directory.parents):
        descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def checkpoint_build_lock(checkpoint: Path, name: str = "checkpoint.lock"):
    directory = checkpoint.with_name(checkpoint.name + ".embedding-attempts")
    if directory.is_symlink():
        raise RuntimeError("Embedding attempt directory must not be a symlink; no resend or overwrite")
    lock_path = directory / name
    recorded_file_exists(lock_path)
    return file_lock(lock_path)


def require_unrecorded_namespace(path: Path) -> None:
    """An existing recorded job must never resume silently through the legacy sender."""
    directory = path.with_name(path.name + ".embedding-attempts")
    try:
        directory.lstat()
    except FileNotFoundError:
        return
    raise ValueError("Recorded build evidence exists; select --record-embedding-attempts "
                     "with --batch-size=1 --retry-attempts=0, no unrecorded resume")


def request_record_paths(checkpoint: Path, text: str, provider: str, model: str, dimensions: int):
    """One permanent attempt per exact input/vector space beside this checkpoint."""
    identity = {"provider": provider, "model": model, "dimensions": dimensions,
                "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    request_id = hashlib.sha256(canonical_bytes(identity)).hexdigest()
    directory = checkpoint.with_name(checkpoint.name + ".embedding-attempts")
    return identity, directory / (request_id + ".json"), directory / (request_id + ".raw.json")


def recorded_response_vector(path: Path, identity: dict) -> list[float]:
    receipt = decode(path.read_bytes())
    if (not isinstance(receipt, dict) or receipt.get("schema") != "photo-semantic-raw-response/v1"
            or receipt.get("request") != identity):
        raise ValueError("Raw response request binding differs")
    raw = base64.b64decode(receipt["body_base64"], validate=True)
    if hashlib.sha256(raw).hexdigest() != receipt.get("body_sha256"):
        raise ValueError("Raw response body checksum differs")
    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 200:
        raise ValueError("Raw response is not HTTP200")
    body = decode(raw)
    if not isinstance(body, dict):
        raise ValueError("Raw response body must be an object")
    embeddings = body.get("embeddings", [body.get("embedding")])
    if not isinstance(embeddings, list) or len(embeddings) != 1 or not isinstance(embeddings[0], dict):
        raise ValueError("Raw response must contain one embedding")
    values = embeddings[0].get("values")
    if (not isinstance(values, list) or len(values) != identity["dimensions"]
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in values)):
        raise ValueError("Raw embedding must contain finite numeric values of the requested dimensions")
    return [round(float(v), 6) for v in values]


def embed_recorded_once(text: str, *, checkpoint: Path, provider: str, model: str,
                        dimensions: int, allow_new: bool = True) -> list[float]:
    """Recover validated raw responses; never resend an existing attempt."""
    identity, record_path, raw_path = request_record_paths(checkpoint, text, provider, model, dimensions)
    if record_path.parent.is_symlink():
        raise RuntimeError("Embedding attempt directory must not be a symlink; no resend or overwrite")
    lock_path = record_path.with_suffix(".lock")
    recorded_file_exists(lock_path)
    with file_lock(lock_path):
        if recorded_file_exists(record_path):
            previous = decode(record_path.read_bytes())
            if (not isinstance(previous, dict)
                    or previous.get("schema") != "photo-semantic-embedding-attempt/v1"
                    or previous.get("request") != identity):
                raise RuntimeError("Embedding attempt record differs; user review required")
            if previous.get("state") not in ("started", "response_saved", "succeeded"):
                raise RuntimeError("Embedding attempt is stopped or corrupt; user review required, no resend")
            if not recorded_file_exists(raw_path):
                atomic_write(record_path, canonical_bytes({**previous, "state": "unknown"}))
                raise RuntimeError("Recorded embedding has no raw response; user review required, no resend")
            try:
                vector = recorded_response_vector(raw_path, identity)
            except (ValueError, TypeError, KeyError):
                raise RuntimeError("Recorded response failed validation; user review required, no resend") from None
            atomic_write(record_path, canonical_bytes({**previous, "state": "succeeded"}))
            return vector
        if recorded_file_exists(raw_path):
            raise RuntimeError("Orphan raw response requires user review; no resend")
        if not allow_new:
            raise RuntimeError("Existing attempt evidence disappeared; user review required, no resend")
        attempt = {"schema": "photo-semantic-embedding-attempt/v1", "request": identity,
                   "state": "started", "started_at": datetime.now(timezone.utc).isoformat()}
        # Both mkdir ancestry and the attempt must be durable before SDK/key access.
        sync_attempt_directory(record_path.parent)
        atomic_write(record_path, canonical_bytes(attempt))
        def save_raw(status: int, body: bytes):
            if recorded_file_exists(raw_path):
                raise RuntimeError("Raw response already exists; no overwrite")
            atomic_write(raw_path, canonical_bytes({"schema": "photo-semantic-raw-response/v1",
                "request": identity, "http_status": status,
                "body_sha256": hashlib.sha256(body).hexdigest(),
                "body_base64": base64.b64encode(body).decode("ascii")}))
        try:
            embed_texts_with_gemini([text], model=model, dimensions=dimensions,
                retry_attempts=0, retry_initial_delay=0, raw_response_callback=save_raw)
            vector = recorded_response_vector(raw_path, identity)
            atomic_write(record_path, canonical_bytes({**attempt, "state": "succeeded"}))
            return vector
        except BaseException as exc:
            state = "unknown"
            try:
                if recorded_file_exists(raw_path):
                    recorded_response_vector(raw_path, identity)
                    state = "response_saved"
            except (ValueError, TypeError, KeyError, RuntimeError):
                state = "failed"
            try:
                atomic_write(record_path, canonical_bytes({**attempt, "state": state}))
            except OSError:
                pass  # The initial durable started record still blocks a resend.
            # Preserve only this known configuration diagnostic; never echo SDK errors.
            missing_key = "GEMINI_API_KEY or GOOGLE_API_KEY is required for Gemini semantic embeddings."
            diagnostic = missing_key + " " if isinstance(exc, RuntimeError) and exc.args == (missing_key,) else ""
            raise RuntimeError(diagnostic + "Embedding attempt stopped; inspect local raw/state records, no automatic retry") from None


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
    record_embedding_attempts: bool = False,
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
    record_options = {"record_embedding_attempts": True} if record_embedding_attempts else {}

    # The dictionary can stay unchanged while its tokenizer, vector space, or
    # shard count changes. Bind the directory to the complete derived payload
    # so a rebuild cannot overwrite shards referenced by an older manifest.
    generation = hashlib.sha256(json.dumps(
        {"payload": payload, "shard_count": count}, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")).hexdigest()
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
        write_payload(shard_path, shard_payload, compact=True, **record_options)
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
    write_payload(path, manifest, **record_options)
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
    *,
    record_embedding_attempts: bool = False,
) -> dict:
    if record_embedding_attempts:
        if max(1, int(batch_size)) != 1 or retry_attempts != 0:
            raise ValueError("Recorded semantic builds require batch_size=1 and retry_attempts=0")
        with checkpoint_build_lock(checkpoint):
            return _build_resumable_index_payload(data, output, checkpoint, provider,
                model, dimensions, batch_size, request_interval, retry_attempts,
                retry_initial_delay, cache_indexes, progress_callback, record_embedding_attempts=True)
    require_unrecorded_namespace(checkpoint)
    require_unrecorded_namespace(output)
    return _build_resumable_index_payload(data, output, checkpoint, provider,
            model, dimensions, batch_size, request_interval, retry_attempts,
            retry_initial_delay, cache_indexes, progress_callback)


def _build_resumable_index_payload(
    data, output: Path, checkpoint: Path, provider: str, model: str, dimensions: int,
    batch_size: int, request_interval: float, retry_attempts: int, retry_initial_delay: float,
    cache_indexes: Sequence[Path], progress_callback,
    *, record_embedding_attempts: bool = False,
) -> dict:
    if provider != SEMANTIC_PROVIDER:
        raise ValueError(f"Unsupported semantic provider '{provider}'. Only '{SEMANTIC_PROVIDER}' is supported.")
    dims = semantic_dimensions_value(dimensions)
    batch = max(1, int(batch_size))
    record_options = {"record_embedding_attempts": True} if record_embedding_attempts else {}
    if record_embedding_attempts and (batch != 1 or retry_attempts != 0):
        raise ValueError("Recorded semantic builds require batch_size=1 and retry_attempts=0")
    rows = iter_semantic_entries(data)
    expected = base_payload(data, provider, model, dims)
    payload = load_checkpoint(checkpoint, expected, cache_indexes=cache_indexes)
    entries = payload.setdefault("entries", {})

    # Inspect every existing current-input attempt before sending any new row.
    # A stopped later row must not let an earlier new row spend on a rerun.
    recovered = False
    for key, kind, entry, slot in rows if record_embedding_attempts else ():
        text = semantic_text_for_entry(entry, slot, kind=kind)
        _, record_path, raw_path = request_record_paths(checkpoint, text, provider, model, dims)
        if recorded_file_exists(record_path) or recorded_file_exists(raw_path):
            vector = embed_recorded_once(text, checkpoint=checkpoint, provider=provider,
                model=model, dimensions=dims, allow_new=False)
            cached = entries.get(key)
            if cached and cached.get("text") == text and cached.get("vector") != vector:
                raise ValueError("Checkpoint vector differs from its recorded raw response")
            if not cached or cached.get("text") != text:
                entries[key] = {"kind": kind, "slot": slot, "id": entry.get("id"),
                                "text": text, "vector": vector}
                recovered = True
    if recovered:
        write_payload(checkpoint, payload, **record_options)

    pending = []
    for key, kind, entry, slot in rows:
        text = semantic_text_for_entry(entry, slot, kind=kind)
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
        if record_embedding_attempts:
            vectors = [embed_recorded_once(chunk[0][4], checkpoint=checkpoint,
                provider=provider, model=model, dimensions=dims)]
        else:
            vectors = embed_texts_with_gemini([row[4] for row in chunk], model=model,
                dimensions=dims, retry_attempts=retry_attempts, retry_initial_delay=retry_initial_delay)
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
        write_payload(checkpoint, payload, **record_options)
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
    bm25f_payload = build_semantic_bm25f_payload(data)
    bm25f_documents = bm25f_payload.get("documents") or {}
    for key in ordered_entries:
        ordered_entries[key]["bm25f_document"] = bm25f_documents.get(key) or {}
    payload["bm25f"] = {
        key: value for key, value in bm25f_payload.items() if key != "documents"
    }
    payload["entries"] = ordered_entries
    return payload


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Gemini embedding semantic index JSON.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    parser.add_argument("--output", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_semantic_index.json")
    parser.add_argument("--provider", choices=[SEMANTIC_PROVIDER], default=SEMANTIC_PROVIDER)
    parser.add_argument("--model", default=SEMANTIC_MODEL_ID)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_SEMANTIC_DIMENSIONS)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--request-interval", type=float, default=0.8, help="Seconds to sleep between Gemini requests.")
    parser.add_argument("--retry-attempts", type=int, default=4, help="Retry count for Gemini 429 RESOURCE_EXHAUSTED responses.")
    parser.add_argument("--record-embedding-attempts", action="store_true",
        help="Opt in to durable raw recovery and no resend; requires --batch-size=1 --retry-attempts=0.")
    parser.add_argument("--retry-initial-delay", type=float, default=15.0, help="Initial retry sleep in seconds for Gemini 429 responses.")
    parser.add_argument("--checkpoint", default=None, help="Partial index path used for resumable builds. Defaults to OUTPUT.partial.")
    parser.add_argument("--keep-checkpoint", action="store_true", help="Keep the partial checkpoint after a successful final write.")
    parser.add_argument("--shard-count", type=int, default=16, help="Stable hash-shard count for the final index (default: 16).")
    parser.add_argument(
        "--keep-stale-generations",
        action="store_true",
        help="Keep older shard generations after the new manifest is written.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Do not reuse compatible vectors from an existing output index.")
    parser.add_argument("--progress", action="store_true", help="Print embedding progress without vector values.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned index metadata without calling the Gemini API or writing output.")
    parser.add_argument("--no-runtime-publication", action="store_true")
    return parser


def main() -> int:
    load_project_env()
    args = build_argument_parser().parse_args()

    data = load_json(args.tags)
    entry_count = len(iter_semantic_entries(data))

    if args.dry_run:
        print(
            json.dumps(
                {
                    "provider": args.provider,
                    "semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
                    "bm25f_policy_version": SEMANTIC_BM25F_POLICY_VERSION,
                    "embedding_model": args.model,
                    "embedding_dimensions": args.dimensions,
                    "entries": entry_count,
                    "storage_format": SEMANTIC_INDEX_SHARDED_FORMAT,
                    "shard_count": args.shard_count,
                    "output": str(args.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    return build_and_write_index(args, data)


def build_and_write_index(args, data) -> int:
    """Opt-in builds retain output/checkpoint locks through final writes and cleanup."""
    out = Path(args.output)
    checkpoint = checkpoint_path_for(out, args.checkpoint)
    if getattr(args, "record_embedding_attempts", False):
        if max(1, int(args.batch_size)) != 1 or args.retry_attempts != 0:
            raise ValueError("Recorded semantic builds require --batch-size=1 --retry-attempts=0")
        with checkpoint_build_lock(out, "output.lock"), checkpoint_build_lock(checkpoint):
            return _build_and_write_index(args, data)
    require_unrecorded_namespace(out)
    require_unrecorded_namespace(checkpoint)
    return _build_and_write_index(args, data)


def _build_and_write_index(args, data) -> int:
    recorded = getattr(args, "record_embedding_attempts", False)
    record_options = {"record_embedding_attempts": True} if recorded else {}
    try:
        def progress(done: int, total: int) -> None:
            if done == total or done % 50 == 0:
                print(f"Embedded {done}/{total} entries", flush=True)

        out = Path(args.output)
        checkpoint = checkpoint_path_for(out, args.checkpoint)
        cache_indexes = [] if args.no_cache else [out]
        build = _build_resumable_index_payload if recorded else build_resumable_index_payload
        payload = build(
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
            **record_options,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    payload["created_at"] = datetime.now(timezone.utc).isoformat()

    out = Path(args.output)
    if out == Path(args.tags).with_name("photo_prompt_semantic_index.json"):
        from photo_runtime_sources import source_update
        with source_update(Path(args.tags).parent.parent):
            write_sharded_payload(out, payload, shard_count=args.shard_count,
                                  keep_stale_generations=True, **record_options)
        if not args.no_runtime_publication:
            from photo_runtime_sources import publish_if_ready
            publish_if_ready(Path(args.tags).parent.parent)
    else:
        write_sharded_payload(out, payload, shard_count=args.shard_count,
                              keep_stale_generations=args.keep_stale_generations, **record_options)
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
