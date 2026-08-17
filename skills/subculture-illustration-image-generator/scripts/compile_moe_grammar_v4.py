#!/usr/bin/env python3
"""Compile typed visual meaning contracts onto the immutable v3 grammar."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from compile_moe_grammar_v3 import compile_grammar as compile_v3_grammar
from moe_meaning_contract import MEANING_FILENAME, load_meaning_contracts
from moe_visual_contract import (
    IMAGE_EVIDENCE_FILENAME,
    IMAGE_EVIDENCE_SCHEMA,
    VISUAL_MEANING_FILENAME,
    VISUAL_MEANING_SCHEMA,
    load_visual_meaning_contracts,
    visual_contract_sha256,
)


GRAMMAR_SCHEMA = "subculture-illustration-moe-grammar/v4"


def compile_grammar(asset_dir: str | Path) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve()
    v3 = compile_v3_grammar(root)
    v3_path = root / "illustration_moe_grammar_v3.json"
    try:
        v3_raw = v3_path.read_bytes()
        stored_v3 = json.loads(v3_raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load stored v3 grammar: {exc}") from exc
    if stored_v3 != v3:
        raise ValueError("stored v3 grammar is stale")
    expected_ids = [str(element["id"]) for element in v3["elements"]]
    base_meanings = load_meaning_contracts(
        root / "research_evidence_moe_elements" / MEANING_FILENAME,
        expected_element_ids=expected_ids,
    )
    visual_meanings = load_visual_meaning_contracts(
        root / "research_evidence_moe_elements" / VISUAL_MEANING_FILENAME,
        evidence_path=(
            root / "research_evidence_moe_elements" / IMAGE_EVIDENCE_FILENAME
        ),
        base_meanings=base_meanings,
        expected_element_ids=expected_ids,
        expected_aliases={
            str(element["id"]): list(element["aliases"]) for element in v3["elements"]
        },
        expected_candidate_subtypes={
            str(element["id"]): {
                str(candidate["subtype_id"]) for candidate in element["candidates"]
            }
            for element in v3["elements"]
        },
    )
    compiled = copy.deepcopy(v3)
    compiled["schema"] = GRAMMAR_SCHEMA
    compiled["created_at"] = "2026-08-18T00:00:00+09:00"
    compiled["base_grammar_v3_sha256"] = hashlib.sha256(v3_raw).hexdigest()
    compiled["visual_meaning_contract_schema"] = VISUAL_MEANING_SCHEMA
    compiled["visual_meaning_contracts_sha256"] = visual_meanings.sha256
    compiled["image_search_evidence_schema"] = IMAGE_EVIDENCE_SCHEMA
    compiled["image_search_evidence_sha256"] = visual_meanings.evidence_sha256

    for element in compiled["elements"]:
        element_id = str(element["id"])
        visual_contract = copy.deepcopy(
            visual_meanings.contracts_by_id[element_id]
        )
        element["visual_meaning_contract"] = visual_contract
        element["visual_meaning_contract_sha256"] = visual_contract_sha256(
            visual_contract
        )
    return compiled


def _encoded(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    asset_dir = args.asset_dir.expanduser().resolve()
    output = args.output or asset_dir / "illustration_moe_grammar_v4.json"
    payload = compile_grammar(asset_dir)
    encoded = _encoded(payload)
    if args.check:
        try:
            current = output.read_bytes()
        except OSError as exc:
            raise SystemExit(f"cannot read compiled grammar for --check: {exc}")
        if current != encoded:
            raise SystemExit("compiled v4 grammar is stale")
    else:
        output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "elements": payload["element_count"],
                "candidates": payload["candidate_count"],
                "sources": payload["source_count"],
                "check": args.check,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
