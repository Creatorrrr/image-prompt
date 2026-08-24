#!/usr/bin/env python3
"""Resolve reverse-image-prompt modules from detected facets or fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from module_metadata import (
    ROOT,
    expand_dependencies,
    load_manifest,
    module_map,
    module_sort_key,
    resolve_analysis_lanes,
)

FACET_KEY_ALIASES = {
    "subject": "subject",
    "subjects": "subject",
    "primary-subjects": "subject",
    "medium": "medium",
    "media": "medium",
    "relationship": "relationship",
    "relationships": "relationship",
    "concept": "relationship",
    "concepts": "relationship",
    "capture-quality": "capture-quality",
    "capture-qualities": "capture-quality",
    "detail-risk": "detail-risk",
    "detail-risks": "detail-risk",
    "style": "style",
    "styles": "style",
}

VALUE_ALIASES = {
    "detail-risk": {
        "ui": "ui-text",
        "small-prop": "small-props",
        "cropped-edge": "cropped-edges",
    },
    "medium": {
        "photo-like": "photographic",
    },
}

CORE_HANDLED_VALUES = {
    "relationship": {"ordinary"},
    "detail-risk": {"small-props", "cropped-edges"},
}

CAPTURE_QUALITY_TARGET_FACETS = {"medium", "detail-risk"}
CAPTURE_QUALITY_VALUES = {
    "low-quality",
    "compressed",
    "underexposed",
    "motion-blurred",
    "noise",
    "haze",
    "soft-focus",
    "low-resolution",
    "flash",
    "casual-phone",
    "low-light-photo",
}
MANDATORY_FALLBACKS = {
    "medium": "medium.unspecified-visual",
    "subject": "subject.generic-object",
}
MAX_NON_CORE_MODULES = 8


def norm(value: Any) -> str:
    normalized = str(value).strip().lower().replace("_", "-")
    return re.sub(r"[\s-]+", "-", normalized)


def normalize_facets(facets: dict[str, Any]) -> dict[str, set[str]]:
    normalized: dict[str, set[str]] = {}
    for raw_key, raw_values in facets.items():
        normalized_key = norm(raw_key)
        key = FACET_KEY_ALIASES.get(normalized_key, normalized_key)
        if raw_values is None:
            values: list[Any] = []
        elif isinstance(raw_values, list):
            values = raw_values
        else:
            values = [raw_values]
        aliases = VALUE_ALIASES.get(key, {})
        for raw_value in values:
            value = norm(raw_value)
            if value:
                normalized.setdefault(key, set()).add(aliases.get(value, value))
    return normalized


def allowed_values(manifest: dict[str, Any]) -> dict[str, set[str]]:
    allowed: dict[str, set[str]] = {}
    for module in manifest.get("modules", []):
        facet = str(module.get("facet", ""))
        allowed.setdefault(facet, set()).update(norm(v) for v in module.get("facet_values", []))
    for facet, values in CORE_HANDLED_VALUES.items():
        allowed.setdefault(facet, set()).update(values)
    allowed["capture-quality"] = set(CAPTURE_QUALITY_VALUES)
    return allowed


def validate_requested_facets(facet_values: dict[str, set[str]], manifest: dict[str, Any]) -> None:
    allowed = allowed_values(manifest)
    errors: list[str] = []
    for facet, requested in sorted(facet_values.items()):
        if facet not in allowed:
            errors.append(f"unknown facet '{facet}'")
            continue
        unknown = sorted(requested - allowed[facet])
        if unknown:
            errors.append(f"unmapped {facet} value(s): {', '.join(unknown)}")
    if errors:
        raise ValueError("; ".join(errors))


def requested_for_module(facet: str, facet_values: dict[str, set[str]]) -> set[str]:
    requested = set(facet_values.get(facet, set()))
    if facet in CAPTURE_QUALITY_TARGET_FACETS:
        requested.update(facet_values.get("capture-quality", set()))
    return requested


def selected_has_facet(module_ids: set[str], manifest: dict[str, Any], facet: str) -> bool:
    modules = module_map(manifest)
    return any(modules[mid].get("facet") == facet for mid in module_ids if mid in modules)


def resolve_modules(facets: dict[str, Any], manifest: dict[str, Any] | None = None) -> list[str]:
    manifest = manifest or load_manifest(ROOT)
    modules = module_map(manifest)
    facet_values = normalize_facets(facets)
    validate_requested_facets(facet_values, manifest)

    selected: set[str] = set(manifest.get("required_core_modules", []))

    for module in manifest.get("modules", []):
        if int(module.get("tier", 99)) == 0:
            continue
        facet = str(module.get("facet", ""))
        requested = requested_for_module(facet, facet_values)
        values = {norm(v) for v in module.get("facet_values", [])}
        if requested.intersection(values):
            selected.add(module["id"])

    for facet, fallback_id in MANDATORY_FALLBACKS.items():
        if not selected_has_facet(selected, manifest, facet):
            selected.add(fallback_id)

    expanded = expand_dependencies(list(selected), manifest)
    expanded_set = set(expanded)
    conflicts: set[tuple[str, str]] = set()
    for module_id in expanded:
        for conflict in modules[module_id].get("conflicts", []):
            if conflict in expanded_set:
                conflicts.add(tuple(sorted((module_id, conflict))))
    if conflicts:
        rendered = ", ".join(f"{a} conflicts with {b}" for a, b in sorted(conflicts))
        raise ValueError(f"module conflict: {rendered}")

    non_core = [mid for mid in expanded if int(modules[mid].get("tier", 99)) != 0]
    if len(non_core) > MAX_NON_CORE_MODULES:
        raise ValueError(
            f"module budget exceeded: {len(non_core)} non-core modules selected "
            f"(maximum {MAX_NON_CORE_MODULES}); refine the facet map"
        )

    return [m["id"] for m in sorted((modules[mid] for mid in expanded), key=module_sort_key)]


def _canonical_facets(facets: dict[str, Any]) -> dict[str, list[str]]:
    return {
        key: sorted(values)
        for key, values in sorted(normalize_facets(facets).items())
        if values
    }


def analysis_route_fingerprint(route_without_fingerprint: dict[str, Any]) -> str:
    encoded = json.dumps(
        route_without_fingerprint,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def resolve_analysis_route(
    facets: dict[str, Any], manifest: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Resolve modules, then assign a compact set of independent analysis lanes."""

    manifest = manifest or load_manifest(ROOT)
    resolved_modules = resolve_modules(facets, manifest)
    lane_entries = resolve_analysis_lanes(resolved_modules, manifest)
    covered_non_core = {
        module_id
        for lane in lane_entries
        for module_id in lane.get("module_ids", [])
        if module_id not in manifest.get("required_core_modules", [])
    }
    modules = module_map(manifest)
    required_non_core = {
        module_id
        for module_id in resolved_modules
        if int(modules[module_id].get("tier", 99)) != 0
    }
    missing = sorted(required_non_core - covered_non_core)
    if missing:
        raise ValueError(
            "analysis lane coverage missing for routed module(s): " + ", ".join(missing)
        )

    lanes = [
        {
            "id": lane["id"],
            "version": lane["version"],
            "instruction_file": lane["file"],
            "module_ids": lane["module_ids"],
            "owns_sections": lane["owns_sections"],
            "required_topics": lane["required_topics"],
        }
        for lane in lane_entries
    ]
    route = {
        "schema_version": "reverse-image-analysis-route/v1",
        "normalized_facets": _canonical_facets(facets),
        "resolved_modules": resolved_modules,
        "required_lane_ids": [lane["id"] for lane in lanes],
        "lanes": lanes,
    }
    return {**route, "route_fingerprint": analysis_route_fingerprint(route)}


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.get("scenarios", []))
    if isinstance(data, list):
        return data
    raise ValueError("scenario file must contain a JSON-compatible YAML object or list")


