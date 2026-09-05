#!/usr/bin/env python3
"""Generate manifest.json and modules/_registry.md from module frontmatter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from module_metadata import ROOT, build_manifest, registry_markdown


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files differ")
    args = parser.parse_args(argv)

    manifest = build_manifest(ROOT)
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    registry_text = registry_markdown(manifest)

    manifest_path = ROOT / "manifest.json"
    registry_path = ROOT / "modules" / "_registry.md"

    if args.check:
        errors: list[str] = []
        if not manifest_path.exists() or manifest_path.read_text(encoding="utf-8") != manifest_text:
            errors.append(str(manifest_path.relative_to(ROOT)))
        if not registry_path.exists() or registry_path.read_text(encoding="utf-8") != registry_text:
            errors.append(str(registry_path.relative_to(ROOT)))
        if errors:
            print("GENERATED FILES OUT OF DATE")
            for rel in errors:
                print(f"- {rel}")
            return 1
        print("generated files ok")
        return 0

    manifest_path.write_text(manifest_text, encoding="utf-8")
    registry_path.write_text(registry_text, encoding="utf-8")
    print(f"wrote {manifest_path}")
    print(f"wrote {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
