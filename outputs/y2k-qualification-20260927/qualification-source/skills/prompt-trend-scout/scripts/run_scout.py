#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from analyze_corpus import analyze_records
from build_reflection_report import build_report
from collect_sources import collect
from common import default_data_dir, read_records
from diff_against_photo_prompt import diff_candidates
from sanitize_examples import sanitize_records


def validate_paths(paths: list[str]) -> None:
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "validate_harvest_schema.py"), *paths]
    subprocess.run(cmd, check=True)


def run_pipeline(
    *,
    registry: str | None = None,
    data_dir: str | None = None,
    adapters: list[str] | None = None,
    query: str = "",
    since: str = "",
    limit: int = 50,
    cadence: str = "weekly",
) -> dict[str, Any]:
    data_root = default_data_dir(data_dir)
    data_root.mkdir(parents=True, exist_ok=True)
    harvest = collect(
        registry_path=registry,
        data_dir=str(data_root),
        adapters=adapters,
        query=query,
        since=since,
        limit=limit,
    )
    sanitized = sanitize_records(harvest["output"], data_dir=str(data_root))
    candidates = analyze_records(sanitized["output"], data_dir=str(data_root))
    diffed = diff_candidates(candidates["output"], data_dir=str(data_root))
    report = build_report(
        diffed["output"],
        data_dir=str(data_root),
        raw_count=len(harvest["records"]),
        sanitized_count=len(sanitized["records"]),
    )
    validate_paths([harvest["output"], sanitized["output"], diffed["output"], report["json"]])
    return {
        "cadence": cadence,
        "harvest": harvest,
        "sanitized": sanitized,
        "candidates": candidates,
        "diffed": diffed,
        "report": report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the read-only prompt trend scout pipeline.")
    parser.add_argument("--mode", default="collect-analyze", choices=["collect-analyze"])
    parser.add_argument("--cadence", default="weekly", choices=["weekly", "daily", "manual"])
    parser.add_argument("--registry")
    parser.add_argument("--data-dir")
    parser.add_argument("--adapter", action="append", dest="adapters")
    parser.add_argument("--query", default="")
    parser.add_argument("--since", default="")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    result = run_pipeline(
        registry=args.registry,
        data_dir=args.data_dir,
        adapters=args.adapters,
        query=args.query,
        since=args.since,
        limit=args.limit,
        cadence=args.cadence,
    )
    print("Prompt Trend Scout completed without applying changes.")
    print(f"Report markdown: {result['report']['markdown']}")
    print(f"Report json: {result['report']['json']}")
    if result["harvest"]["skipped"]:
        print(f"Skipped adapters: {result['harvest']['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
