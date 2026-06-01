#!/usr/bin/env python3
"""Resolve reverse-image-prompt modules from detected facets or scenario fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from module_metadata import ROOT, expand_dependencies, load_manifest, module_map, module_sort_key

FACET_KEY_ALIASES = {
    "subject": "subject",
    "subjects": "subject",
    "primary_subjects": "subject",
    "primary-subjects": "subject",
    "medium": "medium",
    "media": "medium",
    "relationship": "relationship",
    "relationships": "relationship",
    "concept": "relationship",
    "concepts": "relationship",
    "capture_quality": "detail-risk",
    "capture_qualities": "detail-risk",
    "capture-quality": "detail-risk",
    "capture-qualities": "detail-risk",
    "detail_risk": "detail-risk",
    "detail_risks": "detail-risk",
    "detail-risk": "detail-risk",
    "detail-risks": "detail-risk",
    "style": "style",
    "styles": "style",
}

MANDATORY_FALLBACKS = {
    "medium": "medium.unspecified-visual",
    "subject": "subject.generic-object",
}


def norm(value: Any) -> str:
    return str(value).strip().lower().replace("_", "-")


def normalize_facets(facets: dict[str, Any]) -> dict[str, set[str]]:
    normalized: dict[str, set[str]] = {}
    for raw_key, raw_values in facets.items():
        key = FACET_KEY_ALIASES.get(norm(raw_key), norm(raw_key))
        if raw_values is None:
            values: list[Any] = []
        elif isinstance(raw_values, list):
            values = raw_values
        else:
            values = [raw_values]
        normalized.setdefault(key, set()).update(norm(v) for v in values if str(v).strip())
    return normalized


def selected_has_facet(module_ids: set[str], manifest: dict[str, Any], facet: str) -> bool:
    modules = module_map(manifest)
    return any(modules[mid].get("facet") == facet for mid in module_ids if mid in modules)


def resolve_modules(facets: dict[str, Any], manifest: dict[str, Any] | None = None) -> list[str]:
    manifest = manifest or load_manifest(ROOT)
    modules = module_map(manifest)
    facet_values = normalize_facets(facets)

    selected: set[str] = set(manifest.get("required_core_modules", []))

    for module in manifest.get("modules", []):
        if int(module.get("tier", 99)) == 0:
            continue
        facet = module.get("facet")
        requested = facet_values.get(facet, set())
        values = {norm(v) for v in module.get("facet_values", [])}
        if requested and values.intersection(requested):
            selected.add(module["id"])

    for facet, fallback_id in MANDATORY_FALLBACKS.items():
        if not selected_has_facet(selected, manifest, facet):
            selected.add(fallback_id)

    expanded = expand_dependencies(list(selected), manifest)
    expanded_set = set(expanded)
    conflicts: list[tuple[str, str]] = []
    for module_id in expanded:
        for conflict in modules[module_id].get("conflicts", []):
            if conflict in expanded_set:
                conflicts.append((module_id, conflict))
    if conflicts:
        rendered = ", ".join(f"{a} conflicts with {b}" for a, b in sorted(conflicts))
        raise ValueError(f"module conflict: {rendered}")

    return [m["id"] for m in sorted((modules[mid] for mid in expanded), key=module_sort_key)]


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
    for scenario in scenarios:
        sid = scenario.get("id", "<unnamed>")
        try:
            modules = resolve_modules(scenario.get("facets", {}), manifest)
        except Exception as exc:  # noqa: BLE001 - CLI should show fixture failure plainly.
            failures.append(f"{sid}: resolver error: {exc}")
            continue
        module_set = set(modules)
        missing = [mid for mid in scenario.get("expect_includes", []) if mid not in module_set]
        unexpected = [mid for mid in scenario.get("expect_excludes", []) if mid in module_set]
        if missing:
            failures.append(f"{sid}: missing expected modules: {', '.join(missing)}")
        if unexpected:
            failures.append(f"{sid}: unexpected modules: {', '.join(unexpected)}")
        results.append({"id": sid, "modules": modules})

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
    args = parser.parse_args(argv)

    manifest = load_manifest(ROOT)
    if args.scenarios:
        return check_scenarios(Path(args.scenarios), manifest)
    if args.facets:
        modules = resolve_modules(json.loads(args.facets), manifest)
        print(json.dumps({"modules": modules}, indent=2, ensure_ascii=False))
        return 0
    parser.error("provide --facets or --scenarios")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
