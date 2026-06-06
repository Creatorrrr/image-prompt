#!/usr/bin/env python3
"""Project-local wrapper for the bundled photo prompt generator."""

from __future__ import annotations

import importlib.util
import hashlib
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
BUNDLE_OVERRIDE_SLOTS = {
    "prop",
    "action",
    "location",
    "lighting",
    "light_direction",
    "light_type",
    "light_intensity",
    "color",
    "mood",
    "composition",
    "subject_framing",
    "expression",
    "wardrobe_style",
}


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
        padded = f" {stripped} "
        needle = f" {role} "
        if needle in padded:
            name = " ".join(stripped.replace(role, " ").split())
            return role, name, dict(roles[role] or {})
    return None, stripped, {}


def match_concept_mixins(concept: str, mixins: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    stripped = concept.strip()
    matches: list[tuple[str, dict[str, Any]]] = []
    for mixin in sorted(mixins, key=len, reverse=True):
        if mixin and mixin in stripped:
            matches.append((mixin, dict(mixins[mixin] or {})))
    return matches


def concept_without_mixins(concept: str, mixin_names: Sequence[str]) -> str:
    stripped = concept
    for mixin in mixin_names:
        stripped = stripped.replace(mixin, " ")
    return " ".join(stripped.split())


def select_mixin_intensity_variant(concept: str, mixin_recipe: dict[str, Any]) -> str | None:
    variants = mixin_recipe.get("intensity_variants")
    aliases = mixin_recipe.get("intensity_aliases")
    if not isinstance(variants, dict) or not isinstance(aliases, dict):
        return None

    lowered = concept.lower()
    for variant, raw_aliases in aliases.items():
        if variant not in variants:
            continue
        if any(alias and alias.lower() in lowered for alias in normalize_list(raw_aliases)):
            return str(variant)
    return None


def split_forced_slot(raw: str) -> tuple[str, list[str]] | None:
    if "=" not in raw:
        return None
    slot, ids_raw = raw.split("=", 1)
    slot = slot.strip()
    ids = [item.strip() for item in ids_raw.replace("|", ",").split(",") if item.strip()]
    if not slot or not ids:
        return None
    return slot, ids


def set_values_to_forced(set_values: Any) -> list[str]:
    if isinstance(set_values, dict):
        forced: list[str] = []
        for slot, values in set_values.items():
            ids = normalize_list(values)
            if ids:
                forced.append(f"{slot}={','.join(ids)}")
        return forced
    return normalize_list(set_values)


def merge_forced_set_groups(set_groups: Sequence[tuple[Sequence[str], set[str]]]) -> list[str]:
    by_slot: dict[str, list[str]] = {}
    for forced_sets, override_slots in set_groups:
        parsed_forced_sets: list[tuple[str, list[str]]] = []
        for forced in forced_sets:
            parsed = split_forced_slot(forced)
            if parsed is None:
                continue
            parsed_forced_sets.append(parsed)

        cleared_slots: set[str] = set()
        for slot, ids in parsed_forced_sets:
            if slot in override_slots and slot not in cleared_slots:
                by_slot[slot] = []
                cleared_slots.add(slot)
            slot_pool = by_slot.setdefault(slot, [])
            for item_id in ids:
                if item_id not in slot_pool:
                    slot_pool.append(item_id)
    return [f"{slot}={','.join(ids)}" for slot, ids in by_slot.items()]


def merge_recipe_sets(recipes: Sequence[dict[str, Any]]) -> list[str]:
    return merge_forced_set_groups([(set_values_to_forced(recipe.get("set")), set()) for recipe in recipes])


def forced_sets_to_mapping(forced_sets: Sequence[str]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for forced in forced_sets:
        parsed = split_forced_slot(forced)
        if parsed is None:
            continue
        slot, ids = parsed
        mapping[slot] = ids
    return mapping


def forced_set_slots(forced_sets: Sequence[str]) -> set[str]:
    slots: set[str] = set()
    for forced in forced_sets:
        parsed = split_forced_slot(forced)
        if parsed is not None:
            slots.add(parsed[0])
    return slots


def select_bundle_for_mixin(
    concept: str, mixin_name: str, mixin_recipe: dict[str, Any], args: Sequence[str], role: str | None
) -> dict[str, Any] | None:
    raw_bundles = mixin_recipe.get("bundles")
    bundles = [dict(bundle) for bundle in raw_bundles if isinstance(bundle, dict)] if isinstance(raw_bundles, list) else []
    if not bundles:
        return None

    if role:
        role_bundles = [bundle for bundle in bundles if role in normalize_list(bundle.get("roles"))]
        if role_bundles:
            role_specific_bundles = [
                bundle for bundle in role_bundles if not str(bundle.get("id") or "").startswith("shared_")
            ]
            bundles = role_specific_bundles or role_bundles
    else:
        generic_bundles = [bundle for bundle in bundles if not normalize_list(bundle.get("roles"))]
        if generic_bundles:
            bundles = generic_bundles

    weights = [max(float(bundle.get("weight", 1) or 0), 0.0) for bundle in bundles]
    total = sum(weights)
    if total <= 0:
        return dict(bundles[0])

    seed = option_value(args, "--seed") or ""
    token = f"{concept}|{mixin_name}|{seed}"
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    threshold = int.from_bytes(digest[:8], "big") / 2**64 * total
    cursor = 0.0
    for bundle, weight in zip(bundles, weights):
        cursor += weight
        if threshold < cursor:
            return dict(bundle)
    return dict(bundles[-1])


def add_option(args: list[str], name: str, value: str) -> None:
    if value:
        args.extend([name, value])


def resolve_concepts(args: Sequence[str], concepts: Sequence[str]) -> tuple[list[str], list[dict[str, Any]]]:
    if not concepts:
        return list(args), []

    _, explicit_user_sets = extract_option_values(args, "--set")
    explicit_user_set_slots = forced_set_slots(explicit_user_sets)
    recipes = load_concept_recipes()
    roles = recipes.get("roles", {}) or {}
    mixins = recipes.get("mixins", {}) or {}
    resolved_args = list(args)
    explanations: list[dict[str, Any]] = []
    has_preset_value = has_option(resolved_args, "--preset")
    has_likeness_value = has_option(resolved_args, "--likeness-mode")

    for concept in concepts:
        concept = concept.strip()
        if not concept:
            continue
        mixin_matches = match_concept_mixins(concept, mixins)
        role_concept = concept_without_mixins(concept, [mixin for mixin, _ in mixin_matches])
        role, name, recipe = match_concept_role(role_concept or concept, roles)
        selected_bundles: list[dict[str, Any]] = []
        set_groups: list[tuple[Sequence[str], set[str]]] = []
        applied_recipes = [recipe] if recipe else []
        additional_requirements: list[str] = []
        intent_axes: list[str] = []

        if recipe:
            set_groups.append((set_values_to_forced(recipe.get("set")), set()))
            additional_requirements.extend(normalize_list(recipe.get("additional")))
            intent_axes.extend(normalize_list(recipe.get("intent_axis")))

        for mixin, mixin_recipe in mixin_matches:
            applied_recipes.append(mixin_recipe)
            selected_bundle = select_bundle_for_mixin(concept, mixin, mixin_recipe, args, role)
            mixin_base_set = set_values_to_forced(mixin_recipe.get("set"))
            additional_requirements.extend(normalize_list(mixin_recipe.get("additional")))
            intent_axes.extend(normalize_list(mixin_recipe.get("intent_axis")))
            intensity_variant = select_mixin_intensity_variant(concept, mixin_recipe)
            if intensity_variant:
                variants = mixin_recipe.get("intensity_variants")
                if isinstance(variants, dict):
                    additional_requirements.extend(normalize_list(variants.get(intensity_variant)))
            weapon_cues = mixin_recipe.get("weapon_cues")
            if (
                role
                and isinstance(weapon_cues, dict)
                and not (explicit_user_set_slots & {"prop", "action"})
            ):
                additional_requirements.extend(normalize_list(weapon_cues.get(role)))
            if selected_bundle:
                bundle_preset = str(selected_bundle.get("preset") or "")
                if bundle_preset and not has_preset_value:
                    add_option(resolved_args, "--preset", bundle_preset)
                    has_preset_value = True
                if mixin_base_set:
                    set_groups.append((mixin_base_set, set()))
                bundle_set = selected_bundle.get("set") if isinstance(selected_bundle.get("set"), dict) else {}
                set_groups.append((set_values_to_forced(bundle_set), BUNDLE_OVERRIDE_SLOTS))
                additional_requirements.extend(normalize_list(selected_bundle.get("additional")))
                intent_axes.extend(normalize_list(selected_bundle.get("intent_axis")))
                selected_bundles.append(
                    {
                        "mixin": mixin,
                        "bundle_id": str(selected_bundle.get("id") or ""),
                        "preset": bundle_preset,
                        "set": bundle_set,
                        "weight": selected_bundle.get("weight", 1),
                        "subtype": str(selected_bundle.get("subtype") or ""),
                    }
                )
            else:
                set_groups.append((mixin_base_set, set()))

        if role and any(bundle.get("mixin") == "암살자" for bundle in selected_bundles):
            additional_requirements.append("role outfit is a cover identity/disguise for the assassin persona")

        combined_sets = merge_forced_set_groups(set_groups)
        add_option(resolved_args, "--concept-lock", concept)

        preset = str(recipe.get("preset") or "")
        if not preset:
            preset = next(
                (str(mixin_recipe.get("preset") or "") for _, mixin_recipe in mixin_matches if mixin_recipe.get("preset")),
                "",
            )
        if preset and not has_preset_value:
            add_option(resolved_args, "--preset", preset)
            has_preset_value = True
        for forced in combined_sets:
            add_option(resolved_args, "--set", forced)
        for requirement in additional_requirements:
            add_option(resolved_args, "--additional-requirement", requirement)
        for axis in intent_axes:
            add_option(resolved_args, "--intent-axis", axis)

        likeness_mode = str(recipe.get("likeness_mode") or "")
        if not likeness_mode:
            likeness_mode = next(
                (str(mixin_recipe.get("likeness_mode") or "") for _, mixin_recipe in mixin_matches if mixin_recipe.get("likeness_mode")),
                "",
            )
        if likeness_mode and not has_likeness_value:
            add_option(resolved_args, "--likeness-mode", likeness_mode)
            has_likeness_value = True

        if not applied_recipes:
            add_option(resolved_args, "--intent-axis", concept)

        explanations.append(
            {
                "concept": concept,
                "name": name,
                "role": role,
                "applied_role": role,
                "applied_mixins": [mixin for mixin, _ in mixin_matches],
                "matched": bool(applied_recipes),
                "recipe": recipe,
                "mixins": {mixin: mixin_recipe for mixin, mixin_recipe in mixin_matches},
                "selected_bundles": selected_bundles,
                "combined_forced_slots": forced_sets_to_mapping(combined_sets),
            }
        )

    for forced in explicit_user_sets:
        add_option(resolved_args, "--set", forced)

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
