#!/usr/bin/env python3
"""Copy the single native v8 peer-liking render into the review pack."""

from pathlib import Path
import shutil


SOURCE = Path(
    "/Users/chasoik/.codex/generated_images/019ff4f4-789c-7ce1-b272-55a7a764973f/"
    "exec-9e92b1a8-f31f-4663-ac85-ca43d89e9bc7.png"
)
TARGET = Path(__file__).resolve().parent / (
    "ko_tsundere_nekomimi_maid/render_peer_liking_v8.png"
)

if TARGET.exists():
    raise SystemExit(f"refusing to overwrite existing artifact: {TARGET}")
if not SOURCE.is_file():
    raise SystemExit(f"native image is missing: {SOURCE}")

TARGET.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(SOURCE, TARGET)
print(TARGET)
