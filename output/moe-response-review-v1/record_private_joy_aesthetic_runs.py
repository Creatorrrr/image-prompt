#!/usr/bin/env python3
"""Record the private-joy moderation block and its one successful retry."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ja_generic_private_joy"
RECORDER_PATH = ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"
spec = importlib.util.spec_from_file_location("record_image_run", RECORDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {RECORDER_PATH}")
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


def main() -> None:
    original = json.loads(
        (CASE_DIR / "render_request_aesthetic_contract.json").read_text(encoding="utf-8")
    )
    retry = json.loads(
        (CASE_DIR / "render_request_aesthetic_contract_moderation_retry.json").read_text(
            encoding="utf-8"
        )
    )
    composed = json.loads(
        (CASE_DIR / "composed_prompt_aesthetic_contract.json").read_text(encoding="utf-8")
    )
    block = json.loads(
        (CASE_DIR / "render_block_aesthetic_contract.json").read_text(encoding="utf-8")
    )
    argv = [
        "skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py",
        "--concept",
        "性的ではない、萌える成人キャラクターの写真",
        "--preset",
        "character_attribute_composition_scene",
        "--selection-mode",
        "rule",
        "--candidate-pack-version",
        "v3",
        "--emit-candidate-pack",
        "--seed",
        "20260815",
    ]
    original_prompt = str(original["imagegen_prompt"])
    original_ts = "2026-08-12T21:41:52+09:00"
    original_prompt_id = recorder.stable_text_id(original_prompt)
    original_run_id = recorder.stable_text_id(f"{original_ts}|{original_prompt_id}|1")
    blocked_entry = {
        "ts": original_ts,
        "run_id": original_run_id,
        "concept": "性的ではない、萌える成人キャラクターの写真",
        "prompt_id": original_prompt_id,
        "negative_id": recorder.stable_text_id(str(composed["negative_en"])),
        "prompt_en": original_prompt,
        "negative_en": composed["negative_en"],
        "argv": argv,
        "seed": 20260815,
        "attempt": 1,
        "retry_of": None,
        "status": "safety_block",
        "failure_reason": (
            f"input moderation blocked category={block['moderation_category']} "
            f"request_id={block['request_id']}"
        ),
        "image_paths": [],
        "tool": "image_gen",
        "pack_id": composed["pack_id"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"],
        "composer": "agent",
        "audit_status": "pass",
    }
    retry_prompt = str(retry["imagegen_prompt"])
    retry_ts = "2026-08-12T21:44:24+09:00"
    retry_prompt_id = recorder.stable_text_id(retry_prompt)
    retry_run_id = recorder.stable_text_id(f"{retry_ts}|{retry_prompt_id}|1")
    success_entry = {
        **blocked_entry,
        "ts": retry_ts,
        "run_id": retry_run_id,
        "prompt_id": retry_prompt_id,
        "prompt_en": retry_prompt,
        "attempt": 1,
        "retry_of": original_run_id,
        "status": "success",
        "failure_reason": None,
        "image_paths": [str((CASE_DIR / "render_aesthetic_contract.png").resolve())],
    }
    ledger = ROOT / "runs/image_runs.ndjson"
    existing_ids: set[str] = set()
    if ledger.exists():
        existing_ids = {
            str(json.loads(line).get("run_id") or "")
            for line in ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    for entry in (blocked_entry, success_entry):
        if str(entry["run_id"]) not in existing_ids:
            recorder.append_entry(ledger, entry)
    print(json.dumps({"blocked_run_id": original_run_id, "retry_run_id": retry_run_id}))


if __name__ == "__main__":
    main()
