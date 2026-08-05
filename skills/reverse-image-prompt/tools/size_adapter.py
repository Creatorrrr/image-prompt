#!/usr/bin/env python3
"""Recommend a valid GPT Image 2 size near a source frame."""

from __future__ import annotations

import argparse
import json
import math
import sys

STEP = 16
MAX_EDGE = 3840
MIN_PIXELS = 655_360
MAX_PIXELS = 8_294_400
MAX_RATIO = 3.0


def is_valid_size(width: int, height: int) -> bool:
    if width <= 0 or height <= 0:
        return False
    pixels = width * height
    return (
        width % STEP == 0
        and height % STEP == 0
        and max(width, height) <= MAX_EDGE
        and max(width, height) / min(width, height) <= MAX_RATIO
        and MIN_PIXELS <= pixels <= MAX_PIXELS
    )


def recommend_size(source_width: int, source_height: int) -> tuple[int, int]:
    if source_width <= 0 or source_height <= 0:
        raise ValueError("source dimensions must be positive integers")
    if is_valid_size(source_width, source_height):
        return source_width, source_height

    source_ratio = source_width / source_height
    best: tuple[float, float, int, int] | None = None

    for width in range(STEP, MAX_EDGE + STEP, STEP):
        min_height = max(STEP, math.ceil(MIN_PIXELS / width / STEP) * STEP)
        max_height = min(MAX_EDGE, math.floor(MAX_PIXELS / width / STEP) * STEP)
        for height in range(min_height, max_height + STEP, STEP):
            if not is_valid_size(width, height):
                continue
            ratio_error = abs(math.log((width / height) / source_ratio))
            dimension_error = math.hypot(
                (width - source_width) / source_width,
                (height - source_height) / source_height,
            )
            score = ratio_error * 8.0 + dimension_error
            candidate = (score, ratio_error, width, height)
            if best is None or candidate < best:
                best = candidate

    if best is None:
        raise ValueError("no valid GPT Image 2 size could be found")
    return best[2], best[3]


def result_payload(source_width: int, source_height: int) -> dict[str, object]:
    target_width, target_height = recommend_size(source_width, source_height)
    source_ratio = source_width / source_height
    target_ratio = target_width / target_height
    return {
        "model": "gpt-image-2",
        "source_size": f"{source_width}x{source_height}",
        "target_size": f"{target_width}x{target_height}",
        "source_ratio": round(source_ratio, 6),
        "target_ratio": round(target_ratio, 6),
        "relative_ratio_error": round(abs(target_ratio / source_ratio - 1.0), 6),
        "adjusted": (source_width, source_height) != (target_width, target_height),
        "valid": is_valid_size(target_width, target_height),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    args = parser.parse_args(argv)
    try:
        payload = result_payload(args.width, args.height)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
