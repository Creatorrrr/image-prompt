"""Positive retrieval projection for authored visual profiles.

The allowlist is shared by lexical and vector retrieval. Claim limits,
contrasts, provenance, applicability and validation instructions are retained
in their authored owners but never become positive retrieval evidence. This
projection deliberately does not try to classify or strip negative words:
negation can itself be a meaningful visual property.
"""

from __future__ import annotations

from typing import Any


def _strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        values = [values] if isinstance(values, str) else []
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = " ".join(value.split())
        if text and text.casefold() not in seen:
            seen.add(text.casefold())
            result.append(text)
    return result


def positive_visual_profile_fields(profile: dict[str, Any]) -> dict[str, list[str]]:
    """Return only visual-language fields, preserving complete authored units."""
    semantics = profile.get("semantics") or {}
    activation = profile.get("activation") or {}
    concept = profile.get("concept_candidate") or {}
    components = list(_strings(semantics.get("visual_components")))
    groups = (semantics.get("component_semantics") or {}).get("groups") or []
    for group in groups:
        if isinstance(group, dict):
            components.extend(_strings(group.get("any_terms")))
    return {
        "aliases": _strings(
            _strings(activation.get("exact_terms"))
            + _strings(activation.get("project_glossary_aliases"))
        ),
        "definition": _strings(semantics.get("definition")),
        "paraphrases": _strings(semantics.get("paraphrase_examples")),
        "visual_components": _strings(components),
        "support_cues": _strings(concept.get("concept_terms")),
    }


def positive_visual_profile_text(profile: dict[str, Any]) -> str:
    fields = positive_visual_profile_fields(profile)
    # Exact aliases have their own authoritative lookup. Approximate retrieval
    # describes visible meaning without category IDs or component-group IDs.
    return " | ".join(_strings([
        value
        for name in ("definition", "paraphrases", "visual_components", "support_cues")
        for value in fields[name]
    ]))
