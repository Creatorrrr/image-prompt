#!/usr/bin/env python3
"""Compile the v5 manifest over immutable grammar v4 plus visual additions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from moe_element_runtime import load_moe_element_assets, load_moe_grammar_assets
from moe_visual_addition import (
    ADDITION_FILENAME,
    build_v5_manifest,
    load_moe_visual_additions,
)


def compile_manifest(asset_dir: str | Path) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve()
    legacy = load_moe_element_assets(root)
    base = load_moe_grammar_assets(
        root,
        legacy_assets=legacy,
        grammar_version="v4",
    )
    if base.visual_contracts is None:
        raise ValueError("v4 visual contracts are unavailable")
    additions = load_moe_visual_additions(
        root / "research_evidence_moe_elements" / ADDITION_FILENAME,
        base_grammar_sha256=base.grammar_sha256,
        base_elements_by_id=base.elements_by_id,
        base_alias_bindings=base.visual_contracts.alias_bindings,
    )
    return build_v5_manifest(
        base_grammar_sha256=base.grammar_sha256,
        base_elements_by_id=base.elements_by_id,
        base_visual_contracts=base.visual_contracts.contracts_by_id,
        base_image_evidence=base.visual_contracts.image_evidence_by_id,
        base_candidate_count=int(base.payload["candidate_count"]),
        base_compatibility_sha256=base.compatibility_sha256,
        additions=additions,
    )


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
    root = args.asset_dir.expanduser().resolve()
    output = args.output or root / "illustration_moe_grammar_v5.json"
    encoded = _encoded(compile_manifest(root))
    if args.check:
        if not output.is_file() or output.read_bytes() != encoded:
            raise SystemExit("compiled v5 grammar manifest is stale")
    else:
        output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "check": args.check,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
