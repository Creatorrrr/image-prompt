"""Shared candidate-free envelope and authorial-core normalization.

These are the original producer validators, used on both sides of core freeze.
Only authored current inputs and neutral precore definitions are interpreted.
"""
from __future__ import annotations
import copy
import hashlib
import json
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set
import creative_controls
import photo_camera_authoring as photo_camera_evidence
from photo_authoring_contracts import (
    AUTHORIAL_CORE_V3_CONTRACT_VERSION,
    AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS,
    AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
    AUTHORIAL_PROMPT_MIN_WORDS,
    AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
    CHARACTER_RESPONSE_RELATION_MEMBERS,
    CHARACTER_RESPONSE_REQUIRED_AXES,
    CHARACTER_RESPONSE_REQUIRED_EVIDENCE,
    INTENT_LOCK_CONTRACT_VERSION,
    INTENT_LOCK_DIMENSIONS,
    INTENT_LOCK_PROPERTY_CONTRACT_VERSION,
    RENDER_REPAIR_ALLOWED_AXES,
    RENDER_REPAIR_CONTACT_EXPECTATIONS,
    RENDER_REPAIR_DIMENSION_AXES,
    RENDER_REPAIR_IMPORTANCE_VALUES,
    RENDER_REPAIR_INTERACTION_STATES,
    RENDER_REPAIR_RELATION_ORIGINS,
    REQUEST_BINDING_CONTRACT_VERSION,
    REQUEST_ENVELOPE_CONTRACT_VERSION,
    REQUEST_LINEAGE_V2_CONTRACT_VERSION,
    REQUIRED_INTENT_LOCK_DIMENSIONS,
    SUBJECT_CATEGORIES,
    authored_subject_category,
    canonical_json_sha256,
)
JsonDict = Dict[str, Any]

CHARACTER_RESPONSE_RELATION_FIELDS = {
    "contrasts": {"operator", "left", "right"},
    "same_target": {"operator", "members"},
    "temporal_order": {"operator", "first", "then"},
}

def character_response_relation_signature(
    relation: Mapping[str, Any],
) -> tuple[Any, ...]:
    """Return a semantic signature; same-target member order is immaterial."""

    operator = str(relation.get("operator") or "")
    if operator == "same_target":
        return operator, tuple(sorted(normalize_list(relation.get("members"))))
    if operator == "contrasts":
        return operator, str(relation.get("left") or ""), str(
            relation.get("right") or ""
        )
    if operator == "temporal_order":
        return operator, str(relation.get("first") or ""), str(
            relation.get("then") or ""
        )
    return operator, canonical_json_sha256(relation)

def clean_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text

def find_blanket_negative_directives(text: str) -> List[str]:
    """Find prompt-writing directives that delete broad visual semantics.

    This deliberately targets instruction-shaped prose, not every grammatical
    negation.  Narrative phrases such as ``she does not look away`` are not
    classified here.  Broad clauses such as ``No contact, gore, or extra
    people`` and ``never touching anyone`` are, because they behave like a
    second ungrounded request embedded in the positive prompt.
    """

    value = str(text or "")
    patterns = (
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)((?:no\b|do\s+not\b|don't\b|avoid\b|exclude\b)[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)(never\s+(?:touch(?:es|ed|ing)?|inject(?:s|ed|ing)?|contact(?:s|ed|ing)?|show(?:s|ed|ing)?|depict(?:s|ed|ing)?|include(?:s|d|ing)?|use(?:s|d|ing)?|reveal(?:s|ed|ing)?|sexualiz(?:e|es|ed|ing)|crop(?:s|ped|ping)?|add(?:s|ed|ing)?)\b[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
    )
    directives: List[str] = []
    seen: Set[str] = set()
    for pattern in patterns:
        for match in pattern.finditer(value):
            directive = clean_spaces(match.group(1))
            key = directive.casefold()
            if directive and key not in seen:
                directives.append(directive)
                seen.add(key)
    return directives

def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]

def authorial_request_content_words(text: str) -> List[str]:
    stopwords = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "into",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    return [
        token.lower()
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]*|[가-힣]{2,}|[ぁ-んァ-ン一-龯]{2,}", str(text or ""))
        if token.lower() not in stopwords
    ]

