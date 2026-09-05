#!/usr/bin/env python3
"""Evaluate analyst-defined source/render color groups without choosing semantics.

The input is a successful JSON payload from color_probe.py containing source and
comparison group summaries. Group roles come from the sampling spec or explicit
CLI names. Without a caller-supplied tolerance policy, results remain unscored.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
import sys
from typing import Any, Iterable

from color_probe import delta_e2000


TARGET_POLICY_KEYS = {
    "max_abs_delta_l",
    "max_abs_delta_c",
    "max_abs_hue_degrees",
    "max_delta_e2000",
}
CONTEXT_POLICY_KEYS = {"max_abs_delta_l", "max_opponent_shift"}


def _median_triplets(values: list[list[float]]) -> list[float]:
    if not values:
        raise ValueError("at least one context group is required")
    return [
        statistics.median(float(value[index]) for value in values)
        for index in range(3)
    ]


def _chroma(lab: Iterable[float]) -> float:
    values = list(lab)
    return math.hypot(float(values[1]), float(values[2]))


def _hue(lab: Iterable[float]) -> float:
    values = list(lab)
    return math.degrees(math.atan2(float(values[2]), float(values[1]))) % 360.0


def _hue_delta(target: float, source: float) -> float:
    return (target - source + 180.0) % 360.0 - 180.0


def _delta_lab(source: Iterable[float], target: Iterable[float]) -> list[float]:
    return [float(target_value) - float(source_value) for source_value, target_value in zip(source, target)]


def _round_triplet(values: Iterable[float]) -> list[float]:
    return [round(float(value), 3) for value in values]


def _group_maps(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source = payload.get("source")
    comparison = payload.get("comparison")
    if not isinstance(source, dict) or not isinstance(comparison, dict):
        raise ValueError("report must contain source and comparison objects")
    source_groups = source.get("groups")
    comparison_groups = comparison.get("groups")
    if not isinstance(source_groups, list) or not source_groups:
        raise ValueError("source report must contain group summaries")
    if not isinstance(comparison_groups, list) or not comparison_groups:
        raise ValueError("comparison report must contain group summaries")
    source_map = {group.get("name"): group for group in source_groups if isinstance(group, dict)}
    comparison_map = {
        group.get("name"): group for group in comparison_groups if isinstance(group, dict)
    }
    if set(source_map) != set(comparison_map) or None in source_map:
        raise ValueError("source and comparison reports must contain matching named groups")
    return source_map, comparison_map


def _resolve_group_names(
    source_map: dict[str, Any],
    explicit_targets: list[str] | None,
    explicit_contexts: list[str] | None,
) -> tuple[list[str], list[str]]:
    targets = list(explicit_targets or [])
    contexts = list(explicit_contexts or [])
    if not targets:
        targets = sorted(
            name
            for name, group in source_map.items()
            if group.get("semantic_role") == "target"
        )
    if not contexts:
        contexts = sorted(
            name
            for name, group in source_map.items()
            if group.get("semantic_role") in {"context", "neutral"}
        )
    unknown = sorted((set(targets) | set(contexts)) - set(source_map))
    if unknown:
        raise ValueError("unknown evaluation groups: " + ", ".join(unknown))
    if not targets:
        raise ValueError("at least one target group is required")
    if not contexts:
        raise ValueError("at least one context or neutral group is required")
    if set(targets) & set(contexts):
        raise ValueError("target and context groups must be disjoint")
    return targets, contexts


def _validate_policy(policy: dict[str, Any] | None) -> dict[str, dict[str, float]] | None:
    if policy is None:
        return None
    if not isinstance(policy, dict):
        raise ValueError("policy must be an object")
    validated: dict[str, dict[str, float]] = {"target": {}, "context": {}}
    for section, allowed in (("target", TARGET_POLICY_KEYS), ("context", CONTEXT_POLICY_KEYS)):
        values = policy.get(section, {})
        if not isinstance(values, dict):
            raise ValueError(f"policy.{section} must be an object")
        unknown = sorted(set(values) - allowed)
        if unknown:
            raise ValueError(f"policy.{section} contains unknown keys: {', '.join(unknown)}")
        for key, value in values.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"policy.{section}.{key} must be a positive number")
            validated[section][key] = float(value)
    if not validated["target"] and not validated["context"]:
        raise ValueError("policy must define at least one tolerance")
    return validated


def _target_metrics(source_lab: list[float], render_lab: list[float]) -> dict[str, Any]:
    delta = _delta_lab(source_lab, render_lab)
    return {
        "lab_d65": _round_triplet(delta),
        "abs_delta_l": round(abs(delta[0]), 3),
        "delta_c": round(_chroma(render_lab) - _chroma(source_lab), 3),
        "hue_degrees": round(_hue_delta(_hue(render_lab), _hue(source_lab)), 3),
        "delta_e2000": round(delta_e2000(source_lab, render_lab), 3),
    }


def _target_violations(
    name: str, metrics: dict[str, Any], policy: dict[str, float]
) -> list[str]:
    checks = {
        "max_abs_delta_l": metrics["abs_delta_l"],
        "max_abs_delta_c": abs(metrics["delta_c"]),
        "max_abs_hue_degrees": abs(metrics["hue_degrees"]),
        "max_delta_e2000": metrics["delta_e2000"],
    }
    return [
        f"target:{name}:{key}"
        for key, observed in checks.items()
        if key in policy and observed > policy[key]
    ]


def evaluate_report(
    payload: dict[str, Any],
    policy: dict[str, Any] | None = None,
    target_groups: list[str] | None = None,
    context_groups: list[str] | None = None,
) -> dict[str, Any]:
    """Return global/context movement, target-local residuals, and optional score."""

    source_map, comparison_map = _group_maps(payload)
    targets, contexts = _resolve_group_names(
        source_map, target_groups, context_groups
    )
    validated_policy = _validate_policy(policy)

    context_deltas: list[list[float]] = []
    for name in contexts:
        source_lab = source_map[name]["equal_region_median"]["lab_d65"]
        render_lab = comparison_map[name]["equal_region_median"]["lab_d65"]
        context_deltas.append(_delta_lab(source_lab, render_lab))
    global_shift = _median_triplets(context_deltas)
    global_opponent_shift = math.hypot(global_shift[1], global_shift[2])

    target_results: list[dict[str, Any]] = []
    total_violations: list[str] = []
    local_violations: list[str] = []
    for name in targets:
        source_lab = [
            float(value)
            for value in source_map[name]["equal_region_median"]["lab_d65"]
        ]
        render_lab = [
            float(value)
            for value in comparison_map[name]["equal_region_median"]["lab_d65"]
        ]
        corrected_lab = [
            render_lab[index] - global_shift[index] for index in range(3)
        ]
        total_metrics = _target_metrics(source_lab, render_lab)
        local_metrics = _target_metrics(source_lab, corrected_lab)
        target_results.append(
            {
                "name": name,
                "semantic_role": source_map[name].get("semantic_role"),
                "tone_zone": source_map[name].get("tone_zone"),
                "purpose": source_map[name].get("purpose"),
                "total_render_minus_source": total_metrics,
                "context_corrected_local_residual": local_metrics,
            }
        )
        if validated_policy:
            total_violations.extend(
                _target_violations(name, total_metrics, validated_policy["target"])
            )
            local_violations.extend(
                _target_violations(name, local_metrics, validated_policy["target"])
            )

    context_violations: list[str] = []
    if validated_policy:
        context_policy = validated_policy["context"]
        if (
            "max_abs_delta_l" in context_policy
            and abs(global_shift[0]) > context_policy["max_abs_delta_l"]
        ):
            context_violations.append("context:max_abs_delta_l")
        if (
            "max_opponent_shift" in context_policy
            and global_opponent_shift > context_policy["max_opponent_shift"]
        ):
            context_violations.append("context:max_opponent_shift")

    if validated_policy is None:
        status = "unscored"
        drift_class = "inconclusive"
        dominant_axis = "none"
    else:
        violations = total_violations + context_violations
        status = "fail" if violations else "pass"
        has_global = bool(context_violations)
        has_local = bool(local_violations)
        if has_global and has_local:
            drift_class = "mixed"
        elif has_local:
            drift_class = "target-local"
        elif has_global:
            l_ratio = (
                abs(global_shift[0]) / validated_policy["context"]["max_abs_delta_l"]
                if "max_abs_delta_l" in validated_policy["context"]
                else 0.0
            )
            opponent_ratio = (
                global_opponent_shift
                / validated_policy["context"]["max_opponent_shift"]
                if "max_opponent_shift" in validated_policy["context"]
                else 0.0
            )
            drift_class = "global-exposure" if l_ratio >= opponent_ratio else "global-cast"
        else:
            drift_class = "within-policy"

        axis_ratios: dict[str, float] = {}
        target_policy = validated_policy["target"]
        for target_result in target_results:
            local_metrics = target_result["context_corrected_local_residual"]
            if "max_abs_delta_l" in target_policy:
                axis_ratios["value"] = max(
                    axis_ratios.get("value", 0.0),
                    local_metrics["abs_delta_l"] / target_policy["max_abs_delta_l"],
                )
            if "max_abs_delta_c" in target_policy:
                axis_ratios["chroma"] = max(
                    axis_ratios.get("chroma", 0.0),
                    abs(local_metrics["delta_c"]) / target_policy["max_abs_delta_c"],
                )
            if "max_abs_hue_degrees" in target_policy:
                axis_ratios["hue"] = max(
                    axis_ratios.get("hue", 0.0),
                    abs(local_metrics["hue_degrees"])
                    / target_policy["max_abs_hue_degrees"],
                )
        dominant_axis = max(axis_ratios, key=axis_ratios.get) if axis_ratios else "none"

    return {
        "status": status,
        "comparison_scope": payload.get("comparison_context", {}).get("scope", "unknown"),
        "target_groups": target_results,
        "context_groups": contexts,
        "global_context_movement": {
            "lab_d65": _round_triplet(global_shift),
            "abs_delta_l": round(abs(global_shift[0]), 3),
            "opponent_shift": round(global_opponent_shift, 3),
        },
        "drift_class": drift_class,
        "dominant_residual_axis": dominant_axis,
        "violations": total_violations + context_violations if validated_policy else [],
        "policy": validated_policy,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate color_probe source/render group reports."
    )
    parser.add_argument("report", help="successful color_probe JSON report")
    parser.add_argument("--policy", default="", help="optional tolerance policy JSON")
    parser.add_argument("--target-group", action="append", default=[])
    parser.add_argument("--context-group", action="append", default=[])
    args = parser.parse_args(argv)

    try:
        payload = json.loads(Path(args.report).read_text(encoding="utf-8"))
        if payload.get("status") != "ok":
            raise ValueError("color probe report status must be ok")
        policy = (
            json.loads(Path(args.policy).read_text(encoding="utf-8"))
            if args.policy
            else None
        )
        result = evaluate_report(
            payload,
            policy,
            args.target_group or None,
            args.context_group or None,
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
