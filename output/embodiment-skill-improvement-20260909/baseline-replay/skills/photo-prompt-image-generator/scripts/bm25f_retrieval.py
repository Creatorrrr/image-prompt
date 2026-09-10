#!/usr/bin/env python3
"""Deterministic, field-aware lexical retrieval for photo prompt indexes.

The module deliberately owns no prompt-domain meanings.  Callers provide
authored fields and a versioned policy; this file only normalizes text,
materializes a derived BM25F index, ranks documents, and fuses private ranks.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from functools import lru_cache
from typing import Any, Iterable, Mapping, Optional, Sequence


BM25F_TOKENIZER_RECIPE_VERSION = "photo-bm25f-tokenizer/v3"
BM25F_INDEX_RECIPE_VERSION = "photo-bm25f-index/v1"

_SEGMENT_RE = re.compile(
    r"[a-z0-9]+(?:[_+.-][a-z0-9]+)*|[\uac00-\ud7a3]+|"
    r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]+",
    flags=re.IGNORECASE,
)
_HANGUL_RE = re.compile(r"^[\uac00-\ud7a3]+$")
_JAPANESE_OR_HAN_RE = re.compile(
    r"^[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]+$"
)

# Longest-first removal keeps a full eojeol and emits a conservative stem.
# It handles common particles and request-form endings without treating an
# arbitrary substring inside another Korean noun as an independent term.
_KOREAN_SUFFIXES = tuple(
    sorted(
        {
            "으로부터",
            "에게서",
            "에서부터",
            "으로써",
            "으로서",
            "이라고",
            "해져가는",
            "되어가는",
            "해가는",
            "해지는",
            "해진",
            "하는",
            "하다",
            "되는",
            "되다",
            "된",
            "라는",
            "처럼",
            "보다",
            "까지",
            "부터",
            "에게",
            "한테",
            "에서",
            "으로",
            "하고",
            "이며",
            "이고",
            "하게",
            "스러운",
            "스럽게",
            "함을",
            "라고",
            "이라",
            "와",
            "과",
            "을",
            "를",
            "은",
            "는",
            "이",
            "가",
            "의",
            "에",
            "도",
            "만",
            "로",
            "한",
            "함",
            "감",
        },
        key=lambda value: (-len(value), value),
    )
)


def normalize_bm25f_text(value: Any) -> str:
    """Return the canonical lexical representation used by every lane."""

    return " ".join(
        unicodedata.normalize("NFKC", str(value or "")).casefold().split()
    )


@lru_cache(maxsize=16)
def _normalized_lexicon_cached(terms: tuple[str, ...]) -> tuple[str, ...]:
    normalized = {
        normalize_bm25f_text(term)
        for term in terms
        if normalize_bm25f_text(term)
    }
    # Mixed-script authored aliases such as Han+ASCII+Kana are split by the
    # tokenizer before matching. Retain the full alias and also expose only
    # its Japanese/Han components to the longest-first segmenter. These are
    # derived from caller-owned text; this module still owns no domain terms.
    expanded = set(normalized)
    for term in normalized:
        expanded.update(
            match.group(0)
            for match in _SEGMENT_RE.finditer(term)
            if _JAPANESE_OR_HAN_RE.fullmatch(match.group(0))
        )
    return tuple(sorted(expanded, key=lambda value: (-len(value), value)))


def _normalized_lexicon(terms: Iterable[Any]) -> tuple[str, ...]:
    return _normalized_lexicon_cached(tuple(str(term) for term in terms))


def _korean_stem(token: str) -> Optional[str]:
    for suffix in _KOREAN_SUFFIXES:
        if not token.endswith(suffix):
            continue
        stem = token[: -len(suffix)]
        if len(stem) >= 2:
            return stem
    return None


def _lexicon_segments(token: str, lexicon: Sequence[str]) -> list[str]:
    """Greedily segment Japanese/Han compounds with a caller-owned lexicon."""

    if not token or not lexicon:
        return []
    results: list[str] = []
    cursor = 0
    while cursor < len(token):
        match = next(
            (
                term
                for term in lexicon
                if " " not in term and token.startswith(term, cursor)
            ),
            None,
        )
        if match is None:
            cursor += 1
            continue
        results.append(match)
        cursor += len(match)
    return results


def tokenize_bm25f_text(
    value: Any,
    *,
    lexicon: Sequence[str] = (),
) -> list[str]:
    """Tokenize without raw CJK substring activation.

    Korean eojeols remain whole and may emit one conservative suffix-stripped
    stem.  Japanese/Han compounds may additionally be segmented only by the
    supplied authored lexicon.  The behavior is deterministic and versioned.
    """

    normalized = normalize_bm25f_text(value)
    tokens: list[str] = []
    for match in _SEGMENT_RE.finditer(normalized):
        token = match.group(0)
        tokens.append(token)
        if _HANGUL_RE.fullmatch(token):
            stem = _korean_stem(token)
            if stem and stem != token:
                tokens.append(stem)
                plural_stem = stem[:-1] if stem.endswith("들") else ""
                if len(plural_stem) >= 2:
                    tokens.append(plural_stem)
            elif token.endswith("들") and len(token[:-1]) >= 2:
                tokens.append(token[:-1])
        elif _JAPANESE_OR_HAN_RE.fullmatch(token):
            normalized_lexicon = _normalized_lexicon(lexicon)
            tokens.extend(_lexicon_segments(token, normalized_lexicon))
    return tokens


def _as_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def _policy_fields(policy: Mapping[str, Any]) -> dict[str, dict[str, float]]:
    raw_fields = policy.get("fields")
    if not isinstance(raw_fields, Mapping) or not raw_fields:
        raise ValueError("BM25F policy requires a non-empty fields mapping")
    fields: dict[str, dict[str, float]] = {}
    for name, raw_config in raw_fields.items():
        config = raw_config if isinstance(raw_config, Mapping) else {}
        weight = float(config.get("weight", 1.0))
        b_value = float(config.get("b", 0.75))
        if weight < 0:
            raise ValueError(f"BM25F field {name!r} weight must be non-negative")
        if not 0 <= b_value <= 1:
            raise ValueError(f"BM25F field {name!r} b must be between 0 and 1")
        fields[str(name)] = {"weight": weight, "b": b_value}
    return fields


def canonical_bm25f_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return a JSON-serializable canonical policy."""

    k1 = float(policy.get("k1", 1.2))
    if k1 <= 0:
        raise ValueError("BM25F k1 must be greater than zero")
    query_fields = policy.get("query_fields")
    canonical_query_fields = {
        str(name): float(weight)
        for name, weight in (
            query_fields.items() if isinstance(query_fields, Mapping) else []
        )
        if float(weight) >= 0
    }
    return {
        "k1": k1,
        "fields": _policy_fields(policy),
        "query_fields": canonical_query_fields,
        "rrf_k": max(1, int(policy.get("rrf_k", 60))),
        "candidate_limit": max(1, int(policy.get("candidate_limit", 8))),
    }


