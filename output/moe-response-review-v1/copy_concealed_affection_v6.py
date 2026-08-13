#!/usr/bin/env python3
"""Copy the single native v6 concealed-affection edit into the review pack."""

from pathlib import Path
import shutil


SOURCE = Path(
    "/Users/chasoik/.codex/generated_images/019ff4f4-789c-7ce1-b272-55a7a764973f/"
    "exec-5832b18c-0e1d-4899-83a5-45a944764a57.png"
)
TARGET = Path(__file__).resolve().parent / (
    "ko_tsundere_nekomimi_maid/render_concealed_affection_v6.png"
)

if TARGET.exists():
    raise SystemExit(f"refusing to overwrite existing artifact: {TARGET}")
if not SOURCE.is_file():
    raise SystemExit(f"native image is missing: {SOURCE}")

TARGET.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(SOURCE, TARGET)
print(TARGET)
