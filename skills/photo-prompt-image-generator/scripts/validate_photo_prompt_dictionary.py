#!/usr/bin/env python3
"""Validate optional semantic metadata in photo_prompt_tags.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from visual_profile_contracts import compile_visual_profile, validate_hard_activation, validate_visual_profile_source
import photo_source_manifest
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
import photo_creative_controls as creative_controls

from prompt_generator import (
    DEFAULT_FACET_VOCAB,
    RESEARCH_EXTENSION_FILENAMES as TAXONOMY_EXTENSION_FILENAMES,
    VALID_INTENT_DOMAINS,
    VALID_SUBJECT_CATEGORIES,
    VISUAL_RELATION_CONTRACT_VERSION,
    load_json,
    load_visual_obligation_registry,
    load_visual_profile_index,
    normalize_list,
)


RETIRED_RUNTIME_METADATA_KEYS = {
    "authorship_basis",
    "audience_scope",
    "audience_familiarity",
    "character_family",
    "character_topic",
    "content_basis",
    "cultural_provenance",
    "market_origin",
    "term_level",
}
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
DEFAULT_QUALITY_LAYERS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_quality_layers.json"
DEFAULT_VISUAL_OBLIGATIONS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_visual_obligations.json"
DEFAULT_VISUAL_PROFILE_INDEX = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_visual_profile_index.json"
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

FORBIDDEN_RUNTIME_PROCESS_MARKERS = {
    "named_moe_review_source": re.compile(r"moe[-_ ]review|모에\s*리뷰|萌えレビュー", re.IGNORECASE),
    "source_grounded": re.compile(r"source[-_ ]grounded", re.IGNORECASE),
    "market_researched": re.compile(
        r"(?:public|cjk)[-_ ]market[-_ ]researched|market[-_ ]researched",
        re.IGNORECASE,
    ),
    "research_backed": re.compile(r"research[-_ ](?:backed|based)", re.IGNORECASE),
    "research_router": re.compile(r"research(?:[-_ ]family)?[-_ ]router", re.IGNORECASE),
    "cited_study": re.compile(r"cited(?:[-_ ]interview)?[-_ ]study", re.IGNORECASE),
    "reposted_source": re.compile(r"reposted[-_ ]industry[-_ ]news[-_ ]source", re.IGNORECASE),
    "fan_discourse_provenance": re.compile(r"fan[-_ ]discourse[-_ ]provenance", re.IGNORECASE),
    "nonvisual_provenance": re.compile(r"nonvisual[-_ ]provenance", re.IGNORECASE),
    "derived_research_scene": re.compile(r"derived[-_ ]research[-_ ]scene", re.IGNORECASE),
    "provenance_scope_key": re.compile(r"^provenance_scope$", re.IGNORECASE),
}
FORBIDDEN_VISUAL_ATOM_CONTROL_MARKERS = {
    "provenance_language": re.compile(r"\bprovenance\b", re.IGNORECASE),
    "market_control_language": re.compile(r"\bmarket[-_ ](?:term|label)\b", re.IGNORECASE),
    "nonvisual_instruction": re.compile(r"\bnon[-_ ]?visual\b", re.IGNORECASE),
}
FORBIDDEN_PUBLIC_VISUAL_CONTROL_MARKERS = {
    "provenance_language": re.compile(r"\bprovenance\b", re.IGNORECASE),
    "market_control_language": re.compile(r"\bmarket[-_ ](?:term|label)\b", re.IGNORECASE),
    "term_routing_language": re.compile(r"\bterm[-_ ]routing\b", re.IGNORECASE),
    "nonvisual_instruction": re.compile(r"\bnon[-_ ]?visual\b", re.IGNORECASE),
    "national_style_shorthand": re.compile(r"\bnational[-_ ]style shorthand\b", re.IGNORECASE),
    "rights_status_language": re.compile(r"\brights[-_ ]cleared\b", re.IGNORECASE),
    "copyright_status_language": re.compile(r"\bcopyrighted\b", re.IGNORECASE),
    "market_comparison_language": re.compile(
        r"\b(?:japanese|korean|chinese|cjk)[-_ ]market[-_ ](?:variant|comparison)\b",
        re.IGNORECASE,
    ),
    "audience_priority_language": re.compile(
        r"\baudience[-_ ](?:interest|preference|appeal|priority)\b|"
        r"(?:시청자|관객)\s*(?:흥미|선호|관심)",
        re.IGNORECASE,
    ),
}
PUBLIC_VISUAL_TEXT_FIELDS = (
    "en",
    "ko",
    "embedding_text",
    "aliases",
    "keywords",
    "terms",
    "label",
    "prompt_focus",
    "intent_axis",
    "additional",
)


def iter_json_text(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            yield f"{path}.<key>", key_text
            yield from iter_json_text(child, f"{path}.{key_text}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_json_text(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value




def iter_public_visual_text(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for field in PUBLIC_VISUAL_TEXT_FIELDS:
            text = value.get(field)
            if isinstance(text, str) and text.strip():
                yield f"{path}.{field}", text
            elif isinstance(text, list):
                for index, item in enumerate(text):
                    if isinstance(item, str) and item.strip():
                        yield f"{path}.{field}[{index}]", item
        for key, child in value.items():
            yield from iter_public_visual_text(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_public_visual_text(child, f"{path}[{index}]")


def validate_runtime_process_metadata(paths: list[Path], errors: list[str]) -> None:
    """Reject research/process labels from runtime taxonomy assets.

    Source ledgers and evaluation fixtures live outside the runtime skill. The
    runtime JSON may contain the resulting visual taxonomy, but not source
    names or development-process labels that can steer retrieval/composition.
    """
    for path in paths:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"runtime metadata boundary: cannot read {path.name}: {exc}")
            continue
        for json_path, text in iter_json_text(payload):
            for marker, pattern in FORBIDDEN_RUNTIME_PROCESS_MARKERS.items():
                if pattern.search(text):
                    errors.append(
                        f"runtime metadata boundary: {path.name}:{json_path} contains {marker}"
                    )
        for json_path, text in iter_public_visual_text(payload):
            for marker, pattern in FORBIDDEN_PUBLIC_VISUAL_CONTROL_MARKERS.items():
                if pattern.search(text):
                    errors.append(
                        f"runtime public visual text boundary: {path.name}:{json_path} contains {marker}"
                    )


def validate_retired_runtime_metadata(paths: list[Path], errors: list[str]) -> None:
    """Reject retired control/source classifications from runtime assets."""

    def walk(value: Any, label: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                child = f"{label}.{key}" if label else str(key)
                if str(key) in RETIRED_RUNTIME_METADATA_KEYS:
                    errors.append(f"{child}: retired runtime metadata key is not allowed")
                walk(item, child)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{label}[{index}]")

    for path in paths:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: cannot inspect retired runtime metadata: {exc}")
            continue
        walk(payload, path.name)


def merged_facet_vocab(data: dict[str, Any]) -> dict[str, set[str]]:
    vocab: dict[str, set[str]] = {key: set(values) for key, values in DEFAULT_FACET_VOCAB.items()}
    for key, values in (data.get("facet_vocab") or {}).items():
        vocab.setdefault(str(key), set()).update(str(value) for value in values)
    return vocab


def all_entries(data: dict[str, Any]):
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


def validate_selection_contracts(data: dict[str, Any], errors: list[str]) -> None:
    slots = data.get("slots", {}) or {}
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






def validate_coherence_rules(data: dict[str, Any], errors: list[str]) -> None:
    rules = data.get("coherence_rules", {}) or {}
    if rules and not isinstance(rules, dict):
        errors.append("coherence_rules: must be an object")
        return
    if not rules:
        return

    retired = set(rules) - {"slot_conflicts", "slot_context_rules"}
    if retired:
        errors.append(f"coherence_rules: unsupported fields {sorted(retired)}")
    by_slot = entry_ids_by_slot(data)

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
    if "source" in craft:
        errors.append("quality_layers.photographic_craft.source: retired nonfunctional trace")
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
    if "source" in touch:
        errors.append("quality_layers.artistic_final_touch.source: retired nonfunctional trace")
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
            "subject_routes",
            "subject_categories",
            "domains",
            "literal_subject_stop_terms",
        }:
            errors.append(f"quality_layers.intent_routing: unknown key {key}")
    if "literal_subject_stop_terms" in routing:
        validate_string_list(
            "quality_layers.intent_routing.literal_subject_stop_terms",
            routing.get("literal_subject_stop_terms"),
            errors,
        )

    subject_entries = {
        str(entry.get("id")): entry
        for entry in ((data.get("slots") or {}).get("subject") or [])
        if isinstance(entry, dict) and str(entry.get("id") or "")
    }
    configured_subject_routes: set[str] = set()
    subject_routes = routing.get("subject_routes", [])
    if not isinstance(subject_routes, list):
        errors.append("quality_layers.intent_routing.subject_routes: must be a list")
        subject_routes = []
    for index, row in enumerate(subject_routes):
        label = f"quality_layers.intent_routing.subject_routes[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be an object")
            continue
        for key in row:
            if key not in {"entry_id", "category", "aliases"}:
                errors.append(f"{label}: unknown key {key}")
        entry_id = str(row.get("entry_id") or "").strip()
        category = str(row.get("category") or "").strip()
        if entry_id not in subject_entries:
            errors.append(f"{label}.entry_id: unknown subject entry id {entry_id!r}")
        elif entry_id in configured_subject_routes:
            errors.append(f"{label}.entry_id: duplicate subject route {entry_id}")
        else:
            configured_subject_routes.add(entry_id)
        if category not in VALID_SUBJECT_CATEGORIES:
            errors.append(f"{label}.category: unknown subject category {category!r}")
        validate_string_list(f"{label}.aliases", row.get("aliases"), errors)

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
            if key not in {"domain", "aliases", "standalone_aliases"}:
                errors.append(f"{label}: unknown key {key}")
        domain = str(row.get("domain") or "").strip()
        if domain not in VALID_INTENT_DOMAINS:
            errors.append(f"{label}.domain: unknown request domain {domain!r}")
        elif domain in configured_domains:
            errors.append(f"{label}.domain: duplicate domain {domain}")
        else:
            configured_domains.add(domain)
        validate_string_list(f"{label}.aliases", row.get("aliases"), errors)
        if "standalone_aliases" in row:
            validate_string_list(
                f"{label}.standalone_aliases", row.get("standalone_aliases"), errors
            )


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


def validate_quality_layer_adult_appeal(quality: dict[str, Any], data: dict[str, Any], errors: list[str]) -> None:
    adult = quality.get("adult_appeal")
    if not isinstance(adult, dict):
        errors.append("quality_layers.adult_appeal: must be an object")
        return
    allowed = {"creative_controls_source", "contextual_retrieval", "entry_dimensions", "risk_groups", "hard_combinations", "warning_combinations"}
    if set(adult) - allowed:
        errors.append("quality_layers.adult_appeal: unsupported policy fields")
    if adult.get("creative_controls_source") != "precore/creative_controls.json":
        errors.append("adult_appeal.creative_controls_source: must name neutral pre-core definitions")
    retrieval = adult.get("contextual_retrieval") or {}
    if retrieval.get("contract_version") != "photo-contextual-appeal/v2":
        errors.append("adult_appeal.contextual_retrieval: requires current v2 policy")
    for key in ("candidate_limit_per_axis", "review_limit_per_axis"):
        if not isinstance(retrieval.get(key), int) or not 1 <= retrieval[key] <= 24:
            errors.append(f"adult_appeal.contextual_retrieval.{key}: must be in 1..24")
    by_slot = entry_ids_by_slot(data)
    all_entry_ids = {entry_id for ids in by_slot.values() for entry_id in ids}
    entry_dimensions = adult.get("entry_dimensions", {})
    if not isinstance(entry_dimensions, dict):
        errors.append("adult_appeal.entry_dimensions: must be an object")
    else:
        for source_key, dimensions in entry_dimensions.items():
            slot, separator, entry_id = str(source_key).partition(":")
            if not separator or entry_id not in by_slot.get(slot, set()):
                errors.append(f"adult_appeal.entry_dimensions: unknown candidate {source_key}")
            if (not isinstance(dimensions, list) or not dimensions
                    or any(not isinstance(value, str) for value in dimensions)):
                errors.append(f"adult_appeal.entry_dimensions.{source_key}: requires nonempty dimension names")
            elif (len(dimensions) != len(set(dimensions))
                    or not set(dimensions).issubset(AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)):
                errors.append(f"adult_appeal.entry_dimensions.{source_key}: duplicate or unknown dimensions")
    risk_groups = adult.get("risk_groups") if isinstance(adult.get("risk_groups"), dict) else {}
    for group_id, group in risk_groups.items():
        label = f"quality_layers.adult_appeal.risk_groups.{group_id}"
        if not isinstance(group, dict):
            errors.append(f"{label}: must be an object")
            continue
        validate_string_list(f"{label}.entry_ids", group.get("entry_ids"), errors)
        validate_string_list(f"{label}.prompt_terms", group.get("prompt_terms"), errors)
        for entry_id in normalize_list(group.get("entry_ids")):
            if entry_id not in all_entry_ids:
                errors.append(f"{label}.entry_ids: unknown entry id {entry_id}")
    for rule_type in ("hard_combinations", "warning_combinations"):
        rules = adult.get(rule_type) or []
        if not isinstance(rules, list):
            errors.append(f"quality_layers.adult_appeal.{rule_type}: must be a list")
            continue
        for index, rule in enumerate(rules):
            label = f"quality_layers.adult_appeal.{rule_type}[{index}]"
            if not isinstance(rule, dict):
                errors.append(f"{label}: must be an object")
                continue
            if not str(rule.get("id") or "").strip() or not str(rule.get("reason") or "").strip():
                errors.append(f"{label}: id and reason are required")
            groups = normalize_list(rule.get("all_of"))
            if len(groups) < 2:
                errors.append(f"{label}.all_of: at least two risk groups are required")
            for group_id in groups:
                if group_id not in risk_groups:
                    errors.append(f"{label}.all_of: unknown risk group {group_id}")


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
        validate_quality_layer_adult_appeal(quality, data, errors)
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


REVIEW_GATE_ASSERT_TYPES = {
    "mixin_shape",
    "forced_slot_any",
    "forced_slot_absent",
    "bundle_selected",
    "role_costume_preserved",
}


def validate_slot_applicability(data: dict[str, Any], errors: list[str]) -> None:
    config = data.get("slot_applicability", {}) or {}
    if config and not isinstance(config, dict):
        errors.append("slot_applicability: must be an object")
        return
    if not config:
        return

    by_slot = entry_ids_by_slot(data)
    subject_ids = by_slot.get("subject", set())

    subject_overrides = config.get("subject_category_overrides", {}) or {}
    if subject_overrides and not isinstance(subject_overrides, dict):
        errors.append("slot_applicability.subject_category_overrides: must be an object")
    for entry_id, category in subject_overrides.items():
        if str(entry_id) not in subject_ids:
            errors.append(f"slot_applicability.subject_category_overrides: unknown subject id {entry_id}")
        if str(category) not in VALID_SUBJECT_CATEGORIES:
            errors.append(f"slot_applicability.subject_category_overrides.{entry_id}: unknown subject category {category}")

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
                if domain not in VALID_INTENT_DOMAINS:
                    errors.append(f"slot_applicability.slots.{slot}.{key}: unknown request domain {domain}")
        for key in ("require_domain_match", "allow_domains_override_subject_categories"):
            if key in policy and not isinstance(policy.get(key), bool):
                errors.append(f"slot_applicability.slots.{slot}.{key}: must be a boolean")


def validate_visual_relation_contract(
    relation: Any,
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(relation, dict):
        errors.append(f"{label}: must be an object")
        return
    allowed_keys = {
        "schema_version",
        "status",
        "source",
        "owner_axis",
        "entities",
        "visible_regions",
        "relations",
        "observable_effects",
        "confusion_negatives",
        "observability",
        "activation",
        "invariant_fields",
        "flexible_fields",
    }
    unknown = sorted(set(relation) - allowed_keys)
    if unknown:
        errors.append(f"{label}: unknown keys {unknown}")
    if relation.get("schema_version") != VISUAL_RELATION_CONTRACT_VERSION:
        errors.append(
            f"{label}.schema_version: expected {VISUAL_RELATION_CONTRACT_VERSION!r}"
        )
    if relation.get("status") not in {"request_scoped", "advisory"}:
        errors.append(f"{label}.status: must be request_scoped or advisory")
    if re.fullmatch(r"[a-z][a-z0-9_]+", str(relation.get("owner_axis") or "")) is None:
        errors.append(f"{label}.owner_axis: must be one stable snake_case owner")

    source = relation.get("source")
    if not isinstance(source, dict) or set(source) != {
        "kind",
        "literal_evidence",
        "priority",
        "confidence",
    }:
        errors.append(
            f"{label}.source: keys must be kind, literal_evidence, priority, confidence"
        )
    else:
        if source.get("kind") not in {
            "request_exact",
            "authorial_core",
            "reference_observation",
            "advisory_candidate",
        }:
            errors.append(f"{label}.source.kind: invalid source kind")
        if source.get("priority") not in {"P0", "P1", "P2"}:
            errors.append(f"{label}.source.priority: invalid priority")
        if source.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{label}.source.confidence: invalid confidence")
        if not normalize_list(source.get("literal_evidence")):
            errors.append(f"{label}.source.literal_evidence: must be non-empty")

    for key in (
        "entities",
        "visible_regions",
        "relations",
        "observable_effects",
        "confusion_negatives",
        "invariant_fields",
        "flexible_fields",
    ):
        values = normalize_list(relation.get(key))
        if not values or len(set(values)) != len(values):
            errors.append(f"{label}.{key}: must be non-empty and distinct")

    observability = relation.get("observability")
    expected_observability_keys = {
        "required_visible_regions",
        "minimum_review_scale",
        "crop_policy",
        "occlusion_policy",
        "proof_budget",
        "ineligible_state",
    }
    if not isinstance(observability, dict) or set(observability) != expected_observability_keys:
        errors.append(
            f"{label}.observability: keys must be {sorted(expected_observability_keys)}"
        )
    else:
        required_regions = normalize_list(
            observability.get("required_visible_regions")
        )
        visible_regions = set(normalize_list(relation.get("visible_regions")))
        if not required_regions or not set(required_regions) <= visible_regions:
            errors.append(
                f"{label}.observability.required_visible_regions: must be a non-empty subset of visible_regions"
            )
        if observability.get("minimum_review_scale") not in {
            "thumbnail",
            "native",
            "both",
        }:
            errors.append(f"{label}.observability.minimum_review_scale: invalid value")
        for key in ("crop_policy", "occlusion_policy"):
            if len(str(observability.get(key) or "").split()) < 4:
                errors.append(f"{label}.observability.{key}: must be concrete")
        proof_budget = observability.get("proof_budget")
        if not isinstance(proof_budget, dict) or set(proof_budget) != {
            "thumbnail",
            "native",
        }:
            errors.append(
                f"{label}.observability.proof_budget: must declare thumbnail and native"
            )
        elif any(
            len(str(proof_budget.get(key) or "").split()) < 3
            for key in ("thumbnail", "native")
        ):
            errors.append(
                f"{label}.observability.proof_budget: both scales must be concrete"
            )
        if observability.get("ineligible_state") != "UNSCORED":
            errors.append(f"{label}.observability.ineligible_state: must be UNSCORED")

    activation = relation.get("activation")
    expected_activation_keys = {
        "hard_only_from_exact_source",
        "embedding_only_is_advisory",
        "all_required_components_coexist",
    }
    if not isinstance(activation, dict) or set(activation) != expected_activation_keys:
        errors.append(
            f"{label}.activation: keys must be {sorted(expected_activation_keys)}"
        )
    elif any(activation.get(key) is not True for key in expected_activation_keys):
        errors.append(f"{label}.activation: every guard must be true")


def validate_visual_obligation_registry(path: Path, errors: list[str], *, inventory=None) -> None:
    if not path.exists():
        errors.append(f"visual obligation registry missing: {path}")
        return
    try:
        payload = load_visual_obligation_registry(path, inventory=inventory)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"visual obligation registry is not valid JSON: {exc}")
        return
    if not isinstance(payload, dict):
        errors.append("visual obligation registry: root must be an object")
        return
    expected_versions = {
        "schema_version": "photo-visual-obligation-registry/v3",
        "contract_version": "photo-visual-obligations/v1",
        "visual_intent_contract_version": "photo-visual-intent/v1",
        "concept_contract_version": "photo-visual-concepts/v1",
    }
    for field, expected in expected_versions.items():
        if payload.get(field) != expected:
            errors.append(
                f"visual obligation registry.{field}: expected {expected!r}"
            )
    if payload.get("relation_contract_version") not in {
        None,
        VISUAL_RELATION_CONTRACT_VERSION,
    }:
        errors.append(
            "visual obligation registry.relation_contract_version: invalid value"
        )
    precedence = normalize_list(payload.get("precedence"))
    if not precedence or len(set(precedence)) != len(precedence):
        errors.append("visual obligation registry.precedence: must be non-empty and distinct")
    activation_policy = payload.get("activation_policy")
    if not isinstance(activation_policy, dict):
        errors.append("visual obligation registry.activation_policy: must be an object")
    elif any(value is not True for value in activation_policy.values()):
        errors.append("visual obligation registry.activation_policy: every guard must be true")
    retrieval_policy = payload.get("retrieval_policy")
    if not isinstance(retrieval_policy, dict) or set(retrieval_policy) != {
        "minimum_similarity",
        "best_score_margin",
        "candidate_limit",
    }:
        errors.append(
            "visual obligation registry.retrieval_policy: must declare minimum_similarity, "
            "best_score_margin, and candidate_limit"
        )
    else:
        try:
            minimum_similarity = float(retrieval_policy.get("minimum_similarity"))
            best_score_margin = float(retrieval_policy.get("best_score_margin"))
            candidate_limit = int(retrieval_policy.get("candidate_limit"))
        except (TypeError, ValueError):
            minimum_similarity = -1.0
            best_score_margin = -1.0
            candidate_limit = 0
        if not 0.0 <= minimum_similarity <= 1.0:
            errors.append(
                "visual obligation registry.retrieval_policy.minimum_similarity: "
                "must be between 0 and 1"
            )
        if not 0.0 <= best_score_margin <= 1.0:
            errors.append(
                "visual obligation registry.retrieval_policy.best_score_margin: "
                "must be between 0 and 1"
            )
        if candidate_limit < 1:
            errors.append(
                "visual obligation registry.retrieval_policy.candidate_limit: must be at least 1"
            )
    evidence_policy = payload.get("evidence_policy")
    if not isinstance(evidence_policy, dict):
        errors.append("visual obligation registry.evidence_policy: must be an object")
    else:
        try:
            default_min_words = int(evidence_policy.get("minimum_content_words_default"))
        except (TypeError, ValueError):
            default_min_words = 0
        try:
            overlap_limit = float(
                evidence_policy.get("maximum_pairwise_content_token_overlap_ratio")
            )
        except (TypeError, ValueError):
            overlap_limit = -1.0
        if default_min_words < 2:
            errors.append(
                "visual obligation registry.evidence_policy.minimum_content_words_default: "
                "must be at least 2"
            )
        if not 0.0 < overlap_limit < 1.0:
            errors.append(
                "visual obligation registry.evidence_policy."
                "maximum_pairwise_content_token_overlap_ratio: must be between 0 and 1"
            )
        fillers = normalize_list(evidence_policy.get("forbidden_filler_phrases"))
        if not fillers or len({value.casefold() for value in fillers}) != len(fillers):
            errors.append(
                "visual obligation registry.evidence_policy.forbidden_filler_phrases: "
                "must be non-empty and distinct"
            )

    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        errors.append("visual obligation registry.profiles: must be a non-empty list")
        return
    profile_ids: set[str] = set()
    gate_ids: set[str] = set()
    glossary_alias_owners: dict[str, str] = {}
    allowed_profile_keys = {
        "id",
        "category",
        "activation",
        "semantics",
        "composition_instruction",
        "concept_candidate",
        "runtime_expression",
        "required_evidence_fields",
        "evidence_requirements",
        "render_gates",
        "reject_substitutes",
        "visual_relation",
        "authored_components",
    }
    for index, profile in enumerate(profiles):
        label = f"visual obligation registry.profiles[{index}]"
        if not isinstance(profile, dict):
            errors.append(f"{label}: must be an object")
            continue
        unknown = sorted(set(profile) - allowed_profile_keys)
        if unknown:
            errors.append(f"{label}: unknown keys {unknown}")
        profile_id = str(profile.get("id") or "")
        if re.fullmatch(r"[a-z][a-z0-9_]+", profile_id) is None:
            errors.append(f"{label}.id: must be a stable snake_case id")
        elif profile_id in profile_ids:
            errors.append(f"{label}.id: duplicate {profile_id}")
        profile_ids.add(profile_id)
        if "authored_components" in profile:
            try:
                compile_visual_profile(profile)
            except ValueError as exc:
                errors.append(f"{label}.authored_components: {exc}")
        if not str(profile.get("category") or "").strip():
            errors.append(f"{label}.category: must be non-empty")
        if len(str(profile.get("composition_instruction") or "").split()) < 8:
            errors.append(f"{label}.composition_instruction: must be concrete")
        activation = profile.get("activation")
        if not isinstance(activation, dict):
            errors.append(f"{label}.activation: must be an object")
        else:
            unknown_activation = sorted(
                set(activation)
                - {
                    "exact_terms",
                    "project_glossary_aliases",
                    "exclude_if_any_terms",
                    "context_disambiguation",
                    "requires_adult_character",
                    "semantic_discovery_requires_component_evidence",
                    "hard_activation",
                }
            )
            if unknown_activation:
                errors.append(f"{label}.activation: unknown keys {unknown_activation}")
            if "hard_activation" in activation:
                try:
                    validate_hard_activation(activation["hard_activation"])
                except ValueError as exc:
                    errors.append(f"{label}.activation.hard_activation: {exc}")
            terms = normalize_list(activation.get("exact_terms"))
            if not terms or len({term.lower() for term in terms}) != len(terms):
                errors.append(f"{label}.activation.exact_terms: must be non-empty and distinct")
            glossary_aliases = normalize_list(
                activation.get("project_glossary_aliases")
            )
            if "project_glossary_aliases" in activation and (
                not glossary_aliases
                or len({alias.casefold() for alias in glossary_aliases})
                != len(glossary_aliases)
            ):
                errors.append(
                    f"{label}.activation.project_glossary_aliases: "
                    "must be non-empty and distinct when declared"
                )
            natural_term_keys = {term.casefold() for term in terms}
            for alias in glossary_aliases:
                alias_key = alias.casefold()
                if alias_key in natural_term_keys:
                    errors.append(
                        f"{label}.activation.project_glossary_aliases: "
                        f"{alias!r} must not duplicate exact_terms"
                    )
                prior_owner = glossary_alias_owners.get(alias_key)
                if prior_owner is not None and prior_owner != profile_id:
                    errors.append(
                        f"{label}.activation.project_glossary_aliases: "
                        f"{alias!r} is already owned by {prior_owner}"
                    )
                glossary_alias_owners[alias_key] = profile_id
            if not isinstance(
                activation.get("requires_adult_character"),
                bool,
            ):
                errors.append(
                    f"{label}.activation.requires_adult_character: must be boolean"
                )
            if (
                "semantic_discovery_requires_component_evidence" in activation
                and not isinstance(
                    activation.get(
                        "semantic_discovery_requires_component_evidence"
                    ),
                    bool,
                )
            ):
                errors.append(
                    f"{label}.activation."
                    "semantic_discovery_requires_component_evidence: must be boolean"
                )
            for term_key in ("exclude_if_any_terms",):
                values = normalize_list(activation.get(term_key))
                if term_key in activation and (
                    not values
                    or len({value.casefold() for value in values}) != len(values)
                ):
                    errors.append(
                        f"{label}.activation.{term_key}: must be non-empty and distinct when declared"
                    )
            context_disambiguation = activation.get("context_disambiguation")
            if context_disambiguation is not None:
                if not isinstance(context_disambiguation, dict):
                    errors.append(
                        f"{label}.activation.context_disambiguation: must be an object"
                    )
                else:
                    allowed_context_keys = {
                        "required_with_authorial_core",
                        "any_terms",
                        "exclude_if_any_terms",
                    }
                    unknown_context_keys = sorted(
                        set(context_disambiguation) - allowed_context_keys
                    )
                    if unknown_context_keys:
                        errors.append(
                            f"{label}.activation.context_disambiguation: "
                            f"unknown keys {unknown_context_keys}"
                        )
                    if (
                        context_disambiguation.get(
                            "required_with_authorial_core"
                        )
                        is not True
                    ):
                        errors.append(
                            f"{label}.activation.context_disambiguation."
                            "required_with_authorial_core: must be true"
                        )
                    for context_key in ("any_terms", "exclude_if_any_terms"):
                        context_values = normalize_list(
                            context_disambiguation.get(context_key)
                        )
                        if not context_values or len(
                            {value.casefold() for value in context_values}
                        ) != len(context_values):
                            errors.append(
                                f"{label}.activation.context_disambiguation."
                                f"{context_key}: must be non-empty and distinct"
                            )
            semantics = profile.get("semantics")
            if not isinstance(semantics, dict):
                errors.append(f"{label}.semantics: must be an object")
                semantics = {}
            else:
                unknown_semantic_keys = sorted(
                    set(semantics)
                    - {
                        "definition",
                        "paraphrase_examples",
                        "contrast_examples",
                        "component_semantics",
                        "visual_components",
                        "claim_limits",
                        "interpretation_scope",
                    }
                )
                if unknown_semantic_keys:
                    errors.append(
                        f"{label}.semantics: unknown keys {unknown_semantic_keys}"
                    )
                # The positive retrieval projection already consumes these
                # optional descriptive units. They confer no hard activation.
                if "visual_components" in semantics:
                    visual_components = semantics["visual_components"]
                    if (
                        not isinstance(visual_components, list)
                        or not visual_components
                        or any(not isinstance(value, str) or not value.strip() for value in visual_components)
                        or len({value.strip().casefold() for value in visual_components if isinstance(value, str)}) != len(visual_components)
                    ):
                        errors.append(f"{label}.semantics.visual_components: must be a non-empty list of distinct non-empty strings")
                if "claim_limits" in semantics:
                    limits = normalize_list(semantics["claim_limits"])
                    if not limits or len({value.casefold() for value in limits}) != len(limits):
                        errors.append(f"{label}.semantics.claim_limits: must be non-empty and distinct")
                if "interpretation_scope" in semantics:
                    scope = semantics["interpretation_scope"]
                    if not isinstance(scope, dict) or set(scope) != {"kind", "description"}:
                        errors.append(f"{label}.semantics.interpretation_scope: requires kind and description")
                    elif scope["kind"] not in {"project_visual_interpretation", "observable_relation"} or not str(scope["description"]).strip():
                        errors.append(f"{label}.semantics.interpretation_scope: invalid kind or description")
                if len(str(semantics.get("definition") or "").split()) < 8:
                    errors.append(f"{label}.semantics.definition: must be concrete")
                for semantic_key in ("paraphrase_examples", "contrast_examples"):
                    semantic_values = normalize_list(semantics.get(semantic_key))
                    if not semantic_values or len(
                        {value.casefold() for value in semantic_values}
                    ) != len(semantic_values):
                        errors.append(
                            f"{label}.semantics.{semantic_key}: must be non-empty and distinct"
                        )
                semantic_examples = {
                    value.casefold()
                    for value in normalize_list(semantics.get("paraphrase_examples"))
                }
                exact_keys = {
                    value.casefold()
                    for value in [
                        *terms,
                        *normalize_list(activation.get("project_glossary_aliases")),
                    ]
                }
                overlap = sorted(semantic_examples & exact_keys)
                if overlap:
                    errors.append(
                        f"{label}.semantics.paraphrase_examples: must not duplicate exact activation terms {overlap}"
                    )
            component_semantics = semantics.get("component_semantics")
            if not isinstance(component_semantics, dict):
                errors.append(f"{label}.semantics.component_semantics: must be an object")
            else:
                allowed_component_keys = {
                    "minimum_component_groups",
                    "required_group_ids",
                    "groups",
                }
                unknown_component_keys = sorted(
                    set(component_semantics) - allowed_component_keys
                )
                if unknown_component_keys:
                    errors.append(
                        f"{label}.semantics.component_semantics: unknown keys "
                        f"{unknown_component_keys}"
                    )
                groups = component_semantics.get("groups")
                group_ids: set[str] = set()
                if not isinstance(groups, list) or not groups:
                    errors.append(
                        f"{label}.semantics.component_semantics.groups: "
                        "must be a non-empty list"
                    )
                    groups = []
                for group_index, group in enumerate(groups):
                    group_label = (
                        f"{label}.semantics.component_semantics.groups[{group_index}]"
                    )
                    if not isinstance(group, dict) or set(group) != {"id", "any_terms"}:
                        errors.append(
                            f"{group_label}: keys must be id and any_terms"
                        )
                        continue
                    group_id = str(group.get("id") or "")
                    if re.fullmatch(r"[a-z][a-z0-9_]+", group_id) is None:
                        errors.append(f"{group_label}.id: invalid snake_case id")
                    elif group_id in group_ids:
                        errors.append(f"{group_label}.id: duplicate {group_id}")
                    group_ids.add(group_id)
                    group_terms = normalize_list(group.get("any_terms"))
                    if not group_terms or len(
                        {value.casefold() for value in group_terms}
                    ) != len(group_terms):
                        errors.append(
                            f"{group_label}.any_terms: must be non-empty and distinct"
                        )
                try:
                    minimum_groups = int(
                        component_semantics.get("minimum_component_groups")
                    )
                except (TypeError, ValueError):
                    minimum_groups = 0
                if minimum_groups < 1 or minimum_groups > max(1, len(group_ids)):
                    errors.append(
                        f"{label}.semantics.component_semantics.minimum_component_groups: "
                        "must fit the declared group count"
                    )
                required_group_ids = set(
                    normalize_list(component_semantics.get("required_group_ids"))
                )
                if not required_group_ids or not required_group_ids <= group_ids:
                    errors.append(
                        f"{label}.semantics.component_semantics.required_group_ids: "
                        "must be a non-empty subset of groups"
                    )
        concept_candidate = profile.get("concept_candidate")
        candidate_keys = {"concept_terms", "core_assertion_discovery",
                          "affected_dimensions", "affected_properties"}
        if (not isinstance(concept_candidate, dict)
                or "concept_terms" not in concept_candidate
                or set(concept_candidate) - candidate_keys):
            errors.append(f"{label}.concept_candidate: has missing or unsupported candidate fields")
        else:
            concept_terms = normalize_list(concept_candidate.get("concept_terms"))
            if not concept_terms or len(
                {value.casefold() for value in concept_terms}
            ) != len(concept_terms):
                errors.append(
                    f"{label}.concept_candidate.concept_terms: must be non-empty and distinct"
                )
            # Use the same scoped opt-in contract as the registry loader.
            # A discoverable candidate still creates no requester obligation.
            if set(concept_candidate) - {"concept_terms"}:
                import photo_candidate_semantics
                try:
                    photo_candidate_semantics.validate_candidate_entries(
                        {"slots": {"profile": [{
                            **concept_candidate, "id": profile["id"],
                            "concept_units": (profile.get("semantics") or {}).get("visual_components") or [],
                        }]}}, AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
                except ValueError as exc:
                    errors.append(f"{label}.concept_candidate: {exc}")
        runtime_expression = profile.get("runtime_expression")
        if not isinstance(runtime_expression, dict) or set(runtime_expression) != {
            "default_mode",
            "prompt_label_terms",
            "forbidden_prompt_terms",
            "runtime_forbidden_labels",
        }:
            errors.append(
                f"{label}.runtime_expression: keys must be default_mode, "
                "prompt_label_terms, forbidden_prompt_terms, runtime_forbidden_labels"
            )
        else:
            mode = runtime_expression.get("default_mode")
            if mode not in {
                "definition_only",
                "label_plus_definition",
                "definition_with_optional_label",
            }:
                errors.append(f"{label}.runtime_expression.default_mode: invalid value")
            label_terms = normalize_list(runtime_expression.get("prompt_label_terms"))
            forbidden_terms = normalize_list(
                runtime_expression.get("forbidden_prompt_terms")
            )
            runtime_forbidden_labels = normalize_list(
                runtime_expression.get("runtime_forbidden_labels")
            )
            if mode == "label_plus_definition" and not label_terms:
                errors.append(
                    f"{label}.runtime_expression.prompt_label_terms: "
                    "label_plus_definition requires at least one term"
                )
            if len({value.casefold() for value in label_terms}) != len(label_terms):
                errors.append(
                    f"{label}.runtime_expression.prompt_label_terms: must be distinct"
                )
            if len({value.casefold() for value in forbidden_terms}) != len(
                forbidden_terms
            ):
                errors.append(
                    f"{label}.runtime_expression.forbidden_prompt_terms: must be distinct"
                )
            if len(
                {value.casefold() for value in runtime_forbidden_labels}
            ) != len(runtime_forbidden_labels):
                errors.append(
                    f"{label}.runtime_expression.runtime_forbidden_labels: must be distinct"
                )
            if not {
                value.casefold() for value in runtime_forbidden_labels
            }.issubset({value.casefold() for value in forbidden_terms}):
                errors.append(
                    f"{label}.runtime_expression.runtime_forbidden_labels: "
                    "must be a subset of forbidden_prompt_terms"
                )
            if mode == "definition_only" and not runtime_forbidden_labels:
                errors.append(
                    f"{label}.runtime_expression.runtime_forbidden_labels: "
                    "definition_only requires at least one runtime label"
                )
        evidence_fields = normalize_list(profile.get("required_evidence_fields"))
        if not evidence_fields or len(set(evidence_fields)) != len(evidence_fields):
            errors.append(f"{label}.required_evidence_fields: must be non-empty and distinct")
        for field in evidence_fields:
            if re.fullmatch(r"[a-z][a-z0-9_]+_phrase", field) is None:
                errors.append(f"{label}.required_evidence_fields: invalid field {field!r}")
        evidence_requirements = profile.get("evidence_requirements")
        if not isinstance(evidence_requirements, dict):
            errors.append(f"{label}.evidence_requirements: must be an object")
            evidence_requirements = {}
        missing_requirement_fields = sorted(
            set(evidence_fields) - set(evidence_requirements)
        )
        extra_requirement_fields = sorted(
            set(evidence_requirements) - set(evidence_fields)
        )
        if missing_requirement_fields or extra_requirement_fields:
            errors.append(
                f"{label}.evidence_requirements: keys must exactly match required fields; "
                f"missing={missing_requirement_fields}, extra={extra_requirement_fields}"
            )
        for field, requirement in evidence_requirements.items():
            requirement_label = f"{label}.evidence_requirements.{field}"
            if not isinstance(requirement, dict):
                errors.append(f"{requirement_label}: must be an object")
                continue
            unknown_requirement_keys = sorted(
                set(requirement) - {"min_content_words", "must_mention_any", "must_not_contain"}
            )
            if unknown_requirement_keys:
                errors.append(
                    f"{requirement_label}: unknown keys {unknown_requirement_keys}"
                )
            try:
                min_content_words = int(requirement.get("min_content_words"))
            except (TypeError, ValueError):
                min_content_words = 0
            if min_content_words < 2:
                errors.append(
                    f"{requirement_label}.min_content_words: must be at least 2"
                )
            must_mention = normalize_list(requirement.get("must_mention_any"))
            if not must_mention or len(
                {value.casefold() for value in must_mention}
            ) != len(must_mention):
                errors.append(
                    f"{requirement_label}.must_mention_any: must be non-empty and distinct"
                )
            must_not = normalize_list(requirement.get("must_not_contain"))
            if "must_not_contain" in requirement and len(
                {value.casefold() for value in must_not}
            ) != len(must_not):
                errors.append(
                    f"{requirement_label}.must_not_contain: must be distinct"
                )
        gates = profile.get("render_gates")
        if not isinstance(gates, list) or not gates:
            errors.append(f"{label}.render_gates: must be a non-empty list")
        else:
            for gate_index, gate in enumerate(gates):
                gate_label = f"{label}.render_gates[{gate_index}]"
                if not isinstance(gate, dict):
                    errors.append(f"{gate_label}: must be an object")
                    continue
                if set(gate) != {"id", "review_scale", "description"}:
                    errors.append(
                        f"{gate_label}: keys must be id, review_scale, description"
                    )
                gate_id = str(gate.get("id") or "")
                if re.fullmatch(r"vo_[a-z0-9_]+", gate_id) is None:
                    errors.append(f"{gate_label}.id: must start with vo_ and use snake_case")
                elif gate_id in gate_ids:
                    errors.append(f"{gate_label}.id: duplicate {gate_id}")
                gate_ids.add(gate_id)
                if gate.get("review_scale") not in {"thumbnail", "native", "both"}:
                    errors.append(f"{gate_label}.review_scale: invalid value")
                if len(str(gate.get("description") or "").split()) < 6:
                    errors.append(f"{gate_label}.description: must be concrete")
        rejects = normalize_list(profile.get("reject_substitutes"))
        if not rejects or len(set(rejects)) != len(rejects):
            errors.append(f"{label}.reject_substitutes: must be non-empty and distinct")
        if "visual_relation" in profile:
            validate_visual_relation_contract(
                profile.get("visual_relation"),
                f"{label}.visual_relation",
                errors,
            )

    thigh_profile = next(
        (
            profile
            for profile in profiles
            if isinstance(profile, dict)
            and profile.get("id") == "inner_thigh_negative_space"
        ),
        None,
    )
    if not isinstance(thigh_profile, dict):
        errors.append("visual obligation registry: missing inner_thigh_negative_space profile")
    else:
        thigh_glossary_aliases = {
            term.casefold()
            for term in normalize_list(
                (thigh_profile.get("activation") or {}).get(
                    "project_glossary_aliases"
                )
            )
        }
        required_thigh_aliases = {"절대공역", "사이갭", "사이 갭"}
        if not required_thigh_aliases <= thigh_glossary_aliases:
            errors.append(
                "inner_thigh_negative_space: project glossary must map 절대공역, "
                "사이갭, and 사이 갭 to the explicit close-leg inner-thigh geometry profile"
            )


def validate_visual_profile_index_file(
    registry_path: Path,
    index_path: Path,
    errors: list[str],
) -> None:
    try:
        registry = load_visual_obligation_registry(registry_path)
        load_visual_profile_index(index_path, registry)
    except (OSError, ValueError) as exc:
        errors.append(f"visual profile index: {exc}")


def validate_source_corpus(root: Path, data: dict, inventory=None) -> list[str]:
    """Authored/cross-source checks; callers also deep-validate both indexes."""
    assets = Path(root) / "assets"
    inventory = inventory or photo_source_manifest.SourceInventory.load(assets)
    errors = []
    try:
        inventory.validate()
    except ValueError as exc:
        errors.append(str(exc))
    for name in ["photo_prompt_visual_obligations.json", *inventory.files("visual_profile")]:
        path = assets / name
        if not path.is_file():
            continue
        try:
            for profile in json.loads(path.read_text(encoding="utf-8")).get("profiles") or []:
                validate_visual_profile_source(profile)
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{name}: invalid authored profile source: {exc}")
    paths = [assets / "photo_prompt_tags.json", *[assets / name for name in inventory.files("candidate")]]
    validate_runtime_process_metadata(paths, errors)
    validate_retired_runtime_metadata(paths, errors)
    validate_selection_contracts(data, errors)
    validate_no_text_required_entries(data, errors)
    validate_coherence_rules(data, errors)
    validate_slot_applicability(data, errors)
    validate_quality_layers(assets / "photo_prompt_quality_layers.json", data, errors)
    validate_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json", errors, inventory=inventory)
    vocab = merged_facet_vocab(data)
    for label, entry in all_entries(data):
        validate_facets(label, entry, vocab, errors)
        validate_hard_guards(label, entry, vocab, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate photo prompt dictionary semantic metadata.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    parser.add_argument("--quality-layers")
    parser.add_argument("--visual-obligations")
    parser.add_argument("--visual-profile-index")
    parser.add_argument("--no-runtime-publication", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []

    tags_path = Path(args.tags)
    args.quality_layers = args.quality_layers or tags_path.with_name(DEFAULT_QUALITY_LAYERS.name)
    args.visual_obligations = args.visual_obligations or tags_path.with_name(DEFAULT_VISUAL_OBLIGATIONS.name)
    args.visual_profile_index = args.visual_profile_index or tags_path.with_name(DEFAULT_VISUAL_PROFILE_INDEX.name)
    photo_source_manifest.validate_source_files(tags_path.parent, errors, tags_path.with_name("photo_prompt_source_manifest.json"))
    try:
        inventory = photo_source_manifest.SourceInventory.load(tags_path.parent)
    except (OSError, ValueError) as exc:
        print(f"source manifest: {exc}", file=sys.stderr)
        return 1
    profile_path = Path(args.visual_obligations)
    for source_path in [profile_path, *[profile_path.with_name(name)
                                      for name in inventory.files("visual_profile")]]:
        if not source_path.is_file():
            continue
        try:
            raw = json.loads(source_path.read_text(encoding="utf-8"))
            for profile in raw.get("profiles") or []:
                validate_visual_profile_source(profile)
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{source_path.name}: invalid authored profile source: {exc}")
    runtime_asset_paths = [tags_path] + [
        tags_path.with_name(filename) for filename in inventory.files("candidate")
    ]
    validate_runtime_process_metadata(runtime_asset_paths, errors)
    validate_retired_runtime_metadata(runtime_asset_paths, errors)

    try:
        data = load_json(args.tags, inventory=inventory)
    except (OSError, ValueError) as exc:
        errors.append(f"{tags_path.name}: cannot load dictionary: {exc}")
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    vocab = merged_facet_vocab(data)

    validate_selection_contracts(data, errors)
    validate_no_text_required_entries(data, errors)
    validate_coherence_rules(data, errors)
    validate_slot_applicability(data, errors)
    validate_quality_layers(Path(args.quality_layers), data, errors)
    validate_visual_obligation_registry(Path(args.visual_obligations), errors, inventory=inventory)
    validate_visual_profile_index_file(
        Path(args.visual_obligations),
        Path(args.visual_profile_index),
        errors,
    )
    for label, entry in all_entries(data):
        validate_facets(label, entry, vocab, errors)
        validate_hard_guards(label, entry, vocab, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("photo prompt dictionary metadata is valid")
    if not args.no_runtime_publication:
        from photo_runtime_sources import publish_if_ready
        publish_if_ready(tags_path.parent.parent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
