#!/usr/bin/env python3
"""Measure analyst-selected lightness regions and profiles without inferring semantics.

The probe reports display-relative diagnostics only. It does not detect subjects,
materials, shadows, or light direction and never emits prompt wording or PASS/FAIL.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import statistics
import sys
from typing import Any

from color_probe import (  # local sibling; shares profile handling and Lab conversion.
    RegionSpec,
    _load_srgb,
    _percentile,
    analyze_image,
    comparison_context,
    srgb_to_lab,
)


@dataclass(frozen=True)
class RelationSpec:
    name: str
    left_region: str
    right_region: str


@dataclass(frozen=True)
class ProfileSpec:
    name: str
    line: tuple[float, float, float, float]
    samples: int = 64
    width_px: int = 1


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _normalized_quad(value: Any, label: str) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must contain four normalized coordinates")
    if not all(isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{label} coordinates must be numeric")
    result = tuple(float(item) for item in value)
    if not all(0.0 <= item <= 1.0 for item in result):
        raise ValueError(f"{label} coordinates must stay within 0..1")
    return result


def _bounds(value: Any, label: str) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = _normalized_quad(value, label)
    if not (x0 < x1 and y0 < y1):
        raise ValueError(f"{label} must satisfy x0 < x1 and y0 < y1")
    return x0, y0, x1, y1


def _line(value: Any, label: str) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = _normalized_quad(value, label)
    if x0 == x1 and y0 == y1:
        raise ValueError(f"{label} endpoints must differ")
    return x0, y0, x1, y1


def load_spec(
    path: Path,
) -> tuple[
    list[RegionSpec],
    list[RegionSpec],
    list[RelationSpec],
    list[ProfileSpec],
    list[ProfileSpec],
]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("sampling spec must be an object")

    raw_regions = payload.get("regions", [])
    if not isinstance(raw_regions, list):
        raise ValueError("sampling spec regions must be a list")
    source_regions: list[RegionSpec] = []
    comparison_regions: list[RegionSpec] = []
    region_names: set[str] = set()
    for index, item in enumerate(raw_regions):
        label = f"sampling spec regions[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{label} must be an object")
        name = _nonempty_string(item.get("name"), f"{label}.name")
        if name in region_names:
            raise ValueError(f"duplicate region name: {name}")
        region_names.add(name)
        source_bounds = _bounds(item.get("source_bounds"), f"{label}.source_bounds")
        comparison_bounds = _bounds(
            item.get("comparison_bounds", item.get("source_bounds")),
            f"{label}.comparison_bounds",
        )
        source_regions.append(RegionSpec(name, source_bounds))
        comparison_regions.append(RegionSpec(name, comparison_bounds))

    raw_relations = payload.get("relations", [])
    if not isinstance(raw_relations, list):
        raise ValueError("sampling spec relations must be a list")
    relations: list[RelationSpec] = []
    relation_names: set[str] = set()
    for index, item in enumerate(raw_relations):
        label = f"sampling spec relations[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{label} must be an object")
        name = _nonempty_string(item.get("name"), f"{label}.name")
        if name in relation_names:
            raise ValueError(f"duplicate relation name: {name}")
        relation_names.add(name)
        left = _nonempty_string(item.get("left_region"), f"{label}.left_region")
        right = _nonempty_string(item.get("right_region"), f"{label}.right_region")
        unknown = {left, right} - region_names
        if unknown:
            raise ValueError(
                f"{label} references unknown regions: {', '.join(sorted(unknown))}"
            )
        if left == right:
            raise ValueError(f"{label} must compare two different regions")
        relations.append(RelationSpec(name, left, right))

    raw_profiles = payload.get("profiles", [])
    if not isinstance(raw_profiles, list):
        raise ValueError("sampling spec profiles must be a list")
    source_profiles: list[ProfileSpec] = []
    comparison_profiles: list[ProfileSpec] = []
    profile_names: set[str] = set()
    for index, item in enumerate(raw_profiles):
        label = f"sampling spec profiles[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{label} must be an object")
        name = _nonempty_string(item.get("name"), f"{label}.name")
        if name in profile_names:
            raise ValueError(f"duplicate profile name: {name}")
        profile_names.add(name)
        samples = item.get("samples", 64)
        width_px = item.get("width_px", 1)
        if not isinstance(samples, int) or not 8 <= samples <= 2048:
            raise ValueError(f"{label}.samples must be an integer from 8 to 2048")
        if not isinstance(width_px, int) or not 1 <= width_px <= 101:
            raise ValueError(f"{label}.width_px must be an integer from 1 to 101")
        source_line = _line(item.get("source_line"), f"{label}.source_line")
        comparison_line = _line(
            item.get("comparison_line", item.get("source_line")),
            f"{label}.comparison_line",
        )
        source_profiles.append(ProfileSpec(name, source_line, samples, width_px))
        comparison_profiles.append(
            ProfileSpec(name, comparison_line, samples, width_px)
        )

    if not source_regions and not source_profiles:
        raise ValueError("sampling spec requires at least one region or profile")
    return (
        source_regions,
        comparison_regions,
        relations,
        source_profiles,
        comparison_profiles,
    )


def _sample_lightness_profile(image: Any, spec: ProfileSpec) -> list[float]:
    width, height = image.size
    x0, y0, x1, y1 = spec.line
    radius = spec.width_px // 2
    pixels = image.load()
    values: list[float] = []
    for index in range(spec.samples):
        fraction = index / (spec.samples - 1)
        center_x = round((x0 + (x1 - x0) * fraction) * (width - 1))
        center_y = round((y0 + (y1 - y0) * fraction) * (height - 1))
        local: list[float] = []
        for py in range(max(0, center_y - radius), min(height, center_y + radius + 1)):
            for px in range(max(0, center_x - radius), min(width, center_x + radius + 1)):
                local.append(srgb_to_lab(pixels[px, py])[0])
        values.append(statistics.mean(local))
    return values


def _crossing_index(values: list[float], target: float, increasing: bool) -> int | None:
    for index, value in enumerate(values):
        if (increasing and value >= target) or (not increasing and value <= target):
            return index
    return None


def summarize_profile(values: list[float]) -> dict[str, Any]:
    window = max(1, len(values) // 10)
    start = statistics.median(values[:window])
    end = statistics.median(values[-window:])
    net_change = end - start
    endpoint_change = values[-1] - values[0]
    adjacent = [values[index + 1] - values[index] for index in range(len(values) - 1)]
    total_variation = sum(abs(value) for value in adjacent)
    monotonicity = abs(endpoint_change) / total_variation if total_variation else 1.0
    transition_width: float | None = None
    if abs(net_change) >= 1.0 and monotonicity >= 0.6:
        increasing = net_change > 0
        index_10 = _crossing_index(values, start + 0.1 * net_change, increasing)
        index_90 = _crossing_index(values, start + 0.9 * net_change, increasing)
        if index_10 is not None and index_90 is not None:
            transition_width = abs(index_90 - index_10) / (len(values) - 1)
    return {
        "sample_count": len(values),
        "lightness": {
            "p10": round(_percentile(values, 0.10), 3),
            "p50": round(_percentile(values, 0.50), 3),
            "p90": round(_percentile(values, 0.90), 3),
            "robust_range_p90_p10": round(
                _percentile(values, 0.90) - _percentile(values, 0.10), 3
            ),
            "start_median": round(start, 3),
            "end_median": round(end, 3),
            "net_change": round(net_change, 3),
            "total_variation": round(total_variation, 3),
            "max_adjacent_gradient": round(max(abs(value) for value in adjacent), 3),
            "monotonicity": round(monotonicity, 6),
            "transition_width_fraction_10_90": (
                round(transition_width, 6) if transition_width is not None else None
            ),
        },
    }


def analyze_light(
    path: Path,
    regions: list[RegionSpec],
    relations: list[RelationSpec],
    profiles: list[ProfileSpec],
) -> dict[str, Any]:
    image, profile_status, warnings = _load_srgb(path)
    region_report = analyze_image(path, regions) if regions else {"regions": []}
    simplified_regions = []
    region_lightness: dict[str, float] = {}
    for region in region_report["regions"]:
        lightness = float(region["median"]["lab_d65"][0])
        region_lightness[region["name"]] = lightness
        simplified_regions.append(
            {
                "name": region["name"],
                "normalized_bounds": region["normalized_bounds"],
                "median_lightness": round(lightness, 3),
                "iqr_lightness": region["iqr"]["lightness"],
                "sample_count": region["sample_count"],
            }
        )
    relation_report = [
        {
            "name": relation.name,
            "left_region": relation.left_region,
            "right_region": relation.right_region,
            "left_minus_right_lightness": round(
                region_lightness[relation.left_region]
                - region_lightness[relation.right_region],
                3,
            ),
        }
        for relation in relations
    ]
    profile_report = []
    for profile in profiles:
        summary = summarize_profile(_sample_lightness_profile(image, profile))
        profile_report.append(
            {
                "name": profile.name,
                "normalized_line": [round(value, 6) for value in profile.line],
                "width_px": profile.width_px,
                **summary,
            }
        )
    return {
        "path": str(path.resolve()),
        "size": {"width": image.width, "height": image.height},
        "profile_status": profile_status,
        "warnings": warnings,
        "regions": simplified_regions,
        "relations": relation_report,
        "profiles": profile_report,
    }


def _named(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["name"]): item for item in items}


def compare_light_reports(source: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "context": comparison_context(source, target),
        "regions": [],
        "relations": [],
        "profiles": [],
        "evaluation_status": "diagnostic-unscored",
    }
    for key, metric in (
        ("regions", "median_lightness"),
        ("relations", "left_minus_right_lightness"),
    ):
        source_items = _named(source[key])
        target_items = _named(target[key])
        if set(source_items) != set(target_items):
            raise ValueError(f"source and comparison {key} names must match")
        for name in sorted(source_items):
            result[key].append(
                {
                    "name": name,
                    "target_minus_source": round(
                        float(target_items[name][metric])
                        - float(source_items[name][metric]),
                        3,
                    ),
                    "metric": metric,
                }
            )

    source_profiles = _named(source["profiles"])
    target_profiles = _named(target["profiles"])
    if set(source_profiles) != set(target_profiles):
        raise ValueError("source and comparison profile names must match")
    metrics = (
        "robust_range_p90_p10",
        "net_change",
        "total_variation",
        "max_adjacent_gradient",
        "monotonicity",
    )
    for name in sorted(source_profiles):
        source_lightness = source_profiles[name]["lightness"]
        target_lightness = target_profiles[name]["lightness"]
        deltas = {
            metric: round(
                float(target_lightness[metric]) - float(source_lightness[metric]),
                6,
            )
            for metric in metrics
        }
        source_width = source_lightness["transition_width_fraction_10_90"]
        target_width = target_lightness["transition_width_fraction_10_90"]
        deltas["transition_width_fraction_10_90"] = (
            round(float(target_width) - float(source_width), 6)
            if source_width is not None and target_width is not None
            else None
        )
        result["profiles"].append({"name": name, "target_minus_source": deltas})
    return result


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="source image")
    parser.add_argument("--compare", default="", help="optional rendered comparison image")
    parser.add_argument("--spec", required=True, help="analyst-authored sampling JSON")
    args = parser.parse_args(argv)
    try:
        (
            source_regions,
            comparison_regions,
            relations,
            source_profiles,
            comparison_profiles,
        ) = load_spec(Path(args.spec))
        source = analyze_light(
            Path(args.source), source_regions, relations, source_profiles
        )
        payload: dict[str, Any] = {
            "scope": "analyst-selected-display-relative-lightness",
            "source": source,
            "limitations": [
                "no semantic detection",
                "no physical-light inference",
                "no automatic prompt wording",
                "no automatic fidelity threshold",
            ],
        }
        if args.compare:
            target = analyze_light(
                Path(args.compare),
                comparison_regions,
                relations,
                comparison_profiles,
            )
            payload["comparison"] = target
            payload["delta"] = compare_light_reports(source, target)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
