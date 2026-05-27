#!/usr/bin/env python3
"""Project-local wrapper for the bundled photo prompt generator."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TAGS = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERATOR_PATH = Path(__file__).resolve().with_name("prompt_generator.py")


def has_option(args: Sequence[str], name: str) -> bool:
    return name in args or any(arg.startswith(name + "=") for arg in args)


def remove_flag(args: Sequence[str], name: str) -> list[str]:
    return [arg for arg in args if arg != name]


def load_generator():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_forward_args(argv: Sequence[str]) -> list[str]:
    args = list(argv)

    plain = "--plain" in args
    no_negative = "--no-negative" in args
    args = remove_flag(remove_flag(args, "--plain"), "--no-negative")

    if not has_option(args, "--tags"):
        args[:0] = ["--tags", str(DEFAULT_TAGS)]
    if not has_option(args, "--n"):
        args.extend(["--n", "1"])
    if not has_option(args, "--lang"):
        args.extend(["--lang", "both"])
    if not has_option(args, "--detail-level"):
        args.extend(["--detail-level", "detailed"])
    if not plain and not has_option(args, "--json-output"):
        args.append("--json-output")
    if not no_negative and not has_option(args, "--include-negative"):
        args.append("--include-negative")

    return args


def main(argv: Sequence[str] | None = None) -> int:
    generator = load_generator()
    return generator.main(build_forward_args(argv or sys.argv[1:]))


if __name__ == "__main__":
    raise SystemExit(main())
