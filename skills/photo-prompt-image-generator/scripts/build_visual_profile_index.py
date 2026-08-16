#!/usr/bin/env python3
"""Build or verify the registry-bound visual-profile hybrid index."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Sequence

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    SEMANTIC_PROVIDER,
    VISUAL_OBLIGATION_REGISTRY_FILENAME,
    VISUAL_PROFILE_INDEX_FILENAME,
    build_visual_profile_index_payload,
    embed_texts_with_gemini,
    load_json,
    load_visual_obligation_registry,
    load_visual_profile_index,
    visual_profile_semantic_text,
)


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]
DEFAULT_REGISTRY = SKILL_DIR / "assets" / VISUAL_OBLIGATION_REGISTRY_FILENAME
DEFAULT_OUTPUT = SKILL_DIR / "assets" / VISUAL_PROFILE_INDEX_FILENAME


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


def reusable_vectors(
    paths: Sequence[Path],
    registry: dict,
    *,
    provider: str,
    model: str,
    dimensions: int,
) -> dict[str, list[float]]:
    expected_texts = {
        str(profile["id"]): visual_profile_semantic_text(profile)
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    }
    vectors: dict[str, list[float]] = {}
    for path in paths:
        if not path.exists():
            continue
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if (
            payload.get("provider") != provider
            or payload.get("embedding_model") != model
            or int(payload.get("embedding_dimensions", -1)) != int(dimensions)
        ):
            continue
        for profile_id, expected_text in expected_texts.items():
            entry = (payload.get("entries") or {}).get(profile_id)
            if not isinstance(entry, dict) or entry.get("text") != expected_text:
                continue
            vector = entry.get("vector")
            if isinstance(vector, list) and len(vector) == int(dimensions):
                vectors[profile_id] = [float(value) for value in vector]
    return vectors


def write_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the exact+embedding visual-profile index from one registry."
    )
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--cache-index", action="append", default=[])
    parser.add_argument("--provider", default=SEMANTIC_PROVIDER)
    parser.add_argument("--model", default=SEMANTIC_MODEL_ID)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_SEMANTIC_DIMENSIONS)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--request-interval", type=float, default=0.0)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    output_path = Path(args.output)
    registry = load_visual_obligation_registry(registry_path)
    if args.check:
        payload = load_visual_profile_index(
            output_path,
            registry,
            provider=args.provider,
            model=args.model,
            dimensions=args.dimensions,
        )
        print(
            "visual profile index ok: "
            f"{len(payload.get('entries') or {})} profiles, "
            f"{len(payload.get('exact_lookup') or [])} exact terms"
        )
        return 0

    if args.provider != SEMANTIC_PROVIDER:
        raise ValueError(
            f"Unsupported visual-profile provider {args.provider!r}; "
            f"expected {SEMANTIC_PROVIDER!r}"
        )
    batch_size = max(1, int(args.batch_size))
    cache_paths = [Path(value) for value in args.cache_index]
    vectors = reusable_vectors(
        [*cache_paths, output_path],
        registry,
        provider=args.provider,
        model=args.model,
        dimensions=args.dimensions,
    )
    profile_rows = [
        profile
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    ]
    pending = [
        profile for profile in profile_rows if str(profile["id"]) not in vectors
    ]
    if pending:
        load_project_env()
    for start in range(0, len(pending), batch_size):
        chunk = pending[start : start + batch_size]
        texts = [visual_profile_semantic_text(profile) for profile in chunk]
        embedded = embed_texts_with_gemini(
            texts,
            model=args.model,
            dimensions=args.dimensions,
        )
        if len(embedded) != len(chunk):
            raise RuntimeError(
                f"Gemini returned {len(embedded)} embeddings for {len(chunk)} visual profiles"
            )
        for profile, vector in zip(chunk, embedded):
            vectors[str(profile["id"])] = vector
        print(f"embedded {min(start + len(chunk), len(pending))}/{len(pending)} pending profiles")
        if args.request_interval > 0 and start + len(chunk) < len(pending):
            time.sleep(args.request_interval)

    payload = build_visual_profile_index_payload(
        registry,
        vectors=vectors,
        provider=args.provider,
        model=args.model,
        dimensions=args.dimensions,
    )
    write_payload(output_path, payload)
    load_visual_profile_index(
        output_path,
        registry,
        provider=args.provider,
        model=args.model,
        dimensions=args.dimensions,
    )
    print(
        f"wrote {output_path}: {len(payload['entries'])} profiles, "
        f"{len(payload['exact_lookup'])} exact terms"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
