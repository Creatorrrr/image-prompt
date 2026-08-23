#!/usr/bin/env python3
"""Classify source-visible color axes and compose controlled axis language.

The tool does not detect semantic regions, infer biological or material true color,
or invent or choose a friendly label.  An analyst may request a deterministic
natural-language composition of the classified axes for a named visible surface;
the calling plan still decides whether that phrase is emitted.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any


VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_FINISH = {"matte", "satin", "luminous", "dewy", "uncertain"}
VALID_EVENNESS = {"even", "naturally-varied", "freckled", "uncertain"}
VALID_LABEL_SCOPES = {
    "value-depth",
    "undertone",
    "surface-finish",
    "composite-appearance",
}
VALID_CANDIDATE_SOURCES = {"user-supplied", "versioned-vocabulary"}
CLASSIFIED_AXES = {"value_depth", "chroma", "undertone", "finish", "evenness"}
REQUIRED_SCOPE_AXES = {
    "value-depth": {"value_depth"},
    "undertone": {"undertone"},
    "surface-finish": {"finish"},
    "composite-appearance": {"value_depth", "chroma", "undertone"},
}
CONTROLLED_DESCRIPTOR_CORE_AXES = ("value_depth", "chroma", "undertone")
UNRESOLVED_DESCRIPTOR_TERMS = {"mixed", "uncertain"}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    return float(value)


def _load(path: Path, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _object(payload, label)


def _circular_distance(left: float, right: float) -> float:
    return abs((left - right + 180.0) % 360.0 - 180.0)


def _downgrade(confidence: str) -> str:
    return {"high": "medium", "medium": "low", "low": "low"}[confidence]


def _classify_scalar(
    value: float,
    bins: list[dict[str, Any]],
    boundary_margin: float,
    dispersion: float | None,
    max_dispersion: float,
    label: str,
) -> dict[str, Any]:
    normalized: list[tuple[str, float, float]] = []
    for index, item in enumerate(bins):
        spec = _object(item, f"{label}[{index}]")
        term = _string(spec.get("term"), f"{label}[{index}].term")
        lower = _number(spec.get("min_inclusive"), f"{label}[{index}].min_inclusive")
        upper = _number(spec.get("max_exclusive"), f"{label}[{index}].max_exclusive")
        if lower >= upper:
            raise ValueError(f"{label}[{index}] must satisfy min_inclusive < max_exclusive")
        normalized.append((term, lower, upper))
    normalized.sort(key=lambda item: item[1])
    selected_index = next(
        (index for index, (_, lower, upper) in enumerate(normalized) if lower <= value < upper),
        None,
    )
    if selected_index is None:
        return {"term": "uncertain", "confidence": "low", "runner_up": None}
    term, lower, upper = normalized[selected_index]
    boundary_distance = min(value - lower, upper - value)
    confidence = "medium" if boundary_distance <= boundary_margin else "high"
    if dispersion is not None and dispersion > max_dispersion:
        confidence = "low"
    candidates: list[tuple[float, str]] = []
    if selected_index > 0:
        candidates.append((abs(value - lower), normalized[selected_index - 1][0]))
    if selected_index + 1 < len(normalized):
        candidates.append((abs(upper - value), normalized[selected_index + 1][0]))
    runner_up = min(candidates)[1] if candidates else None
    return {
        "term": term,
        "confidence": confidence,
        "runner_up": runner_up,
        "distance_to_nearest_boundary": round(boundary_distance, 3),
    }


def _classify_undertone(
    a_value: float,
    b_value: float,
    policy: dict[str, Any],
) -> dict[str, Any]:
    chroma = math.hypot(a_value, b_value)
    neutral_max = _number(policy.get("neutral_max_chroma"), "undertone.neutral_max_chroma")
    if chroma <= neutral_max:
        confidence = "high" if chroma <= neutral_max * 0.75 else "medium"
        return {
            "term": "neutral",
            "confidence": confidence,
            "runner_up": None,
            "hue_degrees": None if chroma == 0.0 else round(math.degrees(math.atan2(b_value, a_value)) % 360.0, 3),
        }
    hue = math.degrees(math.atan2(b_value, a_value)) % 360.0
    prototypes = policy.get("prototypes")
    if not isinstance(prototypes, list) or len(prototypes) < 2:
        raise ValueError("undertone.prototypes must contain at least two entries")
    distances: list[tuple[float, str]] = []
    for index, item in enumerate(prototypes):
        spec = _object(item, f"undertone.prototypes[{index}]")
        term = _string(spec.get("term"), f"undertone.prototypes[{index}].term")
        angle = _number(spec.get("hue_degrees"), f"undertone.prototypes[{index}].hue_degrees")
        distances.append((_circular_distance(hue, angle), term))
    distances.sort()
    nearest, runner_up = distances[0], distances[1]
    maximum = _number(
        policy.get("maximum_candidate_distance_degrees"),
        "undertone.maximum_candidate_distance_degrees",
    )
    ambiguity = _number(
        policy.get("ambiguity_margin_degrees"),
        "undertone.ambiguity_margin_degrees",
    )
    if nearest[0] > maximum:
        term, confidence = "mixed", "low"
    elif runner_up[0] - nearest[0] <= ambiguity:
        term, confidence = "mixed", "low"
    else:
        term = nearest[1]
        confidence = "high" if nearest[0] <= maximum / 2.0 else "medium"
    return {
        "term": term,
        "confidence": confidence,
        "runner_up": runner_up[1],
        "hue_degrees": round(hue, 3),
        "nearest_distance_degrees": round(nearest[0], 3),
    }


def _surface_axis(
    surface: dict[str, Any], axis: str, allowed: set[str]
) -> dict[str, Any]:
    raw = surface.get(axis)
    if raw is None:
        return {
            "term": "uncertain",
            "confidence": "low",
            "source": "not-observed",
            "source_evidence": [],
        }
    spec = _object(raw, f"surface_evidence.{axis}")
    term = _string(spec.get("term"), f"surface_evidence.{axis}.term")
    if term not in allowed:
        raise ValueError(f"surface_evidence.{axis}.term is invalid")
    confidence = _string(spec.get("confidence"), f"surface_evidence.{axis}.confidence")
    if confidence not in VALID_CONFIDENCE:
        raise ValueError(f"surface_evidence.{axis}.confidence is invalid")
    evidence = spec.get("source_evidence")
    if not isinstance(evidence, list) or not all(isinstance(item, str) and item.strip() for item in evidence):
        raise ValueError(f"surface_evidence.{axis}.source_evidence must contain strings")
    return {
        "term": term,
        "confidence": confidence,
        "source": "analyst-observed",
        "source_evidence": evidence,
    }


def classify_observation(
    observation: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    scope = _string(observation.get("observation_scope"), "observation_scope")
    if scope != policy.get("observation_scope"):
        raise ValueError("observation_scope must match the selected language policy")
    profile_status = _string(observation.get("profile_status"), "profile_status")
    region_id = _string(observation.get("region_id"), "region_id")
    lab = observation.get("lab_d65")
    if not isinstance(lab, list) or len(lab) != 3:
        raise ValueError("lab_d65 must contain three numeric values")
    lightness, a_value, b_value = (
        _number(value, f"lab_d65[{index}]") for index, value in enumerate(lab)
    )
    chroma = math.hypot(a_value, b_value)
    dispersion = observation.get("dispersion", {})
    dispersion = _object(dispersion, "dispersion")
    lightness_range = dispersion.get("lightness_range")
    chroma_range = dispersion.get("chroma_range")
    lightness_range = _number(lightness_range, "dispersion.lightness_range") if lightness_range is not None else None
    chroma_range = _number(chroma_range, "dispersion.chroma_range") if chroma_range is not None else None
    confidence_policy = _object(policy.get("confidence"), "confidence")
    value_depth = _classify_scalar(
        lightness,
        policy.get("value_depth_bins", []),
        _number(confidence_policy.get("value_boundary_margin"), "confidence.value_boundary_margin"),
        lightness_range,
        _number(confidence_policy.get("max_lightness_dispersion"), "confidence.max_lightness_dispersion"),
        "value_depth_bins",
    )
    chroma_class = _classify_scalar(
        chroma,
        policy.get("chroma_bins", []),
        _number(confidence_policy.get("chroma_boundary_margin"), "confidence.chroma_boundary_margin"),
        chroma_range,
        _number(confidence_policy.get("max_chroma_dispersion"), "confidence.max_chroma_dispersion"),
        "chroma_bins",
    )
    undertone = _classify_undertone(a_value, b_value, _object(policy.get("undertone"), "undertone"))
    if profile_status != "embedded-profile-converted-to-srgb":
        for axis in (value_depth, chroma_class, undertone):
            axis["confidence"] = _downgrade(str(axis["confidence"]))
    surface = observation.get("surface_evidence", {})
    surface = _object(surface, "surface_evidence")
    return {
        "policy_id": _string(policy.get("id"), "policy.id"),
        "policy_status": _string(policy.get("status"), "policy.status"),
        "observation_scope": scope,
        "profile_status": profile_status,
        "region_id": region_id,
        "measurement": {
            "lab_d65": [round(lightness, 3), round(a_value, 3), round(b_value, 3)],
            "chroma": round(chroma, 3),
            "dispersion": {
                "lightness_range": lightness_range,
                "chroma_range": chroma_range,
            },
        },
        "axis_classification": {
            "value_depth": value_depth,
            "chroma": chroma_class,
            "undertone": undertone,
            "finish": _surface_axis(surface, "finish", VALID_FINISH),
            "evenness": _surface_axis(surface, "evenness", VALID_EVENNESS),
        },
    }


def _controlled_axis_excerpt(axis: str, term: str) -> str | None:
    """Serialize one controlled axis term without a preferred term lookup table."""

    if term in UNRESOLVED_DESCRIPTOR_TERMS:
        return None
    words = " ".join(term.replace("_", "-").split("-")).strip()
    if not words:
        return None
    if axis == "value_depth":
        return f"a {words} value"
    if axis == "chroma":
        return f"{words} chroma"
    if axis in {"undertone", "finish"}:
        article = "an" if words[0].casefold() in "aeiou" else "a"
        noun = "undertone" if axis == "undertone" else "finish"
        return f"{article} {words} {noun}"
    raise ValueError(f"unsupported controlled descriptor axis: {axis}")


def compose_controlled_descriptor(
    classification: dict[str, Any],
    surface_term: str,
    *,
    include_finish: bool = True,
) -> dict[str, Any]:
    """Compose literal classified axes without inventing a semantic label.

    ``surface_term`` is supplied by the analyst (for example, the visible region
    name).  Low-confidence, mixed, or uncertain required evidence fails closed.
    The return value deliberately contains no production ``emit`` decision.
    """

    surface = _string(surface_term, "surface_term")
    axes = _object(classification.get("axis_classification"), "axis_classification")
    requested_axes = list(CONTROLLED_DESCRIPTOR_CORE_AXES)
    if include_finish:
        requested_axes.append("finish")

    excerpts: dict[str, str] = {}
    unresolved: list[str] = []
    for axis in requested_axes:
        axis_spec = _object(axes.get(axis), f"axis_classification.{axis}")
        term = _string(axis_spec.get("term"), f"axis_classification.{axis}.term")
        confidence = _string(
            axis_spec.get("confidence"), f"axis_classification.{axis}.confidence"
        )
        if confidence not in VALID_CONFIDENCE:
            raise ValueError(f"axis_classification.{axis}.confidence is invalid")
        phrase = _controlled_axis_excerpt(axis, term)
        if confidence == "low" or phrase is None:
            unresolved.append(axis)
        else:
            excerpts[axis] = phrase

    if unresolved:
        return {
            "status": "inconclusive",
            "surface_term": surface,
            "included_axes": requested_axes,
            "axis_excerpts": excerpts,
            "unresolved_axes": unresolved,
            "composition_source": "axis-composed",
        }

    ordered_excerpts = [excerpts[axis] for axis in requested_axes]
    if len(ordered_excerpts) == 1:
        joined = ordered_excerpts[0]
    elif len(ordered_excerpts) == 2:
        joined = " and ".join(ordered_excerpts)
    else:
        joined = ", ".join(ordered_excerpts[:-1]) + ", and " + ordered_excerpts[-1]
    return {
        "status": "ready",
        "surface_term": surface,
        "phrase": f"{surface} with {joined}",
        "included_axes": requested_axes,
        "axis_excerpts": excerpts,
        "unresolved_axes": [],
        "composition_source": "axis-composed",
    }


def review_candidates(
    classification: dict[str, Any], candidate_payload: dict[str, Any]
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
    reports: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_candidates):
        candidate = _object(raw, f"candidates[{index}]")
        phrase = _string(candidate.get("phrase"), f"candidates[{index}].phrase")
        scope = _string(candidate.get("label_scope"), f"candidates[{index}].label_scope")
        if scope not in VALID_LABEL_SCOPES:
            raise ValueError(f"candidates[{index}].label_scope is invalid")
        requirements = _object(candidate.get("axis_requirements"), f"candidates[{index}].axis_requirements")
        unknown_axes = sorted(set(requirements) - CLASSIFIED_AXES)
        if unknown_axes:
            raise ValueError(f"candidates[{index}] contains unknown axes: {', '.join(unknown_axes)}")
        missing_axes = REQUIRED_SCOPE_AXES[scope] - set(requirements)
        if scope == "composite-appearance" and not ({"finish", "evenness"} & set(requirements)):
            missing_axes.add("finish-or-evenness")
        if missing_axes:
            raise ValueError(
                f"candidates[{index}] does not support its label scope: "
                + ", ".join(sorted(missing_axes))
            )
        matched: list[str] = []
        conflicting: list[str] = []
        unresolved: list[str] = []
        for axis, allowed in requirements.items():
            if not isinstance(allowed, list) or not allowed or not all(isinstance(item, str) and item for item in allowed):
                raise ValueError(f"candidates[{index}].axis_requirements.{axis} must contain terms")
            term = axes[axis]["term"]
            if term == "uncertain" or axes[axis]["confidence"] == "low":
                unresolved.append(axis)
            elif term in allowed:
                matched.append(axis)
            else:
                conflicting.append(axis)
        status = "conflicting" if conflicting else "inconclusive" if unresolved else "compatible"
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
    parser.add_argument("observation", help="analyst-authored Lab observation JSON")
    parser.add_argument("--policy", required=True, help="versioned language policy JSON")
    parser.add_argument("--candidates", default="", help="optional externally supplied label candidates JSON")
    parser.add_argument(
        "--compose-for",
        default="",
        help="optional analyst-supplied visible surface term for an axis-composed descriptor",
    )
    parser.add_argument(
        "--without-finish",
        action="store_true",
        help="compose only value depth, chroma, and undertone",
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
                "source-visible language classification only",
                "no semantic region detection",
                "no biological, demographic, or material true-color inference",
                "no friendly-label candidate invention",
                "no automatic friendly-label selection",
                "controlled descriptor composition does not decide prompt emission",
            ],
        }
        if args.compose_for:
            payload["controlled_descriptor"] = compose_controlled_descriptor(
                classification,
                args.compose_for,
                include_finish=not args.without_finish,
            )
        if args.candidates:
            payload["friendly_label_review"] = review_candidates(
                classification, _load(Path(args.candidates), "candidate payload")
            )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
