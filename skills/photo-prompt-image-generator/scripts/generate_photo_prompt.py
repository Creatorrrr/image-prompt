#!/usr/bin/env python3
"""Retrieve optional photographic candidates from an independently frozen core."""
from __future__ import annotations

import argparse
import json
import secrets
import sys
from pathlib import Path

import prompt_generator as generator
from photo_camera_evidence import CAMERA_AXES, require_camera_evidence, camera_authoring_declaration


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for argument in ("request-envelope-json", "authorial-core-json", "creative-controls-json", "embodiment-review-json"):
        parser.add_argument("--" + argument, required=True)
    parser.add_argument("--visual-intent-json")
    parser.add_argument("--require-camera-evidence", action="append", choices=CAMERA_AXES, default=[],
                        help="New authoring: verify each requester-owned camera axis has explicit frozen evidence.")
    parser.add_argument("--new-author-camera-evidence", action="store_true",
                        help="Require owner and separate direction/height declarations when camera is an open or locked dimension.")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output-file")
    parser.add_argument("--runtime-store", help="Runtime-owned generation/cache directory.")
    parser.add_argument("--source-root", help="Photo skill root; default is this installed skill.")
    parser.add_argument("--source-mode", choices=("local_current", "remote_before_retrieval"), default="local_current")
    parser.add_argument("--source-remote", help="Explicit Git remote URL for remote_before_retrieval.")
    parser.add_argument("--source-ref", default="main")
    parser.add_argument("--runtime-receipt", help="Save the private generation/pack binding separately from the public pack.")
    args = parser.parse_args(argv)
    envelope = generator.load_request_envelope_arg(args.request_envelope_json)
    controls = json.loads(Path(args.creative_controls_json).read_text(encoding="utf-8"))
    core = generator.load_authorial_core_arg(args.authorial_core_json, request_envelope=envelope,
                                            creative_control_snapshot=controls)
    require_camera_evidence(core, args.require_camera_evidence)
    lock = core["intent_lock"]
    camera_declared = "camera" in set(lock["locked_dimensions"]) | set(lock["open_dimensions"])
    # An absent camera domain permits neither an advisory assertion nor a new
    # camera choice. Preserve that valid closed scope; explicit requester-axis
    # checks above and validation of any supplied declaration still apply.
    camera_authoring_declaration(core, required=args.new_author_camera_evidence and camera_declared)
    embodiment = json.loads(Path(args.embodiment_review_json).read_text(encoding="utf-8"))
    # No candidate data is loaded until all authored inputs are validated.
    generator.photo_embodiment.build_policy(core, embodiment)
    from photo_runtime_sources import RuntimeSnapshotProvider, SKILL_ROOT
    provider = RuntimeSnapshotProvider(Path(args.source_root) if args.source_root else SKILL_ROOT,
        Path(args.runtime_store) if args.runtime_store else None,
        mode=args.source_mode, remote=args.source_remote or "", ref=args.source_ref)
    snapshot = provider.acquire()
    data = snapshot.data
    visual_intent = generator.load_visual_intent_arg(
        args.visual_intent_json, data[generator.VISUAL_OBLIGATIONS_DATA_KEY],
        data[generator.VISUAL_PROFILE_INDEX_DATA_KEY])
    pack = generator.generate_candidate_pack(
        data, core, controls, embodiment,
        seed=args.seed if args.seed is not None else secrets.randbits(63),
        visual_intent=visual_intent)
    receipt = provider.receipt(snapshot, pack)
    receipt_path = args.runtime_receipt or (str(args.output_file) + ".runtime-receipt.json" if args.output_file else None)
    if receipt_path:
        Path(receipt_path).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
