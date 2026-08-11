#!/usr/bin/env python3
"""CLI for the explicit, additive moe-element planning layer."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

from moe_element_runtime import (
    MoeElementError,
    audit_moe_element_prompt,
    build_moe_element_plan,
    canonical_json_bytes,
    list_moe_elements,
    load_moe_element_assets,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build an explicit-only, source-backed moe-element prompt plan. "
            "This command does not change the ordinary illustration candidate pack."
        )
    )
    parser.add_argument(
        "--element",
        action="append",
        default=[],
        help="exact moe element ID or complete reviewed alias; repeat up to three times",
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
    parser.add_argument("--list-elements", action="store_true")
    parser.add_argument(
        "--audit-prompt", help="audit this English prompt against the generated plan"
    )
    parser.add_argument("--output-file", help="write canonical JSON to this path")
    parser.add_argument("--asset-dir", help=argparse.SUPPRESS)
    return parser


def _write(path_value: str, payload: Any) -> None:
    path = Path(path_value).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(payload) + b"\n")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        assets = load_moe_element_assets(args.asset_dir)
        if args.list_elements:
            if args.element or args.audit_prompt:
                raise MoeElementError(
                    "--list-elements cannot be combined with selection or audit"
                )
            payload: Any = {
                "schema": "subculture-illustration-moe-element-list/v1",
                "elements": list_moe_elements(assets),
            }
        else:
            payload = build_moe_element_plan(
                args.element,
                output_mode=args.output_mode,
                assets=assets,
            )
            if args.audit_prompt is not None:
                payload = {
                    "plan": payload,
                    "audit": audit_moe_element_prompt(
                        payload, args.audit_prompt, assets=assets
                    ),
                }
        if args.output_file:
            _write(args.output_file, payload)
        sys.stdout.buffer.write(canonical_json_bytes(payload) + b"\n")
        return 0
    except (MoeElementError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
