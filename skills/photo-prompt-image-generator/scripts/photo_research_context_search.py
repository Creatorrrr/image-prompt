#!/usr/bin/env python3
"""Search the authored fashion-interest research context, not image candidates.

This read-only lookup builds a small BM25F index in memory from current source
files. Results are context evidence only and carry no candidate or image-use
authority. It does not change the installed H-F2 generation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from bm25f_retrieval import build_bm25f_index, rank_bm25f, tokenize_bm25f_text

ASSETS = Path(__file__).resolve().parents[1] / "assets"
INTEREST = "photo_fashion_interest_context_20261108.json"
POSE_CONTEXT = "photo_fashion_pose_photo_research_context_views_20261108.json"
POLICY = {
    "k1": 1.2,
    "fields": {
        "term": {"weight": 4.0, "b": 0.75},
        "context": {"weight": 1.5, "b": 0.75},
        "boundary": {"weight": 0.5, "b": 0.75},
        "tags": {"weight": 0.5, "b": 0.75},
    },
}
FETISH_CUES = frozenset({
    "fetish", "fetishism", "fetishist", "fetishistic", "fetishwear", "fetish-inspired",
    "페티시", "페티시즘", "페티시스트", "페티시적인", "페티시웨어",
    "podophilia", "trichophilia",
})
KOREAN_PARTICLES = ("에서", "으로", "이란", "라는", "란", "의", "에", "을", "를", "은", "는", "이", "가", "와", "과")


def korean_alias_stems(query, records):
    """Recognize authored Korean aliases with a bounded particle, including 발/손."""
    words = {word for row in records.values() for alias in row["search_aliases"]
             for word in alias.split() if re.fullmatch(r"[가-힣]+", word)}
    endings = "|".join(KOREAN_PARTICLES)
    return sorted(word for word in words if re.search(
        rf"(?<![가-힣]){re.escape(word)}(?:{endings})(?![가-힣])", query))


def load_records(assets=ASSETS):
    """Load only explicitly scoped, research-only rows with their source hashes."""
    records = {}
    for filename in (INTEREST, POSE_CONTEXT):
        raw = (Path(assets) / filename).read_bytes()
        payload = json.loads(raw)
        expected = ("photo-fashion-interest-research-context/v1" if filename == INTEREST
                    else "fashion-pose-photo-research-context-views/v1")
        if payload.get("schema") != expected:
            raise ValueError(f"unexpected research context schema: {filename}")
        for row in payload["views"]:
            # This release exposes the reviewed interest inventory and just the
            # explicitly reviewed couture row, not all unrelated pose research.
            if filename == POSE_CONTEXT and row.get("term_id") != "FVP-10-075":
                continue
            if row.get("context_only") is not True or row.get("native_approval") is not False:
                raise ValueError("research context must not grant native approval")
            rid = row["id"]
            if rid in records:
                raise ValueError("duplicate research context id")
            tags = row.get("tags", [])
            if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
                raise ValueError("invalid context tags")
            aliases = row.get("search_aliases", [])
            if not isinstance(aliases, list) or any(not isinstance(a, str) or not a for a in aliases):
                raise ValueError("invalid context search aliases")
            records[rid] = {
                "id": rid,
                "term": row.get("term", row.get("source_term_label", "")),
                "context_ko": row["context_ko"],
                "boundary": row.get("boundary_ko", row.get("boundary", "")),
                "tags": tags,
                "search_aliases": aliases,
                "source_file": filename,
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "context_only": True,
                "native_approval": False,
            }
    return records


def search(query, *, tag=None, limit=10, assets=ASSETS):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be nonempty")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")
    if tag not in (None, "fetish"):
        raise ValueError("unknown research context tag")
    records = load_records(assets)
    stems = korean_alias_stems(query, records)
    docs = {
        rid: {
            "term": [row["term"], *row["search_aliases"]], "context": row["context_ko"],
            "boundary": row["boundary"],
            # A bilingual rendering indexes the same authored tag, not a new
            # claim that the visual contents of another record are a fetish.
            "tags": ["fetish 페티시" for t in row["tags"] if t == "fetish"],
        } for rid, row in records.items()
    }
    index = build_bm25f_index(docs, policy=POLICY)
    explicit_fetish_lookup = tag == "fetish" or bool((set(tokenize_bm25f_text(query)) | set(stems)) & FETISH_CUES)
    # General object queries must not silently assign sexual context to the
    # object. An explicit research tag filter is also an intentional lookup.
    allowed = [rid for rid, row in records.items()
               if (not tag or tag in row["tags"])
               and (explicit_fetish_lookup or "fetish" not in row["tags"])]
    hits = rank_bm25f(index, {"query": query, "authored_alias_stems": stems}, allowed_ids=allowed, limit=limit)
    return {
        "schema": "photo-research-context-search/v1", "query": query,
        "tag_filter": tag, "explicit_fetish_lookup": explicit_fetish_lookup,
        "index": "in_memory_bm25f", "source_count": len(records),
        "scope": "research_context_only", "native_approval": False,
        "results": [{**records[h["document_id"]], "score": h["score"],
                     "matched_terms": h["matched_terms"]} for h in hits],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("query")
    parser.add_argument("--tag", choices=["fetish"])
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(search(args.query, tag=args.tag, limit=args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
