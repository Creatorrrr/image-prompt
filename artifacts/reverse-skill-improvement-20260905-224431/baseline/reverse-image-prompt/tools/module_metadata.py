#!/usr/bin/env python3
"""Shared frontmatter and manifest helpers for reverse-image-prompt tools."""

from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "modules"
LANES_DIR = ROOT / "lanes"

TIERS = {
    0: "always-on core",
    1: "concept and relationship",
    2: "subject and medium",
    3: "detail-risk",
    4: "narrow style",
}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + len("\n---\n") :].lstrip()
    return text


def parse_frontmatter_text(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")

    raw = text[4:end]
    body = text[end + len("\n---\n") :].lstrip()
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            if current_key is None:
                raise ValueError(f"list item without key: {line}")
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if line.startswith(" "):
            raise ValueError(f"unsupported frontmatter indentation: {line}")
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        current_key = None
        if value == "":
            data[key] = []
            current_key = key
        elif value == "[]":
            data[key] = []
        elif value.isdigit():
            data[key] = int(value)
        else:
            data[key] = value

    return data, body


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    try:
        return parse_frontmatter_text(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ValueError(f"{path}: {exc}") from exc


def module_files(root: Path = ROOT) -> list[Path]:
    modules_dir = root / "modules"
    return sorted(p for p in modules_dir.glob("*.md") if p.name != "_registry.md")


def lane_files(root: Path = ROOT) -> list[Path]:
    lanes_dir = root / "lanes"
    return sorted(lanes_dir.glob("*.md")) if lanes_dir.exists() else []


def module_sort_key(module: dict[str, Any]) -> tuple[int, int, str]:
    return (
        int(module.get("tier", 99)),
        -int(module.get("priority", 0)),
        str(module.get("id", "")),
    )


def load_manifest(root: Path = ROOT) -> dict[str, Any]:
    return read_json_manifest(root / "manifest.json")


def read_json_manifest(path: Path) -> dict[str, Any]:
    import json

    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def module_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {m["id"]: m for m in manifest.get("modules", [])}


def lane_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {lane["id"]: lane for lane in manifest.get("analysis_lanes", [])}


def lane_matches_module(lane: dict[str, Any], module: dict[str, Any]) -> bool:
    return (
        module.get("type") in set(lane.get("select_types", []))
        or module.get("facet") in set(lane.get("select_facets", []))
        or module.get("id") in set(lane.get("select_module_ids", []))
    )


def resolve_analysis_lanes(
    module_ids: list[str], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    """Return active lane contracts and their exact routed module context."""

    modules = module_map(manifest)
    selected = [modules[module_id] for module_id in module_ids if module_id in modules]
    resolved: list[dict[str, Any]] = []
    for lane in manifest.get("analysis_lanes", []):
        matched_ids = [
            module["id"]
            for module in selected
            if lane_matches_module(lane, module)
            and (
                lane.get("activation") == "always"
                or int(module.get("tier", 99)) != 0
            )
        ]
        if lane.get("activation") != "always" and not matched_ids:
            continue
        context_ids = set(matched_ids)
        context_ids.update(
            module_id
            for module_id in lane.get("required_common_modules", [])
            if module_id in module_ids
        )
        entry = dict(lane)
        entry["module_ids"] = [
            module_id for module_id in module_ids if module_id in context_ids
        ]
        resolved.append(entry)
    return sorted(
        resolved,
        key=lambda lane: (-int(lane.get("priority", 0)), str(lane.get("id", ""))),
    )


def build_manifest(root: Path = ROOT) -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    for path in module_files(root):
        meta, _body = parse_frontmatter(path)
        rel = path.relative_to(root).as_posix()
        entry = {
            "id": meta["id"],
            "version": int(meta["version"]),
            "file": rel,
            "type": meta["type"],
            "tier": int(meta["tier"]),
            "facet": meta["facet"],
            "facet_values": list(meta.get("facet_values", [])),
            "priority": int(meta["priority"]),
            "triggers": list(meta.get("triggers", [])),
            "avoid_when": list(meta.get("avoid_when", [])),
            "dependencies": list(meta.get("dependencies", [])),
            "conflicts": list(meta.get("conflicts", [])),
            "provides_anchors": list(meta.get("provides_anchors", [])),
        }
        modules.append(entry)

    modules.sort(key=module_sort_key)
    lanes: list[dict[str, Any]] = []
    for path in lane_files(root):
        meta, _body = parse_frontmatter(path)
        lanes.append(
            {
                "id": meta["id"],
                "version": int(meta["version"]),
                "file": path.relative_to(root).as_posix(),
                "priority": int(meta["priority"]),
                "activation": meta["activation"],
                "select_types": list(meta.get("select_types", [])),
                "select_facets": list(meta.get("select_facets", [])),
                "select_module_ids": list(meta.get("select_module_ids", [])),
                "required_common_modules": list(
                    meta.get("required_common_modules", [])
                ),
                "owns_sections": list(meta.get("owns_sections", [])),
                "required_topics": list(meta.get("required_topics", [])),
            }
        )
    lanes.sort(key=lambda lane: (-int(lane["priority"]), str(lane["id"])))
    return {
        "name": "reverse-image-prompt",
        "architecture": "distributed modular facet router",
        "version": "3.7.0-compact-residual-closure",
        "entrypoint": "SKILL.md",
        "source": "generated from modules/*.md and lanes/*.md frontmatter by tools/gen_manifest.py",
        "analysis_orchestration": {
            "route_schema": "reverse-image-analysis-route/v2",
            "default_profile": "prompt",
            "supported_profiles": ["prompt", "audited"],
            "prompt_report_schema": "reverse-image-analysis-lane-report/compact-v2",
            "prompt_set_schema": "reverse-image-analysis-compact-set/v2",
            "audited_report_schema": "reverse-image-analysis-lane-report/v2",
            "audited_bundle_schema": "reverse-image-analysis-bundle/v2",
            "reference": "references/analysis-orchestration.md",
        },
        "analysis_lanes": lanes,
        "tiers": {str(k): v for k, v in TIERS.items()},
        "required_core_modules": [m["id"] for m in modules if int(m["tier"]) == 0],
        "modules": modules,
    }


def registry_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Reverse Image Prompt Module Registry",
        "",
        "Generated by `tools/gen_manifest.py`; edit module frontmatter, not this file.",
        "",
    ]
    modules = manifest.get("modules", [])
    lanes = manifest.get("analysis_lanes", [])
    if lanes:
        lines += [
            "## Analysis lanes",
            "",
            "| Lane | Version | Activation | Selectors | Common modules | Owns |",
            "|---|---:|---|---|---|---|",
        ]
        for lane in lanes:
            selectors = ", ".join(
                [f"type:{item}" for item in lane.get("select_types", [])]
                + [f"facet:{item}" for item in lane.get("select_facets", [])]
                + [f"module:{item}" for item in lane.get("select_module_ids", [])]
            ) or "-"
            common = ", ".join(lane.get("required_common_modules", [])) or "-"
            owns = ", ".join(lane.get("owns_sections", [])) or "-"
            lines.append(
                f"| `{lane['id']}` | {lane['version']} | `{lane['activation']}` | "
                f"{selectors} | {common} | {owns} |"
            )
        lines.append("")
    for tier_key, tier_name in manifest.get("tiers", {}).items():
        tier = int(tier_key)
        tier_modules = [m for m in modules if int(m.get("tier", -1)) == tier]
        if not tier_modules:
            continue
        lines += [
            f"## Tier {tier}: {tier_name}",
            "",
            "| Module | Version | Facet | Values | Dependencies | Provides anchors |",
            "|---|---:|---|---|---|---|",
        ]
        for module in tier_modules:
            values = ", ".join(module.get("facet_values", [])) or "-"
            deps = ", ".join(module.get("dependencies", [])) or "-"
            anchors = ", ".join(module.get("provides_anchors", [])) or "-"
            lines.append(
                f"| `{module['id']}` | {module['version']} | `{module['facet']}` | "
                f"{values} | {deps} | {anchors} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def expand_dependencies(module_ids: list[str], manifest: dict[str, Any]) -> list[str]:
    modules = module_map(manifest)
    resolved: set[str] = set()
    visiting: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in resolved:
            return
        if module_id in visiting:
            raise ValueError(f"dependency cycle at {module_id}")
        if module_id not in modules:
            raise KeyError(module_id)
        visiting.add(module_id)
        for dep in modules[module_id].get("dependencies", []):
            visit(dep)
        visiting.remove(module_id)
        resolved.add(module_id)

    for module_id in module_ids:
        visit(module_id)

    return [
        m["id"] for m in sorted((modules[mid] for mid in resolved), key=module_sort_key)
    ]
