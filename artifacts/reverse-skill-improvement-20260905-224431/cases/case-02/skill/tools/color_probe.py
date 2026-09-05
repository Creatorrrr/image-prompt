#!/usr/bin/env python3
"""Measure user-selected image regions without choosing semantic targets.

The probe is diagnostic only. It reports robust source-relative color evidence,
profile status, and optional source/render deltas; it never emits prompt text or
auto-detects skin, products, backgrounds, or other semantic regions. Optional
groups are analyst-named and use equal region weighting.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import sys
from typing import Any, Iterable

try:
    from PIL import Image, ImageCms
except ImportError:  # pragma: no cover - exercised only without optional dependency.
    Image = None
    ImageCms = None


MAX_DEFAULT_SAMPLES = 50_000
VALID_TONE_ZONES = {"highlight", "midtone", "shadow", "flat", "mixed"}
VALID_SEMANTIC_ROLES = {"target", "context", "neutral", "supporting"}
VALID_PURPOSES = {
    "intrinsic-displayed-color",
    "highlight-response",
    "shadow-response",
    "global-cast-and-exposure",
    "relative-relation",
    "diagnostic",
}


@dataclass(frozen=True)
class RegionSpec:
    name: str
    bounds: tuple[float, float, float, float]
    semantic_role: str = ""
    tone_zone: str = ""
    purpose: str = ""


@dataclass(frozen=True)
class GroupSpec:
    name: str
    region_names: tuple[str, ...]
    semantic_role: str = ""
    tone_zone: str = ""
    purpose: str = ""


def parse_region(raw: str) -> RegionSpec:
    """Parse NAME=X0,Y0,X1,Y1 with normalized coordinates."""

    if "=" not in raw:
        raise ValueError("region must use NAME=X0,Y0,X1,Y1")
    name, raw_bounds = raw.split("=", 1)
    name = name.strip()
    if not name:
        raise ValueError("region name must be non-empty")
    parts = [part.strip() for part in raw_bounds.split(",")]
    if len(parts) != 4:
        raise ValueError(f"region {name!r} must contain four coordinates")
    try:
        x0, y0, x1, y1 = (float(part) for part in parts)
    except ValueError as exc:
        raise ValueError(f"region {name!r} contains a non-numeric coordinate") from exc
    if not (0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
        raise ValueError(
            f"region {name!r} coordinates must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1"
        )
    return RegionSpec(name=name, bounds=(x0, y0, x1, y1))


def parse_group(raw: str) -> GroupSpec:
    """Parse NAME=REGION_A,REGION_B with at least two unique members."""

    if "=" not in raw:
        raise ValueError("group must use NAME=REGION_A,REGION_B")
    name, raw_members = raw.split("=", 1)
    name = name.strip()
    if not name:
        raise ValueError("group name must be non-empty")
    region_names = tuple(part.strip() for part in raw_members.split(",") if part.strip())
    if len(region_names) < 2:
        raise ValueError(f"group {name!r} must contain at least two regions")
    if len(set(region_names)) != len(region_names):
        raise ValueError(f"group {name!r} region names must be unique")
    return GroupSpec(name=name, region_names=region_names)


def _parse_bounds(value: Any, label: str) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must contain four normalized coordinates")
    if not all(isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{label} coordinates must be numeric")
    x0, y0, x1, y1 = (float(item) for item in value)
    if not (0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
        raise ValueError(
            f"{label} must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1"
        )
    return x0, y0, x1, y1


def _validate_region_metadata(
    semantic_role: Any,
    tone_zone: Any,
    purpose: Any,
    label: str,
) -> tuple[str, str, str]:
    if semantic_role not in VALID_SEMANTIC_ROLES:
        raise ValueError(f"{label}.semantic_role is invalid")
    if tone_zone not in VALID_TONE_ZONES:
        raise ValueError(f"{label}.tone_zone is invalid")
    if purpose not in VALID_PURPOSES:
        raise ValueError(f"{label}.purpose is invalid")
    if purpose == "intrinsic-displayed-color" and tone_zone not in {"midtone", "flat"}:
        raise ValueError(
            f"{label}: intrinsic-displayed-color requires a midtone or flat tone_zone"
        )
    return str(semantic_role), str(tone_zone), str(purpose)


def load_sampling_spec(
    path: Path,
) -> tuple[list[RegionSpec], list[RegionSpec], list[GroupSpec]]:
    """Load analyst-authored source/render bounds and semantic group metadata."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("sampling spec must be an object")
    raw_regions = payload.get("regions")
    if not isinstance(raw_regions, list) or not raw_regions:
        raise ValueError("sampling spec regions must be a non-empty list")

    source_regions: list[RegionSpec] = []
    comparison_regions: list[RegionSpec] = []
    seen_names: set[str] = set()
    for index, raw_region in enumerate(raw_regions):
        label = f"sampling spec regions[{index}]"
        if not isinstance(raw_region, dict):
            raise ValueError(f"{label} must be an object")
        name = raw_region.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{label}.name must be non-empty")
        name = name.strip()
        if name in seen_names:
            raise ValueError(f"duplicate sampling region name: {name}")
        seen_names.add(name)
        source_bounds = _parse_bounds(raw_region.get("source_bounds"), f"{label}.source_bounds")
        comparison_bounds = _parse_bounds(
            raw_region.get("comparison_bounds", raw_region.get("source_bounds")),
            f"{label}.comparison_bounds",
        )
        semantic_role, tone_zone, purpose = _validate_region_metadata(
            raw_region.get("semantic_role"),
            raw_region.get("tone_zone"),
            raw_region.get("purpose"),
            label,
        )
        source_regions.append(
            RegionSpec(name, source_bounds, semantic_role, tone_zone, purpose)
        )
        comparison_regions.append(
            RegionSpec(name, comparison_bounds, semantic_role, tone_zone, purpose)
        )

    raw_groups = payload.get("groups", [])
    if not isinstance(raw_groups, list):
        raise ValueError("sampling spec groups must be a list")
    groups: list[GroupSpec] = []
    seen_group_names: set[str] = set()
    region_map = {region.name: region for region in source_regions}
    for index, raw_group in enumerate(raw_groups):
        label = f"sampling spec groups[{index}]"
        if not isinstance(raw_group, dict):
            raise ValueError(f"{label} must be an object")
        name = raw_group.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{label}.name must be non-empty")
        name = name.strip()
        if name in seen_group_names:
            raise ValueError(f"duplicate sampling group name: {name}")
        seen_group_names.add(name)
        raw_members = raw_group.get("region_names")
        if not isinstance(raw_members, list) or len(raw_members) < 2 or not all(
            isinstance(item, str) and item.strip() for item in raw_members
        ):
            raise ValueError(f"{label}.region_names must contain at least two names")
        region_names = tuple(item.strip() for item in raw_members)
        if len(set(region_names)) != len(region_names):
            raise ValueError(f"{label}.region_names must be unique")
        unknown = sorted(set(region_names) - set(region_map))
        if unknown:
            raise ValueError(f"{label} references unknown regions: {', '.join(unknown)}")
        semantic_role, tone_zone, purpose = _validate_region_metadata(
            raw_group.get("semantic_role"),
            raw_group.get("tone_zone"),
            raw_group.get("purpose"),
            label,
        )
        for region_name in region_names:
            region = region_map[region_name]
            if (
                region.semantic_role != semantic_role
                or region.tone_zone != tone_zone
                or region.purpose != purpose
            ):
                raise ValueError(
                    f"{label} metadata must match every member region"
                )
        groups.append(
            GroupSpec(name, region_names, semantic_role, tone_zone, purpose)
        )

    return source_regions, comparison_regions, groups


