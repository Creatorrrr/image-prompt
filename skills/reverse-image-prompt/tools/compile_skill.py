#!/usr/bin/env python3
"""Compile the modular reverse-image-prompt skill into one markdown file.

Examples:
  python tools/compile_skill.py --profile all --output SKILL.compiled.all.md
  python tools/compile_skill.py --profile screenshot --output SKILL.compiled.screenshot.md
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from module_metadata import ROOT, expand_dependencies, load_manifest, module_map, module_sort_key, strip_frontmatter

PROFILE_MODULES = {
    "portrait": [
        "subject.human",
        "detail.human-face-likeness",
        "detail.human-body-form",
        "medium.photographic-capture",
        "detail.pose-hands-gesture",
        "detail.clothing-fashion",
    ],
    "screenshot": [
        "medium.screenshot-ui",
        "subject.generic-object",
        "detail.low-quality-artifacts",
    ],
    "product": [
        "subject.product",
        "medium.photographic-capture",
        "detail.text-logo-label",
        "detail.pose-hands-gesture",
    ],
}


def default_modules(manifest: dict, profile: str | None, selected: list[str]) -> list[str]:
    core = list(manifest.get("required_core_modules", []))
    if selected:
        ids = core + selected
    elif profile == "all":
        ids = [m["id"] for m in sorted(manifest.get("modules", []), key=module_sort_key)]
    elif profile == "core":
        ids = core
    elif profile in PROFILE_MODULES:
        ids = core + PROFILE_MODULES[profile]
    else:
        ids = core
    return expand_dependencies(ids, manifest)


def compile_skill(module_ids: list[str], output: Path) -> None:
    manifest = load_manifest(ROOT)
    mods = module_map(manifest)
    missing = [mid for mid in module_ids if mid not in mods]
    if missing:
        raise SystemExit("Unknown module id(s): " + ", ".join(missing))

    root_skill = ROOT / "SKILL.md"
    parts = [root_skill.read_text(encoding="utf-8").rstrip()]
    parts.append(
        "\n\n---\n\n# Compiled module bundle\n\n"
        "The following module files were appended for runtimes that cannot read sibling files dynamically.\n"
    )
    for mid in module_ids:
        path = ROOT / mods[mid]["file"]
        text = path.read_text(encoding="utf-8")
        parts.append(f"\n\n---\n\n# Included module: `{mid}`\n\n" + strip_frontmatter(text).rstrip())
    adapter_reference = ROOT / "references" / "model-adapters.md"
    if adapter_reference.exists():
        parts.append(
            "\n\n---\n\n# Optional model adapter reference\n\n"
            "Apply only the section for the named downstream generator.\n\n"
            + adapter_reference.read_text(encoding="utf-8").rstrip()
        )
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {output}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=["core", "all", "portrait", "screenshot", "product"], default="core")
    parser.add_argument("--modules", default="", help="comma-separated module ids to include in addition to required core modules")
    parser.add_argument("--output", default="SKILL.compiled.md")
    args = parser.parse_args(argv)

    manifest = load_manifest(ROOT)
    selected = [m.strip() for m in args.modules.split(",") if m.strip()]
    module_ids = default_modules(manifest, args.profile, selected)
    compile_skill(module_ids, ROOT / args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
