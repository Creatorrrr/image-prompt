#!/usr/bin/env python3
"""Fail closed when a rendered moe candidate is not eligible for promotion.

This auditor validates recorded pixel-review evidence; it does not inspect or
score an image by itself.  A technical PASS still cannot establish that the
result feels moe: representative promotion also requires the requesting user's
explicit acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import audit_composed_prompt


REVIEW_SCHEMA_VERSION = "moe-render-review/v1"
VISUAL_OBLIGATIONS_CONTRACT_VERSION = "photo-visual-obligations/v1"
USER_JUDGMENT_VALUES = {"accepted", "rejected", "pending", "not_applicable"}
USER_JUDGMENT_SOURCES = {"requesting_user", "not_yet_received"}


def load_json_arg(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("{") or raw.startswith("["):
        return json.loads(raw)
    return json.loads(Path(raw).read_text(encoding="utf-8"))


def first_pack(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError("candidate pack list must contain exactly one pack")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise ValueError("candidate pack must be a JSON object or one-item list")
    return payload


def review_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("render review must be a JSON object")
    return payload


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_result_path(result_image: str, review_path: Path | None) -> Path:
    candidate = Path(result_image).expanduser()
    if not candidate.is_absolute() and review_path is not None:
        candidate = review_path.parent / candidate
    return candidate.resolve()


def audit_moe_render_review(
    pack: dict[str, Any],
    review: dict[str, Any],
    *,
    composed: dict[str, Any] | None = None,
    review_path: Path | None = None,
) -> dict[str, Any]:
    """Return a deterministic promotion decision from declared review gates."""

    schema_failures: list[dict[str, Any]] = []
    failed_hard_gates: list[dict[str, Any]] = []

    contract = pack.get("moe_response")
    if not isinstance(contract, dict) or contract.get("enabled") is not True:
        schema_failures.append(
            {
                "check": "moe_response",
                "reason": "candidate pack does not contain an enabled moe_response contract",
            }
        )
        contract = {}
    qualification = contract.get("render_qualification")
    if not isinstance(qualification, dict) or qualification.get("required") is not True:
        schema_failures.append(
            {
                "check": "render_qualification",
                "reason": "moe_response contract does not require render qualification",
            }
        )
        qualification = {}

    base_required_gates = [
        str(value)
        for value in qualification.get("required_hard_gates") or []
        if isinstance(value, str) and value.strip()
    ]
    effective_visual_contract, visual_selection_failures = (
        audit_composed_prompt.derive_effective_visual_obligation_contract(
            pack,
            composed,
        )
    )
    schema_failures.extend(
        {
            "check": f"effective_visual_contract.{failure.get('check')}",
            "reason": failure.get("reason"),
            **{
                key: value
                for key, value in failure.items()
                if key not in {"check", "reason"}
            },
        }
        for failure in visual_selection_failures
    )
    effective_visual_gates = [
        str(value)
        for value in (effective_visual_contract or {}).get("required_hard_gates") or []
        if isinstance(value, str) and value.strip()
    ]
    required_gates = list(dict.fromkeys(base_required_gates + effective_visual_gates))
    if not required_gates:
        schema_failures.append(
            {
                "check": "required_hard_gates",
                "reason": "render qualification exposes no hard gates",
            }
        )

    if review.get("schema_version") != REVIEW_SCHEMA_VERSION:
        schema_failures.append(
            {
                "check": "schema_version",
                "reason": f"render review must use {REVIEW_SCHEMA_VERSION}",
            }
        )
    if str(review.get("pack_id") or "") != str(pack.get("pack_id") or ""):
        schema_failures.append(
            {
                "check": "pack_id",
                "reason": "render review pack_id differs from candidate pack",
            }
        )
    if str(review.get("contract_version") or "") != str(contract.get("contract_version") or ""):
        schema_failures.append(
            {
                "check": "contract_version",
                "reason": "render review contract_version differs from moe_response contract",
            }
        )
    if not isinstance(review.get("reviewer"), str) or not str(review.get("reviewer") or "").strip():
        schema_failures.append(
            {
                "check": "reviewer",
                "reason": "render review requires a named human or agent pixel reviewer",
            }
        )

    result_image = str(review.get("result_image") or "").strip()
    result_sha256 = str(review.get("result_sha256") or "").strip().lower()
    if not result_image:
        schema_failures.append(
            {"check": "result_image", "reason": "render review requires an exact result image path"}
        )
    if re.fullmatch(r"[0-9a-f]{64}", result_sha256) is None:
        schema_failures.append(
            {"check": "result_sha256", "reason": "result_sha256 must be a 64-character hex digest"}
        )
    if result_image:
        resolved_result = resolve_result_path(result_image, review_path)
        if not resolved_result.is_file():
            schema_failures.append(
                {
                    "check": "result_image",
                    "reason": "result image does not exist at the review-relative path",
                    "path": str(resolved_result),
                }
            )
        elif re.fullmatch(r"[0-9a-f]{64}", result_sha256) is not None:
            actual_sha256 = sha256_path(resolved_result)
            if actual_sha256 != result_sha256:
                schema_failures.append(
                    {
                        "check": "result_sha256",
                        "reason": "result image bytes differ from the recorded digest",
                        "expected": result_sha256,
                        "actual": actual_sha256,
                    }
                )

    hard_gates = review.get("hard_gates")
    if not isinstance(hard_gates, dict):
        schema_failures.append(
            {"check": "hard_gates", "reason": "render review requires a hard_gates object"}
        )
        hard_gates = {}
    visual_contract = pack.get("visual_obligations")
    if isinstance(visual_contract, dict) and visual_contract.get("enabled") is True:
        if visual_contract.get("contract_version") != VISUAL_OBLIGATIONS_CONTRACT_VERSION:
            schema_failures.append(
                {
                    "check": "visual_obligations.contract_version",
                    "reason": "unsupported visual-obligations contract_version",
                }
            )
        visual_required_gates = [
            str(value)
            for value in visual_contract.get("required_hard_gates") or []
            if isinstance(value, str) and value.strip()
        ]
        missing_from_qualification = sorted(
            set(visual_required_gates) - set(base_required_gates)
        )
        if missing_from_qualification:
            schema_failures.append(
                {
                    "check": "visual_obligations.required_hard_gates",
                    "reason": "visual hard gates were not merged into moe render qualification",
                    "missing": missing_from_qualification,
                }
            )
    if (
        isinstance(effective_visual_contract, dict)
        and effective_visual_contract.get("strict_gate_set") is True
    ):
        missing_review_gates = sorted(set(required_gates) - set(hard_gates))
        extra_hard_gates = sorted(set(hard_gates) - set(required_gates))
        if missing_review_gates or extra_hard_gates:
            schema_failures.append(
                {
                    "check": "hard_gates",
                    "reason": (
                        "strict visual-obligation reviews must exactly equal the effective "
                        "pack-plus-composed hard-gate set; supplemental observations belong outside hard_gates"
                    ),
                    "missing": missing_review_gates,
                    "extra": extra_hard_gates,
                }
            )
    for gate in required_gates:
        item = hard_gates.get(gate)
        if not isinstance(item, dict):
            failed_hard_gates.append(
                {"gate": gate, "status": "missing", "reason": "required hard gate is missing"}
            )
            continue
        status = str(item.get("status") or "").strip()
        evidence = str(item.get("evidence") or "").strip()
        if status not in {"pass", "fail"}:
            schema_failures.append(
                {
                    "check": f"hard_gates.{gate}.status",
                    "reason": "hard gate status must be exactly pass or fail; partial cannot be promoted",
                }
            )
        if len(evidence) < 12:
            schema_failures.append(
                {
                    "check": f"hard_gates.{gate}.evidence",
                    "reason": "hard gate requires concise image-grounded evidence",
                }
            )
        if status != "pass":
            failed_hard_gates.append(
                {"gate": gate, "status": status or "missing", "evidence": evidence}
            )

    user_judgment = review.get("user_judgment")
    if not isinstance(user_judgment, dict):
        schema_failures.append(
            {"check": "user_judgment", "reason": "render review requires user_judgment"}
        )
        user_judgment = {}
    baseline_available = user_judgment.get("baseline_available") is True
    genuinely_moe = str(user_judgment.get("genuinely_moe") or "").strip()
    better_than_baseline = str(user_judgment.get("better_than_baseline") or "").strip()
    user_judgment_source = str(user_judgment.get("source") or "").strip()
    user_judgment_evidence = str(user_judgment.get("evidence") or "").strip()
    for field, value in (
        ("genuinely_moe", genuinely_moe),
        ("better_than_baseline", better_than_baseline),
    ):
        if value not in USER_JUDGMENT_VALUES:
            schema_failures.append(
                {
                    "check": f"user_judgment.{field}",
                    "reason": "user judgment must be accepted, rejected, pending, or not_applicable",
                }
            )
    if user_judgment_source not in USER_JUDGMENT_SOURCES:
        schema_failures.append(
            {
                "check": "user_judgment.source",
                "reason": "user judgment source must be requesting_user or not_yet_received",
            }
        )
    decided_values = {genuinely_moe, better_than_baseline} & {"accepted", "rejected"}
    if decided_values and user_judgment_source != "requesting_user":
        schema_failures.append(
            {
                "check": "user_judgment.source",
                "reason": "accepted or rejected judgments must come from the requesting user",
            }
        )
    if user_judgment_source == "requesting_user" and len(user_judgment_evidence) < 8:
        schema_failures.append(
            {
                "check": "user_judgment.evidence",
                "reason": "requesting-user judgment requires a concise quote or faithful decision summary",
            }
        )
    if (
        genuinely_moe == "pending"
        and better_than_baseline in {"pending", "not_applicable"}
        and user_judgment_source != "not_yet_received"
    ):
        schema_failures.append(
            {
                "check": "user_judgment.source",
                "reason": "fully pending judgment must be recorded as not_yet_received",
            }
        )
    if genuinely_moe == "not_applicable":
        schema_failures.append(
            {
                "check": "user_judgment.genuinely_moe",
                "reason": "genuine moe acceptance is always required for representative promotion",
            }
        )
    if baseline_available and better_than_baseline == "not_applicable":
        schema_failures.append(
            {
                "check": "user_judgment.better_than_baseline",
                "reason": "baseline comparison is required when a baseline is available",
            }
        )
    if not baseline_available and better_than_baseline not in {"not_applicable", "pending"}:
        schema_failures.append(
            {
                "check": "user_judgment.better_than_baseline",
                "reason": "without a baseline, better_than_baseline must be not_applicable or pending",
            }
        )

    technical_qualified = not schema_failures and not failed_hard_gates
    comparison_accepted = (
        better_than_baseline == "accepted"
        if baseline_available
        else better_than_baseline == "not_applicable"
    )
    representative_eligible = (
        technical_qualified and genuinely_moe == "accepted" and comparison_accepted
    )
    if not technical_qualified:
        qualification_status = "failed_technical_hard_gates"
    elif genuinely_moe == "rejected" or better_than_baseline == "rejected":
        qualification_status = "rejected_by_requesting_user"
    elif representative_eligible:
        qualification_status = "representative_eligible"
    else:
        qualification_status = "pending_requesting_user_judgment"

    return {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "pack_id": str(pack.get("pack_id") or ""),
        "contract_version": str(contract.get("contract_version") or ""),
        "qualification_status": qualification_status,
        "technical_qualified": technical_qualified,
        "representative_eligible": representative_eligible,
        "required_hard_gate_count": len(required_gates),
        "effective_visual_contract_sha256": (
            audit_composed_prompt.effective_visual_obligation_sha256(
                effective_visual_contract
            )
        ),
        "selected_visual_concept_ids": [
            str(value)
            for value in (effective_visual_contract or {}).get(
                "selected_visual_concept_ids"
            )
            or []
            if str(value).strip()
        ],
        "failed_hard_gates": failed_hard_gates,
        "schema_failures": schema_failures,
        "user_judgment": {
            "baseline_available": baseline_available,
            "genuinely_moe": genuinely_moe,
            "better_than_baseline": better_than_baseline,
            "source": user_judgment_source,
            "evidence": user_judgment_evidence,
        },
        "boundary": (
            "This audit validates recorded pixel-review evidence and user acceptance; "
            "it does not infer visual truth from metadata, authenticate who authored a review, "
            "or declare moe on the user's behalf."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, help="Candidate-pack JSON path or inline JSON")
    parser.add_argument(
        "--composed",
        help=(
            "Audited composed-prompt JSON; required when the pack exposes optional "
            "visual concept candidates"
        ),
    )
    parser.add_argument("--review", required=True, help="Render-review JSON path or inline JSON")
    parser.add_argument("--output", help="Optional path for the audit JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        pack = first_pack(load_json_arg(args.pack))
        composed = (
            audit_composed_prompt.composed_object(load_json_arg(args.composed))
            if args.composed
            else None
        )
        review = review_object(load_json_arg(args.review))
        review_path = None
        raw_review_path = Path(args.review).expanduser()
        if not args.review.strip().startswith(("{", "[")) and raw_review_path.is_file():
            review_path = raw_review_path.resolve()
        summary = audit_moe_render_review(
            pack,
            review,
            composed=composed,
            review_path=review_path,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    rendered = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if summary["representative_eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