def _load_srgb(path: Path) -> tuple[Image.Image, str, list[str]]:
    if Image is None or ImageCms is None:
        raise RuntimeError("color_probe.py requires Pillow")
    image = Image.open(path)
    warnings: list[str] = []
    if "A" in image.getbands():
        warnings.append("alpha channel was discarded for color measurement")

    icc_profile = image.info.get("icc_profile")
    if icc_profile:
        try:
            source_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_profile))
            srgb_profile = ImageCms.createProfile("sRGB")
            image = ImageCms.profileToProfile(
                image,
                source_profile,
                srgb_profile,
                outputMode="RGB",
            )
            profile_status = "embedded-profile-converted-to-srgb"
        except Exception as exc:  # noqa: BLE001 - diagnostic tool must preserve uncertainty.
            image = image.convert("RGB")
            profile_status = "embedded-profile-conversion-failed"
            warnings.append(f"embedded profile could not be converted: {exc}")
    else:
        image = image.convert("RGB")
        profile_status = "missing-profile-assumed-srgb"
        warnings.append(
            "no embedded ICC profile; values assume ordinary sRGB display interpretation"
        )
    return image, profile_status, warnings


def _srgb_channel_to_linear(value: float) -> float:
    value /= 255.0
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def srgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    """Convert an sRGB triplet to CIE Lab using a D65 reference white."""

    red, green, blue = (_srgb_channel_to_linear(float(value)) for value in rgb)
    x = red * 0.4124564 + green * 0.3575761 + blue * 0.1804375
    y = red * 0.2126729 + green * 0.7151522 + blue * 0.0721750
    z = red * 0.0193339 + green * 0.1191920 + blue * 0.9503041
    x /= 0.95047
    z /= 1.08883
    delta = 6.0 / 29.0

    def transform(value: float) -> float:
        return (
            value ** (1.0 / 3.0)
            if value > delta**3
            else value / (3.0 * delta**2) + 4.0 / 29.0
        )

    fx, fy, fz = transform(x), transform(y), transform(z)
    return 116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz)


