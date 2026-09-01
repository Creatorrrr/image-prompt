#!/usr/bin/env python3
"""Build explicitly synthetic-vector run-local indexes for exact/BM25F tests.

The shared skill requires real Gemini vectors for promotion. This helper never
writes shared assets and marks every synthesized vector in a separate manifest.
It exists only so exact visual-profile routing, BM25F candidate retrieval, pack
composition, and image-call auditing can be exercised while GEMINI_API_KEY is
unavailable. Embedding-similarity claims are forbidden for these outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_semantic_index  # noqa: E402
import prompt_generator  # noqa: E402


def deterministic_vector(key: str, dimensions: int) -> list[float]:
    values: list[float] = []
    counter = 0
    while len(values) < dimensions:
        digest = hashlib.sha256(f"{key}:{counter}".encode("utf-8")).digest()
        values.extend((byte - 127.5) / 127.5 for byte in digest)
        counter += 1
    clipped = values[:dimensions]
    norm = math.sqrt(sum(value * value for value in clipped)) or 1.0
    return [value / norm for value in clipped]


def load_raw_payload(path: Path) -> dict:
    if not path.exists():
        return {}
    return prompt_generator.load_semantic_index_payload(path)


def build_visual_index(
    registry_path: Path,
    cache_path: Path,
    output_path: Path,
    dimensions: int,
) -> tuple[int, list[str]]:
    registry = prompt_generator.load_visual_obligation_registry(registry_path)
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    cached_entries = cache.get("entries") if isinstance(cache, dict) else {}
    if not isinstance(cached_entries, dict):
        cached_entries = {}

    vectors: dict[str, list[float]] = {}
    synthetic: list[str] = []
    for profile in registry.get("profiles") or []:
        profile_id = str(profile.get("id") or "")
        text = prompt_generator.visual_profile_semantic_text(profile)
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        cached = cached_entries.get(profile_id)
        if (
            isinstance(cached, dict)
            and cached.get("text_sha256") == text_hash
            and isinstance(cached.get("vector"), list)
            and len(cached["vector"]) == dimensions
        ):
            vectors[profile_id] = cached["vector"]
            continue
        vectors[profile_id] = deterministic_vector(f"visual:{profile_id}:{text_hash}", dimensions)
        synthetic.append(profile_id)

    payload = prompt_generator.build_visual_profile_index_payload(
        registry,
        vectors=vectors,
        provider=prompt_generator.SEMANTIC_PROVIDER,
        model=prompt_generator.SEMANTIC_MODEL_ID,
        dimensions=dimensions,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    prompt_generator.load_visual_profile_index(output_path, registry)
    return len(payload["entries"]), synthetic


def build_semantic(
    tags_path: Path,
    cache_path: Path,
    output_path: Path,
    dimensions: int,
) -> tuple[int, list[str]]:
    data = prompt_generator.load_json(tags_path)
    cache = load_raw_payload(cache_path)
    cached_entries = cache.get("entries") if isinstance(cache, dict) else {}
    if not isinstance(cached_entries, dict):
        cached_entries = {}

    payload = build_semantic_index.base_payload(
        data,
        prompt_generator.SEMANTIC_PROVIDER,
        prompt_generator.SEMANTIC_MODEL_ID,
        dimensions,
    )
    entries: dict[str, dict] = {}
    synthetic: list[str] = []
    rows = prompt_generator.iter_semantic_entries(data)
    bm25f_payload = prompt_generator.build_semantic_bm25f_payload(data)
    bm25f_documents = bm25f_payload.get("documents") or {}

    for key, kind, entry, slot in rows:
        text = prompt_generator.semantic_text_for_entry(entry, slot, kind=kind)
        cached = cached_entries.get(key)
        if (
            isinstance(cached, dict)
            and cached.get("text") == text
            and isinstance(cached.get("vector"), list)
            and len(cached["vector"]) == dimensions
        ):
            vector = cached["vector"]
        else:
            vector = deterministic_vector(f"semantic:{key}:{text}", dimensions)
            synthetic.append(key)
        entries[key] = {
            "kind": kind,
            "slot": slot,
            "id": entry.get("id"),
            "text": text,
            "vector": vector,
            "bm25f_document": bm25f_documents.get(key) or {},
        }

    payload["bm25f"] = {
        key: value for key, value in bm25f_payload.items() if key != "documents"
    }
    payload["entries"] = entries
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    loaded = prompt_generator.load_semantic_index(output_path, data)
    return len(loaded["entries"]), synthetic


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    assets = SKILL_DIR / "assets"
    registry = assets / "photo_prompt_visual_obligations.json"
    tags = assets / "photo_prompt_tags.json"
    visual_cache = assets / "photo_prompt_visual_profile_index.json"
    semantic_cache = assets / "photo_prompt_semantic_index.json"
    visual_output = output_dir / "photo_prompt_visual_profile_index.json"
    semantic_output = output_dir / "photo_prompt_semantic_index.json"

    visual_count, synthetic_profiles = build_visual_index(
        registry, visual_cache, visual_output, prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS
    )
    semantic_count, synthetic_entries = build_semantic(
        tags, semantic_cache, semantic_output, prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS
    )

    manifest = {
        "schema_version": "photo-run-local-index-manifest/v1",
        "purpose": "exact_and_bm25f_desire_three_arm_test_only",
        "embedding_similarity_claims_allowed": False,
        "shared_assets_modified": False,
        "provider_label_retained_for_schema_compatibility": prompt_generator.SEMANTIC_PROVIDER,
        "model_label_retained_for_schema_compatibility": prompt_generator.SEMANTIC_MODEL_ID,
        "dimensions": prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS,
        "visual_index": {
            "path": str(visual_output),
            "sha256": sha256(visual_output),
            "entry_count": visual_count,
            "synthetic_vector_profile_ids": synthetic_profiles,
        },
        "semantic_index": {
            "path": str(semantic_output),
            "sha256": sha256(semantic_output),
            "entry_count": semantic_count,
            "synthetic_vector_entry_keys": synthetic_entries,
        },
        "limitations": [
            "No synthetic vector may support an embedding or RRF similarity claim.",
            "The shared generated indexes remain stale until rebuilt with real Gemini embeddings at batch size one.",
            "The run-local indexes support exact-profile and BM25F contract testing only.",
        ],
    }
    manifest_path = output_dir / "run_local_index_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
