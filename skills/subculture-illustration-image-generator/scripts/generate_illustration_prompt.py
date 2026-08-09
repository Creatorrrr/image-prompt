#!/usr/bin/env python3
"""CLI wrapper for deterministic subculture illustration candidate packs."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

from illustration_runtime import (
    IllustrationRuntimeError,
    InputContractError,
    build_candidate_pack,
    canonical_json_bytes,
    list_formats,
    list_topics,
    load_runtime_assets,
)


EXIT_OK = 0
EXIT_UNEXPECTED = 1
EXIT_INPUT = 2
EXIT_ASSET = 3
EXIT_RESOLUTION = 4
EXIT_IO = 5


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve a typed illustration topic/format and emit one deterministic "
            "candidate pack. This command does not compose a final prompt or call an image API."
        ),
    )
    parser.add_argument("--concept", help="natural-language illustration request")
    parser.add_argument(
        "--topic",
        "--route",
        dest="topic",
        default="auto",
        help="auto or one exact topic/route ID (default: auto)",
    )
    parser.add_argument(
        "--format",
        dest="format_id",
        default="auto",
        help="auto or one exact format variant ID (default: auto)",
    )
    parser.add_argument("--seed", type=int, default=0, help="deterministic signed integer seed")
    parser.add_argument(
        "--creativity",
        type=float,
        default=0.5,
        help="creative-development level from 0 through 1 (default: 0.5)",
    )
    parser.add_argument(
        "--safety-evaluation",
        action="store_true",
        help="record the explicitly requested local contract evaluation instead of the automatic-pass default",
    )
    parser.add_argument(
        "--emit-candidate-pack",
        action="store_true",
        help="emit the full candidate pack on stdout (accepted for skill-contract clarity)",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="print machine-readable JSON instead of a compact human summary",
    )
    parser.add_argument("--output-file", help="atomically write the JSON result to this path")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--list-topics", action="store_true", help="list the 24 exact topic IDs")
    modes.add_argument("--list-formats", action="store_true", help="list the 10 exact format variants")
    parser.add_argument(
        "--asset-dir",
        help=argparse.SUPPRESS,
    )
    return parser


def _atomic_write_json(path_value: str, payload: Any) -> None:
    path = Path(path_value).expanduser().resolve()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = canonical_json_bytes(payload) + b"\n"
        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=str(path.parent),
        )
        try:
            with os.fdopen(file_descriptor, "wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, path)
        except BaseException:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise
    except OSError as exc:
        raise OSError(f"cannot atomically write {path}: {exc}") from exc


def _print_json(payload: Any) -> None:
    sys.stdout.buffer.write(canonical_json_bytes(payload) + b"\n")


def _print_topic_list(items: list[dict[str, Any]]) -> None:
    for item in items:
        variants = ",".join(item["allowed_variant_ids"])
        print(
            f"{item['ordinal']:02d}  {item['topic_id']}  "
            f"family={item['family_id']}  default={item['default_variant_id']}  "
            f"allowed={variants}"
        )


def _print_format_list(items: list[dict[str, Any]]) -> None:
    for item in items:
        print(f"{item['variant_id']}  family={item['family_id']}")


def _print_pack_summary(pack: dict[str, Any]) -> None:
    request = pack["request_contract"]
    profile = pack["format_profile"]
    grammar = pack["visual_grammar"]
    supports = ", ".join(grammar["support_runtime_ids"]) or "none"
    print(f"contract: {pack['contract_version']}")
    print(f"pack_id: {pack['pack_id']}")
    print(f"topic: {request['route_id']} ({request['route_source']})")
    print(f"format: {profile['variant_id']} / {profile['family_id']} ({request['format_source']})")
    print(f"primary: {grammar['primary_runtime_id']}")
    print(f"supports: {supports}")
    print("composition: deferred to the agent; audit the composed object before rendering")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.list_topics or args.list_formats:
        if args.concept is not None:
            parser.error("--concept cannot be combined with a list mode")
    elif not isinstance(args.concept, str) or not args.concept.strip():
        parser.error("--concept is required unless --list-topics or --list-formats is used")

    try:
        assets = load_runtime_assets(args.asset_dir)
        if args.list_topics:
            payload: Any = {
                "schema": "subculture-illustration-topic-list/v1",
                "topics": list_topics(assets),
            }
        elif args.list_formats:
            payload = {
                "schema": "subculture-illustration-format-list/v1",
                "formats": list_formats(assets),
            }
        else:
            payload = build_candidate_pack(
                args.concept,
                topic=args.topic,
                format_id=args.format_id,
                seed=args.seed,
                creativity=args.creativity,
                safety_evaluation=args.safety_evaluation,
                assets=assets,
            )

        if args.output_file:
            _atomic_write_json(args.output_file, payload)

        if args.json_output or args.emit_candidate_pack:
            _print_json(payload)
        elif args.list_topics:
            _print_topic_list(payload["topics"])
        elif args.list_formats:
            _print_format_list(payload["formats"])
        else:
            _print_pack_summary(payload)
        return EXIT_OK
    except IllustrationRuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.exit_code
    except OSError as exc:
        print(f"error: I/O failure: {exc}", file=sys.stderr)
        return EXIT_IO
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"error: unexpected runtime failure: {exc}", file=sys.stderr)
        return EXIT_UNEXPECTED


if __name__ == "__main__":
    raise SystemExit(main())