def check_scenarios(path: Path, manifest: dict[str, Any]) -> int:
    scenarios = load_scenarios(path)
    failures: list[str] = []
    results: list[dict[str, Any]] = []
    module_meta = module_map(manifest)

    for scenario in scenarios:
        sid = scenario.get("id", "<unnamed>")
        try:
            resolved = resolve_modules(scenario.get("facets", {}), manifest)
        except Exception as exc:  # noqa: BLE001 - CLI should show fixture failure plainly.
            expected_error = scenario.get("expect_error_contains")
            if expected_error and str(expected_error) in str(exc):
                results.append({"id": sid, "expected_error": str(exc)})
                continue
            failures.append(f"{sid}: resolver error: {exc}")
            continue

        if scenario.get("expect_error_contains"):
            failures.append(f"{sid}: expected resolver error containing {scenario['expect_error_contains']!r}")
            continue

        module_set = set(resolved)
        missing = [mid for mid in scenario.get("expect_includes", []) if mid not in module_set]
        unexpected = [mid for mid in scenario.get("expect_excludes", []) if mid in module_set]
        if missing:
            failures.append(f"{sid}: missing expected modules: {', '.join(missing)}")
        if unexpected:
            failures.append(f"{sid}: unexpected modules: {', '.join(unexpected)}")

        non_core_count = sum(int(module_meta[mid].get("tier", 99)) != 0 for mid in resolved)
        maximum = int(scenario.get("max_non_core_modules", MAX_NON_CORE_MODULES))
        if non_core_count > maximum:
            failures.append(f"{sid}: selected {non_core_count} non-core modules, maximum is {maximum}")

        results.append({"id": sid, "non_core_count": non_core_count, "modules": resolved})

    if failures:
        print("ROUTING FAILED")
        for failure in failures:
            print(f"- {failure}")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps({"status": "ok", "scenario_count": len(scenarios), "results": results}, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--facets", default="", help="JSON object containing detected facets")
    parser.add_argument("--scenarios", default="", help="JSON-compatible YAML scenario fixture")
    parser.add_argument(
        "--analysis-route",
        action="store_true",
        help="include the deterministic distributed-analysis lane route",
    )
    args = parser.parse_args(argv)

    manifest = load_manifest(ROOT)
    if args.scenarios:
        return check_scenarios(Path(args.scenarios), manifest)
    if args.facets:
        facets = json.loads(args.facets)
        if args.analysis_route:
            print(
                json.dumps(
                    resolve_analysis_route(facets, manifest),
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0
        resolved = resolve_modules(facets, manifest)
        modules = module_map(manifest)
        non_core_count = sum(int(modules[mid].get("tier", 99)) != 0 for mid in resolved)
        print(json.dumps({"non_core_count": non_core_count, "modules": resolved}, indent=2, ensure_ascii=False))
        return 0
    parser.error("provide --facets or --scenarios")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