def delta_e2000(
    lab_a: Iterable[float], lab_b: Iterable[float]
) -> float:
    """Return CIEDE2000 color difference for two CIELAB triplets."""

    l1, a1, b1 = (float(value) for value in lab_a)
    l2, a2, b2 = (float(value) for value in lab_b)
    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_bar = (c1 + c2) / 2.0
    c_bar_7 = c_bar**7
    g = 0.5 * (1.0 - math.sqrt(c_bar_7 / (c_bar_7 + 25.0**7)))
    a1_prime = (1.0 + g) * a1
    a2_prime = (1.0 + g) * a2
    c1_prime = math.hypot(a1_prime, b1)
    c2_prime = math.hypot(a2_prime, b2)

    def hue_prime(a_value: float, b_value: float) -> float:
        if a_value == 0.0 and b_value == 0.0:
            return 0.0
        return math.degrees(math.atan2(b_value, a_value)) % 360.0

    h1_prime = hue_prime(a1_prime, b1)
    h2_prime = hue_prime(a2_prime, b2)
    delta_l_prime = l2 - l1
    delta_c_prime = c2_prime - c1_prime
    if c1_prime * c2_prime == 0.0:
        delta_h_prime = 0.0
    else:
        raw_delta_h = h2_prime - h1_prime
        if abs(raw_delta_h) <= 180.0:
            delta_h_prime = raw_delta_h
        elif raw_delta_h > 180.0:
            delta_h_prime = raw_delta_h - 360.0
        else:
            delta_h_prime = raw_delta_h + 360.0
    delta_big_h_prime = 2.0 * math.sqrt(c1_prime * c2_prime) * math.sin(
        math.radians(delta_h_prime / 2.0)
    )

    l_bar_prime = (l1 + l2) / 2.0
    c_bar_prime = (c1_prime + c2_prime) / 2.0
    if c1_prime * c2_prime == 0.0:
        h_bar_prime = h1_prime + h2_prime
    elif abs(h1_prime - h2_prime) <= 180.0:
        h_bar_prime = (h1_prime + h2_prime) / 2.0
    elif h1_prime + h2_prime < 360.0:
        h_bar_prime = (h1_prime + h2_prime + 360.0) / 2.0
    else:
        h_bar_prime = (h1_prime + h2_prime - 360.0) / 2.0

    t = (
        1.0
        - 0.17 * math.cos(math.radians(h_bar_prime - 30.0))
        + 0.24 * math.cos(math.radians(2.0 * h_bar_prime))
        + 0.32 * math.cos(math.radians(3.0 * h_bar_prime + 6.0))
        - 0.20 * math.cos(math.radians(4.0 * h_bar_prime - 63.0))
    )
    delta_theta = 30.0 * math.exp(-(((h_bar_prime - 275.0) / 25.0) ** 2))
    c_bar_prime_7 = c_bar_prime**7
    r_c = 2.0 * math.sqrt(
        c_bar_prime_7 / (c_bar_prime_7 + 25.0**7)
    )
    s_l = 1.0 + (0.015 * ((l_bar_prime - 50.0) ** 2)) / math.sqrt(
        20.0 + ((l_bar_prime - 50.0) ** 2)
    )
    s_c = 1.0 + 0.045 * c_bar_prime
    s_h = 1.0 + 0.015 * c_bar_prime * t
    r_t = -math.sin(math.radians(2.0 * delta_theta)) * r_c

    l_term = delta_l_prime / s_l
    c_term = delta_c_prime / s_c
    h_term = delta_big_h_prime / s_h
    return math.sqrt(
        l_term**2 + c_term**2 + h_term**2 + r_t * c_term * h_term
    )


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot summarize an empty sample")
    position = fraction * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _sample_pixels(image: Image.Image, max_samples: int) -> list[tuple[int, int, int]]:
    width, height = image.size
    pixel_count = width * height
    if pixel_count <= max_samples:
        return list(image.getdata())
    scale = math.sqrt(max_samples / pixel_count)
    sampled = image.resize(
        (max(1, round(width * scale)), max(1, round(height * scale))),
        Image.Resampling.BOX,
    )
    return list(sampled.getdata())


