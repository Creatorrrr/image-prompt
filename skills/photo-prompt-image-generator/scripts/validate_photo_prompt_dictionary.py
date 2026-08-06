#!/usr/bin/env python3
"""Validate optional semantic metadata in photo_prompt_tags.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from prompt_generator import (
    DEFAULT_FACET_VOCAB,
    VALID_PRESET_DOMAINS,
    VALID_SUBJECT_CATEGORIES,
    load_json,
    normalize_list,
)


VALID_AXIS_SIGNAL_SUFFIXES = {"strong", "ambient"}
VALID_AXIS_SIGNAL_ALIASES = {"human_portrait"}
VALID_MATCH_RULE_KEYS = {
    "id",
    "any_terms",
    "all_terms",
    "any_tokens",
    "all_tokens",
    "boundary",
    "match_fields",
    "case_sensitive",
}
VALID_MATCH_FIELDS = {"id", "en", "ko", "embedding_text", "semantic_anchor"}
DEFAULT_CONCEPT_RECIPES = Path(__file__).resolve().parents[1] / "assets" / "concept_recipes.json"
DEFAULT_QUALITY_LAYERS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_quality_layers.json"
NO_TEXT_REQUIRED_TAG = "no_text_required"
NO_TEXT_ANCHOR_TERMS = {
    "abstract",
    "blank",
    "blurred",
    "fictional",
    "generic",
    "no readable",
    "no_text",
    "non-legible",
    "non_legible",
    "unbranded",
    "unreadable",
}
PHOTOGRAPHIC_CRAFT_ENTITY_BLOCKLIST = {
    "apple",
    "cat",
    "cathedral",
    "chapel",
    "church",
    "concert",
    "dog",
    "felt",
    "feline",
    "idol",
    "k-pop",
    "kpop",
    "microphone",
    "persian",
    "priest",
    "priestess",
    "stage",
    "stained glass",
    "wool",
    "고양이",
    "대성당",
    "마이크",
    "무대",
    "사과",
    "성당",
    "스테이지",
    "아이돌",
    "전광판",
    "펠트",
    "프리스트",
}


def merged_facet_vocab(data: dict[str, Any]) -> dict[str, set[str]]:
    vocab: dict[str, set[str]] = {key: set(values) for key, values in DEFAULT_FACET_VOCAB.items()}
    for key, values in (data.get("facet_vocab") or {}).items():
        vocab.setdefault(str(key), set()).update(str(value) for value in values)
    return vocab


def all_entries(data: dict[str, Any]):
    for preset in data.get("presets", []):
        yield f"preset:{preset.get('id')}", preset
    for recipe in data.get("recipes", []):
        yield f"recipe:{recipe.get('id')}", recipe
    for slot, entries in data.get("slots", {}).items():
        for entry in entries:
            yield f"slot:{slot}:{entry.get('id')}", entry


def validate_facets(label: str, entry: dict[str, Any], vocab: dict[str, set[str]], errors: list[str]) -> None:
    facets = entry.get("facets", {}) or {}
    if facets and not isinstance(facets, dict):
        errors.append(f"{label}: facets must be an object")
        return
    for key, raw_values in facets.items():
        if key not in vocab:
            errors.append(f"{label}: unknown facet key {key}")
            continue
        for value in normalize_list(raw_values):
            if value not in vocab[key]:
                errors.append(f"{label}: unknown facet value {key}:{value}")


def validate_guard_token(label: str, token: str, vocab: dict[str, set[str]], errors: list[str]) -> None:
    if ":" not in token:
        errors.append(f"{label}: guard facet must use key:value format: {token}")
        return
    key, value = token.split(":", 1)
    if key not in vocab:
        errors.append(f"{label}: unknown facet key {key}")
        return
    if value not in vocab[key]:
        errors.append(f"{label}: unknown facet value {key}:{value}")


def validate_hard_guards(label: str, entry: dict[str, Any], vocab: dict[str, set[str]], errors: list[str]) -> None:
    guards = entry.get("hard_guards", {}) or {}
    if guards and not isinstance(guards, dict):
        errors.append(f"{label}: hard_guards must be an object")
        return
    for key in ("requires_facets", "exclude_facets"):
        for token in normalize_list(guards.get(key)):
            validate_guard_token(label, token, vocab, errors)


def validate_filter_ids(data: dict[str, Any], errors: list[str]) -> None:
    slots = data.get("slots", {})
    for preset in data.get("presets", []):
        for slot, flt in preset.get("filters", {}).items():
            if slot not in slots:
                errors.append(f"preset:{preset.get('id')}: missing filtered slot {slot}")
                continue
            valid_ids = {entry.get("id") for entry in slots[slot]}
            for tag_id in flt.get("ids", []):
                if tag_id not in valid_ids:
                    errors.append(f"preset:{preset.get('id')}: unknown {slot} id {tag_id}")


def validate_selection_contracts(data: dict[str, Any], errors: list[str]) -> None:
    slots = data.get("slots", {}) or {}
    for preset in data.get("presets", []) or []:
        preset_id = str(preset.get("id") or "")
        required = preset.get("required_slots")
        if not isinstance(required, list) or not required:
            errors.append(f"preset:{preset_id}: required_slots must be a non-empty list")
            continue
        for slot in required:
            if str(slot) not in slots:
                errors.append(f"preset:{preset_id}: required_slots references unknown slot {slot}")
        try:
            weight = float(preset.get("weight", 1))
        except (TypeError, ValueError):
            errors.append(f"preset:{preset_id}: weight must be numeric")
        else:
            if not 0 < weight <= 5:
                errors.append(f"preset:{preset_id}: weight must be greater than 0 and at most 5")
    for slot, entries in slots.items():
        for entry in entries or []:
            entry_id = str(entry.get("id") or "")
            try:
                weight = float(entry.get("weight", 1))
            except (TypeError, ValueError):
                errors.append(f"slot:{slot}:{entry_id}: weight must be numeric")
            else:
                if not 0 < weight <= 5:
                    errors.append(f"slot:{slot}:{entry_id}: weight must be greater than 0 and at most 5")
            if "requires_primary_any_tags" in entry:
                primary_tags = entry.get("requires_primary_any_tags")
                if not isinstance(primary_tags, list) or not primary_tags or any(not str(tag).strip() for tag in primary_tags):
                    errors.append(
                        f"slot:{slot}:{entry_id}: requires_primary_any_tags must be a non-empty string list"
                    )


def validate_no_text_required_entries(data: dict[str, Any], errors: list[str]) -> None:
    """Require explicit non-readable anchors for text-prone flatlay props and contexts."""
    for label, entry in all_entries(data):
        tags = {str(tag).lower() for tag in normalize_list(entry.get("tags"))}
        if NO_TEXT_REQUIRED_TAG not in tags:
            continue
        text = " ".join(
            [
                str(entry.get("id", "")),
                str(entry.get("en", "")),
                str(entry.get("ko", "")),
                str(entry.get("embedding_text", "")),
                " ".join(str(tag) for tag in normalize_list(entry.get("tags"))),
                " ".join(str(keyword) for keyword in normalize_list(entry.get("keywords"))),
            ]
        ).lower()
        if not any(anchor in text for anchor in NO_TEXT_ANCHOR_TERMS):
            errors.append(f"{label}: no_text_required entries need a blank/unreadable/non-legible/unbranded anchor")


def entry_ids_by_slot(data: dict[str, Any]) -> dict[str, set[str]]:
    return {
        str(slot): {str(entry.get("id")) for entry in entries}
        for slot, entries in (data.get("slots", {}) or {}).items()
    }


def all_known_entry_ids(data: dict[str, Any]) -> set[str]:
    by_slot = entry_ids_by_slot(data)
    all_ids: set[str] = set()
    for ids in by_slot.values():
        all_ids |= ids
    all_ids |= {str(preset.get("id")) for preset in data.get("presets", [])}
    all_ids |= {str(recipe.get("id")) for recipe in data.get("recipes", [])}
    all_ids |= {f"virtual:{recipe.get('id')}" for recipe in data.get("recipes", [])}
    return all_ids


def valid_semantic_families(data: dict[str, Any]) -> set[str]:
    policy = data.get("semantic_policy", {}) or {}
    families = (policy.get("families", {}) or {}) if isinstance(policy, dict) else {}
    return {str(family) for family in families}


def validate_coherence_rules(data: dict[str, Any], errors: list[str]) -> None:
    rules = data.get("coherence_rules", {}) or {}
    if rules and not isinstance(rules, dict):
        errors.append("coherence_rules: must be an object")
        return
    if not rules:
        return

    valid_families = valid_semantic_families(data)
    by_slot = entry_ids_by_slot(data)
    all_ids = all_known_entry_ids(data)

    strengths = rules.get("family_strength", {}) or {}
    if strengths and not isinstance(strengths, dict):
        errors.append("coherence_rules.family_strength: must be an object")
    for family, tiers in strengths.items():
        if family not in valid_families:
            errors.append(f"coherence_rules.family_strength: unknown family {family}")
            continue
        if not isinstance(tiers, dict):
            errors.append(f"coherence_rules.family_strength.{family}: must be an object")
            continue
        strong = set(normalize_list(tiers.get("strong")))
        ambient = set(normalize_list(tiers.get("ambient")))
        if not strong and not ambient:
            errors.append(f"coherence_rules.family_strength.{family}: strong or ambient ids are required")
        overlap = strong & ambient
        if overlap:
            errors.append(f"coherence_rules.family_strength.{family}: ids cannot be both strong and ambient: {sorted(overlap)}")
        for tier, ids in (("strong", strong), ("ambient", ambient)):
            for entry_id in ids:
                if entry_id not in all_ids:
                    errors.append(f"coherence_rules.family_strength.{family}.{tier}: unknown id {entry_id}")

    conflicts = rules.get("family_conflicts", {}) or {}
    if conflicts and not isinstance(conflicts, dict):
        errors.append("coherence_rules.family_conflicts: must be an object")
    for family, slot_map in conflicts.items():
        if family not in valid_families:
            errors.append(f"coherence_rules.family_conflicts: unknown family {family}")
            continue
        if not isinstance(slot_map, dict):
            errors.append(f"coherence_rules.family_conflicts.{family}: must be an object")
            continue
        for slot, ids in slot_map.items():
            if slot not in by_slot:
                errors.append(f"coherence_rules.family_conflicts.{family}: unknown slot {slot}")
                continue
            valid_ids = by_slot[slot]
            for entry_id in normalize_list(ids):
                if entry_id not in valid_ids:
                    errors.append(f"coherence_rules.family_conflicts.{family}.{slot}: unknown id {entry_id}")

    vocab = merged_facet_vocab(data)

    def validate_facet_tokens(label: str, tokens: Any) -> None:
        for token in normalize_list(tokens):
            if ":" not in token:
                errors.append(f"{label}: facet token must be key:value, got {token}")
                continue
            key, value = token.split(":", 1)
            if key not in vocab:
                errors.append(f"{label}: unknown facet key {key}")
            elif value not in vocab[key]:
                errors.append(f"{label}: unknown facet value {token}")

    def validate_side(label: str, side: Any) -> None:
        if not isinstance(side, dict):
            errors.append(f"{label}: must be an object")
            return
        slot = str(side.get("slot") or "")
        if slot not in by_slot:
            errors.append(f"{label}: unknown slot {slot!r}")
            return
        ids = normalize_list(side.get("ids"))
        tokens = normalize_list(side.get("tokens"))
        facets = normalize_list(side.get("facets"))
        if not ids and not tokens and not facets:
            errors.append(f"{label}: requires at least one of ids/tokens/facets")
        for entry_id in ids:
            if entry_id not in by_slot[slot]:
                errors.append(f"{label}: unknown id {entry_id} for slot {slot}")
        validate_facet_tokens(label, facets)

    slot_conflicts = rules.get("slot_conflicts", []) or []
    if slot_conflicts and not isinstance(slot_conflicts, list):
        errors.append("coherence_rules.slot_conflicts: must be a list")
        slot_conflicts = []
    seen_conflict_ids: set[str] = set()
    for index, rule in enumerate(slot_conflicts):
        label = f"coherence_rules.slot_conflicts[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{label}: must be an object")
            continue
        rule_id = str(rule.get("id") or "")
        if not rule_id:
            errors.append(f"{label}: id is required")
        elif rule_id in seen_conflict_ids:
            errors.append(f"{label}: duplicate id {rule_id}")
        else:
            seen_conflict_ids.add(rule_id)
        severity = str(rule.get("severity", "hard"))
        if severity not in {"hard", "soft"}:
            errors.append(f"{label}: severity must be hard or soft, got {severity!r}")
        if severity == "soft":
            try:
                penalty = float(rule.get("penalty", 0.25))
            except (TypeError, ValueError):
                penalty = -1.0
            if not 0.0 < penalty < 1.0:
                errors.append(f"{label}: soft penalty must be in (0, 1)")
        validate_side(f"{label}.left", rule.get("left"))
        validate_side(f"{label}.right", rule.get("right"))

    context_rules = rules.get("slot_context_rules", []) or []
    if context_rules and not isinstance(context_rules, list):
        errors.append("coherence_rules.slot_context_rules: must be a list")
        context_rules = []
    seen_context_ids: set[str] = set()
    for index, rule in enumerate(context_rules):
        label = f"coherence_rules.slot_context_rules[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{label}: must be an object")
            continue
        rule_id = str(rule.get("id") or "")
        if not rule_id:
            errors.append(f"{label}: id is required")
        elif rule_id in seen_context_ids:
            errors.append(f"{label}: duplicate id {rule_id}")
        else:
            seen_context_ids.add(rule_id)
        slots = normalize_list(rule.get("slots"))
        if not slots:
            errors.append(f"{label}: slots is required")
        for slot in slots:
            if slot not in by_slot:
                errors.append(f"{label}: unknown slot {slot}")
        slot_id_union: set[str] = set()
        for slot in slots:
            slot_id_union |= by_slot.get(slot, set())
        for entry_id in normalize_list(rule.get("match_ids")):
            if entry_id not in slot_id_union:
                errors.append(f"{label}: match_ids id {entry_id} not found in slots {slots}")
        validate_facet_tokens(label, rule.get("match_facets"))
        scope = str(rule.get("context_scope", "all"))
        if scope not in {"all", "scene"}:
            errors.append(f"{label}: context_scope must be all or scene, got {scope!r}")
        severity = str(rule.get("severity", "hard"))
        if severity != "hard":
            errors.append(f"{label}: only hard severity is supported for slot_context_rules")
        if not normalize_list(rule.get("requires_context_any")) and not normalize_list(rule.get("requires_item_any")):
            errors.append(f"{label}: requires_context_any or requires_item_any is required")


def validate_semantic_metadata(data: dict[str, Any], errors: list[str]) -> None:
    metadata = data.get("semantic_metadata", {}) or {}
    if metadata and not isinstance(metadata, dict):
        errors.append("semantic_metadata: must be an object")
        return
    if not metadata:
        return

    by_slot = entry_ids_by_slot(data)
    valid_families = valid_semantic_families(data)

    for key, slot in (("subject_groups", "subject"), ("location_tones", "location")):
        groups = metadata.get(key, {}) or {}
        if groups and not isinstance(groups, dict):
            errors.append(f"semantic_metadata.{key}: must be an object")
            continue
        valid_ids = by_slot.get(slot, set())
        for group, ids in groups.items():
            if not str(group):
                errors.append(f"semantic_metadata.{key}: empty group name")
            for entry_id in normalize_list(ids):
                if entry_id not in valid_ids:
                    errors.append(f"semantic_metadata.{key}.{group}: unknown {slot} id {entry_id}")

    axis_signals = metadata.get("axis_signals", {}) or {}
    if axis_signals and not isinstance(axis_signals, dict):
        errors.append("semantic_metadata.axis_signals: must be an object")
    for signal, slot_map in axis_signals.items():
        parts = str(signal).rsplit("_", 1)
        if str(signal) in VALID_AXIS_SIGNAL_ALIASES:
            pass
        elif len(parts) != 2 or parts[0] not in valid_families or parts[1] not in VALID_AXIS_SIGNAL_SUFFIXES:
            errors.append(f"semantic_metadata.axis_signals: invalid signal {signal}")
            continue
        if not isinstance(slot_map, dict):
            errors.append(f"semantic_metadata.axis_signals.{signal}: must be an object")
            continue
        for slot, ids in slot_map.items():
            if slot != "*" and slot not in by_slot:
                errors.append(f"semantic_metadata.axis_signals.{signal}: unknown slot {slot}")
                continue
            valid_ids = set().union(*by_slot.values()) if slot == "*" else by_slot[slot]
            for entry_id in normalize_list(ids):
                if entry_id not in valid_ids:
                    errors.append(f"semantic_metadata.axis_signals.{signal}.{slot}: unknown id {entry_id}")

    tone_conflicts = metadata.get("family_tone_conflicts", {}) or {}
    if tone_conflicts and not isinstance(tone_conflicts, dict):
        errors.append("semantic_metadata.family_tone_conflicts: must be an object")
    known_tones = set((metadata.get("location_tones", {}) or {}).keys())
    for family, config in tone_conflicts.items():
        if family not in valid_families:
            errors.append(f"semantic_metadata.family_tone_conflicts: unknown family {family}")
            continue
        if not isinstance(config, dict):
            errors.append(f"semantic_metadata.family_tone_conflicts.{family}: must be an object")
            continue
        for tone in normalize_list(config.get("location_tone")):
            if tone not in known_tones:
                errors.append(f"semantic_metadata.family_tone_conflicts.{family}.location_tone: unknown tone {tone}")

    cliche_weights = metadata.get("cliche_weights", {}) or {}
    if cliche_weights and not isinstance(cliche_weights, dict):
        errors.append("semantic_metadata.cliche_weights: must be an object")
    for slot, weights in cliche_weights.items():
        if slot not in by_slot:
            errors.append(f"semantic_metadata.cliche_weights: unknown slot {slot}")
            continue
        if not isinstance(weights, dict):
            errors.append(f"semantic_metadata.cliche_weights.{slot}: must be an object")
            continue
        for entry_id, raw_weight in weights.items():
            if str(entry_id) not in by_slot[slot]:
                errors.append(f"semantic_metadata.cliche_weights.{slot}: unknown id {entry_id}")
            try:
                weight = float(raw_weight)
            except (TypeError, ValueError):
                errors.append(f"semantic_metadata.cliche_weights.{slot}.{entry_id}: must be numeric")
                continue
            if not 0.0 <= weight <= 1.0:
                errors.append(f"semantic_metadata.cliche_weights.{slot}.{entry_id}: must be between 0 and 1")


def is_match_rule(value: Any) -> bool:
    return isinstance(value, dict) and bool(set(value.keys()) & VALID_MATCH_RULE_KEYS)


def validate_string_list(label: str, value: Any, errors: list[str]) -> None:
    values = normalize_list(value)
    if not values:
        errors.append(f"{label}: at least one value is required")
    for item in values:
        if not str(item).strip():
            errors.append(f"{label}: empty value")


def validate_match_rule(label: str, rule: Any, errors: list[str]) -> None:
    if isinstance(rule, str):
        if not rule.strip():
            errors.append(f"{label}: empty match term")
        return
    if not isinstance(rule, dict):
        errors.append(f"{label}: must be a string or object")
        return
    for key in rule:
        if key not in VALID_MATCH_RULE_KEYS:
            errors.append(f"{label}: unknown match rule key {key}")
    if not any(normalize_list(rule.get(key)) for key in ("any_terms", "all_terms", "any_tokens", "all_tokens")):
        errors.append(f"{label}: any_terms, all_terms, any_tokens, or all_tokens is required")
    for key in ("any_terms", "all_terms", "any_tokens", "all_tokens"):
        if key in rule:
            validate_string_list(f"{label}.{key}", rule.get(key), errors)
    for key in ("boundary", "case_sensitive"):
        if key in rule and not isinstance(rule.get(key), bool):
            errors.append(f"{label}.{key}: must be a boolean")
    for field in normalize_list(rule.get("match_fields")):
        if field not in VALID_MATCH_FIELDS:
            errors.append(f"{label}.match_fields: unknown field {field}")
    if "id" in rule and not str(rule.get("id") or "").strip():
        errors.append(f"{label}.id: must be non-empty")


def validate_match_rules(label: str, rules: Any, errors: list[str]) -> None:
    if rules is None:
        errors.append(f"{label}: required")
        return
    if isinstance(rules, str) or is_match_rule(rules):
        validate_match_rule(label, rules, errors)
        return
    if isinstance(rules, list):
        if not rules:
            errors.append(f"{label}: at least one rule is required")
        for index, rule in enumerate(rules):
            validate_match_rule(f"{label}[{index}]", rule, errors)
        return
    errors.append(f"{label}: must be a string, object, or list")


def validate_quality_layer_category_terms(label: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict) or not value:
        errors.append(f"{label}: must be a non-empty object")
        return
    for category, terms in value.items():
        if not str(category).strip():
            errors.append(f"{label}: empty category id")
        validate_string_list(f"{label}.{category}", terms, errors)


def validate_quality_layer_suggested_phrases(
    label: str,
    value: Any,
    valid_categories: set[str],
    errors: list[str],
) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return
    for category, phrases in value.items():
        if category not in valid_categories:
            errors.append(f"{label}: unknown category {category}")
            continue
        validate_string_list(f"{label}.{category}", phrases, errors)


def validate_quality_layer_facet_match(
    label: str,
    value: Any,
    vocab: dict[str, set[str]],
    errors: list[str],
) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or not value:
        errors.append(f"{label}: must be a non-empty object")
        return
    for facet, raw_values in value.items():
        facet_key = str(facet)
        if facet_key not in vocab:
            errors.append(f"{label}: unknown facet key {facet_key}")
            continue
        values = normalize_list(raw_values)
        if not values:
            errors.append(f"{label}.{facet_key}: at least one value is required")
            continue
        for facet_value in values:
            if facet_value not in vocab[facet_key]:
                errors.append(f"{label}.{facet_key}: unknown value {facet_value}")


def validate_quality_layer_localized_text(label: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return
    for lang in ("en", "ko"):
        if not str(value.get(lang) or "").strip():
            errors.append(f"{label}.{lang}: required")
    for key, text in value.items():
        if key not in {"en", "ko"}:
            errors.append(f"{label}.{key}: unsupported localized key")
        if not str(text or "").strip():
            errors.append(f"{label}.{key}: empty value")


def quality_layer_craft_has_blocked_entity(text: str, blocked: str) -> bool:
    lowered = text.lower()
    blocked_lower = blocked.lower()
    if re.search(r"[A-Za-z0-9]", blocked_lower):
        if " " in blocked_lower:
            return blocked_lower in lowered
        tokens = set(re.findall(r"[a-z0-9][a-z0-9-]*", lowered))
        return blocked_lower in tokens
    return blocked_lower in lowered


def validate_quality_layer_craft_text(label: str, value: Any, errors: list[str]) -> None:
    texts: list[str] = []
    if isinstance(value, dict):
        texts.extend(str(item) for item in value.values() if str(item).strip())
    elif isinstance(value, list):
        texts.extend(str(item) for item in value if str(item).strip())
    elif value is not None and str(value).strip():
        texts.append(str(value))
    for text in texts:
        for blocked in PHOTOGRAPHIC_CRAFT_ENTITY_BLOCKLIST:
            if quality_layer_craft_has_blocked_entity(text, blocked):
                errors.append(f"{label}: blocked scene-specific craft term {blocked}")


def validate_quality_layer_photographic_craft(
    quality: dict[str, Any],
    vocab: dict[str, set[str]],
    errors: list[str],
) -> None:
    craft = quality.get("photographic_craft")
    if not isinstance(craft, dict):
        errors.append("quality_layers.photographic_craft: must be an object")
        return
    if "enabled" in craft and not isinstance(craft.get("enabled"), bool):
        errors.append("quality_layers.photographic_craft.enabled: must be a boolean")
    source = str(craft.get("source") or "").strip()
    if not source:
        errors.append("quality_layers.photographic_craft.source: required")
    profile_ids = {
        str(profile_id)
        for profile_id in (quality.get("quality_profiles") or {})
        if str(profile_id).strip()
    }
    for integer_key, minimum, maximum in (
        ("prompt_dimension_limit", 1, 3),
        ("refinement_limit_per_dimension", 0, 4),
    ):
        try:
            value = int(craft.get(integer_key))
        except (TypeError, ValueError):
            errors.append(f"quality_layers.photographic_craft.{integer_key}: must be an integer")
            continue
        if value < minimum or value > maximum:
            errors.append(f"quality_layers.photographic_craft.{integer_key}: must be between {minimum} and {maximum}")

    dimensions = craft.get("dimensions") or []
    if not isinstance(dimensions, list) or not dimensions:
        errors.append("quality_layers.photographic_craft.dimensions: must be a non-empty list")
        dimensions = []
    if len(dimensions) > 12:
        errors.append("quality_layers.photographic_craft.dimensions: must contain at most 12 dimensions")
    seen_dimension_ids: set[str] = set()
    for index, dimension in enumerate(dimensions):
        label = f"quality_layers.photographic_craft.dimensions[{index}]"
        if not isinstance(dimension, dict):
            errors.append(f"{label}: must be an object")
            continue
        if "terms" in dimension:
            errors.append(f"{label}.terms: not allowed; use facet_match refinements only")
        dimension_id = str(dimension.get("id") or "").strip()
        if not dimension_id:
            errors.append(f"{label}.id: required")
        elif dimension_id in seen_dimension_ids:
            errors.append(f"{label}.id: duplicate id {dimension_id}")
        else:
            seen_dimension_ids.add(dimension_id)
        for text_key in ("id", "label", "baseline_principle"):
            if text_key in dimension:
                validate_quality_layer_craft_text(f"{label}.{text_key}", dimension.get(text_key), errors)
        if not str(dimension.get("baseline_principle") or "").strip():
            errors.append(f"{label}.baseline_principle: required")
        validate_quality_layer_localized_text(f"{label}.guidance", dimension.get("guidance"), errors)
        validate_quality_layer_craft_text(f"{label}.guidance", dimension.get("guidance"), errors)
        validate_string_list(f"{label}.audit_terms", dimension.get("audit_terms"), errors)
        validate_quality_layer_craft_text(f"{label}.audit_terms", dimension.get("audit_terms"), errors)
        refinements = dimension.get("refinements") or []
        if refinements and not isinstance(refinements, list):
            errors.append(f"{label}.refinements: must be a list")
            refinements = []
        if len(refinements) > 8:
            errors.append(f"{label}.refinements: must contain at most 8 refinements")
        seen_refinement_ids: set[str] = set()
        for refinement_index, refinement in enumerate(refinements):
            refinement_label = f"{label}.refinements[{refinement_index}]"
            if not isinstance(refinement, dict):
                errors.append(f"{refinement_label}: must be an object")
                continue
            if "terms" in refinement:
                errors.append(f"{refinement_label}.terms: not allowed; use facet_match only")
            refinement_id = str(refinement.get("id") or "").strip()
            if not refinement_id:
                errors.append(f"{refinement_label}.id: required")
            elif refinement_id in seen_refinement_ids:
                errors.append(f"{refinement_label}.id: duplicate id {refinement_id}")
            else:
                seen_refinement_ids.add(refinement_id)
            validate_quality_layer_facet_match(f"{refinement_label}.facet_match", refinement.get("facet_match"), vocab, errors)
            if "profile_match" in refinement:
                validate_string_list(f"{refinement_label}.profile_match", refinement.get("profile_match"), errors)
                for profile_id in normalize_list(refinement.get("profile_match")):
                    if profile_id not in profile_ids:
                        errors.append(f"{refinement_label}.profile_match: unknown quality profile {profile_id}")
            if not str(refinement.get("principle") or "").strip():
                errors.append(f"{refinement_label}.principle: required")
            for text_key in ("id", "principle"):
                if text_key in refinement:
                    validate_quality_layer_craft_text(f"{refinement_label}.{text_key}", refinement.get(text_key), errors)
            validate_quality_layer_localized_text(f"{refinement_label}.guidance", refinement.get("guidance"), errors)
            validate_quality_layer_craft_text(f"{refinement_label}.guidance", refinement.get("guidance"), errors)
            validate_string_list(f"{refinement_label}.audit_terms", refinement.get("audit_terms"), errors)
            validate_quality_layer_craft_text(f"{refinement_label}.audit_terms", refinement.get("audit_terms"), errors)

    strategies = craft.get("strategies") or []
    if not isinstance(strategies, list) or not strategies:
        errors.append("quality_layers.photographic_craft.strategies: must be a non-empty list")
        strategies = []
    seen_strategy_ids: set[str] = set()
    for index, strategy in enumerate(strategies):
        label = f"quality_layers.photographic_craft.strategies[{index}]"
        if not isinstance(strategy, dict):
            errors.append(f"{label}: must be an object")
            continue
        strategy_id = str(strategy.get("id") or "").strip()
        if not strategy_id:
            errors.append(f"{label}.id: required")
        elif strategy_id in seen_strategy_ids:
            errors.append(f"{label}.id: duplicate id {strategy_id}")
        else:
            seen_strategy_ids.add(strategy_id)
        for text_key in ("id", "label"):
            if text_key in strategy:
                validate_quality_layer_craft_text(f"{label}.{text_key}", strategy.get(text_key), errors)
        if "profile_match" in strategy:
            validate_string_list(f"{label}.profile_match", strategy.get("profile_match"), errors)
            for profile_id in normalize_list(strategy.get("profile_match")):
                if profile_id not in profile_ids:
                    errors.append(f"{label}.profile_match: unknown quality profile {profile_id}")
        emphasize = normalize_list(strategy.get("emphasize"))
        if not emphasize:
            errors.append(f"{label}.emphasize: at least one dimension id is required")
        for dimension_id in emphasize:
            if dimension_id not in seen_dimension_ids:
                errors.append(f"{label}.emphasize: unknown dimension id {dimension_id}")
    default_strategy = str(craft.get("default_strategy") or "").strip()
    if default_strategy and default_strategy not in seen_strategy_ids:
        errors.append("quality_layers.photographic_craft.default_strategy: unknown strategy id")


def validate_quality_layer_artistic_final_touch(quality: dict[str, Any], errors: list[str]) -> None:
    touch = quality.get("artistic_final_touch")
    if touch is None:
        return
    if not isinstance(touch, dict):
        errors.append("quality_layers.artistic_final_touch: must be an object")
        return
    if "enabled" in touch and not isinstance(touch.get("enabled"), bool):
        errors.append("quality_layers.artistic_final_touch.enabled: must be a boolean")
    if "default_enabled" in touch and not isinstance(touch.get("default_enabled"), bool):
        errors.append("quality_layers.artistic_final_touch.default_enabled: must be a boolean")
    profiles = quality.get("quality_profiles") if isinstance(quality.get("quality_profiles"), dict) else {}
    for profile_id in normalize_list(touch.get("enabled_profiles")):
        if profile_id not in profiles:
            errors.append(f"quality_layers.artistic_final_touch.enabled_profiles: unknown profile {profile_id}")
    source = str(touch.get("source") or "").strip()
    if not source:
        errors.append("quality_layers.artistic_final_touch.source: required")
    sentences = touch.get("sentences")
    if not isinstance(sentences, dict):
        errors.append("quality_layers.artistic_final_touch.sentences: must be an object")
        sentences = {}
    for lang in ("en", "ko"):
        localized = sentences.get(lang)
        label = f"quality_layers.artistic_final_touch.sentences.{lang}"
        if not isinstance(localized, dict):
            errors.append(f"{label}: must be an object")
            continue
        default_sentence = str(localized.get("default") or "").strip()
        if not default_sentence:
            errors.append(f"{label}.default: required")
        for key, value in localized.items():
            if key not in {"default", "compact", "detailed", "standard"}:
                errors.append(f"{label}.{key}: unsupported sentence variant")
            if not str(value or "").strip():
                errors.append(f"{label}.{key}: empty value")
    if "audit_terms" in touch:
        validate_string_list("quality_layers.artistic_final_touch.audit_terms", touch.get("audit_terms"), errors)


def validate_quality_layer_intent_routing(
    quality: dict[str, Any], data: dict[str, Any], errors: list[str]
) -> None:
    routing = quality.get("intent_routing")
    if not isinstance(routing, dict):
        errors.append("quality_layers.intent_routing: must be an object")
        return
    for key in routing:
        if key not in {
            "subject_categories",
            "domains",
            "scoped_routes",
            "literal_subject_stop_terms",
        }:
            errors.append(f"quality_layers.intent_routing: unknown key {key}")
    if "literal_subject_stop_terms" in routing:
        validate_string_list(
            "quality_layers.intent_routing.literal_subject_stop_terms",
            routing.get("literal_subject_stop_terms"),
            errors,
        )

    configured_categories: set[str] = set()
    categories = routing.get("subject_categories")
    if not isinstance(categories, list) or not categories:
        errors.append("quality_layers.intent_routing.subject_categories: must be a non-empty list")
        categories = []
    for index, row in enumerate(categories):
        label = f"quality_layers.intent_routing.subject_categories[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be an object")
            continue
        for key in row:
            if key not in {"category", "aliases"}:
                errors.append(f"{label}: unknown key {key}")
        category = str(row.get("category") or "").strip()
        if category not in VALID_SUBJECT_CATEGORIES:
            errors.append(f"{label}.category: unknown subject category {category!r}")
        elif category in configured_categories:
            errors.append(f"{label}.category: duplicate category {category}")
        else:
            configured_categories.add(category)
        validate_string_list(f"{label}.aliases", row.get("aliases"), errors)

    configured_domains: set[str] = set()
    domains = routing.get("domains")
    if not isinstance(domains, list) or not domains:
        errors.append("quality_layers.intent_routing.domains: must be a non-empty list")
        domains = []
    for index, row in enumerate(domains):
        label = f"quality_layers.intent_routing.domains[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be an object")
            continue
        for key in row:
            if key not in {"domain", "aliases"}:
                errors.append(f"{label}: unknown key {key}")
        domain = str(row.get("domain") or "").strip()
        if domain not in VALID_PRESET_DOMAINS:
            errors.append(f"{label}.domain: unknown preset domain {domain!r}")
        elif domain in configured_domains:
            errors.append(f"{label}.domain: duplicate domain {domain}")
        else:
            configured_domains.add(domain)
        validate_string_list(f"{label}.aliases", row.get("aliases"), errors)

    scoped_routes = routing.get("scoped_routes", [])
    if not isinstance(scoped_routes, list):
        errors.append("quality_layers.intent_routing.scoped_routes: must be a list")
        scoped_routes = []
    preset_ids = {
        str(preset.get("id"))
        for preset in data.get("presets", [])
        if isinstance(preset, dict) and str(preset.get("id") or "")
    }
    configured_routes: set[tuple[str, str]] = set()
    for index, row in enumerate(scoped_routes):
        label = f"quality_layers.intent_routing.scoped_routes[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be an object")
            continue
        for key in row:
            if key not in {"domain", "preset_id", "aliases"}:
                errors.append(f"{label}: unknown key {key}")
        domain = str(row.get("domain") or "").strip()
        preset_id = str(row.get("preset_id") or "").strip()
        if domain not in VALID_PRESET_DOMAINS:
            errors.append(f"{label}.domain: unknown preset domain {domain!r}")
        if preset_id not in preset_ids:
            errors.append(f"{label}.preset_id: unknown preset id {preset_id!r}")
        route_key = (domain, preset_id)
        if route_key in configured_routes:
            errors.append(f"{label}: duplicate scoped route {domain}:{preset_id}")
        else:
            configured_routes.add(route_key)
        validate_string_list(f"{label}.aliases", row.get("aliases"), errors)


def validate_quality_layer_selection_balance(quality: dict[str, Any], errors: list[str]) -> None:
    balance = quality.get("selection_balance")
    if not isinstance(balance, dict):
        errors.append("quality_layers.selection_balance: must be an object")
        return
    for key in balance:
        if key not in {"implicit_theme_multiplier", "request_relevance", "themes"}:
            errors.append(f"quality_layers.selection_balance: unknown key {key}")
    try:
        multiplier = float(balance.get("implicit_theme_multiplier"))
    except (TypeError, ValueError):
        errors.append("quality_layers.selection_balance.implicit_theme_multiplier: must be numeric")
    else:
        if not 0.0 < multiplier <= 1.0:
            errors.append("quality_layers.selection_balance.implicit_theme_multiplier: must be greater than 0 and at most 1")
    relevance = balance.get("request_relevance")
    if not isinstance(relevance, dict):
        errors.append("quality_layers.selection_balance.request_relevance: must be an object")
    else:
        for key in relevance:
            if key not in {
                "enabled",
                "per_term_multiplier",
                "max_multiplier",
                "minimum_term_length",
                "deterministic_minimum_matches",
                "deterministic_minimum_lead",
            }:
                errors.append(f"quality_layers.selection_balance.request_relevance: unknown key {key}")
        if not isinstance(relevance.get("enabled"), bool):
            errors.append("quality_layers.selection_balance.request_relevance.enabled: must be boolean")
        for key in ("per_term_multiplier", "max_multiplier"):
            try:
                value = float(relevance.get(key))
            except (TypeError, ValueError):
                errors.append(f"quality_layers.selection_balance.request_relevance.{key}: must be numeric")
            else:
                if value <= 0:
                    errors.append(f"quality_layers.selection_balance.request_relevance.{key}: must be greater than 0")
        try:
            minimum_term_length = int(relevance.get("minimum_term_length"))
        except (TypeError, ValueError):
            errors.append("quality_layers.selection_balance.request_relevance.minimum_term_length: must be an integer")
        else:
            if minimum_term_length < 2:
                errors.append("quality_layers.selection_balance.request_relevance.minimum_term_length: must be at least 2")
        for key in ("deterministic_minimum_matches", "deterministic_minimum_lead"):
            try:
                value = int(relevance.get(key))
            except (TypeError, ValueError):
                errors.append(f"quality_layers.selection_balance.request_relevance.{key}: must be an integer")
            else:
                if value < 1:
                    errors.append(f"quality_layers.selection_balance.request_relevance.{key}: must be at least 1")
    themes = balance.get("themes")
    if not isinstance(themes, dict) or not themes:
        errors.append("quality_layers.selection_balance.themes: must be a non-empty object")
        return
    for theme, aliases in themes.items():
        label = f"quality_layers.selection_balance.themes.{theme}"
        if not str(theme).strip():
            errors.append("quality_layers.selection_balance.themes: empty theme id")
        validate_string_list(label, aliases, errors)


def validate_quality_layer_applicability_guards(quality: dict[str, Any], errors: list[str]) -> None:
    guards = quality.get("applicability_guards")
    if not isinstance(guards, list) or not guards:
        errors.append("quality_layers.applicability_guards: must be a non-empty list")
        return
    seen_ids: set[str] = set()
    for index, guard in enumerate(guards):
        label = f"quality_layers.applicability_guards[{index}]"
        if not isinstance(guard, dict):
            errors.append(f"{label}: must be an object")
            continue
        for key in guard:
            if key not in {
                "id",
                "match_any_tags",
                "match_any_terms",
                "slots",
                "exclude_slots",
                "requires_primary_any_tags",
            }:
                errors.append(f"{label}: unknown key {key}")
        guard_id = str(guard.get("id") or "").strip()
        if not guard_id:
            errors.append(f"{label}.id: required")
        elif guard_id in seen_ids:
            errors.append(f"{label}.id: duplicate id {guard_id}")
        else:
            seen_ids.add(guard_id)
        validate_string_list(f"{label}.match_any_tags", guard.get("match_any_tags"), errors)
        if "match_any_terms" in guard:
            validate_string_list(f"{label}.match_any_terms", guard.get("match_any_terms"), errors)
        validate_string_list(f"{label}.requires_primary_any_tags", guard.get("requires_primary_any_tags"), errors)
        if "slots" in guard:
            validate_string_list(f"{label}.slots", guard.get("slots"), errors)
        if "exclude_slots" in guard:
            validate_string_list(f"{label}.exclude_slots", guard.get("exclude_slots"), errors)


def validate_quality_layers(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    try:
        quality = load_json(path)
    except FileNotFoundError:
        errors.append(f"quality_layers: missing file {path}")
        return
    except json.JSONDecodeError as exc:
        errors.append(f"quality_layers: invalid JSON: {exc}")
        return
    if not isinstance(quality, dict):
        errors.append("quality_layers: must be an object")
        return
    try:
        schema_version = int(quality.get("schema_version"))
    except (TypeError, ValueError):
        errors.append("quality_layers.schema_version: must be 1 or 2")
        schema_version = None
    if schema_version not in {1, 2}:
        errors.append("quality_layers.schema_version: must be 1 or 2")
    profiles = quality.get("quality_profiles", {}) or {}
    if schema_version == 2 and (not isinstance(profiles, dict) or not profiles):
        errors.append("quality_layers.quality_profiles: must be a non-empty object for schema 2")
    if schema_version == 2:
        validate_quality_layer_intent_routing(quality, data, errors)
        validate_quality_layer_applicability_guards(quality, errors)
        validate_quality_layer_selection_balance(quality, errors)
    validate_quality_layer_artistic_final_touch(quality, errors)
    vocab = merged_facet_vocab(data)
    validate_quality_layer_photographic_craft(quality, vocab, errors)

    photographic = quality.get("photographic_integration")
    if not isinstance(photographic, dict):
        errors.append("quality_layers.photographic_integration: must be an object")
        photographic = {}
    categories = photographic.get("categories") if isinstance(photographic, dict) else {}
    validate_quality_layer_category_terms("quality_layers.photographic_integration.categories", categories, errors)
    valid_categories = {str(category) for category in categories} if isinstance(categories, dict) else set()
    baseline = photographic.get("baseline") if isinstance(photographic, dict) else {}
    if not isinstance(baseline, dict):
        errors.append("quality_layers.photographic_integration.baseline: must be an object")
        baseline = {}
    validate_string_list("quality_layers.photographic_integration.baseline.required_categories", baseline.get("required_categories"), errors)
    for category in normalize_list(baseline.get("required_categories")):
        if category not in valid_categories:
            errors.append(f"quality_layers.photographic_integration.baseline.required_categories: unknown category {category}")
    validate_string_list("quality_layers.photographic_integration.baseline.principles", baseline.get("principles"), errors)
    validate_quality_layer_suggested_phrases(
        "quality_layers.photographic_integration.baseline.suggested_phrases",
        baseline.get("suggested_phrases"),
        valid_categories,
        errors,
    )
    if "minimum_category_hits" in baseline:
        try:
            minimum = int(baseline.get("minimum_category_hits"))
        except (TypeError, ValueError):
            errors.append("quality_layers.photographic_integration.baseline.minimum_category_hits: must be an integer")
        else:
            if minimum < 1:
                errors.append("quality_layers.photographic_integration.baseline.minimum_category_hits: must be at least 1")

    axes = photographic.get("axes") if isinstance(photographic, dict) else []
    if not isinstance(axes, list) or not axes:
        errors.append("quality_layers.photographic_integration.axes: must be a non-empty list")
        axes = []
    seen_axis_ids: set[str] = set()
    profile_ids = {str(profile_id) for profile_id in profiles if str(profile_id).strip()}
    for index, axis in enumerate(axes):
        label = f"quality_layers.photographic_integration.axes[{index}]"
        if not isinstance(axis, dict):
            errors.append(f"{label}: must be an object")
            continue
        axis_id = str(axis.get("id") or "")
        if not axis_id:
            errors.append(f"{label}.id: required")
        elif axis_id in seen_axis_ids:
            errors.append(f"{label}.id: duplicate id {axis_id}")
        else:
            seen_axis_ids.add(axis_id)
        validate_quality_layer_facet_match(f"{label}.facet_match", axis.get("facet_match"), vocab, errors)
        if "profile_match" in axis:
            validate_string_list(f"{label}.profile_match", axis.get("profile_match"), errors)
            for profile_id in normalize_list(axis.get("profile_match")):
                if profile_id not in profile_ids:
                    errors.append(f"{label}.profile_match: unknown quality profile {profile_id}")
        validate_string_list(f"{label}.terms", axis.get("terms"), errors)
        validate_string_list(f"{label}.required_categories", axis.get("required_categories"), errors)
        for category in normalize_list(axis.get("required_categories")):
            if category not in valid_categories:
                errors.append(f"{label}.required_categories: unknown category {category}")
        validate_string_list(f"{label}.principles", axis.get("principles"), errors)
        validate_quality_layer_suggested_phrases(
            f"{label}.suggested_phrases",
            axis.get("suggested_phrases"),
            valid_categories,
            errors,
        )

    proposition = quality.get("visual_proposition")
    if not isinstance(proposition, dict):
        errors.append("quality_layers.visual_proposition: must be an object")
        proposition = {}
    by_slot = entry_ids_by_slot(data)
    proposition_slots = normalize_list(proposition.get("slots"))
    if not proposition_slots:
        errors.append("quality_layers.visual_proposition.slots: at least one slot is required")
    for slot in proposition_slots:
        if slot not in by_slot:
            errors.append(f"quality_layers.visual_proposition.slots: unknown slot {slot}")
    try:
        candidate_limit = int(proposition.get("candidate_limit", 3))
    except (TypeError, ValueError):
        errors.append("quality_layers.visual_proposition.candidate_limit: must be an integer")
    else:
        if candidate_limit < 1:
            errors.append("quality_layers.visual_proposition.candidate_limit: must be at least 1")

    subject_classes = proposition.get("subject_classes") or []
    if not isinstance(subject_classes, list) or not subject_classes:
        errors.append("quality_layers.visual_proposition.subject_classes: must be a non-empty list")
        subject_classes = []
    seen_class_ids: set[str] = set()
    for index, subject_class in enumerate(subject_classes):
        label = f"quality_layers.visual_proposition.subject_classes[{index}]"
        if not isinstance(subject_class, dict):
            errors.append(f"{label}: must be an object")
            continue
        class_id = str(subject_class.get("id") or "")
        if not class_id:
            errors.append(f"{label}.id: required")
        elif class_id in seen_class_ids:
            errors.append(f"{label}.id: duplicate id {class_id}")
        else:
            seen_class_ids.add(class_id)
        validate_quality_layer_facet_match(f"{label}.facet_match", subject_class.get("facet_match"), vocab, errors)
        validate_string_list(f"{label}.terms", subject_class.get("terms"), errors)
        if str(subject_class.get("core_policy", "allow")) not in {"allow", "contextual", "none"}:
            errors.append(f"{label}.core_policy: must be allow, contextual, or none")

    registers = proposition.get("registers") or {}
    if not isinstance(registers, dict) or not registers:
        errors.append("quality_layers.visual_proposition.registers: must be a non-empty object")
        registers = {}
    for register, policy in registers.items():
        label = f"quality_layers.visual_proposition.registers.{register}"
        if not isinstance(policy, dict):
            errors.append(f"{label}: must be an object")
            continue
        if "terms" in policy:
            for term in normalize_list(policy.get("terms")):
                if not str(term).strip():
                    errors.append(f"{label}.terms: empty value")
        validate_quality_layer_facet_match(f"{label}.facet_match", policy.get("facet_match"), vocab, errors)
        try:
            minimum = int(policy.get("minimum_hits", 1))
        except (TypeError, ValueError):
            errors.append(f"{label}.minimum_hits: must be an integer")
        else:
            if minimum < 0:
                errors.append(f"{label}.minimum_hits: must be non-negative")
        validate_string_list(f"{label}.principles", policy.get("principles"), errors)

    fallback = proposition.get("fallback") or {}
    if not isinstance(fallback, dict):
        errors.append("quality_layers.visual_proposition.fallback: must be an object")
        fallback = {}
    for slot, ids in fallback.items():
        if slot not in by_slot:
            errors.append(f"quality_layers.visual_proposition.fallback: unknown slot {slot}")
            continue
        for entry_id in normalize_list(ids):
            if entry_id not in by_slot[slot]:
                errors.append(f"quality_layers.visual_proposition.fallback.{slot}: unknown id {entry_id}")
    validate_string_list("quality_layers.visual_proposition.evidence_terms", proposition.get("evidence_terms"), errors)
    validate_string_list("quality_layers.visual_proposition.anti_patterns", proposition.get("anti_patterns"), errors)


def validate_semantic_policy(data: dict[str, Any], errors: list[str]) -> None:
    policy = data.get("semantic_policy", {}) or {}
    if policy and not isinstance(policy, dict):
        errors.append("semantic_policy: must be an object")
        return
    if not policy:
        return
    try:
        schema_version = int(policy.get("schema_version"))
    except (TypeError, ValueError):
        errors.append("semantic_policy.schema_version: must be 1")
        schema_version = None
    if schema_version != 1:
        errors.append("semantic_policy.schema_version: must be 1")

    soft_body_guard = policy.get("soft_body_first_guard", {}) or {}
    by_slot = entry_ids_by_slot(data)
    vocab = merged_facet_vocab(data)
    if soft_body_guard:
        if not isinstance(soft_body_guard, dict):
            errors.append("semantic_policy.soft_body_first_guard: must be an object")
        else:
            slot = str(soft_body_guard.get("slot") or "")
            if slot and slot not in by_slot:
                errors.append(f"semantic_policy.soft_body_first_guard.slot: unknown slot {slot}")
            for guard_slot in normalize_list(soft_body_guard.get("slots")):
                if guard_slot not in by_slot:
                    errors.append(f"semantic_policy.soft_body_first_guard.slots: unknown slot {guard_slot}")
            for token in normalize_list(soft_body_guard.get("demote_facets")):
                validate_guard_token("semantic_policy.soft_body_first_guard.demote_facets", token, vocab, errors)
            for token in normalize_list(soft_body_guard.get("prefer_facets")):
                validate_guard_token("semantic_policy.soft_body_first_guard.prefer_facets", token, vocab, errors)
            if "demote_multiplier" in soft_body_guard:
                try:
                    value = float(soft_body_guard.get("demote_multiplier"))
                except (TypeError, ValueError):
                    errors.append("semantic_policy.soft_body_first_guard.demote_multiplier: must be numeric")
                else:
                    if not 0.0 <= value <= 1.0:
                        errors.append("semantic_policy.soft_body_first_guard.demote_multiplier: must be between 0 and 1")
            per_slot_multiplier = soft_body_guard.get("per_slot_multiplier") or {}
            if per_slot_multiplier and not isinstance(per_slot_multiplier, dict):
                errors.append("semantic_policy.soft_body_first_guard.per_slot_multiplier: must be an object")
            elif isinstance(per_slot_multiplier, dict):
                for multiplier_slot, raw_value in per_slot_multiplier.items():
                    if multiplier_slot not in by_slot:
                        errors.append(f"semantic_policy.soft_body_first_guard.per_slot_multiplier: unknown slot {multiplier_slot}")
                        continue
                    try:
                        value = float(raw_value)
                    except (TypeError, ValueError):
                        errors.append(f"semantic_policy.soft_body_first_guard.per_slot_multiplier.{multiplier_slot}: must be numeric")
                    else:
                        if not 0.0 <= value <= 1.0:
                            errors.append(f"semantic_policy.soft_body_first_guard.per_slot_multiplier.{multiplier_slot}: must be between 0 and 1")

    soft_diversity = policy.get("soft_anchor_diversity", {}) or {}
    if soft_diversity:
        if not isinstance(soft_diversity, dict):
            errors.append("semantic_policy.soft_anchor_diversity: must be an object")
        else:
            for key in ("candidate_probability_floor", "max_single_candidate_probability", "batch_repeat_decay", "ledger_repeat_decay"):
                if key in soft_diversity:
                    try:
                        value = float(soft_diversity.get(key))
                    except (TypeError, ValueError):
                        errors.append(f"semantic_policy.soft_anchor_diversity.{key}: must be numeric")
                        continue
                    if not 0.0 <= value <= 1.0:
                        errors.append(f"semantic_policy.soft_anchor_diversity.{key}: must be between 0 and 1")

    families = policy.get("families", {}) or {}
    if not isinstance(families, dict):
        errors.append("semantic_policy.families: must be an object")
        return

    for family in normalize_list(policy.get("steering_priority")):
        if family not in families:
            errors.append(f"semantic_policy.steering_priority: unknown family {family}")

    all_ids = all_known_entry_ids(data)
    valid_signal_tiers = {"core", "support", "strong", "ambient"}

    for family, config in families.items():
        family_label = f"semantic_policy.families.{family}"
        if not isinstance(config, dict):
            errors.append(f"{family_label}: must be an object")
            continue
        if not str(config.get("policy_id") or "").strip():
            errors.append(f"{family_label}.policy_id: required")
        if not (normalize_list(config.get("keywords")) or normalize_list(config.get("aliases"))):
            errors.append(f"{family_label}: keywords or aliases are required")
        for key in ("axis_label", "axis_embedding_text"):
            if not str(config.get(key) or "").strip():
                errors.append(f"{family_label}.{key}: required")
        for key in ("routed_slots", "steering_slots"):
            for slot in normalize_list(config.get(key)):
                if slot not in by_slot:
                    errors.append(f"{family_label}.{key}: unknown slot {slot}")

        signal_lexicon = config.get("signal_lexicon", {}) or {}
        if signal_lexicon and not isinstance(signal_lexicon, dict):
            errors.append(f"{family_label}.signal_lexicon: must be an object")
        elif isinstance(signal_lexicon, dict):
            for tier, rules in signal_lexicon.items():
                if tier not in {"strong", "ambient"}:
                    errors.append(f"{family_label}.signal_lexicon: unknown tier {tier}")
                    continue
                validate_match_rules(f"{family_label}.signal_lexicon.{tier}", rules, errors)

        reason_labels = config.get("steering_reason_labels", {}) or {}
        if reason_labels and not isinstance(reason_labels, dict):
            errors.append(f"{family_label}.steering_reason_labels: must be an object")
        elif isinstance(reason_labels, dict):
            for slot, label in reason_labels.items():
                if slot not in by_slot:
                    errors.append(f"{family_label}.steering_reason_labels: unknown slot {slot}")
                if not str(label or "").strip():
                    errors.append(f"{family_label}.steering_reason_labels.{slot}: must be non-empty")

        preset_policy = config.get("preset_policy", {}) or {}
        if preset_policy and not isinstance(preset_policy, dict):
            errors.append(f"{family_label}.preset_policy: must be an object")
        elif isinstance(preset_policy, dict):
            allow_ids = set(normalize_list(preset_policy.get("allow_ids")))
            deny_ids = set(normalize_list(preset_policy.get("deny_ids")))
            overlap = allow_ids & deny_ids
            if overlap:
                errors.append(f"{family_label}.preset_policy: allow/deny overlap {sorted(overlap)}")
            for key, ids in (("allow_ids", allow_ids), ("deny_ids", deny_ids)):
                for entry_id in ids:
                    if entry_id not in all_ids:
                        errors.append(f"{family_label}.preset_policy.{key}: unknown id {entry_id}")

        slot_signals = config.get("slot_signals", {}) or {}
        if slot_signals and not isinstance(slot_signals, dict):
            errors.append(f"{family_label}.slot_signals: must be an object")
        elif isinstance(slot_signals, dict):
            for slot, tiers in slot_signals.items():
                slot_label = f"{family_label}.slot_signals.{slot}"
                if slot not in by_slot:
                    errors.append(f"{family_label}.slot_signals: unknown slot {slot}")
                    continue
                if not isinstance(tiers, dict):
                    errors.append(f"{slot_label}: must be an object")
                    continue
                term_rules = tiers.get("term_rules", {}) or {}
                if term_rules and not isinstance(term_rules, dict):
                    errors.append(f"{slot_label}.term_rules: must be an object")
                elif isinstance(term_rules, dict):
                    for tier, rules in term_rules.items():
                        if tier not in valid_signal_tiers:
                            errors.append(f"{slot_label}.term_rules: unknown tier {tier}")
                            continue
                        validate_match_rules(f"{slot_label}.term_rules.{tier}", rules, errors)
                tier_sets = {
                    tier: set(normalize_list(ids))
                    for tier, ids in tiers.items()
                    if tier != "term_rules"
                }
                for tier, ids in tier_sets.items():
                    if tier not in valid_signal_tiers:
                        errors.append(f"{slot_label}: unknown tier {tier}")
                        continue
                    for entry_id in ids:
                        if entry_id not in by_slot[slot]:
                            errors.append(f"{slot_label}.{tier}: unknown {slot} id {entry_id}")
                if tier_sets.get("core", set()) & tier_sets.get("support", set()):
                    errors.append(f"{slot_label}: ids cannot be both core and support")

        slot_defaults = config.get("slot_signal_defaults", {}) or {}
        if slot_defaults and not isinstance(slot_defaults, dict):
            errors.append(f"{family_label}.slot_signal_defaults: must be an object")
        elif isinstance(slot_defaults, dict):
            for tier, rules in slot_defaults.items():
                if tier not in valid_signal_tiers:
                    errors.append(f"{family_label}.slot_signal_defaults: unknown tier {tier}")
                    continue
                validate_match_rules(f"{family_label}.slot_signal_defaults.{tier}", rules, errors)

        promotions = config.get("concept_lock_promotions", {}) or {}
        if promotions and not isinstance(promotions, dict):
            errors.append(f"{family_label}.concept_lock_promotions: must be an object")
        elif isinstance(promotions, dict):
            for slot, rules in promotions.items():
                if slot not in by_slot:
                    errors.append(f"{family_label}.concept_lock_promotions: unknown slot {slot}")
                    continue
                if not isinstance(rules, list):
                    errors.append(f"{family_label}.concept_lock_promotions.{slot}: must be a list")
                    continue
                for index, rule in enumerate(rules):
                    rule_label = f"{family_label}.concept_lock_promotions.{slot}[{index}]"
                    if not isinstance(rule, dict):
                        errors.append(f"{rule_label}: must be an object")
                        continue
                    if not normalize_list(rule.get("terms")):
                        errors.append(f"{rule_label}.terms: required")
                    ids = normalize_list(rule.get("ids"))
                    if not ids:
                        errors.append(f"{rule_label}.ids: required")
                    for entry_id in ids:
                        if entry_id not in by_slot[slot]:
                            errors.append(f"{rule_label}.ids: unknown {slot} id {entry_id}")

        redundancy_rules = config.get("redundancy_rules", []) or []
        if redundancy_rules and not isinstance(redundancy_rules, list):
            errors.append(f"{family_label}.redundancy_rules: must be a list")
        elif isinstance(redundancy_rules, list):
            for index, rule in enumerate(redundancy_rules):
                rule_label = f"{family_label}.redundancy_rules[{index}]"
                if not isinstance(rule, dict):
                    errors.append(f"{rule_label}: must be an object")
                    continue
                when_slot = str(rule.get("when_slot") or "")
                when_id = str(rule.get("when_id") or "")
                if when_slot not in by_slot:
                    errors.append(f"{rule_label}.when_slot: unknown slot {when_slot}")
                elif when_id not in by_slot[when_slot]:
                    errors.append(f"{rule_label}.when_id: unknown {when_slot} id {when_id}")
                suppress = rule.get("suppress", {}) or {}
                if not isinstance(suppress, dict):
                    errors.append(f"{rule_label}.suppress: must be an object")
                    continue
                for slot, ids in suppress.items():
                    if slot not in by_slot:
                        errors.append(f"{rule_label}.suppress: unknown slot {slot}")
                        continue
                    for entry_id in normalize_list(ids):
                        if entry_id not in by_slot[slot]:
                            errors.append(f"{rule_label}.suppress.{slot}: unknown id {entry_id}")

        repair = config.get("coverage_repair", {}) or {}
        if repair and not isinstance(repair, dict):
            errors.append(f"{family_label}.coverage_repair: must be an object")
        elif isinstance(repair, dict):
            for slot in normalize_list(repair.get("target_slots")):
                if slot not in by_slot:
                    errors.append(f"{family_label}.coverage_repair.target_slots: unknown slot {slot}")
            for entry_id in normalize_list(repair.get("anchor_ids")):
                if entry_id not in all_ids:
                    errors.append(f"{family_label}.coverage_repair.anchor_ids: unknown id {entry_id}")
            if "min_anchors" in repair:
                try:
                    int(repair.get("min_anchors"))
                except (TypeError, ValueError):
                    errors.append(f"{family_label}.coverage_repair.min_anchors: must be an integer")


def parse_forced_set(raw: str) -> tuple[str, list[str]] | None:
    if "=" not in raw:
        return None
    slot, ids_raw = raw.split("=", 1)
    slot = slot.strip()
    ids = [item.strip() for item in ids_raw.replace("|", ",").split(",") if item.strip()]
    if not slot or not ids:
        return None
    return slot, ids


def validate_recipe_set(label: str, set_value: Any, by_slot: dict[str, set[str]], errors: list[str]) -> None:
    if not set_value:
        return
    forced_items: list[tuple[str, list[str]]] = []
    if isinstance(set_value, dict):
        forced_items = [(str(slot), normalize_list(ids)) for slot, ids in set_value.items()]
    else:
        for raw in normalize_list(set_value):
            parsed = parse_forced_set(raw)
            if parsed is None:
                errors.append(f"{label}.set: invalid forced set {raw}")
                continue
            forced_items.append(parsed)
    for slot, ids in forced_items:
        if slot not in by_slot:
            errors.append(f"{label}.set: unknown slot {slot}")
            continue
        for entry_id in ids:
            if entry_id not in by_slot[slot]:
                errors.append(f"{label}.set.{slot}: unknown id {entry_id}")


def validate_recipe_slot_list(label: str, field: str, value: Any, by_slot: dict[str, set[str]], errors: list[str]) -> None:
    for slot in normalize_list(value):
        if slot not in by_slot:
            errors.append(f"{label}.{field}: unknown slot {slot}")


def validate_anchor_families(label: str, recipe: dict[str, Any], by_slot: dict[str, set[str]], errors: list[str]) -> None:
    families = recipe.get("anchor_families") or {}
    if families and not isinstance(families, dict):
        errors.append(f"{label}.anchor_families: must be an object")
        return
    if not isinstance(families, dict):
        return
    for family, spec in families.items():
        family_label = f"{label}.anchor_families.{family}"
        if not str(family).strip():
            errors.append(f"{label}.anchor_families: empty family name")
        if not isinstance(spec, dict):
            errors.append(f"{family_label}: must be an object")
            continue
        slots = normalize_list(spec.get("slots"))
        terms = normalize_list(spec.get("terms"))
        if not slots and not terms:
            errors.append(f"{family_label}: slots or terms are required")
        for slot in slots:
            if slot not in by_slot:
                errors.append(f"{family_label}.slots: unknown slot {slot}")
        if "min_hits" in spec and (not isinstance(spec.get("min_hits"), int) or spec.get("min_hits") < 1):
            errors.append(f"{family_label}.min_hits: must be a positive integer")


def validate_forbidden_slot_values(label: str, recipe: dict[str, Any], by_slot: dict[str, set[str]], errors: list[str]) -> None:
    forbidden = recipe.get("forbidden_slot_values") or {}
    if forbidden and not isinstance(forbidden, dict):
        errors.append(f"{label}.forbidden_slot_values: must be an object")
        return
    if not isinstance(forbidden, dict):
        return
    for slot, ids in forbidden.items():
        if slot not in by_slot:
            errors.append(f"{label}.forbidden_slot_values: unknown slot {slot}")
            continue
        for entry_id in normalize_list(ids):
            if entry_id not in by_slot[slot]:
                errors.append(f"{label}.forbidden_slot_values.{slot}: unknown id {entry_id}")


def validate_conditional_additional(label: str, recipe: dict[str, Any], by_slot: dict[str, set[str]], errors: list[str]) -> None:
    rules = recipe.get("conditional_additional")
    if rules is None:
        return
    if not isinstance(rules, list):
        errors.append(f"{label}.conditional_additional: must be a list")
        return
    for index, rule in enumerate(rules):
        rule_label = f"{label}.conditional_additional[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{rule_label}: must be an object")
            continue
        if not (normalize_list(rule.get("text")) or normalize_list(rule.get("additional"))):
            errors.append(f"{rule_label}: text or additional is required")
        for bool_key in ("requires_role", "requires_bundle"):
            if bool_key in rule and not isinstance(rule.get(bool_key), bool):
                errors.append(f"{rule_label}.{bool_key}: must be a boolean")
        validate_recipe_slot_list(rule_label, "unless_user_set_slots_any", rule.get("unless_user_set_slots_any"), by_slot, errors)


def validate_concept_recipe_entry(
    label: str,
    recipe: dict[str, Any],
    data: dict[str, Any],
    errors: list[str],
) -> None:
    by_slot = entry_ids_by_slot(data)
    preset_ids = {str(preset.get("id")) for preset in data.get("presets", [])}
    preset = str(recipe.get("preset") or "")
    if preset and preset not in preset_ids:
        errors.append(f"{label}.preset: unknown preset {preset}")
    if "register" in recipe and not isinstance(recipe.get("register"), bool):
        errors.append(f"{label}.register: must be a boolean")
    validate_recipe_set(label, recipe.get("set"), by_slot, errors)
    identity_core = recipe.get("identity_core")
    if identity_core is not None:
        if not isinstance(identity_core, dict) or not identity_core:
            errors.append(f"{label}.identity_core: must be a non-empty object")
        else:
            validate_recipe_set(f"{label}.identity_core", identity_core, by_slot, errors)
    scene_variants = recipe.get("scene_variants")
    if scene_variants is not None:
        if not isinstance(scene_variants, list) or len(scene_variants) < 2:
            errors.append(f"{label}.scene_variants: must contain at least two variants")
        else:
            seen_scene_ids: set[str] = set()
            for index, variant in enumerate(scene_variants):
                variant_label = f"{label}.scene_variants[{index}]"
                if not isinstance(variant, dict):
                    errors.append(f"{variant_label}: must be an object")
                    continue
                variant_id = str(variant.get("id") or "").strip()
                if not variant_id:
                    errors.append(f"{variant_label}.id: required")
                elif variant_id in seen_scene_ids:
                    errors.append(f"{variant_label}.id: duplicate id {variant_id}")
                seen_scene_ids.add(variant_id)
                try:
                    weight = float(variant.get("weight", 1))
                except (TypeError, ValueError):
                    weight = 0.0
                if weight <= 0:
                    errors.append(f"{variant_label}.weight: must be greater than 0")
                validate_recipe_set(variant_label, variant.get("set"), by_slot, errors)
    validate_recipe_slot_list(label, "override_slots", recipe.get("override_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "bundle_override_slots", recipe.get("bundle_override_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "soft_anchor_slots", recipe.get("soft_anchor_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "soft_free_slots", recipe.get("soft_free_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "critical_anchor_slots", recipe.get("critical_anchor_slots"), by_slot, errors)
    validate_anchor_families(label, recipe, by_slot, errors)
    validate_forbidden_slot_values(label, recipe, by_slot, errors)
    concept_mode_default = recipe.get("concept_mode_default")
    if concept_mode_default is not None and str(concept_mode_default) not in {"legacy", "soft"}:
        errors.append(f"{label}.concept_mode_default: must be legacy or soft")
    validate_anchor_expansion(label, recipe.get("anchor_expansion"), errors)
    validate_concept_guide(label, recipe.get("guide"), errors)
    validate_reference_scaffold_schema(label, recipe, by_slot, errors)
    validate_review_gates_schema(label, recipe.get("review_gates"), by_slot, errors)

    def weighted_pool_ids(pool_label: str, value: Any) -> list[str]:
        """Pools accept plain id strings and {"id", "w"} objects."""
        ids: list[str] = []
        raw_items = value if isinstance(value, list) else normalize_list(value)
        for item in raw_items:
            if isinstance(item, dict):
                entry_id = str(item.get("id") or "").strip()
                if not entry_id:
                    errors.append(f"{pool_label}: weighted pool entry requires id")
                    continue
                ids.append(entry_id)
                raw_weight = item.get("w", 1.0)
                try:
                    weight = float(raw_weight)
                except (TypeError, ValueError):
                    weight = -1.0
                if weight <= 0:
                    errors.append(f"{pool_label}: weighted pool entry {entry_id} requires w > 0")
            else:
                entry_id = str(item).strip()
                if entry_id:
                    ids.append(entry_id)
        return ids

    anchor_pool = recipe.get("anchor_pool") or {}
    if anchor_pool and not isinstance(anchor_pool, dict):
        errors.append(f"{label}.anchor_pool: must be an object")
    elif isinstance(anchor_pool, dict):
        for slot, ids in anchor_pool.items():
            if slot not in by_slot:
                errors.append(f"{label}.anchor_pool: unknown slot {slot}")
                continue
            for entry_id in weighted_pool_ids(f"{label}.anchor_pool.{slot}", ids):
                if entry_id not in by_slot[slot]:
                    errors.append(f"{label}.anchor_pool.{slot}: unknown id {entry_id}")
    primary_anchor_pool = recipe.get("primary_anchor_pool") or {}
    if primary_anchor_pool and not isinstance(primary_anchor_pool, dict):
        errors.append(f"{label}.primary_anchor_pool: must be an object")
    elif isinstance(primary_anchor_pool, dict):
        for slot, ids in primary_anchor_pool.items():
            if slot not in by_slot:
                errors.append(f"{label}.primary_anchor_pool: unknown slot {slot}")
                continue
            for entry_id in weighted_pool_ids(f"{label}.primary_anchor_pool.{slot}", ids):
                if entry_id not in by_slot[slot]:
                    errors.append(f"{label}.primary_anchor_pool.{slot}: unknown id {entry_id}")
                if slot == "prop" and entry_id == "angel_halo_wings_tail_set" and "천사" in label:
                    errors.append(f"{label}.primary_anchor_pool.{slot}: angel soft primary pool must use tail-free halo/wings prop")
    anchor_variants = recipe.get("anchor_variants") or {}
    if anchor_variants and not isinstance(anchor_variants, dict):
        errors.append(f"{label}.anchor_variants: must be an object")
    elif isinstance(anchor_variants, dict):
        for slot, variant in anchor_variants.items():
            variant_label = f"{label}.anchor_variants.{slot}"
            if slot not in by_slot:
                errors.append(f"{label}.anchor_variants: unknown slot {slot}")
                continue
            if not isinstance(variant, dict):
                errors.append(f"{variant_label}: must be an object")
                continue
            if not str(variant.get("group") or "").strip():
                errors.append(f"{variant_label}.group: required")
            options = normalize_list(variant.get("options"))
            if len(options) < 2:
                errors.append(f"{variant_label}.options: at least two values are required")
            for entry_id in options:
                if entry_id not in by_slot[slot]:
                    errors.append(f"{variant_label}.options: unknown id {entry_id}")
                if slot == "prop" and entry_id == "angel_halo_wings_tail_set" and "천사" in label:
                    errors.append(f"{variant_label}.options: angel soft variants must use tail-free halo/wings prop")
            if "select" in variant and str(variant.get("select")) not in {"seed_rotate", "weighted"}:
                errors.append(f"{variant_label}.select: must be seed_rotate or weighted")
    anchor_terms = recipe.get("anchor_terms") or {}
    if anchor_terms and not isinstance(anchor_terms, dict):
        errors.append(f"{label}.anchor_terms: must be an object")
    elif isinstance(anchor_terms, dict):
        for slot, terms in anchor_terms.items():
            if slot not in by_slot:
                errors.append(f"{label}.anchor_terms: unknown slot {slot}")
            for term in normalize_list(terms):
                if not str(term).strip():
                    errors.append(f"{label}.anchor_terms.{slot}: empty term")
    anchor_floor = recipe.get("anchor_floor") or {}
    if anchor_floor and not isinstance(anchor_floor, dict):
        errors.append(f"{label}.anchor_floor: must be an object")
    elif isinstance(anchor_floor, dict):
        for source, value in anchor_floor.items():
            if str(source) not in {"role", "mixin", "bundle"}:
                errors.append(f"{label}.anchor_floor: unknown source {source}")
            if not isinstance(value, int) or value < 0:
                errors.append(f"{label}.anchor_floor.{source}: must be a non-negative integer")
    anchor_group_floor = recipe.get("anchor_group_floor") or {}
    if anchor_group_floor and not isinstance(anchor_group_floor, dict):
        errors.append(f"{label}.anchor_group_floor: must be an object")
    elif isinstance(anchor_group_floor, dict):
        for group, value in anchor_group_floor.items():
            if not str(group).strip():
                errors.append(f"{label}.anchor_group_floor: empty group")
            if not isinstance(value, int) or value < 0:
                errors.append(f"{label}.anchor_group_floor.{group}: must be a non-negative integer")
    anchor_groups = recipe.get("anchor_groups") or {}
    if anchor_groups and not isinstance(anchor_groups, dict):
        errors.append(f"{label}.anchor_groups: must be an object")
    elif isinstance(anchor_groups, dict):
        for slot, groups in anchor_groups.items():
            if slot not in by_slot:
                errors.append(f"{label}.anchor_groups: unknown slot {slot}")
            for group in normalize_list(groups):
                if not str(group).strip():
                    errors.append(f"{label}.anchor_groups.{slot}: empty group")
    visual_guard = recipe.get("visual_guard")
    guards = [visual_guard] if isinstance(visual_guard, dict) else (visual_guard or [])
    if visual_guard is not None and not isinstance(visual_guard, (dict, list)):
        errors.append(f"{label}.visual_guard: must be an object or list")
    elif isinstance(guards, list):
        for index, guard in enumerate(guards):
            guard_label = f"{label}.visual_guard[{index}]"
            if not isinstance(guard, dict):
                errors.append(f"{guard_label}: must be an object")
                continue
            for key in ("deny_ids", "prefer_ids"):
                raw_map = guard.get(key) or {}
                if raw_map and not isinstance(raw_map, dict):
                    errors.append(f"{guard_label}.{key}: must be an object")
                    continue
                for slot, ids in raw_map.items():
                    if slot not in by_slot:
                        errors.append(f"{guard_label}.{key}: unknown slot {slot}")
                        continue
                    for entry_id in normalize_list(ids):
                        if entry_id not in by_slot[slot]:
                            errors.append(f"{guard_label}.{key}.{slot}: unknown id {entry_id}")
            raw_facets = guard.get("deny_facets") or {}
            if raw_facets and not isinstance(raw_facets, dict):
                errors.append(f"{guard_label}.deny_facets: must be an object")
            elif isinstance(raw_facets, dict):
                vocab = merged_facet_vocab(data)
                for slot, tokens in raw_facets.items():
                    if slot not in by_slot:
                        errors.append(f"{guard_label}.deny_facets: unknown slot {slot}")
                        continue
                    for token in normalize_list(tokens):
                        validate_guard_token(f"{guard_label}.deny_facets.{slot}", token, vocab, errors)
    render_priority_terms = recipe.get("render_priority_terms")
    term_groups = [render_priority_terms] if isinstance(render_priority_terms, dict) else (render_priority_terms or [])
    if render_priority_terms is not None and not isinstance(render_priority_terms, (dict, list, str)):
        errors.append(f"{label}.render_priority_terms: must be a string, object, or list")
    elif isinstance(term_groups, list):
        for index, group in enumerate(term_groups):
            if isinstance(group, dict):
                if not normalize_list(group.get("terms")):
                    errors.append(f"{label}.render_priority_terms[{index}].terms: required")
                if "min_hits" in group and (not isinstance(group.get("min_hits"), int) or group.get("min_hits") < 1):
                    errors.append(f"{label}.render_priority_terms[{index}].min_hits: must be a positive integer")
                if "tier" in group and str(group.get("tier")) not in {"required", "support"}:
                    errors.append(f"{label}.render_priority_terms[{index}].tier: must be required or support")
                if "group" in group and not str(group.get("group") or "").strip():
                    errors.append(f"{label}.render_priority_terms[{index}].group: must be non-empty")
                validate_recipe_slot_list(
                    f"{label}.render_priority_terms[{index}]",
                    "target_slots",
                    group.get("target_slots"),
                    by_slot,
                    errors,
                )
            elif not normalize_list(group):
                errors.append(f"{label}.render_priority_terms[{index}]: empty value")
    if "soft_min_anchors" in recipe and (not isinstance(recipe.get("soft_min_anchors"), int) or recipe.get("soft_min_anchors") < 0):
        errors.append(f"{label}.soft_min_anchors: must be a non-negative integer")
    if "mixin_cue_budget" in recipe and (not isinstance(recipe.get("mixin_cue_budget"), int) or recipe.get("mixin_cue_budget") < 0):
        errors.append(f"{label}.mixin_cue_budget: must be a non-negative integer")
    free_slot_constraints = recipe.get("free_slot_constraints") or {}
    if free_slot_constraints and not isinstance(free_slot_constraints, dict):
        errors.append(f"{label}.free_slot_constraints: must be an object")
    elif isinstance(free_slot_constraints, dict):
        for slot, constraint in free_slot_constraints.items():
            constraint_label = f"{label}.free_slot_constraints.{slot}"
            if slot not in by_slot:
                errors.append(f"{label}.free_slot_constraints: unknown slot {slot}")
                continue
            if not isinstance(constraint, dict):
                errors.append(f"{constraint_label}: must be an object")
                continue
            for key in ("allow_pool", "deny_pool", "prefer_ids"):
                for entry_id in normalize_list(constraint.get(key)):
                    if entry_id not in by_slot[slot]:
                        errors.append(f"{constraint_label}.{key}: unknown id {entry_id}")
    render_suppress_terms = recipe.get("render_suppress_terms")
    if render_suppress_terms is not None and not isinstance(render_suppress_terms, (list, str)):
        errors.append(f"{label}.render_suppress_terms: must be a string or list of strings")
    for term in normalize_list(render_suppress_terms):
        if not str(term).strip():
            errors.append(f"{label}.render_suppress_terms: empty value")
    safety_negative_floor = recipe.get("safety_negative_floor")
    if safety_negative_floor is not None and not isinstance(safety_negative_floor, (list, str)):
        errors.append(f"{label}.safety_negative_floor: must be a string or list of strings")
    for term in normalize_list(safety_negative_floor):
        if not str(term).strip():
            errors.append(f"{label}.safety_negative_floor: empty value")
    soft_repair_policy = recipe.get("soft_repair_policy") or {}
    if soft_repair_policy and not isinstance(soft_repair_policy, dict):
        errors.append(f"{label}.soft_repair_policy: must be an object")
    elif isinstance(soft_repair_policy, dict):
        if "max_attempts" in soft_repair_policy and (
            not isinstance(soft_repair_policy.get("max_attempts"), int) or soft_repair_policy.get("max_attempts") < 0
        ):
            errors.append(f"{label}.soft_repair_policy.max_attempts: must be a non-negative integer")
        if "enabled" in soft_repair_policy and not isinstance(soft_repair_policy.get("enabled"), bool):
            errors.append(f"{label}.soft_repair_policy.enabled: must be a boolean")
        if "fail_open" in soft_repair_policy and not isinstance(soft_repair_policy.get("fail_open"), bool):
            errors.append(f"{label}.soft_repair_policy.fail_open: must be a boolean")
        if "strategy" in soft_repair_policy and str(soft_repair_policy.get("strategy")) not in {"prefer_then_reselect"}:
            errors.append(f"{label}.soft_repair_policy.strategy: must be prefer_then_reselect")
        for check in normalize_list(soft_repair_policy.get("trigger_checks")):
            if check not in {
                "required_render_priority_missing",
                "dual_read_missing",
                "body_first_survivor",
                "free_slot_constraint_violation",
            }:
                errors.append(f"{label}.soft_repair_policy.trigger_checks: unknown check {check}")
        validate_recipe_slot_list(label, "soft_repair_policy.target_slots", soft_repair_policy.get("target_slots"), by_slot, errors)
    render_directives = recipe.get("render_directives")
    directive_items = [render_directives] if isinstance(render_directives, dict) else (render_directives or [])
    if render_directives is not None and not isinstance(render_directives, (dict, list)):
        errors.append(f"{label}.render_directives: must be an object or list")
    elif isinstance(directive_items, list):
        for index, directive in enumerate(directive_items):
            directive_label = f"{label}.render_directives[{index}]"
            if not isinstance(directive, dict):
                errors.append(f"{directive_label}: must be an object")
                continue
            if not normalize_list(directive.get("cue_terms")):
                errors.append(f"{directive_label}.cue_terms: required")
            for term in normalize_list(directive.get("cue_terms")):
                if not str(term).strip():
                    errors.append(f"{directive_label}.cue_terms: empty value")
            if not str(directive.get("positive_clause") or "").strip():
                errors.append(f"{directive_label}.positive_clause: required")
            for term in normalize_list(directive.get("suppress_terms")):
                if not str(term).strip():
                    errors.append(f"{directive_label}.suppress_terms: empty value")
    dual_read = recipe.get("dual_read_requirement") or {}
    if dual_read and not isinstance(dual_read, dict):
        errors.append(f"{label}.dual_read_requirement: must be an object")
    elif isinstance(dual_read, dict):
        if "enabled" in dual_read and not isinstance(dual_read.get("enabled"), bool):
            errors.append(f"{label}.dual_read_requirement.enabled: must be a boolean")
        for key in ("role_terms", "mixin_terms"):
            for term in normalize_list(dual_read.get(key)):
                if not str(term).strip():
                    errors.append(f"{label}.dual_read_requirement.{key}: empty value")
        for key in ("min_role_hits", "min_mixin_hits"):
            if key in dual_read and (not isinstance(dual_read.get(key), int) or dual_read.get(key) < 1):
                errors.append(f"{label}.dual_read_requirement.{key}: must be a positive integer")
    preset_affinity = recipe.get("preset_affinity") or {}
    if preset_affinity and not isinstance(preset_affinity, dict):
        errors.append(f"{label}.preset_affinity: must be an object")
    elif isinstance(preset_affinity, dict):
        for key in ("preferred_presets", "discouraged_presets"):
            for preset_id in normalize_list(preset_affinity.get(key)):
                if preset_id not in preset_ids:
                    errors.append(f"{label}.preset_affinity.{key}: unknown preset {preset_id}")
        for key in ("preferred_axes", "discouraged_axes"):
            for axis in normalize_list(preset_affinity.get(key)):
                if not str(axis).strip():
                    errors.append(f"{label}.preset_affinity.{key}: empty value")
    for key in ("safety_requirements", "salience_cues"):
        raw = recipe.get(key)
        if raw is not None and not isinstance(raw, (list, str)):
            errors.append(f"{label}.{key}: must be a string or list of strings")
        for item in normalize_list(raw):
            if not str(item).strip():
                errors.append(f"{label}.{key}: empty value")
    validate_conditional_additional(label, recipe, by_slot, errors)


def validate_species_variants(label: str, recipe: dict[str, Any], data: dict[str, Any], errors: list[str]) -> None:
    config = recipe.get("species_variants")
    if config is None:
        return
    if not isinstance(config, dict):
        errors.append(f"{label}.species_variants: must be an object")
        return
    variants = config.get("variants", []) or []
    if not isinstance(variants, list):
        errors.append(f"{label}.species_variants.variants: must be a list")
        return
    allowed_tiers = {"default_safe", "guarded_safe", "opt_in"}
    seen_ids: set[str] = set()
    for index, variant in enumerate(variants):
        variant_label = f"{label}.species_variants.variants[{index}]"
        if not isinstance(variant, dict):
            errors.append(f"{variant_label}: must be an object")
            continue
        variant_id = str(variant.get("id") or "").strip()
        if not variant_id:
            errors.append(f"{variant_label}.id: required")
        elif variant_id in seen_ids:
            errors.append(f"{variant_label}.id: duplicate id {variant_id}")
        seen_ids.add(variant_id)
        tier = str(variant.get("tier") or "default_safe")
        if tier not in allowed_tiers:
            errors.append(f"{variant_label}.tier: must be one of {sorted(allowed_tiers)}")
        if tier == "opt_in" and not normalize_list(variant.get("aliases")):
            errors.append(f"{variant_label}.aliases: opt_in variants require at least one alias")
        if "weight" in variant:
            try:
                float(variant.get("weight"))
            except (TypeError, ValueError):
                errors.append(f"{variant_label}.weight: must be numeric")
        validate_concept_recipe_entry(variant_label, variant, data, errors)


REVIEW_GATE_ASSERT_TYPES = {
    "mixin_shape",
    "forced_slot_any",
    "forced_slot_absent",
    "bundle_selected",
    "role_costume_preserved",
}


def validate_concept_guide(label: str, guide: Any, errors: list[str]) -> None:
    if guide is None:
        return
    if not isinstance(guide, dict):
        errors.append(f"{label}.guide: must be an object")
        return
    definition = guide.get("definition_ko")
    if not isinstance(definition, str) or not definition.strip():
        errors.append(f"{label}.guide.definition_ko: non-empty string is required")
    for key in ("dominant_axes", "anti_patterns"):
        value = guide.get(key)
        if value is None:
            continue
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            errors.append(f"{label}.guide.{key}: must be a list of non-empty strings")


def validate_reference_scaffold_schema(
    label: str,
    recipe: dict[str, Any],
    by_slot: dict[str, set[str]],
    errors: list[str],
) -> None:
    identity_axes = recipe.get("identity_axes")
    if identity_axes is not None:
        raw_axes = identity_axes.get("required") if isinstance(identity_axes, dict) else identity_axes
        if not isinstance(raw_axes, list):
            errors.append(f"{label}.identity_axes: must be a list or object with required")
        else:
            seen_axes: set[str] = set()
            for index, axis in enumerate(raw_axes):
                axis_label = f"{label}.identity_axes[{index}]"
                if isinstance(axis, str):
                    if not axis.strip():
                        errors.append(f"{axis_label}: empty axis")
                    continue
                if not isinstance(axis, dict):
                    errors.append(f"{axis_label}: must be a string or object")
                    continue
                axis_id = str(axis.get("id") or axis.get("axis") or "").strip()
                if not axis_id:
                    errors.append(f"{axis_label}.id: required")
                elif axis_id in seen_axes:
                    errors.append(f"{axis_label}.id: duplicate {axis_id}")
                else:
                    seen_axes.add(axis_id)
                for term in normalize_list(axis.get("terms")):
                    if not term.strip():
                        errors.append(f"{axis_label}.terms: empty term")

    motif_pools = recipe.get("motif_pools")
    if motif_pools is not None:
        if not isinstance(motif_pools, dict):
            errors.append(f"{label}.motif_pools: must be an object")
        else:
            for motif, pool in motif_pools.items():
                motif_id = str(motif or "").strip()
                pool_label = f"{label}.motif_pools.{motif_id or '<empty>'}"
                if not motif_id:
                    errors.append(f"{label}.motif_pools: empty motif id")
                    continue
                if not isinstance(pool, dict):
                    errors.append(f"{pool_label}: must be an object")
                    continue
                if "axis" in pool and not str(pool.get("axis") or "").strip():
                    errors.append(f"{pool_label}.axis: empty value")
                slot_candidates = pool.get("slot_candidates") or {}
                if slot_candidates and not isinstance(slot_candidates, dict):
                    errors.append(f"{pool_label}.slot_candidates: must be an object")
                elif isinstance(slot_candidates, dict):
                    for slot, ids in slot_candidates.items():
                        slot_label = f"{pool_label}.slot_candidates.{slot}"
                        if slot not in by_slot:
                            errors.append(f"{pool_label}.slot_candidates: unknown slot {slot}")
                            continue
                        values = normalize_list(ids)
                        if not values:
                            errors.append(f"{slot_label}: at least one id is required")
                            continue
                        for entry_id in values:
                            if entry_id not in by_slot[slot]:
                                errors.append(f"{slot_label}: unknown id {entry_id}")
                if "terms" in pool and not normalize_list(pool.get("terms")):
                    errors.append(f"{pool_label}.terms: at least one term is required when present")

    motif_quotas = recipe.get("motif_quotas")
    if motif_quotas is not None:
        if not isinstance(motif_quotas, dict):
            errors.append(f"{label}.motif_quotas: must be an object")
        else:
            for motif, quota in motif_quotas.items():
                quota_label = f"{label}.motif_quotas.{motif}"
                if not str(motif or "").strip():
                    errors.append(f"{label}.motif_quotas: empty motif id")
                    continue
                if isinstance(quota, (int, float)):
                    if not 0 <= float(quota) <= 1:
                        errors.append(f"{quota_label}: numeric quota must be between 0 and 1")
                    continue
                if not isinstance(quota, dict):
                    errors.append(f"{quota_label}: must be an object or number")
                    continue
                for key in ("max_batch_share", "max_recent_share"):
                    if key in quota:
                        try:
                            value = float(quota.get(key))
                        except (TypeError, ValueError):
                            errors.append(f"{quota_label}.{key}: must be numeric")
                            continue
                        if not 0 <= value <= 1:
                            errors.append(f"{quota_label}.{key}: must be between 0 and 1")
                for key in ("max_batch_uses", "max_recent_uses"):
                    if key in quota and (not isinstance(quota.get(key), int) or quota.get(key) < 0):
                        errors.append(f"{quota_label}.{key}: must be a non-negative integer")
                if "avoid_when_pressure" in quota and not isinstance(quota.get("avoid_when_pressure"), bool):
                    errors.append(f"{quota_label}.avoid_when_pressure: must be a boolean")

    semantic_dropout = recipe.get("semantic_dropout")
    if semantic_dropout is not None:
        if not isinstance(semantic_dropout, dict):
            errors.append(f"{label}.semantic_dropout: must be an object")
        else:
            if "enabled" in semantic_dropout and not isinstance(semantic_dropout.get("enabled"), bool):
                errors.append(f"{label}.semantic_dropout.enabled: must be a boolean")
            for bucket in normalize_list(semantic_dropout.get("maskable_buckets")):
                if bucket not in {"environment", "action_prop", "camera_composition", "style_finish"}:
                    errors.append(f"{label}.semantic_dropout.maskable_buckets: unknown bucket {bucket}")
            for key in ("min_buckets", "max_buckets"):
                if key in semantic_dropout and (
                    not isinstance(semantic_dropout.get(key), int) or semantic_dropout.get(key) < 0
                ):
                    errors.append(f"{label}.semantic_dropout.{key}: must be a non-negative integer")
            if "probability" in semantic_dropout:
                try:
                    probability = float(semantic_dropout.get("probability"))
                except (TypeError, ValueError):
                    errors.append(f"{label}.semantic_dropout.probability: must be numeric")
                else:
                    if not 0 <= probability <= 1:
                        errors.append(f"{label}.semantic_dropout.probability: must be between 0 and 1")

    exemplar_set = recipe.get("exemplar_set")
    if exemplar_set is not None and not isinstance(exemplar_set, (dict, list, str)):
        errors.append(f"{label}.exemplar_set: must be an object, list, or string")


def validate_review_gates_schema(
    label: str,
    gates: Any,
    by_slot: dict[str, set[str]],
    errors: list[str],
) -> None:
    if gates is None:
        return
    if not isinstance(gates, list):
        errors.append(f"{label}.review_gates: must be a list")
        return
    seen: set[str] = set()
    for index, gate in enumerate(gates):
        gate_label = f"{label}.review_gates[{index}]"
        if not isinstance(gate, dict):
            errors.append(f"{gate_label}: must be an object")
            continue
        gate_id = str(gate.get("id") or "")
        if not gate_id:
            errors.append(f"{gate_label}: id is required")
        elif gate_id in seen:
            errors.append(f"{gate_label}: duplicate id {gate_id}")
        else:
            seen.add(gate_id)
        if not str(gate.get("check") or "").strip():
            errors.append(f"{gate_label}: check description is required")
        machine = gate.get("machine_checkable")
        if machine is not None and not isinstance(machine, bool):
            errors.append(f"{gate_label}: machine_checkable must be a boolean")
        spec = gate.get("assert")
        if not machine:
            continue
        if not isinstance(spec, dict):
            errors.append(f"{gate_label}: machine_checkable gate requires an assert object")
            continue
        assert_type = str(spec.get("type") or "")
        if assert_type not in REVIEW_GATE_ASSERT_TYPES:
            errors.append(f"{gate_label}.assert: unknown type {assert_type!r}")
            continue
        if assert_type in {"mixin_shape", "bundle_selected"} and not str(spec.get("mixin") or "").strip():
            errors.append(f"{gate_label}.assert: mixin is required for {assert_type}")
        if assert_type in {"forced_slot_any", "forced_slot_absent"}:
            slot = str(spec.get("slot") or "")
            if slot not in by_slot:
                errors.append(f"{gate_label}.assert: unknown slot {slot!r}")
                continue
            id_key = "any_of" if assert_type == "forced_slot_any" else "values"
            for entry_id in normalize_list(spec.get(id_key)):
                if entry_id not in by_slot[slot]:
                    errors.append(f"{gate_label}.assert.{id_key}: unknown id {entry_id} for slot {slot}")


def validate_anchor_expansion(label: str, config: Any, errors: list[str]) -> None:
    if config is None:
        return
    if not isinstance(config, dict):
        errors.append(f"{label}.anchor_expansion: must be an object")
        return
    if "enabled" in config and not isinstance(config.get("enabled"), bool):
        errors.append(f"{label}.anchor_expansion.enabled: must be a boolean")
    if "top_k" in config:
        try:
            top_k = int(config.get("top_k"))
        except (TypeError, ValueError):
            top_k = -1
        if top_k < 1:
            errors.append(f"{label}.anchor_expansion.top_k: must be an integer >= 1")
    if "min_similarity" in config:
        try:
            min_similarity = float(config.get("min_similarity"))
        except (TypeError, ValueError):
            min_similarity = -1.0
        if not 0.0 < min_similarity <= 1.0:
            errors.append(f"{label}.anchor_expansion.min_similarity: must be in (0, 1]")
    if "weight_ratio" in config:
        try:
            weight_ratio = float(config.get("weight_ratio"))
        except (TypeError, ValueError):
            weight_ratio = -1.0
        if not 0.0 < weight_ratio <= 1.0:
            errors.append(f"{label}.anchor_expansion.weight_ratio: must be in (0, 1]")
    unknown = set(config) - {"enabled", "top_k", "min_similarity", "weight_ratio"}
    if unknown:
        errors.append(f"{label}.anchor_expansion: unknown keys {sorted(unknown)}")


def validate_concept_recipes(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    if not path.exists():
        return
    try:
        recipes = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"concept_recipes: invalid JSON: {exc}")
        return
    if not isinstance(recipes, dict):
        errors.append("concept_recipes: must be an object")
        return
    by_slot = entry_ids_by_slot(data)
    validate_recipe_slot_list("concept_recipes", "bundle_override_slots", recipes.get("bundle_override_slots"), by_slot, errors)
    validate_recipe_slot_list("concept_recipes", "override_slots", recipes.get("override_slots"), by_slot, errors)

    defaults = recipes.get("soft_anchor_defaults", {}) or {}
    if isinstance(defaults, dict):
        validate_anchor_expansion("concept_recipes.soft_anchor_defaults", defaults.get("anchor_expansion"), errors)

    concept_safety = recipes.get("concept_safety", {}) or {}
    if concept_safety and not isinstance(concept_safety, dict):
        errors.append("concept_recipes.concept_safety: must be an object")
    elif isinstance(concept_safety, dict):
        for pool, terms in concept_safety.items():
            if not str(pool).strip():
                errors.append("concept_recipes.concept_safety: empty pool name")
            normalized_terms = normalize_list(terms)
            if not normalized_terms:
                errors.append(f"concept_recipes.concept_safety.{pool}: at least one term is required")
            for term in normalized_terms:
                if not str(term).strip():
                    errors.append(f"concept_recipes.concept_safety.{pool}: empty term")

    aliases = recipes.get("aliases", {}) or {}
    if aliases and not isinstance(aliases, dict):
        errors.append("concept_recipes.aliases: must be an object")
    elif isinstance(aliases, dict):
        role_names = set((recipes.get("roles", {}) or {}).keys())
        mixin_names = set((recipes.get("mixins", {}) or {}).keys())
        for alias, canonical in aliases.items():
            if not str(alias).strip():
                errors.append("concept_recipes.aliases: empty alias")
                continue
            canonical_text = str(canonical or "")
            if not canonical_text.strip():
                errors.append(f"concept_recipes.aliases.{alias}: empty canonical value")
                continue
            if not any(name in canonical_text for name in role_names) and not any(
                name in canonical_text for name in mixin_names
            ):
                errors.append(
                    f"concept_recipes.aliases.{alias}: canonical {canonical_text!r} does not reference any role or mixin"
                )

    roles = recipes.get("roles", {}) or {}
    if roles and not isinstance(roles, dict):
        errors.append("concept_recipes.roles: must be an object")
    elif isinstance(roles, dict):
        for role, recipe in roles.items():
            if not isinstance(recipe, dict):
                errors.append(f"concept_recipes.roles.{role}: must be an object")
                continue
            validate_concept_recipe_entry(f"concept_recipes.roles.{role}", recipe, data, errors)

    mixins = recipes.get("mixins", {}) or {}
    if mixins and not isinstance(mixins, dict):
        errors.append("concept_recipes.mixins: must be an object")
    elif isinstance(mixins, dict):
        for mixin, recipe in mixins.items():
            if not isinstance(recipe, dict):
                errors.append(f"concept_recipes.mixins.{mixin}: must be an object")
                continue
            label = f"concept_recipes.mixins.{mixin}"
            validate_concept_recipe_entry(label, recipe, data, errors)
            validate_species_variants(label, recipe, data, errors)
            bundles = recipe.get("bundles", []) or []
            if bundles and not isinstance(bundles, list):
                errors.append(f"{label}.bundles: must be a list")
                continue
            for index, bundle in enumerate(bundles):
                bundle_label = f"{label}.bundles[{index}]"
                if not isinstance(bundle, dict):
                    errors.append(f"{bundle_label}: must be an object")
                    continue
                validate_concept_recipe_entry(bundle_label, bundle, data, errors)

    diversity_policy = recipes.get("mixin_diversity_policy", {}) or {}
    if diversity_policy and not isinstance(diversity_policy, dict):
        errors.append("concept_recipes.mixin_diversity_policy: must be an object")
    elif isinstance(diversity_policy, dict):
        known_mixins = set(mixins.keys()) if isinstance(mixins, dict) else set()
        for mixin, policy in diversity_policy.items():
            policy_label = f"concept_recipes.mixin_diversity_policy.{mixin}"
            if mixin not in known_mixins:
                errors.append(f"concept_recipes.mixin_diversity_policy: unknown mixin {mixin}")
                continue
            if not isinstance(policy, dict):
                errors.append(f"{policy_label}: must be an object")
                continue
            axes = normalize_list(policy.get("aspect_axes"))
            if "aspect_axes" in policy and not axes:
                errors.append(f"{policy_label}.aspect_axes: at least one axis is required when present")
            for axis in axes:
                if not str(axis).strip():
                    errors.append(f"{policy_label}.aspect_axes: empty axis")
            for key in ("min_distinct_aspects_per_batch",):
                if key in policy and (not isinstance(policy.get(key), int) or policy.get(key) < 1):
                    errors.append(f"{policy_label}.{key}: must be a positive integer")
            for key in ("max_same_prop_ratio", "max_same_composition_ratio", "max_same_location_ratio", "ledger_repeat_decay", "batch_repeat_decay"):
                if key in policy and not isinstance(policy.get(key), (int, float)):
                    errors.append(f"{policy_label}.{key}: must be numeric")
            if "prefer_bundle_rotation" in policy and not isinstance(policy.get("prefer_bundle_rotation"), bool):
                errors.append(f"{policy_label}.prefer_bundle_rotation: must be a boolean")


def validate_slot_applicability(data: dict[str, Any], errors: list[str]) -> None:
    config = data.get("slot_applicability", {}) or {}
    if config and not isinstance(config, dict):
        errors.append("slot_applicability: must be an object")
        return
    if not config:
        return

    by_slot = entry_ids_by_slot(data)
    subject_ids = by_slot.get("subject", set())
    preset_ids = {str(preset.get("id")) for preset in data.get("presets", [])}
    preset_ids |= {f"virtual:{recipe.get('id')}" for recipe in data.get("recipes", [])}

    subject_overrides = config.get("subject_category_overrides", {}) or {}
    if subject_overrides and not isinstance(subject_overrides, dict):
        errors.append("slot_applicability.subject_category_overrides: must be an object")
    for entry_id, category in subject_overrides.items():
        if str(entry_id) not in subject_ids:
            errors.append(f"slot_applicability.subject_category_overrides: unknown subject id {entry_id}")
        if str(category) not in VALID_SUBJECT_CATEGORIES:
            errors.append(f"slot_applicability.subject_category_overrides.{entry_id}: unknown subject category {category}")

    preset_overrides = config.get("preset_domain_overrides", {}) or {}
    if preset_overrides and not isinstance(preset_overrides, dict):
        errors.append("slot_applicability.preset_domain_overrides: must be an object")
    for preset_id, domains in preset_overrides.items():
        if str(preset_id) not in preset_ids:
            errors.append(f"slot_applicability.preset_domain_overrides: unknown preset id {preset_id}")
        for domain in normalize_list(domains):
            if domain not in VALID_PRESET_DOMAINS:
                errors.append(f"slot_applicability.preset_domain_overrides.{preset_id}: unknown preset domain {domain}")

    slot_policies = config.get("slots", {}) or {}
    if slot_policies and not isinstance(slot_policies, dict):
        errors.append("slot_applicability.slots: must be an object")
    valid_policy_keys = {
        "subject_categories",
        "deny_subject_categories",
        "allow_domains",
        "deny_domains",
        "allow_domains_override_subject_categories",
        "require_domain_match",
    }
    for slot, policy in slot_policies.items():
        if slot not in by_slot:
            errors.append(f"slot_applicability.slots: unknown slot {slot}")
            continue
        if not isinstance(policy, dict):
            errors.append(f"slot_applicability.slots.{slot}: must be an object")
            continue
        for key in policy:
            if key not in valid_policy_keys:
                errors.append(f"slot_applicability.slots.{slot}: unknown policy key {key}")
        for key in ("subject_categories", "deny_subject_categories"):
            for category in normalize_list(policy.get(key)):
                if category not in VALID_SUBJECT_CATEGORIES:
                    errors.append(f"slot_applicability.slots.{slot}.{key}: unknown subject category {category}")
        for key in ("allow_domains", "deny_domains"):
            for domain in normalize_list(policy.get(key)):
                if domain not in VALID_PRESET_DOMAINS:
                    errors.append(f"slot_applicability.slots.{slot}.{key}: unknown preset domain {domain}")
        for key in ("require_domain_match", "allow_domains_override_subject_categories"):
            if key in policy and not isinstance(policy.get(key), bool):
                errors.append(f"slot_applicability.slots.{slot}.{key}: must be a boolean")


def validate_skill_doc_literals(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    """Cross-check `--preset X` and `--set slot=id` literals in SKILL.md against the dictionary."""
    if not path.exists():
        return
    import re

    text = path.read_text(encoding="utf-8")
    by_slot = entry_ids_by_slot(data)
    preset_ids = {str(preset.get("id")) for preset in data.get("presets", [])}
    for match in re.finditer(r"--preset[ =]([A-Za-z0-9_]+)", text):
        preset_id = match.group(1)
        if preset_id not in preset_ids:
            errors.append(f"SKILL.md: unknown preset id {preset_id}")
    for match in re.finditer(r"--set[ =]([A-Za-z0-9_]+)=([A-Za-z0-9_|]+)", text):
        slot, values = match.group(1), match.group(2)
        if slot not in by_slot:
            errors.append(f"SKILL.md: unknown slot {slot} in --set example")
            continue
        for value in values.split("|"):
            if value and value not in by_slot[slot]:
                errors.append(f"SKILL.md: unknown id {value} for slot {slot} in --set example")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate photo prompt dictionary semantic metadata.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    parser.add_argument("--concept-recipes", default=DEFAULT_CONCEPT_RECIPES)
    parser.add_argument("--quality-layers", default=DEFAULT_QUALITY_LAYERS)
    parser.add_argument("--skill-doc", default=Path(__file__).resolve().parents[1] / "SKILL.md")
    args = parser.parse_args()

    data = load_json(args.tags)
    errors: list[str] = []
    vocab = merged_facet_vocab(data)

    validate_filter_ids(data, errors)
    validate_selection_contracts(data, errors)
    validate_no_text_required_entries(data, errors)
    validate_coherence_rules(data, errors)
    validate_semantic_policy(data, errors)
    validate_semantic_metadata(data, errors)
    validate_slot_applicability(data, errors)
    validate_concept_recipes(Path(args.concept_recipes), data, errors)
    validate_quality_layers(Path(args.quality_layers), data, errors)
    validate_skill_doc_literals(Path(args.skill_doc), data, errors)
    for label, entry in all_entries(data):
        validate_facets(label, entry, vocab, errors)
        validate_hard_guards(label, entry, vocab, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("photo prompt dictionary metadata is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
