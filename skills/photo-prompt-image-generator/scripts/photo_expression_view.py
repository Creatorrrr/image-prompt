#!/usr/bin/env python3
"""Exact, source-bound expression lookup over one sealed native V4 module.

This view is deliberately separate from material retrieval. It does not rank,
embed, infer meaning, authorize a source, or establish a visual fact.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any


SCHEMA = "photo-expression-view/v1"
MODULE_RELATIVE_PATH = "assets/photo_candidate_reactorprompt_pose_composition_20261026.json"
NATIVE_MODULE_SCHEMA = "photo-candidate-module/v4"
MEANING_SCHEMA = "photo-canonical-meaning/v1"
NATIVE_TREE_SCHEMA = "photo-native-literal-tree/v1"
LOOKUP_FIELDS = ("aliases", "keywords", "labels")
PRIMARY_MEANING_FIELDS = {
    "en": "/content/en",
    "ko": "/content/ko",
    "definition": "/content/definition",
}


class ExpressionViewError(ValueError):
    """A fail-closed input, run, release, or native V4 contract error."""

    def __init__(self, code: str, **details: Any):
        self.code = code
        self.details = details
        super().__init__(code)


def normalize_expression(value: str) -> str:
    """Only case-fold and collapse whitespace; punctuation and wording stay literal."""
    if not isinstance(value, str):
        raise ExpressionViewError("expression_must_be_text")
    return " ".join(value.casefold().split())


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _json_digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return _sha256(raw)


def _require(condition: Any, code: str) -> None:
    if not condition:
        raise ExpressionViewError(code)


def _verified_module_bytes(native_root: Path, native_manifest: dict[str, Any],
                           relative_path: str = MODULE_RELATIVE_PATH) -> tuple[bytes, str]:
    members = native_manifest.get("members")
    _require(isinstance(members, dict), "native_manifest_members_missing")
    row = members.get(relative_path)
    _require(isinstance(row, dict), "sealed_candidate_module_not_in_native_manifest")
    expected_sha = row.get("sha256")
    expected_bytes = row.get("bytes")
    _require(isinstance(expected_sha, str) and re.fullmatch(r"[0-9a-f]{64}", expected_sha),
             "sealed_candidate_module_hash_missing")
    member = Path(relative_path)
    _require(not member.is_absolute() and ".." not in member.parts, "unsafe_sealed_candidate_module_path")
    path = Path(native_root) / member
    _require(path.is_file() and not path.is_symlink(), "sealed_candidate_module_missing_or_unsafe")
    raw = path.read_bytes()
    _require(expected_bytes is None or len(raw) == expected_bytes, "sealed_candidate_module_size_mismatch")
    actual_sha = _sha256(raw)
    _require(actual_sha == expected_sha, "sealed_candidate_module_hash_mismatch")
    return raw, actual_sha


def _literal_text(literals: dict[str, Any], literal_id: Any) -> str:
    _require(isinstance(literal_id, str) and literal_id in literals, "canonical_literal_reference_missing")
    value = literals[literal_id]
    _require(isinstance(value, str), "canonical_literal_not_text")
    return value


def _decode_tree(value: Any, literals: dict[str, Any]) -> Any:
    if isinstance(value, dict) and set(value) == {"$literal"}:
        return _literal_text(literals, value["$literal"])
    if isinstance(value, list):
        return [_decode_tree(item, literals) for item in value]
    if isinstance(value, dict):
        return {key: _decode_tree(item, literals) for key, item in value.items()}
    return value


def _canonical_cues(record: dict[str, Any]) -> list[dict[str, str]]:
    meaning = record.get("meaning")
    _require(isinstance(meaning, dict) and meaning.get("schema") == MEANING_SCHEMA,
             "canonical_meaning_v1_required")
    literals = meaning.get("literals")
    search = meaning.get("search")
    fields = search.get("fields") if isinstance(search, dict) else None
    _require(isinstance(literals, dict) and isinstance(fields, dict), "canonical_search_fields_missing")

    native = record.get("native")
    _require(isinstance(native, dict) and native.get("schema") == NATIVE_TREE_SCHEMA,
             "canonical_native_literal_tree_required")
    tree = _decode_tree(native.get("tree"), literals)
    _require(isinstance(tree, dict), "canonical_native_tree_missing")

    cues: list[dict[str, str]] = []
    for field in LOOKUP_FIELDS:
        references = fields.get(field, [])
        _require(isinstance(references, list), "canonical_lookup_field_not_list")
        terms = [_literal_text(literals, ref) for ref in references]
        if field in {"aliases", "keywords"}:
            tree_terms = tree.get(field, [])
            _require(isinstance(tree_terms, list) and all(isinstance(item, str) for item in tree_terms),
                     "canonical_native_lookup_field_not_list")
            _require(tree_terms == terms, "canonical_native_lookup_field_mismatch")
        for term in terms:
            if normalize_expression(term):
                cues.append({"field": field, "text": term})
    return cues


def _canonical_meaning(record: dict[str, Any]) -> dict[str, str]:
    meaning = record["meaning"]
    literals = meaning["literals"]
    primary = meaning.get("primary")
    base = primary.get("base") if isinstance(primary, dict) else None
    _require(isinstance(base, dict), "canonical_primary_meaning_missing")
    result = {}
    for field, pointer in PRIMARY_MEANING_FIELDS.items():
        _require(pointer in base, "canonical_primary_meaning_field_missing")
        result[field] = _literal_text(literals, base[pointer])
    return result


def _route_record_kind(record: dict[str, Any]) -> tuple[str, str]:
    retrieval_class = record["meaning"].get("retrieval_class")
    record_kind = record.get("record_kind")
    if retrieval_class == "positive" and record_kind == "visual_option":
        return "positive_discovery", "positive"
    if retrieval_class == "diagnostic" and record_kind == "diagnostic":
        effects = record.get("effects")
        _require(isinstance(effects, dict), "diagnostic_effects_missing")
        _require(not effects.get("dimensions") and not effects.get("properties"),
                 "diagnostic_must_not_carry_visual_effects")
        return "diagnostic/source_limited", "diagnostic"
    raise ExpressionViewError("candidate_retrieval_class_record_kind_mismatch")


def lookup_module(module: dict[str, Any], expression: str, *, module_sha256: str,
                  generation_id: str, native_generation_id: str,
                  execution: dict[str, Any]) -> dict[str, Any]:
    """Exact normalized lookup; every matching CID and canonical meaning is returned."""
    _require(isinstance(module, dict) and module.get("schema") == NATIVE_MODULE_SCHEMA,
             "photo_candidate_module_v4_required")
    query = normalize_expression(expression)
    _require(bool(query), "expression_must_not_be_empty")
    candidates = module.get("candidates")
    _require(isinstance(candidates, dict), "candidate_map_missing")

    matches: list[dict[str, Any]] = []
    for cid in sorted(candidates):
        record = candidates[cid]
        _require(isinstance(cid, str) and isinstance(record, dict) and record.get("id") == cid,
                 "candidate_identity_mismatch")
        classification, retrieval_class = _route_record_kind(record)
        cues = _canonical_cues(record)
        exact_cues = [cue for cue in cues if normalize_expression(cue["text"]) == query]
        if not exact_cues:
            continue
        seen = set()
        unique_cues = []
        for cue in exact_cues:
            key = (cue["field"], cue["text"])
            if key in seen:
                continue
            seen.add(key)
            unique_cues.append({**cue, "cue_role": "lookup_cue_only_not_fact"})
        meaning = _canonical_meaning(record)
        provenance = record.get("provenance", [])
        _require(isinstance(provenance, list), "candidate_provenance_not_list")
        matches.append({
            "cid": cid,
            "classification": classification,
            "retrieval_class": retrieval_class,
            "matched_lookup_cues": unique_cues,
            "meaning": {
                **meaning,
                "basis": "canonical_native_v4_primary_meaning; source-authored and not an independently verified fact",
            },
            "provenance": provenance,
            "native_approval": False,
        })

    meaning_keys = {
        (row["meaning"]["en"], row["meaning"]["ko"], row["meaning"]["definition"])
        for row in matches
    }
    status = "unrecognized" if not matches else ("ambiguous" if len(meaning_keys) > 1 else "matched")
    variants = [
        {"cid": row["cid"], **{key: row["meaning"][key] for key in ("en", "ko", "definition")}}
        for row in matches
    ]
    return {
        "schema": SCHEMA,
        "status": status,
        "execution": execution,
        "lookup": {
            "expression": expression,
            "normalized_expression": query,
            "method": "exact_casefold_whitespace_only",
            "ranked": False,
            "inferred_meaning": None,
        },
        "source": {
            "generation_id": generation_id,
            "native_generation_id": native_generation_id,
            "run_bound_generation_id": execution.get("run_bound_generation_id"),
            "module": MODULE_RELATIVE_PATH,
            "module_sha256": module_sha256,
        },
        "matched_cids": [row["cid"] for row in matches],
        "meaning_variants": variants,
        "matches": matches,
        "native_approval": False,
        "lookup_authority": False,
        "visual_fact_established": False,
    }


def lookup_from_release(expression: str, *, api, store: Path, generation_id: str,
                        execution: dict[str, Any]) -> dict[str, Any]:
    """Use the installed resolver, then verify and read only this candidate module."""
    try:
        native_root, h2_manifest, native_manifest = api.release(store, generation_id)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ExpressionViewError("sealed_h2_generation_unavailable",
                                  lookup_generation_id=generation_id,
                                  run_bound_generation_id=execution.get("run_bound_generation_id")) from exc
    try:
        raw, module_sha = _verified_module_bytes(native_root, native_manifest)
    except ExpressionViewError as exc:
        raise ExpressionViewError(exc.code, lookup_generation_id=generation_id,
                                  run_bound_generation_id=execution.get("run_bound_generation_id")) from exc
    try:
        module = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ExpressionViewError("sealed_candidate_module_invalid_json") from exc
    return lookup_module(
        module,
        expression,
        module_sha256=module_sha,
        generation_id=generation_id,
        native_generation_id=h2_manifest.get("native_generation_id", ""),
        execution=execution,
    )
