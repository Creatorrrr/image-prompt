#!/usr/bin/env python3
"""Record the bounded aesthetic-contract image runs without shell re-quoting."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORDER_PATH = (
    ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"
)
spec = importlib.util.spec_from_file_location("record_image_run", RECORDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {RECORDER_PATH}")
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


CASES = (
    {
        "case_id": "ko_tsundere_nekomimi_maid",
        "ts": "2026-08-12T21:38:45+09:00",
        "concept": "야하지 않은 모에한 성인 네코미미 츤데레 메이드",
        "seed": 20260812,
        "image": "render_aesthetic_contract.png",
    },
    {
        "case_id": "ko_gap_moe_guard",
        "ts": "2026-08-12T21:40:23+09:00",
        "concept": "평소 냉정한 성인 경호원이 작은 실수를 감추려는 갭모에 사진",
        "seed": 20260813,
        "image": "render_aesthetic_contract.png",
    },
    {
        "case_id": "ko_nekomimi_barista",
        "ts": "2026-08-12T21:41:52+09:00",
        "concept": "성인 네코미미 바리스타의 모에한 순간",
        "seed": 20260814,
        "image": "render_aesthetic_contract.png",
    },
)


def entry_for(case: dict[str, object]) -> dict[str, object]:
    case_dir = Path(__file__).resolve().parent / str(case["case_id"])
    request = json.loads(
        (case_dir / "render_request_aesthetic_contract.json").read_text(encoding="utf-8")
    )
    composed = json.loads(
        (case_dir / "composed_prompt_aesthetic_contract.json").read_text(encoding="utf-8")
    )
    prompt = str(request["imagegen_prompt"])
    return {
        "ts": case["ts"],
        "run_id": recorder.stable_text_id(
            f"{case['ts']}|{recorder.stable_text_id(prompt)}|1"
        ),
        "concept": case["concept"],
        "prompt_id": recorder.stable_text_id(prompt),
        "negative_id": recorder.stable_text_id(str(composed["negative_en"])),
        "prompt_en": prompt,
        "negative_en": composed["negative_en"],
        "argv": [
            "skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py",
            "--concept",
            case["concept"],
            "--selection-mode",
            "rule",
            "--candidate-pack-version",
            "v3",
            "--emit-candidate-pack",
            "--seed",
            str(case["seed"]),
        ],
        "seed": case["seed"],
        "attempt": 1,
        "retry_of": None,
        "status": "success",
        "failure_reason": None,
        "image_paths": [str((case_dir / str(case["image"])).resolve())],
        "tool": "image_gen",
        "pack_id": composed["pack_id"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"],
        "composer": "agent",
        "audit_status": "pass",
    }


def main() -> None:
    ledger = ROOT / "runs/image_runs.ndjson"
    entries = [entry_for(case) for case in CASES]
    existing_ids: set[str] = set()
    if ledger.exists():
        existing_ids = {
            str(json.loads(line).get("run_id") or "")
            for line in ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    for entry in entries:
        if str(entry["run_id"]) not in existing_ids:
            recorder.append_entry(ledger, entry)
        print(json.dumps({"run_id": entry["run_id"], "prompt_id": entry["prompt_id"]}))


if __name__ == "__main__":
    main()
