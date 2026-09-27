#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from common import json_files, load_json, read_records


REQUIRED = {
    "harvest": {"id", "collected_at", "adapter", "collection_method", "source_url", "source", "raw_text", "media", "license_signals", "flags"},
    "sanitized": {"id", "from_harvest_id", "sanitized_prompt", "stripped_segments", "image_observation", "abstract_visual_grammar", "no_raw_reuse", "flags"},
    "candidate": {"candidate_id", "kind", "target_asset", "proposed", "abstracted_from", "frequency", "novelty", "overlap_with_existing", "confidence", "rationale", "risk_flags", "verbatim_similarity", "recommendation"},
    "report": {"report_id", "generated_at", "no_changes_applied", "counts", "gate_status", "candidates", "report_markdown"},
}
ALLOWED_METHODS = {"official_api", "allowed_feed", "local_inbox"}
HANDLE_RE = re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,30}")
PROMO_RE = re.compile(r"(?i)\b(follow me|follow for more|link in bio|join my discord|subscribe|prompt by|created by|made by|credit to)\b")


def validate_required(kind: str, record: dict[str, Any], label: str) -> list[str]:
    errors = []
    missing = REQUIRED[kind] - set(record)
    if missing:
        errors.append(f"{label}: missing {sorted(missing)}")
    return errors


def validate_records(kind: str, path: Path) -> list[str]:
    errors: list[str] = []
    if kind == "report":
        report = load_json(path)
        errors.extend(validate_required(kind, report, str(path)))
        if report.get("no_changes_applied") is not True:
            errors.append(f"{path}: no_changes_applied must be true")
        text = report.get("report_markdown", "")
        if HANDLE_RE.search(text) or PROMO_RE.search(text):
            errors.append(f"{path}: report contains source handle or promo text")
        for candidate in report.get("candidates", []):
            errors.extend(validate_required("candidate", candidate, f"{path}:{candidate.get('candidate_id', '?')}"))
        return errors

    for record in read_records(path):
        label = f"{path}:{record.get('id') or record.get('candidate_id') or '?'}"
        errors.extend(validate_required(kind, record, label))
        if kind == "harvest" and record.get("collection_method") not in ALLOWED_METHODS:
            errors.append(f"{label}: blocked collection_method {record.get('collection_method')}")
        if kind == "sanitized":
            text = record.get("sanitized_prompt", "")
            if HANDLE_RE.search(text) or PROMO_RE.search(text):
                errors.append(f"{label}: sanitized text contains source handle or promo text")
        if kind == "candidate":
            text = " ".join(
                [
                    str(record.get("rationale", "")),
                    str(record.get("proposed", {}).get("en", "")),
                    str(record.get("proposed", {}).get("ko", "")),
                ]
            )
            if HANDLE_RE.search(text) or PROMO_RE.search(text):
                errors.append(f"{label}: candidate contains source handle or promo text")
    return errors


def infer_kind(path: Path) -> str:
    text = str(path)
    if "/raw/" in text:
        return "harvest"
    if "/sanitized/" in text:
        return "sanitized"
    if "/candidates/" in text:
        return "candidate"
    if "/reports/" in text:
        return "report"
    raise ValueError(f"Cannot infer record kind for {path}; pass --kind")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate prompt-trend-scout runtime records.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--kind", choices=sorted(REQUIRED))
    args = parser.parse_args()
    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        for file_path in json_files(path):
            kind = args.kind or infer_kind(file_path)
            errors.extend(validate_records(kind, file_path))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("prompt-trend-scout validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
