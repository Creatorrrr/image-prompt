from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from .common import MaintenanceError, RECIPES, decode
from .links import path_key

REQUIRED = {"record_id", "finding_or_path_key", "decision", "rationale", "evidence_refs",
            "input_entity_hashes", "recipe_versions", "reviewed_at"}


def load_reviews(path: Path | None) -> list:
    if path is None:
        return []
    rows, ids = [], set()
    for number, raw in enumerate(path.read_bytes().splitlines(), 1):
        if not raw.strip():
            continue
        row = decode(raw)
        if (not isinstance(row, dict) or not REQUIRED <= row.keys() or row.keys() - REQUIRED - {"reviewer", "support_level"}
                or row["decision"] not in {"retain", "revise", "reject", "defer"}
                or not isinstance(row["rationale"], str) or not row["rationale"].strip()
                or not isinstance(row["evidence_refs"], list) or not row["evidence_refs"]
                or not isinstance(row["input_entity_hashes"], dict) or not row["input_entity_hashes"]
                or not isinstance(row["record_id"], str) or not row["record_id"]
                or not isinstance(row["finding_or_path_key"], str)
                or not row["finding_or_path_key"].startswith(("finding:", "path:", "edge:"))
                or any(not isinstance(key, str) or not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
                       for key, value in row["input_entity_hashes"].items())
                or not isinstance(row["recipe_versions"], dict)
                or row.get("support_level", "undetermined") not in {"partial_support", "collective_support", "insufficient", "undetermined", "full_support"}):
            raise MaintenanceError("review_invalid", f"invalid review row {number}")
        if row["record_id"] in ids:
            raise MaintenanceError("review_invalid", f"duplicate review record ID at row {number}")
        if datetime.fromisoformat(row["reviewed_at"].replace("Z", "+00:00")).tzinfo is None:
            raise MaintenanceError("review_invalid", "review time requires a timezone")
        ids.add(row["record_id"])
        rows.append(row)
    return rows


def review_states(rows: list, inventory: dict, findings: list, links: dict | None) -> dict:
    nodes = {row["id"]: row for row in inventory["nodes"]}
    subjects = {row["id"]: row["entity_ids"] for row in findings}
    edge_pairs = set()
    if links:
        for edge in links["edges"]:
            subjects[edge["id"]] = [edge["source"], edge["target"]]
            edge_pairs.add((edge["source"], edge["target"]))
    result = {}
    # NDJSON order is append order; the last decision is the effective one.
    for row in rows:
        key = row["finding_or_path_key"]
        identities = row["input_entity_hashes"]
        expected = subjects.get(key)
        if key.startswith("path:"):
            path = sorted(identities, key=lambda identity: {"slot": 0, "bundle": 1, "profile": 2}.get(identity.split(":", 1)[0], 3))
            if path_key(path) == key and all(pair in edge_pairs for pair in zip(path, path[1:])):
                expected = path
        valid = (expected is not None and set(expected) == set(identities)
                 and row["recipe_versions"] == RECIPES
                 and all(identity in nodes and nodes[identity]["entity_sha256"] == value for identity, value in identities.items()))
        result[key] = {"status": "current" if valid else "stale", "record_id": row["record_id"],
                       "decision": row["decision"], "rationale": row["rationale"],
                       "support_level": row.get("support_level", "undetermined")}
    return result
