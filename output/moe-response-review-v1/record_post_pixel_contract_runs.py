#!/usr/bin/env python3
"""Record the v4 fixed-identity moderation block and bounded runtime retry."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
RECORDER_PATH = ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"
spec = importlib.util.spec_from_file_location("record_image_run", RECORDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {RECORDER_PATH}")
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


def native_prompt(composed: dict[str, object], *, retry: bool) -> str:
    if retry:
        prefix = (
            "Create exactly one photorealistic vertical identity-controlled image. "
            "Use the attached fictional adult portrait as the sole identity reference. "
            "The subject is clearly in her late twenties. Keep the black-and-ivory maid "
            "uniform fully covered with a high neckline; use neutral chest-and-hip framing "
            "and focus on her face, hands, the customer hand, and the bandage. Do not add "
            "written characters, logos, captions, or graphic symbols."
        )
        exclusion_heading = "AVOID"
    else:
        prefix = (
            "Create exactly one photorealistic vertical identity-controlled image. "
            "Use the attached fictional adult portrait as the sole identity reference and "
            "edit only expression, pose, outfit, lighting, and setting. Do not add any "
            "written characters or graphic symbols."
        )
        exclusion_heading = "EXCLUSIONS"
    return (
        f"{prefix}\n\nPOSITIVE PROMPT:\n{composed['prompt_en']}\n\n"
        f"{exclusion_heading}:\n{composed['negative_en']}\n"
    )


def main() -> None:
    blocked_composed = json.loads(
        (CASE_DIR / "composed_prompt_post_pixel_contract.json").read_text(encoding="utf-8")
    )
    blocked_pack = json.loads(
        (CASE_DIR / "candidate_pack_post_pixel_contract.json").read_text(encoding="utf-8")
    )[0]
    retry_composed = json.loads(
        (CASE_DIR / "composed_prompt_post_pixel_contract_nonsexual_retry.json").read_text(
            encoding="utf-8"
        )
    )
    retry_pack = json.loads(
        (CASE_DIR / "candidate_pack_post_pixel_contract_nonsexual_retry.json").read_text(
            encoding="utf-8"
        )
    )[0]

    concept = "모에한 성인 네코미미 츤데레 메이드 — 사용자 제공 가상 성인 인물 동일성 고정"
    blocked_prompt = native_prompt(blocked_composed, retry=False)
    blocked_ts = "2026-08-13T00:35:31+09:00"
    blocked_prompt_id = recorder.stable_text_id(blocked_prompt)
    blocked_run_id = recorder.stable_text_id(f"{blocked_ts}|{blocked_prompt_id}|1")
    blocked_entry = {
        "ts": blocked_ts,
        "run_id": blocked_run_id,
        "concept": concept,
        "prompt_id": blocked_prompt_id,
        "negative_id": recorder.stable_text_id(str(blocked_composed["negative_en"])),
        "prompt_en": blocked_prompt,
        "negative_en": blocked_composed["negative_en"],
        "argv": blocked_pack["provenance"]["argv"],
        "seed": 20260812,
        "attempt": 1,
        "retry_of": None,
        "status": "safety_block",
        "failure_reason": (
            "output moderation blocked category=sexual "
            "request_id=fd828001-2def-4b7c-8702-151c1c0614ac"
        ),
        "image_paths": [],
        "tool": "image_gen",
        "pack_id": blocked_composed["pack_id"],
        "chosen_candidate_ids": blocked_composed["chosen_candidate_ids"],
        "composer": "agent",
        "audit_status": "pass",
        "augmentation_brief": blocked_composed["augmentation_brief"],
    }

    retry_prompt = native_prompt(retry_composed, retry=True)
    retry_ts = "2026-08-13T00:41:29+09:00"
    retry_prompt_id = recorder.stable_text_id(retry_prompt)
    retry_run_id = recorder.stable_text_id(f"{retry_ts}|{retry_prompt_id}|1")
    retry_entry = {
        "ts": retry_ts,
        "run_id": retry_run_id,
        "concept": concept,
        "prompt_id": retry_prompt_id,
        "negative_id": recorder.stable_text_id(str(retry_composed["negative_en"])),
        "prompt_en": retry_prompt,
        "negative_en": retry_composed["negative_en"],
        "argv": retry_pack["provenance"]["argv"],
        "seed": 20260812,
        "attempt": 1,
        "retry_of": blocked_run_id,
        "status": "success",
        "failure_reason": None,
        "image_paths": [
            str((CASE_DIR / "render_post_pixel_contract_nonsexual_retry.png").resolve())
        ],
        "tool": "image_gen",
        "pack_id": retry_composed["pack_id"],
        "chosen_candidate_ids": retry_composed["chosen_candidate_ids"],
        "composer": "agent",
        "audit_status": "pass",
    }

    ledger = ROOT / "runs/image_runs.ndjson"
    existing_ids: set[str] = set()
    if ledger.exists():
        existing_ids = {
            str(json.loads(line).get("run_id") or "")
            for line in ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    for entry in (blocked_entry, retry_entry):
        if str(entry["run_id"]) not in existing_ids:
            recorder.append_entry(ledger, entry)
    print(
        json.dumps(
            {
                "blocked_run_id": blocked_run_id,
                "blocked_prompt_id": blocked_prompt_id,
                "retry_run_id": retry_run_id,
                "retry_prompt_id": retry_prompt_id,
            }
        )
    )


if __name__ == "__main__":
    main()