def build_bm25f_index(
    documents: Mapping[str, Mapping[str, Any]],
    *,
    policy: Mapping[str, Any],
    lexicon: Sequence[str] = (),
) -> dict[str, Any]:
    """Materialize a deterministic BM25F corpus from fielded documents."""

    canonical_policy = canonical_bm25f_policy(policy)
    field_configs = canonical_policy["fields"]
    normalized_lexicon = list(_normalized_lexicon(lexicon))
    indexed_documents: dict[str, Any] = {}
    field_length_totals = {field: 0 for field in field_configs}
    document_frequencies: Counter[str] = Counter()

    for document_id in sorted(str(key) for key in documents):
        source = documents[document_id]
        indexed_fields: dict[str, Any] = {}
        document_terms: set[str] = set()
        for field in field_configs:
            values = _as_values(source.get(field))
            tokens: list[str] = []
            for value in values:
                tokens.extend(tokenize_bm25f_text(value, lexicon=normalized_lexicon))
            frequencies = Counter(tokens)
            length = len(tokens)
            field_length_totals[field] += length
            document_terms.update(frequencies)
            indexed_fields[field] = {
                "length": length,
                "term_frequencies": dict(sorted(frequencies.items())),
            }
        document_frequencies.update(document_terms)
        indexed_documents[document_id] = {"fields": indexed_fields}

    document_count = len(indexed_documents)
    average_field_lengths = {
        field: (
            field_length_totals[field] / document_count if document_count else 0.0
        )
        for field in field_configs
    }
    return {
        "recipe_version": BM25F_INDEX_RECIPE_VERSION,
        "tokenizer_recipe": BM25F_TOKENIZER_RECIPE_VERSION,
        "policy": canonical_policy,
        "lexicon": normalized_lexicon,
        "document_count": document_count,
        "average_field_lengths": average_field_lengths,
        "document_frequencies": dict(sorted(document_frequencies.items())),
        "documents": indexed_documents,
    }


def validate_bm25f_index(
    payload: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
    *,
    policy: Mapping[str, Any],
    lexicon: Sequence[str] = (),
) -> None:
    """Reject any stale or independently edited derived BM25F payload."""

    expected = build_bm25f_index(documents, policy=policy, lexicon=lexicon)
    if payload != expected:
        raise ValueError("BM25F index is stale; regenerate it from the authored source")


