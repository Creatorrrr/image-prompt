#!/usr/bin/env python3
"""Validate analyst-supplied lighting axes and review external friendly labels.

The tool does not inspect images, infer a physical rig, invent a friendly label,
or emit production prompt prose. It may compose one explanation-only summary from
literal axis tokens declared by the selected versioned policy.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_CANDIDATE_SOURCES = {"user-supplied", "versioned-vocabulary"}
VALID_LABEL_SCOPES = {
    "key-character",
    "edge-character",
    "modeling-character",
    "composite-lighting",
}
REQUIRED_SCOPE_AXES = {
    "key-character": {"displayed_key_level"},
    "edge-character": {"edge_softness"},
    "modeling-character": {"local_form_contrast"},
    "composite-lighting": {
        "displayed_key_level",
        "edge_softness",
        "local_form_contrast",
    },
}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValueError(f"{label} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise ValueError(f"{label} must contain at least one string")
    return [item.strip() for item in value]


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    return value


def _load(path: Path, label: str) -> dict[str, Any]:
    return _object(json.loads(path.read_text(encoding="utf-8")), label)


def _policy_axes(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_axes = _object(policy.get("axes"), "policy.axes")
    if not raw_axes:
        raise ValueError("policy.axes must not be empty")
    axes: dict[str, dict[str, Any]] = {}
    for axis, raw_spec in raw_axes.items():
        if not isinstance(axis, str) or not axis:
            raise ValueError("policy.axes keys must be non-empty strings")
        spec = _object(raw_spec, f"policy.axes.{axis}")
        terms = _string_list(spec.get("terms"), f"policy.axes.{axis}.terms")
        if len(terms) != len(set(terms)):
            raise ValueError(f"policy.axes.{axis}.terms contains duplicates")
        summary_tokens = spec.get("summary_tokens", {})
        summary_tokens = _object(summary_tokens, f"policy.axes.{axis}.summary_tokens")
        unknown_tokens = sorted(set(summary_tokens) - set(terms))
        if unknown_tokens:
            raise ValueError(
                f"policy.axes.{axis}.summary_tokens contains unknown terms: "
                + ", ".join(unknown_tokens)
            )
        for term, token in summary_tokens.items():
            _string(token, f"policy.axes.{axis}.summary_tokens.{term}")
        axes[axis] = {"terms": terms, "summary_tokens": summary_tokens}
    return axes


def _compose_summary(
    classifications: dict[str, dict[str, Any]], policy: dict[str, Any]
) -> dict[str, Any]:
    summary = _object(policy.get("controlled_summary"), "policy.controlled_summary")
    order = _string_list(summary.get("axis_order"), "policy.controlled_summary.axis_order")
    minimum_confidence = _string(
        summary.get("minimum_confidence"),
        "policy.controlled_summary.minimum_confidence",
    )
    if minimum_confidence not in VALID_CONFIDENCE:
        raise ValueError("policy.controlled_summary.minimum_confidence is invalid")
    minimum_axis_count = _integer(
        summary.get("minimum_axis_count"),
        "policy.controlled_summary.minimum_axis_count",
    )
    if minimum_axis_count < 2 or minimum_axis_count > len(order):
        raise ValueError(
            "policy.controlled_summary.minimum_axis_count must be between 2 and axis_order length"
        )
    suffix = _string(summary.get("suffix"), "policy.controlled_summary.suffix")
    axes = _policy_axes(policy)
    unknown = sorted(set(order) - set(axes))
    if unknown:
        raise ValueError(
            "policy.controlled_summary.axis_order contains unknown axes: "
            + ", ".join(unknown)
        )
    tokens: list[str] = []
    decomposed_axes: list[str] = []
    unresolved_axes: list[str] = []
    for axis in order:
        spec = classifications[axis]
        term = spec["term"]
        confidence = spec["confidence"]
        token = axes[axis]["summary_tokens"].get(term)
        if (
            term in {"mixed", "uncertain"}
            or CONFIDENCE_RANK[confidence] < CONFIDENCE_RANK[minimum_confidence]
            or not token
        ):
            unresolved_axes.append(axis)
            continue
        tokens.append(str(token))
        decomposed_axes.append(axis)
    if len(tokens) < minimum_axis_count:
        return {
            "phrase": None,
            "status": "inconclusive",
            "emit": False,
            "decomposed_axes": decomposed_axes,
            "unresolved_axes": unresolved_axes,
        }
    return {
        "phrase": " ".join([*tokens, suffix]),
        "status": "explanation-only",
        "emit": False,
        "decomposed_axes": decomposed_axes,
        "unresolved_axes": unresolved_axes,
    }


def classify_observation(
    observation: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    scope = _string(observation.get("observation_scope"), "observation_scope")
    if scope != policy.get("observation_scope"):
        raise ValueError("observation_scope must match the selected language policy")
    region_id = _string(observation.get("region_id"), "region_id")
    source_evidence = _string_list(observation.get("source_evidence"), "source_evidence")
    axes = _policy_axes(policy)
    raw_classifications = _object(
        observation.get("axis_classification"), "axis_classification"
    )
    unknown_axes = sorted(set(raw_classifications) - set(axes))
    missing_axes = sorted(set(axes) - set(raw_classifications))
    if unknown_axes:
        raise ValueError(
            "axis_classification contains unknown axes: " + ", ".join(unknown_axes)
        )
    if missing_axes:
        raise ValueError(
            "axis_classification is missing axes: " + ", ".join(missing_axes)
        )
    classifications: dict[str, dict[str, Any]] = {}
    for axis, policy_spec in axes.items():
        spec = _object(raw_classifications.get(axis), f"axis_classification.{axis}")
        term = _string(spec.get("term"), f"axis_classification.{axis}.term")
        if term not in policy_spec["terms"]:
            raise ValueError(f"axis_classification.{axis}.term is invalid")
        confidence = _string(
            spec.get("confidence"), f"axis_classification.{axis}.confidence"
        )
        if confidence not in VALID_CONFIDENCE:
            raise ValueError(f"axis_classification.{axis}.confidence is invalid")
        evidence = _string_list(
            spec.get("source_evidence", []),
            f"axis_classification.{axis}.source_evidence",
            allow_empty=True,
        )
        if term not in {"mixed", "uncertain"} and not evidence:
            raise ValueError(
                f"axis_classification.{axis}.source_evidence is required for a resolved term"
            )
        classifications[axis] = {
            "term": term,
            "confidence": confidence,
            "source_evidence": evidence,
        }
    return {
        "policy_id": _string(policy.get("id"), "policy.id"),
        "policy_status": _string(policy.get("status"), "policy.status"),
        "observation_scope": scope,
        "region_id": region_id,
        "source_evidence": source_evidence,
        "axis_classification": classifications,
        "controlled_summary": _compose_summary(classifications, policy),
    }


def review_candidates(
    classification: dict[str, Any],
    candidate_payload: dict[str, Any],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    raw_source = _object(candidate_payload.get("candidate_source"), "candidate_source")
    source_kind = _string(raw_source.get("kind"), "candidate_source.kind")
    if source_kind not in VALID_CANDIDATE_SOURCES:
        raise ValueError("candidate_source.kind is invalid")
    candidate_source = {
        "kind": source_kind,
        "reference": _string(raw_source.get("reference"), "candidate_source.reference"),
    }
    raw_candidates = candidate_payload.get("candidates")
    if not isinstance(raw_candidates, list):
        raise ValueError("candidates must be a list")
    axes = classification["axis_classification"]
    policy_axes = _policy_axes(policy)
    classified_axes = set(axes)
    reports: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_candidates):
        candidate = _object(raw, f"candidates[{index}]")
        phrase = _string(candidate.get("phrase"), f"candidates[{index}].phrase")
        scope = _string(candidate.get("label_scope"), f"candidates[{index}].label_scope")
        if scope not in VALID_LABEL_SCOPES:
            raise ValueError(f"candidates[{index}].label_scope is invalid")
        requirements = _object(
            candidate.get("axis_requirements"),
            f"candidates[{index}].axis_requirements",
        )
        unknown_axes = sorted(set(requirements) - classified_axes)
        if unknown_axes:
            raise ValueError(
                f"candidates[{index}] contains unknown axes: " + ", ".join(unknown_axes)
            )
        missing_axes = REQUIRED_SCOPE_AXES[scope] - set(requirements)
        if missing_axes:
            raise ValueError(
                f"candidates[{index}] does not support its label scope: "
                + ", ".join(sorted(missing_axes))
            )
        matched: list[str] = []
        conflicting: list[str] = []
        unresolved: list[str] = []
        for axis, allowed in requirements.items():
            if not isinstance(allowed, list) or not allowed or not all(
                isinstance(item, str) and item in policy_axes[axis]["terms"]
                for item in allowed
            ):
                raise ValueError(
                    f"candidates[{index}].axis_requirements.{axis} contains invalid policy terms"
                )
            term = axes[axis]["term"]
            confidence = axes[axis]["confidence"]
            if term in {"mixed", "uncertain"} or confidence == "low":
                unresolved.append(axis)
            elif term in allowed:
                matched.append(axis)
            else:
                conflicting.append(axis)
        status = (
            "conflicting"
            if conflicting
            else "inconclusive"
            if unresolved
            else "compatible"
        )
        reports.append(
            {
                "phrase": phrase,
                "candidate_source": candidate_source,
                "label_scope": scope,
                "review_status": status,
                "matched_axes": matched,
                "conflicting_axes": conflicting,
                "unresolved_axes": unresolved,
                "axis_requirements": requirements,
            }
        )
    return reports


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", help="analyst-authored lighting-axis JSON")
    parser.add_argument("--policy", required=True, help="versioned lighting-language policy JSON")
    parser.add_argument(
        "--candidates",
        default="",
        help="optional externally supplied friendly-label candidates JSON",
    )
    args = parser.parse_args(argv)
    try:
        observation = _load(Path(args.observation), "observation")
        policy = _load(Path(args.policy), "policy")
        classification = classify_observation(observation, policy)
        payload: dict[str, Any] = {
            "status": "ok",
            **classification,
            "limitations": [
                "source-visible lighting language only",
                "no image or semantic region detection",
                "no physical-light or lamp-power inference",
                "controlled summary is explanation-only",
                "no friendly-label candidate invention",
                "no automatic friendly-label selection",
                "no automatic production prompt wording",
            ],
        }
        if args.candidates:
            payload["friendly_label_review"] = review_candidates(
                classification,
                _load(Path(args.candidates), "candidate payload"),
                policy,
            )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
