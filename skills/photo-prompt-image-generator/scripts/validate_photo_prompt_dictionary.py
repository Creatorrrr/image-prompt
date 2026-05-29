#!/usr/bin/env python3
"""Validate optional semantic metadata in photo_prompt_tags.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from prompt_generator import DEFAULT_FACET_VOCAB, load_json, normalize_list


def merged_facet_vocab(data: dict[str, Any]) -> dict[str, set[str]]:
    vocab: dict[str, set[str]] = {key: set(values) for key, values in DEFAULT_FACET_VOCAB.items()}
    for key, values in (data.get("facet_vocab") or {}).items():
        vocab.setdefault(str(key), set()).update(str(value) for value in values)
    return vocab


def all_entries(data: dict[str, Any]):
    for preset in data.get("presets", []):
        yield f"preset:{preset.get('id')}", preset
    for recipe in data.get("recipes", []):
        yield f"recipe:{recipe.get('id')}", recipe
    for slot, entries in data.get("slots", {}).items():
        for entry in entries:
            yield f"slot:{slot}:{entry.get('id')}", entry


def validate_facets(label: str, entry: dict[str, Any], vocab: dict[str, set[str]], errors: list[str]) -> None:
    facets = entry.get("facets", {}) or {}
    if facets and not isinstance(facets, dict):
        errors.append(f"{label}: facets must be an object")
        return
    for key, raw_values in facets.items():
        if key not in vocab:
            errors.append(f"{label}: unknown facet key {key}")
            continue
        for value in normalize_list(raw_values):
            if value not in vocab[key]:
                errors.append(f"{label}: unknown facet value {key}:{value}")


def validate_guard_token(label: str, token: str, vocab: dict[str, set[str]], errors: list[str]) -> None:
    if ":" not in token:
        errors.append(f"{label}: guard facet must use key:value format: {token}")
        return
    key, value = token.split(":", 1)
    if key not in vocab:
        errors.append(f"{label}: unknown facet key {key}")
        return
    if value not in vocab[key]:
        errors.append(f"{label}: unknown facet value {key}:{value}")


def validate_hard_guards(label: str, entry: dict[str, Any], vocab: dict[str, set[str]], errors: list[str]) -> None:
    guards = entry.get("hard_guards", {}) or {}
    if guards and not isinstance(guards, dict):
        errors.append(f"{label}: hard_guards must be an object")
        return
    for key in ("requires_facets", "exclude_facets"):
        for token in normalize_list(guards.get(key)):
            validate_guard_token(label, token, vocab, errors)


def validate_filter_ids(data: dict[str, Any], errors: list[str]) -> None:
    slots = data.get("slots", {})
    for preset in data.get("presets", []):
        for slot, flt in preset.get("filters", {}).items():
            if slot not in slots:
                errors.append(f"preset:{preset.get('id')}: missing filtered slot {slot}")
                continue
            valid_ids = {entry.get("id") for entry in slots[slot]}
            for tag_id in flt.get("ids", []):
                if tag_id not in valid_ids:
                    errors.append(f"preset:{preset.get('id')}: unknown {slot} id {tag_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate photo prompt dictionary semantic metadata.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    args = parser.parse_args()

    data = load_json(args.tags)
    errors: list[str] = []
    vocab = merged_facet_vocab(data)

    validate_filter_ids(data, errors)
    for label, entry in all_entries(data):
        validate_facets(label, entry, vocab, errors)
        validate_hard_guards(label, entry, vocab, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("photo prompt dictionary metadata is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
