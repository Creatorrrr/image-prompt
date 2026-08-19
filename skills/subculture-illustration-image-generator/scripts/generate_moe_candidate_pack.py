#!/usr/bin/env python3
"""Build or audit current v7 or explicit historical v6/v5/v4 moe packs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from moe_element_runtime import (
    MoeElementError,
    audit_moe_candidate_pack,
    build_moe_candidate_pack,
    canonical_json_bytes,
    compose_moe_prompt_draft,
    load_moe_element_assets,
    load_moe_grammar_assets,
)


def _load_object(value: str, *, name: str) -> dict[str, Any]:
    candidate = Path(value).expanduser()
    try:
        raw = candidate.read_text(encoding="utf-8") if candidate.is_file() else value
    except OSError as exc:
        raise MoeElementError(f"cannot read {name}: {exc}") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise MoeElementError(f"invalid {name} JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise MoeElementError(f"{name} must contain one JSON object")
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Wrap one unchanged illustration candidate pack with explicit, "
            "research-backed moe candidates and preference-aware selection."
        )
    )
    parser.add_argument(
        "--base-pack", required=True, help="base v1-v3 pack path or JSON"
    )
    parser.add_argument(
        "--element",
        action="append",
        default=[],
        help="exact element ID or complete reviewed alias; repeat up to three times",
    )
    parser.add_argument(
        "--preference-text",
        help="full user wording used only to rank candidates inside explicitly selected elements",
    )
    parser.add_argument(
        "--output-mode",
        choices=(
            "auto",
            "single_frame",
            "paired_frame",
            "sequence",
            "optical_interaction",
        ),
        default="auto",
    )
    parser.add_argument(
        "--grammar-version",
        choices=("v5", "v4", "v3", "v2"),
        default="v5",
        help=(
            "current researched visual-additions v5 (default), visual v4 replay, "
            "meaning-only v3 replay, or historical v2 replay"
        ),
    )
    parser.add_argument(
        "--compose-from",
        help="optional already-audited base English prompt; emits an auditable draft",
    )
    parser.add_argument(
        "--audit-composed",
        help="optional composed JSON path or inline JSON",
    )
    parser.add_argument("--asset-dir", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        legacy = load_moe_element_assets(args.asset_dir)
        grammar = load_moe_grammar_assets(
            args.asset_dir,
            legacy_assets=legacy,
            grammar_version=args.grammar_version,
        )
        pack = build_moe_candidate_pack(
            _load_object(args.base_pack, name="base pack"),
            args.element,
            preference_text=args.preference_text,
            output_mode=args.output_mode,
            legacy_assets=legacy,
            grammar_assets=grammar,
        )
        payload: Any = pack
        if args.compose_from is not None:
            payload = {
                "candidate_pack": pack,
                "composed": compose_moe_prompt_draft(pack, args.compose_from),
            }
        if args.audit_composed is not None:
            composed = _load_object(args.audit_composed, name="composed prompt")
            payload = {
                "candidate_pack": pack,
                "audit": audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=legacy,
                    grammar_assets=grammar,
                ),
            }
        sys.stdout.buffer.write(canonical_json_bytes(payload) + b"\n")
        return 0
    except (MoeElementError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