def _round_triplet(values: Iterable[float], digits: int = 3) -> list[float]:
    return [round(float(value), digits) for value in values]


def _quartiles(values: list[float]) -> dict[str, float]:
    return {
        "p25": round(_percentile(values, 0.25), 3),
        "p50": round(_percentile(values, 0.50), 3),
        "p75": round(_percentile(values, 0.75), 3),
    }


def _weighted_hue_statistics(
    a_values: list[float], b_values: list[float]
) -> dict[str, float | None]:
    weights = [math.hypot(a_value, b_value) for a_value, b_value in zip(a_values, b_values)]
    total_weight = sum(weights)
    if total_weight == 0.0:
        return {"weighted_mean_degrees": None, "concentration": 0.0}
    x = sum(
        weight * math.cos(math.atan2(b_value, a_value))
        for a_value, b_value, weight in zip(a_values, b_values, weights)
    )
    y = sum(
        weight * math.sin(math.atan2(b_value, a_value))
        for a_value, b_value, weight in zip(a_values, b_values, weights)
    )
    mean = math.degrees(math.atan2(y, x)) % 360.0
    return {
        "weighted_mean_degrees": round(mean, 3),
        "concentration": round(math.hypot(x, y) / total_weight, 6),
    }


def _summarize_region(
    image: Image.Image,
    region: RegionSpec,
    max_samples: int,
) -> dict[str, Any]:
    width, height = image.size
    x0, y0, x1, y1 = region.bounds
    pixel_bounds = (
        math.floor(x0 * width),
        math.floor(y0 * height),
        math.ceil(x1 * width),
        math.ceil(y1 * height),
    )
    crop = image.crop(pixel_bounds)
    pixels = _sample_pixels(crop, max_samples)
    labs = [srgb_to_lab(pixel) for pixel in pixels]

    rgb_median = tuple(statistics.median(pixel[channel] for pixel in pixels) for channel in range(3))
    l_values = [lab[0] for lab in labs]
    a_values = [lab[1] for lab in labs]
    b_values = [lab[2] for lab in labs]
    chroma_values = [math.hypot(lab[1], lab[2]) for lab in labs]
    lab_median = (
        statistics.median(l_values),
        statistics.median(a_values),
        statistics.median(b_values),
    )
    chroma = math.hypot(lab_median[1], lab_median[2])
    hue = math.degrees(math.atan2(lab_median[2], lab_median[1])) % 360.0

    return {
        "name": region.name,
        "semantic_role": region.semantic_role or None,
        "tone_zone": region.tone_zone or None,
        "purpose": region.purpose or None,
        "normalized_bounds": _round_triplet(region.bounds, 6),
        "pixel_bounds": list(pixel_bounds),
        "sample_count": len(pixels),
        "median": {
            "srgb": _round_triplet(rgb_median, 2),
            "lab_d65": _round_triplet(lab_median, 3),
            "chroma": round(chroma, 3),
            "hue_degrees": round(hue, 3),
        },
        "iqr": {
            "lightness": round(_percentile(l_values, 0.75) - _percentile(l_values, 0.25), 3),
            "a": round(_percentile(a_values, 0.75) - _percentile(a_values, 0.25), 3),
            "b": round(_percentile(b_values, 0.75) - _percentile(b_values, 0.25), 3),
            "chroma": round(
                _percentile(chroma_values, 0.75)
                - _percentile(chroma_values, 0.25),
                3,
            ),
        },
        "quantiles": {
            "lightness": _quartiles(l_values),
            "a": _quartiles(a_values),
            "b": _quartiles(b_values),
            "chroma": _quartiles(chroma_values),
        },
        "hue_statistics": _weighted_hue_statistics(a_values, b_values),
    }


def analyze_image(
    path: Path,
    regions: list[RegionSpec],
    max_samples: int = MAX_DEFAULT_SAMPLES,
) -> dict[str, Any]:
    if max_samples < 1:
        raise ValueError("max_samples must be positive")
    if not regions:
        raise ValueError("at least one manually selected region is required")
    names = [region.name for region in regions]
    if len(set(names)) != len(names):
        raise ValueError("region names must be unique")

    image, profile_status, warnings = _load_srgb(path)
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size": {"width": image.width, "height": image.height},
        "profile_status": profile_status,
        "warnings": warnings,
        "regions": [
            _summarize_region(image, region, max_samples) for region in regions
        ],
    }


