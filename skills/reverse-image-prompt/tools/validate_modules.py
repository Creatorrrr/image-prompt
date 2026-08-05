#!/usr/bin/env python3
"""Validate the modular reverse-image-prompt skill package."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from anchor_catalog import ANCHORS
from module_metadata import ROOT, build_manifest, module_files, module_map, parse_frontmatter, registry_markdown

MANIFEST = ROOT / "manifest.json"
REGISTRY = ROOT / "modules" / "_registry.md"
REQUIRED_HEADINGS = ("## When to load",)
VALID_TYPES = {"core", "concept", "subject", "detail", "medium", "style"}
VALID_FACETS = {"core", "relationship", "subject", "medium", "detail-risk", "style"}
MAX_MODULE_WORDS = 1200
MAX_MODULE_LINES = 160
MAX_TOTAL_MODULE_WORDS = 15000
MAX_CORE_WORDS = 3500
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
