#!/usr/bin/env python3
"""Record the single native v8 render without inheriting preflight PASS."""

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


NEGATIVE_EN = (
    "duplicate faces, awkward expression, fake-looking background, 3D render look, "
    "low resolution, distorted fingers, plastic-looking skin, unnatural pose, body "
    "distortion, cropped-off head, over-processed retouching, cartoon style, costume "
    "headband ears, clip-on tail, mascot suit, animal onesie, face-paint whiskers, "
    "anthro cartoon furry style, snout replacing the human face, detachable cosplay "
    "animal parts, stiff headband wire, fabric seam at ear base, clip-on tail strap, "
    "glued-on feathers, oversized animal ears, furry forearms, paw hands, long claws, "
    "full-body fur, animal muzzle, mascot head, clip-on ears, headband seam, "
    "symmetrical upright cat ears, both cat ears facing forward, tail unless requested, "
    "soft selfie smile, demure compliance, graceful courtly shyness, body-first framing, "
    "pin-up pose, sultry authority pose, surveillance evidence, photo wall, holding prop "
    "without direction, solo glance without handoff context, oversaturated red blush, "
    "anime blush circles, generic sparkle overlays, decorative blush circles, childlike "
    "facial morphology, minor appearance, school-age coding, oversized anime eyes, blank "
    "bored expression, listless expression, pure scowl without a warm micro-expression, "
    "unrequested heart symbols, heart-shaped pupils, heart-shaped latte art, cartoon "
    "motion lines, manga reaction marks, comic emphasis marks, readable background text, "
    "pseudo-writing, menu board lettering, chalkboard writing, signage behind the subject"
)

ACTUAL_TOOL_PROMPT = f"""Use case: identity-preserve photographic edit. Create exactly one photorealistic vertical image. Image 1 is the sole facial-identity and adult-age reference. Image 2 supplies only the scene, maid costume, pose, hands, bandage, camera, and already accepted low-intensity adult sensual tone.

Adult woman, pretty and cute: refined face, eyes, glossy hair. Image 1 reference portrait is sole identity: preserve eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging. Image 2 supplies maid costume, pose, hands, bandage, cafe, subtle adult allure only. Bandaged hand fills foreground; same adult customer's face-level near-lens eye line above. Cheek puffed, lips pursed mid-protest. Head stays aside; irises return to that eye line; private liking barely softens lower lids before she stops an almost-smile. Caught mid-bandaging, she holds scraped knuckle; one wing open. Compact cat ears, half human-ear height: near ear turns toward hand; far ear keeps another angle. Pad covers scrape; wing unfastened. Face, hands, apron, ears, bandage share one focal plane. Plain unlettered bokeh.

Avoid: {NEGATIVE_EN}"""


def main() -> None:
    pack = json.loads(
        (CASE_DIR / "candidate_pack_peer_liking_v8.json").read_text(encoding="utf-8")
    )[0]
    composed = json.loads(
        (CASE_DIR / "composed_prompt_peer_liking_v8.json").read_text(encoding="utf-8")
    )
    timestamp = "2026-08-13T04:28:12+09:00"
    prompt_id = recorder.stable_text_id(ACTUAL_TOOL_PROMPT)
    run_id = recorder.stable_text_id(f"{timestamp}|{prompt_id}|1")
    entry = {
        "ts": timestamp,
        "run_id": run_id,
        "concept": "동일 성인 인물의 츤데레 돌봄에서 부정 아래 또래 호감을 은은하게 누출",
        "prompt_id": prompt_id,
        "negative_id": recorder.stable_text_id(NEGATIVE_EN),
        "prompt_en": ACTUAL_TOOL_PROMPT,
        "negative_en": NEGATIVE_EN,
        "argv": pack["provenance"]["argv"],
        "seed": 20260812,
        "attempt": 1,
        "retry_of": None,
        "status": "success",
        "failure_reason": None,
        "image_paths": [str((CASE_DIR / "render_peer_liking_v8.png").resolve())],
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
