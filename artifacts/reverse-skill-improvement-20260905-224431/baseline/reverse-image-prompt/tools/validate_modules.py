#!/usr/bin/env python3
"""Validate the modular reverse-image-prompt skill package."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from anchor_catalog import ANCHORS
from module_metadata import (
    ROOT,
    build_manifest,
    lane_files,
    lane_matches_module,
    module_files,
    module_map,
    parse_frontmatter,
    registry_markdown,
)

MANIFEST = ROOT / "manifest.json"
REGISTRY = ROOT / "modules" / "_registry.md"
REQUIRED_HEADINGS = ("## When to load",)
VALID_TYPES = {"core", "concept", "subject", "detail", "medium", "style"}
VALID_FACETS = {"core", "relationship", "subject", "medium", "detail-risk", "style"}
MAX_MODULE_WORDS = 1200
MAX_MODULE_LINES = 160
MAX_TOTAL_MODULE_WORDS = 17000
MAX_CORE_WORDS = 3800
MAX_DUPLICATE_LINE_RATIO = 0.10
PROHIBITED_RUNTIME_TEXT = (
    "Legacy monolith fidelity rules preserved verbatim",
    "Fill every field with source-specific values",
    "Do not compress or summarize the output contract",
    "include a dedicated coordinate-lock passage",
)
REQUIRED_FIELDS = (
    "id",
    "version",
    "priority",
    "type",
    "tier",
    "facet",
    "facet_values",
    "triggers",
    "avoid_when",
    "dependencies",
    "conflicts",
    "provides_anchors",
)
LANE_REQUIRED_FIELDS = (
    "id",
    "version",
    "priority",
    "activation",
    "select_types",
    "select_facets",
    "select_module_ids",
    "required_common_modules",
    "owns_sections",
    "required_topics",
)
LANE_REQUIRED_HEADINGS = (
    "## Role",
    "## Input boundary",
    "## Output contract",
    "## Completion gate",
)
VALID_LANE_ACTIVATIONS = {"always", "matched"}
MAX_LANE_WORDS = 350


def main() -> int:
    errors: list[str] = []
    total_module_words = 0
    core_words = 0
    runtime_lines: list[str] = []
    if not MANIFEST.exists():
        errors.append(f"missing manifest: {MANIFEST}")
        print_errors(errors)
        return 1

    generated_manifest = build_manifest(ROOT)
    generated_registry = registry_markdown(generated_manifest)
    try:
        current_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"manifest json parse error: {exc}")
        current_manifest = {}

    if current_manifest and current_manifest != generated_manifest:
        errors.append("manifest.json is not generated from current module frontmatter")
    if not REGISTRY.exists():
        errors.append(f"missing registry: {REGISTRY}")
    elif REGISTRY.read_text(encoding="utf-8") != generated_registry:
        errors.append("modules/_registry.md is not generated from current module frontmatter")

    manifest = generated_manifest
    modules = manifest.get("modules", [])
    id_set = {m["id"] for m in modules}
    if len(id_set) != len(modules):
        errors.append("duplicate module id in generated manifest")
    orchestration = manifest.get("analysis_orchestration")
    if not isinstance(orchestration, dict):
        errors.append("manifest analysis_orchestration must be an object")
    else:
        reference = orchestration.get("reference")
        if not isinstance(reference, str) or not (ROOT / reference).is_file():
            errors.append("analysis orchestration reference is missing")

    for core in manifest.get("required_core_modules", []):
        module = module_map(manifest).get(core)
        if not module:
            errors.append(f"required core module missing: {core}")
        elif int(module.get("tier", -1)) != 0:
            errors.append(f"required core module is not tier 0: {core}")

    for path in module_files(ROOT):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        try:
            fm, body = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        mid = fm.get("id", "")
        if path.stem != mid:
            errors.append(f"module filename/id mismatch: {rel} has id {mid}")
        for field in REQUIRED_FIELDS:
            if field not in fm:
                errors.append(f"frontmatter field missing in {rel}: {field}")
        if fm.get("type") not in VALID_TYPES:
            errors.append(f"unknown type for {rel}: {fm.get('type')}")
        if fm.get("facet") not in VALID_FACETS:
            errors.append(f"unknown facet for {rel}: {fm.get('facet')}")
        if not isinstance(fm.get("priority"), int):
            errors.append(f"priority missing/not numeric: {rel}")
        if not isinstance(fm.get("version"), int) or int(fm.get("version", 0)) < 1:
            errors.append(f"version missing/not positive numeric: {rel}")
        if not isinstance(fm.get("tier"), int) or int(fm.get("tier", -1)) not in {0, 1, 2, 3, 4}:
            errors.append(f"tier missing/not in 0..4: {rel}")
        if not fm.get("facet_values"):
            errors.append(f"facet_values missing/empty: {rel}")
        if not fm.get("triggers"):
            errors.append(f"triggers missing/empty: {rel}")
        for heading in REQUIRED_HEADINGS:
            if heading not in body:
                errors.append(f"required heading absent in {rel}: {heading}")
        word_count = len(body.split())
        line_count = len(body.splitlines())
        total_module_words += word_count
        if int(fm.get("tier", -1)) == 0:
            core_words += word_count
        runtime_lines.extend(
            line.strip()
            for line in body.splitlines()
            if len(line.strip()) >= 30 and not line.lstrip().startswith("#")
        )
        if word_count > MAX_MODULE_WORDS:
            errors.append(f"module body too large in {rel}: {word_count} words > {MAX_MODULE_WORDS}")
        if line_count > MAX_MODULE_LINES:
            errors.append(f"module body too long in {rel}: {line_count} lines > {MAX_MODULE_LINES}")
        for prohibited in PROHIBITED_RUNTIME_TEXT:
            if prohibited in text:
                errors.append(f"prohibited runtime text in {rel}: {prohibited}")

        for dep in fm.get("dependencies", []):
            if dep not in id_set:
                errors.append(f"unknown dependency in {mid}: {dep}")
        for conflict in fm.get("conflicts", []):
            if conflict not in id_set:
                errors.append(f"unknown conflict in {mid}: {conflict}")
        for anchor_id in fm.get("provides_anchors", []):
            anchor_text = ANCHORS.get(anchor_id)
            if anchor_text is None:
                errors.append(f"unknown provided anchor in {mid}: {anchor_id}")
            elif anchor_text not in text:
                errors.append(f"provided anchor text absent in {mid}: {anchor_id}")

    lanes = manifest.get("analysis_lanes", [])
    lane_ids: set[str] = set()
    owned_sections: dict[str, str] = {}
    for path in lane_files(ROOT):
        rel = path.relative_to(ROOT).as_posix()
        try:
            fm, body = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        lane_id = fm.get("id", "")
        if path.stem != lane_id:
            errors.append(f"lane filename/id mismatch: {rel} has id {lane_id}")
        if lane_id in lane_ids:
            errors.append(f"duplicate analysis lane id: {lane_id}")
        lane_ids.add(str(lane_id))
        for field in LANE_REQUIRED_FIELDS:
            if field not in fm:
                errors.append(f"lane frontmatter field missing in {rel}: {field}")
        if fm.get("activation") not in VALID_LANE_ACTIVATIONS:
            errors.append(f"invalid lane activation in {rel}: {fm.get('activation')}")
        if not isinstance(fm.get("version"), int) or int(fm.get("version", 0)) < 1:
            errors.append(f"lane version missing/not positive numeric: {rel}")
        if not isinstance(fm.get("priority"), int):
            errors.append(f"lane priority missing/not numeric: {rel}")
        selectors = (
            list(fm.get("select_types", []))
            + list(fm.get("select_facets", []))
            + list(fm.get("select_module_ids", []))
        )
        if fm.get("activation") == "matched" and not selectors:
            errors.append(f"matched lane has no selector: {rel}")
        unknown_types = sorted(set(fm.get("select_types", [])) - VALID_TYPES)
        unknown_facets = sorted(set(fm.get("select_facets", [])) - VALID_FACETS)
        unknown_module_ids = sorted(set(fm.get("select_module_ids", [])) - id_set)
        unknown_common = sorted(set(fm.get("required_common_modules", [])) - id_set)
        if unknown_types:
            errors.append(f"{rel} selects unknown module types: {', '.join(unknown_types)}")
        if unknown_facets:
            errors.append(f"{rel} selects unknown facets: {', '.join(unknown_facets)}")
        if unknown_module_ids:
            errors.append(f"{rel} selects unknown modules: {', '.join(unknown_module_ids)}")
        if unknown_common:
            errors.append(f"{rel} requires unknown common modules: {', '.join(unknown_common)}")
        sections = fm.get("owns_sections", [])
        topics = fm.get("required_topics", [])
        if not sections or len(sections) != len(set(sections)):
            errors.append(f"{rel}.owns_sections must be non-empty and unique")
        if not topics or len(topics) != len(set(topics)):
            errors.append(f"{rel}.required_topics must be non-empty and unique")
        for section in sections:
            previous = owned_sections.get(section)
            if previous is not None:
                errors.append(
                    f"analysis lane section {section!r} is owned by both {previous} and {lane_id}"
                )
            else:
                owned_sections[section] = str(lane_id)
        for heading in LANE_REQUIRED_HEADINGS:
            if heading not in body:
                errors.append(f"required lane heading absent in {rel}: {heading}")
        if len(body.split()) > MAX_LANE_WORDS:
            errors.append(
                f"analysis lane body too large in {rel}: {len(body.split())} words > {MAX_LANE_WORDS}"
            )

    if not any(lane.get("activation") == "always" for lane in lanes):
        errors.append("at least one analysis lane must always activate")
    for module in modules:
        if int(module.get("tier", 99)) == 0:
            continue
        if not any(lane_matches_module(lane, module) for lane in lanes):
            errors.append(
                f"non-core module is not covered by an analysis lane: {module['id']}"
            )

    if total_module_words > MAX_TOTAL_MODULE_WORDS:
        errors.append(
            f"runtime module corpus too large: {total_module_words} words > {MAX_TOTAL_MODULE_WORDS}"
        )
    if core_words > MAX_CORE_WORDS:
        errors.append(f"tier 0 core too large: {core_words} words > {MAX_CORE_WORDS}")
    if runtime_lines:
        counts = Counter(runtime_lines)
        duplicate_instances = sum(count - 1 for count in counts.values())
        duplicate_ratio = duplicate_instances / len(runtime_lines)
        if duplicate_ratio > MAX_DUPLICATE_LINE_RATIO:
            errors.append(
                "runtime exact-line duplication too high: "
                f"{duplicate_ratio:.1%} > {MAX_DUPLICATE_LINE_RATIO:.1%}"
            )

    if errors:
        print_errors(errors)
        return 1
    print(json.dumps({
        "status": "ok",
        "module_count": len(modules),
        "analysis_lane_count": len(lanes),
        "required_core_modules": manifest.get("required_core_modules", []),
        "runtime_module_words": total_module_words,
        "tier_0_words": core_words,
        "exact_line_duplicate_ratio": round(duplicate_ratio, 4) if runtime_lines else 0,
    }, indent=2, ensure_ascii=False))
    return 0


def print_errors(errors: list[str]) -> None:
    print("VALIDATION FAILED")
    for err in errors:
        print("-", err)


if __name__ == "__main__":
    raise SystemExit(main())
