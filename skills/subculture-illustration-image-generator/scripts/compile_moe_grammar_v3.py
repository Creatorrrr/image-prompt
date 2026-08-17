#!/usr/bin/env python3
"""Compile canonical meaning contracts onto the immutable v2 candidate grammar."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from compile_moe_grammar_v2 import compile_grammar as compile_v2_grammar
from moe_meaning_contract import (
    MEANING_FILENAME,
    MEANING_SCHEMA,
    contract_sha256,
    load_meaning_contracts,
    runtime_label_present,
)


GRAMMAR_SCHEMA = "subculture-illustration-moe-grammar/v3"


def compile_grammar(asset_dir: str | Path) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve()
    v2 = compile_v2_grammar(root)
    expected_ids = [str(element["id"]) for element in v2["elements"]]
    meanings = load_meaning_contracts(
        root / "research_evidence_moe_elements" / MEANING_FILENAME,
        expected_element_ids=expected_ids,
    )
    compiled = copy.deepcopy(v2)
    compiled["schema"] = GRAMMAR_SCHEMA
    compiled["created_at"] = "2026-08-17T00:00:00+09:00"
    compiled["meaning_contract_schema"] = MEANING_SCHEMA
    compiled["meaning_contracts_sha256"] = meanings.sha256

    for element in compiled["elements"]:
        element_id = str(element["id"])
        contract = copy.deepcopy(meanings.contracts_by_id[element_id])
        element["definition_and_history"] = contract["canonical_definition_ko"]
        element["semantic_subtypes"] = [
            subtype
            for subtype in element["semantic_subtypes"]
            if not str(subtype.get("id", "")).startswith("researched_variant_")
        ]
        if len(element["semantic_subtypes"]) < 2:
            raise ValueError(
                f"{element_id} lacks two non-placeholder semantic subtypes"
            )
        element["meaning_contract"] = contract

        for candidate in element["candidates"]:
            runtime_fragments = [
                candidate["primary_atom"]["prompt_fragment_en"],
                *[atom["prompt_fragment_en"] for atom in candidate["support_atoms"]],
            ]
            for label in contract["runtime_forbidden_labels"]:
                if any(
                    runtime_label_present(label, fragment)
                    for fragment in runtime_fragments
                ):
                    raise ValueError(
                        f"{element_id}/{candidate['id']} leaks runtime-forbidden label {label!r}"
                    )
        element["meaning_contract_sha256"] = contract_sha256(contract)
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
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the deterministic compile result without writing",
    )
    args = parser.parse_args()
    asset_dir = args.asset_dir.expanduser().resolve()
    output = args.output or asset_dir / "illustration_moe_grammar_v3.json"
    payload = compile_grammar(asset_dir)
    encoded = _encoded(payload)
    if args.check:
        try:
            current = output.read_bytes()
        except OSError as exc:
            raise SystemExit(f"cannot read compiled grammar for --check: {exc}")
        if current != encoded:
            raise SystemExit("compiled v3 grammar is stale")
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
