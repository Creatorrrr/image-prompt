#!/usr/bin/env python3
"""Check invariant ownership for compiled bundles and routed module paths."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from anchor_catalog import ANCHORS, CORE_ANCHOR_IDS, REQUIRED_ANCHOR_IDS
from module_metadata import ROOT, load_manifest, module_map
from route_resolver import load_scenarios, resolve_modules


def provided_anchors(module_ids: list[str], manifest: dict) -> set[str]:
    modules = module_map(manifest)
    out: set[str] = set()
    for module_id in module_ids:
        out.update(modules[module_id].get("provides_anchors", []))
    return out


def check_compiled(compiled_path: Path) -> int:
    compiled = compiled_path.read_text(encoding="utf-8")
    missing: list[tuple[str, str]] = []
    for anchor_id in REQUIRED_ANCHOR_IDS:
        anchor = ANCHORS[anchor_id]
        if anchor not in compiled:
            missing.append((anchor_id, anchor))

    if missing:
        print("COMPILED COVERAGE FAILED")
        for anchor_id, anchor in missing:
            print(f"- {anchor_id}: {anchor}")
        return 1
    print(f"COMPILED REQUIRED COVERAGE OK: {len(REQUIRED_ANCHOR_IDS)} anchors present")
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
            expected_error = scenario.get("expect_error_contains")
            if expected_error and str(expected_error) in str(exc):
                continue
            failures.append(f"{sid}: resolver error: {exc}")
            continue
        if scenario.get("expect_error_contains"):
            failures.append(f"{sid}: expected resolver error containing {scenario['expect_error_contains']!r}")
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
    parser.add_argument("--legacy", default="", help="deprecated compatibility argument; no longer inspected")
    parser.add_argument("--compiled", default="")
    parser.add_argument("--scenario-matrix", default="")
    args = parser.parse_args(argv)

    status = 0
    if args.compiled:
        status = max(status, check_compiled(Path(args.compiled)))
    elif args.legacy:
        parser.error("--legacy is deprecated and only accepted alongside --compiled")
    if args.scenario_matrix:
        status = max(status, check_scenario_matrix(Path(args.scenario_matrix)))
    if not (args.compiled or args.scenario_matrix):
        parser.error("provide --compiled and/or --scenario-matrix")
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
