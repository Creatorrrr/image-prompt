#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import TARGET_SKILL_DIR, load_json, write_json


def selected_candidates(report: dict[str, Any], select: str) -> list[dict[str, Any]]:
    selected = {item.strip() for item in select.split(",") if item.strip()}
    if not selected:
        raise SystemExit("--select must include at least one candidate id")
    candidates = [c for c in report.get("candidates", []) if c.get("candidate_id") in selected]
    missing = selected - {c.get("candidate_id") for c in candidates}
    if missing:
        raise SystemExit(f"Unknown candidate ids: {', '.join(sorted(missing))}")
    return candidates


def dry_run_lines(candidates: list[dict[str, Any]]) -> list[str]:
    lines = ["DRY RUN - no files changed"]
    for candidate in candidates:
        proposed = candidate.get("proposed", {})
        lines.append(
            "{candidate_id}: {kind} -> {target_asset} :: {proposed}".format(
                candidate_id=candidate["candidate_id"],
                kind=candidate["kind"],
                target_asset=candidate["target_asset"],
                proposed=proposed.get("en") or proposed.get("id"),
            )
        )
    return lines


def apply_candidates(candidates: list[dict[str, Any]]) -> list[str]:
    tags_path = TARGET_SKILL_DIR / "assets" / "photo_prompt_tags.json"
    tags = load_json(tags_path)
    changed: list[str] = []
    for candidate in candidates:
        proposed = candidate.get("proposed", {})
        if candidate["kind"] == "tag":
            slot = proposed.get("slot")
            value = proposed.get("value") or proposed.get("id")
            if not slot or slot not in tags.get("slots", {}):
                changed.append(f"SKIP {candidate['candidate_id']}: unknown slot {slot}")
                continue
            if any(item.get("id") == value for item in tags["slots"][slot]):
                changed.append(f"SKIP {candidate['candidate_id']}: already exists")
                continue
            tags["slots"][slot].append(
                {
                    "id": value,
                    "ko": proposed.get("ko", proposed.get("en", value)),
                    "en": proposed.get("en", value),
                    "weight": 0.8,
                    "tags": ["trend_scout"],
                }
            )
            changed.append(f"ADD tag {slot}.{value}")
        elif candidate["kind"] == "facet_value":
            facet_name = proposed.get("facet_name")
            value = proposed.get("value") or proposed.get("id")
            if not facet_name or facet_name not in tags.get("facet_vocab", {}):
                changed.append(f"SKIP {candidate['candidate_id']}: unknown facet {facet_name}")
                continue
            if value not in tags["facet_vocab"][facet_name]:
                tags["facet_vocab"][facet_name].append(value)
                changed.append(f"ADD facet {facet_name}.{value}")
        else:
            changed.append(f"MANUAL {candidate['candidate_id']}: {candidate['kind']} requires hand edit")
    if any(line.startswith("ADD ") for line in changed):
        write_json(tags_path, tags)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply approved prompt trend reflection candidates.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--select", required=True)
    parser.add_argument("--approved-by", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--no-dry-run", action="store_true")
    args = parser.parse_args()

    if not args.approved_by.strip():
        raise SystemExit("--approved-by is required")
    report = load_json(Path(args.report))
    if report.get("no_changes_applied") is not True:
        raise SystemExit("Refusing to apply a report that lacks no_changes_applied=true")
    candidates = selected_candidates(report, args.select)
    if args.no_dry_run:
        for line in apply_candidates(candidates):
            print(line)
        print("Approved changes applied. Run photo-prompt-image-generator validation next.")
    else:
        for line in dry_run_lines(candidates):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
