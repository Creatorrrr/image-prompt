#!/usr/bin/env python3
"""Project-local wrapper for the bundled photo prompt generator."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]
DEFAULT_TAGS = SKILL_DIR / "assets" / "photo_prompt_tags.json"
DEFAULT_CONCEPT_RECIPES = SKILL_DIR / "assets" / "concept_recipes.json"
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


def extract_option_values(args: Sequence[str], name: str) -> tuple[list[str], list[str]]:
    remaining: list[str] = []
    values: list[str] = []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == name:
            if index + 1 >= len(args):
                raise ValueError(f"{name} requires a value")
            values.append(args[index + 1])
            index += 2
            continue
        if arg.startswith(name + "="):
            values.append(arg.split("=", 1)[1])
            index += 1
            continue
        remaining.append(arg)
        index += 1
    return remaining, values


def extract_flag(args: Sequence[str], name: str) -> tuple[list[str], bool]:
    remaining: list[str] = []
    found = False
    for arg in args:
        if arg == name:
            found = True
        else:
            remaining.append(arg)
    return remaining, found


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def load_concept_recipes(path: Path = DEFAULT_CONCEPT_RECIPES) -> dict[str, Any]:
    if not path.exists():
        return {"roles": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def match_concept_role(concept: str, roles: dict[str, Any]) -> tuple[str | None, str, dict[str, Any]]:
    stripped = concept.strip()
    for role in sorted(roles, key=len, reverse=True):
        if stripped == role or stripped.endswith(role):
            name = stripped[: -len(role)].strip()
            return role, name, dict(roles[role] or {})
    return None, stripped, {}


def add_option(args: list[str], name: str, value: str) -> None:
    if value:
        args.extend([name, value])


def resolve_concepts(args: Sequence[str], concepts: Sequence[str]) -> tuple[list[str], list[dict[str, Any]]]:
    if not concepts:
        return list(args), []

    recipes = load_concept_recipes()
    roles = recipes.get("roles", {}) or {}
    resolved_args = list(args)
    explanations: list[dict[str, Any]] = []
    has_preset_value = has_option(resolved_args, "--preset")
    has_likeness_value = has_option(resolved_args, "--likeness-mode")

    for concept in concepts:
        concept = concept.strip()
        if not concept:
            continue
        role, name, recipe = match_concept_role(concept, roles)
        add_option(resolved_args, "--concept-lock", concept)

        if recipe.get("preset") and not has_preset_value:
            add_option(resolved_args, "--preset", str(recipe["preset"]))
            has_preset_value = True
        for forced in normalize_list(recipe.get("set")):
            add_option(resolved_args, "--set", forced)
        for requirement in normalize_list(recipe.get("additional")):
            add_option(resolved_args, "--additional-requirement", requirement)
        for axis in normalize_list(recipe.get("intent_axis")):
            add_option(resolved_args, "--intent-axis", axis)

        likeness_mode = str(recipe.get("likeness_mode") or "")
        if likeness_mode and not has_likeness_value:
            add_option(resolved_args, "--likeness-mode", likeness_mode)
            has_likeness_value = True

        if not recipe:
            add_option(resolved_args, "--intent-axis", concept)

        explanations.append(
            {
                "concept": concept,
                "name": name,
                "role": role,
                "matched": bool(recipe),
                "recipe": recipe,
            }
        )

    return resolved_args, explanations


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
    args, concepts = extract_option_values(args, "--concept")
    args, _ = extract_flag(args, "--explain-concept")
    args, _ = resolve_concepts(args, concepts)

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
    raw_args = list(argv or sys.argv[1:])
    concept_args, concepts = extract_option_values(raw_args, "--concept")
    _, explain_concept = extract_flag(concept_args, "--explain-concept")
    if explain_concept:
        forward_args = build_forward_args(raw_args)
        _, explanations = resolve_concepts(extract_flag(concept_args, "--explain-concept")[0], concepts)
        print(json.dumps({"concepts": explanations, "forward_args": forward_args}, ensure_ascii=False, indent=2))
        return 0
    generator = load_generator()
    return generator.main(build_forward_args(raw_args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
