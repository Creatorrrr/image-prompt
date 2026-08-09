#!/usr/bin/env python3
"""Append one externally executed image-generation attempt to the run ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parents[1]
DEFAULT_LEDGER = PROJECT_ROOT / "runs" / "image_runs.ndjson"
VALID_STATUSES = {"success", "safety_block", "error"}
VALID_COMPOSERS = {"agent", "auto"}
VALID_AUDIT_STATUSES = {"pass", "warn", "fail", "not_run"}


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
    if args.composer:
        entry["composer"] = args.composer
    if args.audit_status:
        entry["audit_status"] = args.audit_status
    augmentation_brief = parse_augmentation_brief(args.augmentation_brief_json)
    if augmentation_brief is not None:
        entry["augmentation_brief"] = augmentation_brief
    return entry


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
    parser.add_argument("--composer", choices=sorted(VALID_COMPOSERS), default=None, help="Prompt composer type.")
    parser.add_argument("--audit-status", choices=sorted(VALID_AUDIT_STATUSES), default=None, help="Composed prompt audit status.")
    parser.add_argument("--augmentation-brief-json", default=None, help="Audited hybrid augmentation_brief as an inline JSON object.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help=f"NDJSON ledger path. Defaults to {DEFAULT_LEDGER}.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        entry = build_entry(args)
        append_entry(args.ledger, entry)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"run_id": entry["run_id"], "prompt_id": entry["prompt_id"], "ledger": str(args.ledger)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
