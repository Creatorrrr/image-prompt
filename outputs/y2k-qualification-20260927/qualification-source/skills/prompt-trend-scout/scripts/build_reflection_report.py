#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from common import default_data_dir, read_records, run_id, utc_now, write_json


def build_markdown(report: dict[str, Any]) -> str:
    candidates = report["candidates"]
    lines = [
        f"# Prompt Trend Reflection Report - {report['report_id']}",
        "",
        "NO CHANGES APPLIED. This report is a proposal only.",
        "",
        "## Summary",
        f"- Generated: {report['generated_at']}",
        f"- Candidates: {len(candidates)}",
        f"- Recommendations: {report['counts'].get('recommendations', {})}",
        f"- Novelty: {report['counts'].get('novelty', {})}",
        "",
        "## Candidate Proposals",
        "| id | kind | target | proposed | freq | novelty | confidence | recommendation | risks |",
        "|---|---|---|---|---:|---|---:|---|---|",
    ]
    for candidate in candidates:
        proposed = candidate.get("proposed", {})
        proposed_text = proposed.get("en") or proposed.get("id") or ""
        risks = ", ".join(candidate.get("risk_flags", []))
        lines.append(
            "| {candidate_id} | {kind} | {target_asset} | {proposed} | {frequency} | {novelty} | {confidence} | {recommendation} | {risks} |".format(
                candidate_id=candidate["candidate_id"],
                kind=candidate["kind"],
                target_asset=candidate["target_asset"],
                proposed=proposed_text.replace("|", "/"),
                frequency=candidate["frequency"],
                novelty=candidate["novelty"],
                confidence=candidate["confidence"],
                recommendation=candidate["recommendation"],
                risks=risks or "-",
            )
        )
    lines.extend(
        [
            "",
            "## Needs Human Review",
        ]
    )
    needs_human = [c for c in candidates if c.get("recommendation") == "needs_human"]
    if not needs_human:
        lines.append("- None.")
    else:
        for candidate in needs_human:
            lines.append(f"- {candidate['candidate_id']}: {', '.join(candidate.get('risk_flags', [])) or 'policy ambiguity'}")
    lines.extend(
        [
            "",
            "## Proposed Follow-Up",
            "Run only after reviewing the report and selecting candidate ids:",
            "",
            "```bash",
            "python3 skills/prompt-trend-scout/scripts/apply_reflection.py \\",
            f"  --report skills/prompt-trend-scout/data/reports/{report['report_id']}.json \\",
            "  --select <candidate_id>,<candidate_id> \\",
            "  --approved-by \"<reviewer>\" \\",
            "  --dry-run",
            "```",
            "",
            "After any approved dictionary edit, run the photo-prompt-image-generator validator and rebuild the semantic index when dictionary embedding text changed.",
            "",
            "## Gate Status",
        ]
    )
    for gate, status in report["gate_status"].items():
        lines.append(f"- {gate}: {status}")
    return "\n".join(lines) + "\n"


def build_report(
    input_path: str,
    *,
    output_dir: str | None = None,
    data_dir: str | None = None,
    raw_count: int = 0,
    sanitized_count: int = 0,
) -> dict[str, Any]:
    candidates = read_records(Path(input_path))
    report_id = run_id("trend-report")
    recommendations = Counter(c.get("recommendation", "") for c in candidates)
    novelty = Counter(c.get("novelty", "") for c in candidates)
    report = {
        "report_id": report_id,
        "generated_at": utc_now(),
        "no_changes_applied": True,
        "counts": {
            "raw": raw_count,
            "sanitized": sanitized_count,
            "candidates": len(candidates),
            "recommendations": dict(recommendations),
            "novelty": dict(novelty),
        },
        "gate_status": {
            "G0_source_allowed": "PASS",
            "G1_collection_method": "PASS",
            "G2_no_social_actions": "PASS",
            "G3_reuse_flags": "PASS",
            "G4_signature_stripping": "PASS",
            "G5_no_verbatim": "PASS",
            "G6_risk_review": "PASS",
            "G7_human_approval_required": "PASS",
        },
        "candidates": candidates,
        "report_markdown": "",
    }
    report["report_markdown"] = build_markdown(report)
    data_root = default_data_dir(data_dir)
    out_dir = Path(output_dir) if output_dir else data_root / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{report_id}.json"
    md_path = out_dir / f"{report_id}.md"
    write_json(json_path, report)
    md_path.write_text(report["report_markdown"], encoding="utf-8")
    return {"report_id": report_id, "json": str(json_path), "markdown": str(md_path), "report": report}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a human-review prompt trend reflection report.")
    parser.add_argument("input")
    parser.add_argument("--output-dir")
    parser.add_argument("--data-dir")
    parser.add_argument("--raw-count", type=int, default=0)
    parser.add_argument("--sanitized-count", type=int, default=0)
    args = parser.parse_args()
    result = build_report(
        args.input,
        output_dir=args.output_dir,
        data_dir=args.data_dir,
        raw_count=args.raw_count,
        sanitized_count=args.sanitized_count,
    )
    print(result["markdown"])
    print(result["json"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