def _hue_delta(target: float, source: float) -> float:
    return (target - source + 180.0) % 360.0 - 180.0


def compare_reports(source: dict[str, Any], target: dict[str, Any]) -> list[dict[str, Any]]:
    source_regions = {region["name"]: region for region in source["regions"]}
    target_regions = {region["name"]: region for region in target["regions"]}
    if set(source_regions) != set(target_regions):
        raise ValueError("source and comparison reports must use matching region names")

    comparisons: list[dict[str, Any]] = []
    for name in sorted(source_regions):
        source_median = source_regions[name]["median"]
        target_median = target_regions[name]["median"]
        source_lab = source_median["lab_d65"]
        target_lab = target_median["lab_d65"]
        delta_lab = [target_lab[index] - source_lab[index] for index in range(3)]
        comparisons.append(
            {
                "name": name,
                "target_minus_source": {
                    "lab_d65": _round_triplet(delta_lab, 3),
                    "delta_e76": round(math.sqrt(sum(value * value for value in delta_lab)), 3),
                    "delta_e2000": round(delta_e2000(source_lab, target_lab), 3),
                    "chroma": round(
                        target_median["chroma"] - source_median["chroma"], 3
                    ),
                    "hue_degrees": round(
                        _hue_delta(
                            target_median["hue_degrees"],
                            source_median["hue_degrees"],
                        ),
                        3,
                    ),
                },
            }
        )
    return comparisons


def summarize_groups(
    report: dict[str, Any], groups: list[GroupSpec]
) -> list[dict[str, Any]]:
    """Summarize analyst-selected groups with equal weight per region median."""

    group_names = [group.name for group in groups]
    if len(set(group_names)) != len(group_names):
        raise ValueError("group names must be unique")
    region_map = {region["name"]: region for region in report["regions"]}

    summaries: list[dict[str, Any]] = []
    for group in groups:
        unknown = sorted(set(group.region_names) - set(region_map))
        if unknown:
            raise ValueError(
                f"group {group.name!r} references unknown regions: {', '.join(unknown)}"
            )
        medians = [region_map[name]["median"] for name in group.region_names]
        lab_median = tuple(
            statistics.median(median["lab_d65"][axis] for median in medians)
            for axis in range(3)
        )
        chroma = math.hypot(lab_median[1], lab_median[2])
        hue = math.degrees(math.atan2(lab_median[2], lab_median[1])) % 360.0
        lightness_values = [median["lab_d65"][0] for median in medians]
        chroma_values = [median["chroma"] for median in medians]
        summaries.append(
            {
                "name": group.name,
                "region_names": list(group.region_names),
                "region_count": len(group.region_names),
                "semantic_role": group.semantic_role or None,
                "tone_zone": group.tone_zone or None,
                "purpose": group.purpose or None,
                "equal_region_median": {
                    "lab_d65": _round_triplet(lab_median, 3),
                    "chroma": round(chroma, 3),
                    "hue_degrees": round(hue, 3),
                },
                "region_median_ranges": {
                    "lightness": _round_triplet(
                        (min(lightness_values), max(lightness_values)), 3
                    ),
                    "a": _round_triplet(
                        (
                            min(median["lab_d65"][1] for median in medians),
                            max(median["lab_d65"][1] for median in medians),
                        ),
                        3,
                    ),
                    "b": _round_triplet(
                        (
                            min(median["lab_d65"][2] for median in medians),
                            max(median["lab_d65"][2] for median in medians),
                        ),
                        3,
                    ),
                    "chroma": _round_triplet(
                        (min(chroma_values), max(chroma_values)), 3
                    ),
                },
            }
        )
    return summaries


