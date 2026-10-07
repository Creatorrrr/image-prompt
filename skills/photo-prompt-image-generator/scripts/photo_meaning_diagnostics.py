"""Deterministic evidence for authored class and relation matching.

This module reads no assets and supplies no requester meaning. Unknown text is
not a contradiction. A class match never creates a typed relation or hard gate.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Mapping

VERSION = "photo-meaning-diagnostics/v1"


def raw_axis_values(value: Any) -> list:
    """Retain the frozen assertion's text, spacing and scalar types."""
    if value is None:
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]


def axis_value_matches(value: Any, aliases: Mapping[str, list[str]]) -> dict:
    text = str(value or "")
    positive, negative, evidence = set(), set(), []
    for class_id, terms in aliases.items():
        for alias in terms:
            phrase = str(alias).strip()
            if not phrase:
                continue
            japanese = any("\u3040" <= char <= "\u30ff" for char in phrase)
            left_boundary = r"(?<![A-Za-z0-9_\uAC00-\uD7A3])" if japanese else r"(?<!\w)"
            pattern = left_boundary + r"\s+".join(re.escape(part) for part in phrase.split()) + r"(?=\W|$|(?:이|가|은|는|을|를|하지|하지는)?\s*(?:아니|않|없)|(?:は|が)?(?:ではない|じゃない|でない))"
            for hit in re.finditer(pattern, text, re.IGNORECASE):
                # Scope negation to this clause and this authored phrase. Other
                # natural-language scope remains unresolved rather than inferred.
                prefix = re.split(r"[,:;.!?。！？]|\b(?:but|however|yet)\b", text[:hit.start()], flags=re.I)[-1]
                suffix = text[hit.end():]
                before = bool(re.search(r"\b(?:not|never|without|no)\b(?:\W+\w+){0,4}\W*$", prefix, re.I))
                after = bool(re.match(r"\s*(?:은|는|이|가|을|를|하지|하지는)?\s*(?:아니|않|없|ではない|じゃない|でない)", suffix))
                uncertain = bool(re.search(r"\bnot\s+(?:only|just|merely)\s*$", prefix, re.I))
                negated = before or after or (japanese and prefix.endswith(("不", "非", "無")))
                (negative if negated else positive).add(class_id)
                if uncertain:
                    positive.add(class_id); negative.add(class_id)
                evidence.append({"class_id": class_id, "authored_term": phrase,
                                 "text": hit.group(), "start": hit.start(), "end": hit.end(),
                                 "polarity": "unresolved" if uncertain else ("negated" if negated else "positive"),
                                 "negation_context": prefix + hit.group() + suffix if negated or uncertain else None})
    ambiguous = positive & negative
    return {"classes": sorted(positive - ambiguous), "negated_classes": sorted(negative),
            "ambiguous_classes": sorted(ambiguous), "evidence": evidence,
            "match_basis": "authored_exact_or_bounded_phrase"}


def axis_check(axis: str, values: list, allowed: list, excluded: list,
               matcher: Callable[[Any], dict], *, source_id: str, advisory: bool = False) -> dict:
    matches = [matcher(value) for value in values]
    classes = set().union(*(set(row["classes"]) for row in matches)) if matches else set()
    negated = any(row["negated_classes"] for row in matches)
    negative_classes = set().union(*(set(row["negated_classes"]) for row in matches)) if matches else set()
    ambiguous = any(row["ambiguous_classes"] for row in matches) or bool(classes & negative_classes)
    classes -= negative_classes
    if not any(str(value if value is not None else "").strip() for value in values):
        code = "axis_absent"
    elif ambiguous:
        code = "axis_polarity_unresolved"
    elif classes & set(excluded):
        code = "axis_excluded_class"
    elif classes & set(allowed) or (not allowed and classes):
        code = "axis_class_match"
    elif not classes:
        code = "axis_value_negated" if negated else "axis_value_unrecognized"
    else:
        code = "axis_class_mismatch"
    return {"kind": "axis", "axis": axis, "code": code, "source_id": source_id,
            "source_path": f"semantic_assertions[{source_id}].axes.{axis}",
            "raw_value": values, "expected": {"allowed": allowed, "excluded": excluded},
            "observed": sorted(classes), "evidence": [item for row in matches for item in row["evidence"]],
            "match_basis": "authored_exact_or_bounded_phrase",
            "blocking_effect": not advisory and code != "axis_class_match"}


def relation_check(expected: dict, actual: list[dict], signature: Callable,
                   *, source_id: str) -> dict:
    operator = expected.get("operator")
    relevant = [row for row in actual if row.get("operator") == operator]
    if any(signature(row) == signature(expected) for row in relevant):
        code = "relation_match"
    elif not relevant:
        code = "relation_operator_absent"
    elif operator == "same_target":
        code = "relation_members_mismatch"
    elif operator == "temporal_order":
        code = "relation_order_mismatch"
    else:
        code = "relation_endpoints_mismatch"
    return {"kind": "relation", "code": code, "source_id": source_id,
            "source_path": f"semantic_assertions[{source_id}].relations", "raw_value": relevant,
            "expected": expected, "observed": relevant,
            "evidence": [row for row in relevant if signature(row) == signature(expected)],
            "match_basis": "typed_relation_signature", "blocking_effect": code != "relation_match"}
