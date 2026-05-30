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
    SEMANTIC_AXIS_FAMILY_KEYWORDS,
    VALID_PRESET_DOMAINS,
    VALID_SUBJECT_CATEGORIES,
    load_json,
    normalize_list,
)


VALID_AXIS_SIGNAL_SUFFIXES = {"strong", "ambient"}
VALID_AXIS_SIGNAL_ALIASES = {"human_portrait"}


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


def validate_coherence_rules(data: dict[str, Any], errors: list[str]) -> None:
    rules = data.get("coherence_rules", {}) or {}
    if rules and not isinstance(rules, dict):
        errors.append("coherence_rules: must be an object")
        return
    if not rules:
        return

    valid_families = set(SEMANTIC_AXIS_FAMILY_KEYWORDS)
    by_slot = entry_ids_by_slot(data)
    all_ids = set()
    for ids in by_slot.values():
        all_ids |= ids
    all_ids |= {str(preset.get("id")) for preset in data.get("presets", [])}
    all_ids |= {str(recipe.get("id")) for recipe in data.get("recipes", [])}

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
    valid_families = set(SEMANTIC_AXIS_FAMILY_KEYWORDS)

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
    args = parser.parse_args()

    data = load_json(args.tags)
    errors: list[str] = []
    vocab = merged_facet_vocab(data)

    validate_filter_ids(data, errors)
    validate_coherence_rules(data, errors)
    validate_semantic_metadata(data, errors)
    validate_slot_applicability(data, errors)
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
