#!/usr/bin/env python3
"""Project-local wrapper for the bundled photo prompt generator."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import re
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
CONCEPT_MODES = {"legacy", "soft"}
SAFETY_EVALUATION_FLAG = "--safety-evaluation"
SAFETY_TRANSFORM_TEXT_TOKENS = (
    "adult",
    "sexual",
    "fetish",
    "lingerie",
    "nudity",
    "nude",
    "gore",
    "blood",
    "wound",
    "injury",
    "weapon",
    "violence",
    "coercion",
    "victim",
    "avoid",
    "no ",
    "non-graphic",
    "nonsexualized",
    "covered",
    "readable text",
    "unreadable",
)
DEFAULT_SOFT_ANCHOR_SLOTS = {
    "appearance_type",
    "costume_style",
    "expression",
    "location",
    "prop",
    "wardrobe_style",
}
DEFAULT_SOFT_FREE_SLOTS = {
    "camera_direction",
    "camera_type",
    "color",
    "composition",
    "film_emulation",
    "focus",
    "format",
    "genre",
    "lens",
    "light_direction",
    "light_intensity",
    "light_shape",
    "light_type",
    "lighting",
    "medium",
    "mood",
    "motion",
    "quality",
    "texture",
    "time_of_day",
    "weather",
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
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def normalize_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def recipe_soft_anchor_slots(recipes: dict[str, Any], recipe: dict[str, Any]) -> set[str]:
    explicit = set(normalize_list(recipe.get("soft_anchor_slots")))
    if explicit:
        return explicit
    defaults = recipes.get("soft_anchor_defaults", {}) if isinstance(recipes, dict) else {}
    if isinstance(defaults, dict):
        configured = set(normalize_list(defaults.get("anchor_slots")))
        if configured:
            return configured
    return set(DEFAULT_SOFT_ANCHOR_SLOTS)


def recipe_soft_free_slots(recipes: dict[str, Any], recipe: dict[str, Any]) -> set[str]:
    explicit = set(normalize_list(recipe.get("soft_free_slots")))
    if explicit:
        return explicit
    defaults = recipes.get("soft_anchor_defaults", {}) if isinstance(recipes, dict) else {}
    if isinstance(defaults, dict):
        configured = set(normalize_list(defaults.get("free_slots")))
        if configured:
            return configured
    return set(DEFAULT_SOFT_FREE_SLOTS)


def fallback_anchor_terms(slot: str, ids: Sequence[str]) -> list[str]:
    slot_terms = [token for token in re_split_identifier(slot) if token not in {"style", "type"}]
    id_terms: list[str] = []
    for item_id in ids:
        for token in re_split_identifier(item_id):
            if token in {"costume", "style", "set", "prop", "portrait"}:
                continue
            id_terms.append(token)
    seen: set[str] = set()
    terms: list[str] = []
    for term in [*slot_terms, *id_terms]:
        if term and term not in seen:
            seen.add(term)
            terms.append(term)
    return terms[:6]


def re_split_identifier(value: str) -> list[str]:
    return [token for token in re.split(r"[^A-Za-z0-9가-힣]+", str(value).lower()) if token]


def anchor_terms_for_slot(recipe: dict[str, Any], slot: str, ids: Sequence[str]) -> list[str]:
    configured = recipe.get("anchor_terms")
    if isinstance(configured, dict):
        terms = normalize_list(configured.get(slot))
        if terms:
            return terms
    return fallback_anchor_terms(slot, ids)


def normalize_weighted_pool(raw: Any) -> tuple[list[str], dict[str, float]]:
    """Normalize a pool that may mix plain id strings and {"id", "w"} objects."""
    ids: list[str] = []
    weights: dict[str, float] = {}
    if not isinstance(raw, list):
        raw = normalize_list(raw)
    for item in raw:
        if isinstance(item, dict):
            item_id = str(item.get("id") or "").strip()
            if not item_id:
                continue
            ids.append(item_id)
            try:
                weight = float(item.get("w", 1.0))
            except (TypeError, ValueError):
                weight = 1.0
            if weight > 0 and weight != 1.0:
                weights[item_id] = weight
        else:
            item_id = str(item).strip()
            if item_id:
                ids.append(item_id)
    return ids, weights


def anchor_pool_for_slot(recipe: dict[str, Any], slot: str, ids: Sequence[str]) -> list[str]:
    configured = recipe.get("anchor_pool")
    if isinstance(configured, dict):
        pool, _weights = normalize_weighted_pool(configured.get(slot))
        if pool:
            return pool
    return [str(item_id) for item_id in ids if str(item_id).strip()]


def anchor_pool_weights_for_slot(recipe: dict[str, Any], slot: str) -> dict[str, float]:
    configured = recipe.get("anchor_pool")
    if isinstance(configured, dict):
        _pool, weights = normalize_weighted_pool(configured.get(slot))
        return weights
    return {}


def primary_anchor_pool_for_slot(recipe: dict[str, Any], slot: str) -> list[str]:
    configured = recipe.get("primary_anchor_pool")
    if isinstance(configured, dict):
        pool, _weights = normalize_weighted_pool(configured.get(slot))
        return pool
    return []


def primary_anchor_pool_weights_for_slot(recipe: dict[str, Any], slot: str) -> dict[str, float]:
    configured = recipe.get("primary_anchor_pool")
    if isinstance(configured, dict):
        _pool, weights = normalize_weighted_pool(configured.get(slot))
        return weights
    return {}


def anchor_variant_for_slot(recipe: dict[str, Any], slot: str) -> dict[str, Any]:
    configured = recipe.get("anchor_variants")
    if not isinstance(configured, dict):
        return {}
    variant = configured.get(slot)
    return variant if isinstance(variant, dict) else {}


def critical_anchor_slots_for_recipe(recipe: dict[str, Any]) -> set[str]:
    return set(normalize_list(recipe.get("critical_anchor_slots")))


def default_anchor_groups(source: str, primary: bool = False) -> list[str]:
    groups: list[str] = []
    if source == "role":
        groups.append("role_primary")
    if source in {"mixin", "bundle"} and primary:
        groups.append("mixin_primary")
    return groups


def anchor_groups_for_slot(recipe: dict[str, Any], source: str, slot: str, primary: bool = False) -> list[str]:
    configured = recipe.get("anchor_groups")
    groups: list[str] = []
    if isinstance(configured, dict):
        groups.extend(normalize_list(configured.get(slot)))
    groups.extend(group for group in default_anchor_groups(source, primary=primary) if group not in groups)
    return groups


def anchor_floor_for_recipe(recipe: dict[str, Any]) -> dict[str, int]:
    floors = recipe.get("anchor_floor") or {}
    if not isinstance(floors, dict):
        return {}
    normalized: dict[str, int] = {}
    for source, value in floors.items():
        number = normalize_int(value, 0)
        if number > 0:
            normalized[str(source)] = number
    return normalized


def anchor_group_floor_for_recipe(recipe: dict[str, Any]) -> dict[str, int]:
    floors = recipe.get("anchor_group_floor") or {}
    if not isinstance(floors, dict):
        return {}
    normalized: dict[str, int] = {}
    for group, value in floors.items():
        number = normalize_int(value, 0)
        if number > 0:
            normalized[str(group)] = number
    return normalized


def visual_guards_for_recipe(recipe: dict[str, Any]) -> list[dict[str, Any]]:
    raw = recipe.get("visual_guard")
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        return [guard for guard in raw if isinstance(guard, dict)]
    return []


def free_slot_constraints_for_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    raw = recipe.get("free_slot_constraints")
    return raw if isinstance(raw, dict) else {}


def render_suppress_terms_for_recipe(recipe: dict[str, Any]) -> list[str]:
    return normalize_list(recipe.get("render_suppress_terms"))


def render_directives_for_recipe(recipe: dict[str, Any]) -> list[dict[str, Any]]:
    raw = recipe.get("render_directives")
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    directives: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        cue_terms = normalize_list(item.get("cue_terms"))
        positive_clause = str(item.get("positive_clause") or "").strip()
        if not cue_terms or not positive_clause:
            continue
        directives.append(
            {
                "id": str(item.get("id") or f"render_directive_{index}"),
                "cue_terms": cue_terms,
                "render_as": str(item.get("render_as") or ""),
                "positive_clause": positive_clause,
                "suppress_terms": normalize_list(item.get("suppress_terms")),
            }
        )
    return directives


def dual_read_requirement_for_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    raw = recipe.get("dual_read_requirement")
    return raw if isinstance(raw, dict) else {}


def preset_affinity_for_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    raw = recipe.get("preset_affinity")
    return raw if isinstance(raw, dict) else {}


def role_scene_policy_for_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    raw = recipe.get("role_scene_policy")
    if not isinstance(raw, dict):
        return {}
    policy: dict[str, Any] = {}
    for key in (
        "allowed_locations",
        "preferred_locations",
        "forbidden_locations",
        "discouraged_generic_locations",
        "discouraged_generic_moods",
        "support_presets",
        "discouraged_presets",
    ):
        values = normalize_list(raw.get(key))
        if values:
            policy[key] = values
    for key in ("enabled", "enforce", "role_first", "generic_preset_support_only_when_role_scene_missing"):
        if key in raw:
            policy[key] = bool(raw.get(key))
    for key in ("scene_family", "reason"):
        value = str(raw.get(key) or "").strip()
        if value:
            policy[key] = value
    if policy and "enabled" not in policy:
        policy["enabled"] = True
    return policy


def soft_repair_policy_for_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    raw = recipe.get("soft_repair_policy")
    return raw if isinstance(raw, dict) else {}


def safety_negative_floor_for_recipe(recipe: dict[str, Any]) -> list[str]:
    return normalize_list(recipe.get("safety_negative_floor"))


def mixin_cue_budget_for_recipe(recipe: dict[str, Any]) -> int:
    value = normalize_int(recipe.get("mixin_cue_budget"), 0)
    return max(0, value)


def render_priority_terms_for_recipe(recipe: dict[str, Any]) -> list[dict[str, Any]]:
    raw = recipe.get("render_priority_terms")
    groups: list[dict[str, Any]] = []
    if isinstance(raw, dict):
        raw = [raw]
    if isinstance(raw, list):
        for index, item in enumerate(raw):
            if isinstance(item, dict):
                terms = normalize_list(item.get("terms"))
                min_hits = max(1, normalize_int(item.get("min_hits"), 1))
                if terms:
                    groups.append(
                        {
                            "id": str(item.get("id") or f"priority_{index}"),
                            "group": str(item.get("group") or item.get("id") or f"priority_{index}"),
                            "tier": str(item.get("tier") or "required"),
                            "terms": terms,
                            "min_hits": min_hits,
                            "target_slots": normalize_list(item.get("target_slots")),
                        }
                    )
            else:
                terms = normalize_list(item)
                if terms:
                    groups.append({"id": f"priority_{index}", "terms": terms, "min_hits": 1})
    elif isinstance(raw, str):
        groups.append({"id": "priority_0", "terms": [raw], "min_hits": 1})
    return groups


def soft_safety_requirements_for_recipe(recipe: dict[str, Any]) -> list[str]:
    return normalize_list(recipe.get("safety_requirements"))


def is_safety_transform_text(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in SAFETY_TRANSFORM_TEXT_TOKENS)


def safety_transform_items_for_recipe(label: str, recipe: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    def append(field: str, values: Any) -> None:
        if isinstance(values, dict):
            if values:
                items.append({"source": label, "field": field, "kind": "object"})
            return
        normalized = normalize_list(values)
        if normalized:
            items.append({"source": label, "field": field, "items": normalized})

    append("safety_requirements", recipe.get("safety_requirements"))
    safety_additional = [
        item for item in normalize_list(recipe.get("additional")) if is_safety_transform_text(item)
    ]
    append("additional", safety_additional)
    append("safety_negative_floor", recipe.get("safety_negative_floor"))
    append("render_suppress_terms", recipe.get("render_suppress_terms"))
    append("render_directives", recipe.get("render_directives"))
    append("visual_guard", recipe.get("visual_guard"))
    append("free_slot_constraints", recipe.get("free_slot_constraints"))
    soft_repair_policy = recipe.get("soft_repair_policy")
    if isinstance(soft_repair_policy, dict) and soft_repair_policy.get("enabled"):
        items.append({"source": label, "field": "soft_repair_policy", "kind": "object"})
    return items


def safety_evaluation_payload(
    items: Sequence[dict[str, Any]],
    *,
    requested: bool,
) -> dict[str, Any]:
    unique_items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        unique_items.append(item)
    evaluated_items = [
        {
            **item,
            "status": "pass",
            "finding": "declarative prompt transform retained",
        }
        for item in unique_items
    ]
    return {
        "mode": "explicit_evaluation" if requested else "automatic",
        "evaluation_requested": requested,
        "status": "pass",
        "requires_user_approval": False,
        "items": evaluated_items if requested else [],
    }


def soft_salience_cues_for_recipe(recipe: dict[str, Any]) -> list[str]:
    return normalize_list(recipe.get("salience_cues"))


def soft_min_anchors_for_recipe(recipe: dict[str, Any], default: int) -> int:
    value = normalize_int(recipe.get("soft_min_anchors"), default)
    return max(0, value)


def normalize_recipe_identity_axes(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        raw = raw.get("required") or raw.get("axes") or []
    if not isinstance(raw, list):
        raw = normalize_list(raw)
    axes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw:
        if isinstance(item, dict):
            axis_id = str(item.get("id") or item.get("axis") or "").strip()
            if not axis_id:
                continue
            axis = {
                "id": axis_id,
                "terms": normalize_list(item.get("terms")),
                "description": str(item.get("description") or "").strip(),
            }
        else:
            axis_id = str(item or "").strip()
            if not axis_id:
                continue
            axis = {"id": axis_id, "terms": [], "description": ""}
        if axis_id in seen:
            continue
        seen.add(axis_id)
        axes.append(axis)
    return axes


def normalize_recipe_motif_pools(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    pools: dict[str, Any] = {}
    for motif, pool in raw.items():
        motif_id = str(motif or "").strip()
        if not motif_id or not isinstance(pool, dict):
            continue
        normalized: dict[str, Any] = {
            "axis": str(pool.get("axis") or "").strip(),
            "bucket": str(pool.get("bucket") or "").strip(),
            "terms": normalize_list(pool.get("terms")),
        }
        slot_candidates = pool.get("slot_candidates")
        if isinstance(slot_candidates, dict):
            normalized["slot_candidates"] = {
                str(slot): normalize_list(ids)
                for slot, ids in slot_candidates.items()
                if normalize_list(ids)
            }
        exemplars = normalize_list(pool.get("exemplars"))
        if exemplars:
            normalized["exemplars"] = exemplars
        pools[motif_id] = {key: value for key, value in normalized.items() if value}
    return pools


def normalize_recipe_motif_quotas(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    quotas: dict[str, Any] = {}
    for motif, quota in raw.items():
        motif_id = str(motif or "").strip()
        if not motif_id:
            continue
        if isinstance(quota, dict):
            normalized: dict[str, Any] = {}
            for key in ("max_batch_share", "max_recent_share"):
                if key in quota:
                    try:
                        normalized[key] = max(0.0, min(1.0, float(quota.get(key))))
                    except (TypeError, ValueError):
                        pass
            for key in ("max_batch_uses", "max_recent_uses"):
                if key in quota:
                    try:
                        value = int(quota.get(key))
                    except (TypeError, ValueError):
                        continue
                    if value >= 0:
                        normalized[key] = value
            if quota.get("avoid_when_pressure"):
                normalized["avoid_when_pressure"] = True
            if normalized:
                quotas[motif_id] = normalized
        else:
            try:
                quotas[motif_id] = {"max_batch_share": max(0.0, min(1.0, float(quota)))}
            except (TypeError, ValueError):
                continue
    return quotas


def normalize_recipe_semantic_dropout(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    normalized: dict[str, Any] = {"enabled": bool(raw.get("enabled", True))}
    buckets = normalize_list(raw.get("maskable_buckets"))
    if buckets:
        normalized["maskable_buckets"] = buckets
    for key in ("min_buckets", "max_buckets"):
        if key in raw:
            normalized[key] = max(0, normalize_int(raw.get(key), 0))
    if "probability" in raw:
        try:
            normalized["probability"] = max(0.0, min(1.0, float(raw.get("probability"))))
        except (TypeError, ValueError):
            normalized["probability"] = 0.0
    return normalized


def normalize_recipe_exemplar_set(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        normalized: dict[str, Any] = {}
        for key, value in raw.items():
            values = normalize_list(value)
            if values:
                normalized[str(key)] = values
        return normalized
    values = normalize_list(raw)
    return {"examples": values} if values else {}


def apply_reference_scaffold_fields(spec: dict[str, Any], recipes: Sequence[dict[str, Any]]) -> dict[str, Any]:
    identity_axes: list[dict[str, Any]] = []
    seen_axes: set[str] = set()
    motif_pools: dict[str, Any] = {}
    motif_quotas: dict[str, Any] = {}
    semantic_dropout: dict[str, Any] = {}
    exemplar_set: dict[str, Any] = {}
    for recipe in recipes:
        if not isinstance(recipe, dict):
            continue
        for axis in normalize_recipe_identity_axes(recipe.get("identity_axes")):
            axis_id = str(axis.get("id") or "")
            if axis_id and axis_id not in seen_axes:
                identity_axes.append(axis)
                seen_axes.add(axis_id)
        motif_pools.update(normalize_recipe_motif_pools(recipe.get("motif_pools")))
        motif_quotas.update(normalize_recipe_motif_quotas(recipe.get("motif_quotas")))
        semantic_dropout.update(normalize_recipe_semantic_dropout(recipe.get("semantic_dropout")))
        exemplar_set.update(normalize_recipe_exemplar_set(recipe.get("exemplar_set")))
    if identity_axes:
        spec["identity_axes"] = identity_axes
    if motif_pools:
        spec["motif_pools"] = motif_pools
    if motif_quotas:
        spec["motif_quotas"] = motif_quotas
    if semantic_dropout:
        spec["semantic_dropout"] = semantic_dropout
    if exemplar_set:
        spec["exemplar_set"] = exemplar_set
    return spec


def soft_anchor_specs_from_mapping(
    recipes: dict[str, Any],
    mapping: dict[str, list[str]],
    recipe: dict[str, Any],
    source: str,
    explicit_user_set_slots: set[str],
    local_pool_slots: set[str] | None = None,
    atomic_group: str = "",
) -> list[dict[str, Any]]:
    local_pool_slots = local_pool_slots or set()
    anchor_slots = recipe_soft_anchor_slots(recipes, recipe)
    free_slots = recipe_soft_free_slots(recipes, recipe)
    critical_slots = critical_anchor_slots_for_recipe(recipe)
    floors = anchor_floor_for_recipe(recipe)
    group_floors = anchor_group_floor_for_recipe(recipe)
    visual_guards = visual_guards_for_recipe(recipe)
    render_priority_terms = render_priority_terms_for_recipe(recipe)
    free_slot_constraints = free_slot_constraints_for_recipe(recipe)
    render_suppress_terms = render_suppress_terms_for_recipe(recipe)
    render_directives = render_directives_for_recipe(recipe)
    dual_read_requirement = dual_read_requirement_for_recipe(recipe)
    preset_affinity = preset_affinity_for_recipe(recipe)
    role_scene_policy = role_scene_policy_for_recipe(recipe)
    role_scene_locations = set(normalize_list(role_scene_policy.get("allowed_locations")))
    role_scene_locations.update(normalize_list(role_scene_policy.get("preferred_locations")))
    role_scene_group = ""
    if role_scene_policy.get("enabled") and role_scene_locations:
        role_scene_group = "role_scene:" + str(role_scene_policy.get("scene_family") or source)
    soft_repair_policy = soft_repair_policy_for_recipe(recipe)
    safety_negative_floor = safety_negative_floor_for_recipe(recipe)
    mixin_cue_budget = mixin_cue_budget_for_recipe(recipe)
    specs: list[dict[str, Any]] = []
    mapped_slots: set[str] = set()
    for slot, ids in sorted(mapping.items()):
        if slot in explicit_user_set_slots:
            continue
        if slot in free_slots and slot not in anchor_slots:
            continue
        if slot not in anchor_slots:
            continue
        clean_ids = [str(item_id) for item_id in ids if str(item_id).strip()]
        if not clean_ids:
            continue
        mapped_slots.add(slot)
        variant = anchor_variant_for_slot(recipe, slot)
        variant_options = normalize_list(variant.get("options")) if variant else []
        variant_group = str(variant.get("group") or "") if variant else ""
        primary_pool = primary_anchor_pool_for_slot(recipe, slot)
        if slot in local_pool_slots:
            pool = clean_ids
        else:
            pool = primary_pool or variant_options or anchor_pool_for_slot(recipe, slot, clean_ids)
        if slot in local_pool_slots:
            pool_weights = {}
        elif primary_pool:
            pool_weights = primary_anchor_pool_weights_for_slot(recipe, slot)
        elif variant_options:
            pool_weights = {}
        else:
            pool_weights = anchor_pool_weights_for_slot(recipe, slot)
        pool_weights = {item_id: weight for item_id, weight in pool_weights.items() if item_id in pool}
        effective_variant_group = atomic_group if slot in local_pool_slots and atomic_group else variant_group
        effective_variant_strategy = (
            "atomic_scene"
            if slot in local_pool_slots and atomic_group
            else (str(variant.get("select") or "") if variant else "")
        )
        if slot == "location" and role_scene_group and set(pool) & role_scene_locations:
            effective_variant_group = role_scene_group
            effective_variant_strategy = "role_scene_rotation"
        specs.append(
            {
                "slot": slot,
                "ids": clean_ids,
                "pool": pool,
                "pool_weights": pool_weights,
                "terms": anchor_terms_for_slot(recipe, slot, clean_ids),
                "source": source,
                "required": True,
                "critical": slot in critical_slots,
                "source_floors": floors,
                "groups": anchor_groups_for_slot(recipe, source, slot, primary=bool(primary_pool)),
                "primary": bool(primary_pool),
                "variant_group": effective_variant_group,
                "variant_strategy": effective_variant_strategy,
                "group_floors": group_floors,
                "visual_guards": visual_guards,
                "render_priority_terms": render_priority_terms,
                "free_slot_constraints": free_slot_constraints,
                "render_suppress_terms": render_suppress_terms,
                "render_directives": render_directives,
                "dual_read_requirement": dual_read_requirement,
                "preset_affinity": preset_affinity,
                "role_scene_policy": role_scene_policy,
                "soft_repair_policy": soft_repair_policy,
                "safety_negative_floor": safety_negative_floor,
                "mixin_cue_budget": mixin_cue_budget,
            }
        )
    primary_pool = recipe.get("primary_anchor_pool")
    if isinstance(primary_pool, dict):
        for slot, ids in sorted(primary_pool.items()):
            if slot in mapped_slots or slot in explicit_user_set_slots:
                continue
            if slot in free_slots and slot not in anchor_slots:
                continue
            if slot not in anchor_slots:
                continue
            clean_ids, clean_weights = normalize_weighted_pool(ids)
            if not clean_ids:
                continue
            variant = anchor_variant_for_slot(recipe, slot)
            variant_group = str(variant.get("group") or "") if variant else ""
            effective_variant_group = variant_group
            effective_variant_strategy = str(variant.get("select") or "") if variant else ""
            if slot == "location" and role_scene_group and set(clean_ids) & role_scene_locations:
                effective_variant_group = role_scene_group
                effective_variant_strategy = "role_scene_rotation"
            specs.append(
                {
                    "slot": slot,
                    "ids": clean_ids,
                    "pool": clean_ids,
                    "pool_weights": clean_weights,
                    "terms": anchor_terms_for_slot(recipe, slot, clean_ids),
                    "source": source,
                    "required": True,
                    "critical": slot in critical_slots,
                    "source_floors": floors,
                    "groups": anchor_groups_for_slot(recipe, source, slot, primary=True),
                    "primary": True,
                    "variant_group": effective_variant_group,
                    "variant_strategy": effective_variant_strategy,
                    "group_floors": group_floors,
                    "visual_guards": visual_guards,
                    "render_priority_terms": render_priority_terms,
                    "free_slot_constraints": free_slot_constraints,
                    "render_suppress_terms": render_suppress_terms,
                    "render_directives": render_directives,
                    "dual_read_requirement": dual_read_requirement,
                    "preset_affinity": preset_affinity,
                    "role_scene_policy": role_scene_policy,
                    "soft_repair_policy": soft_repair_policy,
                    "safety_negative_floor": safety_negative_floor,
                    "mixin_cue_budget": mixin_cue_budget,
                }
            )
    return specs


def merge_role_scene_policy(target: dict[str, Any], policy: dict[str, Any]) -> None:
    if not isinstance(policy, dict) or not policy:
        return
    target["enabled"] = bool(target.get("enabled") or policy.get("enabled", True))
    for key in (
        "allowed_locations",
        "preferred_locations",
        "forbidden_locations",
        "discouraged_generic_locations",
        "discouraged_generic_moods",
        "support_presets",
        "discouraged_presets",
    ):
        values = normalize_list(policy.get(key))
        if not values:
            continue
        bucket = target.setdefault(key, [])
        for value in values:
            if value not in bucket:
                bucket.append(value)
    for key in ("enforce", "role_first", "generic_preset_support_only_when_role_scene_missing"):
        if key in policy:
            target[key] = bool(target.get(key) or policy.get(key))
    for key in ("scene_family", "reason"):
        value = str(policy.get(key) or "").strip()
        if value and not target.get(key):
            target[key] = value


def merge_species_family_policy(target: dict[str, Any], policy: dict[str, Any]) -> None:
    if not isinstance(policy, dict) or not policy:
        return
    target["enabled"] = bool(target.get("enabled") or policy.get("enabled", True))
    for key in ("family", "variant_id", "mixin", "tier"):
        value = str(policy.get(key) or "").strip()
        if value and not target.get(key):
            target[key] = value
    for key in ("enforce", "hybrid_allowed"):
        if key in policy:
            target[key] = bool(target.get(key) or policy.get(key))
    raw_allowed = policy.get("allowed")
    if isinstance(raw_allowed, dict):
        allowed = target.setdefault("allowed", {})
        for slot, ids in raw_allowed.items():
            values = normalize_list(ids)
            if not values:
                continue
            bucket = allowed.setdefault(str(slot), [])
            for value in values:
                if value not in bucket:
                    bucket.append(value)


def dedupe_soft_anchor_specs(specs: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, bool, str, tuple[str, ...], bool], dict[str, Any]] = {}
    critical_slots = {str(spec.get("slot") or "") for spec in specs if spec.get("critical")}
    for spec in specs:
        slot = str(spec.get("slot") or "")
        ids = normalize_list(spec.get("ids"))
        if not slot or not ids:
            continue
        critical = bool(spec.get("critical"))
        if slot in critical_slots and not critical:
            continue
        source = str(spec.get("source") or "")
        groups_key = tuple(sorted(normalize_list(spec.get("groups"))))
        primary = bool(spec.get("primary", False))
        key = (slot, critical, source, groups_key, primary)
        current = by_key.setdefault(
            key,
            {
                "slot": slot,
                "ids": [],
                "pool": [],
                "pool_weights": {},
                "terms": [],
                "source": [],
                "required": False,
                "critical": critical,
                "source_floors": {},
                "groups": [],
                "primary": primary,
                "variant_group": "",
                "variant_strategy": "",
                "group_floors": {},
                "visual_guards": [],
                "render_priority_terms": [],
                "free_slot_constraints": {},
                "render_suppress_terms": [],
                "render_directives": [],
                "dual_read_requirement": {},
                "preset_affinity": {},
                "role_scene_policy": {},
                "species_family_policy": {},
                "soft_repair_policy": {},
                "safety_negative_floor": [],
                "mixin_cue_budget": 0,
            },
        )
        for item_id in ids:
            if item_id not in current["ids"]:
                current["ids"].append(item_id)
        for item_id in normalize_list(spec.get("pool")) or ids:
            if item_id not in current["pool"]:
                current["pool"].append(item_id)
        for item_id, weight in (spec.get("pool_weights") or {}).items():
            try:
                value = float(weight)
            except (TypeError, ValueError):
                continue
            if value > 0:
                current["pool_weights"][str(item_id)] = max(
                    value, float(current["pool_weights"].get(str(item_id), 0.0))
                )
        for term in normalize_list(spec.get("terms")):
            if term not in current["terms"]:
                current["terms"].append(term)
        if source and source not in current["source"]:
            current["source"].append(source)
        current["required"] = bool(current["required"] or spec.get("required", True))
        current["primary"] = bool(current["primary"] or primary)
        if not current["variant_group"] and str(spec.get("variant_group") or ""):
            current["variant_group"] = str(spec.get("variant_group") or "")
        if not current["variant_strategy"] and str(spec.get("variant_strategy") or ""):
            current["variant_strategy"] = str(spec.get("variant_strategy") or "")
        for group in normalize_list(spec.get("groups")):
            if group not in current["groups"]:
                current["groups"].append(group)
        for floor_source, value in (spec.get("source_floors", {}) or {}).items():
            current["source_floors"][floor_source] = max(
                normalize_int(current["source_floors"].get(floor_source), 0),
                normalize_int(value, 0),
            )
        for group, value in (spec.get("group_floors", {}) or {}).items():
            current["group_floors"][group] = max(
                normalize_int(current["group_floors"].get(group), 0),
                normalize_int(value, 0),
            )
        for guard in spec.get("visual_guards", []) or []:
            if guard not in current["visual_guards"]:
                current["visual_guards"].append(guard)
        for group in spec.get("render_priority_terms", []) or []:
            if group not in current["render_priority_terms"]:
                current["render_priority_terms"].append(group)
        for slot, constraint in (spec.get("free_slot_constraints", {}) or {}).items():
            if isinstance(constraint, dict):
                current["free_slot_constraints"].setdefault(slot, {}).update(constraint)
        for term in normalize_list(spec.get("render_suppress_terms")):
            if term not in current["render_suppress_terms"]:
                current["render_suppress_terms"].append(term)
        for directive in spec.get("render_directives", []) or []:
            current.setdefault("render_directives", [])
            if directive not in current["render_directives"]:
                current["render_directives"].append(directive)
        if spec.get("dual_read_requirement"):
            current["dual_read_requirement"].update(spec.get("dual_read_requirement") or {})
        if spec.get("preset_affinity"):
            current["preset_affinity"].update(spec.get("preset_affinity") or {})
        if spec.get("role_scene_policy"):
            merge_role_scene_policy(current.setdefault("role_scene_policy", {}), spec.get("role_scene_policy") or {})
        if spec.get("species_family_policy"):
            merge_species_family_policy(
                current.setdefault("species_family_policy", {}),
                spec.get("species_family_policy") or {},
            )
        if spec.get("soft_repair_policy"):
            current.setdefault("soft_repair_policy", {}).update(spec.get("soft_repair_policy") or {})
        for term in normalize_list(spec.get("safety_negative_floor")):
            if term not in current.setdefault("safety_negative_floor", []):
                current["safety_negative_floor"].append(term)
        current["mixin_cue_budget"] = max(
            normalize_int(current.get("mixin_cue_budget"), 0),
            normalize_int(spec.get("mixin_cue_budget"), 0),
        )
    normalized = []
    for spec in by_key.values():
        item = dict(spec)
        item["source"] = "+".join(item["source"]) if item["source"] else "recipe"
        item["source_floors"] = {key: value for key, value in item["source_floors"].items() if value > 0}
        normalized.append(item)
    return sorted(normalized, key=lambda item: item["slot"])


def collect_concept_guides(applied: Sequence[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    guides: dict[str, Any] = {}
    for name, recipe in applied:
        guide = recipe.get("guide")
        if isinstance(guide, dict) and guide:
            guides[name] = guide
    return guides


def collect_review_gates(applied: Sequence[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for name, recipe in applied:
        raw = recipe.get("review_gates")
        if not isinstance(raw, list):
            continue
        for gate in raw:
            if isinstance(gate, dict):
                merged = dict(gate)
                merged.setdefault("source", name)
                gates.append(merged)
    return gates


def evaluate_gate_assert(
    spec: dict[str, Any],
    explanation: dict[str, Any],
    role_recipe: dict[str, Any] | None,
) -> tuple[bool, str]:
    kind = str(spec.get("type") or "")
    forced = explanation.get("combined_forced_slots") or {}
    applied_mixins = list(explanation.get("applied_mixins") or [])
    role = str(explanation.get("role") or "")

    if kind == "mixin_shape":
        mixin = str(spec.get("mixin") or "")
        allowed = {mixin, *normalize_list(spec.get("allow_additional"))}
        if mixin not in applied_mixins or any(item not in allowed for item in applied_mixins):
            return False, (
                f"applied_mixins={applied_mixins}, expected '{mixin}' with only allowed additions "
                f"{sorted(allowed - {mixin})}"
            )
        if len(applied_mixins) != len(set(applied_mixins)):
            return False, f"applied_mixins contains duplicates: {applied_mixins}"
        detail = f"applied_mixins accepted {applied_mixins}"
        return True, detail + (f" with role {role}" if role else " standalone")

    if kind == "forced_slot_any":
        slot = str(spec.get("slot") or "")
        values = set(normalize_list(spec.get("any_of")))
        forced_values = set(normalize_list(forced.get(slot)))
        if not forced_values:
            return False, f"slot {slot} is not forced"
        if values and not (forced_values & values):
            return False, f"slot {slot} forced to {sorted(forced_values)}, expected one of {sorted(values)}"
        return True, f"slot {slot} forced to {sorted(forced_values)}"

    if kind == "forced_slot_absent":
        slot = str(spec.get("slot") or "")
        values = set(normalize_list(spec.get("values")))
        forced_values = set(normalize_list(forced.get(slot)))
        hits = forced_values & values if values else forced_values
        if hits:
            return False, f"slot {slot} unexpectedly forced to {sorted(hits)}"
        return True, f"slot {slot} clear"

    if kind == "bundle_selected":
        mixin = str(spec.get("mixin") or "")
        bundles = explanation.get("selected_bundles") or []
        for bundle in bundles:
            if str(bundle.get("mixin")) == mixin and str(bundle.get("bundle_id") or ""):
                return True, f"bundle {bundle.get('bundle_id')} selected for {mixin}"
        return False, f"no bundle selected for {mixin}"

    if kind == "role_costume_preserved":
        if not role or not role_recipe:
            return True, "no role applied (not applicable)"
        role_mapping = forced_sets_to_mapping(set_values_to_forced(role_recipe.get("set")))
        bundle_mappings = [
            forced_sets_to_mapping(set_values_to_forced(bundle.get("set")))
            for bundle in explanation.get("selected_bundles") or []
            if isinstance(bundle, dict)
        ]
        for slot in ("costume_style", "wardrobe_style"):
            role_values = set(normalize_list(role_mapping.get(slot)))
            if not role_values:
                continue
            forced_values = set(normalize_list(forced.get(slot)))
            authorized_values = set(role_values)
            for bundle_mapping in bundle_mappings:
                authorized_values.update(normalize_list(bundle_mapping.get(slot)))
            if not forced_values:
                return False, f"slot {slot} is not forced; expected role or selected-bundle wardrobe"
            if not (forced_values & authorized_values):
                return False, (
                    f"slot {slot} forced to {sorted(forced_values)}, expected role or selected-bundle values "
                    f"{sorted(authorized_values)}"
                )
        return True, "role costume slots preserved or explicitly transformed by the selected bundle"

    return False, f"unknown assert type {kind!r}"


def evaluate_review_gates(
    gates: Sequence[dict[str, Any]],
    explanation: dict[str, Any],
    role_recipe: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for gate in gates:
        gate_id = str(gate.get("id") or "")
        entry: dict[str, Any] = {
            "id": gate_id,
            "source": gate.get("source"),
            "check": gate.get("check"),
        }
        if not gate.get("machine_checkable"):
            entry["status"] = "manual"
            results.append(entry)
            continue
        spec = gate.get("assert")
        if not isinstance(spec, dict):
            entry["status"] = "fail"
            entry["detail"] = "machine_checkable gate has no assert spec"
            results.append(entry)
            continue
        passed, detail = evaluate_gate_assert(spec, explanation, role_recipe)
        entry["status"] = "pass" if passed else "fail"
        entry["detail"] = detail
        results.append(entry)
    return results


def merge_affine_presets(spec: dict[str, Any], preset_ids: Sequence[str]) -> dict[str, Any]:
    """Concept-affine presets (role/bundle preset ids) become preferred presets
    so soft mode keeps preset selection near the concept's home domain."""
    clean = [str(pid) for pid in preset_ids if str(pid or "").strip()]
    if not clean:
        return spec
    affinity = spec.setdefault("preset_affinity", {})
    preferred = normalize_list(affinity.get("preferred_presets"))
    for pid in clean:
        if pid not in preferred:
            preferred.append(pid)
    affinity["preferred_presets"] = preferred
    return spec


