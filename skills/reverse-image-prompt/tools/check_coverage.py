#!/usr/bin/env python3
"""Check anchor coverage for compiled bundles and routed module paths."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from anchor_catalog import ANCHORS, CORE_ANCHOR_IDS, LEGACY_ANCHOR_IDS
from module_metadata import ROOT, load_manifest, module_map
from route_resolver import load_scenarios, resolve_modules


def provided_anchors(module_ids: list[str], manifest: dict) -> set[str]:
    modules = module_map(manifest)
    out: set[str] = set()
    for module_id in module_ids:
        out.update(modules[module_id].get("provides_anchors", []))
    return out


def check_legacy_compiled(legacy_path: Path, compiled_path: Path) -> int:
    legacy = legacy_path.read_text(encoding="utf-8")
    compiled = compiled_path.read_text(encoding="utf-8")
    missing: list[tuple[str, str]] = []
    absent_from_legacy: list[tuple[str, str]] = []
    for anchor_id in LEGACY_ANCHOR_IDS:
        anchor = ANCHORS[anchor_id]
        if anchor not in legacy:
            absent_from_legacy.append((anchor_id, anchor))
        if anchor not in compiled:
            missing.append((anchor_id, anchor))

    if absent_from_legacy:
        print("COVERAGE CHECK CONFIG ERROR: anchors absent from legacy")
        for anchor_id, anchor in absent_from_legacy:
            print(f"- {anchor_id}: {anchor}")
        return 2
    if missing:
        print("COVERAGE FAILED")
        for anchor_id, anchor in missing:
            print(f"- {anchor_id}: {anchor}")
        return 1
    print(f"LEGACY UNION COVERAGE OK: {len(LEGACY_ANCHOR_IDS)} anchors present")
    return 0


def check_scenario_matrix(path: Path) -> int:
    manifest = load_manifest(ROOT)
    modules = module_map(manifest)
    failures: list[str] = []
    scenarios = load_scenarios(path)
    for scenario in scenarios:
        sid = scenario.get("id", "<unnamed>")
        try:
            module_ids = resolve_modules(scenario.get("facets", {}), manifest)
        except Exception as exc:  # noqa: BLE001 - coverage CLI should report fixture problems directly.
            failures.append(f"{sid}: resolver error: {exc}")
            continue

        have = provided_anchors(module_ids, manifest)
        required = set(CORE_ANCHOR_IDS)
        required.update(scenario.get("required_anchors", []))
        missing = sorted(anchor for anchor in required if anchor not in have)
        if missing:
            failures.append(f"{sid}: missing required anchors: {', '.join(missing)}")

        for module_id in module_ids:
            module = modules[module_id]
            text = (ROOT / module["file"]).read_text(encoding="utf-8")
            for anchor_id in module.get("provides_anchors", []):
                anchor_text = ANCHORS.get(anchor_id)
                if anchor_text is None:
                    failures.append(f"{sid}: {module_id} provides unknown anchor {anchor_id}")
                elif anchor_text not in text:
                    failures.append(f"{sid}: {module_id} missing anchor text for {anchor_id}")

    if failures:
        print("SCENARIO COVERAGE FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"SCENARIO COVERAGE OK: {len(scenarios)} scenarios")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy", default="")
    parser.add_argument("--compiled", default="")
    parser.add_argument("--scenario-matrix", default="")
    args = parser.parse_args(argv)

    status = 0
    if args.legacy or args.compiled:
        if not args.legacy or not args.compiled:
            parser.error("--legacy and --compiled must be provided together")
        status = max(status, check_legacy_compiled(Path(args.legacy), Path(args.compiled)))
    if args.scenario_matrix:
        status = max(status, check_scenario_matrix(Path(args.scenario_matrix)))
    if not (args.legacy or args.compiled or args.scenario_matrix):
        parser.error("provide --legacy/--compiled and/or --scenario-matrix")
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
