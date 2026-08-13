#!/usr/bin/env python3
"""Record the sole v9-direction render without inheriting composed preflight PASS."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = Path(__file__).resolve().parent / "ko_tsundere_nekomimi_maid"
RECORDER_PATH = ROOT / "skills/photo-prompt-image-generator/scripts/record_image_run.py"
spec = importlib.util.spec_from_file_location("record_image_run_v9", RECORDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {RECORDER_PATH}")
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


ACTUAL_AVOID = (
    "direct frontal eye contact, face pointing at camera, selfie gaze, centered viewer gaze, openly affectionate "
    "smile, symmetrical pout with no warm leak, wary or suspicious side-eye, benevolent maternal expression, "
    "enlarged or rounder eyes, shortened face, narrowed jaw, dollified facial proportions, de-aged identity, "
    "childlike morphology, giant cat ears, symmetrical upright ears, headband ears, furry limbs, paws, tail, "
    "hearts, sparkles, blush circles, captions, menu lettering, pseudo-writing, watermark, extra fingers, altered "
    "bandaging action."
)

ACTUAL_TOOL_PROMPT = """Use case: identity-preserve
Asset type: one photorealistic product-validation portrait; create exactly one edited result.

Input images:
- Image 1 is the sole identity and adult-age reference. Preserve this exact fictional adult woman's eye aperture, eye shape and spacing, brows, nose, lips, face length, cheekbones, lower-face and jaw width, skin tone, natural asymmetry, hairline, and adult maturity.
- Image 2 is the edit target and the sole baseline for scene, black-and-ivory maid costume, body, hands, unfinished bandaging action, adult customer's hand in the lower foreground, warm cafe lighting, camera distance, and the existing restrained low-intensity adult sensual appeal.

Primary request:
Keep the same adult person from Image 1 inside the scene of Image 2. Change only the head/gaze micro-geometry, tsundere micro-expression, cat-ear scale/direction, and distracting written background.

Audited scene brief:
Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait: eye aperture/shape/spacing; nose, lips; face length, lower-face/jaw width; hairline, adult age. No enlarging, rounding, shortening, narrowing. Customer's bandaged hand fills lower foreground; same adult customer's off-axis face-level eye line stays upper-left. Cheek puffed, lips pursed mid-protest. Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left. Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens. Mid-bandaging, she holds scraped knuckle; one wing open. Human-ear-scale near ear turns toward hand; far ear keeps different angle. Pad covers scrape; wing unfastened. Face, hands, maid apron, bandage share one focal plane. Restrained allure. Unlettered bokeh.

Critical expression and gaze:
- Her head and nose are clearly turned about 25–35 degrees toward image-right in a natural three-quarter pose; the nose axis must miss the lens.
- The same adult recipient's face-level eye line is just upper-left of the lens. Only her irises make a small oblique return toward that off-axis eye line. Do not look into the lens and do not center both pupils toward the viewer.
- Keep a cute active protest: subtly puffed cheek and pursed lips caught mid-denial.
- At second glance only, soften the lower lids slightly and let exactly one mouth corner begin a tiny lift before she visibly suppresses and flattens it. This must read as private peer-level liking leaking through denial, not an open smile, generic warmth, wary side-eye, or maternal kindness.
- She continues carefully bandaging the scraped knuckle; the caring hands contradict her mouth.

Nekomimi:
Use small living feline ears organically rooted in the hairline, each no taller than her visible human ear. Leave one human ear partly visible for scale. The nearer cat ear turns toward the lower bandaging hand; the farther ear retains a clearly different outward angle. No oversized ears.

Invariants:
Preserve Image 1's facial proportions even if a different face would look conventionally cuter. Achieve pretty-and-cute appeal through grooming, light, and micro-expression, never eye enlargement, face shortening, jaw narrowing, smoothing, or de-aging. Preserve Image 2's costume coverage, body proportions, hands, bandage, cafe intimacy, framing, and appropriate restrained adult sensual level. Plain warm unlettered cafe bokeh; no readable signs or pseudo-writing.

Avoid:
direct frontal eye contact, face pointing at camera, selfie gaze, centered viewer gaze, openly affectionate smile, symmetrical pout with no warm leak, wary or suspicious side-eye, benevolent maternal expression, enlarged or rounder eyes, shortened face, narrowed jaw, dollified facial proportions, de-aged identity, childlike morphology, giant cat ears, symmetrical upright ears, headband ears, furry limbs, paws, tail, hearts, sparkles, blush circles, captions, menu lettering, pseudo-writing, watermark, extra fingers, altered bandaging action."""


def main() -> None:
    pack = json.loads(
        (CASE_DIR / "candidate_pack_peer_liking_v9.json").read_text(encoding="utf-8")
    )[0]
    composed = json.loads(
        (CASE_DIR / "composed_prompt_peer_liking_v9.json").read_text(encoding="utf-8")
    )
    timestamp = "2026-08-13T05:34:59+09:00"
    prompt_id = recorder.stable_text_id(ACTUAL_TOOL_PROMPT)
    run_id = recorder.stable_text_id(f"{timestamp}|{prompt_id}|1")
    entry = {
        "ts": timestamp,
        "run_id": run_id,
        "concept": "동일 성인 인물의 츤데레 돌봄에서 정면응시 없이 또래 호감이 은은하게 새는 v9 방향",
        "prompt_id": prompt_id,
        "negative_id": recorder.stable_text_id(ACTUAL_AVOID),
        "prompt_en": ACTUAL_TOOL_PROMPT,
        "negative_en": ACTUAL_AVOID,
        "argv": pack["provenance"]["argv"],
        "seed": 20260812,
        "attempt": 1,
        "retry_of": None,
        "status": "success",
        "failure_reason": None,
        "image_paths": [str((CASE_DIR / "render_peer_liking_v9.png").resolve())],
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
    print(
        json.dumps(
            {
                "run_id": run_id,
                "prompt_id": prompt_id,
                "negative_matches_pack": ACTUAL_AVOID == pack["negative_en"],
            }
        )
    )


if __name__ == "__main__":
    main()
