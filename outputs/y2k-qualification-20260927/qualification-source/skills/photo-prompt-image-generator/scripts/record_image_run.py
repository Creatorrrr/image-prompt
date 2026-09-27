#!/usr/bin/env python3
"""Append one externally executed image-generation attempt to the run ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]
DEFAULT_LEDGER = PROJECT_ROOT / "runs" / "image_runs.ndjson"
VALID_STATUSES = {"success", "safety_block", "error"}
VALID_COMPOSERS = {"agent", "auto"}
VALID_AUDIT_STATUSES = {"pass", "warn", "fail", "not_run"}
VALID_CANDIDATE_PACK_VERSIONS = {"v2", "v3", "v4", "v5", "v6"}
LEGACY_INDEPENDENT_RUN_MANIFEST_VERSION = "photo-independent-run-manifest/v1"
MODERN_INDEPENDENT_RUN_MANIFEST_VERSION = "photo-independent-run-manifest/v2"


def stable_text_id(text: str | None, length: int = 16) -> str | None:
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def parse_argv_json(raw: str | None) -> list[str]:
    if not raw:
        return []
    value = json.loads(raw)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("--argv-json must be a JSON array of strings")
    return value


def parse_chosen_candidate_ids(raw: str | None) -> object | None:
    if not raw:
        return None
    value = json.loads(raw)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    if isinstance(value, dict):
        for slot, ids in value.items():
            if not isinstance(slot, str):
                raise ValueError("--chosen-candidate-ids-json object keys must be strings")
            if isinstance(ids, str):
                continue
            if isinstance(ids, list) and all(isinstance(item, str) for item in ids):
                continue
            raise ValueError("--chosen-candidate-ids-json object values must be strings or string arrays")
        return value
    raise ValueError("--chosen-candidate-ids-json must be a JSON string array or object")


def parse_chosen_visual_concept_ids(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    value = json.loads(raw)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValueError(
            "--chosen-visual-concept-ids-json must be a JSON string array"
        )
    if len(value) != len(set(value)):
        raise ValueError("--chosen-visual-concept-ids-json values must be distinct")
    return value


def parse_augmentation_brief(raw: str | None) -> object | None:
    if not raw:
        return None
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("--augmentation-brief-json must be a JSON object")
    return value


def build_entry(args: argparse.Namespace) -> dict[str, object]:
    computed_prompt_id = stable_text_id(args.prompt_en)
    if args.prompt_id and args.prompt_id != computed_prompt_id:
        raise ValueError(f"prompt_id mismatch: given={args.prompt_id} computed={computed_prompt_id}")

    if args.attempt < 1:
        raise ValueError("--attempt must be at least 1")
    if args.status not in VALID_STATUSES:
        raise ValueError(f"--status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    if args.composer and args.composer not in VALID_COMPOSERS:
        raise ValueError(f"--composer must be one of: {', '.join(sorted(VALID_COMPOSERS))}")
    if args.audit_status and args.audit_status not in VALID_AUDIT_STATUSES:
        raise ValueError(f"--audit-status must be one of: {', '.join(sorted(VALID_AUDIT_STATUSES))}")

    run_id = stable_text_id(f"{args.ts}|{computed_prompt_id}|{args.attempt}") or ""
    entry: dict[str, object] = {
        "ts": args.ts,
        "run_id": run_id,
        "concept": args.concept,
        "prompt_id": computed_prompt_id,
        "negative_id": stable_text_id(args.negative_en),
        "prompt_en": args.prompt_en,
        "negative_en": args.negative_en,
        "argv": parse_argv_json(args.argv_json),
        "seed": args.seed,
        "attempt": args.attempt,
        "retry_of": args.retry_of,
        "status": args.status,
        "failure_reason": args.failure_reason,
        "image_paths": list(args.image_path or []),
        "tool": args.tool,
    }
    if args.pack_id:
        entry["pack_id"] = args.pack_id
    chosen_candidate_ids = parse_chosen_candidate_ids(args.chosen_candidate_ids_json)
    if chosen_candidate_ids is not None:
        entry["chosen_candidate_ids"] = chosen_candidate_ids
    chosen_visual_concept_ids = parse_chosen_visual_concept_ids(
        args.chosen_visual_concept_ids_json
    )
    if chosen_visual_concept_ids is not None:
        entry["chosen_visual_concept_ids"] = chosen_visual_concept_ids
    if args.effective_visual_contract_sha256:
        if not re.fullmatch(r"[0-9a-f]{64}", args.effective_visual_contract_sha256):
            raise ValueError(
                "--effective-visual-contract-sha256 must be a 64-character SHA-256"
            )
        if not chosen_visual_concept_ids:
            raise ValueError(
                "--effective-visual-contract-sha256 requires at least one chosen visual concept"
            )
        entry["effective_visual_contract_sha256"] = (
            args.effective_visual_contract_sha256
        )
    if args.composer:
        entry["composer"] = args.composer
    if args.audit_status:
        entry["audit_status"] = args.audit_status
    augmentation_brief = parse_augmentation_brief(args.augmentation_brief_json)
    if augmentation_brief is not None:
        entry["augmentation_brief"] = augmentation_brief
    for field in (
        "skill_sha256",
        "authorial_request_sha256",
        "authorial_core_sha256",
        "intent_lock_sha256",
        "render_repair_contract_sha256",
    ):
        value = str(getattr(args, field) or "")
        if value and not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"--{field.replace('_', '-')} must be a 64-character SHA-256")
    failed_repair_gate_ids = [
        str(value).strip()
        for value in args.failed_repair_gate_id or []
        if str(value).strip()
    ]
    if len(failed_repair_gate_ids) != len(set(failed_repair_gate_ids)):
        raise ValueError("--failed-repair-gate-id values must be distinct")
    if failed_repair_gate_ids and not args.render_repair_contract_sha256:
        raise ValueError(
            "--failed-repair-gate-id requires --render-repair-contract-sha256"
        )
    for value in args.reference_sha256 or []:
        if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
            raise ValueError("--reference-sha256 must be a 64-character SHA-256")
    if args.image_call_count is not None and args.image_call_count < 1:
        raise ValueError("--image-call-count must be at least 1")
    optional_provenance = {
        "arm_id": args.arm_id,
        "worktree_id": args.worktree_id,
        "skill_sha256": args.skill_sha256,
        "source_ref": args.source_ref,
        "candidate_pack_version": args.candidate_pack_version,
        "authorial_request_sha256": args.authorial_request_sha256,
        "authorial_core_sha256": args.authorial_core_sha256,
        "intent_lock_sha256": args.intent_lock_sha256,
        "render_repair_contract_sha256": args.render_repair_contract_sha256,
        "failed_repair_gate_ids": failed_repair_gate_ids,
        "reference_sha256": list(args.reference_sha256 or []),
        "image_call_count": args.image_call_count,
    }
    for key, value in optional_provenance.items():
        if value not in (None, "", []):
            entry[key] = value
    if args.independent_no_cross_arm_inputs:
        entry["cross_arm_inputs_used"] = False
    return entry


def build_independent_manifest(
    entry: dict[str, object],
    args: argparse.Namespace,
) -> dict[str, object]:
    common_required_values = {
        "arm_id": args.arm_id,
        "worktree_id": args.worktree_id,
        "skill_sha256": args.skill_sha256,
        "source_ref": args.source_ref,
        "candidate_pack_version": args.candidate_pack_version,
        "image_call_count": args.image_call_count,
    }
    is_modern = args.candidate_pack_version in {"v5", "v6"}
    contract_version = (
        MODERN_INDEPENDENT_RUN_MANIFEST_VERSION
        if is_modern
        else LEGACY_INDEPENDENT_RUN_MANIFEST_VERSION
    )
    required_values = {
        **common_required_values,
        **(
            {
                "authorial_core_sha256": args.authorial_core_sha256,
                "intent_lock_sha256": args.intent_lock_sha256,
            }
            if is_modern
            else {"authorial_request_sha256": args.authorial_request_sha256}
        ),
    }
    missing = [
        key
        for key, value in required_values.items()
        if value in (None, "", [])
    ]
    if missing:
        raise ValueError(
            "--manifest requires independent-run provenance fields: "
            + ", ".join(missing)
        )
    if not args.independent_no_cross_arm_inputs:
        raise ValueError(
            "--manifest requires --independent-no-cross-arm-inputs"
        )
    image_hashes: list[dict[str, str]] = []
    for raw_path in entry.get("image_paths") or []:
        image_path = Path(str(raw_path))
        if not image_path.exists() or not image_path.is_file():
            continue
        image_hashes.append(
            {
                "path": str(image_path),
                "sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
            }
        )
    manifest: dict[str, object] = {
        "contract_version": contract_version,
        **required_values,
        # A text-only generation has no reference inputs. Keep that fact explicit
        # without treating an empty list as missing independent-run provenance.
        "reference_sha256": list(args.reference_sha256 or []),
        "cross_arm_inputs_used": False,
        "ledger_run_id": entry["run_id"],
        "pack_id": entry.get("pack_id"),
        "prompt_id": entry["prompt_id"],
        "status": entry["status"],
        "tool": entry.get("tool"),
        "image_paths": list(entry.get("image_paths") or []),
        "image_hashes": image_hashes,
    }
    for field in (
        "chosen_visual_concept_ids",
        "effective_visual_contract_sha256",
        "render_repair_contract_sha256",
        "failed_repair_gate_ids",
    ):
        if field in entry:
            manifest[field] = entry[field]
    return manifest


def append_entry(ledger: Path, entry: dict[str, object]) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and append one image-generation attempt to an NDJSON run ledger.")
    parser.add_argument("--ts", required=True, help="ISO8601 timestamp for this attempt.")
    parser.add_argument("--concept", default=None, help="Original user concept, if available.")
    parser.add_argument("--prompt-en", required=True, help="Exact prompt_en text used for the image-generation attempt.")
    parser.add_argument("--negative-en", default=None, help="Exact negative_en text used for the attempt.")
    parser.add_argument("--prompt-id", default=None, help="Expected prompt_id. If supplied, it must match --prompt-en.")
    parser.add_argument("--seed", type=int, default=None, help="Prompt generation seed, if available.")
    parser.add_argument("--attempt", type=int, required=True, help="1-based attempt number for this prompt.")
    parser.add_argument("--retry-of", default=None, help="run_id of the previous attempt, when this is a retry.")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES), help="Attempt outcome.")
    parser.add_argument("--failure-reason", default=None, help="Safety/filter/tool error detail, if any.")
    parser.add_argument("--image-path", action="append", default=[], help="Generated image path. Repeatable.")
    parser.add_argument("--tool", default=None, help="External image tool name.")
    parser.add_argument("--argv-json", default=None, help="Prompt-generation argv as a JSON string array.")
    parser.add_argument("--pack-id", default=None, help="Candidate pack id used for agent composition.")
    parser.add_argument("--chosen-candidate-ids-json", default=None, help="JSON array or slot map of candidate ids chosen by the composer.")
    parser.add_argument("--chosen-visual-concept-ids-json", default=None, help="Exact composed chosen_visual_concept_ids JSON array, including [] when the pack exposed optional visual concepts.")
    parser.add_argument("--effective-visual-contract-sha256", default=None, help="Pack-plus-composed effective visual contract SHA-256 when a visual concept was selected.")
    parser.add_argument("--composer", choices=sorted(VALID_COMPOSERS), default=None, help="Prompt composer type.")
    parser.add_argument("--audit-status", choices=sorted(VALID_AUDIT_STATUSES), default=None, help="Composed prompt audit status.")
    parser.add_argument("--augmentation-brief-json", default=None, help="Audited hybrid augmentation_brief as an inline JSON object.")
    parser.add_argument("--arm-id", default=None, help="Independent generation arm identifier.")
    parser.add_argument("--worktree-id", default=None, help="Isolated worktree or environment identifier.")
    parser.add_argument("--skill-sha256", default=None, help="SHA-256 of the frozen skill snapshot used by the arm.")
    parser.add_argument("--source-ref", default=None, help="Commit or source-snapshot identity used by the arm.")
    parser.add_argument("--candidate-pack-version", choices=sorted(VALID_CANDIDATE_PACK_VERSIONS), default=None, help="Candidate-pack version used by the arm.")
    parser.add_argument("--authorial-request-sha256", default=None, help="Canonical pre-pack authorial request SHA-256.")
    parser.add_argument("--authorial-core-sha256", default=None, help="Canonical pre-pack authorial core SHA-256 for v5/v6.")
    parser.add_argument("--intent-lock-sha256", default=None, help="Canonical requesting-user intent-lock SHA-256 for v5/v6.")
    parser.add_argument("--render-repair-contract-sha256", default=None, help="Canonical generic render-repair contract SHA-256, when enabled.")
    parser.add_argument("--failed-repair-gate-id", action="append", default=[], help="Failed generic repair hard-gate ID. Repeatable.")
    parser.add_argument("--reference-sha256", action="append", default=[], help="SHA-256 for an attached reference input. Repeatable.")
    parser.add_argument("--image-call-count", type=int, default=None, help="Total image-tool calls consumed by this arm.")
    parser.add_argument("--independent-no-cross-arm-inputs", action="store_true", help="Assert that no other arm output was used as input.")
    parser.add_argument("--manifest", type=Path, default=None, help="Write a validated independent-run manifest JSON alongside the ledger entry.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help=f"NDJSON ledger path. Defaults to {DEFAULT_LEDGER}.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        entry = build_entry(args)
        manifest = build_independent_manifest(entry, args) if args.manifest else None
        append_entry(args.ledger, entry)
        if args.manifest and manifest is not None:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"run_id": entry["run_id"], "prompt_id": entry["prompt_id"], "ledger": str(args.ledger)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
