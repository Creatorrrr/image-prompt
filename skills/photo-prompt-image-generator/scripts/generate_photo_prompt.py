#!/usr/bin/env python3
"""Project-local wrapper for the bundled photo prompt generator."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]
DEFAULT_TAGS = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERATOR_PATH = Path(__file__).resolve().with_name("prompt_generator.py")
DEFAULT_SELECTION_MODE = "semantic"
DEFAULT_SEMANTIC_INTENT = (
    "photorealistic image-ready photo prompt with coherent subject, location, "
    "lighting, mood, camera, composition, texture, and format"
)


def has_option(args: Sequence[str], name: str) -> bool:
    return name in args or any(arg.startswith(name + "=") for arg in args)


def remove_flag(args: Sequence[str], name: str) -> list[str]:
    return [arg for arg in args if arg != name]


def option_value(args: Sequence[str], name: str) -> str | None:
    for index, arg in enumerate(args):
        if arg == name and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
    return None


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} or key in os.environ:
            continue
        value = value.strip().strip("\"'")
        if value:
            os.environ[key] = value


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
    selection_mode_defaulted = not has_option(args, "--selection-mode")
    intent_axis_explicit = has_option(args, "--intent-axis")
    if selection_mode_defaulted:
        args.extend(["--selection-mode", DEFAULT_SELECTION_MODE])
    selection_mode = option_value(args, "--selection-mode") or DEFAULT_SELECTION_MODE
    if selection_mode in {"semantic", "hybrid"} and not has_option(args, "--intent"):
        args.extend(["--intent", DEFAULT_SEMANTIC_INTENT])
        if not has_option(args, "--default-intent"):
            args.append("--default-intent")
        if selection_mode_defaulted and not intent_axis_explicit and not has_option(args, "--semantic-default"):
            args.append("--semantic-default")
    if not plain and not has_option(args, "--json-output"):
        args.append("--json-output")
    if not no_negative and not has_option(args, "--include-negative"):
        args.append("--include-negative")

    return args


def main(argv: Sequence[str] | None = None) -> int:
    load_project_env()
    generator = load_generator()
    return generator.main(build_forward_args(argv or sys.argv[1:]))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