def _query_term_weights(
    query_fields: Mapping[str, Any],
    *,
    policy: Mapping[str, Any],
    lexicon: Sequence[str],
) -> Counter[str]:
    weights: Counter[str] = Counter()
    configured = policy.get("query_fields")
    query_weights = configured if isinstance(configured, Mapping) else {}
    for field, raw_value in query_fields.items():
        field_weight = float(query_weights.get(field, 1.0))
        if field_weight <= 0:
            continue
        for value in _as_values(raw_value):
            for token in tokenize_bm25f_text(value, lexicon=lexicon):
                weights[token] += field_weight
    return weights


def rank_bm25f(
    payload: Mapping[str, Any],
    query_fields: Mapping[str, Any],
    *,
    limit: Optional[int] = None,
    allowed_ids: Optional[Iterable[str]] = None,
    blocked_ids: Iterable[str] = (),
) -> list[dict[str, Any]]:
    """Return private BM25F ranks with deterministic document-ID tie breaks."""

    if payload.get("recipe_version") != BM25F_INDEX_RECIPE_VERSION:
        raise ValueError("unsupported BM25F index recipe_version")
    if payload.get("tokenizer_recipe") != BM25F_TOKENIZER_RECIPE_VERSION:
        raise ValueError("unsupported BM25F tokenizer recipe")
    policy = canonical_bm25f_policy(payload.get("policy") or {})
    field_configs = policy["fields"]
    lexicon = [str(value) for value in payload.get("lexicon") or []]
    query_terms = _query_term_weights(
        query_fields,
        policy=policy,
        lexicon=lexicon,
    )
    if not query_terms:
        return []

    allowed = {str(value) for value in allowed_ids} if allowed_ids is not None else None
    blocked = {str(value) for value in blocked_ids}
    document_count = int(payload.get("document_count", 0) or 0)
    average_lengths = payload.get("average_field_lengths") or {}
    document_frequencies = payload.get("document_frequencies") or {}
    documents = payload.get("documents") or {}
    rows: list[dict[str, Any]] = []

    for document_id in sorted(str(key) for key in documents):
        if allowed is not None and document_id not in allowed:
            continue
        if document_id in blocked:
            continue
        document = documents.get(document_id) or {}
        indexed_fields = document.get("fields") or {}
        score = 0.0
        matched_terms: list[str] = []
        for term, query_weight in query_terms.items():
            weighted_tf = 0.0
            for field, config in field_configs.items():
                field_data = indexed_fields.get(field) or {}
                term_frequency = float(
                    (field_data.get("term_frequencies") or {}).get(term, 0)
                )
                if term_frequency <= 0:
                    continue
                field_length = float(field_data.get("length", 0) or 0)
                average_length = float(average_lengths.get(field, 0) or 0)
                length_ratio = field_length / average_length if average_length > 0 else 1.0
                normalization = 1.0 - config["b"] + config["b"] * length_ratio
                weighted_tf += config["weight"] * term_frequency / max(
                    normalization,
                    1e-12,
                )
            if weighted_tf <= 0:
                continue
            frequency = int(document_frequencies.get(term, 0) or 0)
            idf = math.log(
                1.0
                + (document_count - frequency + 0.5) / max(frequency + 0.5, 1e-12)
            )
            score += (
                float(query_weight)
                * idf
                * ((weighted_tf * (policy["k1"] + 1.0)) / (policy["k1"] + weighted_tf))
            )
            matched_terms.append(term)
        if score > 0:
            rows.append(
                {
                    "document_id": document_id,
                    "score": round(score, 12),
                    "matched_terms": sorted(set(matched_terms)),
                }
            )

    rows.sort(key=lambda row: (-float(row["score"]), str(row["document_id"])))
    effective_limit = (
        max(1, int(limit)) if limit is not None else int(policy["candidate_limit"])
    )
    return rows[:effective_limit]


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]],
    *,
    k: int = 60,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Fuse incomparable private ranks without treating raw scores as calibrated."""

    denominator_offset = max(1, int(k))
    scores: Counter[str] = Counter()
    lanes: dict[str, set[int]] = {}
    for lane_index, ranking in enumerate(rankings):
        seen: set[str] = set()
        for rank, raw_id in enumerate(ranking, start=1):
            document_id = str(raw_id)
            if not document_id or document_id in seen:
                continue
            seen.add(document_id)
            scores[document_id] += 1.0 / (denominator_offset + rank)
            lanes.setdefault(document_id, set()).add(lane_index)
    rows = [
        {
            "document_id": document_id,
            "score": round(float(score), 12),
            "lane_count": len(lanes.get(document_id, set())),
        }
        for document_id, score in scores.items()
    ]
    rows.sort(
        key=lambda row: (
            -float(row["score"]),
            -int(row["lane_count"]),
            str(row["document_id"]),
        )
    )
    return rows[: max(1, int(limit))] if limit is not None else rows
