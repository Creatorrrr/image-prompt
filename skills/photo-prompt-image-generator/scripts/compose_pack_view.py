#!/usr/bin/env python3
"""Create a lossless, on-demand composition view of an immutable v6 pack.

Only known optional candidate inventories are deferred. Every other field,
including unknown future requirements, remains visible. This is a reading aid;
the original pack remains the sole input to composition and runtime audits.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

VERSION = "photo-composer-view/v1"
OPTIONAL_PATHS = (
    ("presets",),
    ("photographic_integration", "category_candidates"),
    ("visual_proposition", "core_candidates"),
    ("visual_proposition", "tension_candidates"),
    ("photographic_craft", "dimension_candidates"),
    ("visual_concept_candidates", "candidates"),
    ("creative_augmentation", "candidates"),
    ("character_response", "advisory_retrieval", "candidates"),
)
SUMMARY_FIELDS = (
    "concept_terms", "applicability", "conflicts_with", "affected_dimensions",
    "slot", "axis", "semantic_band", "hard_eligible", "semantic_consistency",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def source_pack(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list) and len(payload) == 1:
        payload = payload[0]
    if not isinstance(payload, dict) or payload.get("contract_version") != "photo-candidate-pack/v6":
        raise ValueError("composer view requires exactly one original v6 candidate pack")
    hashable = dict(payload, pack_id=None)
    if payload.get("pack_id") != digest(hashable)[:16]:
        raise ValueError("source pack_id does not match the immutable pack content")
    return payload


def pointer(path: tuple[str, ...]) -> str:
    return "/" + "/".join(part.replace("~", "~0").replace("/", "~1") for part in path)


def inventory_paths(pack: dict[str, Any]) -> list[tuple[str, ...]]:
    paths = list(OPTIONAL_PATHS)
    if isinstance(pack.get("slots"), dict):
        paths.extend(("slots", slot, "candidates") for slot in pack["slots"])
    return paths


def locate(root: dict[str, Any], path: tuple[str, ...]) -> tuple[dict[str, Any], str] | None:
    parent = root
    for key in path[:-1]:
        parent = parent.get(key)
        if not isinstance(parent, dict):
            return None
    return (parent, path[-1]) if path[-1] in parent else None


def deferable(rows: Any) -> bool:
    if not isinstance(rows, list) or not rows:
        return False
    for row in rows:
        if not isinstance(row, dict) or not (row.get("id") or row.get("candidate_id")):
            return False
        applicability = row.get("applicability") or {}
        if not isinstance(applicability, dict):
            return False
        if row.get("required_in_final_prompt") or row.get("required") or applicability.get("status") == "required":
            return False
    return True


def build_view(payload: Any, candidate_ids: list[str] | None = None) -> dict[str, Any]:
    pack = source_pack(payload)
    projection = copy.deepcopy(pack)
    catalog: list[dict[str, Any]] = []
    records: dict[str, list[dict[str, Any]]] = {}
    for path in inventory_paths(pack):
        found = locate(projection, path)
        if found is None:
            continue
        parent, key = found
        rows = parent[key]
        if not deferable(rows):
            continue
        ids = []
        for index, row in enumerate(rows):
            candidate_id = str(row.get("id") or row["candidate_id"])
            ids.append(candidate_id)
            source_pointer = pointer((*path, str(index)))
            record = {"id": candidate_id, "source_pointer": source_pointer, "candidate": copy.deepcopy(row)}
            records.setdefault(candidate_id, []).append(record)
            summary = {"id": candidate_id, "source_pointer": source_pointer}
            summary.update({field: copy.deepcopy(row[field]) for field in SUMMARY_FIELDS if field in row})
            catalog.append(summary)
        parent[key] = {"deferred_candidate_ids": ids, "read_details_before_selection": True}

    binding = {"source_pack_id": pack["pack_id"], "source_pack_sha256": digest(pack)}
    if candidate_ids:
        missing = sorted(set(candidate_ids) - records.keys())
        if missing:
            raise ValueError("unknown deferred candidate IDs: " + ", ".join(missing))
        result = {
            "contract_version": VERSION,
            "mode": "candidate_details",
            **binding,
            "candidates": [record for candidate_id in dict.fromkeys(candidate_ids) for record in records[candidate_id]],
        }
    else:
        result = {
            "contract_version": VERSION,
            "mode": "composition_overview",
            **binding,
            "audit_input": "original_candidate_pack_only",
            "selection_rule": "Read full details before selecting a deferred candidate. Every selected visual concept brings its entire opt-in obligation and render gates.",
            "requirements": projection,
            "candidate_catalog": catalog,
        }
    result["view_sha256"] = digest(result)
    return result


def verify_view(pack: Any, view: Any) -> None:
    if not isinstance(view, dict):
        raise ValueError("view must contain one JSON object")
    ids = None
    if view.get("mode") == "candidate_details":
        ids = list(dict.fromkeys(row["id"] for row in view.get("candidates", [])))
        if not ids:
            raise ValueError("candidate detail view must contain selected records")
    if view != build_view(pack, ids):
        raise ValueError("view differs from its original pack projection")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--candidate-id", action="append")
    parser.add_argument("--verify-view", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        pack = json.loads(args.pack.read_text(encoding="utf-8"))
        if args.verify_view:
            verify_view(pack, json.loads(args.verify_view.read_text(encoding="utf-8")))
            result = {"status": "pass", "source_pack_id": source_pack(pack)["pack_id"]}
        else:
            result = build_view(pack, args.candidate_id)
        serialized = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
        if args.output:
            if args.output.resolve() == args.pack.resolve():
                raise ValueError("output cannot overwrite the original candidate pack")
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"composer view: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
