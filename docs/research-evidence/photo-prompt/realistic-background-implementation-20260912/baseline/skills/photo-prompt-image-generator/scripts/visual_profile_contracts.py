"""Data-authored activation and component projection for visual profiles.

This module has no keyword-specific routing. Request evidence governs hard
activation; an authored component is the single source for its discovery,
literal evidence, composition instruction, and pixel gate.
"""

from __future__ import annotations

import copy
import re
from collections.abc import Callable, Mapping
from typing import Any


HARD_ACTIVATION_VERSION = "photo-visual-hard-activation/v1"
AUTHORED_COMPONENT_VERSION = "photo-authored-visual-components/v1"


def _terms(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value or any(
        not isinstance(term, str) or not term.strip() for term in value
    ):
        raise ValueError(f"{label} must be a non-empty string list")
    if len({term.casefold() for term in value}) != len(value):
        raise ValueError(f"{label} must contain distinct strings")
    return value


def validate_hard_activation(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {
        "contract_version", "required_any_groups"
    }:
        raise ValueError("hard_activation requires contract_version and required_any_groups")
    if value["contract_version"] != HARD_ACTIVATION_VERSION:
        raise ValueError("unsupported hard_activation contract_version")
    groups = value["required_any_groups"]
    if not isinstance(groups, list) or not groups:
        raise ValueError("hard_activation requires at least one evidence group")
    ids: set[str] = set()
    for group in groups:
        if not isinstance(group, dict) or set(group) != {"id", "any_terms"}:
            raise ValueError("hard_activation groups require id and any_terms")
        group_id = group["id"]
        if not isinstance(group_id, str) or not re.fullmatch(r"[a-z][a-z0-9_]+", group_id):
            raise ValueError("hard_activation group id must be snake_case")
        if group_id in ids:
            raise ValueError("duplicate hard_activation group id")
        ids.add(group_id)
        _terms(group["any_terms"], "hard_activation.any_terms")


def hard_activation_is_supported(
    profile: Mapping[str, Any],
    request_text: str,
    *,
    matches: Callable[[str, str], bool],
    is_negated: Callable[[str, str], bool],
) -> bool:
    policy = (profile.get("activation") or {}).get("hard_activation")
    if policy is None:
        return True
    validate_hard_activation(policy)
    return all(
        any(matches(request_text, term) and not is_negated(request_text, term)
            for term in group["any_terms"])
        for group in policy["required_any_groups"]
    )


def compile_visual_profile(
    profile: Mapping[str, Any],
    *,
    context_text: str = "",
    request_text: str = "",
    matches: Callable[[str, str], bool] | None = None,
) -> dict[str, Any]:
    """Compile source components, optionally specializing visible evidence.

    Omitted evidence is computed from request/core text and never supplied by
    a composer as a pass flag. Direct requester evidence for that component
    takes precedence over a visibility exception.
    """
    result = copy.deepcopy(dict(profile))
    source = profile.get("authored_components")
    if source is None:
        return result
    if (context_text or request_text) and matches is None:
        raise ValueError("context specialization requires a negation-aware request matcher")
    if context_text or request_text:
        # A loaded profile may carry compiled compatibility surfaces. Verify
        # their default source projection before applying request conditions.
        compile_visual_profile(profile)
    if not isinstance(source, dict) or set(source) != {"contract_version", "components"}:
        raise ValueError("authored_components requires contract_version and components")
    if source["contract_version"] != AUTHORED_COMPONENT_VERSION:
        raise ValueError("unsupported authored_components contract_version")
    components = source["components"]
    if not isinstance(components, list) or not components:
        raise ValueError("authored_components requires non-empty components")
    active: list[dict[str, Any]] = []
    seen: dict[str, set[str]] = {"id": set(), "evidence_field": set(), "gate": set()}
    for component in components:
        required = {"id", "match_terms", "evidence_field", "evidence_terms", "min_content_words", "instruction", "render_gate"}
        if not isinstance(component, dict) or not required <= set(component) or set(component) - required - {"applicability"}:
            raise ValueError("invalid authored component keys")
        for key in ("id", "evidence_field"):
            value = component[key]
            if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9_]+", value) or value in seen[key]:
                raise ValueError(f"invalid or duplicate authored component {key}")
            seen[key].add(value)
        if not component["evidence_field"].endswith("_phrase"):
            raise ValueError("authored component evidence_field must end in _phrase")
        _terms(component["match_terms"], "component.match_terms")
        _terms(component["evidence_terms"], "component.evidence_terms")
        if type(component["min_content_words"]) is not int or component["min_content_words"] < 2:
            raise ValueError("component.min_content_words must be at least two")
        if not isinstance(component["instruction"], str) or len(component["instruction"].split()) < 6:
            raise ValueError("component.instruction must describe a concrete relation")
        gate = component["render_gate"]
        if not isinstance(gate, dict) or set(gate) != {"id", "review_scale", "description"}:
            raise ValueError("invalid authored component render_gate")
        if not isinstance(gate["id"], str) or not re.fullmatch(r"vo_[a-z0-9_]+", gate["id"]) or gate["id"] in seen["gate"]:
            raise ValueError("invalid or duplicate authored component render gate id")
        seen["gate"].add(gate["id"])
        if gate["review_scale"] not in {"thumbnail", "native", "both"} or len(str(gate["description"]).split()) < 6:
            raise ValueError("invalid authored component render gate scope or description")
        applicability = component.get("applicability")
        if applicability is not None:
            if not isinstance(applicability, dict) or set(applicability) != {"omit_if_any_terms", "retain_if_requested_any_terms"}:
                raise ValueError("invalid component applicability keys")
            omitted_terms = _terms(applicability["omit_if_any_terms"], "component.omit_if_any_terms")
            retained_terms = _terms(applicability["retain_if_requested_any_terms"], "component.retain_if_requested_any_terms")
            if matches is not None and any(matches(context_text, term) for term in omitted_terms) and not any(
                matches(request_text, term) for term in retained_terms
            ):
                continue
        active.append(component)
    if not active:
        raise ValueError("component applicability cannot remove every invariant")
    result.setdefault("semantics", {})["component_semantics"] = {
        "minimum_component_groups": len(active),
        "required_group_ids": [item["id"] for item in active],
        "groups": [{"id": item["id"], "any_terms": copy.deepcopy(item["match_terms"])} for item in active],
    }
    result["required_evidence_fields"] = [item["evidence_field"] for item in active]
    result["evidence_requirements"] = {
        item["evidence_field"]: {
            "min_content_words": item["min_content_words"],
            "must_mention_any": copy.deepcopy(item["evidence_terms"]),
        }
        for item in active
    }
    result["render_gates"] = [copy.deepcopy(item["render_gate"]) for item in active]
    result["composition_instruction"] = " ".join(item["instruction"] for item in active)
    if not context_text and not request_text:
        for field in ("required_evidence_fields", "evidence_requirements", "render_gates", "composition_instruction"):
            if field in profile and profile[field] != result[field]:
                raise ValueError(f"{field} conflicts with its authored component source")
        existing_groups = (profile.get("semantics") or {}).get("component_semantics")
        if existing_groups is not None and existing_groups != result["semantics"]["component_semantics"]:
            raise ValueError("component_semantics conflicts with its authored component source")
    return result
