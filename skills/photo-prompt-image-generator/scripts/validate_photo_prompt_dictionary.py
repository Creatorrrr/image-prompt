#!/usr/bin/env python3
"""Validate optional semantic metadata in photo_prompt_tags.json."""

from __future__ import annotations

import argparse
import json
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
    validate_recipe_set(label, recipe.get("set"), by_slot, errors)
    validate_recipe_slot_list(label, "override_slots", recipe.get("override_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "bundle_override_slots", recipe.get("bundle_override_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "soft_anchor_slots", recipe.get("soft_anchor_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "soft_free_slots", recipe.get("soft_free_slots"), by_slot, errors)
    validate_recipe_slot_list(label, "critical_anchor_slots", recipe.get("critical_anchor_slots"), by_slot, errors)
    anchor_pool = recipe.get("anchor_pool") or {}
    if anchor_pool and not isinstance(anchor_pool, dict):
        errors.append(f"{label}.anchor_pool: must be an object")
    elif isinstance(anchor_pool, dict):
        for slot, ids in anchor_pool.items():
            if slot not in by_slot:
                errors.append(f"{label}.anchor_pool: unknown slot {slot}")
                continue
            for entry_id in normalize_list(ids):
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
            for entry_id in normalize_list(ids):
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
        if "require_domain_match" in policy and not isinstance(policy.get("require_domain_match"), bool):
            errors.append(f"slot_applicability.slots.{slot}.require_domain_match: must be a boolean")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate photo prompt dictionary semantic metadata.")
    parser.add_argument("--tags", default=Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json")
    parser.add_argument("--concept-recipes", default=DEFAULT_CONCEPT_RECIPES)
    args = parser.parse_args()

    data = load_json(args.tags)
    errors: list[str] = []
    vocab = merged_facet_vocab(data)

    validate_filter_ids(data, errors)
    validate_coherence_rules(data, errors)
    validate_semantic_policy(data, errors)
    validate_semantic_metadata(data, errors)
    validate_slot_applicability(data, errors)
    validate_concept_recipes(Path(args.concept_recipes), data, errors)
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
