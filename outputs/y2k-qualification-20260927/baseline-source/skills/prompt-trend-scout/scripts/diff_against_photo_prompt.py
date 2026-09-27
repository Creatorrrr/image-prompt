#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import TARGET_SKILL_DIR, default_data_dir, load_json, read_records, run_id, utc_now, write_json


def existing_index() -> dict[str, Any]:
    tags = load_json(TARGET_SKILL_DIR / "assets" / "photo_prompt_tags.json")
    recipes = load_json(TARGET_SKILL_DIR / "assets" / "concept_recipes.json")
    slot_ids: dict[str, set[str]] = {}
    slot_text: dict[str, set[str]] = {}
    for slot, values in tags.get("slots", {}).items():
        ids: set[str] = set()
        text_values: set[str] = set()
        for item in values if isinstance(values, list) else []:
            if isinstance(item, dict):
                ids.add(str(item.get("id", "")))
                text_values.add(str(item.get("en", "")).lower())
                text_values.add(str(item.get("ko", "")).lower())
        slot_ids[slot] = ids
        slot_text[slot] = {v for v in text_values if v}
    facet_values = {
        facet: {str(value) for value in values}
        for facet, values in tags.get("facet_vocab", {}).items()
        if isinstance(values, list)
    }
    recipe_names = set(recipes.get("roles", {})) | set(recipes.get("mixins", {})) | set(recipes.get("aliases", {}))
    return {"slot_ids": slot_ids, "slot_text": slot_text, "facet_values": facet_values, "recipe_names": recipe_names}


def diff_candidates(input_path: str, *, output: str | None = None, data_dir: str | None = None) -> dict[str, Any]:
    candidates = read_records(Path(input_path))
    index = existing_index()
    diffed: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate = dict(candidate)
        proposed = candidate.get("proposed", {})
        overlaps: list[str] = []
        novelty = "new"
        if candidate["kind"] == "tag":
            slot = proposed.get("slot", "")
            value = proposed.get("value") or proposed.get("id")
            en = str(proposed.get("en", "")).lower()
            if value in index["slot_ids"].get(slot, set()):
                novelty = "reinforce"
                overlaps.append(f"{slot}.{value}")
            elif en and en in index["slot_text"].get(slot, set()):
                novelty = "reinforce"
                overlaps.append(f"{slot}.text:{en}")
            elif slot not in index["slot_ids"]:
                novelty = "conflict"
                overlaps.append(f"unknown_slot:{slot}")
        elif candidate["kind"] == "facet_value":
            facet = proposed.get("facet_name", "")
            value = proposed.get("value") or proposed.get("id")
            if value in index["facet_values"].get(facet, set()):
                novelty = "reinforce"
                overlaps.append(f"facet:{facet}.{value}")
            elif facet and facet not in index["facet_values"]:
                novelty = "conflict"
                overlaps.append(f"unknown_facet:{facet}")
        elif candidate["kind"] == "recipe":
            name = proposed.get("id", "")
            if name in index["recipe_names"]:
                novelty = "reinforce"
                overlaps.append(f"recipe:{name}")
        candidate["novelty"] = novelty
        candidate["overlap_with_existing"] = overlaps
        if novelty == "conflict" and candidate.get("recommendation") == "adopt":
            candidate["recommendation"] = "needs_human"
        diffed.append(candidate)

    data_root = default_data_dir(data_dir)
    rid = run_id("diffed")
    out = Path(output) if output else data_root / "candidates" / f"{rid}.json"
    write_json(out, {"run_id": rid, "generated_at": utc_now(), "records": diffed})
    return {"run_id": rid, "output": str(out), "records": diffed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare prompt trend candidates with photo-prompt assets.")
    parser.add_argument("input")
    parser.add_argument("--output")
    parser.add_argument("--data-dir")
    args = parser.parse_args()
    result = diff_candidates(args.input, output=args.output, data_dir=args.data_dir)
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
