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
VALID_BINDING_STATUSES = {
    "explicitly-applied",
    "auto",
    "unsupported",
    "unbound",
}


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


def _relative_ratio_error(
    width: int, height: int, reference_width: int, reference_height: int
) -> float:
    return round(abs((width / height) / (reference_width / reference_height) - 1.0), 6)


def result_payload(
    source_width: int,
    source_height: int,
    *,
    binding_status: str | None = None,
    delivered_width: int | None = None,
    delivered_height: int | None = None,
) -> dict[str, object]:
    target_width, target_height = recommend_size(source_width, source_height)
    source_ratio = source_width / source_height
    target_ratio = target_width / target_height
    payload: dict[str, object] = {
        "model": "gpt-image-2",
        "source_size": f"{source_width}x{source_height}",
        "target_size": f"{target_width}x{target_height}",
        "source_ratio": round(source_ratio, 6),
        "target_ratio": round(target_ratio, 6),
        "relative_ratio_error": round(abs(target_ratio / source_ratio - 1.0), 6),
        "adjusted": (source_width, source_height) != (target_width, target_height),
        "valid": is_valid_size(target_width, target_height),
    }

    has_delivered_width = delivered_width is not None
    has_delivered_height = delivered_height is not None
    if has_delivered_width != has_delivered_height:
        raise ValueError("delivered width and height must be supplied together")
    if binding_status is None:
        if has_delivered_width:
            raise ValueError("a binding status is required for delivered-size evidence")
        return payload
    if binding_status not in VALID_BINDING_STATUSES:
        raise ValueError(
            "binding status must be one of " + ", ".join(sorted(VALID_BINDING_STATUSES))
        )

    exact_target_match: bool | None = None
    source_delivery_error: float | None = None
    target_delivery_error: float | None = None
    delivered_size: str | None = None
    if delivered_width is not None and delivered_height is not None:
        if delivered_width <= 0 or delivered_height <= 0:
            raise ValueError("delivered dimensions must be positive integers")
        delivered_size = f"{delivered_width}x{delivered_height}"
        exact_target_match = (delivered_width, delivered_height) == (
            target_width,
            target_height,
        )
        source_delivery_error = _relative_ratio_error(
            delivered_width,
            delivered_height,
            source_width,
            source_height,
        )
        target_delivery_error = _relative_ratio_error(
            delivered_width,
            delivered_height,
            target_width,
            target_height,
        )

    frame_delivery_status = "unscored"
    if binding_status == "explicitly-applied" and exact_target_match is not None:
        frame_delivery_status = "pass" if exact_target_match else "fail"

    tool_support = {
        "explicitly-applied": "supported",
        "auto": "supported",
        "unsupported": "unsupported",
        "unbound": "unverified",
    }[binding_status]
    requested_setting: str | None = None
    if binding_status == "explicitly-applied":
        requested_setting = str(payload["target_size"])
    elif binding_status == "auto":
        requested_setting = "auto"

    payload["size_binding"] = {
        "binding_status": binding_status,
        "tool_support": tool_support,
        "requested_setting": requested_setting,
        "delivered_size": delivered_size,
        "exact_target_match": exact_target_match,
        "source_to_delivery_relative_ratio_error": source_delivery_error,
        "target_to_delivery_relative_ratio_error": target_delivery_error,
        "frame_delivery_status": frame_delivery_status,
    }
    return payload


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument(
        "--binding-status",
        choices=sorted(VALID_BINDING_STATUSES),
        help="how the target size was exposed to the generator",
    )
    parser.add_argument("--delivered-width", type=int)
    parser.add_argument("--delivered-height", type=int)
    args = parser.parse_args(argv)
    try:
        payload = result_payload(
            args.width,
            args.height,
            binding_status=args.binding_status,
            delivered_width=args.delivered_width,
            delivered_height=args.delivered_height,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
