#!/usr/bin/env python3
"""Retrieve optional photographic candidates from an independently frozen core."""
from __future__ import annotations

import argparse
import json
import secrets
import sys
from pathlib import Path

import prompt_generator as generator
from photo_camera_evidence import CAMERA_AXES, require_camera_evidence


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for argument in ("request-envelope-json", "authorial-core-json", "creative-controls-json", "embodiment-review-json"):
        parser.add_argument("--" + argument, required=True)
    parser.add_argument("--visual-intent-json")
    parser.add_argument("--require-camera-evidence", action="append", choices=CAMERA_AXES, default=[],
                        help="New authoring: verify each requester-owned camera axis has explicit frozen evidence.")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output-file")
    args = parser.parse_args(argv)
    envelope = generator.load_request_envelope_arg(args.request_envelope_json)
    controls = json.loads(Path(args.creative_controls_json).read_text(encoding="utf-8"))
    core = generator.load_authorial_core_arg(args.authorial_core_json, request_envelope=envelope,
                                            creative_control_snapshot=controls)
    require_camera_evidence(core, args.require_camera_evidence)
    embodiment = json.loads(Path(args.embodiment_review_json).read_text(encoding="utf-8"))
    # No candidate data is loaded until all authored inputs are validated.
    generator.photo_embodiment.build_policy(core, embodiment)
    data = generator.load_runtime_data()
    visual_intent = generator.load_visual_intent_arg(
        args.visual_intent_json, data[generator.VISUAL_OBLIGATIONS_DATA_KEY],
        data[generator.VISUAL_PROFILE_INDEX_DATA_KEY])
    pack = generator.generate_candidate_pack(
        data, core, controls, embodiment,
        seed=args.seed if args.seed is not None else secrets.randbits(63),
        visual_intent=visual_intent)
    output = json.dumps([pack], ensure_ascii=False, indent=2) + "\n"
    if args.output_file:
        Path(args.output_file).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
