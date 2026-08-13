#!/usr/bin/env python3
"""Record the single native expression edit without conflating it with v6 preflight."""

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


ACTUAL_TOOL_PROMPT = """Use case: identity-preserve photographic edit.
Image 1 is the edit target and accepted tsundere baseline. Image 2 is the sole facial-identity reference.
Edit exactly one photorealistic vertical image. Preserve Image 1's adult woman, facial identity anchored to Image 2, long dark wavy hair, black-and-ivory frilled maid costume, body pose, hands, customer's hand, half-applied beige bandage, warm cafe, framing, lighting, current cat ears, sideways head angle, and current restrained adult sensual appeal.
Change only the micro-expression and eye direction: keep one cheek subtly puffed and the lips pursed in a small mid-protest pout. Keep her face angled away. Let a very brief sideways glance return toward the customer's eyes; soften only the lower eyelids slightly, and let one mouth corner almost lift before she suppresses it. The liking must be visible only as restrained concealed fondness, not an open confession.
The result must still read tsundere first: active protest and guarded posture remain, while recipient-directed affection leaks through the eyes on second reading.
Do not make her smile openly, face the viewer directly, look maternally kind, serene, nurturing, compliant, sad, bored, or genuinely angry. Do not increase sexualization. Do not alter identity, age, facial geometry, costume, pose, hands, bandage state, scene, camera, or crop. Do not add text, hearts, symbols, or decorations."""


def main() -> None:
    pack = json.loads(
        (CASE_DIR / "candidate_pack_active_denial_v6.json").read_text(encoding="utf-8")
    )[0]
    composed = json.loads(
        (CASE_DIR / "composed_prompt_concealed_affection_v6.json").read_text(
            encoding="utf-8"
        )
    )
    timestamp = "2026-08-13T01:56:26+09:00"
    prompt_id = recorder.stable_text_id(ACTUAL_TOOL_PROMPT)
    run_id = recorder.stable_text_id(f"{timestamp}|{prompt_id}|1")
    entry = {
        "ts": timestamp,
        "run_id": run_id,
        "concept": "동일 인물 츤데레 기준에서 상대를 좋아하는 본심만 은은하게 누출",
        "prompt_id": prompt_id,
        "negative_id": None,
        "prompt_en": ACTUAL_TOOL_PROMPT,
        "negative_en": None,
        "argv": pack["provenance"]["argv"],
        "seed": 20260812,
        "attempt": 1,
        "retry_of": None,
        "status": "success",
        "failure_reason": None,
        "image_paths": [str((CASE_DIR / "render_concealed_affection_v6.png").resolve())],
        "tool": "image_gen",
        "pack_id": composed["pack_id"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"],
        "composer": "agent",
        "audit_status": "not_run",
    }

    ledger = ROOT / "runs/image_runs.ndjson"
    existing_ids = {
        str(json.loads(line).get("run_id") or "")
        for line in ledger.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    if run_id not in existing_ids:
        recorder.append_entry(ledger, entry)
    print(json.dumps({"run_id": run_id, "prompt_id": prompt_id}))


if __name__ == "__main__":
    main()