def compare_group_reports(
    source_groups: list[dict[str, Any]],
    target_groups: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Compare matching equal-region group summaries."""

    source_map = {group["name"]: group for group in source_groups}
    target_map = {group["name"]: group for group in target_groups}
    if set(source_map) != set(target_map):
        raise ValueError("source and comparison reports must use matching group names")

    comparisons: list[dict[str, Any]] = []
    for name in sorted(source_map):
        source_group = source_map[name]
        target_group = target_map[name]
        if set(source_group["region_names"]) != set(target_group["region_names"]):
            raise ValueError(f"group {name!r} must use matching region names")
        for field in ("semantic_role", "tone_zone", "purpose"):
            if source_group.get(field) != target_group.get(field):
                raise ValueError(f"group {name!r} must use matching {field}")
        source_median = source_group["equal_region_median"]
        target_median = target_group["equal_region_median"]
        source_lab = source_median["lab_d65"]
        target_lab = target_median["lab_d65"]
        delta_lab = [target_lab[index] - source_lab[index] for index in range(3)]
        comparisons.append(
            {
                "name": name,
                "region_names": source_group["region_names"],
                "semantic_role": source_group.get("semantic_role"),
                "tone_zone": source_group.get("tone_zone"),
                "purpose": source_group.get("purpose"),
                "target_minus_source": {
                    "lab_d65": _round_triplet(delta_lab, 3),
                    "delta_e76": round(
                        math.sqrt(sum(value * value for value in delta_lab)), 3
                    ),
                    "delta_e2000": round(delta_e2000(source_lab, target_lab), 3),
                    "chroma": round(
                        target_median["chroma"] - source_median["chroma"], 3
                    ),
                    "hue_degrees": round(
                        _hue_delta(
                            target_median["hue_degrees"],
                            source_median["hue_degrees"],
                        ),
                        3,
                    ),
                },
            }
        )
    return comparisons


def comparison_context(
    source: dict[str, Any], target: dict[str, Any]
) -> dict[str, str]:
    """State the strongest color interpretation supported by profile evidence."""

    statuses = {source.get("profile_status"), target.get("profile_status")}
    if statuses == {"embedded-profile-converted-to-srgb"}:
        return {
            "scope": "color-managed-relative",
            "limitation": (
                "relative displayed-color comparison after converting both embedded profiles; "
                "scene-referred or material true color remains unsupported"
            ),
        }
    return {
        "scope": "assumed-display-space-relative",
        "limitation": (
            "relative displayed-color comparison with missing or failed profile evidence; "
            "absolute scene-referred, material, or biological color is unsupported"
        ),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Probe manually selected normalized image regions for color evidence."
    )
    parser.add_argument("image", help="source image path")
    parser.add_argument(
        "--region",
        action="append",
        default=[],
        help="NAME=X0,Y0,X1,Y1 using normalized coordinates; repeat as needed",
    )
    parser.add_argument(
        "--spec",
        default="",
        help="optional JSON sampling spec with source/comparison bounds and group metadata",
    )
    parser.add_argument("--compare", default="", help="optional comparison image")
    parser.add_argument(
        "--compare-region",
        action="append",
        default=[],
        help="optional comparison bounds using matching region names; defaults to source bounds",
    )
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        help="NAME=REGION_A,REGION_B; repeat for analyst-named equal-weight groups",
    )
    parser.add_argument("--max-samples", type=int, default=MAX_DEFAULT_SAMPLES)
    args = parser.parse_args(argv)

    try:
        if args.spec and (args.region or args.compare_region or args.group):
            raise ValueError(
                "--spec cannot be combined with --region, --compare-region, or --group"
            )
        sampling_spec_record: dict[str, str] | None = None
        if args.spec:
            spec_path = Path(args.spec)
            source_regions, compare_regions, groups = load_sampling_spec(spec_path)
            sampling_spec_record = {
                "path": str(spec_path.resolve()),
                "sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
            }
        else:
            if not args.region:
                raise ValueError("provide at least one --region or a --spec")
            source_regions = [parse_region(raw) for raw in args.region]
            compare_regions = (
                [parse_region(raw) for raw in args.compare_region]
                if args.compare_region
                else source_regions
            )
            groups = [parse_group(raw) for raw in args.group]
        source = analyze_image(Path(args.image), source_regions, args.max_samples)
        source_groups = summarize_groups(source, groups) if groups else []
        if source_groups:
            source["groups"] = source_groups
        payload: dict[str, Any] = {"source": source}
        if sampling_spec_record:
            payload["sampling_spec"] = sampling_spec_record
        if args.compare:
            target = analyze_image(Path(args.compare), compare_regions, args.max_samples)
            payload["comparison"] = target
            payload["deltas"] = compare_reports(source, target)
            payload["comparison_context"] = comparison_context(source, target)
            if groups:
                target_groups = summarize_groups(target, groups)
                target["groups"] = target_groups
                payload["group_deltas"] = compare_group_reports(
                    source_groups, target_groups
                )
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1

    print(json.dumps({"status": "ok", **payload}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
