#!/usr/bin/env python3
"""Read-only source diagnostics and generation-bound relationship reports."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.photo_data_maintenance.common import MaintenanceError
from tools.photo_data_maintenance.corpus import DEFAULT_ROOT, capture_draft, capture_generation
from tools.photo_data_maintenance.links import query
from tools.photo_data_maintenance.report import activate, current_report, difference, load_report, pointer_directory, read_pointer, require_current, write_report
from tools.photo_data_maintenance.reviews import load_reviews


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("audit", "build"):
        sub = commands.add_parser(command, allow_abbrev=False)
        sub.add_argument("--source-root", type=Path, default=DEFAULT_ROOT)
        sub.add_argument("--output", type=Path, required=True)
        sub.add_argument("--reviews", type=Path)
        if command == "audit":
            sub.add_argument("--runtime-store", type=Path)
        if command == "build":
            sub.add_argument("--runtime-store", type=Path, required=True)
            sub.add_argument("--generation", required=True)
            sub.add_argument("--report-store", type=Path)
    sub = commands.add_parser("query", allow_abbrev=False)
    report_choice = sub.add_mutually_exclusive_group(required=True)
    report_choice.add_argument("--report", type=Path)
    report_choice.add_argument("--report-store", type=Path)
    choice = sub.add_mutually_exclusive_group(required=True)
    choice.add_argument("--candidate")
    choice.add_argument("--profile")
    choice.add_argument("--bundle")
    sub.add_argument("--require-current", action="store_true")
    sub.add_argument("--source-root", type=Path)
    sub.add_argument("--runtime-store", type=Path)
    sub = commands.add_parser("diff", allow_abbrev=False)
    sub.add_argument("--before", type=Path, required=True)
    sub.add_argument("--after", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command in {"audit", "build"}:
        expected = None
        if args.command == "build" and args.report_store:
            expected = read_pointer(pointer_directory(args.report_store, str(args.source_root)))
        captured = (capture_draft(args.source_root, runtime_store=args.runtime_store) if args.command == "audit" else
                    capture_generation(args.source_root, args.runtime_store, args.generation))
        manifest = write_report(captured, args.output, load_reviews(args.reviews))
        result = {"report": str(args.output.resolve()), "manifest": manifest}
        if args.command == "build" and args.report_store:
            result["publication"] = activate(args.output, args.report_store, args.source_root, args.runtime_store, expected)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if manifest["findings_count"]["error"] else 0
    if args.command == "query":
        if args.report_store:
            if args.source_root is None or args.runtime_store is None:
                parser.error("--report-store needs --source-root and --runtime-store")
            args.report = current_report(args.report_store, args.source_root)
            args.require_current = True
        report = load_report(args.report, require_links=True)
        if args.require_current:
            if args.source_root is None or args.runtime_store is None:
                parser.error("--require-current needs --source-root and --runtime-store")
            require_current(report, args.source_root, args.runtime_store)
        node = args.candidate or ("profile:" + args.profile if args.profile else "bundle:" + args.bundle)
        result = query(report["inventory"], report["links"], node, report["reviews"])
        result["generation_id"] = report["manifest"]["binding"]["generation_id"]
        result["source_fingerprint"] = report["manifest"]["binding"]["source_fingerprint"]
        result["freshness"] = "current_verified" if args.require_current else "pinned_report"
    else:
        result = difference(load_report(args.before), load_report(args.after))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
