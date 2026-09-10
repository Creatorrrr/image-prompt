#!/usr/bin/env python3
"""Audit a recorded pixel review against a frozen generic render-repair contract.

This script validates review provenance and gate coverage.  It does not inspect
pixels itself and therefore never converts an unrecorded visual impression into
technical qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import audit_composed_prompt


SCHEMA_VERSION = "photo-image-render-review/v1"
AUDIT_SCHEMA_VERSION = "photo-image-render-review-audit/v1"
VALID_GATE_STATUSES = {"pass", "fail"}
VALID_REVIEW_SCALES = {"thumbnail", "native"}


def load_json_arg(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("{") or raw.startswith("["):
        return json.loads(raw)
    return json.loads(Path(raw).read_text(encoding="utf-8"))


def one_object(payload: Any, label: str) -> dict[str, Any]:
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError(f"{label} list must contain exactly one object")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object or one-item list")
    return payload


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(raw: str, review_path: Path | None) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute() and review_path is not None:
        path = review_path.parent / path
    return path.resolve()


def required_scales(render_gate: dict[str, Any]) -> set[str]:
    scale = str(render_gate.get("review_scale") or "")
    if scale == "both":
        return {"thumbnail", "native"}
    return {scale} if scale in VALID_REVIEW_SCALES else set()


def audit_image_render_review(
    pack: dict[str, Any],
    composed: dict[str, Any],
    review: dict[str, Any],
    *,
    review_path: Path | None = None,
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []

    if review.get("schema_version") != SCHEMA_VERSION:
        failures.append(
            {
                "check": "schema_version",
                "reason": f"render review must use {SCHEMA_VERSION}",
            }
        )

    pack_id = str(pack.get("pack_id") or "")
    if (
        not pack_id
        or str(composed.get("pack_id") or "") != pack_id
        or str(review.get("pack_id") or "") != pack_id
    ):
        failures.append(
            {
                "check": "pack_id",
                "reason": "pack, composed prompt, and render review must share one exact pack_id",
            }
        )

    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    expected_contract = audit_composed_prompt.expected_render_repair_contract(core)
    supplied_contract = (
        pack.get("render_repair")
        if isinstance(pack.get("render_repair"), dict)
        else None
    )
    if expected_contract is None:
        failures.append(
            {
                "check": "render_repair_contract",
                "reason": "pixel repair review requires a v2 lineage repair target",
            }
        )
        expected_contract = {}
    elif supplied_contract != expected_contract:
        failures.append(
            {
                "check": "render_repair_contract",
                "reason": "candidate-pack render-repair contract does not match the frozen core",
            }
        )
    expected_contract_sha = str(expected_contract.get("canonical_sha256") or "")
    if review.get("source_render_repair_contract_sha256") != expected_contract_sha:
        failures.append(
            {
                "check": "source_render_repair_contract_sha256",
                "reason": "review must bind the exact frozen render-repair contract",
                "expected": expected_contract_sha or None,
                "actual": review.get("source_render_repair_contract_sha256"),
            }
        )

    reviewer = review.get("reviewer")
    if (
        not isinstance(reviewer, dict)
        or set(reviewer) != {"reviewer_id", "method"}
        or len(str(reviewer.get("reviewer_id") or "").strip()) < 2
        or reviewer.get("method") != "direct_pixel_inspection"
    ):
        failures.append(
            {
                "check": "reviewer",
                "reason": "review requires a named reviewer using direct_pixel_inspection",
            }
        )

    result = review.get("result")
    actual_result_sha = ""
    resolved_result: Path | None = None
    if not isinstance(result, dict) or set(result) != {"path", "sha256"}:
        failures.append(
            {
                "check": "result",
                "reason": "review result must contain exactly path and sha256",
            }
        )
    else:
        raw_path = str(result.get("path") or "").strip()
        expected_sha = str(result.get("sha256") or "").strip().lower()
        if not raw_path:
            failures.append(
                {"check": "result.path", "reason": "reviewed image path is required"}
            )
        else:
            resolved_result = resolve_path(raw_path, review_path)
            if not resolved_result.is_file():
                failures.append(
                    {
                        "check": "result.path",
                        "reason": "reviewed image file does not exist",
                        "path": str(resolved_result),
                    }
                )
            else:
                actual_result_sha = sha256_path(resolved_result)
                if expected_sha != actual_result_sha:
                    failures.append(
                        {
                            "check": "result.sha256",
                            "reason": "reviewed image bytes differ from the recorded digest",
                            "expected": expected_sha,
                            "actual": actual_result_sha,
                        }
                    )

    expected_gates: dict[str, dict[str, Any]] = {
        str(gate.get("id") or ""): gate
        for target in expected_contract.get("targets") or []
        if isinstance(target, dict)
        for gate in target.get("render_gates") or []
        if isinstance(gate, dict) and str(gate.get("id") or "")
    }
    rows = review.get("gates")
    if not isinstance(rows, list):
        failures.append(
            {"check": "gates", "reason": "render review gates must be a list"}
        )
        rows = []
    actual_gates: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {
            "gate_id",
            "status",
            "reviewed_scales",
            "evidence",
        }:
            failures.append(
                {
                    "check": f"gates[{index}]",
                    "reason": "each gate must contain exactly gate_id, status, reviewed_scales, and evidence",
                }
            )
            continue
        gate_id = str(row.get("gate_id") or "")
        if not gate_id or gate_id in actual_gates:
            failures.append(
                {
                    "check": f"gates[{index}].gate_id",
                    "reason": "gate_id must be non-empty and unique",
                }
            )
            continue
        actual_gates[gate_id] = row
        if row.get("status") not in VALID_GATE_STATUSES:
            failures.append(
                {
                    "check": f"gates[{index}].status",
                    "reason": "gate status must be pass or fail; partial is not allowed",
                }
            )
        evidence = str(row.get("evidence") or "").strip()
        if len(evidence) < 12:
            failures.append(
                {
                    "check": f"gates[{index}].evidence",
                    "reason": "gate review requires concise, concrete visual evidence",
                }
            )
        scales = row.get("reviewed_scales")
        if (
            not isinstance(scales, list)
            or not scales
            or len(scales) != len(set(scales))
            or not set(scales).issubset(VALID_REVIEW_SCALES)
        ):
            failures.append(
                {
                    "check": f"gates[{index}].reviewed_scales",
                    "reason": "reviewed_scales must be a distinct non-empty subset of thumbnail and native",
                }
            )

    if set(actual_gates) != set(expected_gates):
        failures.append(
            {
                "check": "gate_set",
                "reason": "review must cover the exact frozen hard-gate set with no omissions or additions",
                "missing": sorted(set(expected_gates) - set(actual_gates)),
                "extra": sorted(set(actual_gates) - set(expected_gates)),
            }
        )
    for gate_id, render_gate in expected_gates.items():
        row = actual_gates.get(gate_id)
        if not isinstance(row, dict):
            continue
        required = required_scales(render_gate)
        actual = set(row.get("reviewed_scales") or [])
        if actual != required:
            failures.append(
                {
                    "check": f"gates.{gate_id}.reviewed_scales",
                    "reason": "gate must be reviewed at its exact frozen scale set",
                    "expected": sorted(required),
                    "actual": sorted(actual),
                }
            )

    failed_gate_ids = sorted(
        gate_id
        for gate_id, row in actual_gates.items()
        if row.get("status") == "fail" and gate_id in expected_gates
    )
    schema_status = "pass" if not failures else "fail"
    technical_qualified = not failures and not failed_gate_ids
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "pack_id": pack_id,
        "status": schema_status,
        "qualification_status": "pass" if technical_qualified else "fail",
        "technical_qualified": technical_qualified,
        "source_render_repair_contract_sha256": expected_contract_sha or None,
        "reviewed_result_path": str(resolved_result) if resolved_result else None,
        "reviewed_result_sha256": actual_result_sha or None,
        "failed_gate_ids": failed_gate_ids,
        "failures": failures,
        "boundary": (
            "This audit validates a named review record and its exact generic hard-gate set. "
            "The reviewer supplies pixel judgments; the audit does not infer pixels or user preference."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--composed", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        pack = one_object(load_json_arg(args.pack), "candidate pack")
        composed = one_object(load_json_arg(args.composed), "composed prompt")
        review = one_object(load_json_arg(args.review), "render review")
        review_path = None
        raw_review_path = Path(args.review).expanduser()
        if not args.review.strip().startswith(("{", "[")) and raw_review_path.is_file():
            review_path = raw_review_path.resolve()
        result = audit_image_render_review(
            pack,
            composed,
            review,
            review_path=review_path,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(
            json.dumps(
                {"status": "error", "reason": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["technical_qualified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