def anchor_expansion_config(
    recipes: dict[str, Any],
    applied_recipes: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Merge anchor_expansion config: soft_anchor_defaults first, recipes override."""
    defaults = recipes.get("soft_anchor_defaults", {}) if isinstance(recipes, dict) else {}
    base = defaults.get("anchor_expansion") if isinstance(defaults, dict) else None
    merged: dict[str, Any] = dict(base) if isinstance(base, dict) else {}
    for recipe in applied_recipes:
        if not isinstance(recipe, dict):
            continue
        override = recipe.get("anchor_expansion")
        if isinstance(override, dict):
            merged.update(override)
    return merged


def build_soft_anchor_spec(
    specs: Sequence[dict[str, Any]],
    min_anchor_candidates: Sequence[int],
    concept: str,
    anchor_expansion: dict[str, Any] | None = None,
    safety_evaluation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    anchors = dedupe_soft_anchor_specs(specs)
    source_floors: dict[str, int] = {}
    group_floors: dict[str, int] = {}
    visual_guards: list[dict[str, Any]] = []
    render_priority_terms: list[dict[str, Any]] = []
    free_slot_constraints: dict[str, Any] = {}
    render_suppress_terms: list[str] = []
    render_directives: list[dict[str, Any]] = []
    dual_read_requirement: dict[str, Any] = {}
    preset_affinity: dict[str, Any] = {}
    role_scene_policy: dict[str, Any] = {}
    species_family_policy: dict[str, Any] = {}
    soft_repair_policy: dict[str, Any] = {}
    safety_negative_floor: list[str] = []
    mixin_cue_budgets: list[int] = []
    for anchor in anchors:
        for source, value in (anchor.get("source_floors", {}) or {}).items():
            source_floors[source] = max(normalize_int(source_floors.get(source), 0), normalize_int(value, 0))
        anchor.pop("source_floors", None)
        for group, value in (anchor.get("group_floors", {}) or {}).items():
            group_floors[group] = max(normalize_int(group_floors.get(group), 0), normalize_int(value, 0))
        anchor.pop("group_floors", None)
        for guard in anchor.pop("visual_guards", []) or []:
            if guard not in visual_guards:
                visual_guards.append(guard)
        for group in anchor.pop("render_priority_terms", []) or []:
            if group not in render_priority_terms:
                render_priority_terms.append(group)
        for slot, constraint in (anchor.pop("free_slot_constraints", {}) or {}).items():
            if isinstance(constraint, dict):
                free_slot_constraints.setdefault(slot, {}).update(constraint)
        for term in normalize_list(anchor.pop("render_suppress_terms", [])):
            if term not in render_suppress_terms:
                render_suppress_terms.append(term)
        for directive in anchor.pop("render_directives", []) or []:
            if isinstance(directive, dict) and directive not in render_directives:
                render_directives.append(directive)
        if anchor.get("dual_read_requirement"):
            dual_read_requirement.update(anchor.pop("dual_read_requirement") or {})
        else:
            anchor.pop("dual_read_requirement", None)
        if anchor.get("preset_affinity"):
            preset_affinity.update(anchor.pop("preset_affinity") or {})
        else:
            anchor.pop("preset_affinity", None)
        if anchor.get("role_scene_policy"):
            merge_role_scene_policy(role_scene_policy, anchor.pop("role_scene_policy") or {})
        else:
            anchor.pop("role_scene_policy", None)
        if anchor.get("species_family_policy"):
            merge_species_family_policy(species_family_policy, anchor.pop("species_family_policy") or {})
        else:
            anchor.pop("species_family_policy", None)
        if anchor.get("soft_repair_policy"):
            soft_repair_policy.update(anchor.pop("soft_repair_policy") or {})
        else:
            anchor.pop("soft_repair_policy", None)
        for term in normalize_list(anchor.pop("safety_negative_floor", [])):
            if term not in safety_negative_floor:
                safety_negative_floor.append(term)
        budget = normalize_int(anchor.pop("mixin_cue_budget", 0), 0)
        if budget > 0:
            mixin_cue_budgets.append(budget)
    if not source_floors:
        sources = {source for anchor in anchors for source in str(anchor.get("source") or "").split("+")}
        if "role" in sources:
            source_floors["role"] = 1
        if "mixin" in sources:
            source_floors["mixin"] = 1

    # Orphaned-floor clamp: dedupe can drop a non-critical anchor whose group
    # or source backed a floor (e.g. a mixin primary anchor on a role-critical
    # slot). A floor no surviving anchor can satisfy would make the soft match
    # permanently fail, so clamp floors to what the surviving anchors carry.
    group_carriers: dict[str, int] = {}
    source_carriers: dict[str, int] = {}
    for anchor in anchors:
        for group in normalize_list(anchor.get("groups")):
            group_carriers[group] = group_carriers.get(group, 0) + 1
        for source in str(anchor.get("source") or "").split("+"):
            if source:
                source_carriers[source] = source_carriers.get(source, 0) + 1
    group_floors = {
        group: min(value, group_carriers.get(group, 0))
        for group, value in group_floors.items()
        if min(value, group_carriers.get(group, 0)) > 0
    }
    source_floors = {
        source: min(value, source_carriers.get(source, 0))
        for source, value in source_floors.items()
        if min(value, source_carriers.get(source, 0)) > 0
    }
    positive_minima = [value for value in min_anchor_candidates if value > 0]
    default_min = min(2, len(anchors)) if len(anchors) >= 2 else len(anchors)
    min_anchors = max(positive_minima) if positive_minima else default_min
    min_anchors = min(max(min_anchors, 0), len(anchors))
    salience_floor = 1 if any("mixin" in str(anchor.get("source") or "").split("+") for anchor in anchors) else 0
    role_terms: list[str] = []
    mixin_terms: list[str] = []
    for anchor in anchors:
        target = role_terms if "role" in str(anchor.get("source") or "").split("+") else mixin_terms
        for term in normalize_list(anchor.get("terms")):
            if term not in target:
                target.append(term)
    if role_terms and mixin_terms:
        dual_read_requirement.setdefault("enabled", True)
        dual_read_requirement.setdefault("role_terms", role_terms[:8])
        dual_read_requirement.setdefault("mixin_terms", mixin_terms[:8])
    result = {
        "mode": "soft",
        "concept": concept,
        "anchor_expansion": dict(anchor_expansion) if isinstance(anchor_expansion, dict) else {},
        "min_anchors": min_anchors,
        "source_floors": source_floors,
        "group_floors": group_floors,
        "salience_floor": salience_floor,
        "visual_guards": visual_guards,
        "render_priority_terms": render_priority_terms,
        "free_slot_constraints": free_slot_constraints,
        "render_suppress_terms": render_suppress_terms,
        "render_directives": render_directives,
        "dual_read_requirement": dual_read_requirement,
        "preset_affinity": preset_affinity,
        "role_scene_policy": role_scene_policy,
        "species_family_policy": species_family_policy,
        "soft_repair_policy": soft_repair_policy,
        "safety_negative_floor": safety_negative_floor,
        "mixin_cue_budget": min(mixin_cue_budgets) if mixin_cue_budgets else 0,
        "anchors": anchors,
    }
    if isinstance(safety_evaluation, dict) and safety_evaluation:
        result["safety_evaluation"] = safety_evaluation
    return result


def soft_anchor_spec_has_runtime_controls(spec: dict[str, Any]) -> bool:
    return bool(
        spec.get("anchors")
        or spec.get("visual_guards")
        or spec.get("free_slot_constraints")
        or spec.get("render_directives")
        or spec.get("render_suppress_terms")
        or spec.get("safety_negative_floor")
    )


def resolve_concept_mode(values: Sequence[str]) -> str:
    mode = str(values[-1]).strip() if values else "legacy"
    if mode not in CONCEPT_MODES:
        raise ValueError("--concept-mode must be one of: legacy, soft")
    return mode


def load_concept_recipes(path: Path = DEFAULT_CONCEPT_RECIPES) -> dict[str, Any]:
    if not path.exists():
        return {"roles": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def canonicalize_concept(concept: str, recipes: dict[str, Any]) -> str:
    aliases = recipes.get("aliases", {}) if isinstance(recipes, dict) else {}
    if not isinstance(aliases, dict):
        return concept
    normalized = concept
    roles = recipes.get("roles", {}) if isinstance(recipes, dict) else {}
    non_role_followers = {
        "시스템",
        "정책",
        "기술",
        "설정",
        "카메라",
        "솔루션",
        "프로그램",
        "장치",
        "산업",
    }
    for alias, canonical in sorted(aliases.items(), key=lambda item: len(str(item[0])), reverse=True):
        alias_text = str(alias or "").strip()
        canonical_text = str(canonical or "").strip()
        if alias_text and canonical_text:
            pattern = re.compile(
                rf"(?<![A-Za-z0-9가-힣]){re.escape(alias_text)}(?![A-Za-z0-9가-힣])"
            )

            def replace(match: re.Match[str]) -> str:
                if canonical_text in roles:
                    tail = normalized[match.end() :].lstrip()
                    follower = tail.split(None, 1)[0] if tail else ""
                    if follower in non_role_followers:
                        return match.group(0)
                return canonical_text

            normalized = pattern.sub(replace, normalized)
    return normalized


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
    remaining = stripped
    matches: list[tuple[str, dict[str, Any]]] = []
    for mixin in sorted(mixins, key=len, reverse=True):
        if mixin and mixin in remaining:
            matches.append((mixin, dict(mixins[mixin] or {})))
            remaining = remaining.replace(mixin, " ")
    return matches


def concept_without_mixins(concept: str, mixin_names: Sequence[str]) -> str:
    stripped = concept
    for mixin in mixin_names:
        stripped = stripped.replace(mixin, " ")
    return " ".join(stripped.split())


def filter_role_duplicate_mixins(
    concept: str,
    roles: dict[str, Any],
    mixin_matches: Sequence[tuple[str, dict[str, Any]]],
) -> list[tuple[str, dict[str, Any]]]:
    filtered: list[tuple[str, dict[str, Any]]] = []
    for mixin, recipe in mixin_matches:
        if mixin in roles:
            without_this_mixin = concept_without_mixins(concept, [mixin])
            alternate_role, _, _ = match_concept_role(without_this_mixin, roles) if without_this_mixin else (None, "", {})
            if alternate_role is None:
                continue
        filtered.append((mixin, recipe))
    role_concept = concept_without_mixins(concept, [mixin for mixin, _ in filtered])
    role, _, _ = match_concept_role(role_concept, roles) if role_concept else (None, "", {})
    if role is None:
        role_like_mixins = [(mixin, recipe) for mixin, recipe in filtered if mixin in roles]
        if len(role_like_mixins) > 1:
            role_like_mixins.sort(key=lambda item: concept.find(item[0]) if item[0] in concept else len(concept))
            restored_role = role_like_mixins[0][0]
            candidate = [(mixin, recipe) for mixin, recipe in filtered if mixin != restored_role]
            candidate_role_concept = concept_without_mixins(concept, [mixin for mixin, _ in candidate])
            candidate_role, _, _ = match_concept_role(candidate_role_concept, roles) if candidate_role_concept else (None, "", {})
            if candidate_role == restored_role:
                filtered = candidate
    return filtered


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


def select_mixin_species_variant(
    concept: str, mixin_name: str, mixin_recipe: dict[str, Any], args: Sequence[str], role: str = ""
) -> dict[str, Any] | None:
    species_config = mixin_recipe.get("species_variants")
    if not isinstance(species_config, dict):
        return None
    raw_variants = species_config.get("variants")
    variants = [dict(variant) for variant in raw_variants if isinstance(variant, dict)] if isinstance(raw_variants, list) else []
    if not variants:
        return None

    lowered = concept.lower()
    alias_text = lowered.replace(str(role or "").lower(), " ") if role else lowered
    for variant in variants:
        aliases = normalize_list(variant.get("aliases"))
        if any(alias and alias.lower() in alias_text for alias in aliases):
            selected = dict(variant)
            if str(selected.get("tier") or "") == "opt_in":
                selected["opt_in_activated"] = True
                selected["activation"] = "alias"
            return selected

    excluded_default_families = set(normalize_list(species_config.get("excluded_default_families")))
    # Batch species-diversity support: callers generating one concept per CLI
    # invocation pass previously selected families to avoid convergence.
    _, user_excluded = extract_option_values(list(args), "--exclude-species")
    user_excluded_families = {value.strip() for value in user_excluded if value.strip()}
    selectable_variants = [
        variant
        for variant in variants
        if str(variant.get("tier") or "") != "opt_in"
        and str(variant.get("family") or variant.get("id") or "") not in excluded_default_families
        and str(variant.get("id") or "") not in excluded_default_families
        and str(variant.get("family") or "") not in user_excluded_families
        and str(variant.get("id") or "") not in user_excluded_families
    ]
    if not selectable_variants:
        selectable_variants = [
            variant
            for variant in variants
            if str(variant.get("tier") or "") != "opt_in"
            and str(variant.get("family") or variant.get("id") or "") not in excluded_default_families
            and str(variant.get("id") or "") not in excluded_default_families
    ] or [
            variant for variant in variants if str(variant.get("tier") or "") != "opt_in"
        ] or variants

    ledger_counts = species_family_counts_from_anchor_ledger(args)
    if ledger_counts and selectable_variants:
        min_count = min(
            int(ledger_counts.get(str(variant.get("family") or variant.get("id") or ""), 0))
            for variant in selectable_variants
        )
        balanced_variants = [
            variant
            for variant in selectable_variants
            if int(ledger_counts.get(str(variant.get("family") or variant.get("id") or ""), 0)) == min_count
        ]
        if balanced_variants:
            selectable_variants = balanced_variants

    weights = [max(float(variant.get("weight", 1) or 0), 0.0) for variant in selectable_variants]
    total = sum(weights)
    if total <= 0:
        return selectable_variants[0]

    seed = option_value(args, "--seed") or ""
    stream = str(species_config.get("stream") or "species")
    token = f"{concept}|{mixin_name}|{stream}|{seed}"
    value = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:16], 16) / float(16**16)
    threshold = value * total
    running = 0.0
    for variant, weight in zip(selectable_variants, weights):
        running += weight
        if threshold <= running:
            return variant
    return selectable_variants[-1]


def species_family_counts_from_anchor_ledger(args: Sequence[str]) -> dict[str, int]:
    ledger_path = option_value(args, "--anchor-diversity-ledger")
    if not ledger_path:
        return {}
    try:
        payload = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    raw_counts = payload.get("species_family") if isinstance(payload, dict) else {}
    if not isinstance(raw_counts, dict):
        return {}
    counts: dict[str, int] = {}
    for family, count in raw_counts.items():
        try:
            value = int(count)
        except (TypeError, ValueError):
            continue
        if value > 0:
            counts[str(family)] = value
    return counts


def species_family_policy_for_variant(mixin_name: str, variant: dict[str, Any]) -> dict[str, Any]:
    mapping = forced_sets_to_mapping(set_values_to_forced(variant.get("set")))
    allowed: dict[str, list[str]] = {}
    for slot in ("species_marker", "texture", "anatomical_connection"):
        values = normalize_list(mapping.get(slot))
        if values:
            allowed[slot] = values
    if not allowed:
        return {}
    return {
        "enabled": True,
        "mixin": mixin_name,
        "family": str(variant.get("family") or variant.get("id") or ""),
        "variant_id": str(variant.get("id") or ""),
        "tier": str(variant.get("tier") or ""),
        "allowed": allowed,
        "enforce": True,
        "hybrid_allowed": False,
    }


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


def recipe_override_slots(
    recipes: dict[str, Any],
    mixin_recipe: dict[str, Any],
    selected_bundle: dict[str, Any],
) -> set[str]:
    for source, keys in (
        (selected_bundle, ("override_slots",)),
        (mixin_recipe, ("bundle_override_slots", "override_slots")),
        (recipes, ("bundle_override_slots", "override_slots")),
    ):
        for key in keys:
            if key in source:
                return set(normalize_list(source.get(key)))
    return set()


def conditional_additional_requirements(
    recipe: dict[str, Any],
    *,
    role: str | None,
    mixin: str | None = None,
    selected_bundle: dict[str, Any] | None = None,
    explicit_user_set_slots: set[str] | None = None,
) -> list[str]:
    rules = recipe.get("conditional_additional")
    if not isinstance(rules, list):
        return []
    explicit_user_set_slots = explicit_user_set_slots or set()
    selected_bundle = selected_bundle or {}
    requirements: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if rule.get("requires_role") and not role:
            continue
        allowed_roles = set(normalize_list(rule.get("roles")))
        if allowed_roles and role not in allowed_roles:
            continue
        excluded_roles = set(normalize_list(rule.get("exclude_roles")))
        if excluded_roles and role in excluded_roles:
            continue
        if rule.get("requires_bundle") and not selected_bundle:
            continue
        rule_mixin = str(rule.get("mixin") or "")
        if rule_mixin and rule_mixin != (mixin or ""):
            continue
        bundle_id = str(rule.get("bundle_id") or "")
        if bundle_id and bundle_id != str(selected_bundle.get("id") or ""):
            continue
        blocked_slots = set(normalize_list(rule.get("unless_user_set_slots_any")))
        if blocked_slots and explicit_user_set_slots & blocked_slots:
            continue
        requirements.extend(normalize_list(rule.get("text") or rule.get("additional")))
    return requirements


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
            else:
                return None
    else:
        generic_bundles = [bundle for bundle in bundles if not normalize_list(bundle.get("roles"))]
        if generic_bundles:
            bundles = generic_bundles
        else:
            # A standalone mixin must never inherit a bundle authored for an
            # unrelated role. Fall back to the mixin core when no generic
            # aspect exists.
            return None

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


def select_recipe_scene_variant(
    concept: str,
    recipe: dict[str, Any],
    args: Sequence[str],
) -> dict[str, Any] | None:
    raw_variants = recipe.get("scene_variants")
    variants = [dict(item) for item in raw_variants or [] if isinstance(item, dict)]
    if not variants:
        return None
    weights = [max(float(item.get("weight", 1) or 0), 0.0) for item in variants]
    total = sum(weights)
    if total <= 0:
        return variants[0]
    seed = option_value(args, "--seed") or ""
    digest = hashlib.sha256(f"scene-variant|{concept}|{seed}".encode("utf-8")).digest()
    threshold = int.from_bytes(digest[:8], "big") / 2**64 * total
    cursor = 0.0
    for variant, weight in zip(variants, weights):
        cursor += weight
        if threshold < cursor:
            return variant
    return variants[-1]


def resolved_role_set(
    recipe: dict[str, Any],
    scene_variant: dict[str, Any] | None,
) -> list[str]:
    if not isinstance(recipe.get("identity_core"), dict):
        return set_values_to_forced(recipe.get("set"))
    identity = set_values_to_forced(recipe.get("identity_core"))
    scene = set_values_to_forced((scene_variant or {}).get("set"))
    return merge_forced_set_groups(
        [
            (identity, set()),
            (scene, forced_set_slots(scene)),
        ]
    )


def add_option(args: list[str], name: str, value: str) -> None:
    if value:
        args.extend([name, value])


def resolve_concepts(
    args: Sequence[str],
    concepts: Sequence[str],
    concept_mode: str = "legacy",
    concept_mode_explicit: bool = True,
    safety_evaluation_requested: bool = False,
    enforce_gates: bool = True,
) -> tuple[list[str], list[dict[str, Any]]]:
    if concept_mode not in CONCEPT_MODES:
        raise ValueError("--concept-mode must be one of: legacy, soft")
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
        concept = canonicalize_concept(concept, recipes)
        mixin_matches = match_concept_mixins(concept, mixins)
        mixin_matches = filter_role_duplicate_mixins(concept, roles, mixin_matches)
        role_concept = concept_without_mixins(concept, [mixin for mixin, _ in mixin_matches])
        role, name, recipe = match_concept_role(role_concept or concept, roles)

        # Per-recipe gradual soft promotion: an explicit --concept-mode always
        # wins; otherwise a recipe that passed the soft benchmark gate may opt
        # into soft mode via concept_mode_default.
        effective_mode = concept_mode
        if not concept_mode_explicit:
            recipe_default = str((recipe or {}).get("concept_mode_default") or "")
            if not recipe_default:
                recipe_default = next(
                    (
                        str(mixin_recipe.get("concept_mode_default") or "")
                        for _, mixin_recipe in mixin_matches
                        if mixin_recipe.get("concept_mode_default")
                    ),
                    "",
                )
            if recipe_default in CONCEPT_MODES:
                effective_mode = recipe_default
        selected_bundles: list[dict[str, Any]] = []
        selected_species_variants: list[dict[str, Any]] = []
        selected_scene_variants: list[dict[str, Any]] = []
        set_groups: list[tuple[Sequence[str], set[str]]] = []
        applied_recipes = [recipe] if recipe else []
        scaffold_recipes: list[dict[str, Any]] = [recipe] if recipe else []
        additional_requirements: list[str] = []
        soft_safety_requirements: list[str] = []
        safety_evaluation_items: list[dict[str, Any]] = []
        soft_salience_cues: list[str] = []
        soft_mixin_cue_budgets: list[int] = []
        intent_axes: list[str] = []
        soft_anchor_specs: list[dict[str, Any]] = []
        soft_min_anchor_candidates: list[int] = []

        if recipe:
            role_scene_variant = select_recipe_scene_variant(concept, recipe, args)
            if role_scene_variant:
                scaffold_recipes.append(role_scene_variant)
                add_option(resolved_args, "--concept-scene-variant", str(role_scene_variant.get("id") or ""))
                selected_scene_variants.append(
                    {
                        "role": role or concept,
                        "id": str(role_scene_variant.get("id") or ""),
                        "weight": role_scene_variant.get("weight", 1),
                        "set": role_scene_variant.get("set", {}),
                    }
                )
            safety_evaluation_items.extend(
                safety_transform_items_for_recipe(role or concept, recipe)
            )
            if role_scene_variant:
                safety_evaluation_items.extend(
                    safety_transform_items_for_recipe(
                        str(role_scene_variant.get("id") or f"{role}_scene"),
                        role_scene_variant,
                    )
                )
            role_set = resolved_role_set(recipe, role_scene_variant)
            set_groups.append((role_set, set()))
            role_mapping = forced_sets_to_mapping(role_set)
            scene_variant_mapping = forced_sets_to_mapping(
                set_values_to_forced((role_scene_variant or {}).get("set"))
            )
            atomic_scene_slots = set(scene_variant_mapping)
            atomic_scene_group = (
                f"role_scene:{str((role_scene_variant or {}).get('id') or '')}"
                if role_scene_variant
                else ""
            )
            soft_anchor_specs.extend(
                soft_anchor_specs_from_mapping(
                    recipes,
                    role_mapping,
                    recipe,
                    "role",
                    explicit_user_set_slots,
                    local_pool_slots=atomic_scene_slots,
                    atomic_group=atomic_scene_group,
                )
            )
            soft_min_anchor_candidates.append(soft_min_anchors_for_recipe(recipe, 1))
            additional_requirements.extend(normalize_list(recipe.get("additional")))
            additional_requirements.extend(normalize_list((role_scene_variant or {}).get("additional")))
            soft_safety_requirements.extend(soft_safety_requirements_for_recipe(recipe))
            soft_salience_cues.extend(soft_salience_cues_for_recipe(recipe))
            budget = mixin_cue_budget_for_recipe(recipe)
            if budget > 0:
                soft_mixin_cue_budgets.append(budget)
            additional_requirements.extend(
                conditional_additional_requirements(
                    recipe,
                    role=role,
                    explicit_user_set_slots=explicit_user_set_slots,
                )
            )
            intent_axes.extend(normalize_list(recipe.get("intent_axis")))
            intent_axes.extend(normalize_list((role_scene_variant or {}).get("intent_axis")))

        for mixin, mixin_recipe in mixin_matches:
            applied_recipes.append(mixin_recipe)
            scaffold_recipes.append(mixin_recipe)
            safety_evaluation_items.extend(
                safety_transform_items_for_recipe(mixin, mixin_recipe)
            )
            selected_bundle = select_bundle_for_mixin(concept, mixin, mixin_recipe, args, role)
            mixin_base_set = set_values_to_forced(mixin_recipe.get("set"))
            additional_requirements.extend(normalize_list(mixin_recipe.get("additional")))
            soft_safety_requirements.extend(soft_safety_requirements_for_recipe(mixin_recipe))
            soft_salience_cues.extend(soft_salience_cues_for_recipe(mixin_recipe))
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
            species_variant = select_mixin_species_variant(concept, mixin, mixin_recipe, args, role=role or "")
            if species_variant:
                scaffold_recipes.append(species_variant)
                safety_evaluation_items.extend(
                    safety_transform_items_for_recipe(
                        str(species_variant.get("id") or f"{mixin}_variant"),
                        species_variant,
                    )
                )
                species_variant_set = set_values_to_forced(species_variant.get("set"))
                species_family_policy = species_family_policy_for_variant(mixin, species_variant)
                if species_variant_set:
                    set_groups.append((species_variant_set, set()))
                    variant_specs = soft_anchor_specs_from_mapping(
                        recipes,
                        forced_sets_to_mapping(species_variant_set),
                        species_variant,
                        "mixin",
                        explicit_user_set_slots,
                    )
                    if species_family_policy:
                        for spec in variant_specs:
                            spec["species_family_policy"] = species_family_policy
                            if spec.get("slot") in species_family_policy.get("allowed", {}):
                                spec["variant_group"] = "species_family"
                                spec["variant_strategy"] = "locked_family"
                    soft_anchor_specs.extend(variant_specs)
                    soft_min_anchor_candidates.append(soft_min_anchors_for_recipe(species_variant, 1))
                additional_requirements.extend(normalize_list(species_variant.get("additional")))
                soft_safety_requirements.extend(soft_safety_requirements_for_recipe(species_variant))
                soft_salience_cues.extend(soft_salience_cues_for_recipe(species_variant))
                intent_axes.extend(normalize_list(species_variant.get("intent_axis")))
                selected_species_variants.append(
                    {
                        "mixin": mixin,
                        "variant_id": str(species_variant.get("id") or ""),
                        "family": str(species_variant.get("family") or species_variant.get("id") or ""),
                        "tier": str(species_variant.get("tier") or ""),
                        "weight": species_variant.get("weight", 1),
                        "opt_in_activated": bool(species_variant.get("opt_in_activated")),
                        "activation": str(species_variant.get("activation") or "weighted"),
                        "species_family_policy": species_family_policy,
                    }
                )
            if selected_bundle:
                scaffold_recipes.append(selected_bundle)
                safety_evaluation_items.extend(
                    safety_transform_items_for_recipe(
                        str(selected_bundle.get("id") or f"{mixin}_bundle"),
                        selected_bundle,
                    )
                )
                bundle_preset = str(selected_bundle.get("preset") or "")
                if effective_mode == "legacy" and bundle_preset and not has_preset_value:
                    add_option(resolved_args, "--preset", bundle_preset)
                    has_preset_value = True
                if mixin_base_set:
                    set_groups.append((mixin_base_set, set()))
                    soft_anchor_specs.extend(
                        soft_anchor_specs_from_mapping(
                            recipes,
                            forced_sets_to_mapping(mixin_base_set),
                            mixin_recipe,
                            "mixin",
                            explicit_user_set_slots,
                        )
                    )
                    soft_min_anchor_candidates.append(soft_min_anchors_for_recipe(mixin_recipe, 1))
                bundle_set = selected_bundle.get("set") if isinstance(selected_bundle.get("set"), dict) else {}
                bundle_forced = set_values_to_forced(bundle_set)
                set_groups.append((bundle_forced, recipe_override_slots(recipes, mixin_recipe, selected_bundle)))
                soft_anchor_specs.extend(
                    soft_anchor_specs_from_mapping(
                        recipes,
                        forced_sets_to_mapping(bundle_forced),
                        selected_bundle,
                        "bundle",
                        explicit_user_set_slots,
                    )
                )
                soft_min_anchor_candidates.append(
                    soft_min_anchors_for_recipe(selected_bundle, 2 if role else 1)
                )
                additional_requirements.extend(normalize_list(selected_bundle.get("additional")))
                soft_safety_requirements.extend(soft_safety_requirements_for_recipe(selected_bundle))
                soft_salience_cues.extend(soft_salience_cues_for_recipe(selected_bundle))
                budget = mixin_cue_budget_for_recipe(selected_bundle)
                if budget > 0:
                    soft_mixin_cue_budgets.append(budget)
                additional_requirements.extend(
                    conditional_additional_requirements(
                        mixin_recipe,
                        role=role,
                        mixin=mixin,
                        selected_bundle=selected_bundle,
                        explicit_user_set_slots=explicit_user_set_slots,
                    )
                )
                intent_axes.extend(normalize_list(selected_bundle.get("intent_axis")))
                selected_bundles.append(
                    {
                        "mixin": mixin,
                        "bundle_id": str(selected_bundle.get("id") or ""),
                        "aspect": str(selected_bundle.get("aspect") or ""),
                        "preset": bundle_preset,
                        "set": bundle_set,
                        "weight": selected_bundle.get("weight", 1),
                        "subtype": str(selected_bundle.get("subtype") or ""),
                    }
                )
            else:
                set_groups.append((mixin_base_set, set()))
                if mixin_base_set:
                    soft_anchor_specs.extend(
                        soft_anchor_specs_from_mapping(
                            recipes,
                            forced_sets_to_mapping(mixin_base_set),
                            mixin_recipe,
                            "mixin",
                            explicit_user_set_slots,
                        )
                    )
                    soft_min_anchor_candidates.append(soft_min_anchors_for_recipe(mixin_recipe, 1))

        combined_sets = merge_forced_set_groups(set_groups)
        expansion_config = anchor_expansion_config(recipes, applied_recipes)
        safety_evaluation = safety_evaluation_payload(
            safety_evaluation_items,
            requested=safety_evaluation_requested,
        )
        add_option(resolved_args, "--concept-lock", concept)

        preset = str(recipe.get("preset") or "")
        if not preset:
            preset = next(
                (str(mixin_recipe.get("preset") or "") for _, mixin_recipe in mixin_matches if mixin_recipe.get("preset")),
                "",
            )
        affine_presets = [str(recipe.get("preset") or "")] if recipe else []
        affine_presets += [str(m.get("preset") or "") for _, m in mixin_matches]
        affine_presets += [str(b.get("preset") or "") for b in selected_bundles]
        if effective_mode == "legacy" and preset and not has_preset_value:
            add_option(resolved_args, "--preset", preset)
            has_preset_value = True
        if effective_mode == "legacy":
            for forced in combined_sets:
                add_option(resolved_args, "--set", forced)
            if soft_anchor_specs:
                soft_anchor_spec = apply_reference_scaffold_fields(
                    build_soft_anchor_spec(
                        soft_anchor_specs,
                        soft_min_anchor_candidates,
                        concept,
                        expansion_config,
                        safety_evaluation,
                    ),
                    scaffold_recipes,
                )
                if (
                    soft_anchor_spec["anchors"]
                    and soft_anchor_spec["min_anchors"] > 0
                    and soft_anchor_spec_has_runtime_controls(soft_anchor_spec)
                ):
                    add_option(
                        resolved_args,
                        "--soft-anchor-spec",
                        json.dumps(soft_anchor_spec, ensure_ascii=False, separators=(",", ":")),
                    )
            for requirement in additional_requirements:
                add_option(resolved_args, "--additional-requirement", requirement)
        elif soft_anchor_specs:
            soft_anchor_spec = apply_reference_scaffold_fields(
                build_soft_anchor_spec(
                    soft_anchor_specs,
                    soft_min_anchor_candidates,
                    concept,
                    expansion_config,
                    safety_evaluation,
                ),
                scaffold_recipes,
            )
            merge_affine_presets(soft_anchor_spec, affine_presets)
            if soft_anchor_spec["anchors"] and soft_anchor_spec["min_anchors"] > 0:
                add_option(
                    resolved_args,
                    "--soft-anchor-spec",
                    json.dumps(soft_anchor_spec, ensure_ascii=False, separators=(",", ":")),
                )
                # Role/mixin/bundle descriptive guidance is identity-bearing
                # (e.g. Joseon-court styling); soft mode keeps it alongside the
                # safety floor instead of dropping it with the forced slots.
                effective_requirements = list(additional_requirements)
                effective_requirements.extend(soft_safety_requirements)
                for requirement in dict.fromkeys(effective_requirements):
                    add_option(resolved_args, "--additional-requirement", requirement)
                defaults = recipes.get("soft_anchor_defaults", {}) if isinstance(recipes, dict) else {}
                max_salience = normalize_int(defaults.get("max_salience_cues") if isinstance(defaults, dict) else None, 2)
                if soft_mixin_cue_budgets:
                    max_salience = min(max_salience, min(soft_mixin_cue_budgets))
                for cue in list(dict.fromkeys(soft_salience_cues))[: max(0, max_salience)]:
                    add_option(resolved_args, "--soft-requirement", cue)
        for axis in intent_axes:
            add_option(resolved_args, "--intent-axis", axis)

        likeness_mode = str(recipe.get("likeness_mode") or "")
        if not likeness_mode:
            likeness_mode = next(
                (str(mixin_recipe.get("likeness_mode") or "") for _, mixin_recipe in mixin_matches if mixin_recipe.get("likeness_mode")),
                "",
            )
        if likeness_mode and name and not has_likeness_value:
            add_option(resolved_args, "--likeness-mode", likeness_mode)
            add_option(resolved_args, "--likeness-reference", name)
            has_likeness_value = True

        if not applied_recipes:
            add_option(resolved_args, "--intent-axis", concept)

        applied_named: list[tuple[str, dict[str, Any]]] = []
        if recipe:
            applied_named.append((role or concept, recipe))
        applied_named.extend(mixin_matches)
        explanation = {
            "concept": concept,
            "concept_mode": effective_mode,
            "name": name,
            "role": role,
            "applied_role": role,
            "applied_mixins": [mixin for mixin, _ in mixin_matches],
            "matched": bool(applied_recipes),
            "recipe": recipe,
            "mixins": {mixin: mixin_recipe for mixin, mixin_recipe in mixin_matches},
            "selected_bundles": selected_bundles,
            "selected_species_variants": selected_species_variants,
            "selected_scene_variants": selected_scene_variants,
            "combined_forced_slots": forced_sets_to_mapping(combined_sets),
            "soft_anchor_spec": merge_affine_presets(
                apply_reference_scaffold_fields(
                    build_soft_anchor_spec(
                        soft_anchor_specs,
                        soft_min_anchor_candidates,
                        concept,
                        expansion_config,
                        safety_evaluation,
                    ),
                    scaffold_recipes,
                ),
                affine_presets,
            ),
            "forced_slots_applied": effective_mode == "legacy",
        }
        explanation["safety"] = safety_evaluation
        explanation["guide"] = collect_concept_guides(applied_named)
        review_gates = collect_review_gates(applied_named)
        explanation["review_gates"] = review_gates
        gate_results = evaluate_review_gates(review_gates, explanation, recipe)
        explanation["gate_results"] = gate_results
        add_option(
            resolved_args,
            "--concept-gates-json",
            json.dumps(gate_results, ensure_ascii=False, separators=(",", ":")),
        )
        failed_gates = [
            str(gate.get("id") or "unknown")
            for gate in gate_results
            if isinstance(gate, dict) and gate.get("status") == "fail"
        ]
        if failed_gates and enforce_gates:
            raise ValueError(
                f"concept review gate failed for '{concept}': {', '.join(failed_gates)}"
            )
        explanations.append(explanation)

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
    safety_evaluation_requested = SAFETY_EVALUATION_FLAG in args
    _, user_additional_requirements = extract_option_values(args, "--additional-requirement")
    args = remove_flag(remove_flag(args, "--plain"), "--no-negative")
    args, concepts = extract_option_values(args, "--concept")
    args, concept_mode_values = extract_option_values(args, "--concept-mode")
    emit_candidate_pack = has_option(args, "--emit-candidate-pack")
    concept_mode = resolve_concept_mode(concept_mode_values or (["soft"] if emit_candidate_pack else []))
    args, explain_concept = extract_flag(args, "--explain-concept")
    args, _ = resolve_concepts(
        args,
        concepts,
        concept_mode,
        concept_mode_explicit=bool(concept_mode_values) or emit_candidate_pack,
        safety_evaluation_requested=safety_evaluation_requested,
        enforce_gates=not explain_concept,
    )
    # Wrapper-only option: consumed by species-variant selection, not the engine.
    args, _ = extract_option_values(args, "--exclude-species")

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
    for requirement in user_additional_requirements:
        args.extend(["--user-mandatory-intent", requirement])

    return args


def main(argv: Sequence[str] | None = None) -> int:
    load_project_env()
    raw_args = list(argv or sys.argv[1:])
    concept_args, concepts = extract_option_values(raw_args, "--concept")
    _, explain_concept = extract_flag(concept_args, "--explain-concept")
    if explain_concept:
        forward_args = build_forward_args(raw_args)
        explain_args = extract_flag(concept_args, "--explain-concept")[0]
        explain_args, concept_mode_values = extract_option_values(explain_args, "--concept-mode")
        emit_candidate_pack = has_option(explain_args, "--emit-candidate-pack")
        concept_mode = resolve_concept_mode(concept_mode_values or (["soft"] if emit_candidate_pack else []))
        _, explanations = resolve_concepts(
            explain_args,
            concepts,
            concept_mode,
            concept_mode_explicit=bool(concept_mode_values) or emit_candidate_pack,
            safety_evaluation_requested=SAFETY_EVALUATION_FLAG in raw_args,
            enforce_gates=False,
        )
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