def normalize_request_envelope(payload: Any) -> JsonDict:
    """Validate the requesting-user text before an agent authors a v2 core.

    The envelope is intentionally separate from the core.  It gives the CLI a
    second, exact source of truth and lets a multi-part request select only
    byte-grounded spans instead of inventing a per-arm paraphrase.
    """

    if not isinstance(payload, dict):
        raise ValueError("--request-envelope-json must contain one JSON object")
    allowed_fields = {
        "contract_version",
        "provenance",
        "request_id",
        "request_text",
        "request_sha256",
        "active_spans",
    }
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "request envelope contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    if payload.get("contract_version") != REQUEST_ENVELOPE_CONTRACT_VERSION:
        raise ValueError(
            "request envelope contract_version must be "
            f"{REQUEST_ENVELOPE_CONTRACT_VERSION!r}"
        )
    if payload.get("provenance") != "requesting_user":
        raise ValueError("request envelope provenance must be 'requesting_user'")

    request_id = str(payload.get("request_id") or "").strip()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", request_id) is None:
        raise ValueError(
            "request envelope request_id must be a stable 1-128 character identifier"
        )
    request_text = payload.get("request_text")
    if not isinstance(request_text, str) or not request_text.strip():
        raise ValueError("request envelope request_text must be the non-empty exact user text")
    request_sha256 = str(payload.get("request_sha256") or "").lower()
    expected_request_sha256 = hashlib.sha256(request_text.encode("utf-8")).hexdigest()
    if request_sha256 != expected_request_sha256:
        raise ValueError("request envelope request_sha256 does not match request_text bytes")

    raw_spans = payload.get("active_spans")
    if not isinstance(raw_spans, list) or not 1 <= len(raw_spans) <= 16:
        raise ValueError("request envelope active_spans must contain one to sixteen rows")
    spans: List[JsonDict] = []
    seen_ids: Set[str] = set()
    seen_texts: Set[str] = set()
    for index, item in enumerate(raw_spans):
        if not isinstance(item, dict) or set(item) != {"span_id", "start", "end", "text"}:
            raise ValueError(
                f"request envelope active span {index} must contain only span_id, start, end, and text"
            )
        span_id = str(item.get("span_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", span_id) is None:
            raise ValueError(f"request envelope active span {index} has an invalid span_id")
        if span_id in seen_ids:
            raise ValueError(f"request envelope repeats active span id {span_id!r}")
        seen_ids.add(span_id)
        start = item.get("start")
        end = item.get("end")
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, int)
            or not isinstance(end, int)
            or start < 0
            or end <= start
            or end > len(request_text)
        ):
            raise ValueError(f"request envelope active span {index} has invalid offsets")
        text = item.get("text")
        if not isinstance(text, str) or request_text[start:end] != text:
            raise ValueError(
                f"request envelope active span {index} text does not match request_text offsets"
            )
        text_key = text.casefold()
        if text_key in seen_texts:
            raise ValueError("request envelope active span texts must be distinct")
        seen_texts.add(text_key)
        spans.append({"span_id": span_id, "start": start, "end": end, "text": text})
    spans.sort(key=lambda row: (int(row["start"]), int(row["end"]), str(row["span_id"])))
    for previous, current in zip(spans, spans[1:]):
        if int(current["start"]) < int(previous["end"]):
            raise ValueError("request envelope active spans must not overlap")

    normalized: JsonDict = {
        "contract_version": REQUEST_ENVELOPE_CONTRACT_VERSION,
        "provenance": "requesting_user",
        "request_id": request_id,
        "request_text": request_text,
        "request_sha256": request_sha256,
        "active_spans": spans,
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    normalized["envelope_id"] = normalized["canonical_sha256"][:16]
    return normalized

def request_envelope_active_texts(envelope: JsonDict) -> List[str]:
    return [
        str(item.get("text") or "")
        for item in envelope.get("active_spans") or []
        if isinstance(item, dict) and str(item.get("text") or "")
    ]

def request_scope_contains(envelope: JsonDict, source_text: str) -> bool:
    needle = str(source_text or "").strip().casefold()
    return bool(needle) and any(
        needle in text.casefold() for text in request_envelope_active_texts(envelope)
    )

def normalize_intent_lock(
    payload: Any,
    *,
    envelope: JsonDict,
    baseline_prompt_en: str,
    allowed_dimensions: Set[str] = INTENT_LOCK_DIMENSIONS,
    minimum_open_dimensions: int = 2,
) -> JsonDict:
    if not isinstance(payload, dict):
        raise ValueError("authorial core intent_lock must be one JSON object")
    allowed_fields = {
        "contract_version",
        "priority",
        "semantic_anchors",
        "locked_dimensions",
        "open_dimensions",
    }
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core intent_lock contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    property_lock = payload.get("contract_version") == INTENT_LOCK_PROPERTY_CONTRACT_VERSION
    if payload.get("contract_version") not in {INTENT_LOCK_CONTRACT_VERSION, INTENT_LOCK_PROPERTY_CONTRACT_VERSION}:
        raise ValueError(
            f"authorial core intent_lock contract_version must be {INTENT_LOCK_CONTRACT_VERSION!r}"
        )
    if payload.get("priority") != "requesting_user":
        raise ValueError("authorial core intent_lock priority must be 'requesting_user'")
    if minimum_open_dimensions == 0 and not isinstance(
        payload.get("open_dimensions"), list
    ):
        raise ValueError(
            "authorial core intent_lock requires an explicit open_dimensions list; use [] when no variation is permitted"
        )

    locked_dimensions = [
        str(item).strip()
        for item in normalize_list(payload.get("locked_dimensions"))
        if str(item).strip()
    ]
    open_dimensions = [
        str(item).strip()
        for item in normalize_list(payload.get("open_dimensions"))
        if str(item).strip()
    ]
    if not locked_dimensions or len(set(locked_dimensions)) != len(locked_dimensions):
        raise ValueError("authorial core intent_lock requires distinct locked_dimensions")
    if len(open_dimensions) < minimum_open_dimensions:
        raise ValueError(
            "authorial core intent_lock requires at least two distinct open_dimensions"
        )
    if len(set(open_dimensions)) != len(open_dimensions):
        raise ValueError("authorial core intent_lock requires distinct open_dimensions")
    unknown_dimensions = sorted(
        (set(locked_dimensions) | set(open_dimensions)) - allowed_dimensions
    )
    if unknown_dimensions:
        raise ValueError(
            "authorial core intent_lock contains unknown dimensions: "
            + ", ".join(unknown_dimensions)
        )
    missing_required_dimensions = sorted(
        REQUIRED_INTENT_LOCK_DIMENSIONS - set(locked_dimensions)
    )
    if missing_required_dimensions:
        raise ValueError(
            "authorial core intent_lock must lock the governing concept, subject, and event dimensions: "
            + ", ".join(missing_required_dimensions)
        )
    overlap = sorted(set(locked_dimensions) & set(open_dimensions))
    if overlap:
        raise ValueError(
            "authorial core intent_lock dimensions cannot be both locked and open: "
            + ", ".join(overlap)
        )

    raw_anchors = payload.get("semantic_anchors")
    if not isinstance(raw_anchors, list) or not 1 <= len(raw_anchors) <= 16:
        raise ValueError(
            "authorial core intent_lock semantic_anchors must contain one to sixteen rows"
        )
    anchors: List[JsonDict] = []
    seen_ids: Set[str] = set()
    seen_evidence: Set[str] = set()
    seen_properties: Set[tuple] = set()
    for index, item in enumerate(raw_anchors):
        anchor_fields = {
            "anchor_id",
            "source_text",
            "dimension",
            "prompt_evidence",
        }
        if property_lock and isinstance(item, dict) and "property" in item:
            anchor_fields.update({"target", "property"})
        if not isinstance(item, dict) or set(item) != anchor_fields:
            raise ValueError(
                f"authorial core intent anchor {index} must contain only anchor_id, source_text, dimension, and prompt_evidence"
            )
        anchor_id = str(item.get("anchor_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", anchor_id) is None:
            raise ValueError(f"authorial core intent anchor {index} has an invalid anchor_id")
        if anchor_id in seen_ids:
            raise ValueError(f"authorial core repeats intent anchor id {anchor_id!r}")
        seen_ids.add(anchor_id)
        source_text = str(item.get("source_text") or "").strip()
        dimension = str(item.get("dimension") or "").strip()
        evidence = clean_spaces(str(item.get("prompt_evidence") or ""))
        if len(authorial_request_content_words(source_text)) < 1:
            raise ValueError(
                f"authorial core intent anchor {index} source_text must contain a substantive requester term"
            )
        if not request_scope_contains(envelope, source_text):
            raise ValueError(
                f"authorial core intent anchor {index} source_text is not grounded in an active requesting-user span"
            )
        is_property = "property" in item
        if is_property:
            if dimension not in open_dimensions or any(
                re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*", str(item[key])) is None
                for key in ("target", "property")
            ):
                raise ValueError("a property anchor needs an open dimension and canonical target/property paths")
            property_key = (dimension, item["target"], item["property"])
            if property_key in seen_properties:
                raise ValueError("intent_lock contains duplicate property anchors")
            seen_properties.add(property_key)
        elif dimension not in locked_dimensions:
            raise ValueError(
                f"authorial core intent anchor {index} dimension must be locked"
            )
        if len(authorial_request_content_words(evidence)) < 2:
            raise ValueError(
                f"authorial core intent anchor {index} prompt_evidence needs at least two content words"
            )
        if evidence.casefold() not in baseline_prompt_en.casefold():
            raise ValueError(
                f"authorial core intent anchor {index} prompt_evidence must occur in baseline_prompt_en"
            )
        if evidence.casefold() in seen_evidence and not is_property:
            raise ValueError(
                "authorial core intent anchors require distinct prompt_evidence for each locked dimension"
            )
        seen_evidence.add(evidence.casefold())
        anchors.append(
            {
                "anchor_id": anchor_id,
                "source_text": source_text,
                "dimension": dimension,
                "prompt_evidence": evidence,
                **({"target": item["target"], "property": item["property"]} if is_property else {}),
            }
        )

    anchored_dimensions = {str(item["dimension"]) for item in anchors}
    missing_dimension_anchors = sorted(set(locked_dimensions) - anchored_dimensions)
    if missing_dimension_anchors:
        raise ValueError(
            "authorial core intent_lock requires at least one semantic anchor for every locked dimension: "
            + ", ".join(missing_dimension_anchors)
        )
    uncovered_span_ids = [
        str(span.get("span_id") or "")
        for span in envelope.get("active_spans") or []
        if isinstance(span, dict)
        and not any(
            str(anchor.get("source_text") or "").casefold()
            in str(span.get("text") or "").casefold()
            for anchor in anchors
        )
    ]
    if uncovered_span_ids:
        raise ValueError(
            "authorial core intent_lock requires semantic-anchor coverage for every active requesting-user span: "
            + ", ".join(uncovered_span_ids)
        )

    normalized: JsonDict = {
        "contract_version": payload["contract_version"],
        "priority": "requesting_user",
        "semantic_anchors": anchors,
        "locked_dimensions": locked_dimensions,
        "open_dimensions": open_dimensions,
        "augmentation_policy": "open_dimensions_only_and_subordinate",
        "material_change_policy": "rebuild_core_after_requester_input",
        "candidate_revision_policy": "forbidden",
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    normalized["lock_id"] = normalized["canonical_sha256"][:16]
    return normalized

def normalize_semantic_assertions(
    payload: Any,
    *,
    envelope: JsonDict,
    intent_lock: JsonDict,
    baseline_prompt_en: str,
) -> List[JsonDict]:
    """Validate typed, source-grounded meaning without re-parsing raw text."""

    if not isinstance(payload, list) or len(payload) > 16:
        raise ValueError(
            "authorial core v3 semantic_assertions must be a list of at most sixteen rows"
        )
    span_ids = {
        str(item.get("source_span_id", item.get("span_id")) or "")
        for item in envelope.get("active_spans") or []
        if isinstance(item, dict)
    }
    locked_dimensions = set(intent_lock.get("locked_dimensions") or [])
    open_dimensions = set(intent_lock.get("open_dimensions") or [])
    normalized: List[JsonDict] = []
    seen_ids: Set[str] = set()
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"semantic assertion {index} must be one JSON object")
        allowed_fields = {
            "assertion_id",
            "dimension",
            "polarity",
            "source_span_ids",
            "axes",
            "relations",
            "evidence",
            "affected_dimensions",
        }
        unknown_fields = sorted(set(item) - allowed_fields)
        if unknown_fields:
            raise ValueError(
                f"semantic assertion {index} contains unsupported fields: "
                + ", ".join(unknown_fields)
            )
        assertion_id = str(item.get("assertion_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", assertion_id) is None:
            raise ValueError(f"semantic assertion {index} has an invalid assertion_id")
        if assertion_id in seen_ids:
            raise ValueError(f"semantic assertion repeats id {assertion_id!r}")
        seen_ids.add(assertion_id)
        dimension = str(item.get("dimension") or "").strip()
        if dimension not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
            raise ValueError(
                f"semantic assertion {assertion_id!r} has unknown dimension {dimension!r}"
            )
        polarity = str(item.get("polarity") or "").strip()
        if polarity not in {"required", "advisory", "excluded"}:
            raise ValueError(
                f"semantic assertion {assertion_id!r} polarity must be required, advisory, or excluded"
            )
        source_span_ids = [
            str(value).strip()
            for value in normalize_list(item.get("source_span_ids"))
            if str(value).strip()
        ]
        if (
            not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids).issubset(span_ids)
        ):
            raise ValueError(
                f"semantic assertion {assertion_id!r} requires distinct active source_span_ids"
            )
        affected_dimensions = [
            str(value).strip()
            for value in normalize_list(item.get("affected_dimensions") or [dimension])
            if str(value).strip()
        ]
        if (
            not affected_dimensions
            or len(affected_dimensions) != len(set(affected_dimensions))
            or not set(affected_dimensions).issubset(
                AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
            )
        ):
            raise ValueError(
                f"semantic assertion {assertion_id!r} has invalid affected_dimensions"
            )
        if polarity == "required" and not set(affected_dimensions).issubset(
            locked_dimensions
        ):
            raise ValueError(
                f"required semantic assertion {assertion_id!r} must affect only locked dimensions"
            )
        if polarity == "advisory" and not set(affected_dimensions).issubset(
            open_dimensions
        ):
            raise ValueError(
                f"advisory semantic assertion {assertion_id!r} must affect only open dimensions"
            )

        raw_axes = item.get("axes")
        if not isinstance(raw_axes, dict) or not 1 <= len(raw_axes) <= 16:
            raise ValueError(
                f"semantic assertion {assertion_id!r} axes must contain one to sixteen typed values"
            )
        axes: JsonDict = {}
        for raw_key, raw_value in raw_axes.items():
            key = str(raw_key).strip()
            if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key) is None:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} has invalid axis key {key!r}"
                )
            values = (
                [clean_spaces(str(value)) for value in raw_value]
                if isinstance(raw_value, list)
                else [clean_spaces(str(raw_value))]
            )
            values = [value for value in values if value]
            if not values or len(values) > 8 or len(values) != len(set(values)):
                raise ValueError(
                    f"semantic assertion {assertion_id!r} axis {key!r} has invalid values"
                )
            axes[key] = values if isinstance(raw_value, list) else values[0]

        relations: List[JsonDict] = []
        if "relations" in item:
            raw_relations = item.get("relations")
            if dimension != "character_response":
                raise ValueError(
                    f"semantic assertion {assertion_id!r} relations are supported only for character_response"
                )
            if not isinstance(raw_relations, list) or not 1 <= len(raw_relations) <= 8:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} relations must contain one to eight rows"
                )
            relation_signatures: Set[tuple[Any, ...]] = set()
            for relation_index, raw_relation in enumerate(raw_relations):
                if not isinstance(raw_relation, dict):
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} must be one object"
                    )
                operator = str(raw_relation.get("operator") or "").strip()
                expected_fields = CHARACTER_RESPONSE_RELATION_FIELDS.get(operator)
                if expected_fields is None or set(raw_relation) != expected_fields:
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} has an invalid operator or shape"
                    )
                if operator == "same_target":
                    members = [
                        str(value).strip()
                        for value in normalize_list(raw_relation.get("members"))
                        if str(value).strip()
                    ]
                    if (
                        not 2 <= len(members) <= 8
                        or len(members) != len(set(members))
                        or "relationship_target" not in members
                        or not set(members).issubset(
                            CHARACTER_RESPONSE_RELATION_MEMBERS
                        )
                        or any(
                            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", value) is None
                            for value in members
                        )
                    ):
                        raise ValueError(
                            f"semantic assertion {assertion_id!r} relation {relation_index} needs distinct semantic members"
                        )
                    normalized_relation = {"operator": operator, "members": members}
                    signature = character_response_relation_signature(
                        normalized_relation
                    )
                    if signature in relation_signatures:
                        raise ValueError(
                            f"semantic assertion {assertion_id!r} relation {relation_index} repeats a semantic relation"
                        )
                    relation_signatures.add(signature)
                    relations.append(normalized_relation)
                    continue
                left_key, right_key = (
                    ("left", "right")
                    if operator == "contrasts"
                    else ("first", "then")
                )
                left = str(raw_relation.get(left_key) or "").strip()
                right = str(raw_relation.get(right_key) or "").strip()
                if (
                    left == right
                    or left not in CHARACTER_RESPONSE_RELATION_MEMBERS
                    or right not in CHARACTER_RESPONSE_RELATION_MEMBERS
                    or re.fullmatch(r"[a-z][a-z0-9_]{0,63}", left) is None
                    or re.fullmatch(r"[a-z][a-z0-9_]{0,63}", right) is None
                ):
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} needs two distinct semantic members"
                    )
                normalized_relation = {
                    "operator": operator,
                    left_key: left,
                    right_key: right,
                }
                signature = character_response_relation_signature(
                    normalized_relation
                )
                if signature in relation_signatures:
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} repeats a semantic relation"
                    )
                relation_signatures.add(signature)
                relations.append(normalized_relation)

        raw_evidence = item.get("evidence") or {}
        if not isinstance(raw_evidence, dict) or len(raw_evidence) > 16:
            raise ValueError(
                f"semantic assertion {assertion_id!r} evidence must be one bounded object"
            )
        evidence: JsonDict = {}
        for raw_key, raw_value in raw_evidence.items():
            key = str(raw_key).strip()
            if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key) is None:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} has invalid evidence key {key!r}"
                )
            phrase = clean_spaces(str(raw_value or ""))
            if len(authorial_request_content_words(phrase)) < 2:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} evidence {key!r} needs at least two content words"
                )
            if phrase.casefold() not in baseline_prompt_en.casefold():
                raise ValueError(
                    f"semantic assertion {assertion_id!r} evidence {key!r} must occur in baseline_prompt_en"
                )
            evidence[key] = phrase
        if polarity == "required" and not evidence:
            raise ValueError(
                f"required semantic assertion {assertion_id!r} needs frozen baseline evidence"
            )
        if dimension == "character_response" and polarity == "required":
            missing_axes = sorted(CHARACTER_RESPONSE_REQUIRED_AXES - set(axes))
            if missing_axes:
                raise ValueError(
                    "required character_response assertion is missing generic semantic axes: "
                    + ", ".join(missing_axes)
                )
            primary_actions = normalize_list(axes.get("primary_action"))
            if len(primary_actions) != 1:
                raise ValueError(
                    "required character_response assertion must select exactly one primary_action"
                )
            leak_channels = axes.get("affect_leak_channels")
            if not isinstance(leak_channels, list) or len(leak_channels) != 1:
                raise ValueError(
                    "required character_response assertion must select exactly one primary affect_leak_channel"
                )
            missing_evidence = sorted(
                CHARACTER_RESPONSE_REQUIRED_EVIDENCE - set(evidence)
            )
            if missing_evidence:
                raise ValueError(
                    "required character_response assertion is missing generic causal evidence: "
                    + ", ".join(missing_evidence)
                )
        normalized_assertion = {
            "assertion_id": assertion_id,
            "dimension": dimension,
            "polarity": polarity,
            "source_span_ids": source_span_ids,
            "axes": axes,
            "evidence": evidence,
            "affected_dimensions": affected_dimensions,
        }
        if relations:
            normalized_assertion["relations"] = relations
        normalized.append(normalized_assertion)
    required_character_assertions = [
        item
        for item in normalized
        if item.get("dimension") == "character_response"
        and item.get("polarity") == "required"
    ]
    if len(required_character_assertions) > 1:
        raise ValueError(
            "authorial core v3 allows at most one required character_response assertion"
        )
    return normalized

