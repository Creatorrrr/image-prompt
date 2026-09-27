#!/usr/bin/env python3
"""Validate the neutral pre-core catalog and an arm-specific feature-selection record."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


CATALOG_VERSION = "photo-precore-feature-catalog/v1"
SELECTION_VERSION = "photo-precore-feature-selection/v1"
CATALOG_PATH = "skills/photo-prompt-image-generator/precore/visual_feature_catalog.json"
CANONICAL_CATALOG_FILE = (
    Path(__file__).resolve().parents[1] / "precore" / "visual_feature_catalog.json"
)
GROUPS = {
    "meaning_and_event",
    "subject_and_embodiment",
    "place_and_traces",
    "delivery_and_technique",
}
CATEGORY_ID = re.compile(r"feature\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class SelectionValidationError(ValueError):
    """A catalog or selection artifact does not satisfy the pre-core contract."""


def _fail(message: str) -> None:
    raise SelectionValidationError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"{label} must be an object")
    return value


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be nonempty text")
    return value


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        _fail(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        _fail(f"{label} must contain nonempty text")
    if len(value) != len(set(value)):
        _fail(f"{label} must not contain duplicates")
    return value


def _only_fields(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = set(value) - allowed
    if extra:
        _fail(f"{label} has unsupported fields: {', '.join(sorted(extra))}")


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256.fullmatch(value) is None:
        _fail(f"{label} must be a lowercase SHA-256 hex digest")
    return value


def clean_spaces(text: str) -> str:
    """Match the core normalizer's canonical baseline whitespace and punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text