def normalize_request_lineage(
    payload: Any,
    *,
    current_request_id: str,
    envelope: Optional[JsonDict] = None,
    intent_lock: Optional[JsonDict] = None,
    baseline_prompt_en: str = "",
    semantic_assertions: Optional[Sequence[JsonDict]] = None,
) -> Optional[JsonDict]:
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValueError("authorial core request_lineage must be an object or null")
    base_fields = {
        "parent_request_id",
        "parent_core_sha256",
        "preserved_dimensions",
        "allowed_changes",
    }
    contract_version = str(payload.get("contract_version") or "").strip()
    is_v2 = contract_version == REQUEST_LINEAGE_V2_CONTRACT_VERSION
    if contract_version and not is_v2:
        raise ValueError(
            "request_lineage contract_version must be "
            f"{REQUEST_LINEAGE_V2_CONTRACT_VERSION!r} when supplied"
        )
    allowed_fields = set(base_fields)
    if is_v2:
        allowed_fields.update({"contract_version", "repair_targets"})
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core request_lineage contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    parent_request_id = str(payload.get("parent_request_id") or "").strip()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", parent_request_id) is None:
        raise ValueError("request_lineage parent_request_id is invalid")
    if parent_request_id == current_request_id:
        raise ValueError("request_lineage parent_request_id must differ from the current request")
    parent_core_sha256 = str(payload.get("parent_core_sha256") or "").lower()
    if re.fullmatch(r"[0-9a-f]{64}", parent_core_sha256) is None:
        raise ValueError("request_lineage parent_core_sha256 must be one SHA-256 digest")
    preserved_dimensions = [
        str(value).strip()
        for value in normalize_list(payload.get("preserved_dimensions"))
        if str(value).strip()
    ]
    allowed_changes = [
        str(value).strip()
        for value in normalize_list(payload.get("allowed_changes"))
        if str(value).strip()
    ]
    for label, values in (
        ("preserved_dimensions", preserved_dimensions),
        ("allowed_changes", allowed_changes),
    ):
        if (
            not values
            or len(values) != len(set(values))
            or not set(values).issubset(AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        ):
            raise ValueError(f"request_lineage {label} contains invalid dimensions")
    if set(preserved_dimensions) & set(allowed_changes):
        raise ValueError(
            "request_lineage preserved_dimensions and allowed_changes must be disjoint"
        )
    normalized: JsonDict = {
        "parent_request_id": parent_request_id,
        "parent_core_sha256": parent_core_sha256,
        "preserved_dimensions": preserved_dimensions,
        "allowed_changes": allowed_changes,
    }
    if not is_v2:
        return normalized

    if envelope is None or intent_lock is None:
        raise ValueError(
            "photo-request-lineage/v2 requires the active request envelope and intent lock"
        )
    raw_targets = payload.get("repair_targets")
    if not isinstance(raw_targets, list) or not 1 <= len(raw_targets) <= 8:
        raise ValueError(
            "photo-request-lineage/v2 repair_targets must contain one to eight rows"
        )
    active_span_ids = {
        str(row.get("span_id") or "")
        for row in envelope.get("active_spans") or []
        if isinstance(row, dict)
    }
    locked_dimensions = set(intent_lock.get("locked_dimensions") or [])
    assertions = [
        row
        for row in semantic_assertions or []
        if isinstance(row, dict) and row.get("polarity") == "required"
    ]
    normalized_targets: List[JsonDict] = []
    seen_repair_ids: Set[str] = set()
    for index, raw_target in enumerate(raw_targets):
        if not isinstance(raw_target, dict):
            raise ValueError(f"request_lineage repair target {index} must be one object")
        expected_fields = {
            "repair_id",
            "source_span_ids",
            "importance",
            "relation_origin",
            "actor_phrase",
            "object_phrase",
            "interaction_state",
            "actor_object_contact",
            "protected_dimensions",
            "allowed_repair_axes",
            "interaction_phrase",
            "recognition_phrase",
        }
        if set(raw_target) != expected_fields:
            raise ValueError(
                f"request_lineage repair target {index} must contain exactly: "
                + ", ".join(sorted(expected_fields))
            )
        repair_id = str(raw_target.get("repair_id") or "").strip()
        if (
            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", repair_id) is None
            or repair_id in seen_repair_ids
        ):
            raise ValueError(
                f"request_lineage repair target {index} has an invalid or repeated repair_id"
            )
        seen_repair_ids.add(repair_id)
        source_span_ids = [
            str(value).strip()
            for value in normalize_list(raw_target.get("source_span_ids"))
            if str(value).strip()
        ]
        if (
            not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids).issubset(active_span_ids)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} requires distinct active source_span_ids"
            )
        importance = str(raw_target.get("importance") or "").strip()
        if importance not in RENDER_REPAIR_IMPORTANCE_VALUES:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} importance must be primary or supporting"
            )
        relation_origin = str(raw_target.get("relation_origin") or "").strip()
        if relation_origin not in RENDER_REPAIR_RELATION_ORIGINS:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported relation_origin"
            )
        interaction_state = str(raw_target.get("interaction_state") or "").strip()
        if interaction_state not in RENDER_REPAIR_INTERACTION_STATES:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported interaction_state"
            )
        actor_object_contact = str(
            raw_target.get("actor_object_contact") or ""
        ).strip()
        if actor_object_contact not in RENDER_REPAIR_CONTACT_EXPECTATIONS:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported actor_object_contact"
            )
        if (
            interaction_state
            in {"held", "wielded", "used", "handed_off", "carried", "worn"}
            and actor_object_contact == "absent"
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} cannot remove actor-object contact from an interactive state"
            )
        protected_dimensions = [
            str(value).strip()
            for value in normalize_list(raw_target.get("protected_dimensions"))
            if str(value).strip()
        ]
        protected_source_dimensions = (
            set(preserved_dimensions)
            if relation_origin == "parent_preserved"
            else set(allowed_changes)
        )
        if (
            not protected_dimensions
            or len(protected_dimensions) != len(set(protected_dimensions))
            or "action" not in protected_dimensions
            or not set(protected_dimensions).issubset(locked_dimensions)
            or not set(protected_dimensions).issubset(protected_source_dimensions)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} must protect locked action plus any other dimensions from its declared relation origin"
            )
        allowed_repair_axes = [
            str(value).strip()
            for value in normalize_list(raw_target.get("allowed_repair_axes"))
            if str(value).strip()
        ]
        if (
            not allowed_repair_axes
            or len(allowed_repair_axes) != len(set(allowed_repair_axes))
            or not set(allowed_repair_axes).issubset(RENDER_REPAIR_ALLOWED_AXES)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has invalid allowed_repair_axes"
            )
        for repair_axis, dimension in RENDER_REPAIR_DIMENSION_AXES.items():
            if repair_axis in allowed_repair_axes and dimension not in allowed_changes:
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} axis {repair_axis!r} requires {dimension!r} in allowed_changes"
                )

        actor_phrase = clean_spaces(str(raw_target.get("actor_phrase") or ""))
        object_phrase = clean_spaces(str(raw_target.get("object_phrase") or ""))
        interaction_phrase = clean_spaces(
            str(raw_target.get("interaction_phrase") or "")
        )
        recognition_phrase = clean_spaces(
            str(raw_target.get("recognition_phrase") or "")
        )
        for label, phrase, minimum in (
            ("actor_phrase", actor_phrase, 1),
            ("object_phrase", object_phrase, 1),
            ("interaction_phrase", interaction_phrase, 4),
            ("recognition_phrase", recognition_phrase, 4),
        ):
            if len(authorial_request_content_words(phrase)) < minimum:
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} {label} is not substantive"
                )
            if phrase.casefold() not in baseline_prompt_en.casefold():
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} {label} must occur in baseline_prompt_en"
                )
        if interaction_phrase.casefold() == recognition_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} needs distinct interaction and recognition evidence"
            )
        if actor_phrase.casefold() not in interaction_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} interaction_phrase must contain actor_phrase"
            )
        if object_phrase.casefold() not in interaction_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} interaction_phrase must contain object_phrase"
            )
        if object_phrase.casefold() not in recognition_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} recognition_phrase must contain object_phrase"
            )
        evidence_pair = {interaction_phrase.casefold(), recognition_phrase.casefold()}
        owns_evidence_pair = any(
            evidence_pair.issubset(
                {
                    str(value).casefold()
                    for value in (assertion.get("evidence") or {}).values()
                    if str(value).strip()
                }
            )
            for assertion in assertions
            if "action" in set(assertion.get("affected_dimensions") or [])
        )
        if not owns_evidence_pair:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} must bind interaction and recognition phrases through one required action semantic assertion"
            )
        normalized_targets.append(
            {
                "repair_id": repair_id,
                "source_span_ids": source_span_ids,
                "importance": importance,
                "relation_origin": relation_origin,
                "actor_phrase": actor_phrase,
                "object_phrase": object_phrase,
                "interaction_state": interaction_state,
                "actor_object_contact": actor_object_contact,
                "protected_dimensions": protected_dimensions,
                "allowed_repair_axes": allowed_repair_axes,
                "interaction_phrase": interaction_phrase,
                "recognition_phrase": recognition_phrase,
            }
        )

    normalized = {
        "contract_version": REQUEST_LINEAGE_V2_CONTRACT_VERSION,
        **normalized,
        "repair_targets": normalized_targets,
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    return normalized

def normalize_authorial_core(
    payload: Any,
    *,
    request_envelope: Optional[JsonDict] = None,
    creative_control_snapshot: Optional[JsonDict] = None,
) -> JsonDict:
    """Validate an agent-authored concept core frozen before candidate retrieval.

    This contract is deliberately domain-neutral.  The deterministic generator
    validates and preserves the agent's work; it does not invent a replacement
    concept from taxonomy entries or candidate-pack output.
    """

    if not isinstance(payload, dict):
        raise ValueError("--authorial-core-json must contain one JSON object")
    visual_envelope = request_envelope
    if creative_control_snapshot is not None:
        creative_controls.validate(creative_control_snapshot, payload.get("source_request"))
        if payload.get("creative_controls_sha256") != creative_control_snapshot["canonical_sha256"]:
            raise ValueError("authorial core must bind the supplied creative-control snapshot")
    if request_envelope is not None:
        visual_spans, _ = creative_controls.split_request_spans(
            request_envelope, creative_control_snapshot
        )
        visual_envelope = {**request_envelope, "active_spans": visual_spans}
    core_version = str(payload.get("contract_version") or "")
    if core_version != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        raise ValueError(
            f"authorial core contract_version must be {AUTHORIAL_CORE_V3_CONTRACT_VERSION}"
        )
    allowed_fields = {
        "contract_version",
        "provenance",
        "source_request",
        "interpreted_intent",
        "subject",
        "setting",
        "event",
        "visual_priorities",
        "baseline_prompt_en",
        "user_definitions",
        "interpretation_provenance",
        "unresolved_ambiguities",
        "user_exclusions",
        "style",
        "variation_key",
    }
    allowed_fields.update({"intent_lock", "runtime_forbidden_labels"})
    allowed_fields.update({"semantic_assertions", "request_lineage", "creative_controls_sha256"})
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core contains pack-derived or unsupported fields: "
            + ", ".join(unknown_fields)
        )
    for required_field in ("interpretation_provenance", "unresolved_ambiguities"):
        if required_field not in payload:
            raise ValueError(
                f"authorial core requires {required_field}; resolve meaning before freezing the baseline"
            )
    source_request = str(payload.get("source_request") or "")
    normalized: JsonDict = {
        "contract_version": "photo-authorial-core/v3",
        "provenance": str(payload.get("provenance") or ""),
        "source_request": source_request,
        "interpreted_intent": clean_spaces(str(payload.get("interpreted_intent") or "")),
        "subject": clean_spaces(str(payload.get("subject") or "")),
        "setting": clean_spaces(str(payload.get("setting") or "")),
        "event": clean_spaces(str(payload.get("event") or "")),
        "visual_priorities": [
            clean_spaces(str(item))
            for item in normalize_list(payload.get("visual_priorities"))
            if clean_spaces(str(item))
        ],
        "baseline_prompt_en": clean_spaces(str(payload.get("baseline_prompt_en") or "")),
        "user_definitions": [],
        "interpretation_provenance": [],
        "unresolved_ambiguities": [],
        "user_exclusions": [
            clean_spaces(str(item))
            for item in normalize_list(payload.get("user_exclusions"))
            if clean_spaces(str(item))
        ],
        "style": None,
        "variation_key": str(payload.get("variation_key") or "").strip(),
    }
    if request_envelope is None:
        raise ValueError("photo-authorial-core/v3 requires --request-envelope-json")
    if source_request != str(request_envelope.get("request_text") or ""):
        raise ValueError(
            "authorial core source_request must exactly match request envelope request_text bytes"
        )
    normalized["request_binding"] = {
        "contract_version": REQUEST_BINDING_CONTRACT_VERSION,
        "request_id": str(request_envelope.get("request_id") or ""),
        "request_sha256": str(request_envelope.get("request_sha256") or ""),
        "request_envelope_sha256": str(request_envelope.get("canonical_sha256") or ""),
        "active_spans": copy.deepcopy(request_envelope.get("active_spans") or []),
    }
    runtime_forbidden_labels = [
        str(item).strip()
        for item in normalize_list(payload.get("runtime_forbidden_labels"))
        if str(item).strip()
    ]
    if len(runtime_forbidden_labels) > 12 or len(
        {item.casefold() for item in runtime_forbidden_labels}
    ) != len(runtime_forbidden_labels):
        raise ValueError(
            "authorial core runtime_forbidden_labels must contain at most twelve distinct phrases"
        )
    for label in runtime_forbidden_labels:
        if not request_scope_contains(request_envelope, label):
            raise ValueError(
                "authorial core runtime_forbidden_labels must be grounded in an active requesting-user span"
            )
    normalized["runtime_forbidden_labels"] = runtime_forbidden_labels
    if normalized["provenance"] != "agent_prepack":
        raise ValueError("authorial core provenance must be 'agent_prepack'")
    if "creative_controls_sha256" in payload:
        if re.fullmatch("[0-9a-f]{64}", str(payload["creative_controls_sha256"])) is None:
            raise ValueError("creative_controls_sha256 must bind the resolved pre-core snapshot")
        normalized["creative_controls_sha256"] = payload["creative_controls_sha256"]
    if not normalized["source_request"]:
        raise ValueError("authorial core source_request must be non-empty")
    minimum_words = {"interpreted_intent": 4, "subject": 2, "setting": 3, "event": 3}
    for field, minimum in minimum_words.items():
        if len(authorial_request_content_words(normalized[field])) < minimum:
            raise ValueError(
                f"authorial core {field} needs at least {minimum} concrete content words"
            )
    priorities = normalized["visual_priorities"]
    if not 2 <= len(priorities) <= 6:
        raise ValueError("authorial core visual_priorities must contain two to six phrases")
    if len({item.lower() for item in priorities}) != len(priorities):
        raise ValueError("authorial core visual_priorities must be distinct")
    for phrase in priorities:
        if len(authorial_request_content_words(phrase)) < 2:
            raise ValueError(
                "each authorial core visual priority needs at least two concrete content words"
            )
    baseline_words = re.findall(
        "[A-Za-z0-9]+(?:['’\\-][A-Za-z0-9]+)*", normalized["baseline_prompt_en"]
    )
    if not AUTHORIAL_PROMPT_MIN_WORDS <= len(baseline_words) <= AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS:
        raise ValueError(
            f"authorial core baseline_prompt_en must contain {AUTHORIAL_PROMPT_MIN_WORDS} "
            f"to {AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS} English words; "
            f"{AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS} is the recommended maximum"
        )
    blanket_negative_directives = find_blanket_negative_directives(normalized["baseline_prompt_en"])
    if blanket_negative_directives:
        raise ValueError(
            "authorial core baseline_prompt_en contains blanket negative directives; keep semantic exclusions in request-grounded user_exclusions, keep platform policy outside prompt prose, and express local boundaries as positive geometry or visible state: "
            + " | ".join(blanket_negative_directives)
        )
    assert request_envelope is not None
    normalized["intent_lock"] = normalize_intent_lock(
        payload.get("intent_lock"),
        envelope=visual_envelope,
        baseline_prompt_en=normalized["baseline_prompt_en"],
        allowed_dimensions=AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS,
        minimum_open_dimensions=0,
    )
    leaked_runtime_labels = [
        label
        for label in normalized.get("runtime_forbidden_labels") or []
        if str(label).casefold() in normalized["baseline_prompt_en"].casefold()
    ]
    if leaked_runtime_labels:
        raise ValueError(
            "authorial core baseline_prompt_en contains runtime-only labels: "
            + ", ".join(leaked_runtime_labels)
        )
    if "semantic_assertions" not in payload:
        raise ValueError("photo-authorial-core/v3 requires an explicit semantic_assertions list")
    normalized["semantic_assertions"] = normalize_semantic_assertions(
        payload.get("semantic_assertions"),
        envelope=visual_envelope,
        intent_lock=normalized["intent_lock"],
        baseline_prompt_en=normalized["baseline_prompt_en"],
    )
    photo_camera_evidence.camera_authoring_declaration(normalized)
    authored_subject_category(normalized["semantic_assertions"],
        (creative_control_snapshot or {}).get("context"))
    normalized["request_lineage"] = normalize_request_lineage(
        payload.get("request_lineage"),
        current_request_id=str(normalized.get("request_binding", {}).get("request_id") or ""),
        envelope=request_envelope,
        intent_lock=normalized["intent_lock"],
        baseline_prompt_en=normalized["baseline_prompt_en"],
        semantic_assertions=normalized["semantic_assertions"],
    )
    raw_definitions = payload.get("user_definitions", [])
    if raw_definitions is None:
        raw_definitions = []
    if not isinstance(raw_definitions, list) or len(raw_definitions) > 8:
        raise ValueError("authorial core user_definitions must be a list of at most eight items")
    seen_terms: Set[str] = set()
    source_request_lower = normalized["source_request"].lower()
    for index, item in enumerate(raw_definitions):
        if not isinstance(item, dict):
            raise ValueError(f"authorial core user definition {index} must be an object")
        allowed_definition_fields = {
            "term",
            "source_text",
            "interpreted_meaning",
            "prompt_evidence",
        }
        item_unknown = sorted(set(item) - allowed_definition_fields)
        if item_unknown:
            raise ValueError(
                f"authorial core user definition {index} contains unsupported fields: "
                + ", ".join(item_unknown)
            )
        term = clean_spaces(str(item.get("term") or ""))
        source_text = clean_spaces(str(item.get("source_text") or ""))
        meaning = clean_spaces(str(item.get("interpreted_meaning") or ""))
        prompt_evidence = clean_spaces(str(item.get("prompt_evidence") or ""))
        if not term or not source_text:
            raise ValueError(
                f"authorial core user definition {index} requires term and source_text"
            )
        if term.lower() in seen_terms:
            raise ValueError(f"authorial core repeats user definition term {term!r}")
        seen_terms.add(term.lower())
        if source_text.lower() not in source_request_lower:
            raise ValueError(
                f"authorial core user definition {index} source_text is not grounded in source_request"
            )
        if request_envelope is not None and source_text.casefold() not in {
            text.casefold() for text in request_envelope_active_texts(visual_envelope)
        }:
            raise ValueError(
                f"authorial core user definition {index} source_text must equal one complete active requesting-user span"
            )
        if source_text.casefold() == term.casefold():
            raise ValueError(
                f"authorial core user definition {index} cannot infer a requesting-user definition from a bare term; use interpretation_provenance instead"
            )
        if len(authorial_request_content_words(meaning)) < 4:
            raise ValueError(
                f"authorial core user definition {index} interpreted_meaning needs at least four content words"
            )
        if len(authorial_request_content_words(prompt_evidence)) < 4:
            raise ValueError(
                f"authorial core user definition {index} prompt_evidence needs at least four content words"
            )
        if prompt_evidence.lower() not in normalized["baseline_prompt_en"].lower():
            raise ValueError(
                f"authorial core user definition {index} prompt_evidence must occur in baseline_prompt_en"
            )
        normalized["user_definitions"].append(
            {
                "term": term,
                "source_text": source_text,
                "interpreted_meaning": meaning,
                "prompt_evidence": prompt_evidence,
            }
        )
    raw_interpretations = payload.get("interpretation_provenance")
    if not isinstance(raw_interpretations, list) or len(raw_interpretations) > 8:
        raise ValueError(
            "authorial core interpretation_provenance must be a list of at most eight items"
        )
    allowed_interpretation_bases = {
        "agent_general_knowledge",
        "request_context",
        "public_web_research",
    }
    seen_interpretation_terms: Set[str] = set()
    for index, item in enumerate(raw_interpretations):
        if not isinstance(item, dict):
            raise ValueError(f"authorial core interpretation provenance {index} must be an object")
        allowed_interpretation_fields = {"term", "source_text", "basis", "resolution", "sources"}
        item_unknown = sorted(set(item) - allowed_interpretation_fields)
        if item_unknown:
            raise ValueError(
                f"authorial core interpretation provenance {index} contains unsupported fields: "
                + ", ".join(item_unknown)
            )
        term = clean_spaces(str(item.get("term") or ""))
        source_text = clean_spaces(str(item.get("source_text") or ""))
        basis = str(item.get("basis") or "").strip()
        resolution = clean_spaces(str(item.get("resolution") or ""))
        raw_sources = item.get("sources", [])
        if not term or not source_text:
            raise ValueError(
                f"authorial core interpretation provenance {index} requires term and source_text"
            )
        if term.lower() in seen_interpretation_terms:
            raise ValueError(f"authorial core repeats interpreted term {term!r}")
        if term.lower() in seen_terms:
            raise ValueError(
                f"authorial core term {term!r} cannot be both a requesting-user definition and an agent interpretation"
            )
        seen_interpretation_terms.add(term.lower())
        if source_text.lower() not in source_request_lower:
            raise ValueError(
                f"authorial core interpretation provenance {index} source_text is not grounded in source_request"
            )
        if request_envelope is not None and (
            not request_scope_contains(visual_envelope, source_text)
        ):
            raise ValueError(
                f"authorial core interpretation provenance {index} source_text is not grounded in an active requesting-user span"
            )
        if basis not in allowed_interpretation_bases:
            raise ValueError(
                f"authorial core interpretation provenance {index} basis must be one of {sorted(allowed_interpretation_bases)}"
            )
        if len(authorial_request_content_words(resolution)) < 4:
            raise ValueError(
                f"authorial core interpretation provenance {index} resolution needs at least four content words"
            )
        if not isinstance(raw_sources, list) or len(raw_sources) > 4:
            raise ValueError(
                f"authorial core interpretation provenance {index} sources must be a list of at most four URLs"
            )
        sources = [clean_spaces(str(value)) for value in raw_sources]
        if any((not value for value in sources)) or len(set(sources)) != len(sources):
            raise ValueError(
                f"authorial core interpretation provenance {index} sources must be non-empty and distinct"
            )
        if basis == "public_web_research":
            if not sources or any(
                (
                    re.fullmatch("https?://[^\\s]+", value, flags=re.IGNORECASE) is None
                    for value in sources
                )
            ):
                raise ValueError(
                    f"authorial core interpretation provenance {index} public web research requires at least one HTTP(S) source"
                )
        elif sources:
            raise ValueError(
                f"authorial core interpretation provenance {index} sources are allowed only for public_web_research"
            )
        normalized["interpretation_provenance"].append(
            {
                "term": term,
                "source_text": source_text,
                "basis": basis,
                "resolution": resolution,
                "sources": sources,
            }
        )
    assert request_envelope is not None
    semantic_source_texts = [
        str(item.get("source_text") or "")
        for item in [*normalized["user_definitions"], *normalized["interpretation_provenance"]]
        if isinstance(item, dict) and str(item.get("source_text") or "")
    ]
    uncovered_interpretation_spans = [
        str(span.get("span_id") or "")
        for span in visual_envelope.get("active_spans") or []
        if isinstance(span, dict)
        and (
            not any(
                (
                    source.casefold() in str(span.get("text") or "").casefold()
                    for source in semantic_source_texts
                )
            )
        )
    ]
    if uncovered_interpretation_spans:
        raise ValueError(
            "photo-authorial-core/v3 requires requesting-user definition or interpretation provenance coverage for every active span: "
            + ", ".join(uncovered_interpretation_spans)
        )
    raw_unresolved = payload.get("unresolved_ambiguities")
    if not isinstance(raw_unresolved, list):
        raise ValueError("authorial core unresolved_ambiguities must be a list")
    unresolved = [clean_spaces(str(item)) for item in raw_unresolved if clean_spaces(str(item))]
    if unresolved:
        raise ValueError(
            "authorial core cannot be frozen with unresolved ambiguities; ask the requester or research the public meaning first: "
            + "; ".join(unresolved)
        )
    exclusions = normalized["user_exclusions"]
    if len(exclusions) > 12:
        raise ValueError("authorial core user_exclusions must contain at most twelve phrases")
    if len({item.lower() for item in exclusions}) != len(exclusions):
        raise ValueError("authorial core user_exclusions must be distinct")
    assert request_envelope is not None
    ungrounded_exclusions = [
        item for item in exclusions if not request_scope_contains(request_envelope, item)
    ]
    if ungrounded_exclusions:
        raise ValueError(
            "photo-authorial-core/v3 user_exclusions must be grounded in active requesting-user spans: "
            + ", ".join(ungrounded_exclusions)
        )
    runtime_label_keys = {
        str(item).casefold() for item in normalized.get("runtime_forbidden_labels") or []
    }
    overlap = [item for item in exclusions if item.casefold() in runtime_label_keys]
    if overlap:
        raise ValueError(
            "a runtime-only label cannot also be a semantic user exclusion: " + ", ".join(overlap)
        )
    leaked_exclusions = [
        item for item in exclusions if item.lower() in normalized["baseline_prompt_en"].lower()
    ]
    if leaked_exclusions:
        raise ValueError(
            "authorial core baseline_prompt_en contains excluded phrases: "
            + ", ".join(leaked_exclusions)
        )
    raw_style = payload.get("style")
    if raw_style is not None:
        if not isinstance(raw_style, dict):
            raise ValueError("authorial core style must be an object or null")
        unknown_style_fields = sorted(set(raw_style) - {"domain", "family", "evidence"})
        if unknown_style_fields:
            raise ValueError(
                "authorial core style contains unsupported fields: "
                + ", ".join(unknown_style_fields)
            )
        domain = clean_spaces(str(raw_style.get("domain") or ""))
        family = clean_spaces(str(raw_style.get("family") or ""))
        evidence = [
            clean_spaces(str(item))
            for item in normalize_list(raw_style.get("evidence"))
            if clean_spaces(str(item))
        ]
        if not domain or not family or len(evidence) < 2:
            raise ValueError(
                "authorial core style requires domain, family, and at least two evidence phrases"
            )
        if len({item.lower() for item in evidence}) != len(evidence):
            raise ValueError("authorial core style evidence phrases must be distinct")
        normalized["style"] = {"domain": domain, "family": family, "evidence": evidence}
    canonical_bytes = json.dumps(
        normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    normalized["canonical_sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
    normalized["core_id"] = normalized["canonical_sha256"][:16]
    return normalized