def validate_catalog(payload: Any) -> dict[str, dict[str, Any]]:
    catalog = _object(payload, "catalog")
    _only_fields(catalog, {"schema_version", "categories"}, "catalog")
    if catalog.get("schema_version") != CATALOG_VERSION:
        _fail("catalog schema_version is unsupported")
    categories = catalog.get("categories")
    if not isinstance(categories, list):
        _fail("catalog categories must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    source_numbers: list[int] = []
    for index, raw in enumerate(categories):
        category = _object(raw, f"category {index}")
        _only_fields(
            category,
            {
                "id",
                "source_number",
                "origin",
                "added_reason",
                "group",
                "name_ko",
                "name_en",
                "source_examples",
                "added_examples",
            },
            f"category {index}",
        )
        category_id = _nonempty(category.get("id"), f"category {index} id")
        if CATEGORY_ID.fullmatch(category_id) is None or category_id in by_id:
            _fail(f"category {index} has an invalid or duplicate ID")
        by_id[category_id] = category
        if category.get("group") not in GROUPS:
            _fail(f"{category_id} has an invalid group")
        _nonempty(category.get("name_ko"), f"{category_id} name_ko")
        _nonempty(category.get("name_en"), f"{category_id} name_en")
        source_examples = _string_list(
            category.get("source_examples"),
            f"{category_id} source_examples",
            allow_empty=True,
        )
        added_examples = _string_list(
            category.get("added_examples"),
            f"{category_id} added_examples",
            allow_empty=True,
        )
        if set(source_examples) & set(added_examples):
            _fail(f"{category_id} repeats a source example as an addition")
        source_number = category.get("source_number")
        if type(source_number) is int:
            source_numbers.append(source_number)
            if not source_examples or "origin" in category or "added_reason" in category:
                _fail(f"{category_id} must keep source examples and source provenance")
        elif source_number is None:
            if source_examples or category.get("origin") != "added" or not added_examples:
                _fail(f"{category_id} has invalid added-category provenance")
            _nonempty(category.get("added_reason"), f"{category_id} added_reason")
        else:
            _fail(f"{category_id} source_number must be an integer or null")

    if sorted(source_numbers) != list(range(1, 46)):
        _fail("catalog must preserve source categories numbered 1 through 45")
    return by_id


def _active_spans(envelope: dict[str, Any]) -> tuple[str, dict[str, str]]:
    request = _nonempty(envelope.get("request_text"), "envelope request_text")
    digest = hashlib.sha256(request.encode("utf-8")).hexdigest()
    if _sha(envelope.get("request_sha256"), "envelope request_sha256") != digest:
        _fail("envelope request_sha256 does not match request_text")
    spans = envelope.get("active_spans")
    if not isinstance(spans, list) or not spans:
        _fail("envelope must contain active_spans")
    by_id: dict[str, str] = {}
    for index, raw in enumerate(spans):
        span = _object(raw, f"active span {index}")
        span_id = _nonempty(span.get("span_id"), f"active span {index} span_id")
        start, end, text = span.get("start"), span.get("end"), span.get("text")
        if (
            span_id in by_id
            or type(start) is not int
            or type(end) is not int
            or start < 0
            or end <= start
            or end > len(request)
            or not isinstance(text, str)
            or request[start:end] != text
        ):
            _fail(f"active span {index} does not match request_text")
        by_id[span_id] = text
    return request, by_id


def validate_selection(
    catalog: Any,
    catalog_bytes: bytes,
    selection: Any,
    envelope: Any,
    core: Any,
    embodiment_review: Any,
) -> dict[str, Any]:
    categories = validate_catalog(catalog)
    record = _object(selection, "selection")
    _only_fields(
        record,
        {
            "contract_version",
            "request_id",
            "active_span_ids",
            "catalog_path",
            "catalog_schema_version",
            "catalog_sha256",
            "request_sha256",
            "baseline_prompt_sha256",
            "selected",
        },
        "selection",
    )
    if record.get("contract_version") != SELECTION_VERSION:
        _fail("selection contract_version is unsupported")
    if record.get("catalog_path") != CATALOG_PATH:
        _fail("selection catalog_path is not the permitted pre-core catalog")
    if record.get("catalog_schema_version") != CATALOG_VERSION:
        _fail("selection catalog_schema_version is unsupported")
    catalog_digest = hashlib.sha256(catalog_bytes).hexdigest()
    if _sha(record.get("catalog_sha256"), "selection catalog_sha256") != catalog_digest:
        _fail("selection catalog_sha256 does not match catalog bytes")

    request_envelope = _object(envelope, "envelope")
    if request_envelope.get("contract_version") != "photo-request-envelope/v1":
        _fail("envelope contract_version is unsupported")
    if request_envelope.get("provenance") != "requesting_user":
        _fail("envelope provenance must be requesting_user")
    request, spans = _active_spans(request_envelope)
    request_id = _nonempty(request_envelope.get("request_id"), "envelope request_id")
    if record.get("request_id") != request_id:
        _fail("selection request_id does not match envelope")
    if record.get("request_sha256") != request_envelope["request_sha256"]:
        _fail("selection request_sha256 does not match envelope")
    active_ids = _string_list(record.get("active_span_ids"), "selection active_span_ids")
    if set(active_ids) != set(spans):
        _fail("selection active_span_ids do not match this arm's envelope")

    authorial_core = _object(core, "authorial core")
    if authorial_core.get("contract_version") != "photo-authorial-core/v3":
        _fail("authorial core contract_version is unsupported")
    if authorial_core.get("provenance") != "agent_prepack":
        _fail("authorial core provenance must be agent_prepack")
    if authorial_core.get("source_request") != request:
        _fail("authorial core source_request does not match envelope")
    baseline_raw = _nonempty(
        authorial_core.get("baseline_prompt_en"), "authorial core baseline_prompt_en"
    )
    baseline = clean_spaces(baseline_raw)
    if baseline_raw != baseline:
        _fail("authorial core baseline_prompt_en must already be canonical")
    baseline_digest = hashlib.sha256(baseline.encode("utf-8")).hexdigest()
    if (
        _sha(record.get("baseline_prompt_sha256"), "selection baseline_prompt_sha256")
        != baseline_digest
    ):
        _fail("selection baseline_prompt_sha256 does not match the core")
    review = _object(embodiment_review, "embodiment review")
    if review.get("contract_version") != "photo-embodiment-review/v1":
        _fail("embodiment review contract_version is unsupported")
    if review.get("provenance") != "agent_prepack":
        _fail("embodiment review provenance must be agent_prepack")
    if review.get("prompt_sha256") != baseline_digest:
        _fail("embodiment review prompt_sha256 does not match the core")

    selected = record.get("selected")
    if not isinstance(selected, list) or not 5 <= len(selected) <= 10:
        _fail("selection must contain five to ten categories")
    selected_ids: list[str] = []
    reasons: list[str] = []
    evidence_phrases: list[str] = []
    evidence_pairs: list[tuple[str, str]] = []
    technique_count = 0
    for index, raw in enumerate(selected):
        item = _object(raw, f"selected item {index}")
        _only_fields(
            item,
            {
                "category_id",
                "basis",
                "source_span_ids",
                "source_text",
                "derivation",
                "reason",
                "baseline_evidence",
            },
            f"selected item {index}",
        )
        category_id = _nonempty(item.get("category_id"), f"selected item {index} category_id")
        if category_id not in categories or category_id in selected_ids:
            _fail(f"selected item {index} has an unknown or duplicate category")
        selected_ids.append(category_id)
        if categories[category_id]["group"] == "delivery_and_technique":
            technique_count += 1
        basis = item.get("basis")
        source_ids = _string_list(
            item.get("source_span_ids"),
            f"selected item {index} source_span_ids",
            allow_empty=True,
        )
        if any(span_id not in spans for span_id in source_ids):
            _fail(f"selected item {index} cites an inactive request span")
        source_text = item.get("source_text")
        derivation = item.get("derivation")
        if basis == "explicit_request":
            if (
                not source_ids
                or not isinstance(source_text, str)
                or not source_text.strip()
                or not any(source_text in spans[span_id] for span_id in source_ids)
                or derivation is not None
            ):
                _fail(f"selected item {index} lacks exact requester evidence")
        elif basis == "request_derived":
            if not source_ids or source_text is not None:
                _fail(f"selected item {index} lacks request-derived provenance")
            _nonempty(derivation, f"selected item {index} derivation")
        elif basis == "agent_visual_choice":
            if source_ids or source_text is not None or derivation is not None:
                _fail(f"selected item {index} must not claim requester provenance")
        else:
            _fail(f"selected item {index} has an unsupported basis")
        reason = _nonempty(item.get("reason"), f"selected item {index} reason")
        evidence = _nonempty(
            item.get("baseline_evidence"), f"selected item {index} baseline_evidence"
        )
        if evidence not in baseline:
            _fail(f"selected item {index} evidence is absent from baseline_prompt_en")
        normalized_reason = clean_spaces(reason).casefold()
        normalized_evidence = clean_spaces(evidence).casefold()
        reasons.append(normalized_reason)
        evidence_phrases.append(normalized_evidence)
        evidence_pairs.append((normalized_reason, normalized_evidence))

    warnings: list[str] = []
    if len(set(reasons)) != len(reasons):
        warnings.append("repeated_reason")
    if len(set(evidence_phrases)) != len(evidence_phrases):
        warnings.append("repeated_evidence")
    if len(set(evidence_pairs)) != len(evidence_pairs):
        warnings.append("repeated_reason_and_evidence")
    if technique_count > len(selected) / 2:
        warnings.append("technique_categories_are_majority")
    return {
        "valid": True,
        "contract_version": SELECTION_VERSION,
        "request_id": request_id,
        "selected_category_ids": selected_ids,
        "selected_count": len(selected_ids),
        "warnings": warnings,
    }


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(f"could not read {path.name}: {type(exc).__name__}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CANONICAL_CATALOG_FILE)
    parser.add_argument(
        "--historical-catalog",
        action="store_true",
        help="allow an archived catalog snapshot for historical verification only",
    )
    parser.add_argument("--request-envelope", type=Path, required=True)
    parser.add_argument("--authorial-core", type=Path, required=True)
    parser.add_argument("--embodiment-review", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        catalog_bytes = args.catalog.read_bytes()
        if not args.historical_catalog and catalog_bytes != CANONICAL_CATALOG_FILE.read_bytes():
            _fail("catalog bytes differ from the current permitted pre-core catalog")
        result = validate_selection(
            json.loads(catalog_bytes),
            catalog_bytes,
            _read_json(args.selection),
            _read_json(args.request_envelope),
            _read_json(args.authorial_core),
            _read_json(args.embodiment_review),
        )
    except (OSError, UnicodeError, json.JSONDecodeError, SelectionValidationError) as exc:
        print(f"invalid pre-core feature selection: {exc}", file=sys.stderr)
        return 2
    result["catalog_mode"] = "historical" if args.historical_catalog else "current"
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
